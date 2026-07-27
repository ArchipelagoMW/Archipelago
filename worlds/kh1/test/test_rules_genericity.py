import random
import unittest

from BaseClasses import CollectionState

from . import KH1TestBase
from ..Rules import build_rule_dicts

_MAXIMAL_EXISTENCE_OPTIONS = {
    "super_bosses": True,
    "cups": "hades_cup",
    "hundred_acre_wood": True,
    "atlantica": True,
    "destiny_islands": True,
    "jungle_slider": True,
    "final_rest_door_key": "lucky_emblems",
}


class TestRulesBuildDictsAreOptionGeneric(KH1TestBase):
    """Builds two worlds with deliberately different option values (that historically baked
    differently-shaped rule trees) and asserts build_rule_dicts() produces byte-identical JSON for
    every location/entrance, regardless of those differences."""

    options = {
        **_MAXIMAL_EXISTENCE_OPTIONS,
        "logic_difficulty": "beginner",
        "keyblades_unlock_chests": False,
        "stacking_world_items": False,
        "halloween_town_key_item_bundle": False,
        "puppy_value": 1,
        "day_2_materials": 1,
        "homecoming_materials": 1,
        "required_lucky_emblems_eotw": 1,
        "required_lucky_emblems_door": 1,
    }

    def test_to_dict_identical_across_wildly_different_options(self) -> None:
        other_options = {
            **_MAXIMAL_EXISTENCE_OPTIONS,
            "logic_difficulty": "proud",
            "keyblades_unlock_chests": True,
            "stacking_world_items": True,
            "halloween_town_key_item_bundle": True,
            "puppy_value": 7,
            "day_2_materials": 13,
            "homecoming_materials": 18,
            "required_lucky_emblems_eotw": 17,
            "required_lucky_emblems_door": 19,
        }

        class _OtherWorld(KH1TestBase):
            options = other_options

        other = _OtherWorld()
        other.setUp()

        base_locations, base_entrances = build_rule_dicts(self.world)
        other_locations, other_entrances = build_rule_dicts(other.world)

        self.assertEqual(set(base_locations), set(other_locations),
                          "Different option values changed which locations got a rule at all")
        self.assertEqual(set(base_entrances), set(other_entrances),
                          "Different option values changed which entrances got a rule at all")

        mismatches = []
        for name, base_rule in base_locations.items():
            if base_rule.to_dict() != other_locations[name].to_dict():
                mismatches.append(f"Location: {name}")
        for name, base_rule in base_entrances.items():
            if base_rule.to_dict() != other_entrances[name].to_dict():
                mismatches.append(f"Entrance: {name}")

        if mismatches:
            self.fail(
                "These rules are NOT option-generic - their to_dict() output changed between two "
                "worlds that only differ in difficulty/keyblades_unlock_chests/stacking_world_items/"
                "halloween_town_key_item_bundle/puppy_value/day_2_materials/homecoming_materials/"
                "required_lucky_emblems_*:\n" + "\n".join(f"  {m}" for m in mismatches)
            )


class TestRulesRoundTrip(KH1TestBase):
    
    options = {**_MAXIMAL_EXISTENCE_OPTIONS, "logic_difficulty": "proud", "keyblades_unlock_chests": True}

    def test_round_trip_optionfilter_rule(self) -> None:
        # Has an OptionFilter (difficulty tier) nested inside an OptionFilter (keyblades_unlock_chests,
        # from the generic location_table pass) - a good stress test for from_dict()'s recursion.
        self._assert_round_trips("Agrabah Main Street High Above Palace Gates Entrance Chest")

    def test_round_trip_field_resolver_rule(self) -> None:
        # Uses the custom PuppiesRequiredCount FieldResolver.
        self._assert_round_trips("Traverse Town Piano Room Return 50 Puppies Reward 1")

    def _assert_round_trips(self, location_name: str) -> None:
        location_rules, _ = build_rule_dicts(self.world)
        original_rule = location_rules[location_name]
        reconstructed_rule = type(self.world).rule_from_dict(original_rule.to_dict())

        original_resolved = original_rule.resolve(self.world)
        reconstructed_resolved = reconstructed_rule.resolve(self.world)

        states = [CollectionState(self.multiworld)]
        all_items = list(self.multiworld.itempool)
        rng = random.Random(0xC0FFEE)
        for _ in range(10):
            state = CollectionState(self.multiworld)
            for item in rng.sample(all_items, rng.randint(0, len(all_items))):
                state.collect(item, prevent_sweep=True)
            state.sweep_for_advancements()
            states.append(state)

        for state in states:
            self.assertEqual(
                original_resolved(state), reconstructed_resolved(state),
                f"{location_name}: round-tripped rule disagrees with the original",
            )


if __name__ == "__main__":
    unittest.main()
