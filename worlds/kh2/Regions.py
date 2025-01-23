import typing

from BaseClasses import MultiWorld, Region
from . import Locations

from .Subclasses import KH2Location
from .Names import LocationName, RegionName
from .Items import Events_Table

KH2REGIONS: typing.Dict[str, typing.List[str]] = {
    "Menu":                        [],
    RegionName.GoA:                [
        LocationName.GardenofAssemblageMap,
        LocationName.GoALostIllusion,
        LocationName.ProofofNonexistence,
        # LocationName.DonaldStarting1,
        # LocationName.DonaldStarting2,
        # LocationName.GoofyStarting1,
        # LocationName.GoofyStarting2
    ],
    RegionName.LoD:                [
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
    ],
    RegionName.ShanYu:             [
        LocationName.ShanYu,
        LocationName.ShanYuGetBonus,
        LocationName.HiddenDragon,
        LocationName.GoofyShanYu,
        LocationName.ShanYuEventLocation
    ],
    RegionName.LoD2:               [],
    RegionName.AnsemRiku:          [
        LocationName.ThroneRoomTornPages,
        LocationName.ThroneRoomPalaceMap,
        LocationName.ThroneRoomAPBoost,
        LocationName.ThroneRoomQueenRecipe,
        LocationName.ThroneRoomAPBoost2,
        LocationName.ThroneRoomOgreShield,
        LocationName.ThroneRoomMythrilCrystal,
        LocationName.ThroneRoomOrichalcum,
        LocationName.AnsemRikuEventLocation,
    ],
    RegionName.StormRider:         [
        LocationName.StormRider,
        LocationName.GoofyStormRider,
        LocationName.StormRiderEventLocation
    ],
    RegionName.DataXigbar:         [
        LocationName.XigbarDataDefenseBoost,
        LocationName.DataXigbarEventLocation
    ],
    RegionName.Ag:                 [
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
        LocationName.GoofyTreasureRoom,
        LocationName.DonaldAbuEscort
    ],
    RegionName.TwinLords:          [
        LocationName.ElementalLords,
        LocationName.LampCharm,
        LocationName.TwinLordsEventLocation
    ],
    RegionName.Ag2:                [
        LocationName.RuinedChamberTornPages,
        LocationName.RuinedChamberRuinsMap,
    ],
    RegionName.GenieJafar:         [
        LocationName.GenieJafar,
        LocationName.WishingLamp,
        LocationName.GenieJafarEventLocation,
    ],
    RegionName.DataLexaeus:        [
        LocationName.LexaeusBonus,
        LocationName.LexaeusASStrengthBeyondStrength,
        LocationName.LexaeusDataLostIllusion,
        LocationName.DataLexaeusEventLocation
    ],
    RegionName.Dc:                 [
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
        LocationName.MinnieEscortGetBonus
    ],
    RegionName.Tr:                 [
        LocationName.CornerstoneHillMap,
        LocationName.CornerstoneHillFrostShard,
        LocationName.PierMythrilShard,
        LocationName.PierHiPotion,
    ],
    RegionName.OldPete:            [
        LocationName.WaterwayMythrilStone,
        LocationName.WaterwayAPBoost,
        LocationName.WaterwayFrostStone,
        LocationName.WindowofTimeMap,
        LocationName.BoatPete,
        LocationName.DonaldBoatPete,
        LocationName.DonaldBoatPeteGetBonus,
        LocationName.OldPeteEventLocation,
    ],
    RegionName.FuturePete:         [
        LocationName.FuturePete,
        LocationName.FuturePeteGetBonus,
        LocationName.Monochrome,
        LocationName.WisdomForm,
        LocationName.GoofyFuturePete,
        LocationName.FuturePeteEventLocation
    ],
    RegionName.DataMarluxia:       [
        LocationName.MarluxiaGetBonus,
        LocationName.MarluxiaASEternalBlossom,
        LocationName.MarluxiaDataLostIllusion,
        LocationName.DataMarluxiaEventLocation
    ],
    RegionName.Terra:              [
        LocationName.LingeringWillBonus,
        LocationName.LingeringWillProofofConnection,
        LocationName.LingeringWillManifestIllusion,
        LocationName.TerraEventLocation
    ],
    RegionName.Ha1:                [
        LocationName.PoohsHouse100AcreWoodMap,
        LocationName.PoohsHouseAPBoost,
        LocationName.PoohsHouseMythrilStone
    ],
    RegionName.Ha2:                [
        LocationName.PigletsHouseDefenseBoost,
        LocationName.PigletsHouseAPBoost,
        LocationName.PigletsHouseMythrilGem
    ],
    RegionName.Ha3:                [
        LocationName.RabbitsHouseDrawRing,
        LocationName.RabbitsHouseMythrilCrystal,
        LocationName.RabbitsHouseAPBoost,
    ],
    RegionName.Ha4:                [
        LocationName.KangasHouseMagicBoost,
        LocationName.KangasHouseAPBoost,
        LocationName.KangasHouseOrichalcum,
    ],
    RegionName.Ha5:                [
        LocationName.SpookyCaveMythrilGem,
        LocationName.SpookyCaveAPBoost,
        LocationName.SpookyCaveOrichalcum,
        LocationName.SpookyCaveGuardRecipe,
        LocationName.SpookyCaveMythrilCrystal,
        LocationName.SpookyCaveAPBoost2,
        LocationName.SweetMemories,
        LocationName.SpookyCaveMap
    ],
    RegionName.Ha6:                [
        LocationName.StarryHillCosmicRing,
        LocationName.StarryHillStyleRecipe,
        LocationName.StarryHillCureElement,
        LocationName.StarryHillOrichalcumPlus
    ],
    RegionName.Pr:                 [
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
        LocationName.DonaldBoatFight,
        LocationName.GoofyInterceptorBarrels,

    ],
    RegionName.Barbosa:            [
        LocationName.Barbossa,
        LocationName.BarbossaGetBonus,
        LocationName.FollowtheWind,
        LocationName.GoofyBarbossa,
        LocationName.GoofyBarbossaGetBonus,
        LocationName.BarbosaEventLocation,
    ],
    RegionName.Pr2:                [],
    RegionName.GrimReaper1:        [
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
        LocationName.GrimReaper1EventLocation,
    ],
    RegionName.GrimReaper2:        [
        LocationName.DonaladGrimReaper2,
        LocationName.GrimReaper2,
        LocationName.SecretAnsemReport6,
        LocationName.GrimReaper2EventLocation,
    ],
    RegionName.DataLuxord:         [
        LocationName.LuxordDataAPBoost,
        LocationName.DataLuxordEventLocation
    ],
    RegionName.Oc:                 [
        LocationName.PassageMythrilShard,
        LocationName.PassageMythrilStone,
        LocationName.PassageEther,
        LocationName.PassageAPBoost,
        LocationName.PassageHiPotion,
        LocationName.InnerChamberUnderworldMap,
        LocationName.InnerChamberMythrilShard,
    ],
    RegionName.Cerberus:           [
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
        LocationName.CerberusEventLocation
    ],
    RegionName.OlympusPete:        [
        LocationName.PeteOC,
        LocationName.DonaldDemyxOC,
        LocationName.GoofyPeteOC,
        LocationName.OlympusPeteEventLocation
    ],
    RegionName.Hydra:              [
        LocationName.Hydra,
        LocationName.HydraGetBonus,
        LocationName.HerosCrest,
        LocationName.HydraEventLocation
    ],
    RegionName.Oc2:                [
        LocationName.AuronsStatue,
    ],
    RegionName.Hades:              [
        LocationName.Hades,
        LocationName.HadesGetBonus,
        LocationName.GuardianSoul,
        LocationName.HadesEventLocation
    ],
    RegionName.OcPainAndPanicCup:  [
        LocationName.ProtectBeltPainandPanicCup,
        LocationName.SerenityGemPainandPanicCup,
        LocationName.OcPainAndPanicCupEventLocation
    ],
    RegionName.OcCerberusCup:      [
        LocationName.RisingDragonCerberusCup,
        LocationName.SerenityCrystalCerberusCup,
        LocationName.OcCerberusCupEventLocation
    ],
    RegionName.Oc2TitanCup:        [
        LocationName.GenjiShieldTitanCup,
        LocationName.SkillfulRingTitanCup,
        LocationName.Oc2TitanCupEventLocation
    ],
    RegionName.Oc2GofCup:          [
        LocationName.FatalCrestGoddessofFateCup,
        LocationName.OrichalcumPlusGoddessofFateCup,
        LocationName.Oc2GofCupEventLocation,
    ],
    RegionName.HadesCups:          [
        LocationName.HadesCupTrophyParadoxCups,
        LocationName.HadesCupEventLocations
    ],
    RegionName.DataZexion:         [
        LocationName.ZexionBonus,
        LocationName.ZexionASBookofShadows,
        LocationName.ZexionDataLostIllusion,
        LocationName.GoofyZexion,
        LocationName.DataZexionEventLocation
    ],
    RegionName.Bc:                 [
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
    ],
    RegionName.Thresholder:        [
        LocationName.Thresholder,
        LocationName.DungeonBasementMap,
        LocationName.DungeonAPBoost,
        LocationName.SecretPassageMythrilShard,
        LocationName.SecretPassageHiPotion,
        LocationName.SecretPassageLucidShard,
        LocationName.TheWestHallAPBoostPostDungeon,
        LocationName.TheWestWingMythrilShard,
        LocationName.TheWestWingTent,
        LocationName.DonaldThresholder,
        LocationName.ThresholderEventLocation
    ],
    RegionName.Beast:              [
        LocationName.Beast,
        LocationName.TheBeastsRoomBlazingShard,
        LocationName.GoofyBeast,
        LocationName.BeastEventLocation
    ],
    RegionName.DarkThorn:          [
        LocationName.DarkThorn,
        LocationName.DarkThornGetBonus,
        LocationName.DarkThornCureElement,
        LocationName.DarkThornEventLocation,
    ],
    RegionName.Bc2:                [
        LocationName.RumblingRose,
        LocationName.CastleWallsMap
    ],
    RegionName.Xaldin:             [
        LocationName.Xaldin,
        LocationName.XaldinGetBonus,
        LocationName.DonaldXaldinGetBonus,
        LocationName.SecretAnsemReport4,
        LocationName.XaldinEventLocation
    ],
    RegionName.DataXaldin:         [
        LocationName.XaldinDataDefenseBoost,
        LocationName.DataXaldinEventLocation
    ],
    RegionName.Sp:                 [
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
        LocationName.DonaldScreens,
    ],
    RegionName.HostileProgram:     [
        LocationName.HostileProgram,
        LocationName.HostileProgramGetBonus,
        LocationName.PhotonDebugger,
        LocationName.GoofyHostileProgram,
        LocationName.HostileProgramEventLocation
    ],
    RegionName.Sp2:                [
        LocationName.SolarSailer,
        LocationName.CentralComputerCoreAPBoost,
        LocationName.CentralComputerCoreOrichalcumPlus,
        LocationName.CentralComputerCoreCosmicArts,
        LocationName.CentralComputerCoreMap,
        LocationName.DonaldSolarSailer
    ],
    RegionName.Mcp:                [
        LocationName.MCP,
        LocationName.MCPGetBonus,
        LocationName.McpEventLocation
    ],
    RegionName.DataLarxene:        [
        LocationName.LarxeneBonus,
        LocationName.LarxeneASCloakedThunder,
        LocationName.LarxeneDataLostIllusion,
        LocationName.DataLarxeneEventLocation
    ],
    RegionName.Ht:                 [
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
    ],
    RegionName.PrisonKeeper:       [
        LocationName.PrisonKeeper,
        LocationName.DonaldPrisonKeeper,
        LocationName.PrisonKeeperEventLocation,
    ],
    RegionName.OogieBoogie:        [
        LocationName.OogieBoogie,
        LocationName.OogieBoogieMagnetElement,
        LocationName.GoofyOogieBoogie,
        LocationName.OogieBoogieEventLocation
    ],
    RegionName.Ht2:                [
        LocationName.Lock,
        LocationName.Present,
        LocationName.DecoyPresents,
        LocationName.GoofyLock
    ],
    RegionName.Experiment:         [
        LocationName.Experiment,
        LocationName.DecisivePumpkin,
        LocationName.DonaldExperiment,
        LocationName.ExperimentEventLocation,
    ],
    RegionName.DataVexen:          [
        LocationName.VexenBonus,
        LocationName.VexenASRoadtoDiscovery,
        LocationName.VexenDataLostIllusion,
        LocationName.DataVexenEventLocation
    ],
    RegionName.Hb:                 [
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
        LocationName.BaseballCharm
    ],
    RegionName.Hb2:                [
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
    ],
    RegionName.HBDemyx:            [
        LocationName.DonaldDemyxHBGetBonus,
        LocationName.DemyxHB,
        LocationName.DemyxHBGetBonus,
        LocationName.FFFightsCureElement,
        LocationName.CrystalFissureTornPages,
        LocationName.CrystalFissureTheGreatMawMap,
        LocationName.CrystalFissureEnergyCrystal,
        LocationName.CrystalFissureAPBoost,
        LocationName.HBDemyxEventLocation,
    ],
    RegionName.ThousandHeartless:  [
        LocationName.ThousandHeartless,
        LocationName.ThousandHeartlessSecretAnsemReport1,
        LocationName.ThousandHeartlessIceCream,
        LocationName.ThousandHeartlessPicture,
        LocationName.PosternGullWing,
        LocationName.HeartlessManufactoryCosmicChain,
        LocationName.ThousandHeartlessEventLocation,
    ],
    RegionName.DataDemyx:          [
        LocationName.DemyxDataAPBoost,
        LocationName.DataDemyxEventLocation,
    ],
    RegionName.Mushroom13:         [
        LocationName.WinnersProof,
        LocationName.ProofofPeace,
        LocationName.Mushroom13EventLocation,
    ],
    RegionName.Sephi:              [
        LocationName.SephirothBonus,
        LocationName.SephirothFenrir,
        LocationName.SephiEventLocation
    ],
    RegionName.CoR:                [ #todo: make logic for getting these checks.
        LocationName.CoRDepthsAPBoost,
        LocationName.CoRDepthsPowerCrystal,
        LocationName.CoRDepthsFrostCrystal,
        LocationName.CoRDepthsManifestIllusion,
        LocationName.CoRDepthsAPBoost2,
        LocationName.CoRMineshaftLowerLevelDepthsofRemembranceMap,
        LocationName.CoRMineshaftLowerLevelAPBoost,
    ],
    RegionName.CorFirstFight:      [
        LocationName.CoRDepthsUpperLevelRemembranceGem,
        LocationName.CoRMiningAreaSerenityGem,
        LocationName.CoRMiningAreaAPBoost,
        LocationName.CoRMiningAreaSerenityCrystal,
        LocationName.CoRMiningAreaManifestIllusion,
        LocationName.CoRMiningAreaSerenityGem2,
        LocationName.CoRMiningAreaDarkRemembranceMap,
        LocationName.CorFirstFightEventLocation,
    ],
    RegionName.CorSecondFight:     [
        LocationName.CoRMineshaftMidLevelPowerBoost,
        LocationName.CoREngineChamberSerenityCrystal,
        LocationName.CoREngineChamberRemembranceCrystal,
        LocationName.CoREngineChamberAPBoost,
        LocationName.CoREngineChamberManifestIllusion,
        LocationName.CoRMineshaftUpperLevelMagicBoost,
        LocationName.CorSecondFightEventLocation,
    ],
    RegionName.Transport:          [
        LocationName.CoRMineshaftUpperLevelAPBoost,  # last chest
        LocationName.TransporttoRemembrance,
        LocationName.TransportEventLocation,
    ],
    RegionName.Pl:                 [
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

        LocationName.GoofyHyenas1
    ],
    RegionName.Scar:               [
        LocationName.Scar,
        LocationName.ScarFireElement,
        LocationName.DonaldScar,
        LocationName.ScarEventLocation,
    ],
    RegionName.Pl2:                [
        LocationName.Hyenas2,
        LocationName.GoofyHyenas2
    ],
    RegionName.GroundShaker:       [
        LocationName.Groundshaker,
        LocationName.GroundshakerGetBonus,
        LocationName.GroundShakerEventLocation,
    ],
    RegionName.DataSaix:           [
        LocationName.SaixDataDefenseBoost,
        LocationName.DataSaixEventLocation
    ],
    RegionName.Stt:                [
        LocationName.TwilightTownMap,
        LocationName.MunnyPouchOlette,
        LocationName.StationDusks,
        LocationName.StationofSerenityPotion,
        LocationName.StationofCallingPotion,
    ],
    RegionName.TwilightThorn:      [
        LocationName.TwilightThorn,
        LocationName.TwilightThornEventLocation
    ],
    RegionName.Axel1:              [
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
        LocationName.Axel1EventLocation
    ],
    RegionName.Axel2:              [
        LocationName.Axel2,
        LocationName.MansionBasementCorridorHiPotion,
        LocationName.Axel2EventLocation
    ],
    RegionName.DataRoxas:          [
        LocationName.RoxasDataMagicBoost,
        LocationName.DataRoxasEventLocation
    ],
    RegionName.Tt:                 [
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
        LocationName.ValorForm
    ],
    RegionName.Tt2:                [
        LocationName.SeifersTrophy,
        LocationName.Oathkeeper,
        LocationName.LimitForm
    ],
    RegionName.Tt3:                [
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
        LocationName.DonaldMansionNobodies
    ],
    RegionName.DataAxel:           [
        LocationName.AxelDataMagicBoost,
        LocationName.DataAxelEventLocation,
    ],
    RegionName.Twtnw:              [
        LocationName.FragmentCrossingMythrilStone,
        LocationName.FragmentCrossingMythrilCrystal,
        LocationName.FragmentCrossingAPBoost,
        LocationName.FragmentCrossingOrichalcum
    ],
    RegionName.Roxas:              [
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
        LocationName.RoxasEventLocation
    ],
    RegionName.Xigbar:             [
        LocationName.XigbarBonus,
        LocationName.XigbarSecretAnsemReport3,
        LocationName.NaughtsSkywayMythrilGem,
        LocationName.NaughtsSkywayOrichalcum,
        LocationName.NaughtsSkywayMythrilCrystal,
        LocationName.Oblivion,
        LocationName.CastleThatNeverWasMap,
        LocationName.XigbarEventLocation,
    ],
    RegionName.Luxord:             [
        LocationName.Luxord,
        LocationName.LuxordGetBonus,
        LocationName.LuxordSecretAnsemReport9,
        LocationName.LuxordEventLocation,
    ],
    RegionName.Saix:               [
        LocationName.SaixBonus,
        LocationName.SaixSecretAnsemReport12,
        LocationName.SaixEventLocation,
    ],
    RegionName.Twtnw2:             [
        LocationName.PreXemnas1SecretAnsemReport11,
        LocationName.RuinandCreationsPassageMythrilStone,
        LocationName.RuinandCreationsPassageAPBoost,
        LocationName.RuinandCreationsPassageMythrilCrystal,
        LocationName.RuinandCreationsPassageOrichalcum
    ],
    RegionName.Xemnas:             [
        LocationName.Xemnas1,
        LocationName.Xemnas1GetBonus,
        LocationName.Xemnas1SecretAnsemReport13,
        LocationName.XemnasEventLocation

    ],
    RegionName.ArmoredXemnas:      [
        LocationName.ArmoredXemnasEventLocation
    ],
    RegionName.ArmoredXemnas2:     [
        LocationName.ArmoredXemnas2EventLocation
    ],
    RegionName.FinalXemnas:        [
        LocationName.FinalXemnasEventLocation
    ],
    RegionName.DataXemnas:         [
        LocationName.XemnasDataPowerBoost,
        LocationName.DataXemnasEventLocation
    ],
    RegionName.AtlanticaSongOne:   [
        LocationName.UnderseaKingdomMap
    ],
    RegionName.AtlanticaSongTwo:   [

    ],
    RegionName.AtlanticaSongThree: [
        LocationName.MysteriousAbyss
    ],
    RegionName.AtlanticaSongFour:  [
        LocationName.MusicalBlizzardElement,
        LocationName.MusicalOrichalcumPlus
    ],
    RegionName.Valor:              [
        LocationName.Valorlvl2,
        LocationName.Valorlvl3,
        LocationName.Valorlvl4,
        LocationName.Valorlvl5,
        LocationName.Valorlvl6,
        LocationName.Valorlvl7
    ],
    RegionName.Wisdom:             [
        LocationName.Wisdomlvl2,
        LocationName.Wisdomlvl3,
        LocationName.Wisdomlvl4,
        LocationName.Wisdomlvl5,
        LocationName.Wisdomlvl6,
        LocationName.Wisdomlvl7
    ],
    RegionName.Limit:              [
        LocationName.Limitlvl2,
        LocationName.Limitlvl3,
        LocationName.Limitlvl4,
        LocationName.Limitlvl5,
        LocationName.Limitlvl6,
        LocationName.Limitlvl7
    ],
    RegionName.Master:             [
        LocationName.Masterlvl2,
        LocationName.Masterlvl3,
        LocationName.Masterlvl4,
        LocationName.Masterlvl5,
        LocationName.Masterlvl6,
        LocationName.Masterlvl7
    ],
    RegionName.Final:              [
        LocationName.Finallvl2,
        LocationName.Finallvl3,
        LocationName.Finallvl4,
        LocationName.Finallvl5,
        LocationName.Finallvl6,
        LocationName.Finallvl7
    ],
    RegionName.Keyblade:           [
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
        LocationName.UltimateMushroom
    ],
}
level_region_list = [
    RegionName.LevelsVS1,
    RegionName.LevelsVS3,
    RegionName.LevelsVS6,
    RegionName.LevelsVS9,
    RegionName.LevelsVS12,
    RegionName.LevelsVS15,
    RegionName.LevelsVS18,
    RegionName.LevelsVS21,
    RegionName.LevelsVS24,
    RegionName.LevelsVS26,
]


