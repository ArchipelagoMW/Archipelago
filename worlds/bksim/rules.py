from __future__ import annotations
from math import floor
from rule_builder.rules import Has, True_
from .common import *
from .locations import BKSim_Location
import typing
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import BKSimWorld


def set_rules(world: BKSimWorld) -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    world.create_entrance(world.get_region(RID.HOME), world.get_region(RID.SUNNY))
    world.create_entrance(world.get_region(RID.HOME), world.get_region(RID.RAINY))
    world.create_entrance(world.get_region(RID.HOME), world.get_region(RID.SNOWY), Has(ITEM.BOOTS))

    locs_list: typing.Iterable[BKSim_Location] = typing.cast(typing.Iterable[BKSim_Location], multiworld.get_locations(player))
    loc_count = options.locs_per_weather.value
    max_rule = True_()
    for loc in locs_list:
        if loc.info.region_id == RID.SUNNY:
            if loc.info.index == 0:
                continue
            tmp_rule = Has(ITEM.SHOES, floor(loc.info.index / 2))
            if loc.info.index == loc_count - 1:  # Append the strictest requirement to a 'max rule'
                max_rule &= tmp_rule
            world.set_rule(loc, tmp_rule)
        elif loc.info.region_id == RID.RAINY:
            tmp_rule = Has(ITEM.SHOES, loc.info.index) | (Has(ITEM.NEWLOC) & Has(ITEM.SHOES, floor(loc.info.index / 2) + 1))
            if loc.info.index == loc_count - 1:  # Append the strictest requirement to a 'max rule'
                max_rule &= tmp_rule
            world.set_rule(loc, tmp_rule)
        elif loc.info.region_id == RID.SNOWY:
            tmp_rule = Has(ITEM.BOOTS, floor(loc.info.index / 2) + 1)
            if loc.info.index == loc_count - 1:  # Append the strictest requirement to a 'max rule'
                max_rule &= tmp_rule
            world.set_rule(loc, tmp_rule)

    world.set_completion_rule(max_rule)  # Require all the strictest requirements, as goal requires completing all locations.
