from BaseClasses import ItemClassification
from Fill import distribute_items_restrictive

from . import ShellipelagoTestBase
from .. import ShellipelagoWorld
from ..locations import location_table


class TestDefaultGeneration(ShellipelagoTestBase):
    def test_default_location_count(self) -> None:
        self.assertEqual(len(self.multiworld.get_locations(self.player)), 107)

    def test_victory_location(self) -> None:
        victory_location = self.world.get_location(ShellipelagoWorld.victory_location_name)

        self.assertIsNone(victory_location.address)
        self.assertIsNotNone(victory_location.item)
        self.assertEqual(victory_location.item.name, "Victory")
        self.assertIsNone(victory_location.item.code)
        self.assertEqual(victory_location.item.classification, ItemClassification.progression_skip_balancing)

    def test_completion_requires_victory(self) -> None:
        victory_item = self.world.get_location(ShellipelagoWorld.victory_location_name).item
        completion_condition = self.multiworld.completion_condition[self.player]

        self.assertFalse(completion_condition(self.multiworld.state))
        self.multiworld.state.collect(victory_item, True)
        self.assertTrue(completion_condition(self.multiworld.state))

    def test_traps_not_in_pool(self) -> None:
        trap_locations = [
            self.world.get_location(location_data["name"])
            for location_data in location_table.values()
            if location_data.get("trap_location")
        ]

        self.assertEqual(len(trap_locations), 9)
        self.assertFalse(any(item.trap for item in self.multiworld.itempool))


class TestExpandedChecks(ShellipelagoTestBase):
    options = {
        "add_easy_destructible_checks": True,
        "enemies_are_checks": True,
    }

    def test_expanded_location_count(self) -> None:
        self.assertEqual(len(self.multiworld.get_locations(self.player)), 1695)


class TestTrapsEnabled(ShellipelagoTestBase):
    options = {
        "add_traps_to_pool": True,
    }

    def test_traps_in_pool(self) -> None:
        trap_items = [item for item in self.multiworld.itempool if item.trap]

        self.assertTrue(trap_items)
        self.assertTrue(all(item.classification == ItemClassification.trap for item in trap_items))


class TestHintsEnabled(ShellipelagoTestBase):
    options = {
        "enemies_are_hints": True,
    }

    def test_hint_triggers(self) -> None:
        distribute_items_restrictive(self.multiworld)
        hint_triggers = self.world.fill_slot_data()["hint_triggers"]
        location_ids = set(self.world.location_name_to_id.values())

        self.assertTrue(hint_triggers)
        self.assertTrue(all(location_id in location_ids for location_id in hint_triggers.values()))


class TestEssentialShuffleOff(ShellipelagoTestBase):
    options = {
        "shuffle_essential_items": False,
    }

    def test_vanilla_trap_locations_not_in_pool(self) -> None:
        for location_data in location_table.values():
            if location_data.get("trap_location"):
                self.assertRaises(KeyError, self.world.get_location, location_data["name"])
