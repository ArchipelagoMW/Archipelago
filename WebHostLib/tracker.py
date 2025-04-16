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

_multidata_cache = {}
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

    def get_slot_data(self, team: int, player: int) -> Dict[str, Any]:
        """Retrieves the slot data for a given player."""
        return self._multidata["slot_data"][player]

    def get_slot_info(self, team: int, player: int) -> NetworkSlot:
        """Retrieves the NetworkSlot data for a given player."""
        return self._multidata["slot_info"][player]

    def get_player_name(self, team: int, player: int) -> str:
        """Retrieves the slot name for a given player."""
        return self.get_slot_info(team, player).name

    def get_player_game(self, team: int, player: int) -> str:
        """Retrieves the game for a given player."""
        return self.get_slot_info(team, player).game

    def get_player_locations(self, team: int, player: int) -> Dict[int, ItemMetadata]:
        """Retrieves all locations with their containing item's metadata for a given player."""
        return self._multidata["locations"][player]

    def get_player_starting_inventory(self, team: int, player: int) -> List[int]:
        """Retrieves a list of all item codes a given slot starts with."""
        return self._multidata["precollected_items"][player]

    def get_player_checked_locations(self, team: int, player: int) -> Set[int]:
        """Retrieves the set of all locations marked complete by this player."""
        return self._multisave.get("location_checks", {}).get((team, player), set())

    @_cache_results
    def get_player_missing_locations(self, team: int, player: int) -> Set[int]:
        """Retrieves the set of all locations not marked complete by this player."""
        return set(self.get_player_locations(team, player)) - self.get_player_checked_locations(team, player)

    def get_player_received_items(self, team: int, player: int) -> List[NetworkItem]:
        """Returns all items received to this player in order of received."""
        return self._multisave.get("received_items", {}).get((team, player, True), [])

    @_cache_results
    def get_player_inventory_counts(self, team: int, player: int) -> collections.Counter:
        """Retrieves a dictionary of all items received by their id and their received count."""
        received_items = self.get_player_received_items(team, player)
        starting_items = self.get_player_starting_inventory(team, player)
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
            team: sum(len(self.get_player_locations(team, player)) for player in players)
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
                if self.get_slot_info(0, player).type == SlotType.player
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
            (team, player): self.get_player_locations(team, player)
            for team, players in self.get_all_players().items() for player in players
        }

    @_cache_results
    def get_room_games(self) -> Dict[TeamPlayer, str]:
        """Retrieves a dictionary of games for each player."""
        return {
            (team, player): self.get_player_game(team, player)
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
                    long_player_names[team, player] = f"{alias} ({self.get_player_name(team, player)})"
                else:
                    long_player_names[team, player] = self.get_player_name(team, player)

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
    game_specific_tracker = _player_trackers.get(tracker_data.get_player_game(tracked_team, tracked_player), None)
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
    game = tracker_data.get_player_game(team, player)

    received_items_in_order = {}
    starting_inventory = tracker_data.get_player_starting_inventory(team, player)
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
        locations=tracker_data.get_player_locations(team, player),
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
            if tracker_data.get_player_game(team, player) == "Factorio"
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
        if tracker_data.get_slot_data(team, player).get("bombless_start", True):
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
            for player in players if tracker_data.get_slot_info(team, player).game == "A Link to the Past"
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
            for player in players if tracker_data.get_slot_info(team, player).game == "A Link to the Past"
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
            player_name=tracker_data.get_player_name(team, player),
            regions=regions,
            known_regions=known_regions,
        )

    _multiworld_trackers["A Link to the Past"] = render_ALinkToThePast_multiworld_tracker
    _player_trackers["A Link to the Past"] = render_ALinkToThePast_tracker

if "Minecraft" in network_data_package["games"]:
    def render_Minecraft_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        icons = {
            "Wooden Pickaxe":     "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d2/Wooden_Pickaxe_JE3_BE3.png",
            "Stone Pickaxe":      "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c4/Stone_Pickaxe_JE2_BE2.png",
            "Iron Pickaxe":       "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d1/Iron_Pickaxe_JE3_BE2.png",
            "Diamond Pickaxe":    "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e7/Diamond_Pickaxe_JE3_BE3.png",
            "Wooden Sword":       "https://static.wikia.nocookie.net/minecraft_gamepedia/images/d/d5/Wooden_Sword_JE2_BE2.png",
            "Stone Sword":        "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b1/Stone_Sword_JE2_BE2.png",
            "Iron Sword":         "https://static.wikia.nocookie.net/minecraft_gamepedia/images/8/8e/Iron_Sword_JE2_BE2.png",
            "Diamond Sword":      "https://static.wikia.nocookie.net/minecraft_gamepedia/images/4/44/Diamond_Sword_JE3_BE3.png",
            "Leather Tunic":      "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b7/Leather_Tunic_JE4_BE2.png",
            "Iron Chestplate":    "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Iron_Chestplate_JE2_BE2.png",
            "Diamond Chestplate": "https://static.wikia.nocookie.net/minecraft_gamepedia/images/e/e0/Diamond_Chestplate_JE3_BE2.png",
            "Iron Ingot":         "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Iron_Ingot_JE3_BE2.png",
            "Block of Iron":      "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7e/Block_of_Iron_JE4_BE3.png",
            "Brewing Stand":      "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b3/Brewing_Stand_%28empty%29_JE10.png",
            "Ender Pearl":        "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/f6/Ender_Pearl_JE3_BE2.png",
            "Bucket":             "https://static.wikia.nocookie.net/minecraft_gamepedia/images/f/fc/Bucket_JE2_BE2.png",
            "Bow":                "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/ab/Bow_%28Pull_2%29_JE1_BE1.png",
            "Shield":             "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c6/Shield_JE2_BE1.png",
            "Red Bed":            "https://static.wikia.nocookie.net/minecraft_gamepedia/images/6/6a/Red_Bed_%28N%29.png",
            "Netherite Scrap":    "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/33/Netherite_Scrap_JE2_BE1.png",
            "Flint and Steel":    "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/94/Flint_and_Steel_JE4_BE2.png",
            "Enchanting Table":   "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/31/Enchanting_Table.gif",
            "Fishing Rod":        "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/7f/Fishing_Rod_JE2_BE2.png",
            "Campfire":           "https://static.wikia.nocookie.net/minecraft_gamepedia/images/9/91/Campfire_JE2_BE2.gif",
            "Water Bottle":       "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/75/Water_Bottle_JE2_BE2.png",
            "Spyglass":           "https://static.wikia.nocookie.net/minecraft_gamepedia/images/c/c1/Spyglass_JE2_BE1.png",
            "Dragon Egg Shard":   "https://static.wikia.nocookie.net/minecraft_gamepedia/images/3/38/Dragon_Egg_JE4.png",
            "Lead":               "https://static.wikia.nocookie.net/minecraft_gamepedia/images/1/1f/Lead_JE2_BE2.png",
            "Saddle":             "https://i.imgur.com/2QtDyR0.png",
            "Channeling Book":    "https://i.imgur.com/J3WsYZw.png",
            "Silk Touch Book":    "https://i.imgur.com/iqERxHQ.png",
            "Piercing IV Book":   "https://i.imgur.com/OzJptGz.png",
        }

        minecraft_location_ids = {
            "Story":       [42073, 42023, 42027, 42039, 42002, 42009, 42010, 42070,
                            42041, 42049, 42004, 42031, 42025, 42029, 42051, 42077],
            "Nether":      [42017, 42044, 42069, 42058, 42034, 42060, 42066, 42076, 42064, 42071, 42021,
                            42062, 42008, 42061, 42033, 42011, 42006, 42019, 42000, 42040, 42001, 42015, 42104, 42014],
            "The End":     [42052, 42005, 42012, 42032, 42030, 42042, 42018, 42038, 42046],
            "Adventure":   [42047, 42050, 42096, 42097, 42098, 42059, 42055, 42072, 42003, 42109, 42035, 42016, 42020,
                            42048, 42054, 42068, 42043, 42106, 42074, 42075, 42024, 42026, 42037, 42045, 42056, 42105,
                            42099, 42103, 42110, 42100],
            "Husbandry":   [42065, 42067, 42078, 42022, 42113, 42107, 42007, 42079, 42013, 42028, 42036, 42108, 42111,
                            42112,
                            42057, 42063, 42053, 42102, 42101, 42092, 42093, 42094, 42095],
            "Archipelago": [42080, 42081, 42082, 42083, 42084, 42085, 42086, 42087, 42088, 42089, 42090, 42091],
        }

        display_data = {}

        # Determine display for progressive items
        progressive_items = {
            "Progressive Tools":             45013,
            "Progressive Weapons":           45012,
            "Progressive Armor":             45014,
            "Progressive Resource Crafting": 45001
        }
        progressive_names = {
            "Progressive Tools":             ["Wooden Pickaxe", "Stone Pickaxe", "Iron Pickaxe", "Diamond Pickaxe"],
            "Progressive Weapons":           ["Wooden Sword", "Stone Sword", "Iron Sword", "Diamond Sword"],
            "Progressive Armor":             ["Leather Tunic", "Iron Chestplate", "Diamond Chestplate"],
            "Progressive Resource Crafting": ["Iron Ingot", "Iron Ingot", "Block of Iron"]
        }

        inventory = tracker_data.get_player_inventory_counts(team, player)
        for item_name, item_id in progressive_items.items():
            level = min(inventory[item_id], len(progressive_names[item_name]) - 1)
            display_name = progressive_names[item_name][level]
            base_name = item_name.split(maxsplit=1)[1].lower().replace(" ", "_")
            display_data[base_name + "_url"] = icons[display_name]

        # Multi-items
        multi_items = {
            "3 Ender Pearls":    45029,
            "8 Netherite Scrap": 45015,
            "Dragon Egg Shard":  45043
        }
        for item_name, item_id in multi_items.items():
            base_name = item_name.split()[-1].lower()
            count = inventory[item_id]
            if count >= 0:
                display_data[base_name + "_count"] = count

        # Victory condition
        game_state = tracker_data.get_player_client_status(team, player)
        display_data["game_finished"] = game_state == 30

        # Turn location IDs into advancement tab counts
        checked_locations = tracker_data.get_player_checked_locations(team, player)
        lookup_name = lambda id: tracker_data.location_id_to_name["Minecraft"][id]
        location_info = {tab_name: {lookup_name(id): (id in checked_locations) for id in tab_locations}
                         for tab_name, tab_locations in minecraft_location_ids.items()}
        checks_done = {tab_name: len([id for id in tab_locations if id in checked_locations])
                       for tab_name, tab_locations in minecraft_location_ids.items()}
        checks_done["Total"] = len(checked_locations)
        checks_in_area = {tab_name: len(tab_locations) for tab_name, tab_locations in minecraft_location_ids.items()}
        checks_in_area["Total"] = sum(checks_in_area.values())

        lookup_any_item_id_to_name = tracker_data.item_id_to_name["Minecraft"]
        return render_template(
            "tracker__Minecraft.html",
            inventory=inventory,
            icons=icons,
            acquired_items={lookup_any_item_id_to_name[id] for id, count in inventory.items() if count > 0},
            player=player,
            team=team,
            room=tracker_data.room,
            player_name=tracker_data.get_player_name(team, player),
            saving_second=tracker_data.get_room_saving_second(),
            checks_done=checks_done,
            checks_in_area=checks_in_area,
            location_info=location_info,
            **display_data,
        )

    _player_trackers["Minecraft"] = render_Minecraft_tracker

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

        locations = tracker_data.get_player_locations(team, player)
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
            player_name=tracker_data.get_player_name(team, player),
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
        }

        timespinner_location_ids = {
            "Present":         [
                1337000, 1337001, 1337002, 1337003, 1337004, 1337005, 1337006, 1337007, 1337008, 1337009,
                1337010, 1337011, 1337012, 1337013, 1337014, 1337015, 1337016, 1337017, 1337018, 1337019,
                1337020, 1337021, 1337022, 1337023, 1337024, 1337025, 1337026, 1337027, 1337028, 1337029,
                1337030, 1337031, 1337032, 1337033, 1337034, 1337035, 1337036, 1337037, 1337038, 1337039,
                1337040, 1337041, 1337042, 1337043, 1337044, 1337045, 1337046, 1337047, 1337048, 1337049,
                1337050, 1337051, 1337052, 1337053, 1337054, 1337055, 1337056, 1337057, 1337058, 1337059,
                1337060, 1337061, 1337062, 1337063, 1337064, 1337065, 1337066, 1337067, 1337068, 1337069,
                1337070, 1337071, 1337072, 1337073, 1337074, 1337075, 1337076, 1337077, 1337078, 1337079,
                1337080, 1337081, 1337082, 1337083, 1337084, 1337085],
            "Past":            [
                1337086, 1337087, 1337088, 1337089,
                1337090, 1337091, 1337092, 1337093, 1337094, 1337095, 1337096, 1337097, 1337098, 1337099,
                1337100, 1337101, 1337102, 1337103, 1337104, 1337105, 1337106, 1337107, 1337108, 1337109,
                1337110, 1337111, 1337112, 1337113, 1337114, 1337115, 1337116, 1337117, 1337118, 1337119,
                1337120, 1337121, 1337122, 1337123, 1337124, 1337125, 1337126, 1337127, 1337128, 1337129,
                1337130, 1337131, 1337132, 1337133, 1337134, 1337135, 1337136, 1337137, 1337138, 1337139,
                1337140, 1337141, 1337142, 1337143, 1337144, 1337145, 1337146, 1337147, 1337148, 1337149,
                1337150, 1337151, 1337152, 1337153, 1337154, 1337155,
                1337171, 1337172, 1337173, 1337174, 1337175],
            "Ancient Pyramid": [
                1337236,
                1337246, 1337247, 1337248, 1337249]
        }

        slot_data = tracker_data.get_slot_data(team, player)
        if (slot_data["DownloadableItems"]):
            timespinner_location_ids["Present"] += [
                1337156, 1337157, 1337159,
                1337160, 1337161, 1337162, 1337163, 1337164, 1337165, 1337166, 1337167, 1337168, 1337169,
                1337170]
        if (slot_data["Cantoran"]):
            timespinner_location_ids["Past"].append(1337176)
        if (slot_data["LoreChecks"]):
            timespinner_location_ids["Present"] += [
                1337177, 1337178, 1337179,
                1337180, 1337181, 1337182, 1337183, 1337184, 1337185, 1337186, 1337187]
            timespinner_location_ids["Past"] += [
                1337188, 1337189,
                1337190, 1337191, 1337192, 1337193, 1337194, 1337195, 1337196, 1337197, 1337198]
        if (slot_data["GyreArchives"]):
            timespinner_location_ids["Ancient Pyramid"] += [
                1337237, 1337238, 1337239,
                1337240, 1337241, 1337242, 1337243, 1337244, 1337245]
        if (slot_data["PyramidStart"]):
            timespinner_location_ids["Ancient Pyramid"] += [
                1337233, 1337234, 1337235]

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
            player_name=tracker_data.get_player_name(team, player),
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
            player_name=tracker_data.get_player_name(team, player),
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
        locations = tracker_data.get_player_locations(team, player)

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
            player_name=tracker_data.get_player_name(team, player),
            checks_done=checks_done,
            checks_in_area=checks_in_area,
            location_info=location_info,
            **display_data,
        )

    _player_trackers["ChecksFinder"] = render_ChecksFinder_tracker

