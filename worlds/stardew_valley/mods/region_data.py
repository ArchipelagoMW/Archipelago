from .mod_data import ModNames
from ..content.mods.sve import SVE_GINGER_ISLAND_PACK
from ..regions.model import RegionData, ConnectionData, MergeFlag, RandomizationFlag, ModRegionsData
from ..strings.entrance_names import Entrance, DeepWoodsEntrance, EugeneEntrance, LaceyEntrance, BoardingHouseEntrance, \
    JasperEntrance, AlecEntrance, YobaEntrance, JunaEntrance, MagicEntrance, AyeishaEntrance, RileyEntrance, SVEEntrance, AlectoEntrance
from ..strings.region_names import Region, DeepWoodsRegion, EugeneRegion, JasperRegion, BoardingHouseRegion, \
    AlecRegion, YobaRegion, JunaRegion, MagicRegion, AyeishaRegion, RileyRegion, SVERegion, AlectoRegion, LaceyRegion

deep_woods_regions = [
    RegionData(Region.farm, (DeepWoodsEntrance.use_woods_obelisk,)),
    RegionData(DeepWoodsRegion.woods_obelisk_menu, (DeepWoodsEntrance.deep_woods_depth_1,
                                                    DeepWoodsEntrance.deep_woods_depth_10,
                                                    DeepWoodsEntrance.deep_woods_depth_20,
                                                    DeepWoodsEntrance.deep_woods_depth_30,
                                                    DeepWoodsEntrance.deep_woods_depth_40,
                                                    DeepWoodsEntrance.deep_woods_depth_50,
                                                    DeepWoodsEntrance.deep_woods_depth_60,
                                                    DeepWoodsEntrance.deep_woods_depth_70,
                                                    DeepWoodsEntrance.deep_woods_depth_80,
                                                    DeepWoodsEntrance.deep_woods_depth_90,
                                                    DeepWoodsEntrance.deep_woods_depth_100)),
    RegionData(Region.secret_woods, (DeepWoodsEntrance.secret_woods_to_deep_woods,)),
    RegionData(DeepWoodsRegion.main_lichtung, (DeepWoodsEntrance.deep_woods_house,)),
    RegionData(DeepWoodsRegion.abandoned_home),
    RegionData(DeepWoodsRegion.floor_10),
    RegionData(DeepWoodsRegion.floor_20),
    RegionData(DeepWoodsRegion.floor_30),
    RegionData(DeepWoodsRegion.floor_40),
    RegionData(DeepWoodsRegion.floor_50),
    RegionData(DeepWoodsRegion.floor_60),
    RegionData(DeepWoodsRegion.floor_70),
    RegionData(DeepWoodsRegion.floor_80),
    RegionData(DeepWoodsRegion.floor_90),
    RegionData(DeepWoodsRegion.floor_100),
]

deep_woods_entrances = [
    ConnectionData(DeepWoodsEntrance.use_woods_obelisk, DeepWoodsRegion.woods_obelisk_menu),
    ConnectionData(DeepWoodsEntrance.secret_woods_to_deep_woods, DeepWoodsRegion.main_lichtung),
    ConnectionData(DeepWoodsEntrance.deep_woods_house, DeepWoodsRegion.abandoned_home, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_1, DeepWoodsRegion.main_lichtung),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_10, DeepWoodsRegion.floor_10),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_20, DeepWoodsRegion.floor_20),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_30, DeepWoodsRegion.floor_30),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_40, DeepWoodsRegion.floor_40),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_50, DeepWoodsRegion.floor_50),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_60, DeepWoodsRegion.floor_60),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_70, DeepWoodsRegion.floor_70),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_80, DeepWoodsRegion.floor_80),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_90, DeepWoodsRegion.floor_90),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_100, DeepWoodsRegion.floor_100),
]

eugene_regions = [
    RegionData(Region.forest, (EugeneEntrance.forest_to_garden,)),
    RegionData(EugeneRegion.eugene_garden, (EugeneEntrance.garden_to_bedroom,)),
    RegionData(EugeneRegion.eugene_bedroom),
]

