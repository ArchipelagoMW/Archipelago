import datetime
import collections
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, NamedTuple, Counter
from uuid import UUID
from email.utils import parsedate_to_datetime

from flask import make_response, render_template, request, Request, Response
from werkzeug.exceptions import abort

from MultiServer import Context, get_saving_second
from NetUtils import ClientStatus, Hint, NetworkItem, NetworkSlot, SlotType
from Utils import restricted_loads, KeyedDefaultDict
from . import app, cache
from .models import GameDataPackage, Room

# Multisave is currently updated, at most, every minute.
TRACKER_CACHE_TIMEOUT_IN_SECONDS = 60

_multiworld_trackers: Dict[str, Callable] = {}
_player_trackers: Dict[str, Callable] = {}

TeamPlayer = Tuple[int, int]
ItemMetadata = Tuple[int, int, int]


def _cache_results(func: Callable) -> Callable:
    """Stores the results of any computationally expensive methods after the initial call in TrackerData.
    If called again, returns the cached result instead, as results will not change for the lifetime of TrackerData.
    """
    def method_wrapper(self: "TrackerData", *args):
        cache_key = f"{func.__name__}{''.join(f'_[{arg.__repr__()}]' for arg in args)}"
        if cache_key in self._tracker_cache:
            return self._tracker_cache[cache_key]

        result = func(self, *args)
        self._tracker_cache[cache_key] = result
        return result

    return method_wrapper


@dataclass
class TrackerData:
    """A helper dataclass that is instantiated each time an HTTP request comes in for tracker data.

    Provides helper methods to lazily load necessary data that each tracker require and caches any results so any
    subsequent helper method calls do not need to recompute results during the lifetime of this instance.
    """
    room: Room
    _multidata: Dict[str, Any]
    _multisave: Dict[str, Any]
    _tracker_cache: Dict[str, Any]

    def __init__(self, room: Room):
        """Initialize a new RoomMultidata object for the current room."""
        self.room = room
        self._multidata = Context.decompress(room.seed.multidata)
        self._multisave = restricted_loads(room.multisave) if room.multisave else {}
        self._tracker_cache = {}

        self.item_name_to_id: Dict[str, Dict[str, int]] = {}
        self.location_name_to_id: Dict[str, Dict[str, int]] = {}

        # Generate inverse lookup tables from data package, useful for trackers.
        self.item_id_to_name: Dict[str, Dict[int, str]] = KeyedDefaultDict(lambda game_name: {
            game_name: KeyedDefaultDict(lambda code: f"Unknown Game {game_name} - Item (ID: {code})")
        })
        self.location_id_to_name: Dict[str, Dict[int, str]] = KeyedDefaultDict(lambda game_name: {
            game_name: KeyedDefaultDict(lambda code: f"Unknown Game {game_name} - Location (ID: {code})")
        })
        for game, game_package in self._multidata["datapackage"].items():
            game_package = restricted_loads(GameDataPackage.get(checksum=game_package["checksum"]).data)
            self.item_id_to_name[game] = KeyedDefaultDict(lambda code: f"Unknown Item (ID: {code})", {
                id: name for name, id in game_package["item_name_to_id"].items()})
            self.location_id_to_name[game] = KeyedDefaultDict(lambda code: f"Unknown Location (ID: {code})", {
                id: name for name, id in game_package["location_name_to_id"].items()})

            # Normal lookup tables as well.
            self.item_name_to_id[game] = game_package["item_name_to_id"]
            self.location_name_to_id[game] = game_package["location_name_to_id"]

    def get_seed_name(self) -> str:
        """Retrieves the seed name."""
        return self._multidata["seed_name"]

    def get_slot_data(self, player: int) -> Dict[str, Any]:
        """Retrieves the slot data for a given player."""
        return self._multidata["slot_data"][player]

    def get_slot_info(self, player: int) -> NetworkSlot:
        """Retrieves the NetworkSlot data for a given player."""
        return self._multidata["slot_info"][player]

    def get_player_name(self, player: int) -> str:
        """Retrieves the slot name for a given player."""
        return self.get_slot_info(player).name

    def get_player_game(self, player: int) -> str:
        """Retrieves the game for a given player."""
        return self.get_slot_info(player).game

    def get_player_locations(self, player: int) -> Dict[int, ItemMetadata]:
        """Retrieves all locations with their containing item's metadata for a given player."""
        return self._multidata["locations"][player]

    def get_player_starting_inventory(self, player: int) -> List[int]:
        """Retrieves a list of all item codes a given slot starts with."""
        return self._multidata["precollected_items"][player]

    def get_player_checked_locations(self, team: int, player: int) -> Set[int]:
        """Retrieves the set of all locations marked complete by this player."""
        return self._multisave.get("location_checks", {}).get((team, player), set())

    @_cache_results
    def get_player_missing_locations(self, team: int, player: int) -> Set[int]:
        """Retrieves the set of all locations not marked complete by this player."""
        return set(self.get_player_locations(player)) - self.get_player_checked_locations(team, player)

    def get_player_received_items(self, team: int, player: int) -> List[NetworkItem]:
        """Returns all items received to this player in order of received."""
        return self._multisave.get("received_items", {}).get((team, player, True), [])

    @_cache_results
    def get_player_inventory_counts(self, team: int, player: int) -> collections.Counter:
        """Retrieves a dictionary of all items received by their id and their received count."""
        received_items = self.get_player_received_items(team, player)
        starting_items = self.get_player_starting_inventory(player)
        inventory = collections.Counter()
        for item in received_items:
            inventory[item.item] += 1
        for item in starting_items:
            inventory[item] += 1

        return inventory

    @_cache_results
    def get_player_hints(self, team: int, player: int) -> Set[Hint]:
        """Retrieves a set of all hints relevant for a particular player."""
        return self._multisave.get("hints", {}).get((team, player), set())

    @_cache_results
    def get_player_last_activity(self, team: int, player: int) -> Optional[datetime.timedelta]:
        """Retrieves the relative timedelta for when a particular player was last active.
        Returns None if no activity was ever recorded.
        """
        return self.get_room_last_activity().get((team, player), None)

    def get_player_client_status(self, team: int, player: int) -> ClientStatus:
        """Retrieves the ClientStatus of a particular player."""
        return self._multisave.get("client_game_state", {}).get((team, player), ClientStatus.CLIENT_UNKNOWN)

    def get_player_alias(self, team: int, player: int) -> Optional[str]:
        """Returns the alias of a particular player, if any."""
        return self._multisave.get("name_aliases", {}).get((team, player), None)

    @_cache_results
    def get_team_completed_worlds_count(self) -> Dict[int, int]:
        """Retrieves a dictionary of number of completed worlds per team."""
        return {
            team: sum(
                self.get_player_client_status(team, player) == ClientStatus.CLIENT_GOAL for player in players
            ) for team, players in self.get_all_players().items()
        }

    @_cache_results
    def get_team_hints(self) -> Dict[int, Set[Hint]]:
        """Retrieves a dictionary of all hints per team."""
        hints = {}
        for team, players in self.get_all_slots().items():
            hints[team] = set()
            for player in players:
                hints[team] |= self.get_player_hints(team, player)

        return hints

    @_cache_results
    def get_team_locations_total_count(self) -> Dict[int, int]:
        """Retrieves a dictionary of total player locations each team has."""
        return {
            team: sum(len(self.get_player_locations(player)) for player in players)
            for team, players in self.get_all_players().items()
        }

    @_cache_results
    def get_team_locations_checked_count(self) -> Dict[int, int]:
        """Retrieves a dictionary of checked player locations each team has."""
        return {
            team: sum(len(self.get_player_checked_locations(team, player)) for player in players)
            for team, players in self.get_all_players().items()
        }

    # TODO: Change this method to properly build for each team once teams are properly implemented, as they don't
    #       currently exist in multidata to easily look up, so these are all assuming only 1 team: Team #0
    @_cache_results
    def get_all_slots(self) -> Dict[int, List[int]]:
        """Retrieves a dictionary of all players ids on each team."""
        return {
            0: [
                player for player, slot_info in self._multidata["slot_info"].items()
            ]
        }

    # TODO: Change this method to properly build for each team once teams are properly implemented, as they don't
    #       currently exist in multidata to easily look up, so these are all assuming only 1 team: Team #0
    @_cache_results
    def get_all_players(self) -> Dict[int, List[int]]:
        """Retrieves a dictionary of all player slot-type players ids on each team."""
        return {
            0: [
                player for player, slot_info in self._multidata["slot_info"].items()
                if self.get_slot_info(player).type == SlotType.player
            ]
        }

    @_cache_results
    def get_room_saving_second(self) -> int:
        """Retrieves the saving second value for this seed.

        Useful for knowing when the multisave gets updated so trackers can attempt to update.
        """
        return get_saving_second(self.get_seed_name())

    @_cache_results
    def get_room_locations(self) -> Dict[TeamPlayer, Dict[int, ItemMetadata]]:
        """Retrieves a dictionary of all locations and their associated item metadata per player."""
        return {
            (team, player): self.get_player_locations(player)
            for team, players in self.get_all_players().items() for player in players
        }

    @_cache_results
    def get_room_games(self) -> Dict[TeamPlayer, str]:
        """Retrieves a dictionary of games for each player."""
        return {
            (team, player): self.get_player_game(player)
            for team, players in self.get_all_slots().items() for player in players
        }

    @_cache_results
    def get_room_locations_complete(self) -> Dict[TeamPlayer, int]:
        """Retrieves a dictionary of all locations complete per player."""
        return {
            (team, player): len(self.get_player_checked_locations(team, player))
            for team, players in self.get_all_players().items() for player in players
        }

    @_cache_results
    def get_room_client_statuses(self) -> Dict[TeamPlayer, ClientStatus]:
        """Retrieves a dictionary of all ClientStatus values per player."""
        return {
            (team, player): self.get_player_client_status(team, player)
            for team, players in self.get_all_players().items() for player in players
        }

    @_cache_results
    def get_room_long_player_names(self) -> Dict[TeamPlayer, str]:
        """Retrieves a dictionary of names with aliases for each player."""
        long_player_names = {}
        for team, players in self.get_all_slots().items():
            for player in players:
                alias = self.get_player_alias(team, player)
                if alias:
                    long_player_names[team, player] = f"{alias} ({self.get_player_name(player)})"
                else:
                    long_player_names[team, player] = self.get_player_name(player)

        return long_player_names

    @_cache_results
    def get_room_last_activity(self) -> Dict[TeamPlayer, datetime.timedelta]:
        """Retrieves a dictionary of all players and the timedelta from now to their last activity.
        Does not include players who have no activity recorded.
        """
        last_activity: Dict[TeamPlayer, datetime.timedelta] = {}
        now = datetime.datetime.utcnow()
        for (team, player), timestamp in self._multisave.get("client_activity_timers", []):
            last_activity[team, player] = now - datetime.datetime.utcfromtimestamp(timestamp)

        return last_activity

    @_cache_results
    def get_room_videos(self) -> Dict[TeamPlayer, Tuple[str, str]]:
        """Retrieves a dictionary of any players who have video streaming enabled and their feeds.

        Only supported platforms are Twitch and YouTube.
        """
        video_feeds = {}
        for (team, player), video_data in self._multisave.get("video", []):
            video_feeds[team, player] = video_data

        return video_feeds

    @_cache_results
    def get_spheres(self) -> List[List[int]]:
        """ each sphere is { player: { location_id, ... } } """
        return self._multidata.get("spheres", [])


