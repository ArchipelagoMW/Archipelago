import unittest
from random import Random

from worlds.AutoWorld import AutoWorldRegister
from test.general import setup_solo_multiworld

from ..Items import *
from ..Overcooked2Levels import (Overcooked2Dlc, Overcooked2Level, OverworldRegion, overworld_region_by_level,
                                 level_id_to_shortname)
from ..Logic import level_logic, overworld_region_logic, level_shuffle_factory
from ..Locations import oc2_location_name_to_id


class Overcooked2Test(unittest.TestCase):
    def testItems(self):
        self.assertEqual(len(item_name_to_id), len(item_id_to_name))
        self.assertEqual(len(item_name_to_id), len(item_table))

        previous_item = None
        for item_name in item_table.keys():
            item: Item = item_table[item_name]
            self.assertGreaterEqual(item.code, oc2_base_id, "Overcooked Item ID out of range")
            self.assertLessEqual(item.code, item_table["Emote Wheel"].code, "Overcooked Item ID out of range")

            if previous_item is not None:
                self.assertEqual(item.code, previous_item + 1,
                                 f"Overcooked Item ID noncontinguous: {item.code-oc2_base_id}")
            previous_item = item.code

        self.assertEqual(item_table["Ok Emote"].code - item_table["Cooking Emote"].code,
                         5, "Overcooked Emotes noncontigious")

        for item_name in item_frequencies:
            self.assertIn(item_name, item_table.keys(), "Unexpected Overcooked Item in item_frequencies")

        for item_name in item_name_to_config_name.keys():
            self.assertIn(item_name, item_table.keys(), "Unexpected config in item-config mapping")

        for config_name in item_name_to_config_name.values():
            self.assertIn(config_name, vanilla_values.keys(), "Unexpected Overcooked Item in default config mapping")

        for config_name in vanilla_values.keys():
            self.assertIn(config_name, item_name_to_config_name.values(),
                          "Unexpected Overcooked Item in default config mapping")

        events = [
            ("Kevin-2", {"action": "UNLOCK_LEVEL", "payload": "38"}),
            ("Curse Emote", {"action": "UNLOCK_EMOTE", "payload": "1"}),
            ("Larger Tip Jar", {"action": "INC_TIP_COMBO", "payload": ""}),
            ("Order Lookahead", {"action": "INC_ORDERS_ON_SCREEN", "payload": ""}),
            ("Control Stick Batteries", {"action": "SET_VALUE", "payload": "DisableControlStick=False"}),
        ]
        for (item_name, expected_event) in events:
            expected_event["message"] = f"{item_name} Acquired!"
            event = item_to_unlock_event(item_name)
            self.assertEqual(event, expected_event)

        self.assertFalse(is_progression("Preparing Emote"))

        for item_name in item_table:
            item_to_unlock_event(item_name)

    def testOvercooked2Levels(self):
        level_count = 0
        for _ in Overcooked2Level():
            level_count += 1
        self.assertEqual(level_count, 44)

    def testOvercooked2ShuffleFactory(self):
        previous_runs = set()

        # Test uniqueness
        for seed in range(0, 5):
            levels = level_shuffle_factory(Random(seed), True, False, True, {x for x in Overcooked2Dlc}, "test")
            self.assertEqual(len(levels), 44)

            self.assertNotIn((levels[5], levels[15]), previous_runs)
            previous_runs.add((levels[5], levels[15]))

        # Test kevin = false
        levels = level_shuffle_factory(Random(123), False, True, False, {x for x in Overcooked2Dlc}, "test")
        self.assertEqual(len(levels), 36)

    def testLevelNameRepresentation(self):
        shortnames = [level.as_generic_level.shortname for level in Overcooked2Level()]

        for shortname in shortnames:
            self.assertIn(shortname, level_logic)

        self.assertEqual(len(level_logic), len(level_id_to_shortname))

        for level_name in level_logic.keys():
            if level_name != "*":
                self.assertIn(level_name, level_id_to_shortname.values())

        for level_name in level_id_to_shortname.values():
            if level_name != "Tutorial":
                self.assertIn(level_name, level_logic.keys())

        region_names = [level.level_name for level in Overcooked2Level()]
        for location_name in oc2_location_name_to_id.keys():
            level_name = location_name.split(" ")[0]
            self.assertIn(level_name, region_names)

    def testLogic(self):
        for level_name in level_logic.keys():
            logic = level_logic[level_name]
            self.assertEqual(len(logic), 3, "Levels must provide logic for 1, 2, and 3 stars")
            
            for l in logic:
                self.assertEqual(len(l), 2)
                (exclusive, additive) = l

                for req in exclusive:
                    self.assertEqual(type(req), str)
                    self.assertIn(req, item_table.keys())

                if len(additive) != 0:
                    self.assertGreater(len(additive), 1)
                    total_weight = 0.0
                    for req in additive:
                        self.assertEqual(len(req), 2)
                        (item_name, weight) = req
                        self.assertEqual(type(item_name), str)
                        self.assertEqual(type(weight), float)
                        total_weight += weight
                        self.assertIn(item_name, item_table.keys())

                    self.assertGreaterEqual(total_weight, 0.99, "Additive requirements must add to 1.0 or greater to have any effect")

    def testItemLocationMapping(self):
        number_of_items = 0
        for item_name in item_frequencies:
            freq = item_frequencies[item_name]
            self.assertGreaterEqual(freq, 0)
            number_of_items += freq
        
        for item_name in item_table:
            if item_name not in item_frequencies.keys():
                number_of_items += 1

        self.assertLessEqual(number_of_items, len(oc2_location_name_to_id), "Too many items (before fillers placed)")

    def testDlcExclusives(self):
        for item in dlc_exclusives:
            self.assertIn(item, item_table)

    def testLevelCounts(self):
        for dlc in Overcooked2Dlc:
            level_id_range = range(dlc.start_level_id, dlc.end_level_id)
            
            for level_id in dlc.excluded_levels():
                self.assertIn(level_id, level_id_range, f"Excluded level {dlc.name} - {level_id} out of range")
            
            for level_id in dlc.horde_levels():
                self.assertIn(level_id, level_id_range, f"Horde level {dlc.name} - {level_id} out of range")
            
            for level_id in dlc.prep_levels():
                self.assertIn(level_id, level_id_range, f"Prep level {dlc.name} - {level_id} out of range")

            for level_id in level_id_range:
                self.assertIn((dlc, level_id), level_id_to_shortname, "A valid level is not represented in level directory")
            
            count = 0
            for (dlc_key, _) in level_id_to_shortname:
                if dlc == dlc_key:
                    count += 1
            
            self.assertEqual(count, len(level_id_range), f"Number of levels in {dlc.name} has discrepancy between level_id range and directory")

    def testOverworldRegion(self):
        # OverworldRegion
        # overworld_region_by_level
        # overworld_region_logic

        # Test for duplicates
        regions_list = [x for x in OverworldRegion]
        regions_set = set(regions_list)
        self.assertEqual(len(regions_list), len(regions_set), f"Duplicate values in OverworldRegion")
        
        # Test all levels represented
        shortnames = [level.as_generic_level.shortname for level in Overcooked2Level()]
        for shortname in shortnames:
            if " " in shortname:
                shortname = shortname.split(" ")[1]
            shortname = shortname.replace("K-", "Kevin-")
            self.assertIn(shortname, overworld_region_by_level)

        for region in overworld_region_by_level.values():
            # Test all regions valid
            self.assertIn(region, regions_list)

            # Test Region Coverage
            self.assertIn(region, overworld_region_logic)

        # Test all regions valid
        for region in overworld_region_logic:
            self.assertIn(region, regions_set)

        self.assertIn("Overcooked! 2", AutoWorldRegister.world_types.keys())
        world_type = AutoWorldRegister.world_types["Overcooked! 2"]
        world = setup_solo_multiworld(world_type)
        state = world.get_all_state(False)

        # Test region logic
        for logic in overworld_region_logic.values():
            for allow_tricks in [False, True]:
                result = logic(state, 1, allow_tricks, list())
                self.assertIn(result, [False, True])
