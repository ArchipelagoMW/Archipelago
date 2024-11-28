import json
import os
from typing import Any, Dict
from Fill import distribute_items_restrictive
from ..PrimeOptions import BlastShieldRandomization, DoorColorRandomization
from ..Config import make_config
from . import MetroidPrimeTestBase

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_output")


def dict_diff(d1: Any, d2: Any, path: str = ""):
    """Prints out the differences between two dictionaries recursively, will show up if the test fails"""
    for k in d1:
        if k not in d2:
            print(f"{path}: Key {k} not found in second dict")
        elif isinstance(d1[k], dict) and isinstance(d2[k], dict):
            dict_diff(d1[k], d2[k], path=f"{path}.{k}")
        elif d1[k] != d2[k]:
            print(f"Difference at {path}.{k}: {d1[k]} != {d2[k]}")

    for k in d2:
        if k not in d1:
            print(f"{path}: Key {k} not found in first dict")


class TestDefaultOutputGeneration(MetroidPrimeTestBase):
    auto_construct = False
    options = {}

    def test_output_generates_correctly(self) -> None:
        self.world_setup()  # type: ignore
        distribute_items_restrictive(self.multiworld)
        output = make_config(self.world)
        expected_output = {}
        path = os.path.join(os.path.dirname(__file__), "data", "default_config.json")
        with open(path, "r") as f:
            expected_output = json.load(f)

        dict_diff(expected_output, output)
        dump_output_if_test_fails(self, output, expected_output)


class TestMainPBAndMissileLauncherOutputGeneration(MetroidPrimeTestBase):
    auto_construct = False
    options = {"missile_launcher": 1, "main_power_bomb": 1}

    def test_output_generates_correctly_with_main_pb_and_missile_launcher(self) -> None:
        self.world_setup()  # type: ignore
        distribute_items_restrictive(self.multiworld)
        output = make_config(self.world)
        expected_output = {}
        path = os.path.join(
            os.path.dirname(__file__), "data", "missile_launcher_main_pb_config.json"
        )
        with open(path, "r") as f:
            expected_output = json.load(f)

        dict_diff(expected_output, output)
        dump_output_if_test_fails(self, output, expected_output)


class TestAllRandomizedOutput(MetroidPrimeTestBase):
    auto_construct = False
    options = {
        "elevator_randomization": True,
        "door_color_randomization": DoorColorRandomization.option_regional,
        "blast_shield_randomization": BlastShieldRandomization.option_mix_it_up,
    }

    def test_output_generates_correctly_with_all_randomized(self) -> None:
        self.world_setup()  # type: ignore
        distribute_items_restrictive(self.multiworld)
        output = make_config(self.world)
        expected_output = {}
        path = os.path.join(os.path.dirname(__file__), "data", "all_randomized.json")
        with open(path, "r") as f:
            expected_output = json.load(f)

        dict_diff(expected_output, output)
        dump_output_if_test_fails(self, output, expected_output)


def dump_output_if_test_fails(
    test: MetroidPrimeTestBase, output: Dict[str, Any], expected_output: Dict[str, Any]
):
    try:
        test.assertDictEqual(output, expected_output)
    except AssertionError:
        # If the test fails, write the expected output to a file
        os.makedirs(
            OUTPUT_DIR, exist_ok=True
        )  # Create the directory if it does not exist
        with open(f"{OUTPUT_DIR}/{test._testMethodName}.json", "w") as f:
            json.dump(output, f, indent=4)
        raise  # Re-raise the exception to fail the test
