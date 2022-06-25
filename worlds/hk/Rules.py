from ..generic.Rules import set_rule, add_rule
from BaseClasses import MultiWorld
from ..AutoWorld import World
from .GeneratedRules import set_generated_rules
from typing import NamedTuple


class CostTerm(NamedTuple):
    term: str
    option: str
    singular: str
    plural: str


cost_terms = {x.term: x for x in (
    CostTerm("RANCIDEGGS", "Egg", "Rancid Egg", "Rancid Eggs"),
    CostTerm("GRUBS", "Grub", "Grub", "Grubs"),
    CostTerm("ESSENCE", "Essence", "Essence", "Essence"),
    CostTerm("CHARMS", "Charm", "Charm", "Charms"),
    CostTerm("GEO", "Geo", "Geo", "Geo"),
)}


def hk_set_rule(hk_world: World, location: str, rule):
    count = hk_world.created_multi_locations[location]
    player = hk_world.player
    if count:
        locations = [f"{location}_{x}" for x in range(1, count+1)]
    elif (location, hk_world.player) in hk_world.world._location_cache:
        locations = [location]
    else:
        return
    for location in locations:
        set_rule(hk_world.world.get_location(location, player), rule)


def set_rules(hk_world: World):
    player = hk_world.player
    world = hk_world.world
    set_generated_rules(hk_world, hk_set_rule)

    # Shop costs
    for region in world.get_regions(player):
        for location in region.locations:
            if location.costs:
                for term, amount in location.costs.items():
                    if term == "GEO":  # No geo logic!
                        continue
                    add_rule(location, lambda state, term=term, amount=amount: state.count(term, player) >= amount)
