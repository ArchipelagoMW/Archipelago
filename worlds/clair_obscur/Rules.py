from BaseClasses import Region
from worlds.clair_obscur.Data import data
from worlds.generic.Rules import set_rule, add_rule

def set_rules(world):
    player = world.player
    world = world.multiworld

    goal = 1
    goal_loc = ""
    match goal:
        case 0:
            goal_loc = "The Monolith: The Paintress"
        case 1:
            goal_loc = "Lumiere: The Curator"
        case 2:
            goal_loc = "Endless Tower: Stage 11-3"
        case 3:
            goal_loc = "The Abyss: Simon"

    world.completion_condition[player] = (
        lambda state: state.can_reach_location(goal_loc, player)
    )

    #connection access: direct area tickets

    #paint break reqs

    #broad transition reqs: FCS -> SS, SS -> NS
    #   % of area tickets based on settings, character reqs

    #lost gestrals

