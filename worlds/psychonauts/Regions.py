from typing import Dict, Set, Iterable, TYPE_CHECKING

if TYPE_CHECKING:
    from . import PSYWorld

from BaseClasses import MultiWorld, Region

from .Names import RegionName, ItemName
from .Subclasses import PSYLocation
from .Locations import (
    ALL_LOCATIONS,
    AP_LOCATION_OFFSET,
    CAGP_DEEP_ARROWHEAD_CHECKS,
    CAMA_DEEP_ARROWHEAD_CHECKS,
    CARE_DEEP_ARROWHEAD_CHECKS,
    CABH_DEEP_ARROWHEAD_CHECKS,
    BB_COBWEB_CHECKS,
    SA_COBWEB_CHECKS,
    MI_COBWEB_CHECKS,
    BT_COBWEB_CHECKS,
    LO_COBWEB_CHECKS,
    MM_COBWEB_CHECKS,
    TH_COBWEB_CHECKS,
    WW_COBWEB_CHECKS,
    BV_COBWEB_CHECKS,
    MC_COBWEB_CHECKS,
)
from .Names import LocationName
from . import Options

DEFAULT_REGIONS = {
    # Starting region for Archipelago
    "Menu": [],

    # --- Real World ----
    # Sasha's Lab
    RegionName.CASA: [
        LocationName.BehindFurnitureCard,
        LocationName.StaircaseLedgesCard,
        LocationName.UpperLedgeFossil,
    ],

    # Wilderness and GPC
    RegionName.CAGP: [
        LocationName.TopofGPCCard,
        LocationName.UnderGPCCard,
        LocationName.MountainLionLogBridgeCard,
        LocationName.AboveEntranceLakeCard,
        LocationName.RockWallBehindTreeCard,
        LocationName.RockWallTopPirateScope,
        LocationName.TreeNearFenceCard,
        LocationName.TreeNearGeyserCard,
        LocationName.FenceBehindGPCCard,
        LocationName.NeartheBearCard,
        LocationName.RockyPlatformsBehindGPCRightCard,
        LocationName.RockyPlatformsBehindGPCLeftCard,
        LocationName.TopofLogFlumeCard,
        LocationName.RidetheLogFlumeCard,
        LocationName.BottomofLogFlumeCard,
        LocationName.BigRockNearFordCard,
        LocationName.RuinedCabinChallengeMarker,
        LocationName.BranchSwingingCourseStartCard,
        LocationName.BranchSwingingCourseMidCard,
        LocationName.BranchSwingingCourseEndChallengeMarker,
        LocationName.BranchAboveSquirrelCard,
        LocationName.CreekGrateGlassEye,
    ],
    RegionName.CAGPSquirrel: [
        LocationName.SquirrelsAcornGoldenAcorn,
    ],
    RegionName.CAGPGeyser: [
        LocationName.GeyserMinersSkull,
    ],

    # Main Campgrounds
    RegionName.CAMA: [
        LocationName.FenceNearKidsCabinsCard,
        LocationName.UnderLodgeFrontStepsCard,
        LocationName.BehindTreeNearLodgeCard,
        LocationName.UndertheLodgeGoldDoubloon,
        LocationName.Loudspeaker1PlatformCard,
        LocationName.UnderLodgeMetalRoofCard,
        LocationName.LoudspeakerTightropeWalkCard,
        LocationName.Loudspeaker2PlatformCard,
        LocationName.LodgeRoofChallengeMarker,
        LocationName.MetalRoofOutcroppingCard,
        LocationName.LoudspeakerAboveStumpCard,
        LocationName.TreePlatformLeftCard,
        LocationName.TreePlatformRightEagleClaw,
        LocationName.RockWallTopCard,
        LocationName.ParkingLotArchCard,
        LocationName.ParkingLotSmallLogCard,
        LocationName.OleandersCarCard,
        LocationName.ParkingLotBasketballHoopCard,
        LocationName.ParkingLotOuthouseCard,
        LocationName.RockNearBenchCard,
    ],
    RegionName.CAMALev: [
        LocationName.ParkingLotHistoryBoardCard,
    ],

    # Kids' Cabins
    RegionName.CAKC: [
        LocationName.GrindingontheRootsCard,
        LocationName.UnderStairsCard,
        LocationName.TopotheLoudspeakerCard,
        LocationName.CabinRoof1Card,
        LocationName.TrampolineAboveOuthouseCard,
        LocationName.TrampolinePlatformChallengeMarker,
        LocationName.CabinsOuthouseCard,
        LocationName.BehindCabinCard,
        LocationName.RoofofCabin2Card,
        LocationName.CaveEntranceCard,
        LocationName.DeepCavePathCard,
        LocationName.DeepCaveLadderCard,
    ],
    RegionName.CAKCLev: [
        LocationName.HighUpTightropeCard,
    ],
    RegionName.CAKCPyro: [
        LocationName.CaveRefrigeratorTurkeySandwich,
    ],

    # Reception Area
    RegionName.CARE: [
        LocationName.GraveyardBearCard,
        LocationName.NearBeehiveCard,
        LocationName.MineshaftTrailerEntranceCard,
        LocationName.TightropeStartCard,
        LocationName.TightropeEndCard,
        LocationName.RocksNearTrailerCard,
        LocationName.FireplaceTreeRockCard,
        LocationName.BigLogPlatformCard,
        LocationName.AboveWaterfallLeftCard,
        LocationName.AboveWaterfallRightCard,
        LocationName.BehindtheWaterfallCard,
        LocationName.WeirdTreeLeftCherryWoodPipe,
        LocationName.WeirdTreeRightCard,
        LocationName.LogHillTopCard,
        LocationName.LogHillBehindCard,
        LocationName.MineshaftGrindRailCard,
        LocationName.MineshaftUpperEntranceCard,
        LocationName.MineshaftAboveUpperEntranceCard,
        LocationName.InsideMineshaftCard,
        LocationName.MineshaftBearCard,
        LocationName.SwampBirdsNestCondorEgg,
        LocationName.CollapsedCaveChallengeMarker,
    ],
    RegionName.CARELev: [
        LocationName.FireplaceTreeLowerCard,
        LocationName.FireplaceTreeTopDinosaurBone,
        LocationName.SwampSkinnyPolesCard,

    ],
    RegionName.CAREMark: [
        LocationName.HornetNestFertilityIdol,
    ],

    # Boathouse and Lake
    RegionName.CABH: [
        LocationName.UndertheFirstBridgeCard,
        LocationName.BehindStumpCard,
        LocationName.LeftofEntranceRockWallCard,
        LocationName.PolesonLakeCard,
        LocationName.BathysphereRoofCard,
        LocationName.BathysphereDockCard,
        LocationName.MetalRoofAboveFordCard,
        LocationName.AboveFordRopesCard,
        LocationName.AboveFordCabinPlatformCard,
        LocationName.OutsideCougarCaveCard,
        LocationName.InsideCougarCaveDiversHelmet,
        LocationName.BulletinBoardBushesCard,
        LocationName.PinkTreesPlatformLeftCard,
        LocationName.PinkTreesPlatformRightCard,
        LocationName.RockWallUpperCard,
        LocationName.LakeShoreCard,
        LocationName.TinyIslandCard,
        LocationName.RockWallGapPsychonautsComic1,
        LocationName.LungfishBossComplete,
    ],
    RegionName.CABHLev: [
        LocationName.TopofBigRockChallengeMarker,
    ],

    # Main Lodge
    RegionName.CALI: [
        LocationName.MainLodgeRaftersVoodooDoll,
    ],

    # Ford's Sanctuary
    RegionName.CAJA: [
        LocationName.TopofSanctuaryCard,
        LocationName.BottomofSanctuaryCard,
    ],
    RegionName.RANK5to20: [
        LocationName.PSIRank05,
        LocationName.PSIRank10,
        LocationName.PSIRank15,
        LocationName.PSIRank20,
    ],
    RegionName.RANK25to40: [
        LocationName.PSIRank25,
        LocationName.PSIRank30,
        LocationName.PSIRank35,
        LocationName.PSIRank40,
    ],
    RegionName.RANK45to60: [
        LocationName.PSIRank45,
        LocationName.PSIRank50,
        LocationName.PSIRank55,
        LocationName.PSIRank60,
    ],
    RegionName.RANK65to80: [
        LocationName.PSIRank65,
        LocationName.PSIRank70,
        LocationName.PSIRank75,
        LocationName.PSIRank80,
    ],
    RegionName.RANK85to101: [
        LocationName.PSIRank85,
        LocationName.PSIRank90,
        LocationName.PSIRank95,
        LocationName.PSIRank101,
    ],

    # Asylum Grounds
    RegionName.ASGR: [
        LocationName.RockWallBottom,
        LocationName.RockWallLadder,
        LocationName.FountainTop,
        LocationName.HedgeAlcove,
        LocationName.AsylumDoorsRight,
        LocationName.AsylumDoorsLeft,
        LocationName.CornerNearFence,
        LocationName.LedgeBeforeGloria,
    ],
    RegionName.ASGRLev: [
        LocationName.OutsideFrontGate,
        LocationName.PillarAboveGate,
    ],

    # Asylum Courtyard
    RegionName.ASCO: [
        LocationName.AboveElevator,
        LocationName.LedgeAboveFredLeft,
        LocationName.LedgeAboveFredRight,
        LocationName.LedgeOppositeElevator,
        LocationName.EdgarsRoom,
        LocationName.BehindElevator,
        LocationName.JunkCorner,
    ],
    RegionName.ASCOLev: [
        LocationName.AboveEdgar,
    ],
    RegionName.ASCOInvis: [
        LocationName.CrowsBasket,
    ],

    # Asylum Upper Floors
    RegionName.ASUP: [
        LocationName.BehindMattressWall,
        LocationName.CheckeredBathroom,
        LocationName.RoomNearCheckeredBathroom,
        LocationName.ElevatorShaft,
        LocationName.RoomLeftOfPipeSlide,
        LocationName.FloatingInHole,
        LocationName.NextToHole,
        LocationName.CrumblingOuterWallPlanks,
        LocationName.CrumblingOuterWallPillar,
        LocationName.CrumblingOuterWallBelowPlatform,
    ],
    RegionName.ASUPLev: [
        LocationName.CrumblingOuterWallPlatform,
        LocationName.RoomAboveTiltedStairs,
        LocationName.AcidRoomFloor,
        LocationName.AcidRoomTable,
        LocationName.AcidRoomWindow,
        LocationName.AcidRoomOverhang,
        LocationName.SmallWindowsLedge,
        LocationName.RoundWoodPlatform,
        LocationName.GrateClimbBottom,
        LocationName.GrateClimbMid,
        LocationName.SinkPlatformLeft,
        LocationName.SinkPlatformRight,
        LocationName.PipesBelowChairDoor,
    ],
    RegionName.ASUPTele: [
        LocationName.RoomOppositeChairDoor,
        LocationName.PipeSlideNearChairDoor,
        LocationName.RaftersAboveChairDoor,
    ],

    # Asylum Lab
    RegionName.ASLB: [
        LocationName.LabCagedCrowLeft,
        LocationName.LabCagedCrowRight,
        LocationName.NextToPokeylope,
        LocationName.LabTopRailingLeft1,
        LocationName.LabTopRailingLeft2,
        LocationName.LabTopElevator,
        LocationName.LabTopRailingRight,
        LocationName.TeaRoom,
    ],

    # --- Mental Worlds ----
    # Basic Braining
    RegionName.BBA1: [
        LocationName.JumpingTutorial1,
        LocationName.JumpingTutorial2,
        LocationName.PoleClimbingTutorialFloor,
        LocationName.BelowTheTripleTrampolines,
    ],
    RegionName.BBA2: [
        LocationName.GiantSoldierCutOut,
        LocationName.DodgingBullets1,
        LocationName.DodgingBullets2,
        LocationName.MachineGunTurret,
        LocationName.PoleSwingingTutorial,
        LocationName.TrapezePlatform,
        LocationName.InsidePlaneWreckage,
        LocationName.EndOfObstacleCourseLeft,
        LocationName.EndOfObstacleCourseRight,
        LocationName.BasicBrainingComplete,
    ],
    RegionName.BBA2Duster: [
        LocationName.TrapezeCobweb,
    ],

    # Sasha's Shooting Gallery
    RegionName.SACU: [
        LocationName.OnTheBed,
        LocationName.OnThePillow,
        LocationName.BuildingBlocksLeft,
        LocationName.BuildingBlocksBelow,
        LocationName.BuildingBlocksRight,
        LocationName.TopOfBedFrame,
        LocationName.RoundPlatformsBottom,
        LocationName.RoundPlatformsNearValve,
        LocationName.SideOfCubeFace3,
        LocationName.BottomOfShoeboxLadder,
        LocationName.ShoeboxPedestal,
        LocationName.ShoeboxTowerTop,
        LocationName.FlameTowerSteps,
        LocationName.FlameTowerTop1,
        LocationName.FlameTowerTop2,
        LocationName.SashasShootingGalleryComplete,
    ],
    RegionName.SACULev: [
        LocationName.RoundPlatformsFarFromValve,
    ],

    # Milla's Dance Party
    RegionName.MIFL: [
        LocationName.IntroRingsTutorial,
        LocationName.DancingCamperPlatform1,
        LocationName.DemonRoom,
        LocationName.WindyLadderBottom,
        LocationName.PinballPlunger,
        LocationName.PlungerPartyLedge,
        LocationName.GrindrailRings,
        LocationName.CensorHallway,
        LocationName.PinkBowlBottom,
        LocationName.PinkBowlSmallPlatform,
        LocationName.BubblyFanBottom,
        LocationName.BubblyFanPlatform,
        LocationName.BubblyFanTop,
        LocationName.MillasPartyRoom,
        LocationName.MillasDancePartyComplete,
    ],

    # Brain Tumbler Experiment (Nightmare in the Brain Tumbler)
    RegionName.NIMP: [
        LocationName.OutsideCaravan,
        LocationName.BehindTheEgg,
        LocationName.ShadowMonsterPath,
    ],
    RegionName.NIMPMark: [
        LocationName.ShadowMonsterBlueMushrooms,
        LocationName.LedgeBehindShadowMonster,
        LocationName.BelowTheSteepLedge,
        LocationName.ForestPathBlueMushrooms,
        LocationName.ForestBlueLedge,
        LocationName.ForestHighPlatform,
        LocationName.ForestPathThorns,
        LocationName.BehindThornTowerLeft,
        LocationName.BehindThornTowerMid,
        LocationName.BehindThornTowerRight,
    ],
    RegionName.NIBA: [
        LocationName.BrainTumblerExperimentComplete,
    ],

    # Lungfishopolis
    RegionName.LOMA: [
        LocationName.SkyscraperStart,
        LocationName.CornerNearJail,
        LocationName.SkyscraperBeforeDam,
    ],
    RegionName.LOMAShield: [
        LocationName.BehindLasersLeft1,
        LocationName.BehindLasersLeft2,
        LocationName.BehindLasersRight,
        LocationName.BlimpHop,
        LocationName.EndOfDam,
        LocationName.EndOfDamPlatform,
        LocationName.SkyscraperAfterDam,
        LocationName.NearBattleships,
        LocationName.OnTheBridge,
        LocationName.GroundAfterBridge,
        LocationName.SkyscraperAfterBridge,
        LocationName.TunnelSuitcaseTag,
        LocationName.FinalSkyscrapersLeft,
        LocationName.FinalSkyscrapersRight,
        LocationName.KochamaraIntroLeft,
        LocationName.KochamaraIntroRight,
        LocationName.LungfishopolisComplete,
    ],

    # The Milkman Conspiracy
    RegionName.MMI1Fridge: [
        LocationName.BoydsFridgeClv,
    ],
    RegionName.MMI1BeforeSign: [
        LocationName.FirstHouseDufflebagTag,
        LocationName.SecondHouseRollingPin,
        LocationName.CarTrunk1StopSign,
    ],
    RegionName.MMI1AfterSign: [
        LocationName.RoofAfterRoadCrewPurseTag,
        LocationName.CarTrunk2HedgeTrimmers,
        LocationName.CarHouseBackyardSteamertrunkTag,
        LocationName.GraveyardPatioVault,
        LocationName.GraveyardBehindTreeOneUp,
        LocationName.BehindGraveyardDufflebag,
        LocationName.HedgeMazeFlowers,
        LocationName.CarTrunk3WateringCan,
        LocationName.PostOfficeRoofOneUp,
        LocationName.PostOfficeLobbySuitcase,
    ],
    RegionName.MMI1Hedgetrimmers: [
        LocationName.LandscapersHouseBackyardSuitcaseTag,
        LocationName.LandscapersHouseTablePurse,
    ],
    RegionName.MMI1RollingPin: [
        LocationName.LandscapersHouseKitchenAmmoUp,
    ],
    RegionName.MMI1Powerlines: [
        LocationName.PowerlineIslandSandboxHatboxTag,
        LocationName.PowerlineIslandLeftMemoryVault,
        LocationName.PowerlineIslandRightMaxLives,
    ],
    RegionName.MMI1Duster: [
        LocationName.InsideWebbedGarageHatbox,
        LocationName.PostOfficeBasementPlunger,
    ],
    RegionName.MMI2: [
        LocationName.BehindBookDepositorySteamerTrunk,
    ],
    RegionName.MMDM: [
        LocationName.MilkmanComplete,
    ],

    # Gloria's Theater
    RegionName.THMS: [
        LocationName.NearTheCriticPurse,
        LocationName.BelowTheSpotlightSteamertrunkTag,
        LocationName.BehindStagePurseTag,
    ],
    RegionName.THMSLev: [
        LocationName.InTheAudienceAmmoUp,
    ],
    RegionName.THMSDuster: [
        LocationName.BehindStageCobwebSuitcase,
    ],
    RegionName.THMSStorage: [
        LocationName.StorageRoomFloorVault,
        LocationName.StorageRoomLeftSteamertrunk,
        LocationName.StorageRoomRightLowerSuitcaseTag,
        LocationName.StorageRoomRightUpperCandle1,
        LocationName.BonitasRoom,
    ],
    RegionName.THCW: [
        LocationName.DoghouseSlicersDufflebagTag,
        LocationName.BigPlatform1Hatbox,
        LocationName.BigPlatform2Vault,
        LocationName.BigPlatform3OneUp,
        LocationName.BigPlatformAboveHatboxTag,
        LocationName.NextToOatmealDufflebag,
        LocationName.CandleBasketCandle2,
        LocationName.CurtainSlideConfusionAmmoUp,
    ],
    RegionName.THFB: [
        LocationName.GloriasTheaterComplete,
    ],

    # Waterloo World
    RegionName.WWMA: [
        LocationName.FredsRoomHatboxTag,
        LocationName.TheFireplacePricelessCoin,
        LocationName.GameBoardSuitcaseTag,
        LocationName.OutsideVillager1HouseOneUp,
        LocationName.SmallArchTopMaxLives,
        LocationName.SmallArchBelowPurseTag,
        LocationName.TopOfVillager2sHouseDufflebagTag,
        LocationName.CastleTowerOneUp,
        LocationName.CastleInsideVault,
        LocationName.CastleWallSteamertrunk,
        LocationName.HelpTheCarpenter,
    ],
    RegionName.WWMALev: [
        LocationName.TopOfVillager3sHouseAmmoUp,
        LocationName.TopOfKnightsHouseConfusionAmmoUp,
    ],
    RegionName.WWMACarpRoof: [
        LocationName.CarpentersRoofVault,
        LocationName.TightropeRoomDufflebag,
    ],
    RegionName.WWMADuster: [
        LocationName.UnderTheGuillotineSuitcase,
        LocationName.FredsHouseBasementHatbox,
        LocationName.BlacksmithsLeftBuildingPurse,
    ],
    RegionName.WWMADusterLev: [
        LocationName.BlacksmithsRightBuildingSteamertrunkTag,
    ],
    RegionName.WWMADusterLevPyro: [
        LocationName.BlacksmithsHaybaleTheMusket,
    ],
    RegionName.WWMAV1: [
        LocationName.HelpVillager1,
    ],
    RegionName.WWMAKnight: [
        LocationName.HelpTheKnight,
    ],
    RegionName.WWMAV2: [
        LocationName.HelpVillager2,
    ],
    RegionName.WWMAV3: [
        LocationName.HelpVillager3,
    ],
    RegionName.WWMADone: [
        LocationName.WaterlooWorldComplete,
    ],

    # Black Velvetopia
    RegionName.BVRB: [
        LocationName.ClubStreetLadySteamertrunk,
        LocationName.AlleywaysLedgeHatboxTag,
        LocationName.SewersMainVault,
        LocationName.NearDiegosHouseMaxLives,
    ],
    RegionName.BVRBLev: [
        LocationName.ClubStreetMetalBalconyDufflebagTag,
        LocationName.HeartStreetHIGHBalconyAmmoUp,
    ],
    RegionName.BVRBTele: [
        LocationName.ClubStreetGatedSteamerTrunkTag,
        LocationName.TheGardenVault,
    ],
    RegionName.BVRBDuster: [
        LocationName.DiegosBedSuitcaseTag,
        LocationName.DiegosRoomHatbox,
        LocationName.DiegosHouseGrindrailSuitcase,
        LocationName.GrindrailBalconyConfusionAmmoUp,
    ],
    RegionName.BVRBLogs: [
        LocationName.BurnTheLogsDufflebag,
    ],
    RegionName.BVES: [
        LocationName.SanctuaryGroundPurse,
        LocationName.TigerWrestler,
        LocationName.DragonWrestler,
        LocationName.EagleWrestler,

    ],
    RegionName.BVESLev: [
        LocationName.SanctuaryBalconyPurseTag,
    ],
    RegionName.BVESCobra: [
        LocationName.CobraWrestler,
    ],
    RegionName.BVESBoss: [
        LocationName.BlackVelvetopiaComplete,
    ],

    # Meat Circus
    RegionName.MCTC: [
        LocationName.CrumblingPathSteamertrunk,
        LocationName.CrumblingPathEndRightHatboxTag,
        LocationName.CrumblingPathEndLeftConfusionAmmoUp,
        LocationName.OllieEscortFloorSuitcaseTag,
    ],
    RegionName.MCTCLev: [
        LocationName.EntranceAwningSteamertrunkTag,
    ],
    RegionName.MCTCEscort: [
        LocationName.OllieEscortMiddleHatbox,
        LocationName.OllieEscortTopLeftVault,
        LocationName.OllieEscortTopRightPurseTag,
        LocationName.TunnelOfLoveStartPurse,
        LocationName.TunnelOfLoveCornerSuitcase,
        LocationName.TunnelOfLoveRailDufflebagTag,
        LocationName.NextToTheFatLadyDufflebag,
    ],
}


