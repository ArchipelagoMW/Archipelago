from typing import Callable
from BaseClasses import CollectionState, Item, Region, Location, Entrance, Tutorial, ItemClassification
from .ArbitraryGameDefs import BASE_ID, GAME_NAME, AutopelagoRegion, num_locations_in
from .Items import item_table
from ..AutoWorld import World, WebWorld


class AutopelagoWebWorld(WebWorld):
    theme = 'partyTime'
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to playing Autopelago',
            language='English',
            file_name='guide_en.md',
            link='guide/en',
            authors=['Joe Amenta']
        )
    ]


class AutopelagoWorld(World):
    """
    An idle game, in the same vein as ArchipIDLE but intended to be more sophisticated.
    """
    game = GAME_NAME
    topology_present = False # it's static, so setting this to True isn't actually helpful
    data_version = 1
    web = AutopelagoWebWorld()

    location_name_to_id = { }
    item_name_to_id = { }
    _location_name_to_item_name: dict[str, str] = { }
    _item_name_to_classification: dict[str, ItemClassification] = { }
    _next_offset = 0
    for r in AutopelagoRegion:
        prog_count = 1 if r.get_location_name(0) in ["a", "b", "c", "d", "e", "f", "goal"] \
            else 8 if r == AutopelagoRegion.Before8Rats \
            else 3 if r == AutopelagoRegion.AfterCBefore20Rats \
            else 3 if r == AutopelagoRegion.AfterDBefore20Rats \
            else 0

        midpoint = (num_locations_in[r] - prog_count + 1) // 2

        for i in range(num_locations_in[r]):
            location_name = r.get_location_name(i)
            location_name_to_id[location_name] = BASE_ID + _next_offset
            item_name = item_table[_next_offset]
            item_name_to_id[item_name] = BASE_ID + _next_offset

            _location_name_to_item_name[location_name] = item_name
            _item_name_to_classification[item_name] = \
                ItemClassification.progression if prog_count == 1 else \
                ItemClassification.progression_skip_balancing if i < prog_count else \
                ItemClassification.useful if i < midpoint else \
                ItemClassification.filler

            _next_offset += 1

    # I DON'T KNOW WHY I NEED TO CREATE ONE EXTRA ITEM.
    item_name_to_id[item_table[_next_offset]] = BASE_ID + _next_offset
    _item_name_to_classification[item_table[_next_offset]] = ItemClassification.filler
    _next_offset += 1

    _goal_item_name = _location_name_to_item_name["goal"]

    def set_rules(self):
        def _connect(r_from: AutopelagoRegion, r_to: AutopelagoRegion, access_rule: Callable[[CollectionState], bool] | None = None):
            r_from_real = self.multiworld.get_region(r_from.name, self.player)
            r_to_real = self.multiworld.get_region(r_to.name, self.player)
            connection = Entrance(self.player, '', r_from_real)
            if access_rule:
                connection.access_rule = access_rule
            r_from_real.exits.append(connection)
            connection.connect(r_to_real)

        _connect(AutopelagoRegion.Before8Rats, AutopelagoRegion.After8RatsBeforeA, lambda state: state.prog_items[self.player].total() >= 8)
        _connect(AutopelagoRegion.Before8Rats, AutopelagoRegion.After8RatsBeforeB, lambda state: state.prog_items[self.player].total() >= 8)
        _connect(AutopelagoRegion.After8RatsBeforeA, AutopelagoRegion.A)
        _connect(AutopelagoRegion.After8RatsBeforeB, AutopelagoRegion.B)
        _connect(AutopelagoRegion.A, AutopelagoRegion.AfterABeforeC, lambda state: state.has(self._location_name_to_item_name["a"], self.player))
        _connect(AutopelagoRegion.B, AutopelagoRegion.AfterBBeforeD, lambda state: state.has(self._location_name_to_item_name["b"], self.player))
        _connect(AutopelagoRegion.AfterABeforeC, AutopelagoRegion.C)
        _connect(AutopelagoRegion.AfterBBeforeD, AutopelagoRegion.D)
        _connect(AutopelagoRegion.C, AutopelagoRegion.AfterCBefore20Rats, lambda state: state.has(self._location_name_to_item_name["c"], self.player))
        _connect(AutopelagoRegion.D, AutopelagoRegion.AfterDBefore20Rats, lambda state: state.has(self._location_name_to_item_name["d"], self.player))
        _connect(AutopelagoRegion.AfterCBefore20Rats, AutopelagoRegion.After20RatsBeforeE, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.AfterCBefore20Rats, AutopelagoRegion.After20RatsBeforeF, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeE, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeF, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.After20RatsBeforeE, AutopelagoRegion.E)
        _connect(AutopelagoRegion.After20RatsBeforeF, AutopelagoRegion.F)
        _connect(AutopelagoRegion.E, AutopelagoRegion.TryingForGoal, lambda state: state.has(self._location_name_to_item_name["e"], self.player))
        _connect(AutopelagoRegion.F, AutopelagoRegion.TryingForGoal, lambda state: state.has(self._location_name_to_item_name["f"], self.player))

        self.multiworld.get_location("goal", self.player).place_locked_item(self.create_item(self._goal_item_name))
        self.multiworld.completion_condition[self.player] = lambda state: state.has(self._goal_item_name, self.player)

    def create_item(self, name: str) -> Item:
        id = self.item_name_to_id[name]
        classification = self._item_name_to_classification[name]
        item = AutopelagoItem(name, classification, id, self.player)
        return item

    def create_items(self):
        self.multiworld.itempool += (self.create_item(name) for name in self.item_name_to_id if name != self._goal_item_name)

    def create_regions(self):
        self.multiworld.regions += (self.create_region(r) for r in AutopelagoRegion)

        # logic assumes that the player starts in a special hardcoded "Menu" region
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)
        entrance = Entrance(self.player, '', menu)
        menu.exits.append(entrance)
        entrance.connect(self.multiworld.get_region(AutopelagoRegion.Before8Rats.name, self.player))

    def create_region(self, r: AutopelagoRegion):
        region = Region(r.name, self.player, self.multiworld)
        for i in range(num_locations_in[r]):
            location_name = r.get_location_name(i)
            location_id = self.location_name_to_id[location_name]
            location = AutopelagoLocation(self.player, location_name, location_id, region)
            region.locations.append(location)
        return region

    def get_filler_item_name(self) -> str:
        return "Monkey's Paw"


class AutopelagoItem(Item):
    game = GAME_NAME


class AutopelagoLocation(Location):
    game = GAME_NAME

