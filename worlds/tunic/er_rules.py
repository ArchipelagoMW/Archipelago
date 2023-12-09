from typing import Dict, TYPE_CHECKING
from worlds.generic.Rules import set_rule, forbid_item
from .rules import has_ability, has_sword
from BaseClasses import Region, CollectionState

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
ice_rod = "Pages 52-53 (Ice Rod)"
key = "Key"
house_key = "Old House Key"
vault_key = "Fortress Vault Key"
mask = "Scavenger Mask"
red_hexagon = "Red Questagon"
green_hexagon = "Green Questagon"
blue_hexagon = "Blue Questagon"
gold_hexagon = "Gold Questagon"


def has_stick(state: CollectionState, player: int) -> bool:
    return state.has("Stick", player) or state.has("Sword Upgrade", player, 1) or state.has("Sword", player)


def set_er_region_rules(world: "TunicWorld", ability_unlocks: Dict[str, int], regions: Dict[str, Region]) -> None:
    player = world.player
    options = world.options

    regions["Menu"].connect(
        connecting_region=regions["Overworld"])

    # Overworld
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Holy Cross"],
        rule=lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Belltower"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld Belltower"].connect(
        connecting_region=regions["Overworld"])

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Ruined Passage Door"],
        rule=lambda state: state.has(key, player, 2))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Laurels"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld Laurels"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has(laurels, player))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Old House Door"],
        rule=lambda state: state.has(house_key, player))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Southeast Cross Door"],
        rule=lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    regions["Overworld Southeast Cross Door"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Fountain Cross Door"],
        rule=lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    regions["Overworld Fountain Cross Door"].connect(
        connecting_region=regions["Overworld"])

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Town Portal"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Overworld Town Portal"].connect(
        connecting_region=regions["Overworld"])

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Spawn Portal"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Overworld Spawn Portal"].connect(
        connecting_region=regions["Overworld"])

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Temple Door"],
        name="Overworld Temple Door",
        rule=lambda state: (has_stick(state, player) or state.has(fire_wand, player)))

    # Overworld side areas
    regions["Old House Front"].connect(
        connecting_region=regions["Old House Back"])

    regions["Sealed Temple"].connect(
        connecting_region=regions["Sealed Temple Rafters"])
    regions["Sealed Temple Rafters"].connect(
        connecting_region=regions["Sealed Temple"],
        rule=lambda state: state.has(laurels, player))

    regions["Furnace Walking Path"].connect(
        connecting_region=regions["Furnace Ladder Area"],
        rule=lambda state: state.has(laurels, player))
    regions["Furnace Ladder Area"].connect(
        connecting_region=regions["Furnace Walking Path"],
        rule=lambda state: state.has(laurels, player))

    regions["Furnace Walking Path"].connect(
        connecting_region=regions["Furnace Fuse"],
        rule=lambda state: state.has(laurels, player))
    regions["Furnace Fuse"].connect(
        connecting_region=regions["Furnace Walking Path"],
        rule=lambda state: state.has(laurels, player))

    regions["Furnace Fuse"].connect(
        connecting_region=regions["Furnace Ladder Area"],
        rule=lambda state: state.has(laurels, player))
    regions["Furnace Ladder Area"].connect(
        connecting_region=regions["Furnace Fuse"],
        rule=lambda state: state.has(laurels, player))

    # East Forest
    regions["Forest Belltower Upper"].connect(
        connecting_region=regions["Forest Belltower Main"])

    regions["Forest Belltower Main"].connect(
        connecting_region=regions["Forest Belltower Lower"])

    regions["East Forest"].connect(
        connecting_region=regions["East Forest Dance Fox Spot"],
        rule=lambda state: state.has(laurels, player))
    regions["East Forest Dance Fox Spot"].connect(
        connecting_region=regions["East Forest"],
        rule=lambda state: state.has(laurels, player))

    regions["East Forest"].connect(
        connecting_region=regions["East Forest Portal"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["East Forest Portal"].connect(
        connecting_region=regions["East Forest"])

    regions["Guard House 1 East"].connect(
        connecting_region=regions["Guard House 1 West"])
    regions["Guard House 1 West"].connect(
        connecting_region=regions["Guard House 1 East"],
        rule=lambda state: state.has(laurels, player))

    regions["Forest Grave Path Upper"].connect(
        connecting_region=regions["Forest Grave Path Main"],
        rule=lambda state: state.has(laurels, player))
    regions["Forest Grave Path Main"].connect(
        connecting_region=regions["Forest Grave Path Upper"],
        rule=lambda state: state.has(laurels, player))

    regions["Forest Grave Path Main"].connect(
        connecting_region=regions["Forest Grave Path by Grave"])

    regions["Forest Grave Path by Grave"].connect(
        connecting_region=regions["Forest Hero's Grave"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Forest Hero's Grave"].connect(
        connecting_region=regions["Forest Grave Path by Grave"])

    # Bottom of the Well and Dark Tomb
    regions["Bottom of the Well Front"].connect(
        connecting_region=regions["Bottom of the Well Main"],
        rule=lambda state: has_stick(state, player))
    regions["Bottom of the Well Main"].connect(
        connecting_region=regions["Bottom of the Well Front"],
        rule=lambda state: has_stick(state, player))

    regions["Bottom of the Well Back"].connect(
        connecting_region=regions["Bottom of the Well Main"],
        rule=lambda state: has_stick(state, player))
    regions["Bottom of the Well Main"].connect(
        connecting_region=regions["Bottom of the Well Back"],
        rule=lambda state: has_stick(state, player))

    regions["Well Boss"].connect(
        connecting_region=regions["Dark Tomb Checkpoint"])
    regions["Dark Tomb Checkpoint"].connect(
        connecting_region=regions["Well Boss"],
        rule=lambda state: state.has(laurels, player))

    regions["Dark Tomb Entry Point"].connect(
        connecting_region=regions["Dark Tomb Main"],
        rule=lambda state: state.has(lantern, player))
    regions["Dark Tomb Main"].connect(
        connecting_region=regions["Dark Tomb Entry Point"],
        rule=lambda state: state.has(lantern, player))

    regions["Dark Tomb Main"].connect(
        connecting_region=regions["Dark Tomb Dark Exit"],
        rule=lambda state: state.has(lantern, player))
    regions["Dark Tomb Dark Exit"].connect(
        connecting_region=regions["Dark Tomb Main"],
        rule=lambda state: state.has(lantern, player))

    # West Garden
    regions["West Garden Laurels Exit"].connect(
        connecting_region=regions["West Garden"],
        rule=lambda state: state.has(laurels, player))
    regions["West Garden"].connect(
        connecting_region=regions["West Garden Laurels Exit"],
        rule=lambda state: state.has(laurels, player))

    regions["West Garden after Boss"].connect(
        connecting_region=regions["West Garden"],
        rule=lambda state: state.has(laurels, player))
    regions["West Garden"].connect(
        connecting_region=regions["West Garden after Boss"],
        rule=lambda state: state.has(laurels, player) or has_sword(state, player))

    regions["West Garden"].connect(
        connecting_region=regions["West Garden Hero's Grave"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["West Garden Hero's Grave"].connect(
        connecting_region=regions["West Garden"])

    # Atoll and Frog's Domain
    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Lower Entry Area"],
        rule=lambda state: state.has(laurels, player))
    regions["Ruined Atoll Lower Entry Area"].connect(
        connecting_region=regions["Ruined Atoll"],
        rule=lambda state: state.has(laurels, player) or state.has(grapple, player))

    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Frog Mouth"],
        rule=lambda state: state.has(laurels, player) or state.has(grapple, player))
    regions["Ruined Atoll Frog Mouth"].connect(
        connecting_region=regions["Ruined Atoll"],
        rule=lambda state: state.has(laurels, player) or state.has(grapple, player))

    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Portal"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Ruined Atoll Portal"].connect(
        connecting_region=regions["Ruined Atoll"])

    regions["Frog's Domain"].connect(
        connecting_region=regions["Frog's Domain Back"],
        rule=lambda state: state.has(grapple, player))

    # Library
    regions["Library Exterior Tree"].connect(
        connecting_region=regions["Library Exterior Ladder"],
        rule=lambda state: state.has(grapple, player) or state.has(laurels, player))
    regions["Library Exterior Ladder"].connect(
        connecting_region=regions["Library Exterior Tree"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks)
        and (state.has(grapple, player) or state.has(laurels, player)))

    regions["Library Hall"].connect(
        connecting_region=regions["Library Hero's Grave"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Library Hero's Grave"].connect(
        connecting_region=regions["Library Hall"])

    regions["Library Lab Lower"].connect(
        connecting_region=regions["Library Lab"],
        rule=lambda state: state.has(laurels, player) or state.has(grapple, player))
    regions["Library Lab"].connect(
        connecting_region=regions["Library Lab Lower"],
        rule=lambda state: state.has(laurels, player))

    regions["Library Lab"].connect(
        connecting_region=regions["Library Portal"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Library Portal"].connect(
        connecting_region=regions["Library Lab"])

    # Eastern Vault Fortress
    regions["Fortress Exterior from East Forest"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"],
        rule=lambda state: state.has(laurels, player) or state.has(grapple, player))
    regions["Fortress Exterior from Overworld"].connect(
        connecting_region=regions["Fortress Exterior from East Forest"],
        rule=lambda state: state.has(laurels, player))

    regions["Fortress Exterior from East Forest"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"],
        rule=lambda state: state.has(laurels, player) or state.has(grapple, player))
    regions["Fortress Exterior from Overworld"].connect(
        connecting_region=regions["Fortress Exterior from East Forest"],
        rule=lambda state: state.has(laurels, player))

    regions["Fortress Exterior near cave"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"],
        rule=lambda state: state.has(laurels, player))
    regions["Fortress Exterior from Overworld"].connect(
        connecting_region=regions["Fortress Exterior near cave"],
        rule=lambda state: state.has(laurels, player) or has_ability(state, player, prayer, options, ability_unlocks))

    regions["Fortress Courtyard"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"],
        rule=lambda state: state.has(laurels, player))
    regions["Fortress Exterior from Overworld"].connect(
        connecting_region=regions["Fortress Courtyard"],
        rule=lambda state: state.has(laurels, player))

    regions["Fortress Courtyard Upper"].connect(
        connecting_region=regions["Fortress Courtyard"])

    regions["Fortress Courtyard Upper"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"])

    regions["Beneath the Vault Front"].connect(
        connecting_region=regions["Beneath the Vault Back"],
        rule=lambda state: state.has(lantern, player))
    regions["Beneath the Vault Back"].connect(
        connecting_region=regions["Beneath the Vault Front"])

    regions["Fortress East Shortcut Upper"].connect(
        connecting_region=regions["Fortress East Shortcut Lower"])

    regions["Eastern Vault Fortress"].connect(
        connecting_region=regions["Eastern Vault Fortress Gold Door"],
        name="Fortress Gold Door",
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))

    regions["Fortress Grave Path"].connect(
        connecting_region=regions["Fortress Grave Path Dusty Entrance"],
        rule=lambda state: state.has(laurels, player))
    regions["Fortress Grave Path Dusty Entrance"].connect(
        connecting_region=regions["Fortress Grave Path"],
        rule=lambda state: state.has(laurels, player))

    regions["Fortress Grave Path"].connect(
        connecting_region=regions["Fortress Hero's Grave"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Fortress Hero's Grave"].connect(
        connecting_region=regions["Fortress Grave Path"])

    regions["Fortress Arena"].connect(
        connecting_region=regions["Fortress Arena Portal"],
        name="Fortress Arena to Fortress Portal",
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Fortress Arena Portal"].connect(
        connecting_region=regions["Fortress Arena"])

    # Quarry
    regions["Lower Mountain"].connect(
        connecting_region=regions["Lower Mountain Stairs"],
        rule=lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    regions["Lower Mountain Stairs"].connect(
        connecting_region=regions["Lower Mountain"],
        rule=lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))

    regions["Quarry Entry"].connect(
        connecting_region=regions["Quarry Portal"],
        name="Quarry to Quarry Portal",
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks) and state.has(grapple, player))
    regions["Quarry Portal"].connect(
        connecting_region=regions["Quarry Entry"])

    regions["Quarry Entry"].connect(
        connecting_region=regions["Quarry"],
        rule=lambda state: state.has(fire_wand, player) or has_sword(state, player))
    regions["Quarry"].connect(
        connecting_region=regions["Quarry Entry"])

    regions["Quarry Back"].connect(
        connecting_region=regions["Quarry"],
        rule=lambda state: state.has(fire_wand, player) or has_sword(state, player))
    regions["Quarry"].connect(
        connecting_region=regions["Quarry Back"])

    regions["Quarry Monastery Entry"].connect(
        connecting_region=regions["Quarry"],
        rule=lambda state: state.has(fire_wand, player) or has_sword(state, player))
    regions["Quarry"].connect(
        connecting_region=regions["Quarry Monastery Entry"])

    regions["Monastery Rope"].connect(
        connecting_region=regions["Quarry Back"])

    regions["Quarry"].connect(
        connecting_region=regions["Lower Quarry"],
        rule=lambda state: state.has(mask, player))

    regions["Lower Quarry"].connect(
        connecting_region=regions["Lower Quarry Zig Door"],
        name="Quarry to Zig Door",
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks) and state.has(grapple, player))

    regions["Monastery Front"].connect(
        connecting_region=regions["Monastery Back"])
    regions["Monastery Back"].connect(
        connecting_region=regions["Monastery Front"],
        rule=lambda state: state.has(laurels, player))

    regions["Monastery Back"].connect(
        connecting_region=regions["Monastery Hero's Grave"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Monastery Hero's Grave"].connect(
        connecting_region=regions["Monastery Back"])

    # Ziggurat
    regions["Rooted Ziggurat Upper Entry"].connect(
        connecting_region=regions["Rooted Ziggurat Upper Front"])

    regions["Rooted Ziggurat Upper Front"].connect(
        connecting_region=regions["Rooted Ziggurat Upper Back"],
        rule=lambda state: state.has(laurels, player) or has_sword(state, player))
    regions["Rooted Ziggurat Upper Back"].connect(
        connecting_region=regions["Rooted Ziggurat Upper Front"],
        rule=lambda state: state.has(laurels, player))

    regions["Rooted Ziggurat Middle Top"].connect(
        connecting_region=regions["Rooted Ziggurat Middle Bottom"])

    regions["Rooted Ziggurat Lower Front"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Back"],
        rule=lambda state: state.has(laurels, player)
        or (has_sword(state, player) and has_ability(state, player, prayer, options, ability_unlocks)))
    regions["Rooted Ziggurat Lower Back"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Front"],
        rule=lambda state: state.has(laurels, player))

    regions["Rooted Ziggurat Lower Back"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room Entrance"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Rooted Ziggurat Portal Room Entrance"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Back"])

    regions["Rooted Ziggurat Portal"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room Exit"],
        name="Zig Portal Room Exit",
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Rooted Ziggurat Portal Room Exit"].connect(
        connecting_region=regions["Rooted Ziggurat Portal"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))

    # Swamp and Cathedral
    regions["Swamp"].connect(
        connecting_region=regions["Swamp to Cathedral Main Entrance"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))

    regions["Swamp"].connect(
        connecting_region=regions["Swamp to Cathedral Treasure Room"],
        rule=lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    regions["Swamp to Cathedral Treasure Room"].connect(
        connecting_region=regions["Swamp"])

    regions["Back of Swamp"].connect(
        connecting_region=regions["Back of Swamp Laurels Area"],
        rule=lambda state: state.has(laurels, player))
    regions["Back of Swamp Laurels Area"].connect(
        connecting_region=regions["Back of Swamp"],
        rule=lambda state: state.has(laurels, player))

    regions["Back of Swamp"].connect(
        connecting_region=regions["Swamp Hero's Grave"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Swamp Hero's Grave"].connect(
        connecting_region=regions["Back of Swamp"])

    regions["Cathedral Gauntlet Checkpoint"].connect(
        connecting_region=regions["Cathedral Gauntlet"])

    regions["Cathedral Gauntlet"].connect(
        connecting_region=regions["Cathedral Gauntlet Exit"],
        rule=lambda state: state.has(laurels, player))
    regions["Cathedral Gauntlet Exit"].connect(
        connecting_region=regions["Cathedral Gauntlet"],
        rule=lambda state: state.has(laurels, player))

    # Far Shore
    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Spawn"],
        rule=lambda state: state.has(laurels, player))
    regions["Far Shore to Spawn"].connect(
        connecting_region=regions["Far Shore"],
        rule=lambda state: state.has(laurels, player))

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to East Forest"],
        rule=lambda state: state.has(laurels, player))
    regions["Far Shore to East Forest"].connect(
        connecting_region=regions["Far Shore"],
        rule=lambda state: state.has(laurels, player))

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to West Garden"],
        name="Far Shore to West Garden",
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Far Shore to West Garden"].connect(
        connecting_region=regions["Far Shore"])

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Quarry"],
        name="Far Shore to Quarry",
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks) and state.has(grapple, player))
    regions["Far Shore to Quarry"].connect(
        connecting_region=regions["Far Shore"])

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Fortress"],
        name="Far Shore to Fortress",
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Far Shore to Fortress"].connect(
        connecting_region=regions["Far Shore"])

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Library"],
        name="Far Shore to Library",
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Far Shore to Library"].connect(
        connecting_region=regions["Far Shore"])

    # Misc
    regions["Shop Entrance 1"].connect(
        connecting_region=regions["Shop"])
    regions["Shop Entrance 2"].connect(
        connecting_region=regions["Shop"])
    regions["Shop Entrance 3"].connect(
        connecting_region=regions["Shop"])
    regions["Shop Entrance 4"].connect(
        connecting_region=regions["Shop"])
    regions["Shop Entrance 5"].connect(
        connecting_region=regions["Shop"])
    regions["Shop Entrance 6"].connect(
        connecting_region=regions["Shop"])

    regions["Spirit Arena"].connect(
        connecting_region=regions["Spirit Arena Victory"],
        rule=lambda state: (state.has(gold_hexagon, player, world.options.hexagon_goal.value) if
                            world.options.hexagon_quest else
                            state.has_all({red_hexagon, green_hexagon, blue_hexagon}, player)))


