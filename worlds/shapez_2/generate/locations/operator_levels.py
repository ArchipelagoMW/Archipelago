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

    for level in range(adjust["Operator level checks"]):
        region_num = level // max(5, adjust["Operator level checks"] // adjust["Operator lines"] + 1) + 1
        region = regions[f"Operator levels (section {region_num})"]
        name = f"Operator level {level + 1}"
        region.locations.append(Shapez2Location(world.player, name, world.location_name_to_id[name], region,
                                                all_locations[name].progress_type(world), rule))
