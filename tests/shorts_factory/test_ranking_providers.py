from __future__ import annotations

import io
import json
import os
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

from shorts_factory.errors import ModelOutputError
from shorts_factory.ranking import (
    DEFAULT_OPENAI_MODEL,
    AutoModelClient,
    ModelProviderError,
    OpenAIModelClient,
)


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.body = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self, amount: int = -1) -> bytes:
        return self.body if amount < 0 else self.body[:amount]


class RecordingModelClient:
    def __init__(self, results: list[object]) -> None:
        self.results = list(results)
        self.calls: list[dict[str, object]] = []

    def complete(
        self,
        *,
        model: str,
        system: str,
        user: str,
        max_tokens: int,
    ) -> str:
        self.calls.append(
            {
                "model": model,
                "system": system,
                "user": user,
                "max_tokens": max_tokens,
            }
        )
        result = self.results.pop(0)
        if isinstance(result, Exception):
            raise result
        return str(result)


class AnthropicLowCreditError(RuntimeError):
    status_code = 400
    body = {
        "type": "error",
        "error": {
            "type": "invalid_request_error",
            "message": "Your credit balance is too low to access the Anthropic API. "
            "Please go to Plans & Billing to purchase credits.",
        },
    }


class AnthropicRateLimitError(RuntimeError):
    status_code = 429
    body = {
        "type": "error",
        "error": {
            "type": "rate_limit_error",
            "message": "Rate limit exceeded; retry later.",
        },
    }


class OpenAIModelClientTests(unittest.TestCase):
    def test_chat_completions_uses_owned_default_model_and_json_object_mode(self) -> None:
        captured: dict[str, object] = {}

        def fake_urlopen(request: object, *, timeout: float) -> FakeResponse:
            captured["request"] = request
            captured["timeout"] = timeout
            return FakeResponse(
                {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {"content": '{"ranking": []}'},
                        }
                    ]
                }
            )

        client = OpenAIModelClient(api_key="sk-test-not-real-123456", urlopen=fake_urlopen)
        result = client.complete(
            model="claude-model-must-not-cross-provider-boundary",
            system="Return JSON.",
            user="Rank this.",
            max_tokens=321,
        )

        request = captured["request"]
        payload = json.loads(request.data.decode("utf-8"))  # type: ignore[attr-defined]
        self.assertEqual(request.full_url, "https://api.openai.com/v1/chat/completions")  # type: ignore[attr-defined]
        self.assertEqual(request.get_method(), "POST")  # type: ignore[attr-defined]
        self.assertEqual(payload["model"], DEFAULT_OPENAI_MODEL)
        self.assertEqual(payload["response_format"], {"type": "json_object"})
        self.assertEqual(payload["max_completion_tokens"], 321)
        self.assertEqual(
            [message["role"] for message in payload["messages"]],
            ["system", "user"],
        )
        self.assertEqual(result, '{"ranking": []}')
        self.assertEqual(client.provider_used, "openai")
        self.assertEqual(client.model_used, DEFAULT_OPENAI_MODEL)

    def test_http_error_is_structured_and_does_not_leak_api_key(self) -> None:
        api_key = "sk-secret-should-never-appear-123456"
        error_body = json.dumps(
            {
                "error": {
                    "message": f"bad credential {api_key} and Bearer {api_key}",
                    "type": "invalid_request_error",
                    "code": "bad_request",
                }
            }
        ).encode("utf-8")

        def fake_urlopen(request: object, *, timeout: float) -> FakeResponse:
            del request, timeout
            raise HTTPError(
                "https://api.openai.com/v1/chat/completions",
                400,
                "Bad Request",
                hdrs=None,
                fp=io.BytesIO(error_body),
            )

        client = OpenAIModelClient(api_key=api_key, urlopen=fake_urlopen)
        with self.assertRaises(ModelProviderError) as raised:
            client.complete(
                model="ignored",
                system="system",
                user="user",
                max_tokens=10,
            )
        error = raised.exception
        self.assertEqual(error.status_code, 400)
        self.assertEqual(error.error_code, "bad_request")
        self.assertNotIn(api_key, str(error))
        self.assertIn("[REDACTED]", str(error))

    def test_truncated_completion_fails_closed(self) -> None:
        client = OpenAIModelClient(
            api_key="sk-test-not-real-123456",
            urlopen=lambda request, timeout: FakeResponse(
                {
                    "choices": [
                        {
                            "finish_reason": "length",
                            "message": {"content": '{"ranking":'},
                        }
                    ]
                }
            ),
        )
        with self.assertRaisesRegex(ModelOutputError, "truncated"):
            client.complete(
                model="ignored",
                system="system",
                user="user",
                max_tokens=10,
            )


