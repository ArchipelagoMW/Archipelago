from ..AutoWorld import World
from ..generic.Rules import set_rule, add_item_rule
from BaseClasses import Region, Location, Entrance, Item
from Utils import get_options, output_path
import typing
import os
import os.path
import threading

try:
    import pyevermizer  # from package
except ImportError:
    import traceback
    traceback.print_exc()
    from . import pyevermizer  # as part of the source tree

from . import Logic  # load logic mixin
from .Options import soe_options
from .Patch import SoEDeltaPatch, get_base_rom_path

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

_id_base = 64000
_id_offset: typing.Dict[int, int] = {
    pyevermizer.CHECK_ALCHEMY: _id_base + 0,  # alchemy 64000..64049
    pyevermizer.CHECK_BOSS: _id_base + 50,  # bosses 64050..6499
    pyevermizer.CHECK_GOURD: _id_base + 100,  # gourds 64100..64399
    pyevermizer.CHECK_NPC: _id_base + 400,  # npc 64400..64499
    # TODO: sniff 64500..64799
}

# cache native evermizer items and locations
_items = pyevermizer.get_items()
_locations = pyevermizer.get_locations()
# fix up texts for AP
for _loc in _locations:
    if _loc.type == pyevermizer.CHECK_GOURD:
        _loc.name = f'{_loc.name} #{_loc.index}'


def _get_location_mapping() -> typing.Tuple[typing.Dict[str, int], typing.Dict[int, pyevermizer.Location]]:
    name_to_id = {}
    id_to_raw = {}
    for loc in _locations:
        apid = _id_offset[loc.type] + loc.index
        id_to_raw[apid] = loc
        name_to_id[loc.name] = apid
    name_to_id['Done'] = None
    return name_to_id, id_to_raw


def _get_item_mapping() -> typing.Tuple[typing.Dict[str, int], typing.Dict[int, pyevermizer.Item]]:
    name_to_id = {}
    id_to_raw = {}
    for item in _items:
        if item.name in name_to_id:
            continue
        apid = _id_offset[item.type] + item.index
        id_to_raw[apid] = item
        name_to_id[item.name] = apid
    name_to_id['Victory'] = None
    return name_to_id, id_to_raw


