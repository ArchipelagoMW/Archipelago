from BaseClasses import ItemClassification
from Fill import distribute_items_restrictive
from dataclasses import fields

from . import ShellipelagoTestBase
from .. import ShellipelagoWorld
from ..items import item_table
from ..locations import location_table


class TestDefaultGeneration(ShellipelagoTestBase):
    def test_complete_item_catalog(self) -> None:
        expected_items = {
            "Graphics", "Progressive Room", "Bombs", "Gun", "Sword", "Fire",
            "Max HP", "Max Rounds", "SFX", "BGM", "Pickaxe", "Water Walkers",
            "Tank Treads", "Tank Chassis", "Tank Cannon", "Magnifying Glass",
            "Orthopedic Inserts", "Teleportation", "Steel Toe", "Vermin Pouch",
            "Health Potion", "Energy Gem", "Round Pouch", "Item Pool", "Stun Trap",
            "Invisible Trap", "Fast Trap", "Slow Trap", "Reverse Trap",
            "Screen Flip Trap", "Zoom In Trap", "Instant Death Trap", "Snake Trap",
        }

        self.assertEqual(set(item_table), expected_items)

    def test_enemies_require_weapon(self) -> None:
        enemy_locations = [
            location_data for location_data in location_table.values()
            if location_data["category"] == "enemy"
        ]

        self.assertTrue(enemy_locations)
        for location_data in enemy_locations:
            weapon_names = {"Sword", "Bombs", "Fire"}
            if location_data.get("enemy_type") != "Nega Slime":
                weapon_names.add("Gun")
            self.assertTrue(any(
                {requirement["item"] for requirement in requirement_row} == weapon_names
                for requirement_row in location_data["requirements"]
            ), location_data["name"])

    def test_enemy_rounds_requirements(self) -> None:
        rounds_items = {"Bombs", "Fire", "Gun"}

        for location_data in location_table.values():
            if location_data["category"] != "enemy":
                continue

            requirement_sets = [
                {(requirement["item"], requirement.get("amount", 1)) for requirement in requirement_row}
                for requirement_row in location_data["requirements"]
            ]
            for requirement_set in requirement_sets:
                if not any(item in rounds_items for item, _ in requirement_set):
                    continue

                expected_rounds_set = {
                    requirement for requirement in requirement_set
                    if requirement[0] not in rounds_items
                } | {("Max Rounds", 2)}
                self.assertIn(expected_rounds_set, requirement_sets, location_data["name"])

    def test_logic_items_are_progression(self) -> None:
        for location_data in location_table.values():
            for requirement_row in location_data["requirements"]:
                for requirement in requirement_row:
                    if requirement["item"] == "Tank":
                        continue

                    self.assertEqual(
                        item_table[requirement["item"]]["classification_name"],
                        "progression",
                        location_data["name"],
                    )

    def test_default_location_count(self) -> None:
        self.assertEqual(len(self.multiworld.get_locations(self.player)), 109)

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

        self.assertEqual(len(trap_locations), 8)
        self.assertFalse(any(item.trap for item in self.multiworld.itempool))


class TestExpandedChecks(ShellipelagoTestBase):
    options = {
        "add_easy_destructible_checks": True,
        "enemies_are_checks": True,
    }

    def test_expanded_location_count(self) -> None:
        self.assertEqual(len(self.multiworld.get_locations(self.player)), 1612)


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


class TestUniversalTracker(ShellipelagoTestBase):
    def test_slot_data_has_all_yaml_options(self) -> None:
        slot_data = self.world.fill_slot_data()
        option_names = {option_field.name for option_field in fields(self.world.options)}

        self.assertTrue(option_names.issubset(slot_data))

    def test_passthrough_restores_options(self) -> None:
        self.multiworld.re_gen_passthrough = {
            self.world.game: {
                "add_easy_destructible_checks": 1,
                "trap_pool_spawn": ["Stun Trap"],
                "trap_weights": {"Stun Trap": 7},
            }
        }

        self.world.generate_early()

        self.assertTrue(bool(self.world.options.add_easy_destructible_checks))
        self.assertEqual(self.world.options.trap_pool_spawn.value, {"Stun Trap"})
        self.assertEqual(self.world.options.trap_weights.value, {"Stun Trap": 7})

    def test_slot_data_interpretation_is_passthrough(self) -> None:
        slot_data = {"shuffle_essential_items": 0}

        self.assertIs(ShellipelagoWorld.interpret_slot_data(slot_data), slot_data)
