"""Location definitions for Mystical Ninja Starring Goemon (MN64)."""

from typing import Dict, NamedTuple

from BaseClasses import Location


class MN64Location(Location):
    """Location class for MN64."""

    game: str = "Mystical Ninja Starring Goemon"


class LocationData(NamedTuple):
    """Data structure for location information."""

    id: int
    region: str
    category: str = ""


# Base ID for all MN64 locations
BASE_ID = 6474000

# Oedo Town & Zazen Town Locations
OedoZazenLoc_table: Dict[str, LocationData] = {
    "PipeMakersHouse - Sudden Impact": LocationData(BASE_ID + 0, "PipeMakersHouse", "Ability"),
    "SuperPassBridge - Silver Fortune Doll": LocationData(BASE_ID + 1, "SuperPassBridge", "Fortune Doll"),
    "OedoCastleMainGate - Silver Fortune Doll": LocationData(BASE_ID + 2, "OedoCastleMainGate", "Fortune Doll"),
    "ZazenTownEntrance - Yae": LocationData(BASE_ID + 3, "ZazenTownEntrance", "Character"),
    "ZazenTownWateringhole - Silver Fortune Doll": LocationData(BASE_ID + 4, "ZazenTownWateringhole", "Fortune Doll"),
    "ZazenTownWateringhole - Miracle Snow": LocationData(BASE_ID + 5, "ZazenTownWateringhole", "Miracle"),
    "GoldenTemple - Mini Ebisumaru": LocationData(BASE_ID + 6, "GoldenTemple", "Ability"),
    "GoldenTemple - Jump Gym Key": LocationData(BASE_ID + 7, "GoldenTemple", "Key"),
}

# Musashi Province Locations
MusashiLoc_table: Dict[str, LocationData] = {
    "MtNyoigatakeFireShrine - Cucumber": LocationData(BASE_ID + 8, "MtNyoigatakeFireShrine", "Quest Item"),
    "MusashiBeach - Silver Fortune Doll": LocationData(BASE_ID + 38, "MusashiBeach", "Fortune Doll"),
    "TunneltoNortheast1 - Golden Health": LocationData(BASE_ID + 39, "TunneltoNortheast1", "Health"),
    "TunneltoNortheast2 - Silver Fortune Doll": LocationData(BASE_ID + 40, "TunneltoNortheast2", "Fortune Doll"),
    "TunneltoNortheast2 - Normal Health": LocationData(BASE_ID + 41, "TunneltoNortheast2", "Health"),
    "TunneltoNortheast2 - Golden Health": LocationData(BASE_ID + 42, "TunneltoNortheast2", "Health"),
}

