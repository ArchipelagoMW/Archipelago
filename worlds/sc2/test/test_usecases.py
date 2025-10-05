"""
Unit tests for yaml usecases we want to support
"""

from .test_base import Sc2SetupTestBase
from .. import get_all_missions, mission_tables, options
from ..item import item_groups, item_tables, item_names
from ..mission_tables import SC2Race, SC2Mission, SC2Campaign, MissionFlag
from ..options import (
    EnabledCampaigns, MasteryLocations, MissionOrder, EnableRaceSwapVariants, ShuffleCampaigns,
    ShuffleNoBuild, StarterUnit, RequiredTactics, KerriganPresence, KerriganLevelItemDistribution, GrantStoryTech,
    GrantStoryLevels, BasebustLocations, ChallengeLocations, DifficultyCurve, EnableMorphling, ExcludeOverpoweredItems,
    ExcludeVeryHardMissions, ExtraLocations, GenericUpgradeItems, GenericUpgradeResearch, GenericUpgradeResearchSpeedup,
    KerriganPrimalStatus, KeyMode, MissionOrderScouting, EnableMissionRaceBalancing,
    NovaGhostOfAChanceVariant, PreventativeLocations, SpeedrunLocations, TakeOverAIAllies, VanillaItemsOnly
)


class TestSupportedUseCases(Sc2SetupTestBase):
    def test_vanilla_all_campaigns_generates(self) -> None:
        world_options = {
            'mission_order': options.MissionOrder.option_vanilla,
            'enabled_campaigns': EnabledCampaigns.valid_keys,
        }

        self.generate_world(world_options)
        world_regions = [region.name for region in self.multiworld.regions if region.name != "Menu"]

        self.assertEqual(len(world_regions), 83, "Unexpected number of missions for vanilla mission order")

    def test_terran_with_nco_units_only_generates(self):
        world_options = {
            'enabled_campaigns': {
                SC2Campaign.WOL.campaign_name,
                SC2Campaign.NCO.campaign_name
            },
            'excluded_items': {
                item_groups.ItemGroupNames.TERRAN_UNITS: 0,
            },
            'unexcluded_items': {
                item_groups.ItemGroupNames.NCO_UNITS: 0,
            },
            'max_number_of_upgrades': 2,
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
            'enabled_campaigns': {
                SC2Campaign.NCO.campaign_name
            },
            'shuffle_no_build': options.ShuffleNoBuild.option_false,
            'mission_order': options.MissionOrder.option_mini_campaign,
        }

        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        missions = get_all_missions(self.world.custom_mission_order)

        self.assertNotIn(mission_tables.SC2Mission.THE_ESCAPE, missions)
        self.assertNotIn(mission_tables.SC2Mission.IN_THE_ENEMY_S_SHADOW, missions)
        for mission in missions:
            self.assertEqual(mission_tables.SC2Campaign.NCO, mission.campaign)

    def test_terran_with_nco_upgrades_units_only_generates(self):
        world_options = {
            'enabled_campaigns': {
                SC2Campaign.WOL.campaign_name,
                SC2Campaign.NCO.campaign_name
            },
            'mission_order': options.MissionOrder.option_vanilla_shuffled,
            'excluded_items': {
                item_groups.ItemGroupNames.TERRAN_ITEMS: 0,
            },
            'unexcluded_items': {
                item_groups.ItemGroupNames.NCO_MAX_PROGRESSIVE_ITEMS: 0,
                item_groups.ItemGroupNames.NCO_MIN_PROGRESSIVE_ITEMS: 1,
            },
            'excluded_missions': [
                # These missions have trouble fulfilling Terran Power Rating under these terms
                SC2Mission.SUPERNOVA.mission_name,
                SC2Mission.WELCOME_TO_THE_JUNGLE.mission_name,
                SC2Mission.TROUBLE_IN_PARADISE.mission_name,
            ],
            'mastery_locations': MasteryLocations.option_disabled,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool + self.multiworld.precollected_items[1]]
        self.assertTrue(world_item_names)
        missions = get_all_missions(self.world.custom_mission_order)

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
            'enabled_campaigns': {
                SC2Campaign.WOL.campaign_name,
                SC2Campaign.NCO.campaign_name
            },
            'excluded_missions': [
                mission.mission_name for mission in mission_tables.SC2Mission
                if mission.campaign == mission_tables.SC2Campaign.WOL
                    and mission.mission_name not in (mission_tables.SC2Mission.LIBERATION_DAY.mission_name, mission_tables.SC2Mission.THE_OUTLAWS.mission_name)
            ],
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'mastery_locations': options.MasteryLocations.option_disabled,
            'vanilla_items_only': True,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]

        self.assertTrue(item_names)
        self.assertNotIn(item_names.LIBERATOR, world_item_names)
        self.assertNotIn(item_names.MARAUDER_PROGRESSIVE_STIMPACK, world_item_names)
        self.assertNotIn(item_names.HELLION_HELLBAT, world_item_names)
        self.assertNotIn(item_names.BATTLECRUISER_CLOAK, world_item_names)
    
    def test_free_protoss_only_generates(self) -> None:
        world_options = {
            'enabled_campaigns': {
                SC2Campaign.PROPHECY.campaign_name,
                SC2Campaign.PROLOGUE.campaign_name
            },
            # todo(mm): Currently, these settings don't generate on grid because there are not enough EASY missions
            'mission_order': options.MissionOrder.option_vanilla_shuffled,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(world_item_names)
        missions = get_all_missions(self.world.custom_mission_order)

        self.assertEqual(len(missions), 7, "Wrong number of missions in free protoss seed")
        for mission in missions:
            self.assertIn(mission.campaign, (mission_tables.SC2Campaign.PROLOGUE, mission_tables.SC2Campaign.PROPHECY))
        for item_name in world_item_names:
            self.assertIn(item_tables.item_table[item_name].race, (mission_tables.SC2Race.ANY, mission_tables.SC2Race.PROTOSS))

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
            'selected_races': {
                SC2Race.TERRAN.get_title(),
                SC2Race.ZERG.get_title(),
            },
            'enabled_campaigns': options.EnabledCampaigns.valid_keys,
            'mission_order': options.MissionOrder.option_grid,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        world_regions = [region.name for region in self.multiworld.regions]
        world_regions.remove('Menu')

        for item_name in world_item_names:
            self.assertNotEqual(item_tables.item_table[item_name].race, mission_tables.SC2Race.PROTOSS, f"{item_name} is a PROTOSS item!")
        for region in world_regions:
            self.assertNotIn(mission_tables.lookup_name_to_mission[region].campaign, 
                             (mission_tables.SC2Campaign.LOTV, mission_tables.SC2Campaign.PROPHECY, mission_tables.SC2Campaign.PROLOGUE),
                             f"{region} is a PROTOSS mission!")

    def test_excluding_terran_excludes_campaigns_and_items(self) -> None:
        world_options = {
            'selected_races': {
                SC2Race.ZERG.get_title(),
                SC2Race.PROTOSS.get_title(),
            },
            'enabled_campaigns': EnabledCampaigns.valid_keys,
            'mission_order': options.MissionOrder.option_grid,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        world_regions = [region.name for region in self.multiworld.regions]
        world_regions.remove('Menu')

        for item_name in world_item_names:
            self.assertNotEqual(item_tables.item_table[item_name].race, mission_tables.SC2Race.TERRAN,
                                f"{item_name} is a TERRAN item!")
        for region in world_regions:
            self.assertNotIn(mission_tables.lookup_name_to_mission[region].campaign,
                             (mission_tables.SC2Campaign.WOL, mission_tables.SC2Campaign.NCO),
                             f"{region} is a TERRAN mission!")

    def test_excluding_zerg_excludes_campaigns_and_items(self) -> None:
        world_options = {
            'selected_races': {
                SC2Race.TERRAN.get_title(),
                SC2Race.PROTOSS.get_title(),
            },
            'enabled_campaigns': EnabledCampaigns.valid_keys,
            'mission_order': options.MissionOrder.option_grid,
            'excluded_missions': [
                SC2Mission.THE_INFINITE_CYCLE.mission_name
            ]
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        world_regions = [region.name for region in self.multiworld.regions]
        world_regions.remove('Menu')

        for item_name in world_item_names:
            self.assertNotEqual(item_tables.item_table[item_name].race, mission_tables.SC2Race.ZERG,
                                f"{item_name} is a ZERG item!")
        # have to manually exclude the only non-zerg HotS mission...
        for region in filter(lambda region: region != "With Friends Like These", world_regions):
            self.assertNotIn(mission_tables.lookup_name_to_mission[region].campaign,
                             ([mission_tables.SC2Campaign.HOTS]),
                             f"{region} is a ZERG mission!")

    def test_excluding_faction_on_vanilla_order_excludes_epilogue(self) -> None:
        world_options = {
            'selected_races': {
                SC2Race.TERRAN.get_title(),
                SC2Race.PROTOSS.get_title(),
            },
            'enabled_campaigns': EnabledCampaigns.valid_keys,
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
            'selected_races': options.SelectedRaces.valid_keys,
            'enable_race_swap': options.EnableRaceSwapVariants.option_pick_one,
            'enabled_campaigns': {
                SC2Campaign.WOL.campaign_name,
            },
            'mission_order': options.MissionOrder.option_grid,
            'excluded_missions': [mission_tables.SC2Mission.ZERO_HOUR.mission_name],
        }

        self.generate_world(world_options)
        world_regions = [region.name for region in self.multiworld.regions]
        world_regions.remove('Menu')
        NUM_WOL_MISSIONS = len([mission for mission in SC2Mission if mission.campaign == SC2Campaign.WOL and MissionFlag.RaceSwap not in mission.flags])
        races = set(mission_tables.lookup_name_to_mission[mission].race for mission in world_regions)

        self.assertEqual(len(world_regions), NUM_WOL_MISSIONS)
        self.assertTrue(SC2Race.ZERG in races or SC2Race.PROTOSS in races)

    def test_start_inventory_upgrade_level_includes_only_correct_bundle(self) -> None:
        world_options = {
            'start_inventory': {
                item_groups.ItemGroupNames.TERRAN_GENERIC_UPGRADES: 1,
            },
            'locked_items': {
                # One unit of each class to guarantee upgrades are available
                item_names.MARINE: 1,
                item_names.VULTURE: 1,
                item_names.BANSHEE: 1,
            },
            'generic_upgrade_items': options.GenericUpgradeItems.option_bundle_unit_class,
            'selected_races': {
                SC2Race.TERRAN.get_title(),
            },
            'enable_race_swap': options.EnableRaceSwapVariants.option_disabled,
            'enabled_campaigns': {
                SC2Campaign.WOL.campaign_name,
            },
            'mission_order': options.MissionOrder.option_grid,
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        world_item_names = [item.name for item in self.multiworld.itempool]
        start_inventory = [item.name for item in self.multiworld.precollected_items[self.player]]

        # Start inventory
        self.assertIn(item_names.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE, start_inventory)
        self.assertIn(item_names.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE, start_inventory)
        self.assertIn(item_names.PROGRESSIVE_TERRAN_SHIP_UPGRADE, start_inventory)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, start_inventory)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR, start_inventory)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON, start_inventory)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR, start_inventory)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, start_inventory)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR, start_inventory)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_ARMOR_UPGRADE, start_inventory)

        # Additional items in pool -- standard tactics will require additional levels
        self.assertIn(item_names.PROGRESSIVE_TERRAN_INFANTRY_UPGRADE, world_item_names)
        self.assertIn(item_names.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE, world_item_names)
        self.assertIn(item_names.PROGRESSIVE_TERRAN_SHIP_UPGRADE, world_item_names)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, world_item_names)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR, world_item_names)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON, world_item_names)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR, world_item_names)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, world_item_names)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR, world_item_names)
        self.assertNotIn(item_names.PROGRESSIVE_TERRAN_ARMOR_UPGRADE, world_item_names)

    def test_kerrigan_max_active_abilities(self):
        target_number: int = 8
        world_options = {
            **self.ALL_CAMPAIGNS,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'selected_races': {
                SC2Race.ZERG.get_title(),
            },
            'enable_race_swap': options.EnableRaceSwapVariants.option_shuffle_all,
            'kerrigan_max_active_abilities': target_number,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        kerrigan_actives = [item_name for item_name in world_item_names if item_name in item_groups.kerrigan_active_abilities]

        self.assertLessEqual(len(kerrigan_actives), target_number)

    def test_kerrigan_max_passive_abilities(self):
        target_number: int = 3
        world_options = {
            **self.ALL_CAMPAIGNS,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'selected_races': {
                SC2Race.ZERG.get_title(),
            },
            'enable_race_swap': options.EnableRaceSwapVariants.option_shuffle_all,
            'kerrigan_max_passive_abilities': target_number,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        kerrigan_passives = [item_name for item_name in world_item_names if item_name in item_groups.kerrigan_passives]

        self.assertLessEqual(len(kerrigan_passives), target_number)

    def test_spear_of_adun_max_active_abilities(self):
        target_number: int = 8
        world_options = {
            **self.ALL_CAMPAIGNS,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'selected_races': {
                SC2Race.PROTOSS.get_title(),
            },
            'enable_race_swap': options.EnableRaceSwapVariants.option_shuffle_all,
            'spear_of_adun_max_active_abilities': target_number,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        spear_of_adun_actives = [item_name for item_name in world_item_names if item_name in item_tables.spear_of_adun_calldowns]

        self.assertLessEqual(len(spear_of_adun_actives), target_number)


    def test_spear_of_adun_max_autocasts(self):
        target_number: int = 2
        world_options = {
            **self.ALL_CAMPAIGNS,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'selected_races': {
                SC2Race.PROTOSS.get_title(),
            },
            'enable_race_swap': options.EnableRaceSwapVariants.option_shuffle_all,
            'spear_of_adun_max_passive_abilities': target_number,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        spear_of_adun_autocasts = [item_name for item_name in world_item_names if item_name in item_tables.spear_of_adun_castable_passives]

        self.assertLessEqual(len(spear_of_adun_autocasts), target_number)


    def test_nova_max_weapons(self):
        target_number: int = 3
        world_options = {
            **self.ALL_CAMPAIGNS,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'selected_races': {
                SC2Race.TERRAN.get_title(),
            },
            'enable_race_swap': options.EnableRaceSwapVariants.option_shuffle_all,
            'nova_max_weapons': target_number,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        nova_weapons = [item_name for item_name in world_item_names if item_name in item_groups.nova_weapons]

        self.assertLessEqual(len(nova_weapons), target_number)


    def test_nova_max_gadgets(self):
        target_number: int = 3
        world_options = {
            **self.ALL_CAMPAIGNS,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'selected_races': {
                SC2Race.TERRAN.get_title(),
            },
            'enable_race_swap': options.EnableRaceSwapVariants.option_shuffle_all,
            'nova_max_gadgets': target_number,
        }

        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        nova_gadgets = [item_name for item_name in world_item_names if item_name in item_groups.nova_gadgets]

        self.assertLessEqual(len(nova_gadgets), target_number)
    
    def test_mercs_only(self) -> None:
        world_options = {
            **self.ALL_CAMPAIGNS,
            'selected_races': [
                SC2Race.TERRAN.get_title(),
                SC2Race.ZERG.get_title(),
            ],
            'required_tactics': options.RequiredTactics.option_any_units,
            'excluded_items': {
                item_groups.ItemGroupNames.TERRAN_UNITS: 0,
                item_groups.ItemGroupNames.ZERG_UNITS: 0,
            },
            'unexcluded_items': {
                item_groups.ItemGroupNames.TERRAN_MERCENARIES: 0,
                item_groups.ItemGroupNames.ZERG_MERCENARIES: 0,
            },
            'start_inventory': {
                item_names.PROGRESSIVE_FAST_DELIVERY: 1,
                item_names.ROGUE_FORCES: 1,
                item_names.UNRESTRICTED_MUTATION: 1,
                item_names.EVOLUTIONARY_LEAP: 1,
            },
            'mission_order': options.MissionOrder.option_grid,
            'excluded_missions': [
                SC2Mission.ENEMY_WITHIN.mission_name,  # Requires a unit for Niadra to build
            ],
        }
        self.generate_world(world_options)
        world_item_names = [item.name for item in self.multiworld.itempool]
        terran_nonmerc_units = tuple(
            item_name
            for item_name in world_item_names
            if item_name in item_groups.terran_units and item_name not in item_groups.terran_mercenaries
        )
        zerg_nonmerc_units = tuple(
            item_name
            for item_name in world_item_names
            if item_name in item_groups.zerg_units and item_name not in item_groups.zerg_mercenaries
        )

        self.assertTupleEqual(terran_nonmerc_units, ())
        self.assertTupleEqual(zerg_nonmerc_units, ())

    def test_zerg_hots_no_terran_items(self) -> None:
        # The actual situation the bug got caught
        world_options = {
            'basebust_locations': BasebustLocations.option_enabled,
            'challenge_locations': ChallengeLocations.option_enabled,
            'difficulty_curve': DifficultyCurve.option_standard,
            'enable_morphling': EnableMorphling.option_false,
            'enable_race_swap': EnableRaceSwapVariants.option_disabled,
            'enabled_campaigns': [SC2Campaign.HOTS.campaign_name],
            'ensure_generic_items': 25,
            'exclude_overpowered_items': ExcludeOverpoweredItems.option_false,
            'exclude_very_hard_missions': ExcludeVeryHardMissions.option_default,
            'excluded_missions': [
                SC2Mission.SUPREME.mission_name
            ],
            'extra_locations': ExtraLocations.option_enabled,
            'generic_upgrade_items': GenericUpgradeItems.option_individual_items,
            'generic_upgrade_missions': 0,
            'generic_upgrade_research': GenericUpgradeResearch.option_auto_in_no_build,
            'generic_upgrade_research_speedup': GenericUpgradeResearchSpeedup.option_false,
            'grant_story_levels': GrantStoryLevels.option_disabled,
            'grant_story_tech': GrantStoryTech.option_no_grant,
            'kerrigan_level_item_distribution': KerriganLevelItemDistribution.option_size_14,
            'kerrigan_level_item_sum': 86,
            'kerrigan_levels_per_mission_completed': 0,
            'kerrigan_levels_per_mission_completed_cap': -1,
            'kerrigan_max_active_abilities': 12,
            'kerrigan_max_passive_abilities': 5,
            'kerrigan_presence': KerriganPresence.option_vanilla,
            'kerrigan_primal_status': KerriganPrimalStatus.option_vanilla,
            'kerrigan_total_level_cap': -1,
            'key_mode': KeyMode.option_progressive_questlines,
            'mastery_locations': MasteryLocations.option_disabled,
            'max_number_of_upgrades': -1,
            'max_upgrade_level': 4,
            'maximum_campaign_size': 40,
            'min_number_of_upgrades': 2,
            'mission_order': MissionOrder.option_mini_campaign,
            'mission_order_scouting': MissionOrderScouting.option_none,
            'mission_race_balancing': EnableMissionRaceBalancing.option_semi_balanced,
            'nova_ghost_of_a_chance_variant': NovaGhostOfAChanceVariant.option_wol,
            'preventative_locations': PreventativeLocations.option_enabled,
            'required_tactics': RequiredTactics.option_standard,
            'shuffle_campaigns': ShuffleCampaigns.option_true,
            'shuffle_no_build': ShuffleNoBuild.option_true,
            'speedrun_locations': SpeedrunLocations.option_disabled,
            'start_primary_abilities': 0,
            'starter_unit': StarterUnit.option_balanced,
            'starting_supply_per_item': 2,
            'take_over_ai_allies': TakeOverAIAllies.option_false,
            'vanilla_items_only': VanillaItemsOnly.option_false,
            'victory_cache': 0,
        }
        self.generate_world(world_options)

        world_item_names = [item.name for item in self.multiworld.itempool]

        self.assertNotIn(item_names.COMMAND_CENTER_SCANNER_SWEEP, world_item_names)
        self.assertNotIn(item_names.COMMAND_CENTER_EXTRA_SUPPLIES, world_item_names)
        self.assertNotIn(item_names.ULTRA_CAPACITORS, world_item_names)
        self.assertNotIn(item_names.ORBITAL_DEPOTS, world_item_names)
        self.assertNotIn(item_names.DOMINION_TROOPER, world_item_names)

    def test_all_kerrigan_missions_are_nobuild_and_grant_story_tech_is_on(self) -> None:
        # The actual situation the bug got caught
        world_options = {
            'mission_order': MissionOrder.option_vanilla_shuffled,
            'selected_races': [
                SC2Race.TERRAN.get_title(),
                SC2Race.ZERG.get_title(),
                SC2Race.PROTOSS.get_title(),
            ],
            'enabled_campaigns': [
                SC2Campaign.WOL.campaign_name,
                SC2Campaign.PROPHECY.campaign_name,
                SC2Campaign.HOTS.campaign_name,
                SC2Campaign.PROLOGUE.campaign_name,
                SC2Campaign.LOTV.campaign_name,
                SC2Campaign.EPILOGUE.campaign_name,
                SC2Campaign.NCO.campaign_name,
            ],
            'enable_race_swap': EnableRaceSwapVariants.option_shuffle_all_non_vanilla, # Causes no build Kerrigan missions to be present, only nobuilds remain
            'shuffle_campaigns': ShuffleCampaigns.option_true,
            'shuffle_no_build': ShuffleNoBuild.option_true,
            'starter_unit': StarterUnit.option_balanced,
            'required_tactics': RequiredTactics.option_standard,
            'kerrigan_presence': KerriganPresence.option_vanilla,
            'kerrigan_levels_per_mission_completed': 0,
            'kerrigan_levels_per_mission_completed_cap': -1,
            'kerrigan_level_item_sum': 87,
            'kerrigan_level_item_distribution': KerriganLevelItemDistribution.option_size_7,
            'kerrigan_total_level_cap': -1,
            'start_primary_abilities': 0,
            'grant_story_tech': GrantStoryTech.option_grant,
            'grant_story_levels': GrantStoryLevels.option_additive,
        }
        self.generate_world(world_options)
        # Just check that the world itself generates under those rules and no exception is thrown
