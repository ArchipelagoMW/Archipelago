import itertools
from dataclasses import fields
from random import Random
import unittest
from typing import List, Set, Iterable

from BaseClasses import ItemClassification, MultiWorld
import Options as CoreOptions
from .. import options, locations
from ..item import item_tables
from ..rules import SC2Logic
from ..mission_tables import SC2Race, MissionFlag, lookup_name_to_mission


class TestInventory:
    """
    Runs checks against inventory with validation if all target items are progression and returns a random result
    """
    def __init__(self) -> None:
        self.random: Random = Random()
        self.progression_types: Set[ItemClassification] = {ItemClassification.progression, ItemClassification.progression_skip_balancing}

    def is_item_progression(self, item: str) -> bool:
        return item_tables.item_table[item].classification in self.progression_types

    def random_boolean(self):
        return self.random.choice([True, False])

    def has(self, item: str, player: int, count: int = 1):
        if not self.is_item_progression(item):
            raise AssertionError("Logic item {} is not a progression item".format(item))
        return self.random_boolean()

    def has_any(self, items: Set[str], player: int):
        non_progression_items = [item for item in items if not self.is_item_progression(item)]
        if len(non_progression_items) > 0:
            raise AssertionError("Logic items {} are not progression items".format(non_progression_items))
        return self.random_boolean()

    def has_all(self, items: Set[str], player: int):
        return self.has_any(items, player)

    def has_group(self, item_group: str, player: int, count: int = 1):
        return self.random_boolean()

    def count_group(self, item_name_group: str, player: int) -> int:
        return self.random.randrange(0, 20)

    def count(self, item: str, player: int) -> int:
        if not self.is_item_progression(item):
            raise AssertionError("Item {} is not a progression item".format(item))
        random_value: int = self.random.randrange(0, 5)
        if random_value == 4:  # 0-3 has a higher chance due to logic rules
            return self.random.randrange(4, 100)
        else:
            return random_value

    def count_from_list(self, items: Iterable[str], player: int) -> int:
        return sum(self.count(item_name, player) for item_name in items)

    def count_from_list_unique(self, items: Iterable[str], player: int) -> int:
        return sum(self.count(item_name, player) for item_name in items)


class TestWorld:
    """
    Mock world to simulate different player options for logic rules
    """
    def __init__(self) -> None:
        defaults = dict()
        for field in fields(options.Starcraft2Options):
            field_class = field.type
            option_name = field.name
            if isinstance(field_class, str):
                if field_class in globals():
                    field_class = globals()[field_class]
                else:
                    field_class = CoreOptions.__dict__[field.type]
            defaults[option_name] = field_class(options.get_option_value(None, option_name))
        self.options: options.Starcraft2Options = options.Starcraft2Options(**defaults)

        self.options.mission_order.value = options.MissionOrder.option_vanilla_shuffled

        self.player = 1
        self.multiworld = MultiWorld(1)


class TestRules(unittest.TestCase):
    def setUp(self) -> None:
        self.required_tactics_values: List[int] = [
            options.RequiredTactics.option_standard, options.RequiredTactics.option_advanced
        ]
        self.all_in_map_values: List[int] = [
            options.AllInMap.option_ground, options.AllInMap.option_air
        ]
        self.take_over_ai_allies_values: List[int] = [
            options.TakeOverAIAllies.option_true, options.TakeOverAIAllies.option_false
        ]
        self.kerrigan_presence_values: List[int] = [
            options.KerriganPresence.option_vanilla, options.KerriganPresence.option_not_present
        ]
        self.NUM_TEST_RUNS = 100

    @staticmethod
    def _get_world(
        required_tactics: int = options.RequiredTactics.default,
        all_in_map: int = options.AllInMap.default,
        take_over_ai_allies: int = options.TakeOverAIAllies.default,
        kerrigan_presence: int = options.KerriganPresence.default,
        # setting this to everywhere catches one extra logic check for Amon's Fall without missing any
        spear_of_adun_passive_presence: int = options.SpearOfAdunPassiveAbilityPresence.option_everywhere,
    ) -> TestWorld:
        test_world = TestWorld()
        test_world.options.required_tactics.value = required_tactics
        test_world.options.all_in_map.value = all_in_map
        test_world.options.take_over_ai_allies.value = take_over_ai_allies
        test_world.options.kerrigan_presence.value = kerrigan_presence
        test_world.options.spear_of_adun_passive_ability_presence.value = spear_of_adun_passive_presence
        test_world.options.enabled_campaigns.value = set(options.EnabledCampaigns.valid_keys)
        test_world.logic = SC2Logic(test_world)  # type: ignore
        return test_world

    def test_items_in_rules_are_progression(self):
        test_inventory = TestInventory()
        for option in self.required_tactics_values:
            test_world = self._get_world(required_tactics=option)
            location_data = locations.get_locations(test_world)
            for location in location_data:
                for _ in range(self.NUM_TEST_RUNS):
                    location.rule(test_inventory)
    
    def test_items_in_all_in_are_progression(self):
        test_inventory = TestInventory()
        for test_options in itertools.product(self.required_tactics_values, self.all_in_map_values):
            test_world = self._get_world(required_tactics=test_options[0], all_in_map=test_options[1])
            for location in locations.get_locations(test_world):
                if 'All-In' not in location.region:
                    continue
                for _ in range(self.NUM_TEST_RUNS):
                    location.rule(test_inventory)

    def test_items_in_kerriganless_missions_are_progression(self):
        test_inventory = TestInventory()
        for test_options in itertools.product(self.required_tactics_values, self.kerrigan_presence_values):
            test_world = self._get_world(required_tactics=test_options[0], kerrigan_presence=test_options[1])
            for location in locations.get_locations(test_world):
                mission = lookup_name_to_mission[location.region]
                if MissionFlag.Kerrigan not in mission.flags:
                    continue
                for _ in range(self.NUM_TEST_RUNS):
                    location.rule(test_inventory)

    def test_items_in_ai_takeover_missions_are_progression(self):
        test_inventory = TestInventory()
        for test_options in itertools.product(self.required_tactics_values, self.take_over_ai_allies_values):
            test_world = self._get_world(required_tactics=test_options[0], take_over_ai_allies=test_options[1])
            for location in locations.get_locations(test_world):
                mission = lookup_name_to_mission[location.region]
                if MissionFlag.AiAlly not in mission.flags:
                    continue
                for _ in range(self.NUM_TEST_RUNS):
                    location.rule(test_inventory)
    
    def test_items_in_hard_rules_are_progression(self):
        test_inventory = TestInventory()
        test_world = TestWorld()
        test_world.options.required_tactics.value = options.RequiredTactics.option_any_units
        test_world.logic = SC2Logic(test_world)
        location_data = locations.get_locations(test_world)
        for location in location_data:
            if location.hard_rule is not None:
                for _ in range(10):
                    location.hard_rule(test_inventory)

    def test_items_in_any_units_rules_are_progression(self):
        test_inventory = TestInventory()
        test_world = TestWorld()
        test_world.options.required_tactics.value = options.RequiredTactics.option_any_units
        logic = SC2Logic(test_world)
        test_world.logic = logic
        for race in (SC2Race.TERRAN, SC2Race.PROTOSS, SC2Race.ZERG):
            for target in range(1, 5):
                rule = logic.has_race_units(target, race)
                for _ in range(10):
                    rule(test_inventory)