# Duck Creek Locations
DuckCreekLoc_table: Dict[str, LocationData] = {
    # "Duck Creek Upstream - Yellow Fish 1": LocationData(BASE_ID + 9, "DuckCreekUpstream", "Fish"),
    # "Duck Creek Upstream - Yellow Fish 2": LocationData(BASE_ID + 10, "DuckCreekUpstream", "Fish"),
    # "Duck Creek Upstream - Yellow Fish 3": LocationData(BASE_ID + 11, "DuckCreekUpstream", "Fish"),
    # "Duck Creek Upstream - Red Fish": LocationData(BASE_ID + 12, "DuckCreekUpstream", "Fish"),
    # "Duck Creek Upstream - Blue Fish": LocationData(BASE_ID + 13, "DuckCreekUpstream", "Fish"),
    # "Duck Creek Under Town Bridge - Red Fish 1": LocationData(BASE_ID + 14, "DuckCreekUnderTownBridge", "Fish"),
    # "Duck Creek Under Town Bridge - Red Fish 2": LocationData(BASE_ID + 15, "DuckCreekUnderTownBridge", "Fish"),
    # "Duck Creek Under Town Bridge - Yellow Fish": LocationData(BASE_ID + 16, "DuckCreekUnderTownBridge", "Fish"),
    # "Duck Creek Under Town Bridge - Blue Fish 1": LocationData(BASE_ID + 17, "DuckCreekUnderTownBridge", "Fish"),
    # "Duck Creek Under Town Bridge - Blue Fish 2": LocationData(BASE_ID + 18, "DuckCreekUnderTownBridge", "Fish"),
    "DuckCreekUshiwaka - Achilles Heel": LocationData(BASE_ID + 19, "DuckCreekUshiwaka", "Equipment"),
    # "Duck Creek Ushiwaka - Yellow Fish": LocationData(BASE_ID + 20, "DuckCreekUshiwaka", "Fish"),
    # "Duck Creek Ushiwaka - Red Fish": LocationData(BASE_ID + 21, "DuckCreekUshiwaka", "Fish"),
    # "Duck Creek Ushiwaka - Blue Fish 1": LocationData(BASE_ID + 22, "DuckCreekUshiwaka", "Fish"),
    # "Duck Creek Ushiwaka - Blue Fish 2": LocationData(BASE_ID + 23, "DuckCreekUshiwaka", "Fish"),
    # "Benkei Bridge - Red Fish 1": LocationData(BASE_ID + 24, "BenkeiBridge", "Fish"),
    # "Benkei Bridge - Red Fish 2": LocationData(BASE_ID + 25, "BenkeiBridge", "Fish"),
    # "Benkei Bridge - Blue Fish 1": LocationData(BASE_ID + 26, "BenkeiBridge", "Fish"),
    # "Benkei Bridge - Blue Fish 2": LocationData(BASE_ID + 27, "BenkeiBridge", "Fish"),
    "DuckCreekJumpArea - Silver Fortune Doll": LocationData(BASE_ID + 28, "DuckCreekJumpArea", "Fortune Doll"),
    # "Duck Creek Jump Area - Red Fish 1": LocationData(BASE_ID + 29, "DuckCreekJumpArea", "Fish"),
    # "Duck Creek Jump Area - Red Fish 2": LocationData(BASE_ID + 30, "DuckCreekJumpArea", "Fish"),
    # "Duck Creek Jump Area - Yellow Fish 1": LocationData(BASE_ID + 31, "DuckCreekJumpArea", "Fish"),
    # "Duck Creek Jump Area - Yellow Fish 2": LocationData(BASE_ID + 32, "DuckCreekJumpArea", "Fish"),
    # "Duck Creek Jump Area - Blue Fish": LocationData(BASE_ID + 33, "DuckCreekJumpArea", "Fish"),
    # "Bizen Bridge - Red Fish 1": LocationData(BASE_ID + 34, "BizenBridge", "Fish"),
    # "Bizen Bridge - Red Fish 2": LocationData(BASE_ID + 35, "BizenBridge", "Fish"),
    # "Bizen Bridge - Red Fish 3": LocationData(BASE_ID + 36, "BizenBridge", "Fish"),
    # "Bizen Bridge - Yellow Fish": LocationData(BASE_ID + 37, "BizenBridge", "Fish"),
}

# Mutsu Province Locations
MutsuLoc_table: Dict[str, LocationData] = {
    "Iga - Golden Health": LocationData(BASE_ID + 43, "Iga", "Health"),
    # "Iga - Triton Shell": LocationData(BASE_ID + 44, "Iga", "Equipment"),
    "UzenTunnel - Silver Fortune Doll": LocationData(BASE_ID + 45, "UzenTunnel", "Fortune Doll"),
}

# Yamamoto Province Locations
YamamotoLoc_table: Dict[str, LocationData] = {
    "WaterfallofKegon - Yae Mermaid": LocationData(BASE_ID + 46, "WaterfallofKegon", "Ability"),
    "WaterfallofKegon - Gold Fortune Doll": LocationData(BASE_ID + 47, "WaterfallofKegon", "Fortune Doll"),
    "FestivalVillageSecretShop - Silver Fortune Doll": LocationData(BASE_ID + 48, "FestivalVillageSecretShop", "Fortune Doll"),
    "YamamotoUnderwaterCave - Silver Fortune Doll": LocationData(BASE_ID + 58, "YamamotoUnderwaterCave", "Fortune Doll"),
    "TurtleStone - Silver Fortune Doll": LocationData(BASE_ID + 59, "TurtleStone", "Fortune Doll"),
    "YamamotoShrineInterior - Normal Health Pickup": LocationData(BASE_ID + 60, "YamamotoShrineInterior", "Health"),
    "YamamotoShrineInterior - Surprise Pack": LocationData(BASE_ID + 61, "YamamotoShrineInterior", "Upgrade"),
    "YamamotoShrineInterior - Silver Fortune Doll Top": LocationData(BASE_ID + 62, "YamamotoShrineInterior", "Fortune Doll"),
    "YamamotoShrineInterior - Silver Fortune Doll Bottom": LocationData(BASE_ID + 63, "YamamotoShrineInterior", "Fortune Doll"),
}

