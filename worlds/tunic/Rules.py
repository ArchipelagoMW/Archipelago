from ..generic.Rules import set_rule, forbid_item

def set_rules(tunic_world):
    player = tunic_world.player
    multiworld = tunic_world.multiworld

    laurels = lambda state: state.has("Hero's Laurels", player)
    grapple = lambda state: state.has("Magic Orb", player)
    ice_dagger = lambda state: state.has("Magic Dagger", player)
    fire_wand = lambda state: state.has("Magic Wand", player)
    lantern = lambda state: state.has("Lantern", player)
    mask = lambda state: state.has("Scavenger Mask", player)
    stick = lambda state: state.has("Stick", player)
    sword = lambda state: state.has("Sword", player)
    fairy_10 = lambda state: state.has("Fairy", 10, player)
    fairy_20 = lambda state: state.has("Fairy", 20, player)
    coins_3 = lambda state: state.has("Golden Coin", 3, player)
    coins_6 = lambda state: state.has("Golden Coin", 6, player)
    coins_10 = lambda state: state.has("Golden Coin", 10, player)
    coins_15 = lambda state: state.has("Golden Coin", 15, player)
    key = lambda state: state.has("Key", 2, player)
    house_key = lambda state: state.has("Old House Key", player)
    vault_key = lambda state: state.has("Fortress Vault Key", player)

    forbid_item(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player), "Fairy", player)

    if multiworld.ability_shuffling[player].value:
        set_ability_shuffle_rules(tunic_world)
    else:
        set_rule(multiworld.get_location("Cathedral Gauntlet - Gauntlet Reward", player), (laurels))
        set_rule(multiworld.get_location("East Forest - Lower Grapple Chest", player), (grapple))
        set_rule(multiworld.get_location("East Forest - Lower Dash Chest", player), (grapple and laurels))
        set_rule(multiworld.get_location("East Forest - Ice Rod Grapple Chest", player),
                 (grapple and ice_dagger and fire_wand))
        set_rule(multiworld.get_location("Overworld - [Southwest] Fountain Page", player), (laurels))
        set_rule(multiworld.get_location("Overworld - [Southwest] Grapple Chest Over Walkway", player),
                 (laurels) or (grapple))
        set_rule(multiworld.get_location("Overworld - [Southwest] West Beach Guarded By Turret 2", player),
                 (laurels) or (grapple))
        set_rule(multiworld.get_location("Far Shore - Secret Chest", player), (laurels))
        set_rule(multiworld.get_location("Overworld - [Southeast] Page on Pillar by Swamp", player), (laurels))
        set_rule(multiworld.get_location("Ruined Atoll - [West] Near Kevin Block", player), (laurels))
        set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Lower Chest", player), (laurels) or (key))
        set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Upper Chest", player), (laurels) or (key))
        set_rule(multiworld.get_location("Frog's Domain - Side Room Grapple Secret", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Frog's Domain - Grapple Above Hot Tub", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Frog's Domain - Escape Chest", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Library Hall - Holy Cross Chest", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Library Lab - Page 1", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Library Lab - Page 2", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Library Lab - Page 3", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Library Lab - Chest By Shrine 1", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Library Lab - Chest By Shrine 2", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Library Lab - Chest By Shrine 3", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Library Lab - Behind Chalkboard by Fuse", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Librarian - Hexagon Green", player), (grapple) or (laurels))
        set_rule(multiworld.get_location("Old House - Normal Chest", player), (house_key))
        set_rule(multiworld.get_location("Old House - Holy Cross Chest", player), (house_key))
        set_rule(multiworld.get_location("Old House - Shield Pickup", player), (house_key))
        set_rule(multiworld.get_location("Secret Gathering Place - 10 Fairy Reward", player), (fairy_10))
        set_rule(multiworld.get_location("Overworld - [Northwest] Page on Pillar by Dark Tomb", player), (laurels))
        set_rule(multiworld.get_location("Dark Tomb - Skulls Chest", player), (lantern))
        set_rule(multiworld.get_location("Dark Tomb - Spike Maze Upper Walkway", player), (lantern))
        set_rule(multiworld.get_location("Dark Tomb - Spike Maze Near Stairs", player), (lantern))
        set_rule(multiworld.get_location("Dark Tomb - Spike Maze Near Exit", player), (lantern))
        set_rule(multiworld.get_location("Dark Tomb - 1st Laser Room Obscured", player), (lantern))
        set_rule(multiworld.get_location("Dark Tomb - 1st Laser Room", player), (lantern))
        set_rule(multiworld.get_location("Dark Tomb - 2nd Laser Room", player), (lantern))
        set_rule(multiworld.get_location("Overworld Belltower - Chest", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("Overworld - [West] Near Gardens Entrance", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [North] Obscured Beneath Hero's Memorial", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [North] Behind Holy Cross Door", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [North] Page Pickup", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [North] Across From Page Pickup", player), (laurels))
        set_rule(multiworld.get_location("West Garden - [West] In Flooded Walkway", player), (laurels))
        set_rule(multiworld.get_location("West Garden - [West] Past Flooded Walkway", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [West Highlands] Upper Left Walkway", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [Central Lowlands] Passage Beneath Bridge", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [Central Lowlands] Chest Near Shortcut Bridge", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [West Lowlands] Tree Holy Cross Chest", player), (laurels))
        set_rule(multiworld.get_location("West Garden - [Central Lowlands] Chest Beneath Save Point", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [Central Lowlands] Chest Beneath Faeries", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [South Highlands] Secret Chest Beneath Fuse", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [Southeast Lowlands] Outside Cave", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden House - [Southeast Lowlands] Ice Dagger Pickup", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [East Lowlands] Page Behind Ice Dagger House", player),
                 (laurels))
        set_rule(multiworld.get_location("West Garden - [Central Lowlands] Below Left Walkway", player), (laurels))
        set_rule(multiworld.get_location("West Garden - [Central Highlands] Behind Guard Captain", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [Central Highlands] Holy Cross (Blue Lines)", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("West Garden - [Central Highlands] Top of Ladder Before Boss", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("Overworld - [Southwest] From West Garden", player), (laurels))
        set_rule(multiworld.get_location("West Garden - [Central Highlands] After Garden Knight", player),
                 (lantern and sword) or (laurels))
        set_rule(multiworld.get_location("Overworld - [West] Chest After Bell", player),
                 (laurels) or (lantern and sword))
        set_rule(multiworld.get_location("Sealed Temple - Holy Cross Chest", player),
                 (laurels and stick) or (laurels and fire_wand) or (lantern and sword))
        set_rule(multiworld.get_location("Sealed Temple - Page Pickup", player),
                 (laurels and stick) or (laurels and fire_wand) or (lantern and sword))
        set_rule(multiworld.get_location("Overworld - [East] Grapple Chest", player), (grapple))
        set_rule(multiworld.get_location("Beneath the Fortress - Obscured Behind Waterfall", player),
                 (lantern) or (lantern and laurels))
        set_rule(multiworld.get_location("Beneath the Fortress - Bridge", player),
                 (lantern and stick) or (lantern and sword) or (lantern and fire_wand) or (lantern and laurels))
        set_rule(multiworld.get_location("Beneath the Fortress - Cell Chest 1", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("Beneath the Fortress - Cell Chest 2", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("Beneath the Fortress - Back Room Chest", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Page Pickup", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Dark Room Chest 1", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Dark Room Chest 2", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Candles Holy Cross", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("Eastern Vault Fortress - [East Wing] Bombable Wall", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("Fortress Grave Path - Upper Walkway", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("Fortress Grave Path - Chest Right of Grave", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("Fortress Grave Path - Obscured Chest Left of Grave", player),
                 (lantern) or (laurels))
        set_rule(multiworld.get_location("Fortress Leaf Piles - Secret Chest", player), (laurels))
        set_rule(multiworld.get_location("Fortress East Shortcut - Chest Near Slimes", player), (lantern) or (laurels))
        set_rule(multiworld.get_location("Fortress Arena - Siege Engine/Vault Key Pickup", player),
                 (sword and lantern) or (sword and laurels))
        set_rule(multiworld.get_location("Fortress Arena - Hexagon Red", player),
                 (vault_key and lantern) or (vault_key and laurels))
        set_rule(multiworld.get_location("Special Shop - Secret Page Pickup", player), (laurels))
        set_rule(multiworld.get_location("Quarry - [West] Upper Area Near Waterfall", player), (mask))
        set_rule(multiworld.get_location("Quarry - [West] Near Shooting Range", player), (mask))
        set_rule(multiworld.get_location("Quarry - [West] Shooting Range Secret Path", player), (mask))
        set_rule(multiworld.get_location("Quarry - [West] Below Shooting Range", player), (mask))
        set_rule(multiworld.get_location("Quarry - [West] Lower Area Below Bridge", player), (mask))
        set_rule(multiworld.get_location("Quarry - [West] Lower Area Isolated Chest", player), (mask))
        set_rule(multiworld.get_location("Quarry - [West] Lower Area After Bridge", player), (mask))
        set_rule(multiworld.get_location("Quarry - [Lowlands] Below Broken Ladder", player), (mask))
        set_rule(multiworld.get_location("Quarry - [Lowlands] Upper Walkway", player), (mask))
        set_rule(multiworld.get_location("Quarry - [Lowlands] Near Elevator", player), (mask))
        set_rule(multiworld.get_location("Quarry - [Central] Above Ladder Dash Chest", player), (laurels))
        set_rule(multiworld.get_location("Rooted Ziggurat Upper - Near Bridge Switch", player), (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Upper - Beneath Bridge To Administrator", player),
                 (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Tower - Inside Tower", player), (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Lower - Near Corpses", player), (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Lower - Spider Ambush", player), (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Lower - Guarded By Double Turrets", player),
                 (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Lower - Guarded By Double Turrets 2", player),
                 (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Lower - After 2nd Double Turret Chest", player),
                 (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Lower - Left Of Checkpoint Before Fuse", player),
                 (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Lower - After Guarded Fuse", player), (grapple and mask))
        set_rule(multiworld.get_location("Rooted Ziggurat Lower - Hexagon Blue", player), (grapple and mask))
        set_rule(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player), (fairy_20))
        set_rule(multiworld.get_location("Swamp - [Entrance] Above Entryway", player), (laurels))
        set_rule(multiworld.get_location("Swamp - [South Graveyard] Upper Walkway Dash Chest", player), (laurels))
        set_rule(multiworld.get_location("Swamp - [Outside Cathedral] Obscured Behind Memorial", player), (laurels))
        set_rule(multiworld.get_location("Cathedral - [1F] Library", player), (laurels))
        set_rule(multiworld.get_location("Cathedral - [1F] Library Secret", player), (laurels))
        set_rule(multiworld.get_location("Cathedral - [1F] Guarded By Lasers", player), (laurels))
        set_rule(multiworld.get_location("Cathedral - [1F] Near Spikes", player), (laurels))
        set_rule(multiworld.get_location("Cathedral - [2F] Bird Room Secret", player), (laurels))
        set_rule(multiworld.get_location("Cathedral - [2F] Bird Room", player), (laurels))
        set_rule(multiworld.get_location("Cathedral - [2F] Entryway Upper Walkway", player), (laurels))
        set_rule(multiworld.get_location("Cathedral - [2F] Library", player), (laurels))
        set_rule(multiworld.get_location("Cathedral - [2F] Guarded By Lasers", player), (laurels))
        set_rule(multiworld.get_location("Coins in the Well - 3 Coins", player), (coins_3))
        set_rule(multiworld.get_location("Coins in the Well - 6 Coins", player), (coins_6))
        set_rule(multiworld.get_location("Coins in the Well - 10 Coins", player), (coins_10))
        set_rule(multiworld.get_location("Coins in the Well - 15 Coins", player), (coins_15))
        set_rule(multiworld.get_location("Hero's Grave - Tooth Relic", player), (laurels))
        set_rule(multiworld.get_location("Hero's Grave - Mushroom Relic", player), (laurels))
        set_rule(multiworld.get_location("Hero's Grave - Ash Relic", player), (laurels))
        set_rule(multiworld.get_location("Hero's Grave - Flowers Relic", player), (laurels))
        set_rule(multiworld.get_location("Hero's Grave - Effigy Relic", player), (laurels))
        set_rule(multiworld.get_location("Hero's Grave - Feathers Relic", player), (laurels))


def set_ability_shuffle_rules(tunic_world):
    player = tunic_world.player
    multiworld = tunic_world.multiworld

    laurels = lambda state: state.has("Hero's Laurels", player)
    grapple = lambda state: state.has("Magic Orb", player)
    ice_dagger = lambda state: state.has("Magic Dagger", player)
    fire_wand = lambda state: state.has("Magic Wand", player)
    lantern = lambda state: state.has("Lantern", player)
    mask = lambda state: state.has("Scavenger Mask", player)
    stick = lambda state: state.has("Stick", player)
    sword = lambda state: state.has("Sword", player)
    fairy_10 = lambda state: state.has("Fairy", 10, player)
    fairy_20 = lambda state: state.has("Fairy", 20, player)
    coins_3 = lambda state: state.has("Golden Coin", 3, player)
    coins_6 = lambda state: state.has("Golden Coin", 6, player)
    coins_10 = lambda state: state.has("Golden Coin", 10, player)
    coins_15 = lambda state: state.has("Golden Coin", 15, player)
    prayer = lambda state: state.has("Pages 24-25 (Prayer)", player)
    holy_cross = lambda state: state.has("Pages 42-43 (Holy Cross)", player)
    ice_combo = lambda state: state.has("Pages 52-53 (Ice Rod)", player)
    key = lambda state: state.has("Key", 2, player)
    house_key = lambda state: state.has("Old House Key", player)
    vault_key = lambda state: state.has("Fortress Vault Key", player)

    set_rule(multiworld.get_location("Cathedral Gauntlet - Gauntlet Reward", player), (laurels))
    set_rule(multiworld.get_location("Overworld - [South] Starting Platform Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Cube Cave - Holy Cross Chest", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [West] Windmill Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Southeast Cross Door - Chest 3", player), (holy_cross))
    set_rule(multiworld.get_location("Southeast Cross Door - Chest 2", player), (holy_cross))
    set_rule(multiworld.get_location("Southeast Cross Door - Chest 1", player), (holy_cross))
    set_rule(multiworld.get_location("Caustic Light Cave - Holy Cross Chest", player), (holy_cross))
    set_rule(multiworld.get_location("Ruined Passage - Holy Cross Chest", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [East] Weathervane Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("East Forest - Dancing Fox Spirit Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Forest Grave Path - Holy Cross Code by Grave", player), (holy_cross))
    set_rule(multiworld.get_location("East Forest - Golden Obelisk Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("East Forest - Lower Grapple Chest", player), (grapple))
    set_rule(multiworld.get_location("East Forest - Lower Dash Chest", player), (grapple and laurels))
    set_rule(multiworld.get_location("East Forest - Ice Rod Grapple Chest", player),
             (grapple and ice_dagger and fire_wand and ice_combo))
    set_rule(multiworld.get_location("Overworld - [Northeast] Flowers Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Patrol Cave - Holy Cross Chest", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [Northwest] Golden Obelisk Page", player), (holy_cross))
    set_rule(multiworld.get_location("Secret Gathering Place - Holy Cross Chest", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [West] Windchimes Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [West] Moss Wall Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Fountain Cross Door - Page Pickup", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [Southwest] Fountain Page", player), (laurels))
    set_rule(multiworld.get_location("Overworld - [Southwest] Fountain Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [Southwest] Grapple Chest Over Walkway", player),
             (laurels) or (grapple))
    set_rule(multiworld.get_location("Overworld - [Southwest] Flowers Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [Southwest] Haiku Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Hourglass Cave - Holy Cross Chest", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [Southwest] West Beach Guarded By Turret 2", player),
             (laurels) or (grapple))
    set_rule(multiworld.get_location("Far Shore - Page Pickup", player), (prayer))
    set_rule(multiworld.get_location("Far Shore - Secret Chest", player), (laurels and prayer))
    set_rule(multiworld.get_location("Maze Cave - Maze Room Holy Cross", player), (holy_cross))
    set_rule(multiworld.get_location("Overworld - [Southeast] Page on Pillar by Swamp", player), (laurels))
    set_rule(multiworld.get_location("Ruined Atoll - [West] Near Kevin Block", player), (laurels))
    set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Lower Chest", player), (laurels) or (key))
    set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Upper Chest", player), (laurels) or (key))
    set_rule(multiworld.get_location("Frog's Domain - Side Room Grapple Secret", player), (grapple) or (laurels))
    set_rule(multiworld.get_location("Frog's Domain - Grapple Above Hot Tub", player), (grapple) or (laurels))
    set_rule(multiworld.get_location("Frog's Domain - Escape Chest", player), (grapple) or (laurels))
    set_rule(multiworld.get_location("Library Hall - Holy Cross Chest", player),
             (grapple and prayer and holy_cross) or (laurels and prayer and holy_cross))
    set_rule(multiworld.get_location("Library Lab - Page 1", player), (grapple and prayer) or (laurels and prayer))
    set_rule(multiworld.get_location("Library Lab - Page 2", player), (grapple and prayer) or (laurels and prayer))
    set_rule(multiworld.get_location("Library Lab - Page 3", player), (grapple and prayer) or (laurels and prayer))
    set_rule(multiworld.get_location("Library Lab - Chest By Shrine 1", player),
             (grapple and prayer) or (laurels and prayer))
    set_rule(multiworld.get_location("Library Lab - Chest By Shrine 2", player),
             (grapple and prayer) or (laurels and prayer))
    set_rule(multiworld.get_location("Library Lab - Chest By Shrine 3", player),
             (grapple and prayer) or (laurels and prayer))
    set_rule(multiworld.get_location("Library Lab - Behind Chalkboard by Fuse", player),
             (grapple and prayer) or (laurels and prayer))
    set_rule(multiworld.get_location("Librarian - Hexagon Green", player), (grapple and prayer) or (laurels and prayer))
    set_rule(multiworld.get_location("Old House - Normal Chest", player), (house_key))
    set_rule(multiworld.get_location("Old House - Holy Cross Chest", player), (house_key and holy_cross))
    set_rule(multiworld.get_location("Old House - Shield Pickup", player), (house_key))
    set_rule(multiworld.get_location("Old House - Holy Cross Door Page", player), (holy_cross))
    set_rule(multiworld.get_location("Secret Gathering Place - 10 Fairy Reward", player), (fairy_10))
    set_rule(multiworld.get_location("Overworld - [Northwest] Page on Pillar by Dark Tomb", player), (laurels))
    set_rule(multiworld.get_location("Bottom of the Well - [Powered Secret Room] Chest", player), (prayer))
    set_rule(multiworld.get_location("Dark Tomb - Skulls Chest", player), (lantern))
    set_rule(multiworld.get_location("Dark Tomb - Spike Maze Upper Walkway", player), (lantern))
    set_rule(multiworld.get_location("Dark Tomb - Spike Maze Near Stairs", player), (lantern))
    set_rule(multiworld.get_location("Dark Tomb - Spike Maze Near Exit", player), (lantern))
    set_rule(multiworld.get_location("Dark Tomb - 1st Laser Room Obscured", player), (lantern))
    set_rule(multiworld.get_location("Dark Tomb - 1st Laser Room", player), (lantern))
    set_rule(multiworld.get_location("Dark Tomb - 2nd Laser Room", player), (lantern))
    set_rule(multiworld.get_location("Overworld Belltower - Chest", player), (lantern) or (laurels))
    set_rule(multiworld.get_location("Overworld - [West] Near Gardens Entrance", player), (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [North] Obscured Beneath Hero's Memorial", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [North] Behind Holy Cross Door", player),
             (lantern and holy_cross) or (laurels and holy_cross))
    set_rule(multiworld.get_location("West Garden - [North] Page Pickup", player), (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [North] Across From Page Pickup", player), (laurels))
    set_rule(multiworld.get_location("West Garden - [West] In Flooded Walkway", player), (laurels))
    set_rule(multiworld.get_location("West Garden - [West] Past Flooded Walkway", player), (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [West Highlands] Upper Left Walkway", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [Central Lowlands] Passage Beneath Bridge", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [Central Lowlands] Chest Near Shortcut Bridge", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [West Lowlands] Tree Holy Cross Chest", player),
             (laurels and holy_cross))
    set_rule(multiworld.get_location("West Garden - [Central Lowlands] Chest Beneath Save Point", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [Central Lowlands] Chest Beneath Faeries", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [South Highlands] Secret Chest Beneath Fuse", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [Southeast Lowlands] Outside Cave", player), (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden House - [Southeast Lowlands] Ice Dagger Pickup", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [East Lowlands] Page Behind Ice Dagger House", player),
             (laurels and prayer))
    set_rule(multiworld.get_location("West Garden - [Central Lowlands] Below Left Walkway", player), (laurels))
    set_rule(multiworld.get_location("West Garden - [Central Highlands] Behind Guard Captain", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("West Garden - [Central Highlands] Holy Cross (Blue Lines)", player),
             (lantern and holy_cross) or (laurels and holy_cross))
    set_rule(multiworld.get_location("West Garden - [Central Highlands] Top of Ladder Before Boss", player),
             (lantern) or (laurels))
    set_rule(multiworld.get_location("Overworld - [Southwest] From West Garden", player), (laurels))
    set_rule(multiworld.get_location("West Garden - [Central Highlands] After Garden Knight", player),
             (lantern and sword) or (laurels))
    set_rule(multiworld.get_location("Overworld - [West] Chest After Bell", player), (laurels) or (lantern and sword))
    set_rule(multiworld.get_location("Sealed Temple - Holy Cross Chest", player),
             (laurels and stick and holy_cross) or (laurels and fire_wand and holy_cross) or (
                     lantern and sword and holy_cross))
    set_rule(multiworld.get_location("Sealed Temple - Page Pickup", player),
             (laurels and stick) or (laurels and fire_wand) or (lantern and sword))
    set_rule(multiworld.get_location("Overworld - [East] Grapple Chest", player), (grapple))
    set_rule(multiworld.get_location("Fortress Courtyard - Chest Near Cave", player), (prayer) or (laurels))
    set_rule(multiworld.get_location("Fortress Courtyard - Page Near Cave", player), (prayer) or (laurels))
    set_rule(multiworld.get_location("Beneath the Fortress - Obscured Behind Waterfall", player),
             (lantern and prayer) or (lantern and laurels))
    set_rule(multiworld.get_location("Beneath the Fortress - Bridge", player),
             (lantern and stick and prayer) or (lantern and sword and prayer) or (lantern and fire_wand and prayer) or (
                     lantern and laurels))
    set_rule(multiworld.get_location("Beneath the Fortress - Cell Chest 1", player), (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Beneath the Fortress - Cell Chest 2", player), (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Beneath the Fortress - Back Room Chest", player),
             (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Page Pickup", player),
             (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Dark Room Chest 1", player),
             (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Dark Room Chest 2", player),
             (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Eastern Vault Fortress - [West Wing] Candles Holy Cross", player),
             (lantern and prayer and holy_cross) or (laurels and holy_cross))
    set_rule(multiworld.get_location("Eastern Vault Fortress - [East Wing] Bombable Wall", player),
             (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Fortress Grave Path - Upper Walkway", player), (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Fortress Grave Path - Chest Right of Grave", player),
             (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Fortress Grave Path - Obscured Chest Left of Grave", player),
             (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Fortress Leaf Piles - Secret Chest", player), (laurels))
    set_rule(multiworld.get_location("Fortress East Shortcut - Chest Near Slimes", player),
             (lantern and prayer) or (laurels))
    set_rule(multiworld.get_location("Fortress Arena - Siege Engine/Vault Key Pickup", player),
             (sword and lantern and prayer) or (sword and laurels and prayer))
    set_rule(multiworld.get_location("Fortress Arena - Hexagon Red", player),
             (vault_key and lantern and prayer) or (vault_key and laurels and prayer))
    set_rule(multiworld.get_location("Special Shop - Secret Page Pickup", player), (laurels))
    set_rule(multiworld.get_location("Top of the Mountain - Page At The Peak", player), (holy_cross))
    set_rule(multiworld.get_location("Quarry - [Back Entrance] Bushes Holy Cross", player), (holy_cross))

    set_rule(multiworld.get_location("Quarry - [West] Upper Area Near Waterfall", player), (mask))
    set_rule(multiworld.get_location("Quarry - [West] Near Shooting Range", player), (mask))
    set_rule(multiworld.get_location("Quarry - [West] Shooting Range Secret Path", player), (mask))
    set_rule(multiworld.get_location("Quarry - [West] Below Shooting Range", player), (mask))
    set_rule(multiworld.get_location("Quarry - [West] Lower Area Below Bridge", player), (mask))
    set_rule(multiworld.get_location("Quarry - [West] Lower Area Isolated Chest", player), (mask))
    set_rule(multiworld.get_location("Quarry - [West] Lower Area After Bridge", player), (mask))
    set_rule(multiworld.get_location("Quarry - [Lowlands] Below Broken Ladder", player), (mask))
    set_rule(multiworld.get_location("Quarry - [Lowlands] Upper Walkway", player), (mask))
    set_rule(multiworld.get_location("Quarry - [Lowlands] Near Elevator", player), (mask))

    set_rule(multiworld.get_location("Quarry - [Central] Above Ladder Dash Chest", player), (laurels))
    set_rule(multiworld.get_location("Rooted Ziggurat Upper - Near Bridge Switch", player),
             (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Upper - Beneath Bridge To Administrator", player),
             (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Tower - Inside Tower", player), (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - Near Corpses", player), (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - Spider Ambush", player), (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - Guarded By Double Turrets", player),
             (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - Guarded By Double Turrets 2", player),
             (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - After 2nd Double Turret Chest", player),
             (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - Left Of Checkpoint Before Fuse", player),
             (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - After Guarded Fuse", player),
             (grapple and mask and prayer))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - Hexagon Blue", player), (grapple and mask and prayer))
    set_rule(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player), (fairy_20))
    set_rule(multiworld.get_location("Swamp - [Entrance] Above Entryway", player), (laurels))
    set_rule(multiworld.get_location("Swamp - [South Graveyard] Upper Walkway Dash Chest", player), (laurels))
    set_rule(multiworld.get_location("Swamp - [Outside Cathedral] Obscured Behind Memorial", player), (laurels))
    set_rule(multiworld.get_location("Cathedral - Secret Legend Trophy Chest", player), (holy_cross))
    set_rule(multiworld.get_location("Cathedral - [1F] Library", player), (laurels and prayer))
    set_rule(multiworld.get_location("Cathedral - [1F] Library Secret", player), (laurels and prayer))
    set_rule(multiworld.get_location("Cathedral - [1F] Guarded By Lasers", player), (laurels and prayer))
    set_rule(multiworld.get_location("Cathedral - [1F] Near Spikes", player), (laurels and prayer))
    set_rule(multiworld.get_location("Cathedral - [2F] Bird Room Secret", player), (laurels and prayer))
    set_rule(multiworld.get_location("Cathedral - [2F] Bird Room", player), (laurels and prayer))
    set_rule(multiworld.get_location("Cathedral - [2F] Entryway Upper Walkway", player), (laurels and prayer))
    set_rule(multiworld.get_location("Cathedral - [2F] Library", player), (laurels and prayer))
    set_rule(multiworld.get_location("Cathedral - [2F] Guarded By Lasers", player), (laurels and prayer))
    set_rule(multiworld.get_location("Coins in the Well - 3 Coins", player), (coins_3))
    set_rule(multiworld.get_location("Coins in the Well - 6 Coins", player), (coins_6))
    set_rule(multiworld.get_location("Coins in the Well - 10 Coins", player), (coins_10))
    set_rule(multiworld.get_location("Coins in the Well - 15 Coins", player), (coins_15))
    set_rule(multiworld.get_location("Hero's Grave - Tooth Relic", player), (laurels and prayer))
    set_rule(multiworld.get_location("Hero's Grave - Mushroom Relic", player), (laurels and prayer))
    set_rule(multiworld.get_location("Hero's Grave - Ash Relic", player), (laurels and prayer))
    set_rule(multiworld.get_location("Hero's Grave - Flowers Relic", player), (laurels and prayer))
    set_rule(multiworld.get_location("Hero's Grave - Effigy Relic", player), (laurels and prayer))
    set_rule(multiworld.get_location("Hero's Grave - Feathers Relic", player), (laurels and prayer))

