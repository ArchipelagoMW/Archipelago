from __future__ import annotations

import collections
import functools
import logging
import random
import secrets
import warnings
from argparse import Namespace
from collections import Counter, deque, defaultdict
from collections.abc import Callable, Collection, Iterable, Iterator, Mapping, MutableSequence, Set as AbstractSet
from enum import IntEnum, IntFlag
from typing import (Any, ClassVar, Dict, List, Literal, NamedTuple,
                    Optional, Protocol, Set, Tuple, Union, TYPE_CHECKING, overload)
import dataclasses

from typing_extensions import NotRequired, TypedDict

import NetUtils
import Options
import Utils

if TYPE_CHECKING:
    from entrance_rando import ERPlacementState
    from rule_builder.rules import Rule
    from worlds import AutoWorld


class Group(TypedDict):
    name: str
    game: str
    world: "AutoWorld.World"
    players: AbstractSet[int]
    item_pool: NotRequired[Set[str]]
    replacement_items: NotRequired[Dict[int, Optional[str]]]
    local_items: NotRequired[Set[str]]
    non_local_items: NotRequired[Set[str]]
    link_replacement: NotRequired[bool]


class ThreadBarrierProxy:
    """Passes through getattr while passthrough is True"""
    def __init__(self, obj: object) -> None:
        self.passthrough = True
        self.obj = obj

    def __getattr__(self, name: str) -> Any:
        if self.passthrough:
            return getattr(self.obj, name)
        else:
            raise RuntimeError("You are in a threaded context and global random state was removed for your safety. "
                               "Please use world.random or randomize ahead of output.")


class HasNameAndPlayer(Protocol):
    name: str
    player: int


@dataclasses.dataclass
class PlandoItemBlock:
    player: int
    from_pool: bool
    force: bool | Literal["silent"]
    worlds: set[int] = dataclasses.field(default_factory=set)
    items: list[str] = dataclasses.field(default_factory=list)
    locations: list[str] = dataclasses.field(default_factory=list)
    resolved_locations: list[Location] = dataclasses.field(default_factory=list)
    count: dict[str, int] = dataclasses.field(default_factory=dict)