def _process_if_request_valid(incoming_request: Request, room: Optional[Room]) -> Optional[Response]:
    if not room:
        abort(404)

    if_modified_str: Optional[str] = incoming_request.headers.get("If-Modified-Since", None)
    if if_modified_str:
        if_modified = parsedate_to_datetime(if_modified_str)
        if if_modified.tzinfo is None:
            abort(400)  # standard requires "GMT" timezone
        # database may use datetime.utcnow(), which is timezone-naive. convert to timezone-aware.
        last_activity = room.last_activity
        if last_activity.tzinfo is None:
            last_activity = room.last_activity.replace(tzinfo=datetime.timezone.utc)
        # if_modified has less precision than last_activity, so we bring them to same precision
        if if_modified >= last_activity.replace(microsecond=0):
            return make_response("",  304)

    return None


@app.route("/tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>")
def get_player_tracker(tracker: UUID, tracked_team: int, tracked_player: int, generic: bool = False) -> Response:
    key = f"{tracker}_{tracked_team}_{tracked_player}_{generic}"
    response: Optional[Response] = cache.get(key)
    if response:
        return response

    # Room must exist.
    room = Room.get(tracker=tracker)

    response = _process_if_request_valid(request, room)
    if response:
        return response

    timeout, last_modified, tracker_page = get_timeout_and_player_tracker(room, tracked_team, tracked_player, generic)
    response = make_response(tracker_page)
    response.last_modified = last_modified
    cache.set(key, response, timeout)
    return response


def get_timeout_and_player_tracker(room: Room, tracked_team: int, tracked_player: int, generic: bool)\
        -> Tuple[int, datetime.datetime, str]:
    tracker_data = TrackerData(room)

    # Load and render the game-specific player tracker, or fallback to generic tracker if none exists.
    game_specific_tracker = _player_trackers.get(tracker_data.get_player_game(tracked_player), None)
    if game_specific_tracker and not generic:
        tracker = game_specific_tracker(tracker_data, tracked_team, tracked_player)
    else:
        tracker = render_generic_tracker(tracker_data, tracked_team, tracked_player)

    return ((tracker_data.get_room_saving_second() - datetime.datetime.now().second)
            % TRACKER_CACHE_TIMEOUT_IN_SECONDS or TRACKER_CACHE_TIMEOUT_IN_SECONDS, room.last_activity, tracker)


@app.route("/generic_tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>")
def get_generic_game_tracker(tracker: UUID, tracked_team: int, tracked_player: int) -> Response:
    return get_player_tracker(tracker, tracked_team, tracked_player, True)


@app.route("/tracker/<suuid:tracker>", defaults={"game": "Generic"})
@app.route("/tracker/<suuid:tracker>/<game>")
def get_multiworld_tracker(tracker: UUID, game: str) -> Response:
    key = f"{tracker}_{game}"
    response: Optional[Response] = cache.get(key)
    if response:
        return response

    # Room must exist.
    room = Room.get(tracker=tracker)

    response = _process_if_request_valid(request, room)
    if response:
        return response

    timeout, last_modified, tracker_page = get_timeout_and_multiworld_tracker(room, game)
    response = make_response(tracker_page)
    response.last_modified = last_modified
    cache.set(key, response, timeout)
    return response


def get_timeout_and_multiworld_tracker(room: Room, game: str)\
        -> Tuple[int, datetime.datetime, str]:
    tracker_data = TrackerData(room)
    enabled_trackers = list(get_enabled_multiworld_trackers(room).keys())
    if game in _multiworld_trackers:
        tracker = _multiworld_trackers[game](tracker_data, enabled_trackers)
    else:
        tracker = render_generic_multiworld_tracker(tracker_data, enabled_trackers)

    return ((tracker_data.get_room_saving_second() - datetime.datetime.now().second)
            % TRACKER_CACHE_TIMEOUT_IN_SECONDS or TRACKER_CACHE_TIMEOUT_IN_SECONDS, room.last_activity, tracker)


def get_enabled_multiworld_trackers(room: Room) -> Dict[str, Callable]:
    # Render the multitracker for any games that exist in the current room if they are defined.
    enabled_trackers = {}
    for game_name, endpoint in _multiworld_trackers.items():
        if any(slot.game == game_name for slot in room.seed.slots):
            enabled_trackers[game_name] = endpoint

    # We resort the tracker to have Generic first, then lexicographically each enabled game.
    return {
        "Generic": render_generic_multiworld_tracker,
        **{key: enabled_trackers[key] for key in sorted(enabled_trackers.keys())},
    }


def render_generic_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
    game = tracker_data.get_player_game(player)

    received_items_in_order = {}
    starting_inventory = tracker_data.get_player_starting_inventory(player)
    for index, item in enumerate(starting_inventory):
        received_items_in_order[item] = index
    for index, network_item in enumerate(tracker_data.get_player_received_items(team, player),
                                         start=len(starting_inventory)):
        received_items_in_order[network_item.item] = index

    return render_template(
        template_name_or_list="genericTracker.html",
        game_specific_tracker=game in _player_trackers,
        room=tracker_data.room,
        get_slot_info=tracker_data.get_slot_info,
        team=team,
        player=player,
        player_name=tracker_data.get_room_long_player_names()[team, player],
        inventory=tracker_data.get_player_inventory_counts(team, player),
        locations=tracker_data.get_player_locations(player),
        checked_locations=tracker_data.get_player_checked_locations(team, player),
        received_items=received_items_in_order,
        saving_second=tracker_data.get_room_saving_second(),
        game=game,
        games=tracker_data.get_room_games(),
        player_names_with_alias=tracker_data.get_room_long_player_names(),
        location_id_to_name=tracker_data.location_id_to_name,
        item_id_to_name=tracker_data.item_id_to_name,
        hints=tracker_data.get_player_hints(team, player),
    )


