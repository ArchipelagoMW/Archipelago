from BaseClasses import CollectionState

#Basic rules
def rule_cartwheel(state : CollectionState, player : int) -> bool:
    return state.has("Cartwheel", player)
def rule_crawl(state : CollectionState, player : int) -> bool:
    return state.has("Crawl", player)
def rule_double_jump(state : CollectionState, player : int) -> bool:
    return state.has("Double Jump", player)
def rule_fist_slam(state : CollectionState, player : int) -> bool:
    return state.has("Fist Slam", player)
def rule_ledge(state : CollectionState, player : int) -> bool:
    return state.has("Ledge Grab", player)
def rule_push(state : CollectionState, player : int) -> bool:
    return state.has("Push", player)
def rule_locate_garib(state : CollectionState, player : int) -> bool:
    return state.has("Locate Garibs", player)
def rule_locate_ball(state : CollectionState, player : int) -> bool:
    return state.has("Locate Ball", player)
def rule_dribble(state : CollectionState, player : int) -> bool:
    return state.has("Dribble", player)
def rule_quick_swap(state : CollectionState, player : int) -> bool:
    return state.has("Quick Swap", player)
def rule_slap(state : CollectionState, player : int) -> bool:
    return state.has("Slap", player)
def rule_throw(state : CollectionState, player : int) -> bool:
    return state.has("Throw", player)
def rule_lob_ball(state : CollectionState, player : int) -> bool:
    return state.has("Ball Toss", player)
def rule_rubber_ball(state : CollectionState, player : int) -> bool:
    return state.has("Rubber Ball", player)
def rule_bowling_ball(state : CollectionState, player : int) -> bool:
    return state.has("Bowling Ball", player)
def rule_ball_bearing(state : CollectionState, player : int) -> bool:
    return state.has("Ball Bearing", player)
def rule_crystal(state : CollectionState, player : int) -> bool:
    return state.has("Crystal", player)
def rule_beachball(state : CollectionState, player : int) -> bool:
    return state.has("Beachball", player)
def rule_death_potion(state : CollectionState, player : int) -> bool:
    return state.has("Death Potion", player)
def rule_helicopter_potion(state : CollectionState, player : int) -> bool:
    return state.has("Helicopter Potion", player)
def rule_frog_potion(state : CollectionState, player : int) -> bool:
    return state.has("Frog Potion", player)
def rule_boomerang_ball(state : CollectionState, player : int) -> bool:
    return state.has("Boomerang Ball", player)
def rule_speed_potion(state : CollectionState, player : int) -> bool:
    return state.has("Speed Potion", player)
def rule_sticky_potion(state : CollectionState, player : int) -> bool:
    return state.has("Sticky Potion", player)
def rule_hercules_potion(state : CollectionState, player : int) -> bool:
    return state.has("Hercules Potion", player)
def rule_jump(state : CollectionState, player : int) -> bool:
    return state.has("Jump", player)
def rule_grab(state : CollectionState, player : int) -> bool:
    return state.has("Grab", player)
def rule_power_ball(state : CollectionState, player : int) -> bool:
    return state.has("Power Ball", player)

#Special rules
def rule_not_crystal(state : CollectionState, player : int) -> bool:
    return state.has("Rubber Ball", player) or state.has("Bowling Ball", player) or state.has("Ball Bearing", player) or state.has("Power Ball", player)
def rule_not_bowling(state : CollectionState, player : int) -> bool:
    return state.has("Rubber Ball", player) or state.has("Ball Bearing", player) or state.has("Crystal", player) or state.has("Power Ball", player)
def rule_not_bowling_or_crystal(state : CollectionState, player : int) -> bool:
    return state.has("Rubber Ball", player) or state.has("Ball Bearing", player) or state.has("Power Ball", player)
def rule_sinks(state : CollectionState, player : int) -> bool:
    return state.has("Bowling Ball", player) or state.has("Ball Bearing", player)
def rule_floats(state : CollectionState, player : int) -> bool:
    return state.has("Rubber Ball", player) or state.has("Crystal", player) or state.has("Power Ball", player)
def rule_ball_up(state : CollectionState, player : int) -> bool:
    return state.has("Throw", player) or state.has("Dribble", player) or state.has("Lob Ball", player)

move_lookup = {
    "Cartwheel" :               rule_cartwheel,
    "Crawl" :                   rule_crawl,
    "Double Jump" :             rule_double_jump,
    "Fist Slam" :               rule_fist_slam,
    "Ledge Grab" :              rule_ledge,
    "Push" :                    rule_push,
    "Locate Garib" :            rule_locate_garib,
    "Locate Ball" :             rule_locate_ball,
    "Dribble" :                 rule_dribble,
    "Quick Swap" :              rule_quick_swap,
    "Slap" :                    rule_slap,
    "Throw" :                   rule_throw,
    "Lob Ball" :                rule_lob_ball,
    "Rubber Ball" :             rule_rubber_ball,
    "Bowling Ball" :            rule_bowling_ball,
    "Ball Bearing" :            rule_ball_bearing,
    "Crystal" :                 rule_crystal,
    "Beachball" :               rule_beachball,
    "Death Potion" :            rule_death_potion,
    "Helicopter Potion" :       rule_helicopter_potion,
    "Frog Potion" :             rule_frog_potion,
    "Boomerang Ball" :          rule_boomerang_ball,
    "Speed Potion" :            rule_speed_potion,
    "Sticky Potion" :           rule_sticky_potion,
    "Hercules Potion" :         rule_hercules_potion,
    "Jump" :                    rule_jump,
    "Not Crystal" :             rule_not_crystal,
    "Not Bowling" :             rule_not_bowling,
    "Sinks" :                   rule_sinks,
    "Floats" :                  rule_floats,
    "Grab" :                    rule_grab,
    "Ball Up" :                 rule_ball_up,
    "Power Ball" :              rule_power_ball,
    "Not Bowling or Crystal" :  rule_not_bowling_or_crystal
}