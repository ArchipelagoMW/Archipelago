import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import LocationName, KH2Location, firstVisits
from .Names import LocationName, ItemName



def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None, None)

    GoA_Region_locations = {
        LocationName.Crit_1: [1],
        LocationName.Crit_2: [2],
        LocationName.Crit_3: [3],
        LocationName.Crit_4: [4],
        LocationName.Crit_5: [5],
        LocationName.Crit_6: [6],
        LocationName.Crit_7: [7],
        LocationName.GardenofAssemblageMap: [8],
        LocationName.GoALostIllusion: [9],
        LocationName.ProofofNonexistence: [10],
        LocationName.DonaldStarting1: [11],
        LocationName.DonaldStarting2: [12],
        LocationName.GoofyStarting1: [13],
        LocationName.GoofyStarting2: [14],
    }
    GoA_Region = create_region(world, player, active_locations, LocationName.GoA_Region,
                               GoA_Region_locations, None)

    LoD_Region_locations = {
        LocationName.BambooGroveDarkShard: [1],
        LocationName.BambooGroveEther: [2],
        LocationName.BambooGroveMythrilShard: [3],
        LocationName.EncampmentAreaMap: [4],
        LocationName.Mission3: [5],
        LocationName.CheckpointHiPotion: [6],
        LocationName.CheckpointMythrilShard: [7],
        LocationName.MountainTrailLightningShard: [8],
        LocationName.MountainTrailRecoveryRecipe: [9],
        LocationName.MountainTrailEther: [10],
        LocationName.MountainTrailMythrilShard: [11],
        LocationName.VillageCaveAreaMap: [12],
        LocationName.VillageCaveAPBoost: [13],
        LocationName.VillageCaveDarkShard: [14],
        LocationName.VillageCaveBonus: [15],
        LocationName.RidgeFrostShard: [16],
        LocationName.RidgeAPBoost: [17],
        LocationName.ShanYu: [18],
        LocationName.ShanYuGetBonus: [19],
        LocationName.HiddenDragon: [20],
        LocationName.GoofyShanYu: [21],
    }
    LoD_Region = create_region(world, player, active_locations, LocationName.LoD_Region,
                               LoD_Region_locations, None)
    LoD2_Region_locations = {
        LocationName.ThroneRoomTornPages: [1],
        LocationName.ThroneRoomPalaceMap: [2],
        LocationName.ThroneRoomAPBoost: [3],
        LocationName.ThroneRoomQueenRecipe: [4],
        LocationName.ThroneRoomAPBoost2: [5],
        LocationName.ThroneRoomOgreShield: [6],
        LocationName.ThroneRoomMythrilCrystal: [7],
        LocationName.ThroneRoomOrichalcum: [8],
        LocationName.StormRider: [9],
        LocationName.XigbarDataDefenseBoost: [10],
        LocationName.GoofyStormRider: [11],
    }
    LoD2_Region = create_region(world, player, active_locations, LocationName.LoD2_Region,
                                LoD2_Region_locations, None)
    Ag_Region_locations = {
        LocationName.AgrabahMap: [1],
        LocationName.AgrabahDarkShard: [2],
        LocationName.AgrabahMythrilShard: [3],
        LocationName.AgrabahHiPotion: [4],
        LocationName.AgrabahAPBoost: [5],
        LocationName.AgrabahMythrilStone: [6],
        LocationName.AgrabahMythrilShard2: [7],
        LocationName.AgrabahSerenityShard: [8],
        LocationName.BazaarMythrilGem: [9],
        LocationName.BazaarPowerShard: [10],
        LocationName.BazaarHiPotion: [11],
        LocationName.BazaarAPBoost: [12],
        LocationName.BazaarMythrilShard: [13],
        LocationName.PalaceWallsSkillRing: [14],
        LocationName.PalaceWallsMythrilStone: [15],
        LocationName.CaveEntrancePowerStone: [16],
        LocationName.CaveEntranceMythrilShard: [17],
        LocationName.ValleyofStoneMythrilStone: [18],
        LocationName.ValleyofStoneAPBoost: [19],
        LocationName.ValleyofStoneMythrilShard: [20],
        LocationName.ValleyofStoneHiPotion: [21],
        LocationName.AbuEscort: [22],
        LocationName.ChasmofChallengesCaveofWondersMap: [23],
        LocationName.ChasmofChallengesAPBoost: [24],
        LocationName.TreasureRoom: [25],
        LocationName.TreasureRoomAPBoost: [26],
        LocationName.TreasureRoomSerenityGem: [27],
        LocationName.ElementalLords: [28],
        LocationName.LampCharm: [29],
        LocationName.GoofyTreasureRoom: [30],
        LocationName.DonaldAbuEscort: [31],
    }
    Ag_Region = create_region(world, player, active_locations, LocationName.Ag_Region,
                              Ag_Region_locations, None)
    Ag2_Region_locations = {
        LocationName.RuinedChamberTornPages: [1],
        LocationName.RuinedChamberRuinsMap: [2],
        LocationName.GenieJafar: [3],
        LocationName.WishingLamp: [4],
        LocationName.LexaeusBonus: [5],
        LocationName.LexaeusASStrengthBeyondStrength: [6],
        LocationName.LexaeusDataLostIllusion: [7],
    }
    Ag2_Region = create_region(world, player, active_locations, LocationName.Ag2_Region,
                               Ag2_Region_locations, None)

    Dc_Region_locations = {
        LocationName.DCCourtyardMythrilShard: [1],
        LocationName.DCCourtyardStarRecipe: [2],
        LocationName.DCCourtyardAPBoost: [3],
        LocationName.DCCourtyardMythrilStone: [4],
        LocationName.DCCourtyardBlazingStone: [5],
        LocationName.DCCourtyardBlazingShard: [6],
        LocationName.DCCourtyardMythrilShard2: [7],
        LocationName.LibraryTornPages: [8],
        LocationName.DisneyCastleMap: [9],
        LocationName.MinnieEscort: [10],
        LocationName.MinnieEscortGetBonus: [11],
    }
    Dc_Region = create_region(world, player, active_locations, LocationName.Dc_Region,
                              Dc_Region_locations, None)
    Tr_Region_locations = {
        LocationName.CornerstoneHillMap: [1],
        LocationName.CornerstoneHillFrostShard: [2],
        LocationName.PierMythrilShard: [3],
        LocationName.PierHiPotion: [4],
        LocationName.WaterwayMythrilStone: [5],
        LocationName.WaterwayAPBoost: [6],
        LocationName.WaterwayFrostStone: [7],
        LocationName.WindowofTimeMap: [8],
        LocationName.BoatPete: [9],
        LocationName.FuturePete: [10],
        LocationName.FuturePeteGetBonus: [10],
        LocationName.Monochrome: [11],
        LocationName.WisdomForm: [12],
        LocationName.MarluxiaGetBonus: [13],
        LocationName.MarluxiaASEternalBlossom: [14],
        LocationName.MarluxiaDataLostIllusion: [15],
        LocationName.LingeringWillBonus: [16],
        LocationName.LingeringWillProofofConnection: [17],
        LocationName.LingeringWillManifestIllusion: [18],
        LocationName.DonaldBoatPete: [19],
        LocationName.DonaldBoatPeteGetBonus: [20],
        LocationName.GoofyFuturePete: [21],
    }
    Tr_Region = create_region(world, player, active_locations, LocationName.Tr_Region,
                              Tr_Region_locations, None)

    HundredAcre1_Region_locations = {
        LocationName.PoohsHouse100AcreWoodMap: [1],
        LocationName.PoohsHouseAPBoost: [2],
        LocationName.PoohsHouseMythrilStone: [3],
    }
    HundredAcre1_Region = create_region(world, player, active_locations, LocationName.HundredAcre1_Region,
                                        HundredAcre1_Region_locations, None)
    HundredAcre2_Region_locations = {
        LocationName.PigletsHouseDefenseBoost: [1],
        LocationName.PigletsHouseAPBoost: [2],
        LocationName.PigletsHouseMythrilGem: [3],
    }
    HundredAcre2_Region = create_region(world, player, active_locations, LocationName.HundredAcre2_Region,
                                        HundredAcre2_Region_locations, None)
    HundredAcre3_Region_locations = {
        LocationName.RabbitsHouseDrawRing: [1],
        LocationName.RabbitsHouseMythrilCrystal: [2],
        LocationName.RabbitsHouseAPBoost: [3],
    }
    HundredAcre3_Region = create_region(world, player, active_locations, LocationName.HundredAcre3_Region,
                                        HundredAcre3_Region_locations, None)
    HundredAcre4_Region_locations = {
        LocationName.KangasHouseMagicBoost: [1],
        LocationName.KangasHouseAPBoost: [2],
        LocationName.KangasHouseOrichalcum: [3],
    }
    HundredAcre4_Region = create_region(world, player, active_locations, LocationName.HundredAcre4_Region,
                                        HundredAcre4_Region_locations, None)
    HundredAcre5_Region_locations = {
        LocationName.SpookyCaveMythrilGem: [1],
        LocationName.SpookyCaveAPBoost: [2],
        LocationName.SpookyCaveOrichalcum: [3],
        LocationName.SpookyCaveGuardRecipe: [4],
        LocationName.SpookyCaveMythrilCrystal: [5],
        LocationName.SpookyCaveAPBoost2: [6],
        LocationName.SweetMemories: [7],
        LocationName.SpookyCaveMap: [8],
    }
    HundredAcre5_Region = create_region(world, player, active_locations, LocationName.HundredAcre5_Region,
                                        HundredAcre5_Region_locations, None)
    HundredAcre6_Region_locations = {
        LocationName.StarryHillCosmicRing: [1],
        LocationName.StarryHillStyleRecipe: [2],
        LocationName.StarryHillCureElement: [3],
        LocationName.StarryHillOrichalcumPlus: [4],
    }
    HundredAcre6_Region = create_region(world, player, active_locations, LocationName.HundredAcre6_Region,
                                        HundredAcre6_Region_locations, None)
    Pr_Region_locations = {
        LocationName.RampartNavalMap: [1],
        LocationName.RampartMythrilStone: [2],
        LocationName.RampartDarkShard: [3],
        LocationName.TownDarkStone: [4],
        LocationName.TownAPBoost: [5],
        LocationName.TownMythrilShard: [6],
        LocationName.TownMythrilGem: [7],
        LocationName.CaveMouthBrightShard: [8],
        LocationName.CaveMouthMythrilShard: [9],
        LocationName.IsladeMuertaMap: [10],
        LocationName.BoatFight: [11],
        LocationName.InterceptorBarrels: [12],
        LocationName.PowderStoreAPBoost1: [13],
        LocationName.PowderStoreAPBoost2: [14],
        LocationName.MoonlightNookMythrilShard: [15],
        LocationName.MoonlightNookSerenityGem: [16],
        LocationName.MoonlightNookPowerStone: [17],
        LocationName.Barbossa: [18],
        LocationName.BarbossaGetBonus: [19],
        LocationName.FollowtheWind: [20],
        LocationName.DonaldBoatFight: [21],
        LocationName.GoofyBarbossa: [22],
        LocationName.GoofyBarbossaGetBonus: [23],
        LocationName.GoofyInterceptorBarrels: [24],
    }
    Pr_Region = create_region(world, player, active_locations, LocationName.Pr_Region,
                              Pr_Region_locations, None)
    Pr2_Region_locations = {
        LocationName.GrimReaper1: [1],
        LocationName.InterceptorsHoldFeatherCharm: [2],
        LocationName.SeadriftKeepAPBoost: [3],
        LocationName.SeadriftKeepOrichalcum: [4],
        LocationName.SeadriftKeepMeteorStaff: [5],
        LocationName.SeadriftRowSerenityGem: [6],
        LocationName.SeadriftRowKingRecipe: [7],
        LocationName.SeadriftRowMythrilCrystal: [8],
        LocationName.SeadriftRowCursedMedallion: [9],
        LocationName.SeadriftRowShipGraveyardMap: [10],
        LocationName.GrimReaper2: [11],
        LocationName.SecretAnsemReport6: [12],
        LocationName.LuxordDataAPBoost: [13],
        LocationName.GoofyGrimReaper1: [14],
        LocationName.DonaladGrimReaper2: [15],
    }
    Pr2_Region = create_region(world, player, active_locations, LocationName.Pr2_Region,
                               Pr2_Region_locations, None)
    Oc_Region_locations = {
        LocationName.PassageMythrilShard: [1],
        LocationName.PassageMythrilStone: [2],
        LocationName.PassageEther: [3],
        LocationName.PassageAPBoost: [4],
        LocationName.PassageHiPotion: [5],
        LocationName.InnerChamberUnderworldMap: [6],
        LocationName.InnerChamberMythrilShard: [7],
        LocationName.Cerberus: [8],
        LocationName.ColiseumMap: [9],
        LocationName.Urns: [10],
        LocationName.UnderworldEntrancePowerBoost: [11],
        LocationName.CavernsEntranceLucidShard: [12],
        LocationName.CavernsEntranceAPBoost: [13],
        LocationName.CavernsEntranceMythrilShard: [14],
        LocationName.TheLostRoadBrightShard: [15],
        LocationName.TheLostRoadEther: [16],
        LocationName.TheLostRoadMythrilShard: [17],
        LocationName.TheLostRoadMythrilStone: [18],
        LocationName.AtriumLucidStone: [19],
        LocationName.AtriumAPBoost: [20],
        LocationName.DemyxOC: [21],
        LocationName.SecretAnsemReport5: [22],
        LocationName.OlympusStone: [23],
        LocationName.TheLockCavernsMap: [24],
        LocationName.TheLockMythrilShard: [25],
        LocationName.TheLockAPBoost: [26],
        LocationName.PeteOC: [27],
        LocationName.Hydra: [28],
        LocationName.HydraGetBonus: [29],
        LocationName.HerosCrest: [30],
        LocationName.DonaldDemyxOC: [31],
        LocationName.GoofyPeteOC: [32],
    }
    Oc_Region = create_region(world, player, active_locations, LocationName.Oc_Region,
                              Oc_Region_locations, None)
    Oc2_Region_locations = {
        LocationName.AuronsStatue: [1],
        LocationName.Hades: [2],
        LocationName.HadesGetBonus: [3],
        LocationName.GuardianSoul: [4],
        LocationName.ZexionBonus: [5],
        LocationName.ZexionASBookofShadows: [6],
        LocationName.ZexionDataLostIllusion: [7],
        LocationName.GoofyZexion: [8],
    }
    Oc2_Region = create_region(world, player, active_locations, LocationName.Oc2_Region,
                               Oc2_Region_locations, None)
    Oc2Cups_Region_locations = {
        LocationName.ProtectBeltPainandPanicCup: [1],
        LocationName.SerenityGemPainandPanicCup: [3],
        LocationName.RisingDragonCerberusCup: [4],
        LocationName.SerenityCrystalCerberusCup: [5],
        LocationName.GenjiShieldTitanCup: [6],
        LocationName.SkillfulRingTitanCup: [7],
        LocationName.FatalCrestGoddessofFateCup: [8],
        LocationName.OrichalcumPlusGoddessofFateCup: [9],
        LocationName.HadesCupTrophyParadoxCups: [10],
    }
    Oc2Cups_Region = create_region(world, player, active_locations, LocationName.Oc2Cups_Region,
                                   Oc2Cups_Region_locations, None)
    Bc_Region_locations = {
        LocationName.BCCourtyardAPBoost: [1],
        LocationName.BCCourtyardHiPotion: [2],
        LocationName.BCCourtyardMythrilShard: [3],
        LocationName.BellesRoomCastleMap: [4],
        LocationName.BellesRoomMegaRecipe: [5],
        LocationName.TheEastWingMythrilShard: [6],
        LocationName.TheEastWingTent: [7],
        LocationName.TheWestHallHiPotion: [8],
        LocationName.TheWestHallPowerShard: [9],
        LocationName.TheWestHallAPBoost: [10],
        LocationName.TheWestHallBrightStone: [11],
        LocationName.TheWestHallMythrilShard: [12],
        LocationName.Thresholder: [13],
        LocationName.DungeonBasementMap: [14],
        LocationName.DungeonAPBoost: [15],
        LocationName.SecretPassageMythrilShard: [16],
        LocationName.SecretPassageHiPotion: [17],
        LocationName.SecretPassageLucidShard: [18],
        LocationName.TheWestHallAPBoostPostDungeon: [19],
        LocationName.TheWestWingMythrilShard: [20],
        LocationName.TheWestWingTent: [21],
        LocationName.Beast: [22],
        LocationName.TheBeastsRoomBlazingShard: [23],
        LocationName.DarkThorn: [25],
        LocationName.DarkThornGetBonus: [26],
        LocationName.DarkThornCureElement: [27],
        LocationName.DonaldThresholder: [28],
        LocationName.GoofyBeast: [29],

    }
    Bc_Region = create_region(world, player, active_locations, LocationName.Bc_Region,
                              Bc_Region_locations, None)
    Bc2_Region_locations = {
        LocationName.RumblingRose: [1],
        LocationName.CastleWallsMap: [2],
        LocationName.Xaldin: [3],
        LocationName.XaldinGetBonus: [4],
        LocationName.SecretAnsemReport4: [5],
        LocationName.XaldinDataDefenseBoost: [6],
        LocationName.DonaldXaldinGetBonus: [7],
    }
    Bc2_Region = create_region(world, player, active_locations, LocationName.Bc2_Region,
                               Bc2_Region_locations, None)
    Sp_Region_locations = {
        LocationName.PitCellAreaMap: [1],
        LocationName.PitCellMythrilCrystal: [2],
        LocationName.CanyonDarkCrystal: [3],
        LocationName.CanyonMythrilStone: [4],
        LocationName.CanyonMythrilGem: [5],
        LocationName.CanyonFrostCrystal: [6],
        LocationName.Screens: [7],
        LocationName.HallwayPowerCrystal: [8],
        LocationName.HallwayAPBoost: [9],
        LocationName.CommunicationsRoomIOTowerMap: [10],
        LocationName.CommunicationsRoomGaiaBelt: [11],
        LocationName.HostileProgram: [12],
        LocationName.HostileProgramGetBonus: [13],
        LocationName.PhotonDebugger: [14],
        LocationName.DonaldScreens: [15],
        LocationName.GoofyHostileProgram: [16],

    }
    Sp_Region = create_region(world, player, active_locations, LocationName.Sp_Region,
                              Sp_Region_locations, None)
    Sp2_Region_locations = {
        LocationName.SolarSailer: [1],
        LocationName.CentralComputerCoreAPBoost: [2],
        LocationName.CentralComputerCoreOrichalcumPlus: [3],
        LocationName.CentralComputerCoreCosmicArts: [4],
        LocationName.CentralComputerCoreMap: [5],
        LocationName.MCP: [6],
        LocationName.MCPGetBonus: [7],
        LocationName.LarxeneBonus: [8],
        LocationName.LarxeneASCloakedThunder: [9],
        LocationName.LarxeneDataLostIllusion: [10],
        LocationName.DonaldSolarSailer: [11],
    }
    Sp2_Region = create_region(world, player, active_locations, LocationName.Sp2_Region,
                               Sp2_Region_locations, None)
    Ht_Region_locations = {
        LocationName.GraveyardMythrilShard: [1],
        LocationName.GraveyardSerenityGem: [2],
        LocationName.FinklesteinsLabHalloweenTownMap: [3],
        LocationName.TownSquareMythrilStone: [4],
        LocationName.TownSquareEnergyShard: [5],
        LocationName.HinterlandsLightningShard: [6],
        LocationName.HinterlandsMythrilStone: [7],
        LocationName.HinterlandsAPBoost: [8],
        LocationName.CandyCaneLaneMegaPotion: [9],
        LocationName.CandyCaneLaneMythrilGem: [10],
        LocationName.CandyCaneLaneLightningStone: [11],
        LocationName.CandyCaneLaneMythrilStone: [12],
        LocationName.SantasHouseChristmasTownMap: [13],
        LocationName.SantasHouseAPBoost: [14],
        LocationName.PrisonKeeper: [15],
        LocationName.OogieBoogie: [16],
        LocationName.OogieBoogieMagnetElement: [17],
        LocationName.DonaldPrisonKeeper: [18],
        LocationName.GoofyOogieBoogie: [19],
    }
    Ht_Region = create_region(world, player, active_locations, LocationName.Ht_Region,
                              Ht_Region_locations, None)
    Ht2_Region_locations = {
        LocationName.Lock: [1],
        LocationName.Present: [2],
        LocationName.DecoyPresents: [3],
        LocationName.Experiment: [4],
        LocationName.DecisivePumpkin: [5],
        LocationName.VexenBonus: [6],
        LocationName.VexenASRoadtoDiscovery: [7],
        LocationName.VexenDataLostIllusion: [8],
        LocationName.DonaldExperiment: [9],
        LocationName.GoofyLock: [10],
    }
    Ht2_Region = create_region(world, player, active_locations, LocationName.Ht2_Region,
                               Ht2_Region_locations, None)

    Hb_Region_locations = {
        LocationName.MarketplaceMap: [1],
        LocationName.BoroughDriveRecovery: [2],
        LocationName.BoroughAPBoost: [3],
        LocationName.BoroughHiPotion: [4],
        LocationName.BoroughMythrilShard: [5],
        LocationName.BoroughDarkShard: [6],
        LocationName.MerlinsHouseMembershipCard: [7],
        LocationName.MerlinsHouseBlizzardElement: [8],
        LocationName.Bailey: [9],
        LocationName.BaileySecretAnsemReport7: [10],
        LocationName.BaseballCharm: [11],
    }
    Hb_Region = create_region(world, player, active_locations, LocationName.Hb_Region,
                              Hb_Region_locations, None)
    Hb2_Region_locations = {
        LocationName.PosternCastlePerimeterMap: [1],
        LocationName.PosternMythrilGem: [2],
        LocationName.PosternAPBoost: [3],
        LocationName.CorridorsMythrilStone: [4],
        LocationName.CorridorsMythrilCrystal: [5],
        LocationName.CorridorsDarkCrystal: [6],
        LocationName.CorridorsAPBoost: [7],
        LocationName.AnsemsStudyMasterForm: [8],
        LocationName.AnsemsStudySleepingLion: [9],
        LocationName.AnsemsStudySkillRecipe: [10],
        LocationName.AnsemsStudyUkuleleCharm: [11],
        LocationName.RestorationSiteMoonRecipe: [12],
        LocationName.RestorationSiteAPBoost: [13],
        LocationName.DemyxHB: [14],
        LocationName.DemyxHBGetBonus: [14],
        LocationName.FFFightsCureElement: [15],
        LocationName.CrystalFissureTornPages: [16],
        LocationName.CrystalFissureTheGreatMawMap: [17],
        LocationName.CrystalFissureEnergyCrystal: [18],
        LocationName.CrystalFissureAPBoost: [19],
        LocationName.ThousandHeartless: [20],
        LocationName.ThousandHeartlessSecretAnsemReport1: [21],
        LocationName.ThousandHeartlessIceCream: [22],
        LocationName.ThousandHeartlessPicture: [23],
        LocationName.PosternGullWing: [24],
        LocationName.HeartlessManufactoryCosmicChain: [25],
        LocationName.SephirothBonus: [26],
        LocationName.SephirothFenrir: [27],
        LocationName.WinnersProof: [28],
        LocationName.ProofofPeace: [29],
        LocationName.DemyxDataAPBoost: [30],
        LocationName.CoRDepthsAPBoost: [31],
        LocationName.CoRDepthsPowerCrystal: [32],
        LocationName.CoRDepthsFrostCrystal: [33],
        LocationName.CoRDepthsManifestIllusion: [34],
        LocationName.CoRDepthsAPBoost2: [35],
        LocationName.CoRMineshaftLowerLevelDepthsofRemembranceMap: [36],
        LocationName.CoRMineshaftLowerLevelAPBoost: [37],
        LocationName.DonaldDemyxHBGetBonus: [38],
    }
    Hb2_Region = create_region(world, player, active_locations, LocationName.Hb2_Region,
                               Hb2_Region_locations, None)

    CoR_Region_locations = {
        LocationName.CoRDepthsUpperLevelRemembranceGem: [1],
        LocationName.CoRMiningAreaSerenityGem: [2],
        LocationName.CoRMiningAreaAPBoost: [3],
        LocationName.CoRMiningAreaSerenityCrystal: [4],
        LocationName.CoRMiningAreaManifestIllusion: [5],
        LocationName.CoRMiningAreaSerenityGem2: [6],
        LocationName.CoRMiningAreaDarkRemembranceMap: [7],
        LocationName.CoRMineshaftMidLevelPowerBoost: [8],
        LocationName.CoREngineChamberSerenityCrystal: [9],
        LocationName.CoREngineChamberRemembranceCrystal: [10],
        LocationName.CoREngineChamberAPBoost: [11],
        LocationName.CoREngineChamberManifestIllusion: [12],
        LocationName.CoRMineshaftUpperLevelMagicBoost: [13],
        LocationName.CoRMineshaftUpperLevelAPBoost: [14],
        LocationName.TransporttoRemembrance: [15],
        LocationName.CoRMineshaftUpperLevelAPBoost: [16],
        LocationName.TransporttoRemembrance: [17],
    }
    CoR_Region = create_region(world, player, active_locations, LocationName.CoR_Region,
                               CoR_Region_locations, None)

    Pl_Region_locations = {
        LocationName.GorgeSavannahMap: [1],
        LocationName.GorgeDarkGem: [2],
        LocationName.GorgeMythrilStone: [3],
        LocationName.ElephantGraveyardFrostGem: [4],
        LocationName.ElephantGraveyardMythrilStone: [5],
        LocationName.ElephantGraveyardBrightStone: [6],
        LocationName.ElephantGraveyardAPBoost: [7],
        LocationName.ElephantGraveyardMythrilShard: [8],
        LocationName.PrideRockMap: [9],
        LocationName.PrideRockMythrilStone: [10],
        LocationName.PrideRockSerenityCrystal: [11],
        LocationName.WildebeestValleyEnergyStone: [12],
        LocationName.WildebeestValleyAPBoost: [13],
        LocationName.WildebeestValleyMythrilGem: [14],
        LocationName.WildebeestValleyMythrilStone: [15],
        LocationName.WildebeestValleyLucidGem: [16],
        LocationName.WastelandsMythrilShard: [17],
        LocationName.WastelandsSerenityGem: [18],
        LocationName.WastelandsMythrilStone: [19],
        LocationName.JungleSerenityGem: [20],
        LocationName.JungleMythrilStone: [21],
        LocationName.JungleSerenityCrystal: [22],
        LocationName.OasisMap: [23],
        LocationName.OasisTornPages: [24],
        LocationName.OasisAPBoost: [25],
        LocationName.CircleofLife: [26],
        LocationName.Hyenas1: [27],
        LocationName.Scar: [28],
        LocationName.ScarFireElement: [29],
        LocationName.DonaldScar: [30],
        LocationName.GoofyHyenas1: [31],

    }
    Pl_Region = create_region(world, player, active_locations, LocationName.Pl_Region,
                              Pl_Region_locations, None)
    Pl2_Region_locations = {
        LocationName.Hyenas2: [1],
        LocationName.Groundshaker: [2],
        LocationName.GroundshakerGetBonus: [3],
        LocationName.SaixDataDefenseBoost: [4],
        LocationName.GoofyHyenas2: [5],
    }
    Pl2_Region = create_region(world, player, active_locations, LocationName.Pl2_Region,
                               Pl2_Region_locations, None)

    STT_Region_locations = {
        LocationName.TwilightTownMap: [1],
        LocationName.MunnyPouchOlette: [2],
        LocationName.StationDusks: [3],
        LocationName.StationofSerenityPotion: [4],
        LocationName.StationofCallingPotion: [5],
        LocationName.TwilightThorn: [6],
        LocationName.Axel1: [7],
        LocationName.JunkChampionBelt: [8],
        LocationName.JunkMedal: [9],
        LocationName.TheStruggleTrophy: [10],
        LocationName.CentralStationPotion1: [11],
        LocationName.STTCentralStationHiPotion: [12],
        LocationName.CentralStationPotion2: [13],
        LocationName.SunsetTerraceAbilityRing: [14],
        LocationName.SunsetTerraceHiPotion: [15],
        LocationName.SunsetTerracePotion1: [16],
        LocationName.SunsetTerracePotion2: [17],
        LocationName.MansionFoyerHiPotion: [18],
        LocationName.MansionFoyerPotion1: [19],
        LocationName.MansionFoyerPotion2: [20],
        LocationName.MansionDiningRoomElvenBandanna: [21],
        LocationName.MansionDiningRoomPotion: [22],
        LocationName.NaminesSketches: [23],
        LocationName.MansionMap: [24],
        LocationName.MansionLibraryHiPotion: [25],
        LocationName.Axel2: [26],
        LocationName.MansionBasementCorridorHiPotion: [27],
        LocationName.RoxasDataMagicBoost: [28],
    }
    STT_Region = create_region(world, player, active_locations, LocationName.STT_Region,
                               STT_Region_locations, None)

    TT_Region_locations = {
        LocationName.OldMansionPotion: [1],
        LocationName.OldMansionMythrilShard: [2],
        LocationName.TheWoodsPotion: [3],
        LocationName.TheWoodsMythrilShard: [4],
        LocationName.TheWoodsHiPotion: [5],
        LocationName.TramCommonHiPotion: [6],
        LocationName.TramCommonAPBoost: [7],
        LocationName.TramCommonTent: [8],
        LocationName.TramCommonMythrilShard1: [9],
        LocationName.TramCommonPotion1: [10],
        LocationName.TramCommonMythrilShard2: [11],
        LocationName.TramCommonPotion2: [12],
        LocationName.StationPlazaSecretAnsemReport2: [13],
        LocationName.MunnyPouchMickey: [14],
        LocationName.CrystalOrb: [15],
        LocationName.CentralStationTent: [16],
        LocationName.TTCentralStationHiPotion: [17],
        LocationName.CentralStationMythrilShard: [18],
        LocationName.TheTowerPotion: [19],
        LocationName.TheTowerHiPotion: [2],
        LocationName.TheTowerEther: [21],
        LocationName.TowerEntrywayEther: [22],
        LocationName.TowerEntrywayMythrilShard: [23],
        LocationName.SorcerersLoftTowerMap: [24],
        LocationName.TowerWardrobeMythrilStone: [25],
        LocationName.StarSeeker: [26],
        LocationName.ValorForm: [27],
    }
    TT_Region = create_region(world, player, active_locations, LocationName.TT_Region,
                              TT_Region_locations, None)
    TT2_Region_locations = {
        LocationName.SeifersTrophy: [1],
        LocationName.Oathkeeper: [2],
        LocationName.LimitForm: [3],
    }
    TT2_Region = create_region(world, player, active_locations, LocationName.TT2_Region,
                               TT2_Region_locations, None)
    TT3_Region_locations = {
        LocationName.UndergroundConcourseMythrilGem: [1],
        LocationName.UndergroundConcourseAPBoost: [2],
        LocationName.UndergroundConcourseMythrilCrystal: [3],
        LocationName.TunnelwayOrichalcum: [4],
        LocationName.TunnelwayMythrilCrystal: [5],
        LocationName.SunsetTerraceOrichalcumPlus: [6],
        LocationName.SunsetTerraceMythrilShard: [7],
        LocationName.SunsetTerraceMythrilCrystal: [8],
        LocationName.SunsetTerraceAPBoost: [9],
        LocationName.MansionNobodies: [10],
        LocationName.MansionFoyerMythrilCrystal: [11],
        LocationName.MansionFoyerMythrilStone: [12],
        LocationName.MansionFoyerSerenityCrystal: [13],
        LocationName.MansionDiningRoomMythrilCrystal: [14],
        LocationName.MansionDiningRoomMythrilStone: [15],
        LocationName.MansionLibraryOrichalcum: [16],
        LocationName.BeamSecretAnsemReport10: [17],
        LocationName.MansionBasementCorridorUltimateRecipe: [18],
        LocationName.BetwixtandBetween: [19],
        LocationName.BetwixtandBetweenBondofFlame: [20],
        LocationName.AxelDataMagicBoost: [21],
        LocationName.DonaldMansionNobodies: [22],
    }
    TT3_Region = create_region(world, player, active_locations, LocationName.TT3_Region,
                               TT3_Region_locations, None)

    Twtnw_Region_locations = {
        LocationName.FragmentCrossingMythrilStone: [1],
        LocationName.FragmentCrossingMythrilCrystal: [2],
        LocationName.FragmentCrossingAPBoost: [3],
        LocationName.FragmentCrossingOrichalcum: [4],
        LocationName.Roxas: [5],
        LocationName.RoxasGetBonus: [5],
        LocationName.RoxasSecretAnsemReport8: [6],
        LocationName.TwoBecomeOne: [7],
        LocationName.MemorysSkyscaperMythrilCrystal: [8],
        LocationName.MemorysSkyscaperAPBoost: [9],
        LocationName.MemorysSkyscaperMythrilStone: [10],
        LocationName.TheBrinkofDespairDarkCityMap: [11],
        LocationName.TheBrinkofDespairOrichalcumPlus: [12],
        LocationName.NothingsCallMythrilGem: [13],
        LocationName.NothingsCallOrichalcum: [14],
        LocationName.TwilightsViewCosmicBelt: [15],
    }
    Twtnw_Region = create_region(world, player, active_locations, LocationName.Twtnw_Region,
                                 Twtnw_Region_locations, None)
    Twtnw2_Region_locations = {
        LocationName.XigbarBonus: [1],
        LocationName.XigbarSecretAnsemReport3: [2],
        LocationName.NaughtsSkywayMythrilGem: [3],
        LocationName.NaughtsSkywayOrichalcum: [4],
        LocationName.NaughtsSkywayMythrilCrystal: [5],
        LocationName.Oblivion: [6],
        LocationName.CastleThatNeverWasMap: [7],
        LocationName.Luxord: [8],
        LocationName.LuxordGetBonus: [9],
        LocationName.LuxordSecretAnsemReport9: [10],
        LocationName.SaixBonus: [11],
        LocationName.SaixSecretAnsemReport12: [12],
        LocationName.PreXemnas1SecretAnsemReport11: [13],
        LocationName.RuinandCreationsPassageMythrilStone: [14],
        LocationName.RuinandCreationsPassageAPBoost: [15],
        LocationName.RuinandCreationsPassageMythrilCrystal: [16],
        LocationName.RuinandCreationsPassageOrichalcum: [17],
        LocationName.Xemnas1: [18],
        LocationName.Xemnas1GetBonus: [18],
        LocationName.Xemnas1SecretAnsemReport13: [19],
        LocationName.FinalXemnas: [20],
        LocationName.XemnasDataPowerBoost: [21],
    }
    Twtnw2_Region = create_region(world, player, active_locations, LocationName.Twtnw2_Region,
                                  Twtnw2_Region_locations, None)

    Valor_Region_locations = {
        LocationName.Valorlvl1: [0],
        LocationName.Valorlvl2: [1],
        LocationName.Valorlvl3: [2],
        LocationName.Valorlvl4: [3],
        LocationName.Valorlvl5: [4],
        LocationName.Valorlvl6: [5],
        LocationName.Valorlvl7: [6],
    }
    Valor_Region = create_region(world, player, active_locations, LocationName.ValorForm,
                                 Valor_Region_locations, None)
    Wisdom_Region_locations = {
        LocationName.Wisdomlvl1: [0],
        LocationName.Wisdomlvl2: [7],
        LocationName.Wisdomlvl3: [8],
        LocationName.Wisdomlvl4: [9],
        LocationName.Wisdomlvl5: [10],
        LocationName.Wisdomlvl6: [11],
        LocationName.Wisdomlvl7: [12],
    }
    Wisdom_Region = create_region(world, player, active_locations, LocationName.WisdomForm,
                                  Wisdom_Region_locations, None)
    Limit_Region_locations = {
        LocationName.Limitlvl1: [0],
        LocationName.Limitlvl2: [13],
        LocationName.Limitlvl3: [14],
        LocationName.Limitlvl4: [15],
        LocationName.Limitlvl5: [16],
        LocationName.Limitlvl6: [17],
        LocationName.Limitlvl7: [18],
    }
    Limit_Region = create_region(world, player, active_locations, LocationName.LimitForm,
                                 Limit_Region_locations, None)
    Master_Region_locations = {
        LocationName.Masterlvl1: [0],
        LocationName.Masterlvl2: [19],
        LocationName.Masterlvl3: [20],
        LocationName.Masterlvl4: [21],
        LocationName.Masterlvl5: [22],
        LocationName.Masterlvl6: [23],
        LocationName.Masterlvl7: [24],
    }
    Master_Region = create_region(world, player, active_locations, LocationName.MasterForm,
                                  Master_Region_locations, None)
    Final_Region_locations = {
        LocationName.Finallvl1: [25],
        LocationName.Finallvl2: [25],
        LocationName.Finallvl3: [26],
        LocationName.Finallvl4: [27],
        LocationName.Finallvl5: [28],
        LocationName.Finallvl6: [29],
        LocationName.Finallvl7: [30],
    }
    Final_Region = create_region(world, player, active_locations, LocationName.FinalForm,
                                 Final_Region_locations, None)
    if world.Level_Depth[player] == 0:
        Level_Region_locations = {
        LocationName.Lvl2 :[1],
        LocationName.Lvl4 :[2],
        LocationName.Lvl7 :[3],
        LocationName.Lvl9 :[4],
        LocationName.Lvl10:[5],
        LocationName.Lvl12:[6],
        LocationName.Lvl14:[7],
        LocationName.Lvl15:[8],
        LocationName.Lvl17:[9],
        LocationName.Lvl20:[10],
        LocationName.Lvl23:[11],
        LocationName.Lvl25:[12],
        LocationName.Lvl28:[13],
        LocationName.Lvl30:[14],
        LocationName.Lvl32:[15],
        LocationName.Lvl34:[16],
        LocationName.Lvl36:[17],
        LocationName.Lvl39:[18],
        LocationName.Lvl41:[19],
        LocationName.Lvl44:[20],
        LocationName.Lvl46:[21],
        LocationName.Lvl48:[22],
        LocationName.Lvl50:[23],
        }
    elif world.Level_Depth[player] == 1:
        Level_Region_locations = {
        LocationName.Lvl7 :[1],
        LocationName.Lvl9 :[2],
        LocationName.Lvl12:[3],
        LocationName.Lvl15:[4],
        LocationName.Lvl17:[5],
        LocationName.Lvl20:[6],
        LocationName.Lvl23:[7],
        LocationName.Lvl25:[8],
        LocationName.Lvl28:[9],
        LocationName.Lvl31:[10],
        LocationName.Lvl33:[11],
        LocationName.Lvl36:[12],
        LocationName.Lvl39:[13],
        LocationName.Lvl41:[14],
        LocationName.Lvl44:[15],
        LocationName.Lvl47:[16],
        LocationName.Lvl49:[17],
        LocationName.Lvl53:[18],
        LocationName.Lvl59:[19],
        LocationName.Lvl65:[20],
        LocationName.Lvl73:[21],
        LocationName.Lvl85:[22],
        LocationName.Lvl99:[23],
        }
    else:
        Level_Region_locations = {
        LocationName.Lvl1: [1],
        LocationName.Lvl2: [2],
        LocationName.Lvl3: [3],
        LocationName.Lvl4: [4],
        LocationName.Lvl5: [5],
        LocationName.Lvl6: [6],
        LocationName.Lvl7: [7],
        LocationName.Lvl8: [8],
        LocationName.Lvl9: [9],
        LocationName.Lvl10: [10],
        LocationName.Lvl11: [11],
        LocationName.Lvl12: [12],
        LocationName.Lvl13: [13],
        LocationName.Lvl14: [14],
        LocationName.Lvl15: [15],
        LocationName.Lvl16: [16],
        LocationName.Lvl17: [17],
        LocationName.Lvl18: [18],
        LocationName.Lvl19: [19],
        LocationName.Lvl20: [20],
        LocationName.Lvl21: [21],
        LocationName.Lvl22: [22],
        LocationName.Lvl23: [23],
        LocationName.Lvl24: [24],
        LocationName.Lvl25: [25],
        LocationName.Lvl26: [26],
        LocationName.Lvl27: [27],
        LocationName.Lvl28: [28],
        LocationName.Lvl29: [29],
        LocationName.Lvl30: [30],
        LocationName.Lvl31: [31],
        LocationName.Lvl32: [32],
        LocationName.Lvl33: [33],
        LocationName.Lvl34: [34],
        LocationName.Lvl35: [35],
        LocationName.Lvl36: [36],
        LocationName.Lvl37: [37],
        LocationName.Lvl38: [38],
        LocationName.Lvl39: [39],
        LocationName.Lvl40: [40],
        LocationName.Lvl41: [41],
        LocationName.Lvl42: [42],
        LocationName.Lvl43: [43],
        LocationName.Lvl44: [44],
        LocationName.Lvl45: [45],
        LocationName.Lvl46: [46],
        LocationName.Lvl47: [47],
        LocationName.Lvl48: [48],
        LocationName.Lvl49: [49],
        LocationName.Lvl50: [50],
        LocationName.Lvl51: [51],
        LocationName.Lvl52: [52],
        LocationName.Lvl53: [53],
        LocationName.Lvl54: [54],
        LocationName.Lvl55: [55],
        LocationName.Lvl56: [56],
        LocationName.Lvl57: [57],
        LocationName.Lvl58: [58],
        LocationName.Lvl59: [59],
        LocationName.Lvl60: [60],
        LocationName.Lvl61: [61],
        LocationName.Lvl62: [62],
        LocationName.Lvl63: [63],
        LocationName.Lvl64: [64],
        LocationName.Lvl65: [65],
        LocationName.Lvl66: [66],
        LocationName.Lvl67: [67],
        LocationName.Lvl68: [68],
        LocationName.Lvl69: [69],
        LocationName.Lvl70: [70],
        LocationName.Lvl71: [71],
        LocationName.Lvl72: [72],
        LocationName.Lvl73: [73],
        LocationName.Lvl74: [74],
        LocationName.Lvl75: [75],
        LocationName.Lvl76: [76],
        LocationName.Lvl77: [77],
        LocationName.Lvl78: [78],
        LocationName.Lvl79: [79],
        LocationName.Lvl80: [80],
        LocationName.Lvl81: [81],
        LocationName.Lvl82: [82],
        LocationName.Lvl83: [83],
        LocationName.Lvl84: [84],
        LocationName.Lvl85: [85],
        LocationName.Lvl86: [86],
        LocationName.Lvl87: [87],
        LocationName.Lvl88: [88],
        LocationName.Lvl89: [89],
        LocationName.Lvl90: [90],
        LocationName.Lvl91: [91],
        LocationName.Lvl92: [92],
        LocationName.Lvl93: [93],
        LocationName.Lvl94: [94],
        LocationName.Lvl95: [95],
        LocationName.Lvl96: [96],
        LocationName.Lvl97: [97],
        LocationName.Lvl98: [98],
        LocationName.Lvl99: [99],
    }
    Level_Region = create_region(world, player, active_locations, LocationName.SoraLevels_Region,
                                 Level_Region_locations, None)
    Keyblade_Region_locations = {
        LocationName.FAKESlot: [1],
        LocationName.DetectionSaberSlot: [2],
        LocationName.EdgeofUltimaSlot: [3],
        LocationName.KingdomKeySlot: [4],
        LocationName.OathkeeperSlot: [5],
        LocationName.OblivionSlot: [6],
        LocationName.StarSeekerSlot: [7],
        LocationName.HiddenDragonSlot: [8],
        LocationName.HerosCrestSlot: [9],
        LocationName.MonochromeSlot: [10],
        LocationName.FollowtheWindSlot: [11],
        LocationName.CircleofLifeSlot: [12],
        LocationName.PhotonDebuggerSlot: [13],
        LocationName.GullWingSlot: [14],
        LocationName.RumblingRoseSlot: [15],
        LocationName.GuardianSoulSlot: [16],
        LocationName.WishingLampSlot: [17],
        LocationName.DecisivePumpkinSlot: [18],
        LocationName.SweetMemoriesSlot: [19],
        LocationName.MysteriousAbyssSlot: [20],
        LocationName.SleepingLionSlot: [21],
        LocationName.BondofFlameSlot: [22],
        LocationName.TwoBecomeOneSlot: [23],
        LocationName.FatalCrestSlot: [24],
        LocationName.FenrirSlot: [25],
        LocationName.UltimaWeaponSlot: [26],
        LocationName.WinnersProofSlot: [27],
        LocationName.PurebloodSlot:     [28],
        LocationName.Centurion2:        [29],
        LocationName.CometStaff:        [30],
        LocationName.HammerStaff:       [31],
        LocationName.LordsBroom:        [32],
        LocationName.MagesStaff:        [33],
        LocationName.MeteorStaff:       [34],
        LocationName.NobodyLance:       [35],
        LocationName.PreciousMushroom:  [36],
        LocationName.PreciousMushroom2: [37],
        LocationName.PremiumMushroom:   [38],
        LocationName.RisingDragon:      [39],
        LocationName.SaveTheQueen2:     [40],
        LocationName.ShamansRelic:      [41],
        LocationName.VictoryBell:       [42],
        LocationName.WisdomWand:        
                                        [43],
        LocationName.AdamantShield:     [44],
        LocationName.AkashicRecord:     [45],
        LocationName.ChainGear:         [46],
        LocationName.DreamCloud:        [47],
        LocationName.FallingStar:       [48],
        LocationName.FrozenPride2:      [49],
        LocationName.GenjiShield:       [50],
        LocationName.KnightDefender:    [51],
        LocationName.KnightsShield:     [52],
        LocationName.MajesticMushroom:  [53],
        LocationName.MajesticMushroom2: [54],
        LocationName.NobodyGuard:       [55],
        LocationName.OgreShield:        [56],
        LocationName.SaveTheKing2:      [57],
        LocationName.UltimateMushroom:  [58],
    }
    Keyblade_Region = create_region(world, player, active_locations, LocationName.Keyblade_Region,
                                    Keyblade_Region_locations, None)

    world.regions += [
        LoD_Region,
        LoD2_Region,
        Ag_Region,
        Ag2_Region,
        Dc_Region,
        Tr_Region,
        HundredAcre1_Region,
        HundredAcre2_Region,
        HundredAcre3_Region,
        HundredAcre4_Region,
        HundredAcre5_Region,
        HundredAcre6_Region,
        Pr_Region,
        Pr2_Region,
        Oc_Region,
        Oc2_Region,
        Oc2Cups_Region,
        Bc_Region,
        Bc2_Region,
        Sp_Region,
        Sp2_Region,
        Ht_Region,
        Ht2_Region,
        Hb_Region,
        Hb2_Region,
        CoR_Region,
        Pl_Region,
        Pl2_Region,
        STT_Region,
        TT_Region,
        TT2_Region,
        TT3_Region,
        Twtnw_Region,
        Twtnw2_Region,
        GoA_Region,
        menu_region,
        Valor_Region,
        Wisdom_Region,
        Limit_Region,
        Master_Region,
        Final_Region,
        Level_Region,
        Keyblade_Region,
    ]


