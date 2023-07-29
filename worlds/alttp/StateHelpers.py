from .SubClasses import LTTPRegion
from BaseClasses import CollectionState


def is_not_bunny(state: CollectionState, region: LTTPRegion, player: int) -> bool:
    if state.has('Moon Pearl', player):
        return True

    return region.is_light_world if state.multiworld.mode[player] != 'inverted' else region.is_dark_world


def can_bomb_clip(state: CollectionState, region: LTTPRegion, player: int) -> bool:
    return is_not_bunny(state, region, player) and state.has('Pegasus Boots', player)


def can_buy_unlimited(state: CollectionState, item: str, player: int) -> bool:
    return any(shop.region.player == player and shop.has_unlimited(item) and shop.region.can_reach(state) for
                shop in state.multiworld.shops)


def can_buy(state: CollectionState, item: str, player: int) -> bool:
    return any(shop.region.player == player and shop.has(item) and shop.region.can_reach(state) for
                shop in state.multiworld.shops)


def can_shoot_arrows(state: CollectionState, player: int) -> bool:
    if state.multiworld.retro_bow[player]:
        return (state.has('Bow', player) or state.has('Silver Bow', player)) and can_buy(state, 'Single Arrow', player)
    return state.has('Bow', player) or state.has('Silver Bow', player)


def has_triforce_pieces(state: CollectionState, player: int) -> bool:
    count = state.multiworld.treasure_hunt_count[player]
    return state.item_count('Triforce Piece', player) + state.item_count('Power Star', player) >= count


def has_crystals(state: CollectionState, count: int, player: int) -> bool:
    found = state.count_group("Crystals", player)
    return found >= count


def can_lift_rocks(state: CollectionState, player: int):
    return state.has('Power Glove', player) or state.has('Titans Mitts', player)


def can_lift_heavy_rocks(state: CollectionState, player: int) -> bool:
    return state.has('Titans Mitts', player)


def bottle_count(state: CollectionState, player: int) -> int:
    return min(state.multiworld.difficulty_requirements[player].progressive_bottle_limit,
                state.count_group("Bottles", player))


def has_hearts(state: CollectionState, player: int, count: int) -> int:
    # Warning: This only considers items that are marked as advancement items
    return heart_count(state, player) >= count


def heart_count(state: CollectionState, player: int) -> int:
    # Warning: This only considers items that are marked as advancement items
    diff = state.multiworld.difficulty_requirements[player]
    return min(state.item_count('Boss Heart Container', player), diff.boss_heart_container_limit) \
            + state.item_count('Sanctuary Heart Container', player) \
            + min(state.item_count('Piece of Heart', player), diff.heart_piece_limit) // 4 \
            + 3  # starting hearts


def can_extend_magic(state: CollectionState, player: int, smallmagic: int = 16,
                        fullrefill: bool = False):  # This reflects the total magic Link has, not the total extra he has.
    basemagic = 8
    if state.has('Magic Upgrade (1/4)', player):
        basemagic = 32
    elif state.has('Magic Upgrade (1/2)', player):
        basemagic = 16
    if can_buy_unlimited(state, 'Green Potion', player) or can_buy_unlimited(state, 'Blue Potion', player):
        if state.multiworld.item_functionality[player] == 'hard' and not fullrefill:
            basemagic = basemagic + int(basemagic * 0.5 * bottle_count(state, player))
        elif state.multiworld.item_functionality[player] == 'expert' and not fullrefill:
            basemagic = basemagic + int(basemagic * 0.25 * bottle_count(state, player))
        else:
            basemagic = basemagic + basemagic * bottle_count(state, player)
    return basemagic >= smallmagic


def can_kill_most_things(state: CollectionState, player: int, enemies: int = 5) -> bool:
    return (has_melee_weapon(state, player)
            or state.has('Cane of Somaria', player)
            or (state.has('Cane of Byrna', player) and (enemies < 6 or can_extend_magic(state, player)))
            or can_shoot_arrows(state, player)
            or state.has('Fire Rod', player)
            or (state.has('Bombs (10)', player) and enemies < 6))


def can_get_good_bee(state: CollectionState, player: int) -> bool:
    cave = state.multiworld.get_region('Good Bee Cave', player)
    return (
            state.has_group("Bottles", player) and
            state.has('Bug Catching Net', player) and
            (state.has('Pegasus Boots', player) or (has_sword(state, player) and state.has('Quake', player))) and
            cave.can_reach(state) and
            is_not_bunny(state, cave, player)
    )


def can_retrieve_tablet(state: CollectionState, player: int) -> bool:
    return state.has('Book of Mudora', player) and (has_beam_sword(state, player) or
                                                    (state.multiworld.swordless[player] and
                                                    state.has("Hammer", player)))


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has('Fighter Sword', player) \
            or state.has('Master Sword', player) \
            or state.has('Tempered Sword', player) \
            or state.has('Golden Sword', player)


def has_beam_sword(state: CollectionState, player: int) -> bool:
    return state.has('Master Sword', player) or state.has('Tempered Sword', player) or state.has('Golden Sword',
                                                                                                player)


def has_melee_weapon(state: CollectionState, player: int) -> bool:
    return has_sword(state, player) or state.has('Hammer', player)


def has_fire_source(state: CollectionState, player: int) -> bool:
    return state.has('Fire Rod', player) or state.has('Lamp', player)


def can_melt_things(state: CollectionState, player: int) -> bool:
    return state.has('Fire Rod', player) or \
            (state.has('Bombos', player) and
            (state.multiworld.swordless[player] or
                has_sword(state, player)))


def has_misery_mire_medallion(state: CollectionState, player: int) -> bool:
    return state.has(state.multiworld.required_medallions[player][0], player)

def has_turtle_rock_medallion(state: CollectionState, player: int) -> bool:
    return state.has(state.multiworld.required_medallions[player][1], player)


def can_boots_clip_lw(state: CollectionState, player: int) -> bool:
    if state.multiworld.mode[player] == 'inverted':
        return state.has('Pegasus Boots', player) and state.has('Moon Pearl', player)
    return state.has('Pegasus Boots', player)


def can_boots_clip_dw(state: CollectionState, player: int) -> bool:
    if state.multiworld.mode[player] != 'inverted':
        return state.has('Pegasus Boots', player) and state.has('Moon Pearl', player)
    return state.has('Pegasus Boots', player)


def can_get_glitched_speed_dw(state: CollectionState, player: int) -> bool:
    rules = [state.has('Pegasus Boots', player), any([state.has('Hookshot', player), has_sword(state, player)])]
    if state.multiworld.mode[player] != 'inverted':
        rules.append(state.has('Moon Pearl', player))
    return all(rules)