# Sanuki Province Locations
SanukiLoc_table: Dict[str, LocationData] = {
    "Shoreline - Normal Health 1": LocationData(BASE_ID + 49, "Shoreline", "Health"),
    "Shoreline - Normal Health 2": LocationData(BASE_ID + 50, "Shoreline", "Health"),
    "Shoreline - Normal Health 3": LocationData(BASE_ID + 51, "Shoreline", "Health"),
    "Shoreline - Normal Health 4": LocationData(BASE_ID + 52, "Shoreline", "Health"),
    "Shoreline - Normal Health 5": LocationData(BASE_ID + 53, "Shoreline", "Health"),
    "Shoreline - Normal Health 6": LocationData(BASE_ID + 54, "Shoreline", "Health"),
    "Shoreline - Normal Health 7": LocationData(BASE_ID + 55, "Shoreline", "Health"),
    "UnderwaterJapanSea - Golden Health": LocationData(BASE_ID + 56, "UnderwaterJapanSea", "Health"),
    "UnderwaterJapanSea - Silver Fortune Doll": LocationData(BASE_ID + 57, "UnderwaterJapanSea", "Fortune Doll"),
    "UnderwaterJapanSea - Surprise Pack": LocationData(BASE_ID + 209, "UnderwaterJapanSea", "Upgrade"),
    "KiiAwajiIsland - Surprise Pack": LocationData(BASE_ID + 64, "KiiAwajiIsland", "Upgrade"),
    "KiiAwajiIsland - Silver Fortune Doll": LocationData(BASE_ID + 65, "KiiAwajiIsland", "Fortune Doll"),
    "HusbandandWifeRocks - Silver Fortune Doll": LocationData(BASE_ID + 67, "HusbandandWifeRocks", "Fortune Doll"),
}

# Folypoke Village Locations
FolypokeLoc_table: Dict[str, LocationData] = {
    "KompuraMountainGrounds - Medal of Flames": LocationData(BASE_ID + 68, "KompuraMountainGrounds", "Equipment"),
    "FolypokeVillageHayFarm - Silver Fortune Doll": LocationData(BASE_ID + 69, "FolypokeVillageHayFarm", "Fortune Doll"),
}

# Tosa Province Locations
TosaLoc_table: Dict[str, LocationData] = {
    "TosaBridge - Silver Fortune Doll": LocationData(BASE_ID + 70, "TosaBridge", "Fortune Doll"),
}

# Iyo Province Locations
IyoLoc_table: Dict[str, LocationData] = {
    "DogoHotsprings - Silver Fortune Doll": LocationData(BASE_ID + 71, "DogoHotsprings", "Fortune Doll"),
}

# Kai Province Locations
KaiLoc_table: Dict[str, LocationData] = {
    "KaiHighway - Silver Fortune Doll": LocationData(BASE_ID + 72, "KaiHighway", "Fortune Doll"),
    "MtFujiBottom - Golden Health": LocationData(BASE_ID + 73, "MtFujiBottom", "Health"),
    "MtFujiBottom - Silver Fortune Doll": LocationData(BASE_ID + 74, "MtFujiBottom", "Fortune Doll"),
    "MtFujiBottom - Normal Health": LocationData(BASE_ID + 75, "MtFujiBottom", "Health"),
    "MtFujiSalesmanRoom - Chain Pipe": LocationData(BASE_ID + 76, "MtFujiSalesmanRoom", "Equipment"),
    "MtFujiSalesmanRoom - Strength Upgrade 1": LocationData(BASE_ID + 77, "MtFujiSalesmanRoom", "Upgrade"),
    "MtFujiGoldenHealthLedge - Golden Health Pickup": LocationData(BASE_ID + 78, "MtFujiGoldenHealthLedge", "Health"),
}

# Bizen Province Locations
BizenLoc_table: Dict[str, LocationData] = {
    "Kurashiki - Gold Fortune Doll": LocationData(BASE_ID + 79, "Kurashiki", "Fortune Doll"),
    "Kurashiki - Silver Fortune Doll": LocationData(BASE_ID + 80, "Kurashiki", "Fortune Doll"),
    "JumpChallegeTraining - Jetpack": LocationData(BASE_ID + 81, "JumpChallegeTraining", "Ability"),
    "Nagato - Silver Fortune Doll": LocationData(BASE_ID + 82, "Nagato", "Fortune Doll"),
    "Nagato - Silver Fortune Doll 2": LocationData(BASE_ID + 83, "Nagato", "Fortune Doll"),
    "Nagato - Normal Health": LocationData(BASE_ID + 84, "Nagato", "Health"),
    # "LakewithaLargetree - Sasuke Battery 2": LocationData(BASE_ID + 85, "LakewithaLargetree", "Upgrade"),
    "LakewithaLargetree - Sasuke": LocationData(BASE_ID + 86, "LakewithaLargetree", "Character"),
    "Inaba - Golden Health": LocationData(BASE_ID + 87, "Inaba", "Health"),
    # "Inaba - Sasuke Battery 1": LocationData(BASE_ID + 88, "Inaba", "Upgrade"),
    "Inaba - Silver Fortune Doll": LocationData(BASE_ID + 89, "Inaba", "Fortune Doll"),
}