def render_generic_multiworld_tracker(tracker_data: TrackerData, enabled_trackers: List[str]) -> str:
    return render_template(
        "multitracker.html",
        enabled_trackers=enabled_trackers,
        current_tracker="Generic",
        room=tracker_data.room,
        get_slot_info=tracker_data.get_slot_info,
        all_slots=tracker_data.get_all_slots(),
        room_players=tracker_data.get_all_players(),
        locations=tracker_data.get_room_locations(),
        locations_complete=tracker_data.get_room_locations_complete(),
        total_team_locations=tracker_data.get_team_locations_total_count(),
        total_team_locations_complete=tracker_data.get_team_locations_checked_count(),
        player_names_with_alias=tracker_data.get_room_long_player_names(),
        completed_worlds=tracker_data.get_team_completed_worlds_count(),
        games=tracker_data.get_room_games(),
        states=tracker_data.get_room_client_statuses(),
        hints=tracker_data.get_team_hints(),
        activity_timers=tracker_data.get_room_last_activity(),
        videos=tracker_data.get_room_videos(),
        item_id_to_name=tracker_data.item_id_to_name,
        location_id_to_name=tracker_data.location_id_to_name,
        saving_second=tracker_data.get_room_saving_second(),
    )


def render_generic_multiworld_sphere_tracker(tracker_data: TrackerData) -> str:
    return render_template(
        "multispheretracker.html",
        room=tracker_data.room,
        tracker_data=tracker_data,
    )


@app.route("/sphere_tracker/<suuid:tracker>")
@cache.memoize(timeout=TRACKER_CACHE_TIMEOUT_IN_SECONDS)
def get_multiworld_sphere_tracker(tracker: UUID):
    # Room must exist.
    room = Room.get(tracker=tracker)
    if not room:
        abort(404)

    tracker_data = TrackerData(room)
    return render_generic_multiworld_sphere_tracker(tracker_data)


# TODO: This is a temporary solution until a proper Tracker API can be implemented for tracker templates and data to
#       live in their respective world folders.

from worlds import network_data_package


if "Factorio" in network_data_package["games"]:
    def render_Factorio_multiworld_tracker(tracker_data: TrackerData, enabled_trackers: List[str]):
        inventories: Dict[TeamPlayer, collections.Counter[str]] = {
            (team, player): collections.Counter({
                tracker_data.item_id_to_name["Factorio"][item_id]: count
                for item_id, count in tracker_data.get_player_inventory_counts(team, player).items()
            }) for team, players in tracker_data.get_all_players().items() for player in players
            if tracker_data.get_player_game(player) == "Factorio"
        }

        return render_template(
            "multitracker__Factorio.html",
            enabled_trackers=enabled_trackers,
            current_tracker="Factorio",
            room=tracker_data.room,
            get_slot_info=tracker_data.get_slot_info,
            all_slots=tracker_data.get_all_slots(),
            room_players=tracker_data.get_all_players(),
            locations=tracker_data.get_room_locations(),
            locations_complete=tracker_data.get_room_locations_complete(),
            total_team_locations=tracker_data.get_team_locations_total_count(),
            total_team_locations_complete=tracker_data.get_team_locations_checked_count(),
            player_names_with_alias=tracker_data.get_room_long_player_names(),
            completed_worlds=tracker_data.get_team_completed_worlds_count(),
            games=tracker_data.get_room_games(),
            states=tracker_data.get_room_client_statuses(),
            hints=tracker_data.get_team_hints(),
            activity_timers=tracker_data.get_room_last_activity(),
            videos=tracker_data.get_room_videos(),
            item_id_to_name=tracker_data.item_id_to_name,
            location_id_to_name=tracker_data.location_id_to_name,
            inventories=inventories,
        )

    _multiworld_trackers["Factorio"] = render_Factorio_multiworld_tracker

if "A Link to the Past" in network_data_package["games"]:
    # Mapping from non-progressive item to progressive name and max level.
    non_progressive_items = {
        "Fighter Sword":  ("Progressive Sword",  1),
        "Master Sword":   ("Progressive Sword",  2),
        "Tempered Sword": ("Progressive Sword",  3),
        "Golden Sword":   ("Progressive Sword",  4),
        "Power Glove":    ("Progressive Glove",  1),
        "Titans Mitts":   ("Progressive Glove",  2),
        "Bow":            ("Progressive Bow",    1),
        "Silver Bow":     ("Progressive Bow",    2),
        "Blue Mail":      ("Progressive Mail",   1),
        "Red Mail":       ("Progressive Mail",   2),
        "Blue Shield":    ("Progressive Shield", 1),
        "Red Shield":     ("Progressive Shield", 2),
        "Mirror Shield":  ("Progressive Shield", 3),
    }

    progressive_item_max = {
        "Progressive Sword":  4,
        "Progressive Glove":  2,
        "Progressive Bow":    2,
        "Progressive Mail":   2,
        "Progressive Shield": 3,
    }

    bottle_items = [
        "Bottle",
        "Bottle (Bee)",
        "Bottle (Blue Potion)",
        "Bottle (Fairy)",
        "Bottle (Good Bee)",
        "Bottle (Green Potion)",
        "Bottle (Red Potion)",
    ]

    known_regions = [
        "Light World", "Dark World", "Hyrule Castle", "Agahnims Tower", "Eastern Palace", "Desert Palace",
        "Tower of Hera", "Palace of Darkness", "Swamp Palace", "Thieves Town", "Skull Woods", "Ice Palace",
        "Misery Mire", "Turtle Rock", "Ganons Tower"
    ]

    class RegionCounts(NamedTuple):
        total: int
        checked: int

    def prepare_inventories(team: int, player: int, inventory: Counter[str], tracker_data: TrackerData):
        for item, (prog_item, level) in non_progressive_items.items():
            if item in inventory:
                inventory[prog_item] = min(max(inventory[prog_item], level), progressive_item_max[prog_item])

        for bottle in bottle_items:
            inventory["Bottles"] = min(inventory["Bottles"] + inventory[bottle], 4)

        if "Progressive Bow (Alt)" in inventory:
            inventory["Progressive Bow"] += inventory["Progressive Bow (Alt)"]
            inventory["Progressive Bow"] = min(inventory["Progressive Bow"], progressive_item_max["Progressive Bow"])

        # Highlight 'bombs' if we received any bomb upgrades in bombless start.
        # In race mode, we'll just assume bombless start for simplicity.
        if tracker_data.get_slot_data(player).get("bombless_start", True):
            inventory["Bombs"] = sum(count for item, count in inventory.items() if item.startswith("Bomb Upgrade"))
        else:
            inventory["Bombs"] = 1

        # Triforce item if we meet goal.
        if tracker_data.get_room_client_statuses()[team, player] == ClientStatus.CLIENT_GOAL:
            inventory["Triforce"] = 1

    def render_ALinkToThePast_multiworld_tracker(tracker_data: TrackerData, enabled_trackers: List[str]):
        inventories: Dict[Tuple[int, int], Counter[str]] = {
            (team, player): collections.Counter({
                tracker_data.item_id_to_name["A Link to the Past"][code]: count
                for code, count in tracker_data.get_player_inventory_counts(team, player).items()
            })
            for team, players in tracker_data.get_all_players().items()
            for player in players if tracker_data.get_slot_info(player).game == "A Link to the Past"
        }

        # Translate non-progression items to progression items for tracker simplicity.
        for (team, player), inventory in inventories.items():
            prepare_inventories(team, player, inventory, tracker_data)

        regions: Dict[Tuple[int, int], Dict[str, RegionCounts]] = {
            (team, player): {
                region_name: RegionCounts(
                    total=len(tracker_data._multidata["checks_in_area"][player][region_name]),
                    checked=sum(
                        1 for location in tracker_data._multidata["checks_in_area"][player][region_name]
                        if location in tracker_data.get_player_checked_locations(team, player)
                    ),
                )
                for region_name in known_regions
            }
            for team, players in tracker_data.get_all_players().items()
            for player in players if tracker_data.get_slot_info(player).game == "A Link to the Past"
        }

        # Get a totals count.
        for player, player_regions in regions.items():
            total = 0
            checked = 0
            for region, region_counts in player_regions.items():
                total += region_counts.total
                checked += region_counts.checked
            regions[player]["Total"] = RegionCounts(total, checked)

        return render_template(
            "multitracker__ALinkToThePast.html",
            enabled_trackers=enabled_trackers,
            current_tracker="A Link to the Past",
            room=tracker_data.room,
            get_slot_info=tracker_data.get_slot_info,
            all_slots=tracker_data.get_all_slots(),
            room_players=tracker_data.get_all_players(),
            locations=tracker_data.get_room_locations(),
            locations_complete=tracker_data.get_room_locations_complete(),
            total_team_locations=tracker_data.get_team_locations_total_count(),
            total_team_locations_complete=tracker_data.get_team_locations_checked_count(),
            player_names_with_alias=tracker_data.get_room_long_player_names(),
            completed_worlds=tracker_data.get_team_completed_worlds_count(),
            games=tracker_data.get_room_games(),
            states=tracker_data.get_room_client_statuses(),
            hints=tracker_data.get_team_hints(),
            activity_timers=tracker_data.get_room_last_activity(),
            videos=tracker_data.get_room_videos(),
            item_id_to_name=tracker_data.item_id_to_name,
            location_id_to_name=tracker_data.location_id_to_name,
            inventories=inventories,
            regions=regions,
            known_regions=known_regions,
        )

    def render_ALinkToThePast_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        inventory = collections.Counter({
            tracker_data.item_id_to_name["A Link to the Past"][code]: count
            for code, count in tracker_data.get_player_inventory_counts(team, player).items()
        })

        # Translate non-progression items to progression items for tracker simplicity.
        prepare_inventories(team, player, inventory, tracker_data)

        regions = {
            region_name: {
                "checked": sum(
                    1 for location in tracker_data._multidata["checks_in_area"][player][region_name]
                    if location in tracker_data.get_player_checked_locations(team, player)
                ),
                "locations": [
                    (
                        tracker_data.location_id_to_name["A Link to the Past"][location],
                        location in tracker_data.get_player_checked_locations(team, player)
                    )
                    for location in tracker_data._multidata["checks_in_area"][player][region_name]
                ],
            }
            for region_name in known_regions
        }

        # Sort locations in regions by name
        for region in regions:
            regions[region]["locations"].sort()

        return render_template(
            template_name_or_list="tracker__ALinkToThePast.html",
            room=tracker_data.room,
            team=team,
            player=player,
            inventory=inventory,
            player_name=tracker_data.get_player_name(player),
            regions=regions,
            known_regions=known_regions,
        )

    _multiworld_trackers["A Link to the Past"] = render_ALinkToThePast_multiworld_tracker
    _player_trackers["A Link to the Past"] = render_ALinkToThePast_tracker

