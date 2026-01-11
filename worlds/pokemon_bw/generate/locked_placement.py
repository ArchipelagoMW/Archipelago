
from typing import TYPE_CHECKING

from BaseClasses import Item, Location, LocationProgressType as LocProgType

if TYPE_CHECKING:
    from .. import PokemonBWWorld


def is_excluded(world: "PokemonBWWorld", location: Location) -> bool:
    return location.progress_type == LocProgType.EXCLUDED or location.name in world.options.exclude_locations


def place_badges_locked(world: "PokemonBWWorld", items: list[Item]) -> None:
    from ..data.locations.ingame_items import special
    from ..data.items import badges

    match world.options.shuffle_badges.current_key:
        case "vanilla":
            # Priority locations are ignored here because of no badges being filler
            # Shuffling items and locations not needed since this option is about specific placement
            badge_items: dict[str, Item] = {
                item.name: item
                for item in items
                if item.name in badges.table
            }
            badge_locations: dict[str, Location] = {
                loc.name: loc
                for loc in world.get_locations()
                if loc.name in special.gym_badges
            }
            placements = {
                "Striaton Gym - Badge reward": "Trio Badge",
                "Nacrene Gym - Badge reward": "Basic Badge",
                "Castelia Gym - Badge reward": "Insect Badge",
                "Nimbasa Gym - Badge reward": "Bolt Badge",
                "Driftveil Gym - Badge reward": "Quake Badge",
                "Mistralton Gym - Badge reward": "Jet Badge",
                "Icirrus Gym - Badge reward": "Freeze Badge",
                "Opelucid Gym - Badge reward": "Legend Badge",
            }
            for loc, it in placements.items():
                if is_excluded(world, badge_locations[loc]):
                    continue
                badge_locations[loc].place_locked_item(badge_items[it])
                items.remove(badge_items[it])
        case "shuffle":
            # Priority locations are ignored here because of no badges being filler
            # Shuffle items because of some locations potentially being skipped
            badge_items: list[Item] = [item for item in items if item.name in badges.table]
            world.random.shuffle(badge_items)
            # Locations not shuffled since items are shuffled
            badge_locations: list[Location] = [
                loc
                for loc in world.get_locations()
                if loc.name in special.gym_badges
                if not is_excluded(world, loc)
            ]
            for location in badge_locations:
                item = badge_items.pop()
                location.place_locked_item(item)
                items.remove(item)
        case "any_badge":
            pass
        case "anything":
            pass
        case _:
            raise Exception(f"Bad shuffle_badges option value for player {world.player_name}")


def place_badges_fill(world: "PokemonBWWorld",
                      progitempool: list[Item],
                      usefulitempool: list[Item],
                      filleritempool: list[Item],
                      fill_locations: list[Location]) -> None:
    from ..data.locations.ingame_items import special

    match world.options.shuffle_badges.current_key:
        case "vanilla":
            pass
        case "shuffle":
            pass
        case "any_badge":
            # Both already shuffled
            # Items already sorted by classification
            # Sort location by progress type (priority - default - excluded)
            badge_items: list[tuple[Item, list[Item]]] = [
                (item, pool)
                for pool in (progitempool, usefulitempool, filleritempool)
                for item in pool
                if "badge" in item.name.lower()
            ]
            badge_locs: list[Location] = [
                loc
                for loc in fill_locations
                if loc.player == world.player and loc.name in special.gym_badges
            ]
            to_place = 0
            for to_check in range(1, len(badge_locs)):
                if badge_locs[to_check].progress_type == LocProgType.PRIORITY:
                    badge_locs[to_check], badge_locs[to_place] = badge_locs[to_place], badge_locs[to_check]
                    to_place += 1
            to_place = len(badge_locs) - 1
            for to_check in reversed(range(0, len(badge_locs)-2)):
                if badge_locs[to_check].progress_type == LocProgType.EXCLUDED:
                    badge_locs[to_check], badge_locs[to_place] = badge_locs[to_place], badge_locs[to_check]
                    to_place -= 1
            # First fill priority locations with prog and useful items until either is exhausted
            min_of_lens = min(len(badge_items), len(badge_locs))
            filled_from_prio = 0
            while filled_from_prio < min_of_lens:
                loc = badge_locs[filled_from_prio]
                if loc.progress_type != LocProgType.PRIORITY:
                    break
                item, pool = badge_items[filled_from_prio]
                if pool == filleritempool:
                    break
                loc.place_locked_item(item)
                pool.remove(item)
                fill_locations.remove(loc)
                filled_from_prio += 1
            # Now fill excluded locations with only filler
            taken_from_excluded = 0
            while taken_from_excluded < min_of_lens:
                loc = badge_locs[-1-taken_from_excluded]
                if loc.progress_type != LocProgType.EXCLUDED:
                    break
                item, pool = badge_items[-1-taken_from_excluded]
                if pool != filleritempool:
                    break
                loc.place_locked_item(item)
                pool.remove(item)
                fill_locations.remove(loc)
                taken_from_excluded += 1
            # Skip potential remaining excluded locations and let them be filled by main fill
            while (
                taken_from_excluded < min_of_lens and
                badge_locs[-1-taken_from_excluded].progress_type == LocProgType.EXCLUDED
            ):
                taken_from_excluded += 1
            # Randomly fill remaining items into remaining locations
            remaining_items = badge_items[filled_from_prio:len(badge_items)-taken_from_excluded]
            remaining_locs = badge_locs[filled_from_prio:len(badge_locs)-taken_from_excluded]
            world.random.shuffle(remaining_items)
            world.random.shuffle(remaining_locs)
            for i in range(min(len(remaining_items), len(remaining_locs))):
                loc = remaining_locs[i]
                item, pool = remaining_items[i]
                loc.place_locked_item(item)
                pool.remove(item)
                fill_locations.remove(loc)
        case "anything":
            pass
        case _:
            raise Exception(f"Bad shuffle_badges option value for player {world.player_name}")