class MultiWorld():
    debug_types = False
    player_name: Dict[int, str]
    worlds: Dict[int, "AutoWorld.World"]
    groups: Dict[int, Group]
    regions: RegionManager
    itempool: List[Item]
    is_race: bool = False
    precollected_items: Dict[int, List[Item]]
    state: CollectionState

    plando_options: PlandoOptions
    early_items: Dict[int, Dict[str, int]]
    local_early_items: Dict[int, Dict[str, int]]
    local_items: Dict[int, Options.LocalItems]
    non_local_items: Dict[int, Options.NonLocalItems]
    progression_balancing: Dict[int, Options.ProgressionBalancing]
    completion_condition: Dict[int, CollectionRule]
    indirect_connections: Dict[Region, Set[Entrance]]
    exclude_locations: Dict[int, Options.ExcludeLocations]
    priority_locations: Dict[int, Options.PriorityLocations]
    start_inventory: Dict[int, Options.StartInventory]
    start_hints: Dict[int, Options.StartHints]
    start_location_hints: Dict[int, Options.StartLocationHints]
    item_links: Dict[int, Options.ItemLinks]

    plando_item_blocks: Dict[int, List[PlandoItemBlock]]

    game: Dict[int, str]

    random: random.Random

    class AttributeProxy():
        def __init__(self, rule):
            self.rule = rule

        def __getitem__(self, player) -> bool:
            return self.rule(player)

    class RegionManager:
        region_cache: Dict[int, Dict[str, Region]]
        entrance_cache: Dict[int, Dict[str, Entrance]]
        location_cache: Dict[int, Dict[str, Location]]

        def __init__(self, players: int):
            self.region_cache = {player: {} for player in range(1, players+1)}
            self.entrance_cache = {player: {} for player in range(1, players+1)}
            self.location_cache = {player: {} for player in range(1, players+1)}

        def __iadd__(self, other: Iterable[Region]):
            self.extend(other)
            return self

        def append(self, region: Region):
            assert region.name not in self.region_cache[region.player], \
                f"{region.name} already exists in region cache."
            self.region_cache[region.player][region.name] = region

        def extend(self, regions: Iterable[Region]):
            for region in regions:
                assert region.name not in self.region_cache[region.player], \
                    f"{region.name} already exists in region cache."
                self.region_cache[region.player][region.name] = region

        def add_group(self, new_id: int):
            self.region_cache[new_id] = {}
            self.entrance_cache[new_id] = {}
            self.location_cache[new_id] = {}

        def __iter__(self) -> Iterator[Region]:
            for regions in self.region_cache.values():
                yield from regions.values()

        def __len__(self):
            return sum(len(regions) for regions in self.region_cache.values())

    def __init__(self, players: int):
        # world-local random state is saved for multiple generations running concurrently
        self.random = ThreadBarrierProxy(random.Random())
        self.players = players
        self.player_types = {player: NetUtils.SlotType.player for player in self.player_ids}
        self.algorithm = 'balanced'
        self.groups = {}
        self.regions = self.RegionManager(players)
        self.itempool = []
        self.seed = None
        self.seed_name: str = "Unavailable"
        self.precollected_items = {player: [] for player in self.player_ids}
        self.required_locations = []
        self.custom = False
        self.customitemarray = []
        self.shuffle_ganon = True
        self.spoiler = Spoiler(self)
        self.early_items = {player: {} for player in self.player_ids}
        self.local_early_items = {player: {} for player in self.player_ids}
        self.indirect_connections = {}
        self.start_inventory_from_pool: Dict[int, Options.StartInventoryPool] = {}
        self.plando_item_blocks = {}

        for player in range(1, players + 1):
            def set_player_attr(attr: str, val) -> None:
                self.__dict__.setdefault(attr, {})[player] = val
            set_player_attr('plando_item_blocks', [])
            set_player_attr('game', "Archipelago")
            set_player_attr('completion_condition', lambda state: True)
        self.worlds = {}
        self.plando_options = PlandoOptions.none

    def get_all_ids(self) -> Tuple[int, ...]:
        return self.player_ids + tuple(self.groups)

    def add_group(self, name: str, game: str, players: AbstractSet[int] = frozenset()) -> Tuple[int, Group]:
        """Create a group with name and return the assigned player ID and group.
        If a group of this name already exists, the set of players is extended instead of creating a new one."""
        from worlds import AutoWorld

        for group_id, group in self.groups.items():
            if group["name"] == name:
                group["players"] |= players
                return group_id, group
        new_id: int = self.players + len(self.groups) + 1

        self.regions.add_group(new_id)
        self.game[new_id] = game
        self.player_types[new_id] = NetUtils.SlotType.group
        world_type = AutoWorld.AutoWorldRegister.world_types[game]
        self.worlds[new_id] = world_type.create_group(self, new_id, players)
        self.worlds[new_id].collect_item = AutoWorld.World.collect_item.__get__(self.worlds[new_id])
        self.worlds[new_id].collect = AutoWorld.World.collect.__get__(self.worlds[new_id])
        self.worlds[new_id].remove = AutoWorld.World.remove.__get__(self.worlds[new_id])
        self.player_name[new_id] = name

        new_group = self.groups[new_id] = Group(name=name, game=game, players=players,
                                                world=self.worlds[new_id])

        return new_id, new_group

    def get_player_groups(self, player: int) -> Set[int]:
        return {group_id for group_id, group in self.groups.items() if player in group["players"]}

    def set_seed(self, seed: Optional[int] = None, secure: bool = False, name: Optional[str] = None):
        assert not self.worlds, "seed needs to be initialized before Worlds"
        self.seed = get_seed(seed)
        if secure:
            self.secure()
        else:
            self.random.seed(self.seed)
        self.seed_name = name if name else str(self.seed)

    def set_options(self, args: Namespace) -> None:
        from worlds import AutoWorld

        for player in self.player_ids:
            world_type = AutoWorld.AutoWorldRegister.world_types[self.game[player]]
            self.worlds[player] = world_type(self, player)
            options_dataclass: type[Options.PerGameCommonOptions] = world_type.options_dataclass
            self.worlds[player].options = options_dataclass(**{option_key: getattr(args, option_key)[player]
                                                               for option_key in options_dataclass.type_hints})

    def set_item_links(self):
        from worlds import AutoWorld

        item_links = {}
        replacement_prio = [False, True, None]
        for player in self.player_ids:
            for item_link in self.worlds[player].options.item_links.value:
                if item_link["name"] in item_links:
                    if item_links[item_link["name"]]["game"] != self.game[player]:
                        raise Exception(f"Cannot ItemLink across games. Link: {item_link['name']}")
                    current_link = item_links[item_link["name"]]
                    current_link["players"][player] = item_link["replacement_item"]
                    current_link["item_pool"] &= set(item_link["item_pool"])
                    current_link["exclude"] |= set(item_link.get("exclude", []))
                    current_link["local_items"] &= set(item_link.get("local_items", []))
                    current_link["non_local_items"] &= set(item_link.get("non_local_items", []))
                    current_link["link_replacement"] = min(current_link["link_replacement"],
                                                           replacement_prio.index(item_link["link_replacement"]))
                else:
                    if item_link["name"] in self.player_name.values():
                        raise Exception(f"Cannot name a ItemLink group the same as a player ({item_link['name']}) "
                                        f"({self.get_player_name(player)}).")
                    item_links[item_link["name"]] = {
                        "players": {player: item_link["replacement_item"]},
                        "item_pool": set(item_link["item_pool"]),
                        "exclude": set(item_link.get("exclude", [])),
                        "game": self.game[player],
                        "local_items": set(item_link.get("local_items", [])),
                        "non_local_items": set(item_link.get("non_local_items", [])),
                        "link_replacement": replacement_prio.index(item_link["link_replacement"]),
                        "skip_if_solo": item_link.get("skip_if_solo", False),
                    }

        for _name, item_link in item_links.items():
            current_item_name_groups = AutoWorld.AutoWorldRegister.world_types[item_link["game"]].item_name_groups
            pool = set()
            local_items = set()
            non_local_items = set()
            for item in item_link["item_pool"]:
                pool |= current_item_name_groups.get(item, {item})
            for item in item_link["exclude"]:
                pool -= current_item_name_groups.get(item, {item})
            for item in item_link["local_items"]:
                local_items |= current_item_name_groups.get(item, {item})
            for item in item_link["non_local_items"]:
                non_local_items |= current_item_name_groups.get(item, {item})
            local_items &= pool
            non_local_items &= pool
            item_link["item_pool"] = pool
            item_link["local_items"] = local_items
            item_link["non_local_items"] = non_local_items

        for group_name, item_link in item_links.items():
            game = item_link["game"]
            if item_link["skip_if_solo"] and len(item_link["players"]) == 1:
                continue
            group_id, group = self.add_group(group_name, game, set(item_link["players"]))

            group["item_pool"] = item_link["item_pool"]
            group["replacement_items"] = item_link["players"]
            group["local_items"] = item_link["local_items"]
            group["non_local_items"] = item_link["non_local_items"]
            group["link_replacement"] = replacement_prio[item_link["link_replacement"]]

    def link_items(self) -> None:
        """Called to link together items in the itempool related to the registered item link groups."""
        from worlds import AutoWorld

        for group_id, group in self.groups.items():
            def find_common_pool(players: Set[int], shared_pool: Set[str]) -> Tuple[
                Optional[Dict[int, Dict[str, int]]], Optional[Dict[str, int]]
            ]:
                classifications: Dict[str, int] = collections.defaultdict(int)
                counters = {player: {name: 0 for name in shared_pool} for player in players}
                for item in self.itempool:
                    if item.player in counters and item.name in shared_pool:
                        counters[item.player][item.name] += 1
                        classifications[item.name] |= item.classification

                for player in players.copy():
                    if all([counters[player][item] == 0 for item in shared_pool]):
                        players.remove(player)
                        del (counters[player])

                if not players:
                    return None, None

                for item in shared_pool:
                    count = min(counters[player][item] for player in players)
                    if count:
                        for player in players:
                            counters[player][item] = count
                    else:
                        for player in players:
                            del (counters[player][item])
                return counters, classifications

            common_item_count, classifications = find_common_pool(group["players"], group["item_pool"])
            if not common_item_count:
                continue

            new_itempool: List[Item] = []
            for item_name, item_count in next(iter(common_item_count.values())).items():
                for _ in range(item_count):
                    new_item = group["world"].create_item(item_name)
                    # mangle together all original classification bits
                    new_item.classification |= classifications[item_name]
                    new_itempool.append(new_item)

            region = Region(group["world"].origin_region_name, group_id, self, "ItemLink")
            self.regions.append(region)
            locations = region.locations
            # ensure that progression items are linked first, then non-progression
            self.itempool.sort(key=lambda item: item.advancement)
            for item in self.itempool:
                count = common_item_count.get(item.player, {}).get(item.name, 0)
                if count:
                    loc = Location(group_id, f"Item Link: {item.name} -> {self.player_name[item.player]} {count}",
                        None, region)
                    loc.access_rule = lambda state, item_name = item.name, group_id_ = group_id, count_ = count: \
                        state.has(item_name, group_id_, count_)

                    locations.append(loc)
                    loc.place_locked_item(item)
                    common_item_count[item.player][item.name] -= 1
                else:
                    new_itempool.append(item)

            itemcount = len(self.itempool)
            self.itempool = new_itempool

            while itemcount > len(self.itempool):
                items_to_add = []
                for player in group["players"]:
                    if group["link_replacement"]:
                        item_player = group_id
                    else:
                        item_player = player
                    if group["replacement_items"][player]:
                        items_to_add.append(AutoWorld.call_single(self, "create_item", item_player,
                            group["replacement_items"][player]))
                    else:
                        items_to_add.append(AutoWorld.call_single(self, "create_filler", item_player))
                self.random.shuffle(items_to_add)
                self.itempool.extend(items_to_add[:itemcount - len(self.itempool)])

    def secure(self):
        self.random = ThreadBarrierProxy(secrets.SystemRandom())
        self.is_race = True

    @functools.cached_property
    def player_ids(self) -> Tuple[int, ...]:
        return tuple(range(1, self.players + 1))

    @Utils.cache_self1
    def get_game_players(self, game_name: str) -> Tuple[int, ...]:
        return tuple(player for player in self.player_ids if self.game[player] == game_name)

    @Utils.cache_self1
    def get_game_groups(self, game_name: str) -> Tuple[int, ...]:
        return tuple(group_id for group_id in self.groups if self.game[group_id] == game_name)

    @Utils.cache_self1
    def get_game_worlds(self, game_name: str):
        return tuple(world for player, world in self.worlds.items() if
                     player not in self.groups and self.game[player] == game_name)

    def get_name_string_for_object(self, obj: HasNameAndPlayer) -> str:
        return obj.name if self.players == 1 else f'{obj.name} ({self.get_player_name(obj.player)})'

    def get_player_name(self, player: int) -> str:
        return self.player_name[player]

    def get_file_safe_player_name(self, player: int) -> str:
        return Utils.get_file_safe_name(self.get_player_name(player))

    def get_out_file_name_base(self, player: int) -> str:
        """ the base name (without file extension) for each player's output file for a seed """
        return f"AP_{self.seed_name}_P{player}_{self.get_file_safe_player_name(player).replace(' ', '_')}"

    @functools.cached_property
    def world_name_lookup(self):
        return {self.player_name[player_id]: player_id for player_id in self.player_ids}

    def get_regions(self, player: Optional[int] = None) -> Collection[Region]:
        return self.regions if player is None else self.regions.region_cache[player].values()

    def get_region(self, region_name: str, player: int) -> Region:
        return self.regions.region_cache[player][region_name]

    def get_entrance(self, entrance_name: str, player: int) -> Entrance:
        return self.regions.entrance_cache[player][entrance_name]

    def get_location(self, location_name: str, player: int) -> Location:
        return self.regions.location_cache[player][location_name]

    def get_all_state(self, use_cache: bool | None = None, allow_partial_entrances: bool = False,
                      collect_pre_fill_items: bool = True, perform_sweep: bool = True) -> CollectionState:
        """
        Creates a new CollectionState, and collects all precollected items, all items in the multiworld itempool, those
        specified in each worlds' `get_pre_fill_items()`, and then sweeps the multiworld collecting any other items
        it is able to reach, building as complete of a completed game state as possible.

        :param use_cache: Deprecated and unused.
        :param allow_partial_entrances: Whether the CollectionState should allow for disconnected entrances while
         sweeping, such as before entrance randomization is complete.
        :param collect_pre_fill_items: Whether the items in each worlds' `get_pre_fill_items()` should be added to this
         state.
        :param perform_sweep: Whether this state should perform a sweep for reachable locations, collecting any placed
         items it can.

        :return: The completed CollectionState.
        """
        if __debug__ and use_cache is not None:
            # TODO swap to Utils.deprecate when we want this to crash on source and warn on frozen
            warnings.warn("multiworld.get_all_state no longer caches all_state and this argument will be removed.",
                          DeprecationWarning)
        ret = CollectionState(self, allow_partial_entrances)

        for item in self.itempool:
            self.worlds[item.player].collect(ret, item)
        if collect_pre_fill_items:
            for player in self.player_ids:
                subworld = self.worlds[player]
                for item in subworld.get_pre_fill_items():
                    subworld.collect(ret, item)
        if perform_sweep:
            ret.sweep_for_advancements()

        return ret

    def get_items(self) -> List[Item]:
        return [loc.item for loc in self.get_filled_locations()] + self.itempool

    def find_item_locations(self, item: str, player: int, resolve_group_locations: bool = False) -> List[Location]:
        if resolve_group_locations:
            player_groups = self.get_player_groups(player)
            return [location for location in self.get_locations() if
                    location.item and location.item.name == item and location.player not in player_groups and
                    (location.item.player == player or location.item.player in player_groups)]
        return [location for location in self.get_locations() if
                location.item and location.item.name == item and location.item.player == player]

    def find_item(self, item: str, player: int) -> Location:
        return next(location for location in self.get_locations() if
                    location.item and location.item.name == item and location.item.player == player)

    def find_items_in_locations(self, items: Set[str], player: int, resolve_group_locations: bool = False) -> List[Location]:
        if resolve_group_locations:
            player_groups = self.get_player_groups(player)
            return [location for location in self.get_locations() if
                    location.item and location.item.name in items and location.player not in player_groups and
                    (location.item.player == player or location.item.player in player_groups)]
        return [location for location in self.get_locations() if
                location.item and location.item.name in items and location.item.player == player]

    def create_item(self, item_name: str, player: int) -> Item:
        return self.worlds[player].create_item(item_name)

    def push_precollected(self, item: Item):
        self.precollected_items[item.player].append(item)
        self.state.collect(item, True)

    def push_item(self, location: Location, item: Item, collect: bool = True):
        location.item = item
        item.location = location
        if collect:
            self.state.collect(item, location.advancement, location)

        logging.debug('Placed %s at %s', item, location)

    def get_entrances(self, player: Optional[int] = None) -> Iterable[Entrance]:
        if player is not None:
            return self.regions.entrance_cache[player].values()
        return Utils.RepeatableChain(tuple(self.regions.entrance_cache[player].values()
                                           for player in self.regions.entrance_cache))

    def register_indirect_condition(self, region: Region, entrance: Entrance):
        """Report that access to this Region can result in unlocking this Entrance,
        state.can_reach(Region) in the Entrance's traversal condition, as opposed to pure transition logic."""
        self.indirect_connections.setdefault(region, set()).add(entrance)

    def get_locations(self, player: int | None = None) -> Collection[Location]:
        if player is not None:
            return self.regions.location_cache[player].values()
        return Utils.RepeatableChain(tuple(self.regions.location_cache[player].values()
                                           for player in self.regions.location_cache))

    def get_unfilled_locations(self, player: Optional[int] = None) -> List[Location]:
        return [location for location in self.get_locations(player) if location.item is None]

    def get_filled_locations(self, player: Optional[int] = None) -> List[Location]:
        return [location for location in self.get_locations(player) if location.item is not None]

    def get_reachable_locations(self, state: Optional[CollectionState] = None, player: Optional[int] = None) -> List[Location]:
        state: CollectionState = state if state else self.state
        return [location for location in self.get_locations(player) if location.can_reach(state)]

    def get_placeable_locations(self, state=None, player=None) -> List[Location]:
        state: CollectionState = state if state else self.state
        return [location for location in self.get_locations(player) if location.item is None and location.can_reach(state)]

    def get_unfilled_locations_for_players(self, location_names: List[str], players: Iterable[int]):
        for player in players:
            if not location_names:
                valid_locations = [location.name for location in self.get_unfilled_locations(player)]
            else:
                valid_locations = location_names
            relevant_cache = self.regions.location_cache[player]
            for location_name in valid_locations:
                location = relevant_cache.get(location_name, None)
                if location and location.item is None:
                    yield location

    def unlocks_new_location(self, item: Item) -> bool:
        temp_state = self.state.copy()
        temp_state.collect(item, True)

        for location in self.get_unfilled_locations(item.player):
            if temp_state.can_reach(location) and not self.state.can_reach(location):
                return True

        return False

    def has_beaten_game(self, state: CollectionState, player: Optional[int] = None) -> bool:
        if player:
            return self.completion_condition[player](state)
        else:
            return all((self.has_beaten_game(state, p) for p in range(1, self.players + 1)))

    def can_beat_game(self,
                      starting_state: Optional[CollectionState] = None,
                      locations: Optional[Iterable[Location]] = None) -> bool:
        if starting_state:
            if self.has_beaten_game(starting_state):
                return True
            state = starting_state.copy()
        else:
            state = CollectionState(self)
            if self.has_beaten_game(state):
                return True

        for _ in state.sweep_for_advancements(locations,
                                              yield_each_sweep=True,
                                              checked_locations=state.locations_checked):
            if self.has_beaten_game(state):
                return True

        return False

    def get_spheres(self) -> Iterator[Set[Location]]:
        """
        yields a set of locations for each logical sphere

        If there are unreachable locations, the last sphere of reachable
        locations is followed by an empty set, and then a set of all of the
        unreachable locations.
        """
        state = CollectionState(self)
        locations = set(self.get_filled_locations())

        while locations:
            sphere: Set[Location] = set()

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

    def get_sendable_spheres(self) -> Iterator[Set[Location]]:
        """
        yields a set of multiserver sendable locations (location.item.code: int) for each logical sphere

        If there are unreachable locations, the last sphere of reachable locations is followed by an empty set,
        and then a set of all of the unreachable locations.
        """
        state = CollectionState(self)
        locations: Set[Location] = set()
        events: Set[Location] = set()
        for location in self.get_filled_locations():
            if type(location.item.code) is int and type(location.address) is int:
                locations.add(location)
            else:
                events.add(location)

        while locations:
            sphere: Set[Location] = set()

            # cull events out
            done_events: Set[Union[Location, None]] = {None}
            while done_events:
                done_events = set()
                for event in events:
                    if event.can_reach(state):
                        state.collect(event.item, True, event)
                        done_events.add(event)
                events -= done_events

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
        players: Dict[str, Set[int]] = {
            "minimal": set(),
            "items": set(),
            "full": set()
        }
        for player, world in self.worlds.items():
            players[world.options.accessibility.current_key].add(player)

        beatable_fulfilled = False

        def location_condition(location: Location) -> bool:
            """Determine if this location has to be accessible, location is already filtered by location_relevant"""
            return location.player in players["full"] or \
                (location.item and location.item.player not in players["minimal"])

        def location_relevant(location: Location) -> bool:
            """Determine if this location is relevant to sweep."""
            return location.player in players["full"] or location.advancement

        def all_done() -> bool:
            """Check if all access rules are fulfilled"""
            if not beatable_fulfilled:
                return False
            if any(location_condition(location) for location in locations):
                return False  # still locations required to be collected
            return True

        locations = [location for location in self.get_locations() if location_relevant(location)]

        while locations:
            sphere: List[Location] = []
            for n in range(len(locations) - 1, -1, -1):
                if locations[n].can_reach(state):
                    sphere.append(locations.pop(n))

            if not sphere:
                if __debug__:
                    from Fill import FillError
                    raise FillError(
                        f"Could not access required locations for accessibility check. Missing: {locations}",
                        multiworld=self,
                    )
                # ran out of places and did not finish yet, quit
                logging.warning(f"Could not access required locations for accessibility check."
                                f" Missing: {locations}")
                return False

            for location in sphere:
                if location.item:
                    state.collect(location.item, True, location)

            if self.has_beaten_game(state):
                beatable_fulfilled = True

            if all_done():
                return True

        return False


