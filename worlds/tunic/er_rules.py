from typing import Dict, Set, List, Tuple, TYPE_CHECKING
from worlds.generic.Rules import set_rule, forbid_item
from .rules import (has_ability, has_sword, has_stick, has_ice_grapple_logic, has_lantern, has_mask, can_ladder_storage,
                    bomb_walls)
from .er_data import Portal
from BaseClasses import Region, CollectionState

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
key = "Key"
house_key = "Old House Key"
vault_key = "Fortress Vault Key"
mask = "Scavenger Mask"
red_hexagon = "Red Questagon"
green_hexagon = "Green Questagon"
blue_hexagon = "Blue Questagon"
gold_hexagon = "Gold Questagon"


def has_ladder(ladder: str, state: CollectionState, world: "TunicWorld") -> bool:
    return not world.options.shuffle_ladders or state.has(ladder, world.player)


def can_shop(state: CollectionState, world: "TunicWorld") -> bool:
    return has_sword(state, world.player) and state.can_reach_region("Shop", world.player)


def set_er_region_rules(world: "TunicWorld", regions: Dict[str, Region], portal_pairs: Dict[Portal, Portal]) -> None:
    player = world.player
    options = world.options

    regions["Menu"].connect(
        connecting_region=regions["Overworld"])

    # Overworld
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Holy Cross"],
        rule=lambda state: has_ability(holy_cross, state, world))

    # grapple on the west side, down the stairs from moss wall, across from ruined shop
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Beach"],
        rule=lambda state: has_ladder("Ladders in Overworld Town", state, world)
        or state.has_any({laurels, grapple}, player))
    regions["Overworld Beach"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladders in Overworld Town", state, world)
        or state.has_any({laurels, grapple}, player))

    regions["Overworld Beach"].connect(
        connecting_region=regions["Overworld West Garden Laurels Entry"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld West Garden Laurels Entry"].connect(
        connecting_region=regions["Overworld Beach"],
        rule=lambda state: state.has(laurels, player))

    regions["Overworld Beach"].connect(
        connecting_region=regions["Overworld to Atoll Upper"],
        rule=lambda state: has_ladder("Ladder to Ruined Atoll", state, world))
    regions["Overworld to Atoll Upper"].connect(
        connecting_region=regions["Overworld Beach"],
        rule=lambda state: has_ladder("Ladder to Ruined Atoll", state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld to Atoll Upper"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld to Atoll Upper"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has_any({laurels, grapple}, player))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Belltower"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld Belltower"].connect(
        connecting_region=regions["Overworld"])

    regions["Overworld Belltower"].connect(
        connecting_region=regions["Overworld to West Garden Upper"],
        rule=lambda state: has_ladder("Ladders to West Bell", state, world))
    regions["Overworld to West Garden Upper"].connect(
        connecting_region=regions["Overworld Belltower"],
        rule=lambda state: has_ladder("Ladders to West Bell", state, world))

    regions["Overworld Belltower"].connect(
        connecting_region=regions["Overworld Belltower at Bell"],
        rule=lambda state: has_ladder("Ladders to West Bell", state, world))

    # long dong, do not make a reverse connection here or to belltower
    regions["Overworld above Patrol Cave"].connect(
        connecting_region=regions["Overworld Belltower at Bell"],
        rule=lambda state: options.logic_rules and state.has(fire_wand, player))

    # nmg: can laurels through the ruined passage door
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Ruined Passage Door"],
        rule=lambda state: state.has(key, player, 2)
        or (state.has(laurels, player) and options.logic_rules))
    regions["Overworld Ruined Passage Door"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has(laurels, player) and options.logic_rules)

    regions["Overworld"].connect(
        connecting_region=regions["After Ruined Passage"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world)
        or has_ice_grapple_logic(True, state, world))
    regions["After Ruined Passage"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Above Ruined Passage"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world)
        or state.has(laurels, player))
    regions["Above Ruined Passage"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world)
        or state.has(laurels, player))

    regions["After Ruined Passage"].connect(
        connecting_region=regions["Above Ruined Passage"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world))
    regions["Above Ruined Passage"].connect(
        connecting_region=regions["After Ruined Passage"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world))

    regions["Above Ruined Passage"].connect(
        connecting_region=regions["East Overworld"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world)
        or has_ice_grapple_logic(True, state, world))
    regions["East Overworld"].connect(
        connecting_region=regions["Above Ruined Passage"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world)
        or state.has(laurels, player))

    # nmg: ice grapple the slimes, works both ways consistently
    regions["East Overworld"].connect(
        connecting_region=regions["After Ruined Passage"],
        rule=lambda state: has_ice_grapple_logic(True, state, world))
    regions["After Ruined Passage"].connect(
        connecting_region=regions["East Overworld"],
        rule=lambda state: has_ice_grapple_logic(True, state, world))

    regions["Overworld"].connect(
        connecting_region=regions["East Overworld"],
        rule=lambda state: has_ladder("Ladders near Overworld Checkpoint", state, world)
        or has_ice_grapple_logic(True, state, world))
    regions["East Overworld"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladders near Overworld Checkpoint", state, world))

    regions["East Overworld"].connect(
        connecting_region=regions["Overworld at Patrol Cave"])
    regions["Overworld at Patrol Cave"].connect(
        connecting_region=regions["East Overworld"],
        rule=lambda state: state.has(laurels, player))

    regions["Overworld at Patrol Cave"].connect(
        connecting_region=regions["Overworld above Patrol Cave"],
        rule=lambda state: has_ladder("Ladders near Patrol Cave", state, world)
        or has_ice_grapple_logic(True, state, world))
    regions["Overworld above Patrol Cave"].connect(
        connecting_region=regions["Overworld at Patrol Cave"],
        rule=lambda state: has_ladder("Ladders near Patrol Cave", state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld above Patrol Cave"],
        rule=lambda state: has_ladder("Ladders near Overworld Checkpoint", state, world)
        or state.has(grapple, player))
    regions["Overworld above Patrol Cave"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladders near Overworld Checkpoint", state, world))

    regions["East Overworld"].connect(
        connecting_region=regions["Overworld above Patrol Cave"],
        rule=lambda state: has_ladder("Ladders near Overworld Checkpoint", state, world)
        or has_ice_grapple_logic(True, state, world))
    regions["Overworld above Patrol Cave"].connect(
        connecting_region=regions["East Overworld"],
        rule=lambda state: has_ladder("Ladders near Overworld Checkpoint", state, world))

    regions["Overworld above Patrol Cave"].connect(
        connecting_region=regions["Upper Overworld"],
        rule=lambda state: has_ladder("Ladders near Patrol Cave", state, world)
        or has_ice_grapple_logic(True, state, world))
    regions["Upper Overworld"].connect(
        connecting_region=regions["Overworld above Patrol Cave"],
        rule=lambda state: has_ladder("Ladders near Patrol Cave", state, world)
        or state.has(grapple, player))

    regions["Upper Overworld"].connect(
        connecting_region=regions["Overworld above Quarry Entrance"],
        rule=lambda state: state.has_any({grapple, laurels}, player))
    regions["Overworld above Quarry Entrance"].connect(
        connecting_region=regions["Upper Overworld"],
        rule=lambda state: state.has_any({grapple, laurels}, player))

    regions["Upper Overworld"].connect(
        connecting_region=regions["Overworld after Temple Rafters"],
        rule=lambda state: has_ladder("Ladder near Temple Rafters", state, world))
    regions["Overworld after Temple Rafters"].connect(
        connecting_region=regions["Upper Overworld"],
        rule=lambda state: has_ladder("Ladder near Temple Rafters", state, world)
        or has_ice_grapple_logic(True, state, world))

    regions["Overworld above Quarry Entrance"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladders near Dark Tomb", state, world))
    regions["Overworld"].connect(
        connecting_region=regions["Overworld above Quarry Entrance"],
        rule=lambda state: has_ladder("Ladders near Dark Tomb", state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld after Envoy"],
        rule=lambda state: state.has_any({laurels, grapple, gun}, player)
        or state.has("Sword Upgrade", player, 4)
        or options.logic_rules)
    regions["Overworld after Envoy"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has_any({laurels, grapple, gun}, player)
        or state.has("Sword Upgrade", player, 4)
        or options.logic_rules)

    regions["Overworld after Envoy"].connect(
        connecting_region=regions["Overworld Quarry Entry"],
        rule=lambda state: has_ladder("Ladder to Quarry", state, world))
    regions["Overworld Quarry Entry"].connect(
        connecting_region=regions["Overworld after Envoy"],
        rule=lambda state: has_ladder("Ladder to Quarry", state, world))

    # ice grapple through the gate
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Quarry Entry"],
        rule=lambda state: has_ice_grapple_logic(False, state, world))
    regions["Overworld Quarry Entry"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ice_grapple_logic(False, state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Swamp Upper Entry"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld Swamp Upper Entry"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has(laurels, player))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Swamp Lower Entry"],
        rule=lambda state: has_ladder("Ladder to Swamp", state, world))
    regions["Overworld Swamp Lower Entry"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladder to Swamp", state, world))

    regions["East Overworld"].connect(
        connecting_region=regions["Overworld Special Shop Entry"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld Special Shop Entry"].connect(
        connecting_region=regions["East Overworld"],
        rule=lambda state: state.has(laurels, player))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Well Ladder"],
        rule=lambda state: has_ladder("Ladders in Well", state, world))
    regions["Overworld Well Ladder"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladders in Well", state, world))

    # nmg: can ice grapple through the door
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Old House Door"],
        rule=lambda state: state.has(house_key, player)
        or has_ice_grapple_logic(False, state, world))

    # not including ice grapple through this because it's very tedious to get an enemy here
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Southeast Cross Door"],
        rule=lambda state: has_ability(holy_cross, state, world))
    regions["Overworld Southeast Cross Door"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ability(holy_cross, state, world))

    # not including ice grapple through this because we're not including it on the other door
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Fountain Cross Door"],
        rule=lambda state: has_ability(holy_cross, state, world))
    regions["Overworld Fountain Cross Door"].connect(
        connecting_region=regions["Overworld"])

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Town Portal"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Overworld Town Portal"].connect(
        connecting_region=regions["Overworld"])

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Spawn Portal"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Overworld Spawn Portal"].connect(
        connecting_region=regions["Overworld"])

    # nmg: ice grapple through temple door
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Temple Door"],
        rule=lambda state: state.has_all({"Ring Eastern Bell", "Ring Western Bell"}, player)
        or has_ice_grapple_logic(False, state, world))

    regions["Overworld Temple Door"].connect(
        connecting_region=regions["Overworld above Patrol Cave"],
        rule=lambda state: state.has(grapple, player))

    regions["Overworld Tunnel Turret"].connect(
        connecting_region=regions["Overworld Beach"],
        rule=lambda state: has_ladder("Ladders in Overworld Town", state, world)
        or state.has(grapple, player))
    regions["Overworld Beach"].connect(
        connecting_region=regions["Overworld Tunnel Turret"],
        rule=lambda state: has_ladder("Ladders in Overworld Town", state, world)
        or has_ice_grapple_logic(True, state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Tunnel Turret"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, world))
    regions["Overworld Tunnel Turret"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has_any({grapple, laurels}, player))

    regions["Overworld"].connect(
        connecting_region=regions["Cube Cave Entrance Region"],
        rule=lambda state: state.has(gun, player) or can_shop(state, world))
    regions["Cube Cave Entrance Region"].connect(
        connecting_region=regions["Overworld"])

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

    regions["Hourglass Cave"].connect(
        connecting_region=regions["Hourglass Cave Tower"],
        rule=lambda state: has_ladder("Ladders in Hourglass Cave", state, world))

    # East Forest
    regions["Forest Belltower Upper"].connect(
        connecting_region=regions["Forest Belltower Main"])

    regions["Forest Belltower Main"].connect(
        connecting_region=regions["Forest Belltower Lower"],
        rule=lambda state: has_ladder("Ladder to East Forest", state, world))

    # nmg: ice grapple up to dance fox spot, and vice versa
    regions["East Forest"].connect(
        connecting_region=regions["East Forest Dance Fox Spot"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, world))
    regions["East Forest Dance Fox Spot"].connect(
        connecting_region=regions["East Forest"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, world))

    regions["East Forest"].connect(
        connecting_region=regions["East Forest Portal"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["East Forest Portal"].connect(
        connecting_region=regions["East Forest"])

    regions["East Forest"].connect(
        connecting_region=regions["Lower Forest"],
        rule=lambda state: has_ladder("Ladders to Lower Forest", state, world)
        or (state.has_all({grapple, fire_wand, ice_dagger}, player) and has_ability(icebolt, state, world)))
    regions["Lower Forest"].connect(
        connecting_region=regions["East Forest"],
        rule=lambda state: has_ladder("Ladders to Lower Forest", state, world))

    regions["Guard House 1 East"].connect(
        connecting_region=regions["Guard House 1 West"])
    regions["Guard House 1 West"].connect(
        connecting_region=regions["Guard House 1 East"],
        rule=lambda state: state.has(laurels, player))

    regions["Guard House 2 Upper"].connect(
        connecting_region=regions["Guard House 2 Lower"],
        rule=lambda state: has_ladder("Ladders to Lower Forest", state, world))
    regions["Guard House 2 Lower"].connect(
        connecting_region=regions["Guard House 2 Upper"],
        rule=lambda state: has_ladder("Ladders to Lower Forest", state, world))

    # nmg: ice grapple from upper grave path exit to the rest of it
    regions["Forest Grave Path Upper"].connect(
        connecting_region=regions["Forest Grave Path Main"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, world))
    regions["Forest Grave Path Main"].connect(
        connecting_region=regions["Forest Grave Path Upper"],
        rule=lambda state: state.has(laurels, player))

    regions["Forest Grave Path Main"].connect(
        connecting_region=regions["Forest Grave Path by Grave"])
    # nmg: ice grapple or laurels through the gate
    regions["Forest Grave Path by Grave"].connect(
        connecting_region=regions["Forest Grave Path Main"],
        rule=lambda state: has_ice_grapple_logic(False, state, world)
        or (state.has(laurels, player) and options.logic_rules))

    regions["Forest Grave Path by Grave"].connect(
        connecting_region=regions["Forest Hero's Grave"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Forest Hero's Grave"].connect(
        connecting_region=regions["Forest Grave Path by Grave"])

    # Beneath the Well and Dark Tomb
    regions["Beneath the Well Ladder Exit"].connect(
        connecting_region=regions["Beneath the Well Front"],
        rule=lambda state: has_ladder("Ladders in Well", state, world))
    regions["Beneath the Well Front"].connect(
        connecting_region=regions["Beneath the Well Ladder Exit"],
        rule=lambda state: has_ladder("Ladders in Well", state, world))

    regions["Beneath the Well Front"].connect(
        connecting_region=regions["Beneath the Well Main"],
        rule=lambda state: has_stick(state, player) or state.has(fire_wand, player))
    regions["Beneath the Well Main"].connect(
        connecting_region=regions["Beneath the Well Front"],
        rule=lambda state: has_stick(state, player) or state.has(fire_wand, player))

    regions["Beneath the Well Main"].connect(
        connecting_region=regions["Beneath the Well Back"],
        rule=lambda state: has_ladder("Ladders in Well", state, world))
    regions["Beneath the Well Back"].connect(
        connecting_region=regions["Beneath the Well Main"],
        rule=lambda state: has_ladder("Ladders in Well", state, world)
        and (has_stick(state, player) or state.has(fire_wand, player)))

    regions["Well Boss"].connect(
        connecting_region=regions["Dark Tomb Checkpoint"])
    # nmg: can laurels through the gate
    regions["Dark Tomb Checkpoint"].connect(
        connecting_region=regions["Well Boss"],
        rule=lambda state: state.has(laurels, player) and options.logic_rules)

    regions["Dark Tomb Entry Point"].connect(
        connecting_region=regions["Dark Tomb Upper"],
        rule=lambda state: has_lantern(state, world))
    regions["Dark Tomb Upper"].connect(
        connecting_region=regions["Dark Tomb Entry Point"])

    regions["Dark Tomb Upper"].connect(
        connecting_region=regions["Dark Tomb Main"],
        rule=lambda state: has_ladder("Ladder in Dark Tomb", state, world))
    regions["Dark Tomb Main"].connect(
        connecting_region=regions["Dark Tomb Upper"],
        rule=lambda state: has_ladder("Ladder in Dark Tomb", state, world))

    regions["Dark Tomb Main"].connect(
        connecting_region=regions["Dark Tomb Dark Exit"])
    regions["Dark Tomb Dark Exit"].connect(
        connecting_region=regions["Dark Tomb Main"],
        rule=lambda state: has_lantern(state, world))

    # West Garden
    regions["West Garden Laurels Exit Region"].connect(
        connecting_region=regions["West Garden"],
        rule=lambda state: state.has(laurels, player))
    regions["West Garden"].connect(
        connecting_region=regions["West Garden Laurels Exit Region"],
        rule=lambda state: state.has(laurels, player))

    regions["West Garden after Boss"].connect(
        connecting_region=regions["West Garden"],
        rule=lambda state: state.has(laurels, player))
    regions["West Garden"].connect(
        connecting_region=regions["West Garden after Boss"],
        rule=lambda state: state.has(laurels, player) or has_sword(state, player))

    regions["West Garden"].connect(
        connecting_region=regions["West Garden Hero's Grave Region"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["West Garden Hero's Grave Region"].connect(
        connecting_region=regions["West Garden"])

    regions["West Garden Portal"].connect(
        connecting_region=regions["West Garden Portal Item"],
        rule=lambda state: state.has(laurels, player))
    regions["West Garden Portal Item"].connect(
        connecting_region=regions["West Garden Portal"],
        rule=lambda state: state.has(laurels, player) and has_ability(prayer, state, world))

    # nmg: can ice grapple to and from the item behind the magic dagger house
    regions["West Garden Portal Item"].connect(
        connecting_region=regions["West Garden"],
        rule=lambda state: has_ice_grapple_logic(True, state, world))
    regions["West Garden"].connect(
        connecting_region=regions["West Garden Portal Item"],
        rule=lambda state: has_ice_grapple_logic(True, state, world))

    # Atoll and Frog's Domain
    # nmg: ice grapple the bird below the portal
    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Lower Entry Area"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, world))
    regions["Ruined Atoll Lower Entry Area"].connect(
        connecting_region=regions["Ruined Atoll"],
        rule=lambda state: state.has(laurels, player) or state.has(grapple, player))

    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Ladder Tops"],
        rule=lambda state: has_ladder("Ladders in South Atoll", state, world))

    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Frog Mouth"],
        rule=lambda state: state.has(laurels, player) or state.has(grapple, player))
    regions["Ruined Atoll Frog Mouth"].connect(
        connecting_region=regions["Ruined Atoll"],
        rule=lambda state: state.has(laurels, player) or state.has(grapple, player))

    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Frog Eye"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world))
    regions["Ruined Atoll Frog Eye"].connect(
        connecting_region=regions["Ruined Atoll"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world))

    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Portal"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Ruined Atoll Portal"].connect(
        connecting_region=regions["Ruined Atoll"])

    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Statue"],
        rule=lambda state: has_ability(prayer, state, world)
        and has_ladder("Ladders in South Atoll", state, world))
    regions["Ruined Atoll Statue"].connect(
        connecting_region=regions["Ruined Atoll"])

    regions["Frog Stairs Eye Exit"].connect(
        connecting_region=regions["Frog Stairs Upper"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world))
    regions["Frog Stairs Upper"].connect(
        connecting_region=regions["Frog Stairs Eye Exit"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world))

    regions["Frog Stairs Upper"].connect(
        connecting_region=regions["Frog Stairs Lower"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world))
    regions["Frog Stairs Lower"].connect(
        connecting_region=regions["Frog Stairs Upper"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world))

    regions["Frog Stairs Lower"].connect(
        connecting_region=regions["Frog Stairs to Frog's Domain"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world))
    regions["Frog Stairs to Frog's Domain"].connect(
        connecting_region=regions["Frog Stairs Lower"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world))

    regions["Frog's Domain Entry"].connect(
        connecting_region=regions["Frog's Domain"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world))

    regions["Frog's Domain"].connect(
        connecting_region=regions["Frog's Domain Back"],
        rule=lambda state: state.has(grapple, player))

    # Library
    regions["Library Exterior Tree Region"].connect(
        connecting_region=regions["Library Exterior Ladder Region"],
        rule=lambda state: state.has_any({grapple, laurels}, player)
        and has_ladder("Ladders in Library", state, world))
    regions["Library Exterior Ladder Region"].connect(
        connecting_region=regions["Library Exterior Tree Region"],
        rule=lambda state: has_ability(prayer, state, world)
        and ((state.has(laurels, player) and has_ladder("Ladders in Library", state, world))
             or state.has(grapple, player)))

    regions["Library Hall Bookshelf"].connect(
        connecting_region=regions["Library Hall"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))
    regions["Library Hall"].connect(
        connecting_region=regions["Library Hall Bookshelf"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))

    regions["Library Hall"].connect(
        connecting_region=regions["Library Hero's Grave Region"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Library Hero's Grave Region"].connect(
        connecting_region=regions["Library Hall"])

    regions["Library Hall to Rotunda"].connect(
        connecting_region=regions["Library Hall"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))
    regions["Library Hall"].connect(
        connecting_region=regions["Library Hall to Rotunda"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))

    regions["Library Rotunda to Hall"].connect(
        connecting_region=regions["Library Rotunda"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))
    regions["Library Rotunda"].connect(
        connecting_region=regions["Library Rotunda to Hall"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))

    regions["Library Rotunda"].connect(
        connecting_region=regions["Library Rotunda to Lab"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))
    regions["Library Rotunda to Lab"].connect(
        connecting_region=regions["Library Rotunda"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))

    regions["Library Lab Lower"].connect(
        connecting_region=regions["Library Lab"],
        rule=lambda state: state.has_any({grapple, laurels}, player)
        and has_ladder("Ladders in Library", state, world))
    regions["Library Lab"].connect(
        connecting_region=regions["Library Lab Lower"],
        rule=lambda state: state.has(laurels, player)
        and has_ladder("Ladders in Library", state, world))

    regions["Library Lab"].connect(
        connecting_region=regions["Library Portal"],
        rule=lambda state: has_ability(prayer, state, world)
        and has_ladder("Ladders in Library", state, world))
    regions["Library Portal"].connect(
        connecting_region=regions["Library Lab"],
        rule=lambda state: has_ladder("Ladders in Library", state, world)
        or state.has(laurels, player))

    regions["Library Lab"].connect(
        connecting_region=regions["Library Lab to Librarian"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))
    regions["Library Lab to Librarian"].connect(
        connecting_region=regions["Library Lab"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))

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
        rule=lambda state: state.has(laurels, player) or has_ability(prayer, state, world))

    regions["Fortress Exterior near cave"].connect(
        connecting_region=regions["Beneath the Vault Entry"],
        rule=lambda state: has_ladder("Ladder to Beneath the Vault", state, world))
    regions["Beneath the Vault Entry"].connect(
        connecting_region=regions["Fortress Exterior near cave"],
        rule=lambda state: has_ladder("Ladder to Beneath the Vault", state, world))

    regions["Fortress Courtyard"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"],
        rule=lambda state: state.has(laurels, player))
    # nmg: can ice grapple an enemy in the courtyard
    regions["Fortress Exterior from Overworld"].connect(
        connecting_region=regions["Fortress Courtyard"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, state, world))

    regions["Fortress Courtyard Upper"].connect(
        connecting_region=regions["Fortress Courtyard"])
    # nmg: can ice grapple to the upper ledge
    regions["Fortress Courtyard"].connect(
        connecting_region=regions["Fortress Courtyard Upper"],
        rule=lambda state: has_ice_grapple_logic(True, state, world))

    regions["Fortress Courtyard Upper"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"])

    regions["Beneath the Vault Ladder Exit"].connect(
        connecting_region=regions["Beneath the Vault Main"],
        rule=lambda state: has_ladder("Ladder to Beneath the Vault", state, world)
        and has_lantern(state, world))
    regions["Beneath the Vault Main"].connect(
        connecting_region=regions["Beneath the Vault Ladder Exit"],
        rule=lambda state: has_ladder("Ladder to Beneath the Vault", state, world))

    regions["Beneath the Vault Main"].connect(
        connecting_region=regions["Beneath the Vault Back"])
    regions["Beneath the Vault Back"].connect(
        connecting_region=regions["Beneath the Vault Main"],
        rule=lambda state: has_lantern(state, world))

    regions["Fortress East Shortcut Upper"].connect(
        connecting_region=regions["Fortress East Shortcut Lower"])
    # nmg: can ice grapple upwards
    regions["Fortress East Shortcut Lower"].connect(
        connecting_region=regions["Fortress East Shortcut Upper"],
        rule=lambda state: has_ice_grapple_logic(True, state, world))

    # nmg: ice grapple through the big gold door, can do it both ways
    regions["Eastern Vault Fortress"].connect(
        connecting_region=regions["Eastern Vault Fortress Gold Door"],
        rule=lambda state: state.has_all({"Activate Eastern Vault West Fuses",
                                          "Activate Eastern Vault East Fuse"}, player)
        or has_ice_grapple_logic(False, state, world))
    regions["Eastern Vault Fortress Gold Door"].connect(
        connecting_region=regions["Eastern Vault Fortress"],
        rule=lambda state: has_ice_grapple_logic(True, state, world))

    regions["Fortress Grave Path"].connect(
        connecting_region=regions["Fortress Grave Path Dusty Entrance Region"],
        rule=lambda state: state.has(laurels, player))
    regions["Fortress Grave Path Dusty Entrance Region"].connect(
        connecting_region=regions["Fortress Grave Path"],
        rule=lambda state: state.has(laurels, player))

    regions["Fortress Grave Path"].connect(
        connecting_region=regions["Fortress Hero's Grave Region"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Fortress Hero's Grave Region"].connect(
        connecting_region=regions["Fortress Grave Path"])

    # nmg: ice grapple from upper grave path to lower
    regions["Fortress Grave Path Upper"].connect(
        connecting_region=regions["Fortress Grave Path"],
        rule=lambda state: has_ice_grapple_logic(True, state, world))

    regions["Fortress Arena"].connect(
        connecting_region=regions["Fortress Arena Portal"],
        rule=lambda state: state.has("Activate Eastern Vault West Fuses", player))
    regions["Fortress Arena Portal"].connect(
        connecting_region=regions["Fortress Arena"])

    # Quarry
    regions["Lower Mountain"].connect(
        connecting_region=regions["Lower Mountain Stairs"],
        rule=lambda state: has_ability(holy_cross, state, world))
    regions["Lower Mountain Stairs"].connect(
        connecting_region=regions["Lower Mountain"],
        rule=lambda state: has_ability(holy_cross, state, world))

    regions["Quarry Entry"].connect(
        connecting_region=regions["Quarry Portal"],
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
        rule=lambda state: has_mask(state, world))

    # need the ladder, or you can ice grapple down in nmg
    regions["Lower Quarry"].connect(
        connecting_region=regions["Even Lower Quarry"],
        rule=lambda state: has_ladder("Ladders in Lower Quarry", state, world)
        or has_ice_grapple_logic(True, state, world))

    # nmg: bring a scav over, then ice grapple through the door, only with ER on to avoid soft lock
    regions["Even Lower Quarry"].connect(
        connecting_region=regions["Lower Quarry Zig Door"],
        rule=lambda state: state.has("Activate Quarry Fuse", player)
        or (has_ice_grapple_logic(False, state, world) and options.entrance_rando))

    # nmg: use ice grapple to get from the beginning of Quarry to the door without really needing mask only with ER on
    regions["Quarry"].connect(
        connecting_region=regions["Lower Quarry Zig Door"],
        rule=lambda state: has_ice_grapple_logic(True, state, world) and options.entrance_rando)

    regions["Monastery Front"].connect(
        connecting_region=regions["Monastery Back"])
    # nmg: can laurels through the gate
    regions["Monastery Back"].connect(
        connecting_region=regions["Monastery Front"],
        rule=lambda state: state.has(laurels, player) and options.logic_rules)

    regions["Monastery Back"].connect(
        connecting_region=regions["Monastery Hero's Grave Region"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Monastery Hero's Grave Region"].connect(
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
        or (has_sword(state, player) and has_ability(prayer, state, world)))
    # unrestricted: use ladder storage to get to the front, get hit by one of the many enemies
    # nmg: can ice grapple on the voidlings to the double admin fight, still need to pray at the fuse
    regions["Rooted Ziggurat Lower Back"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Front"],
        rule=lambda state: ((state.has(laurels, player) or has_ice_grapple_logic(True, state, world))
                            and has_ability(prayer, state, world)
                            and has_sword(state, player))
        or can_ladder_storage(state, world))

    regions["Rooted Ziggurat Lower Back"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room Entrance"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Rooted Ziggurat Portal Room Entrance"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Back"])

    regions["Zig Skip Exit"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Front"])

    regions["Rooted Ziggurat Portal"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room Exit"],
        rule=lambda state: state.has("Activate Ziggurat Fuse", player))
    regions["Rooted Ziggurat Portal Room Exit"].connect(
        connecting_region=regions["Rooted Ziggurat Portal"],
        rule=lambda state: has_ability(prayer, state, world))

    # Swamp and Cathedral
    regions["Swamp Front"].connect(
        connecting_region=regions["Swamp Mid"],
        rule=lambda state: has_ladder("Ladders in Swamp", state, world)
        or state.has(laurels, player)
        or has_ice_grapple_logic(False, state, world))  # nmg: ice grapple through gate
    regions["Swamp Mid"].connect(
        connecting_region=regions["Swamp Front"],
        rule=lambda state: has_ladder("Ladders in Swamp", state, world)
        or state.has(laurels, player)
        or has_ice_grapple_logic(False, state, world))  # nmg: ice grapple through gate

    # nmg: ice grapple through cathedral door, can do it both ways
    regions["Swamp Mid"].connect(
        connecting_region=regions["Swamp to Cathedral Main Entrance Region"],
        rule=lambda state: (has_ability(prayer, state, world) and state.has(laurels, player))
        or has_ice_grapple_logic(False, state, world))
    regions["Swamp to Cathedral Main Entrance Region"].connect(
        connecting_region=regions["Swamp Mid"],
        rule=lambda state: has_ice_grapple_logic(False, state, world))

    regions["Swamp Mid"].connect(
        connecting_region=regions["Swamp Ledge under Cathedral Door"],
        rule=lambda state: has_ladder("Ladders in Swamp", state, world))
    regions["Swamp Ledge under Cathedral Door"].connect(
        connecting_region=regions["Swamp Mid"],
        rule=lambda state: has_ladder("Ladders in Swamp", state, world)
        or has_ice_grapple_logic(True, state, world))  # nmg: ice grapple the enemy at door

    regions["Swamp Ledge under Cathedral Door"].connect(
        connecting_region=regions["Swamp to Cathedral Treasure Room"],
        rule=lambda state: has_ability(holy_cross, state, world))
    regions["Swamp to Cathedral Treasure Room"].connect(
        connecting_region=regions["Swamp Ledge under Cathedral Door"])

    regions["Back of Swamp"].connect(
        connecting_region=regions["Back of Swamp Laurels Area"],
        rule=lambda state: state.has(laurels, player))
    regions["Back of Swamp Laurels Area"].connect(
        connecting_region=regions["Back of Swamp"],
        rule=lambda state: state.has(laurels, player))

    # nmg: can ice grapple down while you're on the pillars
    regions["Back of Swamp Laurels Area"].connect(
        connecting_region=regions["Swamp Mid"],
        rule=lambda state: state.has(laurels, player)
        and has_ice_grapple_logic(True, state, world))

    regions["Back of Swamp"].connect(
        connecting_region=regions["Swamp Hero's Grave Region"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Swamp Hero's Grave Region"].connect(
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
        connecting_region=regions["Far Shore to Spawn Region"],
        rule=lambda state: state.has(laurels, player))
    regions["Far Shore to Spawn Region"].connect(
        connecting_region=regions["Far Shore"],
        rule=lambda state: state.has(laurels, player))

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to East Forest Region"],
        rule=lambda state: state.has(laurels, player))
    regions["Far Shore to East Forest Region"].connect(
        connecting_region=regions["Far Shore"],
        rule=lambda state: state.has(laurels, player))

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to West Garden Region"],
        rule=lambda state: state.has("Activate West Garden Fuse", player))
    regions["Far Shore to West Garden Region"].connect(
        connecting_region=regions["Far Shore"])

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Quarry Region"],
        rule=lambda state: state.has("Activate Quarry Fuse", player))
    regions["Far Shore to Quarry Region"].connect(
        connecting_region=regions["Far Shore"])

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Fortress Region"],
        rule=lambda state: state.has("Activate Eastern Vault West Fuses", player))
    regions["Far Shore to Fortress Region"].connect(
        connecting_region=regions["Far Shore"])

    regions["Far Shore"].connect(
        connecting_region=regions["Far Shore to Library Region"],
        rule=lambda state: state.has("Activate Library Fuse", player))
    regions["Far Shore to Library Region"].connect(
        connecting_region=regions["Far Shore"])

    # Misc
    regions["Spirit Arena"].connect(
        connecting_region=regions["Spirit Arena Victory"],
        rule=lambda state: (state.has(gold_hexagon, player, world.options.hexagon_goal.value) if
                            world.options.hexagon_quest else
                            (state.has_all({red_hexagon, green_hexagon, blue_hexagon, "Unseal the Heir"}, player)
                             and state.has_group_unique("Hero Relics", player, 6)
                             and has_sword(state, player))))

    # connecting the regions portals are in to other portals you can access via ladder storage
    # using has_stick instead of can_ladder_storage since it's already checking the logic rules
    if options.logic_rules == "unrestricted":
        def get_portal_info(portal_sd: str) -> Tuple[str, str]:
            for portal1, portal2 in portal_pairs.items():
                if portal1.scene_destination() == portal_sd:
                    return portal1.name, portal2.region
                if portal2.scene_destination() == portal_sd:
                    return portal2.name, portal1.region
            raise Exception("no matches found in get_paired_region")

        ladder_storages: List[Tuple[str, str, Set[str]]] = [
            # LS from Overworld main
            # The upper Swamp entrance
            ("Overworld", "Overworld Redux, Swamp Redux 2_wall",
             {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town"}),
            # Upper atoll entrance
            ("Overworld", "Overworld Redux, Atoll Redux_upper",
             {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town"}),
            # Furnace entrance, next to the sign that leads to West Garden
            ("Overworld", "Overworld Redux, Furnace_gyro_west",
             {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town"}),
            # Upper West Garden entry, by the belltower
            ("Overworld", "Overworld Redux, Archipelagos Redux_upper",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town"}),
            # Ruined Passage
            ("Overworld", "Overworld Redux, Ruins Passage_east",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town"}),
            # Well rail, west side. Can ls in town, get extra height by going over the portal pad
            ("Overworld", "Overworld Redux, Sewer_west_aqueduct",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town", "Ladder to Quarry"}),
            # Well rail, east side. Need some height from the temple stairs
            ("Overworld", "Overworld Redux, Furnace_gyro_upper_north",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town", "Ladder to Quarry"}),
            # Quarry entry
            ("Overworld", "Overworld Redux, Darkwoods Tunnel_",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town", "Ladders in Well"}),
            # East Forest entry
            ("Overworld", "Overworld Redux, Forest Belltower_",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town", "Ladders in Well",
                 "Ladders near Patrol Cave", "Ladder to Quarry", "Ladders near Dark Tomb"}),
            # Fortress entry
            ("Overworld", "Overworld Redux, Fortress Courtyard_",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town", "Ladders in Well",
                 "Ladders near Patrol Cave", "Ladder to Quarry", "Ladders near Dark Tomb"}),
            # Patrol Cave entry
            ("Overworld", "Overworld Redux, PatrolCave_",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town", "Ladders in Well",
                 "Ladders near Overworld Checkpoint", "Ladder to Quarry", "Ladders near Dark Tomb"}),
            # Special Shop entry, excluded in non-ER due to soft lock potential
            ("Overworld", "Overworld Redux, ShopSpecial_",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town", "Ladders in Well",
                 "Ladders near Overworld Checkpoint", "Ladders near Patrol Cave", "Ladder to Quarry",
                 "Ladders near Dark Tomb"}),
            # Temple Rafters, excluded in non-ER + ladder rando due to soft lock potential
            ("Overworld", "Overworld Redux, Temple_rafters",
                {"Ladders near Weathervane", "Ladder to Swamp", "Ladders in Overworld Town", "Ladders in Well",
                 "Ladders near Overworld Checkpoint", "Ladders near Patrol Cave", "Ladder to Quarry",
                 "Ladders near Dark Tomb"}),
            # Spot above the Quarry entrance,
            # only gets you to the mountain stairs
            ("Overworld above Quarry Entrance", "Overworld Redux, Mountain_",
                {"Ladders near Dark Tomb"}),

            # LS from the Overworld Beach
            # West Garden entry by the Furnace
            ("Overworld Beach", "Overworld Redux, Archipelagos Redux_lower",
                {"Ladders in Overworld Town", "Ladder to Ruined Atoll"}),
            # West Garden laurels entry
            ("Overworld Beach", "Overworld Redux, Archipelagos Redux_lowest",
                {"Ladders in Overworld Town", "Ladder to Ruined Atoll"}),
            # Swamp lower entrance
            ("Overworld Beach", "Overworld Redux, Swamp Redux 2_conduit",
                {"Ladders in Overworld Town", "Ladder to Ruined Atoll"}),
            # Rotating Lights entrance
            ("Overworld Beach", "Overworld Redux, Overworld Cave_",
                {"Ladders in Overworld Town", "Ladder to Ruined Atoll"}),
            # Swamp upper entrance
            ("Overworld Beach", "Overworld Redux, Swamp Redux 2_wall",
                {"Ladder to Ruined Atoll"}),
            # Furnace entrance, next to the sign that leads to West Garden
            ("Overworld Beach", "Overworld Redux, Furnace_gyro_west",
                {"Ladder to Ruined Atoll"}),
            # Upper West Garden entry, by the belltower
            ("Overworld Beach", "Overworld Redux, Archipelagos Redux_upper",
                {"Ladder to Ruined Atoll"}),
            # Ruined Passage
            ("Overworld Beach", "Overworld Redux, Ruins Passage_east",
                {"Ladder to Ruined Atoll"}),
            # Well rail, west side. Can ls in town, get extra height by going over the portal pad
            ("Overworld Beach", "Overworld Redux, Sewer_west_aqueduct",
                {"Ladder to Ruined Atoll"}),
            # Well rail, east side. Need some height from the temple stairs
            ("Overworld Beach", "Overworld Redux, Furnace_gyro_upper_north",
                {"Ladder to Ruined Atoll"}),
            # Quarry entry
            ("Overworld Beach", "Overworld Redux, Darkwoods Tunnel_",
                {"Ladder to Ruined Atoll"}),

            # LS from that low spot where you normally walk to swamp
            # Only has low ones you can't get to from main Overworld
            # West Garden main entry from swamp ladder
            ("Overworld Swamp Lower Entry", "Overworld Redux, Archipelagos Redux_lower",
                {"Ladder to Swamp"}),
            # Maze Cave entry from swamp ladder
            ("Overworld Swamp Lower Entry", "Overworld Redux, Maze Room_",
                {"Ladder to Swamp"}),
            # Hourglass Cave entry from swamp ladder
            ("Overworld Swamp Lower Entry", "Overworld Redux, Town Basement_beach",
                {"Ladder to Swamp"}),
            # Lower Atoll entry from swamp ladder
            ("Overworld Swamp Lower Entry", "Overworld Redux, Atoll Redux_lower",
                {"Ladder to Swamp"}),
            # Lowest West Garden entry from swamp ladder
            ("Overworld Swamp Lower Entry", "Overworld Redux, Archipelagos Redux_lowest",
                {"Ladder to Swamp"}),

            # from the ladders by the belltower
            # Ruined Passage
            ("Overworld to West Garden Upper", "Overworld Redux, Ruins Passage_east",
                {"Ladders to West Bell"}),
            # Well rail, west side. Can ls in town, get extra height by going over the portal pad
            ("Overworld to West Garden Upper", "Overworld Redux, Sewer_west_aqueduct",
                {"Ladders to West Bell"}),
            # Well rail, east side. Need some height from the temple stairs
            ("Overworld to West Garden Upper", "Overworld Redux, Furnace_gyro_upper_north",
                {"Ladders to West Bell"}),
            # Quarry entry
            ("Overworld to West Garden Upper", "Overworld Redux, Darkwoods Tunnel_",
                {"Ladders to West Bell"}),
            # East Forest entry
            ("Overworld to West Garden Upper", "Overworld Redux, Forest Belltower_",
                {"Ladders to West Bell"}),
            # Fortress entry
            ("Overworld to West Garden Upper", "Overworld Redux, Fortress Courtyard_",
                {"Ladders to West Bell"}),
            # Patrol Cave entry
            ("Overworld to West Garden Upper", "Overworld Redux, PatrolCave_",
                {"Ladders to West Bell"}),
            # Special Shop entry, excluded in non-ER due to soft lock potential
            ("Overworld to West Garden Upper", "Overworld Redux, ShopSpecial_",
                {"Ladders to West Bell"}),
            # Temple Rafters, excluded in non-ER and ladder rando due to soft lock potential
            ("Overworld to West Garden Upper", "Overworld Redux, Temple_rafters",
                {"Ladders to West Bell"}),

            # In the furnace
            # Furnace ladder to the fuse entrance
            ("Furnace Ladder Area", "Furnace, Overworld Redux_gyro_upper_north", set()),
            # Furnace ladder to Dark Tomb
            ("Furnace Ladder Area", "Furnace, Crypt Redux_", set()),
            # Furnace ladder to the West Garden connector
            ("Furnace Ladder Area", "Furnace, Overworld Redux_gyro_west", set()),

            # West Garden
            # exit after Garden Knight
            ("West Garden", "Archipelagos Redux, Overworld Redux_upper", set()),
            # West Garden laurels exit
            ("West Garden", "Archipelagos Redux, Overworld Redux_lowest", set()),

            # Atoll, use the little ladder you fix at the beginning
            ("Ruined Atoll", "Atoll Redux, Overworld Redux_lower", set()),
            ("Ruined Atoll", "Atoll Redux, Frog Stairs_mouth", set()),
            ("Ruined Atoll", "Atoll Redux, Frog Stairs_eye", set()),

            # East Forest
            # Entrance by the dancing fox holy cross spot
            ("East Forest", "East Forest Redux, East Forest Redux Laddercave_upper", set()),

            # From the west side of Guard House 1 to the east side
            ("Guard House 1 West", "East Forest Redux Laddercave, East Forest Redux_gate", set()),
            ("Guard House 1 West", "East Forest Redux Laddercave, Forest Boss Room_", set()),

            # Upper exit from the Forest Grave Path, use LS at the ladder by the gate switch
            ("Forest Grave Path Main", "Sword Access, East Forest Redux_upper", set()),

            # Fortress Exterior
            # shop, ls at the ladder by the telescope
            ("Fortress Exterior from Overworld", "Fortress Courtyard, Shop_", set()),
            # Fortress main entry and grave path lower entry, ls at the ladder by the telescope
            ("Fortress Exterior from Overworld", "Fortress Courtyard, Fortress Main_Big Door", set()),
            ("Fortress Exterior from Overworld", "Fortress Courtyard, Fortress Reliquary_Lower", set()),
            # Upper exits from the courtyard. Use the ramp in the courtyard, then the blocks north of the first fuse
            ("Fortress Exterior from Overworld", "Fortress Courtyard, Fortress Reliquary_Upper", set()),
            ("Fortress Exterior from Overworld", "Fortress Courtyard, Fortress East_", set()),

            # same as above, except from the east side of the area
            ("Fortress Exterior from East Forest", "Fortress Courtyard, Overworld Redux_", set()),
            ("Fortress Exterior from East Forest", "Fortress Courtyard, Shop_", set()),
            ("Fortress Exterior from East Forest", "Fortress Courtyard, Fortress Main_Big Door", set()),
            ("Fortress Exterior from East Forest", "Fortress Courtyard, Fortress Reliquary_Lower", set()),
            ("Fortress Exterior from East Forest", "Fortress Courtyard, Fortress Reliquary_Upper", set()),
            ("Fortress Exterior from East Forest", "Fortress Courtyard, Fortress East_", set()),

            # same as above, except from the Beneath the Vault entrance ladder
            ("Fortress Exterior near cave", "Fortress Courtyard, Overworld Redux_",
             {"Ladder to Beneath the Vault"}),
            ("Fortress Exterior near cave", "Fortress Courtyard, Fortress Main_Big Door",
             {"Ladder to Beneath the Vault"}),
            ("Fortress Exterior near cave", "Fortress Courtyard, Fortress Reliquary_Lower",
             {"Ladder to Beneath the Vault"}),
            ("Fortress Exterior near cave", "Fortress Courtyard, Fortress Reliquary_Upper",
             {"Ladder to Beneath the Vault"}),
            ("Fortress Exterior near cave", "Fortress Courtyard, Fortress East_",
             {"Ladder to Beneath the Vault"}),

            # ls at the ladder, need to gain a little height to get up the stairs
            # excluded in non-ER due to soft lock potential
            ("Lower Mountain", "Mountain, Mountaintop_", set()),

            # Where the rope is behind Monastery. Connecting here since, if you have this region, you don't need a sword
            ("Quarry Monastery Entry", "Quarry Redux, Monastery_back", set()),

            # Swamp to Gauntlet
            ("Swamp Mid", "Swamp Redux 2, Cathedral Arena_",
                {"Ladders in Swamp"}),
            # Swamp to Overworld upper
            ("Swamp Mid", "Swamp Redux 2, Overworld Redux_wall",
                {"Ladders in Swamp"}),
            # Ladder by the hero grave
            ("Back of Swamp", "Swamp Redux 2, Overworld Redux_conduit", set()),
            ("Back of Swamp", "Swamp Redux 2, Shop_", set()),
            # Need to put the cathedral HC code mid-flight
            ("Back of Swamp", "Swamp Redux 2, Cathedral Redux_secret", set()),
        ]

        for region_name, scene_dest, ladders in ladder_storages:
            portal_name, paired_region = get_portal_info(scene_dest)
            # this is the only exception, requiring holy cross as well
            if portal_name == "Swamp to Cathedral Secret Legend Room Entrance" and region_name == "Back of Swamp":
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player)
                    and has_ability(holy_cross, state, world)
                    and (has_ladder("Ladders in Swamp", state, world)
                         or has_ice_grapple_logic(True, state, world)
                         or not options.entrance_rando))
            # soft locked without this ladder
            elif portal_name == "West Garden Exit after Boss" and not options.entrance_rando:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player)
                    and (state.has("Ladders to West Bell", player)))
            # soft locked unless you have either ladder. if you have laurels, you use the other Entrance
            elif portal_name in {"Furnace Exit towards West Garden", "Furnace Exit to Dark Tomb"} \
                    and not options.entrance_rando:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player)
                    and state.has_any({"Ladder in Dark Tomb", "Ladders to West Bell"}, player))
            # soft locked for the same reasons as above
            elif portal_name in {"Entrance to Furnace near West Garden", "West Garden Entrance from Furnace"} \
                    and not options.entrance_rando:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player) and state.has_any(ladders, player)
                    and state.has_any({"Ladder in Dark Tomb", "Ladders to West Bell"}, player))
            # soft locked if you can't get past garden knight backwards or up the belltower ladders
            elif portal_name == "West Garden Entrance near Belltower" and not options.entrance_rando:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player) and state.has_any(ladders, player)
                    and state.has_any({"Ladders to West Bell", laurels}, player))
            # soft locked if you can't get back out
            elif portal_name == "Fortress Courtyard to Beneath the Vault" and not options.entrance_rando:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player) and state.has("Ladder to Beneath the Vault", player)
                    and has_lantern(state, world))
            elif portal_name == "Atoll Lower Entrance" and not options.entrance_rando:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player) and state.has_any(ladders, player)
                    and (state.has_any({"Ladders in Overworld Town", grapple}, player)
                         or has_ice_grapple_logic(True, state, world)))
            elif portal_name == "Atoll Upper Entrance" and not options.entrance_rando:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player) and state.has_any(ladders, player)
                    and state.has(grapple, player) or has_ability(prayer, state, world))
            # soft lock potential
            elif portal_name in {"Special Shop Entrance", "Stairs to Top of the Mountain", "Swamp Upper Entrance",
                                 "Swamp Lower Entrance", "Caustic Light Cave Entrance"} and not options.entrance_rando:
                continue
            # soft lock if you don't have the ladder, I regret writing unrestricted logic
            elif portal_name == "Temple Rafters Entrance" and not options.entrance_rando:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player)
                    and state.has_any(ladders, player)
                    and (state.has("Ladder near Temple Rafters", player)
                         or (state.has_all({laurels, grapple}, player)
                             and ((state.has("Ladders near Patrol Cave", player)
                                   and (state.has("Ladders near Dark Tomb", player)
                                        or state.has("Ladder to Quarry", player)
                                        and (state.has(fire_wand, player) or has_sword(state, player))))
                                  or state.has("Ladders near Overworld Checkpoint", player)
                                  or has_ice_grapple_logic(True, state, world)))))
            # if no ladder items are required, just do the basic stick only lambda
            elif not ladders or not options.shuffle_ladders:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player))
            # one ladder required
            elif len(ladders) == 1:
                ladder = ladders.pop()
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player) and state.has(ladder, player))
            # if multiple ladders can be used
            else:
                regions[region_name].connect(
                    regions[paired_region],
                    name=portal_name + " (LS) " + region_name,
                    rule=lambda state: has_stick(state, player) and state.has_any(ladders, player))


