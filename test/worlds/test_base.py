import typing
import unittest
from argparse import Namespace
from test.general import gen_steps
from BaseClasses import MultiWorld, Item
from worlds import AutoWorld
from worlds.AutoWorld import call_all


class WorldTestBase(unittest.TestCase):
    options: typing.Dict[str, typing.Any] = {}
    multiworld: MultiWorld

    game: typing.ClassVar[str]  # define game name in subclass, example "Secret of Evermore"
    auto_construct: typing.ClassVar[bool] = True
    """ automatically set up a world for each test in this class """

    def setUp(self) -> None:
        if self.auto_construct:
            self.world_setup()

    def world_setup(self, seed: typing.Optional[int] = None) -> None:
        if not hasattr(self, "game"):
            raise NotImplementedError("didn't define game name")
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = self.game
        self.multiworld.player_name = {1: "Tester"}
        self.multiworld.set_seed(seed)
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types[self.game].option_definitions.items():
            setattr(args, name, {
                1: option.from_any(self.options.get(name, getattr(option, "default")))
            })
        self.multiworld.set_options(args)
        self.multiworld.set_default_common_options()
        for step in gen_steps:
            call_all(self.multiworld, step)

    def collect_all_but(self, item_names: typing.Union[str, typing.Iterable[str]]) -> None:
        if isinstance(item_names, str):
            item_names = (item_names,)
        for item in self.multiworld.get_items():
            if item.name not in item_names:
                self.multiworld.state.collect(item)

    def get_item_by_name(self, item_name: str) -> Item:
        for item in self.multiworld.get_items():
            if item.name == item_name:
                return item
        raise ValueError("No such item")

    def get_items_by_name(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        if isinstance(item_names, str):
            item_names = (item_names,)
        return [item for item in self.multiworld.itempool if item.name in item_names]

    def collect_by_name(self, item_names: typing.Union[str, typing.Iterable[str]]) -> typing.List[Item]:
        """ collect all of the items in the item pool that have the given names """
        items = self.get_items_by_name(item_names)
        self.collect(items)
        return items

    def collect(self, items: typing.Union[Item, typing.Iterable[Item]]) -> None:
        if isinstance(items, Item):
            items = (items,)
        for item in items:
            self.multiworld.state.collect(item)

    def remove(self, items: typing.Union[Item, typing.Iterable[Item]]) -> None:
        if isinstance(items, Item):
            items = (items,)
        for item in items:
            if item.location and item.location.event and item.location in self.multiworld.state.events:
                self.multiworld.state.events.remove(item.location)
            self.multiworld.state.remove(item)

    def can_reach_location(self, location: str) -> bool:
        return self.multiworld.state.can_reach(location, "Location", 1)

    def count(self, item_name: str) -> int:
        return self.multiworld.state.count(item_name, 1)

    def assertAccessDependency(self,
                               locations: typing.List[str],
                               possible_items: typing.Iterable[typing.Iterable[str]]) -> None:
        all_items = [item_name for item_names in possible_items for item_name in item_names]

        self.collect_all_but(all_items)
        for location in self.multiworld.get_locations():
            self.assertEqual(self.multiworld.state.can_reach(location), location.name not in locations)
        for item_names in possible_items:
            items = self.collect_by_name(item_names)
            for location in locations:
                self.assertTrue(self.can_reach_location(location))
            self.remove(items)

    def assertBeatable(self, beatable: bool):
        self.assertEqual(self.multiworld.can_beat_game(self.multiworld.state), beatable)
