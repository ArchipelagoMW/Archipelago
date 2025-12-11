from typing import Dict, Set

from .Names import LocationName

# eventid matches Randomizer Seed index in table
CA_CHECKS: Dict[str, int] = {
    LocationName.BehindFurnitureCard: 1,
    LocationName.StaircaseLedgesCard: 2,
    LocationName.UpperLedgeFossil: 3,
    LocationName.TopofGPCCard: 4,
    LocationName.UnderGPCCard: 5,
    LocationName.MountainLionLogBridgeCard: 6,
    LocationName.AboveEntranceLakeCard: 7,
    LocationName.RockWallBehindTreeCard: 8,
    LocationName.RockWallTopPirateScope: 9,
    LocationName.TreeNearFenceCard: 10,
    LocationName.TreeNearGeyserCard: 11,
    LocationName.FenceBehindGPCCard: 12,
    LocationName.NeartheBearCard: 13,
    LocationName.RockyPlatformsBehindGPCRightCard: 14,
    LocationName.RockyPlatformsBehindGPCLeftCard: 15,
    LocationName.TopofLogFlumeCard: 16,
    LocationName.RidetheLogFlumeCard: 17,
    LocationName.BottomofLogFlumeCard: 18,
    LocationName.BigRockNearFordCard: 19,
    LocationName.RuinedCabinChallengeMarker: 20,
    LocationName.BranchSwingingCourseStartCard: 21,
    LocationName.BranchSwingingCourseMidCard: 22,
    LocationName.BranchSwingingCourseEndChallengeMarker: 23,
    LocationName.BranchAboveSquirrelCard: 24,
    LocationName.CreekGrateGlassEye: 25,
    LocationName.SquirrelsAcornGoldenAcorn: 26,
    LocationName.GeyserMinersSkull: 27,
    LocationName.FenceNearKidsCabinsCard: 28,
    LocationName.UnderLodgeFrontStepsCard: 29,
    LocationName.BehindTreeNearLodgeCard: 30,
    LocationName.UndertheLodgeGoldDoubloon: 31,
    LocationName.Loudspeaker1PlatformCard: 32,
    LocationName.UnderLodgeMetalRoofCard: 33,
    LocationName.LoudspeakerTightropeWalkCard: 34,
    LocationName.Loudspeaker2PlatformCard: 35,
    LocationName.LodgeRoofChallengeMarker: 36,
    LocationName.MetalRoofOutcroppingCard: 37,
    LocationName.LoudspeakerAboveStumpCard: 38,
    LocationName.TreePlatformLeftCard: 39,
    LocationName.TreePlatformRightEagleClaw: 40,
    LocationName.RockWallTopCard: 41,
    LocationName.ParkingLotArchCard: 42,
    LocationName.ParkingLotSmallLogCard: 43,
    LocationName.OleandersCarCard: 44,
    LocationName.ParkingLotBasketballHoopCard: 45,
    LocationName.ParkingLotHistoryBoardCard: 46,
    LocationName.ParkingLotOuthouseCard: 47,
    LocationName.RockNearBenchCard: 48,
    LocationName.GrindingontheRootsCard: 49,
    LocationName.UnderStairsCard: 50,
    LocationName.TopotheLoudspeakerCard: 51,
    LocationName.CabinRoof1Card: 52,
    LocationName.TrampolineAboveOuthouseCard: 53,
    LocationName.TrampolinePlatformChallengeMarker: 54,
    LocationName.CabinsOuthouseCard: 55,
    LocationName.BehindCabinCard: 56,
    LocationName.RoofofCabin2Card: 57,
    LocationName.CaveEntranceCard: 58,
    LocationName.DeepCavePathCard: 59,
    LocationName.DeepCaveLadderCard: 60,
    LocationName.HighUpTightropeCard: 61,
    LocationName.CaveRefrigeratorTurkeySandwich: 62,
    LocationName.GraveyardBearCard: 63,
    LocationName.NearBeehiveCard: 64,
    LocationName.MineshaftTrailerEntranceCard: 65,
    LocationName.TightropeStartCard: 66,
    LocationName.TightropeEndCard: 67,
    LocationName.RocksNearTrailerCard: 68,
    LocationName.FireplaceTreeLowerCard: 69,
    LocationName.FireplaceTreeRockCard: 70,
    LocationName.SwampSkinnyPolesCard: 71,
    LocationName.BigLogPlatformCard: 72,
    LocationName.AboveWaterfallLeftCard: 73,
    LocationName.AboveWaterfallRightCard: 74,
    LocationName.BehindtheWaterfallCard: 75,
    LocationName.WeirdTreeLeftCherryWoodPipe: 76,
    LocationName.WeirdTreeRightCard: 77,
    LocationName.LogHillTopCard: 78,
    LocationName.LogHillBehindCard: 79,
    LocationName.MineshaftGrindRailCard: 80,
    LocationName.MineshaftUpperEntranceCard: 81,
    LocationName.MineshaftAboveUpperEntranceCard: 82,
    LocationName.InsideMineshaftCard: 83,
    LocationName.MineshaftBearCard: 84,
    LocationName.SwampBirdsNestCondorEgg: 85,
    LocationName.CollapsedCaveChallengeMarker: 86,
    LocationName.FireplaceTreeTopDinosaurBone: 87,
    LocationName.HornetNestFertilityIdol: 88,
    LocationName.UndertheFirstBridgeCard: 89,
    LocationName.BehindStumpCard: 90,
    LocationName.LeftofEntranceRockWallCard: 91,
    LocationName.PolesonLakeCard: 92,
    LocationName.BathysphereRoofCard: 93,
    LocationName.BathysphereDockCard: 94,
    LocationName.MetalRoofAboveFordCard: 95,
    LocationName.AboveFordRopesCard: 96,
    LocationName.AboveFordCabinPlatformCard: 97,
    LocationName.OutsideCougarCaveCard: 98,
    LocationName.InsideCougarCaveDiversHelmet: 99,
    LocationName.BulletinBoardBushesCard: 100,
    LocationName.PinkTreesPlatformLeftCard: 101,
    LocationName.PinkTreesPlatformRightCard: 102,
    LocationName.RockWallUpperCard: 103,
    LocationName.LakeShoreCard: 104,
    LocationName.TinyIslandCard: 105,
    LocationName.TopofBigRockChallengeMarker: 106,
    LocationName.RockWallGapPsychonautsComic1: 107,
    LocationName.LungfishBossComplete: 365,
    LocationName.MainLodgeRaftersVoodooDoll: 108,
    LocationName.TopofSanctuaryCard: 109,
    LocationName.BottomofSanctuaryCard: 110,

}

