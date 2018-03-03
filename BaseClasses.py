import copy
from enum import Enum, unique
import logging
import json
from collections import OrderedDict


class World(object):

    def __init__(self, shuffle, logic, mode, difficulty, timer, progressive, goal, algorithm, place_dungeon_items, check_beatable_only, shuffle_ganon, quickswap, fastmenu, disable_music, keysanity, custom, customitemarray):
        self.shuffle = shuffle
        self.logic = logic
        self.mode = mode
        self.difficulty = difficulty
        self.timer = timer
        self.progressive = progressive
        self.goal = goal
        self.algorithm = algorithm
        self.dungeons = []
        self.regions = []
        self.itempool = []
        self.seed = None
        self.state = CollectionState(self)
        self.required_medallions = ['Ether', 'Quake']
        self._cached_locations = None
        self._entrance_cache = {}
        self._region_cache = {}
        self._entrance_cache = {}
        self._location_cache = {}
        self.required_locations = []
        self.place_dungeon_items = place_dungeon_items  # configurable in future
        self.shuffle_bonk_prizes = False
        self.swamp_patch_required = False
        self.powder_patch_required = False
        self.ganon_at_pyramid = True
        self.ganonstower_vanilla = True
        self.sewer_light_cone = mode == 'standard'
        self.light_world_light_cone = False
        self.dark_world_light_cone = False
        self.treasure_hunt_count = 0
        self.treasure_hunt_icon = 'Triforce Piece'
        self.clock_mode = 'off'
        self.rupoor_cost = 10
        self.aga_randomness = True
        self.lock_aga_door_in_escape = False
        self.fix_trock_doors = self.shuffle != 'vanilla'
        self.save_and_quite_from_boss = False
        self.check_beatable_only = check_beatable_only
        self.fix_skullwoods_exit = self.shuffle not in ['vanilla', 'simple', 'restricted', 'dungeonssimple']
        self.fix_palaceofdarkness_exit = self.shuffle not in ['vanilla', 'simple', 'restricted', 'dungeonssimple']
        self.fix_trock_exit = self.shuffle not in ['vanilla', 'simple', 'restricted', 'dungeonssimple']
        self.shuffle_ganon = shuffle_ganon
        self.fix_gtower_exit = self.shuffle_ganon
        self.can_access_trock_eyebridge = None
        self.quickswap = quickswap
        self.fastmenu = fastmenu
        self.disable_music = disable_music
        self.keysanity = keysanity
        self.custom = custom
        self.customitemarray = customitemarray
        self.can_take_damage = True
        self.difficulty_requirements = None
        self.fix_fake_world = True
        self.spoiler = Spoiler(self)
        self.lamps_needed_for_dark_rooms = 1

    def intialize_regions(self):
        for region in self.regions:
            region.world = self

    def get_region(self, regionname):
        if isinstance(regionname, Region):
            return regionname
        try:
            return self._region_cache[regionname]
        except KeyError:
            for region in self.regions:
                if region.name == regionname:
                    self._region_cache[regionname] = region
                    return region
            raise RuntimeError('No such region %s' % regionname)

    def get_entrance(self, entrance):
        if isinstance(entrance, Entrance):
            return entrance
        try:
            return self._entrance_cache[entrance]
        except KeyError:
            for region in self.regions:
                for exit in region.exits:
                    if exit.name == entrance:
                        self._entrance_cache[entrance] = exit
                        return exit
            raise RuntimeError('No such entrance %s' % entrance)

    def get_location(self, location):
        if isinstance(location, Location):
            return location
        try:
            return self._location_cache[location]
        except KeyError:
            for region in self.regions:
                for r_location in region.locations:
                    if r_location.name == location:
                        self._location_cache[location] = r_location
                        return r_location
        raise RuntimeError('No such location %s' % location)

    def get_all_state(self, keys=False):
        ret = CollectionState(self)

        def soft_collect(item):
            if item.name.startswith('Progressive '):
                if 'Sword' in item.name:
                    if ret.has('Golden Sword'):
                        pass
                    elif ret.has('Tempered Sword') and self.difficulty_requirements.progressive_sword_limit >= 4:
                        ret.prog_items.append('Golden Sword')
                    elif ret.has('Master Sword') and self.difficulty_requirements.progressive_sword_limit >= 3:
                        ret.prog_items.append('Tempered Sword')
                    elif ret.has('Fighter Sword') and self.difficulty_requirements.progressive_sword_limit >= 2:
                        ret.prog_items.append('Master Sword')
                    elif self.difficulty_requirements.progressive_sword_limit >= 1:
                        ret.prog_items.append('Fighter Sword')
                elif 'Glove' in item.name:
                    if ret.has('Titans Mitts'):
                        pass
                    elif ret.has('Power Glove'):
                        ret.prog_items.append('Titans Mitts')
                    else:
                        ret.prog_items.append('Power Glove')
                elif 'Shield' in item.name:
                    if ret.has('Mirror Shield'):
                        pass
                    elif ret.has('Red Shield') and self.difficulty_requirements.progressive_shield_limit >= 3:
                        ret.prog_items.append('Mirror Shield')
                    elif ret.has('Blue Shield')  and self.difficulty_requirements.progressive_shield_limit >= 2:
                        ret.prog_items.append('Red Shield')
                    elif self.difficulty_requirements.progressive_shield_limit >= 1:
                        ret.prog_items.append('Blue Shield')
            elif item.name.startswith('Bottle'):
                if ret.bottle_count() < self.difficulty_requirements.progressive_bottle_limit:
                    ret.prog_items.append(item.name)
            elif item.advancement or item.key:
                ret.prog_items.append(item.name)

        for item in self.itempool:
            soft_collect(item)
        if keys:
            from Items import ItemFactory
            for item in ItemFactory(['Small Key (Escape)', 'Big Key (Eastern Palace)', 'Big Key (Desert Palace)', 'Small Key (Desert Palace)', 'Big Key (Tower of Hera)', 'Small Key (Tower of Hera)', 'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)',
                                     'Big Key (Palace of Darkness)'] + ['Small Key (Palace of Darkness)'] * 6 + ['Big Key (Thieves Town)', 'Small Key (Thieves Town)', 'Big Key (Skull Woods)'] + ['Small Key (Skull Woods)'] * 3 + ['Big Key (Swamp Palace)',
                                     'Small Key (Swamp Palace)', 'Big Key (Ice Palace)'] + ['Small Key (Ice Palace)'] * 2 + ['Big Key (Misery Mire)', 'Big Key (Turtle Rock)', 'Big Key (Ganons Tower)'] + ['Small Key (Misery Mire)'] * 3 + ['Small Key (Turtle Rock)'] * 4 + ['Small Key (Ganons Tower)'] * 4):
                soft_collect(item)
        ret.sweep_for_events()
        ret.clear_cached_unreachable()
        return ret

    def get_items(self):
        return [loc.item for loc in self.get_filled_locations()] + self.itempool

    def find_items(self, item):
        return [location for location in self.get_locations() if location.item is not None and location.item.name == item]

    def push_item(self, location, item, collect=True):
        if not isinstance(location, Location):
            location = self.get_location(location)

        if location.can_fill(self.state, item, False):
            location.item = item
            item.location = location
            if collect:
                self.state.collect(item, location.event, location)

            logging.getLogger('').debug('Placed %s at %s', item, location)
        else:
            raise RuntimeError('Cannot assign item %s to location %s.' % (item, location))

    def get_locations(self):
        if self._cached_locations is None:
            self._cached_locations = []
            for region in self.regions:
                self._cached_locations.extend(region.locations)
        return self._cached_locations

    def get_unfilled_locations(self):
        return [location for location in self.get_locations() if location.item is None]

    def get_filled_locations(self):
        return [location for location in self.get_locations() if location.item is not None]

    def get_reachable_locations(self, state=None):
        if state is None:
            state = self.state
        return [location for location in self.get_locations() if state.can_reach(location)]

    def get_placeable_locations(self, state=None):
        if state is None:
            state = self.state
        return [location for location in self.get_locations() if location.item is None and state.can_reach(location)]

    def unlocks_new_location(self, item):
        temp_state = self.state.copy()
        temp_state.clear_cached_unreachable()
        temp_state.collect(item, True)

        for location in self.get_unfilled_locations():
            if temp_state.can_reach(location) and not self.state.can_reach(location):
                return True

        return False

    def has_beaten_game(self, state):
        if state.has('Triforce'):
            return True
        if self.goal in ['triforcehunt']:
            if state.item_count('Triforce Piece') + state.item_count('Power Star') > self.treasure_hunt_count:
                return True
        return False

    def can_beat_game(self, starting_state=None):
        if starting_state:
            state = starting_state.copy()
        else:
            state = CollectionState(self)

        if self.has_beaten_game(state):
            return True

        prog_locations = [location for location in self.get_locations() if location.item is not None and (location.item.advancement or location.event) and location not in state.locations_checked]

        treasure_pieces_collected = state.item_count('Triforce Piece') + state.item_count('Power Star')
        while prog_locations:
            sphere = []
            # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres
            for location in prog_locations:
                if state.can_reach(location):
                    if location.item.name == 'Triforce':
                        return True
                    elif location.item.name in ['Triforce Piece', 'Power Star']:
                        treasure_pieces_collected += 1
                    if self.goal in ['triforcehunt'] and treasure_pieces_collected >= self.treasure_hunt_count:
                        return True
                    sphere.append(location)

            if not sphere:
                # ran out of places and did not find triforce yet, quit
                return False

            for location in sphere:
                prog_locations.remove(location)
                state.collect(location.item, True, location)

        return False

    @property
    def option_identifier(self):
        id_value = 0
        id_value_max = 1

        def markbool(value):
            nonlocal id_value, id_value_max
            id_value += id_value_max * bool(value)
            id_value_max *= 2
        def marksequence(options, value):
            nonlocal id_value, id_value_max
            id_value += id_value_max * options.index(value)
            id_value_max *= len(options)
        markbool(self.logic == 'noglitches')
        marksequence(['standard', 'open', 'swordless'], self.mode)
        markbool(self.place_dungeon_items)
        marksequence(['ganon', 'pedestal', 'dungeons', 'triforcehunt', 'crystals'], self.goal)
        marksequence(['vanilla', 'simple', 'restricted', 'full', 'crossed', 'insanity', 'restricted_legacy', 'full_legacy', 'madness_legacy', 'insanity_legacy', 'dungeonsfull', 'dungeonssimple'], self.shuffle)
        marksequence(['easy', 'normal', 'hard', 'expert', 'insane'], self.difficulty)
        marksequence(['none', 'display', 'timed', 'timed-ohko', 'timed-countdown', 'ohko'], self.timer)
        marksequence(['on', 'off', 'random'], self.progressive)
        marksequence(['freshness', 'flood', 'vt21', 'vt22', 'vt25', 'vt26', 'balanced'], self.algorithm)
        markbool(self.check_beatable_only)
        markbool(self.shuffle_ganon)
        markbool(self.keysanity)
        assert id_value_max <= 0xFFFFFFFF
        return id_value


