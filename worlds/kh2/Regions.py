import typing

from BaseClasses import MultiWorld, Region, Entrance

from .Locations import KH2Location, RegionTable
from .Names import LocationName, ItemName, RegionName


def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None)

    goa_region_locations = [
        LocationName.Crit_1,
        LocationName.Crit_2,
        LocationName.Crit_3,
        LocationName.Crit_4,
        LocationName.Crit_5,
        LocationName.Crit_6,
        LocationName.Crit_7,
        LocationName.GardenofAssemblageMap,
        LocationName.GoALostIllusion,
        LocationName.ProofofNonexistence,
        LocationName.DonaldStarting1,
        LocationName.DonaldStarting2,
        LocationName.GoofyStarting1,
        LocationName.GoofyStarting2,
    ]

    goa_region = create_region(world, player, active_locations, RegionName.GoA_Region,
                               goa_region_locations)

    lod_Region_locations = [
        LocationName.BambooGroveDarkShard,
        LocationName.BambooGroveEther,
        LocationName.BambooGroveMythrilShard,
        LocationName.EncampmentAreaMap,
        LocationName.Mission3,
        LocationName.CheckpointHiPotion,
        LocationName.CheckpointMythrilShard,
        LocationName.MountainTrailLightningShard,
        LocationName.MountainTrailRecoveryRecipe,
        LocationName.MountainTrailEther,
        LocationName.MountainTrailMythrilShard,
        LocationName.VillageCaveAreaMap,
        LocationName.VillageCaveAPBoost,
        LocationName.VillageCaveDarkShard,
        LocationName.VillageCaveBonus,
        LocationName.RidgeFrostShard,
        LocationName.RidgeAPBoost,
        LocationName.ShanYu,
        LocationName.ShanYuGetBonus,
        LocationName.HiddenDragon,
        LocationName.GoofyShanYu,
    ]
    lod_Region = create_region(world, player, active_locations, RegionName.LoD_Region,
                               lod_Region_locations)
    lod2_Region_locations = [
        LocationName.ThroneRoomTornPages,
        LocationName.ThroneRoomPalaceMap,
        LocationName.ThroneRoomAPBoost,
        LocationName.ThroneRoomQueenRecipe,
        LocationName.ThroneRoomAPBoost2,
        LocationName.ThroneRoomOgreShield,
        LocationName.ThroneRoomMythrilCrystal,
        LocationName.ThroneRoomOrichalcum,
        LocationName.StormRider,
        LocationName.XigbarDataDefenseBoost,
        LocationName.GoofyStormRider,
    ]
    lod2_Region = create_region(world, player, active_locations, RegionName.LoD2_Region,
                                lod2_Region_locations)
    ag_region_locations = [
        LocationName.AgrabahMap,
        LocationName.AgrabahDarkShard,
        LocationName.AgrabahMythrilShard,
        LocationName.AgrabahHiPotion,
        LocationName.AgrabahAPBoost,
        LocationName.AgrabahMythrilStone,
        LocationName.AgrabahMythrilShard2,
        LocationName.AgrabahSerenityShard,
        LocationName.BazaarMythrilGem,
        LocationName.BazaarPowerShard,
        LocationName.BazaarHiPotion,
        LocationName.BazaarAPBoost,
        LocationName.BazaarMythrilShard,
        LocationName.PalaceWallsSkillRing,
        LocationName.PalaceWallsMythrilStone,
        LocationName.CaveEntrancePowerStone,
        LocationName.CaveEntranceMythrilShard,
        LocationName.ValleyofStoneMythrilStone,
        LocationName.ValleyofStoneAPBoost,
        LocationName.ValleyofStoneMythrilShard,
        LocationName.ValleyofStoneHiPotion,
        LocationName.AbuEscort,
        LocationName.ChasmofChallengesCaveofWondersMap,
        LocationName.ChasmofChallengesAPBoost,
        LocationName.TreasureRoom,
        LocationName.TreasureRoomAPBoost,
        LocationName.TreasureRoomSerenityGem,
        LocationName.ElementalLords,
        LocationName.LampCharm,
        LocationName.GoofyTreasureRoom,
        LocationName.DonaldAbuEscort,
    ]
    ag_region = create_region(world, player, active_locations, RegionName.Ag_Region,
                              ag_region_locations)
    ag2_region_locations = [
        LocationName.RuinedChamberTornPages,
        LocationName.RuinedChamberRuinsMap,
        LocationName.GenieJafar,
        LocationName.WishingLamp,
    ]
    ag2_region = create_region(world, player, active_locations, RegionName.Ag2_Region,
                               ag2_region_locations)
    lexaeus_region_locations = [
        LocationName.LexaeusBonus,
        LocationName.LexaeusASStrengthBeyondStrength,
        LocationName.LexaeusDataLostIllusion,
    ]
    lexaeus_region = create_region(world, player, active_locations, RegionName.Lexaeus_Region,
                                   lexaeus_region_locations)

    dc_region_locations = [
        LocationName.DCCourtyardMythrilShard,
        LocationName.DCCourtyardStarRecipe,
        LocationName.DCCourtyardAPBoost,
        LocationName.DCCourtyardMythrilStone,
        LocationName.DCCourtyardBlazingStone,
        LocationName.DCCourtyardBlazingShard,
        LocationName.DCCourtyardMythrilShard2,
        LocationName.LibraryTornPages,
        LocationName.DisneyCastleMap,
        LocationName.MinnieEscort,
        LocationName.MinnieEscortGetBonus,
    ]
    dc_region = create_region(world, player, active_locations, RegionName.Dc_Region,
                              dc_region_locations)
    tr_region_locations = [
        LocationName.CornerstoneHillMap,
        LocationName.CornerstoneHillFrostShard,
        LocationName.PierMythrilShard,
        LocationName.PierHiPotion,
        LocationName.WaterwayMythrilStone,
        LocationName.WaterwayAPBoost,
        LocationName.WaterwayFrostStone,
        LocationName.WindowofTimeMap,
        LocationName.BoatPete,
        LocationName.FuturePete,
        LocationName.FuturePeteGetBonus,
        LocationName.Monochrome,
        LocationName.WisdomForm,
        LocationName.DonaldBoatPete,
        LocationName.DonaldBoatPeteGetBonus,
        LocationName.GoofyFuturePete,
    ]
    tr_region = create_region(world, player, active_locations, RegionName.Tr_Region,
                              tr_region_locations)
    marluxia_region_locations = [
        LocationName.MarluxiaGetBonus,
        LocationName.MarluxiaASEternalBlossom,
        LocationName.MarluxiaDataLostIllusion,
    ]
    marluxia_region = create_region(world, player, active_locations, RegionName.Marluxia_Region,
                                    marluxia_region_locations)
    terra_region_locations = [
        LocationName.LingeringWillBonus,
        LocationName.LingeringWillProofofConnection,
        LocationName.LingeringWillManifestIllusion,
    ]
    terra_region = create_region(world, player, active_locations, RegionName.Terra_Region,
                                 terra_region_locations)

    hundred_acre1_region_locations = [
        LocationName.PoohsHouse100AcreWoodMap,
        LocationName.PoohsHouseAPBoost,
        LocationName.PoohsHouseMythrilStone,
    ]
    hundred_acre1_region = create_region(world, player, active_locations, RegionName.HundredAcre1_Region,
                                         hundred_acre1_region_locations)
    hundred_acre2_region_locations = [
        LocationName.PigletsHouseDefenseBoost,
        LocationName.PigletsHouseAPBoost,
        LocationName.PigletsHouseMythrilGem,
    ]
    hundred_acre2_region = create_region(world, player, active_locations, RegionName.HundredAcre2_Region,
                                         hundred_acre2_region_locations)
    hundred_acre3_region_locations = [
        LocationName.RabbitsHouseDrawRing,
        LocationName.RabbitsHouseMythrilCrystal,
        LocationName.RabbitsHouseAPBoost,
    ]
    hundred_acre3_region = create_region(world, player, active_locations, RegionName.HundredAcre3_Region,
                                         hundred_acre3_region_locations)
    hundred_acre4_region_locations = [
        LocationName.KangasHouseMagicBoost,
        LocationName.KangasHouseAPBoost,
        LocationName.KangasHouseOrichalcum,
    ]
    hundred_acre4_region = create_region(world, player, active_locations, RegionName.HundredAcre4_Region,
                                         hundred_acre4_region_locations)
    hundred_acre5_region_locations = [
        LocationName.SpookyCaveMythrilGem,
        LocationName.SpookyCaveAPBoost,
        LocationName.SpookyCaveOrichalcum,
        LocationName.SpookyCaveGuardRecipe,
        LocationName.SpookyCaveMythrilCrystal,
        LocationName.SpookyCaveAPBoost2,
        LocationName.SweetMemories,
        LocationName.SpookyCaveMap,
    ]
    hundred_acre5_region = create_region(world, player, active_locations, RegionName.HundredAcre5_Region,
                                         hundred_acre5_region_locations)
    hundred_acre6_region_locations = [
        LocationName.StarryHillCosmicRing,
        LocationName.StarryHillStyleRecipe,
        LocationName.StarryHillCureElement,
        LocationName.StarryHillOrichalcumPlus,
    ]
    hundred_acre6_region = create_region(world, player, active_locations, RegionName.HundredAcre6_Region,
                                         hundred_acre6_region_locations)
    pr_region_locations = [
        LocationName.RampartNavalMap,
        LocationName.RampartMythrilStone,
        LocationName.RampartDarkShard,
        LocationName.TownDarkStone,
        LocationName.TownAPBoost,
        LocationName.TownMythrilShard,
        LocationName.TownMythrilGem,
        LocationName.CaveMouthBrightShard,
        LocationName.CaveMouthMythrilShard,
        LocationName.IsladeMuertaMap,
        LocationName.BoatFight,
        LocationName.InterceptorBarrels,
        LocationName.PowderStoreAPBoost1,
        LocationName.PowderStoreAPBoost2,
        LocationName.MoonlightNookMythrilShard,
        LocationName.MoonlightNookSerenityGem,
        LocationName.MoonlightNookPowerStone,
        LocationName.Barbossa,
        LocationName.BarbossaGetBonus,
        LocationName.FollowtheWind,
        LocationName.DonaldBoatFight,
        LocationName.GoofyBarbossa,
        LocationName.GoofyBarbossaGetBonus,
        LocationName.GoofyInterceptorBarrels,
    ]
    pr_region = create_region(world, player, active_locations, RegionName.Pr_Region,
                              pr_region_locations)
    pr2_region_locations = [
        LocationName.GrimReaper1,
        LocationName.InterceptorsHoldFeatherCharm,
        LocationName.SeadriftKeepAPBoost,
        LocationName.SeadriftKeepOrichalcum,
        LocationName.SeadriftKeepMeteorStaff,
        LocationName.SeadriftRowSerenityGem,
        LocationName.SeadriftRowKingRecipe,
        LocationName.SeadriftRowMythrilCrystal,
        LocationName.SeadriftRowCursedMedallion,
        LocationName.SeadriftRowShipGraveyardMap,
        LocationName.GoofyGrimReaper1,

    ]
    pr2_region = create_region(world, player, active_locations, RegionName.Pr2_Region,
                               pr2_region_locations)
    gr2_region_locations = [
        LocationName.DonaladGrimReaper2,
        LocationName.GrimReaper2,
        LocationName.SecretAnsemReport6,
        LocationName.LuxordDataAPBoost,
    ]
    gr2_region = create_region(world, player, active_locations, RegionName.Gr2_Region,
                               gr2_region_locations)
    oc_region_locations = [
        LocationName.PassageMythrilShard,
        LocationName.PassageMythrilStone,
        LocationName.PassageEther,
        LocationName.PassageAPBoost,
        LocationName.PassageHiPotion,
        LocationName.InnerChamberUnderworldMap,
        LocationName.InnerChamberMythrilShard,
        LocationName.Cerberus,
        LocationName.ColiseumMap,
        LocationName.Urns,
        LocationName.UnderworldEntrancePowerBoost,
        LocationName.CavernsEntranceLucidShard,
        LocationName.CavernsEntranceAPBoost,
        LocationName.CavernsEntranceMythrilShard,
        LocationName.TheLostRoadBrightShard,
        LocationName.TheLostRoadEther,
        LocationName.TheLostRoadMythrilShard,
        LocationName.TheLostRoadMythrilStone,
        LocationName.AtriumLucidStone,
        LocationName.AtriumAPBoost,
        LocationName.DemyxOC,
        LocationName.SecretAnsemReport5,
        LocationName.OlympusStone,
        LocationName.TheLockCavernsMap,
        LocationName.TheLockMythrilShard,
        LocationName.TheLockAPBoost,
        LocationName.PeteOC,
        LocationName.Hydra,
        LocationName.HydraGetBonus,
        LocationName.HerosCrest,
        LocationName.DonaldDemyxOC,
        LocationName.GoofyPeteOC,
    ]
    oc_region = create_region(world, player, active_locations, RegionName.Oc_Region,
                              oc_region_locations)
    oc2_region_locations = [
        LocationName.AuronsStatue,
        LocationName.Hades,
        LocationName.HadesGetBonus,
        LocationName.GuardianSoul,

    ]
    oc2_region = create_region(world, player, active_locations, RegionName.Oc2_Region,
                               oc2_region_locations)
    oc2_pain_and_panic_locations = [
        LocationName.ProtectBeltPainandPanicCup,
        LocationName.SerenityGemPainandPanicCup,
    ]
    oc2_titan_locations = [
        LocationName.GenjiShieldTitanCup,
        LocationName.SkillfulRingTitanCup,
    ]
    oc2_cerberus_locations = [
        LocationName.RisingDragonCerberusCup,
        LocationName.SerenityCrystalCerberusCup,
    ]
    oc2_gof_cup_locations = [
        LocationName.FatalCrestGoddessofFateCup,
        LocationName.OrichalcumPlusGoddessofFateCup,
        LocationName.HadesCupTrophyParadoxCups,
    ]
    zexion_region_locations = [
        LocationName.ZexionBonus,
        LocationName.ZexionASBookofShadows,
        LocationName.ZexionDataLostIllusion,
        LocationName.GoofyZexion,
    ]
    oc2_pain_and_panic_cup = create_region(world, player, active_locations, RegionName.Oc2_pain_and_panic_Region,
                                           oc2_pain_and_panic_locations)
    oc2_titan_cup = create_region(world, player, active_locations, RegionName.Oc2_titan_Region, oc2_titan_locations)
    oc2_cerberus_cup = create_region(world, player, active_locations, RegionName.Oc2_cerberus_Region,
                                     oc2_cerberus_locations)
    oc2_gof_cup = create_region(world, player, active_locations, RegionName.Oc2_gof_Region, oc2_gof_cup_locations)
    zexion_region = create_region(world, player, active_locations, RegionName.Zexion_Region, zexion_region_locations)

    bc_region_locations = [
        LocationName.BCCourtyardAPBoost,
        LocationName.BCCourtyardHiPotion,
        LocationName.BCCourtyardMythrilShard,
        LocationName.BellesRoomCastleMap,
        LocationName.BellesRoomMegaRecipe,
        LocationName.TheEastWingMythrilShard,
        LocationName.TheEastWingTent,
        LocationName.TheWestHallHiPotion,
        LocationName.TheWestHallPowerShard,
        LocationName.TheWestHallMythrilShard2,
        LocationName.TheWestHallBrightStone,
        LocationName.TheWestHallMythrilShard,
        LocationName.Thresholder,
        LocationName.DungeonBasementMap,
        LocationName.DungeonAPBoost,
        LocationName.SecretPassageMythrilShard,
        LocationName.SecretPassageHiPotion,
        LocationName.SecretPassageLucidShard,
        LocationName.TheWestHallAPBoostPostDungeon,
        LocationName.TheWestWingMythrilShard,
        LocationName.TheWestWingTent,
        LocationName.Beast,
        LocationName.TheBeastsRoomBlazingShard,
        LocationName.DarkThorn,
        LocationName.DarkThornGetBonus,
        LocationName.DarkThornCureElement,
        LocationName.DonaldThresholder,
        LocationName.GoofyBeast,
    ]
    bc_region = create_region(world, player, active_locations, RegionName.Bc_Region,
                              bc_region_locations)
    bc2_region_locations = [
        LocationName.RumblingRose,
        LocationName.CastleWallsMap,

    ]
    bc2_region = create_region(world, player, active_locations, RegionName.Bc2_Region,
                               bc2_region_locations)
    xaldin_region_locations = [
        LocationName.Xaldin,
        LocationName.XaldinGetBonus,
        LocationName.DonaldXaldinGetBonus,
        LocationName.SecretAnsemReport4,
        LocationName.XaldinDataDefenseBoost,
    ]
    xaldin_region = create_region(world, player, active_locations, RegionName.Xaldin_Region,
                                  xaldin_region_locations)
    sp_region_locations = [
        LocationName.PitCellAreaMap,
        LocationName.PitCellMythrilCrystal,
        LocationName.CanyonDarkCrystal,
        LocationName.CanyonMythrilStone,
        LocationName.CanyonMythrilGem,
        LocationName.CanyonFrostCrystal,
        LocationName.Screens,
        LocationName.HallwayPowerCrystal,
        LocationName.HallwayAPBoost,
        LocationName.CommunicationsRoomIOTowerMap,
        LocationName.CommunicationsRoomGaiaBelt,
        LocationName.HostileProgram,
        LocationName.HostileProgramGetBonus,
        LocationName.PhotonDebugger,
        LocationName.DonaldScreens,
        LocationName.GoofyHostileProgram,

    ]
    sp_region = create_region(world, player, active_locations, RegionName.Sp_Region,
                              sp_region_locations)
    sp2_region_locations = [
        LocationName.SolarSailer,
        LocationName.CentralComputerCoreAPBoost,
        LocationName.CentralComputerCoreOrichalcumPlus,
        LocationName.CentralComputerCoreCosmicArts,
        LocationName.CentralComputerCoreMap,

        LocationName.DonaldSolarSailer,
    ]

    sp2_region = create_region(world, player, active_locations, RegionName.Sp2_Region,
                               sp2_region_locations)
    mcp_region_locations = [
        LocationName.MCP,
        LocationName.MCPGetBonus,
    ]
    mcp_region = create_region(world, player, active_locations, RegionName.Mcp_Region,
                               mcp_region_locations)
    larxene_region_locations = [
        LocationName.LarxeneBonus,
        LocationName.LarxeneASCloakedThunder,
        LocationName.LarxeneDataLostIllusion,
    ]
    larxene_region = create_region(world, player, active_locations, RegionName.Larxene_Region,
                                   larxene_region_locations)
    ht_region_locations = [
        LocationName.GraveyardMythrilShard,
        LocationName.GraveyardSerenityGem,
        LocationName.FinklesteinsLabHalloweenTownMap,
        LocationName.TownSquareMythrilStone,
        LocationName.TownSquareEnergyShard,
        LocationName.HinterlandsLightningShard,
        LocationName.HinterlandsMythrilStone,
        LocationName.HinterlandsAPBoost,
        LocationName.CandyCaneLaneMegaPotion,
        LocationName.CandyCaneLaneMythrilGem,
        LocationName.CandyCaneLaneLightningStone,
        LocationName.CandyCaneLaneMythrilStone,
        LocationName.SantasHouseChristmasTownMap,
        LocationName.SantasHouseAPBoost,
        LocationName.PrisonKeeper,
        LocationName.OogieBoogie,
        LocationName.OogieBoogieMagnetElement,
        LocationName.DonaldPrisonKeeper,
        LocationName.GoofyOogieBoogie,
    ]
    ht_region = create_region(world, player, active_locations, RegionName.Ht_Region,
                              ht_region_locations)
    ht2_region_locations = [
        LocationName.Lock,
        LocationName.Present,
        LocationName.DecoyPresents,
        LocationName.Experiment,
        LocationName.DecisivePumpkin,

        LocationName.DonaldExperiment,
        LocationName.GoofyLock,
    ]
    ht2_region = create_region(world, player, active_locations, RegionName.Ht2_Region,
                               ht2_region_locations)
    vexen_region_locations = [
        LocationName.VexenBonus,
        LocationName.VexenASRoadtoDiscovery,
        LocationName.VexenDataLostIllusion,
    ]
    vexen_region = create_region(world, player, active_locations, RegionName.Vexen_Region,
                                 vexen_region_locations)
    hb_region_locations = [
        LocationName.MarketplaceMap,
        LocationName.BoroughDriveRecovery,
        LocationName.BoroughAPBoost,
        LocationName.BoroughHiPotion,
        LocationName.BoroughMythrilShard,
        LocationName.BoroughDarkShard,
        LocationName.MerlinsHouseMembershipCard,
        LocationName.MerlinsHouseBlizzardElement,
        LocationName.Bailey,
        LocationName.BaileySecretAnsemReport7,
        LocationName.BaseballCharm,
    ]
    hb_region = create_region(world, player, active_locations, RegionName.Hb_Region,
                              hb_region_locations)
    hb2_region_locations = [
        LocationName.PosternCastlePerimeterMap,
        LocationName.PosternMythrilGem,
        LocationName.PosternAPBoost,
        LocationName.CorridorsMythrilStone,
        LocationName.CorridorsMythrilCrystal,
        LocationName.CorridorsDarkCrystal,
        LocationName.CorridorsAPBoost,
        LocationName.AnsemsStudyMasterForm,
        LocationName.AnsemsStudySleepingLion,
        LocationName.AnsemsStudySkillRecipe,
        LocationName.AnsemsStudyUkuleleCharm,
        LocationName.RestorationSiteMoonRecipe,
        LocationName.RestorationSiteAPBoost,
        LocationName.CoRDepthsAPBoost,
        LocationName.CoRDepthsPowerCrystal,
        LocationName.CoRDepthsFrostCrystal,
        LocationName.CoRDepthsManifestIllusion,
        LocationName.CoRDepthsAPBoost2,
        LocationName.CoRMineshaftLowerLevelDepthsofRemembranceMap,
        LocationName.CoRMineshaftLowerLevelAPBoost,
        LocationName.DonaldDemyxHBGetBonus,
    ]
    hb2_region = create_region(world, player, active_locations, RegionName.Hb2_Region,
                               hb2_region_locations)
    onek_region_locations = [
        LocationName.DemyxHB,
        LocationName.DemyxHBGetBonus,
        LocationName.FFFightsCureElement,
        LocationName.CrystalFissureTornPages,
        LocationName.CrystalFissureTheGreatMawMap,
        LocationName.CrystalFissureEnergyCrystal,
        LocationName.CrystalFissureAPBoost,
        LocationName.ThousandHeartless,
        LocationName.ThousandHeartlessSecretAnsemReport1,
        LocationName.ThousandHeartlessIceCream,
        LocationName.ThousandHeartlessPicture,
        LocationName.PosternGullWing,
        LocationName.HeartlessManufactoryCosmicChain,
        LocationName.DemyxDataAPBoost,
    ]
    onek_region = create_region(world, player, active_locations, RegionName.ThousandHeartless_Region,
                                onek_region_locations)
    mushroom_region_locations = [
        LocationName.WinnersProof,
        LocationName.ProofofPeace,
    ]
    mushroom_region = create_region(world, player, active_locations, RegionName.Mushroom13_Region,
                                    mushroom_region_locations)
    sephi_region_locations = [
        LocationName.SephirothBonus,
        LocationName.SephirothFenrir,
    ]
    sephi_region = create_region(world, player, active_locations, RegionName.Sephi_Region,
                                 sephi_region_locations)

    cor_region_locations = [
        LocationName.CoRDepthsUpperLevelRemembranceGem,
        LocationName.CoRMiningAreaSerenityGem,
        LocationName.CoRMiningAreaAPBoost,
        LocationName.CoRMiningAreaSerenityCrystal,
        LocationName.CoRMiningAreaManifestIllusion,
        LocationName.CoRMiningAreaSerenityGem2,
        LocationName.CoRMiningAreaDarkRemembranceMap,
        LocationName.CoRMineshaftMidLevelPowerBoost,
        LocationName.CoREngineChamberSerenityCrystal,
        LocationName.CoREngineChamberRemembranceCrystal,
        LocationName.CoREngineChamberAPBoost,
        LocationName.CoREngineChamberManifestIllusion,
        LocationName.CoRMineshaftUpperLevelMagicBoost,
    ]
    cor_region = create_region(world, player, active_locations, RegionName.CoR_Region,
                               cor_region_locations)
    transport_region_locations = [
        LocationName.CoRMineshaftUpperLevelAPBoost,
        LocationName.TransporttoRemembrance,
    ]
    transport_region = create_region(world, player, active_locations, RegionName.Transport_Region,
                                     transport_region_locations)
    pl_region_locations = [
        LocationName.GorgeSavannahMap,
        LocationName.GorgeDarkGem,
        LocationName.GorgeMythrilStone,
        LocationName.ElephantGraveyardFrostGem,
        LocationName.ElephantGraveyardMythrilStone,
        LocationName.ElephantGraveyardBrightStone,
        LocationName.ElephantGraveyardAPBoost,
        LocationName.ElephantGraveyardMythrilShard,
        LocationName.PrideRockMap,
        LocationName.PrideRockMythrilStone,
        LocationName.PrideRockSerenityCrystal,
        LocationName.WildebeestValleyEnergyStone,
        LocationName.WildebeestValleyAPBoost,
        LocationName.WildebeestValleyMythrilGem,
        LocationName.WildebeestValleyMythrilStone,
        LocationName.WildebeestValleyLucidGem,
        LocationName.WastelandsMythrilShard,
        LocationName.WastelandsSerenityGem,
        LocationName.WastelandsMythrilStone,
        LocationName.JungleSerenityGem,
        LocationName.JungleMythrilStone,
        LocationName.JungleSerenityCrystal,
        LocationName.OasisMap,
        LocationName.OasisTornPages,
        LocationName.OasisAPBoost,
        LocationName.CircleofLife,
        LocationName.Hyenas1,
        LocationName.Scar,
        LocationName.ScarFireElement,
        LocationName.DonaldScar,
        LocationName.GoofyHyenas1,

    ]
    pl_region = create_region(world, player, active_locations, RegionName.Pl_Region,
                              pl_region_locations)
    pl2_region_locations = [
        LocationName.Hyenas2,
        LocationName.Groundshaker,
        LocationName.GroundshakerGetBonus,
        LocationName.SaixDataDefenseBoost,
        LocationName.GoofyHyenas2,
    ]
    pl2_region = create_region(world, player, active_locations, RegionName.Pl2_Region,
                               pl2_region_locations)

    stt_region_locations = [
        LocationName.TwilightTownMap,
        LocationName.MunnyPouchOlette,
        LocationName.StationDusks,
        LocationName.StationofSerenityPotion,
        LocationName.StationofCallingPotion,
        LocationName.TwilightThorn,
        LocationName.Axel1,
        LocationName.JunkChampionBelt,
        LocationName.JunkMedal,
        LocationName.TheStruggleTrophy,
        LocationName.CentralStationPotion1,
        LocationName.STTCentralStationHiPotion,
        LocationName.CentralStationPotion2,
        LocationName.SunsetTerraceAbilityRing,
        LocationName.SunsetTerraceHiPotion,
        LocationName.SunsetTerracePotion1,
        LocationName.SunsetTerracePotion2,
        LocationName.MansionFoyerHiPotion,
        LocationName.MansionFoyerPotion1,
        LocationName.MansionFoyerPotion2,
        LocationName.MansionDiningRoomElvenBandanna,
        LocationName.MansionDiningRoomPotion,
        LocationName.NaminesSketches,
        LocationName.MansionMap,
        LocationName.MansionLibraryHiPotion,
        LocationName.Axel2,
        LocationName.MansionBasementCorridorHiPotion,
        LocationName.RoxasDataMagicBoost,
    ]
    stt_region = create_region(world, player, active_locations, RegionName.STT_Region,
                               stt_region_locations)

    tt_region_locations = [
        LocationName.OldMansionPotion,
        LocationName.OldMansionMythrilShard,
        LocationName.TheWoodsPotion,
        LocationName.TheWoodsMythrilShard,
        LocationName.TheWoodsHiPotion,
        LocationName.TramCommonHiPotion,
        LocationName.TramCommonAPBoost,
        LocationName.TramCommonTent,
        LocationName.TramCommonMythrilShard1,
        LocationName.TramCommonPotion1,
        LocationName.TramCommonMythrilShard2,
        LocationName.TramCommonPotion2,
        LocationName.StationPlazaSecretAnsemReport2,
        LocationName.MunnyPouchMickey,
        LocationName.CrystalOrb,
        LocationName.CentralStationTent,
        LocationName.TTCentralStationHiPotion,
        LocationName.CentralStationMythrilShard,
        LocationName.TheTowerPotion,
        LocationName.TheTowerHiPotion,
        LocationName.TheTowerEther,
        LocationName.TowerEntrywayEther,
        LocationName.TowerEntrywayMythrilShard,
        LocationName.SorcerersLoftTowerMap,
        LocationName.TowerWardrobeMythrilStone,
        LocationName.StarSeeker,
        LocationName.ValorForm,
    ]
    tt_region = create_region(world, player, active_locations, RegionName.TT_Region,
                              tt_region_locations)
    tt2_region_locations = [
        LocationName.SeifersTrophy,
        LocationName.Oathkeeper,
        LocationName.LimitForm,
    ]
    tt2_region = create_region(world, player, active_locations, RegionName.TT2_Region,
                               tt2_region_locations)
    tt3_region_locations = [
        LocationName.UndergroundConcourseMythrilGem,
        LocationName.UndergroundConcourseAPBoost,
        LocationName.UndergroundConcourseMythrilCrystal,
        LocationName.UndergroundConcourseOrichalcum,
        LocationName.TunnelwayOrichalcum,
        LocationName.TunnelwayMythrilCrystal,
        LocationName.SunsetTerraceOrichalcumPlus,
        LocationName.SunsetTerraceMythrilShard,
        LocationName.SunsetTerraceMythrilCrystal,
        LocationName.SunsetTerraceAPBoost,
        LocationName.MansionNobodies,
        LocationName.MansionFoyerMythrilCrystal,
        LocationName.MansionFoyerMythrilStone,
        LocationName.MansionFoyerSerenityCrystal,
        LocationName.MansionDiningRoomMythrilCrystal,
        LocationName.MansionDiningRoomMythrilStone,
        LocationName.MansionLibraryOrichalcum,
        LocationName.BeamSecretAnsemReport10,
        LocationName.MansionBasementCorridorUltimateRecipe,
        LocationName.BetwixtandBetween,
        LocationName.BetwixtandBetweenBondofFlame,
        LocationName.AxelDataMagicBoost,
        LocationName.DonaldMansionNobodies,
    ]
    tt3_region = create_region(world, player, active_locations, RegionName.TT3_Region,
                               tt3_region_locations)

    twtnw_region_locations = [
        LocationName.FragmentCrossingMythrilStone,
        LocationName.FragmentCrossingMythrilCrystal,
        LocationName.FragmentCrossingAPBoost,
        LocationName.FragmentCrossingOrichalcum,
    ]

    twtnw_region = create_region(world, player, active_locations, RegionName.Twtnw_Region,
                                 twtnw_region_locations)
    twtnw_postroxas_region_locations = [
        LocationName.Roxas,
        LocationName.RoxasGetBonus,
        LocationName.RoxasSecretAnsemReport8,
        LocationName.TwoBecomeOne,
        LocationName.MemorysSkyscaperMythrilCrystal,
        LocationName.MemorysSkyscaperAPBoost,
        LocationName.MemorysSkyscaperMythrilStone,
        LocationName.TheBrinkofDespairDarkCityMap,
        LocationName.TheBrinkofDespairOrichalcumPlus,
        LocationName.NothingsCallMythrilGem,
        LocationName.NothingsCallOrichalcum,
        LocationName.TwilightsViewCosmicBelt,

    ]
    twtnw_postroxas_region = create_region(world, player, active_locations, RegionName.Twtnw_PostRoxas,
                                           twtnw_postroxas_region_locations)
    twtnw_postxigbar_region_locations = [
        LocationName.XigbarBonus,
        LocationName.XigbarSecretAnsemReport3,
        LocationName.NaughtsSkywayMythrilGem,
        LocationName.NaughtsSkywayOrichalcum,
        LocationName.NaughtsSkywayMythrilCrystal,
        LocationName.Oblivion,
        LocationName.CastleThatNeverWasMap,
        LocationName.Luxord,
        LocationName.LuxordGetBonus,
        LocationName.LuxordSecretAnsemReport9,
    ]
    twtnw_postxigbar_region = create_region(world, player, active_locations, RegionName.Twtnw_PostXigbar,
                                            twtnw_postxigbar_region_locations)
    twtnw2_region_locations = [
        LocationName.SaixBonus,
        LocationName.SaixSecretAnsemReport12,
        LocationName.PreXemnas1SecretAnsemReport11,
        LocationName.RuinandCreationsPassageMythrilStone,
        LocationName.RuinandCreationsPassageAPBoost,
        LocationName.RuinandCreationsPassageMythrilCrystal,
        LocationName.RuinandCreationsPassageOrichalcum,
        LocationName.Xemnas1,
        LocationName.Xemnas1GetBonus,
        LocationName.Xemnas1SecretAnsemReport13,
        LocationName.FinalXemnas,
        LocationName.XemnasDataPowerBoost,
    ]
    twtnw2_region = create_region(world, player, active_locations, RegionName.Twtnw2_Region,
                                  twtnw2_region_locations)

    valor_region_locations = [
        LocationName.Valorlvl2,
        LocationName.Valorlvl3,
        LocationName.Valorlvl4,
        LocationName.Valorlvl5,
        LocationName.Valorlvl6,
        LocationName.Valorlvl7,
    ]
    valor_region = create_region(world, player, active_locations, RegionName.Valor_Region,
                                 valor_region_locations)
    wisdom_region_locations = [
        LocationName.Wisdomlvl2,
        LocationName.Wisdomlvl3,
        LocationName.Wisdomlvl4,
        LocationName.Wisdomlvl5,
        LocationName.Wisdomlvl6,
        LocationName.Wisdomlvl7,
    ]
    wisdom_region = create_region(world, player, active_locations, RegionName.Wisdom_Region,
                                  wisdom_region_locations)
    limit_region_locations = [
        LocationName.Limitlvl2,
        LocationName.Limitlvl3,
        LocationName.Limitlvl4,
        LocationName.Limitlvl5,
        LocationName.Limitlvl6,
        LocationName.Limitlvl7,
    ]
    limit_region = create_region(world, player, active_locations, RegionName.Limit_Region,
                                 limit_region_locations)
    master_region_locations = [
        LocationName.Masterlvl2,
        LocationName.Masterlvl3,
        LocationName.Masterlvl4,
        LocationName.Masterlvl5,
        LocationName.Masterlvl6,
        LocationName.Masterlvl7,
    ]
    master_region = create_region(world, player, active_locations, RegionName.Master_Region,
                                  master_region_locations)
    final_region_locations = [
        LocationName.Finallvl2,
        LocationName.Finallvl3,
        LocationName.Finallvl4,
        LocationName.Finallvl5,
        LocationName.Finallvl6,
        LocationName.Finallvl7,
    ]
    final_region = create_region(world, player, active_locations, RegionName.Final_Region,
                                 final_region_locations)
    keyblade_region_locations = [
        LocationName.FAKESlot,
        LocationName.DetectionSaberSlot,
        LocationName.EdgeofUltimaSlot,
        LocationName.KingdomKeySlot,
        LocationName.OathkeeperSlot,
        LocationName.OblivionSlot,
        LocationName.StarSeekerSlot,
        LocationName.HiddenDragonSlot,
        LocationName.HerosCrestSlot,
        LocationName.MonochromeSlot,
        LocationName.FollowtheWindSlot,
        LocationName.CircleofLifeSlot,
        LocationName.PhotonDebuggerSlot,
        LocationName.GullWingSlot,
        LocationName.RumblingRoseSlot,
        LocationName.GuardianSoulSlot,
        LocationName.WishingLampSlot,
        LocationName.DecisivePumpkinSlot,
        LocationName.SweetMemoriesSlot,
        LocationName.MysteriousAbyssSlot,
        LocationName.SleepingLionSlot,
        LocationName.BondofFlameSlot,
        LocationName.TwoBecomeOneSlot,
        LocationName.FatalCrestSlot,
        LocationName.FenrirSlot,
        LocationName.UltimaWeaponSlot,
        LocationName.WinnersProofSlot,
        LocationName.PurebloodSlot,
        LocationName.Centurion2,
        LocationName.CometStaff,
        LocationName.HammerStaff,
        LocationName.LordsBroom,
        LocationName.MagesStaff,
        LocationName.MeteorStaff,
        LocationName.NobodyLance,
        LocationName.PreciousMushroom,
        LocationName.PreciousMushroom2,
        LocationName.PremiumMushroom,
        LocationName.RisingDragon,
        LocationName.SaveTheQueen2,
        LocationName.ShamansRelic,
        LocationName.VictoryBell,
        LocationName.WisdomWand,

        LocationName.AdamantShield,
        LocationName.AkashicRecord,
        LocationName.ChainGear,
        LocationName.DreamCloud,
        LocationName.FallingStar,
        LocationName.FrozenPride2,
        LocationName.GenjiShield,
        LocationName.KnightDefender,
        LocationName.KnightsShield,
        LocationName.MajesticMushroom,
        LocationName.MajesticMushroom2,
        LocationName.NobodyGuard,
        LocationName.OgreShield,
        LocationName.SaveTheKing2,
        LocationName.UltimateMushroom,
    ]
    keyblade_region = create_region(world, player, active_locations, RegionName.Keyblade_Region,
                                    keyblade_region_locations)

    world.regions += [
        lod_Region,
        lod2_Region,
        ag_region,
        ag2_region,
        lexaeus_region,
        dc_region,
        tr_region,
        terra_region,
        marluxia_region,
        hundred_acre1_region,
        hundred_acre2_region,
        hundred_acre3_region,
        hundred_acre4_region,
        hundred_acre5_region,
        hundred_acre6_region,
        pr_region,
        pr2_region,
        gr2_region,
        oc_region,
        oc2_region,
        oc2_pain_and_panic_cup,
        oc2_titan_cup,
        oc2_cerberus_cup,
        oc2_gof_cup,
        zexion_region,
        bc_region,
        bc2_region,
        xaldin_region,
        sp_region,
        sp2_region,
        mcp_region,
        larxene_region,
        ht_region,
        ht2_region,
        vexen_region,
        hb_region,
        hb2_region,
        onek_region,
        mushroom_region,
        sephi_region,
        cor_region,
        transport_region,
        pl_region,
        pl2_region,
        stt_region,
        tt_region,
        tt2_region,
        tt3_region,
        twtnw_region,
        twtnw_postroxas_region,
        twtnw_postxigbar_region,
        twtnw2_region,
        goa_region,
        menu_region,
        valor_region,
        wisdom_region,
        limit_region,
        master_region,
        final_region,
        keyblade_region,
    ]
    # Level region depends on level depth.
    # for every 5 levels there should be +3 visit locking
    levelVL1 = []
    levelVL3 = []
    levelVL6 = []
    levelVL9 = []
    levelVL12 = []
    levelVL15 = []
    levelVL18 = []
    levelVL21 = []
    levelVL24 = []
    levelVL26 = []
    # level 50
    if world.LevelDepth[player] == "level_50":
        levelVL1 = [LocationName.Lvl2, LocationName.Lvl4, LocationName.Lvl7, LocationName.Lvl9, LocationName.Lvl10]
        levelVL3 = [LocationName.Lvl12, LocationName.Lvl14, LocationName.Lvl15, LocationName.Lvl17,
                    LocationName.Lvl20, ]
        levelVL6 = [LocationName.Lvl23, LocationName.Lvl25, LocationName.Lvl28, LocationName.Lvl30]
        levelVL9 = [LocationName.Lvl32, LocationName.Lvl34, LocationName.Lvl36, LocationName.Lvl39, LocationName.Lvl41]
        levelVL12 = [LocationName.Lvl44, LocationName.Lvl46, LocationName.Lvl48]
        levelVL15 = [LocationName.Lvl50]
    # level 99
    elif world.LevelDepth[player] == "level_99":
        levelVL1 = [LocationName.Lvl7, LocationName.Lvl9, ]
        levelVL3 = [LocationName.Lvl12, LocationName.Lvl15, LocationName.Lvl17, LocationName.Lvl20]
        levelVL6 = [LocationName.Lvl23, LocationName.Lvl25, LocationName.Lvl28]
        levelVL9 = [LocationName.Lvl31, LocationName.Lvl33, LocationName.Lvl36, LocationName.Lvl39]
        levelVL12 = [LocationName.Lvl41, LocationName.Lvl44, LocationName.Lvl47, LocationName.Lvl49]
        levelVL15 = [LocationName.Lvl53, LocationName.Lvl59]
        levelVL18 = [LocationName.Lvl65]
        levelVL21 = [LocationName.Lvl73]
        levelVL24 = [LocationName.Lvl85]
        levelVL26 = [LocationName.Lvl99]
    # level sanity
    # has to be [] instead of {} for in
    elif world.LevelDepth[player] in ["level_50_sanity", "level_99_sanity"]:
        levelVL1 = [LocationName.Lvl2, LocationName.Lvl3, LocationName.Lvl4, LocationName.Lvl5, LocationName.Lvl6,
                    LocationName.Lvl7, LocationName.Lvl8, LocationName.Lvl9, LocationName.Lvl10]
        levelVL3 = [LocationName.Lvl11, LocationName.Lvl12, LocationName.Lvl13, LocationName.Lvl14, LocationName.Lvl15,
                    LocationName.Lvl16, LocationName.Lvl17, LocationName.Lvl18, LocationName.Lvl19, LocationName.Lvl20]
        levelVL6 = [LocationName.Lvl21, LocationName.Lvl22, LocationName.Lvl23, LocationName.Lvl24, LocationName.Lvl25,
                    LocationName.Lvl26, LocationName.Lvl27, LocationName.Lvl28, LocationName.Lvl29, LocationName.Lvl30]
        levelVL9 = [LocationName.Lvl31, LocationName.Lvl32, LocationName.Lvl33, LocationName.Lvl34, LocationName.Lvl35,
                    LocationName.Lvl36, LocationName.Lvl37, LocationName.Lvl38, LocationName.Lvl39, LocationName.Lvl40]
        levelVL12 = [LocationName.Lvl41, LocationName.Lvl42, LocationName.Lvl43, LocationName.Lvl44, LocationName.Lvl45,
                     LocationName.Lvl46, LocationName.Lvl47, LocationName.Lvl48, LocationName.Lvl49, LocationName.Lvl50]
        # level 99 sanity
        if world.LevelDepth[player] == "level_99_sanity":
            levelVL15 = [LocationName.Lvl51, LocationName.Lvl52, LocationName.Lvl53, LocationName.Lvl54,
                         LocationName.Lvl55, LocationName.Lvl56, LocationName.Lvl57, LocationName.Lvl58,
                         LocationName.Lvl59, LocationName.Lvl60]
            levelVL18 = [LocationName.Lvl61, LocationName.Lvl62, LocationName.Lvl63, LocationName.Lvl64,
                         LocationName.Lvl65, LocationName.Lvl66, LocationName.Lvl67, LocationName.Lvl68,
                         LocationName.Lvl69, LocationName.Lvl70]
            levelVL21 = [LocationName.Lvl71, LocationName.Lvl72, LocationName.Lvl73, LocationName.Lvl74,
                         LocationName.Lvl75, LocationName.Lvl76, LocationName.Lvl77, LocationName.Lvl78,
                         LocationName.Lvl79, LocationName.Lvl80]
            levelVL24 = [LocationName.Lvl81, LocationName.Lvl82, LocationName.Lvl83, LocationName.Lvl84,
                         LocationName.Lvl85, LocationName.Lvl86, LocationName.Lvl87, LocationName.Lvl88,
                         LocationName.Lvl89, LocationName.Lvl90]
            levelVL26 = [LocationName.Lvl91, LocationName.Lvl92, LocationName.Lvl93, LocationName.Lvl94,
                         LocationName.Lvl95, LocationName.Lvl96, LocationName.Lvl97, LocationName.Lvl98,
                         LocationName.Lvl99]

    level_regionVL1 = create_region(world, player, active_locations, RegionName.LevelsVS1,
                                    levelVL1)
    level_regionVL3 = create_region(world, player, active_locations, RegionName.LevelsVS3,
                                    levelVL3)
    level_regionVL6 = create_region(world, player, active_locations, RegionName.LevelsVS6,
                                    levelVL6)
    level_regionVL9 = create_region(world, player, active_locations, RegionName.LevelsVS9,
                                    levelVL9)
    level_regionVL12 = create_region(world, player, active_locations, RegionName.LevelsVS12,
                                     levelVL12)
    level_regionVL15 = create_region(world, player, active_locations, RegionName.LevelsVS15,
                                     levelVL15)
    level_regionVL18 = create_region(world, player, active_locations, RegionName.LevelsVS18,
                                     levelVL18)
    level_regionVL21 = create_region(world, player, active_locations, RegionName.LevelsVS21,
                                     levelVL21)
    level_regionVL24 = create_region(world, player, active_locations, RegionName.LevelsVS24,
                                     levelVL24)
    level_regionVL26 = create_region(world, player, active_locations, RegionName.LevelsVS26,
                                     levelVL26)
    world.regions += [level_regionVL1, level_regionVL3, level_regionVL6, level_regionVL9, level_regionVL12,
                      level_regionVL15, level_regionVL18, level_regionVL21, level_regionVL24, level_regionVL26]


