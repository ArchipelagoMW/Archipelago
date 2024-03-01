from typing import Dict, TYPE_CHECKING
from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule, forbid_item
from .rules import has_ability, has_sword, has_stick, has_ice_grapple_logic, has_lantern, has_mask, can_ladder_storage
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


def can_reach_east_overworld(state: CollectionState, player: int, options: TunicOptions, ability_unlocks: Dict[str, int]) -> bool:
    return (
        state.has_any({"Ladders near Weathervane", "Overworld Shortcut Ladders"}, player)
        or has_ice_grapple_logic(True, state, player, options, ability_unlocks)
        or (can_reach_upper_overworld(state, player, options, ability_unlocks)
            and state.has("Ladders near Patrol Cave", player))
        or can_ladder_storage(state, player, options)
        or (state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))
    )


def can_reach_upper_overworld(state: CollectionState, player: int, options: TunicOptions, ability_unlocks: Dict[str, int]) -> bool:
    return (
        (state.has("Ladders near Dark Tomb", player) and state.has_any({laurels, grapple}, player))
        or ((state.has_any({"Ladders near Weathervane", "Overworld Shortcut Ladders", grapple}, player) 
             or can_ladder_storage(state, player, options)) 
            and (state.has("Ladders near Patrol Cave", player) 
                 or has_ice_grapple_logic(True, state, player, options, ability_unlocks)))
    )