def create_regions(self):
    # Level region depends on level depth.
    # for every 5 levels there should be +3 visit locking
    # level 50
    multiworld = self.multiworld
    player = self.player
    active_locations = self.location_name_to_id

    for level_region_name in level_region_list:
        KH2REGIONS[level_region_name] = []
    if self.options.LevelDepth == "level_50":
        KH2REGIONS[RegionName.LevelsVS1] = [LocationName.Lvl2, LocationName.Lvl4, LocationName.Lvl7, LocationName.Lvl9,
                                            LocationName.Lvl10]
        KH2REGIONS[RegionName.LevelsVS3] = [LocationName.Lvl12, LocationName.Lvl14, LocationName.Lvl15,
                                            LocationName.Lvl17,
                                            LocationName.Lvl20]
        KH2REGIONS[RegionName.LevelsVS6] = [LocationName.Lvl23, LocationName.Lvl25, LocationName.Lvl28,
                                            LocationName.Lvl30]
        KH2REGIONS[RegionName.LevelsVS9] = [LocationName.Lvl32, LocationName.Lvl34, LocationName.Lvl36,
                                            LocationName.Lvl39, LocationName.Lvl41]
        KH2REGIONS[RegionName.LevelsVS12] = [LocationName.Lvl44, LocationName.Lvl46, LocationName.Lvl48]
        KH2REGIONS[RegionName.LevelsVS15] = [LocationName.Lvl50]

    # level 99
    elif self.options.LevelDepth == "level_99":
        KH2REGIONS[RegionName.LevelsVS1] = [LocationName.Lvl7, LocationName.Lvl9]
        KH2REGIONS[RegionName.LevelsVS3] = [LocationName.Lvl12, LocationName.Lvl15, LocationName.Lvl17,
                                            LocationName.Lvl20]
        KH2REGIONS[RegionName.LevelsVS6] = [LocationName.Lvl23, LocationName.Lvl25, LocationName.Lvl28]
        KH2REGIONS[RegionName.LevelsVS9] = [LocationName.Lvl31, LocationName.Lvl33, LocationName.Lvl36,
                                            LocationName.Lvl39]
        KH2REGIONS[RegionName.LevelsVS12] = [LocationName.Lvl41, LocationName.Lvl44, LocationName.Lvl47,
                                             LocationName.Lvl49]
        KH2REGIONS[RegionName.LevelsVS15] = [LocationName.Lvl53, LocationName.Lvl59]
        KH2REGIONS[RegionName.LevelsVS18] = [LocationName.Lvl65]
        KH2REGIONS[RegionName.LevelsVS21] = [LocationName.Lvl73]
        KH2REGIONS[RegionName.LevelsVS24] = [LocationName.Lvl85]
        KH2REGIONS[RegionName.LevelsVS26] = [LocationName.Lvl99]
    # level sanity
    # has to be [] instead of {} for in
    elif self.options.LevelDepth in ["level_50_sanity", "level_99_sanity"]:
        KH2REGIONS[RegionName.LevelsVS1] = [LocationName.Lvl2, LocationName.Lvl3, LocationName.Lvl4, LocationName.Lvl5,
                                            LocationName.Lvl6,
                                            LocationName.Lvl7, LocationName.Lvl8, LocationName.Lvl9, LocationName.Lvl10]
        KH2REGIONS[RegionName.LevelsVS3] = [LocationName.Lvl11, LocationName.Lvl12, LocationName.Lvl13,
                                            LocationName.Lvl14, LocationName.Lvl15,
                                            LocationName.Lvl16, LocationName.Lvl17, LocationName.Lvl18,
                                            LocationName.Lvl19, LocationName.Lvl20]
        KH2REGIONS[RegionName.LevelsVS6] = [LocationName.Lvl21, LocationName.Lvl22, LocationName.Lvl23,
                                            LocationName.Lvl24, LocationName.Lvl25,
                                            LocationName.Lvl26, LocationName.Lvl27, LocationName.Lvl28,
                                            LocationName.Lvl29, LocationName.Lvl30]
        KH2REGIONS[RegionName.LevelsVS9] = [LocationName.Lvl31, LocationName.Lvl32, LocationName.Lvl33,
                                            LocationName.Lvl34, LocationName.Lvl35,
                                            LocationName.Lvl36, LocationName.Lvl37, LocationName.Lvl38,
                                            LocationName.Lvl39, LocationName.Lvl40]
        KH2REGIONS[RegionName.LevelsVS12] = [LocationName.Lvl41, LocationName.Lvl42, LocationName.Lvl43,
                                             LocationName.Lvl44, LocationName.Lvl45,
                                             LocationName.Lvl46, LocationName.Lvl47, LocationName.Lvl48,
                                             LocationName.Lvl49, LocationName.Lvl50]
        # level 99 sanity
        if self.options.LevelDepth == "level_99_sanity":
            KH2REGIONS[RegionName.LevelsVS15] = [LocationName.Lvl51, LocationName.Lvl52, LocationName.Lvl53,
                                                 LocationName.Lvl54,
                                                 LocationName.Lvl55, LocationName.Lvl56, LocationName.Lvl57,
                                                 LocationName.Lvl58,
                                                 LocationName.Lvl59, LocationName.Lvl60]
            KH2REGIONS[RegionName.LevelsVS18] = [LocationName.Lvl61, LocationName.Lvl62, LocationName.Lvl63,
                                                 LocationName.Lvl64,
                                                 LocationName.Lvl65, LocationName.Lvl66, LocationName.Lvl67,
                                                 LocationName.Lvl68,
                                                 LocationName.Lvl69, LocationName.Lvl70]
            KH2REGIONS[RegionName.LevelsVS21] = [LocationName.Lvl71, LocationName.Lvl72, LocationName.Lvl73,
                                                 LocationName.Lvl74,
                                                 LocationName.Lvl75, LocationName.Lvl76, LocationName.Lvl77,
                                                 LocationName.Lvl78,
                                                 LocationName.Lvl79, LocationName.Lvl80]
            KH2REGIONS[RegionName.LevelsVS24] = [LocationName.Lvl81, LocationName.Lvl82, LocationName.Lvl83,
                                                 LocationName.Lvl84,
                                                 LocationName.Lvl85, LocationName.Lvl86, LocationName.Lvl87,
                                                 LocationName.Lvl88,
                                                 LocationName.Lvl89, LocationName.Lvl90]
            KH2REGIONS[RegionName.LevelsVS26] = [LocationName.Lvl91, LocationName.Lvl92, LocationName.Lvl93,
                                                 LocationName.Lvl94,
                                                 LocationName.Lvl95, LocationName.Lvl96, LocationName.Lvl97,
                                                 LocationName.Lvl98, LocationName.Lvl99]
    KH2REGIONS[RegionName.Summon] = []
    if self.options.SummonLevelLocationToggle:
        KH2REGIONS[RegionName.Summon] = [LocationName.Summonlvl2,
                                         LocationName.Summonlvl3,
                                         LocationName.Summonlvl4,
                                         LocationName.Summonlvl5,
                                         LocationName.Summonlvl6,
                                         LocationName.Summonlvl7]
    multiworld.regions += [create_region(multiworld, player, active_locations, region, locations) for region, locations in
                           KH2REGIONS.items()]
    # fill the event locations with events

    for location, item in Locations.event_location_to_item.items():
        multiworld.get_location(location, player).place_locked_item(
                multiworld.worlds[player].create_event_item(item))