AS_CHECKS: Dict[str, int] = {
    LocationName.RockWallBottom: 111,
    LocationName.RockWallLadder: 112,
    LocationName.OutsideFrontGate: 113,
    LocationName.PillarAboveGate: 114,
    LocationName.FountainTop: 115,
    LocationName.HedgeAlcove: 116,
    LocationName.AsylumDoorsRight: 117,
    LocationName.AsylumDoorsLeft: 118,
    LocationName.CornerNearFence: 119,
    LocationName.LedgeBeforeGloria: 120,
    LocationName.AboveElevator: 121,
    LocationName.CrowsBasket: 122,
    LocationName.LedgeAboveFredLeft: 123,
    LocationName.LedgeAboveFredRight: 124,
    LocationName.LedgeOppositeElevator: 125,
    LocationName.EdgarsRoom: 126,
    LocationName.BehindElevator: 127,
    LocationName.JunkCorner: 128,
    LocationName.AboveEdgar: 129,
    LocationName.BehindMattressWall: 130,
    LocationName.CheckeredBathroom: 131,
    LocationName.RoomNearCheckeredBathroom: 132,
    LocationName.ElevatorShaft: 133,
    LocationName.RoomLeftOfPipeSlide: 134,
    LocationName.FloatingInHole: 135,
    LocationName.NextToHole: 136,
    LocationName.CrumblingOuterWallPlanks: 137,
    LocationName.CrumblingOuterWallPillar: 138,
    LocationName.CrumblingOuterWallBelowPlatform: 139,
    LocationName.CrumblingOuterWallPlatform: 140,
    LocationName.RoomAboveTiltedStairs: 141,
    LocationName.AcidRoomFloor: 142,
    LocationName.AcidRoomTable: 143,
    LocationName.AcidRoomWindow: 144,
    LocationName.AcidRoomOverhang: 145,
    LocationName.SmallWindowsLedge: 146,
    LocationName.RoundWoodPlatform: 147,
    LocationName.GrateClimbBottom: 148,
    LocationName.GrateClimbMid: 149,
    LocationName.SinkPlatformLeft: 150,
    LocationName.SinkPlatformRight: 151,
    LocationName.PipesBelowChairDoor: 152,
    LocationName.RoomOppositeChairDoor: 153,
    LocationName.PipeSlideNearChairDoor: 154,
    LocationName.RaftersAboveChairDoor: 155,
    LocationName.LabCagedCrowLeft: 156,
    LocationName.LabCagedCrowRight: 157,
    LocationName.NextToPokeylope: 158,
    LocationName.LabTopRailingLeft1: 159,
    LocationName.LabTopRailingLeft2: 160,
    LocationName.LabTopElevator: 161,
    LocationName.LabTopRailingRight: 162,
    LocationName.TeaRoom: 163,
}

BB_CHECKS: Dict[str, int] = {
    LocationName.JumpingTutorial1: 164,
    LocationName.JumpingTutorial2: 165,
    LocationName.PoleClimbingTutorialFloor: 166,
    LocationName.BelowTheTripleTrampolines: 167,
    LocationName.GiantSoldierCutOut: 168,
    LocationName.DodgingBullets1: 169,
    LocationName.DodgingBullets2: 170,
    LocationName.MachineGunTurret: 171,
    LocationName.PoleSwingingTutorial: 172,
    LocationName.TrapezeCobweb: 173,
    LocationName.TrapezePlatform: 174,
    LocationName.InsidePlaneWreckage: 175,
    LocationName.EndOfObstacleCourseLeft: 176,
    LocationName.EndOfObstacleCourseRight: 177,
    LocationName.BasicBrainingComplete: 178,
}