def place_events(self: "PSYWorld"):
    final_boss_location = self.multiworld.get_location(LocationName.FinalBossEvent, self.player)
    oleander_boss_location = self.multiworld.get_location(LocationName.OleanderBossEvent, self.player)
    redeemed_required_brains = self.multiworld.get_location(LocationName.RedeemedBrainsEvent, self.player)
    # Brain Tank Boss
    if self.options.RequireMeatCircus:
        victory = final_boss_location
    else:
        # Brain Hunt
        if self.options.Goal == Options.Goal.option_brainhunt:
            victory = redeemed_required_brains
        # Brain Tank or Brain Tank AND Brain Hunt
        else:
            victory = oleander_boss_location

    for location in (final_boss_location, oleander_boss_location, redeemed_required_brains):
        if location is victory:
            event_name = ItemName.Victory
        else:
            event_name = ItemName.Filler
        location.place_locked_item(self.create_event_item(event_name))


def _add_locations_to_existing_region(multiworld: MultiWorld, player: int, region_name: str,
                                      locations: Iterable[str]):
    region = multiworld.get_region(region_name, player)
    region.locations.extend(
        PSYLocation(player, name, ALL_LOCATIONS[name] + AP_LOCATION_OFFSET, region) for name in locations
    )


def create_deep_arrowhead_locations(multiworld: MultiWorld, player: int):
    _add_locations_to_existing_region(multiworld, player, RegionName.CAGP, CAGP_DEEP_ARROWHEAD_CHECKS)
    _add_locations_to_existing_region(multiworld, player, RegionName.CAMA, CAMA_DEEP_ARROWHEAD_CHECKS)
    _add_locations_to_existing_region(multiworld, player, RegionName.CARE, CARE_DEEP_ARROWHEAD_CHECKS)
    _add_locations_to_existing_region(multiworld, player, RegionName.CABH, CABH_DEEP_ARROWHEAD_CHECKS)