def set_er_location_rules(world: "TunicWorld") -> None:
    player = world.player
    options = world.options

    forbid_item(world.get_location("Secret Gathering Place - 20 Fairy Reward"), fairies, player)

    # Ability Shuffle Exclusive Rules
    set_rule(world.get_location("East Forest - Dancing Fox Spirit Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Forest Grave Path - Holy Cross Code by Grave"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("East Forest - Golden Obelisk Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Beneath the Well - [Powered Secret Room] Chest"),
             lambda state: state.has("Activate Furnace Fuse", player))
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
    set_rule(world.get_location("Overworld - [Southwest] Flowers Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Overworld - [East] Weathervane Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Overworld - [Northeast] Flowers Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Overworld - [Southwest] Haiku Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Overworld - [Northwest] Golden Obelisk Page"),
             lambda state: has_ability(holy_cross, state, world))

    # Overworld
    set_rule(world.get_location("Overworld - [Southwest] Grapple Chest Over Walkway"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Overworld - [Southwest] West Beach Guarded By Turret 2"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Overworld - [Southwest] From West Garden"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Overworld - [Southeast] Page on Pillar by Swamp"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Overworld - [Southwest] Fountain Page"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Overworld - [Northwest] Page on Pillar by Dark Tomb"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Old House - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Overworld - [East] Grapple Chest"),
             lambda state: state.has(grapple, player))
    set_rule(world.get_location("Sealed Temple - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Caustic Light Cave - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Cube Cave - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Old House - Holy Cross Door Page"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Maze Cave - Maze Room Holy Cross"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Old House - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Patrol Cave - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Ruined Passage - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Hourglass Cave - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
    set_rule(world.get_location("Secret Gathering Place - Holy Cross Chest"),
             lambda state: has_ability(holy_cross, state, world))
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
    set_rule(world.get_location("East Forest - Ice Rod Grapple Chest"), lambda state: (
            state.has_all({grapple, ice_dagger, fire_wand}, player) and has_ability(icebolt, state, world)))

    # West Garden
    set_rule(world.get_location("West Garden - [North] Across From Page Pickup"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("West Garden - [West] In Flooded Walkway"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("West Garden - [West Lowlands] Tree Holy Cross Chest"),
             lambda state: state.has(laurels, player) and has_ability(holy_cross, state, world))
    set_rule(world.get_location("West Garden - [East Lowlands] Page Behind Ice Dagger House"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("West Garden - [Central Lowlands] Below Left Walkway"),
             lambda state: state.has(laurels, player))

    # Ruined Atoll
    set_rule(world.get_location("Ruined Atoll - [West] Near Kevin Block"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Ruined Atoll - [East] Locked Room Lower Chest"),
             lambda state: state.has(laurels, player) or state.has(key, player, 2))
    set_rule(world.get_location("Ruined Atoll - [East] Locked Room Upper Chest"),
             lambda state: state.has(laurels, player) or state.has(key, player, 2))

    # Frog's Domain
    set_rule(world.get_location("Frog's Domain - Side Room Grapple Secret"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Frog's Domain - Grapple Above Hot Tub"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Frog's Domain - Escape Chest"),
             lambda state: state.has_any({grapple, laurels}, player))

    # Eastern Vault Fortress
    set_rule(world.get_location("Fortress Arena - Hexagon Red"),
             lambda state: state.has(vault_key, player))

    # Beneath the Vault
    set_rule(world.get_location("Beneath the Fortress - Bridge"),
             lambda state: state.has_group("Melee Weapons", player, 1) or state.has_any({laurels, fire_wand}, player))

    # Quarry
    set_rule(world.get_location("Quarry - [Central] Above Ladder Dash Chest"),
             lambda state: state.has(laurels, player))

    # Ziggurat
    # if ER is off, you still need to get past the Admin or you'll get stuck in lower zig
    set_rule(world.get_location("Rooted Ziggurat Upper - Near Bridge Switch"),
             lambda state: has_sword(state, player) or (state.has(fire_wand, player) and (state.has(laurels, player)
                                                                                          or options.entrance_rando)))
    set_rule(world.get_location("Rooted Ziggurat Lower - After Guarded Fuse"),
             lambda state: has_sword(state, player) and has_ability(prayer, state, world))

    # Bosses
    set_rule(world.get_location("Fortress Arena - Siege Engine/Vault Key Pickup"),
             lambda state: has_sword(state, player))
    # nmg - kill Librarian with a lure, or gun I guess
    set_rule(world.get_location("Librarian - Hexagon Green"),
             lambda state: (has_sword(state, player) or options.logic_rules)
             and has_ladder("Ladders in Library", state, world))
    # nmg - kill boss scav with orb + firecracker, or similar
    set_rule(world.get_location("Rooted Ziggurat Lower - Hexagon Blue"),
             lambda state: has_sword(state, player) or (state.has(grapple, player) and options.logic_rules))

    # Swamp
    set_rule(world.get_location("Cathedral Gauntlet - Gauntlet Reward"),
             lambda state: state.has(fire_wand, player) and has_sword(state, player))
    set_rule(world.get_location("Swamp - [Entrance] Above Entryway"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Swamp - [South Graveyard] Upper Walkway Dash Chest"),
             lambda state: state.has(laurels, player))
    # these two swamp checks really want you to kill the big skeleton first
    set_rule(world.get_location("Swamp - [South Graveyard] 4 Orange Skulls"),
             lambda state: has_sword(state, player))

    # Hero's Grave and Far Shore
    set_rule(world.get_location("Hero's Grave - Tooth Relic"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Hero's Grave - Mushroom Relic"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Hero's Grave - Ash Relic"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Hero's Grave - Flowers Relic"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Hero's Grave - Effigy Relic"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Hero's Grave - Feathers Relic"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Far Shore - Secret Chest"),
             lambda state: state.has(laurels, player))

    # Events
    set_rule(world.get_location("Eastern Bell"),
             lambda state: (has_stick(state, player) or state.has(fire_wand, player)))
    set_rule(world.get_location("Western Bell"),
             lambda state: (has_stick(state, player) or state.has(fire_wand, player)))
    set_rule(world.get_location("Furnace Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("South and West Fortress Exterior Fuses"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("Upper and Central Fortress Exterior Fuses"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("Beneath the Vault Fuse"),
             lambda state: state.has("Activate South and West Fortress Exterior Fuses", player))
    set_rule(world.get_location("Eastern Vault West Fuses"),
             lambda state: state.has("Activate Beneath the Vault Fuse", player))
    set_rule(world.get_location("Eastern Vault East Fuse"),
             lambda state: state.has_all({"Activate Upper and Central Fortress Exterior Fuses",
                                          "Activate South and West Fortress Exterior Fuses"}, player))
    set_rule(world.get_location("Quarry Connector Fuse"),
             lambda state: has_ability(prayer, state, world) and state.has(grapple, player))
    set_rule(world.get_location("Quarry Fuse"),
             lambda state: state.has("Activate Quarry Connector Fuse", player))
    set_rule(world.get_location("Ziggurat Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("West Garden Fuse"),
             lambda state: has_ability(prayer, state, world))
    set_rule(world.get_location("Library Fuse"),
             lambda state: has_ability(prayer, state, world))

    # Bombable Walls
    for location_name in bomb_walls:
        set_rule(world.get_location(location_name), lambda state: state.has(gun, player) or can_shop(state, world))

    # Shop
    set_rule(world.get_location("Shop - Potion 1"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Shop - Potion 2"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Shop - Coin 1"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Shop - Coin 2"),
             lambda state: has_sword(state, player))
