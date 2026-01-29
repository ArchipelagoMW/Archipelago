from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, TypedDict
from uuid import UUID

from flask import abort

from NetUtils import ClientStatus, Hint, NetworkItem, SlotType
from WebHostLib import cache
from WebHostLib.api import api_endpoints
from WebHostLib.models import Room
from WebHostLib.tracker import TrackerData


class PlayerAlias(TypedDict):
    team: int
    player: int
    alias: str | None


class PlayerItemsReceived(TypedDict):
    team: int
    player: int
    items: list[NetworkItem]


class PlayerChecksDone(TypedDict):
    team: int
    player: int
    locations: list[int]


class TeamTotalChecks(TypedDict):
    team: int
    checks_done: int


class PlayerHints(TypedDict):
    team: int
    player: int
    hints: list[Hint]


class PlayerTimer(TypedDict):
    team: int
    player: int
    time: datetime | None


class PlayerStatus(TypedDict):
    team: int
    player: int
    status: ClientStatus


class TrackerPlayerData(TypedDict):
    team: int
    player: int
    alias: str | None
    items: list[NetworkItem]
    checked_locations: list[int]
    hints: list[Hint]
    time: datetime | None
    status: ClientStatus


@api_endpoints.route("/tracker/<suuid:tracker>")
@cache.memoize(timeout=60)
def tracker_data(tracker: UUID) -> dict[str, Any]:
    """
    Outputs json data to <root_path>/api/tracker/<id of current session tracker>.

    :param tracker: UUID of current session tracker.

    :return: Tracking data for all players in the room. Typing and docstrings describe the format of each value.
    """
    room: Room | None = Room.get(tracker=tracker)
    if not room:
        abort(404)

    tracker_data = TrackerData(room)

    all_players: dict[int, list[int]] = tracker_data.get_all_players()

    total_checks_done: list[TeamTotalChecks] = [
        {"team": team, "checks_done": checks_done}
        for team, checks_done in tracker_data.get_team_locations_checked_count().items()
    ]
    """Total number of locations checked for the entire multiworld per team."""

    hints: list[PlayerHints] = []
    hints: dict[tuple[int, int], list[PlayerHints]] = defaultdict(list)
    """Hints that all players have used or received."""
    for team, players in tracker_data.get_all_slots().items():
        for player in players:
            player_hints = sorted(tracker_data.get_player_hints(team, player))
            hints[team, player] += player_hints
            slot_info = tracker_data.get_slot_info(player)
            # this assumes groups are always after players
            if slot_info.type != SlotType.group:
                continue
            for member in slot_info.group_members:
                hints[team, member] += player_hints

    activity_timers = dict(tracker_data._multisave.get("client_activity_timers", []))
    connection_timers = dict(tracker_data._multisave.get("client_connection_timers", []))

    def get_time(lookup, key) -> datetime | None:
        ret = lookup.get(key)
        if ret is not None:
            return datetime.fromtimestamp(ret, timezone.utc)
        return ret

    player_data: list[TrackerPlayerData] = []
    for team, player in all_players.items():
        for player in players:
            player_data.append({
                "team": team,
                "player": player,
                "alias": tracker_data.get_player_alias(team, player),
                "items": tracker_data.get_player_received_items(team, player),
                "checked_locations": sorted(tracker_data.get_player_checked_locations(team, player)),
                "hints": hints[team, player],
                "activity_time": get_time(activity_timers, (team, player)),
                "connection_time": get_time(activity_timers, (team, player)),
                "status": tracker_data.get_player_client_status(team, player),
                })

    return {
        "total_checks_done": total_checks_done,
        "player_data": player_data,
    }


class PlayerGroups(TypedDict):
    slot: int
    name: str
    members: list[int]


class StaticPlayerData(TypedDict):
    team: int
    player: int
    name: str
    location_count: int
    locations: list[int]
    game: str


@api_endpoints.route("/static_tracker/<suuid:tracker>")
@cache.memoize(timeout=300)
def static_tracker_data(tracker: UUID) -> dict[str, Any]:
    """
    Outputs json data to <root_path>/api/static_tracker/<id of current session tracker>.

    :param tracker: UUID of current session tracker.

    :return: Static tracking data for all players in the room. Typing and docstrings describe the format of each value.
    """
    room: Room | None = Room.get(tracker=tracker)
    if not room:
        abort(404)
    tracker_data = TrackerData(room)

    all_players: dict[int, list[int]] = tracker_data.get_all_players()

    groups: list[PlayerGroups] = []
    """The Slot ID of groups and the IDs of the group's members."""
    for team, players in tracker_data.get_all_slots().items():
        for player in players:
            slot_info = tracker_data.get_slot_info(player)
            if slot_info.type != SlotType.group or not slot_info.group_members:
                continue
            groups.append(
                {
                    "slot": player,
                    "name": slot_info.name,
                    "members": list(slot_info.group_members),
                })
        break

    player_data: list[StaticPlayerData] = []
    for team, players in all_players.items():
        for player in players:
            locations = tracker_data.get_player_locations(player).keys()
            player_data.append({
                "team": team,
                "player": player,
                "name": tracker_data.get_player_name(player),
                "location_count": len(locations),
                "locations": sorted(locations),
                "game": tracker_data.get_player_game(player),
                })

    return {
        "groups": groups,
        "datapackage": tracker_data._multidata["datapackage"],
        "player_data": player_data,
    }


class PlayerSlotData(TypedDict):
    player: int
    slot_data: dict[str, Any]


# It should be exceedingly rare that slot data is needed, so it's separated out.
@api_endpoints.route("/slot_data_tracker/<suuid:tracker>")
@cache.memoize(timeout=300)
def tracker_slot_data(tracker: UUID) -> list[PlayerSlotData]:
    """
    Outputs json data to <root_path>/api/slot_data_tracker/<id of current session tracker>.

    :param tracker: UUID of current session tracker.

    :return: Slot data for all players in the room. Typing completely arbitrary per game.
    """
    room: Room | None = Room.get(tracker=tracker)
    if not room:
        abort(404)
    tracker_data = TrackerData(room)

    all_players: dict[int, list[int]] = tracker_data.get_all_players()

    slot_data: list[PlayerSlotData] = []
    """Slot data for each player."""
    for team, players in all_players.items():
        for player in players:
            slot_data.append({"player": player, "slot_data": tracker_data.get_slot_data(player)})
        break

    return slot_data