PathValue = Tuple[str, Optional["PathValue"]]


class CollectionState():
    prog_items: Dict[int, Counter[str]]
    multiworld: MultiWorld
    reachable_regions: Dict[int, Set[Region]]
    blocked_connections: Dict[int, Set[Entrance]]
    advancements: Set[Location]
    path: Dict[Union[Region, Entrance], PathValue]
    locations_checked: Set[Location]
    """Internal cache for Advancement Locations already checked by this CollectionState. Not for use in logic."""
    stale: Dict[int, bool]
    allow_partial_entrances: bool
    additional_init_functions: List[Callable[[CollectionState, MultiWorld], None]] = []
    additional_copy_functions: List[Callable[[CollectionState, CollectionState], CollectionState]] = []

    def __init__(self, parent: MultiWorld, allow_partial_entrances: bool = False):
        assert parent.worlds, "CollectionState created without worlds initialized in parent"
        self.prog_items = {player: Counter() for player in parent.get_all_ids()}
        self.multiworld = parent
        self.reachable_regions = {player: set() for player in parent.get_all_ids()}
        self.blocked_connections = {player: set() for player in parent.get_all_ids()}
        self.advancements = set()
        self.path = {}
        self.locations_checked = set()
        self.stale = {player: True for player in parent.get_all_ids()}
        self.allow_partial_entrances = allow_partial_entrances
        for function in self.additional_init_functions:
            function(self, parent)
        for items in parent.precollected_items.values():
            for item in items:
                self.collect(item, True)

    def update_reachable_regions(self, player: int):
        self.stale[player] = False
        world: AutoWorld.World = self.multiworld.worlds[player]
        reachable_regions = self.reachable_regions[player]
        queue = deque(self.blocked_connections[player])
        start: Region = world.get_region(world.origin_region_name)

        # init on first call - this can't be done on construction since the regions don't exist yet
        if start not in reachable_regions:
            reachable_regions.add(start)
            self.blocked_connections[player].update(start.exits)
            queue.extend(start.exits)

        if world.explicit_indirect_conditions:
            self._update_reachable_regions_explicit_indirect_conditions(player, queue)
        else:
            self._update_reachable_regions_auto_indirect_conditions(player, queue)

    def _update_reachable_regions_explicit_indirect_conditions(self, player: int, queue: deque[Entrance]):
        reachable_regions = self.reachable_regions[player]
        blocked_connections = self.blocked_connections[player]
        # run BFS on all connections, and keep track of those blocked by missing items
        while queue:
            connection = queue.popleft()
            new_region = connection.connected_region
            if new_region in reachable_regions:
                blocked_connections.remove(connection)
            elif connection.can_reach(self):
                if self.allow_partial_entrances and not new_region:
                    continue
                assert new_region, f"tried to search through an Entrance \"{connection}\" with no connected Region"
                reachable_regions.add(new_region)
                blocked_connections.remove(connection)
                blocked_connections.update(new_region.exits)
                queue.extend(new_region.exits)
                self.path[new_region] = (new_region.name, self.path.get(connection, None))
                self.multiworld.worlds[player].reached_region(self, new_region)

                # Retry connections if the new region can unblock them
                entrances = self.multiworld.indirect_connections.get(new_region)
                if entrances is not None:
                    relevant_entrances = entrances.intersection(blocked_connections)
                    relevant_entrances.difference_update(queue)
                    queue.extend(relevant_entrances)

    def _update_reachable_regions_auto_indirect_conditions(self, player: int, queue: deque[Entrance]):
        reachable_regions = self.reachable_regions[player]
        blocked_connections = self.blocked_connections[player]
        new_connection: bool = True
        # run BFS on all connections, and keep track of those blocked by missing items
        while new_connection:
            new_connection = False
            while queue:
                connection = queue.popleft()
                new_region = connection.connected_region
                if new_region in reachable_regions:
                    blocked_connections.remove(connection)
                elif connection.can_reach(self):
                    if self.allow_partial_entrances and not new_region:
                        continue
                    assert new_region, f"tried to search through an Entrance \"{connection}\" with no connected Region"
                    reachable_regions.add(new_region)
                    blocked_connections.remove(connection)
                    blocked_connections.update(new_region.exits)
                    queue.extend(new_region.exits)
                    self.path[new_region] = (new_region.name, self.path.get(connection, None))
                    new_connection = True
                    self.multiworld.worlds[player].reached_region(self, new_region)
            # sweep for indirect connections, mostly Entrance.can_reach(unrelated_Region)
            queue.extend(blocked_connections)

    def copy(self) -> CollectionState:
        ret = CollectionState(self.multiworld)
        ret.prog_items = {player: counter.copy() for player, counter in self.prog_items.items()}
        ret.reachable_regions = {player: region_set.copy() for player, region_set in
                                 self.reachable_regions.items()}
        ret.blocked_connections = {player: entrance_set.copy() for player, entrance_set in
                                   self.blocked_connections.items()}
        ret.advancements = self.advancements.copy()
        ret.path = self.path.copy()
        ret.locations_checked = self.locations_checked.copy()
        ret.allow_partial_entrances = self.allow_partial_entrances
        for function in self.additional_copy_functions:
            ret = function(self, ret)
        return ret

    def can_reach(self,
                  spot: Union[Location, Entrance, Region, str],
                  resolution_hint: Optional[str] = None,
                  player: Optional[int] = None) -> bool:
        if isinstance(spot, str):
            assert isinstance(player, int), "can_reach: player is required if spot is str"
            # try to resolve a name
            if resolution_hint == 'Location':
                return self.can_reach_location(spot, player)
            elif resolution_hint == 'Entrance':
                return self.can_reach_entrance(spot, player)
            else:
                # default to Region
                return self.can_reach_region(spot, player)
        return spot.can_reach(self)

    def can_reach_location(self, spot: str, player: int) -> bool:
        return self.multiworld.get_location(spot, player).can_reach(self)

    def can_reach_entrance(self, spot: str, player: int) -> bool:
        return self.multiworld.get_entrance(spot, player).can_reach(self)

    def can_reach_region(self, spot: str, player: int) -> bool:
        return self.multiworld.get_region(spot, player).can_reach(self)

    def sweep_for_events(self, locations: Optional[Iterable[Location]] = None) -> None:
        Utils.deprecate("sweep_for_events has been renamed to sweep_for_advancements. The functionality is the same. "
                        "Please switch over to sweep_for_advancements.")
        return self.sweep_for_advancements(locations)

    def _sweep_for_advancements_impl(self, advancements_per_player: List[Tuple[int, List[Location]]],
                                     yield_each_sweep: bool) -> Iterator[None]:
        """
        The implementation for sweep_for_advancements is separated here because it returns a generator due to the use
        of a yield statement.
        """
        all_players = {player for player, _ in advancements_per_player}
        players_to_check = all_players
        # As an optimization, it is assumed that each player's world only logically depends on itself. However, worlds
        # are allowed to logically depend on other worlds, so once there are no more players that should be checked
        # under this assumption, an extra sweep iteration is performed that checks every player, to confirm that the
        # sweep is finished.
        checking_if_finished = False
        while players_to_check:
            next_advancements_per_player: List[Tuple[int, List[Location]]] = []
            next_players_to_check = set()

            for player, locations in advancements_per_player:
                if player not in players_to_check:
                    next_advancements_per_player.append((player, locations))
                    continue

                # Accessibility of each location is checked first because a player's region accessibility cache becomes
                # stale whenever one of their own items is collected into the state.
                reachable_locations: List[Location] = []
                unreachable_locations: List[Location] = []
                for location in locations:
                    if location.can_reach(self):
                        # Locations containing items that do not belong to `player` could be collected immediately
                        # because they won't stale `player`'s region accessibility cache, but, for simplicity, all the
                        # items at reachable locations are collected in a single loop.
                        reachable_locations.append(location)
                    else:
                        unreachable_locations.append(location)
                if unreachable_locations:
                    next_advancements_per_player.append((player, unreachable_locations))

                # A previous player's locations processed in the current `while players_to_check` iteration could have
                # collected items belonging to `player`, but now that all of `player`'s reachable locations have been
                # found, it can be assumed that `player` will not gain any more reachable locations until another one of
                # their items is collected.
                # It would be clearer to not add players to `next_players_to_check` in the first place if they have yet
                # to be processed in the current `while players_to_check` iteration, but checking if a player should be
                # added to `next_players_to_check` would need to be run once for every item that is collected, so it is
                # more performant to instead discard `player` from `next_players_to_check` once their locations have
                # been processed.
                next_players_to_check.discard(player)

                # Collect the items from the reachable locations.
                for advancement in reachable_locations:
                    self.advancements.add(advancement)
                    item = advancement.item
                    assert isinstance(item, Item), "tried to collect advancement Location with no Item"
                    if self.collect(item, True, advancement):
                        # The player the item belongs to may be able to reach additional locations in the next sweep
                        # iteration.
                        next_players_to_check.add(item.player)

            if not next_players_to_check:
                if not checking_if_finished:
                    # It is assumed that each player's world only logically depends on itself, which may not be the
                    # case, so confirm that the sweep is finished by doing an extra iteration that checks every player.
                    checking_if_finished = True
                    next_players_to_check = all_players
            else:
                checking_if_finished = False

            players_to_check = next_players_to_check
            advancements_per_player = next_advancements_per_player

            if yield_each_sweep:
                yield

    @overload
    def sweep_for_advancements(self, locations: Optional[Iterable[Location]] = None, *,
                               yield_each_sweep: Literal[True],
                               checked_locations: Optional[Set[Location]] = None) -> Iterator[None]: ...

    @overload
    def sweep_for_advancements(self, locations: Optional[Iterable[Location]] = None,
                               yield_each_sweep: Literal[False] = False,
                               checked_locations: Optional[Set[Location]] = None) -> None: ...

    def sweep_for_advancements(self, locations: Optional[Iterable[Location]] = None, yield_each_sweep: bool = False,
                               checked_locations: Optional[Set[Location]] = None) -> Optional[Iterator[None]]:
        """
        Sweep through the locations that contain uncollected advancement items, collecting the items into the state
        until there are no more reachable locations that contain uncollected advancement items.

        :param locations: The locations to sweep through, defaulting to all locations in the multiworld.
        :param yield_each_sweep: When True, return a generator that yields at the end of each sweep iteration.
        :param checked_locations: Optional override of locations to filter out from the locations argument, defaults to
        self.advancements when None.
        """
        if checked_locations is None:
            checked_locations = self.advancements

        # Since the sweep loop usually performs many iterations, the locations are filtered in advance.
        # A list of tuples is used, instead of a dictionary, because it is faster to iterate.
        advancements_per_player: List[Tuple[int, List[Location]]]
        if locations is None:
            # `location.advancement` can only be True for filled locations, so unfilled locations are filtered out.
            advancements_per_player = []
            for player, locations_dict in self.multiworld.regions.location_cache.items():
                filtered_locations = [location for location in locations_dict.values()
                                      if location.advancement and location not in checked_locations]
                if filtered_locations:
                    advancements_per_player.append((player, filtered_locations))
        else:
            # Filter and separate the locations into a list for each player.
            advancements_per_player_dict: Dict[int, List[Location]] = defaultdict(list)
            for location in locations:
                if location.advancement and location not in checked_locations:
                    advancements_per_player_dict[location.player].append(location)
            # Convert to a list of tuples.
            advancements_per_player = list(advancements_per_player_dict.items())
            del advancements_per_player_dict

        if yield_each_sweep:
            # Return a generator that will yield at the end of each sweep iteration.
            return self._sweep_for_advancements_impl(advancements_per_player, True)
        else:
            # Create the generator, but tell it not to yield anything, so it will run to completion in zero iterations
            # once started, then start and exhaust the generator by attempting to iterate it.
            for _ in self._sweep_for_advancements_impl(advancements_per_player, False):
                assert False, "Generator yielded when it should have run to completion without yielding"
            return None

    # item name related
    def has(self, item: str, player: int, count: int = 1) -> bool:
        return self.prog_items[player][item] >= count

    # for loops are specifically used in all/any/count methods, instead of all()/any()/sum(), to avoid the overhead of
    # creating and iterating generator instances. In `return all(player_prog_items[item] for item in items)`, the
    # argument to all() would be a new generator instance, for example.
    def has_all(self, items: Iterable[str], player: int) -> bool:
        """Returns True if each item name of items is in state at least once."""
        player_prog_items = self.prog_items[player]
        for item in items:
            if not player_prog_items[item]:
                return False
        return True

    def has_any(self, items: Iterable[str], player: int) -> bool:
        """Returns True if at least one item name of items is in state at least once."""
        player_prog_items = self.prog_items[player]
        for item in items:
            if player_prog_items[item]:
                return True
        return False

    def has_all_counts(self, item_counts: Mapping[str, int], player: int) -> bool:
        """Returns True if each item name is in the state at least as many times as specified."""
        player_prog_items = self.prog_items[player]
        for item, count in item_counts.items():
            if player_prog_items[item] < count:
                return False
        return True

    def has_any_count(self, item_counts: Mapping[str, int], player: int) -> bool:
        """Returns True if at least one item name is in the state at least as many times as specified."""
        player_prog_items = self.prog_items[player]
        for item, count in item_counts.items():
            if player_prog_items[item] >= count:
                return True
        return False

    def count(self, item: str, player: int) -> int:
        return self.prog_items[player][item]

    def has_from_list(self, items: Iterable[str], player: int, count: int) -> bool:
        """Returns True if the state contains at least `count` items matching any of the item names from a list."""
        if count <= 0:
            return True
        found: int = 0
        player_prog_items = self.prog_items[player]
        for item_name in items:
            found += player_prog_items[item_name]
            if found >= count:
                return True
        return False

    def has_from_list_unique(self, items: Iterable[str], player: int, count: int) -> bool:
        """Returns True if the state contains at least `count` items matching any of the item names from a list.
        Ignores duplicates of the same item."""
        if count <= 0:
            return True
        found: int = 0
        player_prog_items = self.prog_items[player]
        for item_name in items:
            found += player_prog_items[item_name] > 0
            if found >= count:
                return True
        return False

    def count_from_list(self, items: Iterable[str], player: int) -> int:
        """Returns the cumulative count of items from a list present in state."""
        player_prog_items = self.prog_items[player]
        total = 0
        for item_name in items:
            total += player_prog_items[item_name]
        return total

    def count_from_list_unique(self, items: Iterable[str], player: int) -> int:
        """Returns the cumulative count of items from a list present in state. Ignores duplicates of the same item."""
        player_prog_items = self.prog_items[player]
        total = 0
        for item_name in items:
            if player_prog_items[item_name] > 0:
                total += 1
        return total

    # item name group related
    def has_group(self, item_name_group: str, player: int, count: int = 1) -> bool:
        """Returns True if the state contains at least `count` items present in a specified item group."""
        if count <= 0:
            return True
        found: int = 0
        player_prog_items = self.prog_items[player]
        for item_name in self.multiworld.worlds[player].item_name_groups[item_name_group]:
            found += player_prog_items[item_name]
            if found >= count:
                return True
        return False

    def has_group_unique(self, item_name_group: str, player: int, count: int = 1) -> bool:
        """Returns True if the state contains at least `count` items present in a specified item group.
        Ignores duplicates of the same item.
        """
        if count <= 0:
            return True
        found: int = 0
        player_prog_items = self.prog_items[player]
        for item_name in self.multiworld.worlds[player].item_name_groups[item_name_group]:
            found += player_prog_items[item_name] > 0
            if found >= count:
                return True
        return False

    def count_group(self, item_name_group: str, player: int) -> int:
        """Returns the cumulative count of items from an item group present in state."""
        player_prog_items = self.prog_items[player]
        return sum(
            player_prog_items[item_name]
            for item_name in self.multiworld.worlds[player].item_name_groups[item_name_group]
        )

    def count_group_unique(self, item_name_group: str, player: int) -> int:
        """Returns the cumulative count of items from an item group present in state.
        Ignores duplicates of the same item."""
        player_prog_items = self.prog_items[player]
        return sum(
            player_prog_items[item_name] > 0
            for item_name in self.multiworld.worlds[player].item_name_groups[item_name_group]
        )

    # Item related
    def collect(self, item: Item, prevent_sweep: bool = False, location: Optional[Location] = None) -> bool:
        if location:
            self.locations_checked.add(location)

        changed = self.multiworld.worlds[item.player].collect(self, item)

        self.stale[item.player] = True

        if changed and not prevent_sweep:
            self.sweep_for_advancements()

        return changed

    def add_item(self, item: str, player: int, count: int = 1) -> None:
        """
        Adds the item to state.

        :param item: The item to be added.
        :param player: The player the item is for.
        :param count: How many of the item to add.
        """
        assert count > 0
        self.prog_items[player][item] += count

    def remove(self, item: Item):
        changed = self.multiworld.worlds[item.player].remove(self, item)
        if changed:
            # invalidate caches, nothing can be trusted anymore now
            self.reachable_regions[item.player] = set()
            self.blocked_connections[item.player] = set()
            self.stale[item.player] = True

    def remove_item(self, item: str, player: int, count: int = 1) -> None:
        """
        Removes the item from state.

        :param item: The item to be removed.
        :param player: The player the item is for.
        :param count: How many of the item to remove.
        """
        assert count > 0
        self.prog_items[player][item] -= count
        if self.prog_items[player][item] < 1:
            del (self.prog_items[player][item])

    def set_item(self, item: str, player: int, count: int) -> None:
        """
        Sets the item in state equal to the provided count.

        :param item: The item to modify.
        :param player: The player the item is for.
        :param count: How many of the item to now have.
        """
        assert count >= 0
        if count == 0:
            del (self.prog_items[player][item])
        else:
            self.prog_items[player][item] = count


