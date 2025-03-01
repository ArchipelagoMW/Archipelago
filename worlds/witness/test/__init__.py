from typing import Any, ClassVar, Dict, Iterable, List, Mapping, Union

from BaseClasses import CollectionState, Entrance, Item, Location, Region

from test.bases import WorldTestBase
from test.general import gen_steps, setup_multiworld
from test.multiworld.test_multiworlds import MultiworldTestBase

from .. import WitnessWorld
from ..data.utils import cast_not_none


class WitnessTestBase(WorldTestBase):
    game = "The Witness"
    player: ClassVar[int] = 1

    world: WitnessWorld

    def can_beat_game_with_items(self, items: Iterable[Item]) -> bool:
        """
        Check that the items listed are enough to beat the game.
        """

        state = CollectionState(self.multiworld)
        for item in items:
            state.collect(item)
        return state.multiworld.can_beat_game(state)

    def assert_dependency_on_event_item(self, spot: Union[Location, Region, Entrance], item_name: str) -> None:
        """
        WorldTestBase.assertAccessDependency, but modified & simplified to work with event items
        """
        event_items = [item for item in self.multiworld.get_items() if item.name == item_name]
        self.assertTrue(event_items, f"Event item {item_name} does not exist.")

        event_locations = [cast_not_none(event_item.location) for event_item in event_items]

        # Checking for an access dependency on an event item requires a bit of extra work,
        # as state.remove forces a sweep, which will pick up the event item again right after we tried to remove it.
        # So, we temporarily set the access rules of the event locations to be impossible.
        original_rules = {event_location.name: event_location.access_rule for event_location in event_locations}
        for event_location in event_locations:
            event_location.access_rule = lambda _: False

        # We can't use self.assertAccessDependency here, it doesn't work for event items. (As of 2024-06-30)
        test_state = self.multiworld.get_all_state(False)

        self.assertFalse(spot.can_reach(test_state), f"{spot.name} is reachable without {item_name}")

        test_state.collect(event_items[0])

        self.assertTrue(spot.can_reach(test_state), f"{spot.name} is not reachable despite having {item_name}")

        # Restore original access rules.
        for event_location in event_locations:
            event_location.access_rule = original_rules[event_location.name]

    def assert_location_exists(self, location_name: str, strict_check: bool = True) -> None:
        """
        Assert that a location exists in this world.
        If strict_check, also make sure that this (non-event) location COULD exist.
        """

        if strict_check:
            self.assertIn(location_name, self.world.location_name_to_id, f"Location {location_name} can never exist")

        try:
            self.world.get_location(location_name)
        except KeyError:
            self.fail(f"Location {location_name} does not exist.")

    def assert_location_does_not_exist(self, location_name: str, strict_check: bool = True) -> None:
        """
        Assert that a location exists in this world.
        If strict_check, be explicit about whether the location could exist in the first place.
        """

        if strict_check:
            self.assertIn(location_name, self.world.location_name_to_id, f"Location {location_name} can never exist")

        self.assertRaises(
            KeyError,
            lambda _: self.world.get_location(location_name),
            f"Location {location_name} exists, but is not supposed to.",
        )

    def assert_can_beat_with_minimally(self, required_item_counts: Mapping[str, int]) -> None:
        """
        Assert that the specified mapping of items is enough to beat the game,
        and that having one less of any item would result in the game being unbeatable.
        """
        # Find the actual items
        found_items = [item for item in self.multiworld.get_items() if item.name in required_item_counts]
        actual_items: Dict[str, List[Item]] = {item_name: [] for item_name in required_item_counts}
        for item in found_items:
            if len(actual_items[item.name]) < required_item_counts[item.name]:
                actual_items[item.name].append(item)

        # Assert that enough items exist in the item pool to satisfy the specified required counts
        for item_name, item_objects in actual_items.items():
            self.assertEqual(
                len(item_objects),
                required_item_counts[item_name],
                f"Couldn't find {required_item_counts[item_name]} copies of item {item_name} available in the pool, "
                f"only found {len(item_objects)}",
            )

        # assert that multiworld is beatable with the items specified
        self.assertTrue(
            self.can_beat_game_with_items(item for items in actual_items.values() for item in items),
            f"Could not beat game with items: {required_item_counts}",
        )

        # assert that one less copy of any item would result in the multiworld being unbeatable
        for item_name, item_objects in actual_items.items():
            with self.subTest(f"Verify cannot beat game with one less copy of {item_name}"):
                removed_item = item_objects.pop()
                self.assertFalse(
                    self.can_beat_game_with_items(item for items in actual_items.values() for item in items),
                    f"Game was beatable despite having {len(item_objects)} copies of {item_name} "
                    f"instead of the specified {required_item_counts[item_name]}",
                )
                item_objects.append(removed_item)


class WitnessMultiworldTestBase(MultiworldTestBase):
    options_per_world: List[Dict[str, Any]]
    common_options: Dict[str, Any] = {}

    def setUp(self) -> None:
        """
        Set up a multiworld with multiple players, each using different options.
        """

        self.multiworld = setup_multiworld([WitnessWorld] * len(self.options_per_world), ())

        for world, options in zip(self.multiworld.worlds.values(), self.options_per_world):
            for option_name, option_value in {**self.common_options, **options}.items():
                option = getattr(world.options, option_name)
                self.assertIsNotNone(option)

                option.value = option.from_any(option_value).value

        self.assertSteps(gen_steps)

    def collect_by_name(self, item_names: Union[str, Iterable[str]], player: int) -> List[Item]:
        """
        Collect all copies of a specified item name (or list of item names) for a player in the multiworld item pool.
        """

        items = self.get_items_by_name(item_names, player)
        for item in items:
            self.multiworld.state.collect(item)
        return items

    def get_items_by_name(self, item_names: Union[str, Iterable[str]], player: int) -> List[Item]:
        """
        Return all copies of a specified item name (or list of item names) for a player in the multiworld item pool.
        """

        if isinstance(item_names, str):
            item_names = (item_names,)
        return [item for item in self.multiworld.itempool if item.name in item_names and item.player == player]

    def assert_location_exists(self, location_name: str, player: int, strict_check: bool = True) -> None:
        """
        Assert that a location exists in this world.
        If strict_check, also make sure that this (non-event) location COULD exist.
        """

        world = self.multiworld.worlds[player]

        if strict_check:
            self.assertIn(location_name, world.location_name_to_id, f"Location {location_name} can never exist")

        try:
            world.get_location(location_name)
        except KeyError:
            self.fail(f"Location {location_name} does not exist.")

    def assert_location_does_not_exist(self, location_name: str, player: int, strict_check: bool = True) -> None:
        """
        Assert that a location exists in this world.
        If strict_check, be explicit about whether the location could exist in the first place.
        """

        world = self.multiworld.worlds[player]

        if strict_check:
            self.assertIn(location_name, world.location_name_to_id, f"Location {location_name} can never exist")

        self.assertRaises(
            KeyError,
            lambda _: world.get_location(location_name),
            f"Location {location_name} exists, but is not supposed to.",
        )
