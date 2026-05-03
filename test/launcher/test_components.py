from __future__ import annotations

import unittest
from unittest.mock import Mock, patch

from core import ComponentKind, ExecutionMode, Ok
from core.requests import RunComponentData

from launcher.components import activate_component, run_component, set_refresh_components
from launcher.models import LauncherEntry


class TestLauncherComponents(unittest.TestCase):
    def tearDown(self) -> None:
        set_refresh_components(None)

    def test_run_component_refreshes_after_utility_action(self) -> None:
        calls: list[tuple[str, ...]] = []
        refreshed: list[str] = []

        component = LauncherEntry(
            id="utility",
            display_name="Utility",
            description="",
            kind=ComponentKind.MISC,
            action=lambda *args: calls.append(args) or "Completed.",
        )
        set_refresh_components(lambda: refreshed.append("refresh"))

        run_component(component, "value")

        self.assertEqual([("value",)], calls)
        self.assertEqual(["refresh"], refreshed)

    @patch("launcher.components.dispatch", return_value=Ok(RunComponentData(component_id="cli_component", message="Running in the background...")))
    def test_activate_component_returns_background_text_for_cli_backend(self, dispatch: Mock) -> None:
        component = LauncherEntry(
            id="cli_component",
            display_name="CLI Component",
            description="",
            kind=ComponentKind.CLIENT,
            core_component_id="cli_component",
            launch_mode=ExecutionMode.TERMINAL,
        )

        result = activate_component(component)

        self.assertEqual("Running in the background...", result)
        dispatch.assert_called_once()

    @patch("launcher.components.dispatch", return_value=Ok(RunComponentData(component_id="host", message="Completed.")))
    def test_run_component_routes_backend_entry_through_core(self, dispatch: Mock) -> None:
        component = LauncherEntry(
            id="host",
            display_name="Host",
            description="",
            kind=ComponentKind.MISC,
            core_component_id="host",
        )

        run_component(component, "example.archipelago")

        dispatch.assert_called_once()