# Oedo Castle Locations
OedoCastleLoc_table: Dict[str, LocationData] = {
    "OedoCastleChainPipeRoom - Silver Key": LocationData(BASE_ID + 90, "OedoCastleChainPipeRoom", "Key"),
    "OedoCastleWaterRoom - Mr Elly Fant": LocationData(BASE_ID + 91, "OedoCastleWaterRoom", "Collectable"),
    "OedoCastleWaterRoom - Silver Fortune Doll": LocationData(BASE_ID + 92, "OedoCastleWaterRoom", "Fortune Doll"),
    "OedoCastleFightRoom1 - Silver Key": LocationData(BASE_ID + 93, "OedoCastleFightRoom1", "Key"),
    "OedoCastleFloorTileRoom - Silver Key": LocationData(BASE_ID + 94, "OedoCastleFloorTileRoom", "Key"),
    "OedoCastle3Platforms - Silver Key": LocationData(BASE_ID + 95, "OedoCastle3Platforms", "Key"),
    "OedoCastleDrummersRoom - Silver Fortune Doll": LocationData(BASE_ID + 96, "OedoCastleDrummersRoom", "Fortune Doll"),
    "OedoCastlePotRoom - Golden Health": LocationData(BASE_ID + 97, "OedoCastlePotRoom", "Health"),
    "OedoCastleFightRoom2 - Gold Key": LocationData(BASE_ID + 98, "OedoCastleFightRoom2", "Key"),
    "OedoCastleSpikeyWaterRoom - Mr Arrow": LocationData(BASE_ID + 99, "OedoCastleSpikeyWaterRoom", "Collectable"),
    "OedoCastleSpikeyWaterRoom - Golden Health": LocationData(BASE_ID + 100, "OedoCastleSpikeyWaterRoom", "Health"),
    "OedoCastleCongoChest - Normal Health": LocationData(BASE_ID + 101, "OedoCastleCongoChest", "Health"),
    "OedoCastleCongoEntranceRoom - Silver Fortune Doll": LocationData(BASE_ID + 102, "OedoCastleCongoEntranceRoom", "Fortune Doll"),
    "OedoCastleCongoEntranceRoom - Normal Health 1": LocationData(BASE_ID + 103, "OedoCastleCongoEntranceRoom", "Health"),
    "OedoCastleCongoEntranceRoom - Normal Health 2": LocationData(BASE_ID + 104, "OedoCastleCongoEntranceRoom", "Health"),
    "CongoBossRoom - Miracle Moon": LocationData(BASE_ID + 105, "CongoBossRoom", "Miracle"),
    "OedoCastleLordRoom - Super Pass": LocationData(BASE_ID + 106, "OedoCastleLordRoom", "Equipment"),
    "OedoCastleFightRoom3 - Silver Key": LocationData(BASE_ID + 107, "OedoCastleFightRoom3", "Key"),
    "OedoCastleTreasureRoom - Silver Fortune Doll": LocationData(BASE_ID + 108, "OedoCastleTreasureRoom", "Fortune Doll"),
}