CollectionRule = Callable[[CollectionState], bool]
DEFAULT_COLLECTION_RULE: CollectionRule = staticmethod(lambda state: True)


class EntranceType(IntEnum):
    ONE_WAY = 1
    TWO_WAY = 2


class Entrance:
    access_rule: CollectionRule = DEFAULT_COLLECTION_RULE
    hide_path: bool = False
    player: int
    name: str
    parent_region: Optional[Region]
    connected_region: Optional[Region] = None
    randomization_group: int
    randomization_type: EntranceType

    def __init__(self, player: int, name: str = "", parent: Optional[Region] = None,
                 randomization_group: int = 0, randomization_type: EntranceType = EntranceType.ONE_WAY) -> None:
        self.name = name
        self.parent_region = parent
        self.player = player
        self.randomization_group = randomization_group
        self.randomization_type = randomization_type

    def can_reach(self, state: CollectionState) -> bool:
        assert self.parent_region, f"called can_reach on an Entrance \"{self}\" with no parent_region"
        if self.parent_region.can_reach(state) and self.access_rule(state):
            if not self.hide_path and self not in state.path:
                state.path[self] = (self.name, state.path.get(self.parent_region, (self.parent_region.name, None)))
            return True

        return False

    def connect(self, region: Region) -> None:
        self.connected_region = region
        region.entrances.append(self)

    def is_valid_source_transition(self, er_state: "ERPlacementState") -> bool:
        """
        Determines whether this is a valid source transition, that is, whether the entrance
        randomizer is allowed to pair it to place any other regions. By default, this is the
        same as a reachability check, but can be modified by Entrance implementations to add
        other restrictions based on the placement state.

        :param er_state: The current (partial) state of the ongoing entrance randomization
        """
        return self.can_reach(er_state.collection_state)

    def can_connect_to(self, other: Entrance, dead_end: bool, er_state: "ERPlacementState") -> bool:
        """
        Determines whether a given Entrance is a valid target transition, that is, whether
        the entrance randomizer is allowed to pair this Entrance to that Entrance. By default,
        only allows connection between entrances of the same type (one ways only go to one ways,
        two ways always go to two ways) and prevents connecting an exit to itself in coupled mode.

        :param other: The proposed Entrance to connect to
        :param dead_end: Whether the other entrance considered a dead end by Entrance randomization
        :param er_state: The current (partial) state of the ongoing entrance randomization
        """
        # the implementation of coupled causes issues for self-loops since the reverse entrance will be the
        # same as the forward entrance. In uncoupled they are ok.
        return self.randomization_type == other.randomization_type and (not er_state.coupled or self.name != other.name)

    def __repr__(self):
        multiworld = self.parent_region.multiworld if self.parent_region else None
        return multiworld.get_name_string_for_object(self) if multiworld else f'{self.name} (Player {self.player})'


