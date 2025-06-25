import unittest

from BaseClasses import CollectionState
from worlds.AutoWorld import AutoWorldRegister
from . import setup_solo_multiworld, gen_steps


class TestBase(unittest.TestCase):
    gen_steps = gen_steps

    default_settings_unreachable_regions = {
        "A Link to the Past": {
            "Chris Houlihan Room",  # glitch room by definition
            "Desert Northern Cliffs",  # on top of mountain, only reachable via OWG
            "Dark Death Mountain Bunny Descent Area"  # OWG Mountain descent
        },
        # These Blasphemous regions are not reachable with default options
        "Blasphemous": {
            "D01Z04S13[SE]", # difficulty must be hard
            "D01Z05S25[E]", # difficulty must be hard
            "D02Z02S05[W]", # difficulty must be hard and purified_hand must be true
            "D04Z01S06[E]", # purified_hand must be true
            "D04Z02S02[NE]", # difficulty must be hard and purified_hand must be true
            "D05Z01S11[SW]", # difficulty must be hard
            "D06Z01S08[N]", # difficulty must be hard and purified_hand must be true
            "D20Z02S11[NW]", # difficulty must be hard
            "D20Z02S11[E]", # difficulty must be hard
        },
        "Ocarina of Time": {
            "Prelude of Light Warp",  # Prelude is not progression by default
            "Serenade of Water Warp",  # Serenade is not progression by default
            "Lost Woods Mushroom Timeout",  # trade quest starts after this item
            "ZD Eyeball Frog Timeout",  # trade quest starts after this item
            "ZR Top of Waterfall",  # dummy region used for entrance shuffle
        },
        # The following SM regions are only used when the corresponding StartLocation option is selected (so not with
        # default settings). Also, those don't have any entrances as they serve as starting Region (that's why they
        # have to be excluded for testAllStateCanReachEverything).
        "Super Metroid": {
            "Ceres",
            "Gauntlet Top",
            "Mama Turtle"
        }
    }

    def test_default_all_state_can_reach_everything(self):
        """Ensure all state can reach everything and complete the game with the defined options"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            unreachable_regions = self.default_settings_unreachable_regions.get(game_name, set())
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type)
                state = multiworld.get_all_state(False)
                for location in multiworld.get_locations():
                    with self.subTest("Location should be reached", location=location.name):
                        self.assertTrue(location.can_reach(state), f"{location.name} unreachable")

                for region in multiworld.get_regions():
                    if region.name in unreachable_regions:
                        with self.subTest("Region should be unreachable", region=region.name):
                            self.assertFalse(region.can_reach(state))
                    else:
                        with self.subTest("Region should be reached", region=region.name):
                            self.assertTrue(region.can_reach(state))

                with self.subTest("Completion Condition"):
                    self.assertTrue(multiworld.can_beat_game(state))

    def test_default_empty_state_can_reach_something(self):
        """Ensure empty state can reach at least one location with the defined options"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest("Game", game=game_name):
                multiworld = setup_solo_multiworld(world_type)
                state = CollectionState(multiworld)
                all_locations = multiworld.get_locations()
                if all_locations:
                    locations = set()
                    for location in all_locations:
                        if location.can_reach(state):
                            locations.add(location)
                    self.assertGreater(len(locations), 0,
                                       msg="Need to be able to reach at least one location to get started.")

    def test_collecting_and_removing_items_maintains_reachability(self):
        """Test that worlds don't have situations where collecting an item makes a location become unreachable,
        or removing an item makes a location become reachable. (Usually due to faulty "score calculation" algorithms)"""

        for game_name, world_type in AutoWorldRegister.world_types.items():
            with self.subTest(game_name, game_name=game_name):
                multiworld = setup_solo_multiworld(
                    world_type,
                    steps=(
                        "generate_early",
                        "create_regions",
                        "create_items",
                        "set_rules",
                        "connect_entrances",
                        "generate_basic"
                    )
                )
                proxy_world = multiworld.worlds[1]

                # First, we need to get a set of items to test on.
                # All of them need to be progression items. To ensure this, we need to do a bit of work.
                # Since this is an actual world that gen steps were called on, we can take the ones from the item pool.
                items_from_pool = [item for item in multiworld.itempool if item.advancement]

                # However, the intent of this test is also to catch scenarios in which extra items were created,
                # e.g. through plando or itemlinks. So, we make some random items from the datapackage as well.
                # First, generate one copy of each item in the world's datapackage using the world's create_item.
                additional_candidate_items = [
                    proxy_world.create_item(item_name) for item_name in world_type.item_name_to_id
                ]
                # Only keep progression items.
                additional_candidate_items = [item for item in additional_candidate_items if item.advancement]

                # Now, we choose random items over and over, allowing duplicates but handling them carefully.-+-
                additional_chosen_items = []
                target_amount = len(additional_candidate_items) / 4
                while len(additional_chosen_items) < target_amount:
                    random_item = proxy_world.random.choice(additional_candidate_items)

                    # If the chosen candidate item is not already in our list of chosen items, just use that instance
                    if random_item not in additional_chosen_items:
                        additional_chosen_items.append(random_item)
                        continue

                    # Otherwise, we'll have to create a new copy.
                    # Depending on the world's create_item, this new instance may not be an advancement.
                    # If that's the case, we stop trying to use this item.
                    second_or_higher_copy = proxy_world.create_item(random_item.name)
                    if not second_or_higher_copy.advancement:
                        additional_candidate_items.remove(random_item)

                        if not additional_candidate_items:
                            break

                        continue

                    additional_chosen_items.append(random_item)

                chosen_items = [*items_from_pool, *additional_chosen_items]
                proxy_world.random.shuffle(chosen_items)

                all_locations = list(proxy_world.get_locations())

                state = CollectionState(multiworld)
                reachable_locations = {
                    location for location in all_locations if location.can_reach(state)
                }
                for item in chosen_items:
                    prog_items_before = str(state.prog_items)  # For error message

                    state.collect(item)

                    new_reachable_locations = {
                        location for location in all_locations if location.can_reach(state)
                    }
                    locations_that_became_unreachable = reachable_locations - new_reachable_locations

                    self.assertFalse(
                        locations_that_became_unreachable,
                        f"Locations {locations_that_became_unreachable} became unreachable after collecting "
                        f"{item} into state. Progression items were:\n"
                        f"Before: {prog_items_before}\nAfter: {state.prog_items}"
                    )

                    reachable_locations = new_reachable_locations

                proxy_world.random.shuffle(chosen_items)

                for item in chosen_items:
                    prog_items_before = str(state.prog_items)  # For error message

                    state.remove(item)

                    new_reachable_locations = {
                        location for location in all_locations if location.can_reach(state)
                    }
                    locations_that_became_reachable = new_reachable_locations - reachable_locations

                    self.assertFalse(
                        locations_that_became_reachable,
                        f"Locations {locations_that_became_reachable} became reachable after removing "
                        f"{item} from state. Progression items were:\n"
                        f"Before: {prog_items_before}\nAfter: {state.prog_items}"
                    )

                    reachable_locations = new_reachable_locations