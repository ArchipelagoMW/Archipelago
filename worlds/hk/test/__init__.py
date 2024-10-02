from test.bases import WorldTestBase
import typing
from BaseClasses import CollectionState  # , Item, MultiWorld
from .. import HKWorld


class HKTestBase(WorldTestBase):
    game = "Hollow Knight"
    world: HKWorld

    def assertAccessIndependency(
            self,
            locations: typing.List[str],
            possible_items: typing.Iterable[typing.Iterable[str]],
            only_check_listed: bool = False) -> None:
        """Asserts that the provided locations can't be reached without
        the listed items but can be reached with any
        one of the provided combinations"""
        all_items = [
            item_name for
            item_names in
            possible_items for
            item_name in
            item_names
            ]

        state = CollectionState(self.multiworld)

        for item_names in possible_items:
            items = self.get_items_by_name(item_names)
            for item in items:
                self.collect_all_but(item.name)
            for location in locations:
                self.assertTrue(state.can_reach(location, "Location", 1),
                                f"{location} not reachable with {item_names}")
            for item in items:
                state.remove(item)

    def assertAccessWithout(
            self,
            locations: typing.List[str],
            possible_items: typing.Iterable[typing.Iterable[str]]) -> None:
        """Asserts that the provided locations can't be reached without the
        listed items but can be reached with any
        one of the provided combinations"""
        all_items = [
            item_name for
            item_names in
            possible_items for
            item_name in
            item_names
            ]

        state = CollectionState(self.multiworld)
        self.collect_all_but(all_items, state)
        for location in locations:
            self.assertTrue(
                state.can_reach(location, "Location", 1),
                f"{location} is not reachable without {all_items}")


class selectSeedHK(WorldTestBase):
    game = "Hollow Knight"
    # player: typing.ClassVar[int] = 1
    seed = 0
    world: HKWorld

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)
