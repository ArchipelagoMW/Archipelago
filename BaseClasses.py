from __future__ import annotations

import copy
from enum import Enum, unique
import logging
import json
from collections import OrderedDict, Counter, deque
from typing import Union, Optional, List, Dict, NamedTuple, Iterable
import secrets
import random

from EntranceShuffle import indirect_connections
from Items import item_name_groups


class World(object):
    debug_types = False
    player_names: Dict[int, List[str]]
    _region_cache: dict
    difficulty_requirements: dict
    required_medallions: dict
    dark_room_logic: Dict[int, str]
    restrict_dungeon_item_on_boss: Dict[int, bool]
    plando_texts: List[Dict[str, str]]
    plando_items: List[PlandoItem]
    plando_connections: List[PlandoConnection]

    def __init__(self, players: int, shuffle, logic, mode, swords, difficulty, difficulty_adjustments, timer,
                 progressive,
                 goal, algorithm, accessibility, shuffle_ganon, retro, custom, customitemarray, hints):
        if self.debug_types:
            import inspect
            methods = inspect.getmembers(self, predicate=inspect.ismethod)

            for name, method in methods:
                if name.startswith("_debug_"):
                    setattr(self, name[7:], method)
                    logging.debug(f"Set {self}.{name[7:]} to {method}")
            self.get_location = self._debug_get_location
        self.random = random.Random()  # world-local random state is saved in case of future use a
        # persistently running program with multiple worlds rolling concurrently
        self.players = players
        self.teams = 1
        self.shuffle = shuffle.copy()
        self.logic = logic.copy()
        self.mode = mode.copy()
        self.swords = swords.copy()
        self.difficulty = difficulty.copy()
        self.difficulty_adjustments = difficulty_adjustments.copy()
        self.timer = timer.copy()
        self.progressive = progressive
        self.goal = goal.copy()
        self.algorithm = algorithm
        self.dungeons = []
        self.regions = []
        self.shops = []
        self.itempool = []
        self.seed = None
        self.precollected_items = []
        self.state = CollectionState(self)
        self._cached_entrances = None
        self._cached_locations = None
        self._entrance_cache = {}
        self._location_cache = {}
        self.required_locations = []
        self.light_world_light_cone = False
        self.dark_world_light_cone = False
        self.rupoor_cost = 10
        self.aga_randomness = True
        self.lock_aga_door_in_escape = False
        self.save_and_quit_from_boss = True
        self.accessibility = accessibility.copy()
        self.shuffle_ganon = shuffle_ganon
        self.fix_gtower_exit = self.shuffle_ganon
        self.retro = retro.copy()
        self.custom = custom
        self.customitemarray: List[int] = customitemarray
        self.hints = hints.copy()
        self.dynamic_regions = []
        self.dynamic_locations = []
        self.spoiler = Spoiler(self)

        for player in range(1, players + 1):
            def set_player_attr(attr, val):
                self.__dict__.setdefault(attr, {})[player] = val
            set_player_attr('_region_cache', {})
            set_player_attr('player_names', [])
            set_player_attr('remote_items', False)
            set_player_attr('required_medallions', ['Ether', 'Quake'])
            set_player_attr('swamp_patch_required', False)
            set_player_attr('powder_patch_required', False)
            set_player_attr('ganon_at_pyramid', True)
            set_player_attr('ganonstower_vanilla', True)
            set_player_attr('sewer_light_cone', self.mode[player] == 'standard')
            set_player_attr('fix_trock_doors', self.shuffle[player] != 'vanilla' or self.mode[player] == 'inverted')
            set_player_attr('fix_skullwoods_exit', self.shuffle[player] not in ['vanilla', 'simple', 'restricted', 'dungeonssimple'])
            set_player_attr('fix_palaceofdarkness_exit', self.shuffle[player] not in ['vanilla', 'simple', 'restricted', 'dungeonssimple'])
            set_player_attr('fix_trock_exit', self.shuffle[player] not in ['vanilla', 'simple', 'restricted', 'dungeonssimple'])
            set_player_attr('can_access_trock_eyebridge', None)
            set_player_attr('can_access_trock_front', None)
            set_player_attr('can_access_trock_big_chest', None)
            set_player_attr('can_access_trock_middle', None)
            set_player_attr('fix_fake_world', True)
            set_player_attr('mapshuffle', False)
            set_player_attr('compassshuffle', False)
            set_player_attr('keyshuffle', False)
            set_player_attr('bigkeyshuffle', False)
            set_player_attr('difficulty_requirements', None)
            set_player_attr('boss_shuffle', 'none')
            set_player_attr('enemy_shuffle', False)
            set_player_attr('enemy_health', 'default')
            set_player_attr('enemy_damage', 'default')
            set_player_attr('killable_thieves', False)
            set_player_attr('tile_shuffle', False)
            set_player_attr('bush_shuffle', False)
            set_player_attr('beemizer', 0)
            set_player_attr('escape_assist', [])
            set_player_attr('crystals_needed_for_ganon', 7)
            set_player_attr('crystals_needed_for_gt', 7)
            set_player_attr('open_pyramid', False)
            set_player_attr('treasure_hunt_icon', 'Triforce Piece')
            set_player_attr('treasure_hunt_count', 0)
            set_player_attr('clock_mode', False)
            set_player_attr('countdown_start_time', 10)
            set_player_attr('red_clock_time', -2)
            set_player_attr('blue_clock_time', 2)
            set_player_attr('green_clock_time', 4)
            set_player_attr('can_take_damage', True)
            set_player_attr('glitch_boots', True)
            set_player_attr('progression_balancing', True)
            set_player_attr('local_items', set())
            set_player_attr('non_local_items', set())
            set_player_attr('triforce_pieces_available', 30)
            set_player_attr('triforce_pieces_required', 20)
            set_player_attr('shop_shuffle', 'off')
            set_player_attr('shop_shuffle_slots', 0)
            set_player_attr('shuffle_prizes', "g")
            set_player_attr('sprite_pool', [])
            set_player_attr('dark_room_logic', "lamp")
            set_player_attr('restrict_dungeon_item_on_boss', False)
            set_player_attr('plando_items', [])
            set_player_attr('plando_texts', {})
            set_player_attr('plando_connections', [])

    def secure(self):
        self.random = secrets.SystemRandom()

    @property
    def player_ids(self):
        yield from range(1, self.players + 1)

    def get_name_string_for_object(self, obj) -> str:
        return obj.name if self.players == 1 else f'{obj.name} ({self.get_player_names(obj.player)})'

    def get_player_names(self, player: int) -> str:
        return ", ".join(self.player_names[player])

    def initialize_regions(self, regions=None):
        for region in regions if regions else self.regions:
            region.world = self
            self._region_cache[region.player][region.name] = region

    def _recache(self):
        """Rebuild world cache"""
        for region in self.regions:
            player = region.player
            self._region_cache[player][region.name] = region
            for exit in region.exits:
                self._entrance_cache[exit.name, player] = exit

            for r_location in region.locations:
                self._location_cache[r_location.name, player] = r_location

    def get_regions(self, player=None):
        return self.regions if player is None else self._region_cache[player].values()

    def get_region(self, regionname: str, player: int) -> Region:
        try:
            return self._region_cache[player][regionname]
        except KeyError:
            self._recache()
            return self._region_cache[player][regionname]

    def _debug_get_region(self, regionname: str, player: int) -> Region:
        if type(regionname) != str:
            raise TypeError(f"expected str, got {type(regionname)} instead")
        try:
            return self._region_cache[player][regionname]
        except KeyError:
            for region in self.regions:
                if region.name == regionname and region.player == player:
                    assert not region.world  # this should only happen before initialization
                    self._region_cache[player][regionname] = region
                    return region
            raise KeyError('No such region %s for player %d' % (regionname, player))

    def get_entrance(self, entrance: str, player: int) -> Entrance:
        try:
            return self._entrance_cache[entrance, player]
        except KeyError:
            self._recache()
            return self._entrance_cache[entrance, player]

    def _debug_get_entrance(self, entrance: str, player: int) -> Entrance:
        if type(entrance) != str:
            raise TypeError(f"expected str, got {type(entrance)} instead")
        try:
            return self._entrance_cache[(entrance, player)]
        except KeyError:
            for region in self.regions:
                for exit in region.exits:
                    if exit.name == entrance and exit.player == player:
                        self._entrance_cache[(entrance, player)] = exit
                        return exit

            raise KeyError('No such entrance %s for player %d' % (entrance, player))

    def get_location(self, location: str, player: int) -> Location:
        try:
            return self._location_cache[location, player]
        except KeyError:
            self._recache()
            return self._location_cache[location, player]

    def _debug_get_location(self, location: str, player: int) -> Location:
        if type(location) != str:
            raise TypeError(f"expected str, got {type(location)} instead")
        try:
            return self._location_cache[(location, player)]
        except KeyError:
            for region in self.regions:
                for r_location in region.locations:
                    if r_location.name == location and r_location.player == player:
                        self._location_cache[(location, player)] = r_location
                        return r_location

        raise KeyError('No such location %s for player %d' % (location, player))

    def get_dungeon(self, dungeonname: str, player: int) -> Dungeon:
        for dungeon in self.dungeons:
            if dungeon.name == dungeonname and dungeon.player == player:
                return dungeon
        raise KeyError('No such dungeon %s for player %d' % (dungeonname, player))

    def _debug_get_dungeon(self, dungeonname: str, player: int) -> Dungeon:
        if type(dungeonname) != str:
            raise TypeError(f"expected str, got {type(dungeonname)} instead")
        for dungeon in self.dungeons:
            if dungeon.name == dungeonname and dungeon.player == player:
                return dungeon
        raise KeyError('No such dungeon %s for player %d' % (dungeonname, player))

    def get_all_state(self, keys=False) -> CollectionState:
        ret = CollectionState(self)

        def soft_collect(item):
            if item.name.startswith('Progressive '):
                if 'Sword' in item.name:
                    if ret.has('Golden Sword', item.player):
                        pass
                    elif ret.has('Tempered Sword', item.player) and self.difficulty_requirements[
                        item.player].progressive_sword_limit >= 4:
                        ret.prog_items['Golden Sword', item.player] += 1
                    elif ret.has('Master Sword', item.player) and self.difficulty_requirements[
                        item.player].progressive_sword_limit >= 3:
                        ret.prog_items['Tempered Sword', item.player] += 1
                    elif ret.has('Fighter Sword', item.player) and self.difficulty_requirements[item.player].progressive_sword_limit >= 2:
                        ret.prog_items['Master Sword', item.player] += 1
                    elif self.difficulty_requirements[item.player].progressive_sword_limit >= 1:
                        ret.prog_items['Fighter Sword', item.player] += 1
                elif 'Glove' in item.name:
                    if ret.has('Titans Mitts', item.player):
                        pass
                    elif ret.has('Power Glove', item.player):
                        ret.prog_items['Titans Mitts', item.player] += 1
                    else:
                        ret.prog_items['Power Glove', item.player] += 1
                elif 'Shield' in item.name:
                    if ret.has('Mirror Shield', item.player):
                        pass
                    elif ret.has('Red Shield', item.player) and self.difficulty_requirements[item.player].progressive_shield_limit >= 3:
                        ret.prog_items['Mirror Shield', item.player] += 1
                    elif ret.has('Blue Shield', item.player)  and self.difficulty_requirements[item.player].progressive_shield_limit >= 2:
                        ret.prog_items['Red Shield', item.player] += 1
                    elif self.difficulty_requirements[item.player].progressive_shield_limit >= 1:
                        ret.prog_items['Blue Shield', item.player] += 1
                elif 'Bow' in item.name:
                    if ret.has('Silver', item.player):
                        pass
                    elif ret.has('Bow', item.player) and self.difficulty_requirements[item.player].progressive_bow_limit >= 2:
                        ret.prog_items['Silver Bow', item.player] += 1
                    elif self.difficulty_requirements[item.player].progressive_bow_limit >= 1:
                        ret.prog_items['Bow', item.player] += 1
            elif item.name.startswith('Bottle'):
                if ret.bottle_count(item.player) < self.difficulty_requirements[item.player].progressive_bottle_limit:
                    ret.prog_items[item.name, item.player] += 1
            elif item.advancement or item.smallkey or item.bigkey:
                ret.prog_items[item.name, item.player] += 1

        for item in self.itempool:
            soft_collect(item)

        if keys:
            for p in range(1, self.players + 1):
                from Items import ItemFactory
                for item in ItemFactory(
                        ['Small Key (Hyrule Castle)', 'Big Key (Eastern Palace)', 'Big Key (Desert Palace)',
                         'Small Key (Desert Palace)', 'Big Key (Tower of Hera)', 'Small Key (Tower of Hera)',
                         'Small Key (Agahnims Tower)', 'Small Key (Agahnims Tower)',
                         'Big Key (Palace of Darkness)'] + ['Small Key (Palace of Darkness)'] * 6 + [
                            'Big Key (Thieves Town)', 'Small Key (Thieves Town)', 'Big Key (Skull Woods)'] + [
                            'Small Key (Skull Woods)'] * 3 + ['Big Key (Swamp Palace)',
                                                              'Small Key (Swamp Palace)', 'Big Key (Ice Palace)'] + [
                            'Small Key (Ice Palace)'] * 2 + ['Big Key (Misery Mire)', 'Big Key (Turtle Rock)',
                                                             'Big Key (Ganons Tower)'] + [
                            'Small Key (Misery Mire)'] * 3 + ['Small Key (Turtle Rock)'] * 4 + [
                            'Small Key (Ganons Tower)'] * 4,
                        p):
                    soft_collect(item)
        ret.sweep_for_events()
        return ret

    def get_items(self) -> list:
        return [loc.item for loc in self.get_filled_locations()] + self.itempool

    def find_items(self, item, player: int) -> list:
        return [location for location in self.get_locations() if
                location.item is not None and location.item.name == item and location.item.player == player]

    def push_precollected(self, item: Item):
        item.world = self
        if (item.smallkey and self.keyshuffle[item.player]) or (item.bigkey and self.bigkeyshuffle[item.player]):
            item.advancement = True
        self.precollected_items.append(item)
        self.state.collect(item, True)

    def push_item(self, location: Location, item: Item, collect: bool = True):
        if not isinstance(location, Location):
            raise RuntimeError(
                'Cannot assign item %s to invalid location %s (player %d).' % (item, location, item.player))

        if location.can_fill(self.state, item, False):
            location.item = item
            item.location = location
            item.world = self
            if collect:
                self.state.collect(item, location.event, location)

            logging.debug('Placed %s at %s', item, location)
        else:
            raise RuntimeError('Cannot assign item %s to location %s.' % (item, location))

    def get_entrances(self) -> list:
        if self._cached_entrances is None:
            self._cached_entrances = [entrance for region in self.regions for entrance in region.entrances]
        return self._cached_entrances

    def clear_entrance_cache(self):
        self._cached_entrances = None

    def get_locations(self) -> list:
        if self._cached_locations is None:
            self._cached_locations = [location for region in self.regions for location in region.locations]
        return self._cached_locations

    def clear_location_cache(self):
        self._cached_locations = None

    def get_unfilled_locations(self, player=None) -> list:
        if player is not None:
            return [location for location in self.get_locations() if
                    location.player == player and not location.item]
        return [location for location in self.get_locations() if not location.item]

    def get_unfilled_dungeon_locations(self):
        return [location for location in self.get_locations() if not location.item and location.parent_region.dungeon]

    def get_filled_locations(self, player=None) -> list:
        if player is not None:
            return [location for location in self.get_locations() if
                    location.player == player and location.item is not None]
        return [location for location in self.get_locations() if location.item is not None]

    def get_reachable_locations(self, state=None, player=None) -> list:
        if state is None:
            state = self.state
        return [location for location in self.get_locations() if
                (player is None or location.player == player) and location.can_reach(state)]

    def get_placeable_locations(self, state=None, player=None) -> list:
        if state is None:
            state = self.state
        return [location for location in self.get_locations() if
                (player is None or location.player == player) and location.item is None and location.can_reach(state)]

    def get_unfilled_locations_for_players(self, location_name: str, players: Iterable[int]):
        for player in players:
            location = self.get_location(location_name, player)
            if location.item is None:
                yield location

    def unlocks_new_location(self, item) -> bool:
        temp_state = self.state.copy()
        temp_state.collect(item, True)

        for location in self.get_unfilled_locations():
            if temp_state.can_reach(location) and not self.state.can_reach(location):
                return True

        return False

    def has_beaten_game(self, state, player: Optional[int] = None):
        if player:
            return state.has('Triforce', player) or state.world.logic[player] == 'nologic'
        else:
            return all((self.has_beaten_game(state, p) for p in range(1, self.players + 1)))

    def can_beat_game(self, starting_state : Optional[CollectionState]=None):
        if starting_state:
            if self.has_beaten_game(starting_state):
                return True
            state = starting_state.copy()
        else:
            if self.has_beaten_game(self.state):
                return True
            state = CollectionState(self)
        prog_locations = {location for location in self.get_locations() if location.item is not None and (
                    location.item.advancement or location.event) and location not in state.locations_checked}

        while prog_locations:
            sphere = []
            # build up spheres of collection radius. Everything in each sphere is independent from each other in dependencies and only depends on lower spheres
            for location in prog_locations:
                if location.can_reach(state):
                    sphere.append(location)

            if not sphere:
                # ran out of places and did not finish yet, quit
                return False

            for location in sphere:
                prog_locations.remove(location)
                state.collect(location.item, True, location)

            if self.has_beaten_game(state):
                return True

        return False

    def get_spheres(self):
        state = CollectionState(self)

        locations = {location for location in self.get_locations()}

        while locations:
            sphere = set()

            for location in locations:
                if location.can_reach(state):
                    sphere.add(location)
            yield sphere
            if not sphere:
                if locations:
                    yield locations  # unreachable locations
                break

            for location in sphere:
                state.collect(location.item, True, location)
            locations -= sphere



    def fulfills_accessibility(self, state: Optional[CollectionState] = None):
        """Check if accessibility rules are fulfilled with current or supplied state."""
        if not state:
            state = CollectionState(self)
        players = {"none" : set(),
                   "items": set(),
                   "locations": set()}
        for player, access in self.accessibility.items():
            players[access].add(player)

        beatable_fulfilled = False

        def location_conditition(location : Location):
            """Determine if this location has to be accessible, location is already filtered by location_relevant"""
            if location.player in players["none"]:
                return False
            return True

        def location_relevant(location : Location):
            """Determine if this location is relevant to sweep."""
            if location.player in players["locations"] or location.event or \
                    (location.item and location.item.advancement):
                return True
            return False

        def all_done():
            """Check if all access rules are fulfilled"""
            if beatable_fulfilled:
                if any(location_conditition(location) for location in locations):
                    return False  # still locations required to be collected
                return True

        locations = {location for location in self.get_locations() if location_relevant(location)}

        while locations:
            sphere = set()
            for location in locations:
                if location.can_reach(state):
                    sphere.add(location)

            if not sphere:
                # ran out of places and did not finish yet, quit
                logging.debug(f"Could not access required locations.")
                return False

            for location in sphere:
                locations.remove(location)
                state.collect(location.item, True, location)

            if self.has_beaten_game(state):
                beatable_fulfilled = True

            if all_done():
                return True

        return False


