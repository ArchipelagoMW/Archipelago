from ..content.mods.sve import SVE_GINGER_ISLAND_PACK
from ..regions.model import (ConnectionData, MergeFlag, ModRegionsData,
                             RandomizationFlag, RegionData, GroupFlag)
from ..strings.entrance_names import (AlecEntrance, AlectoEntrance,
                                      AyeishaEntrance, BoardingHouseEntrance,
                                      DeepWoodsEntrance, Entrance,
                                      EugeneEntrance, JasperEntrance,
                                      JunaEntrance, LaceyEntrance,
                                      LogicEntrance, MagicEntrance,
                                      RileyEntrance, SVEEntrance, YobaEntrance)
from ..strings.region_names import (AlecRegion, AlectoRegion, AyeishaRegion,
                                    BoardingHouseRegion, DeepWoodsRegion,
                                    EugeneRegion, JasperRegion, JunaRegion,
                                    LaceyRegion, LogicRegion, MagicRegion,
                                    Region, RileyRegion, SVERegion, YobaRegion)
from .mod_data import ModNames

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
    ConnectionData(
        EugeneEntrance.forest_to_garden,
        EugeneRegion.eugene_garden,
        flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_OUT,
    ),
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
    ConnectionData(
        AlecEntrance.forest_to_petshop,
        AlecRegion.pet_store,
        flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_IN,
    ),
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
    ConnectionData(
        JunaEntrance.forest_to_juna_cave,
        JunaRegion.juna_cave,
        flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_IN,
    )
]

ayeisha_regions = [
    RegionData(Region.bus_stop, (AyeishaEntrance.bus_stop_to_mail_van,)),
    RegionData(AyeishaRegion.mail_van),
]

ayeisha_entrances = [
    ConnectionData(
        AyeishaEntrance.bus_stop_to_mail_van,
        AyeishaRegion.mail_van,
        flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_IN,
    )
]

riley_regions = [
    RegionData(Region.town, (RileyEntrance.town_to_riley,)),
    RegionData(RileyRegion.riley_house),
]

