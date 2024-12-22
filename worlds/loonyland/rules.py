from BaseClasses import CollectionState


def have_light_source(state: CollectionState, player: int) -> bool:
    return state.has("Lantern", player) or (
        state.has("Stick", player) and state.has("Boots", player) and state.can_reach_region("Swamp Gas Cavern", player)
    )
    # 20/20 when badges added


def have_bombs(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player)
    # or werewolf badge when badges are added


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
    return False


def have_39_badges(state: CollectionState, player: int) -> bool:
    return state.has_group("cheats", player, 10)


def have_all_weapons(state: CollectionState, player: int) -> bool:
    return state.has_group("special_weapons", player, 7)
