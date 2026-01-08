from __future__ import annotations

import typing as t
from BaseClasses import ItemClassification, Location, MultiWorld, Region

from .constants import AVRegions, START_OPTION_MAP
from .location_data import entrance_data, location_data
from .items import AVItem

if t.TYPE_CHECKING:
    from .types import LogicContext


class AVLocation(Location):
    game = "Axiom Verge"


def create_regions(context: LogicContext, multiworld: MultiWorld):
    regions: t.Dict[str, Region] = {}
    for enum_type in AVRegions:
        region_name = enum_type.value
        region = Region(region_name, context.player, multiworld)
        multiworld.regions.append(region)
        regions[region_name] = region

    for source_name, dest_name, condition_func, bidirectional, *name in entrance_data:
        source, destination = regions[source_name], regions[dest_name]
        access_rule = lambda state, func=condition_func: func(state, context)

        if name:
            source.connect(destination, name[0], rule=access_rule)
        else:
            source.connect(destination, rule=access_rule)

        if bidirectional:
            destination.connect(source, rule=access_rule)

    # Dynamically set Menu region connection based on options
    start_region = START_OPTION_MAP[context.start_location][0]
    regions[AVRegions.MENU].connect(regions[start_region])

    for data in location_data:
        region = regions[data.region_name]
        location = AVLocation(context.player, data.name, data.id, region)
        location.access_rule = lambda state, data=data: data.access_rule(state, context)
        region.locations.append(location)

    # Always place Vision Defeated item, regardless of goal
    vision = AVLocation(context.player, 'Vision', None, regions[AVRegions.VISION])
    vision.place_locked_item(AVItem("Vision Defeated", ItemClassification.progression, None, context.player))
    regions[AVRegions.VISION].locations.append(vision)

    # TODO: Other goals
    athetos = AVLocation(context.player, 'Athetos', None, regions[AVRegions.ATHETOS])
    athetos.place_locked_item(AVItem("Athetos Defeated", ItemClassification.progression, None, context.player))
    regions[AVRegions.ATHETOS].locations.append(athetos)
