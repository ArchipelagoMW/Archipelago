import json
import re
import subprocess
import sys
import unittest

from BaseClasses import get_seed
from .. import SVTestCase

# <function Location.<lambda> at 0x102ca98a0>
lambda_regex = re.compile(r"^<function Location\.<lambda> at (.*)>$")


class TestGenerationIsStable(SVTestCase):
    """Let it be known that I hate this tests, and if someone has a better idea than starting subprocesses, please fix this.
    """

    def test_all_locations_and_items_are_the_same_between_two_generations(self):
        if self.skip_long_tests:
            raise unittest.SkipTest("Long tests disabled")

        seed = get_seed()

        output_a = subprocess.check_output([sys.executable, '-m', 'worlds.stardew_valley.test.stability.StabilityOutputScript', '--seed', str(seed)])
        output_b = subprocess.check_output([sys.executable, '-m', 'worlds.stardew_valley.test.stability.StabilityOutputScript', '--seed', str(seed)])

        result_a = json.loads(output_a)
        result_b = json.loads(output_b)

        for i, ((room_a, bundles_a), (room_b, bundles_b)) in enumerate(zip(result_a["bundles"].items(), result_b["bundles"].items())):
            self.assertEqual(room_a, room_b, f"Bundle rooms at index {i} is different between both executions. Seed={seed}")
            for j, ((bundle_a, items_a), (bundle_b, items_b)) in enumerate(zip(bundles_a.items(), bundles_b.items())):
                self.assertEqual(bundle_a, bundle_b, f"Bundle in room {room_a} at index {j} is different between both executions. Seed={seed}")
                self.assertEqual(items_a, items_b, f"Items in bundle {bundle_a} are different between both executions. Seed={seed}")

        for i, (item_a, item_b) in enumerate(zip(result_a["items"], result_b["items"])):
            self.assertEqual(item_a, item_b, f"Item at index {i} is different between both executions. Seed={seed}")

        for i, ((location_a, rule_a), (location_b, rule_b)) in enumerate(zip(result_a["location_rules"].items(), result_b["location_rules"].items())):
            self.assertEqual(location_a, location_b, f"Location at index {i} is different between both executions. Seed={seed}")

            match = lambda_regex.match(rule_a)
            if match:
                self.assertTrue(bool(lambda_regex.match(rule_b)),
                                f"Location rule of {location_a} at index {i} is different between both executions. Seed={seed}")
                continue

            # We check that the actual rule has the same order to make sure it is evaluated in the same order,
            #  so performance tests are repeatable as much as possible.
            self.assertEqual(rule_a, rule_b, f"Location rule of {location_a} at index {i} is different between both executions. Seed={seed}")

        for key, value in result_a["slot_data"].items():
            self.assertEqual(value, result_b["slot_data"][key], f"Slot data {key} is different between both executions. Seed={seed}")