def place_tm_hm_locked(world: "PokemonBWWorld", items: list[Item]) -> None:
    from ..data.locations.ingame_items.special import tm_hm_ncps, gym_tms
    from ..data.locations import all_tm_locations
    from ..data.items import tm_hm, all_tm_hm

    match world.options.shuffle_tm_hm.current_key:
        case "shuffle":
            # Priority locations are ignored here because of no TMs/HMs being filler
            # Get TMs and HMs shuffled
            tm_hm_items: list[Item] = [item for item in items if item.name in all_tm_hm]
            world.random.shuffle(tm_hm_items)
            # Shuffle locations to prevent always having all HMs in the same few spots
            tm_hm_locs: list[Location] = [
                loc
                for loc in world.get_locations()
                if loc.name in all_tm_locations
                if not is_excluded(world, loc)
            ]
            world.random.shuffle(tm_hm_locs)
            # Take only a slice of items and sort included HMs to front to prevent problems with HM rules
            tm_hm_items = tm_hm_items[:len(tm_hm_locs)]
            to_place = 0
            for to_check in range(1, len(tm_hm_items)):
                if tm_hm_items[to_check].name in tm_hm.hm:
                    tm_hm_items[to_check], tm_hm_items[to_place] = tm_hm_items[to_place], tm_hm_items[to_check]
                    to_place += 1
            for item in tm_hm_items:
                for location in tm_hm_locs:
                    hm_rule = all_tm_locations[location.name].hm_rule
                    if hm_rule is None or hm_rule(item.name):
                        tm_hm_locs.remove(location)
                        location.place_locked_item(item)
                        items.remove(item)
                        break
        case "hm_with_badge":
            tm_items = [item for item in items if item.name in tm_hm.tm and "TM70" not in item.name]
            hm_items = [item for item in items if item.name in tm_hm.hm or "TM70" in item.name]
            other_tm_locations: list[Location] = [
                loc
                for loc in world.get_locations()
                if loc.name in tm_hm_ncps
                if not is_excluded(world, loc)
            ]
            gym_tm_locations: list[Location] = [
                loc
                for loc in world.get_locations()
                if loc.name in gym_tms
                if not is_excluded(world, loc)
            ]
            # Shuffle everything
            # If no gym location is excluded, add one random TM to HMs
            if len(gym_tm_locations) == 8:
                rand_tm = world.random.choice(tm_items)
                hm_items.append(rand_tm)
                tm_items.remove(rand_tm)
            world.random.shuffle(hm_items)
            world.random.shuffle(other_tm_locations)
            world.random.shuffle(gym_tm_locations)
            # Place HMs into gym locations first
            for loc in gym_tm_locations:
                item = hm_items.pop()
                loc.place_locked_item(item)
                items.remove(item)
            # If more than one gym location was excluded, add remaining HMs to TM list and shuffle that
            tm_items.extend(hm_items)
            world.random.shuffle(tm_items)
            # Take only a slice of items and sort included HMs to front to prevent problems with HM rules
            tm_items = tm_items[:len(other_tm_locations)]
            to_place = 0
            for to_check in range(1, len(tm_items)):
                if tm_items[to_check].name in tm_hm.hm:
                    tm_items[to_check], tm_items[to_place] = tm_items[to_place], tm_items[to_check]
                    to_place += 1
            for item in tm_items:
                for location in other_tm_locations:
                    hm_rule = all_tm_locations[location.name].hm_rule
                    if hm_rule is None or hm_rule(item.name):
                        other_tm_locations.remove(location)
                        location.place_locked_item(item)
                        items.remove(item)
                        break
        case "any_tm_hm":
            pass
        case "anything":
            pass
        case _:
            raise Exception(f"Bad shuffle_tm_hm option value for player {world.player_name}")


