from worlds.stardew_valley.strings.entrance_names import DeepWoodsEntrance, EugeneEntrance, \
    JasperEntrance, AlecEntrance, YobaEntrance, JunaEntrance
from worlds.stardew_valley.strings.region_names import Region, DeepWoodsRegion, EugeneRegion, JasperRegion, \
    AlecRegion, YobaRegion, JunaRegion
from ..region_classes import RegionData, ConnectionData, RandomizationFlag, ModRegionData
from .mod_data import ModNames

# Making this to reduce clutter from the regions file

# DeepWoods Data
deep_woods_regions = [
    RegionData(Region.farm, [DeepWoodsEntrance.use_woods_obelisk]),
    RegionData(Region.secret_woods, [DeepWoodsEntrance.secret_woods_to_deep_woods]),
    RegionData(DeepWoodsRegion.main_lichtung, [DeepWoodsEntrance.deep_woods_house,
                                               DeepWoodsEntrance.deep_woods_depth_10]),
    RegionData(DeepWoodsRegion.abandoned_home),
    RegionData(DeepWoodsRegion.floor_10, [DeepWoodsEntrance.deep_woods_depth_30]),
    RegionData(DeepWoodsRegion.floor_30, [DeepWoodsEntrance.deep_woods_depth_50]),
    RegionData(DeepWoodsRegion.floor_50, [DeepWoodsEntrance.deep_woods_depth_70]),
    RegionData(DeepWoodsRegion.floor_70, [DeepWoodsEntrance.deep_woods_depth_90]),
    RegionData(DeepWoodsRegion.floor_90, [DeepWoodsEntrance.deep_woods_depth_100]),
    RegionData(DeepWoodsRegion.floor_100)
]

deep_woods_entrances = [
    ConnectionData(DeepWoodsEntrance.use_woods_obelisk, DeepWoodsRegion.main_lichtung),
    ConnectionData(DeepWoodsEntrance.secret_woods_to_deep_woods, DeepWoodsRegion.main_lichtung),
    ConnectionData(DeepWoodsEntrance.deep_woods_house, DeepWoodsRegion.abandoned_home,
                   flag=RandomizationFlag.NON_PROGRESSION),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_10, DeepWoodsRegion.floor_10),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_30, DeepWoodsRegion.floor_30),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_50, DeepWoodsRegion.floor_50),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_70, DeepWoodsRegion.floor_70),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_90, DeepWoodsRegion.floor_90),
    ConnectionData(DeepWoodsEntrance.deep_woods_depth_100, DeepWoodsRegion.floor_100)
]

eugene_regions = [
    RegionData(Region.forest, [EugeneEntrance.forest_to_garden]),
    RegionData(EugeneRegion.eugene_garden, [EugeneEntrance.garden_to_bedroom]),
    RegionData(EugeneRegion.eugene_bedroom)
]

eugene_entrances = [
    ConnectionData(EugeneEntrance.forest_to_garden, EugeneRegion.eugene_garden, flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(EugeneEntrance.garden_to_bedroom, EugeneRegion.eugene_bedroom, flag=RandomizationFlag.BUILDINGS)
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
    ConnectionData(AlecEntrance.forest_to_petshop, AlecRegion.pet_store, flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA),
    ConnectionData(AlecEntrance.petshop_to_bedroom, AlecRegion.alec_bedroom, flag=RandomizationFlag.BUILDINGS)
]

yoba_regions = [
    RegionData(Region.secret_woods, [YobaEntrance.secret_woods_to_clearing]),
    RegionData(YobaRegion.yoba_clearing)
]

yoba_entrances = [
    ConnectionData(YobaEntrance.secret_woods_to_clearing, YobaRegion.yoba_clearing)
]

juna_regions = [
    RegionData(Region.forest, [JunaEntrance.forest_to_juna_cave]),
    RegionData(JunaRegion.juna_cave)
]

juna_entrances = [
    ConnectionData(JunaEntrance.forest_to_juna_cave, JunaRegion.juna_cave, flag=RandomizationFlag.NON_PROGRESSION | RandomizationFlag.LEAD_TO_OPEN_AREA)
]


ModDataList = {
    ModNames.deepwoods: ModRegionData(ModNames.deepwoods, deep_woods_regions, deep_woods_entrances),
    ModNames.eugene: ModRegionData(ModNames.eugene, eugene_regions, eugene_entrances),
    ModNames.jasper: ModRegionData(ModNames.jasper, jasper_regions, jasper_entrances),
    ModNames.alec: ModRegionData(ModNames.alec, alec_regions, alec_entrances),
    ModNames.yoba: ModRegionData(ModNames.yoba, yoba_regions, yoba_entrances),
    ModNames.juna: ModRegionData(ModNames.juna, juna_regions, juna_entrances)
}