def connect_regions(self):
    multiworld = self.multiworld
    player = self.player
    # connecting every first visit to the GoA
    KH2RegionConnections: typing.Dict[str, typing.Set[str]] = {
        "Menu":                        {RegionName.GoA},
        RegionName.GoA:                {RegionName.Sp, RegionName.Pr, RegionName.Tt, RegionName.Oc, RegionName.Ht,
                                        RegionName.LoD,
                                        RegionName.Twtnw, RegionName.Bc, RegionName.Ag, RegionName.Pl, RegionName.Hb,
                                        RegionName.Dc, RegionName.Stt,
                                        RegionName.Ha1, RegionName.Keyblade, RegionName.LevelsVS1,
                                        RegionName.Valor, RegionName.Wisdom, RegionName.Limit, RegionName.Master,
                                        RegionName.Final, RegionName.Summon, RegionName.AtlanticaSongOne},
        RegionName.LoD:                {RegionName.ShanYu},
        RegionName.ShanYu:             {RegionName.LoD2},
        RegionName.LoD2:               {RegionName.AnsemRiku},
        RegionName.AnsemRiku:          {RegionName.StormRider},
        RegionName.StormRider:         {RegionName.DataXigbar},
        RegionName.Ag:                 {RegionName.TwinLords},
        RegionName.TwinLords:          {RegionName.Ag2},
        RegionName.Ag2:                {RegionName.GenieJafar},
        RegionName.GenieJafar:         {RegionName.DataLexaeus},
        RegionName.Dc:                 {RegionName.Tr},
        RegionName.Tr:                 {RegionName.OldPete},
        RegionName.OldPete:            {RegionName.FuturePete},
        RegionName.FuturePete:         {RegionName.Terra, RegionName.DataMarluxia},
        RegionName.Ha1:                {RegionName.Ha2},
        RegionName.Ha2:                {RegionName.Ha3},
        RegionName.Ha3:                {RegionName.Ha4},
        RegionName.Ha4:                {RegionName.Ha5},
        RegionName.Ha5:                {RegionName.Ha6},
        RegionName.Pr:                 {RegionName.Barbosa},
        RegionName.Barbosa:            {RegionName.Pr2},
        RegionName.Pr2:                {RegionName.GrimReaper1},
        RegionName.GrimReaper1:        {RegionName.GrimReaper2},
        RegionName.GrimReaper2:        {RegionName.DataLuxord},
        RegionName.Oc:                 {RegionName.Cerberus},
        RegionName.Cerberus:           {RegionName.OlympusPete},
        RegionName.OlympusPete:        {RegionName.Hydra},
        RegionName.Hydra:              {RegionName.OcPainAndPanicCup, RegionName.OcCerberusCup, RegionName.Oc2},
        RegionName.Oc2:                {RegionName.Hades},
        RegionName.Hades:              {RegionName.Oc2TitanCup, RegionName.Oc2GofCup, RegionName.DataZexion},
        RegionName.Oc2GofCup:          {RegionName.HadesCups},
        RegionName.Bc:                 {RegionName.Thresholder},
        RegionName.Thresholder:        {RegionName.Beast},
        RegionName.Beast:              {RegionName.DarkThorn},
        RegionName.DarkThorn:          {RegionName.Bc2},
        RegionName.Bc2:                {RegionName.Xaldin},
        RegionName.Xaldin:             {RegionName.DataXaldin},
        RegionName.Sp:                 {RegionName.HostileProgram},
        RegionName.HostileProgram:     {RegionName.Sp2},
        RegionName.Sp2:                {RegionName.Mcp},
        RegionName.Mcp:                {RegionName.DataLarxene},
        RegionName.Ht:                 {RegionName.PrisonKeeper},
        RegionName.PrisonKeeper:       {RegionName.OogieBoogie},
        RegionName.OogieBoogie:        {RegionName.Ht2},
        RegionName.Ht2:                {RegionName.Experiment},
        RegionName.Experiment:         {RegionName.DataVexen},
        RegionName.Hb:                 {RegionName.Hb2},
        RegionName.Hb2:                {RegionName.CoR, RegionName.HBDemyx},
        RegionName.HBDemyx:            {RegionName.ThousandHeartless},
        RegionName.ThousandHeartless:  {RegionName.Mushroom13, RegionName.DataDemyx, RegionName.Sephi},
        RegionName.CoR:                {RegionName.CorFirstFight},
        RegionName.CorFirstFight:      {RegionName.CorSecondFight},
        RegionName.CorSecondFight:     {RegionName.Transport},
        RegionName.Pl:                 {RegionName.Scar},
        RegionName.Scar:               {RegionName.Pl2},
        RegionName.Pl2:                {RegionName.GroundShaker},
        RegionName.GroundShaker:       {RegionName.DataSaix},
        RegionName.Stt:                {RegionName.TwilightThorn},
        RegionName.TwilightThorn:      {RegionName.Axel1},
        RegionName.Axel1:              {RegionName.Axel2},
        RegionName.Axel2:              {RegionName.DataRoxas},
        RegionName.Tt:                 {RegionName.Tt2},
        RegionName.Tt2:                {RegionName.Tt3},
        RegionName.Tt3:                {RegionName.DataAxel},
        RegionName.Twtnw:              {RegionName.Roxas},
        RegionName.Roxas:              {RegionName.Xigbar},
        RegionName.Xigbar:             {RegionName.Luxord},
        RegionName.Luxord:             {RegionName.Saix},
        RegionName.Saix:               {RegionName.Twtnw2},
        RegionName.Twtnw2:             {RegionName.Xemnas},
        RegionName.Xemnas:             {RegionName.ArmoredXemnas, RegionName.DataXemnas},
        RegionName.ArmoredXemnas:      {RegionName.ArmoredXemnas2},
        RegionName.ArmoredXemnas2:     {RegionName.FinalXemnas},
        RegionName.LevelsVS1:          {RegionName.LevelsVS3},
        RegionName.LevelsVS3:          {RegionName.LevelsVS6},
        RegionName.LevelsVS6:          {RegionName.LevelsVS9},
        RegionName.LevelsVS9:          {RegionName.LevelsVS12},
        RegionName.LevelsVS12:         {RegionName.LevelsVS15},
        RegionName.LevelsVS15:         {RegionName.LevelsVS18},
        RegionName.LevelsVS18:         {RegionName.LevelsVS21},
        RegionName.LevelsVS21:         {RegionName.LevelsVS24},
        RegionName.LevelsVS24:         {RegionName.LevelsVS26},
        RegionName.AtlanticaSongOne:   {RegionName.AtlanticaSongTwo},
        RegionName.AtlanticaSongTwo:   {RegionName.AtlanticaSongThree},
        RegionName.AtlanticaSongThree: {RegionName.AtlanticaSongFour},
    }

    for source, target in KH2RegionConnections.items():
        source_region = multiworld.get_region(source, player)
        source_region.add_exits(target)


