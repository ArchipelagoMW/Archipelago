import collections

from flask import jsonify
from typing import Optional, Dict, Any, Tuple, List
from Utils import restricted_loads
from uuid import UUID

from ..models import Room
from . import api_endpoints
from ..tracker import fill_tracker_data, get_static_room_data
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name
from WebHostLib import cache


@api_endpoints.route('/tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
@cache.memoize(timeout=60)
def update_player_tracker(tracker: UUID, tracked_team: int, tracked_player: int):

    room: Optional[Room] = Room.get(tracker=tracker)
    locations = get_static_room_data(room)[0]
    items_counter: Dict[int, collections.Counter] = get_item_names_counter(locations)
    player_tracker, multisave, inventory, seed_checks_in_area, lttp_checks_done, \
    slot_data, games, player_name, display_icons = fill_tracker_data(room, tracked_team, tracked_player)

    # convert numbers to string
    for item in player_tracker.items_received:
        if items_counter[tracked_player][item] == 1:
            player_tracker.items_received[item] = '✔'
        else:
            player_tracker.items_received[item] = str(player_tracker.items_received[item])

    return jsonify({
        "items_received": player_tracker.items_received,
        "checked_locations": list(sorted(player_tracker.checked_locations)),
        "icons": display_icons,
        "progressive_names": player_tracker.progressive_names
    })


@cache.cached()
def get_item_names_counter(locations: Dict[int, Dict[int, Tuple[int, int, int]]]):
    # create and fill dictionary of all progression items for players
    items_counters: Dict[int, collections.Counter] = {}
    for player in locations:
        for location in locations[player]:
            item, recipient, flags = locations[player][location]
            item_name = lookup_any_item_id_to_name[item]
            items_counters.setdefault(recipient, collections.Counter())[item_name] += 1

    return items_counters
