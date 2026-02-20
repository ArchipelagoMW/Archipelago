from unittest import TestCase

from settings import Group
from worlds.AutoWorld import AutoWorldRegister


class TestSettings(TestCase):
    def test_settings_can_update(self) -> None:
        """
        Test that world settings can update.
        """
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game=game_name):
                if world_type.settings is not None:
                    assert isinstance(world_type.settings, Group)
                    world_type.settings.update({})  # a previous bug had a crash in this call to update
