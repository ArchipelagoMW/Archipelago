import collections
import datetime
from typing import Any, Callable, Counter, Dict, List, NamedTuple, Optional, Set, Tuple, Union
from uuid import UUID

from flask import render_template
from werkzeug.exceptions import abort

from MultiServer import Context, get_saving_second
from NetUtils import ClientStatus, Hint, SlotType
from Utils import restricted_loads
from worlds import network_data_package
from . import app, cache
from .models import GameDataPackage, Room

# Multisave is currently updated, at most, every minute.
TRACKER_CACHE_TIMEOUT_IN_SECONDS = 60

multidata_cache = {}
multiworld_trackers: Dict[str, Callable] = {}
game_specific_trackers: Dict[str, Callable] = {
    # "Minecraft": __renderMinecraftTracker,
    # "Ocarina of Time": __renderOoTTracker,
    # "Timespinner": __renderTimespinnerTracker,
    # "A Link to the Past": __renderAlttpTracker,
    # "ChecksFinder": __renderChecksfinder,
    # "Super Metroid": __renderSuperMetroidTracker,
    # "Starcraft 2 Wings of Liberty": __renderSC2WoLTracker
}


class RoomData(NamedTuple):
    """Curated metadata from multidata for tracker purposes."""

    # This is a dictionary of player ids to a dictionary of location ids to NetworkItem data (sans location).
    #     The Tuple is (item_code, item_player_id, item_flags)
    multidata: Dict[str, Any]
    locations: Dict[int, Dict[int, Tuple[int, int, int]]]
    room: Room
    names: List[List[str]]
    starting_items: Dict[int, List[int]]
    games: Dict[int, str]
    slot_data: Dict[int, Dict[str, Any]]
    groups: Dict[int, Union[List[int], Tuple[int, ...]]]
    saving_second: int
    location_id_to_name: Dict[str, Dict[int, str]]
    item_id_to_name: Dict[str, Dict[int, str]]


class RoomState(NamedTuple):
    """Curated metadata from RoomData and multisave for multi-tracker purposes."""

    multisave: Dict[str, Any]
    room_data: RoomData
    hints: Dict[int, Set[Hint]]
    player_names: Dict[Tuple[int, int], str]
    player_names_with_alias: Dict[Tuple[int, int], str]
    locations_complete: Dict[int, Dict[int, int]]
    percentage_of_locations_complete: Dict[int, Dict[int, int]]
    total_team_locations: Dict[int, int]
    completed_worlds: int
    activity_timers: Dict[Tuple[int, int], datetime.timedelta]
    states: Dict[Tuple[int, int], ClientStatus]
    videos: Dict[Tuple[int, int], List[str]]


@app.template_filter()
def render_timedelta(delta: datetime.timedelta) -> str:
    hours, minutes = divmod(delta.total_seconds() / 60, 60)
    hours = str(int(hours))
    minutes = str(int(minutes)).zfill(2)
    return f"{hours}:{minutes}"


def get_static_room_data(room: Room) -> RoomData:
    """Fetches the static RoomData for a given room."""

    # If cached, return the cached room data.
    room_data = multidata_cache.get(room.seed.id, None)
    if room_data:
        return room_data

    # In rooms with a lot of players this can take a bit of time, so this is the main reason for caching.
    multidata = Context.decompress(room.seed.multidata)
    games = {slot: slot_info.game for slot, slot_info in multidata["slot_info"].items()}
    location_id_to_name = {}
    item_id_to_name = {}
    for game in games.values():
        if game not in multidata["datapackage"]:
            continue

        checksum = multidata["datapackage"][game]["checksum"]
        game_package = restricted_loads(GameDataPackage.get(checksum=checksum).data)
        location_id_to_name.update({game: {id: name for name, id in game_package["location_name_to_id"].items()}})
        item_id_to_name.update({game: {id: name for name, id in game_package["item_name_to_id"].items()}})

    room_data = RoomData(
        multidata=multidata,
        room=room,
        locations=multidata["locations"],
        names=[[slot_info.name for _, slot_info in sorted(multidata["slot_info"].items())]],
        starting_items=multidata["precollected_items"],
        games=games,
        slot_data=multidata["slot_data"],
        groups={
            slot: slot_info.group_members
            for slot, slot_info in multidata["slot_info"].items()
            if slot_info.type == SlotType.group
        },
        saving_second=get_saving_second(multidata["seed_name"]),
        location_id_to_name=location_id_to_name,
        item_id_to_name=item_id_to_name,
    )

    multidata_cache[room.seed.id] = room_data
    return room_data