if "Ocarina of Time" in network_data_package["games"]:
    def render_OcarinaOfTime_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        icons = {
            "Fairy Ocarina":          "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/97/OoT_Fairy_Ocarina_Icon.png",
            "Ocarina of Time":        "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4e/OoT_Ocarina_of_Time_Icon.png",
            "Slingshot":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/32/OoT_Fairy_Slingshot_Icon.png",
            "Boomerang":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/d5/OoT_Boomerang_Icon.png",
            "Bottle":                 "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/fc/OoT_Bottle_Icon.png",
            "Rutos Letter":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/OoT_Letter_Icon.png",
            "Bombs":                  "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/11/OoT_Bomb_Icon.png",
            "Bombchus":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/36/OoT_Bombchu_Icon.png",
            "Lens of Truth":          "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/05/OoT_Lens_of_Truth_Icon.png",
            "Bow":                    "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/9a/OoT_Fairy_Bow_Icon.png",
            "Hookshot":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/77/OoT_Hookshot_Icon.png",
            "Longshot":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a4/OoT_Longshot_Icon.png",
            "Megaton Hammer":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/93/OoT_Megaton_Hammer_Icon.png",
            "Fire Arrows":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/1e/OoT_Fire_Arrow_Icon.png",
            "Ice Arrows":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3c/OoT_Ice_Arrow_Icon.png",
            "Light Arrows":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/76/OoT_Light_Arrow_Icon.png",
            "Dins Fire":              r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/d/da/OoT_Din%27s_Fire_Icon.png",
            "Farores Wind":           r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/7/7a/OoT_Farore%27s_Wind_Icon.png",
            "Nayrus Love":            r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/be/OoT_Nayru%27s_Love_Icon.png",
            "Kokiri Sword":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/5/53/OoT_Kokiri_Sword_Icon.png",
            "Biggoron Sword":         r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2e/OoT_Giant%27s_Knife_Icon.png",
            "Mirror Shield":          "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b0/OoT_Mirror_Shield_Icon_2.png",
            "Goron Bracelet":         r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b7/OoT_Goron%27s_Bracelet_Icon.png",
            "Silver Gauntlets":       "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/b/b9/OoT_Silver_Gauntlets_Icon.png",
            "Golden Gauntlets":       "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/6a/OoT_Golden_Gauntlets_Icon.png",
            "Goron Tunic":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/1/1c/OoT_Goron_Tunic_Icon.png",
            "Zora Tunic":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/2c/OoT_Zora_Tunic_Icon.png",
            "Silver Scale":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4e/OoT_Silver_Scale_Icon.png",
            "Gold Scale":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/95/OoT_Golden_Scale_Icon.png",
            "Iron Boots":             "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/34/OoT_Iron_Boots_Icon.png",
            "Hover Boots":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/22/OoT_Hover_Boots_Icon.png",
            "Adults Wallet":          r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f9/OoT_Adult%27s_Wallet_Icon.png",
            "Giants Wallet":          r"https://static.wikia.nocookie.net/zelda_gamepedia_en/images/8/87/OoT_Giant%27s_Wallet_Icon.png",
            "Small Magic":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/9f/OoT3D_Magic_Jar_Icon.png",
            "Large Magic":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/3/3e/OoT3D_Large_Magic_Jar_Icon.png",
            "Gerudo Membership Card": "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/4e/OoT_Gerudo_Token_Icon.png",
            "Gold Skulltula Token":   "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/47/OoT_Token_Icon.png",
            "Triforce Piece":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/0b/SS_Triforce_Piece_Icon.png",
            "Triforce":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/6/68/ALttP_Triforce_Title_Sprite.png",
            "Zeldas Lullaby":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
            "Eponas Song":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
            "Sarias Song":            "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
            "Suns Song":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
            "Song of Time":           "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
            "Song of Storms":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/2/21/Grey_Note.png",
            "Minuet of Forest":       "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e4/Green_Note.png",
            "Bolero of Fire":         "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/f/f0/Red_Note.png",
            "Serenade of Water":      "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/0/0f/Blue_Note.png",
            "Requiem of Spirit":      "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/a/a4/Orange_Note.png",
            "Nocturne of Shadow":     "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/97/Purple_Note.png",
            "Prelude of Light":       "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/9/90/Yellow_Note.png",
            "Small Key":              "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/e/e5/OoT_Small_Key_Icon.png",
            "Boss Key":               "https://static.wikia.nocookie.net/zelda_gamepedia_en/images/4/40/OoT_Boss_Key_Icon.png",
        }

        display_data = {}

        # Determine display for progressive items
        progressive_items = {
            "Progressive Hookshot":         66128,
            "Progressive Strength Upgrade": 66129,
            "Progressive Wallet":           66133,
            "Progressive Scale":            66134,
            "Magic Meter":                  66138,
            "Ocarina":                      66139,
        }

        progressive_names = {
            "Progressive Hookshot":         ["Hookshot", "Hookshot", "Longshot"],
            "Progressive Strength Upgrade": ["Goron Bracelet", "Goron Bracelet", "Silver Gauntlets",
                                             "Golden Gauntlets"],
            "Progressive Wallet":           ["Adults Wallet", "Adults Wallet", "Giants Wallet", "Giants Wallet"],
            "Progressive Scale":            ["Silver Scale", "Silver Scale", "Gold Scale"],
            "Magic Meter":                  ["Small Magic", "Small Magic", "Large Magic"],
            "Ocarina":                      ["Fairy Ocarina", "Fairy Ocarina", "Ocarina of Time"]
        }

        inventory = tracker_data.get_player_inventory_counts(team, player)
        for item_name, item_id in progressive_items.items():
            level = min(inventory[item_id], len(progressive_names[item_name]) - 1)
            display_name = progressive_names[item_name][level]
            if item_name.startswith("Progressive"):
                base_name = item_name.split(maxsplit=1)[1].lower().replace(" ", "_")
            else:
                base_name = item_name.lower().replace(" ", "_")
            display_data[base_name + "_url"] = icons[display_name]

            if base_name == "hookshot":
                display_data["hookshot_length"] = {0: "", 1: "H", 2: "L"}.get(level)
            if base_name == "wallet":
                display_data["wallet_size"] = {0: "99", 1: "200", 2: "500", 3: "999"}.get(level)

        # Determine display for bottles. Show letter if it's obtained, determine bottle count
        bottle_ids = [66015, 66020, 66021, 66140, 66141, 66142, 66143, 66144, 66145, 66146, 66147, 66148]
        display_data["bottle_count"] = min(sum(map(lambda item_id: inventory[item_id], bottle_ids)), 4)
        display_data["bottle_url"] = icons["Rutos Letter"] if inventory[66021] > 0 else icons["Bottle"]

        # Determine bombchu display
        display_data["has_bombchus"] = any(map(lambda item_id: inventory[item_id] > 0, [66003, 66106, 66107, 66137]))

        # Multi-items
        multi_items = {
            "Gold Skulltula Token": 66091,
            "Triforce Piece":       66202,
        }
        for item_name, item_id in multi_items.items():
            base_name = item_name.split()[-1].lower()
            display_data[base_name + "_count"] = inventory[item_id]

        # Gather dungeon locations
        area_id_ranges = {
            "Overworld":              ((67000, 67263), (67269, 67280), (67747, 68024), (68054, 68062)),
            "Deku Tree":              ((67281, 67303), (68063, 68077)),
            "Dodongo's Cavern":       ((67304, 67334), (68078, 68160)),
            "Jabu Jabu's Belly":      ((67335, 67359), (68161, 68188)),
            "Bottom of the Well":     ((67360, 67384), (68189, 68230)),
            "Forest Temple":          ((67385, 67420), (68231, 68281)),
            "Fire Temple":            ((67421, 67457), (68282, 68350)),
            "Water Temple":           ((67458, 67484), (68351, 68483)),
            "Shadow Temple":          ((67485, 67532), (68484, 68565)),
            "Spirit Temple":          ((67533, 67582), (68566, 68625)),
            "Ice Cavern":             ((67583, 67596), (68626, 68649)),
            "Gerudo Training Ground": ((67597, 67635), (68650, 68656)),
            "Thieves' Hideout":       ((67264, 67268), (68025, 68053)),
            "Ganon's Castle":         ((67636, 67673), (68657, 68705)),
        }

        def lookup_and_trim(id, area):
            full_name = tracker_data.location_id_to_name["Ocarina of Time"][id]
            if "Ganons Tower" in full_name:
                return full_name
            if area not in ["Overworld", "Thieves' Hideout"]:
                # trim dungeon name. leaves an extra space that doesn't display, or trims fully for DC/Jabu/GC
                return full_name[len(area):]
            return full_name

        locations = tracker_data.get_player_locations(player)
        checked_locations = tracker_data.get_player_checked_locations(team, player).intersection(set(locations))
        location_info = {}
        checks_done = {}
        checks_in_area = {}
        for area, ranges in area_id_ranges.items():
            location_info[area] = {}
            checks_done[area] = 0
            checks_in_area[area] = 0
            for r in ranges:
                min_id, max_id = r
                for id in range(min_id, max_id + 1):
                    if id in locations:
                        checked = id in checked_locations
                        location_info[area][lookup_and_trim(id, area)] = checked
                        checks_in_area[area] += 1
                        checks_done[area] += checked

        checks_done["Total"] = sum(checks_done.values())
        checks_in_area["Total"] = sum(checks_in_area.values())

        # Give skulltulas on non-tracked locations
        non_tracked_locations = tracker_data.get_player_checked_locations(team, player).difference(set(locations))
        for id in non_tracked_locations:
            if "GS" in lookup_and_trim(id, ""):
                display_data["token_count"] += 1

        oot_y = "✔"
        oot_x = "✕"

        # Gather small and boss key info
        small_key_counts = {
            "Forest Temple":          oot_y if inventory[66203] else inventory[66175],
            "Fire Temple":            oot_y if inventory[66204] else inventory[66176],
            "Water Temple":           oot_y if inventory[66205] else inventory[66177],
            "Spirit Temple":          oot_y if inventory[66206] else inventory[66178],
            "Shadow Temple":          oot_y if inventory[66207] else inventory[66179],
            "Bottom of the Well":     oot_y if inventory[66208] else inventory[66180],
            "Gerudo Training Ground": oot_y if inventory[66209] else inventory[66181],
            "Thieves' Hideout":       oot_y if inventory[66210] else inventory[66182],
            "Ganon's Castle":         oot_y if inventory[66211] else inventory[66183],
        }
        boss_key_counts = {
            "Forest Temple":  oot_y if inventory[66149] else oot_x,
            "Fire Temple":    oot_y if inventory[66150] else oot_x,
            "Water Temple":   oot_y if inventory[66151] else oot_x,
            "Spirit Temple":  oot_y if inventory[66152] else oot_x,
            "Shadow Temple":  oot_y if inventory[66153] else oot_x,
            "Ganon's Castle": oot_y if inventory[66154] else oot_x,
        }

        # Victory condition
        game_state = tracker_data.get_player_client_status(team, player)
        display_data["game_finished"] = game_state == 30

        lookup_any_item_id_to_name = tracker_data.item_id_to_name["Ocarina of Time"]
        return render_template(
            "tracker__OcarinaOfTime.html",
            inventory=inventory,
            player=player,
            team=team,
            room=tracker_data.room,
            player_name=tracker_data.get_player_name(player),
            icons=icons,
            acquired_items={lookup_any_item_id_to_name[id] for id, count in inventory.items() if count > 0},
            checks_done=checks_done, checks_in_area=checks_in_area, location_info=location_info,
            small_key_counts=small_key_counts,
            boss_key_counts=boss_key_counts,
            **display_data,
        )

    _player_trackers["Ocarina of Time"] = render_OcarinaOfTime_tracker

