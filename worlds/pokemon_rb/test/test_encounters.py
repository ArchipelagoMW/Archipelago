import unittest
from types import SimpleNamespace
from unittest import mock

from .. import poke_data
from .. import encounters
from ..encounters import get_base_stat_total, get_encounter_slots, process_pokemon_locations, randomize_pokemon
from ..locations import location_data


class FixedTriangularRandom:
    def __init__(self, value: float = 0) -> None:
        self.value = value

    def triangular(self, low: float, high: float, mode: float) -> float:
        return self.value


class FakeChoice:
    def __init__(self, value: int, current_key: str) -> None:
        self.value = value
        self.current_key = current_key

    def __bool__(self) -> bool:
        return bool(self.value)

    def __eq__(self, other) -> bool:
        return other == self.value or other == self.current_key


class FakePlacedLocation:
    def __init__(self, name: str) -> None:
        self.name = name
        self.item = None
        self.locked = False

    def place_locked_item(self, item) -> None:
        self.item = item
        self.locked = True
        item.location = self


class FakeMultiWorld:
    def __init__(self, names) -> None:
        self.locations = {name: FakePlacedLocation(name) for name in names}

    def get_location(self, name: str, player: int) -> FakePlacedLocation:
        return self.locations[name]


def make_world(game_version: int = 1, catch_em_all: bool = False,
               randomize_pokemon_locations: bool = False) -> SimpleNamespace:
    return SimpleNamespace(
        options=SimpleNamespace(
            game_version=SimpleNamespace(value=game_version),
            catch_em_all=catch_em_all,
            randomize_pokemon_locations=randomize_pokemon_locations,
        ),
        local_poke_data=poke_data.pokemon_data,
    )


def slot_by_name(slots):
    return {slot.name: slot for slot in slots}


class TestEncounterSlots(unittest.TestCase):
    def test_get_encounter_slots_filters_to_requested_types(self) -> None:
        slots = get_encounter_slots(make_world(), ["Starter Pokemon"])

        self.assertEqual(
            {"Oak's Lab - Starter 1", "Oak's Lab - Starter 2", "Oak's Lab - Starter 3"},
            {slot.name for slot in slots},
        )

    def test_get_encounter_slots_uses_game_version_for_wild_exclusives(self) -> None:
        red_slots = slot_by_name(get_encounter_slots(make_world(game_version=1), ["Wild Encounter"]))
        blue_slots = slot_by_name(get_encounter_slots(make_world(game_version=0), ["Wild Encounter"]))

        self.assertEqual("Weedle", red_slots["Route 2 - Wild Pokemon - 6"].original_item)
        self.assertEqual("Caterpie", blue_slots["Route 2 - Wild Pokemon - 6"].original_item)

    def test_get_encounter_slots_alternates_exclusives_for_non_randomized_catch_em_all(self) -> None:
        slots = slot_by_name(get_encounter_slots(
            make_world(game_version=1, catch_em_all=True),
            ["Wild Encounter"],
        ))

        self.assertEqual("Weedle", slots["Route 2 - Wild Pokemon - 6"].original_item)
        self.assertEqual("Caterpie", slots["Route 2 - Wild Pokemon - 9"].original_item)
        self.assertEqual("Weedle", slots["Route 2 - Wild Pokemon - 10"].original_item)

    def test_get_encounter_slots_keeps_special_prize_slots_version_specific(self) -> None:
        prize_4_source = next(
            location.original_item for location in location_data
            if location.name == "Celadon Prize Corner - Pokemon Prize - 4"
        )
        prize_5_source = next(
            location.original_item for location in location_data
            if location.name == "Celadon Prize Corner - Pokemon Prize - 5"
        )
        red_slots = slot_by_name(get_encounter_slots(
            make_world(game_version=1, catch_em_all=True),
            ["Static Repeatable Pokemon"],
        ))
        blue_slots = slot_by_name(get_encounter_slots(
            make_world(game_version=0, catch_em_all=True),
            ["Static Repeatable Pokemon"],
        ))

        self.assertEqual(prize_4_source[1], red_slots["Celadon Prize Corner - Pokemon Prize - 4"].original_item)
        self.assertEqual(prize_5_source[1], red_slots["Celadon Prize Corner - Pokemon Prize - 5"].original_item)
        self.assertEqual(prize_4_source[0], blue_slots["Celadon Prize Corner - Pokemon Prize - 4"].original_item)
        self.assertEqual(prize_5_source[0], blue_slots["Celadon Prize Corner - Pokemon Prize - 5"].original_item)

    def test_get_encounter_slots_deepcopies_location_data(self) -> None:
        source_slot = next(location for location in location_data if location.name == "Route 2 - Wild Pokemon - 6")
        returned_slot = slot_by_name(get_encounter_slots(make_world(), ["Wild Encounter"]))[
            "Route 2 - Wild Pokemon - 6"
        ]

        self.assertIsNot(source_slot, returned_slot)
        self.assertEqual(["Weedle", "Caterpie"], source_slot.original_item)
        self.assertEqual("Weedle", returned_slot.original_item)


