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
    lomashield_cobwebs = set(LO_COBWEB_CHECKS).difference(loma_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.LOMA, loma_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.LOMAShield, lomashield_cobwebs)

    # The Milkman Conspiracy cobwebs are split across three regions.
    mmi2_cobwebs = {LocationName.CobwebBookDepository}
    mmi1_before_sign_cobwebs = {LocationName.CobwebThirdHouse}
    # All remaining cobwebs are in MMI1AfterSign.
    mmi1_after_sign_cobwebs = set(MM_COBWEB_CHECKS) - mmi2_cobwebs - mmi1_before_sign_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.MMI1BeforeSign, mmi1_before_sign_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.MMI1AfterSign, mmi1_after_sign_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.MMI2, mmi2_cobwebs)

    # Gloria's Theater cobwebs are split across three regions.
    thmslev_cobwebs = {LocationName.CobwebInTheAudience}
    thmsstorage_cobwebs = {LocationName.CobwebStorageRoomLeft, LocationName.CobwebStorageRoomRight}
    # All remaining cobwebs are in THMS.
    thms_cobwebs = set(TH_COBWEB_CHECKS) - thmslev_cobwebs - thmsstorage_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.THMS, thms_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.THMSLev, thmslev_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.THMSStorage, thmsstorage_cobwebs)

    # Waterloo World cobwebs are split across two regions.
    wwmadusterlev_cobwebs = {LocationName.CobwebBlacksmithsRightBuildingRoof}
    # All the remaining cobwebs are in WWMA.
    wwma_cobwebs = set(WW_COBWEB_CHECKS) - wwmadusterlev_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.WWMA, wwma_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.WWMADusterLev, wwmadusterlev_cobwebs)

    # Black Velvetopia cobwebs are split across two regions.
    # Technically, these locations could all go in either BVRB or BVRBDuster, but it's more accurate to split the
    # cobwebs into the physical regions they are located in.
    bvrbduster_cobwebs = {LocationName.CobwebDiegosHouseFireplace, LocationName.CobwebDiegosHouseGrindrail}
    # All the remaining cobwebs are in BVRB.
    bvrb_cobwebs = set(BV_COBWEB_CHECKS) - bvrbduster_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.BVRB, bvrb_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.BVRBDuster, bvrbduster_cobwebs)

    # Meat Circus cobwebs are split across two regions.
    mctc_escort_cobwebs = {LocationName.CobwebTunnelOfLoveOllieEscortExit}
    mctc_cobwebs = set(MC_COBWEB_CHECKS) - mctc_escort_cobwebs
    _add_locations_to_existing_region(multiworld, player, RegionName.MCTC, mctc_cobwebs)
    _add_locations_to_existing_region(multiworld, player, RegionName.MCTCEscort, mctc_escort_cobwebs)


