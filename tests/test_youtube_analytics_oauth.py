import ctypes
import importlib.util
import io
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.parse import parse_qs


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "youtube_analytics_oauth", SCRIPTS / "youtube_analytics_oauth.py"
)
oauth = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(oauth)


class _Response(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class _MemoryKeychain:
    def __init__(self, raw=None, *, failure=None):
        self.raw = raw
        self.failure = failure
        self.stored = None

    def store_secret(self, service, account, secret):
        if self.failure:
            raise RuntimeError(self.failure)
        self.stored = (service, account, secret)
        self.raw = secret

    def load_secret(self, service, account):
        if self.failure:
            raise RuntimeError(self.failure)
        return self.raw


class _FakeSecurityFramework:
    def __init__(self, stored=None):
        self.stored = stored
        self.buffer = None
        self.add_calls = 0
        self.modify_calls = 0
        self.free_calls = 0

    @staticmethod
    def _set_void_pointer(target, value):
        ctypes.cast(target, ctypes.POINTER(ctypes.c_void_p)).contents.value = value

    def SecKeychainFindGenericPassword(
        self,
        _keychain,
        _service_length,
        _service,
        _account_length,
        _account,
        password_length,
        password_data,
        item_ref,
    ):
        if self.stored is None:
            return oauth.ERR_SEC_ITEM_NOT_FOUND
        if item_ref is not None:
            self._set_void_pointer(item_ref, 0xCAFE)
        if password_length is not None:
            ctypes.cast(
                password_length, ctypes.POINTER(ctypes.c_uint32)
            ).contents.value = len(self.stored)
        if password_data is not None:
            self.buffer = ctypes.create_string_buffer(self.stored)
            self._set_void_pointer(password_data, ctypes.addressof(self.buffer))
        return oauth.ERR_SEC_SUCCESS

    def SecKeychainAddGenericPassword(
        self,
        _keychain,
        _service_length,
        _service,
        _account_length,
        _account,
        secret_length,
        secret_data,
        _item_ref,
    ):
        self.add_calls += 1
        self.stored = ctypes.string_at(secret_data, secret_length)
        return oauth.ERR_SEC_SUCCESS

    def SecKeychainItemModifyAttributesAndData(
        self,
        _item_ref,
        _attributes,
        secret_length,
        secret_data,
    ):
        self.modify_calls += 1
        self.stored = ctypes.string_at(secret_data, secret_length)
        return oauth.ERR_SEC_SUCCESS

    def SecKeychainItemFreeContent(self, _attributes, _data):
        self.free_calls += 1
        return oauth.ERR_SEC_SUCCESS


class _FakeCoreFoundation:
    def __init__(self):
        self.released = []

    def CFRelease(self, item_ref):
        self.released.append(item_ref.value)


def _native_backend(security):
    backend = object.__new__(oauth._MacOSKeychain)
    backend._security = security
    backend._core_foundation = _FakeCoreFoundation()
    return backend


def _credential_payload():
    return {
        "version": 1,
        "client_id": "fixture-client",
        "client_secret": "fixture-secret",
        "refresh_token": "fixture-refresh",
        "token_uri": oauth.TOKEN_URI,
        "scopes": list(oauth.REQUIRED_SCOPES),
    }


def test_scope_set_is_exactly_two_read_only_scopes():
    assert set(oauth.REQUIRED_SCOPES) == {
        "https://www.googleapis.com/auth/youtube.readonly",
        "https://www.googleapis.com/auth/yt-analytics.readonly",
    }


def test_keychain_store_uses_framework_backend_without_process_output(capsys):
    backend = _MemoryKeychain()
    payload = _credential_payload()

    oauth.keychain_store(payload, backend=backend)

    service, account, raw = backend.stored
    assert service == oauth.KEYCHAIN_SERVICE
    assert account == oauth.KEYCHAIN_ACCOUNT
    assert json.loads(raw.decode("utf-8")) == payload
    assert not hasattr(oauth, "subprocess")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_keychain_load_round_trips_framework_bytes():
    payload = _credential_payload()
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

    assert oauth.keychain_load(backend=_MemoryKeychain(raw)) == payload


def test_native_keychain_backend_adds_exact_secret_bytes():
    security = _FakeSecurityFramework()
    backend = _native_backend(security)
    secret = b'{"refresh_token":"native-secret"}'

    backend.store_secret("fixture-service", "fixture-account", secret)

    assert security.stored == secret
    assert security.add_calls == 1
    assert security.modify_calls == 0


def test_native_keychain_backend_updates_and_releases_existing_item():
    security = _FakeSecurityFramework(stored=b"old-secret")
    backend = _native_backend(security)

    backend.store_secret("fixture-service", "fixture-account", b"new-secret")

    assert security.stored == b"new-secret"
    assert security.add_calls == 0
    assert security.modify_calls == 1
    assert backend._core_foundation.released == [0xCAFE]


def test_native_keychain_backend_loads_exact_bytes_and_frees_native_buffer():
    security = _FakeSecurityFramework(stored=b'{"refresh_token":"native-secret"}')
    backend = _native_backend(security)

    assert backend.load_secret("fixture-service", "fixture-account") == security.stored
    assert security.free_calls == 1


def test_keychain_store_failure_has_no_secret_exception_context(capsys):
    backend = _MemoryKeychain(failure="fixture-refresh fixture-secret")
    try:
        oauth.keychain_store(_credential_payload(), backend=backend)
    except oauth.YouTubeOAuthError as exc:
        error = str(exc)
        assert exc.__context__ is None
    else:
        raise AssertionError("Keychain failure was not surfaced")

    captured = capsys.readouterr()
    disclosed = error + captured.out + captured.err
    assert "fixture-refresh" not in disclosed
    assert "fixture-secret" not in disclosed


def test_keychain_decode_failure_has_no_secret_exception_context():
    backend = _MemoryKeychain(b"\xfffixture-refresh")
    try:
        oauth.keychain_load(backend=backend)
    except oauth.YouTubeOAuthError as exc:
        assert exc.__context__ is None
        assert "fixture-refresh" not in str(exc)
    else:
        raise AssertionError("Invalid Keychain bytes were accepted")


def test_connect_storage_requires_exact_validated_keychain_round_trip():
    payload = _credential_payload()
    with (
        patch.object(oauth, "keychain_store") as store,
        patch.object(oauth, "keychain_load", return_value=dict(payload)),
    ):
        oauth._store_and_verify_keychain_payload(payload)

    store.assert_called_once_with(payload)


def test_connect_storage_rejects_silent_keychain_data_loss():
    payload = _credential_payload()
    with (
        patch.object(oauth, "keychain_store"),
        patch.object(oauth, "keychain_load", return_value=None),
    ):
        try:
            oauth._store_and_verify_keychain_payload(payload)
        except oauth.YouTubeOAuthError as exc:
            error = str(exc)
        else:
            raise AssertionError("Missing Keychain round-trip was accepted")

    assert "fixture-refresh" not in error
    assert "not readable" in error


def test_connect_storage_rejects_mismatched_keychain_payload():
    payload = _credential_payload()
    mismatched = dict(payload)
    mismatched["refresh_token"] = "different-refresh"
    with (
        patch.object(oauth, "keychain_store"),
        patch.object(oauth, "keychain_load", return_value=mismatched),
    ):
        try:
            oauth._store_and_verify_keychain_payload(payload)
        except oauth.YouTubeOAuthError as exc:
            error = str(exc)
        else:
            raise AssertionError("Mismatched Keychain payload was accepted")

    assert "fixture-refresh" not in error
    assert "different-refresh" not in error
    assert "did not round-trip" in error


def test_validate_rejects_any_scope_beyond_read_only_set():
    payload = _credential_payload()
    payload["scopes"].append("https://www.googleapis.com/auth/youtube.upload")
    try:
        oauth.validate_stored_credential(payload)
    except oauth.YouTubeOAuthError as exc:
        assert "beyond" in str(exc)
    else:
        raise AssertionError("overprivileged credential was accepted")


def test_refresh_access_token_uses_post_and_returns_token_only_in_memory():
    captured = {}

    def opener(request, timeout):
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["body"] = parse_qs(request.data.decode("utf-8"))
        captured["timeout"] = timeout
        return _Response(json.dumps({"access_token": "short-lived"}).encode())

    token = oauth.refresh_access_token(_credential_payload(), opener=opener)

    assert token == "short-lived"
    assert captured["url"] == oauth.TOKEN_URI
    assert captured["method"] == "POST"
    assert captured["body"]["grant_type"] == ["refresh_token"]
    assert captured["body"]["refresh_token"] == ["fixture-refresh"]


def test_verify_checks_expected_channel_and_private_metric_columns():
    def opener(request, timeout):
        if "youtube/v3/channels" in request.full_url:
            data = {"items": [{"id": "expected-channel"}]}
        elif "youtubeanalytics.googleapis.com" in request.full_url:
            data = {
                "columnHeaders": [
                    {"name": "engagedViews"},
                    {"name": "estimatedMinutesWatched"},
                    {"name": "averageViewDuration"},
                    {"name": "averageViewPercentage"},
                ],
                "rows": [[10, 20, 30, 40]],
            }
        else:
            raise AssertionError(request.full_url)
        return _Response(json.dumps(data).encode())

    result = oauth.verify_access_token(
        "fixture-access",
        expected_channel_id="expected-channel",
        opener=opener,
    )

    assert result["channel_match"] is True
    assert result["analytics_row_count"] == 1
    assert len(result["analytics_columns"]) == 4


def test_live_guard_blocks_connect_before_any_google_request():
    assert oauth.main([
        "connect",
        "--client-secrets",
        "/tmp/client.json",
        "--expected-channel-id",
        "fixture-channel",
    ]) == 2


def test_status_does_not_print_credential_values(capsys):
    with patch.object(oauth, "keychain_load", return_value=_credential_payload()):
        assert oauth.main(["status"]) == 0

    output = capsys.readouterr().out
    assert "fixture-client" not in output
    assert "fixture-secret" not in output
    assert "fixture-refresh" not in output
    assert "read-only" in output
