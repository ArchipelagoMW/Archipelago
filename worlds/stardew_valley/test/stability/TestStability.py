import json
import re
import subprocess
import unittest

from BaseClasses import get_seed
from Utils import Version

# <function Location.<lambda> at 0x102ca98a0>
lambda_regex = re.compile(r"^<function Location\.<lambda> at (.*)>$")
python_version_regex = re.compile(r"^Python (\d+)\.(\d+)\.(\d+)\s*$")


class TestGenerationIsStable(unittest.TestCase):
    """Let it be known that I hate this tests, and if someone has a better idea than starting subprocesses, please fix this.
    """

    def test_all_locations_and_items_are_the_same_between_two_generations(self):
        seed = get_seed()

        try:
            python_version = subprocess.check_output(['python', '--version'])
        except subprocess.CalledProcessError:
            return self.skipTest("It seems that python is not available in you classpath. Skipping.")

        match = python_version_regex.match(python_version.decode("UTF-8"))
        version = Version(*(int(m) for m in match.groups()))
        if version.major < 3:
            return self.skipTest("It seems that the python available in your classpath is python2 instead of python3. Skipping.")

        output_a = subprocess.check_output(['python', '-m', 'worlds.stardew_valley.test.stability.StabilityOutputScript', '--seed', str(seed)])
        output_b = subprocess.check_output(['python', '-m', 'worlds.stardew_valley.test.stability.StabilityOutputScript', '--seed', str(seed)])

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
            self.assertEqual(location_a, location_a, f"Location at index {i} is different between both executions. Seed={seed}")

            match = lambda_regex.match(rule_a)
            if match:
                self.assertTrue(bool(lambda_regex.match(rule_b)),
                                f"Location rule of {location_a} at index {i} is different between both executions. Seed={seed}")
                continue

            self.assertEqual(rule_a, rule_b, f"Location rule of {location_a} at index {i} is different between both executions. Seed={seed}")