if "Starcraft 2" in network_data_package["games"]:
    def render_Starcraft2_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        SC2WOL_LOC_ID_OFFSET = 1000
        SC2HOTS_LOC_ID_OFFSET = 20000000  # Avoid clashes with The Legend of Zelda
        SC2LOTV_LOC_ID_OFFSET = SC2HOTS_LOC_ID_OFFSET + 2000
        SC2NCO_LOC_ID_OFFSET = SC2LOTV_LOC_ID_OFFSET + 2500

        SC2WOL_ITEM_ID_OFFSET = 1000
        SC2HOTS_ITEM_ID_OFFSET = SC2WOL_ITEM_ID_OFFSET + 1000
        SC2LOTV_ITEM_ID_OFFSET = SC2HOTS_ITEM_ID_OFFSET + 1000

        slot_data = tracker_data.get_slot_data(team, player)
        minerals_per_item = slot_data.get("minerals_per_item", 15)
        vespene_per_item = slot_data.get("vespene_per_item", 15)
        starting_supply_per_item = slot_data.get("starting_supply_per_item", 2)

        github_icon_base_url = "https://matthewmarinets.github.io/ap_sc2_icons/icons/"
        organics_icon_base_url = "https://0rganics.org/archipelago/sc2wol/"

        icons = {
            "Starting Minerals":                           github_icon_base_url + "blizzard/icon-mineral-nobg.png",
            "Starting Vespene":                            github_icon_base_url + "blizzard/icon-gas-terran-nobg.png",
            "Starting Supply":                             github_icon_base_url + "blizzard/icon-supply-terran_nobg.png",

            "Terran Infantry Weapons Level 1":             github_icon_base_url + "blizzard/btn-upgrade-terran-infantryweaponslevel1.png",
            "Terran Infantry Weapons Level 2":             github_icon_base_url + "blizzard/btn-upgrade-terran-infantryweaponslevel2.png",
            "Terran Infantry Weapons Level 3":             github_icon_base_url + "blizzard/btn-upgrade-terran-infantryweaponslevel3.png",
            "Terran Infantry Armor Level 1":               github_icon_base_url + "blizzard/btn-upgrade-terran-infantryarmorlevel1.png",
            "Terran Infantry Armor Level 2":               github_icon_base_url + "blizzard/btn-upgrade-terran-infantryarmorlevel2.png",
            "Terran Infantry Armor Level 3":               github_icon_base_url + "blizzard/btn-upgrade-terran-infantryarmorlevel3.png",
            "Terran Vehicle Weapons Level 1":              github_icon_base_url + "blizzard/btn-upgrade-terran-vehicleweaponslevel1.png",
            "Terran Vehicle Weapons Level 2":              github_icon_base_url + "blizzard/btn-upgrade-terran-vehicleweaponslevel2.png",
            "Terran Vehicle Weapons Level 3":              github_icon_base_url + "blizzard/btn-upgrade-terran-vehicleweaponslevel3.png",
            "Terran Vehicle Armor Level 1":                github_icon_base_url + "blizzard/btn-upgrade-terran-vehicleplatinglevel1.png",
            "Terran Vehicle Armor Level 2":                github_icon_base_url + "blizzard/btn-upgrade-terran-vehicleplatinglevel2.png",
            "Terran Vehicle Armor Level 3":                github_icon_base_url + "blizzard/btn-upgrade-terran-vehicleplatinglevel3.png",
            "Terran Ship Weapons Level 1":                 github_icon_base_url + "blizzard/btn-upgrade-terran-shipweaponslevel1.png",
            "Terran Ship Weapons Level 2":                 github_icon_base_url + "blizzard/btn-upgrade-terran-shipweaponslevel2.png",
            "Terran Ship Weapons Level 3":                 github_icon_base_url + "blizzard/btn-upgrade-terran-shipweaponslevel3.png",
            "Terran Ship Armor Level 1":                   github_icon_base_url + "blizzard/btn-upgrade-terran-shipplatinglevel1.png",
            "Terran Ship Armor Level 2":                   github_icon_base_url + "blizzard/btn-upgrade-terran-shipplatinglevel2.png",
            "Terran Ship Armor Level 3":                   github_icon_base_url + "blizzard/btn-upgrade-terran-shipplatinglevel3.png",

            "Bunker":                                      "https://static.wikia.nocookie.net/starcraft/images/c/c5/Bunker_SC2_Icon1.jpg",
            "Missile Turret":                              "https://static.wikia.nocookie.net/starcraft/images/5/5f/MissileTurret_SC2_Icon1.jpg",
            "Sensor Tower":                                "https://static.wikia.nocookie.net/starcraft/images/d/d2/SensorTower_SC2_Icon1.jpg",

            "Projectile Accelerator (Bunker)":             github_icon_base_url + "blizzard/btn-upgrade-zerg-stukov-bunkerresearchbundle_05.png",
            "Neosteel Bunker (Bunker)":                    organics_icon_base_url + "NeosteelBunker.png",
            "Titanium Housing (Missile Turret)":           organics_icon_base_url + "TitaniumHousing.png",
            "Hellstorm Batteries (Missile Turret)":        github_icon_base_url + "blizzard/btn-ability-stetmann-corruptormissilebarrage.png",
            "Advanced Construction (SCV)":                 github_icon_base_url + "blizzard/btn-ability-mengsk-trooper-advancedconstruction.png",
            "Dual-Fusion Welders (SCV)":                   github_icon_base_url + "blizzard/btn-upgrade-swann-scvdoublerepair.png",
            "Hostile Environment Adaptation (SCV)":        github_icon_base_url + "blizzard/btn-upgrade-swann-hellarmor.png",
            "Fire-Suppression System Level 1":             organics_icon_base_url + "Fire-SuppressionSystem.png",
            "Fire-Suppression System Level 2":             github_icon_base_url + "blizzard/btn-upgrade-swann-firesuppressionsystem.png",

            "Orbital Command":                             organics_icon_base_url + "OrbitalCommandCampaign.png",
            "Planetary Command Module":                    github_icon_base_url + "original/btn-orbital-fortress.png",
            "Lift Off (Planetary Fortress)":               github_icon_base_url + "blizzard/btn-ability-terran-liftoff.png",
            "Armament Stabilizers (Planetary Fortress)":   github_icon_base_url + "blizzard/btn-ability-mengsk-siegetank-flyingtankarmament.png",
            "Advanced Targeting (Planetary Fortress)":     github_icon_base_url + "blizzard/btn-ability-terran-detectionconedebuff.png",

            "Marine":                                      "https://static.wikia.nocookie.net/starcraft/images/4/47/Marine_SC2_Icon1.jpg",
            "Medic":                                       github_icon_base_url + "blizzard/btn-unit-terran-medic.png",
            "Firebat":                                     github_icon_base_url + "blizzard/btn-unit-terran-firebat.png",
            "Marauder":                                    "https://static.wikia.nocookie.net/starcraft/images/b/ba/Marauder_SC2_Icon1.jpg",
            "Reaper":                                      "https://static.wikia.nocookie.net/starcraft/images/7/7d/Reaper_SC2_Icon1.jpg",
            "Ghost":                                       "https://static.wikia.nocookie.net/starcraft/images/6/6e/Ghost_SC2_Icon1.jpg",
            "Spectre":                                     github_icon_base_url + "original/btn-unit-terran-spectre.png",
            "HERC":                                        github_icon_base_url + "blizzard/btn-unit-terran-herc.png",

            "Stimpack (Marine)":                           github_icon_base_url + "blizzard/btn-ability-terran-stimpack-color.png",
            "Super Stimpack (Marine)":                     github_icon_base_url + "blizzard/btn-upgrade-terran-superstimppack.png",
            "Combat Shield (Marine)":                      github_icon_base_url + "blizzard/btn-techupgrade-terran-combatshield-color.png",
            "Laser Targeting System (Marine)":             github_icon_base_url + "blizzard/btn-upgrade-terran-lazertargetingsystem.png",
            "Magrail Munitions (Marine)":                  github_icon_base_url + "blizzard/btn-upgrade-terran-magrailmunitions.png",
            "Optimized Logistics (Marine)":                github_icon_base_url + "blizzard/btn-upgrade-terran-optimizedlogistics.png",
            "Advanced Medic Facilities (Medic)":           organics_icon_base_url + "AdvancedMedicFacilities.png",
            "Stabilizer Medpacks (Medic)":                 github_icon_base_url + "blizzard/btn-upgrade-raynor-stabilizermedpacks.png",
            "Restoration (Medic)":                         github_icon_base_url + "original/btn-ability-terran-restoration@scbw.png",
            "Optical Flare (Medic)":                       github_icon_base_url + "blizzard/btn-upgrade-protoss-fenix-dragoonsolariteflare.png",
            "Resource Efficiency (Medic)":                 github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Adaptive Medpacks (Medic)":                   github_icon_base_url + "blizzard/btn-ability-terran-heal-color.png",
            "Nano Projector (Medic)":                      github_icon_base_url + "blizzard/talent-raynor-level03-firebatmedicrange.png",
            "Incinerator Gauntlets (Firebat)":             github_icon_base_url + "blizzard/btn-upgrade-raynor-incineratorgauntlets.png",
            "Juggernaut Plating (Firebat)":                github_icon_base_url + "blizzard/btn-upgrade-raynor-juggernautplating.png",
            "Stimpack (Firebat)":                          github_icon_base_url + "blizzard/btn-ability-terran-stimpack-color.png",
            "Super Stimpack (Firebat)":                    github_icon_base_url + "blizzard/btn-upgrade-terran-superstimppack.png",
            "Resource Efficiency (Firebat)":               github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Infernal Pre-Igniter (Firebat)":              github_icon_base_url + "blizzard/btn-upgrade-terran-infernalpreigniter.png",
            "Kinetic Foam (Firebat)":                      organics_icon_base_url + "KineticFoam.png",
            "Nano Projectors (Firebat)":                   github_icon_base_url + "blizzard/talent-raynor-level03-firebatmedicrange.png",
            "Concussive Shells (Marauder)":                github_icon_base_url + "blizzard/btn-ability-terran-punishergrenade-color.png",
            "Kinetic Foam (Marauder)":                     organics_icon_base_url + "KineticFoam.png",
            "Stimpack (Marauder)":                         github_icon_base_url + "blizzard/btn-ability-terran-stimpack-color.png",
            "Super Stimpack (Marauder)":                   github_icon_base_url + "blizzard/btn-upgrade-terran-superstimppack.png",
            "Laser Targeting System (Marauder)":           github_icon_base_url + "blizzard/btn-upgrade-terran-lazertargetingsystem.png",
            "Magrail Munitions (Marauder)":                github_icon_base_url + "blizzard/btn-upgrade-terran-magrailmunitions.png",
            "Internal Tech Module (Marauder)":             github_icon_base_url + "blizzard/btn-upgrade-terran-internalizedtechmodule.png",
            "Juggernaut Plating (Marauder)":               organics_icon_base_url + "JuggernautPlating.png",
            "U-238 Rounds (Reaper)":                       organics_icon_base_url + "U-238Rounds.png",
            "G-4 Clusterbomb (Reaper)":                    github_icon_base_url + "blizzard/btn-upgrade-terran-kd8chargeex3.png",
            "Stimpack (Reaper)":                           github_icon_base_url + "blizzard/btn-ability-terran-stimpack-color.png",
            "Super Stimpack (Reaper)":                     github_icon_base_url + "blizzard/btn-upgrade-terran-superstimppack.png",
            "Laser Targeting System (Reaper)":             github_icon_base_url + "blizzard/btn-upgrade-terran-lazertargetingsystem.png",
            "Advanced Cloaking Field (Reaper)":            github_icon_base_url + "original/btn-permacloak-reaper.png",
            "Spider Mines (Reaper)":                       github_icon_base_url + "original/btn-ability-terran-spidermine.png",
            "Combat Drugs (Reaper)":                       github_icon_base_url + "blizzard/btn-upgrade-terran-reapercombatdrugs.png",
            "Jet Pack Overdrive (Reaper)":                 github_icon_base_url + "blizzard/btn-ability-hornerhan-reaper-flightmode.png",
            "Ocular Implants (Ghost)":                     organics_icon_base_url + "OcularImplants.png",
            "Crius Suit (Ghost)":                          github_icon_base_url + "original/btn-permacloak-ghost.png",
            "EMP Rounds (Ghost)":                          github_icon_base_url + "blizzard/btn-ability-terran-emp-color.png",
            "Lockdown (Ghost)":                            github_icon_base_url + "original/btn-abilty-terran-lockdown@scbw.png",
            "Resource Efficiency (Ghost)":                 github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Psionic Lash (Spectre)":                      organics_icon_base_url + "PsionicLash.png",
            "Nyx-Class Cloaking Module (Spectre)":         github_icon_base_url + "original/btn-permacloak-spectre.png",
            "Impaler Rounds (Spectre)":                    github_icon_base_url + "blizzard/btn-techupgrade-terran-impalerrounds.png",
            "Resource Efficiency (Spectre)":               github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Juggernaut Plating (HERC)":                   organics_icon_base_url + "JuggernautPlating.png",
            "Kinetic Foam (HERC)":                         organics_icon_base_url + "KineticFoam.png",
            "Resource Efficiency (HERC)":                  github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",

            "Hellion":                                     "https://static.wikia.nocookie.net/starcraft/images/5/56/Hellion_SC2_Icon1.jpg",
            "Vulture":                                     github_icon_base_url + "blizzard/btn-unit-terran-vulture.png",
            "Goliath":                                     github_icon_base_url + "blizzard/btn-unit-terran-goliath.png",
            "Diamondback":                                 github_icon_base_url + "blizzard/btn-unit-terran-cobra.png",
            "Siege Tank":                                  "https://static.wikia.nocookie.net/starcraft/images/5/57/SiegeTank_SC2_Icon1.jpg",
            "Thor":                                        "https://static.wikia.nocookie.net/starcraft/images/e/ef/Thor_SC2_Icon1.jpg",
            "Predator":                                    github_icon_base_url + "original/btn-unit-terran-predator.png",
            "Widow Mine":                                  github_icon_base_url + "blizzard/btn-unit-terran-widowmine.png",
            "Cyclone":                                     github_icon_base_url + "blizzard/btn-unit-terran-cyclone.png",
            "Warhound":                                    github_icon_base_url + "blizzard/btn-unit-terran-warhound.png",

            "Twin-Linked Flamethrower (Hellion)":          github_icon_base_url + "blizzard/btn-upgrade-mengsk-trooper-flamethrower.png",
            "Thermite Filaments (Hellion)":                github_icon_base_url + "blizzard/btn-upgrade-terran-infernalpreigniter.png",
            "Hellbat Aspect (Hellion)":                    github_icon_base_url + "blizzard/btn-unit-terran-hellionbattlemode.png",
            "Smart Servos (Hellion)":                      github_icon_base_url + "blizzard/btn-upgrade-terran-transformationservos.png",
            "Optimized Logistics (Hellion)":               github_icon_base_url + "blizzard/btn-upgrade-terran-optimizedlogistics.png",
            "Jump Jets (Hellion)":                         github_icon_base_url + "blizzard/btn-upgrade-terran-jumpjets.png",
            "Stimpack (Hellion)":                          github_icon_base_url + "blizzard/btn-ability-terran-stimpack-color.png",
            "Super Stimpack (Hellion)":                    github_icon_base_url + "blizzard/btn-upgrade-terran-superstimppack.png",
            "Infernal Plating (Hellion)":                  github_icon_base_url + "blizzard/btn-upgrade-swann-hellarmor.png",
            "Cerberus Mine (Spider Mine)":                 github_icon_base_url + "blizzard/btn-upgrade-raynor-cerberusmines.png",
            "High Explosive Munition (Spider Mine)":       github_icon_base_url + "original/btn-ability-terran-spidermine.png",
            "Replenishable Magazine (Vulture)":            github_icon_base_url + "blizzard/btn-upgrade-raynor-replenishablemagazine.png",
            "Replenishable Magazine (Free) (Vulture)":     github_icon_base_url + "blizzard/btn-upgrade-raynor-replenishablemagazine.png",
            "Ion Thrusters (Vulture)":                     github_icon_base_url + "blizzard/btn-ability-terran-emergencythrusters.png",
            "Auto Launchers (Vulture)":                    github_icon_base_url + "blizzard/btn-upgrade-terran-jotunboosters.png",
            "Auto-Repair (Vulture)":                       github_icon_base_url + "blizzard/ui_tipicon_campaign_space01-repair.png",
            "Multi-Lock Weapons System (Goliath)":         github_icon_base_url + "blizzard/btn-upgrade-swann-multilockweaponsystem.png",
            "Ares-Class Targeting System (Goliath)":       github_icon_base_url + "blizzard/btn-upgrade-swann-aresclasstargetingsystem.png",
            "Jump Jets (Goliath)":                         github_icon_base_url + "blizzard/btn-upgrade-terran-jumpjets.png",
            "Optimized Logistics (Goliath)":               github_icon_base_url + "blizzard/btn-upgrade-terran-optimizedlogistics.png",
            "Shaped Hull (Goliath)":                       organics_icon_base_url + "ShapedHull.png",
            "Resource Efficiency (Goliath)":               github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Internal Tech Module (Goliath)":              github_icon_base_url + "blizzard/btn-upgrade-terran-internalizedtechmodule.png",
            "Tri-Lithium Power Cell (Diamondback)":        github_icon_base_url + "original/btn-upgrade-terran-trilithium-power-cell.png",
            "Tungsten Spikes (Diamondback)":               github_icon_base_url + "original/btn-upgrade-terran-tungsten-spikes.png",
            "Shaped Hull (Diamondback)":                   organics_icon_base_url + "ShapedHull.png",
            "Hyperfluxor (Diamondback)":                   github_icon_base_url + "blizzard/btn-upgrade-mengsk-engineeringbay-orbitaldrop.png",
            "Burst Capacitors (Diamondback)":              github_icon_base_url + "blizzard/btn-ability-terran-electricfield.png",
            "Ion Thrusters (Diamondback)":                 github_icon_base_url + "blizzard/btn-ability-terran-emergencythrusters.png",
            "Resource Efficiency (Diamondback)":           github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Maelstrom Rounds (Siege Tank)":               github_icon_base_url + "blizzard/btn-upgrade-raynor-maelstromrounds.png",
            "Shaped Blast (Siege Tank)":                   organics_icon_base_url + "ShapedBlast.png",
            "Jump Jets (Siege Tank)":                      github_icon_base_url + "blizzard/btn-upgrade-terran-jumpjets.png",
            "Spider Mines (Siege Tank)":                   github_icon_base_url + "blizzard/btn-upgrade-siegetank-spidermines.png",
            "Smart Servos (Siege Tank)":                   github_icon_base_url + "blizzard/btn-upgrade-terran-transformationservos.png",
            "Graduating Range (Siege Tank)":               github_icon_base_url + "blizzard/btn-upgrade-terran-nova-siegetankrange.png",
            "Laser Targeting System (Siege Tank)":         github_icon_base_url + "blizzard/btn-upgrade-terran-lazertargetingsystem.png",
            "Advanced Siege Tech (Siege Tank)":            github_icon_base_url + "blizzard/btn-upgrade-raynor-improvedsiegemode.png",
            "Internal Tech Module (Siege Tank)":           github_icon_base_url + "blizzard/btn-upgrade-terran-internalizedtechmodule.png",
            "Shaped Hull (Siege Tank)":                    organics_icon_base_url + "ShapedHull.png",
            "Resource Efficiency (Siege Tank)":            github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "330mm Barrage Cannon (Thor)":                 github_icon_base_url + "original/btn-ability-thor-330mm.png",
            "Immortality Protocol (Thor)":                 github_icon_base_url + "blizzard/btn-techupgrade-terran-immortalityprotocol.png",
            "Immortality Protocol (Free) (Thor)":          github_icon_base_url + "blizzard/btn-techupgrade-terran-immortalityprotocol.png",
            "High Impact Payload (Thor)":                  github_icon_base_url + "blizzard/btn-unit-terran-thorsiegemode.png",
            "Smart Servos (Thor)":                         github_icon_base_url + "blizzard/btn-upgrade-terran-transformationservos.png",
            "Button With a Skull on It (Thor)":            github_icon_base_url + "blizzard/btn-ability-terran-nuclearstrike-color.png",
            "Laser Targeting System (Thor)":               github_icon_base_url + "blizzard/btn-upgrade-terran-lazertargetingsystem.png",
            "Large Scale Field Construction (Thor)":       github_icon_base_url + "blizzard/talent-swann-level12-immortalityprotocol.png",
            "Resource Efficiency (Predator)":              github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Cloak (Predator)":                            github_icon_base_url + "blizzard/btn-ability-terran-cloak-color.png",
            "Charge (Predator)":                           github_icon_base_url + "blizzard/btn-ability-protoss-charge-color.png",
            "Predator's Fury (Predator)":                  github_icon_base_url + "blizzard/btn-ability-protoss-shadowfury.png",
            "Drilling Claws (Widow Mine)":                 github_icon_base_url + "blizzard/btn-upgrade-terran-researchdrillingclaws.png",
            "Concealment (Widow Mine)":                    github_icon_base_url + "blizzard/btn-ability-terran-widowminehidden.png",
            "Black Market Launchers (Widow Mine)":         github_icon_base_url + "blizzard/btn-ability-hornerhan-widowmine-attackrange.png",
            "Executioner Missiles (Widow Mine)":           github_icon_base_url + "blizzard/btn-ability-hornerhan-widowmine-deathblossom.png",
            "Mag-Field Accelerators (Cyclone)":            github_icon_base_url + "blizzard/btn-upgrade-terran-magfieldaccelerator.png",
            "Mag-Field Launchers (Cyclone)":               github_icon_base_url + "blizzard/btn-upgrade-terran-cyclonerangeupgrade.png",
            "Targeting Optics (Cyclone)":                  github_icon_base_url + "blizzard/btn-upgrade-swann-targetingoptics.png",
            "Rapid Fire Launchers (Cyclone)":              github_icon_base_url + "blizzard/btn-upgrade-raynor-ripwavemissiles.png",
            "Resource Efficiency (Cyclone)":               github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Internal Tech Module (Cyclone)":              github_icon_base_url + "blizzard/btn-upgrade-terran-internalizedtechmodule.png",
            "Resource Efficiency (Warhound)":              github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Reinforced Plating (Warhound)":               github_icon_base_url + "original/btn-research-zerg-fortifiedbunker.png",

            "Medivac":                                     "https://static.wikia.nocookie.net/starcraft/images/d/db/Medivac_SC2_Icon1.jpg",
            "Wraith":                                      github_icon_base_url + "blizzard/btn-unit-terran-wraith.png",
            "Viking":                                      "https://static.wikia.nocookie.net/starcraft/images/2/2a/Viking_SC2_Icon1.jpg",
            "Banshee":                                     "https://static.wikia.nocookie.net/starcraft/images/3/32/Banshee_SC2_Icon1.jpg",
            "Battlecruiser":                               "https://static.wikia.nocookie.net/starcraft/images/f/f5/Battlecruiser_SC2_Icon1.jpg",
            "Raven":                                       "https://static.wikia.nocookie.net/starcraft/images/1/19/SC2_Lab_Raven_Icon.png",
            "Science Vessel":                              "https://static.wikia.nocookie.net/starcraft/images/c/c3/SC2_Lab_SciVes_Icon.png",
            "Hercules":                                    "https://static.wikia.nocookie.net/starcraft/images/4/40/SC2_Lab_Hercules_Icon.png",
            "Liberator":                                   github_icon_base_url + "blizzard/btn-unit-terran-liberator.png",
            "Valkyrie":                                    github_icon_base_url + "original/btn-unit-terran-valkyrie@scbw.png",

            "Rapid Deployment Tube (Medivac)":             organics_icon_base_url + "RapidDeploymentTube.png",
            "Advanced Healing AI (Medivac)":               github_icon_base_url + "blizzard/btn-ability-mengsk-medivac-doublehealbeam.png",
            "Expanded Hull (Medivac)":                     github_icon_base_url + "blizzard/btn-upgrade-mengsk-engineeringbay-neosteelfortifiedarmor.png",
            "Afterburners (Medivac)":                      github_icon_base_url + "blizzard/btn-upgrade-terran-medivacemergencythrusters.png",
            "Scatter Veil (Medivac)":                      github_icon_base_url + "blizzard/btn-upgrade-swann-defensivematrix.png",
            "Advanced Cloaking Field (Medivac)":           github_icon_base_url + "original/btn-permacloak-medivac.png",
            "Tomahawk Power Cells (Wraith)":               organics_icon_base_url + "TomahawkPowerCells.png",
            "Unregistered Cloaking Module (Wraith)":       github_icon_base_url + "original/btn-permacloak-wraith.png",
            "Trigger Override (Wraith)":                   github_icon_base_url + "blizzard/btn-ability-hornerhan-wraith-attackspeed.png",
            "Internal Tech Module (Wraith)":               github_icon_base_url + "blizzard/btn-upgrade-terran-internalizedtechmodule.png",
            "Resource Efficiency (Wraith)":                github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Displacement Field (Wraith)":                 github_icon_base_url + "blizzard/btn-upgrade-swann-displacementfield.png",
            "Advanced Laser Technology (Wraith)":          github_icon_base_url + "blizzard/btn-upgrade-swann-improvedburstlaser.png",
            "Ripwave Missiles (Viking)":                   github_icon_base_url + "blizzard/btn-upgrade-raynor-ripwavemissiles.png",
            "Phobos-Class Weapons System (Viking)":        github_icon_base_url + "blizzard/btn-upgrade-raynor-phobosclassweaponssystem.png",
            "Smart Servos (Viking)":                       github_icon_base_url + "blizzard/btn-upgrade-terran-transformationservos.png",
            "Anti-Mechanical Munition (Viking)":           github_icon_base_url + "blizzard/btn-ability-terran-ignorearmor.png",
            "Shredder Rounds (Viking)":                    github_icon_base_url + "blizzard/btn-ability-hornerhan-viking-piercingattacks.png",
            "W.I.L.D. Missiles (Viking)":                  github_icon_base_url + "blizzard/btn-ability-hornerhan-viking-missileupgrade.png",
            "Cross-Spectrum Dampeners (Banshee)":          github_icon_base_url + "original/btn-banshee-cross-spectrum-dampeners.png",
            "Advanced Cross-Spectrum Dampeners (Banshee)": github_icon_base_url + "original/btn-permacloak-banshee.png",
            "Shockwave Missile Battery (Banshee)":         github_icon_base_url + "blizzard/btn-upgrade-raynor-shockwavemissilebattery.png",
            "Hyperflight Rotors (Banshee)":                github_icon_base_url + "blizzard/btn-upgrade-terran-hyperflightrotors.png",
            "Laser Targeting System (Banshee)":            github_icon_base_url + "blizzard/btn-upgrade-terran-lazertargetingsystem.png",
            "Internal Tech Module (Banshee)":              github_icon_base_url + "blizzard/btn-upgrade-terran-internalizedtechmodule.png",
            "Shaped Hull (Banshee)":                       organics_icon_base_url + "ShapedHull.png",
            "Advanced Targeting Optics (Banshee)":         github_icon_base_url + "blizzard/btn-ability-terran-detectionconedebuff.png",
            "Distortion Blasters (Banshee)":               github_icon_base_url + "blizzard/btn-techupgrade-terran-cloakdistortionfield.png",
            "Rocket Barrage (Banshee)":                    github_icon_base_url + "blizzard/btn-upgrade-terran-nova-bansheemissilestrik.png",
            "Missile Pods (Battlecruiser) Level 1":        organics_icon_base_url + "MissilePods.png",
            "Missile Pods (Battlecruiser) Level 2":        github_icon_base_url + "blizzard/btn-upgrade-terran-nova-bansheemissilestrik.png",
            "Defensive Matrix (Battlecruiser)":            github_icon_base_url + "blizzard/btn-upgrade-swann-defensivematrix.png",
            "Advanced Defensive Matrix (Battlecruiser)":   github_icon_base_url + "blizzard/btn-upgrade-swann-defensivematrix.png",
            "Tactical Jump (Battlecruiser)":               github_icon_base_url + "blizzard/btn-ability-terran-warpjump.png",
            "Cloak (Battlecruiser)":                       github_icon_base_url + "blizzard/btn-ability-terran-cloak-color.png",
            "ATX Laser Battery (Battlecruiser)":           github_icon_base_url + "blizzard/btn-upgrade-terran-nova-specialordance.png",
            "Optimized Logistics (Battlecruiser)":         github_icon_base_url + "blizzard/btn-upgrade-terran-optimizedlogistics.png",
            "Internal Tech Module (Battlecruiser)":        github_icon_base_url + "blizzard/btn-upgrade-terran-internalizedtechmodule.png",
            "Behemoth Plating (Battlecruiser)":            github_icon_base_url + "original/btn-research-zerg-fortifiedbunker.png",
            "Covert Ops Engines (Battlecruiser)":          github_icon_base_url + "blizzard/btn-ability-terran-emergencythrusters.png",
            "Bio Mechanical Repair Drone (Raven)":         github_icon_base_url + "blizzard/btn-unit-biomechanicaldrone.png",
            "Spider Mines (Raven)":                        github_icon_base_url + "blizzard/btn-upgrade-siegetank-spidermines.png",
            "Railgun Turret (Raven)":                      github_icon_base_url + "blizzard/btn-unit-terran-autoturretblackops.png",
            "Hunter-Seeker Weapon (Raven)":                github_icon_base_url + "blizzard/btn-upgrade-terran-nova-specialordance.png",
            "Interference Matrix (Raven)":                 github_icon_base_url + "blizzard/btn-upgrade-terran-interferencematrix.png",
            "Anti-Armor Missile (Raven)":                  github_icon_base_url + "blizzard/btn-ability-terran-shreddermissile-color.png",
            "Internal Tech Module (Raven)":                github_icon_base_url + "blizzard/btn-upgrade-terran-internalizedtechmodule.png",
            "Resource Efficiency (Raven)":                 github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Durable Materials (Raven)":                   github_icon_base_url + "blizzard/btn-upgrade-terran-durablematerials.png",
            "EMP Shockwave (Science Vessel)":              github_icon_base_url + "blizzard/btn-ability-mengsk-ghost-staticempblast.png",
            "Defensive Matrix (Science Vessel)":           github_icon_base_url + "blizzard/btn-upgrade-swann-defensivematrix.png",
            "Improved Nano-Repair (Science Vessel)":       github_icon_base_url + "blizzard/btn-upgrade-swann-improvednanorepair.png",
            "Advanced AI Systems (Science Vessel)":        github_icon_base_url + "blizzard/btn-ability-mengsk-medivac-doublehealbeam.png",
            "Internal Fusion Module (Hercules)":           github_icon_base_url + "blizzard/btn-upgrade-terran-internalizedtechmodule.png",
            "Tactical Jump (Hercules)":                    github_icon_base_url + "blizzard/btn-ability-terran-hercules-tacticaljump.png",
            "Advanced Ballistics (Liberator)":             github_icon_base_url + "blizzard/btn-upgrade-terran-advanceballistics.png",
            "Raid Artillery (Liberator)":                  github_icon_base_url + "blizzard/btn-upgrade-terran-nova-terrandefendermodestructureattack.png",
            "Cloak (Liberator)":                           github_icon_base_url + "blizzard/btn-ability-terran-cloak-color.png",
            "Laser Targeting System (Liberator)":          github_icon_base_url + "blizzard/btn-upgrade-terran-lazertargetingsystem.png",
            "Optimized Logistics (Liberator)":             github_icon_base_url + "blizzard/btn-upgrade-terran-optimizedlogistics.png",
            "Smart Servos (Liberator)":                    github_icon_base_url + "blizzard/btn-upgrade-terran-transformationservos.png",
            "Resource Efficiency (Liberator)":             github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Enhanced Cluster Launchers (Valkyrie)":       github_icon_base_url + "blizzard/btn-ability-stetmann-corruptormissilebarrage.png",
            "Shaped Hull (Valkyrie)":                      organics_icon_base_url + "ShapedHull.png",
            "Flechette Missiles (Valkyrie)":               github_icon_base_url + "blizzard/btn-ability-hornerhan-viking-missileupgrade.png",
            "Afterburners (Valkyrie)":                     github_icon_base_url + "blizzard/btn-upgrade-terran-medivacemergencythrusters.png",
            "Launching Vector Compensator (Valkyrie)":     github_icon_base_url + "blizzard/btn-ability-terran-emergencythrusters.png",
            "Resource Efficiency (Valkyrie)":              github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",

            "War Pigs":                                    "https://static.wikia.nocookie.net/starcraft/images/e/ed/WarPigs_SC2_Icon1.jpg",
            "Devil Dogs":                                  "https://static.wikia.nocookie.net/starcraft/images/3/33/DevilDogs_SC2_Icon1.jpg",
            "Hammer Securities":                           "https://static.wikia.nocookie.net/starcraft/images/3/3b/HammerSecurity_SC2_Icon1.jpg",
            "Spartan Company":                             "https://static.wikia.nocookie.net/starcraft/images/b/be/SpartanCompany_SC2_Icon1.jpg",
            "Siege Breakers":                              "https://static.wikia.nocookie.net/starcraft/images/3/31/SiegeBreakers_SC2_Icon1.jpg",
            "Hel's Angels":                                "https://static.wikia.nocookie.net/starcraft/images/6/63/HelsAngels_SC2_Icon1.jpg",
            "Dusk Wings":                                  "https://static.wikia.nocookie.net/starcraft/images/5/52/DuskWings_SC2_Icon1.jpg",
            "Jackson's Revenge":                           "https://static.wikia.nocookie.net/starcraft/images/9/95/JacksonsRevenge_SC2_Icon1.jpg",
            "Skibi's Angels":                              github_icon_base_url + "blizzard/btn-unit-terran-medicelite.png",
            "Death Heads":                                 github_icon_base_url + "blizzard/btn-unit-terran-deathhead.png",
            "Winged Nightmares":                           github_icon_base_url + "blizzard/btn-unit-collection-wraith-junker.png",
            "Midnight Riders":                             github_icon_base_url + "blizzard/btn-unit-terran-liberatorblackops.png",
            "Brynhilds":                                   github_icon_base_url + "blizzard/btn-unit-collection-vikingfighter-covertops.png",
            "Jotun":                                       github_icon_base_url + "blizzard/btn-unit-terran-thormengsk.png",

            "Ultra-Capacitors":                            "https://static.wikia.nocookie.net/starcraft/images/2/23/SC2_Lab_Ultra_Capacitors_Icon.png",
            "Vanadium Plating":                            "https://static.wikia.nocookie.net/starcraft/images/6/67/SC2_Lab_VanPlating_Icon.png",
            "Orbital Depots":                              "https://static.wikia.nocookie.net/starcraft/images/0/01/SC2_Lab_Orbital_Depot_Icon.png",
            "Micro-Filtering":                             "https://static.wikia.nocookie.net/starcraft/images/2/20/SC2_Lab_MicroFilter_Icon.png",
            "Automated Refinery":                          "https://static.wikia.nocookie.net/starcraft/images/7/71/SC2_Lab_Auto_Refinery_Icon.png",
            "Command Center Reactor":                      "https://static.wikia.nocookie.net/starcraft/images/e/ef/SC2_Lab_CC_Reactor_Icon.png",
            "Tech Reactor":                                "https://static.wikia.nocookie.net/starcraft/images/c/c5/SC2_Lab_Tech_Reactor_Icon.png",
            "Orbital Strike":                              "https://static.wikia.nocookie.net/starcraft/images/d/df/SC2_Lab_Orb_Strike_Icon.png",

            "Shrike Turret (Bunker)":                      "https://static.wikia.nocookie.net/starcraft/images/4/44/SC2_Lab_Shrike_Turret_Icon.png",
            "Fortified Bunker (Bunker)":                   "https://static.wikia.nocookie.net/starcraft/images/4/4f/SC2_Lab_FortBunker_Icon.png",
            "Planetary Fortress":                          "https://static.wikia.nocookie.net/starcraft/images/0/0b/SC2_Lab_PlanetFortress_Icon.png",
            "Perdition Turret":                            "https://static.wikia.nocookie.net/starcraft/images/a/af/SC2_Lab_PerdTurret_Icon.png",
            "Cellular Reactor":                            "https://static.wikia.nocookie.net/starcraft/images/d/d8/SC2_Lab_CellReactor_Icon.png",
            "Regenerative Bio-Steel Level 1":              github_icon_base_url + "original/btn-regenerativebiosteel-green.png",
            "Regenerative Bio-Steel Level 2":              github_icon_base_url + "original/btn-regenerativebiosteel-blue.png",
            "Regenerative Bio-Steel Level 3":              github_icon_base_url + "blizzard/btn-research-zerg-regenerativebio-steel.png",
            "Hive Mind Emulator":                          "https://static.wikia.nocookie.net/starcraft/images/b/bc/SC2_Lab_Hive_Emulator_Icon.png",
            "Psi Disrupter":                               "https://static.wikia.nocookie.net/starcraft/images/c/cf/SC2_Lab_Psi_Disruptor_Icon.png",

            "Structure Armor":                             github_icon_base_url + "blizzard/btn-upgrade-terran-buildingarmor.png",
            "Hi-Sec Auto Tracking":                        github_icon_base_url + "blizzard/btn-upgrade-terran-hisecautotracking.png",
            "Advanced Optics":                             github_icon_base_url + "blizzard/btn-upgrade-swann-vehiclerangeincrease.png",
            "Rogue Forces":                                github_icon_base_url + "blizzard/btn-unit-terran-tosh.png",

            "Ghost Visor (Nova Equipment)":                github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-ghostvisor.png",
            "Rangefinder Oculus (Nova Equipment)":         github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-rangefinderoculus.png",
            "Domination (Nova Ability)":                   github_icon_base_url + "blizzard/btn-ability-nova-domination.png",
            "Blink (Nova Ability)":                        github_icon_base_url + "blizzard/btn-upgrade-nova-blink.png",
            "Stealth Suit Module (Nova Suit Module)":      github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-stealthsuit.png",
            "Cloak (Nova Suit Module)":                    github_icon_base_url + "blizzard/btn-ability-terran-cloak-color.png",
            "Permanently Cloaked (Nova Suit Module)":      github_icon_base_url + "blizzard/btn-upgrade-nova-tacticalstealthsuit.png",
            "Energy Suit Module (Nova Suit Module)":       github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-apolloinfantrysuit.png",
            "Armored Suit Module (Nova Suit Module)":      github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-blinksuit.png",
            "Jump Suit Module (Nova Suit Module)":         github_icon_base_url + "blizzard/btn-upgrade-nova-jetpack.png",
            "C20A Canister Rifle (Nova Weapon)":           github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-canisterrifle.png",
            "Hellfire Shotgun (Nova Weapon)":              github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-shotgun.png",
            "Plasma Rifle (Nova Weapon)":                  github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-plasmagun.png",
            "Monomolecular Blade (Nova Weapon)":           github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-monomolecularblade.png",
            "Blazefire Gunblade (Nova Weapon)":            github_icon_base_url + "blizzard/btn-upgrade-nova-equipment-gunblade_sword.png",
            "Stim Infusion (Nova Gadget)":                 github_icon_base_url + "blizzard/btn-upgrade-terran-superstimppack.png",
            "Pulse Grenades (Nova Gadget)":                github_icon_base_url + "blizzard/btn-upgrade-nova-btn-upgrade-nova-pulsegrenade.png",
            "Flashbang Grenades (Nova Gadget)":            github_icon_base_url + "blizzard/btn-upgrade-nova-btn-upgrade-nova-flashgrenade.png",
            "Ionic Force Field (Nova Gadget)":             github_icon_base_url + "blizzard/btn-upgrade-terran-nova-personaldefensivematrix.png",
            "Holo Decoy (Nova Gadget)":                    github_icon_base_url + "blizzard/btn-upgrade-nova-holographicdecoy.png",
            "Tac Nuke Strike (Nova Ability)":              github_icon_base_url + "blizzard/btn-ability-terran-nuclearstrike-color.png",

            "Zerg Melee Attack Level 1":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-meleeattacks-level1.png",
            "Zerg Melee Attack Level 2":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-meleeattacks-level2.png",
            "Zerg Melee Attack Level 3":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-meleeattacks-level3.png",
            "Zerg Missile Attack Level 1":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-missileattacks-level1.png",
            "Zerg Missile Attack Level 2":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-missileattacks-level2.png",
            "Zerg Missile Attack Level 3":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-missileattacks-level3.png",
            "Zerg Ground Carapace Level 1":                github_icon_base_url + "blizzard/btn-upgrade-zerg-groundcarapace-level1.png",
            "Zerg Ground Carapace Level 2":                github_icon_base_url + "blizzard/btn-upgrade-zerg-groundcarapace-level2.png",
            "Zerg Ground Carapace Level 3":                github_icon_base_url + "blizzard/btn-upgrade-zerg-groundcarapace-level3.png",
            "Zerg Flyer Attack Level 1":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-airattacks-level1.png",
            "Zerg Flyer Attack Level 2":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-airattacks-level2.png",
            "Zerg Flyer Attack Level 3":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-airattacks-level3.png",
            "Zerg Flyer Carapace Level 1":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-flyercarapace-level1.png",
            "Zerg Flyer Carapace Level 2":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-flyercarapace-level2.png",
            "Zerg Flyer Carapace Level 3":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-flyercarapace-level3.png",

            "Automated Extractors (Kerrigan Tier 3)":      github_icon_base_url + "blizzard/btn-ability-kerrigan-automatedextractors.png",
            "Vespene Efficiency (Kerrigan Tier 5)":        github_icon_base_url + "blizzard/btn-ability-kerrigan-vespeneefficiency.png",
            "Twin Drones (Kerrigan Tier 5)":               github_icon_base_url + "blizzard/btn-ability-kerrigan-twindrones.png",
            "Improved Overlords (Kerrigan Tier 3)":        github_icon_base_url + "blizzard/btn-ability-kerrigan-improvedoverlords.png",
            "Ventral Sacs (Overlord)":                     github_icon_base_url + "blizzard/btn-upgrade-zerg-ventralsacs.png",
            "Malignant Creep (Kerrigan Tier 5)":           github_icon_base_url + "blizzard/btn-ability-kerrigan-malignantcreep.png",

            "Spine Crawler":                               github_icon_base_url + "blizzard/btn-building-zerg-spinecrawler.png",
            "Spore Crawler":                               github_icon_base_url + "blizzard/btn-building-zerg-sporecrawler.png",

            "Zergling":                                    github_icon_base_url + "blizzard/btn-unit-zerg-zergling.png",
            "Swarm Queen":                                 github_icon_base_url + "blizzard/btn-unit-zerg-broodqueen.png",
            "Roach":                                       github_icon_base_url + "blizzard/btn-unit-zerg-roach.png",
            "Hydralisk":                                   github_icon_base_url + "blizzard/btn-unit-zerg-hydralisk.png",
            "Aberration":                                  github_icon_base_url + "blizzard/btn-unit-zerg-aberration.png",
            "Mutalisk":                                    github_icon_base_url + "blizzard/btn-unit-zerg-mutalisk.png",
            "Corruptor":                                   github_icon_base_url + "blizzard/btn-unit-zerg-corruptor.png",
            "Swarm Host":                                  github_icon_base_url + "blizzard/btn-unit-zerg-swarmhost.png",
            "Infestor":                                    github_icon_base_url + "blizzard/btn-unit-zerg-infestor.png",
            "Defiler":                                     github_icon_base_url + "original/btn-unit-zerg-defiler@scbw.png",
            "Ultralisk":                                   github_icon_base_url + "blizzard/btn-unit-zerg-ultralisk.png",
            "Brood Queen":                                 github_icon_base_url + "blizzard/btn-unit-zerg-classicqueen.png",
            "Scourge":                                     github_icon_base_url + "blizzard/btn-unit-zerg-scourge.png",

            "Baneling Aspect (Zergling)":                  github_icon_base_url + "blizzard/btn-unit-zerg-baneling.png",
            "Ravager Aspect (Roach)":                      github_icon_base_url + "blizzard/btn-unit-zerg-ravager.png",
            "Impaler Aspect (Hydralisk)":                  github_icon_base_url + "blizzard/btn-unit-zerg-impaler.png",
            "Lurker Aspect (Hydralisk)":                   github_icon_base_url + "blizzard/btn-unit-zerg-lurker.png",
            "Brood Lord Aspect (Mutalisk/Corruptor)":      github_icon_base_url + "blizzard/btn-unit-zerg-broodlord.png",
            "Viper Aspect (Mutalisk/Corruptor)":           github_icon_base_url + "blizzard/btn-unit-zerg-viper.png",
            "Guardian Aspect (Mutalisk/Corruptor)":        github_icon_base_url + "blizzard/btn-unit-zerg-primalguardian.png",
            "Devourer Aspect (Mutalisk/Corruptor)":        github_icon_base_url + "blizzard/btn-unit-zerg-devourerex3.png",

            "Raptor Strain (Zergling)":                    github_icon_base_url + "blizzard/btn-unit-zerg-zergling-raptor.png",
            "Swarmling Strain (Zergling)":                 github_icon_base_url + "blizzard/btn-unit-zerg-zergling-swarmling.png",
            "Hardened Carapace (Zergling)":                github_icon_base_url + "blizzard/btn-upgrade-zerg-hardenedcarapace.png",
            "Adrenal Overload (Zergling)":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-adrenaloverload.png",
            "Metabolic Boost (Zergling)":                  github_icon_base_url + "blizzard/btn-upgrade-zerg-hotsmetabolicboost.png",
            "Shredding Claws (Zergling)":                  github_icon_base_url + "blizzard/btn-upgrade-zergling-armorshredding.png",
            "Zergling Reconstitution (Kerrigan Tier 3)":   github_icon_base_url + "blizzard/btn-ability-kerrigan-zerglingreconstitution.png",
            "Splitter Strain (Baneling)":                  github_icon_base_url + "blizzard/talent-zagara-level14-unlocksplitterling.png",
            "Hunter Strain (Baneling)":                    github_icon_base_url + "blizzard/btn-ability-zerg-cliffjump-baneling.png",
            "Corrosive Acid (Baneling)":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-corrosiveacid.png",
            "Rupture (Baneling)":                          github_icon_base_url + "blizzard/btn-upgrade-zerg-rupture.png",
            "Regenerative Acid (Baneling)":                github_icon_base_url + "blizzard/btn-upgrade-zerg-regenerativebile.png",
            "Centrifugal Hooks (Baneling)":                github_icon_base_url + "blizzard/btn-upgrade-zerg-centrifugalhooks.png",
            "Tunneling Jaws (Baneling)":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-tunnelingjaws.png",
            "Rapid Metamorph (Baneling)":                  github_icon_base_url + "blizzard/btn-upgrade-terran-optimizedlogistics.png",
            "Spawn Larvae (Swarm Queen)":                  github_icon_base_url + "blizzard/btn-unit-zerg-larva.png",
            "Deep Tunnel (Swarm Queen)":                   github_icon_base_url + "blizzard/btn-ability-zerg-deeptunnel.png",
            "Organic Carapace (Swarm Queen)":              github_icon_base_url + "blizzard/btn-upgrade-zerg-organiccarapace.png",
            "Bio-Mechanical Transfusion (Swarm Queen)":    github_icon_base_url + "blizzard/btn-upgrade-zerg-abathur-biomechanicaltransfusion.png",
            "Resource Efficiency (Swarm Queen)":           github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Incubator Chamber (Swarm Queen)":             github_icon_base_url + "blizzard/btn-upgrade-zerg-abathur-incubationchamber.png",
            "Vile Strain (Roach)":                         github_icon_base_url + "blizzard/btn-unit-zerg-roach-vile.png",
            "Corpser Strain (Roach)":                      github_icon_base_url + "blizzard/btn-unit-zerg-roach-corpser.png",
            "Hydriodic Bile (Roach)":                      github_icon_base_url + "blizzard/btn-upgrade-zerg-hydriaticacid.png",
            "Adaptive Plating (Roach)":                    github_icon_base_url + "blizzard/btn-upgrade-zerg-adaptivecarapace.png",
            "Tunneling Claws (Roach)":                     github_icon_base_url + "blizzard/btn-upgrade-zerg-hotstunnelingclaws.png",
            "Glial Reconstitution (Roach)":                github_icon_base_url + "blizzard/btn-upgrade-zerg-glialreconstitution.png",
            "Organic Carapace (Roach)":                    github_icon_base_url + "blizzard/btn-upgrade-zerg-organiccarapace.png",
            "Potent Bile (Ravager)":                       github_icon_base_url + "blizzard/potentbile_coop.png",
            "Bloated Bile Ducts (Ravager)":                github_icon_base_url + "blizzard/btn-ability-zerg-abathur-corrosivebilelarge.png",
            "Deep Tunnel (Ravager)":                       github_icon_base_url + "blizzard/btn-ability-zerg-deeptunnel.png",
            "Frenzy (Hydralisk)":                          github_icon_base_url + "blizzard/btn-upgrade-zerg-frenzy.png",
            "Ancillary Carapace (Hydralisk)":              github_icon_base_url + "blizzard/btn-upgrade-zerg-ancillaryarmor.png",
            "Grooved Spines (Hydralisk)":                  github_icon_base_url + "blizzard/btn-upgrade-zerg-hotsgroovedspines.png",
            "Muscular Augments (Hydralisk)":               github_icon_base_url + "blizzard/btn-upgrade-zerg-evolvemuscularaugments.png",
            "Resource Efficiency (Hydralisk)":             github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Adaptive Talons (Impaler)":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-adaptivetalons.png",
            "Secretion Glands (Impaler)":                  github_icon_base_url + "blizzard/btn-ability-zerg-creepspread.png",
            "Hardened Tentacle Spines (Impaler)":          github_icon_base_url + "blizzard/btn-ability-zerg-dehaka-impaler-tenderize.png",
            "Seismic Spines (Lurker)":                     github_icon_base_url + "blizzard/btn-upgrade-kerrigan-seismicspines.png",
            "Adapted Spines (Lurker)":                     github_icon_base_url + "blizzard/btn-upgrade-zerg-groovedspines.png",
            "Vicious Glaive (Mutalisk)":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-viciousglaive.png",
            "Rapid Regeneration (Mutalisk)":               github_icon_base_url + "blizzard/btn-upgrade-zerg-rapidregeneration.png",
            "Sundering Glaive (Mutalisk)":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-explosiveglaive.png",
            "Severing Glaive (Mutalisk)":                  github_icon_base_url + "blizzard/btn-upgrade-zerg-explosiveglaive.png",
            "Aerodynamic Glaive Shape (Mutalisk)":         github_icon_base_url + "blizzard/btn-ability-dehaka-airbonusdamage.png",
            "Corruption (Corruptor)":                      github_icon_base_url + "blizzard/btn-ability-zerg-causticspray.png",
            "Caustic Spray (Corruptor)":                   github_icon_base_url + "blizzard/btn-ability-zerg-corruption-color.png",
            "Porous Cartilage (Brood Lord)":               github_icon_base_url + "blizzard/btn-upgrade-kerrigan-broodlordspeed.png",
            "Evolved Carapace (Brood Lord)":               github_icon_base_url + "blizzard/btn-upgrade-zerg-chitinousplating.png",
            "Splitter Mitosis (Brood Lord)":               github_icon_base_url + "blizzard/abilityicon_spawnbroodlings_square.png",
            "Resource Efficiency (Brood Lord)":            github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Parasitic Bomb (Viper)":                      github_icon_base_url + "blizzard/btn-ability-zerg-parasiticbomb.png",
            "Paralytic Barbs (Viper)":                     github_icon_base_url + "blizzard/btn-upgrade-zerg-abathur-abduct.png",
            "Virulent Microbes (Viper)":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-abathur-castrange.png",
            "Prolonged Dispersion (Guardian)":             github_icon_base_url + "blizzard/btn-upgrade-zerg-abathur-prolongeddispersion.png",
            "Primal Adaptation (Guardian)":                github_icon_base_url + "blizzard/biomassrecovery_coop.png",
            "Soronan Acid (Guardian)":                     github_icon_base_url + "blizzard/btn-upgrade-zerg-abathur-biomass.png",
            "Corrosive Spray (Devourer)":                  github_icon_base_url + "blizzard/btn-upgrade-zerg-abathur-devourer-corrosivespray.png",
            "Gaping Maw (Devourer)":                       github_icon_base_url + "blizzard/btn-ability-zerg-explode-color.png",
            "Improved Osmosis (Devourer)":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-pneumatizedcarapace.png",
            "Prescient Spores (Devourer)":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-airattacks-level2.png",
            "Carrion Strain (Swarm Host)":                 github_icon_base_url + "blizzard/btn-unit-zerg-swarmhost-carrion.png",
            "Creeper Strain (Swarm Host)":                 github_icon_base_url + "blizzard/btn-unit-zerg-swarmhost-creeper.png",
            "Burrow (Swarm Host)":                         github_icon_base_url + "blizzard/btn-ability-zerg-burrow-color.png",
            "Rapid Incubation (Swarm Host)":               github_icon_base_url + "blizzard/btn-upgrade-zerg-rapidincubation.png",
            "Pressurized Glands (Swarm Host)":             github_icon_base_url + "blizzard/btn-upgrade-zerg-pressurizedglands.png",
            "Locust Metabolic Boost (Swarm Host)":         github_icon_base_url + "blizzard/btn-upgrade-zerg-glialreconstitution.png",
            "Enduring Locusts (Swarm Host)":               github_icon_base_url + "blizzard/btn-upgrade-zerg-evolveincreasedlocustlifetime.png",
            "Organic Carapace (Swarm Host)":               github_icon_base_url + "blizzard/btn-upgrade-zerg-organiccarapace.png",
            "Resource Efficiency (Swarm Host)":            github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Infested Terran (Infestor)":                  github_icon_base_url + "blizzard/btn-unit-zerg-infestedmarine.png",
            "Microbial Shroud (Infestor)":                 github_icon_base_url + "blizzard/btn-ability-zerg-darkswarm.png",
            "Noxious Strain (Ultralisk)":                  github_icon_base_url + "blizzard/btn-unit-zerg-ultralisk-noxious.png",
            "Torrasque Strain (Ultralisk)":                github_icon_base_url + "blizzard/btn-unit-zerg-ultralisk-torrasque.png",
            "Burrow Charge (Ultralisk)":                   github_icon_base_url + "blizzard/btn-upgrade-zerg-burrowcharge.png",
            "Tissue Assimilation (Ultralisk)":             github_icon_base_url + "blizzard/btn-upgrade-zerg-tissueassimilation.png",
            "Monarch Blades (Ultralisk)":                  github_icon_base_url + "blizzard/btn-upgrade-zerg-monarchblades.png",
            "Anabolic Synthesis (Ultralisk)":              github_icon_base_url + "blizzard/btn-upgrade-zerg-anabolicsynthesis.png",
            "Chitinous Plating (Ultralisk)":               github_icon_base_url + "blizzard/btn-upgrade-zerg-chitinousplating.png",
            "Organic Carapace (Ultralisk)":                github_icon_base_url + "blizzard/btn-upgrade-zerg-organiccarapace.png",
            "Resource Efficiency (Ultralisk)":             github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Fungal Growth (Brood Queen)":                 github_icon_base_url + "blizzard/btn-upgrade-zerg-stukov-researchqueenfungalgrowth.png",
            "Ensnare (Brood Queen)":                       github_icon_base_url + "blizzard/btn-ability-zerg-fungalgrowth-color.png",
            "Enhanced Mitochondria (Brood Queen)":         github_icon_base_url + "blizzard/btn-upgrade-zerg-stukov-queenenergyregen.png",
            "Virulent Spores (Scourge)":                   github_icon_base_url + "blizzard/btn-upgrade-zagara-scourgesplashdamage.png",
            "Resource Efficiency (Scourge)":               github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Swarm Scourge (Scourge)":                     github_icon_base_url + "original/btn-upgrade-custom-triple-scourge.png",

            "Infested Medics":                             github_icon_base_url + "blizzard/btn-unit-terran-medicelite.png",
            "Infested Siege Tanks":                        github_icon_base_url + "original/btn-unit-terran-siegetankmercenary-tank.png",
            "Infested Banshees":                           github_icon_base_url + "original/btn-unit-terran-bansheemercenary.png",

            "Primal Form (Kerrigan)":                      github_icon_base_url + "blizzard/btn-unit-zerg-kerriganinfested.png",
            "Kinetic Blast (Kerrigan Tier 1)":             github_icon_base_url + "blizzard/btn-ability-kerrigan-kineticblast.png",
            "Heroic Fortitude (Kerrigan Tier 1)":          github_icon_base_url + "blizzard/btn-ability-kerrigan-heroicfortitude.png",
            "Leaping Strike (Kerrigan Tier 1)":            github_icon_base_url + "blizzard/btn-ability-kerrigan-leapingstrike.png",
            "Crushing Grip (Kerrigan Tier 2)":             github_icon_base_url + "blizzard/btn-ability-swarm-kerrigan-crushinggrip.png",
            "Chain Reaction (Kerrigan Tier 2)":            github_icon_base_url + "blizzard/btn-ability-swarm-kerrigan-chainreaction.png",
            "Psionic Shift (Kerrigan Tier 2)":             github_icon_base_url + "blizzard/btn-ability-kerrigan-psychicshift.png",
            "Wild Mutation (Kerrigan Tier 4)":             github_icon_base_url + "blizzard/btn-ability-kerrigan-wildmutation.png",
            "Spawn Banelings (Kerrigan Tier 4)":           github_icon_base_url + "blizzard/abilityicon_spawnbanelings_square.png",
            "Mend (Kerrigan Tier 4)":                      github_icon_base_url + "blizzard/btn-ability-zerg-transfusion-color.png",
            "Infest Broodlings (Kerrigan Tier 6)":         github_icon_base_url + "blizzard/abilityicon_spawnbroodlings_square.png",
            "Fury (Kerrigan Tier 6)":                      github_icon_base_url + "blizzard/btn-ability-kerrigan-fury.png",
            "Ability Efficiency (Kerrigan Tier 6)":        github_icon_base_url + "blizzard/btn-ability-kerrigan-abilityefficiency.png",
            "Apocalypse (Kerrigan Tier 7)":                github_icon_base_url + "blizzard/btn-ability-kerrigan-apocalypse.png",
            "Spawn Leviathan (Kerrigan Tier 7)":           github_icon_base_url + "blizzard/btn-unit-zerg-leviathan.png",
            "Drop-Pods (Kerrigan Tier 7)":                 github_icon_base_url + "blizzard/btn-ability-kerrigan-droppods.png",

            "Protoss Ground Weapon Level 1":               github_icon_base_url + "blizzard/btn-upgrade-protoss-groundweaponslevel1.png",
            "Protoss Ground Weapon Level 2":               github_icon_base_url + "blizzard/btn-upgrade-protoss-groundweaponslevel2.png",
            "Protoss Ground Weapon Level 3":               github_icon_base_url + "blizzard/btn-upgrade-protoss-groundweaponslevel3.png",
            "Protoss Ground Armor Level 1":                github_icon_base_url + "blizzard/btn-upgrade-protoss-groundarmorlevel1.png",
            "Protoss Ground Armor Level 2":                github_icon_base_url + "blizzard/btn-upgrade-protoss-groundarmorlevel2.png",
            "Protoss Ground Armor Level 3":                github_icon_base_url + "blizzard/btn-upgrade-protoss-groundarmorlevel3.png",
            "Protoss Shields Level 1":                     github_icon_base_url + "blizzard/btn-upgrade-protoss-shieldslevel1.png",
            "Protoss Shields Level 2":                     github_icon_base_url + "blizzard/btn-upgrade-protoss-shieldslevel2.png",
            "Protoss Shields Level 3":                     github_icon_base_url + "blizzard/btn-upgrade-protoss-shieldslevel3.png",
            "Protoss Air Weapon Level 1":                  github_icon_base_url + "blizzard/btn-upgrade-protoss-airweaponslevel1.png",
            "Protoss Air Weapon Level 2":                  github_icon_base_url + "blizzard/btn-upgrade-protoss-airweaponslevel2.png",
            "Protoss Air Weapon Level 3":                  github_icon_base_url + "blizzard/btn-upgrade-protoss-airweaponslevel3.png",
            "Protoss Air Armor Level 1":                   github_icon_base_url + "blizzard/btn-upgrade-protoss-airarmorlevel1.png",
            "Protoss Air Armor Level 2":                   github_icon_base_url + "blizzard/btn-upgrade-protoss-airarmorlevel2.png",
            "Protoss Air Armor Level 3":                   github_icon_base_url + "blizzard/btn-upgrade-protoss-airarmorlevel3.png",

            "Quatro":                                      github_icon_base_url + "blizzard/btn-progression-protoss-fenix-6-forgeresearch.png",

            "Photon Cannon":                               github_icon_base_url + "blizzard/btn-building-protoss-photoncannon.png",
            "Khaydarin Monolith":                          github_icon_base_url + "blizzard/btn-unit-protoss-khaydarinmonolith.png",
            "Shield Battery":                              github_icon_base_url + "blizzard/btn-building-protoss-shieldbattery.png",

            "Enhanced Targeting":                          github_icon_base_url + "blizzard/btn-upgrade-karax-turretrange.png",
            "Optimized Ordnance":                          github_icon_base_url + "blizzard/btn-upgrade-karax-turretattackspeed.png",
            "Khalai Ingenuity":                            github_icon_base_url + "blizzard/btn-upgrade-karax-pylonwarpininstantly.png",
            "Orbital Assimilators":                        github_icon_base_url + "blizzard/btn-ability-spearofadun-orbitalassimilator.png",
            "Amplified Assimilators":                      github_icon_base_url + "original/btn-research-terran-microfiltering.png",
            "Warp Harmonization":                          github_icon_base_url + "blizzard/btn-ability-spearofadun-warpharmonization.png",
            "Superior Warp Gates":                         github_icon_base_url + "blizzard/talent-artanis-level03-warpgatecharges.png",
            "Nexus Overcharge":                            github_icon_base_url + "blizzard/btn-ability-spearofadun-nexusovercharge.png",

            "Zealot":                                      github_icon_base_url + "blizzard/btn-unit-protoss-zealot-aiur.png",
            "Centurion":                                   github_icon_base_url + "blizzard/btn-unit-protoss-zealot-nerazim.png",
            "Sentinel":                                    github_icon_base_url + "blizzard/btn-unit-protoss-zealot-purifier.png",
            "Supplicant":                                  github_icon_base_url + "blizzard/btn-unit-protoss-alarak-taldarim-supplicant.png",
            "Sentry":                                      github_icon_base_url + "blizzard/btn-unit-protoss-sentry.png",
            "Energizer":                                   github_icon_base_url + "blizzard/btn-unit-protoss-sentry-purifier.png",
            "Havoc":                                       github_icon_base_url + "blizzard/btn-unit-protoss-sentry-taldarim.png",
            "Stalker":                                     "https://static.wikia.nocookie.net/starcraft/images/0/0d/Icon_Protoss_Stalker.jpg",
            "Instigator":                                  github_icon_base_url + "blizzard/btn-unit-protoss-stalker-purifier.png",
            "Slayer":                                      github_icon_base_url + "blizzard/btn-unit-protoss-alarak-taldarim-stalker.png",
            "Dragoon":                                     github_icon_base_url + "blizzard/btn-unit-protoss-dragoon-void.png",
            "Adept":                                       github_icon_base_url + "blizzard/btn-unit-protoss-adept-purifier.png",
            "High Templar":                                "https://static.wikia.nocookie.net/starcraft/images/a/a0/Icon_Protoss_High_Templar.jpg",
            "Signifier":                                   github_icon_base_url + "original/btn-unit-protoss-hightemplar-nerazim.png",
            "Ascendant":                                   github_icon_base_url + "blizzard/btn-unit-protoss-hightemplar-taldarim.png",
            "Dark Archon":                                 github_icon_base_url + "blizzard/talent-vorazun-level05-unlockdarkarchon.png",
            "Dark Templar":                                "https://static.wikia.nocookie.net/starcraft/images/9/90/Icon_Protoss_Dark_Templar.jpg",
            "Avenger":                                     github_icon_base_url + "blizzard/btn-unit-protoss-darktemplar-aiur.png",
            "Blood Hunter":                                github_icon_base_url + "blizzard/btn-unit-protoss-darktemplar-taldarim.png",

            "Leg Enhancements (Zealot/Sentinel/Centurion)": github_icon_base_url + "blizzard/btn-ability-protoss-charge-color.png",
            "Shield Capacity (Zealot/Sentinel/Centurion)": github_icon_base_url + "blizzard/btn-upgrade-protoss-shieldslevel1.png",
            "Blood Shield (Supplicant)":                   github_icon_base_url + "blizzard/btn-upgrade-protoss-alarak-supplicantarmor.png",
            "Soul Augmentation (Supplicant)":              github_icon_base_url + "blizzard/btn-upgrade-protoss-alarak-supplicantextrashields.png",
            "Shield Regeneration (Supplicant)":            github_icon_base_url + "blizzard/btn-ability-protoss-voidarmor.png",
            "Force Field (Sentry)":                        github_icon_base_url + "blizzard/btn-ability-protoss-forcefield-color.png",
            "Hallucination (Sentry)":                      github_icon_base_url + "blizzard/btn-ability-protoss-hallucination-color.png",
            "Reclamation (Energizer)":                     github_icon_base_url + "blizzard/btn-ability-protoss-reclamation.png",
            "Forged Chassis (Energizer)":                  github_icon_base_url + "blizzard/btn-upgrade-protoss-groundarmorlevel0.png",
            "Detect Weakness (Havoc)":                     github_icon_base_url + "blizzard/btn-upgrade-protoss-alarak-havoctargetlockbuffed.png",
            "Bloodshard Resonance (Havoc)":                github_icon_base_url + "blizzard/btn-upgrade-protoss-alarak-rangeincrease.png",
            "Cloaking Module (Sentry/Energizer/Havoc)":    github_icon_base_url + "blizzard/btn-upgrade-protoss-alarak-permanentcloak.png",
            "Rapid Recharging (Sentry/Energizer/Havoc/Shield Battery)": github_icon_base_url + "blizzard/btn-upgrade-karax-energyregen200.png",
            "Disintegrating Particles (Stalker/Instigator/Slayer)": github_icon_base_url + "blizzard/btn-ability-protoss-phasedisruptor.png",
            "Particle Reflection (Stalker/Instigator/Slayer)": github_icon_base_url + "blizzard/btn-upgrade-protoss-fenix-adeptchampionbounceattack.png",
            "High Impact Phase Disruptor (Dragoon)":       github_icon_base_url + "blizzard/btn-ability-protoss-phasedisruptor.png",
            "Trillic Compression System (Dragoon)":        github_icon_base_url + "blizzard/btn-ability-protoss-dragoonchassis.png",
            "Singularity Charge (Dragoon)":                github_icon_base_url + "blizzard/btn-upgrade-artanis-singularitycharge.png",
            "Enhanced Strider Servos (Dragoon)":           github_icon_base_url + "blizzard/btn-upgrade-terran-transformationservos.png",
            "Shockwave (Adept)":                           github_icon_base_url + "blizzard/btn-upgrade-protoss-fenix-adept-recochetglaiveupgraded.png",
            "Resonating Glaives (Adept)":                  github_icon_base_url + "blizzard/btn-upgrade-protoss-resonatingglaives.png",
            "Phase Bulwark (Adept)":                       github_icon_base_url + "blizzard/btn-upgrade-protoss-adeptshieldupgrade.png",
            "Unshackled Psionic Storm (High Templar/Signifier)": github_icon_base_url + "blizzard/btn-ability-protoss-psistorm.png",
            "Hallucination (High Templar/Signifier)":      github_icon_base_url + "blizzard/btn-ability-protoss-hallucination-color.png",
            "Khaydarin Amulet (High Templar/Signifier)":   github_icon_base_url + "blizzard/btn-upgrade-protoss-khaydarinamulet.png",
            "High Archon (Archon)":                        github_icon_base_url + "blizzard/btn-upgrade-artanis-healingpsionicstorm.png",
            "Power Overwhelming (Ascendant)":              github_icon_base_url + "blizzard/btn-upgrade-protoss-alarak-ascendantspermanentlybetter.png",
            "Chaotic Attunement (Ascendant)":              github_icon_base_url + "blizzard/btn-upgrade-protoss-alarak-ascendant'spsiorbtravelsfurther.png",
            "Blood Amulet (Ascendant)":                    github_icon_base_url + "blizzard/btn-upgrade-protoss-wrathwalker-chargetimeimproved.png",
            "Feedback (Dark Archon)":                      github_icon_base_url + "blizzard/btn-ability-protoss-feedback-color.png",
            "Maelstrom (Dark Archon)":                     github_icon_base_url + "blizzard/btn-ability-protoss-voidstasis.png",
            "Argus Talisman (Dark Archon)":                github_icon_base_url + "original/btn-upgrade-protoss-argustalisman@scbw.png",
            "Dark Archon Meld (Dark Templar)":             github_icon_base_url + "blizzard/talent-vorazun-level05-unlockdarkarchon.png",
            "Shroud of Adun (Dark Templar/Avenger/Blood Hunter)": github_icon_base_url + "blizzard/talent-vorazun-level01-shadowstalk.png",
            "Shadow Guard Training (Dark Templar/Avenger/Blood Hunter)": github_icon_base_url + "blizzard/btn-ability-terran-heal-color.png",
            "Blink (Dark Templar/Avenger/Blood Hunter)":   github_icon_base_url + "blizzard/btn-ability-protoss-shadowdash.png",
            "Resource Efficiency (Dark Templar/Avenger/Blood Hunter)": github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",

            "Warp Prism":                                  github_icon_base_url + "blizzard/btn-unit-protoss-warpprism.png",
            "Immortal":                                    "https://static.wikia.nocookie.net/starcraft/images/c/c1/Icon_Protoss_Immortal.jpg",
            "Annihilator":                                 github_icon_base_url + "blizzard/btn-unit-protoss-immortal-nerazim.png",
            "Vanguard":                                    github_icon_base_url + "blizzard/btn-unit-protoss-immortal-taldarim.png",
            "Colossus":                                    github_icon_base_url + "blizzard/btn-unit-protoss-colossus-purifier.png",
            "Wrathwalker":                                 github_icon_base_url + "blizzard/btn-unit-protoss-colossus-taldarim.png",
            "Observer":                                    github_icon_base_url + "blizzard/btn-unit-protoss-observer.png",
            "Reaver":                                      github_icon_base_url + "blizzard/btn-unit-protoss-reaver.png",
            "Disruptor":                                   github_icon_base_url + "blizzard/btn-unit-protoss-disruptor.png",

            "Gravitic Drive (Warp Prism)":                 github_icon_base_url + "blizzard/btn-upgrade-protoss-graviticdrive.png",
            "Phase Blaster (Warp Prism)":                  github_icon_base_url + "blizzard/btn-upgrade-protoss-airweaponslevel0.png",
            "War Configuration (Warp Prism)":              github_icon_base_url + "blizzard/btn-upgrade-protoss-alarak-graviticdrive.png",
            "Singularity Charge (Immortal/Annihilator)":   github_icon_base_url + "blizzard/btn-upgrade-artanis-singularitycharge.png",
            "Advanced Targeting Mechanics (Immortal/Annihilator)": github_icon_base_url + "blizzard/btn-ability-terran-detectionconedebuff.png",
            "Agony Launchers (Vanguard)":                  github_icon_base_url + "blizzard/btn-upgrade-protoss-vanguard-aoeradiusincreased.png",
            "Matter Dispersion (Vanguard)":                github_icon_base_url + "blizzard/btn-ability-terran-detectionconedebuff.png",
            "Pacification Protocol (Colossus)":            github_icon_base_url + "blizzard/btn-ability-protoss-chargedblast.png",
            "Rapid Power Cycling (Wrathwalker)":           github_icon_base_url + "blizzard/btn-upgrade-protoss-wrathwalker-chargetimeimproved.png",
            "Eye of Wrath (Wrathwalker)":                  github_icon_base_url + "blizzard/btn-upgrade-protoss-extendedthermallance.png",
            "Gravitic Boosters (Observer)":                github_icon_base_url + "blizzard/btn-upgrade-protoss-graviticbooster.png",
            "Sensor Array (Observer)":                     github_icon_base_url + "blizzard/btn-ability-zeratul-observer-sensorarray.png",
            "Scarab Damage (Reaver)":                      github_icon_base_url + "blizzard/btn-ability-protoss-scarabshot.png",
            "Solarite Payload (Reaver)":                   github_icon_base_url + "blizzard/btn-upgrade-artanis-scarabsplashradius.png",
            "Reaver Capacity (Reaver)":                    github_icon_base_url + "original/btn-upgrade-protoss-increasedscarabcapacity@scbw.png",
            "Resource Efficiency (Reaver)":                github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",

            "Phoenix":                                     "https://static.wikia.nocookie.net/starcraft/images/b/b1/Icon_Protoss_Phoenix.jpg",
            "Mirage":                                      github_icon_base_url + "blizzard/btn-unit-protoss-phoenix-purifier.png",
            "Corsair":                                     github_icon_base_url + "blizzard/btn-unit-protoss-corsair.png",
            "Destroyer":                                   github_icon_base_url + "blizzard/btn-unit-protoss-voidray-taldarim.png",
            "Void Ray":                                    github_icon_base_url + "blizzard/btn-unit-protoss-voidray-nerazim.png",
            "Carrier":                                     "https://static.wikia.nocookie.net/starcraft/images/2/2c/Icon_Protoss_Carrier.jpg",
            "Scout":                                       github_icon_base_url + "original/btn-unit-protoss-scout.png",
            "Tempest":                                     github_icon_base_url + "blizzard/btn-unit-protoss-tempest-purifier.png",
            "Mothership":                                  github_icon_base_url + "blizzard/btn-unit-protoss-mothership-taldarim.png",
            "Arbiter":                                     github_icon_base_url + "blizzard/btn-unit-protoss-arbiter.png",
            "Oracle":                                      github_icon_base_url + "blizzard/btn-unit-protoss-oracle.png",

            "Ionic Wavelength Flux (Phoenix/Mirage)":      github_icon_base_url + "blizzard/btn-upgrade-protoss-airweaponslevel0.png",
            "Anion Pulse-Crystals (Phoenix/Mirage)":       github_icon_base_url + "blizzard/btn-upgrade-protoss-phoenixrange.png",
            "Stealth Drive (Corsair)":                     github_icon_base_url + "blizzard/btn-upgrade-vorazun-corsairpermanentlycloaked.png",
            "Argus Jewel (Corsair)":                       github_icon_base_url + "blizzard/btn-ability-protoss-stasistrap.png",
            "Sustaining Disruption (Corsair)":             github_icon_base_url + "blizzard/btn-ability-protoss-disruptionweb.png",
            "Neutron Shields (Corsair)":                   github_icon_base_url + "blizzard/btn-upgrade-protoss-shieldslevel1.png",
            "Reforged Bloodshard Core (Destroyer)":        github_icon_base_url + "blizzard/btn-amonshardsarmor.png",
            "Flux Vanes (Void Ray/Destroyer)":             github_icon_base_url + "blizzard/btn-upgrade-protoss-fluxvanes.png",
            "Graviton Catapult (Carrier)":                 github_icon_base_url + "blizzard/btn-upgrade-protoss-gravitoncatapult.png",
            "Hull of Past Glories (Carrier)":              github_icon_base_url + "blizzard/btn-progression-protoss-fenix-14-colossusandcarrierchampionsresearch.png",
            "Combat Sensor Array (Scout)":                 github_icon_base_url + "blizzard/btn-upgrade-protoss-fenix-scoutchampionrange.png",
            "Apial Sensors (Scout)":                       github_icon_base_url + "blizzard/btn-upgrade-tychus-detection.png",
            "Gravitic Thrusters (Scout)":                  github_icon_base_url + "blizzard/btn-upgrade-protoss-graviticbooster.png",
            "Advanced Photon Blasters (Scout)":            github_icon_base_url + "blizzard/btn-upgrade-protoss-airweaponslevel3.png",
            "Tectonic Destabilizers (Tempest)":            github_icon_base_url + "blizzard/btn-ability-protoss-disruptionblast.png",
            "Quantic Reactor (Tempest)":                   github_icon_base_url + "blizzard/btn-upgrade-protoss-researchgravitysling.png",
            "Gravity Sling (Tempest)":                     github_icon_base_url + "blizzard/btn-upgrade-protoss-tectonicdisruptors.png",
            "Chronostatic Reinforcement (Arbiter)":        github_icon_base_url + "blizzard/btn-upgrade-protoss-airarmorlevel2.png",
            "Khaydarin Core (Arbiter)":                    github_icon_base_url + "blizzard/btn-upgrade-protoss-adeptshieldupgrade.png",
            "Spacetime Anchor (Arbiter)":                  github_icon_base_url + "blizzard/btn-ability-protoss-stasisfield.png",
            "Resource Efficiency (Arbiter)":               github_icon_base_url + "blizzard/btn-ability-hornerhan-salvagebonus.png",
            "Enhanced Cloak Field (Arbiter)":              github_icon_base_url + "blizzard/btn-ability-stetmann-stetzonegenerator-speed.png",
            "Stealth Drive (Oracle)":                      github_icon_base_url + "blizzard/btn-upgrade-vorazun-oraclepermanentlycloaked.png",
            "Stasis Calibration (Oracle)":                 github_icon_base_url + "blizzard/btn-ability-protoss-oracle-stasiscalibration.png",
            "Temporal Acceleration Beam (Oracle)":         github_icon_base_url + "blizzard/btn-ability-protoss-oraclepulsarcannonon.png",

            "Matrix Overload":                             github_icon_base_url + "blizzard/btn-ability-spearofadun-matrixoverload.png",
            "Guardian Shell":                              github_icon_base_url + "blizzard/btn-ability-spearofadun-guardianshell.png",

            "Chrono Surge (Spear of Adun Calldown)":       github_icon_base_url + "blizzard/btn-ability-spearofadun-chronosurge.png",
            "Proxy Pylon (Spear of Adun Calldown)":        github_icon_base_url + "blizzard/btn-ability-spearofadun-deploypylon.png",
            "Warp In Reinforcements (Spear of Adun Calldown)": github_icon_base_url + "blizzard/btn-ability-spearofadun-warpinreinforcements.png",
            "Pylon Overcharge (Spear of Adun Calldown)":   github_icon_base_url + "blizzard/btn-ability-protoss-purify.png",
            "Orbital Strike (Spear of Adun Calldown)":     github_icon_base_url + "blizzard/btn-ability-spearofadun-orbitalstrike.png",
            "Temporal Field (Spear of Adun Calldown)":     github_icon_base_url + "blizzard/btn-ability-spearofadun-temporalfield.png",
            "Solar Lance (Spear of Adun Calldown)":        github_icon_base_url + "blizzard/btn-ability-spearofadun-solarlance.png",
            "Mass Recall (Spear of Adun Calldown)":        github_icon_base_url + "blizzard/btn-ability-spearofadun-massrecall.png",
            "Shield Overcharge (Spear of Adun Calldown)":  github_icon_base_url + "blizzard/btn-ability-spearofadun-shieldovercharge.png",
            "Deploy Fenix (Spear of Adun Calldown)":       github_icon_base_url + "blizzard/btn-unit-protoss-fenix.png",
            "Purifier Beam (Spear of Adun Calldown)":      github_icon_base_url + "blizzard/btn-ability-spearofadun-purifierbeam.png",
            "Time Stop (Spear of Adun Calldown)":          github_icon_base_url + "blizzard/btn-ability-spearofadun-timestop.png",
            "Solar Bombardment (Spear of Adun Calldown)":  github_icon_base_url + "blizzard/btn-ability-spearofadun-solarbombardment.png",

            "Reconstruction Beam (Spear of Adun Auto-Cast)": github_icon_base_url + "blizzard/btn-ability-spearofadun-reconstructionbeam.png",
            "Overwatch (Spear of Adun Auto-Cast)":         github_icon_base_url + "blizzard/btn-ability-zeratul-chargedcrystal-psionicwinds.png",

            "Nothing":                                     "",
        }
        sc2wol_location_ids = {
            "Liberation Day":          range(SC2WOL_LOC_ID_OFFSET + 100, SC2WOL_LOC_ID_OFFSET + 200),
            "The Outlaws":             range(SC2WOL_LOC_ID_OFFSET + 200, SC2WOL_LOC_ID_OFFSET + 300),
            "Zero Hour":               range(SC2WOL_LOC_ID_OFFSET + 300, SC2WOL_LOC_ID_OFFSET + 400),
            "Evacuation":              range(SC2WOL_LOC_ID_OFFSET + 400, SC2WOL_LOC_ID_OFFSET + 500),
            "Outbreak":                range(SC2WOL_LOC_ID_OFFSET + 500, SC2WOL_LOC_ID_OFFSET + 600),
            "Safe Haven":              range(SC2WOL_LOC_ID_OFFSET + 600, SC2WOL_LOC_ID_OFFSET + 700),
            "Haven's Fall":            range(SC2WOL_LOC_ID_OFFSET + 700, SC2WOL_LOC_ID_OFFSET + 800),
            "Smash and Grab":          range(SC2WOL_LOC_ID_OFFSET + 800, SC2WOL_LOC_ID_OFFSET + 900),
            "The Dig":                 range(SC2WOL_LOC_ID_OFFSET + 900, SC2WOL_LOC_ID_OFFSET + 1000),
            "The Moebius Factor":      range(SC2WOL_LOC_ID_OFFSET + 1000, SC2WOL_LOC_ID_OFFSET + 1100),
            "Supernova":               range(SC2WOL_LOC_ID_OFFSET + 1100, SC2WOL_LOC_ID_OFFSET + 1200),
            "Maw of the Void":         range(SC2WOL_LOC_ID_OFFSET + 1200, SC2WOL_LOC_ID_OFFSET + 1300),
            "Devil's Playground":      range(SC2WOL_LOC_ID_OFFSET + 1300, SC2WOL_LOC_ID_OFFSET + 1400),
            "Welcome to the Jungle":   range(SC2WOL_LOC_ID_OFFSET + 1400, SC2WOL_LOC_ID_OFFSET + 1500),
            "Breakout":                range(SC2WOL_LOC_ID_OFFSET + 1500, SC2WOL_LOC_ID_OFFSET + 1600),
            "Ghost of a Chance":       range(SC2WOL_LOC_ID_OFFSET + 1600, SC2WOL_LOC_ID_OFFSET + 1700),
            "The Great Train Robbery": range(SC2WOL_LOC_ID_OFFSET + 1700, SC2WOL_LOC_ID_OFFSET + 1800),
            "Cutthroat":               range(SC2WOL_LOC_ID_OFFSET + 1800, SC2WOL_LOC_ID_OFFSET + 1900),
            "Engine of Destruction":   range(SC2WOL_LOC_ID_OFFSET + 1900, SC2WOL_LOC_ID_OFFSET + 2000),
            "Media Blitz":             range(SC2WOL_LOC_ID_OFFSET + 2000, SC2WOL_LOC_ID_OFFSET + 2100),
            "Piercing the Shroud":     range(SC2WOL_LOC_ID_OFFSET + 2100, SC2WOL_LOC_ID_OFFSET + 2200),
            "Whispers of Doom":        range(SC2WOL_LOC_ID_OFFSET + 2200, SC2WOL_LOC_ID_OFFSET + 2300),
            "A Sinister Turn":         range(SC2WOL_LOC_ID_OFFSET + 2300, SC2WOL_LOC_ID_OFFSET + 2400),
            "Echoes of the Future":    range(SC2WOL_LOC_ID_OFFSET + 2400, SC2WOL_LOC_ID_OFFSET + 2500),
            "In Utter Darkness":       range(SC2WOL_LOC_ID_OFFSET + 2500, SC2WOL_LOC_ID_OFFSET + 2600),
            "Gates of Hell":           range(SC2WOL_LOC_ID_OFFSET + 2600, SC2WOL_LOC_ID_OFFSET + 2700),
            "Belly of the Beast":      range(SC2WOL_LOC_ID_OFFSET + 2700, SC2WOL_LOC_ID_OFFSET + 2800),
            "Shatter the Sky":         range(SC2WOL_LOC_ID_OFFSET + 2800, SC2WOL_LOC_ID_OFFSET + 2900),
            "All-In":                  range(SC2WOL_LOC_ID_OFFSET + 2900, SC2WOL_LOC_ID_OFFSET + 3000),

            "Lab Rat":                 range(SC2HOTS_LOC_ID_OFFSET + 100, SC2HOTS_LOC_ID_OFFSET + 200),
            "Back in the Saddle":      range(SC2HOTS_LOC_ID_OFFSET + 200, SC2HOTS_LOC_ID_OFFSET + 300),
            "Rendezvous":              range(SC2HOTS_LOC_ID_OFFSET + 300, SC2HOTS_LOC_ID_OFFSET + 400),
            "Harvest of Screams":      range(SC2HOTS_LOC_ID_OFFSET + 400, SC2HOTS_LOC_ID_OFFSET + 500),
            "Shoot the Messenger":     range(SC2HOTS_LOC_ID_OFFSET + 500, SC2HOTS_LOC_ID_OFFSET + 600),
            "Enemy Within":            range(SC2HOTS_LOC_ID_OFFSET + 600, SC2HOTS_LOC_ID_OFFSET + 700),
            "Domination":              range(SC2HOTS_LOC_ID_OFFSET + 700, SC2HOTS_LOC_ID_OFFSET + 800),
            "Fire in the Sky":         range(SC2HOTS_LOC_ID_OFFSET + 800, SC2HOTS_LOC_ID_OFFSET + 900),
            "Old Soldiers":            range(SC2HOTS_LOC_ID_OFFSET + 900, SC2HOTS_LOC_ID_OFFSET + 1000),
            "Waking the Ancient":      range(SC2HOTS_LOC_ID_OFFSET + 1000, SC2HOTS_LOC_ID_OFFSET + 1100),
            "The Crucible":            range(SC2HOTS_LOC_ID_OFFSET + 1100, SC2HOTS_LOC_ID_OFFSET + 1200),
            "Supreme":                 range(SC2HOTS_LOC_ID_OFFSET + 1200, SC2HOTS_LOC_ID_OFFSET + 1300),
            "Infested":                range(SC2HOTS_LOC_ID_OFFSET + 1300, SC2HOTS_LOC_ID_OFFSET + 1400),
            "Hand of Darkness":        range(SC2HOTS_LOC_ID_OFFSET + 1400, SC2HOTS_LOC_ID_OFFSET + 1500),
            "Phantoms of the Void":    range(SC2HOTS_LOC_ID_OFFSET + 1500, SC2HOTS_LOC_ID_OFFSET + 1600),
            "With Friends Like These": range(SC2HOTS_LOC_ID_OFFSET + 1600, SC2HOTS_LOC_ID_OFFSET + 1700),
            "Conviction":              range(SC2HOTS_LOC_ID_OFFSET + 1700, SC2HOTS_LOC_ID_OFFSET + 1800),
            "Planetfall":              range(SC2HOTS_LOC_ID_OFFSET + 1800, SC2HOTS_LOC_ID_OFFSET + 1900),
            "Death From Above":        range(SC2HOTS_LOC_ID_OFFSET + 1900, SC2HOTS_LOC_ID_OFFSET + 2000),
            "The Reckoning":           range(SC2HOTS_LOC_ID_OFFSET + 2000, SC2HOTS_LOC_ID_OFFSET + 2100),

            "Dark Whispers":           range(SC2LOTV_LOC_ID_OFFSET + 100, SC2LOTV_LOC_ID_OFFSET + 200),
            "Ghosts in the Fog":       range(SC2LOTV_LOC_ID_OFFSET + 200, SC2LOTV_LOC_ID_OFFSET + 300),
            "Evil Awoken":             range(SC2LOTV_LOC_ID_OFFSET + 300, SC2LOTV_LOC_ID_OFFSET + 400),

            "For Aiur!":               range(SC2LOTV_LOC_ID_OFFSET + 400, SC2LOTV_LOC_ID_OFFSET + 500),
            "The Growing Shadow":      range(SC2LOTV_LOC_ID_OFFSET + 500, SC2LOTV_LOC_ID_OFFSET + 600),
            "The Spear of Adun":       range(SC2LOTV_LOC_ID_OFFSET + 600, SC2LOTV_LOC_ID_OFFSET + 700),
            "Sky Shield":              range(SC2LOTV_LOC_ID_OFFSET + 700, SC2LOTV_LOC_ID_OFFSET + 800),
            "Brothers in Arms":        range(SC2LOTV_LOC_ID_OFFSET + 800, SC2LOTV_LOC_ID_OFFSET + 900),
            "Amon's Reach":            range(SC2LOTV_LOC_ID_OFFSET + 900, SC2LOTV_LOC_ID_OFFSET + 1000),
            "Last Stand":              range(SC2LOTV_LOC_ID_OFFSET + 1000, SC2LOTV_LOC_ID_OFFSET + 1100),
            "Forbidden Weapon":        range(SC2LOTV_LOC_ID_OFFSET + 1100, SC2LOTV_LOC_ID_OFFSET + 1200),
            "Temple of Unification":   range(SC2LOTV_LOC_ID_OFFSET + 1200, SC2LOTV_LOC_ID_OFFSET + 1300),
            "The Infinite Cycle":      range(SC2LOTV_LOC_ID_OFFSET + 1300, SC2LOTV_LOC_ID_OFFSET + 1400),
            "Harbinger of Oblivion":   range(SC2LOTV_LOC_ID_OFFSET + 1400, SC2LOTV_LOC_ID_OFFSET + 1500),
            "Unsealing the Past":      range(SC2LOTV_LOC_ID_OFFSET + 1500, SC2LOTV_LOC_ID_OFFSET + 1600),
            "Purification":            range(SC2LOTV_LOC_ID_OFFSET + 1600, SC2LOTV_LOC_ID_OFFSET + 1700),
            "Steps of the Rite":       range(SC2LOTV_LOC_ID_OFFSET + 1700, SC2LOTV_LOC_ID_OFFSET + 1800),
            "Rak'Shir":                range(SC2LOTV_LOC_ID_OFFSET + 1800, SC2LOTV_LOC_ID_OFFSET + 1900),
            "Templar's Charge":        range(SC2LOTV_LOC_ID_OFFSET + 1900, SC2LOTV_LOC_ID_OFFSET + 2000),
            "Templar's Return":        range(SC2LOTV_LOC_ID_OFFSET + 2000, SC2LOTV_LOC_ID_OFFSET + 2100),
            "The Host":                range(SC2LOTV_LOC_ID_OFFSET + 2100, SC2LOTV_LOC_ID_OFFSET + 2200),
            "Salvation":               range(SC2LOTV_LOC_ID_OFFSET + 2200, SC2LOTV_LOC_ID_OFFSET + 2300),

            "Into the Void":           range(SC2LOTV_LOC_ID_OFFSET + 2300, SC2LOTV_LOC_ID_OFFSET + 2400),
            "The Essence of Eternity": range(SC2LOTV_LOC_ID_OFFSET + 2400, SC2LOTV_LOC_ID_OFFSET + 2500),
            "Amon's Fall":             range(SC2LOTV_LOC_ID_OFFSET + 2500, SC2LOTV_LOC_ID_OFFSET + 2600),

            "The Escape":              range(SC2NCO_LOC_ID_OFFSET + 100, SC2NCO_LOC_ID_OFFSET + 200),
            "Sudden Strike":           range(SC2NCO_LOC_ID_OFFSET + 200, SC2NCO_LOC_ID_OFFSET + 300),
            "Enemy Intelligence":      range(SC2NCO_LOC_ID_OFFSET + 300, SC2NCO_LOC_ID_OFFSET + 400),
            "Trouble In Paradise":     range(SC2NCO_LOC_ID_OFFSET + 400, SC2NCO_LOC_ID_OFFSET + 500),
            "Night Terrors":           range(SC2NCO_LOC_ID_OFFSET + 500, SC2NCO_LOC_ID_OFFSET + 600),
            "Flashpoint":              range(SC2NCO_LOC_ID_OFFSET + 600, SC2NCO_LOC_ID_OFFSET + 700),
            "In the Enemy's Shadow":   range(SC2NCO_LOC_ID_OFFSET + 700, SC2NCO_LOC_ID_OFFSET + 800),
            "Dark Skies":              range(SC2NCO_LOC_ID_OFFSET + 800, SC2NCO_LOC_ID_OFFSET + 900),
            "End Game":                range(SC2NCO_LOC_ID_OFFSET + 900, SC2NCO_LOC_ID_OFFSET + 1000),
        }

        display_data = {}

        # Grouped Items
        grouped_item_ids = {
            "Progressive Terran Weapon Upgrade":        107 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Armor Upgrade":         108 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Infantry Upgrade":      109 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Vehicle Upgrade":       110 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Ship Upgrade":          111 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Weapon/Armor Upgrade":  112 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Zerg Weapon Upgrade":          105 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Armor Upgrade":           106 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Ground Upgrade":          107 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Flyer Upgrade":           108 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Weapon/Armor Upgrade":    109 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Protoss Weapon Upgrade":       105 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Armor Upgrade":        106 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Ground Upgrade":       107 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Air Upgrade":          108 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Weapon/Armor Upgrade": 109 + SC2LOTV_ITEM_ID_OFFSET,
        }
        grouped_item_replacements = {
            "Progressive Terran Weapon Upgrade":   ["Progressive Terran Infantry Weapon",
                                                    "Progressive Terran Vehicle Weapon",
                                                    "Progressive Terran Ship Weapon"],
            "Progressive Terran Armor Upgrade":    ["Progressive Terran Infantry Armor",
                                                    "Progressive Terran Vehicle Armor",
                                                    "Progressive Terran Ship Armor"],
            "Progressive Terran Infantry Upgrade": ["Progressive Terran Infantry Weapon",
                                                    "Progressive Terran Infantry Armor"],
            "Progressive Terran Vehicle Upgrade":  ["Progressive Terran Vehicle Weapon",
                                                    "Progressive Terran Vehicle Armor"],
            "Progressive Terran Ship Upgrade":     ["Progressive Terran Ship Weapon", "Progressive Terran Ship Armor"],
            "Progressive Zerg Weapon Upgrade":     ["Progressive Zerg Melee Attack", "Progressive Zerg Missile Attack",
                                                    "Progressive Zerg Flyer Attack"],
            "Progressive Zerg Armor Upgrade":      ["Progressive Zerg Ground Carapace",
                                                    "Progressive Zerg Flyer Carapace"],
            "Progressive Zerg Ground Upgrade":     ["Progressive Zerg Melee Attack", "Progressive Zerg Missile Attack",
                                                    "Progressive Zerg Ground Carapace"],
            "Progressive Zerg Flyer Upgrade":      ["Progressive Zerg Flyer Attack", "Progressive Zerg Flyer Carapace"],
            "Progressive Protoss Weapon Upgrade":  ["Progressive Protoss Ground Weapon",
                                                    "Progressive Protoss Air Weapon"],
            "Progressive Protoss Armor Upgrade":   ["Progressive Protoss Ground Armor", "Progressive Protoss Shields",
                                                    "Progressive Protoss Air Armor"],
            "Progressive Protoss Ground Upgrade":  ["Progressive Protoss Ground Weapon",
                                                    "Progressive Protoss Ground Armor",
                                                    "Progressive Protoss Shields"],
            "Progressive Protoss Air Upgrade":     ["Progressive Protoss Air Weapon", "Progressive Protoss Air Armor",
                                                    "Progressive Protoss Shields"]
        }
        grouped_item_replacements["Progressive Terran Weapon/Armor Upgrade"] = \
            grouped_item_replacements["Progressive Terran Weapon Upgrade"] \
            + grouped_item_replacements["Progressive Terran Armor Upgrade"]
        grouped_item_replacements["Progressive Zerg Weapon/Armor Upgrade"] = \
            grouped_item_replacements["Progressive Zerg Weapon Upgrade"] \
            + grouped_item_replacements["Progressive Zerg Armor Upgrade"]
        grouped_item_replacements["Progressive Protoss Weapon/Armor Upgrade"] = \
            grouped_item_replacements["Progressive Protoss Weapon Upgrade"] \
            + grouped_item_replacements["Progressive Protoss Armor Upgrade"]
        replacement_item_ids = {
            "Progressive Terran Infantry Weapon": 100 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Infantry Armor":  102 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Vehicle Weapon":  103 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Vehicle Armor":   104 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Ship Weapon":     105 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Ship Armor":      106 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Zerg Melee Attack":      100 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Missile Attack":    101 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Ground Carapace":   102 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Flyer Attack":      103 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Flyer Carapace":    104 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Protoss Ground Weapon":  100 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Ground Armor":   101 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Shields":        102 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Air Weapon":     103 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Air Armor":      104 + SC2LOTV_ITEM_ID_OFFSET,
        }

        inventory: collections.Counter = tracker_data.get_player_inventory_counts(team, player)
        for grouped_item_name, grouped_item_id in grouped_item_ids.items():
            count: int = inventory[grouped_item_id]
            if count > 0:
                for replacement_item in grouped_item_replacements[grouped_item_name]:
                    replacement_id: int = replacement_item_ids[replacement_item]
                    if replacement_id not in inventory or count > inventory[replacement_id]:
                        # If two groups provide the same individual item, maximum is used
                        # (this behavior is used for Protoss Shields)
                        inventory[replacement_id] = count

        # Determine display for progressive items
        progressive_items = {
            "Progressive Terran Infantry Weapon":                   100 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Infantry Armor":                    102 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Vehicle Weapon":                    103 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Vehicle Armor":                     104 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Ship Weapon":                       105 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Terran Ship Armor":                        106 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Fire-Suppression System":                  206 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Orbital Command":                          207 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Marine)":                        208 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Firebat)":                       226 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Marauder)":                      228 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Reaper)":                        250 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Hellion)":                       259 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Replenishable Magazine (Vulture)":         303 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Tri-Lithium Power Cell (Diamondback)":     306 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Tomahawk Power Cells (Wraith)":            312 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Cross-Spectrum Dampeners (Banshee)":       316 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Missile Pods (Battlecruiser)":             318 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Defensive Matrix (Battlecruiser)":         319 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Immortality Protocol (Thor)":              325 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive High Impact Payload (Thor)":               361 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Augmented Thrusters (Planetary Fortress)": 388 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Regenerative Bio-Steel":                   617 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stealth Suit Module (Nova Suit Module)":   904 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Zerg Melee Attack":                        100 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Missile Attack":                      101 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Ground Carapace":                     102 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Flyer Attack":                        103 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Zerg Flyer Carapace":                      104 + SC2HOTS_ITEM_ID_OFFSET,
            "Progressive Protoss Ground Weapon":                    100 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Ground Armor":                     101 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Shields":                          102 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Air Weapon":                       103 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Protoss Air Armor":                        104 + SC2LOTV_ITEM_ID_OFFSET,
            "Progressive Proxy Pylon (Spear of Adun Calldown)":     701 + SC2LOTV_ITEM_ID_OFFSET,
        }
        # Format: L0, L1, L2, L3
        progressive_names = {
            "Progressive Terran Infantry Weapon":               ["Terran Infantry Weapons Level 1", 
                                                                 "Terran Infantry Weapons Level 1",
                                                                 "Terran Infantry Weapons Level 2", 
                                                                 "Terran Infantry Weapons Level 3"],
            "Progressive Terran Infantry Armor":                ["Terran Infantry Armor Level 1", 
                                                                 "Terran Infantry Armor Level 1",
                                                                 "Terran Infantry Armor Level 2", 
                                                                 "Terran Infantry Armor Level 3"],
            "Progressive Terran Vehicle Weapon":                ["Terran Vehicle Weapons Level 1", 
                                                                 "Terran Vehicle Weapons Level 1",
                                                                 "Terran Vehicle Weapons Level 2", 
                                                                 "Terran Vehicle Weapons Level 3"],
            "Progressive Terran Vehicle Armor":                 ["Terran Vehicle Armor Level 1", 
                                                                 "Terran Vehicle Armor Level 1",
                                                                 "Terran Vehicle Armor Level 2", 
                                                                 "Terran Vehicle Armor Level 3"],
            "Progressive Terran Ship Weapon":                   ["Terran Ship Weapons Level 1",
                                                                 "Terran Ship Weapons Level 1",
                                                                 "Terran Ship Weapons Level 2",
                                                                 "Terran Ship Weapons Level 3"],
            "Progressive Terran Ship Armor":                    ["Terran Ship Armor Level 1", 
                                                                 "Terran Ship Armor Level 1",
                                                                 "Terran Ship Armor Level 2", 
                                                                 "Terran Ship Armor Level 3"],
            "Progressive Fire-Suppression System":              ["Fire-Suppression System Level 1",
                                                                 "Fire-Suppression System Level 1",
                                                                 "Fire-Suppression System Level 2"],
            "Progressive Orbital Command":                      ["Orbital Command", "Orbital Command",
                                                                 "Planetary Command Module"],
            "Progressive Stimpack (Marine)":                    ["Stimpack (Marine)", "Stimpack (Marine)",
                                                                 "Super Stimpack (Marine)"],
            "Progressive Stimpack (Firebat)":                   ["Stimpack (Firebat)", "Stimpack (Firebat)",
                                                                 "Super Stimpack (Firebat)"],
            "Progressive Stimpack (Marauder)":                  ["Stimpack (Marauder)", "Stimpack (Marauder)",
                                                                 "Super Stimpack (Marauder)"],
            "Progressive Stimpack (Reaper)":                    ["Stimpack (Reaper)", "Stimpack (Reaper)",
                                                                 "Super Stimpack (Reaper)"],
            "Progressive Stimpack (Hellion)":                   ["Stimpack (Hellion)", "Stimpack (Hellion)",
                                                                 "Super Stimpack (Hellion)"],
            "Progressive Replenishable Magazine (Vulture)":     ["Replenishable Magazine (Vulture)",
                                                                 "Replenishable Magazine (Vulture)",
                                                                 "Replenishable Magazine (Free) (Vulture)"],
            "Progressive Tri-Lithium Power Cell (Diamondback)": ["Tri-Lithium Power Cell (Diamondback)",
                                                                 "Tri-Lithium Power Cell (Diamondback)",
                                                                 "Tungsten Spikes (Diamondback)"],
            "Progressive Tomahawk Power Cells (Wraith)":        ["Tomahawk Power Cells (Wraith)",
                                                                 "Tomahawk Power Cells (Wraith)",
                                                                 "Unregistered Cloaking Module (Wraith)"],
            "Progressive Cross-Spectrum Dampeners (Banshee)":   ["Cross-Spectrum Dampeners (Banshee)",
                                                                 "Cross-Spectrum Dampeners (Banshee)",
                                                                 "Advanced Cross-Spectrum Dampeners (Banshee)"],
            "Progressive Missile Pods (Battlecruiser)":         ["Missile Pods (Battlecruiser) Level 1",
                                                                 "Missile Pods (Battlecruiser) Level 1",
                                                                 "Missile Pods (Battlecruiser) Level 2"],
            "Progressive Defensive Matrix (Battlecruiser)":     ["Defensive Matrix (Battlecruiser)",
                                                                 "Defensive Matrix (Battlecruiser)",
                                                                 "Advanced Defensive Matrix (Battlecruiser)"],
            "Progressive Immortality Protocol (Thor)":          ["Immortality Protocol (Thor)",
                                                                 "Immortality Protocol (Thor)",
                                                                 "Immortality Protocol (Free) (Thor)"],
            "Progressive High Impact Payload (Thor)":           ["High Impact Payload (Thor)",
                                                                 "High Impact Payload (Thor)", "Smart Servos (Thor)"],
            "Progressive Augmented Thrusters (Planetary Fortress)": ["Lift Off (Planetary Fortress)",
                                                                     "Lift Off (Planetary Fortress)",
                                                                     "Armament Stabilizers (Planetary Fortress)"],
            "Progressive Regenerative Bio-Steel":               ["Regenerative Bio-Steel Level 1",
                                                                 "Regenerative Bio-Steel Level 1",
                                                                 "Regenerative Bio-Steel Level 2",
                                                                 "Regenerative Bio-Steel Level 3"],
            "Progressive Stealth Suit Module (Nova Suit Module)": ["Stealth Suit Module (Nova Suit Module)",
                                                                   "Cloak (Nova Suit Module)",
                                                                   "Permanently Cloaked (Nova Suit Module)"],
            "Progressive Zerg Melee Attack":                    ["Zerg Melee Attack Level 1",
                                                                 "Zerg Melee Attack Level 1",
                                                                 "Zerg Melee Attack Level 2",
                                                                 "Zerg Melee Attack Level 3"],
            "Progressive Zerg Missile Attack":                  ["Zerg Missile Attack Level 1",
                                                                 "Zerg Missile Attack Level 1",
                                                                 "Zerg Missile Attack Level 2",
                                                                 "Zerg Missile Attack Level 3"],
            "Progressive Zerg Ground Carapace":                 ["Zerg Ground Carapace Level 1",
                                                                 "Zerg Ground Carapace Level 1",
                                                                 "Zerg Ground Carapace Level 2",
                                                                 "Zerg Ground Carapace Level 3"],
            "Progressive Zerg Flyer Attack":                    ["Zerg Flyer Attack Level 1",
                                                                 "Zerg Flyer Attack Level 1",
                                                                 "Zerg Flyer Attack Level 2",
                                                                 "Zerg Flyer Attack Level 3"],
            "Progressive Zerg Flyer Carapace":                  ["Zerg Flyer Carapace Level 1",
                                                                 "Zerg Flyer Carapace Level 1",
                                                                 "Zerg Flyer Carapace Level 2",
                                                                 "Zerg Flyer Carapace Level 3"],
            "Progressive Protoss Ground Weapon":                ["Protoss Ground Weapon Level 1",
                                                                 "Protoss Ground Weapon Level 1",
                                                                 "Protoss Ground Weapon Level 2",
                                                                 "Protoss Ground Weapon Level 3"],
            "Progressive Protoss Ground Armor":                 ["Protoss Ground Armor Level 1",
                                                                 "Protoss Ground Armor Level 1",
                                                                 "Protoss Ground Armor Level 2",
                                                                 "Protoss Ground Armor Level 3"],
            "Progressive Protoss Shields":                      ["Protoss Shields Level 1", "Protoss Shields Level 1",
                                                                 "Protoss Shields Level 2", "Protoss Shields Level 3"],
            "Progressive Protoss Air Weapon":                   ["Protoss Air Weapon Level 1",
                                                                 "Protoss Air Weapon Level 1",
                                                                 "Protoss Air Weapon Level 2",
                                                                 "Protoss Air Weapon Level 3"],
            "Progressive Protoss Air Armor":                    ["Protoss Air Armor Level 1",
                                                                 "Protoss Air Armor Level 1",
                                                                 "Protoss Air Armor Level 2",
                                                                 "Protoss Air Armor Level 3"],
            "Progressive Proxy Pylon (Spear of Adun Calldown)": ["Proxy Pylon (Spear of Adun Calldown)",
                                                                 "Proxy Pylon (Spear of Adun Calldown)",
                                                                 "Warp In Reinforcements (Spear of Adun Calldown)"]
        }
        for item_name, item_id in progressive_items.items():
            level = min(inventory[item_id], len(progressive_names[item_name]) - 1)
            display_name = progressive_names[item_name][level]
            base_name = (item_name.split(maxsplit=1)[1].lower()
                         .replace(' ', '_')
                         .replace("-", "")
                         .replace("(", "")
                         .replace(")", ""))
            display_data[base_name + "_level"] = level
            display_data[base_name + "_url"] = icons[display_name] if display_name in icons else "FIXME"
            display_data[base_name + "_name"] = display_name

        # Multi-items
        multi_items = {
            "Additional Starting Minerals": 800 + SC2WOL_ITEM_ID_OFFSET,
            "Additional Starting Vespene":  801 + SC2WOL_ITEM_ID_OFFSET,
            "Additional Starting Supply":   802 + SC2WOL_ITEM_ID_OFFSET
        }
        for item_name, item_id in multi_items.items():
            base_name = item_name.split()[-1].lower()
            count = inventory[item_id]
            if base_name == "supply":
                count = count * starting_supply_per_item
            elif base_name == "minerals":
                count = count * minerals_per_item
            elif base_name == "vespene":
                count = count * vespene_per_item
            display_data[base_name + "_count"] = count
        # Kerrigan level
        level_items = {
            "1 Kerrigan Level":     509 + SC2HOTS_ITEM_ID_OFFSET,
            "2 Kerrigan Levels":    508 + SC2HOTS_ITEM_ID_OFFSET,
            "3 Kerrigan Levels":    507 + SC2HOTS_ITEM_ID_OFFSET,
            "4 Kerrigan Levels":    506 + SC2HOTS_ITEM_ID_OFFSET,
            "5 Kerrigan Levels":    505 + SC2HOTS_ITEM_ID_OFFSET,
            "6 Kerrigan Levels":    504 + SC2HOTS_ITEM_ID_OFFSET,
            "7 Kerrigan Levels":    503 + SC2HOTS_ITEM_ID_OFFSET,
            "8 Kerrigan Levels":    502 + SC2HOTS_ITEM_ID_OFFSET,
            "9 Kerrigan Levels":    501 + SC2HOTS_ITEM_ID_OFFSET,
            "10 Kerrigan Levels":   500 + SC2HOTS_ITEM_ID_OFFSET,
            "14 Kerrigan Levels":   510 + SC2HOTS_ITEM_ID_OFFSET,
            "35 Kerrigan Levels":   511 + SC2HOTS_ITEM_ID_OFFSET,
            "70 Kerrigan Levels":   512 + SC2HOTS_ITEM_ID_OFFSET,
        }
        level_amounts = {
            "1 Kerrigan Level":     1,
            "2 Kerrigan Levels":    2,
            "3 Kerrigan Levels":    3,
            "4 Kerrigan Levels":    4,
            "5 Kerrigan Levels":    5,
            "6 Kerrigan Levels":    6,
            "7 Kerrigan Levels":    7,
            "8 Kerrigan Levels":    8,
            "9 Kerrigan Levels":    9,
            "10 Kerrigan Levels":   10,
            "14 Kerrigan Levels":   14,
            "35 Kerrigan Levels":   35,
            "70 Kerrigan Levels":   70,
        }
        kerrigan_level = 0
        for item_name, item_id in level_items.items():
            count = inventory[item_id]
            amount = level_amounts[item_name]
            kerrigan_level += count * amount
        display_data["kerrigan_level"] = kerrigan_level

        # Victory condition
        game_state = tracker_data.get_player_client_status(team, player)
        display_data["game_finished"] = game_state == 30

        # Turn location IDs into mission objective counts
        locations = tracker_data.get_player_locations(team, player)
        checked_locations = tracker_data.get_player_checked_locations(team, player)
        lookup_name = lambda id: tracker_data.location_id_to_name["Starcraft 2"][id]
        location_info = {mission_name: {lookup_name(id): (id in checked_locations) for id in mission_locations if
                                        id in set(locations)} for mission_name, mission_locations in
                         sc2wol_location_ids.items()}
        checks_done = {mission_name: len(
            [id for id in mission_locations if id in checked_locations and id in set(locations)]) for
                       mission_name, mission_locations in sc2wol_location_ids.items()}
        checks_done['Total'] = len(checked_locations)
        checks_in_area = {mission_name: len([id for id in mission_locations if id in set(locations)]) for
                          mission_name, mission_locations in sc2wol_location_ids.items()}
        checks_in_area['Total'] = sum(checks_in_area.values())

        lookup_any_item_id_to_name = tracker_data.item_id_to_name["Starcraft 2"]
        return render_template(
            "tracker__Starcraft2.html",
            inventory=inventory,
            icons=icons,
            acquired_items={lookup_any_item_id_to_name[id] for id, count in inventory.items() if count > 0},
            player=player,
            team=team,
            room=tracker_data.room,
            player_name=tracker_data.get_player_name(team, player),
            checks_done=checks_done,
            checks_in_area=checks_in_area,
            location_info=location_info,
            **display_data,
        )

    _player_trackers["Starcraft 2"] = render_Starcraft2_tracker
