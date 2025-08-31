# WebHostLib/api/sphere_tracker.py
from __future__ import annotations

from typing import Dict, List, Tuple

from flask import jsonify, request

from .. import cache
from ..models import Room
from ..tracker import TrackerData, TRACKER_CACHE_TIMEOUT_IN_SECONDS
from . import api_endpoints


# Helpers
def _collect_players(td: TrackerData) -> tuple[dict[int, dict[int, dict[str, str]]], set[str]]:
    """
    Returns:
      - players_by_team: { team: { slot: {"name": str, "game": str} } }
      - games_in_room: {game, ...}
    """
    all_players = td.get_all_players() or {}
    players_by_team: dict[int, dict[int, dict[str, str]]] = {}
    games_in_room: set[str] = set()

    for team, slots in (all_players or {}).items():
        team_map: dict[int, dict[str, str]] = players_by_team.setdefault(team, {})
        for slot in (slots or {}):
            name = td.get_player_name(team, slot)
            game = td.get_player_game(team, slot)
            games_in_room.add(game)
            team_map[slot] = {"name": name, "game": game}

    return players_by_team, games_in_room


def _collect_used_data(td: TrackerData) -> tuple[
    dict[int, dict[int, dict[int, dict[int, list[tuple[int, int]]]]]],
    dict[str, set[int]],
    dict[str, dict[int, int]],
]:
    """
    Walks through the spheres and computes:
      - used_pairs_by_team:
          {team: {sphere_idx: {finder_slot: {receiver_slot: [(item_id, loc_id), ...]}}}}
      - used_loc_ids_by_game: {game: {loc_id, ...}}
      - used_item_flags_by_game: {game: {item_id: flags_or}}
    """
    used_pairs_by_team: dict[int, dict[int, dict[int, dict[int, list[tuple[int, int]]]]]] = {}
    used_loc_ids_by_game: dict[str, set[int]] = {}
    used_item_flags_by_game: dict[str, dict[int, int]] = {}

    spheres = td.get_spheres() or []  # list[dict[finder_slot -> set(loc_ids)]]
    all_players = td.get_all_players() or {}

    for team, _players in (all_players or {}).items():
        team_map = used_pairs_by_team.setdefault(team, {})
        for sphere_idx, sphere in enumerate(spheres, start=1):
            sphere_map = team_map.setdefault(sphere_idx, {})
            for finder_slot, sphere_loc_ids in (sphere or {}).items():
                checked = td.get_player_checked_locations(team, finder_slot) or set()
                if not checked:
                    continue

                loc_map = td.get_player_locations(team, finder_slot) or {}
                if not loc_map:
                    continue

                finder_game = td.get_player_game(team, finder_slot)

                for loc_id in set(sphere_loc_ids).intersection(checked):
                    if loc_id not in loc_map:
                        continue
                    item_id, receiver_slot, item_flags = loc_map[loc_id]
                    receiver_game = td.get_player_game(team, receiver_slot)

                    # pairs sorted later
                    finder_map = sphere_map.setdefault(finder_slot, {})
                    rec_list = finder_map.setdefault(receiver_slot, [])
                    rec_list.append((item_id, loc_id))

                    # locations used per finder's game
                    used_loc_ids_by_game.setdefault(finder_game, set()).add(loc_id)

                    # flags accumulated per (receiver's game, item_id)
                    game_flags = used_item_flags_by_game.setdefault(receiver_game, {})
                    game_flags[item_id] = game_flags.get(item_id, 0) | int(item_flags or 0)

    # stable sort for deterministic JSON: by (loc_id, item_id)
    for team_map in used_pairs_by_team.values():
        for sphere_map in team_map.values():
            for finder_map in sphere_map.values():
                for receiver_slot, pairs in finder_map.items():
                    pairs.sort(key=lambda t: (t[1], t[0]))  # (item_id, loc_id) sorted by location then item

    return used_pairs_by_team, used_loc_ids_by_game, used_item_flags_by_game


# Main endpoint
# IMPORTANT: the cache also varies on `expand`