def create_psyregions(world: MultiWorld, player: int):
    # Helper function to reduce duplicate code
    def create_region(name: str, location_names: Iterable[str]):
        region = Region(name, player, world)
        region.locations.extend(PSYLocation(player, loc_name, ALL_LOCATIONS[loc_name] + AP_LOCATION_OFFSET, region)
                                for loc_name in location_names)
        world.regions.append(region)

    locMenu_names = []
    create_region("Menu", locMenu_names)

    locCASA_names = [
        LocationName.BehindFurnitureCard,
        LocationName.StaircaseLedgesCard,
        LocationName.UpperLedgeFossil,
    ]
    create_region(RegionName.CASA, locCASA_names)

    locCAGP_names = [
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
    ]
    create_region(RegionName.CAGP, locCAGP_names)

    locCAGPSquirrel_names = [
        LocationName.SquirrelsAcornGoldenAcorn,
    ]
    create_region(RegionName.CAGPSquirrel, locCAGPSquirrel_names)

    locCAGPGeyser_names = [
        LocationName.GeyserMinersSkull,
    ]
    create_region(RegionName.CAGPGeyser, locCAGPGeyser_names)

    locCAMA_names = [
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
    ]
    create_region(RegionName.CAMA, locCAMA_names)

    locCAMALev_names = [
        LocationName.ParkingLotHistoryBoardCard,
    ]
    create_region(RegionName.CAMALev, locCAMALev_names)

    locCAKC_names = [
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
    ]
    create_region(RegionName.CAKC, locCAKC_names)

    locCAKCLev_names = [
        LocationName.HighUpTightropeCard,
    ]
    create_region(RegionName.CAKCLev, locCAKCLev_names)

    locCAKCPyro_names = [
        LocationName.CaveRefrigeratorTurkeySandwich,
    ]
    create_region(RegionName.CAKCPyro, locCAKCPyro_names)

    locCARE_names = [
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
    ]
    create_region(RegionName.CARE, locCARE_names)

    locCARELev_names = [
        LocationName.FireplaceTreeLowerCard,
        LocationName.FireplaceTreeTopDinosaurBone,
        LocationName.SwampSkinnyPolesCard,

    ]
    create_region(RegionName.CARELev, locCARELev_names)

    locCAREMark_names = [
        LocationName.HornetNestFertilityIdol,
    ]
    create_region(RegionName.CAREMark, locCAREMark_names)

    locCABH_names = [
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
    ]
    create_region(RegionName.CABH, locCABH_names)

    locCABHLev_names = [
        LocationName.TopofBigRockChallengeMarker,
    ]
    create_region(RegionName.CABHLev, locCABHLev_names)

    locCALI_names = [
        LocationName.MainLodgeRaftersVoodooDoll,
    ]
    create_region(RegionName.CALI, locCALI_names)

    locCAJA_names = [
        LocationName.TopofSanctuaryCard,
        LocationName.BottomofSanctuaryCard,
    ]
    create_region(RegionName.CAJA, locCAJA_names)

    regCAJABrains = Region(RegionName.CAJABrains, player, world)
    regCAJABrains.locations += [PSYLocation(player, LocationName.RedeemedBrainsEvent, None, regCAJABrains)]
    world.regions.append(regCAJABrains)

    locRANK5to20_names = [
        LocationName.PSIRank05,
        LocationName.PSIRank10,
        LocationName.PSIRank15,
        LocationName.PSIRank20,

    ]
    create_region(RegionName.RANK5to20, locRANK5to20_names)

    locRANK25to40_names = [
        LocationName.PSIRank25,
        LocationName.PSIRank30,
        LocationName.PSIRank35,
        LocationName.PSIRank40,

    ]
    create_region(RegionName.RANK25to40, locRANK25to40_names)

    locRANK45to60_names = [
        LocationName.PSIRank45,
        LocationName.PSIRank50,
        LocationName.PSIRank55,
        LocationName.PSIRank60,
    ]
    create_region(RegionName.RANK45to60, locRANK45to60_names)

    locRANK65to80_names = [
        LocationName.PSIRank65,
        LocationName.PSIRank70,
        LocationName.PSIRank75,
        LocationName.PSIRank80,
    ]
    create_region(RegionName.RANK65to80, locRANK65to80_names)

    locRANK85to101_names = [
        LocationName.PSIRank85,
        LocationName.PSIRank90,
        LocationName.PSIRank95,
        LocationName.PSIRank101,
    ]
    create_region(RegionName.RANK85to101, locRANK85to101_names)

    locASGR_names = [
        LocationName.RockWallBottom,
        LocationName.RockWallLadder,
        LocationName.FountainTop,
        LocationName.HedgeAlcove,
        LocationName.AsylumDoorsRight,
        LocationName.AsylumDoorsLeft,
        LocationName.CornerNearFence,
        LocationName.LedgeBeforeGloria,
    ]
    create_region(RegionName.ASGR, locASGR_names)

    locASGRLev_names = [
        LocationName.OutsideFrontGate,
        LocationName.PillarAboveGate,
    ]
    create_region(RegionName.ASGRLev, locASGRLev_names)

    locASCO_names = [
        LocationName.AboveElevator,
        LocationName.LedgeAboveFredLeft,
        LocationName.LedgeAboveFredRight,
        LocationName.LedgeOppositeElevator,
        LocationName.EdgarsRoom,
        LocationName.BehindElevator,
        LocationName.JunkCorner,
    ]
    create_region(RegionName.ASCO, locASCO_names)

    locASCOLev_names = [
        LocationName.AboveEdgar,
    ]
    create_region(RegionName.ASCOLev, locASCOLev_names)

    locASCOInvis_names = [
        LocationName.CrowsBasket,
    ]
    create_region(RegionName.ASCOInvis, locASCOInvis_names)

    locASUP_names = [
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
    ]
    create_region(RegionName.ASUP, locASUP_names)

    locASUPLev_names = [
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
    ]
    create_region(RegionName.ASUPLev, locASUPLev_names)

    locASUPTele_names = [
        LocationName.RoomOppositeChairDoor,
        LocationName.PipeSlideNearChairDoor,
        LocationName.RaftersAboveChairDoor,
    ]
    create_region(RegionName.ASUPTele, locASUPTele_names)

    locASLB_names = [
        LocationName.LabCagedCrowLeft,
        LocationName.LabCagedCrowRight,
        LocationName.NextToPokeylope,
        LocationName.LabTopRailingLeft1,
        LocationName.LabTopRailingLeft2,
        LocationName.LabTopElevator,
        LocationName.LabTopRailingRight,
        LocationName.TeaRoom,
    ]
    create_region(RegionName.ASLB, locASLB_names)

    regASLBBoss = Region(RegionName.ASLBBoss, player, world)
    regASLBBoss.locations += [PSYLocation(player, LocationName.OleanderBossEvent, None, regASLBBoss)]
    world.regions.append(regASLBBoss)

    locBBA1_names = [
        LocationName.JumpingTutorial1,
        LocationName.JumpingTutorial2,
        LocationName.PoleClimbingTutorialFloor,
        LocationName.BelowTheTripleTrampolines,
    ]
    create_region(RegionName.BBA1, locBBA1_names)

    locBBA2_names = [
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
    ]
    create_region(RegionName.BBA2, locBBA2_names)

    locBBA2Duster_names = [
        LocationName.TrapezeCobweb,
    ]
    create_region(RegionName.BBA2Duster, locBBA2Duster_names)

    locSACU_names = [
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
    ]
    create_region(RegionName.SACU, locSACU_names)

    locSACULev_names = [
        LocationName.RoundPlatformsFarFromValve,
    ]
    create_region(RegionName.SACULev, locSACULev_names)

    locMIFL_names = [
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
    ]
    create_region(RegionName.MIFL, locMIFL_names)

    locNIMP_names = [
        LocationName.OutsideCaravan,
        LocationName.BehindTheEgg,
        LocationName.ShadowMonsterPath,
    ]
    create_region(RegionName.NIMP, locNIMP_names)

    locNIMPMark_names = [
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
    ]
    create_region(RegionName.NIMPMark, locNIMPMark_names)

    locNIBA_names = [
        LocationName.BrainTumblerExperimentComplete,
    ]
    create_region(RegionName.NIBA, locNIBA_names)

    locLOMA_names = [
        LocationName.SkyscraperStart,
        LocationName.CornerNearJail,
        LocationName.SkyscraperBeforeDam,

    ]
    create_region(RegionName.LOMA, locLOMA_names)

    locLOMAShield_names = [
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
    ]
    create_region(RegionName.LOMAShield, locLOMAShield_names)

    locMMI1Fridge_names = [
        LocationName.BoydsFridgeClv,
    ]
    create_region(RegionName.MMI1Fridge, locMMI1Fridge_names)

    locMMI1BeforeSign_names = [
        LocationName.FirstHouseDufflebagTag,
        LocationName.SecondHouseRollingPin,
        LocationName.CarTrunk1StopSign,
    ]
    create_region(RegionName.MMI1BeforeSign, locMMI1BeforeSign_names)

    locMMI1AfterSign_names = [
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
    ]
    create_region(RegionName.MMI1AfterSign, locMMI1AfterSign_names)

    locMMI1Hedgetrimmers_names = [
        LocationName.LandscapersHouseBackyardSuitcaseTag,
        LocationName.LandscapersHouseTablePurse,
    ]
    create_region(RegionName.MMI1Hedgetrimmers, locMMI1Hedgetrimmers_names)

    locMMI1RollingPin_names = [
        LocationName.LandscapersHouseKitchenAmmoUp,
    ]
    create_region(RegionName.MMI1RollingPin, locMMI1RollingPin_names)

    locMMI1Powerlines_names = [
        LocationName.PowerlineIslandSandboxHatboxTag,
        LocationName.PowerlineIslandLeftMemoryVault,
        LocationName.PowerlineIslandRightMaxLives,
    ]
    create_region(RegionName.MMI1Powerlines, locMMI1Powerlines_names)

    locMMI1Duster_names = [
        LocationName.InsideWebbedGarageHatbox,
        LocationName.PostOfficeBasementPlunger,
    ]
    create_region(RegionName.MMI1Duster, locMMI1Duster_names)

    locMMI2_names = [
        LocationName.BehindBookDepositorySteamerTrunk,
    ]
    create_region(RegionName.MMI2, locMMI2_names)

    locMMDM_names = [
        LocationName.MilkmanComplete,
    ]
    create_region(RegionName.MMDM, locMMDM_names)

    locTHMS_names = [
        LocationName.NearTheCriticPurse,
        LocationName.BelowTheSpotlightSteamertrunkTag,
        LocationName.BehindStagePurseTag,
    ]
    create_region(RegionName.THMS, locTHMS_names)

    locTHMSLev_names = [
        LocationName.InTheAudienceAmmoUp,
    ]
    create_region(RegionName.THMSLev, locTHMSLev_names)

    locTHMSDuster_names = [
        LocationName.BehindStageCobwebSuitcase,
    ]
    create_region(RegionName.THMSDuster, locTHMSDuster_names)

    locTHMSStorage_names = [
        LocationName.StorageRoomFloorVault,
        LocationName.StorageRoomLeftSteamertrunk,
        LocationName.StorageRoomRightLowerSuitcaseTag,
        LocationName.StorageRoomRightUpperCandle1,
        LocationName.BonitasRoom,
    ]
    create_region(RegionName.THMSStorage, locTHMSStorage_names)

    locTHCW_names = [
        LocationName.DoghouseSlicersDufflebagTag,
        LocationName.BigPlatform1Hatbox,
        LocationName.BigPlatform2Vault,
        LocationName.BigPlatform3OneUp,
        LocationName.BigPlatformAboveHatboxTag,
        LocationName.NextToOatmealDufflebag,
        LocationName.CandleBasketCandle2,
        LocationName.CurtainSlideConfusionAmmoUp,
    ]
    create_region(RegionName.THCW, locTHCW_names)

    locTHFB_names = [
        LocationName.GloriasTheaterComplete,
    ]
    create_region(RegionName.THFB, locTHFB_names)

    locWWMA_names = [
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
    ]
    create_region(RegionName.WWMA, locWWMA_names)

    locWWMALev_names = [
        LocationName.TopOfVillager3sHouseAmmoUp,
        LocationName.TopOfKnightsHouseConfusionAmmoUp,
    ]
    create_region(RegionName.WWMALev, locWWMALev_names)

    locWWMACarpRoof_names = [
        LocationName.CarpentersRoofVault,
        LocationName.TightropeRoomDufflebag,
    ]
    create_region(RegionName.WWMACarpRoof, locWWMACarpRoof_names)

    locWWMADuster_names = [
        LocationName.UnderTheGuillotineSuitcase,
        LocationName.FredsHouseBasementHatbox,
        LocationName.BlacksmithsLeftBuildingPurse,
    ]
    create_region(RegionName.WWMADuster, locWWMADuster_names)

    locWWMADusterLev_names = [
        LocationName.BlacksmithsRightBuildingSteamertrunkTag,
    ]
    create_region(RegionName.WWMADusterLev, locWWMADusterLev_names)

    locWWMADusterLevPyro_names = [
        LocationName.BlacksmithsHaybaleTheMusket,
    ]
    create_region(RegionName.WWMADusterLevPyro, locWWMADusterLevPyro_names)

    locWWMAV1_names = [
        LocationName.HelpVillager1,
    ]
    create_region(RegionName.WWMAV1, locWWMAV1_names)

    locWWMAKnight_names = [
        LocationName.HelpTheKnight,
    ]
    create_region(RegionName.WWMAKnight, locWWMAKnight_names)

    locWWMAV2_names = [
        LocationName.HelpVillager2,
    ]
    create_region(RegionName.WWMAV2, locWWMAV2_names)

    locWWMAV3_names = [
        LocationName.HelpVillager3,
    ]
    create_region(RegionName.WWMAV3, locWWMAV3_names)

    locWWMADone_names = [
        LocationName.WaterlooWorldComplete,
    ]
    create_region(RegionName.WWMADone, locWWMADone_names)

    locBVRB_names = [
        LocationName.ClubStreetLadySteamertrunk,
        LocationName.AlleywaysLedgeHatboxTag,
        LocationName.SewersMainVault,
        LocationName.NearDiegosHouseMaxLives,
    ]
    create_region(RegionName.BVRB, locBVRB_names)

    locBVRBLev_names = [
        LocationName.ClubStreetMetalBalconyDufflebagTag,
        LocationName.HeartStreetHIGHBalconyAmmoUp,
    ]
    create_region(RegionName.BVRBLev, locBVRBLev_names)

    locBVRBTele_names = [
        LocationName.ClubStreetGatedSteamerTrunkTag,
        LocationName.TheGardenVault,
    ]
    create_region(RegionName.BVRBTele, locBVRBTele_names)

    locBVRBDuster_names = [
        LocationName.DiegosBedSuitcaseTag,
        LocationName.DiegosRoomHatbox,
        LocationName.DiegosHouseGrindrailSuitcase,
        LocationName.GrindrailBalconyConfusionAmmoUp,
    ]
    create_region(RegionName.BVRBDuster, locBVRBDuster_names)

    locBVRBLogs_names = [
        LocationName.BurnTheLogsDufflebag,
    ]
    create_region(RegionName.BVRBLogs, locBVRBLogs_names)

    locBVES_names = [
        LocationName.SanctuaryGroundPurse,
        LocationName.TigerWrestler,
        LocationName.DragonWrestler,
        LocationName.EagleWrestler,

    ]
    create_region(RegionName.BVES, locBVES_names)

    locBVESLev_names = [
        LocationName.SanctuaryBalconyPurseTag,
    ]
    create_region(RegionName.BVESLev, locBVESLev_names)

    locBVESCobra_names = [
        LocationName.CobraWrestler,
    ]
    create_region(RegionName.BVESCobra, locBVESCobra_names)

    locBVESBoss_names = [
        LocationName.BlackVelvetopiaComplete,
    ]
    create_region(RegionName.BVESBoss, locBVESBoss_names)

    locMCTC_names = [
        LocationName.CrumblingPathSteamertrunk,
        LocationName.CrumblingPathEndRightHatboxTag,
        LocationName.CrumblingPathEndLeftConfusionAmmoUp,
        LocationName.OllieEscortFloorSuitcaseTag,
    ]
    create_region(RegionName.MCTC, locMCTC_names)

    locMCTCLev_names = [
        LocationName.EntranceAwningSteamertrunkTag,
    ]
    create_region(RegionName.MCTCLev, locMCTCLev_names)

    locMCTCEscort_names = [
        LocationName.OllieEscortMiddleHatbox,
        LocationName.OllieEscortTopLeftVault,
        LocationName.OllieEscortTopRightPurseTag,
        LocationName.TunnelOfLoveStartPurse,
        LocationName.TunnelOfLoveCornerSuitcase,
        LocationName.TunnelOfLoveRailDufflebagTag,
        LocationName.NextToTheFatLadyDufflebag,
    ]
    create_region(RegionName.MCTCEscort, locMCTCEscort_names)

    regMCTCBoss = Region(RegionName.MCTCBoss, player, world)
    regMCTCBoss.locations += [PSYLocation(player, LocationName.FinalBossEvent, None, regMCTCBoss)]
    world.regions.append(regMCTCBoss)

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
    PSYRegionConnections: Dict[str, Set[str]] = {
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

    for source, target in PSYRegionConnections.items():
        source_region = multiworld.get_region(source, player)
        source_region.add_exits(target)