# Ghost Toys Castle Locations
GhostToysLoc_table: Dict[str, LocationData] = {
    "GhostToysCastleCraneGame - Wind up Camera": LocationData(BASE_ID + 109, "GhostToysCastleCraneGame", "Equipment"),
    "GhostToysCastleCraneGameBackside - Silver Key": LocationData(BASE_ID + 110, "GhostToysCastleCraneGameBackside", "Key"),
    "GhostToysCastleCraneGameBackside - Silver Fortune Doll": LocationData(BASE_ID + 111, "GhostToysCastleCraneGameBackside", "Fortune Doll"),
    "GhostToysHeadRoom - Silver Fortune Doll": LocationData(BASE_ID + 112, "GhostToysHeadRoom", "Fortune Doll"),
    "GhostToysCastleEllyFantRoom - Mr Elly Fant": LocationData(BASE_ID + 113, "GhostToysCastleEllyFantRoom", "Collectable"),
    "GhostToysCastleEllyFantRoom - Normal Health 1": LocationData(BASE_ID + 114, "GhostToysCastleEllyFantRoom", "Health"),
    "GhostToysCastleEllyFantRoom - Normal Health 2": LocationData(BASE_ID + 115, "GhostToysCastleEllyFantRoom", "Health"),
    "GhostToysCastleFlowerRoom - Silver Key": LocationData(BASE_ID + 116, "GhostToysCastleFlowerRoom", "Key"),
    "GhostToysCastlePlatformRoom - Gold Fortune Doll": LocationData(BASE_ID + 117, "GhostToysCastlePlatformRoom", "Fortune Doll"),
    "GhostToysCastleUndergroundWaterway - Silver Fortune Doll": LocationData(BASE_ID + 118, "GhostToysCastleUndergroundWaterway", "Fortune Doll"),
    "GhostToysCastleMrArrowRoom - Mr Arrow": LocationData(BASE_ID + 119, "GhostToysCastleMrArrowRoom", "Collectable"),
    "GhostToysCastleSpikeyWaterCooridor - Normal Health 1": LocationData(BASE_ID + 120, "GhostToysCastleSpikeyWaterCooridor", "Health"),
    "GhostToysCastleSpikeyWaterCooridor - Normal Health 2": LocationData(BASE_ID + 121, "GhostToysCastleSpikeyWaterCooridor", "Health"),
    "GhostToysCastleGhostKeyRoom - Silver Key": LocationData(BASE_ID + 122, "GhostToysCastleGhostKeyRoom", "Key"),
    "GhostToysCastleSpinningTopRoom - Silver Key": LocationData(BASE_ID + 123, "GhostToysCastleSpinningTopRoom", "Key"),
    "GhostToysCastleLargeWaterRoom - Golden Health": LocationData(BASE_ID + 124, "GhostToysCastleLargeWaterRoom", "Health"),
    "GhostToysCastleLargeWaterRoom - Silver Fortune Doll": LocationData(BASE_ID + 125, "GhostToysCastleLargeWaterRoom", "Fortune Doll"),
    "GhostToysCastleStairsFight - Silver Key": LocationData(BASE_ID + 126, "GhostToysCastleStairsFight", "Key"),
    "GhostToysCastleInvisibleFloor - Surprise Pack": LocationData(BASE_ID + 127, "GhostToysCastleInvisibleFloor", "Upgrade"),
    "GhostToysCastleInvisibleFloor - Gold Key": LocationData(BASE_ID + 128, "GhostToysCastleInvisibleFloor", "Key"),
    "GhostToysCastleBillards - Silver Key": LocationData(BASE_ID + 129, "GhostToysCastleBillards", "Key"),
    "GhostToysCastleBossKeyRoom - Golden Health": LocationData(BASE_ID + 130, "GhostToysCastleBossKeyRoom", "Health"),
    "GhostToysCastleBossKeyRoom - Diamond Key": LocationData(BASE_ID + 131, "GhostToysCastleBossKeyRoom", "Key"),
    "GhostToysCastleBossRoom - Flower Miracle Item": LocationData(BASE_ID + 132, "GhostToysCastleBossRoom", "Miracle"),
}

