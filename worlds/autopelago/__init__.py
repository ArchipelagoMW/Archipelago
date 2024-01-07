from collections import ChainMap
from itertools import zip_longest
from BaseClasses import Item, MultiWorld, Region, Location, Entrance, Tutorial, ItemClassification
from .ArbitraryGameDefs import BASE_ID, AutopelagoRegion, AutopelagoLocationIds, connected_regions, get_autopelago_entrance_name, num_locations_in
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

    item_name_to_id = {}
    start_id = BASE_ID
    for item in item_table:
        item_name_to_id[item] = start_id
        start_id += 1

    location_name_to_id = dict(ChainMap([
        { "goal": AutopelagoRegion.TryingForGoal },
        { r.name.lower(): r for r in AutopelagoRegion.singles() },
        { f"b8r_{i}": i for i in AutopelagoLocationIds.before_8_rats },
        { f"a8rba_{i}": i for i in AutopelagoLocationIds.after_8_rats_before_a },
        { f"a8rbb_{i}": i for i in AutopelagoLocationIds.after_8_rats_before_b },
        { f"aabc_{i}": i for i in AutopelagoLocationIds.after_a_before_c },
        { f"abbd_{i}": i for i in AutopelagoLocationIds.after_b_before_d },
        { f"acb20r_{i}": i for i in AutopelagoLocationIds.after_c_before_20_rats },
        { f"adb20r_{i}": i for i in AutopelagoLocationIds.after_d_before_20_rats },
        { f"a20rbe_{i}": i for i in AutopelagoLocationIds.after_20_rats_before_e },
        { f"a20rbf_{i}": i for i in AutopelagoLocationIds.after_20_rats_before_f },
    ]))

    def set_rules(self):
        def _gate_by_specific_item(r_from: AutopelagoRegion, r_to: AutopelagoRegion):
            set_rule(_get_entrance(r_from, r_to), lambda state: state.has(r_from.get_location_name(0), self.player))

        def _gate_by_num_rats(r_from: AutopelagoRegion, r_to: AutopelagoRegion, num_rats: int):
            set_rule(_get_entrance(r_from, r_to), lambda state: state.prog_items[self.player].total() >= num_rats)

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

        location_goal = self.multiworld.get_location(AutopelagoRegion.TryingForGoal.get_location_name(0), self.player)
        self.multiworld.completion_condition[self.player] = lambda state: location_goal in state.locations_checked

    def create_item(self, name: str) -> Item:
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):
        item_pool = []

        def _appendOne(c: ItemClassification):
            item_pool.append(AutopelagoItem(
                item_table[len(item_pool)],
                c,
                self.item_id_to_name[item_table[len(item_pool)]],
                self.player
            ))

        def _appendMany(r: list[int], prog_count = 0):
            midpoint = (len(r) - prog_count) // 2
            for item_id_offset in range(len(r)):
                _appendOne(\
                    ItemClassification.progression if item_id_offset < prog_count else \
                    ItemClassification.useful if item_id_offset < midpoint else \
                    ItemClassification.filler)

        for _ in AutopelagoRegion.singles():
            _appendOne(ItemClassification.progression)

        _appendMany(AutopelagoLocationIds.before_8_rats, 8)
        _appendMany(AutopelagoLocationIds.after_8_rats_before_a)
        _appendMany(AutopelagoLocationIds.after_8_rats_before_b)
        _appendMany(AutopelagoLocationIds.after_a_before_c)
        _appendMany(AutopelagoLocationIds.after_b_before_d)
        _appendMany(AutopelagoLocationIds.after_c_before_20_rats, 4)
        _appendMany(AutopelagoLocationIds.after_d_before_20_rats, 4)
        _appendMany(AutopelagoLocationIds.after_20_rats_before_e)
        _appendMany(AutopelagoLocationIds.after_20_rats_before_f)

        self.multiworld.itempool += item_pool

    def create_regions(self):
        regions = { r: create_region(self.multiworld, self.player, r) for r in AutopelagoRegion }
        link(self.player, regions)
        self.multiworld.regions += regions.values()

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(item_table)


def create_region(world: MultiWorld, player: int, r: AutopelagoRegion):
    region = Region(r.name, player, world)
    for i, location_id in zip_longest(range(num_locations_in[r]), AutopelagoLocationIds.of(r)):
        location = AutopelagoLocation(player, r.get_location_name(i), location_id, region)
        region.locations.append(location)
    return region

def link(player: int, regions: dict[AutopelagoRegion, Region]):
    for r, base_r in regions.items():
        for connected_r in connected_regions.get(r):
            entrance = Entrance(player, get_autopelago_entrance_name(r, connected_r), base_r)
            base_r.exits.append(entrance)
            entrance.connect(base_r)


class AutopelagoItem(Item):
    game = game_name


class AutopelagoLocation(Location):
    game = game_name
