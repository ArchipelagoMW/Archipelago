import random
import unittest
from types import SimpleNamespace

from .. import poke_data
from ..pokemon import (choose_forced_type, filter_moves, get_move, move_power, process_move_data,
                       set_mon_palettes)
from ..rom_addresses import rom_addresses


class FixedRandom:
    def __init__(self, randint_values=None) -> None:
        self.randint_values = list(randint_values or [])

    def randint(self, low: int, high: int) -> int:
        if self.randint_values:
            return self.randint_values.pop(0)
        return low

    def shuffle(self, sequence) -> None:
        return None


class ReverseShuffleRandom:
    def shuffle(self, sequence) -> None:
        sequence.reverse()


class CyclingChoiceRandom:
    def __init__(self) -> None:
        self.index = 0

    def choice(self, sequence):
        value = sequence[self.index % len(sequence)]
        self.index += 1
        return value


class RecordingPatch:
    def __init__(self) -> None:
        self.calls = []

    def write_token(self, token_type, address, data) -> None:
        self.calls.append((token_type, address, data))


def make_world(**option_overrides) -> SimpleNamespace:
    options = SimpleNamespace(
        randomize_move_types=False,
        move_balancing=False,
        no_trapping_moves=False,
        randomize_tm_moves=False,
        randomize_pokemon_palettes="vanilla",
    )
    for name, value in option_overrides.items():
        setattr(options, name, value)
    return SimpleNamespace(
        options=options,
        random=random.Random(0),
        local_poke_data=poke_data.pokemon_data,
    )


class TestPokemonHelpers(unittest.TestCase):
    def test_choose_forced_type_returns_first_matching_threshold_or_none(self) -> None:
        chances = [[30, "Fire"], [80, "Water"]]

        self.assertEqual("Fire", choose_forced_type(chances, FixedRandom([1])))
        self.assertEqual("Water", choose_forced_type(chances, FixedRandom([50])))
        self.assertIsNone(choose_forced_type(chances, FixedRandom([99])))

    def test_filter_moves_only_keeps_requested_type_and_shuffles_result(self) -> None:
        move_data = {
            "Tackle": {"type": "Normal"},
            "Water Gun": {"type": "Water"},
            "Quick Attack": {"type": "Normal"},
        }

        self.assertEqual(
            ["Quick Attack", "Tackle"],
            filter_moves(move_data, ["Tackle", "Water Gun", "Quick Attack"], "Normal", ReverseShuffleRandom()),
        )

    def test_get_move_skips_non_damaging_options_for_starting_moves(self) -> None:
        local_move_data = {
            "Growl": {"type": "Normal", "accuracy": 100, "power": 0},
            "Tackle": {"type": "Normal", "accuracy": 95, "power": 35},
        }
        moves = ["Growl", "Tackle"]

        move = get_move(local_move_data, moves, [], FixedRandom(), starting_move=True)

        self.assertEqual("Tackle", move)
        self.assertEqual(["Growl"], moves)

    def test_get_move_falls_back_when_forced_type_has_no_moves(self) -> None:
        local_move_data = {
            "Ember": {"type": "Fire", "accuracy": 100, "power": 40},
            "Water Gun": {"type": "Water", "accuracy": 100, "power": 40},
        }
        moves = ["Ember", "Water Gun"]

        move = get_move(local_move_data, moves, [[100, "Psychic"]], FixedRandom([50, 50]))

        self.assertEqual("Ember", move)
        self.assertEqual(["Water Gun"], moves)

    def test_move_power_adjusts_special_cases(self) -> None:
        cases = (
            ({"power": 30, "effect": 29, "id": 1}, 90),
            ({"power": 25, "effect": 77, "id": 41}, 50),
            ({"power": 100, "effect": 48, "id": 36}, 75),
            ({"power": 20, "effect": 3, "id": 71}, 30),
            ({"power": 100, "effect": 39, "id": 13}, 66),
            ({"power": 100, "effect": 39, "id": 91}, 100),
            ({"power": 130, "effect": 7, "id": 120}, 65),
            ({"power": 55, "effect": 0, "id": 75}, 110),
        )

        for move_data, expected in cases:
            with self.subTest(move_data=move_data):
                self.assertEqual(expected, move_power(move_data))

    def test_process_move_data_applies_balancing_and_preserves_source_data(self) -> None:
        world = make_world(move_balancing=True, no_trapping_moves=True)
        original_sing_accuracy = poke_data.moves["Sing"]["accuracy"]
        original_bind_effect = poke_data.moves["Bind"]["effect"]

        process_move_data(world)

        self.assertEqual(30, world.local_move_data["Sing"]["accuracy"])
        self.assertEqual(50, world.local_move_data["Sonicboom"]["power"])
        self.assertEqual(29, world.local_move_data["Bind"]["effect"])
        self.assertEqual(poke_data.tm_moves, world.local_tms)
        self.assertEqual(original_sing_accuracy, poke_data.moves["Sing"]["accuracy"])
        self.assertEqual(original_bind_effect, poke_data.moves["Bind"]["effect"])

    def test_process_move_data_randomizes_tm_pool_without_hms_or_duplicates(self) -> None:
        world = make_world(randomize_tm_moves=True)

        process_move_data(world)

        self.assertEqual(50, len(world.local_tms))
        self.assertEqual(50, len(set(world.local_tms)))
        self.assertFalse(set(world.local_tms) & set(poke_data.hm_moves))
        self.assertNotIn("No Move", world.local_tms)


class TestPokemonPalettes(unittest.TestCase):
    def test_set_mon_palettes_does_nothing_in_vanilla_mode(self) -> None:
        patch = RecordingPatch()

        set_mon_palettes(make_world(randomize_pokemon_palettes="vanilla"), patch)

        self.assertEqual([], patch.calls)

    def test_set_mon_palettes_primary_type_uses_primary_types(self) -> None:
        patch = RecordingPatch()

        set_mon_palettes(make_world(randomize_pokemon_palettes="primary_type"), patch)

        self.assertEqual(1, len(patch.calls))
        _, address, payload = patch.calls[0]
        self.assertEqual(rom_addresses["Mon_Palettes"], address)
        self.assertEqual(len(poke_data.pokemon_data), len(payload))
        self.assertEqual(0x16, payload[0])  # Bulbasaur primary type: Grass
        self.assertEqual(0x12, payload[3])  # Charmander primary type: Fire

    def test_set_mon_palettes_follow_evolutions_reuses_prior_palette_except_eevee(self) -> None:
        patch = RecordingPatch()
        world = make_world(randomize_pokemon_palettes="follow_evolutions")
        world.random = CyclingChoiceRandom()

        set_mon_palettes(world, patch)

        payload = patch.calls[0][2]
        pokemon_order = list(poke_data.pokemon_data)
        bulbasaur = pokemon_order.index("Bulbasaur")
        ivysaur = pokemon_order.index("Ivysaur")
        venusaur = pokemon_order.index("Venusaur")
        eevee = pokemon_order.index("Eevee")
        vaporeon = pokemon_order.index("Vaporeon")

        self.assertEqual(payload[bulbasaur], payload[ivysaur])
        self.assertEqual(payload[ivysaur], payload[venusaur])
        self.assertNotEqual(payload[eevee], payload[vaporeon])