if "Timespinner" in network_data_package["games"]:
    def render_Timespinner_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        icons = {
            "Timespinner Wheel":   "https://timespinnerwiki.com/mediawiki/images/7/76/Timespinner_Wheel.png",
            "Timespinner Spindle": "https://timespinnerwiki.com/mediawiki/images/1/1a/Timespinner_Spindle.png",
            "Timespinner Gear 1":  "https://timespinnerwiki.com/mediawiki/images/3/3c/Timespinner_Gear_1.png",
            "Timespinner Gear 2":  "https://timespinnerwiki.com/mediawiki/images/e/e9/Timespinner_Gear_2.png",
            "Timespinner Gear 3":  "https://timespinnerwiki.com/mediawiki/images/2/22/Timespinner_Gear_3.png",
            "Talaria Attachment":  "https://timespinnerwiki.com/mediawiki/images/6/61/Talaria_Attachment.png",
            "Succubus Hairpin":    "https://timespinnerwiki.com/mediawiki/images/4/49/Succubus_Hairpin.png",
            "Lightwall":           "https://timespinnerwiki.com/mediawiki/images/0/03/Lightwall.png",
            "Celestial Sash":      "https://timespinnerwiki.com/mediawiki/images/f/f1/Celestial_Sash.png",
            "Twin Pyramid Key":    "https://timespinnerwiki.com/mediawiki/images/4/49/Twin_Pyramid_Key.png",
            "Security Keycard D":  "https://timespinnerwiki.com/mediawiki/images/1/1b/Security_Keycard_D.png",
            "Security Keycard C":  "https://timespinnerwiki.com/mediawiki/images/e/e5/Security_Keycard_C.png",
            "Security Keycard B":  "https://timespinnerwiki.com/mediawiki/images/f/f6/Security_Keycard_B.png",
            "Security Keycard A":  "https://timespinnerwiki.com/mediawiki/images/b/b9/Security_Keycard_A.png",
            "Library Keycard V":   "https://timespinnerwiki.com/mediawiki/images/5/50/Library_Keycard_V.png",
            "Tablet":              "https://timespinnerwiki.com/mediawiki/images/a/a0/Tablet.png",
            "Elevator Keycard":    "https://timespinnerwiki.com/mediawiki/images/5/55/Elevator_Keycard.png",
            "Oculus Ring":         "https://timespinnerwiki.com/mediawiki/images/8/8d/Oculus_Ring.png",
            "Water Mask":          "https://timespinnerwiki.com/mediawiki/images/0/04/Water_Mask.png",
            "Gas Mask":            "https://timespinnerwiki.com/mediawiki/images/2/2e/Gas_Mask.png",
            "Djinn Inferno":       "https://timespinnerwiki.com/mediawiki/images/f/f6/Djinn_Inferno.png",
            "Pyro Ring":           "https://timespinnerwiki.com/mediawiki/images/2/2c/Pyro_Ring.png",
            "Infernal Flames":     "https://timespinnerwiki.com/mediawiki/images/1/1f/Infernal_Flames.png",
            "Fire Orb":            "https://timespinnerwiki.com/mediawiki/images/3/3e/Fire_Orb.png",
            "Royal Ring":          "https://timespinnerwiki.com/mediawiki/images/f/f3/Royal_Ring.png",
            "Plasma Geyser":       "https://timespinnerwiki.com/mediawiki/images/1/12/Plasma_Geyser.png",
            "Plasma Orb":          "https://timespinnerwiki.com/mediawiki/images/4/44/Plasma_Orb.png",
            "Kobo":                "https://timespinnerwiki.com/mediawiki/images/c/c6/Familiar_Kobo.png",
            "Merchant Crow":       "https://timespinnerwiki.com/mediawiki/images/4/4e/Familiar_Crow.png",
            "Laser Access":        "https://timespinnerwiki.com/mediawiki/images/9/99/Historical_Documents.png",
            "Lab Glasses":         "https://timespinnerwiki.com/mediawiki/images/4/4a/Lab_Glasses.png",
            "Eye Orb":             "https://timespinnerwiki.com/mediawiki/images/a/a4/Eye_Orb.png",
            "Lab Coat":            "https://timespinnerwiki.com/mediawiki/images/5/51/Lab_Coat.png", 
            "Demon":               "https://timespinnerwiki.com/mediawiki/images/f/f8/Familiar_Demon.png",
            "Cube of Bodie":       "https://timespinnerwiki.com/mediawiki/images/1/14/Menu_Icon_Stats.png"
        }

        timespinner_location_ids = {
            "Present": list(range(1337000, 1337085)),
            "Past": list(range(1337086, 1337175)),
            "Ancient Pyramid": [
                1337236,
                1337246, 1337247, 1337248, 1337249]
        }

        slot_data = tracker_data.get_slot_data(player)
        if (slot_data["DownloadableItems"]):
            timespinner_location_ids["Present"] += [1337156, 1337157] + list(range(1337159, 1337170))
        if (slot_data["Cantoran"]):
            timespinner_location_ids["Past"].append(1337176)
        if (slot_data["LoreChecks"]):
            timespinner_location_ids["Present"] += list(range(1337177, 1337187))
            timespinner_location_ids["Past"] += list(range(1337188, 1337198))
        if (slot_data["GyreArchives"]):
            timespinner_location_ids["Ancient Pyramid"] += list(range(1337237, 1337245))
        if (slot_data["PyramidStart"]):
            timespinner_location_ids["Ancient Pyramid"] += [
                1337233, 1337234, 1337235]
        if (slot_data["PureTorcher"]):
            timespinner_location_ids["Present"] += list(range(1337250, 1337352)) + list(range(1337422, 1337496)) + [1337506] + list(range(1337712, 1337779)) + [1337781, 1337782]
            timespinner_location_ids["Past"] += list(range(1337497, 1337505)) + list(range(1337507, 1337711)) + [1337780]
            timespinner_location_ids["Ancient Pyramid"] += list(range(1337369, 1337421))
            if (slot_data["GyreArchives"]):
                timespinner_location_ids["Ancient Pyramid"] += list(range(1337353, 1337368))

        display_data = {}

        # Victory condition
        game_state = tracker_data.get_player_client_status(team, player)
        display_data["game_finished"] = game_state == 30

        inventory = tracker_data.get_player_inventory_counts(team, player)

        # Turn location IDs into advancement tab counts
        checked_locations = tracker_data.get_player_checked_locations(team, player)
        lookup_name = lambda id: tracker_data.location_id_to_name["Timespinner"][id]
        location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations}
                         for tab_name, tab_locations in timespinner_location_ids.items()}
        checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations])
                       for tab_name, tab_locations in timespinner_location_ids.items()}
        checks_done["Total"] = len(checked_locations)
        checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in timespinner_location_ids.items()}
        checks_in_area["Total"] = sum(checks_in_area.values())
        options = {k for k, v in slot_data.items() if v}

        lookup_any_item_id_to_name = tracker_data.item_id_to_name["Timespinner"]
        return render_template(
            "tracker__Timespinner.html",
            inventory=inventory,
            icons=icons,
            acquired_items={lookup_any_item_id_to_name[id] for id, count in inventory.items() if count > 0},
            player=player,
            team=team,
            room=tracker_data.room,
            player_name=tracker_data.get_player_name(player),
            checks_done=checks_done,
            checks_in_area=checks_in_area,
            location_info=location_info,
            options=options,
            **display_data,
        )

    _player_trackers["Timespinner"] = render_Timespinner_tracker

