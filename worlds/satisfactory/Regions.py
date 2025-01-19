from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Location, Item, CollectionState
from .Locations import LocationData
from .GameLogic import GameLogic, PowerInfrastructureLevel
from .StateLogic import StateLogic
from .Options import SatisfactoryOptions, Placement

class SatisfactoryLocation(Location):
    game: str = "Satisfactory"
    event_name: Optional[str]

    def __init__(self, player: int, data: LocationData, region: Region):
        super().__init__(player, data.name, data.code, region)

        self.event_name = data.event_name

        if data.code is None:
            self.event = True
            self.locked = True

        if (data.rule):
            self.access_rule = data.rule

        if (data.non_progression):
            self.item_rule = self.non_progression_only

    @staticmethod
    def non_progression_only(item: Item) -> bool:
        return not item.advancement


def create_regions_and_return_locations(world: MultiWorld, options: SatisfactoryOptions, player: int, 
            game_logic: GameLogic, state_logic: StateLogic, locations: List[LocationData]):
    
    region_names: List[str] = [
        "Menu",
        "Overworld",
        "Gas Area",
        "Radioactive Area",
        "Mam",
        "AWESOME Shop"
    ]

    for hub_tier, milestones_per_hub_tier in enumerate(game_logic.hub_layout, 1):
        region_names.append(f"Hub Tier {hub_tier}")

        for minestone, _ in enumerate(milestones_per_hub_tier, 1):
            region_names.append(f"Hub {hub_tier}-{minestone}")

    for building_name, building in game_logic.buildings.items():
        if building.can_produce:
            region_names.append(building_name)

    for tree_name, tree in game_logic.man_trees.items():
        region_names.append(tree_name)

        for node in tree.nodes:
            region_names.append(f"{tree_name}: {node.name}")

    locations_per_region: Dict[str, LocationData] = get_locations_per_region(locations)
    regions: Dict[str, Region] = create_regions(world, player, locations_per_region, region_names)

    if __debug__:
        throwIfAnyLocationIsNotAssignedToARegion(regions, locations_per_region.keys())
        
    world.regions += regions.values()

    super_early_game_buildings: List[str] = [
        "Foundation", 
        "Walls Orange"
    ]

    early_game_buildings: List[str] = [
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

    connect(regions, "Menu", "Overworld")
    connect(regions, "Overworld", "Hub Tier 1")
    connect(regions, "Hub Tier 1", "Hub Tier 2",
            lambda state: state_logic.can_build_all(state, super_early_game_buildings))
    connect(regions, "Hub Tier 2", "Hub Tier 3", lambda state: state.has("Elevator Tier 1", player) 
                                                             and state_logic.can_build_all(state, early_game_buildings))
    connect(regions, "Hub Tier 3", "Hub Tier 4")
    connect(regions, "Hub Tier 4", "Hub Tier 5", lambda state: state.has("Elevator Tier 2", player))
    connect(regions, "Hub Tier 5", "Hub Tier 6")
    connect(regions, "Hub Tier 6", "Hub Tier 7", lambda state: state.has("Elevator Tier 3", player))
    connect(regions, "Hub Tier 7", "Hub Tier 8")
    connect(regions, "Hub Tier 8", "Hub Tier 9", lambda state: state.has("Elevator Tier 4", player))
    connect(regions, "Overworld", "Gas Area", lambda state:
                                state_logic.can_produce_all(state, ("Gas Mask", "Gas Filter")))
    connect(regions, "Overworld", "Radioactive Area", lambda state:
                                state_logic.can_produce_all(state, ("Hazmat Suit", "Iodine Infused Filter")))
    connect(regions, "Overworld", "Mam", lambda state: state_logic.can_build(state, "MAM"))
    connect(regions, "Overworld", "AWESOME Shop", lambda state:
                                state_logic.can_build_all(state, ("AWESOME Shop", "AWESOME Sink")))

    def can_produce_all_allowing_handcrafting(parts: Tuple[str, ...]) -> Callable[[CollectionState], bool]:
        def logic_rule(state: CollectionState):
            return state_logic.can_produce_all_allowing_handcrafting(state, game_logic, parts)

        return logic_rule

    for hub_tier, milestones_per_hub_tier in enumerate(game_logic.hub_layout, 1):
        for minestone, parts_per_milestone in enumerate(milestones_per_hub_tier, 1):
            connect(regions, f"Hub Tier {hub_tier}", f"Hub {hub_tier}-{minestone}",
                can_produce_all_allowing_handcrafting(parts_per_milestone.keys()))
            
    for building_name, building in game_logic.buildings.items():
        if building.can_produce:
            connect(regions, "Overworld", building_name,
                lambda state, building_name=building_name: state_logic.can_build(state, building_name))
        
    for tree_name, tree in game_logic.man_trees.items():
        connect(regions, "Mam", tree_name)

        for node in tree.nodes:
            if not node.depends_on:
                connect(regions, tree_name, f"{tree_name}: {node.name}",
                    lambda state, parts=node.unlock_cost.keys(): state_logic.can_produce_all(state, parts))
            else:
                for parent in node.depends_on:
                    connect(regions, f"{tree_name}: {parent}", f"{tree_name}: {node.name}", 
                        lambda state, parts=node.unlock_cost.keys(): state_logic.can_produce_all(state, parts))


def throwIfAnyLocationIsNotAssignedToARegion(regions: Dict[str, Region], regionNames: Set[str]):
    existingRegions = set()

    for region in regions.keys():
        existingRegions.add(region)

    if (regionNames - existingRegions):
        raise Exception(f"Satisfactory: the following regions are used in locations: {regionNames - existingRegions}, but no such region exists")


def create_region(world: MultiWorld, player: int, 
        locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:

    region = Region(name, player, world)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = SatisfactoryLocation(player, location_data, region)
            region.locations.append(location)

    return region


def create_regions(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]],
                    region_names: List[str]) -> Dict[str, Region]:

    regions: Dict[str, Region] = {}

    for name in region_names:
        regions[name] = create_region(world, player, locations_per_region, name)

    return regions


def connect(regions: Dict[str, Region], source: str, target: str, 
        rule: Optional[Callable[[CollectionState], bool]] = None):

    sourceRegion = regions[source]
    targetRegion = regions[target]

    sourceRegion.connect(targetRegion, rule=rule)


def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]]  = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
