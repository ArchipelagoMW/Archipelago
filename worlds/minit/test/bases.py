from test.bases import WorldTestBase
import typing
from BaseClasses import CollectionState
from .. import MinitWorld


class MinitTestBase(WorldTestBase):
    game = "Minit"
    world: MinitWorld

    def assertAccessIndependency(
            self,
            locations: list[str],
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
                self.collect_all_but(item)
            for location in locations:
                self.assertTrue(state.can_reach(location, "Location", 1),
                                f"{location} not reachable with {item_names}")
            for item in items:
                state.remove(item)

    def assertAccessWithout(
            self,
            locations: list[str],
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


class selectSeedMinit(WorldTestBase):
    game = "Minit"
    # player: typing.ClassVar[int] = 1
    seed = 0
    world: MinitWorld

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)