class Region:
    name: str
    _hint_text: str
    player: int
    multiworld: Optional[MultiWorld]
    entrances: List[Entrance]
    exits: List[Entrance]
    locations: List[Location]
    entrance_type: ClassVar[type[Entrance]] = Entrance

    class Register(MutableSequence):
        region_manager: MultiWorld.RegionManager

        def __init__(self, region_manager: MultiWorld.RegionManager):
            self._list = []
            self.region_manager = region_manager

        def __getitem__(self, index: int) -> Location:
            return self._list[index]

        def __setitem__(self, index: int, value: Location) -> None:
            raise NotImplementedError()

        def __len__(self) -> int:
            return len(self._list)

        def __iter__(self):
            return iter(self._list)

        # This seems to not be needed, but that's a bit suspicious.
        # def __del__(self):
        #     self.clear()

        def copy(self):
            return self._list.copy()

    class LocationRegister(Register):
        def __delitem__(self, index: int) -> None:
            location: Location = self._list[index]
            del self._list[index]
            del(self.region_manager.location_cache[location.player][location.name])

        def insert(self, index: int, value: Location) -> None:
            assert value.name not in self.region_manager.location_cache[value.player], \
                f"{value.name} already exists in the location cache."
            self._list.insert(index, value)
            self.region_manager.location_cache[value.player][value.name] = value

    class EntranceRegister(Register):
        def __delitem__(self, index: int) -> None:
            entrance: Entrance = self._list[index]
            del self._list[index]
            del(self.region_manager.entrance_cache[entrance.player][entrance.name])

        def insert(self, index: int, value: Entrance) -> None:
            assert value.name not in self.region_manager.entrance_cache[value.player], \
                f"{value.name} already exists in the entrance cache."
            self._list.insert(index, value)
            self.region_manager.entrance_cache[value.player][value.name] = value

    _locations: LocationRegister[Location]
    _exits: EntranceRegister[Entrance]

    def __init__(self, name: str, player: int, multiworld: MultiWorld, hint: Optional[str] = None):
        self.name = name
        self.entrances = []
        self._exits = self.EntranceRegister(multiworld.regions)
        self._locations = self.LocationRegister(multiworld.regions)
        self.multiworld = multiworld
        self._hint_text = hint
        self.player = player

    def get_locations(self):
        return self._locations

    def set_locations(self, new):
        if new is self._locations:
            return
        self._locations.clear()
        self._locations.extend(new)

    locations = property(get_locations, set_locations)

    def get_exits(self):
        return self._exits

    def set_exits(self, new):
        if new is self._exits:
            return
        self._exits.clear()
        self._exits.extend(new)

    exits = property(get_exits, set_exits)

    def can_reach(self, state: CollectionState) -> bool:
        if state.stale[self.player]:
            state.update_reachable_regions(self.player)
        return self in state.reachable_regions[self.player]

    @property
    def hint_text(self) -> str:
        return self._hint_text if self._hint_text else self.name

    def get_connecting_entrance(self, is_main_entrance: Callable[[Entrance], bool]) -> Entrance:
        for entrance in self.entrances:
            if is_main_entrance(entrance):
                return entrance
        for entrance in self.entrances:  # BFS might be better here, trying DFS for now.
            return entrance.parent_region.get_connecting_entrance(is_main_entrance)

    def add_locations(self, locations: Mapping[str, int | None], location_type: type[Location] | None = None) -> None:
        """
        Adds locations to the Region object, where location_type is your Location class and locations is a dict of
        location names to address.

        :param locations: dictionary of locations to be created and added to this Region `{name: ID}`
        :param location_type: Location class to be used to create the locations with"""
        if location_type is None:
            location_type = Location
        for location, address in locations.items():
            self.locations.append(location_type(self.player, location, address, self))

    def add_event(
        self,
        location_name: str,
        item_name: str | None = None,
        rule: CollectionRule | Rule[Any] | None = None,
        location_type: type[Location] | None = None,
        item_type: type[Item] | None = None,
        show_in_spoiler: bool = True,
    ) -> Item:
        """
        Adds an event location/item pair to the region.

        :param location_name: Name for the event location.
        :param item_name: Name for the event item. If not provided, defaults to location_name.
        :param rule: Callable to determine access for this event location within its region.
        :param location_type: Location class to create the event location with. Defaults to BaseClasses.Location.
        :param item_type: Item class to create the event item with. Defaults to BaseClasses.Item.
        :param show_in_spoiler: Will be passed along to the created event Location's show_in_spoiler attribute.
        :return: The created Event Item
        """
        if location_type is None:
            location_type = Location

        if item_name is None:
            item_name = location_name

        if item_type is None:
            item_type = Item

        event_location = location_type(self.player, location_name, None, self)
        event_location.show_in_spoiler = show_in_spoiler
        if rule is not None:
            self.multiworld.worlds[self.player].set_rule(event_location, rule)

        event_item = item_type(item_name, ItemClassification.progression, None, self.player)

        event_location.place_locked_item(event_item)

        self.locations.append(event_location)

        return event_item

    def connect(self, connecting_region: Region, name: Optional[str] = None,
                rule: Optional[CollectionRule | Rule[Any]] = None) -> Entrance:
        """
        Connects this Region to another Region, placing the provided rule on the connection.

        :param connecting_region: Region object to connect to path is `self -> exiting_region`
        :param name: name of the connection being created
        :param rule: callable to determine access of this connection to go from self to the exiting_region"""
        exit_ = self.create_exit(name if name else f"{self.name} -> {connecting_region.name}")
        if rule is not None:
            self.multiworld.worlds[self.player].set_rule(exit_, rule)
        exit_.connect(connecting_region)
        return exit_

    def create_exit(self, name: str) -> Entrance:
        """
        Creates and returns an Entrance object as an exit of this region.

        :param name: name of the Entrance being created
        """
        exit_ = self.entrance_type(self.player, name, self)
        self.exits.append(exit_)
        return exit_

    def create_er_target(self, name: str) -> Entrance:
        """
        Creates and returns an Entrance object as an entrance to this region

        :param name: name of the Entrance being created
        """
        entrance = self.entrance_type(self.player, name)
        entrance.connect(self)
        return entrance

    def add_exits(self, exits: Iterable[str] | Mapping[str, str | None],
                  rules: Mapping[str, CollectionRule | Rule[Any]] | None = None) -> List[Entrance]:
        """
        Connects current region to regions in exit dictionary. Passed region names must exist first.

        :param exits: exits from the region. format is {"connecting_region": "exit_name"}. if a non dict is provided,
                      created entrances will be named "self.name -> connecting_region"
        :param rules: rules for the exits from this region. format is {"connecting_region": rule}
        """
        if not isinstance(exits, Mapping):
            exits = dict.fromkeys(exits)
        return [
            self.connect(
                self.multiworld.get_region(connecting_region, self.player),
                name,
                rules[connecting_region] if rules and connecting_region in rules else None,
            )
            for connecting_region, name in exits.items()
        ]

    def __repr__(self):
        return self.multiworld.get_name_string_for_object(self) if self.multiworld else f'{self.name} (Player {self.player})'


class LocationProgressType(IntEnum):
    DEFAULT = 1
    PRIORITY = 2
    EXCLUDED = 3


class Location:
    game: str = "Generic"
    player: int
    name: str
    address: Optional[int]
    parent_region: Optional[Region]
    locked: bool = False
    show_in_spoiler: bool = True
    progress_type: LocationProgressType = LocationProgressType.DEFAULT
    always_allow: Callable[[CollectionState, Item], bool] = staticmethod(lambda state, item: False)
    access_rule: CollectionRule = DEFAULT_COLLECTION_RULE
    item_rule: Callable[[Item], bool] = staticmethod(lambda item: True)
    item: Optional[Item] = None

    def __init__(self, player: int, name: str = '', address: Optional[int] = None, parent: Optional[Region] = None):
        self.player = player
        self.name = name
        self.address = address
        self.parent_region = parent

    def can_fill(self, state: CollectionState, item: Item, check_access: bool = True) -> bool:
        return ((
            self.always_allow(state, item)
            and item.name not in state.multiworld.worlds[item.player].options.non_local_items
        ) or (
            (self.progress_type != LocationProgressType.EXCLUDED or not (item.advancement or item.useful))
            and self.item_rule(item)
            and (not check_access or self.can_reach(state))
        ))

    def can_reach(self, state: CollectionState) -> bool:
        # Region.can_reach is just a cache lookup, so placing it first for faster abort on average
        assert self.parent_region, f"called can_reach on a Location \"{self}\" with no parent_region"
        return self.parent_region.can_reach(state) and self.access_rule(state)

    def place_locked_item(self, item: Item):
        if self.item:
            raise Exception(f"Location {self} already filled.")
        self.item = item
        item.location = self
        self.locked = True

    def __repr__(self):
        multiworld = self.parent_region.multiworld if self.parent_region and self.parent_region.multiworld else None
        return multiworld.get_name_string_for_object(self) if multiworld else f'{self.name} (Player {self.player})'

    def __lt__(self, other: Location):
        return (self.player, self.name) < (other.player, other.name)

    @property
    def advancement(self) -> bool:
        return self.item is not None and self.item.advancement

    @property
    def is_event(self) -> bool:
        """Returns True if the address of this location is None, denoting it is an Event Location."""
        return self.address is None

    @property
    def native_item(self) -> bool:
        """Returns True if the item in this location matches game."""
        return self.item is not None and self.item.game == self.game

    @property
    def hint_text(self) -> str:
        return "at " + self.name.replace("_", " ").replace("-", " ")


class ItemClassification(IntFlag):
    filler = 0b00000
    """ aka trash, as in filler items like ammo, currency etc """

    progression = 0b00001
    """ Item that is logically relevant.
    Protects this item from being placed on excluded or unreachable locations. """

    useful = 0b00010
    """ Item that is especially useful.
    Protects this item from being placed on excluded or unreachable locations.
    When combined with another flag like "progression", it means "an especially useful progression item". """

    trap = 0b00100
    """ Item that is detrimental in some way. """

    skip_balancing = 0b01000
    """ should technically never occur on its own
    Item that is logically relevant, but progression balancing should not touch.

    Possible reasons for why an item should not be pulled ahead by progression balancing:
    1. This item is quite insignificant, so pulling it earlier doesn't help (currency/etc.)
    2. It is important for the player experience that this item is evenly distributed in the seed (e.g. goal items) """

    deprioritized = 0b10000
    """ Should technically never occur on its own.
    Will not be considered for priority locations,
    unless Priority Locations Fill runs out of regular progression items before filling all priority locations.

    Should be used for items that would feel bad for the player to find on a priority location.
    Usually, these are items that are plentiful or insignificant. """

    progression_deprioritized_skip_balancing = 0b11001
    """ Since a common case of both skip_balancing and deprioritized is "insignificant progression",
    these items often want both flags. """

    progression_skip_balancing = 0b01001  # only progression gets balanced
    progression_deprioritized = 0b10001  # only progression can be placed during priority fill

    def as_flag(self) -> int:
        """As Network API flag int."""
        return int(self & 0b00111)


