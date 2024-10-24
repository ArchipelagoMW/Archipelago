"""
Unit tests for world generation
"""
from typing import *
from .test_base import Sc2SetupTestBase

from .. import item_groups, item_names, items, mission_groups, mission_tables, options, locations
from .. import get_all_missions, get_first_mission


class TestItemFiltering(Sc2SetupTestBase):
    def test_explicit_locks_excludes_interact_and_set_flags(self):
        world_options = {
            'locked_items': {
                item_names.MARINE: 0,
                item_names.MARAUDER: 0,
                item_names.MEDIVAC: 1,
                item_names.FIREBAT: 1,
                item_names.ZEALOT: 0,
                item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL: 2,
            },
            'excluded_items': {
                item_names.MARINE: 0,
                item_names.MARAUDER: 0,
                item_names.MEDIVAC: 0,
                item_names.FIREBAT: 1,
                item_names.ZERGLING: 0,
                item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL: 2,
            }
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertIn(item_names.MARINE, itempool)
        self.assertIn(item_names.MARAUDER, itempool)
        self.assertIn(item_names.MEDIVAC, itempool)
        self.assertIn(item_names.FIREBAT, itempool)
        self.assertIn(item_names.ZEALOT, itempool)
        self.assertNotIn(item_names.ZERGLING, itempool)
        regen_biosteel_items = [x for x in itempool if x == item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL]
        self.assertEqual(len(regen_biosteel_items), 2)

    def test_unexcludes_cancel_out_excludes(self):
        world_options = {
            'grant_story_tech': True,
            'excluded_items': {
                item_groups.ItemGroupNames.NOVA_EQUIPMENT: 15,
                item_names.MARINE_PROGRESSIVE_STIMPACK: 1,
                item_names.MARAUDER_PROGRESSIVE_STIMPACK: 2,
                item_names.MARINE: 0,
                item_names.MARAUDER: 0,
                item_names.REAPER: 1,
                item_names.DIAMONDBACK: 0,
                item_names.HELLION: 1,
                # Additional excludes to increase the likelihood that unexcluded items actually appear
                item_groups.ItemGroupNames.STARPORT_UNITS: 0,
                item_names.WARHOUND: 0,
                item_names.VULTURE: 0,
                item_names.WIDOW_MINE: 0,
                item_names.THOR: 0,
                item_names.GHOST: 0,
                item_names.SPECTRE: 0,
                item_groups.ItemGroupNames.MENGSK_UNITS: 0,
                item_groups.ItemGroupNames.TERRAN_VETERANCY_UNITS: 0,
            },
            'unexcluded_items': {
                item_names.NOVA_PLASMA_RIFLE: 1,      # Necessary to pass logic
                item_names.NOVA_PULSE_GRENADES: 0,    # Necessary to pass logic
                item_names.NOVA_JUMP_SUIT_MODULE: 0,  # Necessary to pass logic
                item_groups.ItemGroupNames.BARRACKS_UNITS: 0,
                item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE: 1,
                item_names.HELLION: 1,
                item_names.MARINE_PROGRESSIVE_STIMPACK: 1,
                item_names.MARAUDER_PROGRESSIVE_STIMPACK: 0,
                # Additional unexcludes for logic
                item_names.MEDIVAC: 0,
                item_names.BATTLECRUISER: 0,
                item_names.SCIENCE_VESSEL: 0,
            },
            # Terran-only
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_epilogue_missions': False,
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertIn(item_names.MARINE, itempool)
        self.assertIn(item_names.MARAUDER, itempool)
        self.assertIn(item_names.REAPER, itempool)
        self.assertEqual(itempool.count(item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE), 1, f"Stealth suit occurred the wrong number of times")
        self.assertIn(item_names.HELLION, itempool)
        self.assertEqual(itempool.count(item_names.MARINE_PROGRESSIVE_STIMPACK), 2, f"Marine stimpacks weren't unexcluded  (seed {self.multiworld.seed})")
        self.assertEqual(itempool.count(item_names.MARAUDER_PROGRESSIVE_STIMPACK), 2, f"Marauder stimpacks weren't unexcluded (seed {self.multiworld.seed})")
        self.assertNotIn(item_names.DIAMONDBACK, itempool)
        self.assertNotIn(item_names.NOVA_BLAZEFIRE_GUNBLADE, itempool)
        self.assertNotIn(item_names.NOVA_ENERGY_SUIT_MODULE, itempool)

    def test_excluding_groups_excludes_all_items_in_group(self):
        world_options = {
            'excluded_items': [
                item_groups.ItemGroupNames.BARRACKS_UNITS.lower(),
            ]
        }
        self.generate_world(world_options)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertIn(item_names.MARINE, self.world.options.excluded_items)
        for item_name in item_groups.barracks_units:
            self.assertNotIn(item_name, itempool)

    def test_excluding_mission_groups_excludes_all_missions_in_group(self):
        world_options = {
            'excluded_missions': [
                mission_groups.MissionGroupNames.HOTS_ZERUS_MISSIONS,
            ],
            'mission_order': options.MissionOrder.option_grid,
        }
        self.generate_world(world_options)
        missions = get_all_missions(self.world.custom_mission_order)
        self.assertTrue(missions)
        self.assertNotIn(mission_tables.SC2Mission.WAKING_THE_ANCIENT, missions)
        self.assertNotIn(mission_tables.SC2Mission.THE_CRUCIBLE, missions)
        self.assertNotIn(mission_tables.SC2Mission.SUPREME, missions)

    def test_excluding_campaigns_excludes_campaign_specific_items(self) -> None:
        world_options = {
            'enable_wol_missions': True,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        world_items = [(item.name, items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in world_items:
            self.assertNotIn(item_data.type, items.ProtossItemType)
            self.assertNotIn(item_data.type, items.ZergItemType)
            self.assertNotEqual(item_data.type, items.TerranItemType.Nova_Gear)
            self.assertNotEqual(item_name, item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE)

    def test_starter_unit_populates_start_inventory(self):
        world_options = {
            'enable_wol_missions': True,
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'shuffle_no_build': options.ShuffleNoBuild.option_false,
            'mission_order': options.MissionOrder.option_grid,
            'starter_unit': options.StarterUnit.option_any_starter_unit,
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        self.assertTrue(self.multiworld.precollected_items[self.player])

    def test_excluding_all_terran_missions_excludes_all_terran_items(self) -> None:
        world_options = {
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'excluded_missions': [
                mission.mission_name for mission in mission_tables.SC2Mission
                if mission_tables.MissionFlag.Terran in mission.flags
            ],
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        world_items = [(item.name, items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in world_items:
            self.assertNotIn(item_data.type, items.TerranItemType, f"Item '{item_name}' included when all terran missions are excluded")

    def test_excluding_all_terran_build_missions_excludes_all_terran_units(self) -> None:
        world_options = {
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'excluded_missions': [
                mission.mission_name for mission in mission_tables.SC2Mission
                if mission_tables.MissionFlag.Terran in mission.flags
                    and mission_tables.MissionFlag.NoBuild not in mission.flags
            ],
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        world_items = [(item.name, items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in world_items:
            self.assertNotEqual(item_data.type, items.TerranItemType.Unit, f"Item '{item_name}' included when all terran build missions are excluded")
            self.assertNotEqual(item_data.type, items.TerranItemType.Mercenary, f"Item '{item_name}' included when all terran build missions are excluded")
            self.assertNotEqual(item_data.type, items.TerranItemType.Building, f"Item '{item_name}' included when all terran build missions are excluded")

    def test_excluding_all_zerg_and_kerrigan_missions_excludes_all_zerg_items(self) -> None:
        world_options = {
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'excluded_missions': [
                mission.mission_name for mission in mission_tables.SC2Mission
                if (mission_tables.MissionFlag.Kerrigan | mission_tables.MissionFlag.Zerg) & mission.flags
            ],
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        world_items = [(item.name, items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in world_items:
            self.assertNotIn(item_data.type, items.ZergItemType, f"Item '{item_name}' included when all zerg missions are excluded")

    def test_excluding_all_zerg_build_missions_excludes_zerg_units(self) -> None:
        world_options = {
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'excluded_missions': [
                *[mission.mission_name
                    for mission in mission_tables.SC2Mission
                    if mission_tables.MissionFlag.Zerg in mission.flags
                        and mission_tables.MissionFlag.NoBuild not in mission.flags],
                mission_tables.SC2Mission.ENEMY_WITHIN.mission_name,
            ],
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        world_items = [(item.name, items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in world_items:
            self.assertNotEqual(item_data.type, items.ZergItemType.Unit, f"Item '{item_name}' included when all zerg build missions are excluded")
            self.assertNotEqual(item_data.type, items.ZergItemType.Mercenary, f"Item '{item_name}' included when all zerg build missions are excluded")

    def test_excluding_all_protoss_missions_excludes_all_protoss_items(self) -> None:
        world_options = {
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'excluded_missions': [
                *[mission.mission_name
                    for mission in mission_tables.SC2Mission
                    if mission_tables.MissionFlag.Protoss in mission.flags],
            ],
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        world_items = [(item.name, items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in world_items:
            self.assertNotIn(item_data.type, items.ProtossItemType, f"Item '{item_name}' included when all protoss missions are excluded")

    def test_excluding_all_protoss_build_missions_excludes_protoss_units(self) -> None:
        world_options = {
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'excluded_missions': [
                *[mission.mission_name
                    for mission in mission_tables.SC2Mission
                    if mission.race == mission_tables.SC2Race.PROTOSS
                        and mission_tables.MissionFlag.NoBuild not in mission.flags],
                mission_tables.SC2Mission.TEMPLAR_S_RETURN.mission_name,
            ],
        }
        self.generate_world(world_options)
        self.assertTrue(self.multiworld.itempool)
        world_items = [(item.name, items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in world_items:
            self.assertNotEqual(item_data.type, items.ProtossItemType.Unit, f"Item '{item_name}' included when all protoss build missions are excluded")
            self.assertNotEqual(item_data.type, items.ProtossItemType.Unit_2, f"Item '{item_name}' included when all protoss build missions are excluded")
            self.assertNotEqual(item_data.type, items.ProtossItemType.Building, f"Item '{item_name}' included when all protoss build missions are excluded")

    def test_vanilla_items_only_excludes_terran_progressives(self) -> None:
        world_options = {
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(world_options)
        world_items = [(item.name, items.item_table[item.name]) for item in self.multiworld.itempool]
        self.assertTrue(items)
        occurrences: Dict[str, int] = {}
        for item_name, _ in world_items:
            if item_name in item_groups.terran_progressive_items:
                if item_name in item_groups.nova_equipment:
                    # The option imposes no contraint on Nova equipment
                    continue
                occurrences.setdefault(item_name, 0)
                occurrences[item_name] += 1
                self.assertLessEqual(occurrences[item_name], 1, f"'{item_name}' unexpectedly appeared multiple times in the pool")

    def test_vanilla_items_only_includes_only_nova_equipment_and_vanilla_and_filler_items(self) -> None:
        world_options = {
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(world_options)
        world_items = [(item.name, items.item_table[item.name]) for item in self.multiworld.itempool]
        self.assertTrue(items)
        for item_name, item_data in world_items:
            if item_data.quantity == 0:
                continue
            self.assertIn(item_name, item_groups.vanilla_items + item_groups.nova_equipment)

    def test_evil_awoken_with_vanilla_items_only_generates(self) -> None:
        world_options = {
            'enable_wol_missions': False,
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_epilogue_missions': False,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(world_options)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertTrue(itempool)
        self.assertTrue(self.world.get_region(mission_tables.SC2Mission.EVIL_AWOKEN.mission_name))

    def test_enemy_within_and_no_zerg_build_missions_generates(self) -> None:
        world_options = {
            # including WoL to allow for valid goal missions
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'excluded_missions': [
                mission.mission_name for mission in mission_tables.SC2Mission
                if mission_tables.MissionFlag.Zerg in mission.flags
                    and mission_tables.MissionFlag.NoBuild not in mission.flags
            ],
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(world_options)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertTrue(itempool)
        self.assertTrue(self.world.get_region(mission_tables.SC2Mission.ENEMY_WITHIN.mission_name))
        self.assertNotIn(item_names.ULTRALISK, itempool)
        self.assertNotIn(item_names.SWARM_QUEEN, itempool)
        self.assertNotIn(item_names.MUTALISK, itempool)
        self.assertNotIn(item_names.CORRUPTOR, itempool)
        self.assertNotIn(item_names.SCOURGE, itempool)

    def test_soa_items_are_included_in_wol_when_presence_set_to_everywhere(self) -> None:
        world_options = {
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_hots_missions': False,
            'enable_epilogue_missions': False,
            'spear_of_adun_presence': options.SpearOfAdunPresence.option_everywhere,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'excluded_items': {item_groups.ItemGroupNames.BARRACKS_UNITS: 0},
        }
        self.generate_world(world_options)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertTrue(itempool)
        soa_items_in_pool = [item_name for item_name in itempool if items.item_table[item_name].type == items.ProtossItemType.Spear_Of_Adun]
        self.assertGreater(len(soa_items_in_pool), 5)

    def test_lotv_only_doesnt_include_kerrigan_items_with_grant_story_tech(self) -> None:
        world_options = {
            'enable_wol_missions': False,
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': True,
            'enable_hots_missions': False,
            'enable_epilogue_missions': False,
            'mission_order': options.MissionOrder.option_grid,
            'maximum_campaign_size': options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'grant_story_tech': options.GrantStoryTech.option_true,
        }
        self.generate_world(world_options)
        missions = get_all_missions(self.world.custom_mission_order)
        self.assertIn(mission_tables.SC2Mission.TEMPLE_OF_UNIFICATION, missions)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertTrue(itempool)
        kerrigan_items_in_pool = set(item_groups.kerrigan_abilities).intersection(itempool)
        self.assertFalse(kerrigan_items_in_pool)
        kerrigan_passives_in_pool = set(item_groups.kerrigan_passives).intersection(itempool)
        self.assertFalse(kerrigan_passives_in_pool)

    def test_excluding_zerg_units_with_morphling_enabled_doesnt_exclude_aspects(self) -> None:
        world_options = {
            'enable_wol_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
            'required_tactics': options.RequiredTactics.option_no_logic,
            'enable_morphling': options.EnableMorphling.option_true,
            'excluded_items': [
                item_groups.ItemGroupNames.ZERG_UNITS.lower()
            ],
            'unexcluded_items': [
                item_groups.ItemGroupNames.ZERG_MORPHS.lower()
            ]
        }
        self.generate_world(world_options)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertTrue(itempool)
        aspects_in_pool = list(set(itempool).intersection(set(item_groups.zerg_morphs)))
        self.assertTrue(aspects_in_pool)
        units_in_pool = list(set(itempool).intersection(set(item_groups.zerg_units))
                             .difference(set(item_groups.zerg_morphs)))
        self.assertFalse(units_in_pool)

    def test_excluding_zerg_units_with_morphling_disabled_should_exclude_aspects(self) -> None:
        world_options = {
            'enable_wol_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
            'required_tactics': options.RequiredTactics.option_no_logic,
            'enable_morphling': options.EnableMorphling.option_false,
            'excluded_items': [
                item_groups.ItemGroupNames.ZERG_UNITS.lower()
            ],
            'unexcluded_items': [
                item_groups.ItemGroupNames.ZERG_MORPHS.lower()
            ]
        }
        self.generate_world(world_options)
        itempool = [item.name for item in self.multiworld.itempool]
        self.assertTrue(itempool)
        aspects_in_pool = list(set(itempool).intersection(set(item_groups.zerg_morphs)))
        if item_names.OVERLORD_OVERSEER_ASPECT in aspects_in_pool:
            # Overseer morphs from Overlord, that's available always
            aspects_in_pool.remove(item_names.OVERLORD_OVERSEER_ASPECT)
        self.assertFalse(aspects_in_pool)
        units_in_pool = list(set(itempool).intersection(set(item_groups.zerg_units))
                             .difference(set(item_groups.zerg_morphs)))
        self.assertFalse(units_in_pool)

    def test_deprecated_orbital_command_not_present(self) -> None:
        """
        Orbital command got replaced. The item is still there for backwards compatibility.
        It shouldn't be generated.
        :return:
        """
        world_options = {}

        self.generate_world(world_options)
        itempool = [item.name for item in self.multiworld.itempool]

        self.assertTrue(itempool)
        self.assertNotIn(item_names.PROGRESSIVE_ORBITAL_COMMAND, itempool)

    def test_planetary_orbital_module_not_present_without_cc_spells(self) -> None:
        world_options = {
            "excluded_items": [
                item_names.COMMAND_CENTER_MULE,
                item_names.COMMAND_CENTER_SCANNER_SWEEP,
                item_names.COMMAND_CENTER_EXTRA_SUPPLIES
            ],
            "locked_items": [
                item_names.PLANETARY_FORTRESS
            ]
        }

        self.generate_world(world_options)
        itempool = [item.name for item in self.multiworld.itempool]

        self.assertTrue(itempool)
        self.assertIn(item_names.PLANETARY_FORTRESS, itempool)
        self.assertNotIn(item_names.PLANETARY_FORTRESS_ORBITAL_MODULE, itempool)

    def test_disabling_unit_nerfs_start_inventories_war_council_upgrades(self) -> None:
        world_options = {
            'enable_wol_missions': False,
            'enable_prophecy_missions': True,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': True,
            'enable_lotv_missions': True,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
            'mission_order': options.MissionOrder.option_grid,
            'nerf_unit_baselines': options.NerfUnitBaselines.option_false,
        }

        self.generate_world(world_options)
        itempool = [item.name for item in self.multiworld.itempool]
        war_council_item_names = set(item_groups.item_name_groups[item_groups.ItemGroupNames.WAR_COUNCIL])
        present_war_council_items = war_council_item_names.intersection(itempool)
        starting_inventory = [item.name for item in self.multiworld.precollected_items[self.player]]
        starting_war_council_items = war_council_item_names.intersection(starting_inventory)

        self.assertTrue(itempool)
        self.assertFalse(present_war_council_items, f'Found war council upgrades when nerf_unit_baselines is false: {present_war_council_items}')
        self.assertEqual(war_council_item_names, starting_war_council_items)

    def test_disabling_speedrun_locations_removes_them_from_the_pool(self) -> None:
        world_options = {
            'enable_wol_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
            'mission_order': options.MissionOrder.option_grid,
            'speedrun_locations': options.SpeedrunLocations.option_disabled,
            'preventative_locations': options.PreventativeLocations.option_resources,
        }

        self.generate_world(world_options)
        world_regions = list(self.multiworld.regions)
        world_location_names = [location.name for region in world_regions for location in region.locations]
        all_location_names = [location_data.name for location_data in locations.DEFAULT_LOCATION_LIST]
        speedrun_location_name = f"{mission_tables.SC2Mission.LAB_RAT.mission_name}: Win In Under 10 Minutes"
        self.assertIn(speedrun_location_name, all_location_names)
        self.assertNotIn(speedrun_location_name, world_location_names)

    def test_nco_and_wol_picks_correct_starting_mission(self):
        world_options = {
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
        }
        self.generate_world(world_options)
        self.assertEqual(get_first_mission(self.world, self.world.custom_mission_order), mission_tables.SC2Mission.LIBERATION_DAY)

    def test_excluding_mission_short_name_excludes_all_variants_of_mission(self):
        world_options = {
            'excluded_missions': [
                mission_tables.SC2Mission.ZERO_HOUR.mission_name.split(" (")[0]
            ],
            'mission_order': options.MissionOrder.option_grid,
            'selected_races': options.SelectRaces.option_all,
            'enable_race_swap': options.EnableRaceSwapVariants.option_shuffle_all,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
        }
        self.generate_world(world_options)
        missions = get_all_missions(self.world.custom_mission_order)
        self.assertTrue(missions)
        self.assertNotIn(mission_tables.SC2Mission.ZERO_HOUR, missions)
        self.assertNotIn(mission_tables.SC2Mission.ZERO_HOUR_Z, missions)
        self.assertNotIn(mission_tables.SC2Mission.ZERO_HOUR_P, missions)

    def test_excluding_mission_variant_excludes_just_that_variant(self):
        world_options = {
            'excluded_missions': [
                mission_tables.SC2Mission.ZERO_HOUR.mission_name
            ],
            'mission_order': options.MissionOrder.option_grid,
            'selected_races': options.SelectRaces.option_all,
            'enable_race_swap': options.EnableRaceSwapVariants.option_shuffle_all,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
        }
        self.generate_world(world_options)
        missions = get_all_missions(self.world.custom_mission_order)
        self.assertTrue(missions)
        self.assertNotIn(mission_tables.SC2Mission.ZERO_HOUR, missions)
        self.assertIn(mission_tables.SC2Mission.ZERO_HOUR_Z, missions)
        self.assertIn(mission_tables.SC2Mission.ZERO_HOUR_P, missions)

    def test_weapon_armor_upgrades(self):
        world_options = {
            # Vanilla WoL with all missions
            'mission_order': options.MissionOrder.option_vanilla,
            'starter_unit': options.StarterUnit.option_off,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
            'start_inventory': {
                item_names.GOLIATH: 1 # Don't fail with early item placement
            },
            'generic_upgrade_items': options.GenericUpgradeItems.option_individual_items,
            # Disable locations in order to cause item culling
            'vanilla_locations': options.VanillaLocations.option_disabled,
            'extra_locations': options.ExtraLocations.option_disabled,
            'challenge_locations': options.ChallengeLocations.option_disabled,
            'mastery_locations': options.MasteryLocations.option_disabled,
            'speedrun_locations': options.SpeedrunLocations.option_disabled,
            'preventative_locations': options.PreventativeLocations.option_disabled,
        }

        self.generate_world(world_options)
        starting_inventory = [item.name for item in self.multiworld.precollected_items[self.player]]
        itempool = [item.name for item in self.multiworld.itempool]
        world_items = starting_inventory + itempool
        vehicle_weapon_items = [x for x in world_items if x == item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON]

        # Under standard tactics you need to place L3 upgrades for available unit classes
        self.assertGreaterEqual(len(vehicle_weapon_items), 3)

    def test_weapon_armor_upgrades_with_bundles(self):
        world_options = {
            # Vanilla WoL with all missions
            'mission_order': options.MissionOrder.option_vanilla,
            'starter_unit': options.StarterUnit.option_off,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
            'start_inventory': {
                item_names.GOLIATH: 1 # Don't fail with early item placement
            },
            'generic_upgrade_items': options.GenericUpgradeItems.option_bundle_unit_class,
            # Disable locations in order to cause item culling
            'vanilla_locations': options.VanillaLocations.option_disabled,
            'extra_locations': options.ExtraLocations.option_disabled,
            'challenge_locations': options.ChallengeLocations.option_disabled,
            'mastery_locations': options.MasteryLocations.option_disabled,
            'speedrun_locations': options.SpeedrunLocations.option_disabled,
            'preventative_locations': options.PreventativeLocations.option_disabled,
        }

        self.generate_world(world_options)
        starting_inventory = [item.name for item in self.multiworld.precollected_items[self.player]]
        itempool = [item.name for item in self.multiworld.itempool]
        world_items = starting_inventory + itempool
        vehicle_upgrade_items = [x for x in world_items if x == item_names.PROGRESSIVE_TERRAN_VEHICLE_UPGRADE]

        # Under standard tactics you need to place L3 upgrades for available unit classes
        self.assertGreaterEqual(len(vehicle_upgrade_items), 3)

    def test_weapon_armor_upgrades_all_in_air(self):
        world_options = {
            # Vanilla WoL with all missions
            'mission_order': options.MissionOrder.option_vanilla,
            'starter_unit': options.StarterUnit.option_off,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
            'all_in_map': options.AllInMap.option_air, # All-in air forces an air unit
            'start_inventory': {
                item_names.GOLIATH: 1 # Don't fail with early item placement
            },
            'generic_upgrade_items': options.GenericUpgradeItems.option_individual_items,
            # Disable locations in order to cause item culling
            'vanilla_locations': options.VanillaLocations.option_disabled,
            'extra_locations': options.ExtraLocations.option_disabled,
            'challenge_locations': options.ChallengeLocations.option_disabled,
            'mastery_locations': options.MasteryLocations.option_disabled,
            'speedrun_locations': options.SpeedrunLocations.option_disabled,
            'preventative_locations': options.PreventativeLocations.option_disabled,
        }

        self.generate_world(world_options)
        starting_inventory = [item.name for item in self.multiworld.precollected_items[self.player]]
        itempool = [item.name for item in self.multiworld.itempool]
        world_items = starting_inventory + itempool
        vehicle_weapon_items = [x for x in world_items if x == item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON]
        ship_weapon_items = [x for x in world_items if x == item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON]

        # Under standard tactics you need to place L3 upgrades for available unit classes
        self.assertGreaterEqual(len(vehicle_weapon_items), 3)
        self.assertGreaterEqual(len(ship_weapon_items), 3)
