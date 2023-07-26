from typing import Set

from .RulesData import location_rules
from worlds.generic.Rules import set_rule
from BaseClasses import Location, CollectionState


# TODO: implement Mapstone counting, Open, OpenWorld, connection rules

def oribf_has_all(state: CollectionState, items: Set[str], player:int) -> bool:
    return all(state.prog_items[item, player] if type(item) == str
               else state.prog_items[item[0], player] >= item[1] for item in items)

def set_rules(world):
    temp_base_rule(world.multiworld, world.player)
    for logicset in world.logic_sets:
        apply_or_ruleset(world.multiworld, world.player, logicset)


def tautology(state):
    return True


def add_or_rule_check_first(world, location: str, player: int, conditionsets):
    location = world.get_location(location, player)
    for set in conditionsets:
        if "Free" in set:
            location.access_rule = tautology
            return
    rule = lambda state, conditionsets=conditionsets: any(
        oribf_has_all(state, conditionset, player) for conditionset in conditionsets)
    if location.access_rule is Location.access_rule:
        location.access_rule = rule
    else:
        old_rule = location.access_rule
        location.access_rule = lambda state: rule(state) or old_rule(state)


def temp_base_rule(world, player):
    world.completion_condition[player] = lambda state: oribf_has_all(state,
        {"Bash", "ChargeFlame", "ChargeJump", "Climb", "Dash", "DoubleJump", "Glide", "Grenade", "Stomp", "WallJump"},
        player)


def base_rule(world, player):
    if world.logic[player] != 'nologic':
        # Victory gets placed on Escaped Horu Event
        world.completion_condition[player] = lambda state: state.has('Victory', player)
    # Events
    # Also add: can complete goal
    set_rule(world.get_location("Escaped Horu", player),
             lambda state: state.can_reach("HoruEscapeInnerDoor", player)
                           and state.has_any({"Dash", "Stomp", "ChargeJump", "ChargeFlame"}, player))


def apply_or_ruleset(world, player, rulesetname):
    rules = location_rules[rulesetname]
    for location, conditionsets in rules.items():
        add_or_rule_check_first(world, location, player, conditionsets)
