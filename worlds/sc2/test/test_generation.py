"""
Unit tests for world generation
"""
from typing import *
import unittest
import random

from .. import Options, MissionTables, ItemNames, Items, ItemGroups
from .. import FilterItem, ItemFilterFlags, create_and_flag_explicit_item_locks_and_excludes, SC2World

from BaseClasses import MultiWorld, CollectionState, PlandoOptions
from argparse import Namespace
from worlds import AutoWorld
from Generate import get_seed_name
from test.general import gen_steps, call_all


class Sc2SetupTestBase(unittest.TestCase):
    seed: Optional[int] = None
    game = SC2World.game
    player = 1
    def generate_world(self, options: Dict[str, Any]) -> None:
        self.multiworld = MultiWorld(1)
        self.multiworld.game[self.player] = self.game
        self.multiworld.player_name = {self.player: "Tester"}
        self.multiworld.set_seed(self.seed)
        self.multiworld.state = CollectionState(self.multiworld)
        random.seed(self.multiworld.seed)
        self.multiworld.seed_name = get_seed_name(random)  # only called to get same RNG progression as Generate.py
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types[self.game].options_dataclass.type_hints.items():
            new_option = option.from_any(options.get(name, option.default))
            new_option.verify(SC2World, "Tester", PlandoOptions.items|PlandoOptions.connections|PlandoOptions.texts|PlandoOptions.bosses)
            setattr(args, name, {
                1: new_option
            })
        self.multiworld.set_options(args)
        self.world: SC2World = cast(SC2World, self.multiworld.worlds[self.player])
        for step in gen_steps:
            call_all(self.multiworld, step)


class TestItemFiltering(Sc2SetupTestBase):
    def test_explicit_locks_excludes_interact_and_set_flags(self):
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
        self.generate_world(options)
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

    def test_excluding_groups_excludes_all_items_in_group(self):
        options = {
            'excluded_items': [
                ItemGroups.ItemGroupNames.BARRACKS_UNITS,
            ]
        }
        self.generate_world(options)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn(ItemNames.MARINE, self.world.options.excluded_items)
        for item_name in ItemGroups.barracks_units:
            self.assertNotIn(item_name, item_names)

    def test_excluding_campaigns_excludes_campaign_specific_items(self) -> None:
        options = {
            'enable_wol_missions': True,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        item_data_entries = [Items.item_table[item.name] for item in self.multiworld.itempool]
        for item_data in item_data_entries:
            self.assertNotIn(item_data.type, Items.ProtossItemType)
            self.assertNotIn(item_data.type, Items.ZergItemType)
            self.assertNotEqual(item_data.type, Items.TerranItemType.Nova_Gear)

    def test_excluding_all_terran_missions_excludes_all_terran_items(self) -> None:
        options = {
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'excluded_missions': [
                mission.mission_name for mission in MissionTables.SC2Mission
                if MissionTables.MissionFlag.Terran in mission.flags
            ],
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        items = [(item.name, Items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in items:
            self.assertNotIn(item_data.type, Items.TerranItemType, f"Item '{item_name}' included when all terran missions are excluded")

    def test_excluding_all_terran_build_missions_excludes_all_terran_units(self) -> None:
        options = {
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'excluded_missions': [
                mission.mission_name for mission in MissionTables.SC2Mission
                if MissionTables.MissionFlag.Terran in mission.flags
                    and MissionTables.MissionFlag.NoBuild not in mission.flags
            ],
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        items = [(item.name, Items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in items:
            self.assertNotEqual(item_data.type, Items.TerranItemType.Unit, f"Item '{item_name}' included when all terran build missions are excluded")
            self.assertNotEqual(item_data.type, Items.TerranItemType.Mercenary, f"Item '{item_name}' included when all terran build missions are excluded")
            self.assertNotEqual(item_data.type, Items.TerranItemType.Building, f"Item '{item_name}' included when all terran build missions are excluded")

    def test_excluding_all_zerg_and_kerrigan_missions_excludes_all_zerg_items(self) -> None:
        options = {
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'excluded_missions': [
                mission.mission_name for mission in MissionTables.SC2Mission
                if (MissionTables.MissionFlag.Kerrigan | MissionTables.MissionFlag.Zerg) & mission.flags
            ],
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        items = [(item.name, Items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in items:
            self.assertNotIn(item_data.type, Items.ZergItemType, f"Item '{item_name}' included when all zerg missions are excluded")

    def test_excluding_all_zerg_build_missions_excludes_zerg_units(self) -> None:
        options = {
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'excluded_missions': [
                *[mission.mission_name
                    for mission in MissionTables.SC2Mission
                    if MissionTables.MissionFlag.Zerg in mission.flags
                        and MissionTables.MissionFlag.NoBuild not in mission.flags],
                MissionTables.SC2Mission.ENEMY_WITHIN.mission_name,
            ],
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        items = [(item.name, Items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in items:
            self.assertNotEqual(item_data.type, Items.ZergItemType.Unit, f"Item '{item_name}' included when all zerg build missions are excluded")
            self.assertNotEqual(item_data.type, Items.ZergItemType.Mercenary, f"Item '{item_name}' included when all zerg build missions are excluded")

    def test_excluding_all_protoss_missions_excludes_all_protoss_items(self) -> None:
        options = {
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'excluded_missions': [
                *[mission.mission_name
                    for mission in MissionTables.SC2Mission
                    if MissionTables.MissionFlag.Protoss in mission.flags],
            ],
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        items = [(item.name, Items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in items:
            self.assertNotIn(item_data.type, Items.ProtossItemType, f"Item '{item_name}' included when all protoss missions are excluded")

    def test_excluding_all_protoss_build_missions_excludes_protoss_units(self) -> None:
        options = {
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'excluded_missions': [
                *[mission.mission_name
                    for mission in MissionTables.SC2Mission
                    if mission.race == MissionTables.SC2Race.PROTOSS
                        and MissionTables.MissionFlag.NoBuild not in mission.flags],
                MissionTables.SC2Mission.TEMPLAR_S_RETURN.mission_name,
            ],
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        items = [(item.name, Items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in items:
            self.assertNotEqual(item_data.type, Items.ProtossItemType.Unit, f"Item '{item_name}' included when all protoss build missions are excluded")
            self.assertNotEqual(item_data.type, Items.ProtossItemType.Unit_2, f"Item '{item_name}' included when all protoss build missions are excluded")
            self.assertNotEqual(item_data.type, Items.ProtossItemType.Building, f"Item '{item_name}' included when all protoss build missions are excluded")


