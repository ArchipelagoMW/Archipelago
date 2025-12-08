from __future__ import annotations
from math import floor
from ..generic.Rules import set_rule
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

    world.get_region(RID.HOME).connect(connecting_region=world.get_region(RID.SUNNY))
    world.get_region(RID.HOME).connect(connecting_region=world.get_region(RID.RAINY))
    world.get_region(RID.HOME).connect(connecting_region=world.get_region(RID.SNOWY), rule=lambda state: state.has(ITEM.BOOTS, player))

    locs_list: typing.Iterable[BKSim_Location] = typing.cast(typing.Iterable[BKSim_Location], multiworld.get_locations(player))
    loc_count = options.locs_per_weather.value
    max_rules = []
    for loc in locs_list:
        if loc.info.region_id == RID.SUNNY:
            if loc.info.index == 0:
                continue
            tmp_rule = lambda state, idx=loc.info.index: state.has(ITEM.SHOES, player, floor(idx / 2))
            if loc.info.index == loc_count - 1:
                max_rules.append(tmp_rule)
            set_rule(loc, tmp_rule)
        elif loc.info.region_id == RID.RAINY:
            tmp_rule = lambda state, idx=loc.info.index: (state.has(ITEM.SHOES, player, floor(idx / 2) + 1) and state.has(
                ITEM.NEWLOC, player)) or state.has(ITEM.SHOES, player, idx)
            if loc.info.index == loc_count - 1:
                max_rules.append(tmp_rule)
            set_rule(loc, tmp_rule)
        elif loc.info.region_id == RID.SNOWY:
            tmp_rule = lambda state, idx=loc.info.index: state.has(ITEM.BOOTS, player, floor(idx / 2) + 1)
            if loc.info.index == loc_count - 1:
                max_rules.append(tmp_rule)
            set_rule(loc, tmp_rule)

    multiworld.completion_condition[player] = lambda state: all(rule(state) for rule in max_rules)
