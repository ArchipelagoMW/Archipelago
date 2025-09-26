from BaseClasses import Region
from worlds.clair_obscur.Data import data
from worlds.generic.Rules import add_rule

def set_rules(world):
    player = world.player
    mw = world.multiworld

    goal = world.options.goal
    goal_reg = ""
    match goal:
        case 0:
            goal_reg = "The Monolith"
        case 1:
            goal_reg = "Lumiere"
        case 2:
            goal_reg = "Endless Tower Stage 11"
        case 3:
            goal_reg = "Renoir's Drafts"

    mw.completion_condition[player] = (
        lambda state: state.can_reach_region(goal_reg, player)
    )

    #Major map connections- the playthrough will always go through these.
    major_connection_1 = mw.get_entrance("WM: First Continent South -> WM: South Sea", player)
    major_connection_2 = mw.get_entrance("WM: South Sea -> WM: North Sea", player)
    major_connections_3 = [mw.get_entrance("WM: North Sea -> The Monolith", player),
                           mw.get_entrance("WM: North Sea -> WM: Sky", player)]

    #broad transition reqs: FCS -> SS, SS -> NS
    #   % of area tickets based on settings, character reqs
    #   area tickets need to be in distinct groups for major areas in each section of the game; giving the player
    #   Flying Manor won't ensure they have the level range to do Visages for instance
    if world.options.area_logic > 0:
        add_rule(major_connection_1, lambda state: state.has_from_list([
            "Area - Flying Waters",
            "Area - Ancient Sanctuary",
            "Area - Yellow Harvest",
            "Area - Stone Wave Cliffs"
        ], player, 4 / world.options.area_logic))
        add_rule(major_connection_2, lambda state: state.has_from_list([
            "Area - Forgotten Battlefield",
            "Area - Old Lumiere"
        ], player, 2 / world.options.area_logic))
        for conn in major_connections_3:
            add_rule(conn, lambda state: state.has_from_list([
                "Area - Visages",
                "Area - Sirene"
            ], player, 2 / world.options.area_logic))

    if world.options.char_shuffle:
        add_rule(major_connection_1, lambda state: state.has_group("Character", player, 1))
        add_rule(major_connection_2, lambda state: state.has_group("Character", player, 2))

    #Lost Gestral access
    # if world.options.gestral_shuffle:
    #     gestral_rewards_locations = ["Lost Gestral reward 1",
    #                                  "Lost Gestral reward 2",
    #                                  "Lost Gestral reward 3",
    #                                  "Lost Gestral reward 4",
    #                                  "Lost Gestral reward 5",
    #                                  "Lost Gestral reward 6",
    #                                  "Lost Gestral reward 7",
    #                                  "Lost Gestral reward 8",
    #                                  "Lost Gestral reward 9"]
    #     for i in range(0, 9):
    #         loc = mw.get_location(gestral_rewards_locations[i], player)
    #         add_rule(loc, lambda state, pl=player, x=i: state.has("Lost Gestral", pl, x + 1))
    #
    # else:
    if not world.options.char_shuffle:
        #2 gestrals in First Continent North
        add_rule(mw.get_location("Lost Gestral reward 1", player),
                 lambda state: state.has_any_count({"Progressive Rock": 2, "Area - Flying Waters": 1}, player))
        add_rule(mw.get_location("Lost Gestral reward 1", player),
                 lambda state: state.has_any_count({"Progressive Rock": 2, "Area - Flying Waters": 1}, player))
        add_rule(mw.get_location("Lost Gestral reward 2", player),
                 lambda state: state.has_any_count({"Progressive Rock": 2, "Area - Flying Waters": 1}, player))

        #1 gestral in South Sea
        add_rule(mw.get_location("Lost Gestral reward 3", player),
                 lambda state: state.has("Progressive Rock", player, 2))

        #1 in Second Continent South
        add_rule(mw.get_location("Lost Gestral reward 4", player),
                 lambda state: (state.has("Progressive Rock", player, 3) or
                                state.has_all_counts({"Progressive Rock": 2, "Area - Forgotten Battlefield": 1},
                                                     player)))

        #2 in North Sea
        add_rule(mw.get_location("Lost Gestral reward 5", player),
                 lambda state: state.has("Progressive Rock", player, 3))
        add_rule(mw.get_location("Lost Gestral reward 6", player),
                 lambda state: state.has("Progressive Rock", player, 3))

        #3 in Sky
        add_rule(mw.get_location("Lost Gestral reward 7", player),
                 lambda state: state.has("Progressive Rock", player, 4))
        add_rule(mw.get_location("Lost Gestral reward 8", player),
                 lambda state: state.has("Progressive Rock", player, 4))
        add_rule(mw.get_location("Lost Gestral reward 9", player),
                 lambda state: state.has("Progressive Rock", player, 4))

    #Character specific access rules- can't be added to conditions due to shuffle char option
    if world.options.char_shuffle:
        add_rule(mw.get_location("Sacred River: Golgra", player),
                 lambda state: state.has("Monoco", player))
        add_rule(mw.get_entrance("WM: Sky -> The Reacher", player),
                 lambda state: state.has("Maelle", player))
        add_rule(mw.get_entrance("WM: Sky -> Sirene's Dress", player),
                 lambda state: state.has("Sciel", player))
        add_rule(mw.get_entrance("WM: Sky -> The Chosen Path", player),
                 lambda state: state.has_group("Character", player, 5))