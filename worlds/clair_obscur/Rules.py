from BaseClasses import Region
from worlds.clair_obscur.Data import data
from worlds.generic.Rules import add_rule

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
    add_rule(major_connection_2, lambda state, pl=player: state.has_group("Area", pl, 4))

    if world.options.char_shuffle:
        add_rule(major_connection_1, lambda state, pl=player: state.has_group("Character", pl, 1))
        add_rule(major_connection_2, lambda state, pl=player: state.has_group("Character", pl, 2))

    #Lost Gestral access
    if world.options.gestral_shuffle:
        gestral_rewards_locations = ["Lost Gestral reward 1",
                                     "Lost Gestral reward 2",
                                     "Lost Gestral reward 3",
                                     "Lost Gestral reward 4",
                                     "Lost Gestral reward 5",
                                     "Lost Gestral reward 6",
                                     "Lost Gestral reward 7",
                                     "Lost Gestral reward 8",
                                     "Lost Gestral reward 9"]
        for i in range(0, 9):
            loc = mw.get_location(gestral_rewards_locations[i], player)
            add_rule(loc, lambda state, pl=player, x=i: state.has("Lost Gestral", pl, x + 1))

    else:
        #2 gestrals in First Continent North
        add_rule(mw.get_location("Lost Gestral reward 1", player),
                 lambda state: state.can_reach_region("WM: First Continent North", player))
        add_rule(mw.get_location("Lost Gestral reward 2", player),
                 lambda state: state.can_reach_region("WM: First Continent North", player))

        #1 gestral in South Sea
        add_rule(mw.get_location("Lost Gestral reward 3", player),
                 lambda state: state.can_reach_region("WM: South Sea", player))

        #1 in Second Continent South
        add_rule(mw.get_location("Lost Gestral reward 4", player),
                 lambda state: state.can_reach_region("WM: Second Continent South", player))

        #2 in North Sea
        add_rule(mw.get_location("Lost Gestral reward 5", player),
                 lambda state: state.can_reach_region("WM: First Continent North", player))
        add_rule(mw.get_location("Lost Gestral reward 6", player),
                 lambda state: state.can_reach_region("WM: First Continent North", player))

        #3 in Sky
        add_rule(mw.get_location("Lost Gestral reward 7", player),
                 lambda state: state.can_reach_region("WM: Sky", player))
        add_rule(mw.get_location("Lost Gestral reward 8", player),
                 lambda state: state.can_reach_region("WM: Sky", player))
        add_rule(mw.get_location("Lost Gestral reward 9", player),
                 lambda state: state.can_reach_region("WM: Sky", player))
