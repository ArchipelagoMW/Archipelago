from BaseClasses import CollectionState
from typing import TYPE_CHECKING
from .Options import KeyPieces, RouteRequired, KeyHunt, KillSanityPackSize
from rule_builder.options import OptionFilter
from rule_builder.field_resolvers import FromOption
from rule_builder.rules import Has, Rule
import dataclasses

if TYPE_CHECKING:
    from . import UndertaleWorld


def _undertale_is_route(world: "UndertaleWorld", route: int):
    if route == 3:
        return FromOption(RouteRequired).resolve(world) == RouteRequired.option_all_routes
    if FromOption(RouteRequired).resolve(world) == RouteRequired.option_all_routes:
        return True
    if route == 0:
        return FromOption(RouteRequired).resolve(world) == RouteRequired.option_neutral
    if route == 1:
        return FromOption(RouteRequired).resolve(world) == RouteRequired.option_pacifist
    if route == 2:
        return FromOption(RouteRequired).resolve(world) == RouteRequired.option_genocide
    return False

@dataclasses.dataclass()
class _undertale_has_keys(Rule["UndertaleWorld"], game="Undertale"):
    def _instantiate(self, world: "UndertaleWorld") -> Rule.Resolved:
        return ((Has("Left Home Key", options=[OptionFilter(KeyHunt, KeyHunt.option_false)]) & Has("Right Home Key", options=[OptionFilter(KeyHunt, KeyHunt.option_false)])) |
            Has("Key Piece", FromOption(KeyPieces), options=[OptionFilter(KeyHunt, KeyHunt.option_true)])).resolve(world)


def _undertale_exp_available(state: CollectionState, world: "UndertaleWorld", player: int):
    exp = 0
    pack_size = FromOption(KillSanityPackSize).resolve(world)
    if state.can_reach("Ruins Grind Rooms", "Region", player):
        exp += (min(20, state.count("Ruins Population Pack", player) * pack_size) * 2)
        if state.can_reach("room_basement4", "Region", player) and state.count("Ruins Population Pack", player) * \
                pack_size >= 20:
            exp += 150
    if state.can_reach("Snowdin Grind Rooms", "Region", player):
        exp += (min(15, state.count("Snowdin Population Pack", player) * pack_size) * 1)
        if state.count("Snowdin Population Pack", player) * pack_size >= 16:
            exp += 22
        if state.can_reach("room_fogroom", "Region", player) and state.count("Snowdin Population Pack", player) * \
                pack_size >= 16:
            exp += 200
    if state.can_reach("room_tundra5", "Region", player):
        exp += 30
    if state.can_reach("room_tundra_snowpuzz", "Region", player):
        exp += 60
    if state.can_reach("room_tundra_poffzone", "Region", player):
        exp += 80
    if state.can_reach("Waterfall Grind Rooms", "Region", player):
        exp += (min(18, state.count("Waterfall Population Pack", player) * pack_size) * 3)
    if state.can_reach("room_water14", "Region", player):
        exp += 52
    if state.can_reach("room_fire_turn", "Region", player):
        exp += 220
    if state.can_reach("room_fire_spider", "Region", player):
        exp += 300
    if state.can_reach("Hotland Grind Rooms", "Region", player):
        exp += (min(40, state.count("Hotland Population Pack", player) * pack_size) * 70)
    if state.can_reach("Waterfall Grind Rooms", "Region", player):
        if state.can_reach("room_water20", "Region", player) and (_undertale_return_reachable_def(state, world, player, _undertale_return_reachable_level(exp)) >= world.options.undying_req_def and _undertale_return_reachable_atk(state, world, player, _undertale_return_reachable_level(exp)) >= world.options.undying_req_atk and _undertale_return_reachable_hp(state, world, player, _undertale_return_reachable_level(exp)) >= world.options.undying_req_hp) and state.has("ITEM", player) and state.count("Waterfall Population Pack", player) * \
                pack_size >= 18:
            exp += 1500
    if state.can_reach("Hotland Grind Rooms", "Region", player):
        if state.can_reach("room_fire_core_metttest", "Region", player) and \
                state.count("Hotland Population Pack", player) * pack_size >= 40:
            exp = 50000
    if state.can_reach("room_castle_finalshoehorn", "Region", player):
        exp = 99999
    return exp


