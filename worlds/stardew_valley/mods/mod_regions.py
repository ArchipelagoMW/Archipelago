from ..strings.entrance_names import DeepWoodsEntrance, EugeneEntrance, \
    JasperEntrance, AlecEntrance, YobaEntrance, JunaEntrance, MagicEntrance, AyeishaEntrance, RileyEntrance
from ..strings.region_names import Region, DeepWoodsRegion, EugeneRegion, JasperRegion, \
    AlecRegion, YobaRegion, JunaRegion, MagicRegion, AyeishaRegion, RileyRegion
from ..region_classes import RegionData, ConnectionData, RandomizationFlag, ModRegionData
from .mod_data import ModNames

deep_woods_regions = [
    RegionData(Region.farm, [DeepWoodsEntrance.use_woods_obelisk]),
    RegionData(DeepWoodsRegion.woods_obelisk_menu, [DeepWoodsEntrance.deep_woods_depth_1,
                                                    DeepWoodsEntrance.deep_woods_depth_10,
                                                    DeepWoodsEntrance.deep_woods_depth_20,
                                                    DeepWoodsEntrance.deep_woods_depth_30,
                                                    DeepWoodsEntrance.deep_woods_depth_40,
                                                    DeepWoodsEntrance.deep_woods_depth_50,
                                                    DeepWoodsEntrance.deep_woods_depth_60,
                                                    DeepWoodsEntrance.deep_woods_depth_70,
                                                    DeepWoodsEntrance.deep_woods_depth_80,
                                                    DeepWoodsEntrance.deep_woods_depth_90,
                                                    DeepWoodsEntrance.deep_woods_depth_100]),
    RegionData(Region.secret_woods, [DeepWoodsEntrance.secret_woods_to_deep_woods]),
    RegionData(DeepWoodsRegion.main_lichtung, [DeepWoodsEntrance.deep_woods_house]),
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
    RegionData(DeepWoodsRegion.floor_100)
]

deep_woods_entrances = [
    ConnectionData(DeepWoodsEntrance.use_woods_obelisk, DeepWoodsRegion.woods_obelisk_menu),
    ConnectionData(DeepWoodsEntrance.secret_woods_to_deep_woods, DeepWoodsRegion.main_lichtung),
    ConnectionData(DeepWoodsEntrance.deep_woods_house, DeepWoodsRegion.abandoned_home,
                   flag=RandomizationFlag.NON_PROGRESSION),
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
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_100, DeepWoodsRegion.floor_100)
]

eugene_regions = [
    RegionData(Region.forest, [EugeneEntrance.forest_to_garden]),
    RegionData(EugeneRegion.eugene_garden, [EugeneEntrance.garden_to_bedroom]),
    RegionData(EugeneRegion.eugene_bedroom)
]

eugene_entrances = [
    ConnectionData(EugeneEntrance.forest_to_garden, EugeneRegion.eugene_garden,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(EugeneEntrance.garden_to_bedroom, EugeneRegion.eugene_bedroom, flag=RandomizationFlag.BUILDINGS)
]

magic_regions = [
    RegionData(Region.pierre_store, [MagicEntrance.store_to_altar]),
    RegionData(MagicRegion.altar)
]

magic_entrances = [
    ConnectionData(MagicEntrance.store_to_altar, MagicRegion.altar, flag=RandomizationFlag.NOT_RANDOMIZED)
]

jasper_regions = [
    RegionData(Region.museum, [JasperEntrance.museum_to_bedroom]),
    RegionData(JasperRegion.jasper_bedroom)
]

jasper_entrances = [
    ConnectionData(JasperEntrance.museum_to_bedroom, JasperRegion.jasper_bedroom, flag=RandomizationFlag.BUILDINGS)
]
alec_regions = [
    RegionData(Region.forest, [AlecEntrance.forest_to_petshop]),
    RegionData(AlecRegion.pet_store, [AlecEntrance.petshop_to_bedroom]),
    RegionData(AlecRegion.alec_bedroom)
]

alec_entrances = [
    ConnectionData(AlecEntrance.forest_to_petshop, AlecRegion.pet_store,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(AlecEntrance.petshop_to_bedroom, AlecRegion.alec_bedroom, flag=RandomizationFlag.BUILDINGS)
]

yoba_regions = [
    RegionData(Region.secret_woods, [YobaEntrance.secret_woods_to_clearing]),
    RegionData(YobaRegion.yoba_clearing)
]

yoba_entrances = [
    ConnectionData(YobaEntrance.secret_woods_to_clearing, YobaRegion.yoba_clearing, flag=RandomizationFlag.BUILDINGS)
]

juna_regions = [
    RegionData(Region.forest, [JunaEntrance.forest_to_juna_cave]),
    RegionData(JunaRegion.juna_cave)
]

juna_entrances = [
    ConnectionData(JunaEntrance.forest_to_juna_cave, JunaRegion.juna_cave,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA)
]

ayeisha_regions = [
    RegionData(Region.bus_stop, [AyeishaEntrance.bus_stop_to_mail_van]),
    RegionData(AyeishaRegion.mail_van)
]

ayeisha_entrances = [
    ConnectionData(AyeishaEntrance.bus_stop_to_mail_van, AyeishaRegion.mail_van,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA)
]

riley_regions = [
    RegionData(Region.town, [RileyEntrance.town_to_riley]),
    RegionData(RileyRegion.riley_house)
]

riley_entrances = [
    ConnectionData(RileyEntrance.town_to_riley, RileyRegion.riley_house,
                   flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA)
]

ModDataList = {
    ModNames.deepwoods: ModRegionData(ModNames.deepwoods, deep_woods_regions, deep_woods_entrances),
    ModNames.eugene: ModRegionData(ModNames.eugene, eugene_regions, eugene_entrances),
    ModNames.jasper: ModRegionData(ModNames.jasper, jasper_regions, jasper_entrances),
    ModNames.alec: ModRegionData(ModNames.alec, alec_regions, alec_entrances),
    ModNames.yoba: ModRegionData(ModNames.yoba, yoba_regions, yoba_entrances),
    ModNames.juna: ModRegionData(ModNames.juna, juna_regions, juna_entrances),
    ModNames.magic: ModRegionData(ModNames.magic, magic_regions, magic_entrances),
    ModNames.ayeisha: ModRegionData(ModNames.ayeisha, ayeisha_regions, ayeisha_entrances),
    ModNames.riley: ModRegionData(ModNames.riley, riley_regions, riley_entrances),
}
