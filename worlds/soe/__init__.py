import itertools
import os
import os.path
import threading
import typing

import settings
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_item_rule, set_rule
from BaseClasses import Entrance, Item, ItemClassification, Location, LocationProgressType, Region, Tutorial
from Utils import output_path

import pyevermizer  # from package
# from . import pyevermizer  # as part of the source tree

from . import Logic  # load logic mixin
from .Options import soe_options, Difficulty, EnergyCore, RequiredFragments, AvailableFragments
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
instead of implementing virtual locations and virtual items, we simply use them in Logic.py
    e.g. 2DEs+Wheel+Gauge = Rocket

Rules and Locations live on the same logic tree returned by pyevermizer.get_logic()

TODO: for balancing we may want to generate Regions (with Entrances) for some
common rules, place the locations in those Regions and shorten the rules.


Item grouping currently supports
* Any <ingredient name> - "Any Water" matches all Water drops
* Any <healing item name> - "Any Petal" matches all Petal drops
* Any Moniez - Matches the talon/jewel/gold coin/credit drops from chests (not market, fountain or Mungola)
* Ingredients - Matches all ingredient drops
* Alchemy - Matches all alchemy formulas
* Weapons - Matches all weapons but Bazooka, Bone Crusher, Neutron Blade
* Traps - Matches all traps
"""

_id_base = 64000
_id_offset: typing.Dict[int, int] = {
    pyevermizer.CHECK_ALCHEMY: _id_base + 0,  # alchemy 64000..64049
    pyevermizer.CHECK_BOSS: _id_base + 50,  # bosses 64050..6499
    pyevermizer.CHECK_GOURD: _id_base + 100,  # gourds 64100..64399
    pyevermizer.CHECK_NPC: _id_base + 400,  # npc 64400..64499
    # TODO: sniff 64500..64799
    pyevermizer.CHECK_EXTRA: _id_base + 800,  # extra items 64800..64899
    pyevermizer.CHECK_TRAP: _id_base + 900,  # trap 64900..64999
}

# cache native evermizer items and locations
_items = pyevermizer.get_items()
_traps = pyevermizer.get_traps()
_extras = pyevermizer.get_extra_items()  # items that are not placed by default
_locations = pyevermizer.get_locations()
# fix up texts for AP
for _loc in _locations:
    if _loc.type == pyevermizer.CHECK_GOURD:
        _loc.name = f'{_loc.name} #{_loc.index}'
# item helpers
_ingredients = (
    'Wax', 'Water', 'Vinegar', 'Root', 'Oil', 'Mushroom', 'Mud Pepper', 'Meteorite', 'Limestone', 'Iron',
    'Gunpowder', 'Grease', 'Feather', 'Ethanol', 'Dry Ice', 'Crystal', 'Clay', 'Brimstone', 'Bone', 'Atlas Amulet',
    'Ash', 'Acorn'
)
_other_items = (
    'Call bead', 'Petal', 'Biscuit', 'Pixie Dust', 'Nectar', 'Honey', 'Moniez'
)


def _match_item_name(item, substr: str) -> bool:
    sub = item.name.split(' ', 1)[1] if item.name[0].isdigit() else item.name
    return sub == substr or sub == substr+'s'


def _get_location_mapping() -> typing.Tuple[typing.Dict[str, int], typing.Dict[int, pyevermizer.Location]]:
    name_to_id = {}
    id_to_raw = {}
    for loc in _locations:
        ap_id = _id_offset[loc.type] + loc.index
        id_to_raw[ap_id] = loc
        name_to_id[loc.name] = ap_id
    name_to_id['Done'] = None
    return name_to_id, id_to_raw


def _get_item_mapping() -> typing.Tuple[typing.Dict[str, int], typing.Dict[int, pyevermizer.Item]]:
    name_to_id = {}
    id_to_raw = {}
    for item in itertools.chain(_items, _extras, _traps):
        if item.name in name_to_id:
            continue
        ap_id = _id_offset[item.type] + item.index
        id_to_raw[ap_id] = item
        name_to_id[item.name] = ap_id
    name_to_id['Victory'] = None
    return name_to_id, id_to_raw


def _get_item_grouping() -> typing.Dict[str, typing.Set[str]]:
    groups = {}
    ingredients_group = set()
    for ingredient in _ingredients:
        group = set(item.name for item in _items if _match_item_name(item, ingredient))
        groups[f'Any {ingredient}'] = group
        ingredients_group |= group
    groups['Ingredients'] = ingredients_group
    for other in _other_items:
        groups[f'Any {other}'] = set(item.name for item in _items if _match_item_name(item, other))
    groups['Alchemy'] = set(item.name for item in _items if item.type == pyevermizer.CHECK_ALCHEMY)
    groups['Weapons'] = {'Spider Claw', 'Horn Spear', 'Gladiator Sword', 'Bronze Axe', 'Bronze Spear', 'Crusader Sword',
                         'Lance (Weapon)', 'Knight Basher', 'Atom Smasher', 'Laser Lance'}
    groups['Traps'] = {trap.name for trap in _traps}
    return groups


class SoEWebWorld(WebWorld):
    theme = 'jungle'
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Secret of Evermore randomizer. This guide covers single-player, multiworld and related"
        " software.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Black Sliver"]
    )]


class SoESettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the SoE US ROM"""
        description = "Secret of Evermore (USA) ROM"
        copy_to = "Secret of Evermore (USA).sfc"
        md5s = [SoEDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class SoEWorld(World):
    """
    Secret of Evermore is a SNES action RPG. You learn alchemy spells, fight bosses and gather rocket parts to visit a
    space station where the final boss must be defeated. 
    """
    game: str = "Secret of Evermore"
    option_definitions = soe_options
    settings: typing.ClassVar[SoESettings]
    topology_present = False
    data_version = 4
    web = SoEWebWorld()
    required_client_version = (0, 3, 5)

    item_name_to_id, item_id_to_raw = _get_item_mapping()
    location_name_to_id, location_id_to_raw = _get_location_mapping()
    item_name_groups = _get_item_grouping()

    trap_types = [name[12:] for name in option_definitions if name.startswith('trap_chance_')]

    evermizer_seed: int
    connect_name: str
    energy_core: int
    sequence_breaks: int
    out_of_bounds: int
    available_fragments: int
    required_fragments: int

    _halls_ne_chest_names: typing.List[str] = [loc.name for loc in _locations if 'Halls NE' in loc.name]

    def __init__(self, *args, **kwargs):
        self.connect_name_available_event = threading.Event()
        super(SoEWorld, self).__init__(*args, **kwargs)

    def generate_early(self) -> None:
        # store option values that change logic
        self.energy_core = self.multiworld.energy_core[self.player].value
        self.sequence_breaks = self.multiworld.sequence_breaks[self.player].value
        self.out_of_bounds = self.multiworld.out_of_bounds[self.player].value
        self.required_fragments = self.multiworld.required_fragments[self.player].value
        if self.required_fragments > self.multiworld.available_fragments[self.player].value:
            self.multiworld.available_fragments[self.player].value = self.required_fragments
        self.available_fragments = self.multiworld.available_fragments[self.player].value

    def create_event(self, event: str) -> Item:
        return SoEItem(event, ItemClassification.progression, None, self.player)

    def create_item(self, item: typing.Union[pyevermizer.Item, str]) -> Item:
        if isinstance(item, str):
            item = self.item_id_to_raw[self.item_name_to_id[item]]
        if item.type == pyevermizer.CHECK_TRAP:
            classification = ItemClassification.trap
        elif item.progression:
            classification = ItemClassification.progression
        elif item.useful:
            classification = ItemClassification.useful
        else:
            classification = ItemClassification.filler

        return SoEItem(item.name, classification, self.item_name_to_id[item.name], self.player)

    @classmethod
    def stage_assert_generate(cls, multiworld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def create_regions(self):
        # exclude 'hidden' on easy
        max_difficulty = 1 if self.multiworld.difficulty[self.player] == Difficulty.option_easy else 256

        # TODO: generate *some* regions from locations' requirements?
        menu = Region('Menu', self.player, self.multiworld)
        self.multiworld.regions += [menu]

        def get_sphere_index(evermizer_loc):
            """Returns 0, 1 or 2 for locations in spheres 1, 2, 3+"""
            if len(evermizer_loc.requires) == 1 and evermizer_loc.requires[0][1] != pyevermizer.P_WEAPON:
                return 2
            return min(2, len(evermizer_loc.requires))

        # create ingame region
        ingame = Region('Ingame', self.player, self.multiworld)

        # group locations into spheres (1, 2, 3+ at index 0, 1, 2)
        spheres: typing.Dict[int, typing.Dict[int, typing.List[SoELocation]]] = {}
        for loc in _locations:
            spheres.setdefault(get_sphere_index(loc), {}).setdefault(loc.type, []).append(
                SoELocation(self.player, loc.name, self.location_name_to_id[loc.name], ingame,
                            loc.difficulty > max_difficulty))

        # location balancing data
        trash_fills: typing.Dict[int, typing.Dict[int, typing.Tuple[int, int, int, int]]] = {
            0: {pyevermizer.CHECK_GOURD: (20, 40, 40, 40)},  # remove up to 40 gourds from sphere 1
            1: {pyevermizer.CHECK_GOURD: (70, 90, 90, 90)},  # remove up to 90 gourds from sphere 2
        }

        # mark some as excluded based on numbers above
        for trash_sphere, fills in trash_fills.items():
            for typ, counts in fills.items():
                count = counts[self.multiworld.difficulty[self.player].value]
                for location in self.multiworld.random.sample(spheres[trash_sphere][typ], count):
                    assert location.name != "Energy Core #285", "Error in sphere generation"
                    location.progress_type = LocationProgressType.EXCLUDED

        def sphere1_blocked_items_rule(item):
            if isinstance(item, SoEItem):
                # disable certain items in sphere 1
                if item.name in {"Gauge", "Wheel"}:
                    return False
                # and some more for non-easy, non-mystery
                if self.multiworld.difficulty[item.player] not in (Difficulty.option_easy, Difficulty.option_mystery):
                    if item.name in {"Laser Lance", "Atom Smasher", "Diamond Eye"}:
                        return False
            return True

        for locations in spheres[0].values():
            for location in locations:
                add_item_rule(location, sphere1_blocked_items_rule)

        # make some logically late(r) bosses priority locations to increase complexity
        if self.multiworld.difficulty[self.player] == Difficulty.option_mystery:
            late_count = self.multiworld.random.randint(0, 2)
        else:
            late_count = self.multiworld.difficulty[self.player].value
        late_bosses = ("Tiny", "Aquagoth", "Megataur", "Rimsala",
                       "Mungola", "Lightning Storm", "Magmar", "Volcano Viper")
        late_locations = self.multiworld.random.sample(late_bosses, late_count)

        # add locations to the world
        for sphere in spheres.values():
            for locations in sphere.values():
                for location in locations:
                    ingame.locations.append(location)
                    if location.name in late_locations:
                        location.progress_type = LocationProgressType.PRIORITY

        ingame.locations.append(SoELocation(self.player, 'Done', None, ingame))
        menu.connect(ingame, "New Game")
        self.multiworld.regions += [ingame]

    def create_items(self):
        # add regular items to the pool
        exclusions: typing.List[str] = []
        if self.energy_core != EnergyCore.option_shuffle:
            exclusions.append("Energy Core")  # will be placed in generate_basic or replaced by a fragment below
        items = list(map(lambda item: self.create_item(item), (item for item in _items if item.name not in exclusions)))

        # remove one pair of wings that will be placed in generate_basic
        items.remove(self.create_item("Wings"))

        def is_ingredient(item):
            for ingredient in _ingredients:
                if _match_item_name(item, ingredient):
                    return True
            return False

        # add energy core fragments to the pool
        ingredients = [n for n, item in enumerate(items) if is_ingredient(item)]
        if self.energy_core == EnergyCore.option_fragments:
            items.append(self.create_item("Energy Core Fragment"))  # replaces the vanilla energy core
            for _ in range(self.available_fragments - 1):
                if len(ingredients) < 1:
                    break  # out of ingredients to replace
                r = self.multiworld.random.choice(ingredients)
                ingredients.remove(r)
                items[r] = self.create_item("Energy Core Fragment")

        # add traps to the pool
        trap_count = self.multiworld.trap_count[self.player].value
        trap_chances = {}
        trap_names = {}
        if trap_count > 0:
            for trap_type in self.trap_types:
                trap_option = getattr(self.multiworld, f'trap_chance_{trap_type}')[self.player]
                trap_chances[trap_type] = trap_option.value
                trap_names[trap_type] = trap_option.item_name
            trap_chances_total = sum(trap_chances.values())
            if trap_chances_total == 0:
                for trap_type in trap_chances:
                    trap_chances[trap_type] = 1
                trap_chances_total = len(trap_chances)

        def create_trap() -> Item:
            v = self.multiworld.random.randrange(trap_chances_total)
            for t, c in trap_chances.items():
                if v < c:
                    return self.create_item(trap_names[t])
                v -= c
            assert False, "Bug in create_trap"

        for _ in range(trap_count):
            if len(ingredients) < 1:
                break  # out of ingredients to replace
            r = self.multiworld.random.choice(ingredients)
            ingredients.remove(r)
            items[r] = create_trap()

        self.multiworld.itempool += items

    def set_rules(self):
        self.multiworld.completion_condition[self.player] = lambda state: state.has('Victory', self.player)
        # set Done from goal option once we have multiple goals
        set_rule(self.multiworld.get_location('Done', self.player),
                 lambda state: state.soe_has(pyevermizer.P_FINAL_BOSS, self.multiworld, self.player))
        set_rule(self.multiworld.get_entrance('New Game', self.player), lambda state: True)
        for loc in _locations:
            location = self.multiworld.get_location(loc.name, self.player)
            set_rule(location, self.make_rule(loc.requires))

    def make_rule(self, requires: typing.List[typing.Tuple[int, int]]) -> typing.Callable[[typing.Any], bool]:
        def rule(state) -> bool:
            for count, progress in requires:
                if not state.soe_has(progress, self.multiworld, self.player, count):
                    return False
            return True

        return rule

    def make_item_type_limit_rule(self, item_type: int):
        return lambda item: item.player != self.player or self.item_id_to_raw[item.code].type == item_type

    def generate_basic(self):
        # place Victory event
        self.multiworld.get_location('Done', self.player).place_locked_item(self.create_event('Victory'))
        # place wings in halls NE to avoid softlock
        wings_location = self.multiworld.random.choice(self._halls_ne_chest_names)
        wings_item = self.create_item('Wings')
        self.multiworld.get_location(wings_location, self.player).place_locked_item(wings_item)
        # place energy core at vanilla location for vanilla mode
        if self.energy_core == EnergyCore.option_vanilla:
            energy_core = self.create_item('Energy Core')
            self.multiworld.get_location('Energy Core #285', self.player).place_locked_item(energy_core)
        # generate stuff for later
        self.evermizer_seed = self.multiworld.random.randint(0, 2 ** 16 - 1)  # TODO: make this an option for "full" plando?

    def generate_output(self, output_directory: str):
        player_name = self.multiworld.get_player_name(self.player)
        self.connect_name = player_name[:32]
        while len(self.connect_name.encode('utf-8')) > 32:
            self.connect_name = self.connect_name[:-1]
        self.connect_name_available_event.set()
        placement_file = ""
        out_file = ""
        try:
            money = self.multiworld.money_modifier[self.player].value
            exp = self.multiworld.exp_modifier[self.player].value
            switches: typing.List[str] = []
            if self.multiworld.death_link[self.player].value:
                switches.append("--death-link")
            if self.energy_core == EnergyCore.option_fragments:
                switches.extend(('--available-fragments', str(self.available_fragments),
                                 '--required-fragments', str(self.required_fragments)))
            rom_file = get_base_rom_path()
            out_base = output_path(output_directory, self.multiworld.get_out_file_name_base(self.player))
            out_file = out_base + '.sfc'
            placement_file = out_base + '.txt'
            patch_file = out_base + '.apsoe'
            flags = 'l'  # spoiler log
            for option_name in self.option_definitions:
                option = getattr(self.multiworld, option_name)[self.player]
                if hasattr(option, 'to_flag'):
                    flags += option.to_flag()

            with open(placement_file, "wb") as f:  # generate placement file
                for location in self.multiworld.get_locations(self.player):
                    item = location.item
                    assert item is not None, "Can't handle unfilled location"
                    if item.code is None or location.address is None:
                        continue  # skip events
                    loc = self.location_id_to_raw[location.address]
                    if item.player != self.player:
                        line = f'{loc.type},{loc.index}:{pyevermizer.CHECK_NONE},{item.code},{item.player}\n'
                    else:
                        soe_item = self.item_id_to_raw[item.code]
                        line = f'{loc.type},{loc.index}:{soe_item.type},{soe_item.index}\n'
                    f.write(line.encode('utf-8'))

            if not os.path.exists(rom_file):
                raise FileNotFoundError(rom_file)
            if (pyevermizer.main(rom_file, out_file, placement_file, self.multiworld.seed_name, self.connect_name,
                                 self.evermizer_seed, flags, money, exp, switches)):
                raise RuntimeError()
            patch = SoEDeltaPatch(patch_file, player=self.player,
                                  player_name=player_name, patched_path=out_file)
            patch.write()
        except Exception:
            raise
        finally:
            try:
                os.unlink(placement_file)
                os.unlink(out_file)
                os.unlink(out_file[:-4] + '_SPOILER.log')
            except FileNotFoundError:
                pass

    def modify_multidata(self, multidata: dict):
        # wait for self.connect_name to be available.
        self.connect_name_available_event.wait()
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if self.connect_name and self.connect_name != self.multiworld.player_name[self.player]:
            payload = multidata["connect_names"][self.multiworld.player_name[self.player]]
            multidata["connect_names"][self.connect_name] = payload

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(list(self.item_name_groups["Ingredients"]))


class SoEItem(Item):
    game: str = "Secret of Evermore"
    __slots__ = ()  # disable __dict__


class SoELocation(Location):
    game: str = "Secret of Evermore"
    __slots__ = ()  # disables __dict__ once Location has __slots__

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent: Region, exclude: bool = False):
        super().__init__(player, name, address, parent)
        # unconditional assignments favor a split dict, saving memory
        self.progress_type = LocationProgressType.EXCLUDED if exclude else LocationProgressType.DEFAULT
        self.event = not address
