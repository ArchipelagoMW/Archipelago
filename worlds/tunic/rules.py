from random import Random
from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item
from BaseClasses import CollectionState
from .options import TunicOptions
if TYPE_CHECKING:
    from . import TunicWorld

laurels = "Hero's Laurels"
grapple = "Magic Orb"
ice_dagger = "Magic Dagger"
fire_wand = "Magic Wand"
lantern = "Lantern"
fairies = "Fairy"
coins = "Golden Coin"
prayer = "Pages 24-25 (Prayer)"
holy_cross = "Pages 42-43 (Holy Cross)"
icebolt = "Pages 52-53 (Icebolt)"
key = "Key"
house_key = "Old House Key"
vault_key = "Fortress Vault Key"
mask = "Scavenger Mask"
red_hexagon = "Red Questagon"
green_hexagon = "Green Questagon"
blue_hexagon = "Blue Questagon"
gold_hexagon = "Gold Questagon"


def randomize_ability_unlocks(random: Random, options: TunicOptions) -> Dict[str, int]:
    ability_requirement = [1, 1, 1]
    if options.hexagon_quest.value:
        hexagon_goal = options.hexagon_goal.value
        # Set ability unlocks to 25, 50, and 75% of goal amount
        ability_requirement = [hexagon_goal // 4, hexagon_goal // 2, hexagon_goal * 3 // 4]
    abilities = [prayer, holy_cross, icebolt]
    random.shuffle(abilities)
    return dict(zip(abilities, ability_requirement))


def has_ability(state: CollectionState, player: int, ability: str, options: TunicOptions,
                ability_unlocks: Dict[str, int]) -> bool:
    if not options.ability_shuffling:
        return True
    if options.hexagon_quest:
        return state.has(gold_hexagon, player, ability_unlocks[ability])
    return state.has(ability, player)


# a check to see if you can whack things in melee at all
def has_stick(state: CollectionState, player: int) -> bool:
    return state.has("Stick", player) or state.has("Sword Upgrade", player, 1) or state.has("Sword", player)


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has("Sword", player) or state.has("Sword Upgrade", player, 2)


def has_ice_grapple_logic(long_range: bool, state: CollectionState, player: int, options: TunicOptions,
                          ability_unlocks: Dict[str, int]) -> bool:
    if not options.logic_rules:
        return False

    if not long_range:
        return state.has_all({ice_dagger, grapple}, player)
    else:
        return state.has_all({ice_dagger, fire_wand, grapple}, player) and \
            has_ability(state, player, icebolt, options, ability_unlocks)


def can_ladder_storage(state: CollectionState, player: int, options: TunicOptions) -> bool:
    if options.logic_rules == "unrestricted" and has_stick(state, player):
        return True
    else:
        return False


def has_mask(state: CollectionState, player: int, options: TunicOptions) -> bool:
    if options.maskless:
        return True
    else:
        return state.has(mask, player)


def has_lantern(state: CollectionState, player: int, options: TunicOptions) -> bool:
    if options.lanternless:
        return True
    else:
        return state.has(lantern, player)


def set_region_rules(world: "TunicWorld", ability_unlocks: Dict[str, int]) -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    multiworld.get_entrance("Overworld -> Overworld Holy Cross", player).access_rule = \
        lambda state: has_ability(state, player, holy_cross, options, ability_unlocks)
    multiworld.get_entrance("Overworld -> Beneath the Well", player).access_rule = \
        lambda state: has_stick(state, player) or state.has(fire_wand, player)
    multiworld.get_entrance("Overworld -> Dark Tomb", player).access_rule = \
        lambda state: has_lantern(state, player, options)
    multiworld.get_entrance("Overworld -> West Garden", player).access_rule = \
        lambda state: state.has(laurels, player) \
        or can_ladder_storage(state, player, options)
    multiworld.get_entrance("Overworld -> Eastern Vault Fortress", player).access_rule = \
        lambda state: state.has(laurels, player) \
        or has_ice_grapple_logic(True, state, player, options, ability_unlocks) \
        or can_ladder_storage(state, player, options)
    # using laurels or ls to get in is covered by the -> Eastern Vault Fortress rules
    multiworld.get_entrance("Overworld -> Beneath the Vault", player).access_rule = \
        lambda state: has_lantern(state, player, options) and \
        has_ability(state, player, prayer, options, ability_unlocks)
    multiworld.get_entrance("Ruined Atoll -> Library", player).access_rule = \
        lambda state: state.has_any({grapple, laurels}, player) and \
        has_ability(state, player, prayer, options, ability_unlocks)
    multiworld.get_entrance("Overworld -> Quarry", player).access_rule = \
        lambda state: (has_sword(state, player) or state.has(fire_wand, player)) \
        and (state.has_any({grapple, laurels}, player) or can_ladder_storage(state, player, options))
    multiworld.get_entrance("Quarry Back -> Quarry", player).access_rule = \
        lambda state: has_sword(state, player) or state.has(fire_wand, player)
    multiworld.get_entrance("Quarry -> Lower Quarry", player).access_rule = \
        lambda state: has_mask(state, player, options)
    multiworld.get_entrance("Lower Quarry -> Rooted Ziggurat", player).access_rule = \
        lambda state: state.has(grapple, player) and has_ability(state, player, prayer, options, ability_unlocks)
    multiworld.get_entrance("Swamp -> Cathedral", player).access_rule = \
        lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks) \
        or has_ice_grapple_logic(False, state, player, options, ability_unlocks)
    multiworld.get_entrance("Overworld -> Spirit Arena", player).access_rule = \
        lambda state: (state.has(gold_hexagon, player, options.hexagon_goal.value) if options.hexagon_quest.value
                       else state.has_all({red_hexagon, green_hexagon, blue_hexagon}, player)) and \
        has_ability(state, player, prayer, options, ability_unlocks) and has_sword(state, player)


