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


class PlayerLocationsTotal(TypedDict):
    team: int
    player: int
    total_locations: int


@api_endpoints.route("/tracker/<suuid:tracker>")
@cache.memoize(timeout=60)
def tracker_data(tracker: UUID) -> dict[str, Any]:
    room: Room | None = Room.get(tracker=tracker)
    if not room:
        abort(404)

    tracker_data = TrackerData(room)

    all_players: dict[int, list[int]] = tracker_data.get_all_players()

    player_aliases: list[PlayerAlias] = []
    for team, players in all_players.items():
        for player in players:
            player_aliases.append(
                {"team": team, "player": player, "alias": tracker_data.get_player_alias(team, player)}
            )

    player_items_received: list[PlayerItemsReceived] = []
    for team, players in all_players.items():
        for player in players:
            player_items_received.append(
                {"team": team, "player": player, "items": tracker_data.get_player_received_items(team, player)}
            )

    player_checks_done: list[PlayerChecksDone] = []
    for team, players in all_players.items():
        for player in players:
            player_checks_done.append(
                {
                    "team": team,
                    "player": player,
                    "locations": sorted(tracker_data.get_player_checked_locations(team, player)),
                }
            )

    player_locations_total: list[PlayerLocationsTotal] = []
    for team, players in all_players.items():
        for player in players:
            player_locations_total.append(
                {
                    "team": team,
                    "player": player,
                    "total_locations": len(tracker_data.get_player_locations(team, player)),
                }
            )

    total_checks_done: list[TeamTotalChecks] = [
        {"team": team, "checks_done": checks_done}
        for team, checks_done in tracker_data.get_team_locations_checked_count().items()
    ]

    hints_map: dict[tuple[int, int], list[Hint]] = {}
    for team, players in tracker_data.get_all_slots().items():
        for player in players:
            hints_map[(team, player)] = list(sorted(tracker_data.get_player_hints(team, player)))

    for team, players in tracker_data.get_all_slots().items():
        for player in players:
            slot_info = tracker_data.get_slot_info(team, player)
            if slot_info.type == SlotType.group and slot_info.group_members:
                group_hints = hints_map[(team, player)]
                for member in slot_info.group_members:
                    hints_map[(team, member)] = hints_map.get((team, member), [])
                    hints_map[(team, member)].extend(group_hints)

    hints: list[PlayerHints] = [
        {"team": team, "player": player, "hints": hints_map[(team, player)]}
        for (team, player) in hints_map.keys()
    ]

    activity_timers: list[PlayerTimer] = []
    for team, players in all_players.items():
        for player in players:
            activity_timers.append({"team": team, "player": player, "time": None})

    for (team, player), timestamp in tracker_data._multisave.get("client_activity_timers", []):
        for entry in activity_timers:
            if entry["team"] == team and entry["player"] == player:
                entry["time"] = datetime.fromtimestamp(timestamp, timezone.utc)
                break

    connection_timers: list[PlayerTimer] = []
    for team, players in all_players.items():
        for player in players:
            connection_timers.append({"team": team, "player": player, "time": None})

    for (team, player), timestamp in tracker_data._multisave.get("client_connection_timers", []):
        for entry in connection_timers:
            if entry["team"] == team and entry["player"] == player:
                entry["time"] = datetime.fromtimestamp(timestamp, timezone.utc)
                break

    player_status: list[PlayerStatus] = []
    for team, players in all_players.items():
        for player in players:
            player_status.append(
                {"team": team, "player": player, "status": tracker_data.get_player_client_status(team, player)}
            )

    return {
        "aliases": player_aliases,
        "player_items_received": player_items_received,
        "player_checks_done": player_checks_done,
        "player_locations_total": player_locations_total,
        "total_checks_done": total_checks_done,
        "hints": hints,
        "activity_timers": activity_timers,
        "connection_timers": connection_timers,
        "player_status": player_status,
    }


class PlayerGroups(TypedDict):
    slot: int
    name: str
    members: list[int]


class PlayerSlotData(TypedDict):
    team: int
    player: int
    slot_data: dict[str, Any]


@api_endpoints.route("/static_tracker/<suuid:tracker>")
@cache.memoize(timeout=300)
def static_tracker_data(tracker: UUID) -> dict[str, Any]:
    room: Room | None = Room.get(tracker=tracker)
    if not room:
        abort(404)
    tracker_data = TrackerData(room)

    groups: list[PlayerGroups] = []
    for team, players in tracker_data.get_all_slots().items():
        for player in players:
            slot_info = tracker_data.get_slot_info(team, player)
            if slot_info.type != SlotType.group or not slot_info.group_members:
                continue
            groups.append(
                {
                    "slot": player,
                    "name": slot_info.name,
                    "members": list(slot_info.group_members),
                }
            )

    return {
        "groups": groups,
        "datapackage": tracker_data._multidata["datapackage"],
    }


@api_endpoints.route("/slot_data_tracker/<suuid:tracker>")
@cache.memoize(timeout=300)
def tracker_slot_data(tracker: UUID) -> list[PlayerSlotData]:
    room: Room | None = Room.get(tracker=tracker)
    if not room:
        abort(404)
    tracker_data = TrackerData(room)

    all_players: dict[int, list[int]] = tracker_data.get_all_players()

    slot_data: list[PlayerSlotData] = []
    for team, players in all_players.items():
        for player in players:
            slot_data.append(
                {"team": team, "player": player, "slot_data": tracker_data.get_slot_data(team, player)}
            )

    return slot_data
