from BaseClasses import Region
from worlds.clair_obscur.Data import data
from worlds.generic.Rules import set_rule, add_rule

def set_rules(world):
    player = world.player
    mw = world.multiworld

    goal = world.options.goal
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

    mw.completion_condition[player] = (
        lambda state: state.can_reach_location(goal_loc, player)
    )

    #Major map connections- the playthrough will always go through these.
    major_connection_1 = mw.get_entrance("WM: First Continent South -> WM: South Sea", player)
    major_connection_2 = mw.get_entrance("WM: South Sea -> WM: North Sea", player)

    #paint break reqs

    #broad transition reqs: FCS -> SS, SS -> NS
    #   % of area tickets based on settings, character reqs
    #   area tickets need to be in distinct groups for major areas in each section of the game; giving the player
    #   Flying Manor won't ensure they have the level range to do Visages for instance
    add_rule(major_connection_1, lambda state, pl=player: state.has_group("Area", pl, 2))
    add_rule(major_connection_1, lambda state, pl=player: state.has_group("Character", pl, 1))

    add_rule(major_connection_2, lambda state, pl=player: state.has_group("Area", pl, 4))
    add_rule(major_connection_2, lambda state, pl=player: state.has_group("Character", pl, 2))

    #lost gestrals