# Festival Temple Castle Locations
FestivalTempleLoc_table: Dict[str, LocationData] = {
    "FestivalTempleFireClimb - Golden Health": LocationData(BASE_ID + 133, "FestivalTempleFireClimb", "Health"),
    "FestivalTempleGoldKeyRoomUpper - Gold Key": LocationData(BASE_ID + 134, "FestivalTempleGoldKeyRoomUpper", "Key"),
    "FestivalTempleRearEntranceUpper - Gold Fortune Doll": LocationData(BASE_ID + 135, "FestivalTempleRearEntranceUpper", "Fortune Doll"),
    "FestivalTempleRearEntranceLower - Golden Health": LocationData(BASE_ID + 136, "FestivalTempleRearEntranceLower", "Health"),
    "FestivalTempleSpinningSpikeRoom - Mr Elly Fant": LocationData(BASE_ID + 137, "FestivalTempleSpinningSpikeRoom", "Collectable"),
    "FestivalTempleSpinningSpikeRoom - Normal Health": LocationData(BASE_ID + 138, "FestivalTempleSpinningSpikeRoom", "Health"),
    "FestivalTempleSilverKeySplitoff - Golden Health": LocationData(BASE_ID + 139, "FestivalTempleSilverKeySplitoff", "Health"),
    "FestivalTempleSilverKeySplitoff - Silver Fortune Doll": LocationData(BASE_ID + 140, "FestivalTempleSilverKeySplitoff", "Fortune Doll"),
    "FestivalTempleCannonExterior - Surprise Pack": LocationData(BASE_ID + 141, "FestivalTempleCannonExterior", "Upgrade"),
    "FestivalTempleFishClimb - Golden Health": LocationData(BASE_ID + 142, "FestivalTempleFishClimb", "Health"),
    "FestivalTempleFishClimb - Normal Health 1": LocationData(BASE_ID + 143, "FestivalTempleFishClimb", "Health"),
    "FestivalTempleFishClimb - Normal Health 2": LocationData(BASE_ID + 144, "FestivalTempleFishClimb", "Health"),
    "FestivalTempleFishClimb - Silver Fortune Doll": LocationData(BASE_ID + 145, "FestivalTempleFishClimb", "Fortune Doll"),
    "FestivalTempleBossRoom - Miracle Star": LocationData(BASE_ID + 146, "FestivalTempleBossRoom", "Miracle"),
    "FestivalTempleIceKunaiRoom - Ice Kunai": LocationData(BASE_ID + 147, "FestivalTempleIceKunaiRoom", "Equipment"),
    "FestivalTempleIceKunaiRoom - Silver Fortune Doll": LocationData(BASE_ID + 148, "FestivalTempleIceKunaiRoom", "Fortune Doll"),
    "FestivalTempleMeatHammerRoom - Meat Hammer": LocationData(BASE_ID + 149, "FestivalTempleMeatHammerRoom", "Equipment"),
    "FestivalTempleDisplayDrumsRoom - Golden Health 1": LocationData(BASE_ID + 150, "FestivalTempleDisplayDrumsRoom", "Health"),
    "FestivalTempleDisplayDrumsRoom - Golden Health 2": LocationData(BASE_ID + 151, "FestivalTempleDisplayDrumsRoom", "Health"),
    "FestivalTempleMrArrowRoom - Mr Arrow": LocationData(BASE_ID + 152, "FestivalTempleMrArrowRoom", "Collectable"),
    "FestivalTempleWoodenHallwayUpper - Silver Fortune Doll": LocationData(BASE_ID + 153, "FestivalTempleWoodenHallwayUpper", "Fortune Doll"),
    "FestivalTempleWoodenHallwayStaircase - Normal Health 1": LocationData(BASE_ID + 154, "FestivalTempleWoodenHallwayStaircase", "Health"),
    "FestivalTempleWoodenHallwayStaircase - Normal Health 2": LocationData(BASE_ID + 155, "FestivalTempleWoodenHallwayStaircase", "Health"),
    "FestivalTempleWoodenSilverKeyRoom - Silver Key": LocationData(BASE_ID + 156, "FestivalTempleWoodenSilverKeyRoom", "Key"),
}