class TestEncounterRandomizationHelpers(unittest.TestCase):
    def test_get_base_stat_total_sums_all_five_base_stats(self) -> None:
        self.assertEqual(253, get_base_stat_total("Bulbasaur"))

    def test_randomize_pokemon_prefers_type_matches_when_possible(self) -> None:
        world = make_world()

        self.assertEqual(
            "Growlithe",
            randomize_pokemon(world, "Charmander", ["Squirtle", "Growlithe", "Vulpix"], 1, FixedTriangularRandom()),
        )

    def test_randomize_pokemon_falls_back_to_full_list_without_type_matches(self) -> None:
        world = make_world()

        self.assertEqual(
            "Squirtle",
            randomize_pokemon(world, "Charmander", ["Squirtle", "Oddish"], 1, FixedTriangularRandom()),
        )

    def test_randomize_pokemon_prefers_closest_base_stat_total(self) -> None:
        world = make_world()

        self.assertEqual(
            "Ivysaur",
            randomize_pokemon(world, "Bulbasaur", ["Mewtwo", "Ivysaur", "Caterpie"], 2, FixedTriangularRandom()),
        )

    def test_randomize_pokemon_can_match_types_and_stats_together(self) -> None:
        world = make_world()

        self.assertEqual(
            "Oddish",
            randomize_pokemon(world, "Bulbasaur", ["Psyduck", "Oddish", "Bellsprout"], 3, FixedTriangularRandom()),
        )

    def test_process_pokemon_locations_counts_static_repeatable_pokemon_for_catch_em_all(self) -> None:
        repeatable_slot = SimpleNamespace(
            name="Route 4 Pokemon Center - Pokemon For Sale",
            type="Static Repeatable Pokemon",
            original_item="Bulbasaur",
        )
        wild_slots = [
            SimpleNamespace(name="Route 1 - Wild Pokemon - 1", type="Wild Encounter", original_item="Charmander"),
            SimpleNamespace(name="Route 1 - Wild Pokemon - 2", type="Wild Encounter", original_item="Charmander"),
        ]
        multiworld = FakeMultiWorld([repeatable_slot.name, *(slot.name for slot in wild_slots)])
        world = SimpleNamespace(
            options=SimpleNamespace(
                randomize_legendary_pokemon=FakeChoice(0, "vanilla"),
                randomize_pokemon_locations=FakeChoice(4, "completely_random"),
                catch_em_all=FakeChoice(1, "first_stage"),
                area_1_to_1_mapping=False,
                oaks_aide_rt_2=SimpleNamespace(value=0),
                oaks_aide_rt_11=SimpleNamespace(value=0),
                oaks_aide_rt_15=SimpleNamespace(value=0),
                elite_four_pokedex_condition=SimpleNamespace(total=0),
                accessibility="minimal",
            ),
            multiworld=multiworld,
            player=1,
            random=SimpleNamespace(
                shuffle=lambda sequence: None,
                sample=lambda sequence, count: sequence[:count],
            ),
            local_poke_data=poke_data.pokemon_data,
            create_item=lambda name: SimpleNamespace(name=name, location=None),
        )

        def fake_get_encounter_slots(world_obj, types):
            if types == ["Starter Pokemon"] or types == ["Legendary Pokemon"]:
                return []
            if types == ["Static Pokemon", "Static Repeatable Pokemon", "Missable Pokemon"]:
                return [repeatable_slot]
            if types == ["Wild Encounter"]:
                return wild_slots
            raise AssertionError(types)

        with mock.patch.object(encounters, "get_encounter_slots", side_effect=fake_get_encounter_slots), \
                mock.patch.object(encounters, "randomize_pokemon", side_effect=lambda self, mon, mons, typ, rnd: mon), \
                mock.patch.object(encounters.poke_data, "first_stage_pokemon", ["Bulbasaur"]):
            process_pokemon_locations(world)

        self.assertEqual("Bulbasaur", multiworld.get_location(repeatable_slot.name, 1).item.name)
        self.assertEqual("Charmander", multiworld.get_location("Route 1 - Wild Pokemon - 1", 1).item.name)
        self.assertEqual("Charmander", multiworld.get_location("Route 1 - Wild Pokemon - 2", 1).item.name)
