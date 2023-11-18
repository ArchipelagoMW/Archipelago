import datetime
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from uuid import UUID

from flask import render_template
from werkzeug.exceptions import abort

from MultiServer import Context, get_saving_second
from NetUtils import ClientStatus, Hint, NetworkItem, NetworkSlot, SlotType
from Utils import restricted_loads
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
        self.item_id_to_name: Dict[str, Dict[int, str]] = {}
        self.location_id_to_name: Dict[str, Dict[int, str]] = {}
        for game, game_package in self._multidata["datapackage"].items():
            game_package = restricted_loads(GameDataPackage.get(checksum=game_package["checksum"]).data)
            self.item_id_to_name[game] = {id: name for name, id in game_package["item_name_to_id"].items()}
            self.location_id_to_name[game] = {id: name for name, id in game_package["location_name_to_id"].items()}

            # Normal lookup tables as well.
            self.item_name_to_id[game] = game_package["item_name_to_id"]
            self.location_name_to_id[game] = game_package["item_name_to_id"]

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
    def get_player_inventory_counts(self, team: int, player: int) -> Dict[int, int]:
        """Retrieves a dictionary of all items received by their id and their received count."""
        items = self.get_player_received_items(team, player)
        inventory = {item: 0 for item in self.item_id_to_name[self.get_player_game(team, player)]}
        for item in items:
            inventory[item.item] += 1

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
                self.get_player_client_status(team, player) == ClientStatus.CLIENT_GOAL
                for player in players if self.get_slot_info(team, player).type == SlotType.player
            ) for team, players in self.get_team_players().items()
        }

    @_cache_results
    def get_team_hints(self) -> Dict[int, Set[Hint]]:
        """Retrieves a dictionary of all hints per team."""
        hints = {}
        for team, players in self.get_team_players().items():
            hints[team] = set()
            for player in players:
                hints[team] |= self.get_player_hints(team, player)

        return hints

    @_cache_results
    def get_team_locations_total_count(self) -> Dict[int, int]:
        """Retrieves a dictionary of total player locations each team has."""
        return {
            team: sum(len(self.get_player_locations(team, player)) for player in players)
            for team, players in self.get_team_players().items()
        }

    @_cache_results
    def get_team_locations_checked_count(self) -> Dict[int, int]:
        """Retrieves a dictionary of checked player locations each team has."""
        return {
            team: sum(len(self.get_player_checked_locations(team, player)) for player in players)
            for team, players in self.get_team_players().items()
        }

    # TODO: Change this method to properly build for each team once teams are properly implemented, as they don't
    #       currently exist in multidata to easily look up, so these are all assuming only 1 team: Team #0
    @_cache_results
    def get_team_players(self) -> Dict[int, List[int]]:
        """Retrieves a dictionary of all players ids on each team."""
        return {
            0: [player for player, slot_info in self._multidata["slot_info"].items()]
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
            for team, players in self.get_team_players().items() for player in players
        }

    @_cache_results
    def get_room_games(self) -> Dict[TeamPlayer, str]:
        """Retrieves a dictionary of games for each player."""
        return {
            (team, player): self.get_player_game(team, player)
            for team, players in self.get_team_players().items() for player in players
        }

    @_cache_results
    def get_room_locations_complete(self) -> Dict[TeamPlayer, int]:
        """Retrieves a dictionary of all locations complete per player."""
        return {
            (team, player): len(self.get_player_checked_locations(team, player))
            for team, players in self.get_team_players().items() for player in players
        }

    @_cache_results
    def get_room_client_statuses(self) -> Dict[TeamPlayer, ClientStatus]:
        """Retrieves a dictionary of all ClientStatus values per player."""
        return {
            (team, player): self.get_player_client_status(team, player)
            for team, players in self.get_team_players().items() for player in players
        }

    @_cache_results
    def get_room_long_player_names(self) -> Dict[TeamPlayer, str]:
        """Retrieves a dictionary of names with aliases for each player."""
        long_player_names = {}
        for team, players in self.get_team_players().items():
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


@app.route("/tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>")
def get_player_tracker(tracker: UUID, tracked_team: int, tracked_player: int, generic: bool = False) -> str:
    key = f"{tracker}_{tracked_team}_{tracked_player}_{generic}"
    tracker_page = cache.get(key)
    if tracker_page:
        return tracker_page

    timeout, tracker_page = get_timeout_and_tracker(tracker, tracked_team, tracked_player, generic)
    cache.set(key, tracker_page, timeout)
    return tracker_page


@app.route("/generic_tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>")
def get_generic_game_tracker(tracker: UUID, tracked_team: int, tracked_player: int) -> str:
    return get_player_tracker(tracker, tracked_team, tracked_player, True)


@app.route("/tracker/<suuid:tracker>", defaults={"game": "Generic"})
@app.route("/tracker/<suuid:tracker>/<game>")
@cache.memoize(timeout=TRACKER_CACHE_TIMEOUT_IN_SECONDS)
def get_multiworld_tracker(tracker: UUID, game: str):
    # Room must exist.
    room = Room.get(tracker=tracker)
    if not room:
        abort(404)

    tracker_data = TrackerData(room)
    enabled_trackers = list(get_enabled_multiworld_trackers(room).keys())
    if game not in _multiworld_trackers:
        return render_generic_multiworld_tracker(tracker_data, enabled_trackers)

    return _multiworld_trackers[game](tracker_data, enabled_trackers)


def get_timeout_and_tracker(tracker: UUID, tracked_team: int, tracked_player: int, generic: bool) -> Tuple[int, str]:
    # Room must exist.
    room = Room.get(tracker=tracker)
    if not room:
        abort(404)

    tracker_data = TrackerData(room)

    # Load and render the game-specific player tracker, or fallback to generic tracker if none exists.
    game_specific_tracker = _player_trackers.get(tracker_data.get_player_game(tracked_team, tracked_player), None)
    if game_specific_tracker and not generic:
        tracker = game_specific_tracker(tracker_data, tracked_team, tracked_player)
    else:
        tracker = render_generic_tracker(tracker_data, tracked_team, tracked_player)

    return (tracker_data.get_room_saving_second() - datetime.datetime.now().second) % 60 or 60, tracker


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

    # Add received index to all received items, excluding starting inventory.
    received_items_in_order = {}
    for received_index, network_item in enumerate(tracker_data.get_player_received_items(team, player), start=1):
        received_items_in_order[network_item.item] = received_index

    return render_template(
        template_name_or_list="genericTracker.html",
        game_specific_tracker=game in _player_trackers,
        room=tracker_data.room,
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
        room_players=tracker_data.get_team_players(),
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
    )


# TODO: This is a temporary solution until a proper Tracker API can be implemented for tracker templates and data to
#       live in their respective world folders.
import collections

from worlds import network_data_package


