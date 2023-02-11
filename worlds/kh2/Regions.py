import typing

from BaseClasses import MultiWorld, Region, Entrance

from .Locations import KH2Location, valorLevelRegions,wisdomLevelRegions,limitLevelRegions,masterLevelRegions,finalLevelRegions,firstVisits,secondVisits
from .Names import LocationName, ItemName, RegionName


def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None, None)

    goa_region_locations = {
        LocationName.Crit_1:                [1],
        LocationName.Crit_2:                [2],
        LocationName.Crit_3:                [3],
        LocationName.Crit_4:                [4],
        LocationName.Crit_5:                [5],
        LocationName.Crit_6:                [6],
        LocationName.Crit_7:                [7],
        LocationName.GardenofAssemblageMap: [8],
        LocationName.GoALostIllusion:       [9],
        LocationName.ProofofNonexistence:   [10],
        LocationName.DonaldStarting1:       [11],
        LocationName.DonaldStarting2:       [12],
        LocationName.GoofyStarting1:        [13],
        LocationName.GoofyStarting2:        [14],
    }
    goa_region = create_region(world, player, active_locations, RegionName.GoA_Region,
                               goa_region_locations, None)

    lod_Region_locations = {
        LocationName.BambooGroveDarkShard:        [1],
        LocationName.BambooGroveEther:            [2],
        LocationName.BambooGroveMythrilShard:     [3],
        LocationName.EncampmentAreaMap:           [4],
        LocationName.Mission3:                    [5],
        LocationName.CheckpointHiPotion:          [6],
        LocationName.CheckpointMythrilShard:      [7],
        LocationName.MountainTrailLightningShard: [8],
        LocationName.MountainTrailRecoveryRecipe: [9],
        LocationName.MountainTrailEther:          [10],
        LocationName.MountainTrailMythrilShard:   [11],
        LocationName.VillageCaveAreaMap:          [12],
        LocationName.VillageCaveAPBoost:          [13],
        LocationName.VillageCaveDarkShard:        [14],
        LocationName.VillageCaveBonus:            [15],
        LocationName.RidgeFrostShard:             [16],
        LocationName.RidgeAPBoost:                [17],
        LocationName.ShanYu:                      [18],
        LocationName.ShanYuGetBonus:              [19],
        LocationName.HiddenDragon:                [20],
        LocationName.GoofyShanYu:                 [21],
    }
    lod_Region = create_region(world, player, active_locations, RegionName.LoD_Region,
                               lod_Region_locations, None)
    lod2_Region_locations = {
        LocationName.ThroneRoomTornPages:      [1],
        LocationName.ThroneRoomPalaceMap:      [2],
        LocationName.ThroneRoomAPBoost:        [3],
        LocationName.ThroneRoomQueenRecipe:    [4],
        LocationName.ThroneRoomAPBoost2:       [5],
        LocationName.ThroneRoomOgreShield:     [6],
        LocationName.ThroneRoomMythrilCrystal: [7],
        LocationName.ThroneRoomOrichalcum:     [8],
        LocationName.StormRider:               [9],
        LocationName.XigbarDataDefenseBoost:   [10],
        LocationName.GoofyStormRider:          [11],
    }
    lod2_Region = create_region(world, player, active_locations, RegionName.LoD2_Region,
                                lod2_Region_locations, None)
    ag_region_locations = {
        LocationName.AgrabahMap:                        [1],
        LocationName.AgrabahDarkShard:                  [2],
        LocationName.AgrabahMythrilShard:               [3],
        LocationName.AgrabahHiPotion:                   [4],
        LocationName.AgrabahAPBoost:                    [5],
        LocationName.AgrabahMythrilStone:               [6],
        LocationName.AgrabahMythrilShard2:              [7],
        LocationName.AgrabahSerenityShard:              [8],
        LocationName.BazaarMythrilGem:                  [9],
        LocationName.BazaarPowerShard:                  [10],
        LocationName.BazaarHiPotion:                    [11],
        LocationName.BazaarAPBoost:                     [12],
        LocationName.BazaarMythrilShard:                [13],
        LocationName.PalaceWallsSkillRing:              [14],
        LocationName.PalaceWallsMythrilStone:           [15],
        LocationName.CaveEntrancePowerStone:            [16],
        LocationName.CaveEntranceMythrilShard:          [17],
        LocationName.ValleyofStoneMythrilStone:         [18],
        LocationName.ValleyofStoneAPBoost:              [19],
        LocationName.ValleyofStoneMythrilShard:         [20],
        LocationName.ValleyofStoneHiPotion:             [21],
        LocationName.AbuEscort:                         [22],
        LocationName.ChasmofChallengesCaveofWondersMap: [23],
        LocationName.ChasmofChallengesAPBoost:          [24],
        LocationName.TreasureRoom:                      [25],
        LocationName.TreasureRoomAPBoost:               [26],
        LocationName.TreasureRoomSerenityGem:           [27],
        LocationName.ElementalLords:                    [28],
        LocationName.LampCharm:                         [29],
        LocationName.GoofyTreasureRoom:                 [30],
        LocationName.DonaldAbuEscort:                   [31],
    }
    ag_region = create_region(world, player, active_locations, RegionName.Ag_Region,
                              ag_region_locations, None)
    ag2_region_locations = {
        LocationName.RuinedChamberTornPages:          [1],
        LocationName.RuinedChamberRuinsMap:           [2],
        LocationName.GenieJafar:                      [3],
        LocationName.WishingLamp:                     [4],
    }
    ag2_region = create_region(world, player, active_locations, RegionName.Ag2_Region,
                               ag2_region_locations, None)
    lexaeus_region_locations={
        LocationName.LexaeusBonus:                    [5],
        LocationName.LexaeusASStrengthBeyondStrength: [6],
        LocationName.LexaeusDataLostIllusion:         [7],
    }
    lexaeus_region=create_region(world, player, active_locations, RegionName.Lexaeus_Region,
                               lexaeus_region_locations, None)

    dc_region_locations = {
        LocationName.DCCourtyardMythrilShard:  [1],
        LocationName.DCCourtyardStarRecipe:    [2],
        LocationName.DCCourtyardAPBoost:       [3],
        LocationName.DCCourtyardMythrilStone:  [4],
        LocationName.DCCourtyardBlazingStone:  [5],
        LocationName.DCCourtyardBlazingShard:  [6],
        LocationName.DCCourtyardMythrilShard2: [7],
        LocationName.LibraryTornPages:         [8],
        LocationName.DisneyCastleMap:          [9],
        LocationName.MinnieEscort:             [10],
        LocationName.MinnieEscortGetBonus:     [11],
    }
    dc_region = create_region(world, player, active_locations, RegionName.Dc_Region,
                              dc_region_locations, None)
    tr_region_locations = {
        LocationName.CornerstoneHillMap:             [1],
        LocationName.CornerstoneHillFrostShard:      [2],
        LocationName.PierMythrilShard:               [3],
        LocationName.PierHiPotion:                   [4],
        LocationName.WaterwayMythrilStone:           [5],
        LocationName.WaterwayAPBoost:                [6],
        LocationName.WaterwayFrostStone:             [7],
        LocationName.WindowofTimeMap:                [8],
        LocationName.BoatPete:                       [9],
        LocationName.FuturePete:                     [10],
        LocationName.FuturePeteGetBonus:             [10],
        LocationName.Monochrome:                     [11],
        LocationName.WisdomForm:                     [12],




        LocationName.DonaldBoatPete:                 [19],
        LocationName.DonaldBoatPeteGetBonus:         [20],
        LocationName.GoofyFuturePete:                [21],
    }
    tr_region = create_region(world, player, active_locations, RegionName.Tr_Region,
                              tr_region_locations, None)
    marluxia_region_locations={
        LocationName.MarluxiaGetBonus,
        LocationName.MarluxiaASEternalBlossom,
        LocationName.MarluxiaDataLostIllusion,
    }
    marluxia_region=create_region(world, player, active_locations, RegionName.Marluxia_Region,
                              marluxia_region_locations, None)
    terra_region_locations={
        LocationName.LingeringWillBonus:             [16],
        LocationName.LingeringWillProofofConnection: [17],
        LocationName.LingeringWillManifestIllusion:  [18],
    }
    terra_region=create_region(world, player, active_locations, RegionName.Terra_Region,
                              terra_region_locations, None)

    hundred_acre1_region_locations = {
        LocationName.PoohsHouse100AcreWoodMap: [1],
        LocationName.PoohsHouseAPBoost:        [2],
        LocationName.PoohsHouseMythrilStone:   [3],
    }
    hundred_acre1_region = create_region(world, player, active_locations, RegionName.HundredAcre1_Region,
                                         hundred_acre1_region_locations, None)
    hundred_acre2_region_locations = {
        LocationName.PigletsHouseDefenseBoost: [1],
        LocationName.PigletsHouseAPBoost:      [2],
        LocationName.PigletsHouseMythrilGem:   [3],
    }
    hundred_acre2_region = create_region(world, player, active_locations, RegionName.HundredAcre2_Region,
                                         hundred_acre2_region_locations, None)
    hundred_acre3_region_locations = {
        LocationName.RabbitsHouseDrawRing:       [1],
        LocationName.RabbitsHouseMythrilCrystal: [2],
        LocationName.RabbitsHouseAPBoost:        [3],
    }
    hundred_acre3_region = create_region(world, player, active_locations, RegionName.HundredAcre3_Region,
                                         hundred_acre3_region_locations, None)
    hundred_acre4_region_locations = {
        LocationName.KangasHouseMagicBoost: [1],
        LocationName.KangasHouseAPBoost:    [2],
        LocationName.KangasHouseOrichalcum: [3],
    }
    hundred_acre4_region = create_region(world, player, active_locations, RegionName.HundredAcre4_Region,
                                         hundred_acre4_region_locations, None)
    hundred_acre5_region_locations = {
        LocationName.SpookyCaveMythrilGem:     [1],
        LocationName.SpookyCaveAPBoost:        [2],
        LocationName.SpookyCaveOrichalcum:     [3],
        LocationName.SpookyCaveGuardRecipe:    [4],
        LocationName.SpookyCaveMythrilCrystal: [5],
        LocationName.SpookyCaveAPBoost2:       [6],
        LocationName.SweetMemories:            [7],
        LocationName.SpookyCaveMap:            [8],
    }
    hundred_acre5_region = create_region(world, player, active_locations, RegionName.HundredAcre5_Region,
                                         hundred_acre5_region_locations, None)
    hundred_acre6_region_locations = {
        LocationName.StarryHillCosmicRing:     [1],
        LocationName.StarryHillStyleRecipe:    [2],
        LocationName.StarryHillCureElement:    [3],
        LocationName.StarryHillOrichalcumPlus: [4],
    }
    hundred_acre6_region = create_region(world, player, active_locations, RegionName.HundredAcre6_Region,
                                         hundred_acre6_region_locations, None)
    pr_region_locations = {
        LocationName.RampartNavalMap:           [1],
        LocationName.RampartMythrilStone:       [2],
        LocationName.RampartDarkShard:          [3],
        LocationName.TownDarkStone:             [4],
        LocationName.TownAPBoost:               [5],
        LocationName.TownMythrilShard:          [6],
        LocationName.TownMythrilGem:            [7],
        LocationName.CaveMouthBrightShard:      [8],
        LocationName.CaveMouthMythrilShard:     [9],
        LocationName.IsladeMuertaMap:           [10],
        LocationName.BoatFight:                 [11],
        LocationName.InterceptorBarrels:        [12],
        LocationName.PowderStoreAPBoost1:       [13],
        LocationName.PowderStoreAPBoost2:       [14],
        LocationName.MoonlightNookMythrilShard: [15],
        LocationName.MoonlightNookSerenityGem:  [16],
        LocationName.MoonlightNookPowerStone:   [17],
        LocationName.Barbossa:                  [18],
        LocationName.BarbossaGetBonus:          [19],
        LocationName.FollowtheWind:             [20],
        LocationName.DonaldBoatFight:           [21],
        LocationName.GoofyBarbossa:             [22],
        LocationName.GoofyBarbossaGetBonus:     [23],
        LocationName.GoofyInterceptorBarrels:   [24],
    }
    pr_region = create_region(world, player, active_locations, RegionName.Pr_Region,
                              pr_region_locations, None)
    pr2_region_locations = {
        LocationName.GrimReaper1:                  [1],
        LocationName.InterceptorsHoldFeatherCharm: [2],
        LocationName.SeadriftKeepAPBoost:          [3],
        LocationName.SeadriftKeepOrichalcum:       [4],
        LocationName.SeadriftKeepMeteorStaff:      [5],
        LocationName.SeadriftRowSerenityGem:       [6],
        LocationName.SeadriftRowKingRecipe:        [7],
        LocationName.SeadriftRowMythrilCrystal:    [8],
        LocationName.SeadriftRowCursedMedallion:   [9],
        LocationName.SeadriftRowShipGraveyardMap:  [10],
        LocationName.GrimReaper2:                  [11],
        LocationName.SecretAnsemReport6:           [12],
        LocationName.LuxordDataAPBoost:            [13],
        LocationName.GoofyGrimReaper1:             [14],
        LocationName.DonaladGrimReaper2:           [15],
    }
    pr2_region = create_region(world, player, active_locations, RegionName.Pr2_Region,
                               pr2_region_locations, None)
    oc_region_locations = {
        LocationName.PassageMythrilShard:          [1],
        LocationName.PassageMythrilStone:          [2],
        LocationName.PassageEther:                 [3],
        LocationName.PassageAPBoost:               [4],
        LocationName.PassageHiPotion:              [5],
        LocationName.InnerChamberUnderworldMap:    [6],
        LocationName.InnerChamberMythrilShard:     [7],
        LocationName.Cerberus:                     [8],
        LocationName.ColiseumMap:                  [9],
        LocationName.Urns:                         [10],
        LocationName.UnderworldEntrancePowerBoost: [11],
        LocationName.CavernsEntranceLucidShard:    [12],
        LocationName.CavernsEntranceAPBoost:       [13],
        LocationName.CavernsEntranceMythrilShard:  [14],
        LocationName.TheLostRoadBrightShard:       [15],
        LocationName.TheLostRoadEther:             [16],
        LocationName.TheLostRoadMythrilShard:      [17],
        LocationName.TheLostRoadMythrilStone:      [18],
        LocationName.AtriumLucidStone:             [19],
        LocationName.AtriumAPBoost:                [20],
        LocationName.DemyxOC:                      [21],
        LocationName.SecretAnsemReport5:           [22],
        LocationName.OlympusStone:                 [23],
        LocationName.TheLockCavernsMap:            [24],
        LocationName.TheLockMythrilShard:          [25],
        LocationName.TheLockAPBoost:               [26],
        LocationName.PeteOC:                       [27],
        LocationName.Hydra:                        [28],
        LocationName.HydraGetBonus:                [29],
        LocationName.HerosCrest:                   [30],
        LocationName.DonaldDemyxOC:                [31],
        LocationName.GoofyPeteOC:                  [32],
    }
    oc_region = create_region(world, player, active_locations, RegionName.Oc_Region,
                              oc_region_locations, None)
    oc2_region_locations = {
        LocationName.AuronsStatue:           [1],
        LocationName.Hades:                  [2],
        LocationName.HadesGetBonus:          [3],
        LocationName.GuardianSoul:           [4],

    }
    oc2_region = create_region(world, player, active_locations, RegionName.Oc2_Region,
                               oc2_region_locations, None)
    oc2_pain_and_panic_locations = {
        LocationName.ProtectBeltPainandPanicCup: [1],
        LocationName.SerenityGemPainandPanicCup: [3],
    }
    oc2_titan_locations={
        LocationName.GenjiShieldTitanCup:  [6],
        LocationName.SkillfulRingTitanCup: [7],
    }
    oc2_cerberus_locations={
        LocationName.RisingDragonCerberusCup:    [4],
        LocationName.SerenityCrystalCerberusCup: [5],
    }
    oc2_gof_cup_locations={
        LocationName.FatalCrestGoddessofFateCup:     [8],
        LocationName.OrichalcumPlusGoddessofFateCup: [9],
        LocationName.HadesCupTrophyParadoxCups:      [10],
    }
    zexion_region_locations={
        LocationName.ZexionBonus          ,
        LocationName.ZexionASBookofShadows,
        LocationName.ZexionDataLostIllusion,
        LocationName.GoofyZexion          ,
    }
    oc2_pain_and_panic_cup      =create_region(world,player,active_locations,RegionName.Oc2_pain_and_panic_Region,oc2_pain_and_panic_locations,None)
    oc2_titan_cup               =create_region(world,player,active_locations,RegionName.Oc2_titan_Region,oc2_titan_locations,None)
    oc2_cerberus_cup            =create_region(world,player,active_locations,RegionName.Oc2_cerberus_Region,oc2_cerberus_locations,None)
    oc2_gof_cup                 =create_region(world,player,active_locations,RegionName.Oc2_gof_Region,oc2_gof_cup_locations,None)
    zexion_region               =create_region(world,player,active_locations,RegionName.Zexion_Region,zexion_region_locations,None)

    bc_region_locations = {
        LocationName.BCCourtyardAPBoost:            [1],
        LocationName.BCCourtyardHiPotion:           [2],
        LocationName.BCCourtyardMythrilShard:       [3],
        LocationName.BellesRoomCastleMap:           [4],
        LocationName.BellesRoomMegaRecipe:          [5],
        LocationName.TheEastWingMythrilShard:       [6],
        LocationName.TheEastWingTent:               [7],
        LocationName.TheWestHallHiPotion:           [8],
        LocationName.TheWestHallPowerShard:         [9],
        LocationName.TheWestHallMythrilShard2:      [10],
        LocationName.TheWestHallBrightStone:        [11],
        LocationName.TheWestHallMythrilShard:       [12],
        LocationName.Thresholder:                   [13],
        LocationName.DungeonBasementMap:            [14],
        LocationName.DungeonAPBoost:                [15],
        LocationName.SecretPassageMythrilShard:     [16],
        LocationName.SecretPassageHiPotion:         [17],
        LocationName.SecretPassageLucidShard:       [18],
        LocationName.TheWestHallAPBoostPostDungeon: [19],
        LocationName.TheWestWingMythrilShard:       [20],
        LocationName.TheWestWingTent:               [21],
        LocationName.Beast:                         [22],
        LocationName.TheBeastsRoomBlazingShard:     [23],
        LocationName.DarkThorn:                     [25],
        LocationName.DarkThornGetBonus:             [26],
        LocationName.DarkThornCureElement:          [27],
        LocationName.DonaldThresholder:             [28],
        LocationName.GoofyBeast:                    [29],

    }
    bc_region = create_region(world, player, active_locations, RegionName.Bc_Region,
                              bc_region_locations, None)
    bc2_region_locations = {
        LocationName.RumblingRose:           [1],
        LocationName.CastleWallsMap:         [2],
        LocationName.Xaldin:                 [3],
        LocationName.XaldinGetBonus:         [4],
        LocationName.SecretAnsemReport4:     [5],
        LocationName.XaldinDataDefenseBoost: [6],
        LocationName.DonaldXaldinGetBonus:   [7],
    }
    bc2_region = create_region(world, player, active_locations, RegionName.Bc2_Region,
                               bc2_region_locations, None)
    sp_region_locations = {
        LocationName.PitCellAreaMap:               [1],
        LocationName.PitCellMythrilCrystal:        [2],
        LocationName.CanyonDarkCrystal:            [3],
        LocationName.CanyonMythrilStone:           [4],
        LocationName.CanyonMythrilGem:             [5],
        LocationName.CanyonFrostCrystal:           [6],
        LocationName.Screens:                      [7],
        LocationName.HallwayPowerCrystal:          [8],
        LocationName.HallwayAPBoost:               [9],
        LocationName.CommunicationsRoomIOTowerMap: [10],
        LocationName.CommunicationsRoomGaiaBelt:   [11],
        LocationName.HostileProgram:               [12],
        LocationName.HostileProgramGetBonus:       [13],
        LocationName.PhotonDebugger:               [14],
        LocationName.DonaldScreens:                [15],
        LocationName.GoofyHostileProgram:          [16],

    }
    sp_region = create_region(world, player, active_locations, RegionName.Sp_Region,
                              sp_region_locations, None)
    sp2_region_locations = {
        LocationName.SolarSailer:                       [1],
        LocationName.CentralComputerCoreAPBoost:        [2],
        LocationName.CentralComputerCoreOrichalcumPlus: [3],
        LocationName.CentralComputerCoreCosmicArts:     [4],
        LocationName.CentralComputerCoreMap:            [5],
        LocationName.MCP:                               [6],
        LocationName.MCPGetBonus:                       [7],

        LocationName.DonaldSolarSailer:                 [11],
    }
    sp2_region = create_region(world, player, active_locations, RegionName.Sp2_Region,
                               sp2_region_locations, None)
    larxene_region_locations={
        LocationName.LarxeneBonus,
        LocationName.LarxeneASCloakedThunder,
        LocationName.LarxeneDataLostIllusion,
    }
    larxene_region=create_region(world, player, active_locations, RegionName.Larxene_Region,
                               larxene_region_locations, None)
    ht_region_locations = {
        LocationName.GraveyardMythrilShard:           [1],
        LocationName.GraveyardSerenityGem:            [2],
        LocationName.FinklesteinsLabHalloweenTownMap: [3],
        LocationName.TownSquareMythrilStone:          [4],
        LocationName.TownSquareEnergyShard:           [5],
        LocationName.HinterlandsLightningShard:       [6],
        LocationName.HinterlandsMythrilStone:         [7],
        LocationName.HinterlandsAPBoost:              [8],
        LocationName.CandyCaneLaneMegaPotion:         [9],
        LocationName.CandyCaneLaneMythrilGem:         [10],
        LocationName.CandyCaneLaneLightningStone:     [11],
        LocationName.CandyCaneLaneMythrilStone:       [12],
        LocationName.SantasHouseChristmasTownMap:     [13],
        LocationName.SantasHouseAPBoost:              [14],
        LocationName.PrisonKeeper:                    [15],
        LocationName.OogieBoogie:                     [16],
        LocationName.OogieBoogieMagnetElement:        [17],
        LocationName.DonaldPrisonKeeper:              [18],
        LocationName.GoofyOogieBoogie:                [19],
    }
    ht_region = create_region(world, player, active_locations, RegionName.Ht_Region,
                              ht_region_locations, None)
    ht2_region_locations = {
        LocationName.Lock:                   [1],
        LocationName.Present:                [2],
        LocationName.DecoyPresents:          [3],
        LocationName.Experiment:             [4],
        LocationName.DecisivePumpkin:        [5],

        LocationName.DonaldExperiment:       [9],
        LocationName.GoofyLock:              [10],
    }
    ht2_region = create_region(world, player, active_locations, RegionName.Ht2_Region,
                               ht2_region_locations, None)
    vexen_region_locations={
        LocationName.VexenBonus,
        LocationName.VexenASRoadtoDiscovery,
        LocationName.VexenDataLostIllusion,
    }
    vexen_region=create_region(world, player, active_locations, RegionName.Vexen_Region,
                               vexen_region_locations, None)
    hb_region_locations = {
        LocationName.MarketplaceMap:              [1],
        LocationName.BoroughDriveRecovery:        [2],
        LocationName.BoroughAPBoost:              [3],
        LocationName.BoroughHiPotion:             [4],
        LocationName.BoroughMythrilShard:         [5],
        LocationName.BoroughDarkShard:            [6],
        LocationName.MerlinsHouseMembershipCard:  [7],
        LocationName.MerlinsHouseBlizzardElement: [8],
        LocationName.Bailey:                      [9],
        LocationName.BaileySecretAnsemReport7:    [10],
        LocationName.BaseballCharm:               [11],
    }
    hb_region = create_region(world, player, active_locations, RegionName.Hb_Region,
                              hb_region_locations, None)
    hb2_region_locations = {
        LocationName.PosternCastlePerimeterMap:                    [1],
        LocationName.PosternMythrilGem:                            [2],
        LocationName.PosternAPBoost:                               [3],
        LocationName.CorridorsMythrilStone:                        [4],
        LocationName.CorridorsMythrilCrystal:                      [5],
        LocationName.CorridorsDarkCrystal:                         [6],
        LocationName.CorridorsAPBoost:                             [7],
        LocationName.AnsemsStudyMasterForm:                        [8],
        LocationName.AnsemsStudySleepingLion:                      [9],
        LocationName.AnsemsStudySkillRecipe:                       [10],
        LocationName.AnsemsStudyUkuleleCharm:                      [11],
        LocationName.RestorationSiteMoonRecipe:                    [12],
        LocationName.RestorationSiteAPBoost:                       [13],
        LocationName.DemyxHB:                                      [14],
        LocationName.DemyxHBGetBonus:                              [14],
        LocationName.FFFightsCureElement:                          [15],
        LocationName.CrystalFissureTornPages:                      [16],
        LocationName.CrystalFissureTheGreatMawMap:                 [17],
        LocationName.CrystalFissureEnergyCrystal:                  [18],
        LocationName.CrystalFissureAPBoost:                        [19],
        LocationName.ThousandHeartless:                            [20],
        LocationName.ThousandHeartlessSecretAnsemReport1:          [21],
        LocationName.ThousandHeartlessIceCream:                    [22],
        LocationName.ThousandHeartlessPicture:                     [23],
        LocationName.PosternGullWing:                              [24],
        LocationName.HeartlessManufactoryCosmicChain:              [25],
        LocationName.WinnersProof:                                 [26],
        LocationName.ProofofPeace:                                 [27],
        LocationName.DemyxDataAPBoost:                             [28],
        LocationName.CoRDepthsAPBoost:                             [29],
        LocationName.CoRDepthsPowerCrystal:                        [30],
        LocationName.CoRDepthsFrostCrystal:                        [31],
        LocationName.CoRDepthsManifestIllusion:                    [32],
        LocationName.CoRDepthsAPBoost2:                            [33],
        LocationName.CoRMineshaftLowerLevelDepthsofRemembranceMap: [34],
        LocationName.CoRMineshaftLowerLevelAPBoost:                [35],
        LocationName.DonaldDemyxHBGetBonus:                        [36],
    }
    hb2_region = create_region(world, player, active_locations, RegionName.Hb2_Region,
                               hb2_region_locations, None)
    sephi_region_locations={
        LocationName.SephirothBonus,
        LocationName.SephirothFenrir,
    }
    sephi_region=create_region(world, player, active_locations, RegionName.Sephi_Region,
                               sephi_region_locations, None)


    cor_region_locations = {
        LocationName.CoRDepthsUpperLevelRemembranceGem:  [1],
        LocationName.CoRMiningAreaSerenityGem:           [2],
        LocationName.CoRMiningAreaAPBoost:               [3],
        LocationName.CoRMiningAreaSerenityCrystal:       [4],
        LocationName.CoRMiningAreaManifestIllusion:      [5],
        LocationName.CoRMiningAreaSerenityGem2:          [6],
        LocationName.CoRMiningAreaDarkRemembranceMap:    [7],
        LocationName.CoRMineshaftMidLevelPowerBoost:     [8],
        LocationName.CoREngineChamberSerenityCrystal:    [9],
        LocationName.CoREngineChamberRemembranceCrystal: [10],
        LocationName.CoREngineChamberAPBoost:            [11],
        LocationName.CoREngineChamberManifestIllusion:   [12],
        LocationName.CoRMineshaftUpperLevelMagicBoost:   [13],
    }
    cor_region = create_region(world, player, active_locations, RegionName.CoR_Region,
                               cor_region_locations, None)
    transport_region_locations={
        LocationName.CoRMineshaftUpperLevelAPBoost,
        LocationName.TransporttoRemembrance,
    }
    transport_region=create_region(world, player, active_locations, RegionName.Transport_Region,
                               transport_region_locations, None)
    pl_region_locations = {
        LocationName.GorgeSavannahMap:              [1],
        LocationName.GorgeDarkGem:                  [2],
        LocationName.GorgeMythrilStone:             [3],
        LocationName.ElephantGraveyardFrostGem:     [4],
        LocationName.ElephantGraveyardMythrilStone: [5],
        LocationName.ElephantGraveyardBrightStone:  [6],
        LocationName.ElephantGraveyardAPBoost:      [7],
        LocationName.ElephantGraveyardMythrilShard: [8],
        LocationName.PrideRockMap:                  [9],
        LocationName.PrideRockMythrilStone:         [10],
        LocationName.PrideRockSerenityCrystal:      [11],
        LocationName.WildebeestValleyEnergyStone:   [12],
        LocationName.WildebeestValleyAPBoost:       [13],
        LocationName.WildebeestValleyMythrilGem:    [14],
        LocationName.WildebeestValleyMythrilStone:  [15],
        LocationName.WildebeestValleyLucidGem:      [16],
        LocationName.WastelandsMythrilShard:        [17],
        LocationName.WastelandsSerenityGem:         [18],
        LocationName.WastelandsMythrilStone:        [19],
        LocationName.JungleSerenityGem:             [20],
        LocationName.JungleMythrilStone:            [21],
        LocationName.JungleSerenityCrystal:         [22],
        LocationName.OasisMap:                      [23],
        LocationName.OasisTornPages:                [24],
        LocationName.OasisAPBoost:                  [25],
        LocationName.CircleofLife:                  [26],
        LocationName.Hyenas1:                       [27],
        LocationName.Scar:                          [28],
        LocationName.ScarFireElement:               [29],
        LocationName.DonaldScar:                    [30],
        LocationName.GoofyHyenas1:                  [31],

    }
    pl_region = create_region(world, player, active_locations, RegionName.Pl_Region,
                              pl_region_locations, None)
    pl2_region_locations = {
        LocationName.Hyenas2:              [1],
        LocationName.Groundshaker:         [2],
        LocationName.GroundshakerGetBonus: [3],
        LocationName.SaixDataDefenseBoost: [4],
        LocationName.GoofyHyenas2:         [5],
    }
    pl2_region = create_region(world, player, active_locations, RegionName.Pl2_Region,
                               pl2_region_locations, None)

    stt_region_locations = {
        LocationName.TwilightTownMap:                 [1],
        LocationName.MunnyPouchOlette:                [2],
        LocationName.StationDusks:                    [3],
        LocationName.StationofSerenityPotion:         [4],
        LocationName.StationofCallingPotion:          [5],
        LocationName.TwilightThorn:                   [6],
        LocationName.Axel1:                           [7],
        LocationName.JunkChampionBelt:                [8],
        LocationName.JunkMedal:                       [9],
        LocationName.TheStruggleTrophy:               [10],
        LocationName.CentralStationPotion1:           [11],
        LocationName.STTCentralStationHiPotion:       [12],
        LocationName.CentralStationPotion2:           [13],
        LocationName.SunsetTerraceAbilityRing:        [14],
        LocationName.SunsetTerraceHiPotion:           [15],
        LocationName.SunsetTerracePotion1:            [16],
        LocationName.SunsetTerracePotion2:            [17],
        LocationName.MansionFoyerHiPotion:            [18],
        LocationName.MansionFoyerPotion1:             [19],
        LocationName.MansionFoyerPotion2:             [20],
        LocationName.MansionDiningRoomElvenBandanna:  [21],
        LocationName.MansionDiningRoomPotion:         [22],
        LocationName.NaminesSketches:                 [23],
        LocationName.MansionMap:                      [24],
        LocationName.MansionLibraryHiPotion:          [25],
        LocationName.Axel2:                           [26],
        LocationName.MansionBasementCorridorHiPotion: [27],
        LocationName.RoxasDataMagicBoost:             [28],
    }
    stt_region = create_region(world, player, active_locations, RegionName.STT_Region,
                               stt_region_locations, None)

    tt_region_locations = {
        LocationName.OldMansionPotion:               [1],
        LocationName.OldMansionMythrilShard:         [2],
        LocationName.TheWoodsPotion:                 [3],
        LocationName.TheWoodsMythrilShard:           [4],
        LocationName.TheWoodsHiPotion:               [5],
        LocationName.TramCommonHiPotion:             [6],
        LocationName.TramCommonAPBoost:              [7],
        LocationName.TramCommonTent:                 [8],
        LocationName.TramCommonMythrilShard1:        [9],
        LocationName.TramCommonPotion1:              [10],
        LocationName.TramCommonMythrilShard2:        [11],
        LocationName.TramCommonPotion2:              [12],
        LocationName.StationPlazaSecretAnsemReport2: [13],
        LocationName.MunnyPouchMickey:               [14],
        LocationName.CrystalOrb:                     [15],
        LocationName.CentralStationTent:             [16],
        LocationName.TTCentralStationHiPotion:       [17],
        LocationName.CentralStationMythrilShard:     [18],
        LocationName.TheTowerPotion:                 [19],
        LocationName.TheTowerHiPotion:               [2],
        LocationName.TheTowerEther:                  [21],
        LocationName.TowerEntrywayEther:             [22],
        LocationName.TowerEntrywayMythrilShard:      [23],
        LocationName.SorcerersLoftTowerMap:          [24],
        LocationName.TowerWardrobeMythrilStone:      [25],
        LocationName.StarSeeker:                     [26],
        LocationName.ValorForm:                      [27],
    }
    tt_region = create_region(world, player, active_locations, RegionName.TT_Region,
                              tt_region_locations, None)
    tt2_region_locations = {
        LocationName.SeifersTrophy: [1],
        LocationName.Oathkeeper:    [2],
        LocationName.LimitForm:     [3],
    }
    tt2_region = create_region(world, player, active_locations, RegionName.TT2_Region,
                               tt2_region_locations, None)
    tt3_region_locations = {
        LocationName.UndergroundConcourseMythrilGem:        [1],
        LocationName.UndergroundConcourseAPBoost:           [2],
        LocationName.UndergroundConcourseMythrilCrystal:    [3],
        LocationName.UndergroundConcourseOrichalcum:        [4],
        LocationName.TunnelwayOrichalcum:                   [5],
        LocationName.TunnelwayMythrilCrystal:               [6],
        LocationName.SunsetTerraceOrichalcumPlus:           [7],
        LocationName.SunsetTerraceMythrilShard:             [8],
        LocationName.SunsetTerraceMythrilCrystal:           [9],
        LocationName.SunsetTerraceAPBoost:                  [10],
        LocationName.MansionNobodies:                       [11],
        LocationName.MansionFoyerMythrilCrystal:            [12],
        LocationName.MansionFoyerMythrilStone:              [13],
        LocationName.MansionFoyerSerenityCrystal:           [14],
        LocationName.MansionDiningRoomMythrilCrystal:       [15],
        LocationName.MansionDiningRoomMythrilStone:         [16],
        LocationName.MansionLibraryOrichalcum:              [17],
        LocationName.BeamSecretAnsemReport10:               [18],
        LocationName.MansionBasementCorridorUltimateRecipe: [19],
        LocationName.BetwixtandBetween:                     [20],
        LocationName.BetwixtandBetweenBondofFlame:          [21],
        LocationName.AxelDataMagicBoost:                    [22],
        LocationName.DonaldMansionNobodies:                 [23],
    }
    tt3_region = create_region(world, player, active_locations, RegionName.TT3_Region,
                               tt3_region_locations, None)

    twtnw_region_locations = {
        LocationName.FragmentCrossingMythrilStone:    [1],
        LocationName.FragmentCrossingMythrilCrystal:  [2],
        LocationName.FragmentCrossingAPBoost:         [3],
        LocationName.FragmentCrossingOrichalcum:      [4],
        LocationName.Roxas:                           [5],
        LocationName.RoxasGetBonus:                   [5],
        LocationName.RoxasSecretAnsemReport8:         [6],
        LocationName.TwoBecomeOne:                    [7],
        LocationName.MemorysSkyscaperMythrilCrystal:  [8],
        LocationName.MemorysSkyscaperAPBoost:         [9],
        LocationName.MemorysSkyscaperMythrilStone:    [10],
        LocationName.TheBrinkofDespairDarkCityMap:    [11],
        LocationName.TheBrinkofDespairOrichalcumPlus: [12],
    }
    twtnw_region = create_region(world, player, active_locations, RegionName.Twtnw_Region,
                                 twtnw_region_locations, None)
    twtnw2_region_locations = {
        LocationName.NothingsCallMythrilGem:                [1],
        LocationName.NothingsCallOrichalcum:                [2],
        LocationName.TwilightsViewCosmicBelt:               [3],
        LocationName.XigbarBonus:                           [4],
        LocationName.XigbarSecretAnsemReport3:              [5],
        LocationName.NaughtsSkywayMythrilGem:               [6],
        LocationName.NaughtsSkywayOrichalcum:               [7],
        LocationName.NaughtsSkywayMythrilCrystal:           [8],
        LocationName.Oblivion:                              [9],
        LocationName.CastleThatNeverWasMap:                 [10],
        LocationName.Luxord:                                [11],
        LocationName.LuxordGetBonus:                        [12],
        LocationName.LuxordSecretAnsemReport9:              [13],
        LocationName.SaixBonus:                             [14],
        LocationName.SaixSecretAnsemReport12:               [15],
        LocationName.PreXemnas1SecretAnsemReport11:         [16],
        LocationName.RuinandCreationsPassageMythrilStone:   [17],
        LocationName.RuinandCreationsPassageAPBoost:        [18],
        LocationName.RuinandCreationsPassageMythrilCrystal: [19],
        LocationName.RuinandCreationsPassageOrichalcum:     [20],
        LocationName.Xemnas1:                               [21],
        LocationName.Xemnas1GetBonus:                       [22],
        LocationName.Xemnas1SecretAnsemReport13:            [23],
        LocationName.FinalXemnas:                           [24],
        LocationName.XemnasDataPowerBoost:                  [25],
    }
    twtnw2_region = create_region(world, player, active_locations, RegionName.Twtnw2_Region,
                                  twtnw2_region_locations, None)

    valor_region_locations = {
        # LocationName.Valorlvl1: [0],
        LocationName.Valorlvl2: [1],
        LocationName.Valorlvl3: [2],
        LocationName.Valorlvl4: [3],
        LocationName.Valorlvl5: [4],
        LocationName.Valorlvl6: [5],
        LocationName.Valorlvl7: [6],
    }
    valor_region = create_region(world, player, active_locations, RegionName.Valor_Region,
                                 valor_region_locations, None)
    wisdom_region_locations = {
        # LocationName.Wisdomlvl1: [0],
        LocationName.Wisdomlvl2: [7],
        LocationName.Wisdomlvl3: [8],
        LocationName.Wisdomlvl4: [9],
        LocationName.Wisdomlvl5: [10],
        LocationName.Wisdomlvl6: [11],
        LocationName.Wisdomlvl7: [12],
    }
    wisdom_region = create_region(world, player, active_locations, RegionName.Wisdom_Region,
                                  wisdom_region_locations, None)
    limit_region_locations = {
        # LocationName.Limitlvl1: [0],
        LocationName.Limitlvl2: [13],
        LocationName.Limitlvl3: [14],
        LocationName.Limitlvl4: [15],
        LocationName.Limitlvl5: [16],
        LocationName.Limitlvl6: [17],
        LocationName.Limitlvl7: [18],
    }
    limit_region = create_region(world, player, active_locations, RegionName.Limit_Region,
                                 limit_region_locations, None)
    master_region_locations = {
        # LocationName.Masterlvl1: [0],
        LocationName.Masterlvl2: [19],
        LocationName.Masterlvl3: [20],
        LocationName.Masterlvl4: [21],
        LocationName.Masterlvl5: [22],
        LocationName.Masterlvl6: [23],
        LocationName.Masterlvl7: [24],
    }
    master_region = create_region(world, player, active_locations, RegionName.Master_Region,
                                  master_region_locations, None)
    final_region_locations = {
        # LocationName.Finallvl1: [25],
        LocationName.Finallvl2: [25],
        LocationName.Finallvl3: [26],
        LocationName.Finallvl4: [27],
        LocationName.Finallvl5: [28],
        LocationName.Finallvl6: [29],
        LocationName.Finallvl7: [30],
    }
    final_region = create_region(world, player, active_locations, RegionName.Final_Region,
                                 final_region_locations, None)
    # Level region depends on level depth. Moved to bottom of file to keep it clean
    level_region_locations = get_LevelRegion(world, world.LevelDepth[player], player)
    level_region = create_region(world, player, active_locations, RegionName.SoraLevels_Region,
                                 level_region_locations, None)
    keyblade_region_locations = {
        LocationName.FAKESlot:            [1],
        LocationName.DetectionSaberSlot:  [2],
        LocationName.EdgeofUltimaSlot:    [3],
        LocationName.KingdomKeySlot:      [4],
        LocationName.OathkeeperSlot:      [5],
        LocationName.OblivionSlot:        [6],
        LocationName.StarSeekerSlot:      [7],
        LocationName.HiddenDragonSlot:    [8],
        LocationName.HerosCrestSlot:      [9],
        LocationName.MonochromeSlot:      [10],
        LocationName.FollowtheWindSlot:   [11],
        LocationName.CircleofLifeSlot:    [12],
        LocationName.PhotonDebuggerSlot:  [13],
        LocationName.GullWingSlot:        [14],
        LocationName.RumblingRoseSlot:    [15],
        LocationName.GuardianSoulSlot:    [16],
        LocationName.WishingLampSlot:     [17],
        LocationName.DecisivePumpkinSlot: [18],
        LocationName.SweetMemoriesSlot:   [19],
        LocationName.MysteriousAbyssSlot: [20],
        LocationName.SleepingLionSlot:    [21],
        LocationName.BondofFlameSlot:     [22],
        LocationName.TwoBecomeOneSlot:    [23],
        LocationName.FatalCrestSlot:      [24],
        LocationName.FenrirSlot:          [25],
        LocationName.UltimaWeaponSlot:    [26],
        LocationName.WinnersProofSlot:    [27],
        LocationName.PurebloodSlot:       [28],
        LocationName.Centurion2:          [29],
        LocationName.CometStaff:          [30],
        LocationName.HammerStaff:         [31],
        LocationName.LordsBroom:          [32],
        LocationName.MagesStaff:          [33],
        LocationName.MeteorStaff:         [34],
        LocationName.NobodyLance:         [35],
        LocationName.PreciousMushroom:    [36],
        LocationName.PreciousMushroom2:   [37],
        LocationName.PremiumMushroom:     [38],
        LocationName.RisingDragon:        [39],
        LocationName.SaveTheQueen2:       [40],
        LocationName.ShamansRelic:        [41],
        LocationName.VictoryBell:         [42],
        LocationName.WisdomWand:
                                          [43],
        LocationName.AdamantShield:       [44],
        LocationName.AkashicRecord:       [45],
        LocationName.ChainGear:           [46],
        LocationName.DreamCloud:          [47],
        LocationName.FallingStar:         [48],
        LocationName.FrozenPride2:        [49],
        LocationName.GenjiShield:         [50],
        LocationName.KnightDefender:      [51],
        LocationName.KnightsShield:       [52],
        LocationName.MajesticMushroom:    [53],
        LocationName.MajesticMushroom2:   [54],
        LocationName.NobodyGuard:         [55],
        LocationName.OgreShield:          [56],
        LocationName.SaveTheKing2:        [57],
        LocationName.UltimateMushroom:    [58],
    }
    keyblade_region = create_region(world, player, active_locations, RegionName.Keyblade_Region,
                                    keyblade_region_locations, None)

    world.regions += [
        lod_Region,
        lod2_Region,
        ag_region,
        ag2_region,
        dc_region,
        tr_region,
        hundred_acre1_region,
        hundred_acre2_region,
        hundred_acre3_region,
        hundred_acre4_region,
        hundred_acre5_region,
        hundred_acre6_region,
        pr_region,
        pr2_region,
        oc_region,
        oc2_region,
        oc2_pain_and_panic_cup,
        oc2_titan_cup,
        oc2_cerberus_cup,
        oc2_gof_cup,
        bc_region,
        bc2_region,
        sp_region,
        sp2_region,
        ht_region,
        ht2_region,
        hb_region,
        hb2_region,
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
        twtnw2_region,
        goa_region,
        menu_region,
        valor_region,
        wisdom_region,
        limit_region,
        master_region,
        final_region,
        level_region,
        keyblade_region,
        terra_region,
        marluxia_region,
        larxene_region,
        vexen_region,
        lexaeus_region,
        zexion_region,
    ]


