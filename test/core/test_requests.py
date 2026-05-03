from __future__ import annotations

import unittest

from core import (
    Command,
    ExecutionMode,
    GetSupportedGames,
    ListComponents,
    Query,
    ResolveInput,
    RunComponent,
    StartLocalHost,
    ValidateInstall,
)


class TestRequests(unittest.TestCase):
    def test_query_and_command_markers(self) -> None:
        self.assertIsInstance(GetSupportedGames(), Query)
        self.assertIsInstance(ListComponents(), Query)
        self.assertIsInstance(RunComponent(), Command)
        self.assertNotIsInstance(RunComponent(), Query)

    def test_request_defaults_match_core_shape(self) -> None:
        validate = ValidateInstall()
        self.assertEqual("", validate.apworld_path)
        self.assertTrue(bool(validate.request_id))

        start = StartLocalHost()
        self.assertEqual("", start.multidata_path)
        self.assertEqual("127.0.0.1", start.host)
        self.assertEqual(38281, start.port)

        resolve = ResolveInput()
        self.assertEqual("", resolve.value)

        run = RunComponent()
        self.assertEqual("", run.component_id)
        self.assertEqual((), run.args)
        self.assertIs(ExecutionMode.DIRECT, run.execution_mode)
