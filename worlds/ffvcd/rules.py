from worlds.generic.Rules import add_rule, set_rule, forbid_item

def set_rules(ffvcdworld):
    multiworld = ffvcdworld.multiworld
    player = ffvcdworld.player
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
    
    # set_rule(multiworld.get_location("Kelb - CornaJar at Kelb (CornaJar)", ffvcdworld.player),
    #       lambda state: state.has("Catch Ability", ffvcdworld.player) or
    #                     state.has("Trainer Crystal", ffvcdworld.player))
    