SA_CHECKS: Dict[str, int] = {
    LocationName.OnTheBed: 179,
    LocationName.OnThePillow: 180,
    LocationName.BuildingBlocksLeft: 181,
    LocationName.BuildingBlocksBelow: 182,
    LocationName.BuildingBlocksRight: 183,
    LocationName.TopOfBedFrame: 184,
    LocationName.RoundPlatformsBottom: 185,
    LocationName.RoundPlatformsNearValve: 186,
    LocationName.RoundPlatformsFarFromValve: 187,
    LocationName.SideOfCubeFace3: 188,
    LocationName.BottomOfShoeboxLadder: 189,
    LocationName.ShoeboxPedestal: 190,
    LocationName.ShoeboxTowerTop: 191,
    LocationName.FlameTowerSteps: 192,
    LocationName.FlameTowerTop1: 193,
    LocationName.FlameTowerTop2: 194,
    LocationName.SashasShootingGalleryComplete: 195,
}

MI_CHECKS: Dict[str, int] = {
    LocationName.IntroRingsTutorial: 196,
    LocationName.DancingCamperPlatform1: 197,
    LocationName.DemonRoom: 198,
    LocationName.WindyLadderBottom: 199,
    LocationName.PinballPlunger: 200,
    LocationName.PlungerPartyLedge: 201,
    LocationName.GrindrailRings: 202,
    LocationName.CensorHallway: 203,
    LocationName.PinkBowlBottom: 204,
    LocationName.PinkBowlSmallPlatform: 205,
    LocationName.BubblyFanBottom: 206,
    LocationName.BubblyFanPlatform: 207,
    LocationName.BubblyFanTop: 208,
    LocationName.MillasPartyRoom: 209,
    LocationName.MillasDancePartyComplete: 210,
}

NI_CHECKS: Dict[str, int] = {
    LocationName.OutsideCaravan: 211,
    LocationName.BehindTheEgg: 212,
    LocationName.ShadowMonsterPath: 213,
    LocationName.ShadowMonsterBlueMushrooms: 214,
    LocationName.LedgeBehindShadowMonster: 215,
    LocationName.BelowTheSteepLedge: 216,
    LocationName.ForestPathBlueMushrooms: 217,
    LocationName.ForestBlueLedge: 218,
    LocationName.ForestHighPlatform: 219,
    LocationName.ForestPathThorns: 220,
    LocationName.BehindThornTowerLeft: 221,
    LocationName.BehindThornTowerMid: 222,
    LocationName.BehindThornTowerRight: 223,
    LocationName.BrainTumblerExperimentComplete: 224,
}

LO_CHECKS: Dict[str, int] = {
    LocationName.SkyscraperStart: 225,
    LocationName.CornerNearJail: 226,
    LocationName.SkyscraperBeforeDam: 227,
    LocationName.BehindLasersLeft1: 228,
    LocationName.BehindLasersLeft2: 229,
    LocationName.BehindLasersRight: 230,
    LocationName.BlimpHop: 231,
    LocationName.EndOfDam: 232,
    LocationName.EndOfDamPlatform: 233,
    LocationName.SkyscraperAfterDam: 234,
    LocationName.NearBattleships: 235,
    LocationName.OnTheBridge: 236,
    LocationName.GroundAfterBridge: 237,
    LocationName.SkyscraperAfterBridge: 238,
    LocationName.TunnelSuitcaseTag: 239,
    LocationName.FinalSkyscrapersLeft: 240,
    LocationName.FinalSkyscrapersRight: 241,
    LocationName.KochamaraIntroLeft: 242,
    LocationName.KochamaraIntroRight: 243,
    LocationName.LungfishopolisComplete: 244,
}

MM_CHECKS: Dict[str, int] = {
    LocationName.BoydsFridgeClv: 245,
    LocationName.FirstHouseDufflebagTag: 246,
    LocationName.SecondHouseRollingPin: 247,
    LocationName.CarTrunk1StopSign: 248,
    LocationName.RoofAfterRoadCrewPurseTag: 249,
    LocationName.CarTrunk2HedgeTrimmers: 250,
    LocationName.CarHouseBackyardSteamertrunkTag: 251,
    LocationName.InsideWebbedGarageHatbox: 252,
    LocationName.GraveyardPatioVault: 253,
    LocationName.GraveyardBehindTreeOneUp: 254,
    LocationName.BehindGraveyardDufflebag: 255,
    LocationName.HedgeMazeFlowers: 256,
    LocationName.CarTrunk3WateringCan: 257,
    LocationName.PostOfficeRoofOneUp: 258,
    LocationName.PostOfficeLobbySuitcase: 259,
    LocationName.PostOfficeBasementPlunger: 260,
    LocationName.LandscapersHouseBackyardSuitcaseTag: 261,
    LocationName.LandscapersHouseTablePurse: 262,
    LocationName.LandscapersHouseKitchenAmmoUp: 263,
    LocationName.PowerlineIslandSandboxHatboxTag: 264,
    LocationName.PowerlineIslandLeftMemoryVault: 265,
    LocationName.PowerlineIslandRightMaxLives: 266,
    LocationName.BehindBookDepositorySteamerTrunk: 267,
    LocationName.MilkmanComplete: 268,
}

