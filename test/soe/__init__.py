import typing
import unittest
from argparse import Namespace
from test.general import gen_steps
from BaseClasses import MultiWorld, Item
from worlds import AutoWorld
from worlds.AutoWorld import call_all


class SoETestBase(unittest.TestCase):
    options: typing.Dict[str, typing.Any] = {}
    world: MultiWorld
    game = "Secret of Evermore"

    def setUp(self):
        self.world = MultiWorld(1)
        self.world.game[1] = self.game
        self.world.player_name = {1: "Tester"}
        self.world.set_seed()
        args = Namespace()
        for name, option in AutoWorld.AutoWorldRegister.world_types[self.game].option_definitions.items():
            setattr(args, name, {1: option.from_any(self.options.get(name, option.default))})
        self.world.set_options(args)
        self.world.set_default_common_options()
        for step in gen_steps:
            call_all(self.world, step)

    def collect_all_but(self, item_names: typing.Union[str, typing.Iterable[str]]):
        if isinstance(item_names, str):
            item_names = (item_names,)
        for item in self.world.get_items():
            if item.name not in item_names:
                self.world.state.collect(item)

    def get_item_by_name(self, item_name: str):
        for item in self.world.get_items():
            if item.name == item_name:
                return item
        raise ValueError("No such item")

    def get_items_by_name(self, item_names: typing.Union[str, typing.Iterable[str]]):
        if isinstance(item_names, str):
            item_names = (item_names,)
        return [item for item in self.world.itempool if item.name in item_names]

    def collect_by_name(self, item_names: typing.Union[str, typing.Iterable[str]]):
        items = self.get_items_by_name(item_names)
        self.collect(items)
        return items

    def collect(self, items: typing.Union[Item, typing.Iterable[Item]]):
        if isinstance(items, Item):
            items = (items,)
        for item in items:
            self.world.state.collect(item)

    def remove(self, items: typing.Union[Item, typing.Iterable[Item]]):
        if isinstance(items, Item):
            items = (items,)
        for item in items:
            if item.location and item.location.event and item.location in self.world.state.events:
                self.world.state.events.remove(item.location)
            self.world.state.remove(item)

    def can_reach_location(self, location):
        return self.world.state.can_reach(location, "Location", 1)

    def count(self, item_name):
        return self.world.state.count(item_name, 1)

    def assertAccessDependency(self, locations, possible_items):
        all_items = [item_name for item_names in possible_items for item_name in item_names]

        self.collect_all_but(all_items)
        for location in self.world.get_locations():
            self.assertEqual(self.world.state.can_reach(location), location.name not in locations)
        for item_names in possible_items:
            items = self.collect_by_name(item_names)
            for location in locations:
                self.assertTrue(self.can_reach_location(location))
            self.remove(items)

    def assertBeatable(self, beatable: bool):
        self.assertEqual(self.world.can_beat_game(self.world.state), beatable)