class Item:
    game: str = "Generic"
    __slots__ = ("name", "classification", "code", "player", "location")
    name: str
    classification: ItemClassification
    code: Optional[int]
    """an item with code None is called an Event, and does not get written to multidata"""
    player: int
    location: Optional[Location]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        self.name = name
        self.classification = classification
        self.player = player
        self.code = code
        self.location = None

    @property
    def hint_text(self) -> str:
        return getattr(self, "_hint_text", self.name.replace("_", " ").replace("-", " "))

    @property
    def pedestal_hint_text(self) -> str:
        return getattr(self, "_pedestal_hint_text", self.name.replace("_", " ").replace("-", " "))

    @property
    def advancement(self) -> bool:
        return ItemClassification.progression in self.classification

    @property
    def skip_in_prog_balancing(self) -> bool:
        return ItemClassification.progression_skip_balancing in self.classification

    @property
    def useful(self) -> bool:
        return ItemClassification.useful in self.classification

    @property
    def trap(self) -> bool:
        return ItemClassification.trap in self.classification

    @property
    def deprioritized(self) -> bool:
        return ItemClassification.deprioritized in self.classification

    @property
    def filler(self) -> bool:
        return not (self.advancement or self.useful or self.trap)

    @property
    def excludable(self) -> bool:
        return not (self.advancement or self.useful)

    @property
    def flags(self) -> int:
        return self.classification.as_flag()

    @property
    def is_event(self) -> bool:
        return self.code is None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name and self.player == other.player

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        if other.player != self.player:
            return other.player < self.player
        return self.name < other.name

    def __hash__(self) -> int:
        return hash((self.name, self.player))

    def __repr__(self) -> str:
        if self.location and self.location.parent_region and self.location.parent_region.multiworld:
            return self.location.parent_region.multiworld.get_name_string_for_object(self)
        return f"{self.name} (Player {self.player})"


class EntranceInfo(TypedDict, total=False):
    player: int
    entrance: str
    exit: str
    direction: str


