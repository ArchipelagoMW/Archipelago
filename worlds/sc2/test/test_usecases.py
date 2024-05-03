"""
Unit tests for yaml usecases we want to support
"""

from .test_base import Sc2SetupTestBase
from .. import ItemGroups, ItemNames, Options, MissionTables, get_all_missions


class TestSupportedUseCases(Sc2SetupTestBase):
    def test_terran_with_nco_units_only_generates(self):
        options = {
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'excluded_items': {
                ItemGroups.ItemGroupNames.TERRAN_UNITS: 0,
            },
            'unexcluded_items': {
                ItemGroups.ItemGroupNames.NCO_UNITS: 0,
            },
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn(ItemNames.MARINE, item_names)
        self.assertIn(ItemNames.RAVEN, item_names)
        self.assertIn(ItemNames.LIBERATOR, item_names)
        self.assertIn(ItemNames.BATTLECRUISER, item_names)
        self.assertNotIn(ItemNames.DIAMONDBACK, item_names)
        self.assertNotIn(ItemNames.DIAMONDBACK_BURST_CAPACITORS, item_names)
        self.assertNotIn(ItemNames.VIKING, item_names)

    def test_nco_with_nobuilds_excluded_generates(self):
        options = {
            'enable_wol_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'shuffle_no_build': Options.ShuffleNoBuild.option_false,
            'mission_order': Options.MissionOrder.option_mini_campaign,
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        missions = get_all_missions(self.world.mission_req_table)
        self.assertNotIn(MissionTables.SC2Mission.THE_ESCAPE, missions)
        self.assertNotIn(MissionTables.SC2Mission.IN_THE_ENEMY_S_SHADOW, missions)
        for mission in missions:
            self.assertEqual(MissionTables.SC2Campaign.NCO, mission.campaign)

    def test_terran_with_nco_upgrades_units_only_generates(self):
        options = {
            'enable_wol_missions': True,
            'enable_nco_missions': True,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'mission_order': Options.MissionOrder.option_mini_campaign,
            'excluded_items': {
                ItemGroups.ItemGroupNames.TERRAN_ITEMS: 0,
            },
            'unexcluded_items': {
                ItemGroups.ItemGroupNames.NCO_MAX_PROGRESSIVE_ITEMS: 0,
                ItemGroups.ItemGroupNames.NCO_MIN_PROGRESSIVE_ITEMS: 1,
            },
        }
        self.generate_world(options)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(item_names)
        missions = get_all_missions(self.world.mission_req_table)
        for mission in missions:
            self.assertIn(MissionTables.MissionFlag.Terran, mission.flags)
        self.assertIn(ItemNames.MARINE, item_names)
        self.assertIn(ItemNames.MARAUDER, item_names)
        self.assertIn(ItemNames.BUNKER, item_names)
        self.assertIn(ItemNames.BANSHEE, item_names)
        self.assertIn(ItemNames.BATTLECRUISER_ATX_LASER_BATTERY, item_names)
        self.assertIn(ItemNames.NOVA_C20A_CANISTER_RIFLE, item_names)
        self.assertGreaterEqual(item_names.count(ItemNames.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS), 2)
        self.assertGreaterEqual(item_names.count(ItemNames.PROGRESSIVE_TERRAN_SHIP_WEAPON), 3)
        self.assertNotIn(ItemNames.MEDIC, item_names)
        self.assertNotIn(ItemNames.PSI_DISRUPTER, item_names)
        self.assertNotIn(ItemNames.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS, item_names)
        self.assertNotIn(ItemNames.HELLION_INFERNAL_PLATING, item_names)
        self.assertNotIn(ItemNames.CELLULAR_REACTOR, item_names)
        self.assertNotIn(ItemNames.TECH_REACTOR, item_names)
    
    def test_nco_and_2_wol_missions_only_can_generate_with_vanilla_items_only(self) -> None:
        options = {
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'excluded_missions': [
                mission.mission_name for mission in MissionTables.SC2Mission
                if mission.campaign == MissionTables.SC2Campaign.WOL
                    and mission.mission_name not in (MissionTables.SC2Mission.LIBERATION_DAY.mission_name, MissionTables.SC2Mission.THE_OUTLAWS.mission_name)
            ],
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(options)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(item_names)
        self.assertNotIn(ItemNames.LIBERATOR, item_names)
        self.assertNotIn(ItemNames.MARAUDER_PROGRESSIVE_STIMPACK, item_names)
        self.assertNotIn(ItemNames.HELLION_HELLBAT_ASPECT, item_names)
        self.assertNotIn(ItemNames.BATTLECRUISER_CLOAK, item_names)
