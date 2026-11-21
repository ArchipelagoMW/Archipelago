from typing import Optional
from collections.abc import Callable
from BaseClasses import MultiWorld, Region, Location, Item, CollectionState
from .Locations import LocationData
from .GameLogic import GameLogic, PowerInfrastructureLevel
from .StateLogic import StateLogic
from .Options import SatisfactoryOptions, Placement
from .CriticalPathCalculator import CriticalPathCalculator


class SatisfactoryLocation(Location):
    game: str = "Satisfactory"
    event_name: Optional[str]

    def __init__(self, player: int, data: LocationData, region: Region):
        super().__init__(player, data.name, data.code, region)

        self.event_name = data.event_name

        if data.code is None:
            self.event = True
            self.locked = True

        if data.rule:
            self.access_rule = data.rule

        if data.non_progression:
            self.item_rule = self.non_progression_only

    @staticmethod
    def non_progression_only(item: Item) -> bool:
        return not item.advancement


def create_regions_and_return_locations(multiworld: MultiWorld, options: SatisfactoryOptions, player: int,
                                        game_logic: GameLogic, state_logic: StateLogic,
                                        critical_path: CriticalPathCalculator, locations: list[LocationData]) -> None:
    
    region_names: list[str] = [
        "Overworld",
        "Mam",
        "AWESOME Shop"
    ]

    for hub_tier, milestones_per_hub_tier in enumerate(game_logic.hub_layout, 1):
        if hub_tier > (options.final_elevator_phase * 2):
            break

        region_names.append(f"Hub Tier {hub_tier}")

        for milestone, _ in enumerate(milestones_per_hub_tier, 1):
            region_names.append(f"Hub {hub_tier}-{milestone}")

    region_names += [
        building_name
        for building_name, building in game_logic.buildings.items()
        if building.can_produce and building_name in critical_path.required_buildings
    ]

    for tree_name, tree in game_logic.man_trees.items():
        if tree_name == "Ficsmas" and not "Erect a FICSMAS Tree" in options.goal_selection:
            continue

        region_names.append(tree_name)

        for node in tree.nodes:
            if node.minimal_phase <= options.final_elevator_phase:
                region_names.append(f"{tree_name}: {node.name}")

    locations_per_region: dict[str, list[LocationData]] = get_locations_per_region(locations)
    regions: dict[str, Region] = create_regions(multiworld, player, locations_per_region, region_names)

    if __debug__:
        throw_if_any_location_is_not_assigned_to_a__region(regions, locations_per_region)
        
    multiworld.regions += regions.values()

    super_early_game_buildings: list[str] = [
        "Foundation", 
        "Walls Orange"
    ]

    early_game_buildings: list[str] = [
        PowerInfrastructureLevel.Automated.to_name()
    ]

    if options.mam_logic_placement.value == Placement.early:
        early_game_buildings.append("MAM")
    if options.awesome_logic_placement.value == Placement.early:
        early_game_buildings.append("AWESOME Sink")
        early_game_buildings.append("AWESOME Shop")
    if options.energy_link_logic_placement.value == Placement.early:
        early_game_buildings.append("Power Storage")
    if options.splitter_placement == Placement.early:
        super_early_game_buildings.append("Conveyor Splitter")
        super_early_game_buildings.append("Conveyor Merger")

    if options.final_elevator_phase == 1:
        super_early_game_buildings.extend(early_game_buildings)

    # Hub Tier 1 and 2 are always accessible, so universal tracker should display them out the gates
    is_universal_tracker = getattr(multiworld, "generation_is_fake", False)

    connect(regions, "Overworld", "Hub Tier 1")
    connect(regions, "Hub Tier 1", "Hub Tier 2",
            lambda state: is_universal_tracker or state_logic.can_build_all(state, super_early_game_buildings))

    if options.final_elevator_phase >= 2:
        connect(regions, "Hub Tier 2", "Hub Tier 3", lambda state: state.has("Elevator Phase 1", player)
                and (is_universal_tracker or state_logic.can_build_all(state, early_game_buildings)))
        connect(regions, "Hub Tier 3", "Hub Tier 4")
    if options.final_elevator_phase >= 3:
        connect(regions, "Hub Tier 4", "Hub Tier 5", lambda state: state.has("Elevator Phase 2", player))
        connect(regions, "Hub Tier 5", "Hub Tier 6")
    if options.final_elevator_phase >= 4:
        connect(regions, "Hub Tier 6", "Hub Tier 7", lambda state: state.has("Elevator Phase 3", player))
        connect(regions, "Hub Tier 7", "Hub Tier 8")
    if options.final_elevator_phase >= 5:
        connect(regions, "Hub Tier 8", "Hub Tier 9", lambda state: state.has("Elevator Phase 4", player))

    connect(regions, "Overworld", "Mam", lambda state: state_logic.can_build(state, "MAM"))
    connect(regions, "Overworld", "AWESOME Shop",
            lambda state: state_logic.can_build_all(state, ("AWESOME Shop", "AWESOME Sink")))

    for hub_tier, milestones_per_hub_tier in enumerate(game_logic.hub_layout, 1):
        if hub_tier > (options.final_elevator_phase * 2):
            break

        for milestone, parts_per_milestone in enumerate(milestones_per_hub_tier, 1):
            connect(regions, f"Hub Tier {hub_tier}", f"Hub {hub_tier}-{milestone}",
                    state_logic.get_can_produce_all_allowing_handcrafting_rule(parts_per_milestone))
            
    for building_name, building in game_logic.buildings.items():
        if building.can_produce and building_name in critical_path.required_buildings:
            connect(regions, "Overworld", building_name,
                    lambda state, name=building_name: state_logic.can_build(state, name))
        
    for tree_name, tree in game_logic.man_trees.items():
        if tree_name == "Ficsmas" and not "Erect a FICSMAS Tree" in options.goal_selection:
            continue

        connect(regions, "Mam", tree_name)

        for node in tree.nodes:
            if node.minimal_phase > options.final_elevator_phase:
                continue

            if not node.depends_on:
                connect(regions, tree_name, f"{tree_name}: {node.name}",
                        lambda state, parts=node.unlock_cost, items=node.requires_items: \
                                state_logic.can_produce_all(state, parts) and state_logic.has_obtained_all(state, items))
            else:
                for parent in node.depends_on:
                    if f"{tree_name}: {parent}" in region_names:
                        connect(regions, f"{tree_name}: {parent}", f"{tree_name}: {node.name}",
                                lambda state, parts=node.unlock_cost, items=node.requires_items: \
                                        state_logic.can_produce_all(state, parts) and state_logic.has_obtained_all(state, items))


