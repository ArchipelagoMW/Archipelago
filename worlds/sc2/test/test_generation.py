"""
Unit tests for world generation
"""
from typing import *
from .test_base import Sc2SetupTestBase

from .. import Options, MissionTables, ItemNames, Items, ItemGroups
from .. import get_all_missions


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
        self.assertTrue(self.multiworld.itempool)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn(ItemNames.MARINE, item_names)
        self.assertIn(ItemNames.MARAUDER, item_names)
        self.assertIn(ItemNames.MEDIVAC, item_names)
        self.assertIn(ItemNames.FIREBAT, item_names)
        self.assertIn(ItemNames.ZEALOT, item_names)
        self.assertNotIn(ItemNames.ZERGLING, item_names)
        regen_biosteel_items = [x for x in item_names if x == ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL]
        self.assertEqual(len(regen_biosteel_items), 2)

    def test_unexcludes_cancel_out_excludes(self):
        options = {
            'grant_story_tech': True,
            'excluded_items': {
                ItemGroups.ItemGroupNames.NOVA_EQUIPMENT: 15,
                ItemNames.MARINE_PROGRESSIVE_STIMPACK: 1,
                ItemNames.MARAUDER_PROGRESSIVE_STIMPACK: 2,
                ItemNames.MARINE: 0,
                ItemNames.MARAUDER: 0,
                ItemNames.REAPER: 1,
                ItemNames.DIAMONDBACK: 0,
                ItemNames.HELLION: 1,
            },
            'unexcluded_items': {
                ItemNames.NOVA_PLASMA_RIFLE: 1,      # Necessary to pass logic
                ItemNames.NOVA_PULSE_GRENADES: 0,    # Necessary to pass logic
                ItemNames.NOVA_JUMP_SUIT_MODULE: 0,  # Necessary to pass logic
                ItemGroups.ItemGroupNames.BARRACKS_UNITS: 0,
                ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE: 1,
                ItemNames.HELLION: 1,
                ItemNames.MARINE_PROGRESSIVE_STIMPACK: 1,
                ItemNames.MARAUDER_PROGRESSIVE_STIMPACK: 0,
            },
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertIn(ItemNames.MARINE, item_names)
        self.assertIn(ItemNames.MARAUDER, item_names)
        self.assertIn(ItemNames.REAPER, item_names)
        self.assertEqual(item_names.count(ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE), 1, f"Stealth suit occurred the wrong number of times")
        self.assertIn(ItemNames.HELLION, item_names)
        self.assertEqual(item_names.count(ItemNames.MARINE_PROGRESSIVE_STIMPACK), 2, "Marine stimpacks weren't unexcluded")
        self.assertEqual(item_names.count(ItemNames.MARAUDER_PROGRESSIVE_STIMPACK), 2, "Marauder stimpacks weren't unexcluded")
        self.assertNotIn(ItemNames.DIAMONDBACK, item_names)
        self.assertNotIn(ItemNames.NOVA_BLAZEFIRE_GUNBLADE, item_names)
        self.assertNotIn(ItemNames.NOVA_ENERGY_SUIT_MODULE, item_names)

    def test_excluding_groups_excludes_all_items_in_group(self):
        options = {
            'excluded_items': [
                ItemGroups.ItemGroupNames.BARRACKS_UNITS.lower(),
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
        items = [(item.name, Items.item_table[item.name]) for item in self.multiworld.itempool]
        for item_name, item_data in items:
            self.assertNotIn(item_data.type, Items.ProtossItemType)
            self.assertNotIn(item_data.type, Items.ZergItemType)
            self.assertNotEqual(item_data.type, Items.TerranItemType.Nova_Gear)
            self.assertNotEqual(item_name, ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE)

    def test_starter_unit_populates_start_inventory(self):
        options = {
            'enable_wol_missions': True,
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'shuffle_no_build': Options.ShuffleNoBuild.option_false,
            'mission_order': Options.MissionOrder.option_grid,
            'starter_unit': Options.StarterUnit.option_any_starter_unit,
        }
        self.generate_world(options)
        self.assertTrue(self.multiworld.itempool)
        self.assertTrue(self.multiworld.precollected_items[self.player])

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

    def test_vanilla_items_only_excludes_terran_progressives(self) -> None:
        options = {
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(options)
        items = [(item.name, Items.item_table[item.name]) for item in self.multiworld.itempool]
        self.assertTrue(items)
        occurrences: Dict[str, int] = {}
        for item_name, _ in items:
            if item_name in ItemGroups.terran_progressive_items:
                if item_name in ItemGroups.nova_equipment:
                    # The option imposes no contraint on Nova equipment
                    continue
                occurrences.setdefault(item_name, 0)
                occurrences[item_name] += 1
                self.assertLessEqual(occurrences[item_name], 1, f"'{item_name}' unexpectedly appeared multiple times in the pool")

    def test_vanilla_items_only_includes_only_nova_equipment_and_vanilla_and_filler_items(self) -> None:
        options = {
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(options)
        items = [(item.name, Items.item_table[item.name]) for item in self.multiworld.itempool]
        self.assertTrue(items)
        for item_name, item_data in items:
            if item_data.quantity == 0:
                continue
            self.assertIn(item_name, ItemGroups.vanilla_items + ItemGroups.nova_equipment)

    def test_evil_awoken_with_vanilla_items_only_generates(self) -> None:
        options = {
            'enable_wol_missions': False,
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': False,
            'enable_epilogue_missions': False,
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(options)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(item_names)
        self.assertTrue(self.world.get_region(MissionTables.SC2Mission.EVIL_AWOKEN.mission_name))

    def test_enemy_within_and_no_zerg_build_missions_generates(self) -> None:
        options = {
            # including WoL to allow for valid goal missions
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'excluded_missions': [
                mission.mission_name for mission in MissionTables.SC2Mission
                if MissionTables.MissionFlag.Zerg in mission.flags
                    and MissionTables.MissionFlag.NoBuild not in mission.flags
            ],
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'vanilla_items_only': True,
        }
        self.generate_world(options)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(item_names)
        self.assertTrue(self.world.get_region(MissionTables.SC2Mission.ENEMY_WITHIN.mission_name))
        self.assertNotIn(ItemNames.ULTRALISK, item_names)
        self.assertNotIn(ItemNames.SWARM_QUEEN, item_names)
        self.assertNotIn(ItemNames.MUTALISK, item_names)
        self.assertNotIn(ItemNames.CORRUPTOR, item_names)
        self.assertNotIn(ItemNames.SCOURGE, item_names)

    def test_soa_items_are_included_in_wol_when_presence_set_to_everywhere(self) -> None:
        options = {
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_hots_missions': False,
            'enable_epilogue_missions': False,
            'spear_of_adun_presence': Options.SpearOfAdunPresence.option_everywhere,
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'excluded_items': {ItemGroups.ItemGroupNames.BARRACKS_UNITS: 0},
        }
        self.generate_world(options)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(item_names)
        soa_items_in_pool = [item_name for item_name in item_names if Items.item_table[item_name].type == Items.ProtossItemType.Spear_Of_Adun]
        self.assertGreater(len(soa_items_in_pool), 5)

    def test_lotv_only_doesnt_include_kerrigan_items_with_grant_story_tech(self) -> None:
        options = {
            'enable_wol_missions': False,
            'enable_nco_missions': False,
            'enable_prophecy_missions': False,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': True,
            'enable_hots_missions': False,
            'enable_epilogue_missions': False,
            'mission_order': Options.MissionOrder.option_grid,
            'maximum_campaign_size': Options.MaximumCampaignSize.range_end,
            'accessibility': 'locations',
            'grant_story_tech': Options.GrantStoryTech.option_true,
        }
        self.generate_world(options)
        missions = get_all_missions(self.world.mission_req_table)
        self.assertIn(MissionTables.SC2Mission.TEMPLE_OF_UNIFICATION, missions)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(item_names)
        kerrigan_items_in_pool = set(ItemGroups.kerrigan_abilities).intersection(item_names)
        self.assertFalse(kerrigan_items_in_pool)
        kerrigan_passives_in_pool = set(ItemGroups.kerrigan_passives).intersection(item_names)
        self.assertFalse(kerrigan_passives_in_pool)

    def test_excluding_zerg_units_with_morphling_enabled_doesnt_exclude_aspects(self) -> None:
        options = {
            'enable_wol_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
            'required_tactics': Options.RequiredTactics.option_no_logic,
            'enable_morphling': Options.EnableMorphling.option_true,
            'excluded_items': [
                ItemGroups.ItemGroupNames.ZERG_UNITS.lower()
            ],
            'unexcluded_items': [
                ItemGroups.ItemGroupNames.ZERG_MORPHS.lower()
            ]
        }
        self.generate_world(options)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(item_names)
        aspects_in_pool = list(set(item_names).intersection(set(ItemGroups.zerg_morphs)))
        self.assertTrue(aspects_in_pool)
        units_in_pool = list(set(item_names).intersection(set(ItemGroups.zerg_units))
                             .difference(set(ItemGroups.zerg_morphs)))
        self.assertFalse(units_in_pool)

    def test_excluding_zerg_units_with_morphling_disabled_should_exclude_aspects(self) -> None:
        options = {
            'enable_wol_missions': False,
            'enable_prophecy_missions': False,
            'enable_hots_missions': True,
            'enable_lotv_prologue_missions': False,
            'enable_lotv_missions': False,
            'enable_epilogue_missions': False,
            'enable_nco_missions': False,
            'required_tactics': Options.RequiredTactics.option_no_logic,
            'enable_morphling': Options.EnableMorphling.option_false,
            'excluded_items': [
                ItemGroups.ItemGroupNames.ZERG_UNITS.lower()
            ],
            'unexcluded_items': [
                ItemGroups.ItemGroupNames.ZERG_MORPHS.lower()
            ]
        }
        self.generate_world(options)
        item_names = [item.name for item in self.multiworld.itempool]
        self.assertTrue(item_names)
        aspects_in_pool = list(set(item_names).intersection(set(ItemGroups.zerg_morphs)))
        self.assertFalse(aspects_in_pool)
        units_in_pool = list(set(item_names).intersection(set(ItemGroups.zerg_units))
                             .difference(set(ItemGroups.zerg_morphs)))
        self.assertFalse(units_in_pool)