# Gorgeous Music Castle Locations
GorgeousMusicLoc_table: Dict[str, LocationData] = {
    "GorgeousMusicCastleClosingFanRoom - Silver Fortune Doll": LocationData(BASE_ID + 157, "GorgeousMusicCastleClosingFanRoom", "Fortune Doll"),
    "GorgeousMusicCastleChangingRoom - Silver Fortune Doll": LocationData(BASE_ID + 158, "GorgeousMusicCastleChangingRoom", "Fortune Doll"),
    "GorgeousMusicCastleWaterRoom - Silver Fortune Doll": LocationData(BASE_ID + 159, "GorgeousMusicCastleWaterRoom", "Fortune Doll"),
    "GorgeousMusicCastleWaterRoom - Surprise Pack": LocationData(BASE_ID + 160, "GorgeousMusicCastleWaterRoom", "Upgrade"),
    "GorgeousMusicCastleWaterRoom - Golden Health": LocationData(BASE_ID + 161, "GorgeousMusicCastleWaterRoom", "Health"),
    # "GorgeousMusicCastleWaterRoom - Mr Elly Fant": LocationData(BASE_ID + 165, "GorgeousMusicCastleWaterRoom", "Collectable"),
    "GorgeousMusicCastleWaterRoom - Mr Arrow": LocationData(BASE_ID + 162, "GorgeousMusicCastleWaterRoom", "Collectable"),
    "GorgeousMusicCastleGarden - Strength Upgrade 2": LocationData(BASE_ID + 163, "GorgeousMusicCastleGarden", "Upgrade"),
    "GorgeousMusicCastleDancinWarp - Gold Fortune Doll": LocationData(BASE_ID + 164, "GorgeousMusicCastleDancinWarp", "Fortune Doll"),
    "GorgeousMusicCastleConveyorBeltRoom - Golden Health": LocationData(BASE_ID + 210, "GorgeousMusicCastleConveyorBeltRoom", "Health"),
    "GorgeousMusicCastleRaisingPlatform - Diamond Key": LocationData(BASE_ID + 166, "GorgeousMusicCastleRaisingPlatform", "Key"),
    "GorgeousMusicCastleSlideRoomUpper - Golden Health": LocationData(BASE_ID + 167, "GorgeousMusicCastleSlideRoomUpper", "Health"),
    "GorgeousMusicCastleDungeon - Silver Fortune Doll": LocationData(BASE_ID + 168, "GorgeousMusicCastleDungeon", "Fortune Doll"),
    "GorgeousMusicCastleGoldWaterKey - Gold Key": LocationData(BASE_ID + 169, "GorgeousMusicCastleGoldWaterKey", "Key"),
    "GorgeousMusicCastleMovingBoxClimb - Diamond Key": LocationData(BASE_ID + 170, "GorgeousMusicCastleMovingBoxClimb", "Key"),
    "GorgeousMusicCastleSuddenImpactRoomUpper - Mr Ellyfant": LocationData(BASE_ID + 171, "GorgeousMusicCastleSuddenImpactRoomUpper", "Collectable"),
    "GorgeousMusicCastleSuddenImpactRoomUpper - Gold Key": LocationData(BASE_ID + 172, "GorgeousMusicCastleSuddenImpactRoomUpper", "Key"),
    "GorgeousMusicCastleFlameHallwayLower - Golden Health": LocationData(BASE_ID + 173, "GorgeousMusicCastleFlameHallwayLower", "Health"),
    "GorgeousMusicCastleScaffoldingClimbUpper - Golden Health": LocationData(BASE_ID + 174, "GorgeousMusicCastleScaffoldingClimbUpper", "Health"),
    "GorgeousMusicCastleScaffoldingClimbUpper - Silver Key": LocationData(BASE_ID + 175, "GorgeousMusicCastleScaffoldingClimbUpper", "Key"),
    "GorgeousMusicCastleFanJump - Golden Health 1": LocationData(BASE_ID + 176, "GorgeousMusicCastleFanJump", "Health"),
    "GorgeousMusicCastleFanJump - Golden Health 2": LocationData(BASE_ID + 177, "GorgeousMusicCastleFanJump", "Health"),
    "GorgeousMusicCastleFanJump - Gold Key": LocationData(BASE_ID + 178, "GorgeousMusicCastleFanJump", "Key"),
}