def connect_regions(world: MultiWorld, player: int):
    # connecting every first visit to the GoA

    names: typing.Dict[str, int] = {}

    connect(world, player, names, "Menu", RegionName.Keyblade_Region)
    connect(world, player, names, "Menu", RegionName.GoA_Region)

    connect(world, player, names, RegionName.GoA_Region, RegionName.LoD_Region,
            lambda state: state.kh_lod_unlocked(player, 1))
    connect(world, player, names, RegionName.LoD_Region, RegionName.LoD2_Region,
            lambda state: state.kh_lod_unlocked(player, 2))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Oc_Region,
            lambda state: state.kh_oc_unlocked(player, 1))
    connect(world, player, names, RegionName.Oc_Region, RegionName.Oc2_Region,
            lambda state: state.kh_oc_unlocked(player, 2))
    connect(world, player, names, RegionName.Oc2_Region, RegionName.Zexion_Region,
            lambda state: state.kh_datazexion(player))

    connect(world, player, names, RegionName.Oc2_Region, RegionName.Oc2_pain_and_panic_Region,
            lambda state: state.kh_painandpanic(player))
    connect(world, player, names, RegionName.Oc2_Region, RegionName.Oc2_cerberus_Region,
            lambda state: state.kh_cerberuscup(player))
    connect(world, player, names, RegionName.Oc2_Region, RegionName.Oc2_titan_Region,
            lambda state: state.kh_titan(player))
    connect(world, player, names, RegionName.Oc2_Region, RegionName.Oc2_gof_Region,
            lambda state: state.kh_gof(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Ag_Region,
            lambda state: state.kh_ag_unlocked(player, 1))
    connect(world, player, names, RegionName.Ag_Region, RegionName.Ag2_Region,
            lambda state: state.kh_ag_unlocked(player, 2)
                          and (state.has(ItemName.FireElement, player)
                               and state.has(ItemName.BlizzardElement, player)
                               and state.has(ItemName.ThunderElement, player)))
    connect(world, player, names, RegionName.Ag2_Region, RegionName.Lexaeus_Region,
            lambda state: state.kh_datalexaeus(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Dc_Region,
            lambda state: state.kh_dc_unlocked(player, 1))
    connect(world, player, names, RegionName.Dc_Region, RegionName.Tr_Region,
            lambda state: state.kh_dc_unlocked(player, 2))
    connect(world, player, names, RegionName.Tr_Region, RegionName.Marluxia_Region,
            lambda state: state.kh_datamarluxia(player))
    connect(world, player, names, RegionName.Tr_Region, RegionName.Terra_Region, lambda state: state.kh_terra(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Pr_Region,
            lambda state: state.kh_pr_unlocked(player, 1))
    connect(world, player, names, RegionName.Pr_Region, RegionName.Pr2_Region,
            lambda state: state.kh_pr_unlocked(player, 2))
    connect(world, player, names, RegionName.Pr2_Region, RegionName.Gr2_Region,
            lambda state: state.kh_gr2(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Bc_Region,
            lambda state: state.kh_bc_unlocked(player, 1))
    connect(world, player, names, RegionName.Bc_Region, RegionName.Bc2_Region,
            lambda state: state.kh_bc_unlocked(player, 2))
    connect(world, player, names, RegionName.Bc2_Region, RegionName.Xaldin_Region,
            lambda state: state.kh_xaldin(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Sp_Region,
            lambda state: state.kh_sp_unlocked(player, 1))
    connect(world, player, names, RegionName.Sp_Region, RegionName.Sp2_Region,
            lambda state: state.kh_sp_unlocked(player, 2))
    connect(world, player, names, RegionName.Sp2_Region, RegionName.Mcp_Region,
            lambda state: state.kh_mcp(player))
    connect(world, player, names, RegionName.Mcp_Region, RegionName.Larxene_Region,
            lambda state: state.kh_datalarxene(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Ht_Region,
            lambda state: state.kh_ht_unlocked(player, 1))
    connect(world, player, names, RegionName.Ht_Region, RegionName.Ht2_Region,
            lambda state: state.kh_ht_unlocked(player, 2))
    connect(world, player, names, RegionName.Ht2_Region, RegionName.Vexen_Region,
            lambda state: state.kh_datavexen(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Hb_Region,
            lambda state: state.kh_hb_unlocked(player, 1))
    connect(world, player, names, RegionName.Hb_Region, RegionName.Hb2_Region,
            lambda state: state.kh_hb_unlocked(player, 2))
    connect(world, player, names, RegionName.Hb2_Region, RegionName.ThousandHeartless_Region,
            lambda state: state.kh_onek(player))
    connect(world, player, names, RegionName.ThousandHeartless_Region, RegionName.Mushroom13_Region,
            lambda state: state.has(ItemName.ProofofPeace, player))
    connect(world, player, names, RegionName.ThousandHeartless_Region, RegionName.Sephi_Region,
            lambda state: state.kh_sephi(player))

    connect(world, player, names, RegionName.Hb2_Region, RegionName.CoR_Region, lambda state: state.kh_cor(player))
    connect(world, player, names, RegionName.CoR_Region, RegionName.Transport_Region, lambda state:
    state.has(ItemName.HighJump, player, 3)
    and state.has(ItemName.AerialDodge, player, 3)
    and state.has(ItemName.Glide, player, 3))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Pl_Region,
            lambda state: state.kh_pl_unlocked(player, 1))
    connect(world, player, names, RegionName.Pl_Region, RegionName.Pl2_Region,
            lambda state: state.kh_pl_unlocked(player, 2) and (
                    state.has(ItemName.BerserkCharge, player) or state.kh_reflect(player)))

    connect(world, player, names, RegionName.GoA_Region, RegionName.STT_Region,
            lambda state: state.kh_stt_unlocked(player, 1))

    connect(world, player, names, RegionName.GoA_Region, RegionName.TT_Region,
            lambda state: state.kh_tt_unlocked(player, 1))
    connect(world, player, names, RegionName.TT_Region, RegionName.TT2_Region,
            lambda state: state.kh_tt_unlocked(player, 2))
    connect(world, player, names, RegionName.TT2_Region, RegionName.TT3_Region,
            lambda state: state.kh_tt_unlocked(player, 3))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Twtnw_Region,
            lambda state: state.kh_twtnw_unlocked(player, 0))
    connect(world, player, names, RegionName.Twtnw_Region, RegionName.Twtnw_PostRoxas,
            lambda state: state.kh_roxastools(player))
    connect(world, player, names, RegionName.Twtnw_PostRoxas, RegionName.Twtnw_PostXigbar,
            lambda state: state.kh_basetools(player) and (state.kh_donaldlimit(player) or (
                    state.has(ItemName.FinalForm, player) and state.has(ItemName.FireElement, player))))
    connect(world, player, names, RegionName.Twtnw_PostRoxas, RegionName.Twtnw2_Region,
            lambda state: state.kh_twtnw_unlocked(player, 1))

    hundredacrevisits = {RegionName.HundredAcre1_Region: 0, RegionName.HundredAcre2_Region: 1,
                         RegionName.HundredAcre3_Region: 2,
                         RegionName.HundredAcre4_Region: 3, RegionName.HundredAcre5_Region: 4,
                         RegionName.HundredAcre6_Region: 5}
    for visit, tornpage in hundredacrevisits.items():
        connect(world, player, names, RegionName.GoA_Region, visit,
                lambda state: (state.has(ItemName.TornPages, player, tornpage)))

    connect(world, player, names, RegionName.GoA_Region, RegionName.LevelsVS1,
            lambda state: state.kh_visit_locking_amount(player, 1))
    connect(world, player, names, RegionName.LevelsVS1, RegionName.LevelsVS3,
            lambda state: state.kh_visit_locking_amount(player, 3))
    connect(world, player, names, RegionName.LevelsVS3, RegionName.LevelsVS6,
            lambda state: state.kh_visit_locking_amount(player, 6))
    connect(world, player, names, RegionName.LevelsVS6, RegionName.LevelsVS9,
            lambda state: state.kh_visit_locking_amount(player, 9))
    connect(world, player, names, RegionName.LevelsVS9, RegionName.LevelsVS12,
            lambda state: state.kh_visit_locking_amount(player, 12))
    connect(world, player, names, RegionName.LevelsVS12, RegionName.LevelsVS15,
            lambda state: state.kh_visit_locking_amount(player, 15))
    connect(world, player, names, RegionName.LevelsVS15, RegionName.LevelsVS18,
            lambda state: state.kh_visit_locking_amount(player, 18))
    connect(world, player, names, RegionName.LevelsVS18, RegionName.LevelsVS21,
            lambda state: state.kh_visit_locking_amount(player, 21))
    connect(world, player, names, RegionName.LevelsVS21, RegionName.LevelsVS24,
            lambda state: state.kh_visit_locking_amount(player, 24))
    connect(world, player, names, RegionName.LevelsVS24, RegionName.LevelsVS26,
            lambda state: state.kh_visit_locking_amount(player, 25))  # 25 because of goa twtnw bugs with visit locking.

    for region in RegionTable["ValorRegion"]:
        connect(world, player, names, region, RegionName.Valor_Region,
                lambda state: state.has(ItemName.ValorForm, player))
    for region in RegionTable["WisdomRegion"]:
        connect(world, player, names, region, RegionName.Wisdom_Region,
                lambda state: state.has(ItemName.WisdomForm, player))
    for region in RegionTable["LimitRegion"]:
        connect(world, player, names, region, RegionName.Limit_Region,
                lambda state: state.has(ItemName.LimitForm, player))
    for region in RegionTable["MasterRegion"]:
        connect(world, player, names, region, RegionName.Master_Region,
                lambda state: state.has(ItemName.MasterForm, player) and state.has(ItemName.DriveConverter, player))
    for region in RegionTable["FinalRegion"]:
        connect(world, player, names, region, RegionName.Final_Region,
                lambda state: state.has(ItemName.FinalForm, player))


# shamelessly stolen from the sa2b
def connect(world: MultiWorld, player: int, used_names: typing.Dict[str, int], source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, world)
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            if loc_id:
                location = KH2Location(player, location, loc_id.code, ret)
                ret.locations.append(location)

    return ret
