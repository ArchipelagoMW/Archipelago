from __future__ import annotations

import unittest
from unittest.mock import patch

from core import ComponentDescriptor, ComponentKind, ExecutionMode, HandlerId, Ok, ResolveInputData, ResolvedInput, ResolutionKind

from launcher.models import LauncherEntry
from launcher.resolution import get_components, handle_uri, identify


class TestLauncherResolution(unittest.TestCase):
    @patch(
        "launcher.resolution.get_backend_components",
        return_value=[
            ComponentDescriptor(
                id="text_client",
                display_name="Text Client",
                description="",
                kind=ComponentKind.CLIENT,
                handler_id=HandlerId.PROCESS,
                launch_mode=ExecutionMode.BACKGROUND,
            )
        ],
    )
    def test_get_components_includes_launcher_utilities(self, get_backend_components) -> None:
        names = {component.display_name for component in get_components()}
        self.assertIn("Open host.yaml", names)
        self.assertIn("Open Patch", names)
        self.assertIn("Browse Files", names)
        self.assertIn("Text Client", names)

    @patch(
        "launcher.resolution.resolve_input",
        return_value=Ok(
            ResolveInputData(
                resolved=ResolvedInput(
                    raw_value="example.apworld",
                    component=ComponentDescriptor(
                        id="install_apworld",
                        display_name="Install APWorld",
                        description="",
                        kind=ComponentKind.MISC,
                        handler_id=HandlerId.INSTALL_APWORLD,
                        launch_mode=ExecutionMode.DIRECT,
                    ),
                    kind=ResolutionKind.FILE,
                    file_path="example.apworld",
                )
            )
        ),
    )
    @patch("launcher.resolution.to_launcher_entry")
    def test_identify_resolves_patch_handler_and_component_name(self, to_launcher_entry, resolve_input) -> None:
        utility = LauncherEntry(
            id="install_apworld",
            display_name="Install APWorld",
            description="",
            kind=ComponentKind.MISC,
            core_component_id="install_apworld",
        )
        to_launcher_entry.return_value = utility

        file_path, component = identify("example.apworld")

        self.assertEqual("example.apworld", file_path)
        assert component is not None
        self.assertEqual(utility.display_name, component.display_name)

    @patch(
        "launcher.resolution.resolve_input",
        return_value=Ok(
            ResolveInputData(
                resolved=ResolvedInput(
                    raw_value="archipelago://user:pass@example.com:38281?game=Unknown",
                    component=ComponentDescriptor(
                        id="text_client",
                        display_name="Text Client",
                        description="",
                        kind=ComponentKind.CLIENT,
                        handler_id=HandlerId.PROCESS,
                        launch_mode=ExecutionMode.BACKGROUND,
                    ),
                    kind=ResolutionKind.URI,
                    launch_args=("archipelago://user:pass@example.com:38281?game=Unknown",),
                )
            )
        ),
    )
    @patch("launcher.resolution.to_launcher_entry")
    def test_handle_uri_keeps_text_client_fallback(self, to_launcher_entry, resolve_input) -> None:
        text_client = LauncherEntry(
            id="text_client",
            display_name="Text Client",
            description="",
            kind=ComponentKind.CLIENT,
            core_component_id="text_client",
        )
        to_launcher_entry.return_value = text_client

        components, direct_component = handle_uri("archipelago://user:pass@example.com:38281?game=Unknown")

        self.assertEqual([], components)
        assert direct_component is not None
        self.assertEqual(text_client.display_name, direct_component.display_name)