@api_endpoints.route("/sphere_tracker/<suuid:tracker>")
def api_sphere_tracker(tracker):
    """
    IDs-only by default.
    Query:
      - expand=1 : returns names/games/flags.
    """
    expand = 1 if request.args.get("expand", default=0, type=int) == 1 else 0
    return _api_sphere_tracker_cached(tracker, expand)


@cache.memoize(timeout=TRACKER_CACHE_TIMEOUT_IN_SECONDS)
def _api_sphere_tracker_cached(tracker, expand: int):
    """
    Memoized version whose key includes `expand`.
    """
    room = Room.get(tracker=tracker)
    td = TrackerData(room)
    used_pairs_by_team, used_loc_ids_by_game, used_item_flags_by_game = _collect_used_data(td)

    # Compact view: IDs only
    if not expand:
        out: list[dict] = []
        for team_id in sorted(used_pairs_by_team.keys()):
            spheres_out: list[dict] = []
            for sphere_idx in sorted(used_pairs_by_team[team_id].keys()):
                finders_out: list[dict] = []
                for finder_slot in sorted(used_pairs_by_team[team_id][sphere_idx].keys()):
                    receivers_out: list[dict] = []
                    for receiver_slot in sorted(used_pairs_by_team[team_id][sphere_idx][finder_slot].keys()):
                        pairs = [
                            [item_id, loc_id]
                            for (item_id, loc_id) in used_pairs_by_team[team_id][sphere_idx][finder_slot][receiver_slot]
                        ]
                        receivers_out.append({"receiver_slot": receiver_slot, "pairs": pairs})
                    if receivers_out:
                        finders_out.append({"finder_slot": finder_slot, "receivers": receivers_out})
                if finders_out:
                    spheres_out.append({"sphere": sphere_idx, "finders": finders_out})
            if spheres_out:
                out.append({"team": team_id, "spheres": spheres_out})
        return jsonify(out)

    # Expanded view: names / games / flags
    # NOTE: 'game' is tied to the finder (your invariant).
    # Item names usually depend on the receiver's game,
    # and location names on the finder's game.
    item_name = td.item_id_to_name or {}      # {game: {item_id: str}}
    loc_name  = td.location_id_to_name or {}  # {game: {loc_id: str}}
    players_by_team, _ = _collect_players(td)

    def slot_meta(team: int, slot: int) -> tuple[str, str]:
        s = (players_by_team.get(team) or {}).get(slot) or {}
        return s.get("name", str(slot)), s.get("game", "")

    out: list[dict] = []
    for team_id in sorted(used_pairs_by_team.keys()):
        spheres_out: list[dict] = []
        for sphere_idx in sorted(used_pairs_by_team[team_id].keys()):
            finders_out: list[dict] = []
            for finder_slot, rec_map in sorted(used_pairs_by_team[team_id][sphere_idx].items()):
                finder_name, finder_game = slot_meta(team_id, finder_slot)
                receivers_out: list[dict] = []
                for receiver_slot, pairs in sorted(rec_map.items()):
                    receiver_name, receiver_game = slot_meta(team_id, receiver_slot)
                    items_out: list[dict] = []
                    for (item_id, loc_id) in pairs:
                        items_out.append(
                            {
                                "item_id": item_id,
                                "item_name": (item_name.get(receiver_game, {}) or {}).get(item_id, str(item_id)),
                                "item_flag": int((used_item_flags_by_game.get(receiver_game, {}) or {}).get(item_id, 0)),
                                "location_id": loc_id,
                                "location_name": (loc_name.get(finder_game, {}) or {}).get(loc_id, str(loc_id)),
                            }
                        )
                    if items_out:
                        receivers_out.append(
                            {
                                "receiver_slot": receiver_slot,
                                "receiver_name": receiver_name,
                                "items": items_out,
                            }
                        )
                if receivers_out:
                    finders_out.append(
                        {
                            "finder_slot": finder_slot,
                            "finder_name": finder_name,
                            "finder_game": finder_game,  # game is carried by the finder
                            "receivers": receivers_out,
                        }
                    )
            if finders_out:
                spheres_out.append({"sphere": sphere_idx, "finders": finders_out})
        if spheres_out:
            out.append({"team": team_id, "spheres": spheres_out})

    return jsonify(out)
