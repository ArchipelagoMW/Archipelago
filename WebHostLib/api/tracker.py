import collections

from flask import session, jsonify
from typing import Optional, Dict, Any, Tuple, List
from Utils import restricted_loads
from uuid import UUID

from ..models import Room
from . import api_endpoints
from ..tracker import get_static_room_data, attribute_item_solo
from worlds import lookup_any_item_id_to_name, lookup_any_location_id_to_name


@api_endpoints.route('/tracker/<suuid:tracker>/<int:tracked_team>/<int:tracked_player>')
def update_tracker(tracker: UUID, tracked_team: int, tracked_player: int):

    room: Optional[Room] = Room.get(tracker=tracker)
    locations, names, use_door_tracker, seed_checks_in_area, player_location_to_area, \
    precollected_items, games, slot_data, groups = get_static_room_data(room)

    if room.multisave:
        multisave: Dict[str, Any] = restricted_loads(room.multisave)
    else:
        multisave: Dict[str, Any] = {}

    # create and fill dictionary of all progression items for players
    prog_items = collections.Counter()
    for player in locations:
        for location in locations[player]:
            item, recipient, flags = locations[player][location]
            if recipient == tracked_player and flags & 1:
                item_name = lookup_any_item_id_to_name[item]
                prog_items[item_name] += 1


    # find out which locations have been checked so far
    checked_locations: List[str] = []
    items_received: Dict[str, Any] = dict(dict())
    for (team, player), locations_checked in multisave.get("location_checks", {}).items():
        player_locations: Dict[int, Tuple[int, int, int]] = locations[player]
        if team == tracked_team:
            for location in locations_checked:
                item = player_locations[location][0]
                checked_locations.append(lookup_any_location_id_to_name[location])
                if prog_items[lookup_any_item_id_to_name[item]] == 1:
                    items_received[lookup_any_item_id_to_name[item]] = '✔'
                else:
                    if lookup_any_item_id_to_name[item] in items_received:
                        items_received[lookup_any_item_id_to_name[item]] += 1
                    else:
                        items_received[lookup_any_item_id_to_name[item]] = 1

    # convert numbers to string
    for item in items_received:
        items_received[item] = str(items_received[item])

    return jsonify({
        "items_received": items_received,
        "checked_locations": checked_locations
    })