if "Super Metroid" in network_data_package["games"]:
    def render_SuperMetroid_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        icons = {
            "Energy Tank":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/ETank.png",
            "Missile":        "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Missile.png",
            "Super Missile":  "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Super.png",
            "Power Bomb":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/PowerBomb.png",
            "Bomb":           "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Bomb.png",
            "Charge Beam":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Charge.png",
            "Ice Beam":       "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Ice.png",
            "Hi-Jump Boots":  "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/HiJump.png",
            "Speed Booster":  "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/SpeedBooster.png",
            "Wave Beam":      "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Wave.png",
            "Spazer":         "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Spazer.png",
            "Spring Ball":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/SpringBall.png",
            "Varia Suit":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Varia.png",
            "Plasma Beam":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Plasma.png",
            "Grappling Beam": "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Grapple.png",
            "Morph Ball":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Morph.png",
            "Reserve Tank":   "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Reserve.png",
            "Gravity Suit":   "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/Gravity.png",
            "X-Ray Scope":    "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/XRayScope.png",
            "Space Jump":     "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/SpaceJump.png",
            "Screw Attack":   "https://randommetroidsolver.pythonanywhere.com/solver/static/images/tracker/inventory/ScrewAttack.png",
            "Nothing":        "",
            "No Energy":      "",
            "Kraid":          "",
            "Phantoon":       "",
            "Draygon":        "",
            "Ridley":         "",
            "Mother Brain":   "",
        }

        multi_items = {
            "Energy Tank":   83000,
            "Missile":       83001,
            "Super Missile": 83002,
            "Power Bomb":    83003,
            "Reserve Tank":  83020,
        }

        supermetroid_location_ids = {
            'Crateria/Blue Brinstar': [82005, 82007, 82008, 82026, 82029,
                                       82000, 82004, 82006, 82009, 82010,
                                       82011, 82012, 82027, 82028, 82034,
                                       82036, 82037],
            'Green/Pink Brinstar':    [82017, 82023, 82030, 82033, 82035,
                                       82013, 82014, 82015, 82016, 82018,
                                       82019, 82021, 82022, 82024, 82025,
                                       82031],
            'Red Brinstar':           [82038, 82042, 82039, 82040, 82041],
            'Kraid':                  [82043, 82048, 82044],
            'Norfair':                [82050, 82053, 82061, 82066, 82068,
                                       82049, 82051, 82054, 82055, 82056,
                                       82062, 82063, 82064, 82065, 82067],
            'Lower Norfair':          [82078, 82079, 82080, 82070, 82071,
                                       82073, 82074, 82075, 82076, 82077],
            'Crocomire':              [82052, 82060, 82057, 82058, 82059],
            'Wrecked Ship':           [82129, 82132, 82134, 82135, 82001,
                                       82002, 82003, 82128, 82130, 82131,
                                       82133],
            'West Maridia':           [82138, 82136, 82137, 82139, 82140,
                                       82141, 82142],
            'East Maridia':           [82143, 82145, 82150, 82152, 82154,
                                       82144, 82146, 82147, 82148, 82149,
                                       82151],
        }

        display_data = {}
        inventory = tracker_data.get_player_inventory_counts(team, player)

        for item_name, item_id in multi_items.items():
            base_name = item_name.split()[0].lower()
            display_data[base_name + "_count"] = inventory[item_id]

        # Victory condition
        game_state = tracker_data.get_player_client_status(team, player)
        display_data["game_finished"] = game_state == 30

        # Turn location IDs into advancement tab counts
        checked_locations = tracker_data.get_player_checked_locations(team, player)
        lookup_name = lambda id: tracker_data.location_id_to_name["Super Metroid"][id]
        location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations}
                         for tab_name, tab_locations in supermetroid_location_ids.items()}
        checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations])
                       for tab_name, tab_locations in supermetroid_location_ids.items()}
        checks_done['Total'] = len(checked_locations)
        checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in supermetroid_location_ids.items()}
        checks_in_area['Total'] = sum(checks_in_area.values())

        lookup_any_item_id_to_name = tracker_data.item_id_to_name["Super Metroid"]
        return render_template(
            "tracker__SuperMetroid.html",
            inventory=inventory,
            icons=icons,
            acquired_items={lookup_any_item_id_to_name[id] for id, count in inventory.items() if count > 0},
            player=player,
            team=team,
            room=tracker_data.room,
            player_name=tracker_data.get_player_name(player),
            checks_done=checks_done,
            checks_in_area=checks_in_area,
            location_info=location_info,
            **display_data,
        )

    _player_trackers["Super Metroid"] = render_SuperMetroid_tracker

