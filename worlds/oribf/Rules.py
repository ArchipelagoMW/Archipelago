from .RulesData import location_rules
from ..generic.Rules import set_rule
from BaseClasses import Location


# TODO: implement Mapstone counting, Open, OpenWorld, connection rules

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
        state._oribf_has_all(conditionset, player) for conditionset in conditionsets)
    if location.access_rule is Location.access_rule:
        location.access_rule = rule
    else:
        old_rule = location.access_rule
        location.access_rule = lambda state: rule(state) or old_rule(state)


def temp_base_rule(world, player):
    world.completion_condition[player] = lambda state: state._oribf_has_all(
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
