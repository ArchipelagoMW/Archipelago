import unittest
from types import SimpleNamespace

from .. import logic, poke_data


class DummyState:
    def __init__(self, items=None) -> None:
        self.items = dict(items or {})

    def has(self, name: str, player: int, count: int = 1) -> bool:
        return self.items.get(name, 0) >= count

    def count(self, name: str, player: int) -> int:
        return self.items.get(name, 0)

    def has_all(self, names, player: int) -> bool:
        return all(self.has(name, player) for name in names)

    def has_any(self, names, player: int) -> bool:
        return any(self.has(name, player) for name in names)


def make_world(**overrides) -> SimpleNamespace:
    options = SimpleNamespace(
        badges_needed_for_hm_moves=SimpleNamespace(value=1),
        require_item_finder=SimpleNamespace(value=False),
        require_pokedex=False,
        tea=False,
        route_3_condition="open",
        dark_rock_tunnel_logic=True,
    )
    for name, value in overrides.items():
        setattr(options, name, value)
    return SimpleNamespace(
        options=options,
        extra_badges={},
        local_poke_data=poke_data.pokemon_data,
    )


class TestPokemonLogic(unittest.TestCase):
    player = 1

    def test_can_learn_hm_requires_owned_compatible_pokemon(self) -> None:
        world = make_world()

        self.assertTrue(logic.can_learn_hm(DummyState({"Squirtle": 1}), world, "Surf", self.player))
        self.assertFalse(logic.can_learn_hm(DummyState({"Charmander": 1}), world, "Surf", self.player))

    def test_can_surf_allows_extra_badges_or_no_badge_requirement(self) -> None:
        world = make_world()
        world.extra_badges["Surf"] = "Earth Badge"

        self.assertTrue(logic.can_surf(
            DummyState({"HM03 Surf": 1, "Squirtle": 1, "Earth Badge": 1}),
            world,
            self.player,
        ))

        badge_free_world = make_world(badges_needed_for_hm_moves=SimpleNamespace(value=0))
        self.assertTrue(logic.can_surf(
            DummyState({"HM03 Surf": 1, "Squirtle": 1}),
            badge_free_world,
            self.player,
        ))

    def test_can_get_hidden_items_respects_item_finder_requirement(self) -> None:
        required_world = make_world(require_item_finder=SimpleNamespace(value=True))

        self.assertFalse(logic.can_get_hidden_items(DummyState(), required_world, self.player))
        self.assertTrue(logic.can_get_hidden_items(DummyState({"Item Finder": 1}), required_world, self.player))
        self.assertTrue(logic.can_get_hidden_items(DummyState(), make_world(), self.player))

    def test_can_pass_guards_switches_between_tea_and_drinks(self) -> None:
        self.assertTrue(logic.can_pass_guards(DummyState({"Tea": 1}), make_world(tea=True), self.player))
        self.assertFalse(logic.can_pass_guards(DummyState({"Vending Machine Drinks": 1}), make_world(tea=True), self.player))
        self.assertTrue(logic.can_pass_guards(DummyState({"Vending Machine Drinks": 1}), make_world(tea=False), self.player))

    def test_has_key_items_caps_progressive_card_keys_at_ten(self) -> None:
        state = DummyState({
            "Bicycle": 1,
            "Silph Scope": 1,
            "Progressive Card Key": 12,
        })

        self.assertTrue(logic.has_key_items(state, 12, self.player))
        self.assertFalse(logic.has_key_items(state, 13, self.player))

    def test_has_pokemon_counts_unique_species_once_even_with_static_variant(self) -> None:
        state = DummyState({
            "Bulbasaur": 1,
            "Static Bulbasaur": 1,
            "Pikachu": 1,
        })

        self.assertTrue(logic.has_pokemon(state, 2, self.player))
        self.assertFalse(logic.has_pokemon(state, 3, self.player))

    def test_oaks_aide_requires_pokedex_only_when_enabled(self) -> None:
        state = DummyState({
            "Bulbasaur": 1,
            "Pikachu": 1,
        })

        self.assertTrue(logic.oaks_aide(state, make_world(require_pokedex=False), 2, self.player))
        self.assertFalse(logic.oaks_aide(state, make_world(require_pokedex=True), 2, self.player))
        state.items["Pokedex"] = 1
        self.assertTrue(logic.oaks_aide(state, make_world(require_pokedex=True), 2, self.player))

    def test_fossil_checks_respects_ut_glitch_shortcut(self) -> None:
        self.assertTrue(logic.fossil_checks(DummyState({"ut_glitch": 1, "Mt Moon Fossils": 1}), 1, self.player))
        self.assertFalse(logic.fossil_checks(DummyState({"ut_glitch": 1}), 1, self.player))

        normal_state = DummyState({
            "Mt Moon Fossils": 1,
            "Cinnabar Lab": 1,
            "Cinnabar Island": 1,
            "Dome Fossil": 1,
            "Old Amber": 1,
        })
        self.assertTrue(logic.fossil_checks(normal_state, 2, self.player))
        self.assertFalse(logic.fossil_checks(normal_state, 3, self.player))

    def test_ut_glitch_fossil_checks_skip_cinnabar_and_specific_fossil_requirements(self) -> None:
        state = DummyState({
            "Mt Moon Fossils": 1,
        })

        self.assertFalse(logic.fossil_checks(state, 1, self.player))
        state.items["ut_glitch"] = 1
        self.assertTrue(logic.fossil_checks(state, 3, self.player))

    def test_card_key_accepts_specific_master_and_progressive_keys(self) -> None:
        self.assertTrue(logic.card_key(DummyState({"Card Key 5F": 1}), 5, self.player))
        self.assertTrue(logic.card_key(DummyState({"Card Key": 1}), 9, self.player))
        self.assertTrue(logic.card_key(DummyState({"Progressive Card Key": 4}), 5, self.player))
        self.assertFalse(logic.card_key(DummyState({"Progressive Card Key": 4}), 6, self.player))

    def test_route3_conditions_follow_selected_mode(self) -> None:
        cases = (
            ("open", DummyState(), True),
            ("defeat_brock", DummyState({"Defeat Brock": 1}), True),
            ("defeat_brock", DummyState(), False),
            ("defeat_any_gym", DummyState({"Defeat Koga": 1}), True),
            ("boulder_badge", DummyState({"Boulder Badge": 1}), True),
            ("any_badge", DummyState({"Earth Badge": 1}), True),
            ("any_badge", DummyState(), False),
        )

        for mode, state, expected in cases:
            with self.subTest(mode=mode, items=state.items):
                self.assertEqual(expected, logic.route3(state, make_world(route_3_condition=mode), self.player))

    def test_rock_tunnel_only_needs_flash_when_dark_logic_is_enabled(self) -> None:
        self.assertTrue(logic.rock_tunnel(DummyState(), make_world(dark_rock_tunnel_logic=False), self.player))
        self.assertFalse(logic.rock_tunnel(DummyState(), make_world(dark_rock_tunnel_logic=True), self.player))
        self.assertTrue(logic.rock_tunnel(
            DummyState({"Lamp": 1, "Boulder Badge": 1}),
            make_world(dark_rock_tunnel_logic=True),
            self.player,
        ))

    def test_evolve_level_uses_strict_threshold_and_ut_glitch_override(self) -> None:
        state = DummyState({
            "Defeat Brock": 1,
            "Defeat Misty": 1,
        })

        self.assertFalse(logic.evolve_level(state, 14, self.player))
        state.items["Defeat Lt. Surge"] = 1
        self.assertTrue(logic.evolve_level(state, 14, self.player))
        self.assertTrue(logic.evolve_level(DummyState({"ut_glitch": 1}), 99, self.player))

    def test_ut_glitch_evolve_level_bypasses_gym_progress_entirely(self) -> None:
        self.assertFalse(logic.evolve_level(DummyState(), 1, self.player))
        self.assertTrue(logic.evolve_level(DummyState({"ut_glitch": 1}), 1, self.player))
