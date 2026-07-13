"""Two-pass semantic ranking with strict JSON/schema validation."""

from __future__ import annotations

import json
import hashlib
import os
import re
from dataclasses import dataclass
from http.client import HTTPException
from typing import Any, Callable, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen as stdlib_urlopen

from .errors import ModelOutputError, ShortsFactoryError
from .policy import MIN_TOPIC_PURITY


DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-6"
DEFAULT_OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
LANES = {"bsw_buyer", "military", "relocator", "first_time_buyer", "investor", "general"}
CLAIM_TYPES = {
    "monetary",
    "market_stat",
    "commute_time",
    "school_quality",
    "safety",
    "legal_financial",
    "other",
}
CLAIM_SEVERITIES = {"review", "verify", "high_risk"}
SCORE_LIMITS = {
    "hook_strength": 30,
    "angle_quality": 30,
    "audience_fit": 15,
    "arc_payoff": 20,
    "cta_strength": 5,
}
RANKING_INPUT_SCHEMA_VERSION = "shorts-ranking-input/v1"
RANKING_RUBRIC_VERSION = "taylor-shorts-rubric/v4-strict-one-subject"


class ModelClient(Protocol):
    def complete(
        self,
        *,
        model: str,
        system: str,
        user: str,
        max_tokens: int,
    ) -> str: ...


class ModelProviderError(ShortsFactoryError):
    """An API/provider failure with sanitized, inspectable metadata."""

    def __init__(
        self,
        provider: str,
        message: str,
        *,
        status_code: int | None = None,
        error_code: str | None = None,
        error_type: str | None = None,
    ) -> None:
        self.provider = provider
        self.status_code = status_code
        self.error_code = error_code
        self.error_type = error_type
        details = [f"{provider} request failed"]
        if status_code is not None:
            details.append(f"HTTP {status_code}")
        if error_type:
            details.append(error_type)
        if error_code and error_code != error_type:
            details.append(error_code)
        if message:
            details.append(message)
        super().__init__(": ".join(details))


def _sanitize_provider_text(value: Any, *, secrets: tuple[str, ...] = ()) -> str:
    """Keep errors actionable without ever reflecting bearer credentials."""
    text = str(value or "").replace("\r", " ").replace("\n", " ")
    for secret in secrets:
        if secret:
            text = text.replace(secret, "[REDACTED]")
    text = re.sub(
        r"(?i)\bbearer\s+[a-z0-9._~+/=-]+",
        "Bearer [REDACTED]",
        text,
    )
    text = re.sub(r"\bsk-[A-Za-z0-9_-]{12,}\b", "[REDACTED]", text)
    return " ".join(text.split())[:600]


def _provider_error_fields(payload: Any) -> tuple[str, str | None, str | None]:
    if not isinstance(payload, dict):
        return "", None, None
    error = payload.get("error", payload)
    if not isinstance(error, dict):
        return "", None, None
    message = error.get("message")
    code = error.get("code")
    error_type = error.get("type")
    return (
        str(message) if message is not None else "",
        str(code) if code is not None else None,
        str(error_type) if error_type is not None else None,
    )


