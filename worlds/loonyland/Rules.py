from typing import Dict

from BaseClasses import CollectionState
from worlds.generic.Rules import add_item_rule, add_rule, CollectionRule


def have_light_source(state: CollectionState, player: int) -> bool:
    return state.has("Lantern", player) or (state.has("Stick", player) and state.has("Boots", player))


def have_bombs(state: CollectionState, player: int) -> bool:
    return state.has("Bombs", player)
    # or werewolf badge when badges are added


def have_all_orbs(state: CollectionState, player: int) -> bool:
    return state.has("Orb", player, 4)


def have_all_bats(state: CollectionState, player: int) -> bool:
    return state.has("Bat Statue", player, 4)


def have_all_vamps(state: CollectionState, player: int) -> bool:
    return state.has("Vamp Statue", player, 8)


def have_special_weapon_damage(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), player)
    )


def have_special_weapon_bullet(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Ice Spear", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), player)
    )


# return lambda state: True slingshot counts

def have_special_weapon_range_damage(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang"), player)
    )
    # return lambda state: True slingshot counts


def have_special_weapon_through_walls(state: CollectionState, player: int) -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Whoopee"), player)
        # state.has("Hot Pants")
    )


def can_cleanse_crypts(state: CollectionState, player: int) -> bool:
    return (have_light_source(state, player) and can_enter_zombiton(state, player) and have_special_weapon_range_damage(
        state, player))


# these will get removed in favor of region access reqs eventually
def can_enter_zombiton(state: CollectionState, player: int) -> bool:
    return state.has("Boots", player)


def can_enter_rocky_cliffs(state: CollectionState, player: int) -> bool:
    return state.has("Big Gem", player)


def can_enter_vampy(state: CollectionState, player: int) -> bool:
    return can_enter_rocky_cliffs(state, player) and have_light_source(state, player)


def can_enter_vampy_ii(state: CollectionState, player: int) -> bool:
    return can_enter_vampy(state, player) and state.has("Skull Key", player)


def can_enter_vampy_iii(state: CollectionState, player: int) -> bool:
    return can_enter_vampy_ii(state, player) and state.has("Bat Key", player)


def can_enter_vampy_iv(state: CollectionState, player: int) -> bool:
    return can_enter_vampy_iii(state, player) and state.has("Pumpkin Key", player)