from BaseClasses import Item
from .Names import ItemName

class VoidSolsItem(Item):
    game: str = "Void Sols"

weapon_table = {
    ItemName.sword: 1,
    ItemName.dagger: 2,
    ItemName.great_hammer: 3,
    ItemName.pickaxe: 4,
    ItemName.halberd: 5,
    ItemName.katana: 6,
    ItemName.gauntlets: 7,
    ItemName.morningstar: 8,
    ItemName.dual_handaxes: 9,
    ItemName.scythe: 10,
    ItemName.frying_pan: 11,
}

secondary_table = {
    ItemName.parrying_shield: 100,
    ItemName.throwing_dagger: 101,
    ItemName.great_bow: 102,
    ItemName.fishing_rod: 103,
    ItemName.hunters_bow: 104,
    ItemName.fire_talisman: 105,
    ItemName.blizzard_talisman: 106,
    ItemName.lightning_talisman: 107,
    ItemName.crossbow: 108,
    ItemName.heavy_shield: 109,
}

artifact_table = {
    ItemName.steel_feather: 200,
    ItemName.obsidian_arrowhead: 201,
    ItemName.ruby_phial: 202,
    ItemName.bismuth_claw: 203,
    ItemName.iron_pineapple: 204,
    ItemName.jasper_chalice: 205,
    ItemName.golden_clover: 206,
    ItemName.emerald_phial: 207,
    ItemName.topaz_phial: 208,
    ItemName.silver_pouch: 209,
    ItemName.brass_knuckles: 210,
    ItemName.garnet_aegis: 211,
    ItemName.brass_knuckles_plus: 212,
}

relic_table = {
    ItemName.relic_of_agility: 300,
    ItemName.relic_of_power: 301,
    ItemName.relic_of_the_colossus: 302,
    ItemName.relic_of_balance: 303,
    ItemName.relic_of_finesse: 304,
    ItemName.relic_of_redirection: 305,
    ItemName.relic_of_invigoration: 306,
    ItemName.relic_of_dousing: 307,
    ItemName.relic_of_agility_plus: 308,
    ItemName.relic_of_power_plus: 309,
    ItemName.relic_of_the_colossus_plus: 310,
    ItemName.relic_of_balance_plus: 311,
    ItemName.relic_of_finesse_plus: 312,
    ItemName.relic_of_mycology: 313,
}

flask_ingredients_table = {
    ItemName.essence_of_a_hero: 400,
    ItemName.courage_of_a_hero: 401,
    ItemName.guile_of_a_traveler: 402,
    ItemName.hubris_of_a_hero: 403,
    ItemName.guile_of_a_rogue: 404,
    ItemName.hubris_of_a_rogue: 405,
    ItemName.courage_of_a_traveler: 406,
    ItemName.essence_of_a_rogue: 407,
}

usable_items_table = {
    ItemName.glitterstone_x1: 500,
    ItemName.glitterstone_x2: 501,
    ItemName.snare_trap_x2: 502,
    ItemName.flaming_torch_x1: 503,
    ItemName.flaming_torch_x2: 504,
    ItemName.dynamite_x1: 505,
    ItemName.mysterious_mushroom_x1: 506,
    ItemName.harsh_pepper_x1: 507,
    ItemName.ritual_needle_x2: 508,
    ItemName.verdant_berry_x2: 509,
    ItemName.quiver_of_holding_x1: 510,
    ItemName.chewy_seaweed_x2: 511,
    ItemName.purifying_needle_x2: 512,
    ItemName.bursting_bubble_x1: 513,
    ItemName.caltrops_x2: 514,
    ItemName.stale_bread_x1: 515,
    ItemName.stale_bread_x2: 516,
    ItemName.pocket_barrel_x1: 517,
    ItemName.pet_worm_x3: 517,
}

fish_table = {
    ItemName.upstream_fish: 600,
    ItemName.oceanic_fish: 601,
    ItemName.flying_fish: 602,
    ItemName.glitch_fish: 603,
    ItemName.star_fish: 604,
    ItemName.deep_fish: 605,
    ItemName.frog_fish: 606,
    ItemName.rich_fish: 607,
    ItemName.sick_fish: 608,
}

maps_table = {
    ItemName.prison_map_a: 700,
    ItemName.prison_map_b: 701,
    ItemName.prison_yard_map: 702,
    ItemName.world_map: 703,
    ItemName.forest_map_a: 704,
    ItemName.forest_map_b: 705,
    ItemName.village_map: 706,
    ItemName.deep_mines_map: 707,
    ItemName.mines_map_1: 708,
    ItemName.mines_map_2: 709,
    ItemName.mines_map_3: 710,
    ItemName.mines_map_4: 711,
    ItemName.mountain_map_a: 712,
    ItemName.mountain_map_b: 713,
    ItemName.mountain_underpass_map: 714,
    ItemName.supermax_map_a: 715,
    ItemName.supermax_map_b: 716,
    ItemName.supermax_map_c: 717,
    ItemName.cultist_map_a: 718,
    ItemName.cultist_map_b: 719,
    ItemName.factory_map_a: 720,
    ItemName.factory_map_b: 721,
    ItemName.swamp_map: 722,
    ItemName.apex_outskirts_map: 723,
    ItemName.apex_town_map: 724,
    ItemName.apex_hub_map: 725,
    ItemName.hidden_room_map: 726,
}

keys_table = {
    ItemName.prison_key: 800,
    ItemName.gate_key: 801,
    ItemName.forest_bridge_key: 802,
    ItemName.riverside_shack_key: 803,
    ItemName.condemned_shack_key: 804,
    ItemName.alchemist_cage_key: 805,
    ItemName.mine_entrance_lift_key: 806,
    ItemName.mountain_outpost_key: 807,
    ItemName.minecart_wheel: 808,
    ItemName.lift_key: 809,
    ItemName.pit_catwalk_key: 810,
    ItemName.temple_of_the_deep_key: 811,
    ItemName.sol_forge_lab_key: 812,
    ItemName.false_book: 813,
    ItemName.central_cell_key: 814,
    ItemName.minor_cell_key: 815,
    ItemName.apex_outskirts_key: 816,
    ItemName.infernal_key: 817,
    ItemName.east_wing_key: 818,
    ItemName.kings_emblem_right_half: 819,
    ItemName.kings_emblem_left_half: 820,
    ItemName.restricted_access_key: 821,
    ItemName.data_disc_r: 822,
    ItemName.data_disc_g: 823,
    ItemName.data_disc_b: 824,
    ItemName.master_bedroom_key: 825,
    ItemName.apex_east_wing_key: 826,
}

misc_table = {
    ItemName.potion_mixing_unlocked: 900,
    ItemName.metamorphic_alloy: 901,
    ItemName.sol_alembic: 902,
    ItemName.potions_increased: 903,
    ItemName.minor_sol_shard: 904,
    ItemName.major_sol_shard: 905,
    ItemName.strange_totem: 906,
    ItemName.relics_improved: 907,
    ItemName.fish_tokens_x2: 908,
    ItemName.strange_curio: 909,
}

