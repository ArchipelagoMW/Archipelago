
# TODO: typing busted temporarily
def is_not_bunny(state, region: "LTTPRegion", player: int) -> bool:
    if state.has('Moon Pearl', player):
        return True

    return region.is_light_world if state.multiworld.mode[player] != 'inverted' else region.is_dark_world

def can_bomb_clip(state, region: "LTTPRegion", player: int) -> bool:
    return is_not_bunny(state, region, player) and state.has('Pegasus Boots', player)

def can_buy_unlimited(state, item: str, player: int) -> bool:
    return any(shop.region.player == player and shop.has_unlimited(item) and shop.region.can_reach(state) for
                shop in state.multiworld.shops)

def can_buy(state, item: str, player: int) -> bool:
    return any(shop.region.player == player and shop.has(item) and shop.region.can_reach(state) for
                shop in state.multiworld.shops)

def can_shoot_arrows(state, player: int) -> bool:
    if state.multiworld.retro_bow[player]:
        return (state.has('Bow', player) or state.has('Silver Bow', player)) and can_buy(state, 'Single Arrow', player)
    return state.has('Bow', player) or state.has('Silver Bow', player)

def has_triforce_pieces(state, player: int) -> bool:
    count = state.multiworld.treasure_hunt_count[player]
    return state.item_count('Triforce Piece', player) + state.item_count('Power Star', player) >= count

# TODO: we must have some form of item grouping to help with this
def has_crystals(state, count: int, player: int) -> bool:
    found: int = 0
    for crystalnumber in range(1, 8):
        found += state.prog_items[f"Crystal {crystalnumber}", player]
        if found >= count:
            return True
    return False

def can_lift_rocks(state, player: int):
    return state.has('Power Glove', player) or state.has('Titans Mitts', player)