def set_ladder_region_rules(world: "TunicWorld", ability_unlocks: Dict[str, int]) -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    multiworld.get_entrance("Overworld -> Overworld Holy Cross", player).access_rule = \
        lambda state: has_ability(state, player, holy_cross, options, ability_unlocks)
    multiworld.get_entrance("Overworld -> Sealed Temple", player).access_rule = \
        lambda state: ((state.has("Ladder Drop to East Forest", player) and
                       can_reach_east_overworld(state, player, options, ability_unlocks)) and
                       (state.has("Ladders to West Belltower", player) and
                       ((state.has(laurels, player) and (has_sword(state, player) or state.has(fire_wand, player))) or
                        (state.has_all({lantern, "Dark Tomb Ladder"}, player) and has_sword(state, player))))
                       or (can_reach_upper_overworld(state, player, options, ability_unlocks) 
                           and state.has_all({laurels, "Ladder near Temple Rafters"}, player))
                       or has_ice_grapple_logic(False, state, player, options, ability_unlocks)
                       or can_ladder_storage(state, player, options) and state.has(laurels, player))
    multiworld.get_entrance("Overworld -> East Overworld", player).access_rule = \
        lambda state: can_reach_east_overworld(state, player, options, ability_unlocks)
    multiworld.get_entrance("Overworld -> Upper Overworld", player).access_rule = \
        lambda state: can_reach_upper_overworld(state, player, options, ability_unlocks)
    multiworld.get_entrance("Overworld -> East Forest", player).access_rule = \
        lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks)
    multiworld.get_entrance("East Overworld -> East Forest", player).access_rule = \
        lambda state: state.has("Ladder Drop to East Forest", player)
    multiworld.get_entrance("East Forest -> Lower Forest", player).access_rule = \
        lambda state: state.has("Ladders to Lower Forest", player)
    multiworld.get_entrance("Overworld -> Swamp", player).access_rule = \
        lambda state: state.has("Ladder to Swamp", player)
    multiworld.get_entrance("Swamp -> Swamp Middle", player).access_rule = \
        lambda state: (state.has("Central Swamp Ladder", player) or state.has(laurels, player)) \
        or (can_ladder_storage(state, player, options)
            and has_ability(state, player, holy_cross, options, ability_unlocks))
    multiworld.get_entrance("Swamp Middle -> Cathedral", player).access_rule = \
        lambda state: (has_ability(state, player, prayer, options, ability_unlocks)
                       and (state.has(laurels, player)
                            or (can_ladder_storage(state, player, options) and state.has(fire_wand, player)))
                       or has_ice_grapple_logic(False, state, player, options, ability_unlocks))
    multiworld.get_entrance("Overworld -> Back of Swamp", player).access_rule = \
        lambda state: state.has(laurels, player) or can_ladder_storage(state, player, options)
    # before the ladder, just the one chest in the room where you open up the grave to the ladder
    multiworld.get_entrance("Overworld -> Dark Tomb Front", player).access_rule = \
        lambda state: has_lantern(state, player, options)
    multiworld.get_entrance("Dark Tomb Front -> Dark Tomb", player).access_rule = \
        lambda state: state.has("Dark Tomb Ladder", player)
    # dark tomb to west garden has no rule intentionally
    multiworld.get_entrance("Overworld -> West Garden", player).access_rule = \
        lambda state: (state.has(laurels, player) and state.has("Ladders to West Belltower", player)) \
        or can_ladder_storage(state, player, options)
    multiworld.get_entrance("Overworld -> Beneath the Well", player).access_rule = \
        lambda state: state.has("Ladder to Well", player)
    # todo: make sure this ice grapple actually works with enemy rando off
    multiworld.get_entrance("Beneath the Well -> Beneath the Well Back", player).access_rule = \
        lambda state: state.has("Well Back Ladder", player) \
        or has_ice_grapple_logic(True, state, player, options, ability_unlocks)
    # dash to the fuse and have the rear ladder, or dash through the well boss gate in nmg
    multiworld.get_entrance("Overworld -> Beneath the Well Back", player).access_rule = \
        lambda state: state.has(laurels, player) and (state.has("Well Back Ladder", player)
                                                      or options.logic_rules)
    multiworld.get_entrance("Beneath the Well Back -> Beneath the Well", player).access_rule = \
        lambda state: state.has("Well Back Ladder", player)
    multiworld.get_entrance("East Overworld -> Eastern Vault Fortress", player).access_rule = \
        lambda state: state.has(laurels, player) \
        or has_ice_grapple_logic(True, state, player, options, ability_unlocks) \
        or can_ladder_storage(state, player, options)
    multiworld.get_entrance("East Overworld -> Beneath the Vault", player).access_rule = \
        lambda state: has_lantern(state, player, options) \
        and (can_ladder_storage(state, player, options)
             or has_ability(state, player, prayer, options, ability_unlocks)
             or state.has(laurels, player))
    multiworld.get_entrance("Overworld -> Ruined Atoll", player).access_rule = \
        lambda state: state.has_any({"Ladder to Ruined Atoll", laurels, grapple}, player) \
        or has_ability(state, player, prayer, options, ability_unlocks)
    multiworld.get_entrance("Ruined Atoll -> Frog's Domain", player).access_rule = \
        lambda state: state.has("Frog's Domain Ladders", player)
    multiworld.get_entrance("Ruined Atoll -> Library", player).access_rule = \
        lambda state: state.has_any({grapple, laurels}, player) and \
        has_ability(state, player, prayer, options, ability_unlocks) and \
        state.has("South Atoll Ladders", player)
    # have combat items, and the ladder to quarry, and the quarry ladder, or ls to skip those last two
    multiworld.get_entrance("Overworld -> Quarry", player).access_rule = \
        lambda state: (has_sword(state, player) or state.has(fire_wand, player)) \
        and ((state.has_any({grapple, laurels}, player) and state.has("Ladder to Quarry", player))
             or can_ladder_storage(state, player, options))
    multiworld.get_entrance("Quarry Back -> Quarry", player).access_rule = \
        lambda state: has_sword(state, player) or state.has(fire_wand, player)
    multiworld.get_entrance("Quarry -> Lower Quarry", player).access_rule = \
        lambda state: has_mask(state, player, options)
    multiworld.get_entrance("Lower Quarry -> Rooted Ziggurat", player).access_rule = \
        lambda state: state.has(grapple, player) and has_ability(state, player, prayer, options, ability_unlocks)
    multiworld.get_entrance("Overworld -> Spirit Arena", player).access_rule = \
        lambda state: (state.has(gold_hexagon, player, options.hexagon_goal.value) if options.hexagon_quest.value
                       else state.has_all({red_hexagon, green_hexagon, blue_hexagon}, player)) and \
        has_ability(state, player, prayer, options, ability_unlocks) and has_sword(state, player)