eugene_entrances = [
    ConnectionData(EugeneEntrance.forest_to_garden, EugeneRegion.eugene_garden,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(EugeneEntrance.garden_to_bedroom, EugeneRegion.eugene_bedroom, flag=RandomizationFlag.BUILDINGS),
]

magic_regions = [
    RegionData(Region.pierre_store, (MagicEntrance.store_to_altar,)),
    RegionData(MagicRegion.altar),
]

magic_entrances = [
    ConnectionData(MagicEntrance.store_to_altar, MagicRegion.altar, flag=RandomizationFlag.NOT_RANDOMIZED),
]

jasper_regions = [
    RegionData(Region.museum, (JasperEntrance.museum_to_bedroom,)),
    RegionData(JasperRegion.jasper_bedroom),
]

jasper_entrances = [
    ConnectionData(JasperEntrance.museum_to_bedroom, JasperRegion.jasper_bedroom, flag=RandomizationFlag.BUILDINGS),
]
alec_regions = [
    RegionData(Region.forest, (AlecEntrance.forest_to_petshop,)),
    RegionData(AlecRegion.pet_store, (AlecEntrance.petshop_to_bedroom,)),
    RegionData(AlecRegion.alec_bedroom),
]

alec_entrances = [
    ConnectionData(AlecEntrance.forest_to_petshop, AlecRegion.pet_store,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(AlecEntrance.petshop_to_bedroom, AlecRegion.alec_bedroom, flag=RandomizationFlag.BUILDINGS),
]

yoba_regions = [
    RegionData(Region.secret_woods, (YobaEntrance.secret_woods_to_clearing,)),
    RegionData(YobaRegion.yoba_clearing),
]

yoba_entrances = [
    ConnectionData(YobaEntrance.secret_woods_to_clearing, YobaRegion.yoba_clearing, flag=RandomizationFlag.BUILDINGS),
]

juna_regions = [
    RegionData(Region.forest, (JunaEntrance.forest_to_juna_cave,)),
    RegionData(JunaRegion.juna_cave),
]

juna_entrances = [
    ConnectionData(JunaEntrance.forest_to_juna_cave, JunaRegion.juna_cave,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
]

ayeisha_regions = [
    RegionData(Region.bus_stop, (AyeishaEntrance.bus_stop_to_mail_van,)),
    RegionData(AyeishaRegion.mail_van),
]

ayeisha_entrances = [
    ConnectionData(AyeishaEntrance.bus_stop_to_mail_van, AyeishaRegion.mail_van,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
]

riley_regions = [
    RegionData(Region.town, (RileyEntrance.town_to_riley,)),
    RegionData(RileyRegion.riley_house),
]

riley_entrances = [
    ConnectionData(RileyEntrance.town_to_riley, RileyRegion.riley_house,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
]

sve_main_land_regions = [
    RegionData(Region.backwoods, (SVEEntrance.backwoods_to_grove,)),
    RegionData(SVERegion.enchanted_grove, (SVEEntrance.grove_to_outpost_warp, SVEEntrance.grove_to_wizard_warp,
                                           SVEEntrance.grove_to_farm_warp, SVEEntrance.grove_to_guild_warp, SVEEntrance.grove_to_junimo_warp,
                                           SVEEntrance.grove_to_spring_warp, SVEEntrance.grove_to_aurora_warp)),
    RegionData(SVERegion.grove_farm_warp, (SVEEntrance.farm_warp_to_farm,)),
    RegionData(SVERegion.grove_aurora_warp, (SVEEntrance.aurora_warp_to_aurora,)),
    RegionData(SVERegion.grove_guild_warp, (SVEEntrance.guild_warp_to_guild,)),
    RegionData(SVERegion.grove_junimo_warp, (SVEEntrance.junimo_warp_to_junimo,)),
    RegionData(SVERegion.grove_spring_warp, (SVEEntrance.spring_warp_to_spring,)),
    RegionData(SVERegion.grove_outpost_warp, (SVEEntrance.outpost_warp_to_outpost,)),
    RegionData(SVERegion.grove_wizard_warp, (SVEEntrance.wizard_warp_to_wizard,)),
    RegionData(SVERegion.galmoran_outpost, (SVEEntrance.outpost_to_badlands_entrance, SVEEntrance.use_alesia_shop, SVEEntrance.use_isaac_shop)),
    RegionData(SVERegion.badlands_entrance, (SVEEntrance.badlands_entrance_to_badlands,)),
    RegionData(SVERegion.crimson_badlands, (SVEEntrance.badlands_to_cave,)),
    RegionData(SVERegion.badlands_cave),
    RegionData(Region.bus_stop, (SVEEntrance.bus_stop_to_shed,)),
    RegionData(SVERegion.grandpas_shed, (SVEEntrance.grandpa_shed_to_interior, SVEEntrance.grandpa_shed_to_town)),
    RegionData(SVERegion.grandpas_shed_interior, (SVEEntrance.grandpa_interior_to_upstairs,)),
    RegionData(SVERegion.grandpas_shed_upstairs),
    RegionData(Region.forest,
               (SVEEntrance.forest_to_fairhaven, SVEEntrance.forest_to_west, SVEEntrance.forest_to_lost_woods,
                SVEEntrance.forest_to_bmv, SVEEntrance.forest_to_marnie_shed)),
    RegionData(SVERegion.marnies_shed),
    RegionData(SVERegion.fairhaven_farm),
    RegionData(Region.town, (SVEEntrance.town_to_bmv, SVEEntrance.town_to_jenkins, SVEEntrance.town_to_bridge, SVEEntrance.town_to_plot)),
    RegionData(SVERegion.blue_moon_vineyard, (SVEEntrance.bmv_to_sophia, SVEEntrance.bmv_to_beach)),
    RegionData(SVERegion.sophias_house),
    RegionData(SVERegion.jenkins_residence, (SVEEntrance.jenkins_to_cellar,)),
    RegionData(SVERegion.jenkins_cellar),
    RegionData(SVERegion.unclaimed_plot, (SVEEntrance.plot_to_bridge,)),
    RegionData(SVERegion.shearwater),
    RegionData(Region.museum, (SVEEntrance.museum_to_gunther_bedroom,)),
    RegionData(SVERegion.gunther_bedroom),
    RegionData(Region.fish_shop, (SVEEntrance.fish_shop_to_willy_bedroom,)),
    RegionData(SVERegion.willy_bedroom),
    RegionData(Region.mountain, (SVEEntrance.mountain_to_guild_summit,)),
    # These entrances are removed from the mountain region when SVE is enabled
    RegionData(Region.outside_adventure_guild, (Entrance.mountain_to_adventurer_guild, Entrance.mountain_to_the_mines), flag=MergeFlag.REMOVE_EXITS),
    RegionData(SVERegion.guild_summit, (SVEEntrance.guild_to_interior, SVEEntrance.guild_to_mines)),
    RegionData(Region.railroad, (SVEEntrance.to_susan_house, SVEEntrance.enter_summit, SVEEntrance.railroad_to_grampleton_station)),
    RegionData(SVERegion.grampleton_station, (SVEEntrance.grampleton_station_to_grampleton_suburbs,)),
    RegionData(SVERegion.grampleton_suburbs, (SVEEntrance.grampleton_suburbs_to_scarlett_house,)),
    RegionData(SVERegion.scarlett_house),
    RegionData(SVERegion.forest_west, (SVEEntrance.forest_west_to_spring, SVEEntrance.west_to_aurora, SVEEntrance.use_bear_shop,)),
    RegionData(SVERegion.aurora_vineyard, (SVEEntrance.to_aurora_basement,)),
    RegionData(SVERegion.aurora_vineyard_basement),
    RegionData(Region.secret_woods, (SVEEntrance.secret_woods_to_west,)),
    RegionData(SVERegion.bear_shop),
    RegionData(SVERegion.sprite_spring, (SVEEntrance.sprite_spring_to_cave,)),
    RegionData(SVERegion.sprite_spring_cave),
    RegionData(SVERegion.lost_woods, (SVEEntrance.lost_woods_to_junimo_woods,)),
    RegionData(SVERegion.junimo_woods, (SVEEntrance.use_purple_junimo,)),
    RegionData(SVERegion.purple_junimo_shop),
    RegionData(SVERegion.alesia_shop),
    RegionData(SVERegion.isaac_shop),
    RegionData(SVERegion.summit),
    RegionData(SVERegion.susans_house),
]

sve_ginger_island_regions = [
    RegionData(Region.wizard_basement, (SVEEntrance.wizard_to_fable_reef,)),

    RegionData(SVERegion.fable_reef, (SVEEntrance.fable_reef_to_guild,)),
    RegionData(SVERegion.first_slash_guild, (SVEEntrance.first_slash_guild_to_hallway,)),
    RegionData(SVERegion.first_slash_hallway, (SVEEntrance.first_slash_hallway_to_room,)),
    RegionData(SVERegion.first_slash_spare_room),
    RegionData(SVERegion.guild_summit, (SVEEntrance.summit_to_highlands,)),
    RegionData(SVERegion.highlands_outside, (SVEEntrance.highlands_to_lance, SVEEntrance.highlands_to_cave, SVEEntrance.highlands_to_pond), ),
    RegionData(SVERegion.highlands_pond),
    RegionData(SVERegion.highlands_cavern, (SVEEntrance.to_dwarf_prison,)),
    RegionData(SVERegion.dwarf_prison),
    RegionData(SVERegion.lances_house, (SVEEntrance.lance_to_ladder,)),
    RegionData(SVERegion.lances_ladder, (SVEEntrance.lance_ladder_to_highlands,)),
]

sve_main_land_connections = [
    ConnectionData(SVEEntrance.town_to_jenkins, SVERegion.jenkins_residence, flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEEntrance.jenkins_to_cellar, SVERegion.jenkins_cellar, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.forest_to_bmv, SVERegion.blue_moon_vineyard),
    ConnectionData(SVEEntrance.bmv_to_beach, Region.beach),
    ConnectionData(SVEEntrance.town_to_plot, SVERegion.unclaimed_plot),
    ConnectionData(SVEEntrance.town_to_bmv, SVERegion.blue_moon_vineyard),
    ConnectionData(SVEEntrance.town_to_bridge, SVERegion.shearwater),
    ConnectionData(SVEEntrance.plot_to_bridge, SVERegion.shearwater),
    ConnectionData(SVEEntrance.bus_stop_to_shed, SVERegion.grandpas_shed),
    ConnectionData(SVEEntrance.grandpa_shed_to_interior, SVERegion.grandpas_shed_interior,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEEntrance.grandpa_interior_to_upstairs, SVERegion.grandpas_shed_upstairs, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.grandpa_shed_to_town, Region.town),
    ConnectionData(SVEEntrance.bmv_to_sophia, SVERegion.sophias_house, flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEEntrance.summit_to_highlands, SVERegion.highlands_outside),
    ConnectionData(SVEEntrance.guild_to_interior, Region.adventurer_guild, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.backwoods_to_grove, SVERegion.enchanted_grove, flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEEntrance.grove_to_outpost_warp, SVERegion.grove_outpost_warp),
    ConnectionData(SVEEntrance.outpost_warp_to_outpost, SVERegion.galmoran_outpost, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.grove_to_wizard_warp, SVERegion.grove_wizard_warp),
    ConnectionData(SVEEntrance.wizard_warp_to_wizard, Region.wizard_basement, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.grove_to_aurora_warp, SVERegion.grove_aurora_warp),
    ConnectionData(SVEEntrance.aurora_warp_to_aurora, SVERegion.aurora_vineyard_basement, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.grove_to_farm_warp, SVERegion.grove_farm_warp),
    ConnectionData(SVEEntrance.to_aurora_basement, SVERegion.aurora_vineyard_basement, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.farm_warp_to_farm, Region.farm),
    ConnectionData(SVEEntrance.grove_to_guild_warp, SVERegion.grove_guild_warp),
    ConnectionData(SVEEntrance.guild_warp_to_guild, Region.adventurer_guild, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.grove_to_junimo_warp, SVERegion.grove_junimo_warp),
    ConnectionData(SVEEntrance.junimo_warp_to_junimo, SVERegion.junimo_woods, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.use_purple_junimo, SVERegion.purple_junimo_shop),
    ConnectionData(SVEEntrance.grove_to_spring_warp, SVERegion.grove_spring_warp),
    ConnectionData(SVEEntrance.spring_warp_to_spring, SVERegion.sprite_spring, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.outpost_to_badlands_entrance, SVERegion.badlands_entrance, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.badlands_entrance_to_badlands, SVERegion.crimson_badlands, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.badlands_to_cave, SVERegion.badlands_cave, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.guild_to_mines, Region.mines, flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(SVEEntrance.mountain_to_guild_summit, SVERegion.guild_summit),
    ConnectionData(SVEEntrance.forest_to_west, SVERegion.forest_west),
    ConnectionData(SVEEntrance.secret_woods_to_west, SVERegion.forest_west),
    ConnectionData(SVEEntrance.west_to_aurora, SVERegion.aurora_vineyard, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEEntrance.forest_to_lost_woods, SVERegion.lost_woods),
    ConnectionData(SVEEntrance.lost_woods_to_junimo_woods, SVERegion.junimo_woods),
    ConnectionData(SVEEntrance.forest_to_marnie_shed, SVERegion.marnies_shed, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEEntrance.forest_west_to_spring, SVERegion.sprite_spring, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.to_susan_house, SVERegion.susans_house, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.enter_summit, SVERegion.summit, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.forest_to_fairhaven, SVERegion.fairhaven_farm, flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(SVEEntrance.use_bear_shop, SVERegion.bear_shop),
    ConnectionData(SVEEntrance.use_purple_junimo, SVERegion.purple_junimo_shop),
    ConnectionData(SVEEntrance.use_alesia_shop, SVERegion.alesia_shop),
    ConnectionData(SVEEntrance.use_isaac_shop, SVERegion.isaac_shop),
    ConnectionData(SVEEntrance.railroad_to_grampleton_station, SVERegion.grampleton_station),
    ConnectionData(SVEEntrance.grampleton_station_to_grampleton_suburbs, SVERegion.grampleton_suburbs),
    ConnectionData(SVEEntrance.grampleton_suburbs_to_scarlett_house, SVERegion.scarlett_house, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.sprite_spring_to_cave, SVERegion.sprite_spring_cave, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.fish_shop_to_willy_bedroom, SVERegion.willy_bedroom, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.museum_to_gunther_bedroom, SVERegion.gunther_bedroom, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.highlands_to_pond, SVERegion.highlands_pond),
]

sve_ginger_island_connections = [
    ConnectionData(SVEEntrance.wizard_to_fable_reef, SVERegion.fable_reef, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.fable_reef_to_guild, SVERegion.first_slash_guild, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.highlands_to_lance, SVERegion.lances_house, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.lance_to_ladder, SVERegion.lances_ladder),
    ConnectionData(SVEEntrance.lance_ladder_to_highlands, SVERegion.highlands_outside, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.highlands_to_cave, SVERegion.highlands_cavern, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.to_dwarf_prison, SVERegion.dwarf_prison, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.first_slash_guild_to_hallway, SVERegion.first_slash_hallway, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.first_slash_hallway_to_room, SVERegion.first_slash_spare_room, flag=RandomizationFlag.BUILDINGS),
]

alecto_regions = [
    RegionData(Region.witch_hut, (AlectoEntrance.witch_hut_to_witch_attic,)),
    RegionData(AlectoRegion.witch_attic),
]

alecto_entrances = [
    ConnectionData(AlectoEntrance.witch_hut_to_witch_attic, AlectoRegion.witch_attic, flag=RandomizationFlag.BUILDINGS),
]

lacey_regions = [
    RegionData(Region.forest, (LaceyEntrance.forest_to_hat_house,)),
    RegionData(LaceyRegion.hat_house),
]

lacey_entrances = [
    ConnectionData(LaceyEntrance.forest_to_hat_house, LaceyRegion.hat_house, flag=RandomizationFlag.BUILDINGS),
]

boarding_house_regions = [
    RegionData(Region.bus_stop, (BoardingHouseEntrance.bus_stop_to_boarding_house_plateau,)),
    RegionData(BoardingHouseRegion.boarding_house_plateau, (BoardingHouseEntrance.boarding_house_plateau_to_boarding_house_first,
                                                            BoardingHouseEntrance.boarding_house_plateau_to_buffalo_ranch,
                                                            BoardingHouseEntrance.boarding_house_plateau_to_abandoned_mines_entrance)),
    RegionData(BoardingHouseRegion.boarding_house_first, (BoardingHouseEntrance.boarding_house_first_to_boarding_house_second,)),
    RegionData(BoardingHouseRegion.boarding_house_second),
    RegionData(BoardingHouseRegion.buffalo_ranch),
    RegionData(BoardingHouseRegion.abandoned_mines_entrance, (BoardingHouseEntrance.abandoned_mines_entrance_to_abandoned_mines_1a,
                                                              BoardingHouseEntrance.abandoned_mines_entrance_to_the_lost_valley)),
    RegionData(BoardingHouseRegion.abandoned_mines_1a, (BoardingHouseEntrance.abandoned_mines_1a_to_abandoned_mines_1b,)),
    RegionData(BoardingHouseRegion.abandoned_mines_1b, (BoardingHouseEntrance.abandoned_mines_1b_to_abandoned_mines_2a,)),
    RegionData(BoardingHouseRegion.abandoned_mines_2a, (BoardingHouseEntrance.abandoned_mines_2a_to_abandoned_mines_2b,)),
    RegionData(BoardingHouseRegion.abandoned_mines_2b, (BoardingHouseEntrance.abandoned_mines_2b_to_abandoned_mines_3,)),
    RegionData(BoardingHouseRegion.abandoned_mines_3, (BoardingHouseEntrance.abandoned_mines_3_to_abandoned_mines_4,)),
    RegionData(BoardingHouseRegion.abandoned_mines_4, (BoardingHouseEntrance.abandoned_mines_4_to_abandoned_mines_5,)),
    RegionData(BoardingHouseRegion.abandoned_mines_5, (BoardingHouseEntrance.abandoned_mines_5_to_the_lost_valley,)),
    RegionData(BoardingHouseRegion.the_lost_valley, (BoardingHouseEntrance.the_lost_valley_to_gregory_tent,
                                                     BoardingHouseEntrance.lost_valley_to_lost_valley_minecart,
                                                     BoardingHouseEntrance.the_lost_valley_to_lost_valley_ruins)),
    RegionData(BoardingHouseRegion.gregory_tent),
    RegionData(BoardingHouseRegion.lost_valley_ruins, (BoardingHouseEntrance.lost_valley_ruins_to_lost_valley_house_1,
                                                       BoardingHouseEntrance.lost_valley_ruins_to_lost_valley_house_2)),
    RegionData(BoardingHouseRegion.lost_valley_minecart),
    RegionData(BoardingHouseRegion.lost_valley_house_1),
    RegionData(BoardingHouseRegion.lost_valley_house_2),
]

boarding_house_entrances = [
    ConnectionData(BoardingHouseEntrance.bus_stop_to_boarding_house_plateau, BoardingHouseRegion.boarding_house_plateau),
    ConnectionData(BoardingHouseEntrance.boarding_house_plateau_to_boarding_house_first, BoardingHouseRegion.boarding_house_first,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(BoardingHouseEntrance.boarding_house_first_to_boarding_house_second, BoardingHouseRegion.boarding_house_second,
                   flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.boarding_house_plateau_to_buffalo_ranch, BoardingHouseRegion.buffalo_ranch,
                   flag=RandomizationFlag.BUILDINGS | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(BoardingHouseEntrance.boarding_house_plateau_to_abandoned_mines_entrance, BoardingHouseRegion.abandoned_mines_entrance,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(BoardingHouseEntrance.abandoned_mines_entrance_to_the_lost_valley, BoardingHouseRegion.lost_valley_minecart,
                   flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.abandoned_mines_entrance_to_abandoned_mines_1a, BoardingHouseRegion.abandoned_mines_1a,
                   flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.abandoned_mines_1a_to_abandoned_mines_1b, BoardingHouseRegion.abandoned_mines_1b, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.abandoned_mines_1b_to_abandoned_mines_2a, BoardingHouseRegion.abandoned_mines_2a, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.abandoned_mines_2a_to_abandoned_mines_2b, BoardingHouseRegion.abandoned_mines_2b, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.abandoned_mines_2b_to_abandoned_mines_3, BoardingHouseRegion.abandoned_mines_3, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.abandoned_mines_3_to_abandoned_mines_4, BoardingHouseRegion.abandoned_mines_4, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.abandoned_mines_4_to_abandoned_mines_5, BoardingHouseRegion.abandoned_mines_5, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.abandoned_mines_5_to_the_lost_valley, BoardingHouseRegion.the_lost_valley, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.the_lost_valley_to_gregory_tent, BoardingHouseRegion.gregory_tent, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.lost_valley_to_lost_valley_minecart, BoardingHouseRegion.lost_valley_minecart),
    ConnectionData(BoardingHouseEntrance.the_lost_valley_to_lost_valley_ruins, BoardingHouseRegion.lost_valley_ruins, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.lost_valley_ruins_to_lost_valley_house_1, BoardingHouseRegion.lost_valley_house_1, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.lost_valley_ruins_to_lost_valley_house_2, BoardingHouseRegion.lost_valley_house_2, flag=RandomizationFlag.BUILDINGS),
]

vanilla_connections_to_remove_by_content_pack: dict[str, tuple[str, ...]] = {
    ModNames.sve: (
        Entrance.mountain_to_the_mines,
        Entrance.mountain_to_adventurer_guild,
    )
}

region_data_by_content_pack = {
    ModNames.deepwoods: ModRegionsData(ModNames.deepwoods, deep_woods_regions, deep_woods_entrances),
    ModNames.eugene: ModRegionsData(ModNames.eugene, eugene_regions, eugene_entrances),
    ModNames.jasper: ModRegionsData(ModNames.jasper, jasper_regions, jasper_entrances),
    ModNames.alec: ModRegionsData(ModNames.alec, alec_regions, alec_entrances),
    ModNames.yoba: ModRegionsData(ModNames.yoba, yoba_regions, yoba_entrances),
    ModNames.juna: ModRegionsData(ModNames.juna, juna_regions, juna_entrances),
    ModNames.magic: ModRegionsData(ModNames.magic, magic_regions, magic_entrances),
    ModNames.ayeisha: ModRegionsData(ModNames.ayeisha, ayeisha_regions, ayeisha_entrances),
    ModNames.riley: ModRegionsData(ModNames.riley, riley_regions, riley_entrances),
    ModNames.sve: ModRegionsData(ModNames.sve, sve_main_land_regions, sve_main_land_connections),
    SVE_GINGER_ISLAND_PACK: ModRegionsData(SVE_GINGER_ISLAND_PACK, sve_ginger_island_regions, sve_ginger_island_connections),
    ModNames.alecto: ModRegionsData(ModNames.alecto, alecto_regions, alecto_entrances),
    ModNames.lacey: ModRegionsData(ModNames.lacey, lacey_regions, lacey_entrances),
    ModNames.boarding_house: ModRegionsData(ModNames.boarding_house, boarding_house_regions, boarding_house_entrances),
}
