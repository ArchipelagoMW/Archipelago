from typing import TYPE_CHECKING

from BaseClasses import CollectionState

from .options import IceGrappling

if TYPE_CHECKING:
    from . import TunicWorld


def has_ability(ability: str, state: CollectionState, world: "TunicWorld") -> bool:
    options = world.options
    ability_unlocks = world.ability_unlocks
    if not options.ability_shuffling:
        return True
    if options.hexagon_quest:
        return state.has("Gold Questagon", world.player, ability_unlocks[ability])
    return state.has(ability, world.player)


# a check to see if you can whack things in melee at all
def has_melee(state: CollectionState, player: int) -> bool:
    return state.has_any({"Stick", "Sword", "Sword Upgrade"}, player)


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has("Sword", player) or state.has("Sword Upgrade", player, 2)


def laurels_zip(state: CollectionState, world: "TunicWorld") -> bool:
    return world.options.laurels_zips and state.has("Hero's Laurels", world.player)


def has_ice_grapple_logic(long_range: bool, difficulty: IceGrappling, state: CollectionState, world: "TunicWorld") -> bool:
    if world.options.ice_grappling < difficulty:
        return False
    if not long_range:
        return state.has_all(("Magic Dagger", "Magic Orb"), world.player)
    else:
        return (state.has_all(("Magic Dagger", "Magic Wand", "Magic Orb"), world.player)
                and has_ability("Pages 52-53 (Icebolt)", state, world))


def can_ladder_storage(state: CollectionState, world: "TunicWorld") -> bool:
    if not world.options.ladder_storage:
        return False
    if world.options.ladder_storage_without_items:
        return True
    return has_melee(state, world.player) or state.has_any(("Magic Orb", "Shield"), world.player)


def has_mask(state: CollectionState, world: "TunicWorld") -> bool:
    return world.options.maskless or state.has("Scavenger Mask", world.player)


def has_lantern(state: CollectionState, world: "TunicWorld") -> bool:
    return world.options.lanternless or state.has("Lantern", world.player)


def has_ladder(ladder: str, state: CollectionState, world: "TunicWorld") -> bool:
    return not world.options.shuffle_ladders or state.has(ladder, world.player)


def can_shop(state: CollectionState, world: "TunicWorld") -> bool:
    return has_sword(state, world.player) and state.can_reach_region("Shop", world.player)


# for the ones that are not early bushes where ER can screw you over a bit
def can_get_past_bushes(state: CollectionState, world: "TunicWorld") -> bool:
    # add in glass cannon + stick for grass rando
    return has_sword(state, world.player) or state.has_any(("Magic Wand", "Hero's Laurels", "Gun"), world.player)
