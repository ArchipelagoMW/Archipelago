from typing import Dict, TYPE_CHECKING
from worlds.generic.Rules import set_rule, forbid_item
from .rules import has_ability, has_sword, has_stick, has_ice_grapple_logic, has_lantern, has_mask, can_ladder_storage
from .er_data import Portal
from BaseClasses import Region

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


def set_er_region_rules(world: "TunicWorld", ability_unlocks: Dict[str, int], regions: Dict[str, Region],
                        portal_pairs: Dict[Portal, Portal]) -> None:
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

    # nmg: can laurels through the ruined passage door
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Ruined Passage Door"],
        rule=lambda state: state.has(key, player, 2)
        or (state.has(laurels, player) and options.logic_rules))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Swamp Upper Entry"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld Swamp Upper Entry"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has(laurels, player))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Special Shop Entry"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld Special Shop Entry"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has(laurels, player))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld West Garden Laurels Entry"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld West Garden Laurels Entry"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has(laurels, player))

    # nmg: can ice grapple through the door
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Old House Door"],
        rule=lambda state: state.has(house_key, player)
        or has_ice_grapple_logic(False, state, player, options, ability_unlocks))

    # not including ice grapple through this because it's very tedious to get an enemy here
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Southeast Cross Door"],
        rule=lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))
    regions["Overworld Southeast Cross Door"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ability(state, player, holy_cross, options, ability_unlocks))

    # not including ice grapple through this because we're not including it on the other door
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

    # nmg: ice grapple through temple door
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Temple Door"],
        name="Overworld Temple Door",
        rule=lambda state: state.has_all({"Ring Eastern Bell", "Ring Western Bell"}, player)
        or has_ice_grapple_logic(False, state, player, options, ability_unlocks))

    # Overworld side areas
    regions["Old House Front"].connect(
        connecting_region=regions["Old House Back"])
    # nmg: laurels through the gate
    regions["Old House Back"].connect(
        connecting_region=regions["Old House Front"],
        rule=lambda state: state.has(laurels, player) and options.logic_rules)

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

    # nmg: ice grapple up to dance fox spot, and vice versa
    regions["East Forest"].connect(
        connecting_region=regions["East Forest Dance Fox Spot"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, player, options, ability_unlocks))
    regions["East Forest Dance Fox Spot"].connect(
        connecting_region=regions["East Forest"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, player, options, ability_unlocks))

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

    # nmg: ice grapple from upper grave path exit to the rest of it
    regions["Forest Grave Path Upper"].connect(
        connecting_region=regions["Forest Grave Path Main"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, player, options, ability_unlocks))
    regions["Forest Grave Path Main"].connect(
        connecting_region=regions["Forest Grave Path Upper"],
        rule=lambda state: state.has(laurels, player))

    regions["Forest Grave Path Main"].connect(
        connecting_region=regions["Forest Grave Path by Grave"])
    # nmg: ice grapple or laurels through the gate
    regions["Forest Grave Path by Grave"].connect(
        connecting_region=regions["Forest Grave Path Main"],
        rule=lambda state: has_ice_grapple_logic(False, state, player, options, ability_unlocks)
        or (state.has(laurels, player) and options.logic_rules))

    regions["Forest Grave Path by Grave"].connect(
        connecting_region=regions["Forest Hero's Grave"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Forest Hero's Grave"].connect(
        connecting_region=regions["Forest Grave Path by Grave"])

    # Beneath the Well and Dark Tomb
    regions["Beneath the Well Front"].connect(
        connecting_region=regions["Beneath the Well Main"],
        rule=lambda state: has_stick(state, player) or state.has(fire_wand, player))
    regions["Beneath the Well Main"].connect(
        connecting_region=regions["Beneath the Well Front"],
        rule=lambda state: has_stick(state, player) or state.has(fire_wand, player))

    regions["Beneath the Well Back"].connect(
        connecting_region=regions["Beneath the Well Main"],
        rule=lambda state: has_stick(state, player) or state.has(fire_wand, player))
    regions["Beneath the Well Main"].connect(
        connecting_region=regions["Beneath the Well Back"],
        rule=lambda state: has_stick(state, player) or state.has(fire_wand, player))

    regions["Well Boss"].connect(
        connecting_region=regions["Dark Tomb Checkpoint"])
    # nmg: can laurels through the gate
    regions["Dark Tomb Checkpoint"].connect(
        connecting_region=regions["Well Boss"],
        rule=lambda state: state.has(laurels, player) and options.logic_rules)

    regions["Dark Tomb Entry Point"].connect(
        connecting_region=regions["Dark Tomb Main"],
        rule=lambda state: has_lantern(state, player, options))
    regions["Dark Tomb Main"].connect(
        connecting_region=regions["Dark Tomb Entry Point"],
        rule=lambda state: has_lantern(state, player, options))

    regions["Dark Tomb Main"].connect(
        connecting_region=regions["Dark Tomb Dark Exit"],
        rule=lambda state: has_lantern(state, player, options))
    regions["Dark Tomb Dark Exit"].connect(
        connecting_region=regions["Dark Tomb Main"],
        rule=lambda state: has_lantern(state, player, options))

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

    regions["West Garden Portal"].connect(
        connecting_region=regions["West Garden Portal Item"],
        rule=lambda state: state.has(laurels, player))
    regions["West Garden Portal Item"].connect(
        connecting_region=regions["West Garden Portal"],
        rule=lambda state: state.has(laurels, player) and has_ability(state, player, prayer, options, ability_unlocks))

    # nmg: can ice grapple to and from the item behind the magic dagger house
    regions["West Garden Portal Item"].connect(
        connecting_region=regions["West Garden"],
        rule=lambda state: has_ice_grapple_logic(True, state, player, options, ability_unlocks))
    regions["West Garden"].connect(
        connecting_region=regions["West Garden Portal Item"],
        rule=lambda state: has_ice_grapple_logic(True, state, player, options, ability_unlocks))

    # Atoll and Frog's Domain
    # nmg: ice grapple the bird below the portal
    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Lower Entry Area"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, player, options, ability_unlocks))
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

    regions["Fortress Exterior near cave"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"],
        rule=lambda state: state.has(laurels, player))
    regions["Fortress Exterior from Overworld"].connect(
        connecting_region=regions["Fortress Exterior near cave"],
        rule=lambda state: state.has(laurels, player) or has_ability(state, player, prayer, options, ability_unlocks))

    regions["Fortress Courtyard"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"],
        rule=lambda state: state.has(laurels, player))
    # nmg: can ice grapple an enemy in the courtyard
    regions["Fortress Exterior from Overworld"].connect(
        connecting_region=regions["Fortress Courtyard"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, player, options, ability_unlocks))

    regions["Fortress Courtyard Upper"].connect(
        connecting_region=regions["Fortress Courtyard"])
    # nmg: can ice grapple to the upper ledge
    regions["Fortress Courtyard"].connect(
        connecting_region=regions["Fortress Courtyard Upper"],
        rule=lambda state: has_ice_grapple_logic(True, state, player, options, ability_unlocks))

    regions["Fortress Courtyard Upper"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"])

    regions["Beneath the Vault Front"].connect(
        connecting_region=regions["Beneath the Vault Back"],
        rule=lambda state: has_lantern(state, player, options))
    regions["Beneath the Vault Back"].connect(
        connecting_region=regions["Beneath the Vault Front"])

    regions["Fortress East Shortcut Upper"].connect(
        connecting_region=regions["Fortress East Shortcut Lower"])
    # nmg: can ice grapple upwards
    regions["Fortress East Shortcut Lower"].connect(
        connecting_region=regions["Fortress East Shortcut Upper"],
        rule=lambda state: has_ice_grapple_logic(True, state, player, options, ability_unlocks))

    # nmg: ice grapple through the big gold door, can do it both ways
    regions["Eastern Vault Fortress"].connect(
        connecting_region=regions["Eastern Vault Fortress Gold Door"],
        name="Fortress to Gold Door",
        rule=lambda state: state.has_all({"Activate Eastern Vault West Fuses",
                                          "Activate Eastern Vault East Fuse"}, player)
        or has_ice_grapple_logic(False, state, player, options, ability_unlocks))
    regions["Eastern Vault Fortress Gold Door"].connect(
        connecting_region=regions["Eastern Vault Fortress"],
        name="Gold Door to Fortress",
        rule=lambda state: has_ice_grapple_logic(True, state, player, options, ability_unlocks))

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

    # nmg: ice grapple from upper grave path to lower
    regions["Fortress Grave Path Upper"].connect(
        connecting_region=regions["Fortress Grave Path"],
        rule=lambda state: has_ice_grapple_logic(True, state, player, options, ability_unlocks))

    regions["Fortress Arena"].connect(
        connecting_region=regions["Fortress Arena Portal"],
        name="Fortress Arena to Fortress Portal",
        rule=lambda state: state.has("Activate Eastern Vault West Fuses", player))
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
        rule=lambda state: state.has("Activate Quarry Fuse", player))
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

    regions["Quarry Monastery Entry"].connect(
        connecting_region=regions["Quarry Back"],
        rule=lambda state: state.has(laurels, player))
    regions["Quarry Back"].connect(
        connecting_region=regions["Quarry Monastery Entry"],
        rule=lambda state: state.has(laurels, player))

    regions["Monastery Rope"].connect(
        connecting_region=regions["Quarry Back"])

    regions["Quarry"].connect(
        connecting_region=regions["Lower Quarry"],
        rule=lambda state: has_mask(state, player, options))

    # nmg: bring a scav over, then ice grapple through the door
    regions["Lower Quarry"].connect(
        connecting_region=regions["Lower Quarry Zig Door"],
        name="Quarry to Zig Door",
        rule=lambda state: state.has("Activate Quarry Fuse", player)
        or has_ice_grapple_logic(False, state, player, options, ability_unlocks))

    # nmg: use ice grapple to get from the beginning of Quarry to the door without really needing mask
    regions["Quarry"].connect(
        connecting_region=regions["Lower Quarry Zig Door"],
        rule=lambda state: has_ice_grapple_logic(True, state, player, options, ability_unlocks))

    regions["Monastery Front"].connect(
        connecting_region=regions["Monastery Back"])
    # nmg: can laurels through the gate
    regions["Monastery Back"].connect(
        connecting_region=regions["Monastery Front"],
        rule=lambda state: state.has(laurels, player) and options.logic_rules)

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
    # unrestricted: use ladder storage to get to the front, get hit by one of the many enemies
    regions["Rooted Ziggurat Lower Back"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Front"],
        rule=lambda state: state.has(laurels, player) or can_ladder_storage(state, player, options))

    regions["Rooted Ziggurat Lower Back"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room Entrance"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    regions["Rooted Ziggurat Portal Room Entrance"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Back"])

    regions["Rooted Ziggurat Portal"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room Exit"],
        name="Zig Portal Room Exit",
        rule=lambda state: state.has("Activate Ziggurat Fuse", player))
    regions["Rooted Ziggurat Portal Room Exit"].connect(
        connecting_region=regions["Rooted Ziggurat Portal"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks))

    # Swamp and Cathedral
    # nmg: ice grapple through cathedral door, can do it both ways
    regions["Swamp"].connect(
        connecting_region=regions["Swamp to Cathedral Main Entrance"],
        rule=lambda state: has_ability(state, player, prayer, options, ability_unlocks)
        or has_ice_grapple_logic(False, state, player, options, ability_unlocks))
    regions["Swamp to Cathedral Main Entrance"].connect(
        connecting_region=regions["Swamp"],
        rule=lambda state: has_ice_grapple_logic(False, state, player, options, ability_unlocks))

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

    # nmg: can ice grapple down while you're on the pillars
    regions["Back of Swamp Laurels Area"].connect(
        connecting_region=regions["Swamp"],
        rule=lambda state: state.has(laurels, player)
        and has_ice_grapple_logic(True, state, player, options, ability_unlocks))

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
        rule=lambda state: state.has("Activate West Garden Fuse", player))
    regions["Far Shore to West Garden"].connect(
        connecting_region=regions["Far Shore"])

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Quarry"],
        name="Far Shore to Quarry",
        rule=lambda state: state.has("Activate Quarry Fuse", player))
    regions["Far Shore to Quarry"].connect(
        connecting_region=regions["Far Shore"])

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Fortress"],
        name="Far Shore to Fortress",
        rule=lambda state: state.has("Activate Eastern Vault West Fuses", player))
    regions["Far Shore to Fortress"].connect(
        connecting_region=regions["Far Shore"])

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Library"],
        name="Far Shore to Library",
        rule=lambda state: state.has("Activate Library Fuse", player))
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

    # connecting the regions portals are in to other portals you can access via ladder storage
    # using has_stick instead of can_ladder_storage since it's already checking the logic rules
    if options.logic_rules == "unrestricted":
        def get_paired_region(portal_sd: str) -> str:
            for portal1, portal2 in portal_pairs.items():
                if portal1.scene_destination() == portal_sd:
                    return portal2.region
                if portal2.scene_destination() == portal_sd:
                    return portal1.region
            raise Exception("no matches found in get_paired_region")

        # The upper Swamp entrance
        regions["Overworld"].connect(
            regions[get_paired_region("Overworld Redux, Swamp Redux 2_wall")],
            rule=lambda state: has_stick(state, player))
        # Western Furnace entrance, next to the sign that leads to West Garden
        regions["Overworld"].connect(
            regions[get_paired_region("Overworld Redux, Furnace_gyro_west")],
            rule=lambda state: has_stick(state, player))
        # Upper West Garden entry, by the belltower
        regions["Overworld"].connect(
            regions[get_paired_region("Overworld Redux, Archipelagos Redux_upper")],
            rule=lambda state: has_stick(state, player))
        # West Garden entry by the Furnace
        regions["Overworld"].connect(
            regions[get_paired_region("Overworld Redux, Archipelagos Redux_lower")],
            rule=lambda state: has_stick(state, player))
        # West Garden laurels entrance, by the beach
        regions["Overworld"].connect(
            regions[get_paired_region("Overworld Redux, Archipelagos Redux_lowest")],
            rule=lambda state: has_stick(state, player))
        # Well rail, west side. Can ls in town, get extra height by going over the portal pad
        regions["Overworld"].connect(
            regions[get_paired_region("Overworld Redux, Sewer_west_aqueduct")],
            rule=lambda state: has_stick(state, player))
        # Well rail, east side. Need some height from the temple stairs
        regions["Overworld"].connect(
            regions[get_paired_region("Overworld Redux, Furnace_gyro_upper_north")],
            rule=lambda state: has_stick(state, player))

        # Furnace ladder to the fuse entrance
        regions["Furnace Ladder Area"].connect(
            regions[get_paired_region("Furnace, Overworld Redux_gyro_upper_north")],
            rule=lambda state: has_stick(state, player))
        # Furnace ladder to Dark Tomb
        regions["Furnace Ladder Area"].connect(
            regions[get_paired_region("Furnace, Crypt Redux_")],
            rule=lambda state: has_stick(state, player))
        # Furnace ladder to the West Garden connector
        regions["Furnace Ladder Area"].connect(
            regions[get_paired_region("Furnace, Overworld Redux_gyro_west")],
            rule=lambda state: has_stick(state, player))

        # West Garden exit after Garden Knight
        regions["West Garden"].connect(
            regions[get_paired_region("Archipelagos Redux, Overworld Redux_upper")],
            rule=lambda state: has_stick(state, player))
        # West Garden laurels exit
        regions["West Garden"].connect(
            regions[get_paired_region("Archipelagos Redux, Overworld Redux_lowest")],
            rule=lambda state: has_stick(state, player))

        # Frog mouth entrance
        regions["Ruined Atoll"].connect(
            regions[get_paired_region("Atoll Redux, Frog Stairs_mouth")],
            rule=lambda state: has_stick(state, player))

        # Entrance by the dancing fox holy cross spot
        regions["East Forest"].connect(
            regions[get_paired_region("East Forest Redux, East Forest Redux Laddercave_upper")],
            rule=lambda state: has_stick(state, player))

        # From the west side of guard house 1 to the east side
        regions["Guard House 1 West"].connect(
            regions[get_paired_region("East Forest Redux Laddercave, East Forest Redux_gate")],
            rule=lambda state: has_stick(state, player))
        regions["Guard House 1 West"].connect(
            regions[get_paired_region("East Forest Redux Laddercave, Forest Boss Room_")],
            rule=lambda state: has_stick(state, player))

        # Upper exit from the Forest Grave Path, use ls at the ladder by the gate switch
        regions["Forest Grave Path Main"].connect(
            regions[get_paired_region("Sword Access, East Forest Redux_upper")],
            rule=lambda state: has_stick(state, player))

        # Fortress exterior shop, ls at the ladder by the telescope
        regions["Fortress Exterior from Overworld"].connect(
            regions[get_paired_region("Fortress Courtyard, Shop_")],
            rule=lambda state: has_stick(state, player))
        # Fortress main entry and grave path lower entry, ls at the ladder by the telescope
        regions["Fortress Exterior from Overworld"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress Main_Big Door")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior from Overworld"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress Reliquary_Lower")],
            rule=lambda state: has_stick(state, player))
        # Upper exits from the courtyard. Use the ramp in the courtyard, then the blocks north of the first fuse
        regions["Fortress Exterior from Overworld"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress Reliquary_Upper")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior from Overworld"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress East_")],
            rule=lambda state: has_stick(state, player))

        # same as above, except from the east side of the area
        regions["Fortress Exterior from East Forest"].connect(
            regions[get_paired_region("Fortress Courtyard, Overworld Redux_")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior from East Forest"].connect(
            regions[get_paired_region("Fortress Courtyard, Shop_")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior from East Forest"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress Main_Big Door")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior from East Forest"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress Reliquary_Lower")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior from East Forest"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress Reliquary_Upper")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior from East Forest"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress East_")],
            rule=lambda state: has_stick(state, player))

        # same as above, except from the Beneath the Vault entrance ladder
        regions["Fortress Exterior near cave"].connect(
            regions[get_paired_region("Fortress Courtyard, Overworld Redux_")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior near cave"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress Main_Big Door")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior near cave"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress Reliquary_Lower")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior near cave"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress Reliquary_Upper")],
            rule=lambda state: has_stick(state, player))
        regions["Fortress Exterior near cave"].connect(
            regions[get_paired_region("Fortress Courtyard, Fortress East_")],
            rule=lambda state: has_stick(state, player))

        # ls at the ladder, need to gain a little height to get up the stairs
        regions["Lower Mountain"].connect(
            regions[get_paired_region("Mountain, Mountaintop_")],
            rule=lambda state: has_stick(state, player))

        # Where the rope is behind Monastery. Connecting here since, if you have this region, you don't need a sword
        regions["Quarry Monastery Entry"].connect(
            regions[get_paired_region("Quarry Redux, Monastery_back")],
            rule=lambda state: has_stick(state, player))

        # Swamp to Gauntlet
        regions["Swamp"].connect(
            regions[get_paired_region("Swamp Redux 2, Cathedral Arena_")],
            rule=lambda state: has_stick(state, player))
        # Swamp to Overworld upper
        regions["Swamp"].connect(
            regions[get_paired_region("Swamp Redux 2, Overworld Redux_wall")],
            rule=lambda state: has_stick(state, player))
        # Ladder by the hero grave
        regions["Back of Swamp"].connect(
            regions[get_paired_region("Swamp Redux 2, Overworld Redux_conduit")],
            rule=lambda state: has_stick(state, player))
        regions["Back of Swamp"].connect(
            regions[get_paired_region("Swamp Redux 2, Shop_")],
            rule=lambda state: has_stick(state, player))
        # Need to put the cathedral HC code mid-flight
        regions["Back of Swamp"].connect(
            regions[get_paired_region("Swamp Redux 2, Cathedral Redux_secret")],
            rule=lambda state: has_stick(state, player)
            and has_ability(state, player, holy_cross, options, ability_unlocks))


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
    set_rule(multiworld.get_location("Beneath the Well - [Powered Secret Room] Chest", player),
             lambda state: state.has("Activate Furnace Fuse", player))
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
            has_ability(state, player, icebolt, options, ability_unlocks)))

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
             lambda state: has_lantern(state, player, options))

    # Quarry
    set_rule(multiworld.get_location("Quarry - [Central] Above Ladder Dash Chest", player),
             lambda state: state.has(laurels, player))
    set_rule(multiworld.get_location("Quarry - [West] Upper Area Bombable Wall", player),
             lambda state: has_mask(state, player, options))

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
    # these two swamp checks really want you to kill the big skeleton first
    set_rule(multiworld.get_location("Swamp - [South Graveyard] 4 Orange Skulls", player),
             lambda state: has_sword(state, player))
    set_rule(multiworld.get_location("Swamp - [South Graveyard] Guarded By Tentacles", player),
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

    # Events
    set_rule(multiworld.get_location("Eastern Bell", player),
             lambda state: (has_stick(state, player) or state.has(fire_wand, player)))
    set_rule(multiworld.get_location("Western Bell", player),
             lambda state: (has_stick(state, player) or state.has(fire_wand, player)))
    set_rule(multiworld.get_location("Furnace Fuse", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("South and West Fortress Exterior Fuses", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Upper and Central Fortress Exterior Fuses", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Beneath the Vault Fuse", player),
             lambda state: state.has("Activate South and West Fortress Exterior Fuses", player))
    set_rule(multiworld.get_location("Eastern Vault West Fuses", player),
             lambda state: state.has("Activate Beneath the Vault Fuse", player))
    set_rule(multiworld.get_location("Eastern Vault East Fuse", player),
             lambda state: state.has_all({"Activate Upper and Central Fortress Exterior Fuses",
                                          "Activate South and West Fortress Exterior Fuses"}, player))
    set_rule(multiworld.get_location("Quarry Connector Fuse", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks) and state.has(grapple, player))
    set_rule(multiworld.get_location("Quarry Fuse", player),
             lambda state: state.has("Activate Quarry Connector Fuse", player))
    set_rule(multiworld.get_location("Ziggurat Fuse", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("West Garden Fuse", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks))
    set_rule(multiworld.get_location("Library Fuse", player),
             lambda state: has_ability(state, player, prayer, options, ability_unlocks))