TH_CHECKS: Dict[str, int] = {
    LocationName.NearTheCriticPurse: 269,
    LocationName.InTheAudienceAmmoUp: 270,
    LocationName.BelowTheSpotlightSteamertrunkTag: 271,
    LocationName.BehindStagePurseTag: 272,
    LocationName.BehindStageCobwebSuitcase: 273,
    LocationName.StorageRoomFloorVault: 274,
    LocationName.StorageRoomLeftSteamertrunk: 275,
    LocationName.StorageRoomRightLowerSuitcaseTag: 276,
    LocationName.StorageRoomRightUpperCandle1: 277,
    LocationName.BonitasRoom: 278,
    LocationName.DoghouseSlicersDufflebagTag: 279,
    LocationName.BigPlatform1Hatbox: 280,
    LocationName.BigPlatform2Vault: 281,
    LocationName.BigPlatform3OneUp: 282,
    LocationName.BigPlatformAboveHatboxTag: 283,
    LocationName.NextToOatmealDufflebag: 284,
    LocationName.CandleBasketCandle2: 285,
    LocationName.CurtainSlideConfusionAmmoUp: 286,
    LocationName.GloriasTheaterComplete: 287,
}

WW_CHECKS: Dict[str, int] = {
    LocationName.FredsRoomHatboxTag: 288,
    LocationName.TheFireplacePricelessCoin: 289,
    LocationName.GameBoardSuitcaseTag: 290,
    LocationName.CarpentersRoofVault: 291,
    LocationName.TightropeRoomDufflebag: 292,
    LocationName.OutsideVillager1HouseOneUp: 293,
    LocationName.SmallArchTopMaxLives: 294,
    LocationName.SmallArchBelowPurseTag: 295,
    LocationName.TopOfVillager2sHouseDufflebagTag: 296,
    LocationName.TopOfVillager3sHouseAmmoUp: 297,
    LocationName.TopOfKnightsHouseConfusionAmmoUp: 298,
    LocationName.CastleTowerOneUp: 299,
    LocationName.CastleInsideVault: 300,
    LocationName.CastleWallSteamertrunk: 301,
    LocationName.UnderTheGuillotineSuitcase: 302,
    LocationName.FredsHouseBasementHatbox: 303,

    LocationName.BlacksmithsLeftBuildingPurse: 304,
    LocationName.BlacksmithsRightBuildingSteamertrunkTag: 305,
    LocationName.BlacksmithsHaybaleTheMusket: 306,
    LocationName.HelpTheCarpenter: 307,
    LocationName.HelpVillager1: 308,
    LocationName.HelpTheKnight: 309,
    LocationName.HelpVillager2: 310,
    LocationName.HelpVillager3: 311,
    LocationName.WaterlooWorldComplete: 312,
}

BV_CHECKS: Dict[str, int] = {
    LocationName.ClubStreetLadySteamertrunk: 313,
    LocationName.ClubStreetMetalBalconyDufflebagTag: 314,
    LocationName.HeartStreetHIGHBalconyAmmoUp: 315,
    LocationName.AlleywaysLedgeHatboxTag: 316,
    LocationName.SewersMainVault: 317,
    LocationName.ClubStreetGatedSteamerTrunkTag: 318,
    LocationName.BurnTheLogsDufflebag: 319,

    LocationName.TheGardenVault: 320,
    LocationName.NearDiegosHouseMaxLives: 321,
    LocationName.DiegosBedSuitcaseTag: 322,
    LocationName.DiegosHouseGrindrailSuitcase: 323,
    LocationName.DiegosRoomHatbox: 324,
    LocationName.GrindrailBalconyConfusionAmmoUp: 325,
    LocationName.SanctuaryBalconyPurseTag: 326,

    LocationName.SanctuaryGroundPurse: 327,
    LocationName.TigerWrestler: 328,
    LocationName.DragonWrestler: 329,
    LocationName.EagleWrestler: 330,
    LocationName.CobraWrestler: 331,
    LocationName.BlackVelvetopiaComplete: 332,
}

MC_CHECKS: Dict[str, int] = {
    LocationName.EntranceAwningSteamertrunkTag: 333,
    LocationName.CrumblingPathSteamertrunk: 334,
    LocationName.CrumblingPathEndRightHatboxTag: 335,
    LocationName.CrumblingPathEndLeftConfusionAmmoUp: 336,
    LocationName.OllieEscortFloorSuitcaseTag: 337,
    LocationName.OllieEscortMiddleHatbox: 338,
    LocationName.OllieEscortTopLeftVault: 339,
    LocationName.OllieEscortTopRightPurseTag: 340,
    LocationName.TunnelOfLoveStartPurse: 341,
    LocationName.TunnelOfLoveCornerSuitcase: 342,
    LocationName.TunnelOfLoveRailDufflebagTag: 343,
    LocationName.NextToTheFatLadyDufflebag: 344,
}

