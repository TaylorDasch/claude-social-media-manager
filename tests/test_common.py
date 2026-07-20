import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.common as common


class LoadBannedWordsTests(unittest.TestCase):
    def test_same_term_replacement_is_not_banned(self):
        quality_gates = """# Quality Gates

## GATE 1: Banned Language (HARD)

| Banned | Replacement |
|---|---|
| Fort Hood | Fort Hood |
| turnkey | buy-and-hold |

**Also banned in hooks/openers:**
- "Let me tell you about..."

## GATE 2: Entity Consistency (HARD)
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "QUALITY-GATES.md"
            path.write_text(quality_gates, encoding="utf-8")
            with patch.object(common, "QUALITY_GATES_PATH", path):
                banned = common.load_banned_words()

        self.assertNotIn("fort hood", banned)
        self.assertIn("turnkey", banned)
        self.assertIn("let me tell you about...", banned)


if __name__ == "__main__":
    unittest.main()