class Spoiler:
    multiworld: MultiWorld
    hashes: Dict[int, str]
    entrances: Dict[Tuple[str, str, int], EntranceInfo]
    playthrough: Dict[str, Union[List[str], Dict[str, str]]]  # sphere "0" is list, others are dict
    unreachables: Set[Location]
    paths: Dict[str, List[Union[Tuple[str, str], Tuple[str, None]]]]  # last step takes no further exits

    def __init__(self, multiworld: MultiWorld) -> None:
        self.multiworld = multiworld
        self.hashes = {}
        self.entrances = {}
        self.playthrough = {}
        self.unreachables = set()
        self.paths = {}

    def set_entrance(self, entrance: str, exit_: str, direction: str, player: int) -> None:
        if self.multiworld.players == 1:
            self.entrances[(entrance, direction, player)] = \
                {"entrance": entrance, "exit": exit_, "direction": direction}
        else:
            self.entrances[(entrance, direction, player)] = \
                {"player": player, "entrance": entrance, "exit": exit_, "direction": direction}

    def create_playthrough(self, create_paths: bool = True) -> None:
        """Destructive to the multiworld while it is run, damage gets repaired afterwards."""
        from itertools import chain
        # get locations containing progress items
        multiworld = self.multiworld
        prog_locations = {location for location in multiworld.get_filled_locations() if location.item.advancement}
        state_cache: List[Optional[CollectionState]] = [None]
        collection_spheres: List[Set[Location]] = []
        state = CollectionState(multiworld)
        sphere_candidates = set(prog_locations)
        logging.debug('Building up collection spheres.')
        while sphere_candidates:

            # build up spheres of collection radius.
            # Everything in each sphere is independent from each other in dependencies and only depends on lower spheres

            sphere = {location for location in sphere_candidates if state.can_reach(location)}

            for location in sphere:
                state.collect(location.item, True, location)

            sphere_candidates -= sphere
            collection_spheres.append(sphere)
            state_cache.append(state.copy())

            logging.debug('Calculated sphere %i, containing %i of %i progress items.', len(collection_spheres),
                          len(sphere),
                          len(prog_locations))
            if not sphere:
                logging.debug('The following items could not be reached: %s', ['%s (Player %d) at %s (Player %d)' % (
                    location.item.name, location.item.player, location.name, location.player) for location in
                                                                               sphere_candidates])
                if not multiworld.has_beaten_game(state):
                    raise RuntimeError("During playthrough generation, the game was determined to be unbeatable. "
                                       "Something went terribly wrong here. "
                                       f"Unreachable progression items: {sphere_candidates}")
                else:
                    self.unreachables = sphere_candidates
                    break

        # in the second phase, we cull each sphere such that the game is still beatable,
        # reducing each range of influence to the bare minimum required inside it
        required_locations = {location for sphere in collection_spheres for location in sphere}
        for num, sphere in reversed(tuple(enumerate(collection_spheres))):
            to_delete: Set[Location] = set()
            for location in sphere:
                # we remove the location from required_locations to sweep from, and check if the game is still beatable
                logging.debug('Checking if %s (Player %d) is required to beat the game.', location.item.name,
                              location.item.player)
                required_locations.remove(location)
                if multiworld.can_beat_game(state_cache[num], required_locations):
                    to_delete.add(location)
                else:
                    # still required, got to keep it around
                    required_locations.add(location)

            # cull entries in spheres for spoiler walkthrough at end
            sphere -= to_delete

        # second phase, sphere 0
        removed_precollected: List[Item] = []

        for precollected_items in multiworld.precollected_items.values():
            # The list of items is mutated by removing one item at a time to determine if each item is required to beat
            # the game, and re-adding that item if it was required, so a copy needs to be made before iterating.
            for item in precollected_items.copy():
                if not item.advancement:
                    continue
                logging.debug('Checking if %s (Player %d) is required to beat the game.', item.name, item.player)
                precollected_items.remove(item)
                multiworld.state.remove(item)
                if not multiworld.can_beat_game(multiworld.state, required_locations):
                    # Add the item back into `precollected_items` and collect it into `multiworld.state`.
                    multiworld.push_precollected(item)
                else:
                    removed_precollected.append(item)

        # we are now down to just the required progress items in collection_spheres. Unfortunately
        # the previous pruning stage could potentially have made certain items dependant on others
        # in the same or later sphere (because the location had 2 ways to access but the item originally
        # used to access it was deemed not required.) So we need to do one final sphere collection pass
        # to build up the correct spheres

        required_locations = {item for sphere in collection_spheres for item in sphere}
        state = CollectionState(multiworld)
        collection_spheres = []
        while required_locations:
            sphere = set(filter(state.can_reach, required_locations))

            for location in sphere:
                state.collect(location.item, True, location)

            collection_spheres.append(sphere)

            logging.debug('Calculated final sphere %i, containing %i of %i progress items.', len(collection_spheres),
                          len(sphere), len(required_locations))

            required_locations -= sphere
            if not sphere:
                raise RuntimeError(f'Not all required items reachable. Unreachable locations: {required_locations}')

        # we can finally output our playthrough
        self.playthrough = {"0": sorted([self.multiworld.get_name_string_for_object(item) for item in
                                         chain.from_iterable(multiworld.precollected_items.values())
                                         if item.advancement])}

        for i, sphere in enumerate(collection_spheres):
            self.playthrough[str(i + 1)] = {
                str(location): str(location.item) for location in sorted(sphere)}
        if create_paths:
            self.create_paths(state, collection_spheres)

        # repair the multiworld again
        for item in removed_precollected:
            multiworld.push_precollected(item)

    def create_playthrough_sphere_fulfillment(self, create_paths: bool = True) -> None:
        """
        Wrapper for sphere_fulfillment that logs timing and falls back to default on failure.
        """
        import time
        try:
            t1 = time.time()
            self.sphere_fulfillment(create_paths)
            t2 = time.time()
            logging.info(f"sphere fulfillment completed in {t2 - t1:.2f} seconds")
        except Exception:
            logging.exception("sphere fulfillment failed; falling back to default")
            self.create_playthrough(create_paths)

    def sphere_fulfillment(self, create_paths: bool = True) -> None:
        """
        the main angle of this variation is an acknowledgement that can_beat_game, sweep_for_advancements, and
        update_reachable_regions are expensive operations to run. the first two can be avoided by ensuring
        continuity from sphere 0 to each goal manually. urr can't be avoided, but it is most efficient
        if you keep it player scoped. states are also most efficient when used incrementally, and copying a state
        is usually expensive, but if you keep it player scoped and only copy the needed players containers without
        mutating the others, you can have snapshots with o(n) complexity.
        """
        from itertools import chain
        multiworld = self.multiworld
        candidates = {location for location in multiworld.get_filled_locations() if location.item.advancement}
        start_state = CollectionState(multiworld)
        player_ids = multiworld.player_ids
        # spheres partitioned by recepient player for frontier search
        spheres: list[dict[int, list[Location]]] = []
        # snapshots of each sphere for regression without rebuilding the state
        sphere_snapshots: list[CollectionState] = []
        # which goals are still unfound, to not recheck found goals
        goals_unfound = set(player_ids)
        tally = Counter()

        # vips are goals and locations that are the found prerequisites for other vips. to maintain reachability across
        # the whole set and ensure the game is beatable. vips must all be met each sphere and pass.
        seed_vips = defaultdict(lambda: defaultdict(set))
        goal_spheres = defaultdict(int)

        # wrapper for goals and locations to check if the state fulfills the condition for either.
        # goals are just another condition that needs to be fulfilled each sphere/pass,
        # and being able to reorder when the goal is searched allows more variance
        def is_met(target: int | Location, q_state: CollectionState) -> bool:
            if isinstance(target, int):
                return multiworld.has_beaten_game(q_state, target)
            return q_state.can_reach(target)
        # player for a location or goal
        def owner(target: int | Location) -> int | str:
            if target in global_locations:
                return "global"
            return target if isinstance(target, int) else target.player
        # key for sorting locations for determinism
        def loc_key(target: int | Location) -> tuple[int, str, int, str]:
            if isinstance(target, int): 
                return (target, "", target, "")
            return (target.item.player, target.item.name, target.player, target.name)
        # bulk check reachability of several locations and optionally provide anything collected/not
        def bulk_is_met(
            locations: Iterable[int | Location],
            state: CollectionState,
            unmet_items: list[int | Location] | None = None,
            met_items: list[int | Location] | None = None,
        ) -> bool:
            result = True
            locations = list(locations)
            if unmet_items is not None:
                unmet_items.clear()
            if met_items is not None:
                met_items.clear()
            for location in locations:
                if is_met(location, state):
                    if met_items is not None:
                        met_items.append(location)
                    continue
                result = False
                if unmet_items is not None:
                    unmet_items.append(location)
            return result
        # a simple utility to avoid having to write loops
        def bulk_collect(
            to_collect: Iterable[Any],
            state: CollectionState,
            sphere: dict[int, list[Location]] | None = None,
        ) -> set[int]:
            players_collected = set()
            if isinstance(to_collect, dict):
                for locations in to_collect.values():
                    players_collected.update(bulk_collect(locations, state, sphere))
            else:
                for location in to_collect:
                    if isinstance(location, int):
                        continue
                    if location in state.locations_checked:
                        continue
                    state.collect(location.item, True, location)
                    players_collected.add(location.item.player)
                    if sphere is None:
                        continue
                    sphere[location.item.player].remove(location)
                return players_collected
            return players_collected
        # like binary search, but for all targets at once, still maintaining the player item-location relationship
        # but checking in bulk saves operations and eliminates some order problems
        def bulk_binary_search(
            state: CollectionState,
            locations: list[Location],
            targets: list[int | Location],
            player: int | str,
            fungibles_promoted: set[tuple[int, str]],
        ) -> list[Location]:
            low, high = 0, len(locations) - 1
            if player == "global":
                search_stack = [(state.copy(), low, targets.copy(), 0)]
            else:
                search_stack = [(self.player_state_copy(state, player), low, targets.copy(), 0)]
            results = []
            while search_stack:
                stack_state, low, stack_targets, synced = search_stack[-1]
                for result in results[synced:]:
                    stack_state.collect(result.item, True, result)
                search_stack[-1] = (stack_state, low, stack_targets, len(results))

                if bulk_is_met(stack_targets, stack_state, stack_targets):
                    search_stack.pop()
                    high = low - 1
                    continue
                if low > high:
                    raise RuntimeError("targets unreachable after frontier exhausted")
                stack_targets = stack_targets.copy()
                mid = (low + high) // 2
                if player == "global":
                    probe_state = stack_state.copy()
                else:
                    probe_state = self.player_state_copy(stack_state, player)
                for i in range(low, mid + 1):
                    probe_state.collect(locations[i].item, True, locations[i])
                if bulk_is_met(stack_targets, probe_state, stack_targets):
                    if (low == mid):
                        results.append(locations[mid])
                        if (locations[mid].item.player, locations[mid].item.name) in fungibles:
                            fungibles_promoted.add((locations[mid].item.player, locations[mid].item.name))
                            item_name = locations[mid].item.name
                            while mid > 0 and locations[mid - 1].item.name == item_name:
                                results.append(locations[mid - 1])
                                mid -= 1
                        high = mid - 1
                    else:
                        high = mid
                else:
                    search_stack.append((probe_state, mid + 1, stack_targets, len(results)))
                    continue
            return results

        # sphere building loop. collect items in waves as they become available and populate containers as we go
        while goals_unfound:
            if not candidates:
                raise RuntimeError("No more candidates but still goals unfound")
            # snapshots represent the lower sphere base that stays consistent for the search, so it's taken before the
            # sphere is processed
            sphere_snapshots.append(start_state.copy())
            sphere = defaultdict(list)
            reached = [location for location in candidates if start_state.can_reach(location)]
            if not reached:
                raise RuntimeError(
                    f"goals_unfound with no remaining reachable advancments: {goals_unfound}\n game unbeatable."
                )
            counts = Counter((location.item.player, location.item.name) for location in reached)
            reached.sort(key=lambda location: (counts[location.item.player, location.item.name], loc_key(location)))
            tally.update(counts)
            for location in reached:
                sphere[location.item.player].append(location)
                start_state.collect(location.item, True, location)
            candidates.difference_update(reached)
            spheres.append(sphere)

            sphere_id = len(sphere_snapshots) - 1
            found_goals = {player_goal for player_goal in goals_unfound if is_met(player_goal, start_state)}
            for goal in found_goals:
                seed_vips[sphere_id + 1][goal].add(goal)
            for goal in found_goals:
                goal_spheres[goal] = sphere_id + 1
            goals_unfound -= found_goals

        # test if each of a player's items or goals (indexed by player id) can be met with just their own items, add
        # them to the global locations if not.
        global_locations = set()
        for player in player_ids:
            state = CollectionState(multiworld)
            goal_state = None
            for sphere in range(0, len(spheres)):
                locations = [
                    location for location in chain.from_iterable(spheres[sphere].values()) if location.player == player
                ]
                if goal_spheres[player] == sphere:
                    goal_state = state.copy()
                unmet = []
                bulk_is_met(locations, state, unmet)
                bulk_collect(spheres[sphere][player], state)
                global_locations.update(unmet)
            if goal_state is None:
                goal_state = state
            if not is_met(player, goal_state):
                global_locations.add(player)
                sphere = goal_spheres[player]
                seed_vips[sphere][player].discard(player)
                seed_vips[sphere]["global"].add(player)

        # fungibles are items for which a player has multiple of the same item. when promoted to vip, we know that all
        # copies in the sphere prefix, and all lower spheres are required to satisfy the prereq and don't need to be
        # found again.
        fungibles = {key for key, count in tally.items() if count > 1}
        # cascade_collect is an efficient sweep of reachable from a state that might not yet be collected
        def cascade_collect(
            to_check: dict[int, dict[int | str, set[int | Location]]],
            sphere_id: int,
            state1: CollectionState,
            state2: CollectionState | None = None,
            collected_set: set[Location] | None = None,
        ) -> dict[int, dict[int | str, set[int | Location]]]:
            unfulfilled = {
                sphere: remaining_by_player
                for sphere, player_dicts in to_check.items()
                if sphere > sphere_id
                and (remaining_by_player := {player: set(remaining)
                for player, remaining in player_dicts.items() if remaining})
            }
            changed_players = None
            while True:
                next_changed, progressed, emptied = set(), False, []
                for sphere, player_dicts in unfulfilled.items():
                    for player, remaining in player_dicts.items():
                        if not remaining or (changed_players is not None and player not in changed_players and
                            player != "global"):
                            continue
                        newly_met = []
                        bulk_is_met(remaining, state1, None, newly_met)
                        if not newly_met:
                            continue
                        remaining.difference_update(newly_met)
                        recipients = bulk_collect(newly_met, state1)
                        if collected_set is not None:
                            collected_set.update(newly_met)
                        if state2 is not None:
                            bulk_collect(newly_met, state2)
                        next_changed |= recipients
                        progressed = True
                        if not remaining:
                            emptied.append((sphere, player))
                for sphere, player in emptied:
                    player_dicts = unfulfilled[sphere]
                    player_dicts.pop(player, None)
                    if not player_dicts:
                        unfulfilled.pop(sphere, None)
                if not progressed:
                    break
                changed_players = next_changed
            return unfulfilled
        # we start by violating continuity and forcing all vips into the state to be used as possible prereqs
        # with bulk searches, we guaranteed don't overcollect, and it's very fast, but it can result in circular
        # dependencies so we do individual, order invariant probe searches to try to find the prereqs that locations
        # with circular dependencies need. then repeat until the bulk search doesn't leave circular dependencies and
        # prune any unnecessary circular prereqs
        def process_sphere_bulk_forced(
            sphere: dict[int, list[Location]],
            state: CollectionState,
            vips: dict[int, dict[int | str, set[int | Location]]],
            sphere_id: int,
            fungibles_promoted: set[tuple[int, str]],
        ):
            targets = defaultdict(list)
            forced_state = state.copy()
            prune_state = state.copy()
            for vip_sphere, sphere_dict in vips.items():
                if vip_sphere <= sphere_id:
                    continue
                for location in chain.from_iterable(sphere_dict.values()):
                    targets[owner(location)].append(location)
                    if not isinstance(location, int):
                        forced_state.collect(location.item, True, location)
            bulk_search_state = forced_state.copy()
            prospective_vips = defaultdict(list)
            stale_players = set(targets)
            final_flippers = set()
            while True:
                if targets.get("global", None) and "global" in stale_players:
                    bulk_search_state = forced_state.copy()
                    stale_players.discard("global")
                    global_sphere = list(chain.from_iterable(sphere.values()))
                    prospective_vips["global"] = bulk_binary_search(
                        bulk_search_state,
                        global_sphere,
                        targets["global"],
                        "global", set(fungibles_promoted)
                    )
                    bulk_collect(prospective_vips["global"], bulk_search_state)
                for player, player_targets in targets.items():
                    if player not in stale_players:
                        continue
                    prospective_vips[player] = bulk_binary_search(
                        bulk_search_state,
                        sphere.get(player, []),
                        player_targets,
                        player,
                        set(fungibles_promoted),
                    )
                    stale_players.remove(player)
                loop_state = state.copy()
                loop_sphere = {player: sphere_list.copy() for player, sphere_list in sphere.items()}
                bulk_collect(prospective_vips, loop_state, loop_sphere)
                unfulfilled = cascade_collect(vips, sphere_id, loop_state)
                if not unfulfilled:
                    break
                loop_frontier = loop_state.copy()
                bulk_collect(loop_sphere, loop_frontier)
                roots = defaultdict(set)
                potential_roots = []
                for locs in chain.from_iterable(sphere_locs.values() for sphere_locs in unfulfilled.values()):
                    met = []
                    bulk_is_met(locs, loop_frontier, None, met)
                    potential_roots.extend(met)
                if not potential_roots:
                    raise RuntimeError("unfulfilled vips remain unreachable from frontier")
                potential_roots = sorted(potential_roots, key=loc_key)
                while potential_roots:
                    root = potential_roots.pop()
                    root_state = loop_state.copy()
                    if owner(root) == "global":
                        root_sphere = list(chain.from_iterable(loop_sphere.values()))
                    else:
                        root_sphere = loop_sphere.get(owner(root), [])
                    flippers = bulk_binary_search(
                        root_state,
                        root_sphere,
                        [root],
                        owner(root),
                        set(fungibles_promoted)
                    )
                    roots[root] = set(flippers)
                    if not isinstance(root, int):
                        root_state.collect(root.item, True, root)
                    bulk_collect(flippers, root_state)
                    collected_set = set()
                    cascade_collect(unfulfilled, sphere_id, root_state, None, collected_set)
                    collected_set.discard(root)
                    potential_roots = [loc for loc in potential_roots if loc not in collected_set]
                    for location in collected_set:
                        roots.pop(location, None)
                loop_flippers = set().union(*roots.values())
                if not loop_flippers:
                    raise RuntimeError("sphere fulfillment unable to satisfy some required locations")
                bulk_collect(loop_flippers, forced_state, sphere)
                bulk_collect(loop_flippers, bulk_search_state)
                bulk_collect(loop_flippers, state)
                final_flippers.update(loop_flippers)
                if "global" in roots:
                    stale_players = set(targets)
                else:
                    stale_players.update(loc.item.player for loc in loop_flippers)
            final_flippers.update(prospective_vips["global"])
            prospective_vips.pop("global", None)
            if final_flippers:
                bulk_collect(prospective_vips, prune_state)
                residual = cascade_collect(vips, sphere_id, prune_state)
                for flipper in sorted(final_flippers, key=loc_key):
                    to_collect = final_flippers - {flipper}
                    test_state = prune_state.copy()
                    bulk_collect(to_collect, test_state)
                    unfulfilled = cascade_collect(residual, sphere_id, test_state)
                    if not unfulfilled:
                        final_flippers.discard(flipper)
            for location in chain.from_iterable(prospective_vips.values()):
                vips[sphere_id][owner(location)].add(location)
                if (location.item.player, location.item.name) in fungibles:
                    fungibles_promoted.add((location.item.player, location.item.name))
            for flipper in final_flippers:
                vips[sphere_id][owner(flipper)].add(flipper)
                if (flipper.item.player, flipper.item.name) in fungibles:
                    fungibles_promoted.add((flipper.item.player, flipper.item.name))

        def run_sphere_fulfillment() -> dict[int, dict[int | str, set[int | Location]]]:
            vips: dict[int, dict[int | str, set[int | Location]]] = defaultdict(lambda: defaultdict(set))
            for vip_sphere in seed_vips:
                for player in seed_vips[vip_sphere]:
                    vips[vip_sphere][player] = seed_vips[vip_sphere][player].copy()
            sphere_id = len(spheres) - 1
            fungibles_promoted = set()
            # regress through spheres finding a valid set of prerequisites for all goals and vips at each step
            while len(spheres) > 0:
                sphere = spheres.pop()
                base_state = sphere_snapshots.pop()
                for location in chain.from_iterable(sphere.values()):
                    if (location.item.player, location.item.name) not in fungibles_promoted:
                        continue
                    vips[sphere_id][owner(location)].add(location)
                bulk_collect(vips[sphere_id], base_state, sphere)
                process_sphere_bulk_forced(sphere, base_state, vips, sphere_id, fungibles_promoted)
                sphere_id -= 1
            return vips
        vip_list = run_sphere_fulfillment()


        # remove goals from vips to build the playthrough
        kept = [
            location for players in vip_list.values()
            for locations in players.values()
            for location in locations
            if not isinstance(location, int)
        ]
        if not multiworld.can_beat_game(CollectionState(multiworld), kept):
            raise RuntimeError("Playthrough failed to beat the game")
        # build the playthrough sphere by sphere, collecting items as they are reachable
        walk_state = CollectionState(multiworld)
        playthrough_spheres = []
        remaining = set(kept)
        while remaining:
            sphere = {location for location in remaining if walk_state.can_reach(location)}
            if not sphere:
                raise RuntimeError(f"Kept set not beatable; unreachable: {len(remaining)}")
            for location in sphere:
                walk_state.collect(location.item, True, location)
            playthrough_spheres.append(sphere)
            remaining -= sphere
        # start the playthrough with precollected items
        self.playthrough = {"0": sorted(
                multiworld.get_name_string_for_object(item)
                for item in chain.from_iterable(multiworld.precollected_items.values())
                if item.advancement
            )}
        # add playthrough spheres
        for i, sphere in enumerate(playthrough_spheres):
            self.playthrough[str(i + 1)] = {str(location): str(location.item) for location in sorted(sphere)}

        if create_paths:
            self.create_paths(walk_state, playthrough_spheres)

    @staticmethod
    def player_state_copy(input_state: CollectionState, player: int) -> CollectionState:
        """
        Creates a player-scoped copy of a state. It is intended for use cases where you do not need more than one
        player's entries and don't need shared containers.
        """
        import copy
        ret_state = CollectionState.__new__(CollectionState)
        for attr, val in input_state.__dict__.items():
            if isinstance(val, dict) and player in val:
                cp = getattr(val[player], "copy", None)
                setattr(ret_state, attr, {player: cp() if callable(cp) else copy.deepcopy(val[player])})
            elif isinstance(val, defaultdict):
                setattr(ret_state, attr, defaultdict(val.default_factory))
            elif callable(getattr(val, "clear", None)):
                setattr(ret_state, attr, type(val)())
            else:
                setattr(ret_state, attr, val)
        return ret_state


    def create_paths(self, state: CollectionState, collection_spheres: List[Set[Location]]) -> None:
        from itertools import zip_longest
        multiworld = self.multiworld

        def flist_to_iter(path_value: Optional[PathValue]) -> Iterator[str]:
            while path_value:
                region_or_entrance, path_value = path_value
                yield region_or_entrance

        def get_path(state: CollectionState, region: Region) -> List[Union[Tuple[str, str], Tuple[str, None]]]:
            reversed_path_as_flist: PathValue = state.path.get(region, (str(region), None))
            string_path_flat = reversed(list(map(str, flist_to_iter(reversed_path_as_flist))))
            # Now we combine the flat string list into (region, exit) pairs
            pathsiter = iter(string_path_flat)
            pathpairs = zip_longest(pathsiter, pathsiter)
            return list(pathpairs)

        self.paths = {}
        topology_worlds = (player for player in multiworld.player_ids if multiworld.worlds[player].topology_present)
        for player in topology_worlds:
            self.paths.update(
                {str(location): get_path(state, location.parent_region)
                 for sphere in collection_spheres for location in sphere
                 if location.player == player})
            if player in multiworld.get_game_players("A Link to the Past"):
                # If Pyramid Fairy Entrance needs to be reached, also path to Big Bomb Shop
                # Maybe move the big bomb over to the Event system instead?
                if any(exit_path == 'Pyramid Fairy' for path in self.paths.values()
                       for (_, exit_path) in path):
                    if multiworld.worlds[player].options.mode != 'inverted':
                        self.paths[str(multiworld.get_region('Big Bomb Shop', player))] = \
                            get_path(state, multiworld.get_region('Big Bomb Shop', player))
                    else:
                        self.paths[str(multiworld.get_region('Inverted Big Bomb Shop', player))] = \
                            get_path(state, multiworld.get_region('Inverted Big Bomb Shop', player))

    def to_file(self, filename: str) -> None:
        from itertools import chain
        from worlds import AutoWorld
        from Options import Visibility

        def write_option(option_key: str, option_obj: Options.AssembleOptions) -> None:
            res = getattr(self.multiworld.worlds[player].options, option_key)
            if res.visibility & Visibility.spoiler:
                display_name = getattr(option_obj, "display_name", option_key)
                outfile.write(f"{display_name + ':':33}{res.current_option_name}\n")

        with open(filename, 'w', encoding="utf-8-sig") as outfile:
            outfile.write(
                'Archipelago Version %s  -  Seed: %s\n\n' % (
                    Utils.__version__, self.multiworld.seed))
            outfile.write('Filling Algorithm:               %s\n' % self.multiworld.algorithm)
            outfile.write('Players:                         %d\n' % self.multiworld.players)
            if self.multiworld.players > 1:
                loc_count = len([loc for loc in self.multiworld.get_locations() if not loc.is_event])
                outfile.write('Total Location Count:            %d\n' % loc_count)
            outfile.write(f'Plando Options:                  {self.multiworld.plando_options}\n')
            AutoWorld.call_stage(self.multiworld, "write_spoiler_header", outfile)

            for player in range(1, self.multiworld.players + 1):
                if self.multiworld.players > 1:
                    outfile.write('\nPlayer %d: %s\n' % (player, self.multiworld.get_player_name(player)))
                outfile.write('Game:                            %s\n' % self.multiworld.game[player])

                loc_count = len([loc for loc in self.multiworld.get_locations(player) if not loc.is_event])
                outfile.write('Location Count:                  %d\n' % loc_count)

                for f_option, option in self.multiworld.worlds[player].options_dataclass.type_hints.items():
                    write_option(f_option, option)

                AutoWorld.call_single(self.multiworld, "write_spoiler_header", player, outfile)

            if self.entrances:
                outfile.write('\n\nEntrances:\n\n')
                outfile.write('\n'.join(['%s%s %s %s' % (f'{self.multiworld.get_player_name(entry["player"])}: '
                                                         if self.multiworld.players > 1 else '', entry['entrance'],
                                                         '<=>' if entry['direction'] == 'both' else
                                                         '<=' if entry['direction'] == 'exit' else '=>',
                                                         entry['exit']) for entry in self.entrances.values()]))

            AutoWorld.call_all(self.multiworld, "write_spoiler", outfile)

            precollected_items = [f"{item.name} ({self.multiworld.get_player_name(item.player)})"
                                  if self.multiworld.players > 1
                                  else item.name
                                  for item in chain.from_iterable(self.multiworld.precollected_items.values())]
            if precollected_items:
                outfile.write("\n\nStarting Items:\n\n")
                outfile.write("\n".join([item for item in precollected_items]))

            locations = [(str(location), str(location.item) if location.item is not None else "Nothing")
                         for location in self.multiworld.get_locations() if location.show_in_spoiler]
            outfile.write('\n\nLocations:\n\n')
            outfile.write('\n'.join(
                ['%s: %s' % (location, item) for location, item in locations]))

            outfile.write('\n\nPlaythrough:\n\n')
            outfile.write('\n'.join(['%s: {\n%s\n}' % (sphere_nr, '\n'.join(
                [f"  {location}: {item}" for (location, item) in sphere.items()] if isinstance(sphere, dict) else
                [f"  {item}" for item in sphere])) for (sphere_nr, sphere) in self.playthrough.items()]))
            if self.unreachables:
                outfile.write('\n\nUnreachable Progression Items:\n\n')
                outfile.write(
                    '\n'.join(['%s: %s' % (unreachable.item, unreachable)
                               for unreachable in sorted(self.unreachables)]))

            if self.paths:
                outfile.write('\n\nPaths:\n\n')
                path_listings: List[str] = []
                for location, path in sorted(self.paths.items()):
                    path_lines: List[str] = []
                    for region, exit in path:
                        if exit is not None:
                            path_lines.append("{} -> {}".format(region, exit))
                        else:
                            path_lines.append(region)
                    path_listings.append("{}\n        {}".format(location, "\n   =>   ".join(path_lines)))

                outfile.write('\n'.join(path_listings))
            AutoWorld.call_all(self.multiworld, "write_spoiler_end", outfile)