def throw_if_any_location_is_not_assigned_to_a__region(regions: dict[str, Region],
                                                       region_names: dict[str, list[LocationData]]) -> None:
    existing_regions = set(regions)
    existing_region_names = set(region_names)

    if existing_region_names - existing_regions:
        raise Exception(f"Satisfactory: the following regions are used in locations: "
                        f"{existing_region_names - existing_regions}, but no such region exists")


def create_region(multiworld: MultiWorld, player: int,
                  locations_per_region: dict[str, list[LocationData]], name: str) -> Region:

    region = Region(name, player, multiworld)

    if name in locations_per_region:
        region.locations += [
            SatisfactoryLocation(player, location_data, region)
            for location_data in locations_per_region[name]
        ]

    return region


def create_regions(multiworld: MultiWorld, player: int, locations_per_region: dict[str, list[LocationData]],
                   region_names: list[str]) -> dict[str, Region]:
    return {
        name: create_region(multiworld, player, locations_per_region, name)
        for name in region_names
    }


def connect(regions: dict[str, Region], source: str, target: str,
            rule: Optional[Callable[[CollectionState], bool]] = None) -> None:

    source_region = regions[source]
    target_region = regions[target]

    source_region.connect(target_region, rule=rule)


def get_locations_per_region(locations: list[LocationData]) -> dict[str, list[LocationData]]:
    per_region: dict[str, list[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
