import datetime

from typing import Optional
from flask import abort, jsonify

from Utils import restricted_loads
from uuid import UUID

from WebHostLib.models import Room
from WebHostLib.api import api_endpoints
from WebHostLib.tracker import get_static_room_data
from WebHostLib import cache


# outputs json data to <root_path>/api/tracker/<id of current session tracker>
@api_endpoints.route('/tracker/<suuid:tracker>')
@cache.memoize(timeout=60)
def tracker_data(tracker: UUID):
    room: Optional[Room] = Room.get(tracker=tracker)
    if not room:
        abort(404)

    locations, names, use_door_tracker, player_checks_in_area, \
        player_location_to_area, precollected_items, games, slot_data, groups = get_static_room_data(room)

    checks_done = {team_number: {player_number: 0
                                 for player_number in range(1, len(team) + 1) if player_number not in groups}
                   for team_number, team in enumerate(names)}

    hints = {team: [] for team in range(len(names))}

    player_status = checks_done
    if room.multisave:
        multisave = restricted_loads(room.multisave)
    else:
        multisave = {}

    if "hints" in multisave:
        for (team, slot), slot_hints in multisave["hints"].items():
            hints[team] = [hint for hint in slot_hints]

    for player in locations:
        locations[player] = [loc for loc in locations[player]]

    for (team, player), locations_checked in multisave.get("location_checks", {}).items():
        if player in groups:
            continue
        player_locations = locations[player]
        for location in locations_checked:
            if location not in player_locations or location not in player_location_to_area[player]:
                continue
            checks_done[team][player] += 1

    for (team, player), game_state in multisave.get("client_game_state", {}).items():
        if player in groups:
            continue
        player_status[team][player] = game_state

    activity_timers = {}
    now = datetime.datetime.utcnow()
    for (team, player), timestamp in multisave.get("client_activity_timers", []):
        inactive_time = now - datetime.datetime.utcfromtimestamp(timestamp)
        activity_timers[team] = {player: str(inactive_time)}

    player_names = {}
    for team, names in enumerate(names):
        for player, name in enumerate(names, 1):
            player_names[team] = {player: name}

    aliases = {}
    for (team, player), alias in multisave.get("name_aliases", {}).items():
        aliases[team][player] = alias

    return jsonify({
        "groups": groups,
        "player_names": player_names,
        "aliases": aliases,
        "checks_done": checks_done,
        "total_checks": locations,
        "hints": hints,
        "recent_activity": activity_timers,
        "game_states": player_status,
    })
