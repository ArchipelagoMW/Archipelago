from .Names import LocationName

# eventid matches Randomizer Seed index in table
CA_CHECKS = {
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

    # only if cobwebduster is vanilla
    # LocationName.ShopCobwebDuster: 366,
}

RANK_CHECKS = {
    LocationName.PSIRank05: 111,
    LocationName.PSIRank10: 112,
    LocationName.PSIRank15: 113,
    LocationName.PSIRank20: 114,
    LocationName.PSIRank25: 115,
    LocationName.PSIRank30: 116,
    LocationName.PSIRank35: 117,
    LocationName.PSIRank40: 118,
    LocationName.PSIRank45: 119,
    LocationName.PSIRank50: 120,
    LocationName.PSIRank55: 121,
    LocationName.PSIRank60: 122,
    LocationName.PSIRank65: 123,
    LocationName.PSIRank70: 124,
    LocationName.PSIRank75: 125,
    LocationName.PSIRank80: 126,
    LocationName.PSIRank85: 127,
    LocationName.PSIRank90: 128,
    LocationName.PSIRank95: 129,
    LocationName.PSIRank101: 130,
}

AS_CHECKS = {
    LocationName.RockWallBottom: 131,
    LocationName.RockWallLadder: 132,
    LocationName.OutsideFrontGate: 133,
    LocationName.PillarAboveGate: 134,
    LocationName.FountainTop: 135,
    LocationName.HedgeAlcove: 136,
    LocationName.AsylumDoorsRight: 137,
    LocationName.AsylumDoorsLeft: 138,
    LocationName.CornerNearFence: 139,
    LocationName.LedgeBeforeGloria: 140,
    LocationName.AboveElevator: 141,
    LocationName.CrowsBasket: 142,
    LocationName.LedgeAboveFredLeft: 143,
    LocationName.LedgeAboveFredRight: 144,
    LocationName.LedgeOppositeElevator: 145,
    LocationName.EdgarsRoom: 146,
    LocationName.BehindElevator: 147,
    LocationName.JunkCorner: 148,
    LocationName.AboveEdgar: 149,
    LocationName.BehindMattressWall: 150,
    LocationName.CheckeredBathroom: 151,
    LocationName.RoomNearCheckeredBathroom: 152,
    LocationName.ElevatorShaft: 153,
    LocationName.RoomLeftOfPipeSlide: 154,
    LocationName.FloatingInHole: 155,
    LocationName.NextToHole: 156,
    LocationName.CrumblingOuterWallPlanks: 157,
    LocationName.CrumblingOuterWallPillar: 158,
    LocationName.CrumblingOuterWallBelowPlatform: 159,
    LocationName.CrumblingOuterWallPlatform: 160,
    LocationName.RoomAboveTiltedStairs: 161,
    LocationName.AcidRoomFloor: 162,
    LocationName.AcidRoomTable: 163,
    LocationName.AcidRoomWindow: 164,
    LocationName.AcidRoomOverhang: 165,
    LocationName.SmallWindowsLedge: 166,
    LocationName.RoundWoodPlatform: 167,
    LocationName.GrateClimbBottom: 168,
    LocationName.GrateClimbMid: 169,
    LocationName.SinkPlatformLeft: 170,
    LocationName.SinkPlatformRight: 171,
    LocationName.PipesBelowChairDoor: 172,
    LocationName.RoomOppositeChairDoor: 173,
    LocationName.PipeSlideNearChairDoor: 174,
    LocationName.RaftersAboveChairDoor: 175,
    LocationName.LabCagedCrowLeft: 176,
    LocationName.LabCagedCrowRight: 177,
    LocationName.NextToPokeylope: 178,
    LocationName.LabTopRailingLeft1: 179,
    LocationName.LabTopRailingLeft2: 180,
    LocationName.LabTopElevator: 181,
    LocationName.LabTopRailingRight: 182,
    LocationName.TeaRoom: 183,

}