class AutoModelClientTests(unittest.TestCase):
    def test_missing_anthropic_key_starts_on_configured_openai(self) -> None:
        openai = RecordingModelClient(['{"ok": true}'])
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": ""}, clear=False):
            client = AutoModelClient(
                anthropic_api_key=None,
                openai_client=openai,
            )

            result = client.complete(
                model="claude-primary-test",
                system="system",
                user="user",
                max_tokens=100,
            )

            self.assertEqual(result, '{"ok": true}')
            self.assertEqual(openai.calls[0]["model"], DEFAULT_OPENAI_MODEL)
            self.assertTrue(client.fallback_triggered)
            self.assertEqual(client.provider_used, "openai")

    def test_low_credit_switches_permanently_to_openai_own_model(self) -> None:
        anthropic = RecordingModelClient([AnthropicLowCreditError("low credit")])
        openai = RecordingModelClient(['{"first": true}', '{"second": true}'])
        client = AutoModelClient(
            anthropic_client=anthropic,
            openai_client=openai,
            openai_model="gpt-fallback-test",
        )

        first = client.complete(
            model="claude-primary-test",
            system="system",
            user="first",
            max_tokens=100,
        )
        second = client.complete(
            model="claude-primary-test",
            system="system",
            user="second",
            max_tokens=100,
        )

        self.assertEqual(first, '{"first": true}')
        self.assertEqual(second, '{"second": true}')
        self.assertEqual(len(anthropic.calls), 1)
        self.assertEqual(
            [call["model"] for call in openai.calls],
            ["gpt-fallback-test", "gpt-fallback-test"],
        )
        self.assertTrue(client.fallback_triggered)
        self.assertEqual(client.provider_used, "openai")
        self.assertEqual(client.model_used, "gpt-fallback-test")

    def test_transient_rate_limit_does_not_fallback(self) -> None:
        rate_error = AnthropicRateLimitError("slow down")
        anthropic = RecordingModelClient([rate_error])
        openai = RecordingModelClient(['{"must_not_run": true}'])
        client = AutoModelClient(
            anthropic_client=anthropic,
            openai_client=openai,
        )

        with self.assertRaises(AnthropicRateLimitError) as raised:
            client.complete(
                model="claude-primary-test",
                system="system",
                user="user",
                max_tokens=100,
            )
        self.assertIs(raised.exception, rate_error)
        self.assertEqual(openai.calls, [])
        self.assertFalse(client.fallback_triggered)
        self.assertEqual(client.provider_used, "anthropic")
        self.assertEqual(client.model_used, "claude-primary-test")

    def test_structured_insufficient_quota_code_triggers_fallback(self) -> None:
        quota_error = RuntimeError("request rejected")
        quota_error.body = {  # type: ignore[attr-defined]
            "error": {"code": "insufficient_quota", "message": "try billing"}
        }
        anthropic = RecordingModelClient([quota_error])
        openai = RecordingModelClient(['{"ok": true}'])
        client = AutoModelClient(
            anthropic_client=anthropic,
            openai_client=openai,
        )
        result = client.complete(
            model="claude-primary-test",
            system="system",
            user="user",
            max_tokens=100,
        )
        self.assertEqual(result, '{"ok": true}')
        self.assertEqual(openai.calls[0]["model"], DEFAULT_OPENAI_MODEL)


if __name__ == "__main__":
    unittest.main()