class Tutorial(NamedTuple):
    """Class to build website tutorial pages from a .md file in the world's /docs folder. Order is as follows.
    Name of the tutorial as it will appear on the site. Concise description covering what the guide will entail.
    Language the guide is written in. Name of the file ex 'setup_en.md'. Name of the link on the site; game name is
    filled automatically so 'setup/en' etc. Author or authors."""
    tutorial_name: str
    description: str
    language: str
    file_name: str
    link: str  # unused
    authors: List[str]


class PlandoOptions(IntFlag):
    none = 0b0000
    items = 0b0001
    connections = 0b0010
    texts = 0b0100
    bosses = 0b1000

    @classmethod
    def from_option_string(cls, option_string: str) -> PlandoOptions:
        result = cls(0)
        for part in option_string.split(","):
            part = part.strip().lower()
            if part:
                result = cls._handle_part(part, result)
        return result

    @classmethod
    def from_set(cls, option_set: Set[str]) -> PlandoOptions:
        result = cls(0)
        for part in option_set:
            result = cls._handle_part(part, result)
        return result

    @classmethod
    def _handle_part(cls, part: str, base: PlandoOptions) -> PlandoOptions:
        try:
            return base | cls[part]
        except Exception as e:
            raise KeyError(f"{part} is not a recognized name for a plando module. "
                           f"Known options: {', '.join(str(flag.name) for flag in cls)}") from e

    def __str__(self) -> str:
        if self.value:
            return ", ".join(str(flag.name) for flag in PlandoOptions if self.value & flag.value)
        return "None"


seeddigits = 20


def get_seed(seed: Optional[int] = None) -> int:
    if seed is None:
        random.seed(None)
        return random.randint(0, pow(10, seeddigits) - 1)
    return seed
