import json
from pathlib import Path

import pytest
import requests

import chatbot


class DummyResponse:
    def __init__(self, payload, status_code=200):
        self.text = json.dumps(payload)
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")


def test_sanitize_for_markdown_table_escapes_pipes_and_newlines():
    raw = "line1 | line2\nline3\r\n"
    cleaned = chatbot.sanitize_for_markdown_table(raw)
    assert cleaned == "line1 \\| line2 line3"


def test_query_ollama_success(monkeypatch):
    def fake_post(url, json, timeout):
        assert url == chatbot.OLLAMA_ENDPOINT
        assert json["model"] == chatbot.MODEL_NAME
        assert json["stream"] is False
        assert timeout == 120
        return DummyResponse({"response": "  hello world  "})

    monkeypatch.setattr(chatbot.requests, "post", fake_post)
    result = chatbot.query_ollama("test prompt")
    assert result == "hello world"


def test_query_ollama_connection_error(monkeypatch):
    def fake_post(url, json, timeout):
        raise requests.exceptions.ConnectionError("no connection")

    monkeypatch.setattr(chatbot.requests, "post", fake_post)
    result = chatbot.query_ollama("test prompt")
    assert result == "Error: Could not connect to the Ollama server."


def test_query_ollama_timeout(monkeypatch):
    def fake_post(url, json, timeout):
        raise requests.exceptions.Timeout("timed out")

    monkeypatch.setattr(chatbot.requests, "post", fake_post)
    result = chatbot.query_ollama("test prompt")
    assert result == "Error: Request timed out."


def test_main_writes_results_table_with_two_methods(monkeypatch, tmp_path):
    prompts_dir = tmp_path / "prompts"
    eval_dir = tmp_path / "eval"
    prompts_dir.mkdir(parents=True)
    eval_dir.mkdir(parents=True)

    (prompts_dir / "zero_shot_template.txt").write_text(
        "Customer Query: \"{query}\"\n\nAgent Response:", encoding="utf-8"
    )
    (prompts_dir / "one_shot_template.txt").write_text(
        "--- EXAMPLE START ---\nCustomer Query: \"x\"\nAgent Response: \"y\"\n--- EXAMPLE END ---\n\nCustomer Query: \"{query}\"\n\nAgent Response:",
        encoding="utf-8",
    )

    monkeypatch.setattr(chatbot, "__file__", str(tmp_path / "chatbot.py"))
    monkeypatch.setattr(chatbot, "QUERIES", ["Q1", "Q2"])

    def fake_query(prompt):
        return "one-shot-response" if "EXAMPLE START" in prompt else "zero-shot-response"

    monkeypatch.setattr(chatbot, "query_ollama", fake_query)

    chatbot.main()

    results_file = eval_dir / "results.md"
    assert results_file.exists()

    content = results_file.read_text(encoding="utf-8")
    assert "| Query # | Customer Query | Prompting Method | Response |" in content
    assert content.count("| Zero-Shot |") == 2
    assert content.count("| One-Shot |") == 2
    assert "zero-shot-response" in content
    assert "one-shot-response" in content


def test_main_handles_missing_template_gracefully(monkeypatch, tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir(parents=True)
    (prompts_dir / "zero_shot_template.txt").write_text("Customer Query: \"{query}\"", encoding="utf-8")

    monkeypatch.setattr(chatbot, "__file__", str(tmp_path / "chatbot.py"))
    monkeypatch.setattr(chatbot, "QUERIES", ["Q1"])

    chatbot.main()

    results_file = Path(tmp_path) / "eval" / "results.md"
    assert not results_file.exists()
