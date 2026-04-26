"""Postiz scheduler integration.

Cloud base URL: https://api.postiz.com/public/v1
Auth header:    Authorization: <api-key>          (NO "Bearer" prefix)
Rate limit:     30 requests/hour (Cloud)

Modes:
  verify(): GET /integrations — proves the key works without creating any post.
  push():   POST /posts        — schedules approved drafts (full shape NYI).

Without env vars set, every call returns a graceful no-op so the CLI never
fails because of missing credentials.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request


def _configured() -> bool:
    return bool(os.environ.get("POSTIZ_API_URL") and os.environ.get("POSTIZ_API_KEY"))


def _api_base() -> str:
    """Return the full API base ending in /public/v1 — robust to either input form.

    Taylor may have stored either:
      POSTIZ_API_URL=https://api.postiz.com
      POSTIZ_API_URL=https://api.postiz.com/public/v1
      POSTIZ_API_URL=https://my-self-hosted.app/public/v1
    """
    raw = (os.environ.get("POSTIZ_API_URL") or "").rstrip("/")
    if not raw:
        return ""
    if raw.endswith("/public/v1"):
        return raw
    return raw + "/public/v1"


def _request(method: str, path: str, body: dict | None = None,
             timeout: int = 15) -> tuple[int, dict | str]:
    """Low-level Postiz API call. Returns (status_code, parsed_json_or_text)."""
    api_key = os.environ.get("POSTIZ_API_KEY")
    if not api_key:
        return 0, "POSTIZ_API_KEY not set"
    url = _api_base() + path
    data = None
    headers = {
        "Authorization": api_key,   # NO "Bearer" prefix per Postiz docs
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = resp.read().decode("utf-8") if resp.length != 0 else ""
            try:
                parsed = json.loads(payload) if payload else {}
            except json.JSONDecodeError:
                parsed = payload
            return resp.status, parsed
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        try:
            parsed = json.loads(body_text)
        except json.JSONDecodeError:
            parsed = body_text
        return e.code, parsed
    except Exception as e:
        return -1, f"{type(e).__name__}: {e}"


def _channel_summary(item: dict) -> dict:
    """Extract platform + display name from a Postiz integration record."""
    return {
        "platform": (item.get("providerIdentifier")
                     or item.get("identifier")
                     or item.get("provider")
                     or "unknown"),
        "name": item.get("name") or item.get("display") or "(unnamed)",
        "id": item.get("id"),
    }


def verify() -> dict:
    """Lightweight auth + connectivity check.

    Calls GET /integrations and reports back. Doesn't create or modify anything.
    """
    if not _configured():
        return {
            "ok": False,
            "mode": "postiz.verify",
            "reason": "POSTIZ_API_URL / POSTIZ_API_KEY not set — paste them into ~/shared-keys.env",
        }
    status, data = _request("GET", "/integrations")
    if status == 200:
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get("data") or data.get("integrations") or []
        else:
            items = []
        channels = [_channel_summary(i) for i in items if isinstance(i, dict)]
        return {
            "ok": True,
            "mode": "postiz.verify",
            "base_url": _api_base(),
            "status": status,
            "channels_connected": len(channels),
            "channels": channels,
        }
    return {
        "ok": False,
        "mode": "postiz.verify",
        "base_url": _api_base(),
        "status": status,
        "error": data,
    }


# Maps SMM platform slug → Postiz `__type` settings discriminator + provider id we expect from /integrations
_PLATFORM_MAP = {
    "tiktok":                     {"__type": "tiktok", "providers": ("tiktok",)},
    "instagram_caption":          {"__type": "instagram", "providers": ("instagram", "instagram-standalone")},
    "instagram_reel":             {"__type": "instagram", "providers": ("instagram", "instagram-standalone")},
    "facebook_personal":          {"__type": "facebook", "providers": ("facebook",)},
    "facebook_business":          {"__type": "facebook", "providers": ("facebook",)},
    "linkedin":                   {"__type": "linkedin", "providers": ("linkedin", "linkedin-page")},
    "youtube_long":               {"__type": "youtube", "providers": ("youtube",)},
    "youtube_short":              {"__type": "youtube", "providers": ("youtube",)},
    "youtube_community":          {"__type": "youtube", "providers": ("youtube",)},
    "gmb":                        {"__type": "gmb", "providers": ("gmb",)},
    "biggerpockets":              {"__type": "x", "providers": ("x",)},  # not native; falls through
    "reddit":                     {"__type": "reddit", "providers": ("reddit",)},
    "x_twitter":                  {"__type": "x", "providers": ("x",)},
    "blog":                       {"__type": "wordpress", "providers": ("wordpress", "medium", "devto")},
}

# Per-platform required settings beyond __type. Keep these conservative defaults;
# Taylor can override per-draft later. Sources: Postiz public-api/providers/<platform>.md
_PLATFORM_DEFAULT_SETTINGS = {
    "x":         {"who_can_reply_post": "everyone", "community": ""},
    "tiktok":    {"privacy_level": "PUBLIC_TO_EVERYONE", "duet": False, "stitch": False,
                  "comment": True, "brand_organic_toggle": False, "brand_content_toggle": False,
                  "auto_add_music": False, "title": ""},
    "instagram": {"post_type": "post"},   # post | reel | story (default post; Reels need video)
    "linkedin":  {},
    "facebook":  {},
    "youtube":   {"title": "", "type": "public", "tags": []},
    "gmb":       {},
    "reddit":    [],   # Reddit shape is array, not object — handled in builder
    "wordpress": {},
}


def list_integrations() -> list[dict]:
    """Cached-friendly: returns list of {id, platform, name} for connected channels."""
    if not _configured():
        return []
    status, data = _request("GET", "/integrations")
    if status != 200:
        return []
    items = data if isinstance(data, list) else (data.get("data") or data.get("integrations") or [])
    return [_channel_summary(i) for i in items if isinstance(i, dict)]


def _resolve_integration_id(platform: str, integrations: list[dict]) -> str | None:
    """Find the Postiz integration ID matching an SMM platform slug."""
    spec = _PLATFORM_MAP.get(platform)
    if not spec:
        return None
    for i in integrations:
        if i["platform"] in spec["providers"]:
            return i["id"]
    return None


def _build_post_body(draft, integration_id: str, post_type: str = "schedule",
                    when_iso: str | None = None, short_link: bool = False) -> dict:
    """Build the POST /posts JSON body for a single draft."""
    spec = _PLATFORM_MAP[draft.platform]
    type_key = spec["__type"]
    settings = dict(_PLATFORM_DEFAULT_SETTINGS.get(type_key, {}))
    settings["__type"] = type_key
    body_text = (draft.body or "").strip()
    if draft.cta and draft.cta not in body_text:
        body_text = f"{body_text}\n\n{draft.cta}".strip()
    if draft.hashtags:
        tags = " ".join(h if h.startswith("#") else f"#{h}" for h in draft.hashtags)
        if tags not in body_text:
            body_text = f"{body_text}\n\n{tags}".strip()
    return {
        "type": post_type,
        "date": when_iso or "1970-01-01T00:00:00.000Z",  # placeholder for type=draft
        "shortLink": short_link,
        "tags": [],
        "posts": [
            {
                "integration": {"id": integration_id},
                "value": [{"content": body_text, "image": []}],
                "settings": settings,
            }
        ],
    }


def push(platform: str | None = None, dry_run: bool = True,
         post_type: str = "schedule", when_iso: str | None = None) -> dict:
    """Push approved drafts to Postiz.

    Args:
      platform:   Filter SMM drafts to this platform (None = all approved)
      dry_run:    Default True. Returns auth check + bodies that WOULD be sent.
      post_type:  "schedule" (default) | "now". `--when` required.
                  NOTE: "draft" mode is NOT supported via this path — Postiz's
                  type=draft expects an empty posts array (creates a placeholder
                  slot, not a populated draft). Confirmed silently no-ops with
                  content. Use `type=schedule` with a future date for "soft draft"
                  behavior — Taylor can cancel from Postiz UI before publish time.
      when_iso:   ISO 8601 UTC string for scheduled posts. Required.

    Honors AGENTS.md hard prohibition: "No live API calls without a --live flag."
    Default mode is dry_run; CLI must explicitly flip dry_run=False.
    """
    if not _configured():
        return {
            "ok": False,
            "mode": "postiz",
            "reason": "POSTIZ_API_URL / POSTIZ_API_KEY not set — use CSV export or set env vars",
        }

    if post_type not in ("schedule", "now"):
        return {"ok": False, "mode": "postiz.push",
                "reason": f"invalid post_type {post_type!r}; must be 'schedule' or 'now' (Postiz type=draft is broken with content — use schedule with future date instead)"}
    if post_type == "schedule" and not when_iso:
        return {"ok": False, "mode": "postiz.push",
                "reason": "post_type=schedule requires when_iso (ISO 8601 UTC) — pass --when '+24h' for safe delayed scheduling"}

    # Pull approved drafts via the existing layer
    from smm.drafts import list_drafts
    from smm.compliance import has_hard_violation
    drafts = list_drafts(status="approved", platform=platform, limit=10_000)
    if not drafts:
        return {"ok": True, "mode": f"postiz.push.{post_type}",
                "pushed": 0, "skipped": 0, "errors": [], "results": [],
                "note": "no approved drafts matched"}

    integrations = list_integrations()
    if not integrations:
        return {"ok": False, "mode": "postiz.push",
                "reason": "no integrations connected on Postiz side — connect channels in dashboard first"}

    results = []
    pushed = 0
    skipped = 0
    errors = []
    for d in drafts:
        # Refuse to push drafts with HARD compliance violations even if force-approved
        if has_hard_violation(d.compliance_flags):
            skipped += 1
            results.append({"draft_id": d.id, "platform": d.platform,
                            "status": "skipped", "reason": "HARD compliance flag"})
            continue
        if d.platform not in _PLATFORM_MAP:
            skipped += 1
            results.append({"draft_id": d.id, "platform": d.platform,
                            "status": "skipped",
                            "reason": f"platform {d.platform!r} not in Postiz map"})
            continue
        integration_id = _resolve_integration_id(d.platform, integrations)
        if not integration_id:
            skipped += 1
            results.append({"draft_id": d.id, "platform": d.platform,
                            "status": "skipped",
                            "reason": f"no Postiz integration matches platform {d.platform!r} — connect that channel"})
            continue

        body = _build_post_body(d, integration_id, post_type=post_type, when_iso=when_iso)
        if dry_run:
            results.append({"draft_id": d.id, "platform": d.platform,
                            "status": "would_push", "integration_id": integration_id,
                            "body_preview": body})
            continue

        status, resp = _request("POST", "/posts", body=body)
        if 200 <= status < 300:
            pushed += 1
            results.append({"draft_id": d.id, "platform": d.platform,
                            "status": "pushed", "postiz_response": resp})
            # Mark draft as scheduled in our DB so we don't double-push
            from smm.drafts import set_status
            set_status(d.id, "scheduled" if post_type == "schedule" else "approved",
                       note=f"pushed to Postiz as {post_type}", actor="cli.postiz")
        else:
            errors.append({"draft_id": d.id, "status_code": status, "response": resp})
            results.append({"draft_id": d.id, "platform": d.platform,
                            "status": "error", "code": status, "response": resp})

    return {
        "ok": True if not errors else False,
        "mode": f"postiz.push.{post_type}{'.dry_run' if dry_run else ''}",
        "pushed": pushed,
        "skipped": skipped,
        "errors": errors,
        "results": results,
        "rate_limit_note": "Postiz Cloud: 30 requests/hour — verify counts as 1, push counts as 1 per draft",
    }
