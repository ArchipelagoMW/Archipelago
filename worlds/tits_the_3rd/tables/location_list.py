from collections import namedtuple

from ..names.item_name import ItemName
from ..names.location_name import LocationName
from ..names.region_name import RegionName
from ..names.check_type_name import CheckTypeName

Data = namedtuple('Data', ['flag', 'check_type', 'region', 'vanilla_item','spoiler_name'])

#   Location                                                                                    Flag            Check type                          Region                                          Vanilla item                                        Spoiler Name
location_table = dict([

    ## Character Initial Gear
    ### Kevin
    (LocationName.kevin_initial_weapon,                                                         Data(1180,      CheckTypeName.character_gear,       RegionName.hermit_garden,                       "",                                                 LocationName.kevin_initial_weapon_spoiler)),
    (LocationName.kevin_initial_armor,                                                          Data(1181,      CheckTypeName.character_gear,       RegionName.hermit_garden,                       "",                                                 LocationName.kevin_initial_armor_spoiler)),
    (LocationName.kevin_initial_boots,                                                          Data(1182,      CheckTypeName.character_gear,       RegionName.hermit_garden,                       "",                                                 LocationName.kevin_initial_boots_spoiler)),
    ### Ries
    (LocationName.ries_initial_weapon,                                                          Data(1240,      CheckTypeName.character_gear,       RegionName.hermit_garden,                       "",                                                 LocationName.ries_initial_weapon_spoiler)),
    (LocationName.ries_initial_armor,                                                           Data(1241,      CheckTypeName.character_gear,       RegionName.hermit_garden,                       "",                                                 LocationName.ries_initial_armor_spoiler)),
    (LocationName.ries_initial_boots,                                                           Data(1242,      CheckTypeName.character_gear,       RegionName.hermit_garden,                       "",                                                 LocationName.ries_initial_boots_spoiler)),
    ### Tita
    (LocationName.tita_initial_weapon,                                                          Data(1160,      CheckTypeName.character_gear,       RegionName.jade_corridor_start,                 "",                                                 LocationName.ries_initial_weapon_spoiler)),
    (LocationName.tita_initial_armor,                                                           Data(1161,      CheckTypeName.character_gear,       RegionName.jade_corridor_start,                 "",                                                 LocationName.tita_initial_armor_spoiler)),
    (LocationName.tita_initial_boots,                                                           Data(1162,      CheckTypeName.character_gear,       RegionName.jade_corridor_start,                 "",                                                 LocationName.tita_initial_boots)),
    (LocationName.tita_orbment_item_1,                                                          Data(1163,      CheckTypeName.character_quartz,     RegionName.jade_corridor_start,                 ItemName.ep_cut_2,                                  LocationName.tita_orbment_item_1_spoiler)),
    (LocationName.tita_orbment_item_2,                                                          Data(1164,      CheckTypeName.character_quartz,     RegionName.jade_corridor_start,                 ItemName.attack_1,                                  LocationName.tita_orbment_item_2_spoiler)),
    (LocationName.tita_orbment_item_3,                                                          Data(1165,      CheckTypeName.character_quartz,     RegionName.jade_corridor_start,                 ItemName.eagle_eye,                                 LocationName.tita_orbment_item_3_spoiler)),
    (LocationName.tita_orbment_item_4,                                                          Data(1166,      CheckTypeName.character_quartz,     RegionName.jade_corridor_start,                 ItemName.hp_1,                                      LocationName.tita_orbment_item_4_spoiler)),
    ### Julia
    (LocationName.julia_initial_weapon,                                                         Data(1230,      CheckTypeName.character_gear,       RegionName.jade_corridor_arseille,              "",                                                 LocationName.julia_initial_weapon_spoiler)),
    (LocationName.julia_initial_armor,                                                          Data(1231,      CheckTypeName.character_gear,       RegionName.jade_corridor_arseille,              "",                                                 LocationName.julia_initial_armor_spoiler)),
    (LocationName.julia_initial_boots,                                                          Data(1232,      CheckTypeName.character_gear,       RegionName.jade_corridor_arseille,              "",                                                 LocationName.julia_initial_boots_spoiler)),
    (LocationName.julia_orbment_item_1,                                                         Data(1233,      CheckTypeName.character_quartz,     RegionName.jade_corridor_arseille,              ItemName.ep_cut_2,                                  LocationName.julia_orbment_item_1_spoiler)),
    (LocationName.julia_orbment_item_2,                                                         Data(1234,      CheckTypeName.character_quartz,     RegionName.jade_corridor_arseille,              ItemName.action_1,                                  LocationName.julia_orbment_item_2_spoiler)),
    (LocationName.julia_orbment_item_3,                                                         Data(1235,      CheckTypeName.character_quartz,     RegionName.jade_corridor_arseille,              ItemName.hit_1,                                     LocationName.julia_orbment_item_3_spoiler)),
    (LocationName.julia_orbment_item_4,                                                         Data(1236,      CheckTypeName.character_quartz,     RegionName.jade_corridor_arseille,              ItemName.range_1,                                   LocationName.julia_orbment_item_4_spoiler)),
    (LocationName.julia_orbment_item_5,                                                         Data(1237,      CheckTypeName.character_quartz,     RegionName.jade_corridor_arseille,              ItemName.move_1,                                    LocationName.julia_orbment_item_5_spoiler)),
    (LocationName.julia_orbment_item_6,                                                         Data(1238,      CheckTypeName.character_quartz,     RegionName.jade_corridor_arseille,              ItemName.attack_1,                                  LocationName.julia_orbment_item_6_spoiler)),
    (LocationName.julia_orbment_item_7,                                                         Data(1239,      CheckTypeName.character_quartz,     RegionName.jade_corridor_arseille,              ItemName.shield_1,                                  LocationName.julia_orbment_item_7_spoiler)),

    ## Sealing Stones
    ### Tita
    (LocationName.sealing_stone_tita,                                                           Data(9740,      CheckTypeName.character,            RegionName.jade_corridor_start,                 ItemName.tita,                                      LocationName.sealing_stone_tita_spoiler)),
    (LocationName.sealing_stone_jade_corridor_1_unlock,                                         Data(2256,      CheckTypeName.area_unlock,          RegionName.jade_corridor_start,                 ItemName.jade_corridor_unlock_1,                    "")),
    (LocationName.sealing_stone_arseille_unlock,                                                Data(2258,      CheckTypeName.area_unlock,          RegionName.jade_corridor_start,                 ItemName.jade_corridor_arseille_unlock,             "")),
    ### Julia
    (LocationName.sealing_stone_julia,                                                          Data(9753,      CheckTypeName.character,            RegionName.jade_corridor_arseille,              ItemName.julia,                                     LocationName.sealing_stone_julia_spoiler)),
    (LocationName.sealing_stone_jade_corridor_2_unlock,                                         Data(2257,      CheckTypeName.area_unlock,          RegionName.jade_corridor_arseille,              ItemName.jade_corridor_unlock_2,                    "")),

    ## Bosses
    (LocationName.chapter1_boss_defeated,                                                       Data(9757,      CheckTypeName.boss,                 RegionName.jade_corridor_expansion_area_2,      ItemName.bennu_defeat,                              "")),

    ## Chests
    ### Lusitania
    (LocationName.lusitania_chest_bedroom_beside_banquet,                                       Data(9720,      CheckTypeName.chest,                RegionName.lusitania,                           ItemName.teara_balm,                                "")),
    (LocationName.lusitania_chest_bedroom_past_library,                                         Data(9721,      CheckTypeName.chest,                RegionName.lusitania,                           ItemName.ep_charge,                                 "")),
    (LocationName.lusitania_chest_bedroom_past_casino_left,                                     Data(9722,      CheckTypeName.chest,                RegionName.lusitania,                           ItemName.teara_balm,                                "")),
    (LocationName.lusitania_chest_bedroom_past_casino_right,                                    Data(9723,      CheckTypeName.chest,                RegionName.lusitania,                           ItemName.ep_charge,                                 "")),
    ### Jade Corridor
    #### Start
    (LocationName.jade_corridor_chest_first_hall_straight_from_start,                           Data(9857,      CheckTypeName.chest,                RegionName.jade_corridor_start,                 ItemName.information,                               "")),
    (LocationName.jade_corridor_chest_first_hall_elevated_platform,                             Data(9858,      CheckTypeName.chest,                RegionName.jade_corridor_start,                 ItemName.tear_balm,                                 "")),
    (LocationName.jade_corridor_chest_first_hall_before_first_warp,                             Data(9859,      CheckTypeName.chest,                RegionName.jade_corridor_start,                 ItemName.mira_300,                                  "")),
    #### Area 1
    (LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_second_chest,       Data(9864,      CheckTypeName.chest,                RegionName.jade_corridor_expansion_area_1,      ItemName.extra_spicy_fries,                         "")),
    (LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_third_chest,        Data(9865,      CheckTypeName.chest,                RegionName.jade_corridor_expansion_area_1,      ItemName.tear_balm,                                 "")),
    (LocationName.jade_corridor_chest_down_from_checkpoint_lowered_platform_first_chest,        Data(9866,      CheckTypeName.chest,                RegionName.jade_corridor_expansion_area_1,      ItemName.smelling_salts,                            "")),
    (LocationName.jade_corridor_chest_left_of_sun_door_one,                                     Data(9867,      CheckTypeName.chest,                RegionName.jade_corridor_expansion_area_1,      ItemName.black_bangle,                              "")),
    (LocationName.jade_corridor_chest_right_of_sun_door_one,                                    Data(9868,      CheckTypeName.chest,                RegionName.jade_corridor_expansion_area_1,      ItemName.glam_choker,                               "")),
    #### Arseille
    (LocationName.jade_corridor_chest_arseille_deck,                                            Data(9869,      CheckTypeName.chest,                RegionName.jade_corridor_arseille,              ItemName.royal_spikes,                              "")),
    (LocationName.jade_corridor_chest_arseille_confrence_room,                                  Data(9872,      CheckTypeName.chest,                RegionName.jade_corridor_arseille,              ItemName.hit_2,                                     "")),
    (LocationName.jade_corridor_chest_arseille_kitchen,                                         Data(9873,      CheckTypeName.chest,                RegionName.jade_corridor_arseille,              ItemName.easy_paella_recipe,                        "")),
    (LocationName.jade_corridor_chest_arseille_bedroom_one,                                     Data(9874,      CheckTypeName.chest,                RegionName.jade_corridor_arseille,              ItemName.reviving_balm,                             "")),
    (LocationName.jade_corridor_chest_arseille_bedroom_two,                                     Data(9875,      CheckTypeName.chest,                RegionName.jade_corridor_arseille,              ItemName.mira_300,                                  "")),
    #### Area 2
    (LocationName.jade_corridor_chest_left_from_checkpoint_first_chest,                         Data(9880,      CheckTypeName.chest,                RegionName.jade_corridor_expansion_area_2,      ItemName.fresh_water,                               "")),
    (LocationName.jade_corridor_chest_left_from_checkpoint_second_chest,                        Data(9881,      CheckTypeName.chest,                RegionName.jade_corridor_expansion_area_2,      ItemName.lower_elements_sepith_50,                  "")),
    (LocationName.jade_corridor_chest_left_from_checkpoint_third_chest,                         Data(9884,      CheckTypeName.chest,                RegionName.jade_corridor_expansion_area_2,      ItemName.fishy_finale,                              "")),
    (LocationName.jade_corridor_chest_left_from_checkpoint_fourth_chest,                        Data(9885,      CheckTypeName.chest,                RegionName.jade_corridor_expansion_area_2,      ItemName.higher_elements_sepith_50,                 "")),

    ### Grancel
    #### Day
    ##### South
    (LocationName.day_grancel_south_house_behind_arms_dealer,                                   Data(10112,     CheckTypeName.chest,                RegionName.day_grancel_south,                   ItemName.insulating_tape,                           "")),
    (LocationName.day_grancel_south_bar,                                                        Data(10113,     CheckTypeName.chest,                RegionName.day_grancel_south,                   ItemName.smelling_salts,                            "")),
    (LocationName.day_grancel_south_arms_dealer,                                                Data(10116,     CheckTypeName.chest,                RegionName.day_grancel_south,                   ItemName.akashic_heart,                             "")),
    (LocationName.day_grancel_south_orbment_store,                                              Data(10119,     CheckTypeName.chest,                RegionName.day_grancel_south,                   ItemName.hp_2,                                      "")),
    (LocationName.day_grancel_south_house_behind_bracer_guild,                                  Data(10120,     CheckTypeName.chest,                RegionName.day_grancel_south,                   ItemName.fried_phoenix,                             "")),
    ##### West
    (LocationName.day_grancel_west_house_east_of_stairs,                                        Data(10114,     CheckTypeName.chest,                RegionName.day_grancel_west,                    ItemName.s_tablet,                                  "")),
    (LocationName.day_grancel_west_house_west_of_stairs,                                        Data(10115,     CheckTypeName.chest,                RegionName.day_grancel_west,                    ItemName.teara_balm,                                "")),
    (LocationName.day_grancel_west_restaurant_left_chest,                                       Data(10121,     CheckTypeName.chest,                RegionName.day_grancel_west,                    ItemName.brain_roast,                               "")),
    (LocationName.day_grancel_west_restaurant_right_chest,                                      Data(10122,     CheckTypeName.chest,                RegionName.day_grancel_west,                    ItemName.swingwich,                                 "")),
    (LocationName.day_grancel_west_church_behind_the_lectern,                                   Data(10123,     CheckTypeName.chest,                RegionName.day_grancel_west,                    ItemName.celestial_balm,                            "")),
    (LocationName.day_grancel_west_church_se_room,                                              Data(10124,     CheckTypeName.chest,                RegionName.day_grancel_west,                    ItemName.teara_balm,                                "")),
    (LocationName.day_grancel_west_church_sw_room,                                              Data(10125,     CheckTypeName.chest,                RegionName.day_grancel_west,                    ItemName.stun_gb,                                   "")),
    (LocationName.day_grancel_west_liberl_news,                                                 Data(10133,     CheckTypeName.chest,                RegionName.day_grancel_west,                    ItemName.black_bangle_plus,                         "")),
    (LocationName.day_grancel_west_north_house,                                                 Data(10173,     CheckTypeName.chest,                RegionName.day_grancel_west,                    ItemName.lower_elements_sepith_50,                  "")),
    ##### North
    (LocationName.day_grancel_north_hotel_2nd_floor_lobby,                                      Data(10126,     CheckTypeName.chest,                RegionName.day_grancel_north,                   ItemName.white_bracelet,                            "")),
    (LocationName.day_grancel_north_hotel_1st_floor_ne_room,                                    Data(10127,     CheckTypeName.chest,                RegionName.day_grancel_north,                   ItemName.mira_500,                                  "")),
    (LocationName.day_grancel_north_hotel_2nd_floor_se_room,                                    Data(10128,     CheckTypeName.chest,                RegionName.day_grancel_north,                   ItemName.mira_500,                                  "")),
    (LocationName.day_grancel_north_hotel_2nd_floor_nw_room,                                    Data(10129,     CheckTypeName.chest,                RegionName.day_grancel_north,                   ItemName.mira_500,                                  "")),
    (LocationName.day_grancel_north_west_house,                                                 Data(10172,     CheckTypeName.chest,                RegionName.day_grancel_north,                   ItemName.lower_elements_sepith_50,                  "")),
    ##### East
    (LocationName.day_grancel_east_erebonian_ambassy_center_room,                               Data(10174,     CheckTypeName.chest,                RegionName.day_grancel_east,                    ItemName.bestia_coat,                               "")),
    (LocationName.day_grancel_east_erebonian_ambassy_right_room,                                Data(10175,     CheckTypeName.chest,                RegionName.day_grancel_east,                    ItemName.teara_balm,                                "")),
    (LocationName.day_grancel_east_department_store_se,                                         Data(10176,     CheckTypeName.chest,                RegionName.day_grancel_east,                    ItemName.proxy_puppet,                              "")),
    (LocationName.day_grancel_east_department_store_ne,                                         Data(10177,     CheckTypeName.chest,                RegionName.day_grancel_east,                    ItemName.softening_balm,                            "")),
    (LocationName.day_grancel_east_department_store_nw,                                         Data(10178,     CheckTypeName.chest,                RegionName.day_grancel_east,                    ItemName.septium_drops,                             "")),
    ##### Port
    (LocationName.day_grancel_port_east_of_boat,                                                Data(10160,     CheckTypeName.chest,                RegionName.day_grancel_port,                    ItemName.teara_balm,                                "")),
    (LocationName.day_grancel_port_west_of_boat,                                                Data(10161,     CheckTypeName.chest,                RegionName.day_grancel_port,                    ItemName.purging_balm,                              "")),
    (LocationName.day_grancel_port_around_2nd_warehouse,                                        Data(10162,     CheckTypeName.chest,                RegionName.day_grancel_port,                    ItemName.purging_balm,                              "")),
    (LocationName.day_grancel_port_before_2nd_warehouse,                                        Data(10163,     CheckTypeName.chest,                RegionName.day_grancel_port,                    ItemName.crimson_eye,                               "")),
    (LocationName.day_grancel_port_west_after_first_warehouse,                                  Data(10164,     CheckTypeName.chest,                RegionName.day_grancel_port,                    ItemName.teara_balm,                                "")),
    (LocationName.day_grancel_port_near_lighthouse,                                             Data(10165,     CheckTypeName.chest,                RegionName.day_grancel_port,                    ItemName.scent,                                     "")),
    (LocationName.day_grancel_port_south_east_of_boat,                                          Data(10166,     CheckTypeName.chest,                RegionName.day_grancel_port,                    ItemName.ep_charge,                                 "")),
    (LocationName.day_grancel_port_first_warehouse,                                             Data(10168,     CheckTypeName.chest,                RegionName.day_grancel_port,                    ItemName.long_barrel_2,                             "")),
    #### Night
    ##### South
    (LocationName.night_grancel_south_house_behind_arms_dealer,                                 Data(2112,      CheckTypeName.chest,                RegionName.night_grancel_south,                 "",                                                 "")),
    (LocationName.night_grancel_south_bar,                                                      Data(2113,      CheckTypeName.chest,                RegionName.night_grancel_south,                 "",                                                 "")),
    (LocationName.night_grancel_south_arms_dealer,                                              Data(2116,      CheckTypeName.chest,                RegionName.night_grancel_south,                 "",                                                 "")),
    (LocationName.night_grancel_south_orbment_store,                                            Data(2119,      CheckTypeName.chest,                RegionName.night_grancel_south,                 "",                                                 "")),
    (LocationName.night_grancel_south_house_behind_bracer_guild,                                Data(2120,      CheckTypeName.chest,                RegionName.night_grancel_south,                 "",                                                 "")),
    ##### West
    (LocationName.night_grancel_west_house_east_of_stairs,                                      Data(2114,      CheckTypeName.chest,                RegionName.night_grancel_west,                  "",                                                 "")),
    (LocationName.night_grancel_west_house_west_of_stairs,                                      Data(2115,      CheckTypeName.chest,                RegionName.night_grancel_west,                  "",                                                 "")),
    (LocationName.night_grancel_west_restaurant_left_chest,                                     Data(2121,      CheckTypeName.chest,                RegionName.night_grancel_west,                  "",                                                 "")),
    (LocationName.night_grancel_west_restaurant_right_chest,                                    Data(2122,      CheckTypeName.chest,                RegionName.night_grancel_west,                  "",                                                 "")),
    (LocationName.night_grancel_west_church_behind_the_lectern,                                 Data(2123,      CheckTypeName.chest,                RegionName.night_grancel_west,                  "",                                                 "")),
    (LocationName.night_grancel_west_church_se_room,                                            Data(2124,      CheckTypeName.chest,                RegionName.night_grancel_west,                  "",                                                 "")),
    (LocationName.night_grancel_west_church_sw_room,                                            Data(2125,      CheckTypeName.chest,                RegionName.night_grancel_west,                  "",                                                 "")),
    (LocationName.night_grancel_west_liberl_news,                                               Data(2133,      CheckTypeName.chest,                RegionName.night_grancel_west,                  "",                                                 "")),
    (LocationName.night_grancel_west_north_house,                                               Data(2173,      CheckTypeName.chest,                RegionName.night_grancel_west,                  "",                                                 "")),
    ##### North
    (LocationName.night_grancel_north_hotel_2nd_floor_lobby,                                    Data(2126,      CheckTypeName.chest,                RegionName.night_grancel_north,                 "",                                                 "")),
    (LocationName.night_grancel_north_hotel_1st_floor_ne_room,                                  Data(2127,      CheckTypeName.chest,                RegionName.night_grancel_north,                 "",                                                 "")),
    (LocationName.night_grancel_north_hotel_2nd_floor_se_room,                                  Data(2128,      CheckTypeName.chest,                RegionName.night_grancel_north,                 "",                                                 "")),
    (LocationName.night_grancel_north_hotel_2nd_floor_nw_room,                                  Data(2129,      CheckTypeName.chest,                RegionName.night_grancel_north,                 "",                                                 "")),
    (LocationName.night_grancel_north_west_house,                                               Data(2172,      CheckTypeName.chest,                RegionName.night_grancel_north,                 "",                                                 "")),
    ##### East
    (LocationName.night_grancel_east_erebonian_ambassy_center_room,                             Data(2174,      CheckTypeName.chest,                RegionName.night_grancel_east,                  "",                                                 "")),
    (LocationName.night_grancel_east_erebonian_ambassy_right_room,                              Data(2175,      CheckTypeName.chest,                RegionName.night_grancel_east,                  "",                                                 "")),
    (LocationName.night_grancel_east_department_store_se,                                       Data(2176,      CheckTypeName.chest,                RegionName.night_grancel_east,                  "",                                                 "")),
    (LocationName.night_grancel_east_department_store_ne,                                       Data(2177,      CheckTypeName.chest,                RegionName.night_grancel_east,                  "",                                                 "")),
    (LocationName.night_grancel_east_department_store_nw,                                       Data(2178,      CheckTypeName.chest,                RegionName.night_grancel_east,                  "",                                                 "")),
    ##### Port
    (LocationName.night_grancel_port_east_of_boat,                                              Data(2160,      CheckTypeName.chest,                RegionName.night_grancel_port,                  "",                                                 "")),
    (LocationName.night_grancel_port_west_of_boat,                                              Data(2161,      CheckTypeName.chest,                RegionName.night_grancel_port,                  "",                                                 "")),
    (LocationName.night_grancel_port_around_2nd_warehouse,                                      Data(2162,      CheckTypeName.chest,                RegionName.night_grancel_port,                  "",                                                 "")),
    (LocationName.night_grancel_port_before_2nd_warehouse,                                      Data(2163,      CheckTypeName.chest,                RegionName.night_grancel_port,                  "",                                                 "")),
    (LocationName.night_grancel_port_west_after_first_warehouse,                                Data(2164,      CheckTypeName.chest,                RegionName.night_grancel_port,                  "",                                                 "")),
    (LocationName.night_grancel_port_near_lighthouse,                                           Data(2165,      CheckTypeName.chest,                RegionName.night_grancel_port,                  "",                                                 "")),
    (LocationName.night_grancel_port_south_east_of_boat,                                        Data(2166,      CheckTypeName.chest,                RegionName.night_grancel_port,                  "",                                                 "")),
    (LocationName.night_grancel_port_first_warehouse,                                           Data(2168,      CheckTypeName.chest,                RegionName.night_grancel_port,                  "",                                                 "")),
    #### Castle
    (LocationName.grancel_castle_balcony_west_chest,                                            Data(10136,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.teara_balm,                                "")),
    (LocationName.grancel_castle_balcony_south_chest,                                           Data(10137,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.attack_2,                                  "")),
    (LocationName.grancel_castle_dining_room,                                                   Data(10138,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.shield_2,                                  "")),
    (LocationName.grancel_castle_west_room,                                                     Data(10144,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.teara_balm,                                "")),
    (LocationName.grancel_castle_kitchen_left,                                                  Data(10145,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.queenly_cookie,                            "")),
    (LocationName.grancel_castle_kitchen_right,                                                 Data(10146,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.fluffy_crepe,                              "")),
    (LocationName.grancel_castle_throne_room,                                                   Data(10147,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.glam_choker_plus,                          "")),
    (LocationName.grancel_castle_2nd_floor_east_corridor_sw_room,                               Data(10148,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.zeram_powder,                              "")),
    (LocationName.grancel_castle_2nd_floor_westmost_room,                                       Data(10149,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.pearl_earings,                             "")),
    (LocationName.grancel_castle_basement_north,                                                Data(10150,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.repellent_dish,                            "")),
    (LocationName.grancel_castle_basement_south,                                                Data(10151,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.teara_balm,                                "")),
    (LocationName.grancel_castle_queens_bedroom,                                                Data(10152,     CheckTypeName.chest,                RegionName.grancel_castle,                      ItemName.haze,                                      "")),
])