# cave fight:fire/guard
# hades escape logic:fire,blizzard,slide dash, base tools
# windows:chicken little.fire element,base tools
# chasm of challenges:reflect, blizzard, trinity limit,chicken little
# living bones: magnet
# some things for barbosa(PR), chicken little
# hyneas(magnet,reflect)
# tt2: reflect,chicken,form, guard,aerial recovery,finising plus,
# corridors,dancers:chicken little or stitch +demyx tools
# 1k: guard,once more,limit form,
# snipers +before: stitch, magnet, finishing leap, base tools, reflect
# dragoons:stitch, magnet, base tools, reflect
# oc2 tournament thing: stitch, magnet, base tools, reflera
# lock,shock and barrel: reflect, base tools
# carpet section: magnera, reflect, base tools,
# sp2: reflera, stitch, basse tools, reflera, thundara, fantasia/duck flare,once more.
# tt3: stitch/chicken little, magnera,reflera,base tools,finishing leap,limit form
# cor

def create_region(multiworld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        loc_to_id = {loc: active_locations.get(loc, 0) for loc in locations if active_locations.get(loc, None)}
        ret.add_locations(loc_to_id, KH2Location)
        loc_to_event = {loc: active_locations.get(loc, None) for loc in locations if
                        not active_locations.get(loc, None)}
        ret.add_locations(loc_to_event, KH2Location)

    return ret
