from .Options import soe_options
from ..AutoWorld import World
from ..generic.Rules import set_rule
from BaseClasses import Region, Location, Entrance, Item
import typing
from . import Logic  # load logic mixin

try:
    import pyevermizer  # from package
except ImportError:
    from . import pyevermizer  # as part of the source tree

"""
In evermizer:

Items are uniquely defined by a pair of (type, id).
For most items this is their vanilla location (i.e. CHECK_GOURD, number).

Items have `provides`, which give the actual progression
instead of providing multiple events per item, we iterate through them in Logic.py
    e.g. Found any weapon

Locations have `requires` and `provides`.
Requirements have to be converted to (access) rules for AP
    e.g. Chest locked behind having a weapon
Provides could be events, but instead we iterate through the entire logic in Logic.py
    e.g. NPC available after fighting a Boss

Rules are special locations that don't have a physical location
instead of implementing virtual locations and virtual items, we simply use them  in Logic.py
    e.g. 2DEs+Wheel+Gauge = Rocket

Rules and Locations live on the same logic tree returned by pyevermizer.get_logic()

TODO: for balancing we may want to generate Regions (with Entrances) for some
common rules, place the locations in those Regions and shorten the rules.
"""

GAME_NAME = "Secret of Evermore"
ID_OFF_BASE = 64000
ID_OFFS: typing.Dict[int,int] = {
    pyevermizer.CHECK_ALCHEMY: ID_OFF_BASE + 0,  # alchemy 64000..64049
    pyevermizer.CHECK_BOSS: ID_OFF_BASE + 50,  # bosses 64050..6499
    pyevermizer.CHECK_GOURD: ID_OFF_BASE + 100,  # gourds 64100..64399
    pyevermizer.CHECK_NPC: ID_OFF_BASE + 400,  # npc 64400..64499
    # TODO: sniff 64500..64799
}


def _get_locations():
    locs = pyevermizer.get_locations()
    for loc in locs:
        if loc.type == 3:  # TODO: CHECK_GOURD
            loc.name = f'{loc.name} #{loc.index}'
    return locs


def _get_location_ids():
    m = {}
    for loc in _get_locations():
        m[loc.name] = ID_OFFS[loc.type] + loc.index
    m['Done'] = None
    return m


def _get_items():
    return pyevermizer.get_items()


def _get_item_ids():
    m = {}
    for item in _get_items():
        if item.name in m: continue
        m[item.name] = ID_OFFS[item.type] + item.index
    m['Victory'] = None
    return m


class SoEWorld(World):
    """
    TODO: insert game description here
    """
    game: str = GAME_NAME
    # options = soe_options
    topology_present: bool = True

    item_name_to_id = _get_item_ids()
    location_name_to_id = _get_location_ids()

    remote_items: bool = True  # False # True only for testing

    def generate_basic(self):
        print('SoE: generate_basic')
        itempool = [item for item in map(lambda item: self.create_item(item), _get_items())]
        self.world.itempool += itempool
        self.world.get_location('Done', self.player).place_locked_item(self.create_event('Victory'))

    def create_regions(self):
        # TODO: generate *some* regions from locations' requirements
        r = Region('Menu', None, 'Menu', self.player, self.world)
        r.exits = [Entrance(self.player, 'New Game', r)]
        self.world.regions += [r]

        r = Region('Ingame', None, 'Ingame', self.player, self.world)
        r.locations = [SoELocation(self.player, loc.name, self.location_name_to_id[loc.name], r)
                       for loc in _get_locations()]
        r.locations.append(SoELocation(self.player, 'Done', None, r))
        self.world.regions += [r]

        self.world.get_entrance('New Game', self.player).connect(self.world.get_region('Ingame', self.player))

    def create_event(self, event: str) -> Item:
        progression = True
        return SoEItem(event, progression, None, self.player)

    def create_item(self, item) -> Item:
        # TODO: if item is string: look up item by name
        return SoEItem(item.name, item.progression, self.item_name_to_id[item.name], self.player)

    def set_rules(self):
        print('SoE: set_rules')
        self.world.completion_condition[self.player] = lambda state: state.has('Victory', self.player)
        # set Done from goal option once we have multiple goals
        set_rule(self.world.get_location('Done', self.player),
                 lambda state: state._soe_has(pyevermizer.P_FINAL_BOSS, self.world, self.player))
        set_rule(self.world.get_entrance('New Game', self.player), lambda state: True)
        for loc in _get_locations():
            set_rule(self.world.get_location(loc.name, self.player), self.make_rule(loc.requires))

    def make_rule(self, requires):
        def rule(state):
            for count, progress in requires:
                if not state._soe_has(progress, self.world, self.player, count):
                    return False
            return True

        return rule


class SoEItem(Item):
    game: str = GAME_NAME


class SoELocation(Location):
    game: str = GAME_NAME

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address
