from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from ... import Shapez2World
    from ...data import AccessRule


def create_locations(world: "Shapez2World", regions: dict[str, Region]) -> None:
    from ...locations import Shapez2Location
    from ...data.locations import all_locations

    rule: "AccessRule" = lambda state: True
    adjust = world.options.location_adjustments

    for milestone in range(adjust["Milestones"]):
        checks_count = world.random.randint(adjust["Minimum checks per milestone"],
                                            adjust["Maximum checks per milestone"])
        world.milestone_checks_counts.append(checks_count)
        for check in range(checks_count):
            region = regions[f"Milestone {milestone + 1}"]
            name = f"Milestone {milestone + 1} reward #{check + 1}"
            region.locations.append(Shapez2Location(world.player, name, world.location_name_to_id[name], region,
                                                    all_locations[name].progress_type(world), rule))
