from unittest import TestCase

from BaseClasses import MultiWorld
from test.general import gen_steps, setup_multiworld
from worlds.AutoWorld import call_all
from worlds.generic.Rules import locality_rules
from ... import ALTTPWorld
from ...Options import DungeonItem


class DungeonFillTestBase(TestCase):
    multiworld: MultiWorld
    world_1: ALTTPWorld
    world_2: ALTTPWorld
    options = (
        "big_key_shuffle",
        "small_key_shuffle",
        "key_drop_shuffle",
        "compass_shuffle",
        "map_shuffle",
    )

    def setUp(self):
        self.multiworld = setup_multiworld([ALTTPWorld, ALTTPWorld], ())
        self.world_1 = self.multiworld.worlds[1]
        self.world_2 = self.multiworld.worlds[2]

    def generate_with_options(self, option_value: int):
        for option in self.options:
            getattr(self.world_1.options, option).value = getattr(self.world_2.options, option).value = option_value

        for step in gen_steps:
            call_all(self.multiworld, step)
            # this is where locality rules are set in normal generation which we need to verify this test
            if step == "set_rules":
                locality_rules(self.multiworld)

    def test_original_dungeons(self):
        self.generate_with_options(DungeonItem.option_original_dungeon)
        for location in self.multiworld.get_filled_locations():
            with (self.subTest(location=location)):
                if location.parent_region.dungeon is None:
                    self.assertIs(location.item.dungeon, None)
                else:
                    self.assertEqual(location.player, location.item.player,
                                     f"{location.item} does not belong to {location}'s player")
                    if location.item.dungeon is None:
                        continue
                    self.assertIs(location.item.dungeon, location.parent_region.dungeon,
                                  f"{location.item} was not placed in its original dungeon.")

    def test_own_dungeons(self):
        self.generate_with_options(DungeonItem.option_own_dungeons)
        for location in self.multiworld.get_filled_locations():
            with self.subTest(location=location):
                if location.parent_region.dungeon is None:
                    self.assertIs(location.item.dungeon, None)
                else:
                    self.assertEqual(location.player, location.item.player,
                                     f"{location.item} does not belong to {location}'s player")