class SoEWorld(World):
    """
    Secret of Evermore is a SNES action RPG. You learn alchemy spells, fight bosses and gather rocket parts to visit a
    space station where the final boss must be defeated. 
    """
    game: str = "Secret of Evermore"
    options = soe_options
    topology_present: bool = False
    remote_items: bool = False
    data_version = 1

    item_name_to_id, item_id_to_raw = _get_item_mapping()
    location_name_to_id, location_id_to_raw = _get_location_mapping()

    evermizer_seed: int
    connect_name: str

    _halls_ne_chest_names: typing.List[str] = [loc.name for loc in _locations if 'Halls NE' in loc.name]

    def __init__(self, *args, **kwargs):
        self.connect_name_available_event = threading.Event()
        super(SoEWorld, self).__init__(*args, **kwargs)

    def create_event(self, event: str) -> Item:
        progression = True
        return SoEItem(event, progression, None, self.player)

    def create_item(self, item: typing.Union[pyevermizer.Item, str], force_progression: bool = False) -> Item:
        if type(item) is str:
            item = self.item_id_to_raw[self.item_name_to_id[item]]
        return SoEItem(item.name, force_progression or item.progression, self.item_name_to_id[item.name], self.player)

    def create_regions(self):
        # TODO: generate *some* regions from locations' requirements?
        r = Region('Menu', None, 'Menu', self.player, self.world)
        r.exits = [Entrance(self.player, 'New Game', r)]
        self.world.regions += [r]

        r = Region('Ingame', None, 'Ingame', self.player, self.world)
        r.locations = [SoELocation(self.player, loc.name, self.location_name_to_id[loc.name], r)
                       for loc in _locations]
        r.locations.append(SoELocation(self.player, 'Done', None, r))
        self.world.regions += [r]

        self.world.get_entrance('New Game', self.player).connect(self.world.get_region('Ingame', self.player))

    def create_items(self):
        # add items to the pool
        self.world.itempool += list(map(lambda item: self.create_item(item), _items))

    def set_rules(self):
        self.world.completion_condition[self.player] = lambda state: state.has('Victory', self.player)
        # set Done from goal option once we have multiple goals
        set_rule(self.world.get_location('Done', self.player),
                 lambda state: state._soe_has(pyevermizer.P_FINAL_BOSS, self.world, self.player))
        set_rule(self.world.get_entrance('New Game', self.player), lambda state: True)
        for loc in _locations:
            location = self.world.get_location(loc.name, self.player)
            set_rule(location, self.make_rule(loc.requires))

    def make_rule(self, requires: typing.List[typing.Tuple[int]]) -> typing.Callable[[typing.Any], bool]:
        def rule(state) -> bool:
            for count, progress in requires:
                if not state._soe_has(progress, self.world, self.player, count):
                    return False
            return True

        return rule

    def make_item_type_limit_rule(self, item_type: int):
        return lambda item: item.player != self.player or self.item_id_to_raw[item.code].type == item_type

    def generate_basic(self):
        # place Victory event
        self.world.get_location('Done', self.player).place_locked_item(self.create_event('Victory'))
        # place wings in halls NE to avoid softlock
        wings_location = self.world.random.choice(self._halls_ne_chest_names)
        wings_item = self.create_item('Wings')
        self.world.get_location(wings_location, self.player).place_locked_item(wings_item)
        self.world.itempool.remove(wings_item)
        # generate stuff for later
        self.evermizer_seed = self.world.random.randint(0, 2 ** 16 - 1)  # TODO: make this an option for "full" plando?

    def generate_output(self, output_directory: str):
        player_name = self.world.get_player_name(self.player)
        self.connect_name = player_name[:32]
        while len(self.connect_name.encode('utf-8')) > 32:
            self.connect_name = self.connect_name[:-1]
        self.connect_name_available_event.set()
        placement_file = None
        out_file = None
        try:
            money = self.world.money_modifier[self.player].value
            exp = self.world.exp_modifier[self.player].value
            rom_file = get_base_rom_path()
            out_base = output_path(output_directory, f'AP_{self.world.seed_name}_P{self.player}_{player_name}')
            out_file = out_base + '.sfc'
            placement_file = out_base + '.txt'
            patch_file = out_base + '.apsoe'
            flags = 'l'  # spoiler log
            for option_name in self.options:
                option = getattr(self.world, option_name)[self.player]
                if hasattr(option, 'to_flag'):
                    flags += option.to_flag()

            with open(placement_file, "wb") as f:  # generate placement file
                for location in filter(lambda l: l.player == self.player, self.world.get_locations()):
                    item = location.item
                    if item.code is None:
                        continue  # skip events
                    loc = self.location_id_to_raw[location.address]
                    if item.player != self.player:
                        line = f'{loc.type},{loc.index}:{pyevermizer.CHECK_NONE},{item.code},{item.player}\n'
                    else:
                        item = self.item_id_to_raw[item.code]
                        line = f'{loc.type},{loc.index}:{item.type},{item.index}\n'
                    f.write(line.encode('utf-8'))

            if not os.path.exists(rom_file):
                raise FileNotFoundError(rom_file)
            if (pyevermizer.main(rom_file, out_file, placement_file, self.world.seed_name, self.connect_name,
                                 self.evermizer_seed, flags, money, exp)):
                raise RuntimeError()
            patch = SoEDeltaPatch(patch_file, player=self.player,
                                  player_name=player_name, patched_path=out_file)
            patch.write()
        except:
            raise
        finally:
            try:
                os.unlink(placement_file)
                os.unlink(out_file)
                os.unlink(out_file[:-4] + '_SPOILER.log')
            except:
                pass

    def modify_multidata(self, multidata: dict):
        # wait for self.connect_name to be available.
        self.connect_name_available_event.wait()
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if self.connect_name and self.connect_name != self.world.player_name[self.player]:
            payload = multidata["connect_names"][self.world.player_name[self.player]]
            multidata["connect_names"][self.connect_name] = payload


class SoEItem(Item):
    game: str = "Secret of Evermore"


class SoELocation(Location):
    game: str = "Secret of Evermore"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.event = not address
