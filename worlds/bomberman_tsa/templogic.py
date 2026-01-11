def has_all_elements(state,player): # Debug, checks to see if you have all the element stones
    return (state.has("Fire Stone",player) and state.has("Ice Stone",player) and state.has("Wind Stone",player) and state.has("Earth Stone",player)
                    and state.has("Lightning Stone",player) and state.has("Dark Stone",player) and state.has("Light Stone",player) )

def can_destroy_with_immunity(state, player, immunities):
    stones = ["Fire Stone","Ice Stone","Wind Stone","Earth Stone","Lightning Stone","Dark Stone","Light Stone"]
    for badstone in immunities:
        stones.pop(stones.index(badstone))
    for havestone in stones:
        if state.has(havestone, player):
            return True
    return False

def can_open_car(state, player):
    return lambda state: state.has("Guardian Glove", player) or state.has("Earth Stone", player)

def has_all_guardian(state, player): # Debug, checks to see if you have all the guardian armor
    return state.has("Guardian Glove", player) and state.has("Guardian Helmet", player) and state.has("Guardian Boots", player)

def can_build_ice(state, player):
    return state.has("Ice Stone",player) and can_move_bombs(state,player) 

def has_multibomb(state, player): # has a bomb that can place more than 1 of itself
    return state.has("Fire Stone",player) or state.has("Ice Stone",player) or state.has("Wind Stone",player) or state.has("Lightning Stone",player)

def can_destroy(state,player):
    return state.has("Fire Stone",player) or state.has("Electric Stone",player) or state.has("Ice Stone",player) or state.has("Earth Stone", player)

def can_bomb_jump(state,player): # Depreciated? 
    return (state.has("Fire Stone",player) or state.has("Electric Stone",player) or state.has("Ice Stone",player) or state.has("Wind Stone", player)) and state.has("BombUp", player, 2)

def can_hit_high_object(state,player):
    return state.has("Guardian Glove", player) or (state.has("Ice Stone",player) and state.has("FireUp", player, 2)) or state.has("Dark Stone", player) or state.has("Light Stone", player)

def can_hit_fountain(state, player):
    return state.has("Ice Stone", player) and (state.has("Guardian Glove", player) or state.has("FireUp", player, 2))

def can_build_ladder(state,player,bombcnt):
    return state.has("Guardian Glove", player) and state.has("Guardian Helmet", player) and (((state.has("Fire Stone", player) or state.has("Lightning Stone", player)) and state.has("BombUp", player, bombcnt)) or (has_multibomb(state, player) and state.has("BombUp", player, (bombcnt+1))))

def can_move_bombs(state,player): # Can kick or throw
    return state.has("Guardian Glove", player) or state.has("Guardian Boots", player)

def tempfunc(player):
    return {



    }