class OpenAIModelClient:
    """Minimal stdlib Chat Completions client constrained to JSON objects.

    The constructor owns the OpenAI model. The ``model`` argument accepted by
    :meth:`complete` exists for ``ModelClient`` compatibility, but cannot replace
    this provider-specific model with a Claude model during automatic fallback.
    """

    def __init__(
        self,
        *,
        api_key: str | None = None,
        model: str = DEFAULT_OPENAI_MODEL,
        endpoint: str = OPENAI_CHAT_COMPLETIONS_URL,
        timeout: float = 90.0,
        urlopen: Callable[..., Any] | None = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ShortsFactoryError(
                "OPENAI_API_KEY is not set. Export it before using the OpenAI fallback."
            )
        self.model = model.strip()
        if not self.model:
            raise ValueError("OpenAI model must be non-empty")
        self.endpoint = endpoint
        self.timeout = timeout
        self._urlopen = urlopen or stdlib_urlopen
        self.provider_used: str | None = None
        self.model_used: str | None = None

    def complete(
        self,
        *,
        model: str,
        system: str,
        user: str,
        max_tokens: int,
    ) -> str:
        del model  # Provider model is intentionally configured on this client.
        if max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        self.provider_used = "openai"
        self.model_used = self.model
        body = json.dumps(
            {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "max_completion_tokens": max_tokens,
                "response_format": {"type": "json_object"},
            },
            ensure_ascii=False,
        ).encode("utf-8")
        request = Request(
            self.endpoint,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        try:
            with self._urlopen(request, timeout=self.timeout) as response:
                raw = response.read(4 * 1024 * 1024)
        except HTTPError as exc:
            try:
                error_raw = exc.read(256 * 1024)
                payload = json.loads(error_raw.decode("utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                payload = {}
            message, code, error_type = _provider_error_fields(payload)
            safe_message = _sanitize_provider_text(
                message or "The API rejected the request.",
                secrets=(self.api_key,),
            )
            raise ModelProviderError(
                "OpenAI",
                safe_message,
                status_code=getattr(exc, "code", None),
                error_code=_sanitize_provider_text(code, secrets=(self.api_key,))
                if code
                else None,
                error_type=_sanitize_provider_text(
                    error_type, secrets=(self.api_key,)
                )
                if error_type
                else None,
            ) from exc
        except (URLError, TimeoutError, OSError, HTTPException) as exc:
            reason = getattr(exc, "reason", None)
            safe_reason = _sanitize_provider_text(
                reason or type(exc).__name__,
                secrets=(self.api_key,),
            )
            raise ModelProviderError(
                "OpenAI", f"network transport error ({safe_reason})"
            ) from exc

        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ModelProviderError(
                "OpenAI", "API response was not valid JSON"
            ) from exc
        if not isinstance(payload, dict):
            raise ModelProviderError("OpenAI", "API response was not a JSON object")
        if isinstance(payload.get("error"), dict):
            message, code, error_type = _provider_error_fields(payload)
            raise ModelProviderError(
                "OpenAI",
                _sanitize_provider_text(
                    message or "API returned an error object",
                    secrets=(self.api_key,),
                ),
                error_code=_sanitize_provider_text(code, secrets=(self.api_key,))
                if code
                else None,
                error_type=_sanitize_provider_text(
                    error_type, secrets=(self.api_key,)
                )
                if error_type
                else None,
            )
        choices = payload.get("choices")
        if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
            raise ModelOutputError("OpenAI response contained no completion choice")
        choice = choices[0]
        if choice.get("finish_reason") == "length":
            raise ModelOutputError("OpenAI response was truncated at the token limit")
        message = choice.get("message")
        if not isinstance(message, dict):
            raise ModelOutputError("OpenAI completion choice contained no message")
        content = message.get("content")
        if isinstance(content, list):
            content = "".join(
                str(part.get("text", ""))
                for part in content
                if isinstance(part, dict) and part.get("type") in {"text", "output_text"}
            )
        if not isinstance(content, str) or not content.strip():
            refusal = _sanitize_provider_text(
                message.get("refusal") or "response contained no text content"
            )
            raise ModelOutputError(f"OpenAI {refusal}")
        return content


def _exception_evidence(exc: Exception) -> str:
    """Collect provider metadata for classification, never for display."""
    values: list[Any] = [str(exc)]
    for name in ("body", "error", "code", "type", "message"):
        value = getattr(exc, name, None)
        if value is not None:
            values.append(value)
    response = getattr(exc, "response", None)
    if response is not None:
        values.extend(
            value
            for value in (
                getattr(response, "status_code", None),
                getattr(response, "text", None),
            )
            if value is not None
        )
        try:
            values.append(response.json())
        except Exception:
            pass
    return " ".join(str(value) for value in values).lower()


def _is_billing_or_quota_error(exc: Exception) -> bool:
    """Match credit exhaustion, not transient rate limits or auth failures."""
    status_code = getattr(exc, "status_code", None)
    if status_code is None:
        response = getattr(exc, "response", None)
        status_code = getattr(response, "status_code", None)
    if status_code == 402:
        return True
    evidence = _exception_evidence(exc)
    exact_markers = (
        "insufficient_quota",
        "insufficient quota",
        "credit balance is too low",
        "credit balance too low",
        "billing_hard_limit_reached",
        "billing hard limit",
        "billing limit reached",
        "billing_error",
        "payment_required",
        "payment required",
        "purchase credits",
        "plans & billing",
        "monthly spend limit",
        "spending limit reached",
        "exceeded your current quota",
    )
    return any(marker in evidence for marker in exact_markers)


class AutoModelClient:
    """Use Anthropic first, then permanently fail over on billing exhaustion."""

    def __init__(
        self,
        *,
        anthropic_client: ModelClient | None = None,
        openai_client: ModelClient | None = None,
        anthropic_api_key: str | None = None,
        openai_api_key: str | None = None,
        anthropic_model: str | None = None,
        openai_model: str = DEFAULT_OPENAI_MODEL,
    ) -> None:
        self._anthropic_client = anthropic_client
        self._openai_client = openai_client
        self._anthropic_api_key = anthropic_api_key
        self._openai_api_key = openai_api_key
        self.anthropic_model = anthropic_model
        self.openai_model = openai_model
        self.provider_used: str | None = None
        self.model_used: str | None = None
        anthropic_available = bool(
            anthropic_client
            or anthropic_api_key
            or os.environ.get("ANTHROPIC_API_KEY")
        )
        openai_available = bool(
            openai_client
            or openai_api_key
            or os.environ.get("OPENAI_API_KEY")
        )
        # A configured OpenAI account is a valid failover when Anthropic is not
        # configured at all. Do not require a dummy Anthropic credential merely
        # to reach the already-supported secondary provider.
        self._use_openai = not anthropic_available and openai_available
        self.fallback_triggered = self._use_openai

    def _anthropic(self) -> ModelClient:
        if self._anthropic_client is None:
            self._anthropic_client = AnthropicModelClient(api_key=self._anthropic_api_key)
        return self._anthropic_client

    def _openai(self) -> ModelClient:
        if self._openai_client is None:
            self._openai_client = OpenAIModelClient(
                api_key=self._openai_api_key,
                model=self.openai_model,
            )
        return self._openai_client

    def _complete_openai(
        self, *, system: str, user: str, max_tokens: int
    ) -> str:
        self.provider_used = "openai"
        self.model_used = self.openai_model
        return self._openai().complete(
            model=self.openai_model,
            system=system,
            user=user,
            max_tokens=max_tokens,
        )

    def complete(
        self,
        *,
        model: str,
        system: str,
        user: str,
        max_tokens: int,
    ) -> str:
        if self._use_openai:
            return self._complete_openai(
                system=system, user=user, max_tokens=max_tokens
            )
        anthropic_model = self.anthropic_model or model
        self.provider_used = "anthropic"
        self.model_used = anthropic_model
        try:
            return self._anthropic().complete(
                model=anthropic_model,
                system=system,
                user=user,
                max_tokens=max_tokens,
            )
        except Exception as exc:
            if not _is_billing_or_quota_error(exc):
                raise
            # Flip before attempting OpenAI: later retries/calls must never bill
            # Anthropic again once that account has reported credit exhaustion.
            self._use_openai = True
            self.fallback_triggered = True
            return self._complete_openai(
                system=system, user=user, max_tokens=max_tokens
            )


class AnthropicModelClient:
    """Thin lazy wrapper so unit tests and non-analysis commands need no SDK."""

    def __init__(self, *, api_key: str | None = None) -> None:
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ShortsFactoryError(
                "ANTHROPIC_API_KEY is not set. Export it before analyze/run."
            )
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise ShortsFactoryError(
                "the Anthropic Python package is unavailable in this runtime"
            ) from exc
        self._client = Anthropic(api_key=self.api_key)

    def complete(
        self,
        *,
        model: str,
        system: str,
        user: str,
        max_tokens: int,
    ) -> str:
        response = self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        texts = [
            str(getattr(block, "text"))
            for block in response.content
            if getattr(block, "type", None) == "text"
        ]
        if not texts:
            raise ModelOutputError("Claude response contained no text block")
        return "\n".join(texts)


Validator = Callable[[dict[str, Any]], dict[str, Any]]


@dataclass
class StrictJsonCaller:
    client: ModelClient
    model: str = DEFAULT_CLAUDE_MODEL
    retries: int = 1

    def call(
        self,
        *,
        system: str,
        user: str,
        validator: Validator,
        max_tokens: int = 4096,
    ) -> dict[str, Any]:
        """Reject prose/fences/malformed schemas; retry with the exact error."""
        prompt = user
        last_error = "unknown validation error"
        for attempt in range(self.retries + 1):
            raw = self.client.complete(
                model=self.model,
                system=system,
                user=prompt,
                max_tokens=max_tokens,
            )
            try:
                parsed = json.loads(raw.strip())
                if not isinstance(parsed, dict):
                    raise ModelOutputError("top-level JSON must be an object")
                return validator(parsed)
            except (json.JSONDecodeError, ModelOutputError, TypeError, ValueError) as exc:
                last_error = str(exc)
                if attempt >= self.retries:
                    break
                prompt = (
                    f"{user}\n\nYour previous response was rejected: {last_error}. "
                    "Return one raw JSON object only: no prose, no markdown fences, "
                    "and obey the schema exactly."
                )
        raise ModelOutputError(
            f"Claude returned invalid structured output after {self.retries + 1} attempts: "
            f"{last_error}"
        )


PASS1_SYSTEM = """You are the first-pass editor for Taylor Dasch with EG Realty.
Evaluate only the supplied transcript window. Never invent missing context, facts,
hooks, or a payoff. Taylor's observed short-form rubric is the only rubric:

- Hook strength (0-30): first seconds create a pattern interrupt, identify an
  audience, and avoid generic greetings/setup.
- Angle quality (0-30): honest/contrarian framing, Temple/Belton/BSW/Fort Hood
  specificity, and concrete names or numbers.
- Audience fit (0-15): one clear buyer/relocator/local audience; specificity wins.
- Arc and payoff (0-20): complete standalone thought with the promised answer.
- CTA strength (0-5): natural comment/DM keyword; no CTA earns zero. A CTA can
  never compensate for mixed subjects or an incomplete payoff.

One-subject rule (hard gate): every clip must answer one viewer question with one
promise and one payoff. Multiple facts/examples are allowed only when they support
that same question. `topic_axes` means independent listener decision criteria,
not umbrella labels: taxes, schools, BSW commute, military proximity, downtown,
flood risk, and housing age are separate axes. BSW and military may share one
"work commute" axis only if every sentence answers that exact commute question.
Never hide several criteria under "Temple vs Belton" or "relocation." Mark the
payoff complete only when the spoken excerpt resolves its stated promise. Topic
purity below 90 means the excerpt contains a distinct adjacent detour, even if
that detour provides background for the main subject.

Flag every factual claim that should be checked. Investor material is not eligible
for TikTok. Long-form YouTube derivatives are also not eligible for TikTok under
this repository's governance. Prefer 15-55 seconds. Do not reward a longer clip
merely because it contains more facts. Do not reward hype.
Output raw JSON only."""

PASS2_SYSTEM = f"""You are Taylor Dasch's independent senior short-form editor.
Rerank the already-scored finalists. Favor a spoken hook that works immediately,
a complete standalone payoff, Taylor-specific local insight, honest negatives,
and a set of clips with distinct angles. Every kept clip must stay on exactly one
subject from hook through payoff. Penalize setup, repeated moments, unsupported
certainty, and clips that need prior context. Never keep a finalist marked
more than one topic axis, topic_purity below {MIN_TOPIC_PURITY}, or payoff_complete=false. Do not
rewrite or invent transcript content. Output raw JSON only."""


def ranking_input_context(
    candidates: list[dict[str, Any]],
    *,
    primary_model: str,
    openai_model: str,
    batch_size: int,
    rerank_limit: int,
) -> dict[str, Any]:
    """Bind cached semantic work to exact transcript/prompt/model inputs."""
    payload = {
        "schema_version": RANKING_INPUT_SCHEMA_VERSION,
        "rubric_version": RANKING_RUBRIC_VERSION,
        "primary_model": primary_model,
        "openai_model": openai_model,
        "batch_size": batch_size,
        "rerank_limit": rerank_limit,
        "pass1_system": PASS1_SYSTEM,
        "pass2_system": PASS2_SYSTEM,
        "score_limits": SCORE_LIMITS,
        "lanes": sorted(LANES),
        "candidates": [
            {
                "id": str(candidate["id"]),
                "start": float(candidate["start"]),
                "end": float(candidate["end"]),
                "duration_s": float(candidate["duration_s"]),
                "start_word_id": str(candidate.get("start_word_id", "")),
                "end_word_id": str(candidate.get("end_word_id", "")),
                "strategy": str(candidate.get("strategy", "")),
                "text": str(candidate["text"]),
            }
            for candidate in candidates
        ],
    }
    fingerprint = hashlib.sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return {
        "schema_version": RANKING_INPUT_SCHEMA_VERSION,
        "rubric_version": RANKING_RUBRIC_VERSION,
        "fingerprint": fingerprint,
        "primary_model": primary_model,
        "openai_model": openai_model,
        "batch_size": batch_size,
        "rerank_limit": rerank_limit,
        "candidate_count": len(candidates),
        "candidate_ids": [str(candidate["id"]) for candidate in candidates],
    }


def _require_exact_keys(value: dict[str, Any], required: set[str], label: str) -> None:
    actual = set(value)
    if actual != required:
        raise ModelOutputError(
            f"{label} keys must be {sorted(required)}, got {sorted(actual)}"
        )


def _require_string(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        raise ModelOutputError(f"{label} must be a non-empty string")
    return value.strip()


def _require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ModelOutputError(f"{label} must be a list of strings")
    return [item.strip() for item in value if item.strip()]


def _require_score(value: Any, label: str, maximum: int = 100) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ModelOutputError(f"{label} must be an integer")
    if not 0 <= value <= maximum:
        raise ModelOutputError(f"{label} must be between 0 and {maximum}")
    return value


def validate_pass1(
    parsed: dict[str, Any], expected_ids: list[str]
) -> dict[str, Any]:
    _require_exact_keys(parsed, {"evaluations"}, "pass1")
    evaluations = parsed["evaluations"]
    if not isinstance(evaluations, list):
        raise ModelOutputError("pass1.evaluations must be a list")
    normalized: list[dict[str, Any]] = []
    required = {
        "candidate_id",
        "hook",
        "summary",
        "lane",
        "scores",
        "total_score",
        "standalone",
        "topic_axes",
        "promise",
        "payoff",
        "payoff_complete",
        "topic_purity",
        "claim_flags",
        "warnings",
        "reasons",
    }
    for index, value in enumerate(evaluations):
        if not isinstance(value, dict):
            raise ModelOutputError(f"pass1 evaluation {index} must be an object")
        _require_exact_keys(value, required, f"pass1 evaluation {index}")
        candidate_id = _require_string(value["candidate_id"], "candidate_id")
        lane = _require_string(value["lane"], "lane")
        if lane not in LANES:
            raise ModelOutputError(f"invalid lane for {candidate_id}: {lane}")
        scores = value["scores"]
        if not isinstance(scores, dict):
            raise ModelOutputError(f"scores for {candidate_id} must be an object")
        _require_exact_keys(scores, set(SCORE_LIMITS), f"scores for {candidate_id}")
        checked_scores = {
            name: _require_score(scores[name], f"{candidate_id}.{name}", maximum)
            for name, maximum in SCORE_LIMITS.items()
        }
        total = _require_score(value["total_score"], f"{candidate_id}.total_score")
        if total != sum(checked_scores.values()):
            raise ModelOutputError(
                f"{candidate_id}.total_score must equal rubric sum "
                f"{sum(checked_scores.values())}, got {total}"
            )
        if not isinstance(value["standalone"], bool):
            raise ModelOutputError(f"{candidate_id}.standalone must be boolean")
        topic_axes = _require_string_list(
            value["topic_axes"], f"{candidate_id}.topic_axes"
        )
        if not topic_axes or len(topic_axes) != len(value["topic_axes"]):
            raise ModelOutputError(
                f"{candidate_id}.topic_axes must contain one or more non-empty labels"
            )
        topic_axes = list(dict.fromkeys(topic_axes))
        promise = _require_string(value["promise"], f"{candidate_id}.promise")
        payoff = _require_string(value["payoff"], f"{candidate_id}.payoff")
        if not isinstance(value["payoff_complete"], bool):
            raise ModelOutputError(f"{candidate_id}.payoff_complete must be boolean")
        topic_purity = _require_score(
            value["topic_purity"], f"{candidate_id}.topic_purity"
        )
        claims = value["claim_flags"]
        if not isinstance(claims, list):
            raise ModelOutputError(f"{candidate_id}.claim_flags must be a list")
        normalized_claims: list[dict[str, str]] = []
        for claim_index, claim in enumerate(claims):
            if not isinstance(claim, dict):
                raise ModelOutputError(f"claim {claim_index} for {candidate_id} must be object")
            _require_exact_keys(
                claim,
                {"text", "type", "severity"},
                f"claim {claim_index} for {candidate_id}",
            )
            claim_type = _require_string(claim["type"], "claim.type")
            severity = _require_string(claim["severity"], "claim.severity")
            if claim_type not in CLAIM_TYPES:
                raise ModelOutputError(f"invalid claim type: {claim_type}")
            if severity not in CLAIM_SEVERITIES:
                raise ModelOutputError(f"invalid claim severity: {severity}")
            normalized_claims.append(
                {
                    "text": _require_string(claim["text"], "claim.text"),
                    "type": claim_type,
                    "severity": severity,
                }
            )
        normalized.append(
            {
                "candidate_id": candidate_id,
                "hook": _require_string(value["hook"], "hook"),
                "summary": _require_string(value["summary"], "summary"),
                "lane": lane,
                "scores": checked_scores,
                "total_score": total,
                "standalone": value["standalone"],
                "topic_axes": topic_axes,
                "promise": promise,
                "payoff": payoff,
                "payoff_complete": value["payoff_complete"],
                "topic_purity": topic_purity,
                "claim_flags": normalized_claims,
                "warnings": _require_string_list(value["warnings"], "warnings"),
                "reasons": _require_string_list(value["reasons"], "reasons"),
            }
        )
    actual_ids = [item["candidate_id"] for item in normalized]
    if len(actual_ids) != len(set(actual_ids)) or set(actual_ids) != set(expected_ids):
        raise ModelOutputError(
            f"pass1 must return every candidate exactly once; expected {expected_ids}, "
            f"got {actual_ids}"
        )
    return {"evaluations": normalized}


def is_single_subject_evaluation(value: dict[str, Any]) -> bool:
    """The exact semantic focus gate shared by reranking and cached reuse."""
    return (
        isinstance(value.get("topic_axes"), list)
        and len(value["topic_axes"]) == 1
        and value.get("payoff_complete") is True
        and bool(str(value.get("promise", "")).strip())
        and bool(str(value.get("payoff", "")).strip())
        and int(value.get("topic_purity", 0)) >= MIN_TOPIC_PURITY
    )


def validate_pass2(
    parsed: dict[str, Any], expected_ids: list[str]
) -> dict[str, Any]:
    _require_exact_keys(parsed, {"ranking"}, "pass2")
    ranking = parsed["ranking"]
    if not isinstance(ranking, list):
        raise ModelOutputError("pass2.ranking must be a list")
    normalized: list[dict[str, Any]] = []
    required = {
        "candidate_id",
        "final_score",
        "keep",
        "selection_reason",
        "distinct_angle",
    }
    for index, value in enumerate(ranking):
        if not isinstance(value, dict):
            raise ModelOutputError(f"pass2 ranking {index} must be an object")
        _require_exact_keys(value, required, f"pass2 ranking {index}")
        if not isinstance(value["keep"], bool):
            raise ModelOutputError("pass2.keep must be boolean")
        normalized.append(
            {
                "candidate_id": _require_string(value["candidate_id"], "candidate_id"),
                "final_score": _require_score(value["final_score"], "final_score"),
                "keep": value["keep"],
                "selection_reason": _require_string(
                    value["selection_reason"], "selection_reason"
                ),
                "distinct_angle": _require_string(value["distinct_angle"], "distinct_angle"),
            }
        )
    actual_ids = [item["candidate_id"] for item in normalized]
    if len(actual_ids) != len(set(actual_ids)) or set(actual_ids) != set(expected_ids):
        raise ModelOutputError(
            f"pass2 must rank every finalist exactly once; expected {expected_ids}, "
            f"got {actual_ids}"
        )
    return {"ranking": normalized}


def _pass1_user(candidates: list[dict[str, Any]]) -> str:
    schema = {
        "evaluations": [
            {
                "candidate_id": "exact supplied id",
                "hook": "verbatim opening hook, not a rewrite",
                "summary": "one sentence",
                "lane": "bsw_buyer|military|relocator|first_time_buyer|investor|general",
                "scores": {name: f"integer 0-{maximum}" for name, maximum in SCORE_LIMITS.items()},
                "total_score": "integer rubric sum 0-100",
                "standalone": True,
                "topic_axes": ["one independent listener decision criterion"],
                "promise": "the exact viewer question or promise opened by the excerpt",
                "payoff": "the exact answer delivered inside the excerpt",
                "payoff_complete": True,
                "topic_purity": "integer 0-100",
                "claim_flags": [
                    {
                        "text": "exact claim",
                        "type": "monetary|market_stat|commute_time|school_quality|safety|legal_financial|other",
                        "severity": "review|verify|high_risk",
                    }
                ],
                "warnings": ["short warning"],
                "reasons": ["specific rubric reason"],
            }
        ]
    }
    payload = [
        {
            "candidate_id": candidate["id"],
            "start": candidate["start"],
            "end": candidate["end"],
            "duration_s": candidate["duration_s"],
            "strategy": candidate["strategy"],
            "transcript": candidate["text"],
        }
        for candidate in candidates
    ]
    return (
        "Evaluate every candidate exactly once. Return exactly this JSON shape:\n"
        f"{json.dumps(schema, ensure_ascii=False)}\n\nCandidates:\n"
        f"{json.dumps(payload, ensure_ascii=False)}"
    )


def _pass2_user(finalists: list[dict[str, Any]]) -> str:
    schema = {
        "ranking": [
            {
                "candidate_id": "exact supplied id",
                "final_score": "integer 0-100",
                "keep": True,
                "selection_reason": "specific comparative reason",
                "distinct_angle": "short angle label",
            }
        ]
    }
    payload = [
        {
            # Pass two deliberately uses short, ordinal aliases. Long hashed
            # IDs are easy for a model to mistype even when the ranking itself
            # is valid; the aliases are mapped back only after strict schema
            # validation.
            "candidate_id": item["alias"],
            "start": item["candidate"]["start"],
            "end": item["candidate"]["end"],
            "duration_s": item["candidate"]["duration_s"],
            "transcript": item["candidate"]["text"],
            "first_pass": {
                **item["evaluation"],
                "candidate_id": item["alias"],
            },
        }
        for item in finalists
    ]
    return (
        "Compare and rank every finalist exactly once. Scores are absolute quality, "
        "not ordinal positions. Return exactly this JSON shape:\n"
        f"{json.dumps(schema, ensure_ascii=False)}\n\nFinalists:\n"
        f"{json.dumps(payload, ensure_ascii=False)}"
    )


def rank_two_pass(
    candidates: list[dict[str, Any]],
    *,
    caller: StrictJsonCaller,
    batch_size: int = 8,
    rerank_limit: int = 18,
    pass1_checkpoint: Callable[[dict[str, Any]], None] | None = None,
    existing_pass1: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    if not candidates:
        return [], {"evaluations": []}, {"ranking": []}
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    candidate_ids = [str(candidate["id"]) for candidate in candidates]
    pass1_values: list[dict[str, Any]] = []
    if existing_pass1 is not None:
        raw_evaluations = existing_pass1.get("evaluations")
        if not isinstance(raw_evaluations, list):
            raise ModelOutputError("pass1 checkpoint evaluations must be a list")
        checkpoint_ids = [
            str(item.get("candidate_id"))
            for item in raw_evaluations
            if isinstance(item, dict)
        ]
        if (
            len(checkpoint_ids) != len(raw_evaluations)
            or len(checkpoint_ids) != len(set(checkpoint_ids))
            or any(candidate_id not in candidate_ids for candidate_id in checkpoint_ids)
        ):
            raise ModelOutputError(
                "pass1 checkpoint must contain unique IDs from the current candidate set"
            )
        pass1_values.extend(
            validate_pass1(existing_pass1, checkpoint_ids)["evaluations"]
        )

    completed_ids = {item["candidate_id"] for item in pass1_values}
    remaining_candidates = [
        candidate
        for candidate in candidates
        if str(candidate["id"]) not in completed_ids
    ]
    for offset in range(0, len(remaining_candidates), batch_size):
        batch = remaining_candidates[offset : offset + batch_size]
        expected_ids = [str(candidate["id"]) for candidate in batch]
        parsed = caller.call(
            system=PASS1_SYSTEM,
            user=_pass1_user(batch),
            validator=lambda value, ids=expected_ids: validate_pass1(value, ids),
        )
        pass1_values.extend(parsed["evaluations"])
        if pass1_checkpoint is not None:
            # Persist after every successful batch. A later provider/schema
            # failure cannot erase paid, already-validated first-pass work.
            pass1_checkpoint({"evaluations": list(pass1_values)})

    # A checkpoint is reusable only as a prefix of work; the final first pass
    # must still prove exact coverage of the current candidate set.
    pass1_values = validate_pass1(
        {"evaluations": pass1_values}, candidate_ids
    )["evaluations"]

    evaluations_by_id = {
        evaluation["candidate_id"]: evaluation for evaluation in pass1_values
    }
    candidate_by_id = {str(candidate["id"]): candidate for candidate in candidates}
    eligible_evaluations = [
        evaluation
        for evaluation in pass1_values
        if is_single_subject_evaluation(evaluation)
    ]
    if not eligible_evaluations:
        raise ModelOutputError(
            "no candidate passed the one-subject topic-purity gate"
        )
    finalist_evaluations = sorted(
        eligible_evaluations,
        key=lambda value: value["total_score"],
        reverse=True,
    )[: min(rerank_limit, len(eligible_evaluations))]
    finalists = [
        {
            "candidate": candidate_by_id[evaluation["candidate_id"]],
            "evaluation": evaluation,
            "alias": f"C{index:02d}",
        }
        for index, evaluation in enumerate(finalist_evaluations, start=1)
    ]
    finalist_aliases = [item["alias"] for item in finalists]
    candidate_id_by_alias = {
        item["alias"]: str(item["candidate"]["id"])
        for item in finalists
    }
    pass2_with_aliases = caller.call(
        system=PASS2_SYSTEM,
        user=_pass2_user(finalists),
        validator=lambda value: validate_pass2(value, finalist_aliases),
        max_tokens=4096,
    )
    pass2 = {
        "ranking": [
            {
                **item,
                "candidate_id": candidate_id_by_alias[item["candidate_id"]],
            }
            for item in pass2_with_aliases["ranking"]
        ]
    }
    pass2_by_id = {item["candidate_id"]: item for item in pass2["ranking"]}
    merged = [
        {
            "candidate": candidate_by_id[candidate_id],
            "evaluation": evaluations_by_id[candidate_id],
            "rerank": rerank,
        }
        for candidate_id, rerank in pass2_by_id.items()
    ]
    merged.sort(key=lambda item: item["rerank"]["final_score"], reverse=True)
    return merged, {"evaluations": pass1_values}, pass2
