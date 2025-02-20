from random import Random
from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
from .options import TunicOptions, LadderStorage, IceGrappling
if TYPE_CHECKING:
    from . import TunicWorld

laurels = "Hero's Laurels"
grapple = "Magic Orb"
ice_dagger = "Magic Dagger"
fire_wand = "Magic Wand"
gun = "Gun"
lantern = "Lantern"
fairies = "Fairy"
coins = "Golden Coin"
prayer = "Pages 24-25 (Prayer)"
holy_cross = "Pages 42-43 (Holy Cross)"
icebolt = "Pages 52-53 (Icebolt)"
shield = "Shield"
key = "Key"
house_key = "Old House Key"
vault_key = "Fortress Vault Key"
mask = "Scavenger Mask"
red_hexagon = "Red Questagon"
green_hexagon = "Green Questagon"
blue_hexagon = "Blue Questagon"
gold_hexagon = "Gold Questagon"

# "Quarry - [East] Bombable Wall" is excluded from this list since it has slightly different rules
bomb_walls = ["East Forest - Bombable Wall", "Eastern Vault Fortress - [East Wing] Bombable Wall",
              "Overworld - [Central] Bombable Wall", "Overworld - [Southwest] Bombable Wall Near Fountain",
              "Quarry - [West] Upper Area Bombable Wall", "Ruined Atoll - [Northwest] Bombable Wall"]


def randomize_ability_unlocks(random: Random, options: TunicOptions) -> Dict[str, int]:
    ability_requirement = [1, 1, 1]
    if options.hexagon_quest.value:
        hexagon_goal = options.hexagon_goal.value
        # Set ability unlocks to 25, 50, and 75% of goal amount
        ability_requirement = [hexagon_goal // 4, hexagon_goal // 2, hexagon_goal * 3 // 4]
    abilities = [prayer, holy_cross, icebolt]
    random.shuffle(abilities)
    return dict(zip(abilities, ability_requirement))


def has_ability(ability: str, state: CollectionState, world: "TunicWorld") -> bool:
    options = world.options
    ability_unlocks = world.ability_unlocks
    if not options.ability_shuffling:
        return True
    if options.hexagon_quest:
        return state.has(gold_hexagon, world.player, ability_unlocks[ability])
    return state.has(ability, world.player)


# a check to see if you can whack things in melee at all
def has_melee(state: CollectionState, player: int) -> bool:
    return state.has_any({"Stick", "Sword", "Sword Upgrade"}, player)


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has("Sword", player) or state.has("Sword Upgrade", player, 2)


def laurels_zip(state: CollectionState, world: "TunicWorld") -> bool:
    return world.options.laurels_zips and state.has(laurels, world.player)


def has_ice_grapple_logic(long_range: bool, difficulty: IceGrappling, state: CollectionState, world: "TunicWorld") -> bool:
    if world.options.ice_grappling < difficulty:
        return False
    if not long_range:
        return state.has_all({ice_dagger, grapple}, world.player)
    else:
        return state.has_all({ice_dagger, fire_wand, grapple}, world.player) and has_ability(icebolt, state, world)


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


def set_region_rules(world: "TunicWorld") -> None:
    player = world.player
    options = world.options

    world.get_entrance("Overworld -> Overworld Holy Cross").access_rule = \
        lambda state: has_ability(holy_cross, state, world)
    world.get_entrance("Overworld -> Beneath the Well").access_rule = \
        lambda state: has_melee(state, player) or state.has(fire_wand, player)
    world.get_entrance("Overworld -> Dark Tomb").access_rule = \
        lambda state: has_lantern(state, world)
    # laurels in, ladder storage in through the furnace, or ice grapple down the belltower
    world.get_entrance("Overworld -> West Garden").access_rule = \
        lambda state: (state.has(laurels, player)
                       or can_ladder_storage(state, world)
                       or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
    world.get_entrance("Overworld -> Eastern Vault Fortress").access_rule = \
        lambda state: state.has(laurels, player) \
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world) \
        or can_ladder_storage(state, world)
    # using laurels or ls to get in is covered by the -> Eastern Vault Fortress rules
    world.get_entrance("Overworld -> Beneath the Vault").access_rule = \
        lambda state: (has_lantern(state, world) and has_ability(prayer, state, world)
                       # there's some boxes in the way
                       and (has_melee(state, player) or state.has_any((gun, grapple, fire_wand), player)))
    world.get_entrance("Ruined Atoll -> Library").access_rule = \
        lambda state: state.has_any({grapple, laurels}, player) and has_ability(prayer, state, world)
    world.get_entrance("Overworld -> Quarry").access_rule = \
        lambda state: (has_sword(state, player) or state.has(fire_wand, player)) \
        and (state.has_any({grapple, laurels, gun}, player) or can_ladder_storage(state, world))
    world.get_entrance("Quarry Back -> Quarry").access_rule = \
        lambda state: has_sword(state, player) or state.has(fire_wand, player)
    world.get_entrance("Quarry -> Lower Quarry").access_rule = \
        lambda state: has_mask(state, world)
    world.get_entrance("Lower Quarry -> Rooted Ziggurat").access_rule = \
        lambda state: state.has(grapple, player) and has_ability(prayer, state, world)
    world.get_entrance("Swamp -> Cathedral").access_rule = \
        lambda state: (state.has(laurels, player) and has_ability(prayer, state, world)) \
        or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world)
    world.get_entrance("Overworld -> Spirit Arena").access_rule = \
        lambda state: ((state.has(gold_hexagon, player, options.hexagon_goal.value) if options.hexagon_quest.value
                       else state.has_all({red_hexagon, green_hexagon, blue_hexagon}, player)
                       and state.has_group_unique("Hero Relics", player, 6))
                       and has_ability(prayer, state, world) and has_sword(state, player)
                       and state.has_any({lantern, laurels}, player))

    world.get_region("Quarry").connect(world.get_region("Rooted Ziggurat"),
                                       rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_hard, state, world)
                                       and has_ability(prayer, state, world))

    if options.ladder_storage >= LadderStorage.option_medium:
        # ls at any ladder in a safe spot in quarry to get to the monastery rope entrance
        world.get_region("Quarry Back").connect(world.get_region("Monastery"),
                                                rule=lambda state: can_ladder_storage(state, world))


