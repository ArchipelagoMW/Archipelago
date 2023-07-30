from ..generic.Rules import set_rule, forbid_item
from BaseClasses import MultiWorld


def set_location_rules(multiworld: MultiWorld, player: int):
    laurels = "Hero's Laurels"
    grapple = "Magic Orb"
    ice_dagger = "Magic Dagger"
    fire_wand = "Magic Wand"
    lantern = "Lantern"
    stick = "Stick"
    sword = "Sword"
    fairies = "Fairy"
    coins = "Golden Coin"
    prayer = "Pages 24-25 (Prayer)"
    holy_cross = "Pages 42-43 (Holy Cross)"
    ice_combo = "Pages 52-53 (Ice Rod)"
    key = "Key"
    house_key = "Old House Key"
    vault_key = "Fortress Vault Key"

    ability_shuffle = multiworld.ability_shuffling[player].value

    forbid_item(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player), fairies, player)

    # Ability Shuffle Exclusive Rules
    if ability_shuffle:
        set_rule(multiworld.get_location("Far Shore - Page Pickup", player), lambda state: state.has(prayer, player))
        set_rule(multiworld.get_location("Fortress Courtyard - Chest Near Cave", player),
                 lambda state: state.has(prayer, player) or state.has(laurels, player))
        set_rule(multiworld.get_location("Fortress Courtyard - Page Near Cave", player),
                 lambda state: state.has(prayer, player) or state.has(laurels, player))
        set_rule(multiworld.get_location("East Forest - Dancing Fox Spirit Holy Cross", player),
                 lambda state: state.has(holy_cross, player))
        set_rule(multiworld.get_location("Forest Grave Path - Holy Cross Code by Grave", player),
                 lambda state: state.has(holy_cross, player))
        set_rule(multiworld.get_location("East Forest - Golden Obelisk Holy Cross", player),
                 lambda state: state.has(holy_cross, player))
        set_rule(multiworld.get_location("Bottom of the Well - [Powered Secret Room] Chest", player),
                 lambda state: state.has(prayer, player))
        set_rule(multiworld.get_location("West Garden - [North] Behind Holy Cross Door", player),
                 lambda state: state.has(holy_cross, player))
        set_rule(multiworld.get_location("Library Hall - Holy Cross Chest", player),
                 lambda state: state.has(holy_cross, player))
        set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Candles Holy Cross", player),
                 lambda state: state.has(holy_cross, player))
        set_rule(multiworld.get_location("West Garden - [Central Highlands] Holy Cross (Blue Lines)", player),
                 lambda state: state.has(holy_cross, player))
        set_rule(multiworld.get_location("Quarry - [Back Entrance] Bushes Holy Cross", player),
                 lambda state: state.has(holy_cross, player))
        set_rule(multiworld.get_location("Cathedral - Secret Legend Trophy Chest", player),
                 lambda state: state.has(holy_cross, player))

    # Overworld
    set_rule(multiworld.get_location("Overworld - [Southwest] Fountain Page", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] Grapple Chest Over Walkway", player),
             lambda state: state.has(grapple, player) or state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] West Beach Guarded By Turret 2", player),
             lambda state: state.has(grapple, player) or state.has(laurels, player))
    set_rule(multiworld.get_location("Far Shore - Secret Chest", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player) if ability_shuffle else state.has(
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
             lambda state: state.has(laurels, player) or (state.has(lantern, player) and state.has(sword, player)))
    set_rule(multiworld.get_location("Overworld - [East] Grapple Chest", player),
             lambda state: state.has(grapple, player))
    set_rule(multiworld.get_location("Special Shop - Secret Page Pickup", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Sealed Temple - Holy Cross Chest", player),
             lambda state: state.has(laurels, player) or (state.has(lantern, player) and (
                         state.has(stick, player) or state.has(sword, player) or state.has(fire_wand,
                                                                                           player))) and state.has(
                 holy_cross, player) if ability_shuffle else state.has(laurels, player) or (
                         state.has(lantern, player) and (
                             state.has(stick, player) or state.has(sword, player) or state.has(fire_wand, player))))
    set_rule(multiworld.get_location("Sealed Temple - Page Pickup", player),
             lambda state: state.has(laurels, player) or (
                         state.has(lantern, player) and (state.has(sword, player) or state.has(stick, player))))
    set_rule(multiworld.get_location("Secret Gathering Place - 10 Fairy Reward", player),
             lambda state: state.has(fairies, 10, player))
    set_rule(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player),
             lambda state: state.has(fairies, 20, player))
    set_rule(multiworld.get_location("Coins in the Well - 3 Coins", player), lambda state: state.has(coins, 3, player))
    set_rule(multiworld.get_location("Coins in the Well - 6 Coins", player), lambda state: state.has(coins, 6, player))
    set_rule(multiworld.get_location("Coins in the Well - 10 Coins", player),
             lambda state: state.has(coins, 10, player))
    set_rule(multiworld.get_location("Coins in the Well - 15 Coins", player),
             lambda state: state.has(coins, 15, player))

    # East Forest
    set_rule(multiworld.get_location("East Forest - Lower Grapple Chest", player),
             lambda state: state.has(grapple, player))
    set_rule(multiworld.get_location("East Forest - Lower Dash Chest", player),
             lambda state: state.has(grapple, player) and state.has(laurels, player))
    set_rule(multiworld.get_location("East Forest - Ice Rod Grapple Chest", player), lambda state: (
                state.has(grapple, player) and state.has(ice_dagger, player) and state.has(fire_wand,
                                                                                           player) and state.has(
            ice_combo, player)) if ability_shuffle else (
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
             lambda state: (state.has(laurels, player) and state.has(prayer, player)) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("West Garden - [Central Lowlands] Below Left Walkway", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [Central Highlands] After Garden Knight", player),
             lambda state: state.has(sword, player) or state.has(laurels, player))

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
             lambda state: (state.has(sword, player) and state.has(prayer, player)) if ability_shuffle else state.has(
                 sword, player))
    set_rule(multiworld.get_location("Fortress Arena - Hexagon Red", player), lambda state: (
                state.has(vault_key, player) and state.has(prayer, player)) if ability_shuffle else state.has(vault_key,
                                                                                                              player))
    # Beneath the Vault
    set_rule(multiworld.get_location("Beneath the Fortress - Bridge", player),
             lambda state: state.has(stick, player) or state.has(sword, player) or state.has(fire_wand,
                                                                                             player) or state.has(
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
             lambda state: state.has(laurels, player) and state.has(prayer, player) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Mushroom Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Ash Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Flowers Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Effigy Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player) if ability_shuffle else state.has(
                 laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Feathers Relic", player),
             lambda state: state.has(laurels, player) and state.has(prayer, player) if ability_shuffle else state.has(
                 laurels, player))