BB_CHECKS = {
    LocationName.JumpingTutorial1: 184,
    LocationName.JumpingTutorial2: 185,
    LocationName.PoleClimbingTutorialFloor: 186,
    LocationName.BelowTheTripleTrampolines: 187,
    LocationName.GiantSoldierCutOut: 188,
    LocationName.DodgingBullets1: 189,
    LocationName.DodgingBullets2: 190,
    LocationName.MachineGunTurret: 191,
    LocationName.PoleSwingingTutorial: 192,
    LocationName.TrapezeCobweb: 193,
    LocationName.TrapezePlatform: 194,
    LocationName.InsidePlaneWreckage: 195,
    LocationName.EndOfObstacleCourseLeft: 196,
    LocationName.EndOfObstacleCourseRight: 197,
    LocationName.BasicBrainingComplete: 198,
}

SA_CHECKS = {
    LocationName.OnTheBed: 199,
    LocationName.OnThePillow: 200,
    LocationName.BuildingBlocksLeft: 201,
    LocationName.BuildingBlocksBelow: 202,
    LocationName.BuildingBlocksRight: 203,
    LocationName.TopOfBedFrame: 204,
    LocationName.RoundPlatformsBottom: 205,
    LocationName.RoundPlatformsNearValve: 206,
    LocationName.RoundPlatformsFarFromValve: 207,
    LocationName.SideOfCubeFace3: 208,
    LocationName.BottomOfShoeboxLadder: 209,
    LocationName.ShoeboxPedestal: 210,
    LocationName.ShoeboxTowerTop: 211,
    LocationName.FlameTowerSteps: 212,
    LocationName.FlameTowerTop1: 213,
    LocationName.FlameTowerTop2: 214,
    LocationName.SashasShootingGalleryComplete: 215,

}

MI_CHECKS = {
    LocationName.IntroRingsTutorial: 216,
    LocationName.DancingCamperPlatform1: 217,
    LocationName.DemonRoom: 218,
    LocationName.WindyLadderBottom: 219,
    LocationName.PinballPlunger: 220,
    LocationName.PlungerPartyLedge: 221,
    LocationName.GrindrailRings: 222,
    LocationName.CensorHallway: 223,
    LocationName.PinkBowlBottom: 224,
    LocationName.PinkBowlSmallPlatform: 225,
    LocationName.BubblyFanBottom: 226,
    LocationName.BubblyFanPlatform: 227,
    LocationName.BubblyFanTop: 228,
    LocationName.MillasPartyRoom: 229,
    LocationName.MillasDancePartyComplete: 230,
}

NI_CHECKS = {
    LocationName.OutsideCaravan: 231,
    LocationName.BehindTheEgg: 232,
    LocationName.ShadowMonsterPath: 233,
    LocationName.ShadowMonsterBlueMushrooms: 234,
    LocationName.LedgeBehindShadowMonster: 235,
    LocationName.BelowTheSteepLedge: 236,
    LocationName.ForestPathBlueMushrooms: 237,
    LocationName.ForestBlueLedge: 238,
    LocationName.ForestHighPlatform: 239,
    LocationName.ForestPathThorns: 240,
    LocationName.BehindThornTowerLeft: 241,
    LocationName.BehindThornTowerMid: 242,
    LocationName.BehindThornTowerRight: 243,
    LocationName.BrainTumblerExperimentComplete: 244,

}

LO_CHECKS = {
    LocationName.SkyscraperStart: 245,
    LocationName.CornerNearJail: 246,
    LocationName.SkyscraperBeforeDam: 247,
    LocationName.BehindLasersLeft1: 248,
    LocationName.BehindLasersLeft2: 249,
    LocationName.BehindLasersRight: 250,
    LocationName.BlimpHop: 251,
    LocationName.EndOfDam: 252,
    LocationName.EndOfDamPlatform: 253,
    LocationName.SkyscraperAfterDam: 254,
    LocationName.NearBattleships: 255,
    LocationName.OnTheBridge: 256,
    LocationName.GroundAfterBridge: 257,
    LocationName.SkyscraperAfterBridge: 258,
    LocationName.TunnelSuitcaseTag: 259,
    LocationName.FinalSkyscrapersLeft: 260,
    LocationName.FinalSkyscrapersRight: 261,
    LocationName.KochamaraIntroLeft: 262,
    LocationName.KochamaraIntroRight: 263,
    LocationName.LungfishopolisComplete: 264,

}