# Leave a gap in the IDs so that more locations can be added that place items into the game world without having to
# adjust the IDs of all locations that don't place items into the game world.
EVENT_LOCATIONS: Dict[str, int] = {
    # for beating Meat Circus
    LocationName.MeatCircusFinalBossEvent: 500,
    # for Brain Jar Goal
    LocationName.RedeemedBrainsEvent: 501,
    # for Coach Oleander Brain Tank Boss
    LocationName.OleanderBrainTankBossEvent: 502,
}

# Deep Arrowhead locations.
# These are not included in PsychoRando seed generation so the IDs must be greater than all locations which are included
# in PsychoRando seed generation.
# Main Campgrounds
CAMA_DEEP_ARROWHEAD_CHECKS: Dict[str, int] = {
    LocationName.DeepAHTrashCanNorthOfLodge: 503,
    LocationName.DeepAHMainLodgeWalkway: 504,
    LocationName.DeepAHUnderStartOfLakeBridge: 505,
    LocationName.DeepAHGPCPathBeforeCougar: 506,
    LocationName.DeepAHWestOfStump: 507,
    LocationName.DeepAHReceptionEntrance: 508,
    LocationName.DeepAHParkingLotLogFence: 509,
    LocationName.DeepAHUnderMainLodge: 510,
    LocationName.DeepAHRockWallTop: 511,
}

# GPC and Wilderness
CAGP_DEEP_ARROWHEAD_CHECKS: Dict[str, int] = {
    # GPC (CAGP)
    LocationName.DeepAHInRiverBeforeGrate: 512,
    LocationName.DeepAHInsideGPCFenceNorth: 513,
    LocationName.DeepAHNearStumpDeep: 514,
    LocationName.DeepAHTreeNearSquirrel: 515,
    LocationName.DeepAHRiverNearRuinedCabin: 516,
    LocationName.DeepAHInsideGPCFenceSouthWest: 517,
    LocationName.DeepAHLargerBoulderByLake: 518,
    LocationName.DeepAHGeyser: 519,
    LocationName.DeepAHNearBear: 520,
    LocationName.DeepAHBigRockNearFord: 521,
    LocationName.DeepAHOppositeRiverFromStump: 522,
    LocationName.DeepAHBeforeCampEntrance: 523,
    LocationName.DeepAHBeforeLakeEntrance: 524,
    LocationName.DeepAHSmallerBoulderByLake: 525,
    LocationName.DeepAHInsideGPCFenceSouthEast: 526,
}

# Reception Area
CARE_DEEP_ARROWHEAD_CHECKS: Dict[str, int] = {
    LocationName.DeepAHMineshaftBear: 527,
    LocationName.DeepAHShallowWaterEast: 528,
    LocationName.DeepAHShallowWaterWest: 529,
    LocationName.DeepAHCollapsedCave: 530,
    LocationName.DeepAHFireplaceTree: 531,
    LocationName.DeepAHSouthOfTrailer: 532,
    LocationName.DeepAHEastOfTrailer: 533,
    LocationName.DeepAHGraveyardTree: 534,
    LocationName.DeepAHInFrontOfGraveyard: 535,
    LocationName.DeepAHGraveyardCorner: 536,
    LocationName.DeepAHWestOfCampfire: 537,
    LocationName.DeepAHNorthEastOfCampfire: 538,
    LocationName.DeepAHMineshaftLowerEntrance: 539,
    LocationName.DeepAHByStumpCARE: 540,
    LocationName.DeepAHWaterfallRiverSplit: 541,
    LocationName.DeepAHLogHillInFront: 542,
    LocationName.DeepAHLogHillTop: 543,
    LocationName.DeepAHBelowTightropePlatform: 544,
}

# Lake and Boathouse
CABH_DEEP_ARROWHEAD_CHECKS: Dict[str, int] = {
    LocationName.DeepAHByStumpCABH: 545,
    LocationName.DeepAHLakeShore: 546,
    LocationName.DeepAHBathysphereRock: 547,
    LocationName.DeepAHGPCTunnelEntrance: 548,
    LocationName.DeepAHRockWallUpper: 549,
    LocationName.DeepAHBoathouseEntrance: 550,
    LocationName.DeepAHRightOfEntrance: 551,
}

DEEP_ARROWHEAD_LOCATIONS: Dict[str, int] = {
    **CAGP_DEEP_ARROWHEAD_CHECKS,
    **CAMA_DEEP_ARROWHEAD_CHECKS,
    **CARE_DEEP_ARROWHEAD_CHECKS,
    **CABH_DEEP_ARROWHEAD_CHECKS,
}

