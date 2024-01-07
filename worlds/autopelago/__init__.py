from BaseClasses import Item, Region, Location, Entrance, Tutorial, ItemClassification
from .ArbitraryGameDefs import BASE_ID, AutopelagoRegion, connected_regions, get_autopelago_entrance_name, location_base_ids, num_locations_in
from .Items import item_table
from ..generic.Rules import set_rule
from ..AutoWorld import World, WebWorld

# options aren't ready yet
# from .Options import ArchipelagoOptions

game_name = "Autopelago"


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
    topology_present = False
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

        def _appendOne(location: AutopelagoRegion, c: ItemClassification, item_id_offset: int = 0):
            item_name = item_name_by_location_name[location.get_location_name(item_id_offset)]
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
        _appendMany(AutopelagoRegion.AfterCBefore20Rats, 4)
        _appendMany(AutopelagoRegion.AfterDBefore20Rats, 4)
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
        def _gate_by_specific_item(r_from: AutopelagoRegion, r_to: AutopelagoRegion):
            set_rule(_get_entrance(r_from, r_to), lambda state: state.has(self._item_name_by_location_name[r_from.name.lower()], self.player))
            print(f"To get from {r_from.name} to {r_to.name}, you will need to receive {self._item_name_by_location_name[r_from.name.lower()]}")

        def _gate_by_num_rats(r_from: AutopelagoRegion, r_to: AutopelagoRegion, num_rats: int):
            set_rule(_get_entrance(r_from, r_to), lambda state: state.prog_items[self.player].total() >= num_rats)
            print(f"To get from {r_from.name} to {r_to.name}, you will need {num_rats} rat(s)")

        def _get_entrance(r_from: AutopelagoRegion, r_to: AutopelagoRegion):
            return self.multiworld.get_entrance(get_autopelago_entrance_name(r_from, r_to), self.player)

        _gate_by_num_rats(AutopelagoRegion.Before8Rats, AutopelagoRegion.After8RatsBeforeA, 8)
        _gate_by_num_rats(AutopelagoRegion.Before8Rats, AutopelagoRegion.After8RatsBeforeB, 8)
        _gate_by_specific_item(AutopelagoRegion.A, AutopelagoRegion.AfterABeforeC)
        _gate_by_specific_item(AutopelagoRegion.B, AutopelagoRegion.AfterBBeforeD)
        _gate_by_specific_item(AutopelagoRegion.C, AutopelagoRegion.AfterCBefore20Rats)
        _gate_by_specific_item(AutopelagoRegion.D, AutopelagoRegion.AfterDBefore20Rats)
        _gate_by_num_rats(AutopelagoRegion.AfterCBefore20Rats, AutopelagoRegion.After20RatsBeforeE, 20)
        _gate_by_num_rats(AutopelagoRegion.AfterCBefore20Rats, AutopelagoRegion.After20RatsBeforeF, 20)
        _gate_by_num_rats(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeE, 20)
        _gate_by_num_rats(AutopelagoRegion.AfterDBefore20Rats, AutopelagoRegion.After20RatsBeforeF, 20)
        _gate_by_specific_item(AutopelagoRegion.E, AutopelagoRegion.TryingForGoal)
        _gate_by_specific_item(AutopelagoRegion.F, AutopelagoRegion.TryingForGoal)

        self.multiworld.get_location("goal", self.player).place_locked_item(next(
            i for i in self.multiworld.itempool
            if i.player == self.player
                and i.name == self._item_name_by_location_name["goal"]
        ))

        self.multiworld.completion_condition[self.player] = lambda state: state.has(self._item_name_by_location_name["goal"], self.player);

    def create_item(self, name: str) -> Item:
        (_, classification, code) = self._item_defs_by_name[name]
        return AutopelagoItem(name, classification, code, self.player)

    def create_items(self):
        self.multiworld.itempool += [self.create_item(name) for name, _, _ in self._item_defs]

    def create_regions(self):
        regions = { r: self.create_region(r) for r in AutopelagoRegion }
        for r, base_r in regions.items():
            for connected_r in connected_regions.get(r):
                entrance = Entrance(self.player, get_autopelago_entrance_name(r, connected_r), base_r)
                base_r.exits.append(entrance)
                entrance.connect(base_r)

        # Archipelago hardcoded behavior we need a "Menu" region that connects to one of ours.
        menu = Region('Menu', self.player, self.multiworld)
        menu_to_start_entrance = Entrance(self.player, 'Start of Game', menu)
        menu.exits.append(menu_to_start_entrance)
        menu_to_start_entrance.connect(regions[AutopelagoRegion.Before8Rats])
        regions[None] = menu
        self.multiworld.regions += regions.values()

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(item_table)

    def create_region(self, r: AutopelagoRegion):
        region = Region(r.name, self.player, self.multiworld)
        for i in range(num_locations_in[r]):
            location = AutopelagoLocation(self.player, r.get_location_name(i), self.location_name_to_id[r.get_location_name(i)], region)
            region.locations.append(location)
        return region


class AutopelagoItem(Item):
    game = game_name


class AutopelagoLocation(Location):
    game = game_name
