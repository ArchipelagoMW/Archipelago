from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import UUID

from flask import abort

from MultiServer import Context
from NetUtils import NetworkItem, SlotType, encode
from Utils import restricted_loads
from WebHostLib import cache
from WebHostLib.api import api_endpoints
from WebHostLib.models import GameDataPackage, Room
from WebHostLib.tracker import TrackerData


@api_endpoints.route("/tracker/<suuid:tracker>")
@cache.memoize(timeout=60)
def tracker_data(tracker: UUID):
    """outputs json data to <root_path>/api/tracker/<id of current session tracker>"""
    room: Optional[Room] = Room.get(tracker=tracker)
    if not room:
        abort(404)

    tracker_data = TrackerData(room)

    all_players: Dict[int, List[int]] = tracker_data.get_all_players()

    groups: Dict[int, Dict[int, Dict[str, Union[str, List[int]]]]] = {}
    """The Slot ID of groups and the IDs of the group's members."""
    for team, players in tracker_data.get_all_slots().items():
        for player in players:
            slot_info = tracker_data.get_slot_info(team, player)
            if slot_info.type != SlotType.group or not slot_info.group_members:
                continue
            groups.setdefault(team, {})[player] = {
                "name": slot_info.name,
                "members": list(slot_info.group_members),
            }

    player_names: Dict[int, Dict[int, str]] = {
        team: {
            player: tracker_data.get_player_name(team, player)
            for player in players
        }
        for team, players in all_players.items()
    }
    """Slot names of all players."""

    player_aliases: Dict[int, Dict[int, str]] = {
        team: {
            player: tracker_data.get_player_alias(team, player)
            for player in players
        }
        for team, players in all_players.items()
    }
    """Slot aliases of all players."""

    games: Dict[int, Dict[int, str]] ={
        team: {
            player: tracker_data.get_player_game(team, player)
            for player in players
        }
        for team, players in all_players.items()
    }
    """The game each player is playing."""

    player_items_received: Dict[int, Dict[int, List[NetworkItem]]] = {
        team: {
            player: tracker_data.get_player_received_items(team, player)
            for player in players
        }
        for team, players in all_players.items()
    }
    """Items received by each player."""

    player_checks_done: Dict[int, Dict[int, List[int]]] = {
        team: {
            player: list(tracker_data.get_player_checked_locations(team, player))
            for player in players
        }
        for team, players in all_players.items()
    }
    """ID of all locations checked by each player."""

    total_checks_done: Dict[int, int] = tracker_data.get_team_locations_checked_count()
    """Total number of locations checked for the entire multiworld per team."""

    hints: Dict[int, Dict[int, List[str]]] = {}
    """Hints that all players have used or received."""
    for team, players in tracker_data.get_all_slots().items():
        for player in players:
            player_hints = list(tracker_data.get_player_hints(team, player))
            hints.setdefault(team, {})[player] = player_hints
            slot_info = tracker_data.get_slot_info(team, player)
            # this currently assumes groups are always after players
            if slot_info.type != SlotType.group:
                continue
            for member in slot_info.group_members:
                hints[team][member] += player_hints

    activity_timers: Dict[int, Dict[int, Optional[datetime]]] = {
        team: {
            player: None
            for player in players
        }
        for team, players in all_players.items()
    }
    """Time of last activity per player. Returned as RFC 1123 format and null if no connection has been made."""
    client_activity_timers: Tuple[Tuple[int, int], float] = tracker_data._multisave.get("client_activity_timers", ())
    for (team, player), timestamp in client_activity_timers:
        activity_timers[team][player] = datetime.utcfromtimestamp(timestamp)

    connection_timers: Dict[int, Dict[int, Optional[datetime]]] = {
        team: {
            player: None
            for player in players
        }
        for team, players in all_players.items()
    }
    """Time of last connection per player. Returned as RFC 1123 format and null if no connection has been made."""

    client_connection_timers: Tuple[Tuple[int, int], float] = tracker_data._multisave.get("client_connection_timers", ())
    for (team, player), timestamp in client_connection_timers:
        connection_timers[team][player] = datetime.utcfromtimestamp(timestamp)

    player_status = {
        team: {
            player: tracker_data.get_player_client_status(team, player)
            for player in players
        }
        for team, players in all_players.items()
    }
    """The current client status for each player."""

    slot_data: Dict[int, Dict[int, Dict[str, Any]]] = {
        team: {
            player: tracker_data.get_slot_data(team, player)
            for player in players
        }
        for team, players in all_players.items()
    }
    """Slot data for each player."""

    return {
            "groups": groups,
            "player_names": player_names,
            "player_aliases": player_aliases,
            "games": games,
            "player_items_received": player_items_received,
            "player_checks_done": player_checks_done,
            "total_checks_done": total_checks_done,
            "hints": hints,
            "activity_timers": activity_timers,
            "connection_timers": connection_timers,
            "player_status": player_status,
            "slot_data": encode(slot_data),
            "datapackage": tracker_data._multidata["datapackage"],
        }
