import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import KH2Item
from .Options import FinalEXP, MasterEXP, LimitEXP, WisdomEXP, ValorEXP, Schmovement,SuperBosses
from .Locations import HadesCups, LocationName, Oc2Cups,setup_locations, KH2Location,firstVisits
from .Names import LocationName, ItemName
from ..AutoWorld import LogicMixin


def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None, None)
    
    GoA_Region_locations={
        LocationName.GardenofAssemblageMap :[0x5000B,1],
        LocationName.GoALostIllusion       :[0x5000C,2],
        LocationName.ProofofNonexistence   :[0x5000D,3],
}
    GoA_Region = create_region(world, player, active_locations, LocationName.GoA_Region,
                                       GoA_Region_locations, None)

    LoD_Region_locations = {
        LocationName.BambooGroveDarkShard       :[0x5000E,1],
        LocationName.BambooGroveEther           :[0x5000F,2],
        LocationName.BambooGroveMythrilShard    :[0x50010,3],
        LocationName.EncampmentAreaMap          :[0x50011,4],
        LocationName.Mission3                   :[0x50012,5],
        LocationName.CheckpointHiPotion         :[0x50013,6],
        LocationName.CheckpointMythrilShard     :[0x50014,7],
        LocationName.MountainTrailLightningShard:[0x50015,8],
        LocationName.MountainTrailRecoveryRecipe:[0x50016,9],
        LocationName.MountainTrailEther         :[0x50017,10],
        LocationName.MountainTrailMythrilShard  :[0x50018,11],
        LocationName.VillageCaveAreaMap         :[0x50019,12],
        LocationName.VillageCaveAPBoost         :[0x5001A,13],
        LocationName.VillageCaveDarkShard       :[0x5001B,14],
        LocationName.VillageCaveBonus           :[0x5001C,15],
        LocationName.RidgeFrostShard            :[0x5001D,16],
        LocationName.RidgeAPBoost               :[0x5001E,17],
        LocationName.ShanYu                     :[0x5001F,18],
        LocationName.ShanYuGetBonus             :[0x50020,19],
        LocationName.HiddenDragon               :[0x50021,20],
        } 
    LoD_Region = create_region(world, player, active_locations, LocationName.LoD_Region,
                                       LoD_Region_locations, None)
    LoD2_Region_locations = {
        LocationName.ThroneRoomTornPages     :[0x50022,1],
        LocationName.ThroneRoomPalaceMap     :[0x50023,2],
        LocationName.ThroneRoomAPBoost       :[0x50024,3],
        LocationName.ThroneRoomQueenRecipe   :[0x50025,4],
        LocationName.ThroneRoomAPBoost2      :[0x50026,5],
        LocationName.ThroneRoomOgreShield    :[0x50027,6],
        LocationName.ThroneRoomMythrilCrystal:[0x50028,7],
        LocationName.ThroneRoomOrichalcum    :[0x50029,8],
        LocationName.StormRider              :[0x5002A,9],
        LocationName.XigbarDataDefenseBoost  :[0x5002B,10],
        }                                      
    LoD2_Region = create_region(world, player, active_locations, LocationName.LoD2_Region,
                                       LoD2_Region_locations, None)
    Ag_Region_locations={
        LocationName.AgrabahMap                       :[0x5002C,1],
        LocationName.AgrabahDarkShard                 :[0x5002D,2],
        LocationName.AgrabahMythrilShard              :[0x5002E,3],
        LocationName.AgrabahHiPotion                  :[0x5002F,4],
        LocationName.AgrabahAPBoost                   :[0x50030,5],
        LocationName.AgrabahMythrilStone              :[0x50031,6],
        LocationName.AgrabahMythrilShard2             :[0x50032,7],
        LocationName.AgrabahSerenityShard             :[0x50033,8],
        LocationName.BazaarMythrilGem                 :[0x50034,9],
        LocationName.BazaarPowerShard                 :[0x50035,10],
        LocationName.BazaarHiPotion                   :[0x50036,11],
        LocationName.BazaarAPBoost                    :[0x50037,12],
        LocationName.BazaarMythrilShard               :[0x50038,13],
        LocationName.PalaceWallsSkillRing             :[0x50039,14],
        LocationName.PalaceWallsMythrilStone          :[0x5003A,15],
        LocationName.CaveEntrancePowerStone           :[0x5003B,16],
        LocationName.CaveEntranceMythrilShard         :[0x5003C,17],
        LocationName.ValleyofStoneMythrilStone        :[0x5003D,18],
        LocationName.ValleyofStoneAPBoost             :[0x5003E,19],
        LocationName.ValleyofStoneMythrilShard        :[0x5003F,20],
        LocationName.ValleyofStoneHiPotion            :[0x50040,21],
        LocationName.AbuEscort                        :[0x50041,22],
        LocationName.ChasmofChallengesCaveofWondersMap:[0x50042,23],
        LocationName.ChasmofChallengesAPBoost         :[0x50043,24],
        LocationName.TreasureRoom                     :[0x50044,25],
        LocationName.TreasureRoomAPBoost              :[0x50045,26],
        LocationName.TreasureRoomSerenityGem          :[0x50046,27],
        LocationName.ElementalLords                   :[0x50047,28],
        LocationName.LampCharm                        :[0x50048,29],
        }
    Ag_Region = create_region(world, player, active_locations, LocationName.Ag_Region,
                                       Ag_Region_locations, None)
    Ag2_Region_locations={
        LocationName.RuinedChamberTornPages         :[0x50049,1],
        LocationName.RuinedChamberRuinsMap          :[0x5004A,2],
        LocationName.GenieJafar                     :[0x5004B,3],
        LocationName.WishingLamp                    :[0x5004C,4],
        LocationName.LexaeusBonus                   :[0x5004D,5],
        LocationName.LexaeusASStrengthBeyondStrength:[0x5004E,6],
        LocationName.LexaeusDataLostIllusion        :[0x5004F,7],
        }                                             
    Ag2_Region = create_region(world, player, active_locations, LocationName.Ag2_Region,
                                       Ag2_Region_locations, None)

    Dc_Region_locations = {
            LocationName.DCCourtyardMythrilShard  :[0x50050,1],
            LocationName.DCCourtyardStarRecipe    :[0x50051,2],
            LocationName.DCCourtyardAPBoost       :[0x50052,3],
            LocationName.DCCourtyardMythrilStone  :[0x50053,4],
            LocationName.DCCourtyardBlazingStone  :[0x50054,5],
            LocationName.DCCourtyardBlazingShard  :[0x50055,6],
            LocationName.DCCourtyardMythrilShard2 :[0x50056,7],
            LocationName.LibraryTornPages         :[0x50057,8],
            LocationName.DisneyCastleMap          :[0x50058,9],
            LocationName.MinnieEscort             :[0x50059,10],
            LocationName.MinnieEscortGetBonus     :[0x50086,11],
        }
    Dc_Region = create_region(world, player, active_locations, LocationName.Dc_Region,
                                       Dc_Region_locations, None)
    Tr_Region_locations = {
        LocationName.CornerstoneHillMap            :[0x5005A,1],
        LocationName.CornerstoneHillFrostShard     :[0x5005B,2],
        LocationName.PierMythrilShard              :[0x5005C,3],
        LocationName.PierHiPotion                  :[0x5005D,4],
        LocationName.WaterwayMythrilStone          :[0x5005E,5],
        LocationName.WaterwayAPBoost               :[0x5005F,6],
        LocationName.WaterwayFrostStone            :[0x50060,7],
        LocationName.WindowofTimeMap               :[0x50061,8],
        LocationName.BoatPete                      :[0x50062,9],
        LocationName.FuturePete                    :[0x50063,10],
        #This is out of order because I forgot it
        LocationName.FuturePeteGetBonus            :[0x5022C,10],
        LocationName.Monochrome                    :[0x50064,11],
        LocationName.WisdomForm                    :[0x50065,12],
        LocationName.MarluxiaGetBonus              :[0x50066,13],
        LocationName.MarluxiaASEternalBlossom      :[0x50067,14],
        LocationName.MarluxiaDataLostIllusion      :[0x50068,15],
        LocationName.LingeringWillBonus            :[0x50069,16],
        LocationName.LingeringWillProofofConnection:[0x5006A,17],
        LocationName.LingeringWillManifestIllusion :[0x5006B,18],
        }                                            
    Tr_Region = create_region(world, player, active_locations, LocationName.Tr_Region,
                                       Tr_Region_locations, None)

    HundredAcre1_Region_locations = {
            LocationName.PoohsHouse100AcreWoodMap:[0x5006E,1],
            LocationName.PoohsHouseAPBoost       :[0x5006F,2],
            LocationName.PoohsHouseMythrilStone  :[0x50070,3],
        }
    HundredAcre1_Region = create_region(world, player, active_locations, LocationName.HundredAcre1_Region,
                                       HundredAcre1_Region_locations, None)
    HundredAcre2_Region_locations = {
            LocationName.PigletsHouseDefenseBoost:[0x50071,1],
            LocationName.PigletsHouseAPBoost     :[0x50072,2],
            LocationName.PigletsHouseMythrilGem  :[0x50073,3],
        }
    HundredAcre2_Region = create_region(world, player, active_locations, LocationName.HundredAcre2_Region,
                                       HundredAcre2_Region_locations, None)
    HundredAcre3_Region_locations = {
            LocationName.RabbitsHouseDrawRing       :[0x50074,1],
            LocationName.RabbitsHouseMythrilCrystal :[0x50075,2],
            LocationName.RabbitsHouseAPBoost        :[0x50076,3],
        }
    HundredAcre3_Region = create_region(world, player, active_locations, LocationName.HundredAcre3_Region,
                                       HundredAcre3_Region_locations, None)
    HundredAcre4_Region_locations = {
            LocationName.KangasHouseMagicBoost :[0x50077,1],
            LocationName.KangasHouseAPBoost    :[0x50078,2],
            LocationName.KangasHouseOrichalcum :[0x50079,3],
        }
    HundredAcre4_Region = create_region(world, player, active_locations, LocationName.HundredAcre4_Region,
                                       HundredAcre4_Region_locations, None)
    HundredAcre5_Region_locations = {
            LocationName.SpookyCaveMythrilGem    :[0x5007A,1],
            LocationName.SpookyCaveAPBoost       :[0x5007B,2],
            LocationName.SpookyCaveOrichalcum    :[0x5007C,3],
            LocationName.SpookyCaveGuardRecipe   :[0x5007D,4],
            LocationName.SpookyCaveMythrilCrystal:[0x5007E,5],
            LocationName.SpookyCaveAPBoost2      :[0x5007F,6],
            LocationName.SweetMemories           :[0x50080,7],
            LocationName.SpookyCaveMap           :[0x50081,8],
        }
    HundredAcre5_Region = create_region(world, player, active_locations, LocationName.HundredAcre5_Region,
                                       HundredAcre5_Region_locations, None)
    HundredAcre6_Region_locations = {
            LocationName.StarryHillCosmicRing     :[0x50082,1],
            LocationName.StarryHillStyleRecipe    :[0x50083,2],
            LocationName.StarryHillCureElement    :[0x50084,3],
            LocationName.StarryHillOrichalcumPlus :[0x50085,4],
        }
    HundredAcre6_Region = create_region(world, player, active_locations, LocationName.HundredAcre6_Region,
                                       HundredAcre6_Region_locations, None)
    Pr_Region_locations = {
            LocationName.RampartNavalMap          :[0x50087,1],
            LocationName.RampartMythrilStone      :[0x50088,2],
            LocationName.RampartDarkShard         :[0x50089,3],
            LocationName.TownDarkStone            :[0x5008A,4],
            LocationName.TownAPBoost              :[0x5008B,5],
            LocationName.TownMythrilShard         :[0x5008C,6],
            LocationName.TownMythrilGem           :[0x5008D,7],
            LocationName.CaveMouthBrightShard     :[0x5008E,8],
            LocationName.CaveMouthMythrilShard    :[0x5008F,9],
            LocationName.IsladeMuertaMap          :[0x50090,10],
            LocationName.BoatFight                :[0x50091,11],
            LocationName.InterceptorBarrels       :[0x50092,12],
            LocationName.PowderStoreAPBoost1      :[0x50093,13],
            LocationName.PowderStoreAPBoost2      :[0x50094,14],
            LocationName.MoonlightNookMythrilShard:[0x50095,15],
            LocationName.MoonlightNookSerenityGem :[0x50096,16],
            LocationName.MoonlightNookPowerStone  :[0x50097,17],
            LocationName.Barbossa                 :[0x50098,18],
            LocationName.BarbossaGetBonus         :[0x50099,19],
            LocationName.FollowtheWind            :[0x5009A,20],
        }
    Pr_Region = create_region(world, player, active_locations, LocationName.Pr_Region,
                                       Pr_Region_locations, None)
    Pr2_Region_locations = {
        LocationName.GrimReaper1                 :[0x5009B,1],
        LocationName.InterceptorsHoldFeatherCharm:[0x5009C,2],
        LocationName.SeadriftKeepAPBoost         :[0x5009D,3],
        LocationName.SeadriftKeepOrichalcum      :[0x5009E,4],
        LocationName.SeadriftKeepMeteorStaff     :[0x5009F,5],
        LocationName.SeadriftRowSerenityGem      :[0x500A0,6],
        LocationName.SeadriftRowKingRecipe       :[0x500A1,7],
        LocationName.SeadriftRowMythrilCrystal   :[0x500A2,8],
        LocationName.SeadriftRowCursedMedallion  :[0x500A3,9],
        LocationName.SeadriftRowShipGraveyardMap :[0x500A4,10],
        LocationName.GrimReaper2                 :[0x500A5,11],
        LocationName.SecretAnsemReport6          :[0x500A6,12],
        LocationName.LuxordDataAPBoost           :[0x500A7,13],
        }
    Pr2_Region = create_region(world, player, active_locations, LocationName.Pr2_Region,
                                       Pr2_Region_locations, None)
    Oc_Region_locations = {
            LocationName.PassageMythrilShard         :[0x500A8,1],
            LocationName.PassageMythrilStone         :[0x500A9,2],
            LocationName.PassageEther                :[0x500AA,3],
            LocationName.PassageAPBoost              :[0x500AB,4],
            LocationName.PassageHiPotion             :[0x500AC,5],
            LocationName.InnerChamberUnderworldMap   :[0x500AD,6],
            LocationName.InnerChamberMythrilShard    :[0x500AE,7],
            LocationName.Cerberus                    :[0x500AF,8],
            LocationName.ColiseumMap                 :[0x500B0,9],
            LocationName.Urns                        :[0x500B1,10],
            LocationName.UnderworldEntrancePowerBoost:[0x500B2,11],
            LocationName.CavernsEntranceLucidShard   :[0x500B3,12],
            LocationName.CavernsEntranceAPBoost      :[0x500B4,13],
            LocationName.CavernsEntranceMythrilShard :[0x500B5,14],
            LocationName.TheLostRoadBrightShard      :[0x500B6,15],
            LocationName.TheLostRoadEther            :[0x500B7,16],
            LocationName.TheLostRoadMythrilShard     :[0x500B8,17],
            LocationName.TheLostRoadMythrilStone     :[0x500B9,18],
            LocationName.AtriumLucidStone            :[0x500BA,19],
            LocationName.AtriumAPBoost               :[0x500BB,20],
            LocationName.DemyxOC                     :[0x500BC,21],
            LocationName.SecretAnsemReport5          :[0x500BD,22],
            LocationName.OlympusStone                :[0x500BE,23],
            LocationName.TheLockCavernsMap           :[0x500BF,24],
            LocationName.TheLockMythrilShard         :[0x500C0,25],
            LocationName.TheLockAPBoost              :[0x500C1,26],
            LocationName.PeteOC                      :[0x500C2,27],
            LocationName.Hydra                       :[0x500C3,28],
            LocationName.HydraGetBonus               :[0x500C4,29],
            LocationName.HerosCrest                  :[0x500C5,30],
        }                                              
    Oc_Region = create_region(world, player, active_locations, LocationName.Oc_Region,
                                       Oc_Region_locations, None)
    Oc2_Region_locations = {
            LocationName.AuronsStatue          :[0x500C6,1],
            LocationName.Hades                 :[0x500C7,2],
            LocationName.HadesGetBonus         :[0x500C8,3],
            LocationName.GuardianSoul          :[0x500C9,4],
            LocationName.ZexionBonus           :[0x500CA,5],
            LocationName.ZexionASBookofShadows :[0x500CB,6],
            LocationName.ZexionDataLostIllusion:[0x500CC,7],
        }
    Oc2_Region = create_region(world, player, active_locations, LocationName.Oc2_Region,
                                       Oc2_Region_locations, None)
    Oc2Cups_Region_locations = {
         LocationName.ProtectBeltPainandPanicCup    :[0x500CD,1],
         LocationName.SerenityGemPainandPanicCup    :[0x500CE,3],
         LocationName.RisingDragonCerberusCup       :[0x500CF,4],
         LocationName.SerenityCrystalCerberusCup    :[0x500D0,5],
         LocationName.GenjiShieldTitanCup           :[0x500D1,6],
         LocationName.SkillfulRingTitanCup          :[0x500D2,7],
         LocationName.FatalCrestGoddessofFateCup    :[0x500D3,8],
         LocationName.OrichalcumPlusGoddessofFateCup:[0x500D4,9],
         LocationName.HadesCupTrophyParadoxCups     :[0x500D5,10],
     }                                                
    Oc2Cups_Region = create_region(world, player, active_locations, LocationName.Oc2Cups_Region,
                                       Oc2Cups_Region_locations, None)
    Bc_Region_locations = {
                LocationName.BCCourtyardAPBoost                :[0x500D6,1],
                LocationName.BCCourtyardHiPotion               :[0x500D7,2],
                LocationName.BCCourtyardMythrilShard           :[0x500D8,3],
                LocationName.BellesRoomCastleMap               :[0x500D9,4],
                LocationName.BellesRoomMegaRecipe              :[0x500DA,5],
                LocationName.TheEastWingMythrilShard           :[0x500DB,6],
                LocationName.TheEastWingTent                   :[0x500DC,7],
                LocationName.TheWestHallHiPotion               :[0x500DD,8],
                LocationName.TheWestHallPowerShard             :[0x500DE,9],
                LocationName.TheWestHallAPBoost                :[0x500DF,10],
                LocationName.TheWestHallBrightStone            :[0x500E0,11],
                LocationName.TheWestHallMythrilShard           :[0x500E1,12],
                LocationName.Thresholder                       :[0x500E2,13],
                LocationName.DungeonBasementMap                :[0x500E3,14],
                LocationName.DungeonAPBoost                    :[0x500E4,15],
                LocationName.SecretPassageMythrilShard         :[0x500E5,16],
                LocationName.SecretPassageHiPotion             :[0x500E6,17],
                LocationName.SecretPassageLucidShard           :[0x500E7,18],
                LocationName.TheWestHallMythrilShardPostDungeon:[0x500E8,19],
                LocationName.TheWestWingMythrilShard           :[0x500E9,20],
                LocationName.TheWestWingTent                   :[0x500EA,21],
                LocationName.Beast                             :[0x500EB,22],
                LocationName.TheBeastsRoomBlazingShard         :[0x500EC,23],
                LocationName.DarkThorn                         :[0x500ED,25],
                LocationName.DarkThornGetBonus                 :[0x500EE,26],
                LocationName.DarkThornCureElement              :[0x500EF,27],
        }                                                        
    Bc_Region = create_region(world, player, active_locations, LocationName.Bc_Region,
                                       Bc_Region_locations, None)
    Bc2_Region_locations = {
            LocationName.RumblingRose          :[0x500F0,1],
            LocationName.CastleWallsMap        :[0x500F1,2],
            LocationName.Xaldin                :[0x500F2,3],
            LocationName.XaldinGetBonus        :[0x500F3,4],
            LocationName.SecretAnsemReport4    :[0x500F4,5],
            LocationName.XaldinDataDefenseBoost:[0x500F5,6],
        }                                        
    Bc2_Region = create_region(world, player, active_locations, LocationName.Bc2_Region,
                                       Bc2_Region_locations, None)
    Sp_Region_locations = {
                LocationName.PitCellAreaMap              :[0x500F6,1],
                LocationName.PitCellMythrilCrystal       :[0x500F7,2],
                LocationName.CanyonDarkCrystal           :[0x500F8,3],
                LocationName.CanyonMythrilStone          :[0x500F9,4],
                LocationName.CanyonMythrilGem            :[0x500FA,5],
                LocationName.CanyonFrostCrystal          :[0x500FB,6],
                LocationName.Screens                     :[0x500FC,7],
                LocationName.HallwayPowerCrystal         :[0x500FD,8],
                LocationName.HallwayAPBoost              :[0x500FE,9],
                LocationName.CommunicationsRoomIOTowerMap:[0x500FF,10],
                LocationName.CommunicationsRoomGaiaBelt  :[0x50100,11],
                LocationName.HostileProgram              :[0x50101,12],
                LocationName.HostileProgramGetBonus      :[0x50102,13],
                LocationName.PhotonDebugger              :[0x50103,14],
        }                                                  
    Sp_Region = create_region(world, player, active_locations, LocationName.Sp_Region,
                                       Sp_Region_locations, None)
    Sp2_Region_locations = {
            LocationName.SolarSailer                      :[0x50104,1],
            LocationName.CentralComputerCoreAPBoost       :[0x50105,2],
            LocationName.CentralComputerCoreOrichalcumPlus:[0x50106,3],
            LocationName.CentralComputerCoreCosmicArts    :[0x50107,4],
            LocationName.CentralComputerCoreMap           :[0x50108,5],
            LocationName.MCP                              :[0x50109,6],
            LocationName.MCPGetBonus                      :[0x5010A,7],
            LocationName.LarxeneBonus                     :[0x5010B,8],
            LocationName.LarxeneASCloakedThunder          :[0x5010C,9],
            LocationName.LarxeneDataLostIllusion          :[0x5010D,10],
        }
    Sp2_Region = create_region(world, player, active_locations, LocationName.Sp2_Region,
                                       Sp2_Region_locations, None)
    Ht_Region_locations = {
            LocationName.GraveyardMythrilShard          :[0x5010E,1],
            LocationName.GraveyardSerenityGem           :[0x5010F,2],
            LocationName.FinklesteinsLabHalloweenTownMap:[0x50110,3],
            LocationName.TownSquareMythrilStone         :[0x50111,4],
            LocationName.TownSquareEnergyShard          :[0x50112,5],
            LocationName.HinterlandsLightningShard      :[0x50113,6],
            LocationName.HinterlandsMythrilStone        :[0x50114,7],
            LocationName.HinterlandsAPBoost             :[0x50115,8],
            LocationName.CandyCaneLaneMegaPotion        :[0x50116,9],
            LocationName.CandyCaneLaneMythrilGem        :[0x50117,10],
            LocationName.CandyCaneLaneLightningStone    :[0x50118,11],
            LocationName.CandyCaneLaneMythrilStone      :[0x50119,12],
            LocationName.SantasHouseChristmasTownMap    :[0x5011A,13],
            LocationName.SantasHouseAPBoost             :[0x5011B,14],
            LocationName.PrisonKeeper                   :[0x5011C,15],
            LocationName.OogieBoogie                    :[0x5011D,16],
            LocationName.OogieBoogieMagnetElement       :[0x5011E,17],
        }
    Ht_Region = create_region(world, player, active_locations, LocationName.Ht_Region,
                                       Ht_Region_locations, None)
    Ht2_Region_locations = {
            LocationName.Lock                  :[0x5011E,1],
            LocationName.Present               :[0x5011F,2],
            LocationName.DecoyPresents         :[0x50120,3],
            LocationName.Experiment            :[0x50121,4],
            LocationName.DecisivePumpkin       :[0x50122,5],
            LocationName.VexenBonus            :[0x50123,6],
            LocationName.VexenASRoadtoDiscovery:[0x50124,7],
            LocationName.VexenDataLostIllusion :[0x50125,8],
        }
    Ht2_Region = create_region(world, player, active_locations, LocationName.Ht2_Region,
                                       Ht2_Region_locations, None)

    Hb_Region_locations = {
            LocationName.MarketplaceMap             :[0x50126,1],
            LocationName.BoroughDriveRecovery       :[0x50127,2],
            LocationName.BoroughAPBoost             :[0x50128,3],
            LocationName.BoroughHiPotion            :[0x50129,4],
            LocationName.BoroughMythrilShard        :[0x5012A,5],
            LocationName.BoroughDarkShard           :[0x5012B,6],
            LocationName.MerlinsHouseMembershipCard :[0x5012C,7],
            LocationName.MerlinsHouseBlizzardElement:[0x5012D,8],
            LocationName.Bailey                     :[0x5012E,9],
            LocationName.BaileySecretAnsemReport7   :[0x5012F,10],
            LocationName.BaseballCharm              :[0x50130,11],
        }
    Hb_Region = create_region(world, player, active_locations, LocationName.Hb_Region,
                                       Hb_Region_locations, None)
    Hb2_Region_locations = {
            LocationName.PosternCastlePerimeterMap          :[0x50131,1],
            LocationName.PosternMythrilGem                  :[0x50132,2],
            LocationName.PosternAPBoost                     :[0x50133,3],
            LocationName.CorridorsMythrilStone              :[0x50134,4],
            LocationName.CorridorsMythrilCrystal            :[0x50135,5],
            LocationName.CorridorsDarkCrystal               :[0x50136,6],
            LocationName.CorridorsAPBoost                   :[0x50137,7],
            LocationName.AnsemsStudyMasterForm              :[0x50138,8],
            LocationName.AnsemsStudySleepingLion            :[0x50139,9],
            LocationName.AnsemsStudySkillRecipe             :[0x5013A,10],
            LocationName.AnsemsStudyUkuleleCharm            :[0x5013B,11],
            LocationName.RestorationSiteMoonRecipe          :[0x5013C,12],
            LocationName.RestorationSiteAPBoost             :[0x5013D,13],
            LocationName.DemyxHB                            :[0x5013E,14],
            LocationName.DemyxHBGetBonus                    :[0x5013F,14],
            LocationName.FFFightsCureElement                :[0x50140,15],
            LocationName.CrystalFissureTornPages            :[0x50141,16],
            LocationName.CrystalFissureTheGreatMawMap       :[0x50142,17],
            LocationName.CrystalFissureEnergyCrystal        :[0x50143,18],
            LocationName.CrystalFissureAPBoost              :[0x50144,19],
            LocationName.ThousandHeartless                  :[0x50145,20],
            LocationName.ThousandHeartlessSecretAnsemReport1:[0x50146,21],
            LocationName.ThousandHeartlessIceCream          :[0x50147,22],
            LocationName.ThousandHeartlessPicture           :[0x50148,23],
            LocationName.PosternGullWing                    :[0x50149,24],
            LocationName.HeartlessManufactoryCosmicChain    :[0x5014A,25],
            LocationName.SephirothBonus                     :[0x5014B,26],
            LocationName.SephirothFenrir                    :[0x5014C,27],
            LocationName.WinnersProof                       :[0x5014D,28],
            LocationName.ProofofPeace                       :[0x5014E,29],
            LocationName.DemyxDataAPBoost                   :[0x5014F,30],
             LocationName.CoRDepthsAPBoost                           :[0x50150,31],
            LocationName.CoRDepthsPowerCrystal                       :[0x50151,32],
            LocationName.CoRDepthsFrostCrystal                       :[0x50152,33],
            LocationName.CoRDepthsManifestIllusion                   :[0x50153,34],
            LocationName.CoRDepthsAPBoost2                           :[0x50154,35],
            LocationName.CoRMineshaftLowerLevelDepthsofRemembranceMap:[0x50155,36],
            LocationName.CoRMineshaftLowerLevelAPBoost               :[0x50156,37],
        }
    Hb2_Region = create_region(world, player, active_locations, LocationName.Hb2_Region,
                                       Hb2_Region_locations, None)

    CoR_Region_locations = {
            LocationName.CoRDepthsUpperLevelRemembranceGem:[0x50157,1],
            LocationName.CoRMiningAreaSerenityGem         :[0x50158,2],
            LocationName.CoRMiningAreaAPBoost             :[0x50159,3],
            LocationName.CoRMiningAreaSerenityCrystal     :[0x5015A,4],
            LocationName.CoRMiningAreaManifestIllusion    :[0x5015B,5],
            LocationName.CoRMiningAreaSerenityGem2        :[0x5015C,6],
            LocationName.CoRMiningAreaDarkRemembranceMap  :[0x5015D,7],
            LocationName.CoRMineshaftMidLevelPowerBoost   :[0x5015E,8],
            LocationName.CoREngineChamberSerenityCrystal  :[0x5015F,9],
            LocationName.CoREngineChamberRemembranceCrystal:[0x50160,10],
            LocationName.CoREngineChamberAPBoost          :[0x50161,11],
            LocationName.CoREngineChamberManifestIllusion :[0x50162,12],
            LocationName.CoRMineshaftUpperLevelMagicBoost :[0x50163,13],
            LocationName.CoRMineshaftUpperLevelAPBoost    :[0x50164,14],
            LocationName.TransporttoRemembrance           :[0x50165,15],
            LocationName.CoRMineshaftUpperLevelAPBoost    :[0x50164,16],
            LocationName.TransporttoRemembrance           :[0x50165,17],
        }                                                                             
    CoR_Region = create_region(world, player, active_locations, LocationName.CoR_Region,
                               CoR_Region_locations,None)


    Pl_Region_locations = {
            LocationName.GorgeSavannahMap             :[0x50166,1],
            LocationName.GorgeDarkGem                 :[0x50167,2],
            LocationName.GorgeMythrilStone            :[0x50168,3],
            LocationName.ElephantGraveyardFrostGem    :[0x50169,4],
            LocationName.ElephantGraveyardMythrilStone:[0x5016A,5],
            LocationName.ElephantGraveyardBrightStone :[0x5016B,6],
            LocationName.ElephantGraveyardAPBoost     :[0x5016C,7],
            LocationName.ElephantGraveyardMythrilShard:[0x5016D,8],
            LocationName.PrideRockMap                 :[0x5016E,9],
            LocationName.PrideRockMythrilStone        :[0x5016F,10],
            LocationName.PrideRockSerenityCrystal     :[0x50170,11],
            LocationName.WildebeestValleyEnergyStone  :[0x50171,12],
            LocationName.WildebeestValleyAPBoost      :[0x50172,13],
            LocationName.WildebeestValleyMythrilGem   :[0x50173,14],
            LocationName.WildebeestValleyMythrilStone :[0x50174,15],
            LocationName.WildebeestValleyLucidGem     :[0x50175,16],
            LocationName.WastelandsMythrilShard       :[0x50176,17],
            LocationName.WastelandsSerenityGem        :[0x50177,18],
            LocationName.WastelandsMythrilStone       :[0x50178,19],
            LocationName.JungleSerenityGem            :[0x50179,20],
            LocationName.JungleMythrilStone           :[0x5017A,21],
            LocationName.JungleSerenityCrystal        :[0x5017B,22],
            LocationName.OasisMap                     :[0x5017C,23],
            LocationName.OasisTornPages               :[0x5017D,24],
            LocationName.OasisAPBoost                 :[0x5017E,25],
            LocationName.CircleofLife                 :[0x5017F,26],
            LocationName.Hyenas1                      :[0x50180,27],
            LocationName.Scar                         :[0x50181,28],
            LocationName.ScarFireElement              :[0x50182,29],
        }
    Pl_Region = create_region(world, player, active_locations, LocationName.Pl_Region,
                                       Pl_Region_locations, None)
    Pl2_Region_locations = {
            LocationName.Hyenas2             :[0x50183,1],
            LocationName.Groundshaker        :[0x50184,2],
            LocationName.GroundshakerGetBonus:[0x50185,3],
            LocationName.SaixDataDefenseBoost:[0x50186,4],
        }
    Pl2_Region = create_region(world, player, active_locations, LocationName.Pl2_Region,
                                       Pl2_Region_locations, None)

    STT_Region_locations = {
            LocationName.TwilightTownMap                :[0x50183,1],
            LocationName.MunnyPouchOlette               :[0x50184,2],
            LocationName.StationDusks                   :[0x50185,3],
            LocationName.StationofSerenityPotion        :[0x50186,4],
            LocationName.StationofCallingPotion         :[0x50187,5],
            LocationName.TwilightThorn                  :[0x50188,6],
            LocationName.Axel1                          :[0x50189,7],
            LocationName.JunkChampionBelt               :[0x5018A,8],
            LocationName.JunkMedal                      :[0x5018B,9],
            LocationName.TheStruggleTrophy              :[0x5018C,10],
            LocationName.CentralStationPotion1          :[0x5018D,11],
            LocationName.STTCentralStationHiPotion      :[0x5018E,12],
            LocationName.CentralStationPotion2          :[0x5018F,13],
            LocationName.SunsetTerraceAbilityRing       :[0x50190,14],
            LocationName.SunsetTerraceHiPotion          :[0x50191,15],
            LocationName.SunsetTerracePotion1           :[0x50192,16],
            LocationName.SunsetTerracePotion2           :[0x50193,17],
            LocationName.MansionFoyerHiPotion           :[0x50194,18],
            LocationName.MansionFoyerPotion1            :[0x50195,19],
            LocationName.MansionFoyerPotion2            :[0x50196,20],
            LocationName.MansionDiningRoomElvenBandanna :[0x50197,21],
            LocationName.MansionDiningRoomPotion        :[0x50198,22],
            LocationName.NaminesSketches                :[0x50199,23],
            LocationName.MansionMap                     :[0x5019A,24],
            LocationName.MansionLibraryHiPotion         :[0x5019B,25],
            LocationName.Axel2                          :[0x5019C,26],
            LocationName.MansionBasementCorridorHiPotion:[0x5019D,27],
            LocationName.RoxasDataMagicBoost            :[0x5019E,28],
        }
    STT_Region = create_region(world, player, active_locations, LocationName.STT_Region,
                                       STT_Region_locations, None)

    TT_Region_locations = {
            LocationName.OldMansionPotion              :[0x5019F,1],
            LocationName.OldMansionMythrilShard        :[0x501A0,2],
            LocationName.TheWoodsPotion                :[0x501A1,3],
            LocationName.TheWoodsMythrilShard          :[0x501A2,4],
            LocationName.TheWoodsHiPotion              :[0x501A3,5],
            LocationName.TramCommonHiPotion            :[0x501A4,6],
            LocationName.TramCommonAPBoost             :[0x501A5,7],
            LocationName.TramCommonTent                :[0x501A6,8],
            LocationName.TramCommonMythrilShard1       :[0x501A7,9],
            LocationName.TramCommonPotion1             :[0x501A8,10],
            LocationName.TramCommonMythrilShard2       :[0x501A9,11],
            LocationName.TramCommonPotion2             :[0x501AA,12],
            LocationName.StationPlazaSecretAnsemReport2:[0x501AB,13],
            LocationName.MunnyPouchMickey              :[0x501AC,14],
            LocationName.CrystalOrb                    :[0x501AD,15],
            LocationName.CentralStationTent            :[0x501AE,16],
            LocationName.TTCentralStationHiPotion      :[0x501AF,17],
            LocationName.CentralStationMythrilShard    :[0x501B0,18],
            LocationName.TheTowerPotion                :[0x501B1,19],
            LocationName.TheTowerHiPotion              :[0x501B2,2],
            LocationName.TheTowerEther                 :[0x501B3,21],
            LocationName.TowerEntrywayEther            :[0x501B4,22],
            LocationName.TowerEntrywayMythrilShard     :[0x501B5,23],
            LocationName.SorcerersLoftTowerMap         :[0x501B6,24],
            LocationName.TowerWardrobeMythrilStone     :[0x501B7,25],
            LocationName.StarSeeker                    :[0x501B8,26],
            LocationName.ValorForm                     :[0x501B9,27],
        }
    TT_Region = create_region(world, player, active_locations, LocationName.TT_Region,
                                       TT_Region_locations, None)
    TT2_Region_locations = {
            LocationName.SeifersTrophy:[0x501BA,1],
            LocationName.Oathkeeper   :[0x501BB,2],
            LocationName.LimitForm    :[0x501BC,3],
        }
    TT2_Region = create_region(world, player, active_locations, LocationName.TT2_Region,
                                       TT2_Region_locations, None)
    TT3_Region_locations = {
            LocationName.UndergroundConcourseMythrilGem       :[0x501BD,1],
            LocationName.UndergroundConcourseAPBoost          :[0x501BE,2],
            LocationName.UndergroundConcourseMythrilCrystal   :[0x501BF,3],
            LocationName.TunnelwayOrichalcum                  :[0x501C0,4],
            LocationName.TunnelwayMythrilCrystal              :[0x501C1,5],
            LocationName.SunsetTerraceOrichalcumPlus          :[0x501C2,6],
            LocationName.SunsetTerraceMythrilShard            :[0x501C3,7],
            LocationName.SunsetTerraceMythrilCrystal          :[0x501C4,8],
            LocationName.SunsetTerraceAPBoost                 :[0x501C5,9],
            LocationName.MansionNobodies                      :[0x501C6,10],
            LocationName.MansionFoyerMythrilCrystal           :[0x501C7,11],
            LocationName.MansionFoyerMythrilStone             :[0x501C8,12],
            LocationName.MansionFoyerSerenityCrystal          :[0x501C9,13],
            LocationName.MansionDiningRoomMythrilCrystal      :[0x501CA,14],
            LocationName.MansionDiningRoomMythrilStone        :[0x501CB,15],
            LocationName.MansionLibraryOrichalcum             :[0x501CC,16],
            LocationName.BeamSecretAnsemReport10              :[0x501CD,17],
            LocationName.MansionBasementCorridorUltimateRecipe:[0x501CE,18],
            LocationName.BetwixtandBetween                    :[0x501CF,19],
            LocationName.BetwixtandBetweenBondofFlame         :[0x501D0,20],
            LocationName.AxelDataMagicBoost                   :[0x501D1,21],
        }
    TT3_Region = create_region(world, player, active_locations, LocationName.TT3_Region,
                                       TT3_Region_locations, None)

    Twtnw_Region_locations = {
            LocationName.FragmentCrossingMythrilStone   :[0x501D2,1],
            LocationName.FragmentCrossingMythrilCrystal :[0x501D3,2],
            LocationName.FragmentCrossingAPBoost        :[0x501D4,3],
            LocationName.FragmentCrossingOrichalcum     :[0x501D5,4],
            LocationName.Roxas                          :[0x501D6,5],
            LocationName.RoxasGetBonus                  :[0x501D7,5],
            LocationName.RoxasSecretAnsemReport8        :[0x501D8,6],
            LocationName.TwoBecomeOne                   :[0x501D9,7],
            LocationName.MemorysSkyscaperMythrilCrystal :[0x501DA,8],
            LocationName.MemorysSkyscaperAPBoost        :[0x501DB,9],
            LocationName.MemorysSkyscaperMythrilStone   :[0x501DC,10],
            LocationName.TheBrinkofDespairDarkCityMap   :[0x501DD,11],
            LocationName.TheBrinkofDespairOrichalcumPlus:[0x501DE,12],
            LocationName.NothingsCallMythrilGem         :[0x501DF,13],
            LocationName.NothingsCallOrichalcum         :[0x501E0,14],
            LocationName.TwilightsViewCosmicBelt        :[0x501E1,15],
        }
    Twtnw_Region = create_region(world, player, active_locations, LocationName.Twtnw_Region,
                                       Twtnw_Region_locations, None)
    Twtnw2_Region_locations = {
            LocationName.XigbarBonus                          :[0x501E2,1],
            LocationName.XigbarSecretAnsemReport3             :[0x501E3,2],
            LocationName.NaughtsSkywayMythrilGem              :[0x501E4,3],
            LocationName.NaughtsSkywayOrichalcum              :[0x501E5,4],
            LocationName.NaughtsSkywayMythrilCrystal          :[0x501E6,5],
            LocationName.Oblivion                             :[0x501E7,6],
            LocationName.CastleThatNeverWasMap                :[0x501E8,7],
            LocationName.Luxord                               :[0x501E9,8],
            LocationName.LuxordGetBonus                       :[0x501EA,9],
            LocationName.LuxordSecretAnsemReport9             :[0x501EB,10],
            LocationName.SaixBonus                            :[0x501EC,11],
            LocationName.SaixSecretAnsemReport12              :[0x501ED,12],
            LocationName.PreXemnas1SecretAnsemReport11        :[0x501EE,13],
            LocationName.RuinandCreationsPassageMythrilStone  :[0x501EF,14],
            LocationName.RuinandCreationsPassageAPBoost       :[0x501F0,15],
            LocationName.RuinandCreationsPassageMythrilCrystal:[0x501F1,16],
            LocationName.RuinandCreationsPassageOrichalcum    :[0x501F2,17],
            LocationName.Xemnas1                              :[0x501F3,18],
            LocationName.Xemnas1GetBonus                      :[0x501F3,18],
            LocationName.Xemnas1SecretAnsemReport13           :[0x501F4,19],
            LocationName.FinalXemnas                          :[0x501F5,20],
            LocationName.XemnasDataPowerBoost                 :[0x501F6,21],
        }                                                       
    Twtnw2_Region = create_region(world, player, active_locations, LocationName.Twtnw2_Region,
                                       Twtnw2_Region_locations, None)

    Valor_Region_locations={
         LocationName.Valorlvl2 :[0x501F7,1],
         LocationName.Valorlvl3 :[0x501F8,2],
         LocationName.Valorlvl4 :[0x501F9,3],
         LocationName.Valorlvl5 :[0x501FA,4],
         LocationName.Valorlvl6 :[0x501FB,5],
         LocationName.Valorlvl7 :[0x501FC,6],
        }
    Valor_Region=create_region(world,player,active_locations,LocationName.ValorForm,
                               Valor_Region_locations,None)
    Wisdom_Region_locations={
        LocationName.Wisdomlvl2:[0x501FD,7],
        LocationName.Wisdomlvl3:[0x501FE,8],
        LocationName.Wisdomlvl4:[0x501FF,9],
        LocationName.Wisdomlvl5:[0x50200,10],
        LocationName.Wisdomlvl6:[0x50201,11],
        LocationName.Wisdomlvl7:[0x50202,12],
        }
    Wisdom_Region=create_region(world,player,active_locations,LocationName.WisdomForm,
                               Wisdom_Region_locations,None)
    Limit_Region_locations={
        LocationName.Limitlvl2 :[0x50203,13],
        LocationName.Limitlvl3 :[0x50204,14],
        LocationName.Limitlvl4 :[0x50205,15],
        LocationName.Limitlvl5 :[0x50206,16],
        LocationName.Limitlvl6 :[0x50207,17],
        LocationName.Limitlvl7 :[0x50208,18],
        }
    Limit_Region=create_region(world,player,active_locations,LocationName.LimitForm,
                               Limit_Region_locations,None)
    Master_Region_locations={
        LocationName.Masterlvl2:[0x50209,19],
        LocationName.Masterlvl3:[0x5020A,20],
        LocationName.Masterlvl4:[0x5020B,21],
        LocationName.Masterlvl5:[0x5020C,22],
        LocationName.Masterlvl6:[0x5020D,23],
        LocationName.Masterlvl7:[0x5020E,24],
        }
    Master_Region=create_region(world,player,active_locations,LocationName.MasterForm,
                               Master_Region_locations,None)
    Final_Region_locations={
        LocationName.Finallvl2 :[0x5020F,25],
        LocationName.Finallvl3 :[0x50210,26],
        LocationName.Finallvl4 :[0x50211,27],
        LocationName.Finallvl5 :[0x50212,28],
        LocationName.Finallvl6 :[0x50213,29],
        LocationName.Finallvl7 :[0x50214,30],
        }
    Final_Region=create_region(world,player,active_locations,LocationName.FinalForm,
                               Final_Region_locations,None)
    Level_Region_locations={
            LocationName.Lvl1   :[0x50214,1],
            LocationName.Lvl2   :[0x50215,2],
            LocationName.Lvl3   :[0x50216,3],
            LocationName.Lvl4   :[0x50217,4],
            LocationName.Lvl5   :[0x50218,5],
            LocationName.Lvl6   :[0x50219,6],
            LocationName.Lvl7   :[0x5021A,7],
            LocationName.Lvl8   :[0x5021B,8],
            LocationName.Lvl9   :[0x5021C,9],
            LocationName.Lvl10  :[0x5021D,10],
            LocationName.Lvl11  :[0x5021E,11],
            LocationName.Lvl12  :[0x5021F,12],
            LocationName.Lvl13  :[0x50220,13],
            LocationName.Lvl14  :[0x50221,14],
            LocationName.Lvl15  :[0x50222,15],
            LocationName.Lvl16  :[0x50223,16],
            LocationName.Lvl17  :[0x50224,17],
            LocationName.Lvl18  :[0x50225,18],
            LocationName.Lvl19  :[0x50226,19],
            LocationName.Lvl20  :[0x50227,20],
            LocationName.Lvl21  :[0x50228,21],
            LocationName.Lvl22  :[0x50229,22],
            LocationName.Lvl23  :[0x5022A,23],
            LocationName.Lvl24  :[0x5022B,24],
            LocationName.Lvl25  :[0x5022C,25],
            LocationName.Lvl26  :[0x5022D,26],
            LocationName.Lvl27  :[0x5022E,27],
            LocationName.Lvl28  :[0x5022F,28],
            LocationName.Lvl29  :[0x50230,29],
            LocationName.Lvl30  :[0x50231,30],
            LocationName.Lvl31  :[0x50232,31],
            LocationName.Lvl32  :[0x50233,32],
            LocationName.Lvl33  :[0x50234,33],
            LocationName.Lvl34  :[0x50235,34],
            LocationName.Lvl35  :[0x50236,35],
            LocationName.Lvl36  :[0x50237,36],
            LocationName.Lvl37  :[0x50238,37],
            LocationName.Lvl38  :[0x50239,38],
            LocationName.Lvl39  :[0x5023A,39],
            LocationName.Lvl40  :[0x5023B,40],
            LocationName.Lvl41  :[0x5023C,41],
            LocationName.Lvl42  :[0x5023D,42],
            LocationName.Lvl43  :[0x5023E,43],
            LocationName.Lvl44  :[0x5023F,44],
            LocationName.Lvl45  :[0x50240,45],
            LocationName.Lvl46  :[0x50241,46],
            LocationName.Lvl47  :[0x50242,47],
            LocationName.Lvl48  :[0x50243,48],
            LocationName.Lvl49  :[0x50244,49],
            LocationName.Lvl50  :[0x50245,50],
            LocationName.Lvl51  :[0x50246,51],
            LocationName.Lvl52  :[0x50247,52],
            LocationName.Lvl53  :[0x50248,53],
            LocationName.Lvl54  :[0x50249,54],
            LocationName.Lvl55  :[0x5024A,55],
            LocationName.Lvl56  :[0x5024B,56],
            LocationName.Lvl57  :[0x5024C,57],
            LocationName.Lvl58  :[0x5024D,58],
            LocationName.Lvl59  :[0x5024E,59],
            LocationName.Lvl60  :[0x5024F,60],
            LocationName.Lvl61  :[0x50250,61],
            LocationName.Lvl62  :[0x50251,62],
            LocationName.Lvl63  :[0x50252,63],
            LocationName.Lvl64  :[0x50253,64],
            LocationName.Lvl65  :[0x50254,65],
            LocationName.Lvl66  :[0x50255,66],
            LocationName.Lvl67  :[0x50256,67],
            LocationName.Lvl68  :[0x50257,68],
            LocationName.Lvl69  :[0x50258,69],
            LocationName.Lvl70  :[0x50259,70],
            LocationName.Lvl71  :[0x5025A,71],
            LocationName.Lvl72  :[0x5025B,72],
            LocationName.Lvl73  :[0x5025C,73],
            LocationName.Lvl74  :[0x5025D,74],
            LocationName.Lvl75  :[0x5025E,75],
            LocationName.Lvl76  :[0x5025F,76],
            LocationName.Lvl77  :[0x50260,77],
            LocationName.Lvl78  :[0x50261,78],
            LocationName.Lvl79  :[0x50262,79],
            LocationName.Lvl80  :[0x50263,80],
            LocationName.Lvl81  :[0x50264,81],
            LocationName.Lvl82  :[0x50265,82],
            LocationName.Lvl83  :[0x50266,83],
            LocationName.Lvl84  :[0x50267,84],
            LocationName.Lvl85  :[0x50268,85],
            LocationName.Lvl86  :[0x50269,86],
            LocationName.Lvl87  :[0x5026A,87],
            LocationName.Lvl88  :[0x5026B,88],
            LocationName.Lvl89  :[0x5026C,89],
            LocationName.Lvl90  :[0x5026D,90],
            LocationName.Lvl91  :[0x5026E,91],
            LocationName.Lvl92  :[0x5026F,92],
            LocationName.Lvl93  :[0x50270,93],
            LocationName.Lvl94  :[0x50271,94],
            LocationName.Lvl95  :[0x50272,95],
            LocationName.Lvl96  :[0x50273,96],
            LocationName.Lvl97  :[0x50274,97],
            LocationName.Lvl98  :[0x50275,98],
    }
    Level_Region=create_region(world,player,active_locations,LocationName.SoraLevels_Region,
                               Level_Region_locations,None)
    world.regions += [
    LoD_Region         ,  
    LoD2_Region        ,
    Ag_Region          ,
    Ag2_Region         ,
    Dc_Region          ,       
    Tr_Region          ,
    HundredAcre1_Region,         
    HundredAcre2_Region,
    HundredAcre3_Region,
    HundredAcre4_Region,
    HundredAcre5_Region,
    HundredAcre6_Region,                 
    Pr_Region          ,         
    Pr2_Region         ,         
    Oc_Region          ,   
    Oc2_Region         ,
    Oc2Cups_Region  ,                              
    Bc_Region          ,        
    Bc2_Region         , 
    Sp_Region          ,
    Sp2_Region         ,
    Ht_Region          ,        
    Ht2_Region         ,
    Hb_Region          ,        
    Hb2_Region         ,          
    CoR_Region         ,                         
    Pl_Region          ,        
    Pl2_Region         ,          
    STT_Region         ,         
    TT_Region          ,       
    TT2_Region         ,          
    TT3_Region         ,       
    Twtnw_Region       ,          
    Twtnw2_Region      ,
    GoA_Region          ,
    menu_region         ,
    Valor_Region       ,
    Wisdom_Region      ,
    Limit_Region       ,
    Master_Region      ,
    Final_Region       ,
    Level_Region,
    ]
