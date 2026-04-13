from __future__ import annotations

import unittest

from core import Err, Ok


class TestResult(unittest.TestCase):
    def test_ok_holds_value(self) -> None:
        result = Ok({"value": 1})
        self.assertTrue(result.ok)
        self.assertEqual({"value": 1}, result.value)

    def test_err_holds_error(self) -> None:
        result = Err("boom")
        self.assertFalse(result.ok)
        self.assertEqual("boom", result.error)
