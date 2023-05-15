from dataclasses import dataclass, field
from worlds.stardew_valley.data.entrance_data import DeepWoodsEntrance, EugeneEntrance, \
    JasperEntrance, AlecEntrance, YobaEntrance, JunaEntrance
from worlds.stardew_valley.data.region_data import SVRegion, DeepWoodsRegion, EugeneRegion, JasperRegion, \
    AlecRegion, YobaRegion, JunaRegion
from worlds.stardew_valley.mods.mod_data import ModNames
from typing import List, Dict


# Making this to reduce clutter from the regions file

# DeepWoods Data
deep_woods_regions = {
    SVRegion.farm: [DeepWoodsEntrance.use_woods_obelisk],
    SVRegion.secret_woods: [DeepWoodsEntrance.secret_woods_to_deep_woods],
    DeepWoodsRegion.main_lichtung: [DeepWoodsEntrance.deep_woods_house,
                                    DeepWoodsEntrance.deep_woods_depth_10],
    DeepWoodsRegion.abandoned_home: [],
    DeepWoodsRegion.floor_10: [DeepWoodsEntrance.deep_woods_depth_30],
    DeepWoodsRegion.floor_30: [DeepWoodsEntrance.deep_woods_depth_50],
    DeepWoodsRegion.floor_50: [DeepWoodsEntrance.deep_woods_depth_70],
    DeepWoodsRegion.floor_70: [DeepWoodsEntrance.deep_woods_depth_90],
    DeepWoodsRegion.floor_90: [DeepWoodsEntrance.deep_woods_depth_100],
    DeepWoodsRegion.floor_100: []
}

mandatory_deep_woods_entrances = {
    DeepWoodsEntrance.use_woods_obelisk: DeepWoodsRegion.main_lichtung,
    DeepWoodsEntrance.secret_woods_to_deep_woods: DeepWoodsRegion.main_lichtung,
    DeepWoodsEntrance.deep_woods_house: DeepWoodsRegion.abandoned_home,
    DeepWoodsEntrance.deep_woods_depth_10: DeepWoodsRegion.floor_10,
    DeepWoodsEntrance.deep_woods_depth_30: DeepWoodsRegion.floor_30,
    DeepWoodsEntrance.deep_woods_depth_50: DeepWoodsRegion.floor_50,
    DeepWoodsEntrance.deep_woods_depth_70: DeepWoodsRegion.floor_70,
    DeepWoodsEntrance.deep_woods_depth_90: DeepWoodsRegion.floor_90,
    DeepWoodsEntrance.deep_woods_depth_100: DeepWoodsRegion.floor_100
}

deep_woods_flags = {
    DeepWoodsEntrance.use_woods_obelisk: "EVERYTHING",
    DeepWoodsEntrance.secret_woods_to_deep_woods: "EVERYTHING",
    DeepWoodsEntrance.deep_woods_house: "NON_PROGRESSION",
    DeepWoodsEntrance.deep_woods_depth_10: "EVERYTHING",
    DeepWoodsEntrance.deep_woods_depth_30: "EVERYTHING",
    DeepWoodsEntrance.deep_woods_depth_50: "EVERYTHING",
    DeepWoodsEntrance.deep_woods_depth_70: "EVERYTHING",
    DeepWoodsEntrance.deep_woods_depth_90: "EVERYTHING",
    DeepWoodsEntrance.deep_woods_depth_100: "EVERYTHING"
}

eugene_regions = {
    SVRegion.forest: [EugeneEntrance.forest_to_garden],
    EugeneRegion.eugene_garden: [EugeneEntrance.garden_to_bedroom],
    EugeneRegion.eugene_bedroom: []
}

eugene_entrances = {
    EugeneEntrance.forest_to_garden: EugeneRegion.eugene_garden,
    EugeneEntrance.garden_to_bedroom: EugeneRegion.eugene_bedroom
}

eugene_flags = {
    EugeneEntrance.forest_to_garden: "NON_PROGRESSION",
    EugeneEntrance.garden_to_bedroom: "NON_PROGRESSION"
}

jasper_regions = {
    SVRegion.museum: [JasperEntrance.museum_to_bedroom],
    JasperRegion.jasper_bedroom: []
}

jasper_entrances = {
    JasperEntrance.museum_to_bedroom: JasperRegion.jasper_bedroom
}

jasper_flags = {
    JasperEntrance.museum_to_bedroom: "NON_PROGRESSION"
}

alec_regions = {
    SVRegion.forest: [AlecEntrance.forest_to_petshop],
    AlecRegion.pet_store: [AlecEntrance.petshop_to_bedroom],
    AlecRegion.alec_bedroom: []
}

alec_entrances = {
    AlecEntrance.forest_to_petshop: AlecRegion.pet_store,
    AlecEntrance.petshop_to_bedroom: AlecRegion.alec_bedroom
}

alec_flags = {
    AlecEntrance.forest_to_petshop: "NON_PROGRESSION",
    AlecEntrance.petshop_to_bedroom: "NON_PROGRESSION"
}

yoba_regions = {
    SVRegion.secret_woods: [YobaEntrance.secret_woods_to_clearing],
    YobaRegion.yoba_clearing: []
}

yoba_entrances = {
    YobaEntrance.secret_woods_to_clearing: YobaRegion.yoba_clearing
}

yoba_flags = {
    YobaEntrance.secret_woods_to_clearing: "EVERYTHING"
}

juna_regions = {
    SVRegion.forest: [JunaEntrance.forest_to_juna_cave],
    JunaRegion.juna_cave: []
}

juna_entrances = {
    JunaEntrance.forest_to_juna_cave: JunaRegion.juna_cave
}

juna_flags = {
    JunaEntrance.forest_to_juna_cave: "NON_PROGRESSION"
}
# Dictionary which has:
# - The name of the mod as key
# - Dictionaries containing the regions, connections, and the vanilla connections to remove as the value
# This is compacted to be ultimately used when constructing regions, to mod the vanilla region/connection data
# before it's properly used for logic.


@dataclass(frozen=True)
class ModData:
    mod_name: str
    regions: Dict[str, List[str]]
    connections: Dict[str, str]
    region_remover: Dict[str, List[str]]
    connection_remover: Dict[str, str]
    flags: Dict[str, str]


@dataclass(frozen=True)
class RegionRemoverData:
    name: str
    exits: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ConnectionRemoverData:
    name: str
    destination: str


ModDataList = [
    ModData(ModNames.deepwoods, deep_woods_regions, mandatory_deep_woods_entrances, {}, {}, deep_woods_flags),
    ModData(ModNames.eugene, eugene_regions, eugene_entrances, {}, {}, eugene_flags),
    ModData(ModNames.jasper, jasper_regions, jasper_entrances, {}, {}, jasper_flags),
    ModData(ModNames.alec, alec_regions, alec_entrances, {}, {}, alec_flags),
    ModData(ModNames.yoba, yoba_regions, yoba_entrances, {}, {}, yoba_flags),
    ModData(ModNames.juna, juna_regions, juna_entrances, {}, {}, juna_flags)
]