def connect_regions(world: MultiWorld, player: int, self):
    # connecting every first visit to the GoA
    # 2 Visit locking and is going to be turned off mabybe

    names: typing.Dict[str, int] = {}
    connect(world, player, names, 'Menu', LocationName.GoA_Region)
    connect(world, player, names, "Menu", LocationName.Keyblade_Region)
    connect(world, player, names, LocationName.GoA_Region, LocationName.LoD_Region)
    connect(world, player, names, LocationName.LoD_Region, LocationName.LoD2_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.Oc_Region)
    connect(world, player, names, LocationName.Oc_Region, LocationName.Oc2_Region)

    connect(world, player, names, LocationName.Oc2_Region, LocationName.Oc2Cups_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.Ag_Region)
    connect(world, player, names, LocationName.Ag_Region, LocationName.Ag2_Region,
            lambda state: (state.has(ItemName.FireElement, player)
                           and state.has(ItemName.BlizzardElement, player)
                           and state.has(ItemName.ThunderElement, player)))

    connect(world, player, names, LocationName.GoA_Region, LocationName.Dc_Region)
    connect(world, player, names, LocationName.Dc_Region, LocationName.Tr_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.Pr_Region)
    connect(world, player, names, LocationName.Pr_Region, LocationName.Pr2_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.Bc_Region)
    connect(world, player, names, LocationName.Bc_Region, LocationName.Bc2_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.Sp_Region)
    connect(world, player, names, LocationName.Sp_Region, LocationName.Sp2_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.Ht_Region)
    connect(world, player, names, LocationName.Ht_Region, LocationName.Ht2_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.Hb_Region)
    connect(world, player, names, LocationName.Hb_Region, LocationName.Hb2_Region)

    connect(world, player, names, LocationName.Hb2_Region, LocationName.CoR_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.Pl_Region)
    connect(world, player, names, LocationName.Pl_Region, LocationName.Pl2_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.STT_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.TT_Region)
    connect(world, player, names, LocationName.TT_Region, LocationName.TT2_Region)
    connect(world, player, names, LocationName.TT2_Region, LocationName.TT3_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.Twtnw_Region)
    connect(world, player, names, LocationName.Twtnw_Region, LocationName.Twtnw2_Region)

    connect(world, player, names, LocationName.GoA_Region, LocationName.HundredAcre1_Region)
    connect(world, player, names, LocationName.GoA_Region, LocationName.HundredAcre2_Region,
            lambda state: (state.has(ItemName.TornPages, player, 1)))
    connect(world, player, names, LocationName.GoA_Region, LocationName.HundredAcre3_Region,
            lambda state: (state.has(ItemName.TornPages, player, 2)))
    connect(world, player, names, LocationName.GoA_Region, LocationName.HundredAcre4_Region,
            lambda state: (state.has(ItemName.TornPages, player, 3)))
    connect(world, player, names, LocationName.GoA_Region, LocationName.HundredAcre5_Region,
            lambda state: (state.has(ItemName.TornPages, player, 4)))
    connect(world, player, names, LocationName.GoA_Region, LocationName.HundredAcre6_Region,
            lambda state: (state.has(ItemName.TornPages, player, 5)))

    for region in (firstVisits):
        connect(world, player, names, region, LocationName.SoraLevels_Region)

        connect(world, player, names, region, LocationName.Valor_Region,
                lambda state: state.has(ItemName.ValorForm, player))
        connect(world, player, names, region, LocationName.Wisdom_Region,
                lambda state: state.has(ItemName.WisdomForm, player))
        connect(world, player, names, region, LocationName.Limit_Region,
                lambda state: state.has(ItemName.LimitForm, player))
        connect(world, player, names, region, LocationName.Master_Region,
                lambda state: state.has(ItemName.MasterForm, player))
        connect(world, player, names, region, LocationName.Final_Region,
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
        name = target + (' ' * used_names[source])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None, exits=None):
    # Shamelessly stolen from the SA2B definition that stole from ROR2 definition
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = active_locations.get(location, 0)
            if loc_id:
                location = KH2Location(player, location, loc_id.code, ret)
                ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))
    return ret
