from ..generic.Rules import set_rule, add_rule
from ..AutoWorld import World
from .GeneratedRules import set_generated_rules
from typing import NamedTuple


class CostTerm(NamedTuple):
    term: str
    option: str
    singular: str
    plural: str
    weight: int  # CostSanity
    sort: int


cost_terms = {x.term: x for x in (
    CostTerm("RANCIDEGGS", "Egg", "Rancid Egg", "Rancid Eggs", 1, 3),
    CostTerm("GRUBS", "Grub", "Grub", "Grubs", 1, 2),
    CostTerm("ESSENCE", "Essence", "Essence", "Essence", 1, 4),
    CostTerm("CHARMS", "Charm", "Charm", "Charms", 1, 1),
    CostTerm("GEO", "Geo", "Geo", "Geo", 8, 9999),
)}


def hk_set_rule(hk_world: World, location: str, rule):
    player = hk_world.player

    locations = hk_world.created_multi_locations.get(location)
    if locations is None:
        try:
            locations = [hk_world.multiworld.get_location(location, player)]
        except KeyError:
            return

    for location in locations:
        set_rule(location, rule)


def set_rules(hk_world: World):
    player = hk_world.player
    set_generated_rules(hk_world, hk_set_rule)

    # Shop costs
    for location in hk_world.multiworld.get_locations(player):
        if location.costs:
            for term, amount in location.costs.items():
                if term == "GEO":  # No geo logic!
                    continue
                add_rule(location, lambda state, term=term, amount=amount: state.count(term, player) >= amount)
