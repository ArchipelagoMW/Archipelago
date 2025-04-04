from BaseClasses import CollectionState


def have_light_source(state: CollectionState, player: int) -> bool:
    return state.has("Lantern", player) or state.has("Torch", player) or state.has("20/20 Vision", player)


def can_kill_werewolves(state: CollectionState, player: int) -> bool:
    return state.has("Silver Sling", player) or state.has("Touch Of Death", player)


def have_bombs(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player) or state.has("Combo-Bombo", player) or state.has("Play As Werewolf", player)


def have_many_bombs(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player) or (state.has("Play As Werewolf", player) and state.has("Infinite Gems", player))


def have_special_weapon_damage(state: CollectionState, player: int) -> bool:
    return state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), player)
    # needed for gutsy


def have_special_weapon_bullet(state: CollectionState, player: int) -> bool:
    return True
    # always true as the default character, eventually will be fancier when other starting characters are an option
    # return (
    #    state.has_any(("Bombs", "Ice Spear", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), player)
    # )


def have_special_weapon_range_damage(state: CollectionState, player: int) -> bool:
    return True
    # always true as the default character
    # return (
    #    state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang"), player)
    # )


def have_special_weapon_through_walls(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Whoopee"), player)
        # state.has("Hot Pants") technically possible, but only on diagonals
    )


def can_cleanse_crypts(state: CollectionState, player: int) -> bool:
    return (
        have_light_source(state, player)
        and have_special_weapon_range_damage(state, player)
        and state.can_reach_region("Musty Crypt", player)
        and state.can_reach_region("Dusty Crypt", player)
        and state.can_reach_region("Rusty Crypt", player)
    )


def hundred_percent(state: CollectionState, player: int) -> bool:
    return state.has_group("physical_items", player, 105)


def have_x_badges(state: CollectionState, player: int, count: int) -> bool:
    return state.has("BadgeEarned", player, count)


def have_39_badges(state: CollectionState, player: int) -> bool:
    return state.has("BadgeEarned", player, 39)


def have_all_weapons(state: CollectionState, player: int) -> bool:
    return state.has_group("special_weapons", player, 7)


def can_reach_bats(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("The Shrine Of Bombulus", player)


def can_reach_skeleton(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Halloween Hill", player)


def can_reach_frog(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Halloween Hill", player)


def can_reach_ghost(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Haunted Tower", player)


def can_reach_mummy(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Rocky Cliffs", player)


def can_reach_swampdog(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Halloween Hill", player)


def can_reach_vampire(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Castle Vampy", player)


def can_reach_wolves(state: CollectionState, player: int) -> bool:
    return state.can_reach_region("Halloween Hill", player)


def can_do_collection(state: CollectionState, player: int) -> bool:
    return state.has_group_unique("monster_dolls", player, 8)


def power_level(state: CollectionState, player: int, level_goal: int) -> bool:
    level: int = 0
    level += state.count_group("power", player)
    level += state.count_group("power_big", player) * 5
    level += state.count_group("power_max", player) * 50
    return level > level_goal