@app.route('/tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
def get_player_tracker(tracker: UUID, tracked_team: int, tracked_player: int, want_generic: bool = False) -> str:
    key = f"{tracker}_{tracked_team}_{tracked_player}_{want_generic}"
    tracker_page = cache.get(key)
    if tracker_page:
        return tracker_page
    timeout, tracker_page = _get_player_tracker(tracker, tracked_team, tracked_player, want_generic)
    cache.set(key, tracker_page, timeout)
    return tracker_page


def _get_player_tracker(tracker: UUID, tracked_team: int, tracked_player: int, want_generic: bool) -> Tuple[int, str]:
    """
    :return: Returns a tuple with the timeout value and jinja template
    """

    # Team and player must be positive and greater than zero.
    if tracked_team < 0 or tracked_player < 1:
        abort(404)

    room: Optional[Room] = Room.get(tracker=tracker)
    if not room:
        abort(404)

    # Collect seed information and pare it down to a single player.
    room_data = get_static_room_data(room)
    inventory = collections.Counter()

    # Add starting items to inventory.
    for item_id in room_data.starting_items[tracked_player]:
        inventory[item_id] += 1

    # Load save data.
    if room.multisave:
        multisave: Dict[str, Any] = restricted_loads(room.multisave)
    else:
        multisave: Dict[str, Any] = {}

    slots_player_is_member_of = {tracked_player}
    for group_id, group_members in room_data.groups.items():
        if tracked_player in group_members:
            slots_player_is_member_of.add(group_id)

    # Add items to player inventory.
    for (team, player), locations_checked in multisave.get("location_checks", {}).items():
        # Skip teams and players not matching the request.
        player_locations = room_data.locations[player]

        if team != tracked_team:
            continue

        for location in locations_checked:
            if location in player_locations:
                # Keep track of items received by the player, excluding cheated items.
                (item_code, recipient, _) = player_locations[location]
                if recipient in slots_player_is_member_of:
                    inventory[item_code] += 1

    # Load and render the game-specific player tracker, or fallback to generic tracker if none exists.
    specific_tracker = game_specific_trackers.get(room_data.games[tracked_player], None)
    if specific_tracker and not want_generic:
        tracker = specific_tracker(multisave, room_data, tracked_team, tracked_player, inventory)
    else:
        tracker = __render_generic_tracker(multisave, room_data, tracked_team, tracked_player, inventory)

    return (room_data.saving_second - datetime.datetime.now().second) % 60 or 60, tracker


@app.route('/generic_tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
def get_generic_tracker(tracker: UUID, tracked_team: int, tracked_player: int):
    return get_player_tracker(tracker, tracked_team, tracked_player, True)


def __render_generic_tracker(multisave: dict, room_data: RoomData, team: int, player: int, inventory: Counter) -> str:
    checked_locations = multisave.get("location_checks", {}).get((team, player), set())
    received_items = multisave.get('received_items', {}).get((team, player, True), [])
    received_items_in_order = {}

    # Add received index to all received items, excluding starting inventory.
    for received_index, network_item in enumerate(received_items, start=1):
        received_items_in_order[network_item.item] = received_index

    return render_template(
        template_name_or_list="generic-tracker.html",
        room=room_data.room,
        team=team,
        player=player,
        player_name=room_data.names[team][player],
        inventory=inventory,
        checked_locations=checked_locations,
        not_checked_locations=set(room_data.locations[player]) - checked_locations,
        received_items=received_items_in_order,
        saving_second=room_data.saving_second,
        location_name=room_data.location_id_to_name[room_data.games[player]],
        item_name=room_data.item_id_to_name[room_data.games[player]],
    )


def get_enabled_multiworld_trackers(room: Room, current: str) -> List[Dict[str, Any]]:
    enabled = [{
        "name": "Generic",
        "endpoint": "render_generic_multiworld_tracker",
        "current": current == "Generic"
    }]

    # Render the multitracker for any games that exist in the current room if they are defined.
    for game_name, endpoint in multiworld_trackers.items():
        if any(slot.game == game_name for slot in room.seed.slots) or current == game_name:
            enabled.append({
                "name": game_name,
                "endpoint": endpoint.__name__,
                "current": current == game_name
            })

    return enabled


def get_room_state(tracker: UUID) -> Optional[RoomState]:
    room: Room = Room.get(tracker=tracker)
    if not room:
        return None

    room_data = get_static_room_data(room)

    # Prepare location counters and hints.
    locations_complete = {}
    total_team_locations = {}
    percentage_of_locations_complete = {}
    for team, team_members in enumerate(room_data.names):
        locations_complete.setdefault(team, {})
        total_team_locations.setdefault(team, 0)
        percentage_of_locations_complete.setdefault(team, {})
        for player in range(1, len(team_members) + 1):
            if player in room_data.groups:
                continue

            locations_complete[team][player] = 0
            total_team_locations[team] += len(room_data.locations[player])
            percentage_of_locations_complete[team][player] = 0

    # Load save data.
    if room.multisave:
        multisave = restricted_loads(room.multisave)
    else:
        multisave = {}

    # Load known hints.
    hints = {}
    if "hints" in multisave:
        for (team, slot), slot_hints in multisave["hints"].items():
            hints.setdefault(team, set())
            hints[team] |= set(slot_hints)

    # Iterate over all checked locations and calculate overall state.
    for (team, player), locations_checked in multisave.get("location_checks", {}).items():
        if player in room_data.groups:
            continue

        player_locations = room_data.locations[player]
        locations_complete[team][player] = len(locations_checked)
        percentage_of_locations_complete[team][player] = (
            # If no locations exist, let's report 100%, so we don't divide by 0.
            locations_complete[team][player] / len(player_locations) * 100 if player_locations else 100
        )

    # Calculate activity.
    activity_timers = {}
    now = datetime.datetime.utcnow()
    for (team, player), timestamp in multisave.get("client_activity_timers", []):
        activity_timers[team, player] = now - datetime.datetime.utcfromtimestamp(timestamp)

    # Build an easily accessible player names lookup.
    player_names = {}
    completed_worlds = 0
    states: Dict[Tuple[int, int], ClientStatus] = {}
    for team, team_members in enumerate(room_data.names):
        for player, player_name in enumerate(team_members, 1):
            player_names[team, player] = player_name
            states[team, player] = multisave.get("client_game_state", {}).get((team, player), 0)
            if states[team, player] == ClientStatus.CLIENT_GOAL and player not in room_data.groups:
                completed_worlds += 1

    player_names_with_alias = player_names.copy()
    for (team, player), alias in multisave.get("name_aliases", {}).items():
        player_names[team, player] = alias
        player_names_with_alias[(team, player)] = f"{alias} ({player_names_with_alias[team, player]})"

    # Video / Streaming links.
    videos = {}
    for (team, player), data in multisave.get("video", []):
        videos[team, player] = data

    return RoomState(
        multisave=multisave,
        room_data=room_data,
        hints=hints,
        player_names=player_names,
        player_names_with_alias=player_names_with_alias,
        locations_complete=locations_complete,
        percentage_of_locations_complete=percentage_of_locations_complete,
        total_team_locations=total_team_locations,
        completed_worlds=completed_worlds,
        activity_timers=activity_timers,
        states=states,
        videos=videos,
    )


@app.route('/tracker/<suuid:tracker>')
@cache.memoize(timeout=TRACKER_CACHE_TIMEOUT_IN_SECONDS)
def render_generic_multiworld_tracker(tracker: UUID):
    room_state = get_room_state(tracker)
    if not room_state:
        abort(404)

    return render_template(
        template_name_or_list="multitracker.html",
        enabled_multiworld_trackers=get_enabled_multiworld_trackers(room_state.room_data.room, "Generic"),
        current_tracker="Generic",
        **room_state._asdict(),
    )


if "Factorio" in network_data_package["games"].keys():
    @app.route('/tracker/<suuid:tracker>/Factorio')
    @cache.memoize(timeout=TRACKER_CACHE_TIMEOUT_IN_SECONDS)
    def render_Factorio_multiworld_tracker(tracker: UUID):
        room_state = get_room_state(tracker)
        if not room_state:
            abort(404)

        def _get_inventory_data(room_state: RoomState) -> Dict[int, Dict[int, Dict[int, int]]]:
            inventory: Dict[int, Dict[int, Dict[int, int]]] = {
                team: {player: collections.Counter() for player in team_data}
                for team, team_data in room_state.locations_complete.items()
            }

            groups = room_state.room_data.groups
            for (team, player), locations_checked in room_state.multisave.get("location_checks", {}).items():
                if player in groups:
                    continue

                player_locations = room_state.room_data.locations[player]
                starting_items = room_state.room_data.starting_items[player]
                for item_id in starting_items:
                    inventory[team][player][item_id] += 1
                for location in locations_checked:
                    item_id, recipient, flags = player_locations[location]
                    recipients = groups.get(recipient, [recipient])
                    for recipient in recipients:
                        inventory[team][recipient][item_id] += 1
            return inventory

        def _get_named_inventory(inventory: Dict[int, int]) -> Dict[str, int]:
            """slow"""
            mapping = room_state.room_data.item_id_to_name["Factorio"]
            return collections.Counter({mapping.get(item_id, None): count for item_id, count in inventory.items()})

        inventory = _get_inventory_data(room_state)
        return render_template(
            template_name_or_list="multitracker__Factorio.html",
            enabled_multiworld_trackers=get_enabled_multiworld_trackers(room_state.room_data.room, "Factorio"),
            current_tracker="Factorio",
            inventory=inventory,
            named_inventory={
                team_id: {
                    player_id: _get_named_inventory(inventory)
                    for player_id, inventory in team_inventory.items()
                } for team_id, team_inventory in inventory.items()
            },
            **room_state._asdict(),
        )

    multiworld_trackers["Factorio"] = render_Factorio_multiworld_tracker

if "A Link to the Past" in network_data_package["games"].keys():
    @app.route('/tracker/<suuid:tracker>/A Link to the Past')
    @cache.memoize(timeout=TRACKER_CACHE_TIMEOUT_IN_SECONDS)
    def render_ALinkToThePast_multiworld_tracker(tracker: UUID):
        room_state = get_room_state(tracker)
        if not room_state:
            abort(404)

        # Helper objects.
        alttp_id_lookup = {name: id for id, name in room_state.room_data.item_id_to_name["A Link to the Past"].items()}

        groups = room_state.room_data.groups
        inventory: Dict[int, Dict[int, Dict[int, int]]] = {
            team: {player: collections.Counter() for player in team_data}
            for team, team_data in room_state.locations_complete.items()
        }
        multi_items = {alttp_id_lookup[name] for name in ("Progressive Sword", "Progressive Bow", "Bottle", "Progressive Glove")}
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
            "Fighter Sword":  1,
            "Master Sword":   2,
            "Tempered Sword": 3,
            "Golden Sword":   4,
            "Power Glove":    1,
            "Titans Mitts":   2,
            "Bow":            1,
            "Silver Bow":     2,
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
            player_id: {
                area_name: len(room_state.room_data.multidata["checks_in_area"][player_id][area_name]) if area_name != "Total" else
                           room_state.room_data.multidata["checks_in_area"][player_id]["Total"]
                for area_name in ordered_areas
            }
            for player_id in room_state.room_data.multidata["checks_in_area"]
        }

        tracking_ids = []
        for item in tracking_names:
            tracking_ids.append(alttp_id_lookup[item])

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

        def _attribute_item(team: int, recipient: int, item: int):
            target_item = links.get(item, item)
            if item in levels:  # non-progressive
                inventory[team][recipient][target_item] = max(inventory[team][recipient][target_item], levels[item])
            else:
                inventory[team][recipient][target_item] += 1

        player_location_to_area = {
            player_id: _get_location_table(room_state.room_data.multidata["checks_in_area"][player_id])
            for player_id in room_state.room_data.multidata["checks_in_area"]
        }

        checks_done = {
            team_id: {
                player_id: {
                    loc_name: 0 for loc_name in default_locations
                }
                for player_id in range(1, len(team_members) + 1) if player_id not in groups
            }
            for team_id, team_members in enumerate(room_state.room_data.names)
        }

        # Sum items received and calculate checked locations.
        for (team, player), locations_checked in room_state.multisave.get("location_checks", {}).items():
            if player in groups:
                continue

            player_locations = room_state.room_data.locations[player]
            if room_state.room_data.starting_items:
                starting_items = room_state.room_data.starting_items[player]
                for item_id in starting_items:
                    _attribute_item(team, player, item_id)

            for location in locations_checked:
                item, recipient, flags = player_locations[location]
                recipients = groups.get(recipient, [recipient])
                for recipient in recipients:
                    _attribute_item(team, recipient, item)
                    if room_state.room_data.games[player] == "A Link to the Past":
                        checks_done[team][player][player_location_to_area[player][location]] += 1

            checks_done[team][player]["Total"] = len(locations_checked)

        # Check if game complete.
        for (team, player), game_state in room_state.states.items():
            if player in groups:
                continue

            if game_state == ClientStatus.CLIENT_GOAL:
                inventory[team][player][106] = 1  # Triforce

        # Track key locations.
        player_big_key_locations = {player_id: set() for player_id in range(1, len(room_state.room_data.names[0]) + 1)}
        player_small_key_locations = {player_id: set() for player_id in range(1, len(room_state.room_data.names[0]) + 1)}
        for location_data in room_state.room_data.locations.values():
            for item in location_data.values():
                item_id, receiving_player, flags = item

                if item_id in ids_big_key:
                    player_big_key_locations[receiving_player].add(ids_big_key[item_id])
                elif item_id in ids_small_key:
                    player_small_key_locations[receiving_player].add(ids_small_key[item_id])

        group_big_key_locations = set()
        group_key_locations = set()
        for player in [player for player in range(1, len(room_state.room_data.names[0]) + 1) if player not in groups]:
            group_key_locations |= player_small_key_locations[player]
            group_big_key_locations |= player_big_key_locations[player]

        return render_template(
            template_name_or_list="multitracker__ALinkToThePast.html",
            enabled_multiworld_trackers=get_enabled_multiworld_trackers(room_state.room_data.room, "A Link to the Past"),
            current_tracker="A Link to the Past",
            inventory=inventory,
            get_item_name_from_id=room_state.room_data.item_id_to_name["A Link to the Past"],
            lookup_id_to_name=Items.lookup_id_to_name,
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
            **room_state._asdict(),
        )

    multiworld_trackers["A Link to the Past"] = render_ALinkToThePast_multiworld_tracker
