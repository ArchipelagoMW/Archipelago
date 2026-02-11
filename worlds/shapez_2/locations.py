
import math
from typing import Optional, TYPE_CHECKING

from BaseClasses import Location, Region, LocationProgressType, ItemClassification
from .data.locations import milestones, tasks, operator_levels

if TYPE_CHECKING:
    from . import Shapez2World
    from .data import ExtendedRule, AccessRule


class Shapez2Location(Location):
    game = "shapez 2"

    def __init__(self, player: int, name: str, address: Optional[int], region: Region,
                 progress_type: LocationProgressType, rule: "AccessRule"):
        super(Shapez2Location, self).__init__(player, name, address, region)
        self.progress_type = progress_type
        self.access_rule = rule


def lookup_table() -> dict[str, int]:
    return {
        name: data.location_id
        for table in (milestones.locations, tasks.locations, operator_levels.locations)
        for name, data in table.items()
    }


def get_regions(world: "Shapez2World") -> dict[str, Region]:

    adjust = world.options.location_adjustments

    return {
        "Menu": Region("Menu", world.player, world.multiworld),
        "Events": Region("Events", world.player, world.multiworld),
    } | {
        f"Milestone {x}": Region(f"Milestone {x}", world.player, world.multiworld)
        for x in range(1, adjust["Milestones"] + 1)
    } | {
        f"Task line {x}": Region(f"Task line {x}", world.player, world.multiworld)
        for x in range(1, adjust["Task lines"] + 1)
    } | {
        f"Operator levels (section {x})": Region(f"Operator levels (section {x})", world.player, world.multiworld)
        for x in range(
            1,
            adjust["Operator lines"] + 1
            if adjust["Operator level checks"] // adjust["Operator lines"] >= 5
            else int(math.ceil(adjust["Operator level checks"] / 5)) + 1
        )
    }


def connect_regions(world: "Shapez2World", regions: dict[str, Region]) -> None:
    from .data import region_connections

    def get_rule(ext_rule: Optional["ExtendedRule"]) -> "AccessRule":
        if ext_rule is None:
            return lambda state: True
        else:
            return lambda state: ext_rule(state, world)

    for name, data in region_connections.connections.items():
        if data.entering_region in regions and data.exiting_region in regions:
            regions[data.exiting_region].connect(
                regions[data.entering_region],
                name,
                get_rule(data.rule)
            )


def pre_generate_logic(world: "Shapez2World") -> None:
    from .generate.shapes import milestones, task_lines, operator_lines, blueprint_points

    world.milestone_processors = milestones.get_processors_list(world)
    world.task_processors = task_lines.get_processors_list(world)
    world.operator_processors = operator_lines.get_processors_list(world, world.milestone_processors)

    world.milestone_shapes = milestones.get_shapes_list(world, world.milestone_processors)
    world.task_shapes = task_lines.get_shapes_list(world, world.task_processors)
    world.operator_shapes = operator_lines.get_shapes_list(world, world.operator_processors)
    world.blueprint_shapes = blueprint_points.get_shapes_list(world)

    world.blueprint_points = blueprint_points.get_points(world, world.blueprint_shapes)


def create_events(world: "Shapez2World",
                  regions: dict[str, Region],
                  processor_rules_dict: dict[tuple[str, ...], "AccessRule"]) -> None:
    from .generate.events import milestones, operator_lines, processors, task_lines
    from .items import Shapez2Item

    processors.get_events(world, regions)  # ALWAYS run this first!!!
    milestones.get_events(world, regions, processor_rules_dict)
    task_lines.get_events(world, regions)
    operator_lines.get_events(world, regions, processor_rules_dict)

    if world.options.goal == "milestones":
        world.multiworld.completion_condition[world.player] = lambda state: (
            state.has(f"[ACCESS] Milestone {world.options.location_adjustments['Milestones']}", world.player)
        )
    else:
        item = Shapez2Item("Goal", ItemClassification.progression, None, world.player)
        region = regions["Events"]
        location = Shapez2Location(
            world.player, "[EVENT] Last operator level", None, region, LocationProgressType.DEFAULT,
            lambda state: state.can_reach_location(
                f"Operator level {world.options.location_adjustments['Operator level checks']}", world.player
            )
        )
        region.locations.append(location)
        location.place_locked_item(item)
        world.multiworld.completion_condition[world.player] = lambda state: state.has("Goal", world.player)


def create_and_place_locations(world: "Shapez2World",
                               regions: dict[str, Region],
                               processor_rules_dict: dict[tuple[str, ...], "AccessRule"]) -> None:
    from .generate.locations import milestones, tasks, operator_levels

    milestones.create_locations(world, regions)
    tasks.create_locations(world, regions, processor_rules_dict)
    operator_levels.create_locations(world, regions)