def set_location_rules(world: "TunicWorld") -> None:
    player = world.player

    forbid_item(world.get_location("Secret Gathering Place - 20 Fairy Reward"), fairies, player)

    # Ability Shuffle Exclusive Rules
    set_rule(world.get_location("Far Shore - Page Pickup"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("Fortress Courtyard - Chest Near Cave"),
             lambda state: has_ability(prayer, state, world)
             or state.has(laurels, player)
             or can_ladder_storage(state, world)
             or (has_ice_grapple_logic(True, IceGrappling.option_easy, state, world)
                 and has_lantern(state, world)))
    set_rule(world.get_location("Fortress Courtyard - Page Near Cave"),
             lambda state: has_ability(prayer, state, world) or state.has(laurels, player)
             or can_ladder_storage(state, world)
             or (has_ice_grapple_logic(True, IceGrappling.option_easy, state, world)
                 and has_lantern(state, world)))
    set_rule(world.get_location("East Forest - Dancing Fox Spirit Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Forest Grave Path - Holy Cross Code by Grave"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("East Forest - Golden Obelisk Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Beneath the Well - [Powered Secret Room] Chest"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("West Garden - [North] Behind Holy Cross Door"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Library Hall - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Eastern Vault Fortress - [West Wing] Candles Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("West Garden - [Central Highlands] Holy Cross (Blue Lines)"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Quarry - [Back Entrance] Bushes Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Cathedral - Secret Legend Trophy Chest"),
             lambda state: has_ability(holy_cross, state, world))

    # Overworld
    set_rule(world.get_location("Overworld - [Southwest] Fountain Page"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Overworld - [Southwest] Grapple Chest Over Walkway"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Overworld - [Southwest] West Beach Guarded By Turret 2"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Far Shore - Secret Chest"),
             lambda state: state.has(laurels, player) and has_ability(prayer, state, world))
    set_rule(world.get_location("Overworld - [Southeast] Page on Pillar by Swamp"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Old House - Normal Chest"),
             lambda state: state.has(house_key, player)
             or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world)
             or laurels_zip(state, world))
    set_rule(world.get_location("Old House - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world) and (
                     state.has(house_key, player)
                     or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world)
                     or laurels_zip(state, world)))
    set_rule(world.get_location("Old House - Shield Pickup"),
             lambda state: state.has(house_key, player)
             or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world)
             or laurels_zip(state, world))
    set_rule(world.get_location("Overworld - [Northwest] Page on Pillar by Dark Tomb"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Overworld - [Southwest] From West Garden"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Overworld - [West] Chest After Bell"),
             lambda state: state.has(laurels, player)
             or (has_lantern(state, world) and has_sword(state, player))
             or can_ladder_storage(state, world))
    set_rule(world.get_location("Overworld - [Northwest] Chest Beneath Quarry Gate"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Overworld - [East] Grapple Chest"),
             lambda state: state.has(grapple, player))
    set_rule(world.get_location("Special Shop - Secret Page Pickup"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Sealed Temple - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world)
             and (state.has(laurels, player) or (has_lantern(state, world) and (has_sword(state, player)
                                                                                or state.has(fire_wand, player)))
                  or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world)))
    set_rule(world.get_location("Sealed Temple - Page Pickup"),
             lambda state: state.has(laurels, player)
             or (has_lantern(state, world) and (has_sword(state, player) or state.has(fire_wand, player)))
             or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
    set_rule(world.get_location("West Furnace - Lantern Pickup"),
             lambda state: has_melee(state, player) or state.has_any({fire_wand, laurels}, player))

    set_rule(world.get_location("Secret Gathering Place - 10 Fairy Reward"),
             lambda state: state.has(fairies, player, 10))
    set_rule(world.get_location("Secret Gathering Place - 20 Fairy Reward"),
             lambda state: state.has(fairies, player, 20))
    set_rule(world.get_location("Coins in the Well - 3 Coins"),
             lambda state: state.has(coins, player, 3))
    set_rule(world.get_location("Coins in the Well - 6 Coins"),
             lambda state: state.has(coins, player, 6))
    set_rule(world.get_location("Coins in the Well - 10 Coins"),
             lambda state: state.has(coins, player, 10))
    set_rule(world.get_location("Coins in the Well - 15 Coins"),
             lambda state: state.has(coins, player, 15))

    # East Forest
    set_rule(world.get_location("East Forest - Lower Grapple Chest"),
             lambda state: state.has(grapple, player))
    set_rule(world.get_location("East Forest - Lower Dash Chest"),
             lambda state: state.has_all({grapple, laurels}, player))
    set_rule(world.get_location("East Forest - Ice Rod Grapple Chest"),
             lambda state: state.has_all({grapple, ice_dagger, fire_wand}, player)
             and has_ability(icebolt, state, world))

    # West Garden
    set_rule(world.get_location("West Garden - [North] Across From Page Pickup"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("West Garden - [West] In Flooded Walkway"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("West Garden - [West Lowlands] Tree Holy Cross Chest"),
             lambda state: state.has(laurels, player) and has_ability(holy_cross, state, world))
    set_rule(world.get_location("West Garden - [East Lowlands] Page Behind Ice Dagger House"),
             lambda state: (state.has(laurels, player) and has_ability(prayer, state, world))
             or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
    set_rule(world.get_location("West Garden - [Central Lowlands] Below Left Walkway"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("West Garden - [Central Highlands] After Garden Knight"),
             lambda state: state.has(laurels, player)
             or (has_lantern(state, world) and has_sword(state, player))
             or can_ladder_storage(state, world))

    # Ruined Atoll
    set_rule(world.get_location("Ruined Atoll - [West] Near Kevin Block"),
             lambda state: state.has(laurels, player))
    # ice grapple push a crab through the door
    set_rule(world.get_location("Ruined Atoll - [East] Locked Room Lower Chest"),
             lambda state: state.has(laurels, player) or state.has(key, player, 2)
             or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
    set_rule(world.get_location("Ruined Atoll - [East] Locked Room Upper Chest"),
             lambda state: state.has(laurels, player) or state.has(key, player, 2)
             or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
    set_rule(world.get_location("Librarian - Hexagon Green"),
             lambda state: has_sword(state, player))

    # Frog's Domain
    set_rule(world.get_location("Frog's Domain - Side Room Grapple Secret"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Frog's Domain - Grapple Above Hot Tub"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Frog's Domain - Escape Chest"),
             lambda state: state.has_any({grapple, laurels}, player))

    # Library Lab
    set_rule(world.get_location("Library Lab - Page 1"),
             lambda state: has_melee(state, player) or state.has_any((fire_wand, gun), player))
    set_rule(world.get_location("Library Lab - Page 2"),
             lambda state: has_melee(state, player) or state.has_any((fire_wand, gun), player))
    set_rule(world.get_location("Library Lab - Page 3"),
             lambda state: has_melee(state, player) or state.has_any((fire_wand, gun), player))

    # Eastern Vault Fortress
    # yes, you can clear the leaves with dagger
    # gun isn't included since it can only break one leaf pile at a time, and we don't check how much mana you have
    # but really, I expect the player to just throw a bomb at them if they don't have melee
    set_rule(world.get_location("Fortress Leaf Piles - Secret Chest"),
             lambda state: state.has(laurels, player) and (has_melee(state, player) or state.has(ice_dagger, player)))
    set_rule(world.get_location("Fortress Arena - Siege Engine/Vault Key Pickup"),
             lambda state: has_sword(state, player)
             and (has_ability(prayer, state, world)
                  or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world)))
    set_rule(world.get_location("Fortress Arena - Hexagon Red"),
             lambda state: state.has(vault_key, player)
             and (has_ability(prayer, state, world)
                  or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world)))

    # Beneath the Vault
    set_rule(world.get_location("Beneath the Fortress - Bridge"),
             lambda state: has_melee(state, player) or state.has_any((laurels, fire_wand, ice_dagger, gun), player))
    set_rule(world.get_location("Beneath the Fortress - Obscured Behind Waterfall"),
             lambda state: has_melee(state, player) and has_lantern(state, world))

    # Quarry
    set_rule(world.get_location("Quarry - [Central] Above Ladder Dash Chest"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Rooted Ziggurat Upper - Near Bridge Switch"),
             lambda state: has_sword(state, player) or state.has_all({fire_wand, laurels}, player))
    set_rule(world.get_location("Rooted Ziggurat Lower - Hexagon Blue"),
             lambda state: has_sword(state, player))

    # Swamp
    set_rule(world.get_location("Cathedral Gauntlet - Gauntlet Reward"),
             lambda state: (state.has(fire_wand, player) and has_sword(state, player))
             and (state.has(laurels, player) 
                  or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world)))
    set_rule(world.get_location("Swamp - [Entrance] Above Entryway"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Swamp - [South Graveyard] Upper Walkway Dash Chest"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Swamp - [Outside Cathedral] Obscured Behind Memorial"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Swamp - [South Graveyard] 4 Orange Skulls"),
             lambda state: has_sword(state, player))

    # Hero's Grave
    set_rule(world.get_location("Hero's Grave - Tooth Relic"),
             lambda state: state.has(laurels, player) and has_ability(prayer, state, world))
    set_rule(world.get_location("Hero's Grave - Mushroom Relic"),
             lambda state: state.has(laurels, player) and has_ability(prayer, state, world))
    set_rule(world.get_location("Hero's Grave - Ash Relic"),
             lambda state: state.has(laurels, player) and has_ability(prayer, state, world))
    set_rule(world.get_location("Hero's Grave - Flowers Relic"),
             lambda state: state.has(laurels, player) and has_ability(prayer, state, world))
    set_rule(world.get_location("Hero's Grave - Effigy Relic"),
             lambda state: state.has(laurels, player) and has_ability(prayer, state, world))
    set_rule(world.get_location("Hero's Grave - Feathers Relic"),
             lambda state: state.has(laurels, player) and has_ability(prayer, state, world))

    # Bombable Walls
    for location_name in bomb_walls:
        # has_sword is there because you can buy bombs in the shop
        set_rule(world.get_location(location_name),
                 lambda state: state.has(gun, player)
                 or has_sword(state, player)
                 or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
    add_rule(world.get_location("Cube Cave - Holy Cross Chest"),
             lambda state: state.has(gun, player)
             or has_sword(state, player)
             or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
    # can't ice grapple to this one, not enough space
    set_rule(world.get_location("Quarry - [East] Bombable Wall"),
             lambda state: state.has(gun, player) or has_sword(state, player))

    # Shop
    set_rule(world.get_location("Shop - Potion 1"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Shop - Potion 2"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Shop - Coin 1"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Shop - Coin 2"),
             lambda state: has_sword(state, player))
