from __future__ import annotations

import unittest

from core import GetSupportedGames, ListComponents, Ok

from launcher.bootstrap import create_launcher_composition


class TestLauncherBootstrap(unittest.IsolatedAsyncioTestCase):
    async def test_bootstrap_registers_launcher_handlers(self) -> None:
        composition = create_launcher_composition()

        supported_games = await composition.dispatcher.handle(GetSupportedGames())
        listed_components = await composition.dispatcher.handle(ListComponents())

        self.assertIsInstance(supported_games, Ok)
        self.assertIsInstance(listed_components, Ok)
        assert isinstance(listed_components, Ok)
        self.assertTrue(any(component.display_name == "Text Client" for component in listed_components.value.components))
