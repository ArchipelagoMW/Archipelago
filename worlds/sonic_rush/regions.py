from typing import Dict, Tuple, List, Callable

from BaseClasses import Region, MultiWorld, LocationProgressType as LocProg, ItemClassification, CollectionState
from worlds.generic.Rules import set_rule
from .items import SonicRushItem, emeralds
from .locations import SonicRushLocation
from .options import SonicRushOptions
from .data import region_names, zone_number_by_name, zone_name_by_number, zone_names_without_f_zone


def can_play_zone(state: CollectionState, player: int, zone: str, char: str) -> bool:
    if state.has(zone, player):
        # Zone is unlocked, no further checking needed
        return True
    progressive_level_selects = state.count(f"Progressive Level Select ({char})", player)
    if not progressive_level_selects >= zone_number_by_name[char][zone]:
        # Not enough progressive level selects, zone is unreachable
        return False
    # Zone is reachable through level select, but level select must be accessible through another zone
    for any_zone in range(1, progressive_level_selects+1):
        if state.has(zone_name_by_number[char][any_zone], player):
            return True
    # Neither unlocked nor through level select accessible
    return False


def can_play_f_zone(state: CollectionState, player: int) -> bool:
    return state.has("F-Zone", player)


def can_play_extra_zone(state: CollectionState, player: int) -> bool:
    return state.has_all(emeralds, player)


def can_play_all_main_zones(state: CollectionState, player: int, char: str, options: SonicRushOptions) -> bool:
    for zone in zone_names_without_f_zone:
        if not can_play_zone(state, player, zone, char):
            return False
    return options.screw_f_zone or can_play_f_zone(state, player)


def create_regions(player: int, multiworld: MultiWorld, options: SonicRushOptions, location_name_to_id: dict[str, int],
                   included_locations: List[Tuple[str, str, LocProg]]) -> List[Region]:
    """Creates and returns a list of all regions with entrances and all locations placed correctly."""

    regions: Dict[str, Region] = {
        name: Region(name, player, multiworld)
        for name in region_names
    }

    for loc in included_locations:
        regions[loc[1]].locations += [
            SonicRushLocation(
                player, loc[0], location_name_to_id[loc[0]], regions[loc[1]], loc[2]
            )
        ]

    # Create goal event
    goal_location = SonicRushLocation(player, "Goal", None, regions["Goal"], LocProg.DEFAULT)
    goal_location.place_locked_item(SonicRushItem("Goal", ItemClassification.progression_skip_balancing, None, player))
    if options.goal in ["bosses_once", "bosses_both"]:
        set_rule(
            goal_location,
            lambda state: can_play_all_main_zones(state, player, "Sonic", options) and
                          can_play_all_main_zones(state, player, "Blaze", options)
        )
    elif options.goal == "extra_zone":
        set_rule(
            goal_location,
            lambda state: can_play_extra_zone(state, player)
        )
    elif options.goal == "100_percent":
        set_rule(
            goal_location,
            lambda state: can_play_all_main_zones(state, player, "Sonic", options) and
                          can_play_all_main_zones(state, player, "Blaze", options) and
                          can_play_extra_zone(state, player)
        )
    else:  # In case I add another goal and forget to add a rule for it
        set_rule(goal_location, lambda state: False)
    regions["Goal"].locations.append(goal_location)
    multiworld.completion_condition[player] = lambda state: state.has("Goal", player)

    def get_zone_rule(z: str, c: str) -> Callable[[CollectionState], bool]:
        """Helper function because lambdas don't like to be in for loops"""
        return lambda state: can_play_zone(state, player, z, c)

    # Connect Menu to rest of regions
    regions["Menu"].connect(regions["Goal"], "Defeat Eggman")
    regions["Menu"].connect(
        regions["Extra Zone"], "Access Extra Zone",
        lambda state: can_play_extra_zone(state, player)
    )
    for char in ["Sonic", "Blaze"]:
        regions["Menu"].connect(
            regions[f"F-Zone ({char})"], f"Access F-Zone ({char})",
            lambda state: can_play_f_zone(state, player)
        )
        for zone in zone_names_without_f_zone:
            regions["Menu"].connect(
                regions[f"{zone} ({char})"], f"Access {zone} ({char})",
                get_zone_rule(zone, char)
            )

    return list(regions.values())
