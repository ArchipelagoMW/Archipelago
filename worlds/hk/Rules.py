from ..generic.Rules import set_rule, add_rule
from ..AutoWorld import World
from .GeneratedRules import set_generated_rules
from .GodhomeData import set_godhome_rules
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
    set_godhome_rules(hk_world, hk_set_rule)

    # Shop costs
    for location in hk_world.multiworld.get_locations(player):
        if location.costs:
            for term, amount in location.costs.items():
                if term == "GEO":  # No geo logic!
                    continue
                add_rule(location, lambda state, term=term, amount=amount: state.count(term, player) >= amount)


def _hk_nail_combat(state, player) -> bool:
    return state.has_any({'LEFTSLASH', 'RIGHTSLASH', 'UPSLASH'}, player)


def _hk_can_beat_thk(state, player) -> bool:
    return (
        state.has('Opened_Black_Egg_Temple', player)
        and (state.count('FIREBALL', player) + state.count('SCREAM', player) + state.count('QUAKE', player)) > 1
        and _hk_nail_combat(state, player)
        and (
            state.has_any({'LEFTDASH', 'RIGHTDASH'}, player)
            or state._hk_option(player, 'ProficientCombat')
        )
        and state.has('FOCUS', player)
    )


def _hk_siblings_ending(state, player) -> bool:
    return _hk_can_beat_thk(state, player) and state.has('WHITEFRAGMENT', player, 3)


def _hk_can_beat_radiance(state, player) -> bool:
    return (
        state.has('Opened_Black_Egg_Temple', player)
        and _hk_nail_combat(state, player)
        and state.has('WHITEFRAGMENT', player, 3)
        and state.has('DREAMNAIL', player)
        and (
            (state.has('LEFTCLAW', player) and state.has('RIGHTCLAW', player))
            or state.has('WINGS', player)
        )
        and (state.count('FIREBALL', player) + state.count('SCREAM', player) + state.count('QUAKE', player)) > 1
        and (
            (state.has('LEFTDASH', player, 2) and state.has('RIGHTDASH', player, 2))  # Both Shade Cloaks
            or (state._hk_option(player, 'ProficientCombat') and state.has('QUAKE', player))  # or Dive
        )
    )
