# WebHostLib/api/sphere_tracker.py
from __future__ import annotations

from typing import Dict, List, Tuple, Any

from flask import jsonify, abort

from .. import cache
from ..models import Room
from ..tracker import TrackerData, TRACKER_CACHE_TIMEOUT_IN_SECONDS
from . import api_endpoints


# Helpers

def _collect_used_data(td: TrackerData) -> tuple[
    dict[int, dict[int, dict[int, dict[int, list[tuple[int, int]]]]]],
    dict[str, set[int]],
    dict[str, dict[int, int]],
]:
    """
    Walk through spheres and compute:
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

    # stable sort for a deterministic JSON: by (loc_id, item_id)
    for team_map in used_pairs_by_team.values():
        for sphere_map in team_map.values():
            for finder_map in sphere_map.values():
                for receiver_slot, pairs in finder_map.items():
                    pairs.sort(key=lambda t: (t[1], t[0]))  # sort by location then item

    return used_pairs_by_team, used_loc_ids_by_game, used_item_flags_by_game


def _collect_player_games(td: TrackerData) -> dict[int, dict[int, str]]:
    """
    Build a map {team: {slot: game_name}} using TrackerData.get_player_game.
    """
    all_players = td.get_all_players() or {}
    out: dict[int, dict[int, str]] = {}
    for team, slots in (all_players or {}).items():
        team_map = out.setdefault(team, {})
        for slot in (slots or []):
            team_map[slot] = td.get_player_game(team, slot)
    return out


# Main endpoint (IDs + game meta). Cache varies only on `tracker`.
# Names for items/locations should be resolved client-side via the datapackage.

@api_endpoints.route("/sphere_tracker/<suuid:tracker>")
def api_sphere_tracker(tracker):
    """IDs view enriched with finder/receiver game metadata."""
    return _api_sphere_tracker_cached(tracker)


@cache.memoize(timeout=TRACKER_CACHE_TIMEOUT_IN_SECONDS)
def _api_sphere_tracker_cached(tracker):
    room = Room.get(tracker=tracker)
    if not room:
        # Let the global error handler format the 404 response.
        abort(404)

    td = TrackerData(room)
    used_pairs_by_team, _used_loc_ids_by_game, _used_item_flags_by_game = _collect_used_data(td)
    games_by_team = _collect_player_games(td)  # {team: {slot: game_name}}

    # Build compact payload (IDs) + game metadata with deterministic ordering
    out: list[dict[str, Any]] = []
    for team_id in sorted(used_pairs_by_team.keys()):
        spheres_out: list[dict[str, Any]] = []
        for sphere_idx in sorted(used_pairs_by_team[team_id].keys()):
            finders_out: list[dict[str, Any]] = []
            for finder_slot in sorted(used_pairs_by_team[team_id][sphere_idx].keys()):
                finder_game_name = (games_by_team.get(team_id, {}) or {}).get(finder_slot)
                receivers_out: list[dict[str, Any]] = []
                for receiver_slot in sorted(used_pairs_by_team[team_id][sphere_idx][finder_slot].keys()):
                    receiver_game_name = (games_by_team.get(team_id, {}) or {}).get(receiver_slot)
                    pairs = [
                        [item_id, loc_id]
                        for (item_id, loc_id) in used_pairs_by_team[team_id][sphere_idx][finder_slot][receiver_slot]
                    ]
                    receivers_out.append({
                        "receiver_slot": receiver_slot,
                        "receiver_game_name": receiver_game_name,
                        "pairs": pairs
                    })
                if receivers_out:
                    finders_out.append({
                        "finder_slot": finder_slot,
                        "finder_game_name": finder_game_name,
                        "receivers": receivers_out
                    })
            if finders_out:
                spheres_out.append({"sphere": sphere_idx, "finders": finders_out})
        if spheres_out:
            out.append({"team": team_id, "spheres": spheres_out})

    return jsonify(out)