def connect_regions (world: MultiWorld, player: int, self):
      #connecting every first visit to the GoA 
      #2 Visit locking and is going to be turned off mabybe
      
      names: typing.Dict[str, int] = {}
      connect(world, player, names, 'Menu', LocationName.GoA_Region)
      connect(world, player, names,LocationName.GoA_Region, LocationName.LoD_Region)
      connect(world, player, names,LocationName.LoD_Region, LocationName.LoD2_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.Oc_Region)
      connect(world, player, names,LocationName.Oc_Region, LocationName.Oc2_Region)

      connect(world, player, names,LocationName.Oc2_Region, LocationName.Oc2Cups_Region)   

      connect(world, player, names,LocationName.GoA_Region, LocationName.Ag_Region)
      connect(world, player, names,LocationName.Ag_Region, LocationName.Ag2_Region,
              lambda state: (state.has(ItemName.FireElement, player) 
                             and state.has(ItemName.BlizzardElement,player)
                             and state.has(ItemName.ThunderElement,player)))

      connect(world, player, names,LocationName.GoA_Region, LocationName.Dc_Region)
      connect(world, player, names,LocationName.Dc_Region, LocationName.Tr_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.Pr_Region)
      connect(world, player, names,LocationName.Pr_Region, LocationName.Pr2_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.Bc_Region,)
      connect(world, player, names,LocationName.Bc_Region, LocationName.Bc2_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.Sp_Region)
      connect(world, player, names,LocationName.Sp_Region, LocationName.Sp2_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.Ht_Region)
      connect(world, player, names,LocationName.Ht_Region, LocationName.Ht2_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.Hb_Region)
      connect(world, player, names,LocationName.Hb_Region, LocationName.Hb2_Region)

      connect(world, player, names,LocationName.Hb2_Region, LocationName.CoR_Region)


      connect(world, player, names,LocationName.GoA_Region, LocationName.Pl_Region)
      connect(world, player, names,LocationName.Pl_Region, LocationName.Pl2_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.STT_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.TT_Region)
      connect(world, player, names,LocationName.TT_Region, LocationName.TT2_Region) 
      connect(world, player, names,LocationName.TT2_Region, LocationName.TT3_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.Twtnw_Region)
      connect(world, player, names,LocationName.Twtnw_Region, LocationName.Twtnw2_Region)

      connect(world, player, names,LocationName.GoA_Region, LocationName.HundredAcre1_Region,
          lambda state: (state.has(ItemName.TornPages, player,1)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.HundredAcre2_Region,
          lambda state: (state.has(ItemName.TornPages, player,2)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.HundredAcre3_Region,
          lambda state: (state.has(ItemName.TornPages, player,3)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.HundredAcre4_Region,
          lambda state: (state.has(ItemName.TornPages, player,4)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.HundredAcre5_Region,
          lambda state: (state.has(ItemName.TornPages, player,5)))
      
      

      for region in(firstVisits):
          connect(world, player, names, region,LocationName.SoraLevels_Region)
          
          connect(world, player, names,region, LocationName.Valor_Region,
              lambda state: state.has(ItemName.ValorForm,player))
          connect(world, player, names,region, LocationName.Wisdom_Region,
                  lambda state: state.has(ItemName.WisdomForm,player))
          connect(world, player, names,region, LocationName.Limit_Region,
                  lambda state: state.has(ItemName.LimitForm,player))
          connect(world, player, names,region, LocationName.Master_Region,
                  lambda state: state.has(ItemName.MasterForm,player))
          connect(world, player, names,region, LocationName.Final_Region,
                  lambda state: state.has(ItemName.FinalForm,player))
def connect(world: MultiWorld, player: int, used_names: typing.Dict[str, int], source: str, target: str,
    rule: typing.Optional[typing.Callable] = None):
    source_region = world.multiworld.get_region(source, player)
    target_region = world.multiworld.get_region(target, player)


#shamelessly stolen from the sa2b
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
                location = KH2Location(player, location, loc_id, ret)
                ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))
    return ret