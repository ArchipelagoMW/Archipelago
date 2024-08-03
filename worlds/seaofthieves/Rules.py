import random

from worlds.seaofthieves.Items.Items import Items

from .Configurations import SotOptionsDerived
from BaseClasses import MultiWorld
from .Regions.Regions import Regions, RegionAdder
from .Regions.RegionConnectionRules import create_rules


def set_rules(world: MultiWorld, options: SotOptionsDerived.SotOptionsDerived, player: int, regionAdder: RegionAdder):
    # Make Region Connection Rules
    rules = create_rules(options, world)
    for rule in rules:
        regionAdder.connectFromDetails2(world, rule)

    # Make Location Rules
    regionAdder.addRulesForLocationsInRegions(world)

    # Make Win Condition Rules
    world.completion_condition[player] = lambda state: state.has(Items.pirate_legend.name, player)
    return rules
