from __future__ import annotations

import typing as t
from BaseClasses import ItemClassification, Location, MultiWorld, Region

from . import conditions
from .boss_data import BOSS_DATA
from .constants import AVRegion, AVGlitchRegion, START_OPTION_MAP
from .creature_data import creature_data
from .location_data import entrance_data, location_data
from .items import AVItem

if t.TYPE_CHECKING:
    from .types import AccessRule, LogicContext


class AVLocation(Location):
    game = "Axiom Verge"


def create_regions(context: LogicContext, multiworld: MultiWorld):
    for enum_type in AVRegion:
        region_name = enum_type.value
        region = Region(region_name, context.player, multiworld)
        multiworld.regions.append(region)

    for source_name, dest_name, condition_func, bidirectional, *name in entrance_data:
        source, destination = multiworld.get_region(source_name, context.player), multiworld.get_region(dest_name, context.player)
        access_rule = lambda state, func=condition_func: func(state, context)

        if name:
            source.connect(destination, name[0], rule=access_rule)
        else:
            source.connect(destination, rule=access_rule)

        if bidirectional:
            destination.connect(source, rule=access_rule)

    # Dynamically set Menu region connection based on options
    start_region = START_OPTION_MAP[context.start_location]
    multiworld.get_region(AVRegion.MENU, context.player).connect(multiworld.get_region(start_region, context.player))

    for data in location_data:
        region = multiworld.get_region(data.region_name, context.player)
        location = AVLocation(context.player, data.name, data.id, region)
        location.access_rule = lambda state, data=data: data.access_rule(state, context)
        region.locations.append(location)

    # TODO: Other goals. Maybe a better access rule
    create_boss_item(context, multiworld, "Athetos", AVRegion.ATHETOS, lambda s, c=context: conditions.always_accessible(s, c))


def create_glitchsanity_regions(context: LogicContext, multiworld: MultiWorld):
    # Create some shared regions ahead of the loop
    swarmily = Region(AVGlitchRegion.SWARMILY, context.player, multiworld)
    multiworld.get_region(AVRegion.EAST_ABSU, context.player).connect(swarmily, rule=lambda s, c=context: conditions.has_red_coat(s, c) or conditions.has_glitch_2(s, c))
    multiworld.get_region(AVRegion.UPPER_ERIBU, context.player).connect(swarmily, rule=lambda s, c=context: conditions.bubble_jail_trace_access(s, c))
    multiworld.regions.append(swarmily)

    spitbug = Region(AVGlitchRegion.SPITBUG, context.player, multiworld)
    multiworld.get_region(AVRegion.EAST_ABSU, context.player).connect(spitbug)
    multiworld.get_region(AVRegion.UPPER_ERIBU, context.player).connect(spitbug)
    multiworld.regions.append(spitbug)

    mogra = Region(AVGlitchRegion.MOGRA, context.player, multiworld)
    multiworld.get_region(AVRegion.MOUNTAIN_TOP, context.player).connect(mogra)
    multiworld.get_region(AVRegion.GRAPPLE_CLIFFS, context.player).connect(mogra)
    multiworld.regions.append(mogra)

    for data in creature_data:
        if data.parent_region is not None:
            # Single-region enemy. Just place their item in the region
            region = multiworld.get_region(data.parent_region, context.player)
            location = AVLocation(context.player, data.name, data.id, region)
            location.access_rule = lambda s, data=data: data.glitch_level(s, context)
            region.locations.append(location)
            continue

        # Multi-region enemy. Create a microregion for it, and connect all provided regions to it.
        enemy_region = Region(data.enemy, context.player, multiworld)
        location = AVLocation(context.player, data.name, data.id, enemy_region)
        location.access_rule = lambda s, data=data: data.glitch_level(s, context)
        enemy_region.locations.append(location)
        multiworld.regions.append(enemy_region)
        for region_name, condition_func in data.entrances:
            region = multiworld.get_region(region_name, context.player)
            access_rule = lambda state, func=condition_func: func(state, context)
            region.connect(enemy_region, rule=access_rule)


def create_boss_item(context: LogicContext, multiworld: MultiWorld, boss_name: str, boss_region_name: str, boss_access_rule: AccessRule):
    boss_region = multiworld.get_region(boss_region_name, context.player)
    boss_location = AVLocation(context.player, boss_name, None, boss_region)
    boss_location.place_locked_item(AVItem(f"{boss_name} Defeated", ItemClassification.progression, None, context.player))
    boss_location.access_rule = lambda s, c=context: boss_access_rule(s, c)
    boss_region.locations.append(boss_location)


def create_boss_items(context: LogicContext, multiworld: MultiWorld):
    for name, region, access_rule in BOSS_DATA:
        create_boss_item(context, multiworld, name, region, access_rule)