if "Factorio" in network_data_package["games"]:
    def render_Factorio_multiworld_tracker(tracker_data: TrackerData, enabled_trackers: List[str]):
        inventories: Dict[TeamPlayer, Dict[int, int]] = {
            (team, player): {
                tracker_data.item_id_to_name["Factorio"][item_id]: count
                for item_id, count in tracker_data.get_player_inventory_counts(team, player).items()
            } for team, players in tracker_data.get_team_players().items() for player in players
            if tracker_data.get_player_game(team, player) == "Factorio"
        }

        return render_template(
            "multitracker__Factorio.html",
            enabled_trackers=enabled_trackers,
            current_tracker="Factorio",
            room=tracker_data.room,
            room_players=tracker_data.get_team_players(),
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
    def render_ALinkToThePast_multiworld_tracker(tracker_data: TrackerData, enabled_trackers: List[str]):
        # Helper objects.
        alttp_id_lookup = tracker_data.item_name_to_id["A Link to the Past"]

        multi_items = {
            alttp_id_lookup[name]
            for name in ("Progressive Sword", "Progressive Bow", "Bottle", "Progressive Glove", "Triforce Piece")
        }
        links = {
            "Bow":                   "Progressive Bow",
            "Silver Arrows":         "Progressive Bow",
            "Silver Bow":            "Progressive Bow",
            "Progressive Bow (Alt)": "Progressive Bow",
            "Bottle (Red Potion)":   "Bottle",
            "Bottle (Green Potion)": "Bottle",
            "Bottle (Blue Potion)":  "Bottle",
            "Bottle (Fairy)":        "Bottle",
            "Bottle (Bee)":          "Bottle",
            "Bottle (Good Bee)":     "Bottle",
            "Fighter Sword":         "Progressive Sword",
            "Master Sword":          "Progressive Sword",
            "Tempered Sword":        "Progressive Sword",
            "Golden Sword":          "Progressive Sword",
            "Power Glove":           "Progressive Glove",
            "Titans Mitts":          "Progressive Glove",
        }
        links = {alttp_id_lookup[key]: alttp_id_lookup[value] for key, value in links.items()}
        levels = {
            "Fighter Sword":   1,
            "Master Sword":    2,
            "Tempered Sword":  3,
            "Golden Sword":    4,
            "Power Glove":     1,
            "Titans Mitts":    2,
            "Bow":             1,
            "Silver Bow":      2,
            "Triforce Piece": 90,
        }
        tracking_names = [
            "Progressive Sword", "Progressive Bow", "Book of Mudora", "Hammer", "Hookshot", "Magic Mirror", "Flute",
            "Pegasus Boots", "Progressive Glove", "Flippers", "Moon Pearl", "Blue Boomerang", "Red Boomerang",
            "Bug Catching Net", "Cape", "Shovel", "Lamp", "Mushroom", "Magic Powder", "Cane of Somaria",
            "Cane of Byrna", "Fire Rod", "Ice Rod", "Bombos", "Ether", "Quake", "Bottle", "Triforce Piece", "Triforce",
        ]
        default_locations = {
            "Light World": {
                1572864, 1572865, 60034, 1572867, 1572868, 60037, 1572869, 1572866, 60040, 59788, 60046, 60175,
                1572880, 60049, 60178, 1572883, 60052, 60181, 1572885, 60055, 60184, 191256, 60058, 60187, 1572884,
                1572886, 1572887, 1572906, 60202, 60205, 59824, 166320, 1010170, 60208, 60211, 60214, 60217, 59836,
                60220, 60223, 59839, 1573184, 60226, 975299, 1573188, 1573189, 188229, 60229, 60232, 1573193,
                1573194, 60235, 1573187, 59845, 59854, 211407, 60238, 59857, 1573185, 1573186, 1572882, 212328,
                59881, 59761, 59890, 59770, 193020, 212605
            },
            "Dark World": {
                59776, 59779, 975237, 1572870, 60043, 1572881, 60190, 60193, 60196, 60199, 60840, 1573190, 209095,
                1573192, 1573191, 60241, 60244, 60247, 60250, 59884, 59887, 60019, 60022, 60028, 60031
            },
            "Desert Palace": {1573216, 59842, 59851, 59791, 1573201, 59830},
            "Eastern Palace": {1573200, 59827, 59893, 59767, 59833, 59773},
            "Hyrule Castle": {60256, 60259, 60169, 60172, 59758, 59764, 60025, 60253},
            "Agahnims Tower": {60082, 60085},
            "Tower of Hera": {1573218, 59878, 59821, 1573202, 59896, 59899},
            "Swamp Palace": {60064, 60067, 60070, 59782, 59785, 60073, 60076, 60079, 1573204, 60061},
            "Thieves Town": {59905, 59908, 59911, 59914, 59917, 59920, 59923, 1573206},
            "Skull Woods": {59809, 59902, 59848, 59794, 1573205, 59800, 59803, 59806},
            "Ice Palace": {59872, 59875, 59812, 59818, 59860, 59797, 1573207, 59869},
            "Misery Mire": {60001, 60004, 60007, 60010, 60013, 1573208, 59866, 59998},
            "Turtle Rock": {59938, 59941, 59944, 1573209, 59947, 59950, 59953, 59956, 59926, 59929, 59932, 59935},
            "Palace of Darkness": {
                59968, 59971, 59974, 59977, 59980, 59983, 59986, 1573203, 59989, 59959, 59992, 59962, 59995,
                59965
            },
            "Ganons Tower": {
                60160, 60163, 60166, 60088, 60091, 60094, 60097, 60100, 60103, 60106, 60109, 60112, 60115, 60118,
                60121, 60124, 60127, 1573217, 60130, 60133, 60136, 60139, 60142, 60145, 60148, 60151, 60157
            },
            "Total": set()
        }
        key_only_locations = {
            "Light World": set(),
            "Dark World": set(),
            "Desert Palace": {0x140031, 0x14002b, 0x140061, 0x140028},
            "Eastern Palace": {0x14005b, 0x140049},
            "Hyrule Castle": {0x140037, 0x140034, 0x14000d, 0x14003d},
            "Agahnims Tower": {0x140061, 0x140052},
            "Tower of Hera": set(),
            "Swamp Palace": {0x140019, 0x140016, 0x140013, 0x140010, 0x14000a},
            "Thieves Town": {0x14005e, 0x14004f},
            "Skull Woods": {0x14002e, 0x14001c},
            "Ice Palace": {0x140004, 0x140022, 0x140025, 0x140046},
            "Misery Mire": {0x140055, 0x14004c, 0x140064},
            "Turtle Rock": {0x140058, 0x140007},
            "Palace of Darkness": set(),
            "Ganons Tower": {0x140040, 0x140043, 0x14003a, 0x14001f},
            "Total": set()
        }
        location_to_area = {}
        for area, locations in default_locations.items():
            for location in locations:
                location_to_area[location] = area
        for area, locations in key_only_locations.items():
            for location in locations:
                location_to_area[location] = area

        checks_in_area = {area: len(checks) for area, checks in default_locations.items()}
        checks_in_area["Total"] = 216
        ordered_areas = (
            "Light World", "Dark World", "Hyrule Castle", "Agahnims Tower", "Eastern Palace", "Desert Palace",
            "Tower of Hera", "Palace of Darkness", "Swamp Palace", "Skull Woods", "Thieves Town", "Ice Palace",
            "Misery Mire", "Turtle Rock", "Ganons Tower", "Total"
        )

        player_checks_in_area = {
            (team, player): {
                area_name: len(tracker_data._multidata["checks_in_area"][player][area_name])
                if area_name != "Total" else tracker_data._multidata["checks_in_area"][player]["Total"]
                for area_name in ordered_areas
            }
            for team, players in tracker_data.get_team_players().items()
            for player in players
            if tracker_data.get_slot_info(team, player).type != SlotType.group and
            tracker_data.get_slot_info(team, player).game == "A Link to the Past"
        }

        tracking_ids = []
        for item in tracking_names:
            tracking_ids.append(alttp_id_lookup[item])

        # Can't wait to get this into the apworld. Oof.
        from worlds.alttp import Items

        small_key_ids = {}
        big_key_ids = {}
        ids_small_key = {}
        ids_big_key = {}
        for item_name, data in Items.item_table.items():
            if "Key" in item_name:
                area = item_name.split("(")[1][:-1]
                if "Small" in item_name:
                    small_key_ids[area] = data[2]
                    ids_small_key[data[2]] = area
                else:
                    big_key_ids[area] = data[2]
                    ids_big_key[data[2]] = area

        def _get_location_table(checks_table: dict) -> dict:
            loc_to_area = {}
            for area, locations in checks_table.items():
                if area == "Total":
                    continue
                for location in locations:
                    loc_to_area[location] = area
            return loc_to_area

        player_location_to_area = {
            (team, player): _get_location_table(tracker_data._multidata["checks_in_area"][player])
            for team, players in tracker_data.get_team_players().items()
            for player in players
            if tracker_data.get_slot_info(team, player).type != SlotType.group and
            tracker_data.get_slot_info(team, player).game == "A Link to the Past"
        }

        checks_done: Dict[TeamPlayer, Dict[str: int]] = {
            (team, player): {location_name: 0 for location_name in default_locations}
            for team, players in tracker_data.get_team_players().items()
            for player in players
            if tracker_data.get_slot_info(team, player).type != SlotType.group and
            tracker_data.get_slot_info(team, player).game == "A Link to the Past"
        }

        inventories: Dict[TeamPlayer, Dict[int, int]] = {}
        player_big_key_locations = {(player): set() for player in tracker_data.get_team_players()[0]}
        player_small_key_locations = {player: set() for player in tracker_data.get_team_players()[0]}
        group_big_key_locations = set()
        group_key_locations = set()

        for (team, player), locations in checks_done.items():
            # Check if game complete.
            if tracker_data.get_player_client_status(team, player) == ClientStatus.CLIENT_GOAL:
                inventories[team, player][106] = 1  # Triforce

            # Count number of locations checked.
            for location in tracker_data.get_player_checked_locations(team, player):
                checks_done[team, player][player_location_to_area[team, player][location]] += 1
                checks_done[team, player]["Total"] += 1

            # Count keys.
            for location, (item, receiving, _) in tracker_data.get_player_locations(team, player).items():
                if item in ids_big_key:
                    player_big_key_locations[receiving].add(ids_big_key[item])
                elif item in ids_small_key:
                    player_small_key_locations[receiving].add(ids_small_key[item])

            # Iterate over received items and build inventory/key counts.
            inventories[team, player] = collections.Counter()
            for network_item in tracker_data.get_player_received_items(team, player):
                target_item = links.get(network_item.item, network_item.item)
                if network_item.item in levels:  # non-progressive
                    inventories[team, player][target_item] = (max(inventories[team, player][target_item], levels[network_item.item]))
                else:
                    inventories[team, player][target_item] += 1

            group_key_locations |= player_small_key_locations[player]
            group_big_key_locations |= player_big_key_locations[player]

        return render_template(
            "multitracker__ALinkToThePast.html",
            enabled_trackers=enabled_trackers,
            current_tracker="A Link to the Past",
            room=tracker_data.room,
            room_players=tracker_data.get_team_players(),
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
            tracking_names=tracking_names,
            tracking_ids=tracking_ids,
            multi_items=multi_items,
            checks_done=checks_done,
            ordered_areas=ordered_areas,
            checks_in_area=player_checks_in_area,
            key_locations=group_key_locations,
            big_key_locations=group_big_key_locations,
            small_key_ids=small_key_ids,
            big_key_ids=big_key_ids,
        )

    def render_ALinkToThePast_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        # Helper objects.
        alttp_id_lookup = tracker_data.item_name_to_id["A Link to the Past"]

        links = {
            "Bow":                   "Progressive Bow",
            "Silver Arrows":         "Progressive Bow",
            "Silver Bow":            "Progressive Bow",
            "Progressive Bow (Alt)": "Progressive Bow",
            "Bottle (Red Potion)":   "Bottle",
            "Bottle (Green Potion)": "Bottle",
            "Bottle (Blue Potion)":  "Bottle",
            "Bottle (Fairy)":        "Bottle",
            "Bottle (Bee)":          "Bottle",
            "Bottle (Good Bee)":     "Bottle",
            "Fighter Sword":         "Progressive Sword",
            "Master Sword":          "Progressive Sword",
            "Tempered Sword":        "Progressive Sword",
            "Golden Sword":          "Progressive Sword",
            "Power Glove":           "Progressive Glove",
            "Titans Mitts":          "Progressive Glove",
        }
        links = {alttp_id_lookup[key]: alttp_id_lookup[value] for key, value in links.items()}
        levels = {
            "Fighter Sword":   1,
            "Master Sword":    2,
            "Tempered Sword":  3,
            "Golden Sword":    4,
            "Power Glove":     1,
            "Titans Mitts":    2,
            "Bow":             1,
            "Silver Bow":      2,
            "Triforce Piece": 90,
        }
        tracking_names = [
            "Progressive Sword", "Progressive Bow", "Book of Mudora", "Hammer", "Hookshot", "Magic Mirror", "Flute",
            "Pegasus Boots", "Progressive Glove", "Flippers", "Moon Pearl", "Blue Boomerang", "Red Boomerang",
            "Bug Catching Net", "Cape", "Shovel", "Lamp", "Mushroom", "Magic Powder", "Cane of Somaria",
            "Cane of Byrna", "Fire Rod", "Ice Rod", "Bombos", "Ether", "Quake", "Bottle", "Triforce Piece", "Triforce",
        ]
        default_locations = {
            "Light World": {
                1572864, 1572865, 60034, 1572867, 1572868, 60037, 1572869, 1572866, 60040, 59788, 60046, 60175,
                1572880, 60049, 60178, 1572883, 60052, 60181, 1572885, 60055, 60184, 191256, 60058, 60187, 1572884,
                1572886, 1572887, 1572906, 60202, 60205, 59824, 166320, 1010170, 60208, 60211, 60214, 60217, 59836,
                60220, 60223, 59839, 1573184, 60226, 975299, 1573188, 1573189, 188229, 60229, 60232, 1573193,
                1573194, 60235, 1573187, 59845, 59854, 211407, 60238, 59857, 1573185, 1573186, 1572882, 212328,
                59881, 59761, 59890, 59770, 193020, 212605
            },
            "Dark World": {
                59776, 59779, 975237, 1572870, 60043, 1572881, 60190, 60193, 60196, 60199, 60840, 1573190, 209095,
                1573192, 1573191, 60241, 60244, 60247, 60250, 59884, 59887, 60019, 60022, 60028, 60031
            },
            "Desert Palace": {1573216, 59842, 59851, 59791, 1573201, 59830},
            "Eastern Palace": {1573200, 59827, 59893, 59767, 59833, 59773},
            "Hyrule Castle": {60256, 60259, 60169, 60172, 59758, 59764, 60025, 60253},
            "Agahnims Tower": {60082, 60085},
            "Tower of Hera": {1573218, 59878, 59821, 1573202, 59896, 59899},
            "Swamp Palace": {60064, 60067, 60070, 59782, 59785, 60073, 60076, 60079, 1573204, 60061},
            "Thieves Town": {59905, 59908, 59911, 59914, 59917, 59920, 59923, 1573206},
            "Skull Woods": {59809, 59902, 59848, 59794, 1573205, 59800, 59803, 59806},
            "Ice Palace": {59872, 59875, 59812, 59818, 59860, 59797, 1573207, 59869},
            "Misery Mire": {60001, 60004, 60007, 60010, 60013, 1573208, 59866, 59998},
            "Turtle Rock": {59938, 59941, 59944, 1573209, 59947, 59950, 59953, 59956, 59926, 59929, 59932, 59935},
            "Palace of Darkness": {
                59968, 59971, 59974, 59977, 59980, 59983, 59986, 1573203, 59989, 59959, 59992, 59962, 59995,
                59965
            },
            "Ganons Tower": {
                60160, 60163, 60166, 60088, 60091, 60094, 60097, 60100, 60103, 60106, 60109, 60112, 60115, 60118,
                60121, 60124, 60127, 1573217, 60130, 60133, 60136, 60139, 60142, 60145, 60148, 60151, 60157
            },
            "Total": set()
        }
        key_only_locations = {
            "Light World": set(),
            "Dark World": set(),
            "Desert Palace": {0x140031, 0x14002b, 0x140061, 0x140028},
            "Eastern Palace": {0x14005b, 0x140049},
            "Hyrule Castle": {0x140037, 0x140034, 0x14000d, 0x14003d},
            "Agahnims Tower": {0x140061, 0x140052},
            "Tower of Hera": set(),
            "Swamp Palace": {0x140019, 0x140016, 0x140013, 0x140010, 0x14000a},
            "Thieves Town": {0x14005e, 0x14004f},
            "Skull Woods": {0x14002e, 0x14001c},
            "Ice Palace": {0x140004, 0x140022, 0x140025, 0x140046},
            "Misery Mire": {0x140055, 0x14004c, 0x140064},
            "Turtle Rock": {0x140058, 0x140007},
            "Palace of Darkness": set(),
            "Ganons Tower": {0x140040, 0x140043, 0x14003a, 0x14001f},
            "Total": set()
        }
        location_to_area = {}
        for area, locations in default_locations.items():
            for checked_location in locations:
                location_to_area[checked_location] = area
        for area, locations in key_only_locations.items():
            for checked_location in locations:
                location_to_area[checked_location] = area

        checks_in_area = {area: len(checks) for area, checks in default_locations.items()}
        checks_in_area["Total"] = 216
        ordered_areas = (
            "Light World", "Dark World", "Hyrule Castle", "Agahnims Tower", "Eastern Palace", "Desert Palace",
            "Tower of Hera", "Palace of Darkness", "Swamp Palace", "Skull Woods", "Thieves Town", "Ice Palace",
            "Misery Mire", "Turtle Rock", "Ganons Tower", "Total"
        )

        tracking_ids = []
        for item in tracking_names:
            tracking_ids.append(alttp_id_lookup[item])

        # Can't wait to get this into the apworld. Oof.
        from worlds.alttp import Items

        small_key_ids = {}
        big_key_ids = {}
        ids_small_key = {}
        ids_big_key = {}
        for item_name, data in Items.item_table.items():
            if "Key" in item_name:
                area = item_name.split("(")[1][:-1]
                if "Small" in item_name:
                    small_key_ids[area] = data[2]
                    ids_small_key[data[2]] = area
                else:
                    big_key_ids[area] = data[2]
                    ids_big_key[data[2]] = area

        inventory = collections.Counter()
        checks_done = {loc_name: 0 for loc_name in default_locations}
        player_big_key_locations = set()
        player_small_key_locations = set()

        player_locations = tracker_data.get_player_locations(team, player)
        for checked_location in tracker_data.get_player_checked_locations(team, player):
            if checked_location in player_locations:
                area_name = location_to_area.get(checked_location, None)
                if area_name:
                    checks_done[area_name] += 1

                checks_done["Total"] += 1

        for received_item in tracker_data.get_player_received_items(team, player):
            target_item = links.get(received_item.item, received_item.item)
            if received_item.item in levels:  # non-progressive
                inventory[target_item] = max(inventory[target_item], levels[received_item.item])
            else:
                inventory[target_item] += 1

        for location, (item_id, _, _) in player_locations.items():
            if item_id in ids_big_key:
                player_big_key_locations.add(ids_big_key[item_id])
            elif item_id in ids_small_key:
                player_small_key_locations.add(ids_small_key[item_id])

        # Note the presence of the triforce item
        if tracker_data.get_player_client_status(team, player) == ClientStatus.CLIENT_GOAL:
            inventory[106] = 1  # Triforce

        # Progressive items need special handling for icons and class
        progressive_items = {
            "Progressive Sword":  94,
            "Progressive Glove":  97,
            "Progressive Bow":    100,
            "Progressive Mail":   96,
            "Progressive Shield": 95,
        }
        progressive_names = {
            "Progressive Sword":  [None, "Fighter Sword", "Master Sword", "Tempered Sword", "Golden Sword"],
            "Progressive Glove":  [None, "Power Glove", "Titan Mitts"],
            "Progressive Bow":    [None, "Bow", "Silver Bow"],
            "Progressive Mail":   ["Green Mail", "Blue Mail", "Red Mail"],
            "Progressive Shield": [None, "Blue Shield", "Red Shield", "Mirror Shield"]
        }

        # Determine which icon to use
        display_data = {}
        for item_name, item_id in progressive_items.items():
            level = min(inventory[item_id], len(progressive_names[item_name]) - 1)
            display_name = progressive_names[item_name][level]
            acquired = True
            if not display_name:
                acquired = False
                display_name = progressive_names[item_name][level + 1]
            base_name = item_name.split(maxsplit=1)[1].lower()
            display_data[base_name + "_acquired"] = acquired
            display_data[base_name + "_icon"] = display_name

        # The single player tracker doesn't care about overworld, underworld, and total checks. Maybe it should?
        sp_areas = ordered_areas[2:15]

        return render_template(
            template_name_or_list="tracker__ALinkToThePast.html",
            room=tracker_data.room,
            team=team,
            player=player,
            inventory=inventory,
            player_name=tracker_data.get_player_name(team, player),
            checks_done=checks_done,
            checks_in_area=checks_in_area,
            acquired_items={tracker_data.item_id_to_name["A Link to the Past"][id] for id in inventory},
            sp_areas=sp_areas,
            small_key_ids=small_key_ids,
            key_locations=player_small_key_locations,
            big_key_ids=big_key_ids,
            big_key_locations=player_big_key_locations,
            **display_data,
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

if "Starcraft 2 Wings of Liberty" in network_data_package["games"]:
    def render_Starcraft2WingsOfLiberty_tracker(tracker_data: TrackerData, team: int, player: int) -> str:
        SC2WOL_LOC_ID_OFFSET = 1000
        SC2WOL_ITEM_ID_OFFSET = 1000

        icons = {
            "Starting Minerals":                           "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/icons/icon-mineral-protoss.png",
            "Starting Vespene":                            "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/icons/icon-gas-terran.png",
            "Starting Supply":                             "https://static.wikia.nocookie.net/starcraft/images/d/d3/TerranSupply_SC2_Icon1.gif",

            "Infantry Weapons Level 1":                    "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryweaponslevel1.png",
            "Infantry Weapons Level 2":                    "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryweaponslevel2.png",
            "Infantry Weapons Level 3":                    "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryweaponslevel3.png",
            "Infantry Armor Level 1":                      "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryarmorlevel1.png",
            "Infantry Armor Level 2":                      "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryarmorlevel2.png",
            "Infantry Armor Level 3":                      "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-infantryarmorlevel3.png",
            "Vehicle Weapons Level 1":                     "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleweaponslevel1.png",
            "Vehicle Weapons Level 2":                     "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleweaponslevel2.png",
            "Vehicle Weapons Level 3":                     "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleweaponslevel3.png",
            "Vehicle Armor Level 1":                       "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleplatinglevel1.png",
            "Vehicle Armor Level 2":                       "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleplatinglevel2.png",
            "Vehicle Armor Level 3":                       "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-vehicleplatinglevel3.png",
            "Ship Weapons Level 1":                        "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipweaponslevel1.png",
            "Ship Weapons Level 2":                        "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipweaponslevel2.png",
            "Ship Weapons Level 3":                        "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipweaponslevel3.png",
            "Ship Armor Level 1":                          "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipplatinglevel1.png",
            "Ship Armor Level 2":                          "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipplatinglevel2.png",
            "Ship Armor Level 3":                          "https://sclegacy.com/images/uploaded/starcraftii_beta/gamefiles/upgrades/btn-upgrade-terran-shipplatinglevel3.png",

            "Bunker":                                      "https://static.wikia.nocookie.net/starcraft/images/c/c5/Bunker_SC2_Icon1.jpg",
            "Missile Turret":                              "https://static.wikia.nocookie.net/starcraft/images/5/5f/MissileTurret_SC2_Icon1.jpg",
            "Sensor Tower":                                "https://static.wikia.nocookie.net/starcraft/images/d/d2/SensorTower_SC2_Icon1.jpg",

            "Projectile Accelerator (Bunker)":             "https://0rganics.org/archipelago/sc2wol/ProjectileAccelerator.png",
            "Neosteel Bunker (Bunker)":                    "https://0rganics.org/archipelago/sc2wol/NeosteelBunker.png",
            "Titanium Housing (Missile Turret)":           "https://0rganics.org/archipelago/sc2wol/TitaniumHousing.png",
            "Hellstorm Batteries (Missile Turret)":        "https://0rganics.org/archipelago/sc2wol/HellstormBatteries.png",
            "Advanced Construction (SCV)":                 "https://0rganics.org/archipelago/sc2wol/AdvancedConstruction.png",
            "Dual-Fusion Welders (SCV)":                   "https://0rganics.org/archipelago/sc2wol/Dual-FusionWelders.png",
            "Fire-Suppression System (Building)":          "https://0rganics.org/archipelago/sc2wol/Fire-SuppressionSystem.png",
            "Orbital Command (Building)":                  "https://0rganics.org/archipelago/sc2wol/OrbitalCommandCampaign.png",

            "Marine":                                      "https://static.wikia.nocookie.net/starcraft/images/4/47/Marine_SC2_Icon1.jpg",
            "Medic":                                       "https://static.wikia.nocookie.net/starcraft/images/7/74/Medic_SC2_Rend1.jpg",
            "Firebat":                                     "https://static.wikia.nocookie.net/starcraft/images/3/3c/Firebat_SC2_Rend1.jpg",
            "Marauder":                                    "https://static.wikia.nocookie.net/starcraft/images/b/ba/Marauder_SC2_Icon1.jpg",
            "Reaper":                                      "https://static.wikia.nocookie.net/starcraft/images/7/7d/Reaper_SC2_Icon1.jpg",

            "Stimpack (Marine)":                           "https://0rganics.org/archipelago/sc2wol/StimpacksCampaign.png",
            "Super Stimpack (Marine)":                     "/static/static/icons/sc2/superstimpack.png",
            "Combat Shield (Marine)":                      "https://0rganics.org/archipelago/sc2wol/CombatShieldCampaign.png",
            "Laser Targeting System (Marine)":             "/static/static/icons/sc2/lasertargetingsystem.png",
            "Magrail Munitions (Marine)":                  "/static/static/icons/sc2/magrailmunitions.png",
            "Optimized Logistics (Marine)":                "/static/static/icons/sc2/optimizedlogistics.png",
            "Advanced Medic Facilities (Medic)":           "https://0rganics.org/archipelago/sc2wol/AdvancedMedicFacilities.png",
            "Stabilizer Medpacks (Medic)":                 "https://0rganics.org/archipelago/sc2wol/StabilizerMedpacks.png",
            "Restoration (Medic)":                         "/static/static/icons/sc2/restoration.png",
            "Optical Flare (Medic)":                       "/static/static/icons/sc2/opticalflare.png",
            "Optimized Logistics (Medic)":                 "/static/static/icons/sc2/optimizedlogistics.png",
            "Incinerator Gauntlets (Firebat)":             "https://0rganics.org/archipelago/sc2wol/IncineratorGauntlets.png",
            "Juggernaut Plating (Firebat)":                "https://0rganics.org/archipelago/sc2wol/JuggernautPlating.png",
            "Stimpack (Firebat)":                          "https://0rganics.org/archipelago/sc2wol/StimpacksCampaign.png",
            "Super Stimpack (Firebat)":                    "/static/static/icons/sc2/superstimpack.png",
            "Optimized Logistics (Firebat)":               "/static/static/icons/sc2/optimizedlogistics.png",
            "Concussive Shells (Marauder)":                "https://0rganics.org/archipelago/sc2wol/ConcussiveShellsCampaign.png",
            "Kinetic Foam (Marauder)":                     "https://0rganics.org/archipelago/sc2wol/KineticFoam.png",
            "Stimpack (Marauder)":                         "https://0rganics.org/archipelago/sc2wol/StimpacksCampaign.png",
            "Super Stimpack (Marauder)":                   "/static/static/icons/sc2/superstimpack.png",
            "Laser Targeting System (Marauder)":           "/static/static/icons/sc2/lasertargetingsystem.png",
            "Magrail Munitions (Marauder)":                "/static/static/icons/sc2/magrailmunitions.png",
            "Internal Tech Module (Marauder)":             "/static/static/icons/sc2/internalizedtechmodule.png",
            "U-238 Rounds (Reaper)":                       "https://0rganics.org/archipelago/sc2wol/U-238Rounds.png",
            "G-4 Clusterbomb (Reaper)":                    "https://0rganics.org/archipelago/sc2wol/G-4Clusterbomb.png",
            "Stimpack (Reaper)":                           "https://0rganics.org/archipelago/sc2wol/StimpacksCampaign.png",
            "Super Stimpack (Reaper)":                     "/static/static/icons/sc2/superstimpack.png",
            "Laser Targeting System (Reaper)":             "/static/static/icons/sc2/lasertargetingsystem.png",
            "Advanced Cloaking Field (Reaper)":            "/static/static/icons/sc2/terran-cloak-color.png",
            "Spider Mines (Reaper)":                       "/static/static/icons/sc2/spidermine.png",
            "Combat Drugs (Reaper)":                       "/static/static/icons/sc2/reapercombatdrugs.png",

            "Hellion":                                     "https://static.wikia.nocookie.net/starcraft/images/5/56/Hellion_SC2_Icon1.jpg",
            "Vulture":                                     "https://static.wikia.nocookie.net/starcraft/images/d/da/Vulture_WoL.jpg",
            "Goliath":                                     "https://static.wikia.nocookie.net/starcraft/images/e/eb/Goliath_WoL.jpg",
            "Diamondback":                                 "https://static.wikia.nocookie.net/starcraft/images/a/a6/Diamondback_WoL.jpg",
            "Siege Tank":                                  "https://static.wikia.nocookie.net/starcraft/images/5/57/SiegeTank_SC2_Icon1.jpg",

            "Twin-Linked Flamethrower (Hellion)":          "https://0rganics.org/archipelago/sc2wol/Twin-LinkedFlamethrower.png",
            "Thermite Filaments (Hellion)":                "https://0rganics.org/archipelago/sc2wol/ThermiteFilaments.png",
            "Hellbat Aspect (Hellion)":                    "/static/static/icons/sc2/hellionbattlemode.png",
            "Smart Servos (Hellion)":                      "/static/static/icons/sc2/transformationservos.png",
            "Optimized Logistics (Hellion)":               "/static/static/icons/sc2/optimizedlogistics.png",
            "Jump Jets (Hellion)":                         "/static/static/icons/sc2/jumpjets.png",
            "Stimpack (Hellion)":                          "https://0rganics.org/archipelago/sc2wol/StimpacksCampaign.png",
            "Super Stimpack (Hellion)":                    "/static/static/icons/sc2/superstimpack.png",
            "Cerberus Mine (Spider Mine)":                 "https://0rganics.org/archipelago/sc2wol/CerberusMine.png",
            "High Explosive Munition (Spider Mine)":       "/static/static/icons/sc2/high-explosive-spidermine.png",
            "Replenishable Magazine (Vulture)":            "https://0rganics.org/archipelago/sc2wol/ReplenishableMagazine.png",
            "Ion Thrusters (Vulture)":                     "/static/static/icons/sc2/emergencythrusters.png",
            "Auto Launchers (Vulture)":                    "/static/static/icons/sc2/jotunboosters.png",
            "Multi-Lock Weapons System (Goliath)":         "https://0rganics.org/archipelago/sc2wol/Multi-LockWeaponsSystem.png",
            "Ares-Class Targeting System (Goliath)":       "https://0rganics.org/archipelago/sc2wol/Ares-ClassTargetingSystem.png",
            "Jump Jets (Goliath)":                         "/static/static/icons/sc2/jumpjets.png",
            "Optimized Logistics (Goliath)":               "/static/static/icons/sc2/optimizedlogistics.png",
            "Tri-Lithium Power Cell (Diamondback)":        "https://0rganics.org/archipelago/sc2wol/Tri-LithiumPowerCell.png",
            "Shaped Hull (Diamondback)":                   "https://0rganics.org/archipelago/sc2wol/ShapedHull.png",
            "Hyperfluxor (Diamondback)":                   "/static/static/icons/sc2/hyperfluxor.png",
            "Burst Capacitors (Diamondback)":              "/static/static/icons/sc2/burstcapacitors.png",
            "Optimized Logistics (Diamondback)":           "/static/static/icons/sc2/optimizedlogistics.png",
            "Maelstrom Rounds (Siege Tank)":               "https://0rganics.org/archipelago/sc2wol/MaelstromRounds.png",
            "Shaped Blast (Siege Tank)":                   "https://0rganics.org/archipelago/sc2wol/ShapedBlast.png",
            "Jump Jets (Siege Tank)":                      "/static/static/icons/sc2/jumpjets.png",
            "Spider Mines (Siege Tank)":                   "/static/static/icons/sc2/siegetank-spidermines.png",
            "Smart Servos (Siege Tank)":                   "/static/static/icons/sc2/transformationservos.png",
            "Graduating Range (Siege Tank)":               "/static/static/icons/sc2/siegetankrange.png",
            "Laser Targeting System (Siege Tank)":         "/static/static/icons/sc2/lasertargetingsystem.png",
            "Advanced Siege Tech (Siege Tank)":            "/static/static/icons/sc2/improvedsiegemode.png",
            "Internal Tech Module (Siege Tank)":           "/static/static/icons/sc2/internalizedtechmodule.png",

            "Medivac":                                     "https://static.wikia.nocookie.net/starcraft/images/d/db/Medivac_SC2_Icon1.jpg",
            "Wraith":                                      "https://static.wikia.nocookie.net/starcraft/images/7/75/Wraith_WoL.jpg",
            "Viking":                                      "https://static.wikia.nocookie.net/starcraft/images/2/2a/Viking_SC2_Icon1.jpg",
            "Banshee":                                     "https://static.wikia.nocookie.net/starcraft/images/3/32/Banshee_SC2_Icon1.jpg",
            "Battlecruiser":                               "https://static.wikia.nocookie.net/starcraft/images/f/f5/Battlecruiser_SC2_Icon1.jpg",

            "Rapid Deployment Tube (Medivac)":             "https://0rganics.org/archipelago/sc2wol/RapidDeploymentTube.png",
            "Advanced Healing AI (Medivac)":               "https://0rganics.org/archipelago/sc2wol/AdvancedHealingAI.png",
            "Expanded Hull (Medivac)":                     "/static/static/icons/sc2/neosteelfortifiedarmor.png",
            "Afterburners (Medivac)":                      "/static/static/icons/sc2/medivacemergencythrusters.png",
            "Tomahawk Power Cells (Wraith)":               "https://0rganics.org/archipelago/sc2wol/TomahawkPowerCells.png",
            "Displacement Field (Wraith)":                 "https://0rganics.org/archipelago/sc2wol/DisplacementField.png",
            "Advanced Laser Technology (Wraith)":          "/static/static/icons/sc2/improvedburstlaser.png",
            "Ripwave Missiles (Viking)":                   "https://0rganics.org/archipelago/sc2wol/RipwaveMissiles.png",
            "Phobos-Class Weapons System (Viking)":        "https://0rganics.org/archipelago/sc2wol/Phobos-ClassWeaponsSystem.png",
            "Smart Servos (Viking)":                       "/static/static/icons/sc2/transformationservos.png",
            "Magrail Munitions (Viking)":                  "/static/static/icons/sc2/magrailmunitions.png",
            "Cross-Spectrum Dampeners (Banshee)":          "/static/static/icons/sc2/crossspectrumdampeners.png",
            "Advanced Cross-Spectrum Dampeners (Banshee)": "https://0rganics.org/archipelago/sc2wol/Cross-SpectrumDampeners.png",
            "Shockwave Missile Battery (Banshee)":         "https://0rganics.org/archipelago/sc2wol/ShockwaveMissileBattery.png",
            "Hyperflight Rotors (Banshee)":                "/static/static/icons/sc2/hyperflightrotors.png",
            "Laser Targeting System (Banshee)":            "/static/static/icons/sc2/lasertargetingsystem.png",
            "Internal Tech Module (Banshee)":              "/static/static/icons/sc2/internalizedtechmodule.png",
            "Missile Pods (Battlecruiser)":                "https://0rganics.org/archipelago/sc2wol/MissilePods.png",
            "Defensive Matrix (Battlecruiser)":            "https://0rganics.org/archipelago/sc2wol/DefensiveMatrix.png",
            "Tactical Jump (Battlecruiser)":               "/static/static/icons/sc2/warpjump.png",
            "Cloak (Battlecruiser)":                       "/static/static/icons/sc2/terran-cloak-color.png",
            "ATX Laser Battery (Battlecruiser)":           "/static/static/icons/sc2/specialordance.png",
            "Optimized Logistics (Battlecruiser)":         "/static/static/icons/sc2/optimizedlogistics.png",
            "Internal Tech Module (Battlecruiser)":        "/static/static/icons/sc2/internalizedtechmodule.png",

            "Ghost":                                       "https://static.wikia.nocookie.net/starcraft/images/6/6e/Ghost_SC2_Icon1.jpg",
            "Spectre":                                     "https://static.wikia.nocookie.net/starcraft/images/0/0d/Spectre_WoL.jpg",
            "Thor":                                        "https://static.wikia.nocookie.net/starcraft/images/e/ef/Thor_SC2_Icon1.jpg",

            "Widow Mine":                                  "/static/static/icons/sc2/widowmine.png",
            "Cyclone":                                     "/static/static/icons/sc2/cyclone.png",
            "Liberator":                                   "/static/static/icons/sc2/liberator.png",
            "Valkyrie":                                    "/static/static/icons/sc2/valkyrie.png",

            "Ocular Implants (Ghost)":                     "https://0rganics.org/archipelago/sc2wol/OcularImplants.png",
            "Crius Suit (Ghost)":                          "https://0rganics.org/archipelago/sc2wol/CriusSuit.png",
            "EMP Rounds (Ghost)":                          "/static/static/icons/sc2/terran-emp-color.png",
            "Lockdown (Ghost)":                            "/static/static/icons/sc2/lockdown.png",
            "Psionic Lash (Spectre)":                      "https://0rganics.org/archipelago/sc2wol/PsionicLash.png",
            "Nyx-Class Cloaking Module (Spectre)":         "https://0rganics.org/archipelago/sc2wol/Nyx-ClassCloakingModule.png",
            "Impaler Rounds (Spectre)":                    "/static/static/icons/sc2/impalerrounds.png",
            "330mm Barrage Cannon (Thor)":                 "https://0rganics.org/archipelago/sc2wol/330mmBarrageCannon.png",
            "Immortality Protocol (Thor)":                 "https://0rganics.org/archipelago/sc2wol/ImmortalityProtocol.png",
            "High Impact Payload (Thor)":                  "/static/static/icons/sc2/thorsiegemode.png",
            "Smart Servos (Thor)":                         "/static/static/icons/sc2/transformationservos.png",

            "Optimized Logistics (Predator)":              "/static/static/icons/sc2/optimizedlogistics.png",
            "Drilling Claws (Widow Mine)":                 "/static/static/icons/sc2/drillingclaws.png",
            "Concealment (Widow Mine)":                    "/static/static/icons/sc2/widowminehidden.png",
            "Black Market Launchers (Widow Mine)":         "/static/static/icons/sc2/widowmine-attackrange.png",
            "Executioner Missiles (Widow Mine)":           "/static/static/icons/sc2/widowmine-deathblossom.png",
            "Mag-Field Accelerators (Cyclone)":            "/static/static/icons/sc2/magfieldaccelerator.png",
            "Mag-Field Launchers (Cyclone)":               "/static/static/icons/sc2/cyclonerangeupgrade.png",
            "Targeting Optics (Cyclone)":                  "/static/static/icons/sc2/targetingoptics.png",
            "Rapid Fire Launchers (Cyclone)":              "/static/static/icons/sc2/ripwavemissiles.png",
            "Bio Mechanical Repair Drone (Raven)":         "/static/static/icons/sc2/biomechanicaldrone.png",
            "Spider Mines (Raven)":                        "/static/static/icons/sc2/siegetank-spidermines.png",
            "Railgun Turret (Raven)":                      "/static/static/icons/sc2/autoturretblackops.png",
            "Hunter-Seeker Weapon (Raven)":                "/static/static/icons/sc2/specialordance.png",
            "Interference Matrix (Raven)":                 "/static/static/icons/sc2/interferencematrix.png",
            "Anti-Armor Missile (Raven)":                  "/static/static/icons/sc2/shreddermissile.png",
            "Internal Tech Module (Raven)":                "/static/static/icons/sc2/internalizedtechmodule.png",
            "EMP Shockwave (Science Vessel)":              "/static/static/icons/sc2/staticempblast.png",
            "Defensive Matrix (Science Vessel)":           "https://0rganics.org/archipelago/sc2wol/DefensiveMatrix.png",
            "Advanced Ballistics (Liberator)":             "/static/static/icons/sc2/advanceballistics.png",
            "Raid Artillery (Liberator)":                  "/static/static/icons/sc2/terrandefendermodestructureattack.png",
            "Cloak (Liberator)":                           "/static/static/icons/sc2/terran-cloak-color.png",
            "Laser Targeting System (Liberator)":          "/static/static/icons/sc2/lasertargetingsystem.png",
            "Optimized Logistics (Liberator)":             "/static/static/icons/sc2/optimizedlogistics.png",
            "Enhanced Cluster Launchers (Valkyrie)":       "https://0rganics.org/archipelago/sc2wol/HellstormBatteries.png",
            "Shaped Hull (Valkyrie)":                      "https://0rganics.org/archipelago/sc2wol/ShapedHull.png",
            "Burst Lasers (Valkyrie)":                     "/static/static/icons/sc2/improvedburstlaser.png",
            "Afterburners (Valkyrie)":                     "/static/static/icons/sc2/medivacemergencythrusters.png",

            "War Pigs":                                    "https://static.wikia.nocookie.net/starcraft/images/e/ed/WarPigs_SC2_Icon1.jpg",
            "Devil Dogs":                                  "https://static.wikia.nocookie.net/starcraft/images/3/33/DevilDogs_SC2_Icon1.jpg",
            "Hammer Securities":                           "https://static.wikia.nocookie.net/starcraft/images/3/3b/HammerSecurity_SC2_Icon1.jpg",
            "Spartan Company":                             "https://static.wikia.nocookie.net/starcraft/images/b/be/SpartanCompany_SC2_Icon1.jpg",
            "Siege Breakers":                              "https://static.wikia.nocookie.net/starcraft/images/3/31/SiegeBreakers_SC2_Icon1.jpg",
            "Hel's Angel":                                 "https://static.wikia.nocookie.net/starcraft/images/6/63/HelsAngels_SC2_Icon1.jpg",
            "Dusk Wings":                                  "https://static.wikia.nocookie.net/starcraft/images/5/52/DuskWings_SC2_Icon1.jpg",
            "Jackson's Revenge":                           "https://static.wikia.nocookie.net/starcraft/images/9/95/JacksonsRevenge_SC2_Icon1.jpg",

            "Ultra-Capacitors":                            "https://static.wikia.nocookie.net/starcraft/images/2/23/SC2_Lab_Ultra_Capacitors_Icon.png",
            "Vanadium Plating":                            "https://static.wikia.nocookie.net/starcraft/images/6/67/SC2_Lab_VanPlating_Icon.png",
            "Orbital Depots":                              "https://static.wikia.nocookie.net/starcraft/images/0/01/SC2_Lab_Orbital_Depot_Icon.png",
            "Micro-Filtering":                             "https://static.wikia.nocookie.net/starcraft/images/2/20/SC2_Lab_MicroFilter_Icon.png",
            "Automated Refinery":                          "https://static.wikia.nocookie.net/starcraft/images/7/71/SC2_Lab_Auto_Refinery_Icon.png",
            "Command Center Reactor":                      "https://static.wikia.nocookie.net/starcraft/images/e/ef/SC2_Lab_CC_Reactor_Icon.png",
            "Raven":                                       "https://static.wikia.nocookie.net/starcraft/images/1/19/SC2_Lab_Raven_Icon.png",
            "Science Vessel":                              "https://static.wikia.nocookie.net/starcraft/images/c/c3/SC2_Lab_SciVes_Icon.png",
            "Tech Reactor":                                "https://static.wikia.nocookie.net/starcraft/images/c/c5/SC2_Lab_Tech_Reactor_Icon.png",
            "Orbital Strike":                              "https://static.wikia.nocookie.net/starcraft/images/d/df/SC2_Lab_Orb_Strike_Icon.png",

            "Shrike Turret (Bunker)":                      "https://static.wikia.nocookie.net/starcraft/images/4/44/SC2_Lab_Shrike_Turret_Icon.png",
            "Fortified Bunker (Bunker)":                   "https://static.wikia.nocookie.net/starcraft/images/4/4f/SC2_Lab_FortBunker_Icon.png",
            "Planetary Fortress":                          "https://static.wikia.nocookie.net/starcraft/images/0/0b/SC2_Lab_PlanetFortress_Icon.png",
            "Perdition Turret":                            "https://static.wikia.nocookie.net/starcraft/images/a/af/SC2_Lab_PerdTurret_Icon.png",
            "Predator":                                    "https://static.wikia.nocookie.net/starcraft/images/8/83/SC2_Lab_Predator_Icon.png",
            "Hercules":                                    "https://static.wikia.nocookie.net/starcraft/images/4/40/SC2_Lab_Hercules_Icon.png",
            "Cellular Reactor":                            "https://static.wikia.nocookie.net/starcraft/images/d/d8/SC2_Lab_CellReactor_Icon.png",
            "Regenerative Bio-Steel Level 1":              "/static/static/icons/sc2/SC2_Lab_BioSteel_L1.png",
            "Regenerative Bio-Steel Level 2":              "/static/static/icons/sc2/SC2_Lab_BioSteel_L2.png",
            "Hive Mind Emulator":                          "https://static.wikia.nocookie.net/starcraft/images/b/bc/SC2_Lab_Hive_Emulator_Icon.png",
            "Psi Disrupter":                               "https://static.wikia.nocookie.net/starcraft/images/c/cf/SC2_Lab_Psi_Disruptor_Icon.png",

            "Zealot":                                      "https://static.wikia.nocookie.net/starcraft/images/6/6e/Icon_Protoss_Zealot.jpg",
            "Stalker":                                     "https://static.wikia.nocookie.net/starcraft/images/0/0d/Icon_Protoss_Stalker.jpg",
            "High Templar":                                "https://static.wikia.nocookie.net/starcraft/images/a/a0/Icon_Protoss_High_Templar.jpg",
            "Dark Templar":                                "https://static.wikia.nocookie.net/starcraft/images/9/90/Icon_Protoss_Dark_Templar.jpg",
            "Immortal":                                    "https://static.wikia.nocookie.net/starcraft/images/c/c1/Icon_Protoss_Immortal.jpg",
            "Colossus":                                    "https://static.wikia.nocookie.net/starcraft/images/4/40/Icon_Protoss_Colossus.jpg",
            "Phoenix":                                     "https://static.wikia.nocookie.net/starcraft/images/b/b1/Icon_Protoss_Phoenix.jpg",
            "Void Ray":                                    "https://static.wikia.nocookie.net/starcraft/images/1/1d/VoidRay_SC2_Rend1.jpg",
            "Carrier":                                     "https://static.wikia.nocookie.net/starcraft/images/2/2c/Icon_Protoss_Carrier.jpg",

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
        }

        display_data = {}

        # Grouped Items
        grouped_item_ids = {
            "Progressive Weapon Upgrade":       107 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Armor Upgrade":        108 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Infantry Upgrade":     109 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Vehicle Upgrade":      110 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Ship Upgrade":         111 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Weapon/Armor Upgrade": 112 + SC2WOL_ITEM_ID_OFFSET
        }
        grouped_item_replacements = {
            "Progressive Weapon Upgrade":   ["Progressive Infantry Weapon", "Progressive Vehicle Weapon",
                                             "Progressive Ship Weapon"],
            "Progressive Armor Upgrade":    ["Progressive Infantry Armor", "Progressive Vehicle Armor",
                                             "Progressive Ship Armor"],
            "Progressive Infantry Upgrade": ["Progressive Infantry Weapon", "Progressive Infantry Armor"],
            "Progressive Vehicle Upgrade":  ["Progressive Vehicle Weapon", "Progressive Vehicle Armor"],
            "Progressive Ship Upgrade":     ["Progressive Ship Weapon", "Progressive Ship Armor"]
        }
        grouped_item_replacements["Progressive Weapon/Armor Upgrade"] = grouped_item_replacements[
                                                                            "Progressive Weapon Upgrade"] + \
                                                                        grouped_item_replacements[
                                                                            "Progressive Armor Upgrade"]
        replacement_item_ids = {
            "Progressive Infantry Weapon": 100 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Infantry Armor":  102 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Vehicle Weapon":  103 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Vehicle Armor":   104 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Ship Weapon":     105 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Ship Armor":      106 + SC2WOL_ITEM_ID_OFFSET,
        }

        inventory = tracker_data.get_player_inventory_counts(team, player)
        for grouped_item_name, grouped_item_id in grouped_item_ids.items():
            count: int = inventory[grouped_item_id]
            if count > 0:
                for replacement_item in grouped_item_replacements[grouped_item_name]:
                    replacement_id: int = replacement_item_ids[replacement_item]
                    inventory[replacement_id] = count

        # Determine display for progressive items
        progressive_items = {
            "Progressive Infantry Weapon":                    100 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Infantry Armor":                     102 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Vehicle Weapon":                     103 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Vehicle Armor":                      104 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Ship Weapon":                        105 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Ship Armor":                         106 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Marine)":                  208 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Firebat)":                 226 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Marauder)":                228 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Reaper)":                  250 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Stimpack (Hellion)":                 259 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive High Impact Payload (Thor)":         361 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Cross-Spectrum Dampeners (Banshee)": 316 + SC2WOL_ITEM_ID_OFFSET,
            "Progressive Regenerative Bio-Steel":             617 + SC2WOL_ITEM_ID_OFFSET
        }
        progressive_names = {
            "Progressive Infantry Weapon":                    ["Infantry Weapons Level 1", "Infantry Weapons Level 1",
                                                               "Infantry Weapons Level 2", "Infantry Weapons Level 3"],
            "Progressive Infantry Armor":                     ["Infantry Armor Level 1", "Infantry Armor Level 1",
                                                               "Infantry Armor Level 2", "Infantry Armor Level 3"],
            "Progressive Vehicle Weapon":                     ["Vehicle Weapons Level 1", "Vehicle Weapons Level 1",
                                                               "Vehicle Weapons Level 2", "Vehicle Weapons Level 3"],
            "Progressive Vehicle Armor":                      ["Vehicle Armor Level 1", "Vehicle Armor Level 1",
                                                               "Vehicle Armor Level 2", "Vehicle Armor Level 3"],
            "Progressive Ship Weapon":                        ["Ship Weapons Level 1", "Ship Weapons Level 1",
                                                               "Ship Weapons Level 2", "Ship Weapons Level 3"],
            "Progressive Ship Armor":                         ["Ship Armor Level 1", "Ship Armor Level 1",
                                                               "Ship Armor Level 2", "Ship Armor Level 3"],
            "Progressive Stimpack (Marine)":                  ["Stimpack (Marine)", "Stimpack (Marine)",
                                                               "Super Stimpack (Marine)"],
            "Progressive Stimpack (Firebat)":                 ["Stimpack (Firebat)", "Stimpack (Firebat)",
                                                               "Super Stimpack (Firebat)"],
            "Progressive Stimpack (Marauder)":                ["Stimpack (Marauder)", "Stimpack (Marauder)",
                                                               "Super Stimpack (Marauder)"],
            "Progressive Stimpack (Reaper)":                  ["Stimpack (Reaper)", "Stimpack (Reaper)",
                                                               "Super Stimpack (Reaper)"],
            "Progressive Stimpack (Hellion)":                 ["Stimpack (Hellion)", "Stimpack (Hellion)",
                                                               "Super Stimpack (Hellion)"],
            "Progressive High Impact Payload (Thor)":         ["High Impact Payload (Thor)",
                                                               "High Impact Payload (Thor)", "Smart Servos (Thor)"],
            "Progressive Cross-Spectrum Dampeners (Banshee)": ["Cross-Spectrum Dampeners (Banshee)",
                                                               "Cross-Spectrum Dampeners (Banshee)",
                                                               "Advanced Cross-Spectrum Dampeners (Banshee)"],
            "Progressive Regenerative Bio-Steel":             ["Regenerative Bio-Steel Level 1",
                                                               "Regenerative Bio-Steel Level 1",
                                                               "Regenerative Bio-Steel Level 2"]
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
            display_data[base_name + "_url"] = icons[display_name]
            display_data[base_name + "_name"] = display_name

        # Multi-items
        multi_items = {
            "+15 Starting Minerals": 800 + SC2WOL_ITEM_ID_OFFSET,
            "+15 Starting Vespene":  801 + SC2WOL_ITEM_ID_OFFSET,
            "+2 Starting Supply":    802 + SC2WOL_ITEM_ID_OFFSET
        }
        for item_name, item_id in multi_items.items():
            base_name = item_name.split()[-1].lower()
            count = inventory[item_id]
            if base_name == "supply":
                count = count * 2
                display_data[base_name + "_count"] = count
            else:
                count = count * 15
                display_data[base_name + "_count"] = count

        # Victory condition
        game_state = tracker_data.get_player_client_status(team, player)
        display_data["game_finished"] = game_state == 30

        # Turn location IDs into mission objective counts
        locations = tracker_data.get_player_locations(team, player)
        checked_locations = tracker_data.get_player_checked_locations(team, player)
        lookup_name = lambda id: tracker_data.location_id_to_name["Starcraft 2 Wings of Liberty"][id]
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

        lookup_any_item_id_to_name = tracker_data.item_id_to_name["Starcraft 2 Wings of Liberty"]
        return render_template(
            "tracker__Starcraft2WingsOfLiberty.html",
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

    _player_trackers["Starcraft 2 Wings of Liberty"] = render_Starcraft2WingsOfLiberty_tracker
