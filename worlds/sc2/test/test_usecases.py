"""
Unit tests for yaml usecases we want to support
"""

from .test_base import Sc2SetupTestBase
from .. import get_all_missions, item_groups, item_names, items, mission_tables, options
from ..mission_tables import vanilla_mission_req_table, SC2Campaign, SC2Race


class TestSupportedUseCases(Sc2SetupTestBase):
    def test_vanilla_all_campaigns_generates(self) -> None:
        world_options = {
            'mission_order': options.MissionOrder.option_vanilla,
            'enable_wol_missions': True,
            'enable_nco_missions': True,
            'enable_prophecy_missions': True,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': True,
            'enable_lotv_missions': True,
            'enable_epilogue_missions': True,
        }
        self.generate_world(world_options)
        world_regions = [region.name for region in self.multiworld.regions if region.name != "Menu"]
        self.assertEqual(len(world_regions), 83, "Unexpected number of missions for vanilla mission order")

    def test_terran_with_nco_units_only_generates(self):
        world_options = {
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'excluded_items': {
                item_groups.ItemGroupNames.TERRAN_UNITS: 0,
            },
            'unexcluded_items': {
                item_groups.ItemGroupNames.NCO_UNITS: 0,
            },
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        world_item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn(item_names.MARINE, world_item_names)
        self.assertIn(item_names.RAVEN, world_item_names)
        self.assertIn(item_names.LIBERATOR, world_item_names)
        self.assertIn(item_names.BATTLECRUISER, world_item_names)
        self.assertNotIn(item_names.DIAMONDBACK, world_item_names)
        self.assertNotIn(item_names.DIAMONDBACK_BURST_CAPACITORS, world_item_names)
        self.assertNotIn(item_names.VIKING, world_item_names)

    def test_nco_with_nobuilds_excluded_generates(self):
        world_options = {
            'enable_wol_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'shuffle_no_build': options.ShuffleNoBuild.option_false,
            'mission_order': options.MissionOrder.option_mini_campaign,
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        missions = get_all_missions(self.world.mission_req_table)
        self.assertNotIn(mission_tables.SC2Mission.THE_ESCAPE, missions)
        self.assertNotIn(mission_tables.SC2Mission.IN_THE_ENEMY_S_SHADOW, missions)
        for mission in missions:
            self.assertEqual(mission_tables.SC2Campaign.NCO, mission.campaign)

    def test_terran_with_nco_upgrades_units_only_generates(self):
        world_options = {
            'enable_wol_missions': True,
            'enable_nco_missions': True,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'mission_order': options.MissionOrder.option_vanilla_shuffled,
            'excluded_items': {
                item_groups.ItemGroupNames.TERRAN_ITEMS: 0,
            },
            'unexcluded_items': {
                item_groups.ItemGroupNames.NCO_MAX_PROGRESSIVE_ITEMS: 0,
                item_groups.ItemGroupNames.NCO_MIN_PROGRESSIVE_ITEMS: 1,
            },
        }
        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(world_item_names)
        missions = get_all_missions(self.world.mission_req_table)
        for mission in missions:
            self.assertIn(mission_tables.MissionFlag.Terran, mission.flags)
        self.assertIn(item_names.MARINE, world_item_names)
        self.assertIn(item_names.MARAUDER, world_item_names)
        self.assertIn(item_names.BUNKER, world_item_names)
        self.assertIn(item_names.BANSHEE, world_item_names)
        self.assertIn(item_names.BATTLECRUISER_ATX_LASER_BATTERY, world_item_names)
        self.assertIn(item_names.NOVA_C20A_CANISTER_RIFLE, world_item_names)
        self.assertGreaterEqual(world_item_names.count(item_names.BANSHEE_PROGRESSIVE_CROSS_SPECTRUM_DAMPENERS), 2)
        self.assertGreaterEqual(world_item_names.count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON), 3)
        self.assertNotIn(item_names.MEDIC, world_item_names)
        self.assertNotIn(item_names.PSI_DISRUPTER, world_item_names)
        self.assertNotIn(item_names.BATTLECRUISER_PROGRESSIVE_MISSILE_PODS, world_item_names)
        self.assertNotIn(item_names.HELLION_INFERNAL_PLATING, world_item_names)
        self.assertNotIn(item_names.CELLULAR_REACTOR, world_item_names)
        self.assertNotIn(item_names.TECH_REACTOR, world_item_names)
    
    def test_nco_and_2_wol_missions_only_can_generate_with_vanilla_items_only(self) -> None:
        world_options = {
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'excluded_missions': [
                mission.mission_name for mission in mission_tables.SC2Mission
                if mission.campaign == mission_tables.SC2Campaign.WOL
                    and mission.mission_name not in (mission_tables.SC2Mission.LIBERATION_DAY.mission_name, mission_tables.SC2Mission.THE_OUTLAWS.mission_name)
            ],
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(item_names)
        self.assertNotIn(item_names.LIBERATOR, world_item_names)
        self.assertNotIn(item_names.MARAUDER_PROGRESSIVE_STIMPACK, world_item_names)
        self.assertNotIn(item_names.HELLION_HELLBAT_ASPECT, world_item_names)
        self.assertNotIn(item_names.BATTLECRUISER_CLOAK, world_item_names)
    
    def test_free_protoss_only_generates(self) -> None:
        world_options = {
            'enable_wol_missions': False,
            'enable_nco_missions': False,
            'enable_prophecy_missions': True,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': True,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            # todo(mm): Currently, these settings don't generate on grid because there are not enough EASY missions
            'mission_order': options.MissionOrder.option_vanilla_shuffled,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
        }
        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(world_item_names)
        missions = get_all_missions(self.world.mission_req_table)
        self.assertEqual(len(missions), 7, "Wrong number of missions in free protoss seed")
        for mission in missions:
            self.assertIn(mission.campaign, (mission_tables.SC2Campaign.PROLOGUE, mission_tables.SC2Campaign.PROPHECY))
        for item_name in world_item_names:
            self.assertIn(items.item_table[item_name].race, (mission_tables.SC2Race.ANY, mission_tables.SC2Race.PROTOSS))

    def test_resource_filler_items_may_be_put_in_start_inventory(self) -> None:
        NUM_RESOURCE_ITEMS = 10
        world_options = {
            'start_inventory': {
                item_names.STARTING_MINERALS: NUM_RESOURCE_ITEMS,
                item_names.STARTING_VESPENE: NUM_RESOURCE_ITEMS,
                item_names.STARTING_SUPPLY: NUM_RESOURCE_ITEMS,
            },
        }
        self.generate_world(world_options)
        start_item_names = [item.name for item in self.multiworld.precollected_items[self.player]]
        self.assertEqual(start_item_names.count(item_names.STARTING_MINERALS), NUM_RESOURCE_ITEMS, "Wrong number of starting minerals in starting inventory")
        self.assertEqual(start_item_names.count(item_names.STARTING_VESPENE), NUM_RESOURCE_ITEMS, "Wrong number of starting vespene in starting inventory")
        self.assertEqual(start_item_names.count(item_names.STARTING_SUPPLY), NUM_RESOURCE_ITEMS, "Wrong number of starting supply in starting inventory")

    def test_excluding_protoss_excludes_campaigns_and_items(self) -> None:
        world_options = {
            'selected_races': options.SelectRaces.option_terran_and_zerg,
            'enable_wol_missions': True,
            'enable_nco_missions': True,
            'enable_prophecy_missions': True,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': True,
            'enable_lotv_missions': True,
            'enable_epilogue_missions': True,
            'mission_order': options.MissionOrder.option_grid,
        }
        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        world_regions = [region.name for region in self.multiworld.regions]
        world_regions.remove('Menu')
        for item_name in world_item_names:
            self.assertNotEqual(items.item_table[item_name].race, mission_tables.SC2Race.PROTOSS, f"{item_name} is a PROTOSS item!")
        for region in world_regions:
            self.assertNotIn(mission_tables.lookup_name_to_mission[region].campaign, 
                             (mission_tables.SC2Campaign.LOTV, mission_tables.SC2Campaign.PROPHECY, mission_tables.SC2Campaign.PROLOGUE),
                             f"{region} is a PROTOSS mission!")

    def test_excluding_terran_excludes_campaigns_and_items(self) -> None:
        world_options = {
            'selected_races': options.SelectRaces.option_zerg_and_protoss,
            'enable_wol_missions': True,
            'enable_nco_missions': True,
            'enable_prophecy_missions': True,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': True,
            'enable_lotv_missions': True,
            'enable_epilogue_missions': True,
            'mission_order': options.MissionOrder.option_grid,
        }
        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        world_regions = [region.name for region in self.multiworld.regions]
        world_regions.remove('Menu')
        for item_name in world_item_names:
            self.assertNotEqual(items.item_table[item_name].race, mission_tables.SC2Race.TERRAN,
                                f"{item_name} is a TERRAN item!")
        for region in world_regions:
            self.assertNotIn(mission_tables.lookup_name_to_mission[region].campaign,
                             (mission_tables.SC2Campaign.WOL, mission_tables.SC2Campaign.NCO),
                             f"{region} is a TERRAN mission!")

    def test_excluding_zerg_excludes_campaigns_and_items(self) -> None:
        world_options = {
            'selected_races': options.SelectRaces.option_terran_and_protoss,
            'enable_wol_missions': True,
            'enable_nco_missions': True,
            'enable_prophecy_missions': True,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': True,
            'enable_lotv_missions': True,
            'enable_epilogue_missions': True,
            'mission_order': options.MissionOrder.option_grid,
        }
        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        world_regions = [region.name for region in self.multiworld.regions]
        world_regions.remove('Menu')
        for item_name in world_item_names:
            self.assertNotEqual(items.item_table[item_name].race, mission_tables.SC2Race.ZERG,
                                f"{item_name} is a ZERG item!")
        # have to manually exclude the only non-zerg HotS mission...
        for region in filter(lambda region: region != "With Friends Like These", world_regions):
            self.assertNotIn(mission_tables.lookup_name_to_mission[region].campaign,
                             ([mission_tables.SC2Campaign.HOTS]),
                             f"{region} is a ZERG mission!")

    def test_excluding_faction_on_vanilla_order_excludes_epilogue(self) -> None:
        world_options = {
            'selected_races': options.SelectRaces.option_terran_and_protoss,
            'enable_wol_missions': True,
            'enable_nco_missions': True,
            'enable_prophecy_missions': True,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': True,
            'enable_lotv_missions': True,
            'enable_epilogue_missions': True,
            'mission_order': options.MissionOrder.option_vanilla,
        }
        self.generate_world(world_options)
        world_regions = [region.name for region in self.multiworld.regions]
        world_regions.remove('Menu')
        for region in world_regions:
            self.assertNotIn(mission_tables.lookup_name_to_mission[region].campaign,
                             ([mission_tables.SC2Campaign.EPILOGUE]),
                             f"{region} is an epilogue mission!")

    def test_race_swap_pick_one_has_correct_length_and_includes_swaps(self) -> None:
        world_options = {
            'selected_races': options.SelectRaces.option_all,
            'enable_race_swap': options.EnableRaceSwapVariants.option_pick_one,
            'enable_wol_missions': True,
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'mission_order': options.MissionOrder.option_grid,
            'excluded_missions': [mission_tables.SC2Mission.ZERO_HOUR.mission_name],
        }
        self.generate_world(world_options)
        world_regions = [region.name for region in self.multiworld.regions]
        world_regions.remove('Menu')
        self.assertEqual(len(world_regions), len(vanilla_mission_req_table.get(SC2Campaign.WOL)))
        races = set(mission_tables.lookup_name_to_mission[mission].race for mission in world_regions)
        self.assertTrue(SC2Race.ZERG in races or SC2Race.PROTOSS in races)
