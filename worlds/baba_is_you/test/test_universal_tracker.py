import random
import unittest
from argparse import Namespace

from BaseClasses import CollectionState, MultiWorld
from Generate import get_seed_name
from test.general import gen_steps
from worlds.AutoWorld import call_all

from ..levels import LEVEL_DATA
from ..locations import LOCATION_NAME_TO_ID
from ..world import BabaIsYouWorld


def setup_baba_multiworld(
    options: dict[str, object],
    seed: int,
    slot_data: dict[str, object] | None = None,
) -> MultiWorld:
    multiworld = MultiWorld(1)
    multiworld.game[1] = BabaIsYouWorld.game
    multiworld.player_name = {1: "Tester"}
    multiworld.set_seed(seed)
    random.seed(multiworld.seed)
    multiworld.seed_name = get_seed_name(random)

    args = Namespace()
    for option_name, option in BabaIsYouWorld.options_dataclass.type_hints.items():
        setattr(args, option_name, {1: option.from_any(options.get(option_name, option.default))})

    multiworld.set_options(args)
    multiworld.state = CollectionState(multiworld)
    if slot_data is not None:
        multiworld.re_gen_passthrough = {BabaIsYouWorld.game: slot_data}

    for step in gen_steps:
        call_all(multiworld, step)

    return multiworld


def get_connection_summary(world: BabaIsYouWorld) -> list[tuple[str, str | None]]:
    return sorted(
        (entrance.name, entrance.connected_region.name if entrance.connected_region else None)
        for entrance in world.multiworld.regions.entrance_cache[world.player].values()
    )


class TestUniversalTrackerRegeneration(unittest.TestCase):
    def test_regeneration_uses_slot_data_instead_of_local_options(self) -> None:
        source_options = {
            "goal": 0,
            "goal_levels": 40,
            "goal_blossoms": 8,
            "start_with_default_words": True,
            "open_map": False,
            "world_keys": True,
            "area_access": 0,
            "exclude_whoa": False,
            "exclude_gallery": False,
            "exclude_maze_transform": False,
            "blossom_petals": 16,
            "blossoms": 9,
            "first_gate_blossoms": 4,
            "second_gate_blossoms": 6,
            "third_gate_blossoms": 8,
            "complete_checks": True,
            "transformsanity": False,
            "level_shuffle": 2,
        }
        conflicting_local_options = {
            "goal": 5,
            "goal_levels": 10,
            "goal_blossoms": 2,
            "start_with_default_words": False,
            "open_map": True,
            "world_keys": False,
            "area_access": 0,
            "exclude_whoa": False,
            "exclude_gallery": False,
            "exclude_maze_transform": False,
            "blossom_petals": 0,
            "blossoms": 3,
            "first_gate_blossoms": 1,
            "second_gate_blossoms": 2,
            "third_gate_blossoms": 3,
            "complete_checks": False,
            "transformsanity": False,
            "level_shuffle": 0,
        }

        source_multiworld = setup_baba_multiworld(source_options, seed=12345)
        source_world = source_multiworld.worlds[1]
        slot_data = dict(source_world.fill_slot_data())

        regenerated_multiworld = setup_baba_multiworld(conflicting_local_options, seed=54321, slot_data=slot_data)
        regenerated_world = regenerated_multiworld.worlds[1]

        self.assertEqual(dict(regenerated_world.fill_slot_data()), slot_data)
        self.assertEqual(
            {location.name for location in regenerated_world.get_locations()},
            {location.name for location in source_world.get_locations()},
        )
        self.assertEqual(get_connection_summary(regenerated_world), get_connection_summary(source_world))
        self.assertEqual(
            BabaIsYouWorld.tracker_world["poptracker_name_mapping"],
            regenerated_world._build_poptracker_name_mapping(),
        )

        map_zero_target = regenerated_world.level_shuffle_dict.get("Map-0", "Map-0")
        self.assertEqual(
            BabaIsYouWorld.tracker_world["poptracker_name_mapping"]["Map-0/Map-0"],
            LOCATION_NAME_TO_ID[f"{LEVEL_DATA[map_zero_target]['name']}: Win"],
        )
