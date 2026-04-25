#!/usr/bin/env python3
"""Shared utilities for claude-social-media-manager scripts.

Single source of truth for:
- Project path resolution (PROJECT_ROOT, SITE_ROOT, data + governance paths)
- Governance doc parsing (banned words from QUALITY-GATES.md, states from
  WORKFLOW-STATE-MACHINE.md) — runtime SSOT, no forks in code
- Structured warnings via warn() — replaces bare `except Exception: pass`
- Safe CSV/JSON loaders that warn on failure instead of silent empty returns

Import from scripts/: `from common import PROJECT_ROOT, warn, load_banned_words`

Self-test:
  python3 scripts/common.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any

# ── Paths (single source of truth) ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
GOVERNANCE_DIR = PROJECT_ROOT / "governance"
REFERENCE_DIR = PROJECT_ROOT / "reference"
SKILLS_DIR = PROJECT_ROOT / "skills"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

REGISTRY_PATH = DATA_DIR / "content-registry.csv"
PERFORMANCE_LEDGER_PATH = DATA_DIR / "performance-ledger.csv"
HOOK_BANK_PATH = DATA_DIR / "hook-bank.json"

# Sibling project that hosts the website source. Not all checkouts will have it.
SITE_ROOT = PROJECT_ROOT.parent / "real-estate-redefined"

# Governance doc paths
QUALITY_GATES_PATH = GOVERNANCE_DIR / "QUALITY-GATES.md"
STATE_MACHINE_PATH = GOVERNANCE_DIR / "WORKFLOW-STATE-MACHINE.md"
FACT_HANDLING_PATH = GOVERNANCE_DIR / "FACT-HANDLING.md"


# ── Logging ──
def warn(msg: str, *, context: str | None = None) -> None:
    """Print a warning to stderr. Replaces `except Exception: pass`.

    Evidence over silence — every swallowed exception becomes a logged warning
    so the Operating Bar "scanners lying about counts" failure mode can't recur.
    """
    prefix = f"[WARN:{context}] " if context else "[WARN] "
    print(f"{prefix}{msg}", file=sys.stderr)


def info(msg: str) -> None:
    """Print an informational message to stdout."""
    print(msg)


# ── Governance parsers (runtime SSOT — docs beat hardcoded lists) ──
def load_banned_words() -> list[str]:
    """Parse banned words from governance/QUALITY-GATES.md Gate 1.

    Extracts two sources within Gate 1:
      1. The `| Banned | Replacement |` markdown table
      2. The bullet list under "Also banned in hooks/openers:"

    Returns a list of lowercased phrases. Empty list if doc missing
    (with stderr warning so callers never silently skip the gate).
    """
    if not QUALITY_GATES_PATH.exists():
        warn(f"QUALITY-GATES.md not found at {QUALITY_GATES_PATH}",
             context="governance")
        return []

    text = QUALITY_GATES_PATH.read_text(encoding="utf-8", errors="ignore")

    # Isolate Gate 1 section to avoid pulling words from other gates' examples
    gate1_match = re.search(
        r"## GATE 1:.*?(?=\n## GATE 2:|\Z)", text, re.DOTALL
    )
    if not gate1_match:
        warn("Gate 1 section not found in QUALITY-GATES.md", context="governance")
        return []

    gate1_text = gate1_match.group(0)
    banned: list[str] = []

    # Parse the banned/replacement table
    for line in gate1_text.splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*[^|]+\s*\|", line)
        if not m:
            continue
        word = m.group(1).strip()
        lower = word.lower()
        # Skip header row and markdown separator row
        if lower in ("banned", "don't"):
            continue
        if set(word) <= set("-|: "):
            continue
        banned.append(lower)

    # Parse the "Also banned in hooks/openers" bullet list
    hook_section = re.search(
        r"\*\*Also banned in hooks/openers:\*\*(.*?)(?=\n\*\*|\n##|\Z)",
        gate1_text,
        re.DOTALL,
    )
    if hook_section:
        for bullet in re.findall(
            r'^-\s*"([^"]+)"', hook_section.group(1), re.MULTILINE
        ):
            banned.append(bullet.lower())

    return banned


def load_valid_states() -> set[str]:
    """Parse valid workflow states from governance/WORKFLOW-STATE-MACHINE.md.

    States are declared as H3 headers like `### IDEA`, `### QUEUED`, etc.
    Returns a set. Empty set if doc missing (with stderr warning).
    """
    if not STATE_MACHINE_PATH.exists():
        warn(
            f"WORKFLOW-STATE-MACHINE.md not found at {STATE_MACHINE_PATH}",
            context="governance",
        )
        return set()

    text = STATE_MACHINE_PATH.read_text(encoding="utf-8", errors="ignore")
    return set(re.findall(r"^###\s+([A-Z][A-Z_]+)\s*$", text, re.MULTILINE))


# ── Safe data loaders (no silent failures) ──
def load_registry() -> list[dict]:
    """Load content-registry.csv rows. Warns (not silent) on failure."""
    if not REGISTRY_PATH.exists():
        warn(f"Registry not found at {REGISTRY_PATH}", context="registry")
        return []
    try:
        with REGISTRY_PATH.open("r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception as exc:
        warn(f"Could not read registry: {exc}", context="registry")
        return []


def load_json_safe(path: Path, default: Any = None) -> Any:
    """Load a JSON file, warning on failure.

    Returns `default` (or {} / [] inferred from context) if the file is
    missing or invalid. Never silently returns empty.
    """
    if not path.exists():
        warn(f"File not found: {path}", context="json")
        return default if default is not None else {}
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        warn(f"Could not parse JSON at {path}: {exc}", context="json")
        return default if default is not None else {}


def load_hooks() -> list[dict]:
    """Load hook-bank.json entries as a flat list, even if pillar-keyed."""
    data = load_json_safe(HOOK_BANK_PATH, default={})
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        flat: list[dict] = []
        for value in data.values():
            if isinstance(value, list):
                flat.extend(value)
        return flat
    return []


if __name__ == "__main__":
    # Self-test — run to verify governance parsing works end-to-end
    info(f"PROJECT_ROOT: {PROJECT_ROOT}")
    info(f"SITE_ROOT exists: {SITE_ROOT.exists()}")
    banned = load_banned_words()
    info(f"Banned words parsed: {len(banned)}")
    if banned:
        info(f"  Sample: {banned[:8]}")
    states = load_valid_states()
    info(f"Valid states parsed: {len(states)}")
    if states:
        info(f"  States: {sorted(states)}")
    registry = load_registry()
    info(f"Registry rows loaded: {len(registry)}")
    hooks = load_hooks()
    info(f"Hook bank entries: {len(hooks)}")
