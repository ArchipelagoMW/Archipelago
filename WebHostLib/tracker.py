import collections
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

__tracker_cache: Dict[str, Any] = {}
__multidata_cache = {}
__multiworld_trackers: Dict[str, Callable] = {}
__player_trackers: Dict[str, Callable] = {
    # "Minecraft": __renderMinecraftTracker,
    # "Ocarina of Time": __renderOoTTracker,
    # "Timespinner": __renderTimespinnerTracker,
    # "ChecksFinder": __renderChecksfinder,
    # "Super Metroid": __renderSuperMetroidTracker,
    # "Starcraft 2 Wings of Liberty": __renderSC2WoLTracker
}

TeamPlayer = Tuple[int, int]
ItemMetadata = Tuple[int, int, int]


def _cache_results(func: Callable) -> Callable:
    """Stores the results of any computationally expensive methods after the initial call in TrackerData.
    If called again, returns the cached result instead, as results will not change for the lifetime of TrackerData.
    """
    def method_wrapper(self: "TrackerData", *args):
        cache_key = f"{func.__name__}{''.join(f'_[{arg.__repr__()}]' for arg in args)}"
        if cache_key in __tracker_cache:
            return __tracker_cache[cache_key]

        result = func(self, *args)
        __tracker_cache[cache_key] = result
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

    def __init__(self, room: Room):
        """Initialize a new RoomMultidata object for the current room."""
        self.room = room
        self._multidata = Context.decompress(room.seed.multidata)
        self._multisave = restricted_loads(room.multisave) if room.multisave else {}
        self._cache = {}

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
    if game not in __multiworld_trackers:
        return render_generic_multiworld_tracker(tracker_data, enabled_trackers)

    return __multiworld_trackers[game](tracker_data, enabled_trackers)


def get_timeout_and_tracker(tracker: UUID, tracked_team: int, tracked_player: int, generic: bool) -> Tuple[int, str]:
    # Room must exist.
    room = Room.get(tracker=tracker)
    if not room:
        abort(404)

    tracker_data = TrackerData(room)

    # Load and render the game-specific player tracker, or fallback to generic tracker if none exists.
    game_specific_tracker = __player_trackers.get(tracker_data.get_player_game(tracked_team, tracked_player), None)
    if game_specific_tracker and not generic:
        tracker = game_specific_tracker(tracker_data, tracked_team, tracked_player)
    else:
        tracker = render_generic_tracker(tracker_data, tracked_team, tracked_player)

    return (tracker_data.get_room_saving_second() - datetime.datetime.now().second) % 60 or 60, tracker


def get_enabled_multiworld_trackers(room: Room) -> Dict[str, Callable]:
    # Render the multitracker for any games that exist in the current room if they are defined.
    enabled_trackers = {}
    for game_name, endpoint in __multiworld_trackers.items():
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


# TODO: Implement a proper TrackerAPI and move specific trackers to worlds.
from worlds import network_data_package


if "Factorio" in network_data_package["games"].keys():
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

    __multiworld_trackers["Factorio"] = render_Factorio_multiworld_tracker

if "A Link to the Past" in network_data_package["games"].keys():
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

    def render_ALinkToThePast_tracker(tracker_data: TrackerData, tracked_team: int, tracked_player: int) -> str:
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

        player_locations = tracker_data.get_player_locations(tracked_team, tracked_player)
        for checked_location in tracker_data.get_player_checked_locations(tracked_team, tracked_player):
            if checked_location in player_locations:
                area_name = location_to_area.get(checked_location, None)
                if area_name:
                    checks_done[area_name] += 1

                checks_done["Total"] += 1

        for received_item in tracker_data.get_player_received_items(tracked_team, tracked_player):
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
        if tracker_data.get_player_client_status(tracked_team, tracked_player) == ClientStatus.CLIENT_GOAL:
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
            inventory=inventory,
            player_name=tracker_data.get_player_name(tracked_team, tracked_player),
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

    __multiworld_trackers["A Link to the Past"] = render_ALinkToThePast_multiworld_tracker
    __player_trackers["A Link to the Past"] = render_ALinkToThePast_tracker
