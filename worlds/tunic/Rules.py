from random import Random
from typing import Dict

from ..generic.Rules import set_rule, forbid_item
from BaseClasses import MultiWorld

hexagon_quest_abilities: Dict[str, int] = {}


def set_abilities(multiworld: MultiWorld, player: int, random: Random):
    ability_requirement = [5, 10, 15]
    abilities = ["prayer", "holy_cross", "ice_rod"]
    random.shuffle(ability_requirement)
    random.shuffle(abilities)
    for i in range(3):
        hexagon_quest_abilities[abilities.pop()] = ability_requirement.pop()


def set_region_rules(multiworld: MultiWorld, player: int):
    laurels = "Hero's Laurels"
    grapple = "Magic Orb"
    lantern = "Lantern"
    mask = "Scavenger Mask"
    prayer = "Pages 24-25 (Prayer)"
    holy_cross = "Pages 42-43 (Holy Cross)"
    red_hexagon = "Red Hexagon"
    green_hexagon = "Green Hexagon"
    blue_hexagon = "Blue Hexagon"
    gold_hexagon = "Gold Hexagon"

    prayer_amount = 1
    holy_cross_amount = 1

    ability_shuffle = multiworld.ability_shuffling[player].value

    if multiworld.hexagon_quest[player].value:
        prayer, holy_cross = ["Gold Hexagon", "Gold Hexagon"]
        prayer_amount = hexagon_quest_abilities["prayer"]
        holy_cross_amount = hexagon_quest_abilities["holy_cross"]

    if ability_shuffle:
        multiworld.get_entrance("Overworld -> Overworld Holy Cross", player).access_rule = lambda state: state.has(holy_cross, player, holy_cross_amount)
        multiworld.get_entrance("Library -> Ruined Atoll", player).access_rule = lambda state: state.has(prayer, player, prayer_amount)
        multiworld.get_entrance("Overworld -> Beneath the Vault", player).access_rule = lambda state: state.has(lantern, player) and state.has(prayer, player, prayer_amount)
        multiworld.get_entrance("Lower Quarry -> Rooted Ziggurat", player).access_rule = lambda state: state.has(grapple, player) and state.has(prayer, player, prayer_amount)
        multiworld.get_entrance("Swamp -> Cathedral", player).access_rule = lambda state: state.has(laurels, player) and state.has(prayer, player, prayer_amount)
        multiworld.get_entrance("Ruined Atoll -> Library", player).access_rule = lambda state: (state.has(grapple, player) or state.has(laurels, player)) and state.has(prayer, player, prayer_amount)
        multiworld.get_entrance("Overworld -> Spirit Arena", player).access_rule = lambda state: state.has(gold_hexagon, player, 20) if multiworld.hexagon_quest[player].value else state.has(prayer, player, prayer_amount) and state.has(red_hexagon, player) and state.has(green_hexagon, player) and state.has(blue_hexagon, player)
    else:
        multiworld.get_entrance("Overworld -> Beneath the Vault", player).access_rule = lambda state: state.has(lantern, player)
        multiworld.get_entrance("Lower Quarry -> Rooted Ziggurat", player).access_rule = lambda state: state.has(grapple, player)
        multiworld.get_entrance("Swamp -> Cathedral", player).access_rule = lambda state: state.has(laurels, player)
        multiworld.get_entrance("Ruined Atoll -> Library", player).access_rule = lambda state: state.has(grapple, player) or state.has(laurels, player)
        multiworld.get_entrance("Overworld -> Spirit Arena", player).access_rule = lambda state: state.has(gold_hexagon, player, 20) if multiworld.hexagon_quest[player].value else state.has(red_hexagon, player) and state.has(green_hexagon, player) and state.has(blue_hexagon, player)

    multiworld.get_entrance("Overworld -> Dark Tomb", player).access_rule = lambda state: state.has(lantern, player)
    multiworld.get_entrance("Overworld -> West Garden", player).access_rule = lambda state: state.has(laurels, player)
    multiworld.get_entrance("Overworld -> Eastern Vault Fortress", player).access_rule = lambda state: state.has(laurels, player)
    multiworld.get_entrance("East Forest -> Eastern Vault Fortress", player).access_rule = lambda state: state.has(laurels, player)
    multiworld.get_entrance("Bottom of the Well -> Dark Tomb", player).access_rule = lambda state: state.has(lantern, player)
    multiworld.get_entrance("West Garden -> Dark Tomb", player).access_rule = lambda state: state.has(lantern, player)
    multiworld.get_entrance("Eastern Vault Fortress -> Beneath the Vault", player).access_rule = lambda state: state.has(lantern, player)
    multiworld.get_entrance("Quarry -> Lower Quarry", player).access_rule = lambda state: state.has(mask, player)


