from typing import Callable
from BaseClasses import CollectionState, Item, Region, Location, Entrance, Tutorial, ItemClassification
from .ArbitraryGameDefs import BASE_ID, AutopelagoRegion, location_base_ids, num_locations_in
from .Items import item_table
from ..AutoWorld import World, WebWorld

# options aren't ready yet
# from .Options import ArchipelagoOptions

game_name = "Autopelago"

def _get_autopelago_entrance_name(r_from: AutopelagoRegion, r_to: AutopelagoRegion):
    return f"from {r_from.name} to {r_to.name}"


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
    game = game_name
    topology_present = True
    data_version = 1
    web = AutopelagoWebWorld()

    # options aren't ready yet
    #options_dataclass = ArchipelagoOptions
    #options: ArchipelagoOptions

    location_name_to_id = {
        r.get_location_name(i): location_base_ids[r] + i
        for r in AutopelagoRegion
        for i in range(num_locations_in[r])
    }

    item_name_to_id = {
        item_table[i]: BASE_ID + i
        for i in range(len(location_name_to_id))
    }

    @staticmethod
    def _build_item_defs(item_name_by_location_name: dict[str, str], item_name_to_id: dict[str, int]):
        item_pool: list[tuple[str, ItemClassification, int]] = []

        def _appendOne(reg: AutopelagoRegion, c: ItemClassification, item_id_offset: int = 0):
            location_name = reg.get_location_name(item_id_offset)
            item_name = item_name_by_location_name[location_name]
            item_pool.append((item_name, c, item_name_to_id[item_name]))

        def _appendMany(reg: AutopelagoRegion, prog_count = 0):
            num = num_locations_in[reg]
            midpoint = (num - prog_count + 1) // 2
            for item_id_offset in range(num):
                _appendOne(reg, \
                    ItemClassification.progression_skip_balancing if item_id_offset < prog_count else \
                    ItemClassification.useful if item_id_offset < midpoint else \
                    ItemClassification.filler,
                    item_id_offset)

        _appendOne(AutopelagoRegion.A, ItemClassification.progression)
        _appendOne(AutopelagoRegion.B, ItemClassification.progression)
        _appendOne(AutopelagoRegion.C, ItemClassification.progression)
        _appendOne(AutopelagoRegion.D, ItemClassification.progression)
        _appendOne(AutopelagoRegion.E, ItemClassification.progression)
        _appendOne(AutopelagoRegion.F, ItemClassification.progression)
        _appendOne(AutopelagoRegion.TryingForGoal, ItemClassification.progression)

        _appendMany(AutopelagoRegion.Before8Rats, 8)
        _appendMany(AutopelagoRegion.After8RatsBeforeA)
        _appendMany(AutopelagoRegion.After8RatsBeforeB)
        _appendMany(AutopelagoRegion.AfterABeforeC)
        _appendMany(AutopelagoRegion.AfterBBeforeD)
        _appendMany(AutopelagoRegion.AfterCBefore20Rats, 3)
        _appendMany(AutopelagoRegion.AfterDBefore20Rats, 3)
        _appendMany(AutopelagoRegion.After20RatsBeforeE)
        _appendMany(AutopelagoRegion.After20RatsBeforeF)

        return item_pool

    _item_name_by_location_name: dict[str, str] = { }
    _next_item_index = 0
    for location_name, location_id in location_name_to_id.items():
        _item_name_by_location_name[location_name] = item_table[_next_item_index]
        _next_item_index += 1

    _item_defs = _build_item_defs(_item_name_by_location_name, item_name_to_id)
    _item_defs_by_name = { i[0]: i for i in _item_defs }

    def set_rules(self):
        def _connect(r_from: AutopelagoRegion, r_to: AutopelagoRegion, access_rule: Callable[[CollectionState], bool] | None = None, is_reversed = False):
            r_from_real = self.multiworld.get_region(r_from.get_archipelago_region_name(), self.player)
            r_to_real = self.multiworld.get_region(r_to.get_archipelago_region_name(), self.player)
            connection = Entrance(self.player, '', r_from_real)
            if access_rule:
                connection.access_rule = access_rule
            r_from_real.exits.append(connection)
            connection.connect(r_to_real)
            if not is_reversed:
                _connect(r_to, r_from, is_reversed=True)

        _connect(AutopelagoRegion.Before8Rats, AutopelagoRegion.After8RatsBeforeA, lambda state: state.prog_items[self.player].total() >= 8)
        _connect(AutopelagoRegion.Before8Rats, AutopelagoRegion.After8RatsBeforeB, lambda state: state.prog_items[self.player].total() >= 8)
        _connect(AutopelagoRegion.After8RatsBeforeA, AutopelagoRegion.A)
        _connect(AutopelagoRegion.After8RatsBeforeB, AutopelagoRegion.B)
        _connect(AutopelagoRegion.A, AutopelagoRegion.AfterABeforeC, lambda state: state.has(self._item_name_by_location_name["a"], self.player))
        _connect(AutopelagoRegion.B, AutopelagoRegion.AfterBBeforeD, lambda state: state.has(self._item_name_by_location_name["b"], self.player))
        _connect(AutopelagoRegion.AfterABeforeC, AutopelagoRegion.C)
        _connect(AutopelagoRegion.AfterBBeforeD, AutopelagoRegion.D)
        _connect(AutopelagoRegion.C, AutopelagoRegion.AfterCBefore20Rats, lambda state: state.has(self._item_name_by_location_name["c"], self.player))
        _connect(AutopelagoRegion.D, AutopelagoRegion.AfterDBefore20Rats, lambda state: state.has(self._item_name_by_location_name["d"], self.player))
        _connect(AutopelagoRegion.AfterCBefore20Rats, AutopelagoRegion.After20RatsBeforeE, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.AfterCBefore20Rats, AutopelagoRegion.After20RatsBeforeF, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeE, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeF, lambda state: state.prog_items[self.player].total() >= 20)
        _connect(AutopelagoRegion.After20RatsBeforeE, AutopelagoRegion.E)
        _connect(AutopelagoRegion.After20RatsBeforeF, AutopelagoRegion.F)
        _connect(AutopelagoRegion.E, AutopelagoRegion.TryingForGoal, lambda state: state.has(self._item_name_by_location_name["e"], self.player))
        _connect(AutopelagoRegion.F, AutopelagoRegion.TryingForGoal, lambda state: state.has(self._item_name_by_location_name["f"], self.player))

        goal_item_name = self._item_name_by_location_name["goal"]
        self.multiworld.get_location("goal", self.player).place_locked_item(self.create_item(goal_item_name))
        self.multiworld.completion_condition[self.player] = lambda state: state.has(goal_item_name, self.player)

    def create_item(self, name: str) -> Item:
        (_, classification, code) = self._item_defs_by_name[name]
        item = AutopelagoItem(name, classification, code, self.player)
        return item

    def create_items(self):
        goal_item_name = self._item_name_by_location_name["goal"]
        self.multiworld.itempool += (self.create_item(name) for name, _, _ in self._item_defs if name != goal_item_name)

    def create_regions(self):
        self.multiworld.regions += (self.create_region(r) for r in AutopelagoRegion)

    def create_region(self, r: AutopelagoRegion):
        region = Region(r.get_archipelago_region_name(), self.player, self.multiworld)
        for i in range(num_locations_in[r]):
            location_name = r.get_location_name(i)
            location_id = self.location_name_to_id[location_name]
            location = AutopelagoLocation(self.player, location_name, location_id, region)
            region.locations.append(location)
        return region

    def get_filler_item_name(self) -> str:
        return "Monkey's Paw"


class AutopelagoItem(Item):
    game = game_name


class AutopelagoLocation(Location):
    game = game_name