class CollectionState(object):

    def __init__(self, parent):
        self.prog_items = []
        self.world = parent
        self.region_cache = {}
        self.location_cache = {}
        self.entrance_cache = {}
        self.recursion_count = 0
        self.events = []
        self.path = {}
        self.locations_checked = set()


    def clear_cached_unreachable(self):
        # we only need to invalidate results which were False, places we could reach before we can still reach after adding more items
        self.region_cache = {k: v for k, v in self.region_cache.items() if v}
        self.location_cache = {k: v for k, v in self.location_cache.items() if v}
        self.entrance_cache = {k: v for k, v in self.entrance_cache.items() if v}

    def copy(self):
        ret = CollectionState(self.world)
        ret.prog_items = copy.copy(self.prog_items)
        ret.region_cache = copy.copy(self.region_cache)
        ret.location_cache = copy.copy(self.location_cache)
        ret.entrance_cache = copy.copy(self.entrance_cache)
        ret.events = copy.copy(self.events)
        ret.path = copy.copy(self.path)
        ret.locations_checked = copy.copy(self.locations_checked)
        return ret

    def can_reach(self, spot, resolution_hint=None):
        try:
            spot_type = spot.spot_type
            if spot_type == 'Location':
                correct_cache = self.location_cache
            elif spot_type == 'Region':
                correct_cache = self.region_cache
            elif spot_type == 'Entrance':
                correct_cache = self.entrance_cache
            else:
                raise AttributeError
        except AttributeError:
            # try to resolve a name
            if resolution_hint == 'Location':
                spot = self.world.get_location(spot)
                correct_cache = self.location_cache
            elif resolution_hint == 'Entrance':
                spot = self.world.get_entrance(spot)
                correct_cache = self.entrance_cache
            else:
                # default to Region
                spot = self.world.get_region(spot)
                correct_cache = self.region_cache

        if spot.recursion_count > 0:
            return False

        if spot not in correct_cache:
            # for the purpose of evaluating results, recursion is resolved by always denying recursive access (as that ia what we are trying to figure out right now in the first place
            spot.recursion_count += 1
            self.recursion_count += 1
            can_reach = spot.can_reach(self)
            spot.recursion_count -= 1
            self.recursion_count -= 1

            # we only store qualified false results (i.e. ones not inside a hypothetical)
            if not can_reach:
                if self.recursion_count == 0:
                    correct_cache[spot] = can_reach
            else:
                correct_cache[spot] = can_reach
            return can_reach
        return correct_cache[spot]

    def sweep_for_events(self, key_only=False):
        # this may need improvement
        new_locations = True
        checked_locations = 0
        while new_locations:
            reachable_events = [location for location in self.world.get_filled_locations() if location.event and (not key_only or location.item.key) and self.can_reach(location)]
            for event in reachable_events:
                if event.name not in self.events:
                    self.events.append(event.name)
                    self.collect(event.item, True, event)
            new_locations = len(reachable_events) > checked_locations
            checked_locations = len(reachable_events)

    def has(self, item, count=1):
        if count == 1:
            return item in self.prog_items
        return self.item_count(item) >= count

    def item_count(self, item):
        return len([pritem for pritem in self.prog_items if pritem == item])

    def can_lift_rocks(self):
        return self.has('Power Glove') or self.has('Titans Mitts')

    def has_bottle(self):
        return self.bottle_count() > 0

    def bottle_count(self):
        return len([pritem for pritem in self.prog_items if pritem.startswith('Bottle')])

    def has_hearts(self, count):
        # Warning: This oncly considers items that are marked as advancement items
        return self.heart_count() >= count

    def heart_count(self):
        # Warning: This oncly considers items that are marked as advancement items
        return (
            self.item_count('Boss Heart Container')
            + self.item_count('Sanctuary Heart Container')
            + self.item_count('Piece of Heart') // 4
            + 3 # starting hearts
        )

    def can_lift_heavy_rocks(self):
        return self.has('Titans Mitts')

    def can_extend_magic(self, smallmagic=8, fullrefill=False): #This reflects the total magic Link has, not the total extra he has.
        basemagic = 8
        if self.has('Quarter Magic'):
            basemagic = 32
        elif self.has('Half Magic'):
            basemagic = 16
        if self.world.difficulty == 'hard' and not fullrefill:
            basemagic = basemagic + int(basemagic * 0.5 * self.bottle_count())
        elif self.world.difficulty == 'expert' and not fullrefill:
            basemagic = basemagic + int(basemagic * 0.25 * self.bottle_count())
        elif self.world.difficulty == 'insane' and not fullrefill:
            basemagic = basemagic
        else:
            basemagic = basemagic + basemagic * self.bottle_count()
        return basemagic >= smallmagic # FIXME bottle should really also have a requirement that we can reach some shop that sells green or blue potions

    def can_kill_most_things(self, enemies=5):
        return (self.has_blunt_weapon()
                or self.has('Cane of Somaria')
                or (self.has('Cane of Byrna') and (enemies < 6 or self.can_extend_Magic()))
                or self.has('Bow')
                or self.has('Fire Rod')
               )

    def has_sword(self):
        return self.has('Fighter Sword') or self.has('Master Sword') or self.has('Tempered Sword') or self.has('Golden Sword')

    def has_beam_sword(self):
        return self.has('Master Sword') or self.has('Tempered Sword') or self.has('Golden Sword')

    def has_blunt_weapon(self):
        return self.has_sword() or self.has('Hammer')

    def has_Mirror(self):
        return self.has('Magic Mirror')

    def has_Boots(self):
        return self.has('Pegasus Boots')

    def has_Pearl(self):
        return self.has('Moon Pearl')

    def has_fire_source(self):
        return self.has('Fire Rod') or self.has('Lamp')

    def has_misery_mire_medallion(self):
        return self.has(self.world.required_medallions[0])

    def has_turtle_rock_medallion(self):
        return self.has(self.world.required_medallions[1])

    def collect(self, item, event=False, location=None):
        if location:
            self.locations_checked.add(location)
        changed = False
        if item.name.startswith('Progressive '):
            if 'Sword' in item.name:
                if self.has('Golden Sword'):
                    pass
                elif self.has('Tempered Sword') and self.world.difficulty_requirements.progressive_sword_limit >= 4:
                    self.prog_items.append('Golden Sword')
                    changed = True
                elif self.has('Master Sword') and self.world.difficulty_requirements.progressive_sword_limit >= 3:
                    self.prog_items.append('Tempered Sword')
                    changed = True
                elif self.has('Fighter Sword') and self.world.difficulty_requirements.progressive_sword_limit >= 2:
                    self.prog_items.append('Master Sword')
                    changed = True
                elif self.world.difficulty_requirements.progressive_sword_limit >= 1:
                    self.prog_items.append('Fighter Sword')
                    changed = True
            elif 'Glove' in item.name:
                if self.has('Titans Mitts'):
                    pass
                elif self.has('Power Glove'):
                    self.prog_items.append('Titans Mitts')
                    changed = True
                else:
                    self.prog_items.append('Power Glove')
                    changed = True
            elif 'Shield' in item.name:
                if self.has('Mirror Shield'):
                    pass
                elif self.has('Red Shield') and self.world.difficulty_requirements.progressive_shield_limit >= 3:
                    self.prog_items.append('Mirror Shield')
                    changed = True
                elif self.has('Blue Shield')  and self.world.difficulty_requirements.progressive_shield_limit >= 2:
                    self.prog_items.append('Red Shield')
                    changed = True
                elif self.world.difficulty_requirements.progressive_shield_limit >= 1:
                    self.prog_items.append('Blue Shield')
                    changed = True
        elif item.name.startswith('Bottle'):
            if self.bottle_count() < self.world.difficulty_requirements.progressive_bottle_limit:
                self.prog_items.append(item.name)
                changed = True
        elif event or item.advancement:
            self.prog_items.append(item.name)
            changed = True

        if changed:
            self.clear_cached_unreachable()
            if not event:
                self.sweep_for_events()
                self.clear_cached_unreachable()

    def remove(self, item):
        if item.advancement:
            to_remove = item.name
            if to_remove.startswith('Progressive '):
                if 'Sword' in to_remove:
                    if self.has('Golden Sword'):
                        to_remove = 'Golden Sword'
                    elif self.has('Tempered Sword'):
                        to_remove = 'Tempered Sword'
                    elif self.has('Master Sword'):
                        to_remove = 'Master Sword'
                    elif self.has('Fighter Sword'):
                        to_remove = 'Fighter Sword'
                    else:
                        to_remove = None
                elif 'Glove' in item.name:
                    if self.has('Titans Mitts'):
                        to_remove = 'Titans Mitts'
                    elif self.has('Power Glove'):
                        to_remove = 'Power Glove'
                    else:
                        to_remove = None

            if to_remove is not None:
                try:
                    self.prog_items.remove(to_remove)
                except ValueError:
                    return

                # invalidate caches, nothing can be trusted anymore now
                self.region_cache = {}
                self.location_cache = {}
                self.entrance_cache = {}
                self.recursion_count = 0

    def __getattr__(self, item):
        if item.startswith('can_reach_'):
            return self.can_reach(item[10])
        elif item.startswith('has_'):
            return self.has(item[4])

        raise RuntimeError('Cannot parse %s.' % item)

