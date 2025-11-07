"""
Unit tests for item filtering like pool_filter.py
"""

from .test_base import Sc2SetupTestBase
from ..item import item_groups, item_names
from .. import options
from ..mission_tables import SC2Race

class ItemFilterTests(Sc2SetupTestBase):
    def test_excluding_all_barracks_units_excludes_infantry_upgrades(self) -> None:
        world_options = {
            'excluded_items': {
                item_groups.ItemGroupNames.BARRACKS_UNITS: 0
            },
            'required_tactics': 'standard',
            'min_number_of_upgrades': 1,
            **self.TERRAN_CAMPAIGNS,
            'selected_races': {
                SC2Race.TERRAN.get_title()
            },
            'mission_order': 'grid',
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        races = {mission.race for mission in self.world.custom_mission_order.get_used_missions()}
        self.assertIn(SC2Race.TERRAN, races)
        self.assertNotIn(SC2Race.ZERG, races)
        self.assertNotIn(SC2Race.PROTOSS, races)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertNotIn(item_names.MARINE, itempool)
        self.assertNotIn(item_names.MARAUDER, itempool)

        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, itempool)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR, itempool)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE, itempool)

    def test_excluding_one_item_of_multi_parent_doesnt_filter_children(self) -> None:
        world_options = {
            'locked_items': {
                item_names.SENTINEL: 1,
                item_names.CENTURION: 1,
            },
            'excluded_items': {
                item_names.ZEALOT: 1,
                # Exclude more items to make space
                item_names.WRATHWALKER: 1,
                item_names.ENERGIZER: 1,
                item_names.AVENGER: 1,
                item_names.ARBITER: 1,
                item_names.VOID_RAY: 1,
                item_names.PULSAR: 1,
                item_names.DESTROYER: 1,
                item_names.DAWNBRINGER: 1,
            },
            'min_number_of_upgrades': 2,
            'required_tactics': 'standard',
            **self.ALL_CAMPAIGNS,
            'selected_races': {
                SC2Race.PROTOSS.get_title()
            },
            'mission_order': 'grid',
            'enable_race_swap': options.EnableRaceSwapVariants.option_shuffle_all,
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertIn(item_names.ZEALOT_SENTINEL_CENTURION_SHIELD_CAPACITY, itempool)
        self.assertIn(item_names.ZEALOT_SENTINEL_CENTURION_LEG_ENHANCEMENTS, itempool)

    def test_excluding_all_items_in_multiparent_excludes_child_items(self) -> None:
        world_options = {
            'excluded_items': {
                item_names.ZEALOT: 1,
                item_names.SENTINEL: 1,
                item_names.CENTURION: 1,
            },
            'min_number_of_upgrades': 2,
            'required_tactics': 'standard',
            **self.PROTOSS_CAMPAIGNS,
            'selected_races': {
                SC2Race.PROTOSS.get_title()
            },
            'mission_order': 'grid',
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertNotIn(item_names.ZEALOT_SENTINEL_CENTURION_SHIELD_CAPACITY, itempool)
        self.assertNotIn(item_names.ZEALOT_SENTINEL_CENTURION_LEG_ENHANCEMENTS, itempool)