# Mental Cobweb locations.
# These are not included in PsychoRando seed generation so the IDs must be greater than all locations which are included
# in PsychoRando seed generation.
# The Cobwebs for each level are ordered by their internal names in Psychonauts, so sometimes the order of the Cobwebs
# is a bit weird.
BB_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebTrapezeCobweb: 552,
    LocationName.CobwebTightropeTutorial: 553,
    LocationName.CobwebGrindrailWall: 554,
    LocationName.CobwebBunnyRoomDoor: 555,
    LocationName.CobwebTunnelOfLogsEnd: 556,
}

SA_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebBlockArchLeft: 557,
    LocationName.CobwebBlockArchRight: 558,
    LocationName.CobwebBackOfShoeboxTower: 559,
    LocationName.CobwebShoeboxTower: 560,
    LocationName.CobwebFlameTowerArch: 561,
}

MI_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebIntroStatueCorner: 562,
    LocationName.CobwebBehindPinballLadder: 563,
    LocationName.CobwebGrindrailRings: 564,
    LocationName.CobwebFanRoomEntrance: 565,
    LocationName.CobwebPartyRoomFloor: 566,
}

BT_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebBathtubDrain: 567,
    LocationName.CobwebForestPathThorns: 568,
    LocationName.CobwebForestHighPlatform: 569,
    LocationName.CobwebShadowMonsterMeat: 570,
    LocationName.CobwebThornTowerRight: 571,
}

LO_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebSkyscraperBeforeDam: 572,
    LocationName.CobwebSkyscrapersBeforeTunnel: 573,
    LocationName.CobwebBehindLasers: 574,
    LocationName.CobwebEndOfDam: 575,
    LocationName.CobwebGroundAfterBridge: 576,
}

MM_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebThirdHouse: 577,
    LocationName.CobwebPostOfficeLobby: 578,
    LocationName.CobwebRightHouseBeforePostOffice: 579,
    LocationName.CobwebWebbedGarage: 580,
    LocationName.CobwebBookDepository: 581,
}

TH_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebBackstageCorridor: 582,
    LocationName.CobwebBelowTeleporter: 583,
    LocationName.CobwebStorageRoomLeft: 584,
    LocationName.CobwebInTheAudience: 585,
    LocationName.CobwebBelowTheCritic: 586,
    LocationName.CobwebBehindStage: 587,
    LocationName.CobwebStorageRoomRight: 588,
}

WW_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebBeneathSmallArch: 589,
    LocationName.CobwebBlacksmithsRightBuildingWindow: 590,
    LocationName.CobwebBlacksmithsLeftBuilding: 591,
    LocationName.CobwebBlacksmithsRightBuildingRoof: 592,
    LocationName.CobwebCarpentersHouse: 593,
    LocationName.CobwebFredsHouseBasement: 594,
    LocationName.CobwebUnderTheGuillotine: 595,
}

BV_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebDiegosHouseGrindrail: 596,
    LocationName.CobwebDiegosHouse: 597,
    LocationName.CobwebSewerShowerTunnel: 598,
    LocationName.CobwebAboveQueenOfHearts: 599,
    LocationName.CobwebSewerBeforeGate: 600,
    LocationName.CobwebDiegosHouseFireplace: 601,
    LocationName.CobwebNearDiegosHouse: 602,
}

MC_COBWEB_CHECKS: Dict[str, int] = {
    LocationName.CobwebTunnelOfLoveOllieEscortExit: 603,
    LocationName.CobwebEntranceHall1: 604,
    LocationName.CobwebEntranceHall2: 605,
}

MENTAL_COBWEB_LOCATIONS: Dict[str, int] = {
    **BB_COBWEB_CHECKS,
    **SA_COBWEB_CHECKS,
    **MI_COBWEB_CHECKS,
    **BT_COBWEB_CHECKS,
    **LO_COBWEB_CHECKS,
    **MM_COBWEB_CHECKS,
    **TH_COBWEB_CHECKS,
    **WW_COBWEB_CHECKS,
    **BV_COBWEB_CHECKS,
    **MC_COBWEB_CHECKS,
}

# Rank up rewards, broken into groups of 20 each
# 2-20
RANK_20_CHECKS: Dict[str, int] = {
    LocationName.PSIRank02: 606,
    LocationName.PSIRank03: 607,
    LocationName.PSIRank04: 608,
    LocationName.PSIRank05: 609,
    LocationName.PSIRank06: 610,
    LocationName.PSIRank07: 611,
    LocationName.PSIRank08: 612,
    LocationName.PSIRank09: 613,
    LocationName.PSIRank10: 614,
    LocationName.PSIRank11: 615,
    LocationName.PSIRank12: 616,
    LocationName.PSIRank13: 617,
    LocationName.PSIRank14: 618,
    LocationName.PSIRank15: 619,
    LocationName.PSIRank16: 620,
    LocationName.PSIRank17: 621,
    LocationName.PSIRank18: 622,
    LocationName.PSIRank19: 623,
    LocationName.PSIRank20: 624,
}

