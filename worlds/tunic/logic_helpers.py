from typing import TYPE_CHECKING

from BaseClasses import CollectionState

from .constants import *
from .options import HexagonQuestAbilityUnlockType, IceGrappling

if TYPE_CHECKING:
    from . import TunicWorld


def randomize_ability_unlocks(world: "TunicWorld") -> dict[str, int]:
    options = world.options

    abilities = [prayer, holy_cross, icebolt]
    ability_requirement = [1, 1, 1]
    world.random.shuffle(abilities)

    if options.hexagon_quest.value and options.hexagon_quest_ability_type == HexagonQuestAbilityUnlockType.option_hexagons:
        hexagon_goal = options.hexagon_goal.value
        # Set ability unlocks to 25, 50, and 75% of goal amount
        ability_requirement = [hexagon_goal // 4, hexagon_goal // 2, hexagon_goal * 3 // 4]
        if any(req == 0 for req in ability_requirement):
            ability_requirement = [1, 2, 3]

    return dict(zip(abilities, ability_requirement))


def has_ability(ability: str, state: CollectionState, world: "TunicWorld") -> bool:
    options = world.options
    ability_unlocks = world.ability_unlocks
    if not options.ability_shuffling:
        return True
    if options.hexagon_quest and options.hexagon_quest_ability_type == HexagonQuestAbilityUnlockType.option_hexagons:
        return state.has(gold_hexagon, world.player, ability_unlocks[ability])
    return state.has(ability, world.player)


# a check to see if you can whack things in melee at all
def has_melee(state: CollectionState, player: int) -> bool:
    return state.has_any(("Stick", "Sword", "Sword Upgrade"), player)


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has("Sword", player) or state.has("Sword Upgrade", player, 2)


def laurels_zip(state: CollectionState, world: "TunicWorld") -> bool:
    return world.options.laurels_zips and state.has(laurels, world.player)


def has_ice_grapple_logic(long_range: bool, difficulty: IceGrappling, state: CollectionState, world: "TunicWorld") -> bool:
    if world.options.ice_grappling < difficulty:
        return False
    if not long_range:
        return state.has_all((ice_dagger, grapple), world.player)
    else:
        return state.has_all((ice_dagger, fire_wand, grapple), world.player) and has_ability(icebolt, state, world)


def can_ladder_storage(state: CollectionState, world: "TunicWorld") -> bool:
    if not world.options.ladder_storage:
        return False
    if world.options.ladder_storage_without_items:
        return True
    return has_melee(state, world.player) or state.has_any((grapple, shield), world.player)


def has_mask(state: CollectionState, world: "TunicWorld") -> bool:
    return world.options.maskless or state.has(mask, world.player)


def has_lantern(state: CollectionState, world: "TunicWorld") -> bool:
    return world.options.lanternless or state.has(lantern, world.player)


def has_ladder(ladder: str, state: CollectionState, world: "TunicWorld") -> bool:
    return not world.options.shuffle_ladders or state.has(ladder, world.player)


def can_shop(state: CollectionState, world: "TunicWorld") -> bool:
    return has_sword(state, world.player) and state.can_reach_region("Shop", world.player)


# for the ones that are not early bushes where ER can screw you over a bit
def can_get_past_bushes(state: CollectionState, world: "TunicWorld") -> bool:
    # add in glass cannon + stick for grass rando
    return has_sword(state, world.player) or state.has_any((fire_wand, laurels, gun), world.player)


# for fuse locations and reusing event names to simplify er_rules
fuse_activation_reqs: dict[str, list[str]] = {
    swamp_fuse_2: [swamp_fuse_1],
    swamp_fuse_3: [swamp_fuse_1, swamp_fuse_2],
    fortress_exterior_fuse_2: [fortress_exterior_fuse_1],
    beneath_the_vault_fuse: [fortress_exterior_fuse_1, fortress_exterior_fuse_2],
    fortress_candles_fuse: [fortress_exterior_fuse_1, fortress_exterior_fuse_2, beneath_the_vault_fuse],
    fortress_door_left_fuse: [fortress_exterior_fuse_1, fortress_exterior_fuse_2, beneath_the_vault_fuse,
                              fortress_candles_fuse],
    fortress_courtyard_upper_fuse: [fortress_exterior_fuse_1],
    fortress_courtyard_lower_fuse: [fortress_exterior_fuse_1, fortress_courtyard_upper_fuse],
    fortress_door_right_fuse: [fortress_exterior_fuse_1, fortress_courtyard_upper_fuse, fortress_courtyard_lower_fuse],
    quarry_fuse_2: [quarry_fuse_1],
    "Activate Furnace Fuse": [west_furnace_fuse],
    "Activate South and West Fortress Exterior Fuses": [fortress_exterior_fuse_1, fortress_exterior_fuse_2],
    "Activate Upper and Central Fortress Exterior Fuses": [fortress_exterior_fuse_1, fortress_courtyard_upper_fuse,
                                                           fortress_courtyard_lower_fuse],
    "Activate Beneath the Vault Fuse": [fortress_exterior_fuse_1, fortress_exterior_fuse_2, beneath_the_vault_fuse],
    "Activate Eastern Vault West Fuses": [fortress_exterior_fuse_1, fortress_exterior_fuse_2, beneath_the_vault_fuse,
                                          fortress_candles_fuse, fortress_door_left_fuse],
    "Activate Eastern Vault East Fuse": [fortress_exterior_fuse_1, fortress_courtyard_upper_fuse,
                                         fortress_courtyard_lower_fuse, fortress_door_right_fuse],
    "Activate Quarry Connector Fuse": [quarry_fuse_1],
    "Activate Quarry Fuse": [quarry_fuse_1, quarry_fuse_2],
    "Activate Ziggurat Fuse": [ziggurat_teleporter_fuse],
    "Activate West Garden Fuse": [west_garden_fuse],
    "Activate Library Fuse": [library_lab_fuse],
}


def has_fuses(fuse_event: str, state: CollectionState, world: "TunicWorld") -> bool:
    if world.options.shuffle_fuses:
        return state.has_all(fuse_activation_reqs[fuse_event], world.player)

    return state.has(fuse_event, world.player)