def create_mental_cobweb_locations(multiworld: MultiWorld, player: int):
    _add_locations_to_existing_region(multiworld, player, RegionName.BBA2, BB_COBWEB_CHECKS)
    _add_locations_to_existing_region(multiworld, player, RegionName.SACU, SA_COBWEB_CHECKS)
    _add_locations_to_existing_region(multiworld, player, RegionName.MIFL, MI_COBWEB_CHECKS)
    _add_locations_to_existing_region(multiworld, player, RegionName.NIMPMark, BT_COBWEB_CHECKS)

    # Lungfishopolis cobwebs are split across two regions.
    loma_cobwebs = {LocationName.CobwebSkyscraperBeforeDam}
    # All remaining cobwebs are in LOMAShield.
    loma_shield_cobwebs = set(LO_COBWEB_CHECKS).difference(loma_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.LOMA, loma_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.LOMAShield, loma_shield_cobwebs)

    # The Milkman Conspiracy cobwebs are split across three regions.
    mmi2_cobwebs = {LocationName.CobwebBookDepository}
    mmi1_before_sign_cobwebs = {LocationName.CobwebThirdHouse}
    # All remaining cobwebs are in MMI1AfterSign.
    mmi1_after_sign_cobwebs = set(MM_COBWEB_CHECKS) - mmi2_cobwebs - mmi1_before_sign_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.MMI1BeforeSign, mmi1_before_sign_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.MMI1AfterSign, mmi1_after_sign_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.MMI2, mmi2_cobwebs)

    # Gloria's Theater cobwebs are split across three regions.
    thms_lev_cobwebs = {LocationName.CobwebInTheAudience}
    thms_storage_cobwebs = {LocationName.CobwebStorageRoomLeft, LocationName.CobwebStorageRoomRight}
    # All remaining cobwebs are in THMS.
    thms_cobwebs = set(TH_COBWEB_CHECKS) - thms_lev_cobwebs - thms_storage_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.THMS, thms_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.THMSLev, thms_lev_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.THMSStorage, thms_storage_cobwebs)

    # Waterloo World cobwebs are split across two regions.
    wwma_duster_lev_cobwebs = {LocationName.CobwebBlacksmithsRightBuildingRoof}
    # All the remaining cobwebs are in WWMA.
    wwma_cobwebs = set(WW_COBWEB_CHECKS) - wwma_duster_lev_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.WWMA, wwma_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.WWMADusterLev, wwma_duster_lev_cobwebs)

    # Black Velvetopia cobwebs are split across two regions.
    # Technically, these locations could all go in either BVRB or BVRBDuster because the only difference is that
    # BVRBDuster requires the Cobweb Duster, and all Mental Cobweb locations require the Cobweb Duster to access.
    # However, it is more accurate to split the cobwebs into the different physical regions they are located in.
    bvrb_duster_cobwebs = {LocationName.CobwebDiegosHouseFireplace, LocationName.CobwebDiegosHouseGrindrail}
    # All the remaining cobwebs are in BVRB.
    bvrb_cobwebs = set(BV_COBWEB_CHECKS) - bvrb_duster_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.BVRB, bvrb_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.BVRBDuster, bvrb_duster_cobwebs)

    # Meat Circus cobwebs are split across two regions.
    mctc_escort_cobwebs = {LocationName.CobwebTunnelOfLoveOllieEscortExit}
    mctc_cobwebs = set(MC_COBWEB_CHECKS) - mctc_escort_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.MCTC, mctc_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.MCTCEscort, mctc_escort_cobwebs)


