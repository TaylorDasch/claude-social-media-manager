#!/usr/bin/env python3
"""Least-privilege OAuth support for Taylor's YouTube Analytics pulls.

The refresh credential is stored in macOS Keychain, not in this repository,
``shared-keys.env``, command-line arguments, or a plaintext token file. The
scheduled pull exchanges it for a short-lived access token in memory.

Initial connection and live verification are explicit network actions:

    python3 scripts/youtube_analytics_oauth.py connect \
      --client-secrets ~/.config/taylor/youtube-analytics/client-secret.json \
      --expected-channel-id "$YOUTUBE_CHANNEL_ID" --live
    python3 scripts/youtube_analytics_oauth.py status
    python3 scripts/youtube_analytics_oauth.py verify \
      --expected-channel-id "$YOUTUBE_CHANNEL_ID" --live

The connection requests only ``youtube.readonly`` and
``yt-analytics.readonly``. It cannot upload, edit, publish, delete, or access
revenue data.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Optional


YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YT_ANALYTICS_READONLY_SCOPE = (
    "https://www.googleapis.com/auth/yt-analytics.readonly"
)
REQUIRED_SCOPES = (YOUTUBE_READONLY_SCOPE, YT_ANALYTICS_READONLY_SCOPE)
TOKEN_URI = "https://oauth2.googleapis.com/token"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
KEYCHAIN_SERVICE = "com.taylordasch.youtube-analytics.readonly"
KEYCHAIN_ACCOUNT = "dealswithdasch@gmail.com"
SECURITY_FRAMEWORK_PATH = (
    "/System/Library/Frameworks/Security.framework/Security"
)
CORE_FOUNDATION_FRAMEWORK_PATH = (
    "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"
)
ERR_SEC_SUCCESS = 0
ERR_SEC_DUPLICATE_ITEM = -25299
ERR_SEC_ITEM_NOT_FOUND = -25300
USER_AGENT = "taylor-youtube-analytics/1.0"


class YouTubeOAuthError(RuntimeError):
    """Safe-to-display OAuth/configuration error with no secret material."""


class _KeychainBackendError(RuntimeError):
    """Internal Keychain failure. Never surface its details to callers."""


class _MacOSKeychain:
    """Minimal Security.framework bridge with no subprocess or terminal prompt."""

    def __init__(self) -> None:
        self._security = ctypes.CDLL(SECURITY_FRAMEWORK_PATH)
        self._core_foundation = ctypes.CDLL(CORE_FOUNDATION_FRAMEWORK_PATH)
        self._configure_symbols()

    def _configure_symbols(self) -> None:
        uint32_pointer = ctypes.POINTER(ctypes.c_uint32)
        void_pointer_pointer = ctypes.POINTER(ctypes.c_void_p)

        self._security.SecKeychainFindGenericPassword.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_char_p,
            ctypes.c_uint32,
            ctypes.c_char_p,
            uint32_pointer,
            void_pointer_pointer,
            void_pointer_pointer,
        ]
        self._security.SecKeychainFindGenericPassword.restype = ctypes.c_int32
        self._security.SecKeychainAddGenericPassword.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_char_p,
            ctypes.c_uint32,
            ctypes.c_char_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            void_pointer_pointer,
        ]
        self._security.SecKeychainAddGenericPassword.restype = ctypes.c_int32
        self._security.SecKeychainItemModifyAttributesAndData.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
        ]
        self._security.SecKeychainItemModifyAttributesAndData.restype = ctypes.c_int32
        self._security.SecKeychainItemFreeContent.argtypes = [
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]
        self._security.SecKeychainItemFreeContent.restype = ctypes.c_int32
        self._core_foundation.CFRelease.argtypes = [ctypes.c_void_p]
        self._core_foundation.CFRelease.restype = None

    @staticmethod
    def _identifier(value: str) -> bytes:
        encoded = value.encode("utf-8")
        if not encoded or b"\x00" in encoded:
            raise _KeychainBackendError("Invalid Keychain identifier.")
        return encoded

    def _find_item(self, service: bytes, account: bytes) -> tuple[int, ctypes.c_void_p]:
        item_ref = ctypes.c_void_p()
        status = self._security.SecKeychainFindGenericPassword(
            None,
            len(service),
            service,
            len(account),
            account,
            None,
            None,
            ctypes.byref(item_ref),
        )
        return int(status), item_ref

    def _modify_item(
        self,
        item_ref: ctypes.c_void_p,
        secret_pointer: ctypes.c_void_p,
        secret_length: int,
    ) -> None:
        try:
            status = self._security.SecKeychainItemModifyAttributesAndData(
                item_ref,
                None,
                secret_length,
                secret_pointer,
            )
            if status != ERR_SEC_SUCCESS:
                raise _KeychainBackendError("Could not update Keychain item.")
        finally:
            if item_ref.value:
                self._core_foundation.CFRelease(item_ref)

    def store_secret(self, service_name: str, account_name: str, secret: bytes) -> None:
        if not secret:
            raise _KeychainBackendError("Refusing to store an empty credential.")
        service = self._identifier(service_name)
        account = self._identifier(account_name)
        secret_buffer = ctypes.create_string_buffer(secret)
        secret_pointer = ctypes.cast(secret_buffer, ctypes.c_void_p)

        status, item_ref = self._find_item(service, account)
        if status == ERR_SEC_SUCCESS:
            if not item_ref.value:
                raise _KeychainBackendError("Keychain returned an empty item reference.")
            self._modify_item(item_ref, secret_pointer, len(secret))
            return
        if status != ERR_SEC_ITEM_NOT_FOUND:
            raise _KeychainBackendError("Could not query Keychain item.")

        add_status = self._security.SecKeychainAddGenericPassword(
            None,
            len(service),
            service,
            len(account),
            account,
            len(secret),
            secret_pointer,
            None,
        )
        if add_status == ERR_SEC_DUPLICATE_ITEM:
            # Handle a narrow find/add race without moving the secret to argv.
            find_status, item_ref = self._find_item(service, account)
            if find_status != ERR_SEC_SUCCESS or not item_ref.value:
                raise _KeychainBackendError("Could not recover Keychain item.")
            self._modify_item(item_ref, secret_pointer, len(secret))
            return
        if add_status != ERR_SEC_SUCCESS:
            raise _KeychainBackendError("Could not add Keychain item.")

    def load_secret(self, service_name: str, account_name: str) -> Optional[bytes]:
        service = self._identifier(service_name)
        account = self._identifier(account_name)
        password_length = ctypes.c_uint32()
        password_data = ctypes.c_void_p()
        status = self._security.SecKeychainFindGenericPassword(
            None,
            len(service),
            service,
            len(account),
            account,
            ctypes.byref(password_length),
            ctypes.byref(password_data),
            None,
        )
        if status == ERR_SEC_ITEM_NOT_FOUND:
            return None
        if status != ERR_SEC_SUCCESS:
            raise _KeychainBackendError("Could not read Keychain item.")
        if password_length.value and not password_data.value:
            raise _KeychainBackendError("Keychain returned invalid password data.")

        try:
            secret = (
                ctypes.string_at(password_data, password_length.value)
                if password_length.value
                else b""
            )
        finally:
            if password_data.value:
                free_status = self._security.SecKeychainItemFreeContent(
                    None,
                    password_data,
                )
                if free_status != ERR_SEC_SUCCESS:
                    raise _KeychainBackendError("Could not release Keychain data.")
        return secret


_KEYCHAIN_BACKEND: Optional[_MacOSKeychain] = None


def _service_name() -> str:
    return (
        os.environ.get("YOUTUBE_ANALYTICS_KEYCHAIN_SERVICE", "").strip()
        or KEYCHAIN_SERVICE
    )


def _account_name() -> str:
    return (
        os.environ.get("YOUTUBE_ANALYTICS_KEYCHAIN_ACCOUNT", "").strip()
        or KEYCHAIN_ACCOUNT
    )


def _keychain_backend() -> _MacOSKeychain:
    global _KEYCHAIN_BACKEND
    if _KEYCHAIN_BACKEND is None:
        _KEYCHAIN_BACKEND = _MacOSKeychain()
    return _KEYCHAIN_BACKEND


def keychain_store(payload: dict, *, backend=None) -> None:
    """Store the refresh credential through Security.framework, never argv."""
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode(
        "utf-8"
    )
    failed = False
    try:
        active_backend = backend if backend is not None else _keychain_backend()
        active_backend.store_secret(
            _service_name(),
            _account_name(),
            encoded,
        )
    except Exception:
        failed = True
    if failed:
        raise YouTubeOAuthError(
            "Could not store the YouTube refresh credential in macOS Keychain."
        )


def keychain_load(*, backend=None) -> Optional[dict]:
    """Load the Keychain payload, returning None when no item exists."""
    failed = False
    raw_payload = None
    try:
        active_backend = backend if backend is not None else _keychain_backend()
        raw_payload = active_backend.load_secret(
            _service_name(),
            _account_name(),
        )
    except Exception:
        failed = True
    if failed:
        raise YouTubeOAuthError(
            "Could not read the YouTube refresh credential from macOS Keychain."
        )
    if raw_payload is None:
        return None
    decode_failed = False
    payload = None
    try:
        payload = json.loads(raw_payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError):
        decode_failed = True
    if decode_failed:
        raise YouTubeOAuthError(
            "The YouTube Keychain item is not valid credential JSON."
        )
    if not isinstance(payload, dict):
        raise YouTubeOAuthError(
            "The YouTube Keychain item has an unexpected credential format."
        )
    return payload


def validate_stored_credential(payload: dict) -> dict:
    """Validate required fields and least-privilege scopes."""
    required_fields = ("client_id", "client_secret", "refresh_token", "token_uri")
    missing = [name for name in required_fields if not payload.get(name)]
    if missing:
        raise YouTubeOAuthError(
            "The YouTube Keychain item is missing required credential fields."
        )

    scopes = payload.get("scopes")
    if not isinstance(scopes, list):
        raise YouTubeOAuthError(
            "The YouTube Keychain item does not contain a scope list."
        )
    scope_set = {str(scope) for scope in scopes}
    if not set(REQUIRED_SCOPES).issubset(scope_set):
        raise YouTubeOAuthError(
            "The YouTube credential is missing required read-only scopes."
        )
    if scope_set != set(REQUIRED_SCOPES):
        raise YouTubeOAuthError(
            "The YouTube credential contains scopes beyond the approved read-only set."
        )
    if payload.get("token_uri") != TOKEN_URI:
        raise YouTubeOAuthError("The YouTube credential uses an unexpected token endpoint.")
    return payload


def _read_json_response(response) -> dict:
    try:
        parsed = json.load(response)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise YouTubeOAuthError("Google returned an invalid JSON response.") from exc
    if not isinstance(parsed, dict):
        raise YouTubeOAuthError("Google returned an unexpected response format.")
    return parsed


def refresh_access_token(
    payload: Optional[dict] = None,
    *,
    opener: Callable = urllib.request.urlopen,
) -> str:
    """Exchange the Keychain refresh credential for an in-memory access token."""
    credential = validate_stored_credential(payload or keychain_load() or {})
    request_body = urllib.parse.urlencode({
        "client_id": credential["client_id"],
        "client_secret": credential["client_secret"],
        "refresh_token": credential["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")
    request = urllib.request.Request(
        TOKEN_URI,
        data=request_body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    try:
        with opener(request, timeout=20) as response:
            data = _read_json_response(response)
    except urllib.error.HTTPError as exc:
        if exc.code == 400:
            raise YouTubeOAuthError(
                "Google rejected the saved YouTube grant. Reconnect the read-only access."
            ) from exc
        raise YouTubeOAuthError(
            f"Google token refresh failed with HTTP {exc.code}."
        ) from exc
    except YouTubeOAuthError:
        raise
    except Exception as exc:
        raise YouTubeOAuthError("Could not refresh YouTube access.") from exc

    access_token = data.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise YouTubeOAuthError("Google did not return a YouTube access token.")
    return access_token


def get_access_token() -> str:
    """Public entrypoint used by the scheduled analytics pull."""
    return refresh_access_token()


def _api_get_json(
    url: str,
    *,
    access_token: str,
    opener: Callable = urllib.request.urlopen,
) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with opener(request, timeout=20) as response:
            return _read_json_response(response)
    except urllib.error.HTTPError as exc:
        raise YouTubeOAuthError(
            f"YouTube verification failed with HTTP {exc.code}."
        ) from exc
    except YouTubeOAuthError:
        raise
    except Exception as exc:
        raise YouTubeOAuthError("Could not verify YouTube access.") from exc


def verify_access_token(
    access_token: str,
    *,
    expected_channel_id: str,
    opener: Callable = urllib.request.urlopen,
) -> dict:
    """Prove channel ownership and a minimal private Analytics query."""
    expected_channel_id = expected_channel_id.strip()
    if not expected_channel_id:
        raise YouTubeOAuthError("An expected YouTube channel ID is required.")

    channels_query = urllib.parse.urlencode({
        "part": "id",
        "mine": "true",
        "maxResults": "50",
    })
    channels = _api_get_json(
        f"https://www.googleapis.com/youtube/v3/channels?{channels_query}",
        access_token=access_token,
        opener=opener,
    )
    owned_ids = {
        str(item.get("id", ""))
        for item in channels.get("items", [])
        if isinstance(item, dict) and item.get("id")
    }
    if expected_channel_id not in owned_ids:
        raise YouTubeOAuthError(
            "The authorized Google account does not expose the expected YouTube channel."
        )

    end_date = datetime.now(timezone.utc).date() - timedelta(days=1)
    start_date = end_date - timedelta(days=27)
    analytics_query = urllib.parse.urlencode({
        "ids": f"channel=={expected_channel_id}",
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "metrics": (
            "engagedViews,estimatedMinutesWatched,averageViewDuration,"
            "averageViewPercentage"
        ),
    })
    analytics = _api_get_json(
        f"https://youtubeanalytics.googleapis.com/v2/reports?{analytics_query}",
        access_token=access_token,
        opener=opener,
    )
    columns = [
        str(column.get("name", ""))
        for column in analytics.get("columnHeaders", [])
        if isinstance(column, dict) and column.get("name")
    ]
    expected_metrics = {
        "engagedViews",
        "estimatedMinutesWatched",
        "averageViewDuration",
        "averageViewPercentage",
    }
    if not expected_metrics.issubset(set(columns)):
        raise YouTubeOAuthError(
            "YouTube access worked, but the required private metrics were not returned."
        )
    return {
        "channel_match": True,
        "analytics_columns": sorted(expected_metrics),
        "analytics_row_count": len(analytics.get("rows", [])),
    }


def load_client_secrets(path: Path) -> dict:
    """Load a Google-downloaded Desktop app client file."""
    expanded = path.expanduser()
    try:
        file_mode = expanded.stat().st_mode & 0o777
        parent_mode = expanded.parent.stat().st_mode & 0o777
        if file_mode & 0o077 or parent_mode & 0o077:
            raise YouTubeOAuthError(
                "OAuth client file and its directory must be owner-only (0600/0700)."
            )
        config = json.loads(expanded.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise YouTubeOAuthError(f"OAuth client file not found: {path.expanduser()}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise YouTubeOAuthError("Could not read the OAuth desktop client file.") from exc
    installed = config.get("installed") if isinstance(config, dict) else None
    if not isinstance(installed, dict):
        raise YouTubeOAuthError("OAuth client must be a Google Desktop app client.")
    for field in ("client_id", "client_secret"):
        if not installed.get(field):
            raise YouTubeOAuthError("OAuth desktop client is missing required fields.")
    if installed.get("auth_uri") != AUTH_URI:
        raise YouTubeOAuthError("OAuth desktop client uses an unexpected auth endpoint.")
    token_uri = installed.get("token_uri", TOKEN_URI)
    if token_uri != TOKEN_URI:
        raise YouTubeOAuthError("OAuth desktop client uses an unexpected token endpoint.")
    return config


def _stored_payload(client_config: dict, credentials) -> dict:
    installed = client_config["installed"]
    refresh_token = getattr(credentials, "refresh_token", None)
    if not refresh_token:
        raise YouTubeOAuthError(
            "Google did not issue offline access. Reconnect with consent enabled."
        )

    granted = getattr(credentials, "granted_scopes", None)
    if granted and not set(REQUIRED_SCOPES).issubset(set(granted)):
        raise YouTubeOAuthError(
            "Google did not grant both required read-only YouTube scopes."
        )
    return validate_stored_credential({
        "version": 1,
        "client_id": installed["client_id"],
        "client_secret": installed["client_secret"],
        "refresh_token": refresh_token,
        "token_uri": TOKEN_URI,
        "scopes": list(REQUIRED_SCOPES),
        "created_at": datetime.now(timezone.utc).isoformat(),
    })


def _store_and_verify_keychain_payload(payload: dict) -> None:
    """Persist a credential only if the exact validated payload round-trips."""
    expected = validate_stored_credential(payload)
    keychain_store(expected)
    loaded = keychain_load()
    if loaded is None:
        raise YouTubeOAuthError(
            "The YouTube credential was not readable after Keychain storage."
        )
    actual = validate_stored_credential(loaded)
    if actual != expected:
        raise YouTubeOAuthError(
            "The YouTube credential did not round-trip through macOS Keychain."
        )


def connect(*, client_secrets: Path, expected_channel_id: str) -> dict:
    """Run the loopback+PKCE Desktop flow and store only after verification."""
    client_config = load_client_secrets(client_secrets)
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError as exc:
        raise YouTubeOAuthError(
            "google-auth-oauthlib is required for the one-time connection."
        ) from exc

    flow = InstalledAppFlow.from_client_config(
        client_config,
        scopes=list(REQUIRED_SCOPES),
        autogenerate_code_verifier=True,
    )
    credentials = flow.run_local_server(
        host="127.0.0.1",
        port=0,
        open_browser=False,
        authorization_prompt_message="AUTHORIZATION_URL={url}",
        success_message=(
            "YouTube Analytics read-only access is connected. "
            "You can close this tab."
        ),
        timeout_seconds=600,
        access_type="offline",
        prompt="consent",
        login_hint=_account_name(),
    )
    verification = verify_access_token(
        credentials.token,
        expected_channel_id=expected_channel_id,
    )
    _store_and_verify_keychain_payload(_stored_payload(client_config, credentials))
    return verification


def _require_live(args: argparse.Namespace, action: str) -> None:
    if not args.live:
        raise YouTubeOAuthError(
            f"{action} makes live Google requests; re-run with --live."
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser(
        "status", help="Check local Keychain configuration without network access."
    )
    status_parser.set_defaults(live=False)

    connect_parser = subparsers.add_parser(
        "connect", help="Create a fresh read-only Google OAuth grant."
    )
    connect_parser.add_argument("--client-secrets", type=Path, required=True)
    connect_parser.add_argument("--expected-channel-id", required=True)
    connect_parser.add_argument("--live", action="store_true")

    verify_parser = subparsers.add_parser(
        "verify", help="Refresh and verify the stored grant against YouTube."
    )
    verify_parser.add_argument("--expected-channel-id", required=True)
    verify_parser.add_argument("--live", action="store_true")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "status":
            payload = keychain_load()
            if payload is None:
                print("YouTube Analytics: not connected")
                return 1
            validate_stored_credential(payload)
            print("YouTube Analytics: read-only Keychain credential is configured")
            print("Scopes: youtube.readonly + yt-analytics.readonly")
            return 0

        if args.command == "connect":
            _require_live(args, "Connecting YouTube Analytics")
            result = connect(
                client_secrets=args.client_secrets,
                expected_channel_id=args.expected_channel_id,
            )
            print("YouTube Analytics: connected and verified read-only")
            print(f"Private metrics verified: {len(result['analytics_columns'])}")
            return 0

        if args.command == "verify":
            _require_live(args, "Verifying YouTube Analytics")
            result = verify_access_token(
                refresh_access_token(),
                expected_channel_id=args.expected_channel_id,
            )
            print("YouTube Analytics: stored read-only grant is valid")
            print(f"Private metrics verified: {len(result['analytics_columns'])}")
            return 0
    except YouTubeOAuthError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