class CollectionState(object):

    def __init__(self, parent: World):
        self.prog_items = Counter()
        self.world = parent
        self.reachable_regions = {player: set() for player in range(1, parent.players + 1)}
        self.blocked_connections = {player: set() for player in range(1, parent.players + 1)}
        self.events = set()
        self.path = {}
        self.locations_checked = set()
        self.stale = {player: True for player in range(1, parent.players + 1)}
        for item in parent.precollected_items:
            self.collect(item, True)

    def update_reachable_regions(self, player: int):
        self.stale[player] = False
        rrp = self.reachable_regions[player]
        bc = self.blocked_connections[player]
        queue = deque(self.blocked_connections[player])
        start = self.world.get_region('Menu', player)

        # init on first call - this can't be done on construction since the regions don't exist yet
        if not start in rrp:
            rrp.add(start)
            bc.update(start.exits)
            queue.extend(start.exits)

        # run BFS on all connections, and keep track of those blocked by missing items
        while queue:
            connection = queue.popleft()
            new_region = connection.connected_region
            if new_region in rrp:
                bc.remove(connection)
            elif connection.can_reach(self):
                rrp.add(new_region)
                bc.remove(connection)
                bc.update(new_region.exits)
                queue.extend(new_region.exits)
                self.path[new_region] = (new_region.name, self.path.get(connection, None))

                # Retry connections if the new region can unblock them
                if new_region.name in indirect_connections:
                    new_entrance = self.world.get_entrance(indirect_connections[new_region.name], player)
                    if new_entrance in bc and new_entrance not in queue:
                        queue.append(new_entrance)

    def copy(self) -> CollectionState:
        ret = CollectionState(self.world)
        ret.prog_items = self.prog_items.copy()
        ret.reachable_regions = {player: copy.copy(self.reachable_regions[player]) for player in
                                 range(1, self.world.players + 1)}
        ret.blocked_connections = {player: copy.copy(self.blocked_connections[player]) for player in range(1, self.world.players + 1)}
        ret.events = copy.copy(self.events)
        ret.path = copy.copy(self.path)
        ret.locations_checked = copy.copy(self.locations_checked)
        return ret

    def can_reach(self, spot, resolution_hint=None, player=None) -> bool:
        if not hasattr(spot, "spot_type"):
            # try to resolve a name
            if resolution_hint == 'Location':
                spot = self.world.get_location(spot, player)
            elif resolution_hint == 'Entrance':
                spot = self.world.get_entrance(spot, player)
            else:
                # default to Region
                spot = self.world.get_region(spot, player)
        return spot.can_reach(self)

    def sweep_for_events(self, key_only: bool = False, locations=None):
        if locations is None:
            locations = self.world.get_filled_locations()
        new_locations = True
        while new_locations:
            reachable_events = {location for location in locations if location.event and
                                (not key_only or (not self.world.keyshuffle[
                                    location.item.player] and location.item.smallkey) or (not self.world.bigkeyshuffle[
                                    location.item.player] and location.item.bigkey))
                                and location.can_reach(self)}
            new_locations = reachable_events - self.events
            for event in new_locations:
                self.events.add(event)
                self.collect(event.item, True, event)

    def has(self, item, player: int, count: int = 1):
        return self.prog_items[item, player] >= count

    def has_key(self, item, player, count: int = 1):
        if self.world.logic[player] == 'nologic':
            return True
        if self.world.keyshuffle[player] == "universal":
            return self.can_buy_unlimited('Small Key (Universal)', player)
        return self.prog_items[item, player] >= count

    def can_buy_unlimited(self, item: str, player: int) -> bool:
        return any(shop.region.player == player and shop.has_unlimited(item) and shop.region.can_reach(self) for
                   shop in self.world.shops)

    def can_buy(self, item: str, player: int) -> bool:
        return any(shop.region.player == player and shop.has(item) and shop.region.can_reach(self) for
                   shop in self.world.shops)

    def item_count(self, item, player: int) -> int:
        return self.prog_items[item, player]

    def has_triforce_pieces(self, count: int, player: int) -> bool:
        return self.item_count('Triforce Piece', player) + self.item_count('Power Star', player) >= count

    def has_crystals(self, count: int, player: int) -> bool:
        found: int = 0
        for crystalnumber in range(1, 8):
            found += self.prog_items[f"Crystal {crystalnumber}", player]
            if found >= count:
                return True
        return False

    def can_lift_rocks(self, player: int):
        return self.has('Power Glove', player) or self.has('Titans Mitts', player)

    def has_bottle(self, player: int) -> bool:
        return self.has_bottles(1, player)

    def bottle_count(self, player: int) -> int:
        found: int = 0
        for bottlename in item_name_groups["Bottles"]:
            found += self.prog_items[bottlename, player]
        return found

    def has_bottles(self, bottles: int, player: int) -> bool:
        """Version of bottle_count that allows fast abort"""
        found: int = 0
        for bottlename in item_name_groups["Bottles"]:
            found += self.prog_items[bottlename, player]
            if found >= bottles:
                return True
        return False

    def has_hearts(self, player: int, count: int) -> int:
        # Warning: This only considers items that are marked as advancement items
        return self.heart_count(player) >= count

    def heart_count(self, player: int) -> int:
        # Warning: This only considers items that are marked as advancement items
        diff = self.world.difficulty_requirements[player]
        return min(self.item_count('Boss Heart Container', player), diff.boss_heart_container_limit) \
               + self.item_count('Sanctuary Heart Container', player) \
               + min(self.item_count('Piece of Heart', player), diff.heart_piece_limit) // 4 \
               + 3  # starting hearts

    def can_lift_heavy_rocks(self, player: int) -> bool:
        return self.has('Titans Mitts', player)

    def can_extend_magic(self, player: int, smallmagic: int = 16,
                         fullrefill: bool = False):  # This reflects the total magic Link has, not the total extra he has.
        basemagic = 8
        if self.has('Magic Upgrade (1/4)', player):
            basemagic = 32
        elif self.has('Magic Upgrade (1/2)', player):
            basemagic = 16
        if self.can_buy_unlimited('Green Potion', player) or self.can_buy_unlimited('Blue Potion', player):
            if self.world.difficulty_adjustments[player] == 'hard' and not fullrefill:
                basemagic = basemagic + int(basemagic * 0.5 * self.bottle_count(player))
            elif self.world.difficulty_adjustments[player] == 'expert' and not fullrefill:
                basemagic = basemagic + int(basemagic * 0.25 * self.bottle_count(player))
            else:
                basemagic = basemagic + basemagic * self.bottle_count(player)
        return basemagic >= smallmagic

    def can_kill_most_things(self, player: int, enemies=5) -> bool:
        return (self.has_melee_weapon(player)
                or self.has('Cane of Somaria', player)
                or (self.has('Cane of Byrna', player) and (enemies < 6 or self.can_extend_magic(player)))
                or self.can_shoot_arrows(player)
                or self.has('Fire Rod', player)
                or (self.has('Bombs (10)', player) and enemies < 6))

    def can_shoot_arrows(self, player: int) -> bool:
        if self.world.retro[player]:
            return (self.has('Bow', player) or self.has('Silver Bow', player)) and self.can_buy('Single Arrow', player)
        return self.has('Bow', player) or self.has('Silver Bow', player)

    def can_get_good_bee(self, player: int) -> bool:
        cave = self.world.get_region('Good Bee Cave', player)
        return (
                self.has_bottle(player) and
                self.has('Bug Catching Net', player) and
                (self.has_Boots(player) or (self.has_sword(player) and self.has('Quake', player))) and
                cave.can_reach(self) and
                self.is_not_bunny(cave, player)
        )

    def can_retrieve_tablet(self, player:int) -> bool:
        return self.has('Book of Mudora', player) and (self.has_beam_sword(player) or
               (self.world.swords[player] == "swordless" and
                self.has("Hammer", player)))

    def has_sword(self, player: int) -> bool:
        return self.has('Fighter Sword', player) \
               or self.has('Master Sword', player) \
               or self.has('Tempered Sword', player) \
               or self.has('Golden Sword', player)

    def has_beam_sword(self, player: int) -> bool:
        return self.has('Master Sword', player) or self.has('Tempered Sword', player) or self.has('Golden Sword', player)

    def has_melee_weapon(self, player: int) -> bool:
        return self.has_sword(player) or self.has('Hammer', player)

    def has_Mirror(self, player: int) -> bool:
        return self.has('Magic Mirror', player)

    def has_Boots(self, player: int) -> bool:
        return self.has('Pegasus Boots', player)

    def has_Pearl(self, player: int) -> bool:
        return self.has('Moon Pearl', player)

    def has_fire_source(self, player: int) -> bool:
        return self.has('Fire Rod', player) or self.has('Lamp', player)

    def can_flute(self, player: int) -> bool:
        lw = self.world.get_region('Light World', player)
        return self.has('Flute', player) and lw.can_reach(self) and self.is_not_bunny(lw, player)

    def can_melt_things(self, player: int) -> bool:
        return self.has('Fire Rod', player) or \
               (self.has('Bombos', player) and
                (self.world.swords[player] == "swordless" or
                 self.has_sword(player)))

    def can_avoid_lasers(self, player: int) -> bool:
        return self.has('Mirror Shield', player) or self.has('Cane of Byrna', player) or self.has('Cape', player)

    def is_not_bunny(self, region: Region, player: int) -> bool:
        if self.has_Pearl(player):
            return True

        return region.is_light_world if self.world.mode[player] != 'inverted' else region.is_dark_world

    def can_reach_light_world(self, player: int) -> bool:
        if True in [i.is_light_world for i in self.reachable_regions[player]]:
            return True
        return False

    def can_reach_dark_world(self, player: int) -> bool:
        if True in [i.is_dark_world for i in self.reachable_regions[player]]:
            return True
        return False

    def has_misery_mire_medallion(self, player: int) -> bool:
        return self.has(self.world.required_medallions[player][0], player)

    def has_turtle_rock_medallion(self, player: int) -> bool:
        return self.has(self.world.required_medallions[player][1], player)

    def can_boots_clip_lw(self, player):
        if self.world.mode[player] == 'inverted':
            return self.has_Boots(player) and self.has_Pearl(player)
        return self.has_Boots(player)

    def can_boots_clip_dw(self, player):
        if self.world.mode[player] != 'inverted':
            return self.has_Boots(player) and self.has_Pearl(player)
        return self.has_Boots(player)

    def can_get_glitched_speed_lw(self, player):
        rules = [self.has_Boots(player), any([self.has('Hookshot', player), self.has_sword(player)])]
        if self.world.mode[player] == 'inverted':
            rules.append(self.has_Pearl(player))
        return all(rules)

    def can_superbunny_mirror_with_sword(self, player):
        return self.has_Mirror(player) and self.has_sword(player)

    def can_get_glitched_speed_dw(self, player):
        rules = [self.has_Boots(player), any([self.has('Hookshot', player), self.has_sword(player)])]
        if self.world.mode[player] != 'inverted':
            rules.append(self.has_Pearl(player))
        return all(rules)

    def collect(self, item: Item, event=False, location=None):
        if location:
            self.locations_checked.add(location)
        changed = False
        if item.name.startswith('Progressive '):
            if 'Sword' in item.name:
                if self.has('Golden Sword', item.player):
                    pass
                elif self.has('Tempered Sword', item.player) and self.world.difficulty_requirements[
                    item.player].progressive_sword_limit >= 4:
                    self.prog_items['Golden Sword', item.player] += 1
                    changed = True
                elif self.has('Master Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 3:
                    self.prog_items['Tempered Sword', item.player] += 1
                    changed = True
                elif self.has('Fighter Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 2:
                    self.prog_items['Master Sword', item.player] += 1
                    changed = True
                elif self.world.difficulty_requirements[item.player].progressive_sword_limit >= 1:
                    self.prog_items['Fighter Sword', item.player] += 1
                    changed = True
            elif 'Glove' in item.name:
                if self.has('Titans Mitts', item.player):
                    pass
                elif self.has('Power Glove', item.player):
                    self.prog_items['Titans Mitts', item.player] += 1
                    changed = True
                else:
                    self.prog_items['Power Glove', item.player] += 1
                    changed = True
            elif 'Shield' in item.name:
                if self.has('Mirror Shield', item.player):
                    pass
                elif self.has('Red Shield', item.player) and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 3:
                    self.prog_items['Mirror Shield', item.player] += 1
                    changed = True
                elif self.has('Blue Shield', item.player)  and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 2:
                    self.prog_items['Red Shield', item.player] += 1
                    changed = True
                elif self.world.difficulty_requirements[item.player].progressive_shield_limit >= 1:
                    self.prog_items['Blue Shield', item.player] += 1
                    changed = True
            elif 'Bow' in item.name:
                if self.has('Silver Bow', item.player):
                    pass
                elif self.has('Bow', item.player):
                    self.prog_items['Silver Bow', item.player] += 1
                    changed = True
                else:
                    self.prog_items['Bow', item.player] += 1
                    changed = True
        elif item.name.startswith('Bottle'):
            if self.bottle_count(item.player) < self.world.difficulty_requirements[item.player].progressive_bottle_limit:
                self.prog_items[item.name, item.player] += 1
                changed = True
        elif event or item.advancement:
            self.prog_items[item.name, item.player] += 1
            changed = True

        self.stale[item.player] = True

        if changed:
            if not event:
                self.sweep_for_events()

    def remove(self, item):
        if item.advancement:
            to_remove = item.name
            if to_remove.startswith('Progressive '):
                if 'Sword' in to_remove:
                    if self.has('Golden Sword', item.player):
                        to_remove = 'Golden Sword'
                    elif self.has('Tempered Sword', item.player):
                        to_remove = 'Tempered Sword'
                    elif self.has('Master Sword', item.player):
                        to_remove = 'Master Sword'
                    elif self.has('Fighter Sword', item.player):
                        to_remove = 'Fighter Sword'
                    else:
                        to_remove = None
                elif 'Glove' in item.name:
                    if self.has('Titans Mitts', item.player):
                        to_remove = 'Titans Mitts'
                    elif self.has('Power Glove', item.player):
                        to_remove = 'Power Glove'
                    else:
                        to_remove = None
                elif 'Shield' in item.name:
                    if self.has('Mirror Shield', item.player):
                        to_remove = 'Mirror Shield'
                    elif self.has('Red Shield', item.player):
                        to_remove = 'Red Shield'
                    elif self.has('Blue Shield', item.player):
                        to_remove = 'Blue Shield'
                    else:
                        to_remove = 'None'
                elif 'Bow' in item.name:
                    if self.has('Silver Bow', item.player):
                        to_remove = 'Silver Bow'
                    elif self.has('Bow', item.player):
                        to_remove = 'Bow'
                    else:
                        to_remove = None

            if to_remove is not None:

                self.prog_items[to_remove, item.player] -= 1
                if self.prog_items[to_remove, item.player] < 1:
                    del (self.prog_items[to_remove, item.player])
                # invalidate caches, nothing can be trusted anymore now
                self.reachable_regions[item.player] = set()
                self.blocked_connections[item.player] = set()
                self.stale[item.player] = True

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

    def __init__(self, name: str, type, hint, player: int):
        self.name = name
        self.type = type
        self.entrances = []
        self.exits = []
        self.locations = []
        self.dungeon = None
        self.shop = None
        self.world = None
        self.is_light_world = False  # will be set after making connections.
        self.is_dark_world = False
        self.spot_type = 'Region'
        self.hint_text = hint
        self.recursion_count = 0
        self.player = player

    def can_reach(self, state):
        if state.stale[self.player]:
            state.update_reachable_regions(self.player)
        return self in state.reachable_regions[self.player]

    def can_reach_private(self, state: CollectionState):
        for entrance in self.entrances:
            if entrance.can_reach(state):
                if not self in state.path:
                    state.path[self] = (self.name, state.path.get(entrance, None))
                return True
        return False

    def can_fill(self, item: Item):
        inside_dungeon_item = ((item.smallkey and not self.world.keyshuffle[item.player])
                               or (item.bigkey and not self.world.bigkeyshuffle[item.player])
                               or (item.map and not self.world.mapshuffle[item.player])
                               or (item.compass and not self.world.compassshuffle[item.player]))
        sewer_hack = self.world.mode[item.player] == 'standard' and item.name == 'Small Key (Hyrule Castle)'
        if sewer_hack or inside_dungeon_item:
            return self.dungeon and self.dungeon.is_dungeon_item(item) and item.player == self.player

        return True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.world.get_name_string_for_object(self) if self.world else f'{self.name} (Player {self.player})'


class Entrance(object):

    def __init__(self, player: int, name: str = '', parent=None):
        self.name = name
        self.parent_region = parent
        self.connected_region = None
        self.target = None
        self.addresses = None
        self.spot_type = 'Entrance'
        self.recursion_count = 0
        self.vanilla = None
        self.access_rule = lambda state: True
        self.player = player
        self.hide_path = False

    def can_reach(self, state):
        if self.parent_region.can_reach(state) and self.access_rule(state):
            if not self.hide_path and not self in state.path:
                state.path[self] = (self.name, state.path.get(self.parent_region, (self.parent_region.name, None)))
            return True

        return False

    def connect(self, region, addresses=None, target=None, vanilla=None):
        self.connected_region = region
        self.target = target
        self.addresses = addresses
        self.vanilla = vanilla
        region.entrances.append(self)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        world = self.parent_region.world if self.parent_region else None
        return world.get_name_string_for_object(self) if world else f'{self.name} (Player {self.player})'

class Dungeon(object):

    def __init__(self, name: str, regions, big_key, small_keys, dungeon_items, player: int):
        self.name = name
        self.regions = regions
        self.big_key = big_key
        self.small_keys = small_keys
        self.dungeon_items = dungeon_items
        self.bosses = dict()
        self.player = player
        self.world = None

    @property
    def boss(self):
        return self.bosses.get(None, None)

    @boss.setter
    def boss(self, value):
        self.bosses[None] = value

    @property
    def keys(self):
        return self.small_keys + ([self.big_key] if self.big_key else [])

    @property
    def all_items(self):
        return self.dungeon_items + self.keys

    def is_dungeon_item(self, item: Item) -> bool:
        return item.player == self.player and item.name in [dungeon_item.name for dungeon_item in self.all_items]

    def __eq__(self, other: Item) -> bool:
        return self.name == other.name and self.player == other.player

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.world.get_name_string_for_object(self) if self.world else f'{self.name} (Player {self.player})'

class Boss():
    def __init__(self, name, enemizer_name, defeat_rule, player: int):
        self.name = name
        self.enemizer_name = enemizer_name
        self.defeat_rule = defeat_rule
        self.player = player

    def can_defeat(self, state) -> bool:
        return self.defeat_rule(state, self.player)


class Location():
    shop_slot: bool = False
    shop_slot_disabled: bool = False
    event: bool = False
    locked: bool = False

    def __init__(self, player: int, name: str = '', address=None, crystal: bool = False,
                 hint_text: Optional[str] = None, parent=None,
                 player_address=None):
        self.name = name
        self.parent_region = parent
        self.item = None
        self.crystal = crystal
        self.address = address
        self.player_address = player_address
        self.spot_type = 'Location'
        self.hint_text: str = hint_text if hint_text else name
        self.recursion_count = 0
        self.always_allow = lambda item, state: False
        self.access_rule = lambda state: True
        self.item_rule = lambda item: True
        self.player = player

    def can_fill(self, state: CollectionState, item: Item, check_access=True) -> bool:
        return self.always_allow(state, item) or (self.parent_region.can_fill(item) and self.item_rule(item) and (not check_access or self.can_reach(state)))

    def can_reach(self, state: CollectionState) -> bool:
        # self.access_rule computes faster on average, so placing it first for faster abort
        if self.access_rule(state) and self.parent_region.can_reach(state):
            return True
        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        world = self.parent_region.world if self.parent_region and self.parent_region.world else None
        return world.get_name_string_for_object(self) if world else f'{self.name} (Player {self.player})'

    def __hash__(self):
        return hash((self.name, self.player))

    def __lt__(self, other):
        return (self.player, self.name) < (other.player, other.name)


class Item(object):

    def __init__(self, name='', advancement=False, priority=False, type=None, code=None, pedestal_hint=None, pedestal_credit=None, sickkid_credit=None, zora_credit=None, witch_credit=None, fluteboy_credit=None, hint_text=None, player=None):
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
        self.hint_text = hint_text
        self.code = code
        self.location = None
        self.world = None
        self.player = player

    def __eq__(self, other):
        return self.name == other.name and self.player == other.player

    def __hash__(self):
        return hash((self.name, self.player))

    @property
    def crystal(self) -> bool:
        return self.type == 'Crystal'

    @property
    def smallkey(self) -> bool:
        return self.type == 'SmallKey'

    @property
    def bigkey(self) -> bool:
        return self.type == 'BigKey'

    @property
    def map(self) -> bool:
        return self.type == 'Map'

    @property
    def compass(self) -> bool:
        return self.type == 'Compass'

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.world.get_name_string_for_object(self) if self.world else f'{self.name} (Player {self.player})'


# have 6 address that need to be filled
class Crystal(Item):
    pass


class Spoiler(object):
    world: World

    def __init__(self, world):
        self.world = world
        self.hashes = {}
        self.entrances = OrderedDict()
        self.medallions = {}
        self.playthrough = {}
        self.unreachables = []
        self.startinventory = []
        self.locations = {}
        self.paths = {}
        self.metadata = {}
        self.shops = []
        self.bosses = OrderedDict()

    def set_entrance(self, entrance, exit, direction, player):
        if self.world.players == 1:
            self.entrances[(entrance, direction, player)] = OrderedDict([('entrance', entrance), ('exit', exit), ('direction', direction)])
        else:
            self.entrances[(entrance, direction, player)] = OrderedDict([('player', player), ('entrance', entrance), ('exit', exit), ('direction', direction)])

    def parse_data(self):
        self.medallions = OrderedDict()
        if self.world.players == 1:
            self.medallions['Misery Mire'] = self.world.required_medallions[1][0]
            self.medallions['Turtle Rock'] = self.world.required_medallions[1][1]
        else:
            for player in range(1, self.world.players + 1):
                self.medallions[f'Misery Mire ({self.world.get_player_names(player)})'] = self.world.required_medallions[player][0]
                self.medallions[f'Turtle Rock ({self.world.get_player_names(player)})'] = self.world.required_medallions[player][1]

        self.startinventory = list(map(str, self.world.precollected_items))

        self.locations = OrderedDict()
        listed_locations = set()

        lw_locations = [loc for loc in self.world.get_locations() if loc not in listed_locations and loc.parent_region and loc.parent_region.type == RegionType.LightWorld]
        self.locations['Light World'] = OrderedDict([(str(location), str(location.item) if location.item is not None else 'Nothing') for location in lw_locations])
        listed_locations.update(lw_locations)

        dw_locations = [loc for loc in self.world.get_locations() if loc not in listed_locations and loc.parent_region and loc.parent_region.type == RegionType.DarkWorld]
        self.locations['Dark World'] = OrderedDict([(str(location), str(location.item) if location.item is not None else 'Nothing') for location in dw_locations])
        listed_locations.update(dw_locations)

        cave_locations = [loc for loc in self.world.get_locations() if loc not in listed_locations and loc.parent_region and loc.parent_region.type == RegionType.Cave]
        self.locations['Caves'] = OrderedDict([(str(location), str(location.item) if location.item is not None else 'Nothing') for location in cave_locations])
        listed_locations.update(cave_locations)

        for dungeon in self.world.dungeons:
            dungeon_locations = [loc for loc in self.world.get_locations() if loc not in listed_locations and loc.parent_region and loc.parent_region.dungeon == dungeon]
            self.locations[str(dungeon)] = OrderedDict([(str(location), str(location.item) if location.item is not None else 'Nothing') for location in dungeon_locations])
            listed_locations.update(dungeon_locations)

        other_locations = [loc for loc in self.world.get_locations() if loc not in listed_locations]
        if other_locations:
            self.locations['Other Locations'] = OrderedDict([(str(location), str(location.item) if location.item is not None else 'Nothing') for location in other_locations])
            listed_locations.update(other_locations)

        self.shops = []
        from Shops import ShopType
        for shop in self.world.shops:
            if not shop.custom:
                continue
            shopdata = {'location': str(shop.region),
                        'type': 'Take Any' if shop.type == ShopType.TakeAny else 'Shop'
                       }
            for index, item in enumerate(shop.inventory):
                if item is None:
                    continue
                shopdata['item_{}'.format(index)] = "{} — {}".format(item['item'], item['price']) if item['price'] else item['item']

                if item['player'] > 0:
                    shopdata['item_{}'.format(index)] = shopdata['item_{}'.format(index)].replace('—', '(Player {}) — '.format(item['player']))

                if item['max'] == 0:
                    continue
                shopdata['item_{}'.format(index)] += " x {}".format(item['max'])

                if item['replacement'] is None:
                    continue
                shopdata['item_{}'.format(index)] += ", {} - {}".format(item['replacement'], item['replacement_price']) if item['replacement_price'] else item['replacement']
            self.shops.append(shopdata)

        for player in range(1, self.world.players + 1):
            self.bosses[str(player)] = OrderedDict()
            self.bosses[str(player)]["Eastern Palace"] = self.world.get_dungeon("Eastern Palace", player).boss.name
            self.bosses[str(player)]["Desert Palace"] = self.world.get_dungeon("Desert Palace", player).boss.name
            self.bosses[str(player)]["Tower Of Hera"] = self.world.get_dungeon("Tower of Hera", player).boss.name
            self.bosses[str(player)]["Hyrule Castle"] = "Agahnim"
            self.bosses[str(player)]["Palace Of Darkness"] = self.world.get_dungeon("Palace of Darkness", player).boss.name
            self.bosses[str(player)]["Swamp Palace"] = self.world.get_dungeon("Swamp Palace", player).boss.name
            self.bosses[str(player)]["Skull Woods"] = self.world.get_dungeon("Skull Woods", player).boss.name
            self.bosses[str(player)]["Thieves Town"] = self.world.get_dungeon("Thieves Town", player).boss.name
            self.bosses[str(player)]["Ice Palace"] = self.world.get_dungeon("Ice Palace", player).boss.name
            self.bosses[str(player)]["Misery Mire"] = self.world.get_dungeon("Misery Mire", player).boss.name
            self.bosses[str(player)]["Turtle Rock"] = self.world.get_dungeon("Turtle Rock", player).boss.name
            if self.world.mode[player] != 'inverted':
                self.bosses[str(player)]["Ganons Tower Basement"] = self.world.get_dungeon('Ganons Tower', player).bosses['bottom'].name
                self.bosses[str(player)]["Ganons Tower Middle"] = self.world.get_dungeon('Ganons Tower', player).bosses['middle'].name
                self.bosses[str(player)]["Ganons Tower Top"] = self.world.get_dungeon('Ganons Tower', player).bosses['top'].name
            else:
                self.bosses[str(player)]["Ganons Tower Basement"] = self.world.get_dungeon('Inverted Ganons Tower', player).bosses['bottom'].name
                self.bosses[str(player)]["Ganons Tower Middle"] = self.world.get_dungeon('Inverted Ganons Tower', player).bosses['middle'].name
                self.bosses[str(player)]["Ganons Tower Top"] = self.world.get_dungeon('Inverted Ganons Tower', player).bosses['top'].name

            self.bosses[str(player)]["Ganons Tower"] = "Agahnim 2"
            self.bosses[str(player)]["Ganon"] = "Ganon"

        if self.world.players == 1:
            self.bosses = self.bosses["1"]

        from Utils import __version__ as ERVersion
        self.metadata = {'version': ERVersion,
                         'logic': self.world.logic,
                         'dark_room_logic': self.world.dark_room_logic,
                         'mode': self.world.mode,
                         'retro': self.world.retro,
                         'weapons': self.world.swords,
                         'goal': self.world.goal,
                         'shuffle': self.world.shuffle,
                         'item_pool': self.world.difficulty,
                         'item_functionality': self.world.difficulty_adjustments,
                         'gt_crystals': self.world.crystals_needed_for_gt,
                         'ganon_crystals': self.world.crystals_needed_for_ganon,
                         'open_pyramid': self.world.open_pyramid,
                         'accessibility': self.world.accessibility,
                         'hints': self.world.hints,
                         'mapshuffle': self.world.mapshuffle,
                         'compassshuffle': self.world.compassshuffle,
                         'keyshuffle': self.world.keyshuffle,
                         'bigkeyshuffle': self.world.bigkeyshuffle,
                         'boss_shuffle': self.world.boss_shuffle,
                         'enemy_shuffle': self.world.enemy_shuffle,
                         'enemy_health': self.world.enemy_health,
                         'enemy_damage': self.world.enemy_damage,
                         'killable_thieves': self.world.killable_thieves,
                         'tile_shuffle': self.world.tile_shuffle,
                         'bush_shuffle': self.world.bush_shuffle,
                         'beemizer': self.world.beemizer,
                         'progressive': self.world.progressive,
                         'shufflepots': self.world.shufflepots,
                         'players': self.world.players,
                         'teams': self.world.teams,
                         'progression_balancing': self.world.progression_balancing,
                         'triforce_pieces_available': self.world.triforce_pieces_available,
                         'triforce_pieces_required': self.world.triforce_pieces_required,
                         'shop_shuffle': self.world.shop_shuffle,
                         'shop_shuffle_slots': self.world.shop_shuffle_slots,
                         'shuffle_prizes': self.world.shuffle_prizes,
                         'sprite_pool': self.world.sprite_pool,
                         'restrict_dungeon_item_on_boss': self.world.restrict_dungeon_item_on_boss
                         }

    def to_json(self):
        self.parse_data()
        out = OrderedDict()
        out['Entrances'] = list(self.entrances.values())
        out.update(self.locations)
        out['Starting Inventory'] = self.startinventory
        out['Special'] = self.medallions
        if self.hashes:
            out['Hashes'] = {f"{self.world.player_names[player][team]} (Team {team+1})": hash for (player, team), hash in self.hashes.items()}
        if self.shops:
            out['Shops'] = self.shops
        out['playthrough'] = self.playthrough
        out['paths'] = self.paths
        out['Bosses'] = self.bosses
        out['meta'] = self.metadata

        return json.dumps(out)

    def to_file(self, filename):
        self.parse_data()

        def bool_to_text(variable: Union[bool, str]) -> str:
            if type(variable) == str:
                return variable
            return 'Yes' if variable else 'No'

        with open(filename, 'w', encoding="utf-8-sig") as outfile:
            outfile.write(
                'ALttP Berserker\'s Multiworld Version %s  -  Seed: %s\n\n' % (
                    self.metadata['version'], self.world.seed))
            outfile.write('Filling Algorithm:               %s\n' % self.world.algorithm)
            outfile.write('Players:                         %d\n' % self.world.players)
            outfile.write('Teams:                           %d\n' % self.world.teams)
            for player in range(1, self.world.players + 1):
                if self.world.players > 1:
                    outfile.write('\nPlayer %d: %s\n' % (player, self.world.get_player_names(player)))
                for team in range(self.world.teams):
                    outfile.write('%s%s\n' % (
                        f"Hash - {self.world.player_names[player][team]} (Team {team + 1}): " if self.world.teams > 1 else 'Hash: ',
                        self.hashes[player, team]))
                outfile.write('Logic:                           %s\n' % self.metadata['logic'][player])
                outfile.write('Dark Room Logic:                 %s\n' % self.metadata['dark_room_logic'][player])
                outfile.write('Restricted Boss Drops:           %s\n' %
                              bool_to_text(self.metadata['restrict_dungeon_item_on_boss'][player]))
                if self.world.players > 1:
                    outfile.write('Progression Balanced:            %s\n' % (
                        'Yes' if self.metadata['progression_balancing'][player] else 'No'))
                outfile.write('Mode:                            %s\n' % self.metadata['mode'][player])
                outfile.write('Retro:                           %s\n' %
                              ('Yes' if self.metadata['retro'][player] else 'No'))
                outfile.write('Swords:                          %s\n' % self.metadata['weapons'][player])
                outfile.write('Goal:                            %s\n' % self.metadata['goal'][player])
                if "triforce" in self.metadata["goal"][player]:  # triforce hunt
                    outfile.write("Pieces available for Triforce:   %s\n" %
                                  self.metadata['triforce_pieces_available'][player])
                    outfile.write("Pieces required for Triforce:    %s\n" %
                                  self.metadata["triforce_pieces_required"][player])
                outfile.write('Difficulty:                      %s\n' % self.metadata['item_pool'][player])
                outfile.write('Item Functionality:              %s\n' % self.metadata['item_functionality'][player])
                outfile.write('Item Progression:                %s\n' % self.metadata['progressive'][player])
                outfile.write('Entrance Shuffle:                %s\n' % self.metadata['shuffle'][player])
                outfile.write('Crystals required for GT:        %s\n' % self.metadata['gt_crystals'][player])
                outfile.write('Crystals required for Ganon:     %s\n' % self.metadata['ganon_crystals'][player])
                outfile.write('Pyramid hole pre-opened:         %s\n' % (
                    'Yes' if self.metadata['open_pyramid'][player] else 'No'))
                outfile.write('Accessibility:                   %s\n' % self.metadata['accessibility'][player])
                outfile.write('Map shuffle:                     %s\n' %
                              ('Yes' if self.metadata['mapshuffle'][player] else 'No'))
                outfile.write('Compass shuffle:                 %s\n' %
                              ('Yes' if self.metadata['compassshuffle'][player] else 'No'))
                outfile.write(
                    'Small Key shuffle:               %s\n' % (bool_to_text(self.metadata['keyshuffle'][player])))
                outfile.write('Big Key shuffle:                 %s\n' % (
                    'Yes' if self.metadata['bigkeyshuffle'][player] else 'No'))
                outfile.write('Shop inventory shuffle:          %s\n' %
                              bool_to_text("i" in self.metadata["shop_shuffle"][player]))
                outfile.write('Shop price shuffle:              %s\n' %
                              bool_to_text("p" in self.metadata["shop_shuffle"][player]))
                outfile.write('Shop upgrade shuffle:            %s\n' %
                              bool_to_text("u" in self.metadata["shop_shuffle"][player]))
                outfile.write('New Shop inventory:              %s\n' %
                              bool_to_text("g" in self.metadata["shop_shuffle"][player] or
                                           "f" in self.metadata["shop_shuffle"][player]))
                outfile.write('Custom Potion Shop:              %s\n' %
                              bool_to_text("w" in self.metadata["shop_shuffle"][player]))
                outfile.write('Shop Slots:                      %s\n' %
                              self.metadata["shop_shuffle_slots"][player])
                outfile.write('Boss shuffle:                    %s\n' % self.metadata['boss_shuffle'][player])
                outfile.write(
                    'Enemy shuffle:                   %s\n' % bool_to_text(self.metadata['enemy_shuffle'][player]))
                outfile.write('Enemy health:                    %s\n' % self.metadata['enemy_health'][player])
                outfile.write('Enemy damage:                    %s\n' % self.metadata['enemy_damage'][player])
                outfile.write(f'Killable thieves:                {bool_to_text(self.metadata["killable_thieves"][player])}\n')
                outfile.write(f'Shuffled tiles:                  {bool_to_text(self.metadata["tile_shuffle"][player])}\n')
                outfile.write(f'Shuffled bushes:                 {bool_to_text(self.metadata["bush_shuffle"][player])}\n')
                outfile.write(
                    'Hints:                           %s\n' % ('Yes' if self.metadata['hints'][player] else 'No'))
                outfile.write('Beemizer:                        %s\n' % self.metadata['beemizer'][player])
                outfile.write('Pot shuffle                      %s\n'
                              % ('Yes' if self.metadata['shufflepots'][player] else 'No'))
                outfile.write('Prize shuffle                    %s\n' %
                              self.metadata['shuffle_prizes'][player])
            if self.entrances:
                outfile.write('\n\nEntrances:\n\n')
                outfile.write('\n'.join(['%s%s %s %s' % (f'{self.world.get_player_names(entry["player"])}: '
                                                         if self.world.players > 1 else '', entry['entrance'],
                                                         '<=>' if entry['direction'] == 'both' else
                                                         '<=' if entry['direction'] == 'exit' else '=>',
                                                         entry['exit']) for entry in self.entrances.values()]))
            outfile.write('\n\nMedallions:\n')
            for dungeon, medallion in self.medallions.items():
                outfile.write(f'\n{dungeon}: {medallion}')
            if self.startinventory:
                outfile.write('\n\nStarting Inventory:\n\n')
                outfile.write('\n'.join(self.startinventory))
            outfile.write('\n\nLocations:\n\n')
            outfile.write('\n'.join(['%s: %s' % (location, item) for grouping in self.locations.values() for (location, item) in grouping.items()]))
            outfile.write('\n\nShops:\n\n')
            outfile.write('\n'.join("{} [{}]\n    {}".format(shop['location'], shop['type'], "\n    ".join(item for item in [shop.get('item_0', None), shop.get('item_1', None), shop.get('item_2', None)] if item)) for shop in self.shops))
            for player in range(1, self.world.players + 1):
                if self.world.boss_shuffle[player] != 'none':
                    bossmap = self.bosses[str(player)] if self.world.players > 1 else self.bosses
                    outfile.write(f'\n\nBosses{(f" ({self.world.get_player_names(player)})" if self.world.players > 1 else "")}:\n')
                    outfile.write('    '+'\n    '.join([f'{x}: {y}' for x, y in bossmap.items()]))
            outfile.write('\n\nPlaythrough:\n\n')
            outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(['  %s: %s' % (location, item) for (location, item) in sphere.items()] if sphere_nr != '0' else [f'  {item}' for item in sphere])) for (sphere_nr, sphere) in self.playthrough.items()]))
            if self.unreachables:
                outfile.write('\n\nUnreachable Items:\n\n')
                outfile.write('\n'.join(['%s: %s' % (unreachable.item, unreachable) for unreachable in self.unreachables]))
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


class PlandoItem(NamedTuple):
    item: str
    location: str
    world: Union[bool, str] = False  # False -> own world, True -> not own world
    from_pool: bool = True  # if item should be removed from item pool
    force: str = 'silent'  # false -> warns if item not successfully placed. true -> errors out on failure to place item.

    def warn(self, warning: str):
        if self.force in ['true', 'fail', 'failure', 'none', 'false', 'warn', 'warning']:
            logging.warning(f'{warning}')
        else:
            logging.debug(f'{warning}')

    def failed(self, warning: str, exception=Exception):
        if self.force in ['true', 'fail', 'failure']:
            raise exception(warning)
        else:
            self.warn(warning)


class PlandoConnection(NamedTuple):
    entrance: str
    exit: str
    direction: str  # entrance, exit or both