def create_psyregions(world: MultiWorld, player: int):
    # Create all default regions.
    for region_name, location_names in DEFAULT_REGIONS.items():
        region = Region(region_name, player, world)
        region.locations.extend(PSYLocation(player, loc_name, ALL_LOCATIONS[loc_name] + AP_LOCATION_OFFSET, region)
                                for loc_name in location_names)
        world.regions.append(region)

    # Add the regions for event locations.
    reg_caja_brains = Region(RegionName.CAJABrains, player, world)
    reg_caja_brains.locations += [PSYLocation(player, LocationName.RedeemedBrainsEvent, None, reg_caja_brains)]
    world.regions.append(reg_caja_brains)

    reg_aslb_boss = Region(RegionName.ASLBBoss, player, world)
    reg_aslb_boss.locations += [PSYLocation(player, LocationName.OleanderBossEvent, None, reg_aslb_boss)]
    world.regions.append(reg_aslb_boss)

    reg_mctc_boss = Region(RegionName.MCTCBoss, player, world)
    reg_mctc_boss.locations += [PSYLocation(player, LocationName.FinalBossEvent, None, reg_mctc_boss)]
    world.regions.append(reg_mctc_boss)

    # should only have an item if Cobweb Duster vanilla
    # RegionName.FordShop: [
    #    LocationName.ShopCobwebDuster,
    # ],

    # RegionName.DUMMYLOCATIONS
    # NOT COLLECTIBLE
    #    LocationName.DUMMYLOCATION1NOTCOLLECTIBLE,
    #    LocationName.DUMMYLOCATION2NOTCOLLECTIBLE,
    #    LocationName.DUMMYLOCATION3NOTCOLLECTIBLE,