def set_ladder_location_rules(world: "TunicWorld", ability_unlocks: Dict[str, int]) -> None:
    multiworld = world.multiworld
    player = world.player
    options = world.options

    forbid_item(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player), fairies, player)

    # Ability Shuffle Exclusive Rules
    set_rule(multiworld.get_location("Far Shore - Page Pickup", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Fortress Courtyard - Chest Near Cave", player),
             lambda state: can_ladder_storage(state, player, options)
             or has_ability(state, player, prayer, options, ability_unlocks)
             or state.has(laurels, player))
    set_rule(multiworld.get_location("Fortress Courtyard - Page Near Cave", player),
             lambda state: can_ladder_storage(state, player, options)
             or has_ability(state, player, prayer, options, ability_unlocks)
             or state.has(laurels, player))
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
    set_rule(multiworld.get_location("Overworld - [Northwest] Golden Obelisk Page", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Overworld - [Northeast] Flowers Holy Cross", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Patrol Cave - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks)
             and (can_reach_east_overworld(state, player, options, ability_unlocks)
                  or ((can_reach_upper_overworld(state, player, options, ability_unlocks) or state.has(grapple, player))
                  and state.has("Ladders near Patrol Cave", player))))
    set_rule(multiworld.get_location("Sealed Temple - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Ruined Passage - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks)
             and (state.has("Ladders near Weathervane", player)
                  or state.has(key, player, 2)
                  or (state.has(laurels, player) and options.logic_rules)
                  or has_ice_grapple_logic(True, state, player, options, ability_unlocks)
                  or can_ladder_storage(state, player, options)))
    set_rule(multiworld.get_location("Caustic Light Cave - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Top of the Mountain - Page At The Peak", player),
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
             or (has_lantern(state, player, options) and has_sword(state, player)
                 and state.has_all({"Ladders to West Belltower", "Dark Tomb Ladder"}, player))
             or can_ladder_storage(state, player, options))
    set_rule(multiworld.get_location("Overworld - [Northwest] Chest Beneath Quarry Gate", player),
             lambda state: state.has_any({grapple, laurels}, player) or options.logic_rules)
    set_rule(multiworld.get_location("Overworld - [East] Grapple Chest", player),
             lambda state: state.has(grapple, player))
    set_rule(multiworld.get_location("Special Shop - Secret Page Pickup", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Ruined Passage - Page Pickup", player),
             lambda state: state.has("Ladders near Weathervane", player)
             or state.has(key, player, 2)
             or (state.has(laurels, player) and options.logic_rules)
             or has_ice_grapple_logic(True, state, player, options, ability_unlocks)
             or can_ladder_storage(state, player, options))
    set_rule(multiworld.get_location("Overworld - [East] Between Ladders Near Ruined Passage", player),
             lambda state: state.has("Ladders near Weathervane", player)
             or state.has(key, player, 2)
             or (state.has(laurels, player) and options.logic_rules)
             or has_ice_grapple_logic(True, state, player, options, ability_unlocks)
             or can_ladder_storage(state, player, options))
    set_rule(multiworld.get_location("Overworld - [East] Chest In Trees", player),
             lambda state: state.has_any({laurels, "Ladders near Weathervane"}, player))
    set_rule(multiworld.get_location("Hourglass Cave - Holy Cross Chest", player),
             lambda state: state.has("Hourglass Cave Ladders", player))
    set_rule(multiworld.get_location("Overworld - [Northwest] Chest Near Golden Obelisk", player),
             lambda state: state.has("Ladders near Dark Tomb", player)
             or (can_reach_upper_overworld(state, player, options, ability_unlocks) 
                 and state.has_any({laurels, grapple}, player)))
    set_rule(multiworld.get_location("Patrol Cave - Normal Chest", player),
             lambda state: can_reach_east_overworld(state, player, options, ability_unlocks)
             or ((can_reach_upper_overworld(state, player, options, ability_unlocks) or state.has(grapple, player))
                 and state.has("Ladders near Patrol Cave", player)))

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
             lambda state: has_sword(state, player) or state.has(laurels, player)
             or has_ice_grapple_logic(False, state, player, options, ability_unlocks)
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
    set_rule(multiworld.get_location("Ruined Atoll - [Southeast] Chest Near Fuse", player),
             lambda state: state.has("South Atoll Ladders", player))
    set_rule(multiworld.get_location("Ruined Atoll - [South] Upper Floor On Bricks", player),
             lambda state: state.has("South Atoll Ladders", player))
    set_rule(multiworld.get_location("Ruined Atoll - [South] Upper Floor On Power Line", player),
             lambda state: state.has("South Atoll Ladders", player))

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
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - Hexagon Blue", player),
             lambda state: has_sword(state, player))

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
    set_rule(multiworld.get_location("Swamp - [South Graveyard] Guarded By Tentacles", player),
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