MM_CHECKS = {
    LocationName.BoydsFridgeClv: 265,
    LocationName.FirstHouseDufflebagTag: 266,
    LocationName.SecondHouseRollingPin: 267,
    LocationName.CarTrunk1StopSign: 268,
    LocationName.RoofAfterRoadCrewPurseTag: 269,
    LocationName.CarTrunk2HedgeTrimmers: 270,
    LocationName.CarHouseBackyardSteamertrunkTag: 271,
    LocationName.InsideWebbedGarageHatbox: 272,
    LocationName.GraveyardPatioVault: 273,
    LocationName.GraveyardBehindTreeOneUp: 274,
    LocationName.BehindGraveyardDufflebag: 275,
    LocationName.HedgeMazeFlowers: 276,
    LocationName.CarTrunk3WateringCan: 277,
    LocationName.PostOfficeRoofOneUp: 278,
    LocationName.PostOfficeLobbySuitcase: 279,
    LocationName.PostOfficeBasementPlunger: 280,
    LocationName.LandscapersHouseBackyardSuitcaseTag: 281,
    LocationName.LandscapersHouseTablePurse: 282,
    LocationName.LandscapersHouseKitchenAmmoUp: 283,
    LocationName.PowerlineIslandSandboxHatboxTag: 284,
    LocationName.PowerlineIslandLeftMemoryVault: 285,
    LocationName.PowerlineIslandRightMaxLives: 286,
    LocationName.BehindBookDepositorySteamerTrunk: 287,
    LocationName.MilkmanComplete: 288,

}

TH_CHECKS = {
    LocationName.NearTheCriticPurse: 289,
    LocationName.InTheAudienceAmmoUp: 290,
    LocationName.BelowTheSpotlightSteamertrunkTag: 291,
    LocationName.BehindStagePurseTag: 292,
    LocationName.BehindStageCobwebSuitcase: 293,
    LocationName.StorageRoomFloorVault: 294,
    LocationName.StorageRoomLeftSteamertrunk: 295,
    LocationName.StorageRoomRightLowerSuitcaseTag: 296,
    LocationName.StorageRoomRightUpperCandle1: 297,
    LocationName.BonitasRoom: 298,
    LocationName.DoghouseSlicersDufflebagTag: 299,
    LocationName.BigPlatform1Hatbox: 300,
    LocationName.BigPlatform2Vault: 301,
    LocationName.BigPlatform3OneUp: 302,
    LocationName.BigPlatformAboveHatboxTag: 303,
    LocationName.NextToOatmealDufflebag: 304,
    LocationName.CandleBasketCandle2: 305,
    LocationName.CurtainSlideConfusionAmmoUp: 306,
    LocationName.GloriasTheaterComplete: 307,

}

WW_CHECKS = {
    LocationName.FredsRoomHatboxTag: 308,
    LocationName.TheFireplacePricelessCoin: 309,
    LocationName.GameBoardSuitcaseTag: 310,
    LocationName.CarpentersRoofVault: 311,
    LocationName.TightropeRoomDufflebag: 312,
    LocationName.OutsideVillager1HouseOneUp: 313,
    LocationName.SmallArchTopMaxLives: 314,
    LocationName.SmallArchBelowPurseTag: 315,
    LocationName.TopOfVillager2sHouseDufflebagTag: 316,
    LocationName.TopOfVillager3sHouseAmmoUp: 317,
    LocationName.TopOfKnightsHouseConfusionAmmoUp: 318,
    LocationName.CastleTowerOneUp: 319,
    LocationName.CastleInsideVault: 320,
    LocationName.CastleWallSteamertrunk: 321,
    LocationName.UnderTheGuillotineSuitcase: 322,
    LocationName.FredsHouseBasementHatbox: 323,

    LocationName.BlacksmithsLeftBuildingPurse: 324,
    LocationName.BlacksmithsRightBuildingSteamertrunkTag: 325,
    LocationName.BlacksmithsHaybaleTheMusket: 326,
    LocationName.HelpTheCarpenter: 327,
    LocationName.HelpVillager1: 328,
    LocationName.HelpTheKnight: 329,
    LocationName.HelpVillager2: 330,
    LocationName.HelpVillager3: 331,
    LocationName.WaterlooWorldComplete: 332,

}