def connect_regions(multiworld: MultiWorld, player: int):
    psy_region_connections: Dict[str, Set[str]] = {
        "Menu": {RegionName.CASA},
        # Collective Unconscious connections to everything else
        RegionName.CASA: {RegionName.CAGP, RegionName.CAJA, RegionName.CAJABrains, RegionName.RANK5to20,
                          RegionName.BBA1, RegionName.SACU, RegionName.MIFL,
                          RegionName.NIMP, RegionName.LOMA, RegionName.MMI1Fridge, RegionName.THMS, RegionName.WWMA,
                          RegionName.BVRB, RegionName.MCTC, },

        RegionName.RANK5to20: {RegionName.RANK25to40, },

        RegionName.RANK25to40: {RegionName.RANK45to60, },

        RegionName.RANK45to60: {RegionName.RANK65to80, },

        RegionName.RANK65to80: {RegionName.RANK85to101, },

        RegionName.CAGP: {RegionName.CAGPSquirrel, RegionName.CAGPGeyser, RegionName.CAMA, RegionName.CAKC,
                          RegionName.CARE,
                          RegionName.CABH, RegionName.CALI, },

        RegionName.CAMA: {RegionName.CAMALev, },

        RegionName.CAKC: {RegionName.CAKCLev, RegionName.CAKCPyro, },

        RegionName.CARE: {RegionName.CARELev, RegionName.CAREMark, },

        RegionName.CABH: {RegionName.CABHLev, RegionName.ASGR, },

        RegionName.ASGR: {RegionName.ASGRLev, RegionName.ASCO, RegionName.ASCOLev, RegionName.ASCOInvis},

        RegionName.ASCO: {RegionName.ASUP, },

        RegionName.ASUP: {RegionName.ASUPLev, },

        RegionName.ASUPLev: {RegionName.ASUPTele, },

        RegionName.ASUPTele: {RegionName.ASLB, },

        RegionName.ASLB: {RegionName.ASLBBoss, },

        RegionName.BBA1: {RegionName.BBA2, RegionName.BBA2Duster, },

        RegionName.SACU: {RegionName.SACULev, },

        RegionName.NIMP: {RegionName.NIMPMark, },

        RegionName.NIMPMark: {RegionName.NIBA, },

        RegionName.LOMA: {RegionName.LOMAShield, },

        RegionName.MMI1Fridge: {RegionName.MMI1BeforeSign, },

        RegionName.MMI1BeforeSign: {RegionName.MMI1AfterSign, },

        RegionName.MMI1AfterSign: {RegionName.MMI1Hedgetrimmers, RegionName.MMI1Duster, RegionName.MMI2, },

        RegionName.MMI1Hedgetrimmers: {RegionName.MMI1RollingPin, },

        RegionName.MMI2: {RegionName.MMI1Powerlines, },

        RegionName.MMI1Powerlines: {RegionName.MMDM, },

        RegionName.THMS: {RegionName.THMSLev, RegionName.THMSDuster, },

        RegionName.THMSDuster: {RegionName.THMSStorage, },

        RegionName.THMSStorage: {RegionName.THCW, },

        RegionName.THCW: {RegionName.THFB, },

        RegionName.WWMA: {RegionName.WWMALev, RegionName.WWMACarpRoof, RegionName.WWMADuster, RegionName.WWMAV1,
                          RegionName.WWMAKnight, },

        RegionName.WWMADuster: {RegionName.WWMADusterLev, },

        RegionName.WWMADusterLev: {RegionName.WWMADusterLevPyro, },

        RegionName.WWMAV1: {RegionName.WWMAV2, },

        RegionName.WWMAV2: {RegionName.WWMAV3, },

        RegionName.WWMAV3: {RegionName.WWMADone, },

        RegionName.BVRB: {RegionName.BVRBLev, RegionName.BVRBTele, RegionName.BVRBDuster, RegionName.BVES, },

        RegionName.BVRBTele: {RegionName.BVRBLogs, },

        RegionName.BVES: {RegionName.BVESLev, RegionName.BVESCobra, },

        RegionName.BVESCobra: {RegionName.BVESBoss, },

        RegionName.MCTC: {RegionName.MCTCLev, },

        RegionName.MCTCLev: {RegionName.MCTCEscort, },

        RegionName.MCTCEscort: {RegionName.MCTCBoss, },

    }

    for source, target in psy_region_connections.items():
        source_region = multiworld.get_region(source, player)
        source_region.add_exits(target)
