from typing import TYPE_CHECKING

from BaseClasses import CollectionState
if TYPE_CHECKING:
    from worlds.loonyland import LoonylandWorld


def have_light_source(state: CollectionState, world: "LoonylandWorld") -> bool:
    return (
        state.has("Lantern", world.player)
        or (
            state.has("Stick", world.player)
            and state.has("Boots", world.player)
            and state.can_reach_region("Swamp Gas Cavern", world.player)
        )
        or (state.has("20/20 Vision", world.player))
    )
    # 20/20 when badges added


def can_kill_werewolves(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.has("Silver Sling", world.player) or state.has("Touch Of Death", world.player)


def have_bombs(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.has("Bombs", world.player) or state.has("Combo-Bombo", world.player) or state.has("Play As Werewolf", world.player)
    # or werewolf badge when badges are added


def have_many_bombs(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.has("Bombs", world.player) or (state.has("Play As Werewolf", world.player) and state.has("Infinite Gems", world.player))


def have_special_weapon_damage(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), world.player)
    # needed for gutsy


def have_special_weapon_bullet(state: CollectionState, world: "LoonylandWorld") -> bool:
    return True
    # always true as the default character, eventually will be fancier when other starting characters are an option
    # return (
    #    state.has_any(("Bombs", "Ice Spear", "Cactus", "Boomerang", "Whoopee", "Hot Pants"), world.player)
    # )


def have_special_weapon_range_damage(state: CollectionState, world: "LoonylandWorld") -> bool:
    return True
    # always true as the default character
    # return (
    #    state.has_any(("Bombs", "Shock Wand", "Cactus", "Boomerang"), world.player)
    # )


def have_special_weapon_through_walls(state: CollectionState, world: "LoonylandWorld") -> bool:
    return (
        state.has_any(("Bombs", "Shock Wand", "Whoopee"), world.player)
        # state.has("Hot Pants") technically possible, but only on diagonals
    )


def can_cleanse_crypts(state: CollectionState, world: "LoonylandWorld") -> bool:
    return (
        have_light_source(state, world)
        and have_special_weapon_range_damage(state, world)
        and state.can_reach_region("Musty Crypt", world.player)
        and state.can_reach_region("Dusty Crypt", world.player)
        and state.can_reach_region("Rusty Crypt", world.player)
    )


def hundred_percent(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.has_group("physical_items", world.player, 105)


def have_39_badges(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.has_group("cheats", world.player, 39)


def have_all_weapons(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.has_group("special_weapons", world.player, 7)


def can_reach_bats(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.can_reach_region("The Shrine Of Bombulus", world.player)


def can_reach_skeleton(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.can_reach_region("Halloween Hill", world.player)


def can_reach_frog(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.can_reach_region("Halloween Hill", world.player)


def can_reach_ghost(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.can_reach_region("Haunted Tower", world.player)


def can_reach_mummy(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.can_reach_region("Rocky Cliffs", world.player)


def can_reach_swampdog(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.can_reach_region("Halloween Hill", world.player)


def can_reach_vampire(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.can_reach_region("Castle Vampy", world.player)


def can_reach_wolves(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.can_reach_region("Halloween Hill", world.player)

def can_do_collection(state: CollectionState, world: "LoonylandWorld") -> bool:
    return state.has_group_unique("monster_dolls", world.player, 8)

def power_level(state: CollectionState, world: "LoonylandWorld", level_goal: int) -> bool:
    level: int = 0
    level += state.count_group("power", world.player)
    level += state.count_group("power_big", world.player) * 5
    level += state.count_group("power_max", world.player) * 50
    return level > level_goal