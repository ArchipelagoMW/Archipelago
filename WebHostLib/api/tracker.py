from datetime import datetime, timezone
from typing import Any, TypedDict
from uuid import UUID

from flask import abort

from NetUtils import ClientStatus, Hint, NetworkItem, SlotType
from WebHostLib import cache
from WebHostLib.api import api_endpoints
from WebHostLib.models import Room
from WebHostLib.tracker import TrackerData


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

    class PlayerAlias(TypedDict):
        player: int
        name: str | None

    player_aliases: list[dict[str, int | list[PlayerAlias]]] = []
    """Slot aliases of all players."""
    for team, players in all_players.items():
        team_player_aliases: list[PlayerAlias] = []
        team_aliases = {"team": team, "players": team_player_aliases}
        player_aliases.append(team_aliases)
        for player in players:
            team_player_aliases.append({"player": player, "alias": tracker_data.get_player_alias(team, player)})

    class PlayerItemsReceived(TypedDict):
        player: int
        items: list[NetworkItem]

    player_items_received: list[dict[str, int | list[PlayerItemsReceived]]] = []
    """Items received by each player."""
    for team, players in all_players.items():
        player_received_items: list[PlayerItemsReceived] = []
        team_items_received = {"team": team, "players": player_received_items}
        player_items_received.append(team_items_received)
        for player in players:
            player_received_items.append(
                {"player": player, "items": tracker_data.get_player_received_items(team, player)})

    class PlayerChecksDone(TypedDict):
        player: int
        locations: list[int]

    player_checks_done: list[dict[str, int | list[PlayerChecksDone]]] = []
    """ID of all locations checked by each player."""
    for team, players in all_players.items():
        per_player_checks: list[PlayerChecksDone] = []
        team_checks_done = {"team": team, "players": per_player_checks}
        player_checks_done.append(team_checks_done)
        for player in players:
            per_player_checks.append(
                {"player": player, "locations": sorted(tracker_data.get_player_checked_locations(team, player))})

    total_checks_done: list[dict[str, int]] = [
        {"team": team, "checks_done": checks_done}
        for team, checks_done in tracker_data.get_team_locations_checked_count().items()
    ]
    """Total number of locations checked for the entire multiworld per team."""

    class PlayerHints(TypedDict):
        player: int
        hints: list[Hint]

    hints: list[dict[str, int | list[PlayerHints]]] = []
    """Hints that all players have used or received."""
    for team, players in tracker_data.get_all_slots().items():
        per_player_hints: list[PlayerHints] = []
        team_hints = {"team": team, "players": per_player_hints}
        hints.append(team_hints)
        for player in players:
            player_hints = sorted(tracker_data.get_player_hints(team, player))
            per_player_hints.append({"player": player, "hints": player_hints})
            slot_info = tracker_data.get_slot_info(team, player)
            # this assumes groups are always after players
            if slot_info.type != SlotType.group:
                continue
            for member in slot_info.group_members:
                team_hints[member]["hints"] += player_hints

    class PlayerTimer(TypedDict):
        player: int
        time: datetime | None

    activity_timers: list[dict[str, int | list[PlayerTimer]]] = []
    """Time of last activity per player. Returned as RFC 1123 format and null if no connection has been made."""
    for team, players in all_players.items():
        player_timers: list[PlayerTimer] = []
        team_timers = {"team": team, "players": player_timers}
        activity_timers.append(team_timers)
        for player in players:
            player_timers.append({"player": player, "time": None})

    client_activity_timers: tuple[tuple[int, int], float] = tracker_data._multisave.get("client_activity_timers", ())
    for (team, player), timestamp in client_activity_timers:
        # use index since we can rely on order
        # FIX: key is "players" (not "player_timers")
        activity_timers[team]["players"][player - 1]["time"] = datetime.fromtimestamp(timestamp, timezone.utc)


    connection_timers: list[dict[str, int | list[PlayerTimer]]] = []
    """Time of last connection per player. Returned as RFC 1123 format and null if no connection has been made."""
    for team, players in all_players.items():
        player_timers: list[PlayerTimer] = []
        team_connection_timers = {"team": team, "players": player_timers}
        connection_timers.append(team_connection_timers)
        for player in players:
            player_timers.append({"player": player, "time": None})

    client_connection_timers: tuple[tuple[int, int], float] = tracker_data._multisave.get(
        "client_connection_timers", ())
    for (team, player), timestamp in client_connection_timers:
        connection_timers[team]["players"][player - 1]["time"] = datetime.fromtimestamp(timestamp, timezone.utc)

    class PlayerStatus(TypedDict):
        player: int
        status: ClientStatus

    player_status: list[dict[str, int | list[PlayerStatus]]] = []
    """The current client status for each player."""
    for team, players in all_players.items():
        player_statuses: list[PlayerStatus] = []
        team_status = {"team": team, "players": player_statuses}
        player_status.append(team_status)
        for player in players:
            player_statuses.append({"player": player, "status": tracker_data.get_player_client_status(team, player)})

    return {
        **get_static_tracker_data(room),
        "aliases": player_aliases,
        "player_items_received": player_items_received,
        "player_checks_done": player_checks_done,
        "total_checks_done": total_checks_done,
        "hints": hints,
        "activity_timers": activity_timers,
        "connection_timers": connection_timers,
        "player_status": player_status,
        "datapackage": tracker_data._multidata["datapackage"],
    }

