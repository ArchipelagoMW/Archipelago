import pkgutil
from unittest import TestCase

import yaml

from ..data import PhoneScriptData
from ..phone_data import poke_cmd, data_to_script


class PhoneCallsTest(TestCase):
    max_phone_trap_bytes = 1024
    max_line_length = 18

    def test_phone_calls(self):
        phone_scripts = yaml.safe_load(
            pkgutil.get_data("worlds.pokemon_crystal", "data/phone_data.yaml").decode('utf-8-sig'))

        for script_name, script_data in phone_scripts.items():
            script = data_to_script(PhoneScriptData(script_name, script_data.get("caller"), script_data.get("script")))

            assert len(script.get_script_bytes()) < self.max_phone_trap_bytes

            for line in script.lines:
                assert sum(
                    [len(item) if isinstance(item, str) else 4 if item == poke_cmd else 7 for item in
                     line.contents[1:]]) <= self.max_line_length, f"{line.contents[1:]} is too long."