def _undertale_has_weapon(state: CollectionState, world: "UndertaleWorld", player: int, weapon_name: str):
    if world.options.prog_weapons.value == 1:
        need_count = 0
        if weapon_name == "Toy Knife":
            need_count = 1
        elif weapon_name == "Tough Glove":
            need_count = 2
        elif weapon_name == "Ballet Shoes":
            need_count = 3
        elif weapon_name == "Torn Notebook":
            need_count = 4
        elif weapon_name == "Empty Gun":
            need_count = 5
        elif weapon_name == "Burnt Pan":
            need_count = 6
        elif weapon_name == "Worn Dagger" or weapon_name == "Real Knife":
            need_count = 7
        return state.has("Progressive Weapons", player, need_count)
    else:
        return state.has(weapon_name, player)


def _undertale_has_armor(state: CollectionState, world: "UndertaleWorld", player: int, armor_name: str):
    if world.options.prog_armor.value == 1:
        need_count = 0
        if armor_name == "Faded Ribbon":
            need_count = 1
        elif armor_name == "Manly Bandanna":
            need_count = 2
        elif armor_name == "Old Tutu":
            need_count = 3
        elif armor_name == "Cloudy Glasses":
            need_count = 4
        elif armor_name == "Cowboy Hat":
            need_count = 5
        elif armor_name == "Stained Apron" or (world.options.route_required.value == RouteRequired.option_genocide and armor_name == "The Locket"):
            need_count = 6
        elif armor_name == "Heart Locket" or (world.options.route_required.value == RouteRequired.option_genocide and armor_name == "temy armor"):
            need_count = 7
        elif armor_name == "temy armor" and world.options.route_required.value != RouteRequired.option_genocide:
            need_count = 8
        return state.has("Progressive Armor", player, need_count)
    else:
        return state.has(armor_name, player)


def _undertale_return_reachable_hp(state: CollectionState, world: "UndertaleWorld", player: int, love_current: int):
    met_hp = 20
    if world.options.rando_stats.value == 1:
        met_hp += state.count("HP Up", player) * 4
    elif world.options.rando_love.value == 1:
        met_hp += state.count("LOVE", player) * 4
    else:
        met_hp += (love_current - 1) * 4
    if met_hp > 92:
        met_hp = 99
    return met_hp


def _undertale_return_reachable_inv_tier(state: CollectionState, world: "UndertaleWorld", player: int):
    met_inv = 30
    if _undertale_has_armor(state, world, player, "Cloudy Glasses"):
        met_inv += 30
    elif _undertale_has_armor(state, world, player, "temy armor"):
        met_inv += 15

    if _undertale_has_weapon(state, world, player, "Torn Notebook"):
        met_inv += 15

    met_tier = 0
    if met_inv >= 75:
        met_tier = 3
    elif met_inv >= 60:
        met_tier = 2
    elif met_inv >= 45:
        met_tier = 1
    return met_tier


def _undertale_return_reachable_atk_equipment(state: CollectionState, world: "UndertaleWorld", player: int):
    met_atk = 0
        
    if _undertale_has_armor(state, world, player, "temy armor"):
        met_atk += 10
    elif _undertale_has_armor(state, world, player, "Cowboy Hat"):
        met_atk += 5

    if _undertale_has_weapon(state, world, player, "Real Knife"):
        met_atk += 99
    elif _undertale_has_weapon(state, world, player, "Worn Dagger"):
        met_atk += 15
    elif _undertale_has_weapon(state, world, player, "Empty Gun"):
        met_atk += 12
    elif _undertale_has_weapon(state, world, player, "Burnt Pan"):
        met_atk += 10
    elif _undertale_has_weapon(state, world, player, "Ballet Shoes"):
        met_atk += 7
    elif _undertale_has_weapon(state, world, player, "Tough Glove"):
        met_atk += 5
    elif _undertale_has_weapon(state, world, player, "Toy Knife"):
        met_atk += 3
    elif _undertale_has_weapon(state, world, player, "Torn Notebook"):
        met_atk += 2
    return met_atk


def _undertale_return_reachable_atk(state: CollectionState, world: "UndertaleWorld", player: int, love_current: int):
    met_atk = 10
    if world.options.rando_stats.value == 1:
        met_atk += state.count("ATK Up", player) * 2
    elif world.options.rando_love.value == 1:
        met_atk += state.count("LOVE", player) * 2
    else:
        met_atk += (love_current - 1) * 2
    if met_atk > 46:
        met_atk = 99
        
    if _undertale_has_armor(state, world, player, "temy armor"):
        met_atk += 10
    elif _undertale_has_armor(state, world, player, "Cowboy Hat"):
        met_atk += 5

    if _undertale_has_weapon(state, world, player, "Real Knife"):
        met_atk += 99
    elif _undertale_has_weapon(state, world, player, "Worn Dagger"):
        met_atk += 15
    elif _undertale_has_weapon(state, world, player, "Empty Gun"):
        met_atk += 12
    elif _undertale_has_weapon(state, world, player, "Burnt Pan"):
        met_atk += 10
    elif _undertale_has_weapon(state, world, player, "Ballet Shoes"):
        met_atk += 7
    elif _undertale_has_weapon(state, world, player, "Tough Glove"):
        met_atk += 5
    elif _undertale_has_weapon(state, world, player, "Toy Knife"):
        met_atk += 3
    elif _undertale_has_weapon(state, world, player, "Torn Notebook"):
        met_atk += 2
    return met_atk


