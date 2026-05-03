from __future__ import annotations

import subprocess
import sys
import unittest


class TestCoreBoundaries(unittest.TestCase):
    def test_core_import_does_not_pull_ui_or_web_adapters(self) -> None:
        code = """
import sys
import core
assert 'kivy' not in sys.modules
assert 'flask' not in sys.modules
assert 'WebHostLib' not in sys.modules
print('ok')
"""
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual("ok", result.stdout.strip())
