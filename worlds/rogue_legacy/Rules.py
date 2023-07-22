from BaseClasses import CollectionState, MultiWorld
from worlds.rogue_legacy.Options import FountainDoorRequirement, FountainPiecesAvailable, FountainPiecesRequired


def get_total_upgrades(multiworld: MultiWorld, player: int) -> int:
    return getattr(multiworld, "health_pool")[player].value + \
           getattr(multiworld, "mana_pool")[player].value + \
           getattr(multiworld, "attack_pool")[player].value + \
           getattr(multiworld, "magic_damage_pool")[player].value


def get_upgrade_count(state: CollectionState, player: int) -> int:
    return state.item_count("Health Up", player) + state.item_count("Mana Up", player) + \
           state.item_count("Attack Up", player) + state.item_count("Magic Damage Up", player)


def has_upgrade_amount(state: CollectionState, player: int, amount: int) -> bool:
    return get_upgrade_count(state, player) >= amount


def has_upgrades_percentage(state: CollectionState, player: int, percentage: float) -> bool:
    return has_upgrade_amount(state, player, round(get_total_upgrades(state.multiworld, player) * (percentage / 100)))


def has_movement_rune(state: CollectionState, player: int) -> bool:
    return state.has("Vault Runes", player) or state.has("Sprint Runes", player) or state.has("Sky Runes", player)


def has_enchantress_pieces(state: CollectionState, player: int) -> bool:
    return any([
        state.has("Enchantress - Sword", player),
        state.has("Enchantress - Helm", player),
        state.has("Enchantress - Chest", player),
        state.has("Enchantress - Limbs", player),
        state.has("Enchantress - Cape", player),
    ])


def has_fairy_progression(state: CollectionState, player: int) -> bool:
    return state.has("Dragons", player) or (has_enchantress_pieces(state, player) and has_movement_rune(state, player))


def has_defeated_castle(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Khidr", player) or state.has("Defeat Neo Khidr", player)


def has_defeated_forest(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Alexander", player) or state.has("Defeat Alexander IV", player)


def has_defeated_tower(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Ponce de Leon", player) or state.has("Defeat Ponce de Freon", player)


def has_defeated_dungeon(state: CollectionState, player: int) -> bool:
    return state.has("Defeat Herodotus", player) or state.has("Defeat Astrodotus", player)


def has_defeated_all_bosses(state: CollectionState, player: int) -> bool:
    return all([
        has_defeated_castle(state, player),
        has_defeated_forest(state, player),
        has_defeated_tower(state, player),
        has_defeated_dungeon(state, player),
    ])


def can_open_door(state: CollectionState, player: int) -> bool:
    objective: FountainDoorRequirement = getattr(state.multiworld, "fountain_door_requirement")[player]
    available: FountainPiecesAvailable = getattr(state.multiworld, "fountain_pieces_available")[player].value
    percentage: FountainPiecesRequired = getattr(state.multiworld, "fountain_pieces_percentage")[player].value
    fountain_pieces_requirement = round(max(available * (percentage / 100), 1))

    if objective == "bosses":
        return has_defeated_all_bosses(state, player)
    elif objective == "fountain_pieces":
        return state.has("Piece of the Fountain", player, fountain_pieces_requirement)
    else:
        return all([
            has_defeated_all_bosses(state, player),
            state.has("Piece of the Fountain", player, fountain_pieces_requirement),
        ])