BV_CHECKS = {
    LocationName.ClubStreetLadySteamertrunk: 333,
    LocationName.ClubStreetMetalBalconyDufflebagTag: 334,
    LocationName.HeartStreetHIGHBalconyAmmoUp: 335,
    LocationName.AlleywaysLedgeHatboxTag: 336,
    LocationName.SewersMainVault: 337,
    LocationName.ClubStreetGatedSteamerTrunkTag: 338,
    LocationName.BurnTheLogsDufflebag: 339,

    LocationName.TheGardenVault: 340,
    LocationName.NearDiegosHouseMaxLives: 341,
    LocationName.DiegosBedSuitcaseTag: 342,
    LocationName.DiegosHouseGrindrailSuitcase: 343,
    LocationName.DiegosRoomHatbox: 344,
    LocationName.GrindrailBalconyConfusionAmmoUp: 345,
    LocationName.SanctuaryBalconyPurseTag: 346,

    LocationName.SanctuaryGroundPurse: 347,
    LocationName.TigerWrestler: 348,
    LocationName.DragonWrestler: 349,
    LocationName.EagleWrestler: 350,
    LocationName.CobraWrestler: 351,
    LocationName.BlackVelvetopiaComplete: 352,

}

MC_CHECKS = {
    LocationName.EntranceAwningSteamertrunkTag: 353,
    LocationName.CrumblingPathSteamertrunk: 354,
    LocationName.CrumblingPathEndRightHatboxTag: 355,
    LocationName.CrumblingPathEndLeftConfusionAmmoUp: 356,
    LocationName.OllieEscortFloorSuitcaseTag: 357,
    LocationName.OllieEscortMiddleHatbox: 358,
    LocationName.OllieEscortTopLeftVault: 359,
    LocationName.OllieEscortTopRightPurseTag: 360,
    LocationName.TunnelOfLoveStartPurse: 361,
    LocationName.TunnelOfLoveCornerSuitcase: 362,
    LocationName.TunnelOfLoveRailDufflebagTag: 363,
    LocationName.NextToTheFatLadyDufflebag: 364,
}

# Leave a gap in the IDs so that more locations can be added that place items into the game world without having to
# adjust the IDs of all locations that don't place items into the game world.
EVENT_LOCATIONS = {
    # for beating Meat Circus
    LocationName.FinalBossEvent: 500,
    # for Brain Jar Goal
    LocationName.RedeemedBrainsEvent: 501,
    # for Coach Oleander Brain Tank Boss
    LocationName.OleanderBossEvent: 502,
}