def set_location_rules(multiworld: MultiWorld, player: int):
    laurels = "Hero's Laurels"
    grapple = "Magic Orb"
    ice_dagger = "Magic Dagger"
    fire_wand = "Magic Wand"
    lantern = "Lantern"
    fairies = "Fairy"
    coins = "Golden Coin"
    prayer = "Pages 24-25 (Prayer)"
    holy_cross = "Pages 42-43 (Holy Cross)"
    ice_rod = "Pages 52-53 (Ice Rod)"
    key = "Key"
    house_key = "Old House Key"
    vault_key = "Fortress Vault Key"

    prayer_amount = 1
    holy_cross_amount = 1
    ice_rod_amount = 1


    ability_shuffle = multiworld.ability_shuffling[player].value

    forbid_item(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player), fairies, player)

    if multiworld.hexagon_quest[player].value:
        prayer, holy_cross, ice_rod = ["Gold Hexagon", "Gold Hexagon", "Gold Hexagon"]
        prayer_amount = hexagon_quest_abilities["prayer"]
        holy_cross_amount = hexagon_quest_abilities["holy_cross"]
        ice_rod_amount = hexagon_quest_abilities["ice_rod"]

    # Ability Shuffle Exclusive Rules
    if ability_shuffle:
        set_rule(multiworld.get_location("Far Shore - Page Pickup", player), lambda state: state.has(prayer, player, prayer_amount))
        set_rule(multiworld.get_location("Fortress Courtyard - Chest Near Cave", player),
                 lambda state: state.has(prayer, player, prayer_amount) or state.has(laurels, player))
        set_rule(multiworld.get_location("Fortress Courtyard - Page Near Cave", player),
                 lambda state: state.has(prayer, player, prayer_amount) or state.has(laurels, player))
        set_rule(multiworld.get_location("East Forest - Dancing Fox Spirit Holy Cross", player),
                 lambda state: state.has(holy_cross, player, holy_cross_amount))
        set_rule(multiworld.get_location("Forest Grave Path - Holy Cross Code by Grave", player),
                 lambda state: state.has(holy_cross, player, holy_cross_amount))
        set_rule(multiworld.get_location("East Forest - Golden Obelisk Holy Cross", player),
                 lambda state: state.has(holy_cross, player, holy_cross_amount))
        set_rule(multiworld.get_location("Bottom of the Well - [Powered Secret Room] Chest", player),
                 lambda state: state.has(prayer, player, prayer_amount))
        set_rule(multiworld.get_location("West Garden - [North] Behind Holy Cross Door", player),
                 lambda state: state.has(holy_cross, player, holy_cross_amount))
        set_rule(multiworld.get_location("Library Hall - Holy Cross Chest", player),
                 lambda state: state.has(holy_cross, player, holy_cross_amount))
        set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Candles Holy Cross", player),
                 lambda state: state.has(holy_cross, player, holy_cross_amount))
        set_rule(multiworld.get_location("West Garden - [Central Highlands] Holy Cross (Blue Lines)", player),
                 lambda state: state.has(holy_cross, player, holy_cross_amount))
        set_rule(multiworld.get_location("Quarry - [Back Entrance] Bushes Holy Cross", player),
                 lambda state: state.has(holy_cross, player, holy_cross_amount))
        set_rule(multiworld.get_location("Cathedral - Secret Legend Trophy Chest", player),
                 lambda state: state.has(holy_cross, player, holy_cross_amount))

    # Overworld
    set_rule(multiworld.get_location("Overworld - [Southwest] Fountain Page", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] Grapple Chest Over Walkway", player),
             lambda state: state.has(grapple, player) or state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] West Beach Guarded By Turret 2", player),
             lambda state: state.has(grapple, player) or state.has(laurels, player))
    set_rule(multiworld.get_location("Far Shore - Secret Chest", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player, prayer_amount) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southeast] Page on Pillar by Swamp", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Old House - Normal Chest", player), lambda state: state.has(house_key, player))
    set_rule(multiworld.get_location("Old House - Holy Cross Chest", player),
             lambda state: state.has(house_key, player) and state.has(holy_cross,
                                                                      player) if ability_shuffle else state.has(
                 house_key, player))
    set_rule(multiworld.get_location("Old House - Shield Pickup", player), lambda state: state.has(house_key, player))
    set_rule(multiworld.get_location("Overworld - [Northwest] Page on Pillar by Dark Tomb", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] From West Garden", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [West] Chest After Bell", player),
             lambda state: state.has(laurels, player) or (state.has(lantern, player) and state.has_group("melee weapons", player, 2)))
    set_rule(multiworld.get_location("Overworld - [East] Grapple Chest", player),
             lambda state: state.has(grapple, player))
    set_rule(multiworld.get_location("Special Shop - Secret Page Pickup", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Sealed Temple - Holy Cross Chest", player),
             lambda state: state.has(laurels, player) or (state.has(lantern, player) and (
                         state.has_group("melee weapons", player, 2) or state.has(fire_wand, player))) and state.has(
                 holy_cross, player) if ability_shuffle else state.has(laurels, player) or (
                         state.has(lantern, player) and (
                             state.has_group("melee weapons", player, 2) or state.has(fire_wand, player))))
    set_rule(multiworld.get_location("Sealed Temple - Page Pickup", player),
             lambda state: state.has(laurels, player) or (
                         state.has(lantern, player) and state.has_group("melee weapons", player, 2)))
    set_rule(multiworld.get_location("Secret Gathering Place - 10 Fairy Reward", player),
             lambda state: state.has(fairies, player, 10))
    set_rule(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player),
             lambda state: state.has(fairies, player, 20))
    set_rule(multiworld.get_location("Coins in the Well - 3 Coins", player), lambda state: state.has(coins, player, 3))
    set_rule(multiworld.get_location("Coins in the Well - 6 Coins", player), lambda state: state.has(coins, player, 6))
    set_rule(multiworld.get_location("Coins in the Well - 10 Coins", player),
             lambda state: state.has(coins, player, 10))
    set_rule(multiworld.get_location("Coins in the Well - 15 Coins", player),
             lambda state: state.has(coins, player, 15))

    # East Forest
    set_rule(multiworld.get_location("East Forest - Lower Grapple Chest", player),
             lambda state: state.has(grapple, player))
    set_rule(multiworld.get_location("East Forest - Lower Dash Chest", player),
             lambda state: state.has(grapple, player) and state.has(laurels, player))
    set_rule(multiworld.get_location("East Forest - Ice Rod Grapple Chest", player), lambda state: (
                state.has(grapple, player) and state.has(ice_dagger, player) and state.has(fire_wand,
                                                                                           player) and state.has(
            ice_rod, ice_rod_amount, player)) if ability_shuffle else (
                state.has(grapple, player) and state.has(ice_dagger, player) and state.has(fire_wand, player)))

    # West Garden
    set_rule(multiworld.get_location("West Garden - [North] Across From Page Pickup", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [West] In Flooded Walkway", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [West Lowlands] Tree Holy Cross Chest", player),
             lambda state: state.has(laurels, player) and state.has(holy_cross,
                                                                    player) if ability_shuffle else state.has(laurels,
                                                                                                              player))
    set_rule(multiworld.get_location("West Garden - [East Lowlands] Page Behind Ice Dagger House", player),
             lambda state: (state.has(laurels, player) and state.has(prayer, player, prayer_amount)) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("West Garden - [Central Lowlands] Below Left Walkway", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [Central Highlands] After Garden Knight", player),
             lambda state: state.has_group("melee weapons", player, 2) or state.has(laurels, player))

    # Ruined Atoll
    set_rule(multiworld.get_location("Ruined Atoll - [West] Near Kevin Block", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Lower Chest", player),
             lambda state: state.has(laurels, player) or state.has(key, player))
    set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Upper Chest", player),
             lambda state: state.has(laurels, player) or state.has(key, player))

    # Frog's Domain
    set_rule(multiworld.get_location("Frog's Domain - Side Room Grapple Secret", player),
             lambda state: state.has(grapple, player) or state.has(laurels, player))
    set_rule(multiworld.get_location("Frog's Domain - Grapple Above Hot Tub", player),
             lambda state: state.has(grapple, player) or state.has(laurels, player))
    set_rule(multiworld.get_location("Frog's Domain - Escape Chest", player),
             lambda state: state.has(grapple, player) or state.has(laurels, player))

    # Eastern Vault Fortress
    set_rule(multiworld.get_location("Fortress Leaf Piles - Secret Chest", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Fortress Arena - Siege Engine/Vault Key Pickup", player),
             lambda state: (state.has_group("melee weapons", player, 2) and state.has(prayer, player, prayer_amount))
                 if ability_shuffle else state.has_group("melee weapons", player, 2))
    set_rule(multiworld.get_location("Fortress Arena - Hexagon Red", player), lambda state: (
                state.has(vault_key, player) and state.has(prayer, player, prayer_amount)) if ability_shuffle else state.has(vault_key,
                                                                                                              player))
    # Beneath the Vault
    set_rule(multiworld.get_location("Beneath the Fortress - Bridge", player),
             lambda state: state.has_group("melee weapons", player, 1) or state.has(fire_wand, player) or state.has(
                 laurels, player))

    # Quarry
    set_rule(multiworld.get_location("Quarry - [Central] Above Ladder Dash Chest", player),
             lambda state: state.has(laurels, player))

    # Swamp
    set_rule(multiworld.get_location("Cathedral Gauntlet - Gauntlet Reward", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Swamp - [Entrance] Above Entryway", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Swamp - [South Graveyard] Upper Walkway Dash Chest", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Swamp - [Outside Cathedral] Obscured Behind Memorial", player),
             lambda state: state.has(laurels, player))

    # Hero's Grave
    set_rule(multiworld.get_location("Hero's Grave - Tooth Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player, prayer_amount) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Mushroom Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player, prayer_amount) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Ash Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player, prayer_amount) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Flowers Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player, prayer_amount) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Effigy Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player, prayer_amount) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Feathers Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player, prayer_amount) if ability_shuffle else state.has(
                 laurels, player))
