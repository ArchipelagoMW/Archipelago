from BaseClasses import CollectionState, MultiWorld
from .Options import FountainDoorRequirement, SpendingRestrictions


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
    return all([
        state.has("Defeat Khidr", player) or state.has("Defeat Neo Khidr", player),
        has_upgrades_percentage(state, player, 30),
    ])


def has_defeated_forest(state: CollectionState, player: int) -> bool:
    return all([
        state.has("Defeat Alexander", player) or state.has("Defeat Alexander IV", player),
        has_upgrades_percentage(state, player, 45),
    ])


def has_defeated_tower(state: CollectionState, player: int) -> bool:
    return all([
        state.has("Defeat Ponce de Leon", player) or state.has("Defeat Ponce de Freon", player),
        has_upgrades_percentage(state, player, 60),
    ])


def has_defeated_dungeon(state: CollectionState, player: int) -> bool:
    return all([
        state.has("Defeat Herodotus", player) or state.has("Defeat Astrodotus", player),
        has_upgrades_percentage(state, player, 75),
    ])


def has_defeated_all_bosses(state: CollectionState, player: int) -> bool:
    return all([
        has_defeated_castle(state, player),
        has_defeated_forest(state, player),
        has_defeated_tower(state, player),
        has_defeated_dungeon(state, player),
    ])


def can_open_door(state: CollectionState, player: int) -> bool:
    objective: FountainDoorRequirement = getattr(state.multiworld, "fountain_door_requirement")[player]
    fountain_piece_requirement: int = state.multiworld.worlds[player].fountain_piece_requirement

    if objective == "bosses":
        return has_defeated_all_bosses(state, player)
    elif objective == "fountain_pieces":
        return state.has("Piece of the Fountain", player, fountain_piece_requirement)
    else:
        return all([
            has_defeated_all_bosses(state, player),
            state.has("Piece of the Fountain", player, fountain_piece_requirement),
        ])


def can_access_secret_room(state: CollectionState, player: int) -> bool:
    return all([
        state.has("Calypso's Compass Shrine", player),
        has_defeated_tower(state, player),
    ])


def can_cheat_cheapskate_elf(state: CollectionState, player: int) -> bool:
    return state.has("Nerdy Glasses Shrine", player)


def can_afford_tier2(state: CollectionState, player: int) -> bool:
    restrictions: SpendingRestrictions = getattr(state.multiworld, "spending_restrictions")[player]
    if not has_defeated_castle(state, player):
        return False

    if restrictions:
        return state.has("Progressive Spending", player)

    return True


def can_afford_tier3(state: CollectionState, player: int) -> bool:
    restrictions: SpendingRestrictions = getattr(state.multiworld, "spending_restrictions")[player]
    if not has_defeated_forest(state, player):
        return False

    if restrictions:
        return state.has("Progressive Spending", player, 2)

    return True


def can_afford_tier4(state: CollectionState, player: int) -> bool:
    restrictions: SpendingRestrictions = getattr(state.multiworld, "spending_restrictions")[player]
    if not has_defeated_tower(state, player):
        return False

    if restrictions:
        return state.has("Progressive Spending", player, 3)

    return True