def _undertale_return_reachable_def_equipment(state: CollectionState, world: "UndertaleWorld", player: int):
    met_def = 0

    if _undertale_has_armor(state, world, player, "The Locket"):
        met_def += 99
    elif _undertale_has_armor(state, world, player, "temy armor"):
        met_def += 20
    elif _undertale_has_armor(state, world, player, "Heart Locket"):
        met_def += 15
    elif _undertale_has_armor(state, world, player, "Cowboy Hat"):
        met_def += 12
    elif _undertale_has_armor(state, world, player, "Stained Apron"):
        met_def += 11
    elif _undertale_has_armor(state, world, player, "Old Tutu"):
        met_def += 10
    elif _undertale_has_armor(state, world, player, "Manly Bandanna"):
        met_def += 7
    elif _undertale_has_armor(state, world, player, "Cloudy Glasses"):
        met_def += 5
    elif _undertale_has_armor(state, world, player, "Faded Ribbon"):
        met_def += 3
    return met_def


def _undertale_return_reachable_def(state: CollectionState, world: "UndertaleWorld", player: int, love_current: int):
    met_def = 10
    if world.options.rando_stats.value == 1:
        met_def += state.count("DEF Up", player)
        if met_def > 14:
            met_def = 99
    else:
        met_lv = 1
        if world.options.rando_love.value == 1:
            met_lv = state.count("LOVE", player)
        else:
            met_lv = love_current
        if met_lv >= 5:
            met_def += 1
        if met_lv >= 9:
            met_def += 1
        if met_lv >= 13:
            met_def += 1
        if met_lv >= 17:
            met_def += 1
        if met_lv >= 20:
            met_def = 99

    if _undertale_has_armor(state, world, player, "The Locket"):
        met_def += 99
    elif _undertale_has_armor(state, world, player, "temy armor"):
        met_def += 20
    elif _undertale_has_armor(state, world, player, "Heart Locket"):
        met_def += 15
    elif _undertale_has_armor(state, world, player, "Cowboy Hat"):
        met_def += 12
    elif _undertale_has_armor(state, world, player, "Stained Apron"):
        met_def += 11
    elif _undertale_has_armor(state, world, player, "Old Tutu"):
        met_def += 10
    elif _undertale_has_armor(state, world, player, "Manly Bandanna"):
        met_def += 7
    elif _undertale_has_armor(state, world, player, "Cloudy Glasses"):
        met_def += 5
    elif _undertale_has_armor(state, world, player, "Faded Ribbon"):
        met_def += 3
    return met_def


def _undertale_return_reachable_level(exp: int):
    lvl = 1
    if exp >= 10 and lvl == 1:
        lvl += 1
    if exp >= 30 and lvl == 2:
        lvl += 1
    if exp >= 70 and lvl == 3:
        lvl += 1
    if exp >= 120 and lvl == 4:
        lvl += 1
    if exp >= 200 and lvl == 5:
        lvl += 1
    if exp >= 300 and lvl == 6:
        lvl += 1
    if exp >= 500 and lvl == 7:
        lvl += 1
    if exp >= 800 and lvl == 8:
        lvl += 1
    if exp >= 1200 and lvl == 9:
        lvl += 1
    if exp >= 1700 and lvl == 10:
        lvl += 1
    if exp >= 2500 and lvl == 11:
        lvl += 1
    if exp >= 3500 and lvl == 12:
        lvl += 1
    if exp >= 5000 and lvl == 13:
        lvl += 1
    if exp >= 7000 and lvl == 14:
        lvl += 1
    if exp >= 10000 and lvl == 15:
        lvl += 1
    if exp >= 15000 and lvl == 16:
        lvl += 1
    if exp >= 25000 and lvl == 17:
        lvl += 1
    if exp >= 50000 and lvl == 18:
        lvl += 1
    if exp >= 99999 and lvl == 19:
        lvl += 1
    return lvl
