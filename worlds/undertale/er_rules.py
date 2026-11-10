from typing import TYPE_CHECKING
from .Rules import _undertale_is_route, _undertale_exp_available, _undertale_return_reachable_level, _undertale_has_keys, _undertale_return_reachable_atk, _undertale_return_reachable_def, _undertale_return_reachable_hp, _undertale_return_reachable_inv_tier, _undertale_return_reachable_atk_equipment, _undertale_return_reachable_def_equipment
from rule_builder.options import OptionFilter
from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, CanReachLocation, CanReachRegion
import math
from .Options import HubShopCost, RouteRequired, KillSanity, KillSanityPackSize, SpareSanity, SpareSanityPackSize, SpareSanityMaxSpares

if TYPE_CHECKING:
    from . import UndertaleWorld

def set_er_region_rules(world: "UndertaleWorld") -> None:
    player = world.player

    world.get_region("Menu").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("room_water_undynebridge").connect(
        connecting_region=world.get_region("room_water_undynebridgeend"))

    world.get_region("Trash Zone Fall").connect(
        connecting_region=world.get_region("room_water_undynebridgeend"))

    world.get_region("room_water_undynebridgeend").connect(
        connecting_region=world.get_region("Trash Zone Fall"))

    world.get_region("room_water20").connect(
        connecting_region=world.get_region("room_water21"))

    world.get_region("room_water21").connect(
        connecting_region=world.get_region("room_water20"))

    world.get_region("room_water21").connect(
        connecting_region=world.get_region("room_water_undynefinal"))

    world.get_region("room_water_undynefinal").connect(
        connecting_region=world.get_region("room_water21"))

    world.get_region("room_water_undynefinal").connect(
        connecting_region=world.get_region("room_fire2"))

    world.get_region("room_fire2").connect(
        connecting_region=world.get_region("room_water_undynefinal"))

    world.get_region("Ruins Exit").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("Hotland Exit").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("Snowdin Exit").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("Waterfall Exit").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("room_water_waterfall4").connect(
        connecting_region=world.get_region("Monster Kid Raised Ledge"))

    world.get_region("room_water7").connect(
        connecting_region=world.get_region("Room Water 7 One Way"))

    world.get_region("room_tundra_sanshouse").connect(
        connecting_region=world.get_region("Papyrus Rocks"),
        rule=Has("Complete Skeleton", options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist], operator="in")], filtered_resolution=True))

    world.get_region("Papyrus Rocks").connect(
        connecting_region=world.get_region("room_tundra_sanshouse"),
        rule=Has("Complete Skeleton", options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist], operator="in")], filtered_resolution=True))

    world.get_region("room_water_friendlyhub").connect(
        connecting_region=world.get_region("Undyne Rocks"),
        rule=Has("Fish", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist], operator="in")]))

    world.get_region("Undyne Rocks").connect(
        connecting_region=world.get_region("room_water_friendlyhub"),
        rule=Has("Fish", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist], operator="in")]))

    world.get_region("room_area1").connect(
        connecting_region=world.get_region("Ruins Entrance"),
        rule=Has("Ruins Key"))

    world.get_region("Ruins Entrance").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("room_area1").connect(
        connecting_region=world.get_region("Snowdin Entrance"),
        rule=Has("Snowdin Key"))

    world.get_region("Snowdin Entrance").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("room_area1").connect(
        connecting_region=world.get_region("Waterfall Entrance"),
        rule=Has("Waterfall Key"))

    world.get_region("Waterfall Entrance").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("room_area1").connect(
        connecting_region=world.get_region("Hotland Entrance"),
        rule=Has("Hotland Key"))

    world.get_region("Hotland Entrance").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("room_area1").connect(
        connecting_region=world.get_region("New Home Entrance"))

    world.get_region("New Home Entrance").connect(
        connecting_region=world.get_region("room_area1"))

    world.get_region("Trash Zone Fall").connect(
        connecting_region=world.get_region("room_water_trashzone1"))

    world.get_region("Menu").connect(
        connecting_region=world.get_region("???"))

    world.get_region("Ruins Pit Circle B").connect(
        connecting_region=world.get_region("room_ruins15E"))

    world.get_region("Ruins Pit Circle C").connect(
        connecting_region=world.get_region("room_ruins15E"))

    world.get_region("Ruins Pit Circle D").connect(
        connecting_region=world.get_region("room_ruins15E"))

    world.get_region("Fire Door 1").connect(
        connecting_region=world.get_region("room_fire7"))

    world.get_region("Fire Door 2").connect(
        connecting_region=world.get_region("room_fire_walkandbranch2"))

    world.get_region("room_fire_turn").connect(
        connecting_region=world.get_region("Fire Turn Part 2"))

    world.get_region("room_fire_elevator").connect(
        connecting_region=world.get_region("room_fire_elevator_l1"))

    world.get_region("room_fire_elevator").connect(
        connecting_region=world.get_region("room_fire_elevator_l2"),
        rule= CanReachRegion("room_fire_newsreport", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]))

    world.get_region("room_fire_elevator").connect(
        connecting_region=world.get_region("room_fire_elevator_l3"),
        rule= CanReachRegion("room_fire_newsreport", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]))

    world.get_region("room_fire_elevator").connect(
        connecting_region=world.get_region("room_fire_elevator_r1"))

    world.get_region("room_fire_elevator").connect(
        connecting_region=world.get_region("room_fire_elevator_r2"))

    world.get_region("room_fire_elevator").connect(
        connecting_region=world.get_region("room_fire_elevator_r3"),
        rule= CanReachRegion("room_fire_multitile", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
        | 
        CanReachRegion("room_fire_spider", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_genocide], operator="in")]))

    world.get_region("room_fire_elevator_l1").connect(
        connecting_region=world.get_region("room_fire_elevator"))

    world.get_region("room_fire_elevator_l2").connect(
        connecting_region=world.get_region("room_fire_elevator"))

    world.get_region("room_fire_elevator_l3").connect(
        connecting_region=world.get_region("room_fire_elevator"))

    world.get_region("room_fire_elevator_r1").connect(
        connecting_region=world.get_region("room_fire_elevator"))

    world.get_region("room_fire_elevator_r2").connect(
        connecting_region=world.get_region("room_fire_elevator"))

    world.get_region("room_fire_elevator_r3").connect(
        connecting_region=world.get_region("room_fire_elevator"))

    world.get_region("room_water5").connect(
        connecting_region=world.get_region("water bridge puzzle 2 after"))

    world.get_region("room_water_bridgepuzz1").connect(
        connecting_region=world.get_region("water bridge puzzle after"))

    world.get_region("room_tundra_snowpuzz").connect(
        connecting_region=world.get_region("Snow Puzz After Puzzle"))

    world.get_region("room_ruins15B").connect(
        connecting_region=world.get_region("Ruins 15B Past Puzzles"))

    world.get_region("room_ruins15C").connect(
        connecting_region=world.get_region("Ruins 15C Past Puzzles"))

    world.get_region("room_ruins15D").connect(
        connecting_region=world.get_region("Ruins 15D Past Puzzles"))

    world.get_region("room_tundra_xoxosmall").connect(
        connecting_region=world.get_region("small xoxo after puzzle"))

    world.get_region("room_tundra_xoxopuzz").connect(
        connecting_region=world.get_region("xoxo puzz after puzzle"))

    world.get_region("room_fire_core_metttest").connect(
        connecting_region=world.get_region("room_fire_core_final"),
        rule=(Has("Hotland Population Pack", math.ceil(40 / FromOption(KillSanityPackSize).resolve(world)), options=[OptionFilter(KillSanity, KillSanity.option_locked), OptionFilter(RouteRequired, RouteRequired.option_genocide)], filtered_resolution=True)))

    world.get_region("Metta Entrance").connect(
        connecting_region=world.get_region("room_fire_core_premett"))

    world.get_region("room_water_blookyard").connect(
        connecting_region=world.get_region("hapsta door"),
        rule=Has("Mystery Key"))

    world.get_region("hapsta door").connect(
        connecting_region=world.get_region("room_water_blookyard"))

    world.get_region("room_fire_core_premett").connect(
        connecting_region=world.get_region("Metta Entrance"))

    world.get_region("room_water8").connect(
        connecting_region=world.get_region("room_water9"))

    world.get_region("room_water9").connect(
        connecting_region=world.get_region("room_water8"))

    world.get_region("Metta Entrance").connect(
        connecting_region=world.get_region("room_fire_core_metttest"))

    world.get_region("room_fire_core_metttest").connect(
        connecting_region=world.get_region("Metta Entrance"))

    world.get_region("room_fire_core_final").connect(
        connecting_region=world.get_region("room_fire_core_metttest"))

    world.get_region("room_fire_core_final").connect(
        connecting_region=world.get_region("Hotland Exit"))

    world.get_region("Hotland Exit").connect(
        connecting_region=world.get_region("room_fire_core_final"))

    world.get_region("room_asghouse1").connect(
        connecting_region=world.get_region("room_basement1_final"),
        rule=_undertale_has_keys())

    world.get_region("room_basement1_final").connect(
        connecting_region=world.get_region("room_asghouse1"))

    world.get_region("room_basement1_final").connect(
        connecting_region=world.get_region("room_basement2_final"))

    world.get_region("room_basement2_final").connect(
        connecting_region=world.get_region("room_basement1_final"))

    world.get_region("room_basement2_final").connect(
        connecting_region=world.get_region("room_basement3_final"))

    world.get_region("room_basement3_final").connect(
        connecting_region=world.get_region("room_basement2_final"))

    world.get_region("room_ruins3").connect(
        connecting_region=world.get_region("Ruins 3 Past Puzzles"))

    world.get_region("room_ruins14").connect(
        connecting_region=world.get_region("Ruins 14 Past Puzzles"))

    world.get_region("room_ruins15A").connect(
        connecting_region=world.get_region("Ruins 15A Past Puzzles"))

    world.get_region("room_ruins9").connect(
        connecting_region=world.get_region("Ruins 9 Past Puzzles"))

    world.get_region("room_ruins11").connect(
        connecting_region=world.get_region("Ruins 11 Past Puzzles"))

    world.get_region("room_basement3_final").connect(
        connecting_region=world.get_region("room_basement4_final"))

    world.get_region("room_basement4_final").connect(
        connecting_region=world.get_region("room_basement3_final"))

    world.get_region("room_basement4_final").connect(
        connecting_region=world.get_region("room_lastruins_corridor"))

    world.get_region("room_lastruins_corridor").connect(
        connecting_region=world.get_region("room_basement4_final"))

    world.get_region("room_lastruins_corridor").connect(
        connecting_region=world.get_region("room_sanscorridor"))

    world.get_region("room_sanscorridor").connect(
        connecting_region=world.get_region("room_lastruins_corridor"))

    world.get_region("room_sanscorridor").connect(
        connecting_region=world.get_region("room_castle_finalshoehorn"),
        rule=lambda state, world=world, player=player: world.options.route_required.value == RouteRequired.option_neutral or world.options.route_required.value == RouteRequired.option_pacifist or (_undertale_return_reachable_hp(state, world, player, _undertale_return_reachable_level(_undertale_exp_available(state, world, player))) >= world.options.sans_req_hp and _undertale_return_reachable_inv_tier(state, world, player) >= world.options.sans_req_inv_tier and state.has("ITEM", player) and state.has("Jump", player)))

    world.get_region("room_castle_finalshoehorn").connect(
        connecting_region=world.get_region("room_sanscorridor"))

    world.get_region("room_fire10").connect(
        connecting_region=world.get_region("Fire 10 One Way"))

    world.get_region("room_castle_finalshoehorn").connect(
        connecting_region=world.get_region("room_castle_coffins1"))

    world.get_region("room_castle_finalshoehorn").connect(
        connecting_region=world.get_region("room_castle_throneroom"),
        rule=lambda state, world=world: FromOption(RouteRequired).resolve(world) == RouteRequired.option_genocide or FromOption(RouteRequired).resolve(world) == RouteRequired.option_pacifist or (_undertale_return_reachable_def_equipment(state, world, player) >= world.options.asgore_req_def and _undertale_return_reachable_atk_equipment(state, world, player) >= world.options.asgore_req_atk))

    world.get_region("room_castle_throneroom").connect(
        connecting_region=world.get_region("room_castle_finalshoehorn"))

    world.get_region("room_castle_coffins1").connect(
        connecting_region=world.get_region("room_castle_finalshoehorn"))

    world.get_region("room_castle_coffins1").connect(
        connecting_region=world.get_region("room_castle_coffins2"))

    world.get_region("room_castle_coffins2").connect(
        connecting_region=world.get_region("room_castle_coffins1"))

    world.get_region("Bed Door One-way").connect(
        connecting_region=world.get_region("room_fire_hoteldoors"))

    world.get_region("room_fire_hotellobby").connect(
        connecting_region=world.get_region("room_fire_hotelbed"))

    world.get_region("room_fire_core_bottomleft").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_fire_core_topleft").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_fire_core_topright").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_fire_core_bottomright").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_fire_core_center").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_fire_core_bridge").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_fire5").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_fire6").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_fire_walkandbranch").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_fire_preshootguy4").connect(
        connecting_region=world.get_region("Hotland Grind Rooms"))
    world.get_region("room_water5").connect(
        connecting_region=world.get_region("Waterfall Grind Rooms"))
    world.get_region("room_water6").connect(
        connecting_region=world.get_region("Waterfall Grind Rooms"))
    world.get_region("room_water12").connect(
        connecting_region=world.get_region("Waterfall Grind Rooms"))
    world.get_region("room_water15").connect(
        connecting_region=world.get_region("Waterfall Grind Rooms"))
    world.get_region("room_water16").connect(
        connecting_region=world.get_region("Waterfall Grind Rooms"))
    world.get_region("room_water17").connect(
        connecting_region=world.get_region("Waterfall Grind Rooms"))
    world.get_region("room_tundra3").connect(
        connecting_region=world.get_region("Snowdin Grind Rooms"))
    world.get_region("room_tundra4").connect(
        connecting_region=world.get_region("Snowdin Grind Rooms"))
    world.get_region("room_tundra6").connect(
        connecting_region=world.get_region("Snowdin Grind Rooms"))
    world.get_region("room_tundra_snowpuzz").connect(
        connecting_region=world.get_region("Snowdin Grind Rooms"))
    world.get_region("room_tundra_dangerbridge").connect(
        connecting_region=world.get_region("Snowdin Grind Rooms"))
    world.get_region("room_ruins7").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins9").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins8").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins15A").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins10").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins11").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins15B").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins15C").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins15D").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins14").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))
    world.get_region("room_ruins13").connect(
        connecting_region=world.get_region("Ruins Grind Rooms"))

    world.get_region("room_fogroom").connect(
        connecting_region=world.get_region("Snowdin Exit"))

    world.get_region("Snowdin Exit").connect(
        connecting_region=world.get_region("room_fogroom"))

    world.get_region("room_fire2").connect(
        connecting_region=world.get_region("Waterfall Exit"))

    world.get_region("Waterfall Exit").connect(
        connecting_region=world.get_region("room_fire2"))

    world.get_region("room_ruinsexit").connect(
        connecting_region=world.get_region("Ruins Exit"))

    world.get_region("Ruins Exit").connect(
        connecting_region=world.get_region("room_ruinsexit"))

    world.get_region("room_fire7").connect(
        connecting_region=world.get_region("Fire Door 1"),
        name="Fire Door 1 Block",
        rule=CanReachRegion("room_fire_shootguy_2") & CanReachRegion("room_fire_shootguy_1"))

    world.get_region("room_fire_walkandbranch2").connect(
        connecting_region=world.get_region("Fire Door 2"),
        name="Fire Door 2 Block",
        rule=CanReachRegion("room_fire_shootguy_3") & CanReachRegion("room_fire_shootguy_4"))