@cache.memoize()
def get_static_tracker_data(room: Room) -> dict[str, Any]:
    """
    Builds and caches the static data for this active session tracker, so that it doesn't need to be recalculated.
    """

    tracker_data = TrackerData(room)

    all_players: dict[int, list[int]] = tracker_data.get_all_players()

    class PlayerGroups(TypedDict):
        slot: int
        name: str
        members: list[int]

    groups: list[dict[str, int | list[PlayerGroups]]] = []
    """The Slot ID of groups and the IDs of the group's members."""
    for team, players in tracker_data.get_all_slots().items():
        groups_in_team: list[PlayerGroups] = []
        team_groups = {"team": team, "groups": groups_in_team}
        groups.append(team_groups)
        for player in players:
            slot_info = tracker_data.get_slot_info(team, player)
            if slot_info.type != SlotType.group or not slot_info.group_members:
                continue
            groups_in_team.append(
                {
                    "slot": player,
                    "name": slot_info.name,
                    "members": list(slot_info.group_members),
                })
    class PlayerName(TypedDict):
        player: int
        name: str

    player_names: list[dict[str, str | list[PlayerName]]] = []
    """Slot names of all players."""
    for team, players in all_players.items():
        per_team_player_names: list[PlayerName] = []
        team_names = {"team": team, "players": per_team_player_names}
        player_names.append(team_names)
        for player in players:
            per_team_player_names.append({"player": player, "name": tracker_data.get_player_name(team, player)})

    class PlayerGame(TypedDict):
        player: int
        game: str

    games: list[dict[str, int | list[PlayerGame]]] = []
    """The game each player is playing."""
    for team, players in all_players.items():
        player_games: list[PlayerGame] = []
        team_games = {"team": team, "players": player_games}
        games.append(team_games)
        for player in players:
            player_games.append({"player": player, "game": tracker_data.get_player_game(team, player)})

    class PlayerSlotData(TypedDict):
        player: int
        slot_data: dict[str, Any]

    slot_data: list[dict[str, int | list[PlayerSlotData]]] = []
    """Slot data for each player."""
    for team, players in all_players.items():
        player_slot_data: list[PlayerSlotData] = []
        team_slot_data = {"team": team, "players": player_slot_data}
        slot_data.append(team_slot_data)
        for player in players:
            player_slot_data.append({"player": player, "slot_data": tracker_data.get_slot_data(team, player)})

    return {
        "groups": groups,
        "slot_data": slot_data,
    }