def set_er_location_rules(world: "TunicWorld", ability_unlocks: Dict[str, int]) -> None:
    player = world.player
    multiworld = world.multiworld
    options = world.options
    forbid_item(multiworld.get_location("Secret Gathering Place - 20 Fairy Reward", player), fairies, player)

    # Ability Shuffle Exclusive Rules
    set_rule(multiworld.get_location("East Forest - Dancing Fox Spirit Holy Cross", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Forest Grave Path - Holy Cross Code by Grave", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("East Forest - Golden Obelisk Holy Cross", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Bottom of the Well - [Powered Secret Room] Chest", player),
             lambda state: (has_ability(state, player, prayer, options, ability_unlocks)
             and state.can_reach(multiworld.get_region("Furnace Fuse", player))))
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
    set_rule(multiworld.get_location("Overworld - [Southwest] Grapple Chest Over Walkway", player),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] West Beach Guarded By Turret 2", player),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] From West Garden", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southeast] Page on Pillar by Swamp", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Southwest] Fountain Page", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Overworld - [Northwest] Page on Pillar by Dark Tomb", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Old House - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Overworld - [East] Grapple Chest", player),
             lambda state: state.has(grapple, player))
    set_rule(multiworld.get_location("Sealed Temple - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Caustic Light Cave - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Cube Cave - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Old House - Holy Cross Door Page", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Maze Cave - Maze Room Holy Cross", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Old House - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Patrol Cave - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Ruined Passage - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Hourglass Cave - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    set_rule(multiworld.get_location("Secret Gathering Place - Holy Cross Chest", player),
             lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
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
             lambda state: state.has_all({grapple, laurels}, player))
    set_rule(multiworld.get_location("East Forest - Ice Rod Grapple Chest", player), lambda state: (
            state.has_all({grapple, ice_dagger, fire_wand}, player) and
            has_ability(state, player, ice_rod, options, ability_unlocks)))

    # West Garden
    set_rule(multiworld.get_location("West Garden - [North] Across From Page Pickup", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [West] In Flooded Walkway", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [West Lowlands] Tree Holy Cross Chest", player),
             lambda state: state.has(laurels, player) and has_ability(state, player, holy_cross, options,
                                                                      ability_unlocks))
    set_rule(multiworld.get_location("West Garden - [East Lowlands] Page Behind Ice Dagger House", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("West Garden - [Central Lowlands] Below Left Walkway", player),
             lambda state: state.has(laurels, player))

    # Ruined Atoll
    set_rule(multiworld.get_location("Ruined Atoll - [West] Near Kevin Block", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Lower Chest", player),
             lambda state: state.has_any({laurels, key}, player))
    set_rule(multiworld.get_location("Ruined Atoll - [East] Locked Room Upper Chest", player),
             lambda state: state.has_any({laurels, key}, player))

    # Frog's Domain
    set_rule(multiworld.get_location("Frog's Domain - Side Room Grapple Secret", player),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(multiworld.get_location("Frog's Domain - Grapple Above Hot Tub", player),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(multiworld.get_location("Frog's Domain - Escape Chest", player),
             lambda state: state.has_any({grapple, laurels}, player))

    # Eastern Vault Fortress
    set_rule(multiworld.get_location("Fortress Arena - Hexagon Red", player),
             lambda state: state.has(vault_key, player))

    # Beneath the Vault
    set_rule(multiworld.get_location("Beneath the Fortress - Bridge", player),
             lambda state: state.has_group("melee weapons", player, 1) or state.has_any({laurels, fire_wand}, player))
    set_rule(multiworld.get_location("Beneath the Fortress - Obscured Behind Waterfall", player),
             lambda state: state.has(lantern, player))

    # Quarry
    set_rule(multiworld.get_location("Quarry - [Central] Above Ladder Dash Chest", player),
             lambda state: state.has(laurels, player))

    # Ziggurat
    set_rule(multiworld.get_location("Rooted Ziggurat Upper - Near Bridge Switch", player),
             lambda state: has_sword(state, player) or state.has(fire_wand, player))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - After Guarded Fuse", player),
             lambda state: has_sword(state, player) and has_ability(state, player, prayer, options, ability_unlocks))

    # Bosses
    set_rule(multiworld.get_location("Fortress Arena - Siege Engine/Vault Key Pickup", player),
             lambda state: has_sword(state, player))
    set_rule(multiworld.get_location("Librarian - Hexagon Green", player),
             lambda state: has_sword(state, player))
    set_rule(multiworld.get_location("Rooted Ziggurat Lower - Hexagon Blue", player),
             lambda state: has_sword(state, player))

    # Swamp
    set_rule(multiworld.get_location("Cathedral Gauntlet - Gauntlet Reward", player),
             lambda state: state.has(fire_wand, player) and has_sword(state, player))
    set_rule(multiworld.get_location("Swamp - [Entrance] Above Entryway", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Swamp - [South Graveyard] Upper Walkway Dash Chest", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Swamp - [South Graveyard] 4 Orange Skulls", player),
             lambda state: has_sword(state, player))

    # Hero's Grave and Far Shore
    set_rule(multiworld.get_location("Hero's Grave - Tooth Relic", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Mushroom Relic", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Ash Relic", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Flowers Relic", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Effigy Relic", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Hero's Grave - Feathers Relic", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Far Shore - Secret Chest", player),
             lambda state: state.has(laurels, player))
