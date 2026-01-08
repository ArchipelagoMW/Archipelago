""" data for the connections in area rando """

from .area_rando_types import AreaDoor, DoorPairs


area_doors_unpackable: tuple[AreaDoor, ...] = (
    AreaDoor('1c678', '5BBB00056E06060000800000', 'Early', 'CraterR', 0),
    AreaDoor('1c7a4', '2CBA00040106000000800000', 'Early', 'SunkenNestL', 0),
    AreaDoor('1caf8', 'C2970004115601050080CCA9', 'Early', 'RuinedConcourseBL', 1),
    AreaDoor('1cbc4', 'C29700051E0601000080B6A9', 'Early', 'RuinedConcourseTR', 1),
    AreaDoor('1a1e4', '2FA300013E06030000800000', 'Early', 'CausewayR', 1),
    AreaDoor('1c8c4', '578800052E06020000800000', 'Early', 'SporeFieldTR', 1),
    AreaDoor('1a2ec', '578800053E4603040080E4A6', 'Early', 'SporeFieldBR', 1),
    AreaDoor('1ca74', '0F8500057E26070200800000', 'SandLand', 'OceanShoreR', 0),
    AreaDoor('1c15c', '73CC00050E26000200800000', 'SandLand', 'EleToTurbidPassageR', 2),
    AreaDoor('1c66c', '879F00040116000100800000', 'SandLand', 'PileAnchorL', 0),
    AreaDoor('1a130', '19EC00000206000000800000', 'PirateLab', 'ExcavationSiteL', 1),
    AreaDoor('1bed4', 'B7E100050E16000100800000', 'PirateLab', 'WestCorridorR', 3),
    AreaDoor('197c4', 'CD8A00051E06010000800000', 'PirateLab', 'FoyerR', 3),
    AreaDoor('1c900', 'EB9E00040136000300800000', 'PirateLab', 'ConstructionSiteL', 1),
    AreaDoor('194b8', '3CBF00056E06060000800000', 'PirateLab', 'AlluringCenoteR', 3),
    AreaDoor('1a454', '71A000040106000000800000', 'ServiceSector', 'FieldAccessL', 1),
    AreaDoor('1a0f4', 'B89B00051E06010000800000', 'ServiceSector', 'TransferStationR', 1),
    AreaDoor('1c8f4', '3A8100052E06020000800000', 'ServiceSector', 'CellarR', 1),
    AreaDoor('1c864', 'CC9300040126000200800000', 'ServiceSector', 'SubbasementFissureL', 1),
    AreaDoor('1c6e4', 'C78100040126000200800000', 'SkyWorld', 'WestTerminalAccessL', 0),
    AreaDoor('1a4f0', '93A200040146000400800000', 'SkyWorld', 'MezzanineConcourseL', 1),
    AreaDoor('19788', '598B00044166040600800000', 'SkyWorld', 'VulnarCanyonL', 3),
    AreaDoor('195d8', '9F8B00012E06020000800000', 'SkyWorld', 'CanyonPassageR', 3),
    AreaDoor('1c2f4', 'BAED00040136000300800000', 'SkyWorld', 'ElevatorToCondenserL', 2),
    AreaDoor('1bf4c', '8B9000040216000120010000', 'SpacePort', 'LoadingDockSecurityAreaL', 3),
    AreaDoor('1cb7c', '36CD00040126000200800000', 'LifeTemple', 'ElevatorToWellspringL', 2),
    AreaDoor('1965c', 'E58B00000126000200800000', 'LifeTemple', 'NorakBrookL', 3),
    AreaDoor('1a0b8', '6F8900051E06010000800000', 'LifeTemple', 'NorakPerimeterTR', 3),
    AreaDoor('1bad8', '6F890004012600020080ACA7', 'LifeTemple', 'NorakPerimeterBL', 3),
    AreaDoor('1c87c', 'A9A100040106000000800000', 'FireHive', 'VulnarDepthsElevatorEL', 1),
    AreaDoor('1c888', 'A9A100050E06000000800000', 'FireHive', 'VulnarDepthsElevatorER', 1),
    AreaDoor('1bd84', 'E5D500040146000400800000', 'FireHive', 'HiveBurrowL', 2),
    AreaDoor('1c4b0', '84F300040116000100800000', 'FireHive', 'SequesteredInfernoL', 2),
    AreaDoor('1cb04', '89CB00051E06010000800000', 'FireHive', 'CollapsedPassageR', 2),
    AreaDoor('1c2e8', 'A0BE00040106000000800000', 'Geothermal', 'MagmaPumpL', 2),
    AreaDoor('1c414', 'B0F100051E160101008020A6', 'Geothermal', 'ReservoirMaintenanceTunnelR', 2),
    AreaDoor('1c4c8', '0FF300052E06020000800000', 'Geothermal', 'IntakePumpR', 2),
    AreaDoor('1cbac', 'F09C00055E06050000800000', 'Geothermal', 'ThermalReservoir1R', 2),
    AreaDoor('1c1b0', 'F4CF00043106030000800000', 'Geothermal', 'GeneratorAccessTunnelL', 2),
    AreaDoor('1c0fc', '67EF00050E06000000800000', 'DrayLand', 'ElevatorToMagmaLakeR', 2),
    AreaDoor('1c2b8', 'E99700050E06000000800000', 'DrayLand', 'MagmaPumpAccessR', 2),
    AreaDoor('1c174', 'D7CB00040116000100800000', 'Verdite', 'FieryGalleryL', 2),
    AreaDoor('1c12c', '2FEE00040116000100800000', 'Verdite', 'RagingPitL', 2),
    AreaDoor('1c108', '1BD000051E06010000800000', 'Verdite', 'HollowChamberR', 2),
    AreaDoor('1c8a0', 'CBA300051E06010000800000', 'Verdite', 'PlacidPoolR', 1),
    AreaDoor('1a340', 'A59300040106000000800000', 'Verdite', 'SporousNookL', 1),
    AreaDoor('1bac0', 'E38800040116000100800000', 'Daphne', 'RockyRidgeTrailL', 3),
    AreaDoor('1c7ec', '23A000050E06000000800000', 'Suzi', 'TramToSuziIslandR', 0),
)

