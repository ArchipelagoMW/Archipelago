import copy
import logging


class World(object):

    def __init__(self, shuffle, logic, mode, difficulty, goal, place_dungeon_items):
        self.shuffle = shuffle
        self.logic = logic
        self.mode = mode
        self.difficulty = difficulty
        self.goal = goal
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
        self._item_cache = {}
        self.spoiler = ''
        self.place_dungeon_items = place_dungeon_items  # configurable in future
        self.agahnim_fix_required = False
        self.swamp_patch_required = False
        self.sewer_light_cone = mode == 'standard'
        self.light_world_light_cone = False
        self.dark_world_light_cone = False
        self.treasure_hunt_count = 0
        self.treasure_hunt_icon = 'Power Star'
        self.clock_mode = 'off'
        self.aga_randomness = 'off'
        self.lock_aga_door_in_escape = False

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

    def find_items(self, item):
        return [location for location in self.get_locations() if location.item is not None and location.item.name == item]

    def push_item(self, location, item, collect=True):
        if not isinstance(location, Location):
            location = self.get_location(location)

        if location.item_rule(item):
            location.item = item
            item.location = location
            if collect:
                self.state.collect(item)

            logging.getLogger('').debug('Placed %s at %s' % (item, location))
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
        temp_state._clear_cache()
        temp_state.collect(item)

        for location in self.get_unfilled_locations():
            if temp_state.can_reach(location) and not self.state.can_reach(location):
                return True

        return False

    def can_beat_game(self):
        prog_locations = [location for location in self.get_locations() if location.item is not None and location.item.advancement]

        state = CollectionState(self)
        while prog_locations:
            sphere = []
            # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres
            for location in prog_locations:
                if state.can_reach(location):
                    if location.item.name == 'Triforce':
                        return True
                    sphere.append(location)

            if not sphere:
                # ran out of places and did not find triforce yet, quit
                return False

            for location in sphere:
                prog_locations.remove(location)
                state.collect(location.item)

        return False

    @property
    def option_identifier(self):
        logic = 0 if self.logic == 'noglitches' else 1
        mode = 0 if self.mode == 'open' else 1
        goal = 0 if self.goal == 'ganon' else 1 if self.goal == 'pedestal' else 2
        shuffle = ['vanilla', 'simple', 'restricted', 'full', 'madness', 'insanity', 'dungeonsfull', 'dungeonssimple'].index(self.shuffle)
        dungeonitems = 0 if self.place_dungeon_items else 1
        return logic | (mode << 1) | (goal << 2) | (shuffle << 4) | (dungeonitems << 8)


class CollectionState(object):

    def __init__(self, parent, has_everything=False):
        self.prog_items = []
        self.world = parent
        self.has_everything = has_everything
        self.region_cache = {}
        self.location_cache = {}
        self.entrance_cache = {}
        self.recursion_count = 0

    def _clear_cache(self):
        # we only need to invalidate results which were False, places we could reach before we can still reach after adding more items
        self.region_cache = {k: v for k, v in self.region_cache.items() if v}
        self.location_cache = {k: v for k, v in self.location_cache.items() if v}
        self.entrance_cache = {k: v for k, v in self.entrance_cache.items() if v}

    def copy(self):
        ret = CollectionState(self.world, self.has_everything)
        ret.prog_items = copy.copy(self.prog_items)
        ret.region_cache = copy.copy(self.region_cache)
        ret.location_cache = copy.copy(self.location_cache)
        ret.entrance_cache = copy.copy(self.entrance_cache)
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

    def can_collect(self, item, count=None):
        if isinstance(item, Item):
            item = item.name
        if count is None:
            cached = self.world._item_cache.get(item, None)
            if cached is None:
                candidates = self.world.find_items(item)
                if not candidates:
                    return False
                elif len(candidates) == 1:
                    cached = candidates[0]
                    self.world._item_cache[item] = cached
                else:
                    # this should probably not happen, wonky item distribution?
                    return self._can_reach_n(self.world.find_items(item), 1)
            return self.can_reach(cached)

        return self._can_reach_n(self.world.find_items(item), count)

    def _can_reach_n(self, candidates, count):
        maxfail = len(candidates) - count
        fail = 0
        success = 0
        for candidate in candidates:
            if self.can_reach(candidate):
                success += 1
            else:
                fail += 1
            if fail > maxfail:
                return False
            if success >= count:
                return True
        return False

    def has(self, item):
        if self.has_everything:
            return True
        else:
            return item in self.prog_items

    def can_lift_rocks(self):
        return self.has('Power Glove') or self.has('Titans Mitts')

    def can_lift_heavy_rocks(self):
        return self.has('Titans Mitts')

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

    def collect(self, item):
        changed = False
        if item.name.startswith('Progressive '):
            if 'Sword' in item.name:
                if self.has('Golden Sword'):
                    pass
                elif self.has('Tempered Sword'):
                    self.prog_items.append('Golden Sword')
                    changed = True
                elif self.has('Master Sword'):
                    self.prog_items.append('Tempered Sword')
                    changed = True
                elif self.has('Fighter Sword'):
                    self.prog_items.append('Master Sword')
                    changed = True
                else:
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

        elif item.advancement:
            self.prog_items.append(item.name)
            changed = True

        if changed:
            self._clear_cache()

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
                except IndexError:
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


class Region(object):

    def __init__(self, name):
        self.name = name
        self.entrances = []
        self.exits = []
        self.locations = []
        self.spot_type = 'Region'
        self.hint_text = 'Hyrule'
        self.recursion_count = 0

    def can_reach(self, state):
        for entrance in self.entrances:
            if state.can_reach(entrance):
                return True
        return False

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

    def access_rule(self, state):
        return True

    def can_reach(self, state):
        if self.access_rule(state) and state.can_reach(self.parent_region):
            return True

        return False

    def connect(self, region, addresses=None, target=None):
        self.connected_region = region
        self.target = target
        self.addresses = addresses
        region.entrances.append(self)

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

    def access_rule(self, state):
        return True

    def item_rule(self, item):
        return True

    def can_reach(self, state):
        if self.access_rule(state) and state.can_reach(self.parent_region):
            return True
        return False

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


class Item(object):    

    def __init__(self, name='', advancement=False, priority=False, key=False, crystal=False, code=None, altar_hint=None, altar_credit=None, sickkid_credit=None, zora_credit=None, witch_credit=None, fluteboy_credit=None):
        self.name = name
        self.advancement = advancement
        self.priority = priority
        self.key = key
        self.crystal = crystal
        self.altar_hint_text = altar_hint
        self.altar_credit_text = altar_credit
        self.sickkid_credit_text = sickkid_credit
        self.zora_credit_text = zora_credit
        self.magicshop_credit_text = witch_credit
        self.fluteboy_credit_text = fluteboy_credit
        self.code = code
        self.location = None

    def __str__(self):
        return str(self.__unicode__())

    def __unicode__(self):
        return '%s' % self.name


# have 6 address that need to be filled
class Crystal(Item):
    pass