def set_er_location_rules(world: "UndertaleWorld") -> None:
    player = world.player
    multiworld = world.multiworld
    world.set_rule(multiworld.get_entrance("room_fire_elevator_l1 -> room_fire_prelab", player),
                     ((CanReachRegion("room_fire_savepoint1", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                     CanReachRegion("room_fire_spider", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_genocide], operator="in")]))))
    world.set_rule(multiworld.get_entrance("room_fire_prelab -> room_fire_elevator_l1", player),
                     ((CanReachRegion("room_fire_savepoint1", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                     CanReachRegion("room_fire_spider", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_genocide], operator="in")]))))
    
    world.set_rule(multiworld.get_entrance("room_fire_core_bridge -> room_fire_core_right", player),
                     ((CanReachRegion("room_fire_shootguy_5", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                                                    CanReachRegion("room_fire_core_warrior", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
                     )))
    
    world.set_rule(multiworld.get_entrance("room_basement4 -> room_basement5", player),
                     (CanReachLocation("Toriel Fight")))
    world.set_rule(multiworld.get_entrance("room_fire_core_right -> room_fire_core_bridge", player),
                     ((CanReachRegion("room_fire_shootguy_5", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                                                    CanReachRegion("room_fire_core_warrior", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
                     )))
    world.set_rule(multiworld.get_entrance("room_fire_core_premett -> room_fire_core1", player),
                     ((CanReachRegion("room_fire_shootguy_5", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                                                    CanReachRegion("room_fire_core_warrior", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
                     )))
    world.set_rule(multiworld.get_entrance("room_fire_core1 -> room_fire_core_premett", player),
                     ((CanReachRegion("room_fire_shootguy_5", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                                                    CanReachRegion("room_fire_core_warrior", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
                     )))
    world.set_rule(multiworld.get_entrance("room_torhouse1 -> room_basement1", player),
                     CanReachRegion("room_torhouse2") & CanReachRegion("room_torhouse3"))
    for door in world.all_door_locks:
        if door == "room_fire_prelab <-> room_fire_elevator_l1":
            world.set_rule(multiworld.get_location("Approach Door "+door, player),
                    CanReachRegion(door.split(" <-> ")[1]) | (CanReachRegion(door.split(" <-> ")[0]) & 
                    (CanReachRegion("room_fire_savepoint1", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                     CanReachRegion("room_fire_spider", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_genocide], operator="in")]))))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[0] + " -> " + door.split(" <-> ")[1], player),
                     Has("Door Unlock - "+door) & ((CanReachRegion("room_fire_savepoint1", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                     CanReachRegion("room_fire_spider", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_genocide], operator="in")]))))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[1] + " -> " + door.split(" <-> ")[0], player),
                     Has("Door Unlock - "+door) & ((CanReachRegion("room_fire_savepoint1", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                     CanReachRegion("room_fire_spider", filtered_resolution=False, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_genocide], operator="in")]))))
        elif door == "room_fire_core_right <-> room_fire_core_bridge":
            world.set_rule(multiworld.get_location("Approach Door "+door, player),
                    CanReachRegion(door.split(" <-> ")[1]) | (CanReachRegion(door.split(" <-> ")[0]) & 
                    (CanReachRegion("room_fire_shootguy_5", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                     CanReachRegion("room_fire_core_warrior", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
                     )))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[0] + " -> " + door.split(" <-> ")[1], player),
                     Has("Door Unlock - "+door) & ((CanReachRegion("room_fire_shootguy_5", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                                                    CanReachRegion("room_fire_core_warrior", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
                     )))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[1] + " -> " + door.split(" <-> ")[0], player),
                     Has("Door Unlock - "+door) & ((CanReachRegion("room_fire_shootguy_5", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                                                    CanReachRegion("room_fire_core_warrior", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
                     )))
        elif door == "room_fire_core1 <-> room_fire_core_premett":
            world.set_rule(multiworld.get_location("Approach Door "+door, player),
                    CanReachRegion(door.split(" <-> ")[1]) | CanReachRegion(door.split(" <-> ")[0]))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[0] + " -> " + door.split(" <-> ")[1], player),
                     Has("Door Unlock - "+door) & ((CanReachRegion("room_fire_shootguy_5", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                                                    CanReachRegion("room_fire_core_warrior", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
                     )))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[1] + " -> " + door.split(" <-> ")[0], player),
                     Has("Door Unlock - "+door) & ((CanReachRegion("room_fire_shootguy_5", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")]) | 
                                                    CanReachRegion("room_fire_core_warrior", filtered_resolution=True, options=[OptionFilter(RouteRequired, [RouteRequired.option_all_routes, RouteRequired.option_pacifist, RouteRequired.option_neutral], operator="in")])
                     )))
        elif door == "room_torhouse1 <-> room_basement1":
            world.set_rule(multiworld.get_location("Approach Door "+door, player),
                    CanReachRegion(door.split(" <-> ")[1]) | CanReachRegion(door.split(" <-> ")[0]))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[0] + " -> " + door.split(" <-> ")[1], player),
                     Has("Door Unlock - "+door) & CanReachRegion("room_torhouse2") & CanReachRegion("room_torhouse3"))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[1] + " -> " + door.split(" <-> ")[0], player),
                     Has("Door Unlock - "+door) & CanReachRegion("room_torhouse2") & CanReachRegion("room_torhouse3"))
        elif door == "room_basement4 <-> room_basement5":
            world.set_rule(multiworld.get_location("Approach Door "+door, player),
                     CanReachRegion(door.split(" <-> ")[1]) | (CanReachLocation("Toriel Fight") & CanReachRegion(door.split(" <-> ")[0])))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[0] + " -> " + door.split(" <-> ")[1], player),
                     CanReachLocation("Toriel Fight") & Has("Door Unlock - "+door))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[1] + " -> " + door.split(" <-> ")[0], player),
                     CanReachLocation("Toriel Fight") & Has("Door Unlock - "+door))
        else:
            world.set_rule(multiworld.get_location("Approach Door "+door, player),
                    CanReachRegion(door.split(" <-> ")[0]) | CanReachRegion(door.split(" <-> ")[1]))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[0] + " -> " + door.split(" <-> ")[1], player),
                     Has("Door Unlock - "+door))
            world.set_rule(multiworld.get_entrance(door.split(" <-> ")[1] + " -> " + door.split(" <-> ")[0], player),
                     Has("Door Unlock - "+door))
    
    if world.options.spare_sanity == 2 and (_undertale_is_route(world, 0) or _undertale_is_route(world, 1)):
        for i in range(world.options.spare_sanity_max.value):
            world.set_rule(multiworld.get_location("Ruins Spare " + str(i + 1), player),
                     Has("Ruins Spare", math.ceil((i + 1) / FromOption(SpareSanityPackSize).resolve(world))) & (CanReachRegion("Ruins Grind Rooms")))
            world.set_rule(multiworld.get_location("Snowdin Spare " + str(i + 1), player),
                     Has("Snowdin Spare", math.ceil((i + 1) / FromOption(SpareSanityPackSize).resolve(world))) & (CanReachRegion("Snowdin Grind Rooms")))
            world.set_rule(multiworld.get_location("Waterfall Spare " + str(i + 1), player),
                     Has("Waterfall Spare", math.ceil((i + 1) / FromOption(SpareSanityPackSize).resolve(world))) & (CanReachRegion("Waterfall Grind Rooms")))
            world.set_rule(multiworld.get_location("Hotland Spare " + str(i + 1), player),
                     Has("Hotland Spare", math.ceil((i + 1) / FromOption(SpareSanityPackSize).resolve(world))) & (CanReachRegion("Hotland Grind Rooms")))
    elif world.options.spare_sanity == 1:
        for i in range(world.options.spare_sanity_max.value):
            world.set_rule(multiworld.get_location("Ruins Spare " + str(i + 1), player),
                     (CanReachRegion("Ruins Grind Rooms")))
            world.set_rule(multiworld.get_location("Snowdin Spare " + str(i + 1), player),
                     (CanReachRegion("Snowdin Grind Rooms")))
            world.set_rule(multiworld.get_location("Waterfall Spare " + str(i + 1), player),
                     (CanReachRegion("Waterfall Grind Rooms")))
            world.set_rule(multiworld.get_location("Hotland Spare " + str(i + 1), player),
                     (CanReachRegion("Hotland Grind Rooms")))
    if _undertale_is_route(world, 1):
        world.set_rule(multiworld.get_location("Popato Chisps Machine", player),
                (CanReachLocation("Alphys Date") & Has(
                "DT Extractor")))
        world.set_rule(multiworld.get_location("Papyrus Hangout", player),
                 Has("Complete Skeleton") & CanReachLocation("Papyrus Fight"))
        world.set_rule(multiworld.get_location("Undyne Cook-off", player),
                 CanReachLocation("Papyrus Hangout") & Has("Fish") & CanReachLocation("Undyne Fight"))
        world.set_rule(multiworld.get_location("Alphys Date", player),
                 CanReachRegion("room_water_trashzone1") & CanReachRegion(
                     "room_fire_core_final") & Has("Undyne Letter EX") & CanReachLocation(
                     "Undyne Cook-off"))
        world.set_rule(multiworld.get_location("Right Spider Bake Sale", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Left Spider Bake Sale", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Sans Hot Dog Sale 1", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Sans Hot Cat Sale", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Sans Hot Dog Sale 2", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Sans Hot Dog Sale 3", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Sans Hot Dog Sale 4", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Hotel Door Hush Puppy", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Undyne Letter", player),
                 CanReachRegion("room_fire_core_final") & CanReachLocation("Undyne Cook-off"))
    if (not _undertale_is_route(world, 2)) or _undertale_is_route(world, 3):
        world.set_rule(multiworld.get_location("Free Nicecream", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Nicecream Snowdin", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Nicecream Waterfall", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
        world.set_rule(multiworld.get_location("Punch Card", player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
    if _undertale_is_route(world, 2) and (not _undertale_is_route(world, 3)) and (world.options.kill_sanity.value == 2):
        world.set_rule(multiworld.get_location("Toriel Fight", player),
                 Has("Ruins Population Pack", math.ceil(20 / FromOption(KillSanityPackSize).resolve(world))))
        world.set_rule(multiworld.get_location("Papyrus Fight", player),
                 Has("Snowdin Population Pack", math.ceil(16 / FromOption(KillSanityPackSize).resolve(world))))
        world.set_rule(multiworld.get_location("Undyne Fight", player),
                 lambda state, world=world, player=player: (world.options.route_required.value == RouteRequired.option_neutral or world.options.route_required.value == RouteRequired.option_pacifist or (_undertale_return_reachable_def(state, world, player, _undertale_return_reachable_level(_undertale_exp_available(state, world, player))) >= world.options.undying_req_def and _undertale_return_reachable_atk(state, world, player, _undertale_return_reachable_level(_undertale_exp_available(state, world, player))) >= world.options.undying_req_atk and _undertale_return_reachable_hp(state, world, player, _undertale_return_reachable_level(_undertale_exp_available(state, world, player))) >= world.options.undying_req_hp)) and state.has("ITEM", player) and state.has("Waterfall Population Pack", player, math.ceil(18 / world.options.kill_sanity_pack_size.value)))
    if _undertale_is_route(world, 2) and (not _undertale_is_route(world, 3)) and (world.options.kill_sanity.value != 2):
        world.set_rule(multiworld.get_location("Undyne Fight", player),
                 lambda state, world=world, player=player: (world.options.route_required.value == RouteRequired.option_neutral or world.options.route_required.value == RouteRequired.option_pacifist or (_undertale_return_reachable_def(state, world, player, _undertale_return_reachable_level(_undertale_exp_available(state, world, player))) >= world.options.undying_req_def and _undertale_return_reachable_atk(state, world, player, _undertale_return_reachable_level(_undertale_exp_available(state, world, player))) >= world.options.undying_req_atk and _undertale_return_reachable_hp(state, world, player, _undertale_return_reachable_level(_undertale_exp_available(state, world, player))) >= world.options.undying_req_hp)) and state.has("ITEM", player))
    if _undertale_is_route(world, 2) and (world.options.kill_sanity.value != 0):
        for i in range(0, 16):
            world.set_rule(multiworld.get_location("Ruins Kill " + str(i + 1), player),
                     Has("Ruins Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Ruins Grind Rooms"))
            world.set_rule(multiworld.get_location("Snowdin Kill " + str(i + 1), player),
                     Has("Snowdin Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Snowdin Grind Rooms"))
            world.set_rule(multiworld.get_location("Waterfall Kill " + str(i + 1), player),
                     Has("Waterfall Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Waterfall Grind Rooms"))
            world.set_rule(multiworld.get_location("Hotland Kill " + str(i + 1), player),
                     Has("Hotland Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Hotland Grind Rooms"))
        for i in range(16, 18):
            world.set_rule(multiworld.get_location("Ruins Kill " + str(i + 1), player),
                     Has("Ruins Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Ruins Grind Rooms"))
            world.set_rule(multiworld.get_location("Waterfall Kill " + str(i + 1), player),
                     Has("Waterfall Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Waterfall Grind Rooms"))
            world.set_rule(multiworld.get_location("Hotland Kill " + str(i + 1), player),
                     Has("Hotland Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Hotland Grind Rooms"))
        for i in range(18, 20):
            world.set_rule(multiworld.get_location("Ruins Kill " + str(i + 1), player),
                     Has("Ruins Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Ruins Grind Rooms"))
            world.set_rule(multiworld.get_location("Hotland Kill " + str(i + 1), player),
                     Has("Hotland Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Hotland Grind Rooms"))
        for i in range(20, 40):
            world.set_rule(multiworld.get_location("Hotland Kill " + str(i + 1), player),
                     Has("Hotland Population Pack", math.ceil((i + 1) / FromOption(KillSanityPackSize).resolve(world))) & CanReachRegion("Hotland Grind Rooms"))
    if _undertale_is_route(world, 2) and \
            (bool(world.options.rando_love.value) or bool(world.options.rando_stats.value)):
        maxlv = 1
        while maxlv < 20:
            maxlv += 1
            if world.options.rando_stats:
                world.set_rule(multiworld.get_location(("ATK " + str(maxlv)), player),
                         lambda state, maxlv=maxlv:
                         _undertale_return_reachable_level(_undertale_exp_available(state, world, player)) >= maxlv)
                world.set_rule(multiworld.get_location(("HP " + str(maxlv)), player),
                         lambda state, maxlv=maxlv:
                         _undertale_return_reachable_level(_undertale_exp_available(state, world, player)) >= maxlv)
                if maxlv == 5 or maxlv == 9 or maxlv == 13 or maxlv == 17 or maxlv == 20:
                    world.set_rule(multiworld.get_location(("DEF " + str(maxlv)), player),
                             lambda state, maxlv=maxlv:
                             _undertale_return_reachable_level(_undertale_exp_available(state, world, player)) >= maxlv)
            if world.options.rando_love:
                world.set_rule(multiworld.get_location(("LOVE " + str(maxlv)), player),
                         lambda state, maxlv=maxlv:
                         _undertale_return_reachable_level(_undertale_exp_available(state, world, player)) >= maxlv)
    world.set_rule(multiworld.get_location("Mettaton Fight", player),
             CanReachRegion("room_fire_core_metttest") & Has("Hotland Population Pack", math.ceil(40 / FromOption(KillSanityPackSize).resolve(world)), filtered_resolution=True, options=[OptionFilter(KillSanity, KillSanity.option_locked), OptionFilter(RouteRequired, RouteRequired.option_genocide)]))
    world.set_rule(multiworld.get_location("Snowdin Shop 1", player),
             OptionFilter(RouteRequired, [RouteRequired.option_genocide, RouteRequired.option_all_routes], operator="in") | (((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access"))))
    world.set_rule(multiworld.get_location("Snowdin Shop 2", player),
             OptionFilter(RouteRequired, [RouteRequired.option_genocide, RouteRequired.option_all_routes], operator="in") | (((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access"))))
    world.set_rule(multiworld.get_location("Snowdin Shop 3", player),
             OptionFilter(RouteRequired, [RouteRequired.option_genocide, RouteRequired.option_all_routes], operator="in") | (((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access"))))
    world.set_rule(multiworld.get_location("Snowdin Shop 4", player),
             OptionFilter(RouteRequired, [RouteRequired.option_genocide, RouteRequired.option_all_routes], operator="in") | (((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access"))))
    world.set_rule(multiworld.get_location("Gerson Shop 1", player),
             ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
    world.set_rule(multiworld.get_location("Gerson Shop 2", player),
             ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
    world.set_rule(multiworld.get_location("Gerson Shop 3", player),
             ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
    world.set_rule(multiworld.get_location("Gerson Shop 4", player),
             ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
    world.set_rule(multiworld.get_location("Temmie Shop 1", player),
             CanReachRegion("room_water_piano") | Has("Out of Logic Access"))
    world.set_rule(multiworld.get_location("Temmie Shop 2", player),
             CanReachRegion("room_water_piano") | Has("Out of Logic Access"))
    world.set_rule(multiworld.get_location("Temmie Shop 3", player),
             CanReachRegion("room_water_piano") | Has("Out of Logic Access"))
    world.set_rule(multiworld.get_location("Temmie Shop 4", player),
             (CanReachRegion("room_water_piano") & Has("1000G", 2)) | Has("Out of Logic Access"))
    world.set_rule(multiworld.get_location("Bratty Catty Shop 1", player),
             OptionFilter(RouteRequired, [RouteRequired.option_genocide, RouteRequired.option_all_routes], operator="in") | (((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access"))))
    world.set_rule(multiworld.get_location("Bratty Catty Shop 2", player),
             OptionFilter(RouteRequired, [RouteRequired.option_genocide, RouteRequired.option_all_routes], operator="in") | (((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access"))))
    world.set_rule(multiworld.get_location("Bratty Catty Shop 3", player),
             OptionFilter(RouteRequired, [RouteRequired.option_genocide, RouteRequired.option_all_routes], operator="in") | (((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access"))))
    world.set_rule(multiworld.get_location("Bratty Catty Shop 4", player),
             OptionFilter(RouteRequired, [RouteRequired.option_genocide, RouteRequired.option_all_routes], operator="in") | (((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access"))))
    world.set_rule(multiworld.get_location("Burgerpants Shop 1", player),
             ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
    world.set_rule(multiworld.get_location("Burgerpants Shop 2", player),
             ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
    world.set_rule(multiworld.get_location("Burgerpants Shop 3", player),
             ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
    world.set_rule(multiworld.get_location("Burgerpants Shop 4", player),
             ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")))
    counter = 1
    all_locs = world.get_locations()
    loc_names: list[str] = []
    for a_loc in all_locs:
        loc_names.append(a_loc.name)
    while "Hub Shop "+str(counter) in loc_names:
        world.set_rule(multiworld.get_location("Hub Shop "+str(counter), player),
                 ((CanReachRegion("room_water_piano") & CanReachRegion("room_shop5")) | Has("Out of Logic Access")) | OptionFilter(HubShopCost, 0, "eq"))
        counter += 1