import unittest
from types import SimpleNamespace

from BaseClasses import ItemClassification

from .. import PokemonRedBlueWorld
from ..items import item_groups, item_table
from ..locations import LocationData, PokemonRBLocation, location_groups
from ..poke_data import pokemon_data


class TestPokemonItemMetadata(unittest.TestCase):
    def test_every_declared_item_group_contains_the_declaring_item(self) -> None:
        missing_groups = []
        for item_name, item_data in item_table.items():
            for group in item_data.groups:
                if item_name not in item_groups[group]:
                    missing_groups.append(f"{item_name!r} missing from {group!r}")

        self.assertEqual([], missing_groups)

    def test_all_pokemon_have_standard_item_variants_with_expected_classifications(self) -> None:
        problems = []
        for pokemon in pokemon_data:
            if pokemon not in item_table:
                problems.append(f"missing base item for {pokemon}")
                continue
            if f"Missable {pokemon}" not in item_table:
                problems.append(f"missing missable item for {pokemon}")
                continue
            if f"Static {pokemon}" not in item_table:
                problems.append(f"missing static item for {pokemon}")
                continue
            if item_table[pokemon].classification != ItemClassification.progression:
                problems.append(f"{pokemon} classification changed")
            if item_table[f"Missable {pokemon}"].classification != ItemClassification.useful:
                problems.append(f"Missable {pokemon} classification changed")
            if item_table[f"Static {pokemon}"].classification != ItemClassification.progression:
                problems.append(f"Static {pokemon} classification changed")

        self.assertEqual([], problems)

    def test_badges_group_contains_each_badge_once(self) -> None:
        self.assertCountEqual(
            [
                "Boulder Badge",
                "Cascade Badge",
                "Thunder Badge",
                "Rainbow Badge",
                "Soul Badge",
                "Marsh Badge",
                "Volcano Badge",
                "Earth Badge",
            ],
            item_groups["Badges"],
        )

    def test_ut_glitch_marker_is_registered_for_tracker_logic(self) -> None:
        self.assertEqual("ut_glitch", PokemonRedBlueWorld.glitches_item_name)
        self.assertEqual(ItemClassification.progression, item_table["ut_glitch"].classification)


class TestPokemonLocationMetadata(unittest.TestCase):
    def test_location_data_formats_names_from_region_and_special_cases(self) -> None:
        self.assertEqual(
            "Route 1 - Free Sample Man",
            LocationData("Route 1", "Free Sample Man", "Potion").name,
        )
        self.assertEqual(
            "Cerulean Bicycle Shop",
            LocationData("Cerulean Bicycle Shop", "", "Bicycle").name,
        )
        self.assertEqual(
            "Pokemon Tower 3F - Trainer Parties",
            LocationData("Pokemon Tower 3F", "Trainer Parties", "Trainer Parties").name,
        )
        self.assertEqual(
            "Silph Co 11F - Silph Co President",
            LocationData("Silph Co 11F-C", "Silph Co President", "Master Ball").name,
        )

    def test_location_groups_include_floor_aliases(self) -> None:
        self.assertIn("Silph Co 11F - Silph Co President", location_groups["Silph Co"])
        self.assertIn("Silph Co 11F - Silph Co President", location_groups["Silph Co 11F"])

    def test_pokemon_location_rule_accepts_normal_and_prefixed_pokemon_items(self) -> None:
        location = PokemonRBLocation(1, "Test", None, None, "Static Pokemon", None, None)

        self.assertTrue(location.item_rule(SimpleNamespace(player=1, name="Bulbasaur")))
        self.assertTrue(location.item_rule(SimpleNamespace(player=1, name="Static Bulbasaur")))
        self.assertFalse(location.item_rule(SimpleNamespace(player=1, name="Poke Ball")))
        self.assertFalse(location.item_rule(SimpleNamespace(player=2, name="Static Bulbasaur")))

    def test_trainer_parties_location_rule_only_accepts_trainer_party_items(self) -> None:
        location = PokemonRBLocation(1, "Test", None, None, "Trainer Parties", None, None)

        self.assertTrue(location.item_rule(SimpleNamespace(player=1, name="Trainer Parties")))
        self.assertFalse(location.item_rule(SimpleNamespace(player=1, name="Bulbasaur")))