@unique
class RegionType(Enum):
    LightWorld = 1
    DarkWorld = 2
    Cave = 3 # Also includes Houses
    Dungeon = 4

    @property
    def is_indoors(self):
        """Shorthand for checking if Cave or Dungeon"""
        return self in (RegionType.Cave, RegionType.Dungeon)



class Region(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.entrances = []
        self.exits = []
        self.locations = []
        self.dungeon = None
        self.world = None
        self.is_light_world = False # will be set aftermaking connections.
        self.is_dark_world = False
        self.spot_type = 'Region'
        self.hint_text = 'Hyrule'
        self.recursion_count = 0

    def can_reach(self, state):
        for entrance in self.entrances:
            if state.can_reach(entrance):
                if not self in state.path:
                    state.path[self] = (self.name, state.path.get(entrance, None))
                return True
        return False

    def can_fill(self, item):
        is_dungeon_item = item.key or item.map or item.compass
        sewer_hack = self.world.mode == 'standard' and item.name == 'Small Key (Escape)'
        if sewer_hack or (is_dungeon_item and not self.world.keysanity):
            return self.dungeon and self.dungeon.is_dungeon_item(item)

        return True

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Entrance(object):

    def __init__(self, name='', parent=None):
        self.name = name
        self.parent_region = parent
        self.connected_region = None
        self.target = None
        self.addresses = None
        self.spot_type = 'Entrance'
        self.recursion_count = 0
        self.vanilla = None
        self.access_rule = lambda state: True

    def can_reach(self, state):
        if self.access_rule(state) and state.can_reach(self.parent_region):
            if not self in state.path:
                state.path[self] = (self.name, state.path.get(self.parent_region, (self.parent_region.name, None)))
            return True

        return False

    def connect(self, region, addresses=None, target=None, vanilla=None):
        self.connected_region = region
        self.target = target
        self.addresses = addresses
        self.vanilla = vanilla
        region.entrances.append(self)

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Dungeon(object):

    def __init__(self, name, regions, big_key, small_keys, dungeon_items):
        self.name = name
        self.regions = regions
        self.big_key = big_key
        self.small_keys = small_keys
        self.dungeon_items = dungeon_items

    @property
    def keys(self):
        return self.small_keys + ([self.big_key] if self.big_key else [])

    @property
    def all_items(self):
        return self.dungeon_items + self.keys

    def is_dungeon_item(self, item):
        return item.name in [dungeon_item.name for dungeon_item in self.all_items]

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Location(object):

    def __init__(self, name='', address=None, crystal=False, hint_text=None, parent=None):
        self.name = name
        self.parent_region = parent
        self.item = None
        self.crystal = crystal
        self.address = address
        self.spot_type = 'Location'
        self.hint_text = hint_text if hint_text is not None else 'Hyrule'
        self.recursion_count = 0
        self.staleness_count = 0
        self.event = False
        self.always_allow = lambda item, state: False
        self.access_rule = lambda state: True
        self.item_rule = lambda item: True

    def can_fill(self, state, item, check_access=True):
        return self.always_allow(item, self) or (self.parent_region.can_fill(item) and self.item_rule(item) and (not check_access or self.can_reach(state)))

    def can_reach(self, state):
        if self.access_rule(state) and state.can_reach(self.parent_region):
            return True
        return False

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Item(object):

    def __init__(self, name='', advancement=False, priority=False, type=None, code=None, pedestal_hint=None, pedestal_credit=None, sickkid_credit=None, zora_credit=None, witch_credit=None, fluteboy_credit=None):
        self.name = name
        self.advancement = advancement
        self.priority = priority
        self.type = type
        self.pedestal_hint_text = pedestal_hint
        self.pedestal_credit_text = pedestal_credit
        self.sickkid_credit_text = sickkid_credit
        self.zora_credit_text = zora_credit
        self.magicshop_credit_text = witch_credit
        self.fluteboy_credit_text = fluteboy_credit
        self.code = code
        self.location = None

    @property
    def key(self):
        return self.type == 'SmallKey' or self.type == 'BigKey'

    @property
    def crystal(self):
        return self.type == 'Crystal'

    @property
    def map(self):
        return self.type == 'Map'

    @property
    def compass(self):
        return self.type == 'Compass'

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


# have 6 address that need to be filled
class Crystal(Item):
    pass


class Spoiler(object):

    def __init__(self, world):
        self.world = world
        self.entrances = []
        self.medallions = {}
        self.playthrough = {}
        self.locations = {}
        self.paths = {}
        self.metadata = {}

    def set_entrance(self, entrance, exit, direction):
        self.entrances.append(OrderedDict([('entrance', entrance), ('exit', exit), ('direction', direction)]))

    def parse_data(self):
        self.medallions = OrderedDict([('Misery Mire', self.world.required_medallions[0]), ('Turtle Rock', self.world.required_medallions[1])])
        self.locations = {'other locations': OrderedDict([(str(location), str(location.item) if location.item is not None else 'Nothing') for location in self.world.get_locations()])}
        from Main import __version__ as ERVersion
        self.metadata = {'version': ERVersion,
                         'seed': self.world.seed,
                         'logic': self.world.logic,
                         'mode': self.world.mode,
                         'goal': self.world.goal,
                         'shuffle': self.world.shuffle,
                         'algorithm': self.world.algorithm,
                         'difficulty': self.world.difficulty,
                         'timer': self.world.timer,
                         'progressive': self.world.progressive,
                         'completeable': not self.world.check_beatable_only,
                         'dungeonitems': self.world.place_dungeon_items,
                         'quickswap': self.world.quickswap,
                         'fastmenu': self.world.fastmenu,
                         'disable_music': self.world.disable_music,
                         'keysanity': self.world.keysanity}

    def to_json(self):
        self.parse_data()
        out = OrderedDict()
        out['entrances'] = self.entrances
        out.update(self.locations)
        out['medallions'] = self.medallions
        out['playthrough'] = self.playthrough
        out['paths'] = self.paths
        out['meta'] = self.metadata
        return json.dumps(out)

    def to_file(self, filename):
        self.parse_data()
        with open(filename, 'w') as outfile:
            outfile.write('ALttP Entrance Randomizer Version %s  -  Seed: %s\n\n' % (self.metadata['version'], self.metadata['seed']))
            outfile.write('Logic:                           %s\n' % self.metadata['logic'])
            outfile.write('Mode:                            %s\n' % self.metadata['mode'])
            outfile.write('Goal:                            %s\n' % self.metadata['goal'])
            outfile.write('Entrance Shuffle:                %s\n' % self.metadata['shuffle'])
            outfile.write('Filling Algorithm:               %s\n' % self.metadata['algorithm'])
            outfile.write('All Locations Accessible:        %s\n' % ('Yes' if self.metadata['completeable'] else 'No, some locations may be unreachable'))
            outfile.write('Maps and Compasses in Dungeons:  %s\n' % ('Yes' if self.metadata['dungeonitems'] else 'No'))
            outfile.write('L\\R Quickswap enabled:           %s\n' % ('Yes' if self.metadata['quickswap'] else 'No'))
            outfile.write('Menu speed:                      %s\n' % self.metadata['fastmenu'])
            outfile.write('Keysanity enabled:               %s' % ('Yes' if self.metadata['keysanity'] else 'No'))
            if self.entrances:
                outfile.write('\n\nEntrances:\n\n')
                outfile.write('\n'.join(['%s %s %s' % (entry['entrance'], '<=>' if entry['direction'] == 'both' else '<=' if entry['direction'] == 'exit' else '=>', entry['exit']) for entry in self.entrances]))
            outfile.write('\n\nMedallions')
            outfile.write('\n\nMisery Mire Medallion: %s' % self.medallions['Misery Mire'])
            outfile.write('\nTurtle Rock Medallion: %s' % self.medallions['Turtle Rock'])
            outfile.write('\n\nLocations:\n\n')
            outfile.write('\n'.join(['%s: %s' % (location, item) for (location, item) in self.locations['other locations'].items()]))
            outfile.write('\n\nPlaythrough:\n\n')
            outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(['  %s: %s' % (location, item) for (location, item) in sphere.items()])) for (sphere_nr, sphere) in self.playthrough.items()]))
            outfile.write('\n\nPaths:\n\n')

            path_listings = []
            for location, path in sorted(self.paths.items()):
                path_lines = []
                for region, exit in path:
                    if exit is not None:
                        path_lines.append("{} -> {}".format(region, exit))
                    else:
                        path_lines.append(region)
                path_listings.append("{}\n        {}".format(location, "\n   =>   ".join(path_lines)))

            outfile.write('\n'.join(path_listings))