# Deep Arrowhead locations.
# These are not included in PsychoRando seed generation so the IDs must be greater than all locations which are included
# in PsychoRando seed generation.
# Main Campgrounds
CAMA_DEEP_ARROWHEAD_CHECKS = {
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
CAGP_DEEP_ARROWHEAD_CHECKS = {
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
CARE_DEEP_ARROWHEAD_CHECKS = {
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
CABH_DEEP_ARROWHEAD_CHECKS = {
    LocationName.DeepAHByStumpCABH: 545,
    LocationName.DeepAHLakeShore: 546,
    LocationName.DeepAHBathysphereRock: 547,
    LocationName.DeepAHGPCTunnelEntrance: 548,
    LocationName.DeepAHRockWallUpper: 549,
    LocationName.DeepAHBoathouseEntrance: 550,
    LocationName.DeepAHRightOfEntrance: 551,
}

DEEP_ARROWHEAD_LOCATIONS = {
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
BB_COBWEB_CHECKS = {
    LocationName.CobwebTrapezeCobweb: 552,
    LocationName.CobwebTightropeTutorial: 553,
    LocationName.CobwebGrindrailWall: 554,
    LocationName.CobwebBunnyRoomDoor: 555,
    LocationName.CobwebTunnelOfLogsEnd: 556,
}

SA_COBWEB_CHECKS = {
    LocationName.CobwebBlockArchLeft: 557,
    LocationName.CobwebBlockArchRight: 558,
    LocationName.CobwebBackOfShoeboxTower: 559,
    LocationName.CobwebShoeboxTower: 560,
    LocationName.CobwebFlameTowerArch: 561,
}

MI_COBWEB_CHECKS = {
    LocationName.CobwebIntroStatueCorner: 562,
    LocationName.CobwebBehindPinballLadder: 563,
    LocationName.CobwebGrindrailRings: 564,
    LocationName.CobwebFanRoomEntrance: 565,
    LocationName.CobwebPartyRoomFloor: 566,
}

BT_COBWEB_CHECKS = {
    LocationName.CobwebBathtubDrain: 567,
    LocationName.CobwebForestPathThorns: 568,
    LocationName.CobwebForestHighPlatform: 569,
    LocationName.CobwebShadowMonsterMeat: 570,
    LocationName.CobwebThornTowerRight: 571,
}

LO_COBWEB_CHECKS = {
    LocationName.CobwebSkyscraperBeforeDam: 572,
    LocationName.CobwebSkyscrapersBeforeTunnel: 573,
    LocationName.CobwebBehindLasers: 574,
    LocationName.CobwebEndOfDam: 575,
    LocationName.CobwebGroundAfterBridge: 576,
}

MM_COBWEB_CHECKS = {
    LocationName.CobwebThirdHouse: 577,
    LocationName.CobwebPostOfficeLobby: 578,
    LocationName.CobwebRightHouseBeforePostOffice: 579,
    LocationName.CobwebWebbedGarage: 580,
    LocationName.CobwebBookDepository: 581,
}

TH_COBWEB_CHECKS = {
    LocationName.CobwebBackstageCorridor: 582,
    LocationName.CobwebBelowTeleporter: 583,
    LocationName.CobwebStorageRoomLeft: 584,
    LocationName.CobwebInTheAudience: 585,
    LocationName.CobwebBelowTheCritic: 586,
    LocationName.CobwebBehindStage: 587,
    LocationName.CobwebStorageRoomRight: 588,
}

WW_COBWEB_CHECKS = {
    LocationName.CobwebBeneathSmallArch: 589,
    LocationName.CobwebBlacksmithsRightBuildingWindow: 590,
    LocationName.CobwebBlacksmithsLeftBuilding: 591,
    LocationName.CobwebBlacksmithsRightBuildingRoof: 592,
    LocationName.CobwebCarpentersHouse: 593,
    LocationName.CobwebFredsHouseBasement: 594,
    LocationName.CobwebUnderTheGuillotine: 595,
}

BV_COBWEB_CHECKS = {
    LocationName.CobwebDiegosHouseGrindrail: 596,
    LocationName.CobwebDiegosHouse: 597,
    LocationName.CobwebSewerShowerTunnel: 598,
    LocationName.CobwebAboveQueenOfHearts: 599,
    LocationName.CobwebSewerBeforeGate: 600,
    LocationName.CobwebDiegosHouseFireplace: 601,
    LocationName.CobwebNearDiegosHouse: 602,
}

MC_COBWEB_CHECKS = {
    LocationName.CobwebTunnelOfLoveOllieEscortExit: 603,
    LocationName.CobwebEntranceHall1: 604,
    LocationName.CobwebEntranceHall2: 605,
}

MENTAL_COBWEB_LOCATIONS = {
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

# Includes locations that may not be enabled.
ALL_FILLABLE_LOCATIONS = {
    **CA_CHECKS,
    **RANK_CHECKS,
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
    **MENTAL_COBWEB_LOCATIONS
}

ALL_LOCATIONS = {
    **ALL_FILLABLE_LOCATIONS,
    **EVENT_LOCATIONS,
}

# Locations which do not place items into the game world. When such a location contains a local item, the AP server will
# tell the client to receive the item and the client will send the item to Psychonauts as if the item was non-locally
# placed.
_FULLY_REMOTE_LOCATION_IDS = {
    *DEEP_ARROWHEAD_LOCATIONS.values(),
    *MENTAL_COBWEB_LOCATIONS.values()
}
# IDs of locations that place items into the game world, and are therefore used in PsychoSeed generation.
PSYCHOSEED_LOCATION_IDS = set(ALL_FILLABLE_LOCATIONS.values())
PSYCHOSEED_LOCATION_IDS.difference_update(_FULLY_REMOTE_LOCATION_IDS)

# Offset added to Psychonauts IDs to produce AP IDs.
AP_LOCATION_OFFSET = 42690000