area_doors: dict[str, AreaDoor] = {
    door.name: door
    for door in area_doors_unpackable
}

misc_doors: dict[str, AreaDoor] = {
    'AuroraUnitWreckageL': AreaDoor('1a598', '008000000106000000800000', 'Daphne', 'AuroraUnitWreckageL', 3),
    'WreckedMachineRoomR': AreaDoor('194ac', 'a5ec00090f06000000800000', 'Daphne', 'WreckedMachineRoomR', 3),
    'WreckedCrewQuartersAccessL': AreaDoor(
        '1be44', '9b8500040106000000800000', 'Daphne', 'WreckedCrewQuartersAccessL', 3
    ),
    'RockyRidgeR': AreaDoor('1bb80', '91ba00014e46040400800000', 'Daphne', 'RockyRidgeR', 3),
}

# to make sure this unpacking list is correct:
# print(f"({', '.join([c[3] for c in connections_unpackable])})")

(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable


def vanilla_areas() -> DoorPairs:
    return DoorPairs([
        (CraterR, WestTerminalAccessL),
        (SunkenNestL, OceanShoreR),
        (RuinedConcourseBL, TransferStationR),
        (RuinedConcourseTR, MezzanineConcourseL),
        (CausewayR, ExcavationSiteL),
        (SporeFieldTR, FieldAccessL),
        (SporeFieldBR, SporousNookL),
        (EleToTurbidPassageR, FieryGalleryL),
        (PileAnchorL, TramToSuziIslandR),
        (WestCorridorR, LoadingDockSecurityAreaL),
        (FoyerR, VulnarCanyonL),
        (ConstructionSiteL, CellarR),
        (AlluringCenoteR, NorakPerimeterBL),
        (SubbasementFissureL, VulnarDepthsElevatorER),
        (CanyonPassageR, NorakBrookL),
        (ElevatorToCondenserL, IntakePumpR),
        (ElevatorToWellspringL, CollapsedPassageR),
        (NorakPerimeterTR, RockyRidgeTrailL),
        (VulnarDepthsElevatorEL, PlacidPoolR),
        (HiveBurrowL, ThermalReservoir1R),
        (SequesteredInfernoL, ReservoirMaintenanceTunnelR),
        (MagmaPumpL, MagmaPumpAccessR),
        (GeneratorAccessTunnelL, HollowChamberR),
        (ElevatorToMagmaLakeR, RagingPitL)
    ])
