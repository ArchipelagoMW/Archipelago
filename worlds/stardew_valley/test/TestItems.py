import itertools
import math
import sys
import unittest
import random
from typing import Set

from BaseClasses import ItemClassification, MultiWorld
from . import setup_solo_multiworld, SVTestCase, allsanity_options_without_mods
from .. import ItemData, StardewValleyWorld
from ..items import Group, item_table


class TestItems(SVTestCase):
    def test_can_create_item_of_resource_pack(self):
        item_name = "Resource Pack: 500 Money"

        multi_world = MultiWorld(1)
        multi_world.game[1] = "Stardew Valley"
        multi_world.player_name = {1: "Tester"}
        world = StardewValleyWorld(multi_world, 1)
        item = world.create_item(item_name)

        assert item.name == item_name

    def test_items_table_footprint_is_between_717000_and_737000(self):
        item_with_lowest_id = min((item for item in item_table.values() if item.code is not None), key=lambda x: x.code)
        item_with_highest_id = max((item for item in item_table.values() if item.code is not None),
                                   key=lambda x: x.code)

        assert item_with_lowest_id.code >= 717000
        assert item_with_highest_id.code < 737000

    def test_babies_come_in_all_shapes_and_sizes(self):
        baby_permutations = set()
        for attempt_number in range(50):
            if len(baby_permutations) >= 4:
                print(f"Already got all 4 baby permutations, breaking early [{attempt_number} generations]")
                break
            seed = random.randrange(sys.maxsize)
            multiworld = setup_solo_multiworld(seed=seed)
            baby_items = [item for item in multiworld.get_items() if "Baby" in item.name]
            self.assertEqual(len(baby_items), 2)
            baby_permutations.add(f"{baby_items[0]} - {baby_items[1]}")
        self.assertEqual(len(baby_permutations), 4)

    def test_correct_number_of_stardrops(self):
        seed = random.randrange(sys.maxsize)
        allsanity_options = allsanity_options_without_mods()
        multiworld = setup_solo_multiworld(allsanity_options, seed=seed)
        stardrop_items = [item for item in multiworld.get_items() if "Stardrop" in item.name]
        self.assertEqual(len(stardrop_items), 5)