def connect_regions(world: MultiWorld, player: int, firstvisitlocking,secondvisitlocking):
    # connecting every first visit to the GoA
    # 2 Visit locking and is going to be turned off mabybe

    names: typing.Dict[str, int] = {}

    connect(world, player, names, "Menu", RegionName.Keyblade_Region)
    connect(world, player, names, "Menu", RegionName.GoA_Region)

    connect(world, player, names, RegionName.GoA_Region, RegionName.LoD_Region, lambda state:state.kh_lod_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.LoD_Region, RegionName.LoD2_Region,lambda state:state.kh_lod_unlocked(player,secondvisitlocking))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Oc_Region, lambda state:state.kh_oc_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Oc_Region,  RegionName.Oc2_Region,lambda state:state.kh_oc_unlocked(player,secondvisitlocking))
    connect(world, player, names, RegionName.Oc2_Region, RegionName.Zexion_Region,lambda state: state.kh_datazexion(player))

    for cups in {RegionName.Oc2_pain_and_panic_Region ,RegionName.Oc2_titan_Region ,RegionName.Oc2_cerberus_Region,RegionName.Oc2_gof_Region}:
        connect(world, player, names, RegionName.Oc2_Region, cups)

    connect(world, player, names, RegionName.GoA_Region, RegionName.Ag_Region,lambda state:state.kh_ag_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Ag_Region, RegionName.Ag2_Region,lambda state:state.kh_ag_unlocked(player,secondvisitlocking)
                            and (state.has(ItemName.FireElement, player)
                            and state.has(ItemName.BlizzardElement, player)
                            and state.has(ItemName.ThunderElement, player)))
    connect(world, player, names, RegionName.Ag2_Region, RegionName.Lexaeus_Region,lambda state: state.kh_datalexaeus(player))

    connect(world, player, names, RegionName.GoA_Region,RegionName.Dc_Region,lambda state:state.kh_dc_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Dc_Region, RegionName.Tr_Region,lambda state:state.kh_dc_unlocked(player,secondvisitlocking))
    connect(world, player, names, RegionName.Tr_Region, RegionName.Marluxia_Region, lambda state: state.kh_datamarluxia(player))
    connect(world, player, names, RegionName.Tr_Region, RegionName.Terra_Region, lambda state: state.kh_terra(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Pr_Region ,lambda state:state.kh_pr_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Pr_Region,  RegionName.Pr2_Region,lambda state:state.kh_pr_unlocked(player,secondvisitlocking))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Bc_Region,lambda state:state.kh_bc_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Bc_Region, RegionName.Bc2_Region,lambda state:state.kh_bc_unlocked(player,secondvisitlocking))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Sp_Region,lambda state:state.kh_sp_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Sp_Region, RegionName.Sp2_Region,lambda state:state.kh_sp_unlocked(player,secondvisitlocking))
    connect(world, player, names, RegionName.Sp2_Region, RegionName.Larxene_Region,lambda state: state.kh_datalarxene(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Ht_Region,lambda state:state.kh_ht_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Ht_Region, RegionName.Ht2_Region,lambda state:state.kh_ht_unlocked(player,secondvisitlocking))
    connect(world, player, names, RegionName.Ht2_Region, RegionName.Vexen_Region,lambda state: state.kh_datavexen(player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Hb_Region,lambda state:state.kh_hb_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Hb_Region, RegionName.Hb2_Region,lambda state:state.kh_hb_unlocked(player,secondvisitlocking))
    connect(world, player, names, RegionName.Hb2_Region, RegionName.Sephi_Region, lambda state: state.kh_sephi(player))

    connect(world, player, names, RegionName.Hb2_Region, RegionName.CoR_Region,lambda state:state.kh_cor(player))
    connect(world, player, names, RegionName.CoR_Region, RegionName.Transport_Region, lambda state:
                            state.has(ItemName.HighJump, player, 3)
                            and state.has(ItemName.AerialDodge, player, 3)
                            and state.has(ItemName.Glide, player, 3))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Pl_Region,lambda state:state.kh_pl_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Pl_Region, RegionName.Pl2_Region,lambda state:state.kh_pl_unlocked(player,secondvisitlocking))

    connect(world, player, names, RegionName.GoA_Region, RegionName.STT_Region,lambda state:state.kh_stt_unlocked(player,1))

    connect(world, player, names, RegionName.GoA_Region, RegionName.TT_Region ,lambda state:state.kh_tt_unlocked(player,1))
    connect(world, player, names, RegionName.TT_Region,  RegionName.TT2_Region,lambda state:state.kh_tt2_unlocked(player,1))
    connect(world, player, names, RegionName.TT2_Region, RegionName.TT3_Region,lambda state:state.kh_tt3_unlocked(player,1))

    connect(world, player, names, RegionName.GoA_Region, RegionName.Twtnw_Region,lambda state:state.kh_twtnw_unlocked(player,firstvisitlocking))
    connect(world, player, names, RegionName.Twtnw_Region, RegionName.Twtnw2_Region,lambda state:
            state.kh_twtnw_unlocked(player,secondvisitlocking) and state.kh_basetools(player)
            and state.kh_donaldlimit(player) or state.has(ItemName.FinalForm,player))

    connect(world, player, names, RegionName.GoA_Region, RegionName.HundredAcre1_Region)

    hundredacrevisits={RegionName.HundredAcre2_Region:1,RegionName.HundredAcre3_Region:2,
                       RegionName.HundredAcre4_Region:3,RegionName.HundredAcre5_Region:4,RegionName.HundredAcre6_Region:5}
    for visit,tornpage in hundredacrevisits.items():
        connect(world, player, names, RegionName.GoA_Region, visit,
                lambda state: (state.has(ItemName.TornPages, player, tornpage)))


    for region in valorLevelRegions:
     connect(world, player, names, region, RegionName.Valor_Region,
             lambda state: state.has(ItemName.ValorForm, player))
     connect(world, player, names, region, RegionName.SoraLevels_Region)
     for region in wisdomLevelRegions:
        connect(world, player, names, region, RegionName.Wisdom_Region,
                lambda state: state.has(ItemName.WisdomForm, player))
     for region in limitLevelRegions:
        connect(world, player, names, region, RegionName.Limit_Region,
                lambda state: state.has(ItemName.LimitForm, player))
     for region in masterLevelRegions:
        connect(world, player, names, region, RegionName.Master_Region,
                lambda state: state.has(ItemName.MasterForm, player) and state.has(ItemName.DriveConverter,player))
     for region in finalLevelRegions:
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
        name = target + (' ' * used_names[source])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


def create_region(world: MultiWorld, player: int, active_locations, name: str, locations=None, exits=None):
    # Shamelessly stolen from the SA2B definition that stole from ROR2 definition
    ret = Region(name, None, name, player)
    ret.multiworld = world
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


def get_LevelRegion(world, option, player):
    if option == 0:
        return {
            LocationName.Lvl2:  [1],
            LocationName.Lvl4:  [2],
            LocationName.Lvl7:  [3],
            LocationName.Lvl9:  [4],
            LocationName.Lvl10: [5],
            LocationName.Lvl12: [6],
            LocationName.Lvl14: [7],
            LocationName.Lvl15: [8],
            LocationName.Lvl17: [9],
            LocationName.Lvl20: [10],
            LocationName.Lvl23: [11],
            LocationName.Lvl25: [12],
            LocationName.Lvl28: [13],
            LocationName.Lvl30: [14],
            LocationName.Lvl32: [15],
            LocationName.Lvl34: [16],
            LocationName.Lvl36: [17],
            LocationName.Lvl39: [18],
            LocationName.Lvl41: [19],
            LocationName.Lvl44: [20],
            LocationName.Lvl46: [21],
            LocationName.Lvl48: [22],
            LocationName.Lvl50: [23],
        }

    elif option == 1:
        return {
            LocationName.Lvl7:  [1],
            LocationName.Lvl9:  [2],
            LocationName.Lvl12: [3],
            LocationName.Lvl15: [4],
            LocationName.Lvl17: [5],
            LocationName.Lvl20: [6],
            LocationName.Lvl23: [7],
            LocationName.Lvl25: [8],
            LocationName.Lvl28: [9],
            LocationName.Lvl31: [10],
            LocationName.Lvl33: [11],
            LocationName.Lvl36: [12],
            LocationName.Lvl39: [13],
            LocationName.Lvl41: [14],
            LocationName.Lvl44: [15],
            LocationName.Lvl47: [16],
            LocationName.Lvl49: [17],
            LocationName.Lvl53: [18],
            LocationName.Lvl59: [19],
            LocationName.Lvl65: [20],
            LocationName.Lvl73: [21],
            LocationName.Lvl85: [22],
            LocationName.Lvl99: [23],
        }
    elif option == 2:
        return {
            # LocationName.Lvl1: [1],
            LocationName.Lvl2:  [2],
            LocationName.Lvl3:  [3],
            LocationName.Lvl4:  [4],
            LocationName.Lvl5:  [5],
            LocationName.Lvl6:  [6],
            LocationName.Lvl7:  [7],
            LocationName.Lvl8:  [8],
            LocationName.Lvl9:  [9],
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
    elif option == 4:
        return {}
    else:
        return {
            # LocationName.Lvl1: [1],
            LocationName.Lvl2:  [2],
            LocationName.Lvl3:  [3],
            LocationName.Lvl4:  [4],
            LocationName.Lvl5:  [5],
            LocationName.Lvl6:  [6],
            LocationName.Lvl7:  [7],
            LocationName.Lvl8:  [8],
            LocationName.Lvl9:  [9],
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
        }