def place_tm_hm_fill(world: "PokemonBWWorld",
                     progitempool: list[Item],
                     usefulitempool: list[Item],
                     filleritempool: list[Item],
                     fill_locations: list[Location]) -> None:
    from ..data.locations import all_tm_locations

    match world.options.shuffle_tm_hm.current_key:
        case "shuffle":
            pass
        case "hm_with_badge":
            pass
        case "any_tm_hm":
            # Both already shuffled
            # Items already sorted by classification
            # Sort location by progress type (priority - default - excluded)
            tm_hm_items: list[tuple[Item, list[Item]]] = [
                (item, pool)
                for pool in (progitempool, usefulitempool, filleritempool)
                for item in pool
                if len(item.name) > 2 and item.name[:2].lower() in ("tm", "hm") and item.name[2].isdigit()
            ]
            tm_hm_locs: list[Location] = [
                loc
                for loc in fill_locations
                if loc.player == world.player and loc.name in all_tm_locations
            ]
            # Sort HMs to front to prevent problems with HM rules
            to_place = 0
            for to_check in range(1, len(tm_hm_locs)):
                if all_tm_locations[tm_hm_locs[to_check].name].hm_rule is not None:
                    tm_hm_locs[to_check], tm_hm_locs[to_place] = tm_hm_locs[to_place], tm_hm_locs[to_check]
                    to_place += 1
            # By creating new lists, locations with HM rules should be at the front
            priority_locs = [loc for loc in tm_hm_locs if loc.progress_type == LocProgType.PRIORITY]
            default_locs = [loc for loc in tm_hm_locs if loc.progress_type == LocProgType.DEFAULT]
            excluded_locs = [loc for loc in tm_hm_locs if loc.progress_type == LocProgType.EXCLUDED]
            # First fill priority locations with prog and useful items until either is exhausted
            for loc in priority_locs:
                for item, pool in tm_hm_items:
                    if pool == filleritempool:
                        default_locs.insert(0, loc)
                        break
                    hm_rule = all_tm_locations[loc.name].hm_rule
                    if hm_rule is None or hm_rule(item.name):
                        loc.place_locked_item(item)
                        tm_hm_items.remove((item, pool))
                        pool.remove(item)
                        fill_locations.remove(loc)
                        break
                else:
                    default_locs.insert(0, loc)
            # Now fill excluded locations with only filler
            for loc in excluded_locs:
                for item, pool in reversed(tm_hm_items):
                    if pool != filleritempool:
                        break
                    hm_rule = all_tm_locations[loc.name].hm_rule
                    if hm_rule is None or hm_rule(item.name):
                        loc.place_locked_item(item)
                        tm_hm_items.remove((item, pool))
                        pool.remove(item)
                        fill_locations.remove(loc)
                        break
            # Fill remaining priority and default locations with remaining items
            # Priority locations, which are at the end of the default list, will be filled (with filler) first
            # Shuffle remaining items again to prevent having one world using up all remaining prog or filler items
            # and only leaving useful items for other worlds
            world.random.shuffle(tm_hm_items)
            for loc in default_locs:
                for item, pool in tm_hm_items:
                    hm_rule = all_tm_locations[loc.name].hm_rule
                    if hm_rule is None or hm_rule(item.name):
                        loc.place_locked_item(item)
                        tm_hm_items.remove((item, pool))
                        pool.remove(item)
                        fill_locations.remove(loc)
                        break
        case "anything":
            pass
        case _:
            raise Exception(f"Bad shuffle_tm_hm option value for player {world.player_name}")