if "ChecksFinder" in network_data_package["games"]:
    def render_ChecksFinder_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        icons = {
            "Checks Available": "https://0rganics.org/archipelago/cf/spr_tiles_3.png",
            "Map Width":        "https://0rganics.org/archipelago/cf/spr_tiles_4.png",
            "Map Height":       "https://0rganics.org/archipelago/cf/spr_tiles_5.png",
            "Map Bombs":        "https://0rganics.org/archipelago/cf/spr_tiles_6.png",

            "Nothing":          "",
        }

        checksfinder_location_ids = {
            "Tile 1":  81000,
            "Tile 2":  81001,
            "Tile 3":  81002,
            "Tile 4":  81003,
            "Tile 5":  81004,
            "Tile 6":  81005,
            "Tile 7":  81006,
            "Tile 8":  81007,
            "Tile 9":  81008,
            "Tile 10": 81009,
            "Tile 11": 81010,
            "Tile 12": 81011,
            "Tile 13": 81012,
            "Tile 14": 81013,
            "Tile 15": 81014,
            "Tile 16": 81015,
            "Tile 17": 81016,
            "Tile 18": 81017,
            "Tile 19": 81018,
            "Tile 20": 81019,
            "Tile 21": 81020,
            "Tile 22": 81021,
            "Tile 23": 81022,
            "Tile 24": 81023,
            "Tile 25": 81024,
        }

        display_data = {}
        inventory = tracker_data.get_player_inventory_counts(team, player)
        locations = tracker_data.get_player_locations(player)

        # Multi-items
        multi_items = {
            "Map Width":  80000,
            "Map Height": 80001,
            "Map Bombs":  80002
        }
        for item_name, item_id in multi_items.items():
            base_name = item_name.split()[-1].lower()
            count = inventory[item_id]
            display_data[base_name + "_count"] = count
            display_data[base_name + "_display"] = count + 5

        # Get location info
        checked_locations = tracker_data.get_player_checked_locations(team, player)
        lookup_name = lambda id: tracker_data.location_id_to_name["ChecksFinder"][id]
        location_info = {tile_name: {lookup_name(tile_location): (tile_location in checked_locations)} for
                         tile_name, tile_location in checksfinder_location_ids.items() if
                         tile_location in set(locations)}
        checks_done = {tile_name: len([tile_location]) for tile_name, tile_location in checksfinder_location_ids.items()
                       if tile_location in checked_locations and tile_location in set(locations)}
        checks_done['Total'] = len(checked_locations)
        checks_in_area = checks_done

        # Calculate checks available
        display_data["checks_unlocked"] = min(
            display_data["width_count"] + display_data["height_count"] + display_data["bombs_count"] + 5, 25)
        display_data["checks_available"] = max(display_data["checks_unlocked"] - len(checked_locations), 0)

        # Victory condition
        game_state = tracker_data.get_player_client_status(team, player)
        display_data["game_finished"] = game_state == 30

        lookup_any_item_id_to_name = tracker_data.item_id_to_name["ChecksFinder"]
        return render_template(
            "tracker__ChecksFinder.html",
            inventory=inventory, icons=icons,
            acquired_items={lookup_any_item_id_to_name[id] for id, count in inventory.items() if count > 0},
            player=player,
            team=team,
            room=tracker_data.room,
            player_name=tracker_data.get_player_name(player),
            checks_done=checks_done,
            checks_in_area=checks_in_area,
            location_info=location_info,
            **display_data,
        )

    _player_trackers["ChecksFinder"] = render_ChecksFinder_tracker

