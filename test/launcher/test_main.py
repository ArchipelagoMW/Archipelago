from __future__ import annotations

import importlib
import unittest
from unittest.mock import Mock, patch

import Launcher
from core import ComponentKind, Ok, ResolveInputData, ResolvedInput, ResolutionKind

from launcher.models import LauncherEntry

launcher_main = importlib.import_module("launcher.main")


class TestLauncherMain(unittest.TestCase):
    def test_root_launcher_module_is_thin_shim(self) -> None:
        self.assertIs(Launcher.main, launcher_main.main)
        self.assertIs(Launcher.cli, launcher_main.cli)

    @patch("launcher.main.run_component")
    @patch("launcher.main.to_launcher_entry")
    @patch("launcher.main.resolve_input")
    def test_main_routes_identified_file_to_run_component(
        self,
        resolve_input: Mock,
        to_launcher_entry: Mock,
        run_component: Mock,
    ) -> None:
        entry = LauncherEntry(
            id="install_apworld",
            display_name="Install APWorld",
            description="Install APWorld",
            kind=ComponentKind.MISC,
            core_component_id="install_apworld",
        )
        resolve_input.return_value = Ok(
            ResolveInputData(
                resolved=ResolvedInput(
                    raw_value="example.apworld",
                    component=type("Descriptor", (), {"id": "install_apworld"})(),
                    kind=ResolutionKind.FILE,
                    file_path="example.apworld",
                )
            )
        )
        to_launcher_entry.return_value = entry

        launcher_main.main({"Patch|Game|Component|url": "example.apworld", "update_settings": False, "args": ()})

        run_component.assert_called_once_with(entry, "example.apworld")

    @patch("launcher.gui.run_gui")
    @patch("launcher.main.to_launcher_entry")
    @patch("launcher.main.resolve_input")
    def test_main_routes_uri_selection_to_gui(self, resolve_input: Mock, to_launcher_entry: Mock, run_gui: Mock) -> None:
        text_client = LauncherEntry(
            id="text_client",
            display_name="Text Client",
            description="",
            kind=ComponentKind.CLIENT,
            core_component_id="text_client",
        )
        messenger = LauncherEntry(
            id="messenger_client",
            display_name="Messenger Client",
            description="",
            kind=ComponentKind.CLIENT,
            core_component_id="messenger_client",
        )
        resolve_input.return_value = Ok(
            ResolveInputData(
                resolved=ResolvedInput(
                    raw_value="archipelago://user:pass@example.com:38281?game=The%20Messenger",
                    component=type("Descriptor", (), {"id": "text_client"})(),
                    kind=ResolutionKind.URI,
                    candidates=[type("Descriptor", (), {"id": "messenger_client"})()],
                    launch_args=("archipelago://user:pass@example.com:38281?game=The%20Messenger",),
                )
            )
        )
        to_launcher_entry.side_effect = [text_client, messenger]

        launcher_main.main(
            {
                "Patch|Game|Component|url": "archipelago://user:pass@example.com:38281?game=The%20Messenger",
                "update_settings": False,
                "args": (),
            }
        )

        run_gui.assert_called_once_with(
            [text_client, messenger],
            ("archipelago://user:pass@example.com:38281?game=The%20Messenger",),
        )

    @patch("launcher.main.update_settings")
    def test_main_updates_settings_without_launching(self, update_settings: Mock) -> None:
        launcher_main.main({"update_settings": True, "args": ()})
        update_settings.assert_called_once_with()