def set_location_rules(world: "TunicWorld", ability_unlocks: Dict[str, int]) -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    forbid_item(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player), fairies, player)

    # Ability Shuffle Exclusive Rules
    set_rule(multiworld.get_location("Far Shore - Page Pickup", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Fortress Courtyard - Chest Near Cave", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks) or state.has(laurels, player)
             or can_ladder_storage(state, player, options)
             or (has_ice_grapple_logic(True, state, player, options, ability_unlocks)
                 and has_lantern(state, player, options)))
    set_rule(multiworld.get_location("Fortress Courtyard - Page Near Cave", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks) or state.has(laurels, player)
             or can_ladder_storage(state, player, options)
             or (has_ice_grapple_logic(True, state, player, options, ability_unlocks)
                 and has_lantern(state, player, options)))
    set_rule(multiworld.get_location("East Forest - Dancing Fox Spirit Holy Cross", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Forest Grave Path - Holy Cross Code by Grave", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("East Forest - Golden Obelisk Holy Cross", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Beneath the Well - [Powered Secret Room] Chest", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("West Garden - [North] Behind Holy Cross Door", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Library Hall - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Candles Holy Cross", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("West Garden - [Central Highlands] Holy Cross (Blue Lines)", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Quarry - [Back Entrance] Bushes Holy Cross", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Cathedral - Secret Legend Trophy Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))

    # Overworld
    set_rule(multiworld.get_location("Overworld - [Southwest] Fountain Page", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] Grapple Chest Over Walkway", player),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] West Beach Guarded By Turret 2", player),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(multiworld.get_location("Far Shore - Secret Chest", player),
             lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Overworld - [Southeast] Page on Pillar by Swamp", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Old House - Normal Chest", player),
             lambda state: state.has(house_key, player)
             or has_ice_grapple_logic(False, state, player, options, ability_unlocks)
             or (state.has(laurels, player) and options.logic_rules))
    set_rule(multiworld.get_location("Old House - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks) and
             (state.has(house_key, player)
             or has_ice_grapple_logic(False, state, player, options, ability_unlocks)
             or (state.has(laurels, player) and options.logic_rules)))
    set_rule(multiworld.get_location("Old House - Shield Pickup", player),
             lambda state: state.has(house_key, player)
             or has_ice_grapple_logic(False, state, player, options, ability_unlocks)
             or (state.has(laurels, player) and options.logic_rules))
    set_rule(multiworld.get_location("Overworld - [Northwest] Page on Pillar by Dark Tomb", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] From West Garden", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [West] Chest After Bell", player),
             lambda state: state.has(laurels, player)
             or (has_lantern(state, player, options) and has_sword(state, player))
             or can_ladder_storage(state, player, options))
    set_rule(multiworld.get_location("Overworld - [Northwest] Chest Beneath Quarry Gate", player),
             lambda state: state.has_any({grapple, laurels}, player) or options.logic_rules)
    set_rule(multiworld.get_location("Overworld - [East] Grapple Chest", player),
             lambda state: state.has(grapple, player))
    set_rule(multiworld.get_location("Special Shop - Secret Page Pickup", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Sealed Temple - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks) and
             (state.has(laurels, player)
              or (has_lantern(state, player, options) and
                  (has_sword(state, player) or state.has(fire_wand, player)))
              or has_ice_grapple_logic(False, state, player, options, ability_unlocks)))
    set_rule(multiworld.get_location("Sealed Temple - Page Pickup", player),
             lambda state: state.has(laurels, player)
             or (has_lantern(state, player, options) and (has_sword(state, player) or state.has(fire_wand, player)))
             or has_ice_grapple_logic(False, state, player, options, ability_unlocks))
    set_rule(multiworld.get_location("West Furnace - Lantern Pickup", player),
             lambda state: has_stick(state, player) or state.has_any({fire_wand, laurels}, player))

    set_rule(multiworld.get_location("Secret Gathering Place - 10 Fairy Reward", player),
             lambda state: state.has(fairies, player, 10))
    set_rule(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player),
             lambda state: state.has(fairies, player, 20))
    set_rule(multiworld.get_location("Coins in the Well - 3 Coins", player),
             lambda state: state.has(coins, player, 3))
    set_rule(multiworld.get_location("Coins in the Well - 6 Coins", player),
             lambda state: state.has(coins, player, 6))
    set_rule(multiworld.get_location("Coins in the Well - 10 Coins", player),
             lambda state: state.has(coins, player, 10))
    set_rule(multiworld.get_location("Coins in the Well - 15 Coins", player),
             lambda state: state.has(coins, player, 15))

    # East Forest
    set_rule(multiworld.get_location("East Forest - Lower Grapple Chest", player),
             lambda state: state.has(grapple, player))
    set_rule(multiworld.get_location("East Forest - Lower Dash Chest", player),
             lambda state: state.has_all({grapple, laurels}, player))
    set_rule(multiworld.get_location("East Forest - Ice Rod Grapple Chest", player),
             lambda state: state.has_all({grapple, ice_dagger, fire_wand}, player)
             and has_ability(state, player, icebolt, options, ability_unlocks))

    # West Garden
    set_rule(multiworld.get_location("West Garden - [North] Across From Page Pickup", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [West] In Flooded Walkway", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [West Lowlands] Tree Holy Cross Chest", player),
             lambda state: state.has(laurels, player)
             and has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("West Garden - [East Lowlands] Page Behind Ice Dagger House", player),
             lambda state: (state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))
             or has_ice_grapple_logic(True, state, player, options, ability_unlocks))
    set_rule(multiworld.get_location("West Garden - [Central Lowlands] Below Left Walkway", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [Central Highlands] After Garden Knight", player),
             lambda state: state.has(laurels, player)
             or (has_lantern(state, player, options) and has_sword(state, player))
             or can_ladder_storage(state, player, options))

    # Ruined Atoll
    set_rule(multiworld.get_location("Ruined Atoll - [West] Near Kevin Block", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Lower Chest", player),
             lambda state: state.has_any({laurels, key}, player))
    set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Upper Chest", player),
             lambda state: state.has_any({laurels, key}, player))
    set_rule(multiworld.get_location("Librarian - Hexagon Green", player),
             lambda state: has_sword(state, player) or options.logic_rules)

    # Frog's Domain
    set_rule(multiworld.get_location("Frog's Domain - Side Room Grapple Secret", player),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(multiworld.get_location("Frog's Domain - Grapple Above Hot Tub", player),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(multiworld.get_location("Frog's Domain - Escape Chest", player),
             lambda state: state.has_any({grapple, laurels}, player))

    # Eastern Vault Fortress
    set_rule(multiworld.get_location("Fortress Leaf Piles - Secret Chest", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Fortress Arena - Siege Engine/Vault Key Pickup", player),
             lambda state: has_sword(state, player) and
             (has_ability(state, player, prayer, options, ability_unlocks)
              or has_ice_grapple_logic(False, state, player, options, ability_unlocks)))
    set_rule(multiworld.get_location("Fortress Arena - Hexagon Red", player),
             lambda state: state.has(vault_key, player) and
             (has_ability(state, player, prayer, options, ability_unlocks)
              or has_ice_grapple_logic(False, state, player, options, ability_unlocks)))

    # Beneath the Vault
    set_rule(multiworld.get_location("Beneath the Fortress - Bridge", player),
             lambda state: has_stick(state, player) or state.has_any({laurels, fire_wand}, player))
    set_rule(multiworld.get_location("Beneath the Fortress - Obscured Behind Waterfall", player),
             lambda state: has_stick(state, player) and has_lantern(state, player, options))

    # Quarry
    set_rule(multiworld.get_location("Quarry - [Central] Above Ladder Dash Chest", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Quarry - [West] Upper Area Bombable Wall", player),
             lambda state: has_mask(state, player, options))
    # nmg - kill boss scav with orb + firecracker, or similar
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - Hexagon Blue", player),
             lambda state: has_sword(state, player) or (state.has(grapple, player) and options.logic_rules))

    # Swamp
    set_rule(multiworld.get_location("Cathedral Gauntlet - Gauntlet Reward", player),
             lambda state: state.has(laurels, player) and state.has(fire_wand, player) and has_sword(state, player))
    set_rule(multiworld.get_location("Swamp - [Entrance] Above Entryway", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Swamp - [South Graveyard] Upper Walkway Dash Chest", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Swamp - [Outside Cathedral] Obscured Behind Memorial", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Swamp - [South Graveyard] 4 Orange Skulls", player),
             lambda state: has_sword(state, player))

    # Hero's Grave
    set_rule(multiworld.get_location("Hero's Grave - Tooth Relic", player),
             lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Hero's Grave - Mushroom Relic", player),
             lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Hero's Grave - Ash Relic", player),
             lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Hero's Grave - Flowers Relic", player),
             lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Hero's Grave - Effigy Relic", player),
             lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Hero's Grave - Feathers Relic", player),
             lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))