if "Starcraft 2" in network_data_package["games"]:
    def render_Starcraft2_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        SC2WOL_ITEM_ID_OFFSET = 1000
        SC2HOTS_ITEM_ID_OFFSET = 2000
        SC2LOTV_ITEM_ID_OFFSET = 2000
        SC2_KEY_ITEM_ID_OFFSET = 4000
        NCO_LOCATION_ID_LOW = 20004500
        NCO_LOCATION_ID_HIGH = NCO_LOCATION_ID_LOW + 1000

        STARTING_MINERALS_ITEM_ID = 1800
        STARTING_VESPENE_ITEM_ID = 1801
        STARTING_SUPPLY_ITEM_ID = 1802
        # NOTHING_ITEM_ID = 1803
        MAX_SUPPLY_ITEM_ID = 1804
        SHIELD_REGENERATION_ITEM_ID = 1805
        BUILDING_CONSTRUCTION_SPEED_ITEM_ID = 1806
        UPGRADE_RESEARCH_SPEED_ITEM_ID = 1807
        UPGRADE_RESEARCH_COST_ITEM_ID = 1808
        REDUCED_MAX_SUPPLY_ITEM_ID = 1850
        slot_data = tracker_data.get_slot_data(player)
        inventory: collections.Counter[int] = tracker_data.get_player_inventory_counts(team, player)
        item_id_to_name = tracker_data.item_id_to_name["Starcraft 2"]
        location_id_to_name = tracker_data.location_id_to_name["Starcraft 2"]

        # Filler item counters
        display_data = {}
        display_data["minerals_count"] = slot_data.get("minerals_per_item", 15) * inventory.get(STARTING_MINERALS_ITEM_ID, 0)
        display_data["vespene_count"] = slot_data.get("vespene_per_item", 15) * inventory.get(STARTING_VESPENE_ITEM_ID, 0)
        display_data["supply_count"] = slot_data.get("starting_supply_per_item", 2) * inventory.get(STARTING_SUPPLY_ITEM_ID, 0)
        display_data["max_supply_count"] = slot_data.get("maximum_supply_per_item", 1) * inventory.get(MAX_SUPPLY_ITEM_ID, 0)
        display_data["reduced_supply_count"] = slot_data.get("maximum_supply_reduction_per_item", 1) * inventory.get(REDUCED_MAX_SUPPLY_ITEM_ID, 0)
        display_data["construction_speed_count"] = inventory.get(BUILDING_CONSTRUCTION_SPEED_ITEM_ID, 0)
        display_data["shield_regen_count"] = inventory.get(SHIELD_REGENERATION_ITEM_ID, 0)
        display_data["upgrade_speed_count"] = inventory.get(UPGRADE_RESEARCH_SPEED_ITEM_ID, 0)
        display_data["research_cost_count"] = inventory.get(UPGRADE_RESEARCH_COST_ITEM_ID, 0)

        # Locations
        have_nco_locations = False
        locations = tracker_data.get_player_locations(player)
        checked_locations = tracker_data.get_player_checked_locations(team, player)
        missions: dict[str, list[tuple[str, bool]]] = {}
        for location_id in locations:
            location_name = location_id_to_name.get(location_id, "")
            if ":" not in location_name:
                continue
            mission_name = location_name.split(":", 1)[0]
            missions.setdefault(mission_name, []).append((location_name, location_id in checked_locations))
            if location_id >= NCO_LOCATION_ID_LOW and location_id < NCO_LOCATION_ID_HIGH:
                have_nco_locations = True
        missions = {mission: missions[mission] for mission in sorted(missions)}

        # Kerrigan level
        level_item_id_to_amount = (
            (509 + SC2HOTS_ITEM_ID_OFFSET, 1,),
            (508 + SC2HOTS_ITEM_ID_OFFSET, 2,),
            (507 + SC2HOTS_ITEM_ID_OFFSET, 3,),
            (506 + SC2HOTS_ITEM_ID_OFFSET, 4,),
            (505 + SC2HOTS_ITEM_ID_OFFSET, 5,),
            (504 + SC2HOTS_ITEM_ID_OFFSET, 6,),
            (503 + SC2HOTS_ITEM_ID_OFFSET, 7,),
            (502 + SC2HOTS_ITEM_ID_OFFSET, 8,),
            (501 + SC2HOTS_ITEM_ID_OFFSET, 9,),
            (500 + SC2HOTS_ITEM_ID_OFFSET, 10,),
            (510 + SC2HOTS_ITEM_ID_OFFSET, 14,),
            (511 + SC2HOTS_ITEM_ID_OFFSET, 35,),
            (512 + SC2HOTS_ITEM_ID_OFFSET, 70,),
        )
        kerrigan_level = 0
        for item_id, levels_per_item in level_item_id_to_amount:
            kerrigan_level += levels_per_item * inventory[item_id]
        display_data["kerrigan_level"] = kerrigan_level

        # Hero presence
        display_data["kerrigan_present"] = slot_data.get("kerrigan_presence", 0) == 0
        display_data["nova_present"] = have_nco_locations

        # Upgrades
        TERRAN_INFANTRY_WEAPON_ID = 100 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_INFANTRY_ARMOR_ID =  102 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_VEHICLE_WEAPON_ID =  103 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_VEHICLE_ARMOR_ID =   104 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_SHIP_WEAPON_ID =     105 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_SHIP_ARMOR_ID =      106 + SC2WOL_ITEM_ID_OFFSET
        ZERG_MELEE_ATTACK_ID =      100 + SC2HOTS_ITEM_ID_OFFSET
        ZERG_MISSILE_ATTACK_ID =    101 + SC2HOTS_ITEM_ID_OFFSET
        ZERG_GROUND_CARAPACE_ID =   102 + SC2HOTS_ITEM_ID_OFFSET
        ZERG_FLYER_ATTACK_ID =      103 + SC2HOTS_ITEM_ID_OFFSET
        ZERG_FLYER_CARAPACE_ID =    104 + SC2HOTS_ITEM_ID_OFFSET
        PROTOSS_GROUND_WEAPON_ID =  100 + SC2LOTV_ITEM_ID_OFFSET
        PROTOSS_GROUND_ARMOR_ID =   101 + SC2LOTV_ITEM_ID_OFFSET
        PROTOSS_SHIELDS_ID =        102 + SC2LOTV_ITEM_ID_OFFSET
        PROTOSS_AIR_WEAPON_ID =     103 + SC2LOTV_ITEM_ID_OFFSET
        PROTOSS_AIR_ARMOR_ID =      104 + SC2LOTV_ITEM_ID_OFFSET

        # Bundles
        TERRAN_WEAPON_UPGRADE_ID =        107 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_ARMOR_UPGRADE_ID =         108 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_INFANTRY_UPGRADE_ID =      109 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_VEHICLE_UPGRADE_ID =       110 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_SHIP_UPGRADE_ID =          111 + SC2WOL_ITEM_ID_OFFSET
        TERRAN_WEAPON_ARMOR_UPGRADE_ID =  112 + SC2WOL_ITEM_ID_OFFSET
        ZERG_WEAPON_UPGRADE_ID =          105 + SC2HOTS_ITEM_ID_OFFSET
        ZERG_ARMOR_UPGRADE_ID =           106 + SC2HOTS_ITEM_ID_OFFSET
        ZERG_GROUND_UPGRADE_ID =          107 + SC2HOTS_ITEM_ID_OFFSET
        ZERG_FLYER_UPGRADE_ID =           108 + SC2HOTS_ITEM_ID_OFFSET
        ZERG_WEAPON_ARMOR_UPGRADE_ID =    109 + SC2HOTS_ITEM_ID_OFFSET
        PROTOSS_WEAPON_UPGRADE_ID =       105 + SC2LOTV_ITEM_ID_OFFSET
        PROTOSS_ARMOR_UPGRADE_ID =        106 + SC2LOTV_ITEM_ID_OFFSET
        PROTOSS_GROUND_UPGRADE_ID =       107 + SC2LOTV_ITEM_ID_OFFSET
        PROTOSS_AIR_UPGRADE_ID =          108 + SC2LOTV_ITEM_ID_OFFSET
        PROTOSS_WEAPON_ARMOR_UPGRADE_ID = 109 + SC2LOTV_ITEM_ID_OFFSET
        grouped_item_replacements = {
            TERRAN_WEAPON_UPGRADE_ID: [
                TERRAN_INFANTRY_WEAPON_ID,
                TERRAN_VEHICLE_WEAPON_ID,
                TERRAN_SHIP_WEAPON_ID,
            ],
            TERRAN_ARMOR_UPGRADE_ID: [
                TERRAN_INFANTRY_ARMOR_ID,
                TERRAN_VEHICLE_ARMOR_ID,
                TERRAN_SHIP_ARMOR_ID,
            ],
            TERRAN_INFANTRY_UPGRADE_ID: [
                TERRAN_INFANTRY_WEAPON_ID,
                TERRAN_INFANTRY_ARMOR_ID,
            ],
            TERRAN_VEHICLE_UPGRADE_ID: [
                TERRAN_VEHICLE_WEAPON_ID,
                TERRAN_VEHICLE_ARMOR_ID,
            ],
            TERRAN_SHIP_UPGRADE_ID: [
                TERRAN_SHIP_WEAPON_ID,
                TERRAN_SHIP_ARMOR_ID
            ],
            ZERG_WEAPON_UPGRADE_ID: [
                ZERG_MELEE_ATTACK_ID,
                ZERG_MISSILE_ATTACK_ID,
                ZERG_FLYER_ATTACK_ID,
            ],
            ZERG_ARMOR_UPGRADE_ID: [
                ZERG_GROUND_CARAPACE_ID,
                ZERG_FLYER_CARAPACE_ID,
            ],
            ZERG_GROUND_UPGRADE_ID: [
                ZERG_MELEE_ATTACK_ID,
                ZERG_MISSILE_ATTACK_ID,
                ZERG_GROUND_CARAPACE_ID,
            ],
            ZERG_FLYER_UPGRADE_ID: [
                ZERG_FLYER_ATTACK_ID,
                ZERG_FLYER_CARAPACE_ID,
            ],
            PROTOSS_WEAPON_UPGRADE_ID: [
                PROTOSS_GROUND_WEAPON_ID,
                PROTOSS_AIR_WEAPON_ID,
            ],
            PROTOSS_ARMOR_UPGRADE_ID: [
                PROTOSS_GROUND_ARMOR_ID,
                PROTOSS_SHIELDS_ID,
                PROTOSS_AIR_ARMOR_ID,
            ],
            PROTOSS_GROUND_UPGRADE_ID: [
                PROTOSS_GROUND_WEAPON_ID,
                PROTOSS_GROUND_ARMOR_ID,
                PROTOSS_SHIELDS_ID,
            ],
            PROTOSS_AIR_UPGRADE_ID: [
                PROTOSS_AIR_WEAPON_ID,
                PROTOSS_AIR_ARMOR_ID,
                PROTOSS_SHIELDS_ID,
            ]
        }
        grouped_item_replacements[TERRAN_WEAPON_ARMOR_UPGRADE_ID] = (
            grouped_item_replacements[TERRAN_WEAPON_UPGRADE_ID]
            + grouped_item_replacements[TERRAN_ARMOR_UPGRADE_ID]
        )
        grouped_item_replacements[ZERG_WEAPON_ARMOR_UPGRADE_ID] = (
            grouped_item_replacements[ZERG_WEAPON_UPGRADE_ID]
            + grouped_item_replacements[ZERG_ARMOR_UPGRADE_ID]
        )
        grouped_item_replacements[PROTOSS_WEAPON_ARMOR_UPGRADE_ID] = (
            grouped_item_replacements[PROTOSS_WEAPON_UPGRADE_ID]
            + grouped_item_replacements[PROTOSS_ARMOR_UPGRADE_ID]
        )
        for bundle_id, upgrade_ids in grouped_item_replacements.items():
            bundle_amount = inventory[bundle_id]
            for upgrade_id in upgrade_ids:
                if bundle_amount > inventory[upgrade_id]:
                    # Only assign, don't add.
                    # This behaviour mimics protoss shields, where the output is
                    # the maximum bundle contribution, not the sum
                    inventory[upgrade_id] = bundle_amount


        # Victory condition
        game_state = tracker_data.get_player_client_status(team, player)
        display_data["game_finished"] = game_state == ClientStatus.CLIENT_GOAL

        # Keys
        keys: dict[str, int] = {}
        for item_id, item_count in inventory.items():
            if item_id < SC2_KEY_ITEM_ID_OFFSET:
                continue
            keys[item_id_to_name[item_id]] = item_count

        return render_template(
            "tracker__Starcraft2.html",
            inventory=inventory,
            player=player,
            team=team,
            room=tracker_data.room,
            player_name=tracker_data.get_player_name(player),
            missions=missions,
            locations=locations,
            checked_locations=checked_locations,
            location_id_to_name=location_id_to_name,
            item_id_to_name=item_id_to_name,
            keys=keys,
            saving_second=tracker_data.get_room_saving_second(),
            **display_data,
        )


    _player_trackers["Starcraft 2"] = render_Starcraft2_tracker