riley_entrances = [
    ConnectionData(
        RileyEntrance.town_to_riley,
        RileyRegion.riley_house,
        flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_IN,
    )
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
    ConnectionData(
        SVEEntrance.town_to_jenkins,
        SVERegion.jenkins_residence,
        flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(SVEEntrance.jenkins_to_cellar, SVERegion.jenkins_cellar, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(SVEEntrance.forest_to_bmv, SVERegion.blue_moon_vineyard),
    ConnectionData(SVEEntrance.bmv_to_beach, Region.beach),
    ConnectionData(SVEEntrance.town_to_plot, SVERegion.unclaimed_plot),
    ConnectionData(SVEEntrance.town_to_bmv, SVERegion.blue_moon_vineyard),
    ConnectionData(SVEEntrance.town_to_bridge, SVERegion.shearwater),
    ConnectionData(SVEEntrance.plot_to_bridge, SVERegion.shearwater),
    ConnectionData(SVEEntrance.bus_stop_to_shed, SVERegion.grandpas_shed),
    ConnectionData(
        SVEEntrance.grandpa_shed_to_interior,
        SVERegion.grandpas_shed_interior,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_IN,
    ),
    ConnectionData(
        SVEEntrance.grandpa_interior_to_upstairs, SVERegion.grandpas_shed_upstairs, flag=RandomizationFlag.BUILDINGS
    ),
    ConnectionData(SVEEntrance.grandpa_shed_to_town, Region.town),
    ConnectionData(
        SVEEntrance.bmv_to_sophia,
        SVERegion.sophias_house,
        flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(SVEEntrance.summit_to_highlands, SVERegion.highlands_outside),
    ConnectionData(SVEEntrance.guild_to_interior, Region.adventurer_guild, flag=RandomizationFlag.BUILDINGS),
    ConnectionData(
        SVEEntrance.backwoods_to_grove,
        SVERegion.enchanted_grove,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_OUT,
    ),
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
    ConnectionData(
        SVEEntrance.guild_to_mines, Region.mines, flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_IN
    ),
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
                   flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_IN),
    ConnectionData(BoardingHouseEntrance.boarding_house_first_to_boarding_house_second, BoardingHouseRegion.boarding_house_second,
                   flag=RandomizationFlag.BUILDINGS),
    ConnectionData(BoardingHouseEntrance.boarding_house_plateau_to_buffalo_ranch, BoardingHouseRegion.buffalo_ranch,
                   flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN),
    ConnectionData(BoardingHouseEntrance.boarding_house_plateau_to_abandoned_mines_entrance, BoardingHouseRegion.abandoned_mines_entrance,
                   flag=RandomizationFlag.NON_PROGRESSION, group=GroupFlag.OUT_TO_IN),
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

ginger_island_regions = [
    RegionData(Region.mountain, (Entrance.mountain_to_leo_treehouse,)),
    RegionData(Region.wizard_tower, (Entrance.use_island_obelisk,)),
    RegionData(Region.fish_shop, (Entrance.fish_shop_to_boat_tunnel,)),
    RegionData(
        Region.mines_floor_120,
        (Entrance.dig_to_dangerous_mines_20, Entrance.dig_to_dangerous_mines_60, Entrance.dig_to_dangerous_mines_100),
    ),
    RegionData(Region.skull_cavern_200, (Entrance.enter_dangerous_skull_cavern,)),
    RegionData(Region.leo_treehouse, (Entrance.leo_treehouse_to_mountain,)),
    RegionData(Region.boat_tunnel, (Entrance.boat_tunnel_to_fish_shop, Entrance.boat_to_ginger_island)),
    RegionData(Region.dangerous_skull_cavern),
    RegionData(
        Region.island_south,
        (
            Entrance.boat_from_ginger_island,
            Entrance.island_south_to_west,
            Entrance.island_south_to_north,
            Entrance.island_south_to_east,
            Entrance.island_south_to_southeast,
            Entrance.use_island_resort,
            Entrance.parrot_express_docks_to_volcano,
            Entrance.parrot_express_docks_to_dig_site,
            Entrance.parrot_express_docks_to_jungle,
        ),
    ),
    RegionData(Region.island_resort),
    RegionData(
        Region.island_west,
        (
            Entrance.island_west_to_south,
            Entrance.island_west_to_island_farmhouse,
            Entrance.island_west_to_gourmand_cave,
            Entrance.island_west_to_crystals_cave,
            Entrance.island_west_to_shipwreck,
            Entrance.island_west_to_qi_walnut_room,
            Entrance.use_farm_obelisk,
            Entrance.parrot_express_jungle_to_docks,
            Entrance.parrot_express_jungle_to_dig_site,
            Entrance.parrot_express_jungle_to_volcano,
            LogicEntrance.grow_spring_crops_on_island,
            LogicEntrance.grow_summer_crops_on_island,
            LogicEntrance.grow_fall_crops_on_island,
            LogicEntrance.grow_winter_crops_on_island,
            LogicEntrance.grow_indoor_crops_on_island,
        ),
    ),
    RegionData(
        Region.island_east,
        (Entrance.island_east_to_south, Entrance.island_east_to_leo_hut, Entrance.island_east_to_island_shrine),
    ),
    RegionData(Region.island_shrine, (Entrance.island_shrine_to_island_east,)),
    RegionData(
        Region.island_south_east, (Entrance.island_southeast_to_south, Entrance.island_southeast_to_pirate_cove)
    ),
    RegionData(
        Region.island_north,
        (
            Entrance.island_north_to_south,
            Entrance.talk_to_island_trader,
            Entrance.island_north_to_field_office,
            Entrance.island_north_to_dig_site,
            Entrance.island_north_to_volcano,
            Entrance.parrot_express_volcano_to_dig_site,
            Entrance.parrot_express_volcano_to_jungle,
            Entrance.parrot_express_volcano_to_docks,
        ),
    ),
    RegionData(
        Region.volcano,
        (Entrance.volcano_to_island_north, Entrance.climb_to_volcano_5, Entrance.volcano_to_secret_beach),
    ),
    RegionData(Region.volcano_secret_beach, (Entrance.secret_beach_to_volcano,)),
    RegionData(Region.volcano_floor_5, (Entrance.talk_to_volcano_dwarf, Entrance.climb_to_volcano_10)),
    RegionData(Region.volcano_dwarf_shop),
    RegionData(Region.volcano_floor_10),
    RegionData(Region.island_trader),
    RegionData(Region.island_farmhouse, (Entrance.island_farmhouse_to_island_west, LogicEntrance.island_cooking)),
    RegionData(Region.gourmand_frog_cave, (Entrance.gourmand_cave_to_island_west,)),
    RegionData(Region.colored_crystals_cave, (Entrance.crystals_cave_to_island_west,)),
    RegionData(Region.shipwreck, (Entrance.shipwreck_to_island_west,)),
    RegionData(Region.qi_walnut_room, (Entrance.qi_walnut_room_to_island_west,)),
    RegionData(Region.leo_hut, (Entrance.leo_hut_to_island_east,)),
    RegionData(Region.pirate_cove, (Entrance.pirate_cove_to_island_southeast,)),
    RegionData(Region.field_office, (Entrance.field_office_to_island_north,)),
    RegionData(
        Region.dig_site,
        (
            Entrance.dig_site_to_island_north,
            Entrance.dig_site_to_professor_snail_cave,
            Entrance.parrot_express_dig_site_to_volcano,
            Entrance.parrot_express_dig_site_to_docks,
            Entrance.parrot_express_dig_site_to_jungle,
        ),
    ),
    RegionData(Region.professor_snail_cave, (Entrance.professor_snail_cave_to_dig_site,)),
    RegionData(Region.dangerous_mines_20),
    RegionData(Region.dangerous_mines_60),
    RegionData(Region.dangerous_mines_100),
]


ginger_island_connections = [
    ConnectionData(Entrance.use_island_obelisk, Region.island_south),
    ConnectionData(
        Entrance.use_farm_obelisk,
        Region.farm,
        flag=RandomizationFlag.TRANSITION
        | RandomizationFlag.ENDGAME
        | RandomizationFlag.IS_ONE_WAY
           , group=GroupFlag.OUT_TO_OUT
    ),
    ConnectionData(
        Entrance.mountain_to_leo_treehouse,
        Region.leo_treehouse,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.leo_treehouse_to_mountain,
        Region.mountain,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.fish_shop_to_boat_tunnel,
        Region.boat_tunnel,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_IN,
    ),
    ConnectionData(
        Entrance.boat_tunnel_to_fish_shop,
        Region.fish_shop,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_IN,
    ),
    ConnectionData(
        Entrance.boat_to_ginger_island,
        Region.island_south,
        flag=RandomizationFlag.TRANSITION, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.boat_from_ginger_island,
        Region.boat_tunnel,
        flag=RandomizationFlag.TRANSITION, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(Entrance.enter_dangerous_skull_cavern, Region.dangerous_skull_cavern),
    ConnectionData(Entrance.dig_to_dangerous_mines_20, Region.dangerous_mines_20),
    ConnectionData(Entrance.dig_to_dangerous_mines_60, Region.dangerous_mines_60),
    ConnectionData(Entrance.dig_to_dangerous_mines_100, Region.dangerous_mines_100),
    ConnectionData(
        Entrance.island_south_to_west,
        Region.island_west,
        flag=RandomizationFlag.OVERWORLD, group=GroupFlag.OUT_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_west_to_south,
        Region.island_south,
        flag=RandomizationFlag.OVERWORLD, group=GroupFlag.OUT_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_south_to_north,
        Region.island_north,
        flag=RandomizationFlag.OVERWORLD, group=GroupFlag.OUT_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_north_to_south,
        Region.island_south,
        flag=RandomizationFlag.OVERWORLD, group=GroupFlag.OUT_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_south_to_east,
        Region.island_east,
        flag=RandomizationFlag.OVERWORLD, group=GroupFlag.OUT_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_east_to_south,
        Region.island_south,
        flag=RandomizationFlag.OVERWORLD, group=GroupFlag.OUT_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_south_to_southeast,
        Region.island_south_east,
        flag=RandomizationFlag.OVERWORLD, group=GroupFlag.OUT_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_southeast_to_south,
        Region.island_south,
        flag=RandomizationFlag.OVERWORLD, group=GroupFlag.OUT_TO_OUT,
    ),
    ConnectionData(Entrance.use_island_resort, Region.island_resort),
    ConnectionData(
        Entrance.island_west_to_island_farmhouse,
        Region.island_farmhouse,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.island_farmhouse_to_island_west,
        Region.island_west,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_west_to_gourmand_cave,
        Region.gourmand_frog_cave,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.gourmand_cave_to_island_west,
        Region.island_west,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_west_to_crystals_cave,
        Region.colored_crystals_cave,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.crystals_cave_to_island_west,
        Region.island_west,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_west_to_shipwreck,
        Region.shipwreck,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.shipwreck_to_island_west,
        Region.island_west,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_west_to_qi_walnut_room,
        Region.qi_walnut_room,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.qi_walnut_room_to_island_west,
        Region.island_west,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_east_to_leo_hut, Region.leo_hut, flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN
    ),
    ConnectionData(
        Entrance.leo_hut_to_island_east,
        Region.island_east,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_east_to_island_shrine,
        Region.island_shrine,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.island_shrine_to_island_east,
        Region.island_east,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_southeast_to_pirate_cove,
        Region.pirate_cove,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.pirate_cove_to_island_southeast,
        Region.island_south_east,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_north_to_field_office,
        Region.field_office,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.field_office_to_island_north,
        Region.island_north,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(Entrance.island_north_to_dig_site, Region.dig_site),
    ConnectionData(Entrance.dig_site_to_island_north, Region.island_north),
    ConnectionData(
        Entrance.dig_site_to_professor_snail_cave,
        Region.professor_snail_cave,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN,
    ),
    ConnectionData(
        Entrance.professor_snail_cave_to_dig_site,
        Region.dig_site,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.island_north_to_volcano, Region.volcano, flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN
    ),
    ConnectionData(
        Entrance.volcano_to_island_north,
        Region.island_north,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.volcano_to_secret_beach,
        Region.volcano_secret_beach,
        flag=RandomizationFlag.BUILDINGS, group=GroupFlag.IN_TO_OUT,
    ),
    ConnectionData(
        Entrance.secret_beach_to_volcano, Region.volcano, flag=RandomizationFlag.BUILDINGS, group=GroupFlag.OUT_TO_IN
    ),
    ConnectionData(Entrance.talk_to_island_trader, Region.island_trader),
    ConnectionData(Entrance.climb_to_volcano_5, Region.volcano_floor_5),
    ConnectionData(Entrance.talk_to_volcano_dwarf, Region.volcano_dwarf_shop),
    ConnectionData(Entrance.climb_to_volcano_10, Region.volcano_floor_10),
    ConnectionData(Entrance.parrot_express_jungle_to_docks, Region.island_south),
    ConnectionData(Entrance.parrot_express_dig_site_to_docks, Region.island_south),
    ConnectionData(Entrance.parrot_express_volcano_to_docks, Region.island_south),
    ConnectionData(Entrance.parrot_express_volcano_to_jungle, Region.island_west),
    ConnectionData(Entrance.parrot_express_docks_to_jungle, Region.island_west),
    ConnectionData(Entrance.parrot_express_dig_site_to_jungle, Region.island_west),
    ConnectionData(Entrance.parrot_express_docks_to_dig_site, Region.dig_site),
    ConnectionData(Entrance.parrot_express_volcano_to_dig_site, Region.dig_site),
    ConnectionData(Entrance.parrot_express_jungle_to_dig_site, Region.dig_site),
    ConnectionData(Entrance.parrot_express_dig_site_to_volcano, Region.island_north),
    ConnectionData(Entrance.parrot_express_docks_to_volcano, Region.island_north),
    ConnectionData(Entrance.parrot_express_jungle_to_volcano, Region.island_north),
    ConnectionData(LogicEntrance.grow_spring_crops_on_island, LogicRegion.spring_farming),
    ConnectionData(LogicEntrance.grow_summer_crops_on_island, LogicRegion.summer_farming),
    ConnectionData(LogicEntrance.grow_fall_crops_on_island, LogicRegion.fall_farming),
    ConnectionData(LogicEntrance.grow_winter_crops_on_island, LogicRegion.winter_farming),
    ConnectionData(LogicEntrance.grow_indoor_crops_on_island, LogicRegion.indoor_farming),
    ConnectionData(LogicEntrance.island_cooking, LogicRegion.kitchen),
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
    ModNames.ginger_island: ModRegionsData(ModNames.ginger_island, ginger_island_regions, ginger_island_connections),
}
