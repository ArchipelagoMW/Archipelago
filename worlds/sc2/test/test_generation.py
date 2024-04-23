"""
Unit tests for world generation
"""
from typing import *
import unittest
import random

from .. import Options, MissionTables, ItemNames, Items
from .. import FilterItem, ItemFilterFlags, create_and_flag_explicit_item_locks_and_excludes, SC2World

from BaseClasses import MultiWorld, CollectionState
from argparse import Namespace
from worlds import AutoWorld
from Generate import get_seed_name

class Sc2SetupTestBase(unittest.TestCase):
    seed: Optional[int] = None
    game = SC2World.game
    player = 1
    def setUp(self) -> None:
        self.multiworld = MultiWorld(1)
        self.multiworld.game[self.player] = self.game
        self.multiworld.player_name = {self.player: "Tester"}
        self.multiworld.set_seed(self.seed)
        self.multiworld.state = CollectionState(self.multiworld)
        random.seed(self.multiworld.seed)
        self.multiworld.seed_name = get_seed_name(random)  # only called to get same RNG progression as Generate.py
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types[self.game].options_dataclass.type_hints.items():
            setattr(args, name, {
                1: option.from_any(self.options.get(name, option.default))
            })
        self.multiworld.set_options(args)
        self.world = self.multiworld.worlds[self.player]


class TestItemFiltering(Sc2SetupTestBase):
    options = {
        'locked_items': {
            ItemNames.MARINE: 0,
            ItemNames.MARAUDER: 0,
            ItemNames.MEDIVAC: 1,
            ItemNames.FIREBAT: 1,
            ItemNames.ZEALOT: 0,
            ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL: 2,
        },
        'excluded_items': {
            ItemNames.MARINE: 0,
            ItemNames.MARAUDER: 0,
            ItemNames.MEDIVAC: 0,
            ItemNames.FIREBAT: 1,
            ItemNames.ZERGLING: 0,
            ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL: 2,
        }
    }
    def test_explicit_locks_excludes_interact_and_set_flags(self):
        item_list = create_and_flag_explicit_item_locks_and_excludes(self.world)
        self.assertNotIn(ItemNames.ZERGLING, [x.name for x in item_list], msg=f'{ItemNames.ZERGLING} did not get properly excluded')
        self.assertIn(FilterItem(ItemNames.MARINE, Items.item_table[ItemNames.MARINE], flags=ItemFilterFlags.Locked), item_list)
        self.assertIn(FilterItem(ItemNames.MARAUDER, Items.item_table[ItemNames.MARAUDER], flags=ItemFilterFlags.Locked), item_list)
        self.assertIn(FilterItem(ItemNames.MEDIVAC, Items.item_table[ItemNames.MEDIVAC], flags=ItemFilterFlags.Locked), item_list)
        self.assertIn(FilterItem(ItemNames.FIREBAT, Items.item_table[ItemNames.FIREBAT], flags=ItemFilterFlags.Locked), item_list)
        self.assertIn(FilterItem(ItemNames.ZEALOT, Items.item_table[ItemNames.ZEALOT], flags=ItemFilterFlags.Locked), item_list)
        self.assertIn(FilterItem(ItemNames.DRAGOON, Items.item_table[ItemNames.DRAGOON]), item_list)
        regen_biosteel_items = [x for x in item_list if x.name == ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL]
        self.assertEqual(len(regen_biosteel_items), 2)
        

