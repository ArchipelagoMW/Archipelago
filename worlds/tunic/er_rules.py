from typing import Dict, FrozenSet, Tuple, TYPE_CHECKING
from worlds.generic.Rules import set_rule, forbid_item
from .options import IceGrappling, LadderStorage
from .rules import (has_ability, has_sword, has_stick, has_ice_grapple_logic, has_lantern, has_mask, can_ladder_storage,
                    laurels_zip, bomb_walls)
from .er_data import Portal, get_portal_outlet_region
from .ladder_storage_data import ow_ladder_groups, region_ladders, easy_ls, medium_ls, hard_ls
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
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
    regions["Overworld Belltower"].connect(
        connecting_region=regions["Overworld"])

    # ice grapple rudeling across rubble, drop bridge, ice grapple rudeling down
    regions["Overworld Belltower"].connect(
        connecting_region=regions["Overworld to West Garden Upper"],
        rule=lambda state: has_ladder("Ladders to West Bell", state, world)
        or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
    regions["Overworld to West Garden Upper"].connect(
        connecting_region=regions["Overworld Belltower"],
        rule=lambda state: has_ladder("Ladders to West Bell", state, world))

    regions["Overworld Belltower"].connect(
        connecting_region=regions["Overworld Belltower at Bell"],
        rule=lambda state: has_ladder("Ladders to West Bell", state, world))

    # long dong, do not make a reverse connection here or to belltower, maybe readd later
    # regions["Overworld above Patrol Cave"].connect(
    #     connecting_region=regions["Overworld Belltower at Bell"],
    #     rule=lambda state: options.logic_rules and state.has(fire_wand, player))

    # can laurels through the ruined passage door at either corner
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Ruined Passage Door"],
        rule=lambda state: state.has(key, player, 2)
        or laurels_zip(state, world))
    regions["Overworld Ruined Passage Door"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: laurels_zip(state, world))

    regions["Overworld"].connect(
        connecting_region=regions["After Ruined Passage"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
    regions["After Ruined Passage"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world))

    # for the hard ice grapple, get to the chest after the bomb wall, grab a slime, and grapple push down
    # you can ice grapple through the bomb wall, so no need for shop logic checking
    regions["Overworld"].connect(
        connecting_region=regions["Above Ruined Passage"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world)
        or state.has(laurels, player)
        or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
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
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
    regions["East Overworld"].connect(
        connecting_region=regions["Above Ruined Passage"],
        rule=lambda state: has_ladder("Ladders near Weathervane", state, world)
        or state.has(laurels, player))

    # nmg: ice grapple the slimes, works both ways consistently
    regions["East Overworld"].connect(
        connecting_region=regions["After Ruined Passage"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
    regions["After Ruined Passage"].connect(
        connecting_region=regions["East Overworld"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

    regions["Overworld"].connect(
        connecting_region=regions["East Overworld"],
        rule=lambda state: has_ladder("Ladders near Overworld Checkpoint", state, world)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
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
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
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
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
    regions["Overworld above Patrol Cave"].connect(
        connecting_region=regions["East Overworld"],
        rule=lambda state: has_ladder("Ladders near Overworld Checkpoint", state, world))

    regions["Overworld above Patrol Cave"].connect(
        connecting_region=regions["Upper Overworld"],
        rule=lambda state: has_ladder("Ladders near Patrol Cave", state, world)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
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

    # ice grapple push guard captain down the ledge
    regions["Upper Overworld"].connect(
        connecting_region=regions["Overworld after Temple Rafters"],
        rule=lambda state: has_ladder("Ladder near Temple Rafters", state, world)
        or has_ice_grapple_logic(True, IceGrappling.option_medium, state, world))
    regions["Overworld after Temple Rafters"].connect(
        connecting_region=regions["Upper Overworld"],
        rule=lambda state: has_ladder("Ladder near Temple Rafters", state, world)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

    regions["Overworld above Quarry Entrance"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ladder("Ladders near Dark Tomb", state, world))
    regions["Overworld"].connect(
        connecting_region=regions["Overworld above Quarry Entrance"],
        rule=lambda state: has_ladder("Ladders near Dark Tomb", state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld after Envoy"],
        rule=lambda state: state.has_any({laurels, grapple, gun}, player)
        or state.has("Sword Upgrade", player, 4))
    regions["Overworld after Envoy"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has_any({laurels, grapple, gun}, player)
        or state.has("Sword Upgrade", player, 4))

    regions["Overworld after Envoy"].connect(
        connecting_region=regions["Overworld Quarry Entry"],
        rule=lambda state: has_ladder("Ladder to Quarry", state, world))
    regions["Overworld Quarry Entry"].connect(
        connecting_region=regions["Overworld after Envoy"],
        rule=lambda state: has_ladder("Ladder to Quarry", state, world))

    # ice grapple through the gate
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Quarry Entry"],
        rule=lambda state: has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
    regions["Overworld Quarry Entry"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ice_grapple_logic(False, IceGrappling.option_easy, state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Swamp Upper Entry"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld Swamp Upper Entry"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has(laurels, player))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Swamp Lower Entry"],
        rule=lambda state: has_ladder("Ladder to Swamp", state, world)
        or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
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
        or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))

    # lure enemy over and ice grapple through
    regions["Overworld"].connect(
        connecting_region=regions["Overworld Southeast Cross Door"],
        rule=lambda state: has_ability(holy_cross, state, world)
        or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
    regions["Overworld Southeast Cross Door"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: has_ability(holy_cross, state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Fountain Cross Door"],
        rule=lambda state: has_ability(holy_cross, state, world)
        or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
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
        or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))

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
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

    regions["Overworld"].connect(
        connecting_region=regions["Overworld Tunnel Turret"],
        rule=lambda state: state.has(laurels, player))
    regions["Overworld Tunnel Turret"].connect(
        connecting_region=regions["Overworld"],
        rule=lambda state: state.has_any({grapple, laurels}, player))

    cube_entrance = regions["Overworld"].connect(
        connecting_region=regions["Cube Cave Entrance Region"],
        rule=lambda state: state.has(gun, player) or can_shop(state, world))
    world.multiworld.register_indirect_condition(regions["Shop"], cube_entrance)
    regions["Cube Cave Entrance Region"].connect(
        connecting_region=regions["Overworld"])

    # drop a rudeling down, icebolt or ice bomb
    regions["Overworld"].connect(
        connecting_region=regions["Overworld to West Garden from Furnace"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_hard, state, world))

    # Overworld side areas
    regions["Old House Front"].connect(
        connecting_region=regions["Old House Back"])
    # laurels through the gate, use left wall to space yourself
    regions["Old House Back"].connect(
        connecting_region=regions["Old House Front"],
        rule=lambda state: laurels_zip(state, world))

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

    # ice grapple up to dance fox spot, and vice versa
    regions["East Forest"].connect(
        connecting_region=regions["East Forest Dance Fox Spot"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
    regions["East Forest Dance Fox Spot"].connect(
        connecting_region=regions["East Forest"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

    regions["East Forest"].connect(
        connecting_region=regions["East Forest Portal"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["East Forest Portal"].connect(
        connecting_region=regions["East Forest"])

    regions["East Forest"].connect(
        connecting_region=regions["Lower Forest"],
        rule=lambda state: has_ladder("Ladders to Lower Forest", state, world)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
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

    # ice grapple from upper grave path exit to the rest of it
    regions["Forest Grave Path Upper"].connect(
        connecting_region=regions["Forest Grave Path Main"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
    # for the ice grapple, lure a rudeling up top, then grapple push it across
    regions["Forest Grave Path Main"].connect(
        connecting_region=regions["Forest Grave Path Upper"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))

    regions["Forest Grave Path Main"].connect(
        connecting_region=regions["Forest Grave Path by Grave"])
    # ice grapple or laurels through the gate
    regions["Forest Grave Path by Grave"].connect(
        connecting_region=regions["Forest Grave Path Main"],
        rule=lambda state: has_ice_grapple_logic(False, IceGrappling.option_easy, state, world)
        or laurels_zip(state, world))

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
    # can laurels through the gate, no setup needed
    regions["Dark Tomb Checkpoint"].connect(
        connecting_region=regions["Well Boss"],
        rule=lambda state: laurels_zip(state, world))

    regions["Dark Tomb Entry Point"].connect(
        connecting_region=regions["Dark Tomb Upper"],
        rule=lambda state: has_lantern(state, world))
    regions["Dark Tomb Upper"].connect(
        connecting_region=regions["Dark Tomb Entry Point"])

    # ice grapple through the wall, get the little secret sound to trigger
    regions["Dark Tomb Upper"].connect(
        connecting_region=regions["Dark Tomb Main"],
        rule=lambda state: has_ladder("Ladder in Dark Tomb", state, world)
        or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
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

    # you can grapple Garden Knight to aggro it, then ledge it
    regions["West Garden after Boss"].connect(
        connecting_region=regions["West Garden"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
    # ice grapple push Garden Knight off the side
    regions["West Garden"].connect(
        connecting_region=regions["West Garden after Boss"],
        rule=lambda state: state.has(laurels, player) or has_sword(state, player)
        or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))

    regions["West Garden"].connect(
        connecting_region=regions["West Garden Hero's Grave Region"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["West Garden Hero's Grave Region"].connect(
        connecting_region=regions["West Garden"])

    regions["West Garden Portal"].connect(
        connecting_region=regions["West Garden by Portal"])
    regions["West Garden by Portal"].connect(
        connecting_region=regions["West Garden Portal"],
        rule=lambda state: has_ability(prayer, state, world) and state.has("Activate West Garden Fuse", player))

    regions["West Garden by Portal"].connect(
        connecting_region=regions["West Garden Portal Item"],
        rule=lambda state: state.has(laurels, player))
    regions["West Garden Portal Item"].connect(
        connecting_region=regions["West Garden by Portal"],
        rule=lambda state: state.has(laurels, player))

    # can ice grapple to and from the item behind the magic dagger house
    regions["West Garden Portal Item"].connect(
        connecting_region=regions["West Garden"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
    regions["West Garden"].connect(
        connecting_region=regions["West Garden Portal Item"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_medium, state, world))

    # Atoll and Frog's Domain
    # ice grapple the bird below the portal
    regions["Ruined Atoll"].connect(
        connecting_region=regions["Ruined Atoll Lower Entry Area"],
        rule=lambda state: state.has(laurels, player)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
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
        and (has_ladder("Ladders in South Atoll", state, world)
             # shoot fuse and have the shot hit you mid-LS
             or (can_ladder_storage(state, world) and state.has(fire_wand, player)
                 and options.ladder_storage >= LadderStorage.option_hard)))
    regions["Ruined Atoll Statue"].connect(
        connecting_region=regions["Ruined Atoll"])

    regions["Frog Stairs Eye Exit"].connect(
        connecting_region=regions["Frog Stairs Upper"],
        rule=lambda state: has_ladder("Ladders to Frog's Domain", state, world)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
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
        connecting_region=regions["Library Exterior by Tree"])
    regions["Library Exterior by Tree"].connect(
        connecting_region=regions["Library Exterior Tree Region"],
        rule=lambda state: has_ability(prayer, state, world))

    regions["Library Exterior by Tree"].connect(
        connecting_region=regions["Library Exterior Ladder Region"],
        rule=lambda state: state.has_any({grapple, laurels}, player)
        and has_ladder("Ladders in Library", state, world))
    regions["Library Exterior Ladder Region"].connect(
        connecting_region=regions["Library Exterior by Tree"],
        rule=lambda state: state.has(grapple, player)
        or (state.has(laurels, player) and has_ladder("Ladders in Library", state, world)))

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
        connecting_region=regions["Library Lab on Portal Pad"],
        rule=lambda state: has_ladder("Ladders in Library", state, world))
    regions["Library Lab on Portal Pad"].connect(
        connecting_region=regions["Library Lab"],
        rule=lambda state: has_ladder("Ladders in Library", state, world)
        or state.has(laurels, player))

    regions["Library Lab on Portal Pad"].connect(
        connecting_region=regions["Library Portal"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Library Portal"].connect(
        connecting_region=regions["Library Lab on Portal Pad"])

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

    # shoot far fire pot, enemy gets aggro'd
    regions["Fortress Exterior near cave"].connect(
        connecting_region=regions["Fortress Courtyard"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_hard, state, world))

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
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

    regions["Fortress Courtyard Upper"].connect(
        connecting_region=regions["Fortress Courtyard"])
    # nmg: can ice grapple to the upper ledge
    regions["Fortress Courtyard"].connect(
        connecting_region=regions["Fortress Courtyard Upper"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

    regions["Fortress Courtyard Upper"].connect(
        connecting_region=regions["Fortress Exterior from Overworld"])

    regions["Beneath the Vault Ladder Exit"].connect(
        connecting_region=regions["Beneath the Vault Main"],
        rule=lambda state: has_ladder("Ladder to Beneath the Vault", state, world)
        and has_lantern(state, world)
        # there's some boxes in the way
        and (has_stick(state, player) or state.has_any((gun, grapple, fire_wand, laurels), player)))
    # on the reverse trip, you can lure an enemy over to break the boxes if needed
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
    regions["Fortress East Shortcut Lower"].connect(
        connecting_region=regions["Fortress East Shortcut Upper"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

    regions["Eastern Vault Fortress"].connect(
        connecting_region=regions["Eastern Vault Fortress Gold Door"],
        rule=lambda state: state.has_all({"Activate Eastern Vault West Fuses",
                                          "Activate Eastern Vault East Fuse"}, player)
        or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
    regions["Eastern Vault Fortress Gold Door"].connect(
        connecting_region=regions["Eastern Vault Fortress"],
        rule=lambda state: has_ice_grapple_logic(False, IceGrappling.option_easy, state, world))

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

    regions["Fortress Grave Path Upper"].connect(
        connecting_region=regions["Fortress Grave Path"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

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
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

    # nmg: bring a scav over, then ice grapple through the door, only with ER on to avoid soft lock
    regions["Even Lower Quarry"].connect(
        connecting_region=regions["Lower Quarry Zig Door"],
        rule=lambda state: state.has("Activate Quarry Fuse", player)
        or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))

    # nmg: use ice grapple to get from the beginning of Quarry to the door without really needing mask only with ER on
    regions["Quarry"].connect(
        connecting_region=regions["Lower Quarry Zig Door"],
        rule=lambda state: has_ice_grapple_logic(True, IceGrappling.option_hard, state, world))

    regions["Monastery Front"].connect(
        connecting_region=regions["Monastery Back"])
    # laurels through the gate, no setup needed
    regions["Monastery Back"].connect(
        connecting_region=regions["Monastery Front"],
        rule=lambda state: laurels_zip(state, world))

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
    # nmg: can ice grapple on the voidlings to the double admin fight, still need to pray at the fuse
    regions["Rooted Ziggurat Lower Back"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Front"],
        rule=lambda state: (state.has(laurels, player)
                            or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))
        and has_ability(prayer, state, world)
        and has_sword(state, player))

    regions["Rooted Ziggurat Lower Back"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room Entrance"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Rooted Ziggurat Portal Room Entrance"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Back"])

    regions["Zig Skip Exit"].connect(
        connecting_region=regions["Rooted Ziggurat Lower Front"])

    regions["Rooted Ziggurat Portal"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room"])
    regions["Rooted Ziggurat Portal Room"].connect(
        connecting_region=regions["Rooted Ziggurat Portal"],
        rule=lambda state: has_ability(prayer, state, world))

    regions["Rooted Ziggurat Portal Room"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room Exit"],
        rule=lambda state: state.has("Activate Ziggurat Fuse", player))
    regions["Rooted Ziggurat Portal Room Exit"].connect(
        connecting_region=regions["Rooted Ziggurat Portal Room"])

    # Swamp and Cathedral
    regions["Swamp Front"].connect(
        connecting_region=regions["Swamp Mid"],
        rule=lambda state: has_ladder("Ladders in Swamp", state, world)
        or state.has(laurels, player)
        or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
    regions["Swamp Mid"].connect(
        connecting_region=regions["Swamp Front"],
        rule=lambda state: has_ladder("Ladders in Swamp", state, world)
        or state.has(laurels, player)
        or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))

    # a whole lot of stuff to basically say "you need to pray at the overworld fuse"
    swamp_mid_to_cath = regions["Swamp Mid"].connect(
        connecting_region=regions["Swamp to Cathedral Main Entrance Region"],
        rule=lambda state: (has_ability(prayer, state, world)
                            and (state.has(laurels, player)
                                 # blam yourself in the face with a wand shot off the fuse
                                 or (can_ladder_storage(state, world) and state.has(fire_wand, player)
                                     and options.ladder_storage >= LadderStorage.option_hard
                                     and (not options.shuffle_ladders
                                          or state.has_any({"Ladders in Overworld Town",
                                                            "Ladder to Swamp",
                                                            "Ladders near Weathervane"}, player)
                                          or (state.has("Ladder to Ruined Atoll", player)
                                              and state.can_reach_region("Overworld Beach", player))))))
        or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))

    if options.ladder_storage >= LadderStorage.option_hard and options.shuffle_ladders:
        world.multiworld.register_indirect_condition(regions["Overworld Beach"], swamp_mid_to_cath)

    regions["Swamp to Cathedral Main Entrance Region"].connect(
        connecting_region=regions["Swamp Mid"],
        rule=lambda state: has_ice_grapple_logic(False, IceGrappling.option_easy, state, world))

    # grapple push the enemy by the door down, then grapple to it. Really jank
    regions["Swamp Mid"].connect(
        connecting_region=regions["Swamp Ledge under Cathedral Door"],
        rule=lambda state: has_ladder("Ladders in Swamp", state, world)
        or has_ice_grapple_logic(True, IceGrappling.option_hard, state, world))
    # ice grapple enemy standing at the door
    regions["Swamp Ledge under Cathedral Door"].connect(
        connecting_region=regions["Swamp Mid"],
        rule=lambda state: has_ladder("Ladders in Swamp", state, world)
        or has_ice_grapple_logic(True, IceGrappling.option_easy, state, world))

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

    # ice grapple down from the pillar, or do that really annoying laurels zip
    # the zip goes to front or mid, just doing mid since mid -> front can be done with laurels alone
    regions["Back of Swamp Laurels Area"].connect(
        connecting_region=regions["Swamp Mid"],
        rule=lambda state: laurels_zip(state, world)
        or (state.has(laurels, player)
            and has_ice_grapple_logic(True, IceGrappling.option_easy, state, world)))
    # get one pillar from the gate, then dash onto the gate, very tricky
    regions["Swamp Front"].connect(
        connecting_region=regions["Back of Swamp Laurels Area"],
        rule=lambda state: laurels_zip(state, world))

    regions["Back of Swamp"].connect(
        connecting_region=regions["Swamp Hero's Grave Region"],
        rule=lambda state: has_ability(prayer, state, world))
    regions["Swamp Hero's Grave Region"].connect(
        connecting_region=regions["Back of Swamp"])

    regions["Cathedral"].connect(
        connecting_region=regions["Cathedral to Gauntlet"],
        rule=lambda state: (has_ability(prayer, state, world)
                            or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
        or options.entrance_rando)  # elevator is always there in ER
    regions["Cathedral to Gauntlet"].connect(
        connecting_region=regions["Cathedral"])

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

    if options.ladder_storage:
        def get_portal_info(portal_sd: str) -> Tuple[str, str]:
            for portal1, portal2 in portal_pairs.items():
                if portal1.scene_destination() == portal_sd:
                    return portal1.name, get_portal_outlet_region(portal2, world)
                if portal2.scene_destination() == portal_sd:
                    return portal2.name, get_portal_outlet_region(portal1, world)
            raise Exception("no matches found in get_paired_region")

        # connect ls elevation regions to their destinations
        def ls_connect(origin_name: str, portal_sdt: str) -> None:
            p_name, paired_region_name = get_portal_info(portal_sdt)
            ladder_regions[origin_name].connect(
                regions[paired_region_name],
                name=p_name + " (LS) " + origin_name)

        # get what non-overworld ladder storage connections we want together
        non_ow_ls_list = []
        non_ow_ls_list.extend(easy_ls)
        if options.ladder_storage >= LadderStorage.option_medium:
            non_ow_ls_list.extend(medium_ls)
            if options.ladder_storage >= LadderStorage.option_hard:
                non_ow_ls_list.extend(hard_ls)

        # create the ls elevation regions
        ladder_regions: Dict[str, Region] = {}
        for name in ow_ladder_groups.keys():
            ladder_regions[name] = Region(name, player, world.multiworld)

        # connect the ls elevations to each other where applicable
        if options.ladder_storage >= LadderStorage.option_medium:
            for i in range(len(ow_ladder_groups) - 1):
                ladder_regions[f"LS Elev {i}"].connect(ladder_regions[f"LS Elev {i + 1}"])

        # connect the applicable overworld regions to the ls elevation regions
        for origin_region, ladders in region_ladders.items():
            for ladder_region, region_info in ow_ladder_groups.items():
                # checking if that region has a ladder or ladders for that elevation
                common_ladders: FrozenSet[str] = frozenset(ladders.intersection(region_info.ladders))
                if common_ladders:
                    if options.shuffle_ladders:
                        regions[origin_region].connect(
                            connecting_region=ladder_regions[ladder_region],
                            rule=lambda state, lads=common_ladders: state.has_any(lads, player)
                            and can_ladder_storage(state, world))
                    else:
                        regions[origin_region].connect(
                            connecting_region=ladder_regions[ladder_region],
                            rule=lambda state: can_ladder_storage(state, world))

        # connect ls elevation regions to the region on the other side of the portals
        for ladder_region, region_info in ow_ladder_groups.items():
            for portal_dest in region_info.portals:
                ls_connect(ladder_region, "Overworld Redux, " + portal_dest)

        # convenient staircase means this one is easy difficulty, even though there's an elevation change
        ls_connect("LS Elev 0", "Overworld Redux, Furnace_gyro_west")

        # connect ls elevation regions to regions where you can get an enemy to knock you down, also well rail
        if options.ladder_storage >= LadderStorage.option_medium:
            for ladder_region, region_info in ow_ladder_groups.items():
                for dest_region in region_info.regions:
                    ladder_regions[ladder_region].connect(
                        connecting_region=regions[dest_region],
                        name=ladder_region + " (LS) " + dest_region)
            # well rail, need height off portal pad for one side, and a tiny extra from stairs on the other
            ls_connect("LS Elev 3", "Overworld Redux, Sewer_west_aqueduct")
            ls_connect("LS Elev 3", "Overworld Redux, Furnace_gyro_upper_north")

        # connect ls elevation regions to portals where you need to get behind the map to enter it
        if options.ladder_storage >= LadderStorage.option_hard:
            ls_connect("LS Elev 1", "Overworld Redux, EastFiligreeCache_")
            ls_connect("LS Elev 2", "Overworld Redux, Town_FiligreeRoom_")
            ls_connect("LS Elev 2", "Overworld Redux, Ruins Passage_west")
            ls_connect("LS Elev 3", "Overworld Redux, Overworld Interiors_house")
            ls_connect("LS Elev 5", "Overworld Redux, Temple_main")

        # connect the non-overworld ones
        for ls_info in non_ow_ls_list:
            # for places where the destination is a region (so you have to get knocked down)
            if ls_info.dest_is_region:
                # none of the non-ow ones have multiple ladders that can be used, so don't need has_any
                if options.shuffle_ladders and ls_info.ladders_req:
                    regions[ls_info.origin].connect(
                        connecting_region=regions[ls_info.destination],
                        name=ls_info.destination + " (LS) " + ls_info.origin,
                        rule=lambda state, lad=ls_info.ladders_req: can_ladder_storage(state, world)
                        and state.has(lad, player))
                else:
                    regions[ls_info.origin].connect(
                        connecting_region=regions[ls_info.destination],
                        name=ls_info.destination + " (LS) " + ls_info.origin,
                        rule=lambda state: can_ladder_storage(state, world))
                continue

            portal_name, dest_region = get_portal_info(ls_info.destination)
            # these two are special cases
            if ls_info.destination == "Atoll Redux, Frog Stairs_mouth":
                regions[ls_info.origin].connect(
                    connecting_region=regions[dest_region],
                    name=portal_name + " (LS) " + ls_info.origin,
                    rule=lambda state: can_ladder_storage(state, world)
                    and (has_ladder("Ladders in South Atoll", state, world)
                         or state.has(key, player, 2)  # can do it from the rope
                         # ice grapple push a crab into the door
                         or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world)
                         or options.ladder_storage >= LadderStorage.option_medium))  # use the little ladder
            # holy cross mid-ls to get in here
            elif ls_info.destination == "Swamp Redux 2, Cathedral Redux_secret":
                if ls_info.origin == "Swamp Mid":
                    regions[ls_info.origin].connect(
                        connecting_region=regions[dest_region],
                        name=portal_name + " (LS) " + ls_info.origin,
                        rule=lambda state: can_ladder_storage(state, world) and has_ability(holy_cross, state, world)
                        and has_ladder("Ladders in Swamp", state, world))
                else:
                    regions[ls_info.origin].connect(
                        connecting_region=regions[dest_region],
                        name=portal_name + " (LS) " + ls_info.origin,
                        rule=lambda state: can_ladder_storage(state, world) and has_ability(holy_cross, state, world))

            elif options.shuffle_ladders and ls_info.ladders_req:
                regions[ls_info.origin].connect(
                    connecting_region=regions[dest_region],
                    name=portal_name + " (LS) " + ls_info.origin,
                    rule=lambda state, lad=ls_info.ladders_req: can_ladder_storage(state, world)
                    and state.has(lad, player))
            else:
                regions[ls_info.origin].connect(
                    connecting_region=regions[dest_region],
                    name=portal_name + " (LS) " + ls_info.origin,
                    rule=lambda state: can_ladder_storage(state, world))

        for region in ladder_regions.values():
            world.multiworld.regions.append(region)


def set_er_location_rules(world: "TunicWorld") -> None:
    player = world.player

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
    # ice grapple push a crab through the door
    set_rule(world.get_location("Ruined Atoll - [East] Locked Room Lower Chest"),
             lambda state: state.has(laurels, player) or state.has(key, player, 2)
             or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))
    set_rule(world.get_location("Ruined Atoll - [East] Locked Room Upper Chest"),
             lambda state: state.has(laurels, player) or state.has(key, player, 2)
             or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))

    # Frog's Domain
    set_rule(world.get_location("Frog's Domain - Side Room Grapple Secret"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Frog's Domain - Grapple Above Hot Tub"),
             lambda state: state.has_any({grapple, laurels}, player))
    set_rule(world.get_location("Frog's Domain - Escape Chest"),
             lambda state: state.has_any({grapple, laurels}, player))

    # Library Lab
    set_rule(world.get_location("Library Lab - Page 1"),
             lambda state: has_stick(state, player) or state.has_any((fire_wand, gun), player))
    set_rule(world.get_location("Library Lab - Page 2"),
             lambda state: has_stick(state, player) or state.has_any((fire_wand, gun), player))
    set_rule(world.get_location("Library Lab - Page 3"),
             lambda state: has_stick(state, player) or state.has_any((fire_wand, gun), player))

    # Eastern Vault Fortress
    set_rule(world.get_location("Fortress Arena - Hexagon Red"),
             lambda state: state.has(vault_key, player))
    # yes, you can clear the leaves with dagger
    # gun isn't included since it can only break one leaf pile at a time, and we don't check how much mana you have
    # but really, I expect the player to just throw a bomb at them if they don't have melee
    set_rule(world.get_location("Fortress Leaf Piles - Secret Chest"),
             lambda state: has_stick(state, player) or state.has(ice_dagger, player))

    # Beneath the Vault
    set_rule(world.get_location("Beneath the Fortress - Bridge"),
             lambda state: has_stick(state, player) or state.has_any({laurels, fire_wand}, player))

    # Quarry
    set_rule(world.get_location("Quarry - [Central] Above Ladder Dash Chest"),
             lambda state: state.has(laurels, player))

    # Ziggurat
    # if ER is off, while you can get the chest, you won't be able to actually get through zig
    set_rule(world.get_location("Rooted Ziggurat Upper - Near Bridge Switch"),
             lambda state: has_sword(state, player) or (state.has(fire_wand, player)
                                                        and (state.has(laurels, player)
                                                             or world.options.entrance_rando)))
    set_rule(world.get_location("Rooted Ziggurat Lower - After Guarded Fuse"),
             lambda state: has_sword(state, player) and has_ability(prayer, state, world))

    # Bosses
    set_rule(world.get_location("Fortress Arena - Siege Engine/Vault Key Pickup"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Librarian - Hexagon Green"),
             lambda state: has_sword(state, player)
             and has_ladder("Ladders in Library", state, world))
    # can ice grapple boss scav off the side
    # the grapple from the other side of the bridge isn't in logic 'cause we don't have a misc tricks option
    set_rule(world.get_location("Rooted Ziggurat Lower - Hexagon Blue"),
             lambda state: has_sword(state, player)
             or has_ice_grapple_logic(False, IceGrappling.option_medium, state, world))

    # Swamp
    set_rule(world.get_location("Cathedral Gauntlet - Gauntlet Reward"),
             lambda state: state.has(fire_wand, player) and has_sword(state, player))
    set_rule(world.get_location("Swamp - [Entrance] Above Entryway"),
             lambda state: state.has(laurels, player))
    set_rule(world.get_location("Swamp - [South Graveyard] Upper Walkway Dash Chest"),
             lambda state: state.has(laurels, player))
    # really hard to do 4 skulls with a big skeleton chasing you around
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
             lambda state: has_ability(prayer, state, world) and has_ladder("Ladders in Library", state, world))

    # Bombable Walls
    for location_name in bomb_walls:
        set_rule(world.get_location(location_name),
                 lambda state: state.has(gun, player)
                 or can_shop(state, world)
                 or has_ice_grapple_logic(False, IceGrappling.option_hard, state, world))
    # not enough space to ice grapple into here
    set_rule(world.get_location("Quarry - [East] Bombable Wall"),
             lambda state: state.has(gun, player) or can_shop(state, world))

    # Shop
    set_rule(world.get_location("Shop - Potion 1"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Shop - Potion 2"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Shop - Coin 1"),
             lambda state: has_sword(state, player))
    set_rule(world.get_location("Shop - Coin 2"),
             lambda state: has_sword(state, player))