# 21-40
RANK_40_CHECKS: Dict[str, int] = {
    LocationName.PSIRank21: 625,
    LocationName.PSIRank22: 626,
    LocationName.PSIRank23: 627,
    LocationName.PSIRank24: 628,
    LocationName.PSIRank25: 629,
    LocationName.PSIRank26: 630,
    LocationName.PSIRank27: 631,
    LocationName.PSIRank28: 632,
    LocationName.PSIRank29: 633,
    LocationName.PSIRank30: 634,
    LocationName.PSIRank31: 635,
    LocationName.PSIRank32: 636,
    LocationName.PSIRank33: 637,
    LocationName.PSIRank34: 638,
    LocationName.PSIRank35: 639,
    LocationName.PSIRank36: 640,
    LocationName.PSIRank37: 641,
    LocationName.PSIRank38: 642,
    LocationName.PSIRank39: 643,
    LocationName.PSIRank40: 644,
}

# 41-60
RANK_60_CHECKS: Dict[str, int] = {
    LocationName.PSIRank41: 645,
    LocationName.PSIRank42: 646,
    LocationName.PSIRank43: 647,
    LocationName.PSIRank44: 648,
    LocationName.PSIRank45: 649,
    LocationName.PSIRank46: 650,
    LocationName.PSIRank47: 651,
    LocationName.PSIRank48: 652,
    LocationName.PSIRank49: 653,
    LocationName.PSIRank50: 654,
    LocationName.PSIRank51: 655,
    LocationName.PSIRank52: 656,
    LocationName.PSIRank53: 657,
    LocationName.PSIRank54: 658,
    LocationName.PSIRank55: 659,
    LocationName.PSIRank56: 660,
    LocationName.PSIRank57: 661,
    LocationName.PSIRank58: 662,
    LocationName.PSIRank59: 663,
    LocationName.PSIRank60: 664,
}

#61-80
RANK_80_CHECKS: Dict[str, int] = {
    LocationName.PSIRank61: 665,
    LocationName.PSIRank62: 666,
    LocationName.PSIRank63: 667,
    LocationName.PSIRank64: 668,
    LocationName.PSIRank65: 669,
    LocationName.PSIRank66: 670,
    LocationName.PSIRank67: 671,
    LocationName.PSIRank68: 672,
    LocationName.PSIRank69: 673,
    LocationName.PSIRank70: 674,
    LocationName.PSIRank71: 675,
    LocationName.PSIRank72: 676,
    LocationName.PSIRank73: 677,
    LocationName.PSIRank74: 678,
    LocationName.PSIRank75: 679,
    LocationName.PSIRank76: 680,
    LocationName.PSIRank77: 681,
    LocationName.PSIRank78: 682,
    LocationName.PSIRank79: 683,
    LocationName.PSIRank80: 684,
}

# 80-101
RANK_101_CHECKS: Dict[str, int] = {
    LocationName.PSIRank81: 685,
    LocationName.PSIRank82: 686,
    LocationName.PSIRank83: 687,
    LocationName.PSIRank84: 688,
    LocationName.PSIRank85: 689,
    LocationName.PSIRank86: 690,
    LocationName.PSIRank87: 691,
    LocationName.PSIRank88: 692,
    LocationName.PSIRank89: 693,
    LocationName.PSIRank90: 694,
    LocationName.PSIRank91: 695,
    LocationName.PSIRank92: 696,
    LocationName.PSIRank93: 697,
    LocationName.PSIRank94: 698,
    LocationName.PSIRank95: 699,
    LocationName.PSIRank96: 700,
    LocationName.PSIRank97: 701,
    LocationName.PSIRank98: 702,
    LocationName.PSIRank99: 703,
    LocationName.PSIRank100: 704,
    LocationName.PSIRank101: 705,
}

# Repeating just every five ranks, not all of them
FIVE_RANK_20_CHECKS: Dict[str, int] = {
    LocationName.PSIRank05: 609,
    LocationName.PSIRank10: 614,
    LocationName.PSIRank15: 619,
    LocationName.PSIRank20: 624,
}

FIVE_RANK_40_CHECKS: Dict[str, int] = {
    LocationName.PSIRank25: 629,
    LocationName.PSIRank30: 634,
    LocationName.PSIRank35: 639,
    LocationName.PSIRank40: 644,
}

FIVE_RANK_60_CHECKS: Dict[str, int] = {
    LocationName.PSIRank45: 649,
    LocationName.PSIRank50: 654,
    LocationName.PSIRank55: 659,
    LocationName.PSIRank60: 664,
}

FIVE_RANK_80_CHECKS: Dict[str, int] = {
    LocationName.PSIRank65: 669,
    LocationName.PSIRank70: 674,
    LocationName.PSIRank75: 679,
    LocationName.PSIRank80: 684,
}

FIVE_RANK_101_CHECKS: Dict[str, int] = {
    LocationName.PSIRank85: 689,
    LocationName.PSIRank90: 694,
    LocationName.PSIRank95: 699,
    LocationName.PSIRank101: 705,
}

