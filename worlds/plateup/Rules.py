from typing import TYPE_CHECKING
import math
import sys

# Increase recursion limit to allow deep day chains (up to 1000). Default (~1000) is borderline once
# Archipelago stack usage adds frames. Set higher to prevent RecursionError.
sys.setrecursionlimit(5000)

from BaseClasses import Location, Entrance
from .Locations import (
    DISH_LOCATIONS,
    dish_dictionary
)

if TYPE_CHECKING:
    from . import PlateUpWorld

def set_rule(spot: Location | Entrance, rule):
    spot.access_rule = rule


def add_rule(spot: Location | Entrance, rule, combine="and"):
    old_rule = spot.access_rule
    if old_rule is Location.access_rule:
        spot.access_rule = rule if combine == "and" else old_rule
    else:
        if combine == "and":
            spot.access_rule = lambda state: rule(state) and old_rule(state)
        else:
            spot.access_rule = lambda state: rule(state) or old_rule(state)


def _extract_dish_day_number(name: str) -> int | None:
    if " - Day " not in name:
        return None
    try:
        return int(name.rsplit(" - Day ", 1)[1])
    except ValueError:
        return None


def restrict_locations_by_progression(world: "PlateUpWorld"):
    # Chain dish day locations to require the previous day.
    # For non-starting dishes, Day 1 requires the corresponding Unlock item.
    dish_order = getattr(world, 'valid_dish_locations', [])
    starting_dish = getattr(world, 'starting_dish', None)

    interval = max(1, int(world.options.day_lease_interval.value))
    try:
        required_days = max(1, int(world.options.day_count.value))
    except Exception:
        required_days = 1
    try:
        required_franchises = max(1, int(world.options.franchise_count.value))
    except Exception:
        required_franchises = 1
    total_progress_days = required_days if world.options.goal.value == 1 else 15 * required_franchises
    total_progress_days = max(1, total_progress_days)
    try:
        speed_upgrade_count = max(0, int(world.options.player_speed_upgrade_count.value))
    except Exception:
        speed_upgrade_count = 0
    speed_slots = max(1, speed_upgrade_count)
    speed_interval = max(1, math.ceil(total_progress_days / speed_slots))

    for i in range(len(dish_order) - 1):
        current_loc_name = dish_order[i]
        next_loc_name = dish_order[i + 1]
        # Only set rules when both exist in this world's locations
        if next_loc_name in world.location_name_to_id and current_loc_name in world.location_name_to_id:
            try:
                loc = world.get_location(next_loc_name)
                # Next requires reaching the previous
                add_rule(loc, lambda state, cur=current_loc_name: state.can_reach(cur, "Location", world.player))

                # If next is Day 1 of a non-starting dish, require Unlock
                if next_loc_name.endswith(" - Day 1"):
                    dish_name = next_loc_name.rsplit(" - Day ", 1)[0]
                    if starting_dish and dish_name != starting_dish:
                        unlock_item = f"{dish_name} Unlock"
                        add_rule(loc, lambda state, item=unlock_item: state.has(item, world.player))

                day_number = _extract_dish_day_number(next_loc_name)
                if day_number:
                    leases_required = max(0, (day_number - 1) // interval)
                    speed_required = min(speed_upgrade_count, (day_number - 1) // speed_interval)
                    add_rule(
                        loc,
                        lambda state, req=leases_required, spd=speed_required: (
                            state.has("Day Lease", world.player, req)
                            and state.has("Speed Upgrade Player", world.player, spd)
                        )
                    )
            except KeyError:
                pass


def filter_selected_dishes(world: "PlateUpWorld"):
    dish_count = world.options.dish.value
    if dish_count == 0:
        world.selected_dishes = []
        world.valid_dish_locations = []
        return

    # Do NOT re-randomize here; use the selection established earlier
    # in world.set_selected_dishes/create_items so item pool unlocks match.
    selected = getattr(world, "selected_dishes", [])

    planned_table = getattr(world, "_location_name_to_id", {})
    valid_locs = []
    for dish in selected:
        for day in range(1, 15 + 1):
            loc_name = f"{dish} - Day {day}"
            # Only include if defined and present in the planned location table used by regions
            if loc_name in DISH_LOCATIONS and loc_name in planned_table:
                valid_locs.append(loc_name)

    world.valid_dish_locations = valid_locs

def apply_rules(world: "PlateUpWorld"):
    goal_type = world.options.goal.value

    if goal_type == 1:
        # Chain day completions
        for i in range(2, 1001):  
            current_day = f"Complete Day {i}"
            prev_day = f"Complete Day {i-1}"
            try:
                loc_current = world.get_location(current_day)
                loc_current.access_rule = (
                    lambda state, p=prev_day: state.can_reach(p, "Location", world.player)
                )
            except KeyError:
                pass
        # Chain star completions (each star requires previous star)
        max_stars = (world.options.day_count.value + 2) // 3  # ceil(day_count/3)
        for i in range(2, max_stars + 1):
            current_star = f"Complete Star {i}"
            prev_star = f"Complete Star {i-1}"
            try:
                loc_current = world.get_location(current_star)
                loc_current.access_rule = (
                    lambda state, p=prev_star: state.can_reach(p, "Location", world.player)
                )
            except KeyError:
                pass
    else:
        # Chain franchise goal completions
        for i in range(2, 51):  # expanded to support up to 50 franchises
            suffix = "" if i - 1 == 1 else f" {i-1}"
            try:
                loc = world.get_location(f"Franchise {i} times")
                required_loc = f"Franchise - Complete Day 15 After Franchised{suffix}"
                loc.access_rule = lambda state, req=required_loc: state.can_reach(req, "Location", world.player)
            except KeyError:
                pass
        # Chain stars within each franchise run (each star after the first requires the previous in same run)
        star_labels = ["First Star", "Second Star", "Third Star", "Fourth Star", "Fifth Star"]
        for run in range(50):  # runs 0..49
            suffix = "" if run == 0 else (" After Franchised" if run == 1 else f" After Franchised {run}")
            # Build full names
            for idx in range(1, len(star_labels)):
                prev_name = f"Franchise - {star_labels[idx-1]}{suffix}"
                cur_name = f"Franchise - {star_labels[idx]}{suffix}"
                try:
                    loc_current = world.get_location(cur_name)
                    loc_current.access_rule = (
                        lambda state, p=prev_name: state.can_reach(p, "Location", world.player)
                    )
                except KeyError:
                    pass

        # Explicitly gate franchise day completion locations by Day Lease and Player Speed,
        # mirroring the region entrance rules so spheres reflect lease requirements.
        try:
            required_franchises = int(world.options.franchise_count.value)
        except Exception:
            required_franchises = 1
        # Lease cadence and speed-gating must match Regions.create_plateup_regions
        interval = max(1, int(world.options.day_lease_interval.value))
        # Compute speed interval across all franchise days
        total_days = 15 * required_franchises if required_franchises > 0 else 15
        speed_slots = max(1, int(world.options.player_speed_upgrade_count.value))
        # Ceiling so last chunk can be shorter
        import math as _math
        speed_interval = max(1, _math.ceil(total_days / speed_slots))

        def run_suffix(run: int) -> str:
            if run == 0:
                return ""
            if run == 1:
                return " After Franchised"
            return f" After Franchised {run}"

        def day_label(d: int) -> str:
            mapping = {1: "First Day", 2: "Second Day", 3: "Third Day", 4: "Fourth Day", 5: "Fifth Day"}
            return mapping.get(d, f"Day {d}")

        for run in range(required_franchises):
            suff = run_suffix(run)
            for d in range(1, 16):
                cur_name = f"Franchise - Complete {day_label(d)}{suff}"
                # Leases required based on global day number (run*15 + d)
                global_day = run * 15 + d
                leases_required = (global_day - 1) // interval
                speed_required = min(int(world.options.player_speed_upgrade_count.value), (global_day - 1) // speed_interval)

                # Previous completion within the same run or prior run's Day 15 when d == 1 and run > 0
                if d == 1:
                    if run == 0:
                        prev_name = None
                    else:
                        prev_name = f"Franchise - Complete Day 15{run_suffix(run - 1)}"
                else:
                    prev_name = f"Franchise - Complete {day_label(d-1)}{suff}"

                try:
                    loc_cur = world.get_location(cur_name)
                    # Build rule requiring leases/speed (and previous completion if applicable)
                    if prev_name is None:
                        loc_cur.access_rule = (
                            lambda state, req=leases_required, spd=speed_required: (
                                state.has("Day Lease", world.player, req)
                                and state.has("Speed Upgrade Player", world.player, spd)
                            )
                        )
                    else:
                        loc_cur.access_rule = (
                            lambda state, p=prev_name, req=leases_required, spd=speed_required: (
                                state.can_reach(p, "Location", world.player)
                                and state.has("Day Lease", world.player, req)
                                and state.has("Speed Upgrade Player", world.player, spd)
                            )
                        )
                except KeyError:
                    # This day's franchise completion might not be present (e.g., beyond required runs)
                    pass

    try:
        lose_loc = world.get_location("Lose a Run")
        if world.options.goal.value == 1:
            # Day goal: require completion of Day 1
            lose_loc.access_rule = lambda state: state.can_reach("Complete Day 1", "Location", world.player)
        else:
            # Franchise goal: require completion of the first franchise day
            lose_loc.access_rule = lambda state: state.can_reach("Franchise - Complete First Day", "Location", world.player)
    except KeyError:
        pass