"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Manage locations in the Aquaria game multiworld randomizer
"""

from BaseClasses import Location

class AquariaLocation(Location):
    """
    A location in the game.
    """
    game: str = "Aquaria"
    """The name of the game"""

    def __init__(self, player: int, name="", code=None, parent=None) -> None:
        """
        Initialisation of the object
        :param player: the ID of the player
        :param name: the name of the location
        :param code: the ID (or address) of the location (Event if None)
        :param parent: the Region that this location belongs to
        """
        super(AquariaLocation, self).__init__(player, name, code, parent)
        self.event = code is None


locations_verse_cave_r = {
    "bulb_starting_cave_1": 698107,
    "bulb_starting_cave_2": 698108,
    "collect_big_seed": 698175,
}

locations_verse_cave_l = {
    "bulb_tutorial_1": 698021,
    "bulb_tutorial_2": 698022,
    "bulb_tutorial_3": 698023,
}

locations_home_water = {
    "bulb_home_water_1": 698058,
    "bulb_home_water_2": 698059,
    "bulb_home_water_3": 698060,
    "bulb_home_water_4": 698061,
    "bulb_home_water_5": 698062,
    "bulb_home_water_6": 698063,
    "bulb_home_water_7": 698064,
    "bulb_home_water_8": 698065,
    "collect_nautilus": 698194,
}

locations_naija_home = {
    "bulb_naija_home_1": 698119,
    "bulb_naija_home_2": 698120,
}

locations_song_cave = {
    "bulb_song_cave_1": 698071,
    "bulb_song_cave_2": 698072,
    "bulb_song_cave_3": 698073,
    "bulb_song_cave_4": 698074,
    "bulb_song_cave_5": 698075,
    "health_egg_4": 698160,
    "collect_anemone": 698162,
    "collect_jelly_beacon": 698178,
}

locations_song_cave_anemone = {
    "collect_anemone": 698162,
}

locations_energy_temple_1 = {
    "bulb_energy_temple_1_1": 698027,
    "collect_energy_statue": 698170,
}

locations_energy_temple_2 = {
    "bulb_energy_temple_2_1": 698028,
}

locations_energy_temple_altar = {
    "collect_energy_temple": 698163,
}

locations_energy_temple_3 = {
    "bulb_energy_temple_3_1": 698029,
}

locations_energy_temple_boss = {
    "collect_energy_boss": 698169,
    # Eventually, putting forest boss location here
}

locations_energy_temple_blaster_room = {
    "collect_blaster": 698195,
}

locations_openwater_tl = {
    "bulb_openwater_tl_1": 698001,
    "bulb_openwater_tl_2": 698002,
    "bulb_openwater_tl_3": 698003,
}

locations_openwater_tr = {
    "bulb_openwater_tr_1": 698004,
    "bulb_openwater_tr_2": 698005,
    "bulb_openwater_tr_3": 698006,
    "bulb_openwater_tr_4": 698007,
    "bulb_openwater_tr_5": 698008,
    "urn_openwater_tr_1": 698148,
    "urn_openwater_tr_2": 698149,
    "urn_openwater_tr_3": 698150,
}

locations_openwater_tr_turtle = {
    "bulb_openwater_tr_6": 698009,
}

locations_openwater_bl = {
    "bulb_openwater_bl_2": 698011,
}

locations_openwater_bl_fp = {
    "bulb_openwater_bl_1": 698010,
}

locations_skeleton_path = {
    "bulb_skeleton_path_1": 698012,
    "bulb_skeleton_path_2": 698013,
}

locations_skeleton_path_sc = {
    "collect_skull": 698177,
}

locations_arnassi = {
    "bulb_arnassi_1": 698014,
    "bulb_arnassi_2": 698015,
    "bulb_arnassi_3": 698016,
    "collect_spore_seed": 698179,
    "collect_seahorse_costume": 698191,
}

locations_arnassi_path = {
    "collect_arnassi_statue": 698164,
}

locations_arnassi_crab_boss = {
    "collect_crab_costume": 698187,
}

locations_simon = {
    "beating_simon": 698156,
}

locations_mithalas_city = {
    "bulb_mithalas_city_01": 698030,
    "bulb_mithalas_city_02": 698031,
    "bulb_mithalas_city_04": 698033,
    "bulb_mithalas_city_05": 698034,
    "bulb_mithalas_city_06": 698035,
    "bulb_mithalas_city_08": 698037,
    "bulb_mithalas_city_09": 698038,
    "bulb_mithalas_city_10": 698039,
    "bulb_mithalas_city_12": 698041,
}

locations_mithalas_city_urns = {
    "urn_mithalas_city_1": 698123,
    "urn_mithalas_city_2": 698124,
    "urn_mithalas_city_3": 698125,
    "urn_mithalas_city_4": 698126,
    "urn_mithalas_city_5": 698127,
    "urn_mithalas_city_7": 698129,
}

locations_mithalas_city_top_path = {
    "bulb_mithalas_city_03": 698032,
    "bulb_mithalas_city_07": 698036,
    "bulb_mithalas_city_11": 698040,
    "collect_mithalas_pot": 698174,
}

locations_mithalas_city_top_path_urn = {
    "urn_mithalas_city_6": 698128,
}

locations_mithalas_city_fishpass = {
    "collect_mithala_doll": 698173,
}

locations_cathedral_l = {
    "bulb_cathedral_l_2": 698042,
    "collect_mithalas_banner": 698165,
}

locations_cathedral_l_urns = {
    "urn_cathedral_l_1": 698130,
    "urn_cathedral_l_2": 698131,
    "urn_cathedral_l_3": 698132,
    "urn_cathedral_l_4": 698133,
    "urn_cathedral_l_5": 698134,
    "urn_cathedral_l_6": 698135,
}

locations_cathedral_l_tube = {
    # Eventually, putting mithalas friest boss location here
}

locations_cathedral_l_sc = {
    "collect_trident_head": 698183,
}

locations_cathedral_r = {
    "urn_cathedral_r_01": 698136,
    "urn_cathedral_r_02": 698137,
    "urn_cathedral_r_03": 698138,
    "urn_cathedral_r_04": 698139,
    "urn_cathedral_r_05": 698140,
    "urn_cathedral_r_06": 698141,
    "urn_cathedral_r_07": 698142,
    "urn_cathedral_r_08": 698143,
    "urn_cathedral_r_09": 698144,
    "urn_cathedral_r_10": 698145,
    "urn_cathedral_r_11": 698146,
    "urn_cathedral_r_12": 698147,
    "collect_mithalan_costume": 698189,
}

locations_cathedral_underground = {
    "bulb_cathedral_under_ground_1": 698113,
    "bulb_cathedral_under_ground_2": 698114,
    "bulb_cathedral_under_ground_3": 698115,
    "bulb_cathedral_under_ground_4": 698116,
    "bulb_cathedral_under_ground_5": 698117,
    "bulb_cathedral_under_ground_6": 698118,
}

locations_cathedral_boss = {
    # Eventually, putting mithalas boss location here
}

locations_forest_tl = {
    "bulb_forest_tl_1": 698044,
    "bulb_forest_tl_2": 698045,
    "bulb_forest_tl_3": 698046,
    "collect_upsidedown_seed": 698185,
}

locations_forest_tl_fp = {
    "bulb_forest_tl_4": 698047,
    "health_egg_2": 698158,
}

locations_forest_tr = {
    "bulb_forest_tr_1": 698048,
    "bulb_forest_tr_2": 698049,
    "bulb_forest_tr_4": 698051,
    "bulb_forest_tr_5": 698052,
    "bulb_forest_tr_6": 698053,
}

locations_forest_tr_dark = {
    "collect_blackpearl": 698167,
}

locations_forest_tr_fp = {
    "bulb_forest_tr_3": 698050,
}

locations_forest_bl_sc = {
    "collect_walker": 698186,
    "bulb_forest_bl_1": 698054,
}

locations_forest_br_ship = {
    "collect_treasure_chest": 698168,
}

locations_forest_boss = {
    # Eventually, putting forest boss location here
}

locations_forest_boss_entrance = {
    "bulb_forest_boss_room_1": 698055,
}

locations_forest_fish_cave = {
    # Eventually, putting fish cave location here
}

locations_forest_sprite_cave = {
    "bulb_forest_sprite_cave_1": 698056,
}

locations_forest_sprite_cave_tube = {
    "bulb_forest_sprite_cave_2": 698057,
    "collect_seed_bag": 698176,
}

locations_mermog_cave = {
    "bulb_mermog_cave_1": 698121,
}

locations_mermog_boss = {
    "collect_piranha": 698197,
}

locations_veil_tl = {
    "bulb_veil_tl_3": 698078,
}

locations_veil_tl_fp = {
    "bulb_veil_tl_2": 698077,
}

locations_veil_tl_rock = {
    "bulb_veil_tl_1": 698076,
}

locations_turtle_cave_rocks = {
    "collect_turtle_egg": 698184,
}

locations_turtle_cave_bubble = {
    "bulb_turtlecave": 698000,
}

locations_turtle_cave_top_bubble = {
    "collect_urchin_costume": 698193,
}

locations_veil_tr_l = {
}

locations_veil_tr_r = { # Failaise nécessite le Beast form
    "bulb_veil_tr_1": 698079,
    "collect_gold_star": 698180,
}

locations_veil_tr_water_fall = {
    "bulb_veil_tr_2": 698080,
}

locations_veil_bl = {
    "bulb_veil_b_2": 698082,
}

locations_veil_b_sc = {
    "bulb_veil_b_1": 698081,
}

locations_veil_bl_fp = {
    "health_egg_1": 698157,
}

locations_veil_br = {
    "collect_stone_head": 698181,
}

locations_octo_cave_t = {
    "collect_dumbo": 698196,
}

locations_octo_cave_b = {
    "bulb_octo_cave_1": 698122,
}

locations_bubble_cave = {
    "bulb_bubble_cave_1": 698089,
    "bulb_bubble_cave_2": 698090,
    "health_egg_5": 698161,
}

locations_sun_temple_l = {
    "bulb_sun_temple_4": 698094,
    "bulb_sun_temple_5": 698095,
    "bulb_sun_temple_6": 698096,
    "collect_golden_gear": 698171,
}

locations_sun_temple_r = {
    "bulb_sun_temple_1": 698091,
    "bulb_sun_temple_2": 698092,
    "bulb_sun_temple_3": 698093,
    "collect_sun_key": 698182,
}

locations_sun_temple_boss_lb = {
    "bulb_sunworm_1": 698017,
    "bulb_sunworm_2": 698018,
}

locations_sun_temple_boss_lt = {
    "bulb_sunworm_3": 698019,
    "bulb_sunworm_4": 698020,
}

locations_sun_temple_boss_r = {
    # Eventually, putting sun boss location here
}

locations_abyss_l = {
    "bulb_abyss_l_1": 698024,
    "bulb_abyss_l_2": 698025,
    "collect_bio_seed": 698166,
    "collect_jelly_plant": 698172,
}

locations_abyss_l_fp = {
    "bulb_abyss_l_3": 698026,
}

locations_abyss_r = {
    "bulb_abyss_r_1": 698109,
    "bulb_abyss_r_2": 698110,
    "bulb_abyss_r_3": 698111,
    "bulb_abyss_r_4": 698112,
}

locations_ice_cave = {
    "bulb_ice_cave_1": 698083,
    "bulb_ice_cave_2": 698084,
    "bulb_ice_cave_3": 698085,
    "bulb_ice_cave_4": 698086,
    "bulb_ice_cave_5": 698087,
}

locations_king_jellyfish_cave = {
    "bulb_king_jellyfish_cave_1": 698088,
    "collect_jelly_costume": 698188,
}

locations_whale = {
    "health_egg_3": 698159,
}

locations_sunkencity_r = {
    "crate_sunkencity_1_1": 698154,
    "crate_sunkencity_1_2": 698155,
}

locations_sunkencity_l = {
    "crate_sunkencity_2_1": 698151,
    "crate_sunkencity_2_2": 698152,
    "crate_sunkencity_2_3": 698153,
}

locations_sunkencity_l_bedroom = {
    "collect_teen_costume": 698192,
}

locations_sunkencity_boss = {
    "bulb_boilerroom_1": 698043,
}

locations_body_c = {
    "bulb_final_c_1": 698097,
}

locations_body_l = {
    "bulb_final_l_1": 698066,
    "bulb_final_l_2": 698067,
    "bulb_final_l_3": 698068,
    "bulb_final_l_4": 698069,
    "bulb_final_l_5": 698070,
}

locations_body_rt = {
    "bulb_final_r_3": 698100,
}

locations_body_rb = {
    "bulb_final_r_1": 698098,
    "bulb_final_r_2": 698099,
}

locations_body_b = {
    "bulb_final_b_1": 698101,
    "bulb_final_b_2": 698102,
    "collect_mutant_costume": 698190,
}

locations_final_boss_tube = {
    "bulb_final_boss_1": 698103,
    "bulb_final_boss_2": 698104,
    "bulb_final_boss_3": 698105,
}

locations_final_boss_3_form = {
    "bulb_final_boss_4": 698106,
}

location_table = {
    **locations_openwater_tl,
    **locations_openwater_tr,
    **locations_openwater_tr_turtle,
    **locations_openwater_bl,
    **locations_openwater_bl_fp,
    **locations_skeleton_path,
    **locations_skeleton_path_sc,
    **locations_arnassi,
    **locations_arnassi_path,
    **locations_arnassi_crab_boss,
    **locations_sun_temple_l,
    **locations_sun_temple_r,
    **locations_sun_temple_boss_lt,
    **locations_sun_temple_boss_lb,
    **locations_sun_temple_boss_r,
    **locations_verse_cave_r,
    **locations_verse_cave_l,
    **locations_abyss_l,
    **locations_abyss_l_fp,
    **locations_abyss_r,
    **locations_energy_temple_1,
    **locations_energy_temple_2,
    **locations_energy_temple_3,
    **locations_energy_temple_boss,
    **locations_energy_temple_blaster_room,
    **locations_mithalas_city,
    **locations_mithalas_city_urns,
    **locations_mithalas_city_top_path,
    **locations_mithalas_city_top_path_urn,
    **locations_mithalas_city_fishpass,
    **locations_cathedral_l,
    **locations_cathedral_l_urns,
    **locations_cathedral_l_tube,
    **locations_cathedral_l_sc,
    **locations_cathedral_r,
    **locations_cathedral_underground,
    **locations_cathedral_boss,
    **locations_forest_tl,
    **locations_forest_tl_fp,
    **locations_forest_tr,
    **locations_forest_tr_dark,
    **locations_forest_tr_fp,
    **locations_forest_bl_sc,
    **locations_forest_br_ship,
    **locations_forest_boss,
    **locations_forest_boss_entrance,
    **locations_forest_sprite_cave,
    **locations_forest_sprite_cave_tube,
    **locations_forest_fish_cave,
    **locations_home_water,
    **locations_body_l,
    **locations_body_rt,
    **locations_body_rb,
    **locations_body_c,
    **locations_body_b,
    **locations_final_boss_tube,
    **locations_final_boss_3_form,
    **locations_song_cave,
    **locations_veil_tl,
    **locations_veil_tl_fp,
    **locations_veil_tl_rock,
    **locations_turtle_cave_rocks,
    **locations_turtle_cave_bubble,
    **locations_turtle_cave_top_bubble,
    **locations_veil_tr_l,
    **locations_veil_tr_r,
    **locations_veil_tr_water_fall,
    **locations_veil_bl,
    **locations_veil_b_sc,
    **locations_veil_bl_fp,
    **locations_veil_br,
    **locations_ice_cave,
    **locations_king_jellyfish_cave,
    **locations_bubble_cave,
    **locations_naija_home,
    **locations_mermog_cave,
    **locations_mermog_boss,
    **locations_octo_cave_t,
    **locations_octo_cave_b,
    **locations_sunkencity_l,
    **locations_sunkencity_r,
    **locations_sunkencity_boss,
    **locations_simon,
    **locations_whale,
}