FIVE_RANK_LOCATIONS: Dict[str, int] = {
    **FIVE_RANK_20_CHECKS,
    **FIVE_RANK_40_CHECKS,
    **FIVE_RANK_60_CHECKS,
    **FIVE_RANK_80_CHECKS,
    **FIVE_RANK_101_CHECKS,
}

RANK_LOCATIONS: Dict[str, int] = {
    **RANK_20_CHECKS,
    **RANK_40_CHECKS,
    **RANK_60_CHECKS,
    **RANK_80_CHECKS,
    **RANK_101_CHECKS,
}

# Figment Percentage Locations
# One location sent for every 20 percent of figments found within a level
BB_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.BBFigments20: 706,
    LocationName.BBFigments40: 707,
    LocationName.BBFigments60: 708,
    LocationName.BBFigments80: 709,
    LocationName.BBFigments100: 710,
}

SA_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.SAFigments20: 711,
    LocationName.SAFigments40: 712,
    LocationName.SAFigments60: 713,
    LocationName.SAFigments80: 714,
    LocationName.SAFigments100: 715,
}

MI_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.MIFigments20: 716,
    LocationName.MIFigments40: 717,
    LocationName.MIFigments60: 718,
    LocationName.MIFigments80: 719,
    LocationName.MIFigments100: 720,
}

BT_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.NIFigments20: 721,
    LocationName.NIFigments40: 722,
    LocationName.NIFigments60: 723,
    LocationName.NIFigments80: 724,
    LocationName.NIFigments100: 725,
}

LO_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.LOFigments20: 726,
    LocationName.LOFigments40: 727,
    LocationName.LOFigments60: 728,
    LocationName.LOFigments80: 729,
    LocationName.LOFigments100: 730,
}

MM_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.MMFigments20: 731,
    LocationName.MMFigments40: 732,
    LocationName.MMFigments60: 733,
    LocationName.MMFigments80: 734,
    LocationName.MMFigments100: 735,
}

TH_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.THFigments20: 736,
    LocationName.THFigments40: 737,
    LocationName.THFigments60: 738,
    LocationName.THFigments80: 739,
    LocationName.THFigments100: 740,
}

WW_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.WWFigments20: 741,
    LocationName.WWFigments40: 742,
    LocationName.WWFigments60: 743,
    LocationName.WWFigments80: 744,
    LocationName.WWFigments100: 745,
}

BV_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.BVFigments20: 746,
    LocationName.BVFigments40: 747,
    LocationName.BVFigments60: 748,
    LocationName.BVFigments80: 749,
    LocationName.BVFigments100: 750,
}

MC_FIGMENT_CHECKS: Dict[str, int] = {
    LocationName.MCFigments20: 751,
    LocationName.MCFigments40: 752,
    LocationName.MCFigments60: 753,
    LocationName.MCFigments80: 754,
    LocationName.MCFigments100: 755,
}

FIGMENT_LOCATIONS: Dict[str, int] = {
    **BB_FIGMENT_CHECKS,
    **SA_FIGMENT_CHECKS,
    **MI_FIGMENT_CHECKS,
    **BT_FIGMENT_CHECKS,
    **LO_FIGMENT_CHECKS,
    **MM_FIGMENT_CHECKS,
    **TH_FIGMENT_CHECKS,
    **WW_FIGMENT_CHECKS,
    **BV_FIGMENT_CHECKS,
    **MC_FIGMENT_CHECKS,
}

# Includes locations that may not be enabled.
ALL_FILLABLE_LOCATIONS: Dict[str, int] = {
    **CA_CHECKS,
    **AS_CHECKS,
    **BB_CHECKS,
    **SA_CHECKS,
    **MI_CHECKS,
    **NI_CHECKS,
    **LO_CHECKS,
    **MM_CHECKS,
    **TH_CHECKS,
    **WW_CHECKS,
    **BV_CHECKS,
    **MC_CHECKS,
    **DEEP_ARROWHEAD_LOCATIONS,
    **MENTAL_COBWEB_LOCATIONS,
    **RANK_LOCATIONS,
    **FIGMENT_LOCATIONS,
}

ALL_LOCATIONS: Dict[str, int] = {
    **ALL_FILLABLE_LOCATIONS,
    **EVENT_LOCATIONS,
}

# Locations which do not place items into the game world. When such a location contains a local item, the AP server will
# tell the client to receive the item and the client will send the item to Psychonauts as if the item was non-locally
# placed.
_FULLY_REMOTE_LOCATION_IDS: Set[int] = {
    *DEEP_ARROWHEAD_LOCATIONS.values(),
    *MENTAL_COBWEB_LOCATIONS.values(),
    *RANK_LOCATIONS.values(),
}
# IDs of locations that place items into the game world, and are therefore used in PsychoSeed generation.
PSYCHOSEED_LOCATION_IDS: Set[int] = set(ALL_FILLABLE_LOCATIONS.values())
PSYCHOSEED_LOCATION_IDS.difference_update(_FULLY_REMOTE_LOCATION_IDS)

# Offset added to Psychonauts IDs to produce AP IDs.
AP_LOCATION_OFFSET = 42690000