# Gourmet Submarine Locations
GourmetSubmarineLoc_table: Dict[str, LocationData] = {
    "GourmetSubmarineEntrance - Mr Elly Fant": LocationData(BASE_ID + 179, "GourmetSubmarineEntrance", "Collectable"),
    "GourmetSubmarineFightandHealth - Normal Health 1": LocationData(BASE_ID + 180, "GourmetSubmarineFightandHealth", "Health"),
    "GourmetSubmarineFightandHealth - Normal Health 2": LocationData(BASE_ID + 181, "GourmetSubmarineFightandHealth", "Health"),
    "GourmetSubmarineThreeWayJump - Golden Health": LocationData(BASE_ID + 182, "GourmetSubmarineThreeWayJump", "Health"),
    "GourmetSubmarineSushiConveyer - Silver Key": LocationData(BASE_ID + 183, "GourmetSubmarineSushiConveyer", "Key"),
    "GourmetSubmarineThreeBowls - Mr Arrow": LocationData(BASE_ID + 184, "GourmetSubmarineThreeBowls", "Collectable"),
    "GourmetSubmarineEvilFishRoom - Silver Key": LocationData(BASE_ID + 185, "GourmetSubmarineEvilFishRoom", "Key"),
    "GourmetSubmarineWaterloggedChainpipeHallway - Normal Health 1": LocationData(BASE_ID + 186, "GourmetSubmarineWaterloggedChainpipeHallway", "Health"),
    "GourmetSubmarineWaterloggedChainpipeHallway - Normal Health 2": LocationData(BASE_ID + 187, "GourmetSubmarineWaterloggedChainpipeHallway", "Health"),
    "GourmetSubmarineWaterloggedChainpipeHallway - Normal Health 3": LocationData(BASE_ID + 188, "GourmetSubmarineWaterloggedChainpipeHallway", "Health"),
    "GourmetSubmarineWaterloggedChainpipeHallway - Normal Health 4": LocationData(BASE_ID + 189, "GourmetSubmarineWaterloggedChainpipeHallway", "Health"),
    "GourmetSubmarineWaterloggedChainpipeHallway - Normal Health 5": LocationData(BASE_ID + 190, "GourmetSubmarineWaterloggedChainpipeHallway", "Health"),
    "GourmetSubmarineWaterloggedChainpipeHallway - Normal Health 6": LocationData(BASE_ID + 191, "GourmetSubmarineWaterloggedChainpipeHallway", "Health"),
    "GourmetSubmarineWaterloggedChainpipeHallway - Normal Health 7": LocationData(BASE_ID + 192, "GourmetSubmarineWaterloggedChainpipeHallway", "Health"),
    "GourmetSubmarineWaterloggedChainpipeHallway - Normal Health 8": LocationData(BASE_ID + 193, "GourmetSubmarineWaterloggedChainpipeHallway", "Health"),
    "GourmetSubmarineHotConveyers - Golden Health": LocationData(BASE_ID + 194, "GourmetSubmarineHotConveyers", "Health"),
    "GourmetSubmarineHotConveyers - Silver Key": LocationData(BASE_ID + 195, "GourmetSubmarineHotConveyers", "Key"),
    "GourmetSubmarineZeroGravityFightLower - Gold Key": LocationData(BASE_ID + 196, "GourmetSubmarineZeroGravityFightLower", "Key"),
    "GourmetSubmarineZeroGravityFightLower - Normal Health 1": LocationData(BASE_ID + 197, "GourmetSubmarineZeroGravityFightLower", "Health"),
    "GourmetSubmarineZeroGravityFightLower - Normal Health 2": LocationData(BASE_ID + 198, "GourmetSubmarineZeroGravityFightLower", "Health"),
    "GourmetSubmarineSushiWindupCamera - Golden Health": LocationData(BASE_ID + 199, "GourmetSubmarineSushiWindupCamera", "Health"),
    "GourmetSubmarineGiantCrabFight - Surprise Pack": LocationData(BASE_ID + 200, "GourmetSubmarineGiantCrabFight", "Upgrade"),
    "GourmetSubmarineWiringRoom - Golden Health": LocationData(BASE_ID + 201, "GourmetSubmarineWiringRoom", "Health"),
    "GourmetSubmarineMetalBalanceBeam - Normal Health 1": LocationData(BASE_ID + 202, "GourmetSubmarineMetalBalanceBeam", "Health"),
    "GourmetSubmarineMetalBalanceBeam - Normal Health 2": LocationData(BASE_ID + 203, "GourmetSubmarineMetalBalanceBeam", "Health"),
    "GourmetSubmarineHotWindupCamera - Diamond Key": LocationData(BASE_ID + 204, "GourmetSubmarineHotWindupCamera", "Key"),
    "GourmetSubmarineSushiSamurais - Silver Key": LocationData(BASE_ID + 205, "GourmetSubmarineSushiSamurais", "Key"),
    "GourmetSubmarineZeroGravityFightUpper - Surprise Pack": LocationData(BASE_ID + 206, "GourmetSubmarineZeroGravityFightUpper", "Upgrade"),
    "GourmetSubmarineBurgerRoom - Bazooka": LocationData(BASE_ID + 207, "GourmetSubmarineBurgerRoom", "Equipment"),
    "GourmetSubmarineBurgerRoom - Silver Key": LocationData(BASE_ID + 208, "GourmetSubmarineBurgerRoom", "Key"),
    "OedoTouristCenterAwajiIslandBranch - Dragon Defeated": LocationData(BASE_ID + 66, "OedoTouristCenterAwajiIslandBranch", "Upgrade"),
}

# Combine all location tables
all_locations: Dict[str, LocationData] = {}
all_locations.update(OedoZazenLoc_table)
all_locations.update(MusashiLoc_table)
all_locations.update(DuckCreekLoc_table)
all_locations.update(MutsuLoc_table)
all_locations.update(YamamotoLoc_table)
all_locations.update(SanukiLoc_table)
all_locations.update(FolypokeLoc_table)
all_locations.update(TosaLoc_table)
all_locations.update(IyoLoc_table)
all_locations.update(KaiLoc_table)
all_locations.update(BizenLoc_table)
all_locations.update(OedoCastleLoc_table)
all_locations.update(GhostToysLoc_table)
all_locations.update(FestivalTempleLoc_table)
all_locations.update(GorgeousMusicLoc_table)
all_locations.update(GourmetSubmarineLoc_table)


def get_location_name_to_id() -> Dict[str, int]:
    """Get a dictionary mapping location names to their IDs."""
    return {name: data.id for name, data in all_locations.items()}


def get_locations_by_category(category: str) -> Dict[str, LocationData]:
    """Get all locations of a specific category."""
    return {name: data for name, data in all_locations.items() if data.category == category}


def get_locations_by_region(region: str) -> Dict[str, LocationData]:
    """Get all locations in a specific region."""
    return {name: data for name, data in all_locations.items() if data.region == region}
