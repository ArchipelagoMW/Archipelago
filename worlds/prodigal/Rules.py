from BaseClasses import CollectionState

def prodigal_can_hit(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.has("Progressive Pick", world.player) or state.has("Progressive Knuckle", world.player)

def prodigal_can_hit_fire(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.has("Progressive Pick", world.player) or state.has("Progressive Knuckle", world.player, 2)

def prodigal_can_reach_zaegul(state: CollectionState, world: "ProdigalWorld") -> bool:
    return (state.has("Progressive Pick", world.player) or prodigal_can_long_jump(state, world) or
            ((state.has("Progressive Knuckle", world.player, 2) or prodigal_skips(state, world)) and
            state.has("Lariat", world.player))) and \
            state.has("Harmonica", world.player) and state.can_reach("Tidal Mines", "Region", world.player)

def prodigal_has_key(state: CollectionState, world: "ProdigalWorld", region: str, count: int) -> bool:
    return state.has(f"Key ({region})", world.player, count) if world.options.specific_keys \
            else prodigal_can_reach_zaegul(state, world)

def prodigal_has_ice_key(state: CollectionState, world: "ProdigalWorld") -> bool:
    return prodigal_can_reach_zaegul(state, world)

def prodigal_skips(state: CollectionState, world: "ProdigalWorld") -> bool:
    return world.options.skips_in_logic

def prodigal_can_long_jump(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.has("Progressive Knuckle", world.player, 2) and prodigal_skips(state, world)

def prodigal_can_remove_boulders(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.has("Progressive Knuckle", world.player) or \
            (state.has("Progressive Hand", world.player, 2) and prodigal_skips(state, world))

def prodigal_has_cleats(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.has("Cleated Boots", world.player) or state.has("Boots of Graile", world.player)

def prodigal_has_crest(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.has("Crest Fragment", world.player, world.options.crest_fragments_required)

def prodigal_time_out_1_open(state: CollectionState, world: "ProdigalWorld") -> bool:
    return prodigal_has_colors(state, world, 2)

def prodigal_time_out_2_open(state: CollectionState, world: "ProdigalWorld") -> bool:
    return prodigal_has_colors(state, world, 2)

def prodigal_has_enough_coins(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.has("Coin of Crowl", world.player, world.options.coins_of_crowl_required)

def prodigal_has_enough_blessings(state: CollectionState, world: "ProdigalWorld") -> bool:
    return prodigal_has_blessings(state, world, world.options.blessings_required)

def prodigal_has_colors(state: CollectionState, world: "ProdigalWorld", count: int) -> bool:
    return state.count("Shattered Soul", world.player) + state.count("Fury Heart", world.player) + \
            state.count("Frozen Heart", world.player) + state.count("Red Crystal", world.player) + \
            state.count("Sunset Painting", world.player) >= count

def prodigal_has_blessings(state: CollectionState, world: "ProdigalWorld", count: int) -> bool:
    return state.count("Life Blessing", world.player) + state.count("Light Blessing", world.player) + \
            state.count("Storm Blessing", world.player) + state.count("Earth Blessing", world.player) + \
            state.count("Water Blessing", world.player) >= count

def prodigal_can_kill_grelins(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.can_reach("Waterfall Cave - Item", "Location", world.player) or \
            state.can_reach("Magma Heart - Main Room Left Chest", "Location", world.player)

def prodigal_has_tar(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.can_reach("Crocasino - Hidden Chest", "Location", world.player)

def prodigal_can_enter_tidal_mines(state: CollectionState, world: "ProdigalWorld") -> bool:
    return state.has_any({"Progressive Hand", "Lariat"}, world.player) and \
            (state.has("Progressive Pick", world.player) or (state.has("Lariat", world.player) and
            (state.has("Progressive Knuckle", world.player, 2) or prodigal_skips(state, world))) or
            prodigal_can_long_jump(state, world))

def prodigal_can_enter_east_crystal_caves(state: CollectionState, world: "ProdigalWorld") -> bool:
    return (state.has("Progressive Knuckle", world.player, 2) or state.has("Lariat", world.player)) and \
            (prodigal_can_long_jump(state, world) or (state.has("Progressive Pick", world.player) and
            (prodigal_skips(state, world) or state.has("Lariat", world.player) or \
            prodigal_has_cleats(state, world))))

def prodigal_can_enter_northeast_crystal_caves(state: CollectionState, world: "ProdigalWorld") -> bool:
    return prodigal_can_enter_east_crystal_caves(state, world) and \
            state.has("Progressive Knuckle", world.player, 2) and \
            (state.has("Progressive Pick", world.player) or state.has("Lariat", world.player) or \
            prodigal_can_long_jump(state, world)) and prodigal_has_key(state, world, "Crystal Caves", 2)
