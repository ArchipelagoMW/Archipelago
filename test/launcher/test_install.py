from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from core import InstallApworldData, Ok, ValidateInstallData
from launcher.components.install import _install_apworld, _validated_apworld


class TestLauncherInstall(unittest.TestCase):
    @patch(
        "launcher.components.install.dispatch",
        return_value=Ok(
            ValidateInstallData(
                valid=True,
                apworld_name="example.apworld",
                module_name="example",
                checks={"valid": True},
                error=None,
            )
        ),
    )
    def test_validated_apworld_uses_core_validation(self, dispatch) -> None:
        result = _validated_apworld("example.apworld")
        self.assertEqual((Path("example.apworld"), "example", "example.apworld"), result)
        dispatch.assert_called_once()

    @patch(
        "launcher.components.install.dispatch",
        side_effect=[
            Ok(
                InstallApworldData(
                    source_path="example.apworld",
                    target_path="custom_worlds/example.apworld",
                    restart_required=False,
                )
            )
        ],
    )
    def test_install_apworld_routes_through_core_install(self, dispatch) -> None:
        result = _install_apworld("example.apworld")
        assert result is not None
        source_path, target_path = result
        self.assertEqual(Path("example.apworld"), source_path)
        self.assertEqual(Path("custom_worlds/example.apworld"), target_path)
        dispatch.assert_called_once()
