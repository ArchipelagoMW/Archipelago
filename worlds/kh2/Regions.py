from pickle import TRUE
import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Items import KH2Item
from .Options import FinalEXP, MasterEXP, LimitEXP, WisdomEXP, ValorEXP, Schmovement,SuperBosses
from .Locations import HadesCups, LocationName, Oc2Cups,setup_locations,KH2Location
from .Names import LocationName, ItemName

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

def create_regions(world, player: int, active_locations):
    menu_region = create_region(world, player, active_locations, 'Menu', None, None)
    
    GoA_Region_locations={
        LocationName.GardenofAssemblageMap :[0x4864,1],
        LocationName.GoALostIllusion       :[0x4865,2],
        LocationName.ProofofNonexistence   :[0x4866,3],
}
    GoA_Region = create_region(world, player, active_locations, LocationName.GoA_Region,
                                       GoA_Region_locations, None)

    LoD_Region_locations = {
        LocationName.BambooGroveDarkShard       :[4867,1],
        LocationName.BambooGroveEther           :[4868,2],
        LocationName.BambooGroveMythrilShard    :[4869,3],
        LocationName.EncampmentAreaMap          :[4870,4],
        LocationName.Mission3                   :[4871,5],
        LocationName.CheckpointHiPotion         :[4872,6],
        LocationName.CheckpointMythrilShard     :[4873,7],
        LocationName.MountainTrailLightningShard:[4874,8],
        LocationName.MountainTrailRecoveryRecipe:[4875,9],
        LocationName.MountainTrailEther         :[4876,10],
        LocationName.MountainTrailMythrilShard  :[4877,11],
        LocationName.VillageCaveAreaMap         :[4878,12],
        LocationName.VillageCaveAPBoost         :[4879,13],
        LocationName.VillageCaveDarkShard       :[4880,14],
        LocationName.VillageCaveBonus           :[4881,15],
        LocationName.RidgeFrostShard            :[4882,16],
        LocationName.RidgeAPBoost               :[4883,17],
        LocationName.ShanYu                     :[4884,18],
        LocationName.HiddenDragon               :[4885,19],
        } 
    LoD_Region = create_region(world, player, active_locations, LocationName.LoD_Region,
                                       LoD_Region_locations, None)
    LoD2_Region_locations = {
        LocationName.ThroneRoomTornPages     :[4886,1],
        LocationName.ThroneRoomPalaceMap     :[4887,2],
        LocationName.ThroneRoomAPBoost       :[4888,3],
        LocationName.ThroneRoomQueenRecipe   :[4889,4],
        LocationName.ThroneRoomAPBoost2      :[4890,5],
        LocationName.ThroneRoomOgreShield    :[4891,6],
        LocationName.ThroneRoomMythrilCrystal:[4892,7],
        LocationName.ThroneRoomOrichalcum    :[4893,8],
        LocationName.StormRider              :[4894,9],
        LocationName.XigbarDataDefenseBoost  :[4895,10],
        }
    LoD2_Region = create_region(world, player, active_locations, LocationName.LoD2_Region,
                                       LoD2_Region_locations, None)
    Ag_Region_locations={
        LocationName.AgrabahMap                       :[4896,1],
        LocationName.AgrabahDarkShard                 :[4897,2],
        LocationName.AgrabahMythrilShard              :[4898,3],
        LocationName.AgrabahHiPotion                  :[4899,4],
        LocationName.AgrabahAPBoost                   :[4900,5],
        LocationName.AgrabahMythrilStone              :[4901,6],
        LocationName.AgrabahMythrilShard2             :[4902,7],
        LocationName.AgrabahSerenityShard             :[4903,8],
        LocationName.BazaarMythrilGem                 :[4904,9],
        LocationName.BazaarPowerShard                 :[4905,10],
        LocationName.BazaarHiPotion                   :[4906,11],
        LocationName.BazaarAPBoost                    :[4907,12],
        LocationName.BazaarMythrilShard               :[4908,13],
        LocationName.PalaceWallsSkillRing             :[4909,14],
        LocationName.PalaceWallsMythrilStone          :[4910,15],
        LocationName.CaveEntrancePowerStone           :[4911,16],
        LocationName.CaveEntranceMythrilShard         :[4912,17],
        LocationName.ValleyofStoneMythrilStone        :[4913,18],
        LocationName.ValleyofStoneAPBoost             :[4914,19],
        LocationName.ValleyofStoneMythrilShard        :[4915,20],
        LocationName.ValleyofStoneHiPotion            :[4916,21],
        LocationName.AbuEscort                        :[4917,22],
        LocationName.ChasmofChallengesCaveofWondersMap:[4918,23],
        LocationName.ChasmofChallengesAPBoost         :[4919,24],
        LocationName.TreasureRoom                     :[4920,25],
        LocationName.TreasureRoomAPBoost              :[4921,26],
        LocationName.TreasureRoomSerenityGem          :[4922,27],
        LocationName.ElementalLords                   :[4923,28],
        LocationName.LampCharm                        :[4924,29],
        }
    Ag_Region = create_region(world, player, active_locations, LocationName.Ag_Region,
                                       Ag_Region_locations, None)
    Ag2_Region_locations={
        LocationName.RuinedChamberTornPages         :[4925,1],
        LocationName.RuinedChamberRuinsMap          :[4926,2],
        LocationName.GenieJafar                     :[4927,3],
        LocationName.WishingLamp                    :[4928,4],
        LocationName.LexaeusBonus                   :[4929,5],
        LocationName.LexaeusASStrengthBeyondStrength:[4930,6],
        LocationName.LexaeusDataLostIllusion        :[4931,7],
        }
    Ag2_Region = create_region(world, player, active_locations, LocationName.Ag2_Region,
                                       Ag2_Region_locations, None)

    Dc_Region_locations = {
            LocationName.DCCourtyardMythrilShard  :[4932,1],
            LocationName.DCCourtyardStarRecipe    :[4933,2],
            LocationName.DCCourtyardAPBoost       :[4934,3],
            LocationName.DCCourtyardMythrilStone  :[4935,4],
            LocationName.DCCourtyardBlazingStone  :[4936,5],
            LocationName.DCCourtyardBlazingShard  :[4937,6],
            LocationName.DCCourtyardMythrilShard2 :[4938,7],
            LocationName.LibraryTornPages         :[4939,8],
            LocationName.DisneyCastleMap          :[4940,9],
            LocationName.MinnieEscort             :[4941,10],
        }
    Dc_Region = create_region(world, player, active_locations, LocationName.Dc_Region,
                                       Dc_Region_locations, None)
    Tr_Region_locations = {
        LocationName.CornerstoneHillMap            :[4942,1],
        LocationName.CornerstoneHillFrostShard     :[4943,2],
        LocationName.PierMythrilShard              :[4944,3],
        LocationName.PierHiPotion                  :[4945,4],
        LocationName.WaterwayMythrilStone          :[4946,5],
        LocationName.WaterwayAPBoost               :[4947,6],
        LocationName.WaterwayFrostStone            :[4948,7],
        LocationName.WindowofTimeMap               :[4949,8],
        LocationName.BoatPete                      :[4950,9],
        LocationName.FuturePete                    :[4951,10],
        LocationName.Monochrome                    :[4952,11],
        LocationName.WisdomForm                    :[4953,12],
        LocationName.MarluxiaBonus                 :[4954,13],
        LocationName.MarluxiaASEternalBlossom      :[4955,14],
        LocationName.MarluxiaDataLostIllusion      :[4956,15],
        LocationName.LingeringWillBonus            :[4957,16],
        LocationName.LingeringWillProofofConnection:[4958,17],
        LocationName.LingeringWillManifestIllusion :[4959,18],
        }
    Tr_Region = create_region(world, player, active_locations, LocationName.Tr_Region,
                                       Tr_Region_locations, None)

    HundredAcre1_Region_locations = {
            LocationName.PoohsHouse100AcreWoodMap:[4960,1],
            LocationName.PoohsHouseAPBoost       :[4961,2],
            LocationName.PoohsHouseMythrilStone  :[4962,3],
        }
    HundredAcre1_Region = create_region(world, player, active_locations, LocationName.HundredAcre1_Region,
                                       HundredAcre1_Region_locations, None)
    HundredAcre2_Region_locations = {
            LocationName.PigletsHouseDefenseBoost:[4963,1],
            LocationName.PigletsHouseAPBoost     :[4964,2],
            LocationName.PigletsHouseMythrilGem  :[4965,3],
        }
    HundredAcre2_Region = create_region(world, player, active_locations, LocationName.HundredAcre2_Region,
                                       HundredAcre2_Region_locations, None)
    HundredAcre3_Region_locations = {
            LocationName.RabbitsHouseDrawRing       :[4966,1],
            LocationName.RabbitsHouseMythrilCrystal :[4967,2],
            LocationName.RabbitsHouseAPBoost        :[4968,3],
        }
    HundredAcre3_Region = create_region(world, player, active_locations, LocationName.HundredAcre3_Region,
                                       HundredAcre3_Region_locations, None)
    HundredAcre4_Region_locations = {
            LocationName.KangasHouseMagicBoost :[4969,1],
            LocationName.KangasHouseAPBoost    :[4970,2],
            LocationName.KangasHouseOrichalcum :[4971,3],
        }
    HundredAcre4_Region = create_region(world, player, active_locations, LocationName.HundredAcre4_Region,
                                       HundredAcre4_Region_locations, None)
    HundredAcre5_Region_locations = {
            LocationName.SpookyCaveMythrilGem    :[4972,1],
            LocationName.SpookyCaveAPBoost       :[4973,2],
            LocationName.SpookyCaveOrichalcum    :[4974,3],
            LocationName.SpookyCaveGuardRecipe   :[4975,4],
            LocationName.SpookyCaveMythrilCrystal:[4976,5],
            LocationName.SpookyCaveAPBoost2      :[4977,6],
            LocationName.SweetMemories           :[4978,7],
            LocationName.SpookyCaveMap           :[4979,8],
        }
    HundredAcre5_Region = create_region(world, player, active_locations, LocationName.HundredAcre5_Region,
                                       HundredAcre5_Region_locations, None)
    HundredAcre6_Region_locations = {
            LocationName.StarryHillCosmicRing     :[4980,1],
            LocationName.StarryHillStyleRecipe    :[4981,2],
            LocationName.StarryHillCureElement    :[4982,3],
            LocationName.StarryHillOrichalcumPlus :[4983,4],
        }
    HundredAcre6_Region = create_region(world, player, active_locations, LocationName.HundredAcre6_Region,
                                       HundredAcre6_Region_locations, None)
    Pr_Region_locations = {
            LocationName.RampartNavalMap          :[4984,1],
            LocationName.RampartMythrilStone      :[4985,2],
            LocationName.RampartDarkShard         :[4986,3],
            LocationName.TownDarkStone            :[4987,4],
            LocationName.TownAPBoost              :[4988,5],
            LocationName.TownMythrilShard         :[4989,6],
            LocationName.TownMythrilGem           :[4990,7],
            LocationName.CaveMouthBrightShard     :[4991,8],
            LocationName.CaveMouthMythrilShard    :[4992,9],
            LocationName.IsladeMuertaMap          :[4993,10],
            LocationName.BoatFight                :[4994,11],
            LocationName.InterceptorBarrels       :[4995,12],
            LocationName.PowderStoreAPBoost1      :[4996,13],
            LocationName.PowderStoreAPBoost2      :[4997,14],
            LocationName.MoonlightNookMythrilShard:[4998,15],
            LocationName.MoonlightNookSerenityGem :[4999,16],
            LocationName.MoonlightNookPowerStone  :[5000,17],
            LocationName.Barbossa                 :[5001,18],
            LocationName.FollowtheWind            :[5002,19],
        }
    Pr_Region = create_region(world, player, active_locations, LocationName.Pr_Region,
                                       Pr_Region_locations, None)
    Pr2_Region_locations = {
        LocationName.GrimReaper1                 :[5003,1],
        LocationName.InterceptorsHoldFeatherCharm:[5004,2],
        LocationName.SeadriftKeepAPBoost         :[5005,3],
        LocationName.SeadriftKeepOrichalcum      :[5006,4],
        LocationName.SeadriftKeepMeteorStaff     :[5007,5],
        LocationName.SeadriftRowSerenityGem      :[5008,6],
        LocationName.SeadriftRowKingRecipe       :[5009,7],
        LocationName.SeadriftRowMythrilCrystal   :[5010,8],
        LocationName.SeadriftRowCursedMedallion  :[5011,9],
        LocationName.SeadriftRowShipGraveyardMap :[5012,10],
        LocationName.GrimReaper2                 :[5013,11],
        LocationName.SecretAnsemReport6          :[5014,12],
        LocationName.LuxordDataAPBoost           :[5015,13],
        }
    Pr2_Region = create_region(world, player, active_locations, LocationName.Pr2_Region,
                                       Pr2_Region_locations, None)
    Oc_Region_locations = {
            LocationName.PassageMythrilShard         :[5016,1],
            LocationName.PassageMythrilStone         :[5017,2],
            LocationName.PassageEther                :[5018,3],
            LocationName.PassageAPBoost              :[5019,4],
            LocationName.PassageHiPotion             :[5020,5],
            LocationName.InnerChamberUnderworldMap   :[5021,6],
            LocationName.InnerChamberMythrilShard    :[5022,7],
            LocationName.Cerberus                    :[5023,8],
            LocationName.ColiseumMap                 :[5024,9],
            LocationName.Urns                        :[5025,10],
            LocationName.UnderworldEntrancePowerBoost:[5026,11],
            LocationName.CavernsEntranceLucidShard   :[5027,12],
            LocationName.CavernsEntranceAPBoost      :[5028,13],
            LocationName.CavernsEntranceMythrilShard :[5029,14],
            LocationName.TheLostRoadBrightShard      :[5030,15],
            LocationName.TheLostRoadEther            :[5031,16],
            LocationName.TheLostRoadMythrilShard     :[5032,17],
            LocationName.TheLostRoadMythrilStone     :[5033,18],
            LocationName.AtriumLucidStone            :[5034,19],
            LocationName.AtriumAPBoost               :[5035,20],
            LocationName.DemyxOC                     :[5036,21],
            LocationName.SecretAnsemReport5          :[5037,22],
            LocationName.OlympusStone                :[5038,23],
            LocationName.TheLockCavernsMap           :[5039,24],
            LocationName.TheLockMythrilShard         :[5040,25],
            LocationName.TheLockAPBoost              :[5041,26],
            LocationName.PeteOC                      :[5042,27],
            LocationName.Hydra                       :[5043,28],
            LocationName.HerosCrest                  :[5044,29],
        }
    Oc_Region = create_region(world, player, active_locations, LocationName.Oc_Region,
                                       Oc_Region_locations, None)
    Oc2_Region_locations = {
            LocationName.AuronsStatue          :[5045,1],
            LocationName.Hades                 :[5046,2],
            LocationName.GuardianSoul          :[5047,3],
            LocationName.ZexionBonus           :[5048,4],
            LocationName.ZexionASBookofShadows :[5049,5],
            LocationName.ZexionDataLostIllusion:[5050,6],
        }
    Oc2_Region = create_region(world, player, active_locations, LocationName.Oc2_Region,
                                       Oc2_Region_locations, None)
    Oc2Cups_Region_locations = {
            LocationName.ProtectBeltPainandPanicCup    :[5051,1],
            LocationName.SerenityGemPainandPanicCup    :[5052,3],
            LocationName.RisingDragonCerberusCup       :[5053,4],
            LocationName.SerenityCrystalCerberusCup    :[5054,5],
            LocationName.GenjiShieldTitanCup           :[5055,6],
            LocationName.SkillfulRingTitanCup          :[5056,7],
            LocationName.FatalCrestGoddessofFateCup    :[5057,8],
            LocationName.OrichalcumPlusGoddessofFateCup:[5058,9],
        }
    Oc2Cups_Region = create_region(world, player, active_locations, LocationName.Oc2Cups_Region,
                                       Oc2Cups_Region_locations, None)
    HadesCups_Region_locations = {
            LocationName.HadesCupTrophyParadoxCups :[5059,1],
        }
    HadesCups_Region = create_region(world, player, active_locations, LocationName.HadesCups_Region,
                                       HadesCups_Region_locations, None)
    Bc_Region_locations = {
                LocationName.BCCourtyardAPBoost                :[5060,1],
                LocationName.BCCourtyardHiPotion               :[5061,2],
                LocationName.BCCourtyardMythrilShard           :[5062,3],
                LocationName.BellesRoomCastleMap               :[5063,4],
                LocationName.BellesRoomMegaRecipe              :[5064,5],
                LocationName.TheEastWingMythrilShard           :[5065,6],
                LocationName.TheEastWingTent                   :[5066,7],
                LocationName.TheWestHallHiPotion               :[5067,8],
                LocationName.TheWestHallPowerShard             :[5068,9],
                LocationName.TheWestHallAPBoost                :[5069,10],
                LocationName.TheWestHallBrightStone            :[5070,11],
                LocationName.TheWestHallMythrilShard           :[5071,12],
                LocationName.Thresholder                       :[5072,13],
                LocationName.DungeonBasementMap                :[5073,14],
                LocationName.DungeonAPBoost                    :[5074,15],
                LocationName.SecretPassageMythrilShard         :[5075,16],
                LocationName.SecretPassageHiPotion             :[5076,17],
                LocationName.SecretPassageLucidShard           :[5077,18],
                LocationName.TheWestHallMythrilShardPostDungeon:[5078,19],
                LocationName.TheWestWingMythrilShard           :[5079,20],
                LocationName.TheWestWingTent                   :[5080,21],
                LocationName.Beast                             :[5081,22],
                LocationName.TheBeastsRoomBlazingShard         :[5082,23],
                LocationName.DarkThornBonus                    :[5083,24],
                LocationName.DarkThornCureElement              :[5084,25],
        }
    Bc_Region = create_region(world, player, active_locations, LocationName.Bc_Region,
                                       Bc_Region_locations, None)
    Bc2_Region_locations = {
            LocationName.RumblingRose          :[5085,1],
            LocationName.CastleWallsMap        :[5086,2],
            LocationName.XaldinBonus           :[5087,3],
            LocationName.SecretAnsemReport4    :[5088,4],
            LocationName.XaldinDataDefenseBoost:[5089,5],
        }
    Bc2_Region = create_region(world, player, active_locations, LocationName.Bc2_Region,
                                       Bc2_Region_locations, None)
    Sp_Region_locations = {
                LocationName.PitCellAreaMap              :[5090,1],
                LocationName.PitCellMythrilCrystal       :[5091,2],
                LocationName.CanyonDarkCrystal           :[5092,3],
                LocationName.CanyonMythrilStone          :[5093,4],
                LocationName.CanyonMythrilGem            :[5094,5],
                LocationName.CanyonFrostCrystal          :[5095,6],
                LocationName.Screens                     :[5096,7],
                LocationName.HallwayPowerCrystal         :[5097,8],
                LocationName.HallwayAPBoost              :[5098,9],
                LocationName.CommunicationsRoomIOTowerMap:[5099,10],
                LocationName.CommunicationsRoomGaiaBelt  :[5100,11],
                LocationName.HostileProgram              :[5101,12],
                LocationName.PhotonDebugger              :[5102,13],
        }
    Sp_Region = create_region(world, player, active_locations, LocationName.Sp_Region,
                                       Sp_Region_locations, None)
    Sp2_Region_locations = {
            LocationName.SolarSailer                      :[5103,1],
            LocationName.CentralComputerCoreAPBoost       :[5104,2],
            LocationName.CentralComputerCoreOrichalcumPlus:[5105,3],
            LocationName.CentralComputerCoreCosmicArts    :[5106,4],
            LocationName.CentralComputerCoreMap           :[5107,5],
            LocationName.MCP                              :[5108,6],
            LocationName.LarxeneBonus                     :[5109,7],
            LocationName.LarxeneASCloakedThunder          :[5110,8],
            LocationName.LarxeneDataLostIllusion          :[5111,9],
        }
    Sp2_Region = create_region(world, player, active_locations, LocationName.Sp2_Region,
                                       Sp2_Region_locations, None)
    Ht_Region_locations = {
            LocationName.GraveyardMythrilShard          :[5112,1],
            LocationName.GraveyardSerenityGem           :[5113,2],
            LocationName.FinklesteinsLabHalloweenTownMap:[5114,3],
            LocationName.TownSquareMythrilStone         :[5115,4],
            LocationName.TownSquareEnergyShard          :[5116,5],
            LocationName.HinterlandsLightningShard      :[5117,6],
            LocationName.HinterlandsMythrilStone        :[5118,7],
            LocationName.HinterlandsAPBoost             :[5119,8],
            LocationName.CandyCaneLaneMegaPotion        :[5120,9],
            LocationName.CandyCaneLaneMythrilGem        :[5121,10],
            LocationName.CandyCaneLaneLightningStone    :[5122,11],
            LocationName.CandyCaneLaneMythrilStone      :[5123,12],
            LocationName.SantasHouseChristmasTownMap    :[5124,13],
            LocationName.SantasHouseAPBoost             :[5125,14],
            LocationName.PrisonKeeper                   :[5126,15],
            LocationName.OogieBoogie                    :[5127,16],
            LocationName.OogieBoogieMagnetElement       :[5128,17],
        }
    Ht_Region = create_region(world, player, active_locations, LocationName.Ht_Region,
                                       Ht_Region_locations, None)
    Ht2_Region_locations = {
            LocationName.Lock                  :[5129,1],
            LocationName.Present               :[5130,2],
            LocationName.DecoyPresents         :[5131,3],
            LocationName.Experiment            :[5132,4],
            LocationName.DecisivePumpkin       :[5133,5],
            LocationName.VexenBonus            :[5134,6],
            LocationName.VexenASRoadtoDiscovery:[5135,7],
            LocationName.VexenDataLostIllusion :[5136,8],
        }
    Ht2_Region = create_region(world, player, active_locations, LocationName.Ht2_Region,
                                       Ht2_Region_locations, None)

    Hb_Region_locations = {
            LocationName.MarketplaceMap             :[5137,1],
            LocationName.BoroughDriveRecovery       :[5138,2],
            LocationName.BoroughAPBoost             :[5139,3],
            LocationName.BoroughHiPotion            :[5140,4],
            LocationName.BoroughMythrilShard        :[5141,5],
            LocationName.BoroughDarkShard           :[5142,6],
            LocationName.MerlinsHouseMembershipCard :[5143,7],
            LocationName.MerlinsHouseBlizzardElement:[5144,8],
            LocationName.Bailey                     :[5145,9],
            LocationName.BaileySecretAnsemReport7   :[5146,10],
            LocationName.BaseballCharm              :[5147,11],
        }
    Hb_Region = create_region(world, player, active_locations, LocationName.Hb_Region,
                                       Hb_Region_locations, None)
    Hb2_Region_locations = {
            LocationName.PosternCastlePerimeterMap          :[5148,1],
            LocationName.PosternMythrilGem                  :[5149,2],
            LocationName.PosternAPBoost                     :[5150,3],
            LocationName.CorridorsMythrilStone              :[5151,4],
            LocationName.CorridorsMythrilCrystal            :[5152,5],
            LocationName.CorridorsDarkCrystal               :[5153,6],
            LocationName.CorridorsAPBoost                   :[5154,7],
            LocationName.AnsemsStudyMasterForm              :[5155,8],
            LocationName.AnsemsStudySleepingLion            :[5156,9],
            LocationName.AnsemsStudySkillRecipe             :[5157,10],
            LocationName.AnsemsStudyUkuleleCharm            :[5158,11],
            LocationName.RestorationSiteMoonRecipe          :[5159,12],
            LocationName.RestorationSiteAPBoost             :[5160,13],
            LocationName.DemyxHB                            :[5161,14],
            LocationName.FFFightsCureElement                :[5162,15],
            LocationName.CrystalFissureTornPages            :[5163,16],
            LocationName.CrystalFissureTheGreatMawMap       :[5164,17],
            LocationName.CrystalFissureEnergyCrystal        :[5165,18],
            LocationName.CrystalFissureAPBoost              :[5166,19],
            LocationName.ThousandHeartless                  :[5167,20],
            LocationName.ThousandHeartlessSecretAnsemReport1:[5168,20],
            LocationName.ThousandHeartlessIceCream          :[5169,21],
            LocationName.ThousandHeartlessPicture           :[5170,22],
            LocationName.PosternGullWing                    :[5171,23],
            LocationName.HeartlessManufactoryCosmicChain    :[5172,24],
            LocationName.SephirothBonus                     :[5173,25],
            LocationName.SephirothFenrir                    :[5174,26],
            LocationName.WinnersProof                       :[5175,27],
            LocationName.ProofofPeace                       :[5176,28],
            LocationName.DemyxDataAPBoost                   :[5177,29],
        }
    Hb2_Region = create_region(world, player, active_locations, LocationName.Hb2_Region,
                                       Hb2_Region_locations, None)

    CoR_Region_locations = {
            LocationName.CoRDepthsAPBoost                            :[5178,1],
            LocationName.CoRDepthsPowerCrystal                       :[5179,2],
            LocationName.CoRDepthsFrostCrystal                       :[5180,3],
            LocationName.CoRDepthsManifestIllusion                   :[5181,4],
            LocationName.CoRDepthsAPBoost2                           :[5182,5],
            LocationName.CoRMineshaftLowerLevelDepthsofRemembranceMap:[5183,6],
            LocationName.CoRMineshaftLowerLevelAPBoost               :[5184,7],
        }
    CoR_Region = create_region(world, player, active_locations, LocationName.CoR_Region,
                                       CoR_Region_locations, None)
    FirstHalf_Region_locations = {
            LocationName.CoRDepthsUpperLevelRemembranceGem:[5185,1],
            LocationName.CoRMiningAreaSerenityGem         :[5186,2],
            LocationName.CoRMiningAreaAPBoost             :[5187,3],
            LocationName.CoRMiningAreaSerenityCrystal     :[5188,4],
            LocationName.CoRMiningAreaManifestIllusion    :[5189,5],
            LocationName.CoRMiningAreaSerenityGem2        :[5190,6],
            LocationName.CoRMiningAreaDarkRemembranceMap  :[5191,7],
            LocationName.CoRMineshaftMidLevelPowerBoost   :[5192,8],
            LocationName.CoREngineChamberSerenityCrystal  :[5193,9],
            LocationName.CoREngineChamberRemembranceCrystal:[5194,10],
            LocationName.CoREngineChamberAPBoost          :[5195,11],
            LocationName.CoREngineChamberManifestIllusion :[5196,12],
            LocationName.CoRMineshaftUpperLevelMagicBoost :[5197,13],
        }
    FirstHalf_Region = create_region(world, player, active_locations, LocationName.FirstHalf_Region,
                                       FirstHalf_Region_locations, None)
    SecondHalf_Region_locations = {
            LocationName.CoRMineshaftUpperLevelAPBoost:[5198,1],
            LocationName.TransporttoRemembrance       :[5199,2],
        }
    SecondHalf_Region = create_region(world, player, active_locations, LocationName.SecondHalf_Region,
                                       SecondHalf_Region_locations, None)

    Pl_Region_locations = {
            LocationName.GorgeSavannahMap             :[5200,1],
            LocationName.GorgeDarkGem                 :[5201,2],
            LocationName.GorgeMythrilStone            :[5202,3],
            LocationName.ElephantGraveyardFrostGem    :[5203,4],
            LocationName.ElephantGraveyardMythrilStone:[5204,5],
            LocationName.ElephantGraveyardBrightStone :[5205,6],
            LocationName.ElephantGraveyardAPBoost     :[5206,7],
            LocationName.ElephantGraveyardMythrilShard:[5207,8],
            LocationName.PrideRockMap                 :[5208,9],
            LocationName.PrideRockMythrilStone        :[5209,10],
            LocationName.PrideRockSerenityCrystal     :[5210,11],
            LocationName.WildebeestValleyEnergyStone  :[5211,12],
            LocationName.WildebeestValleyAPBoost      :[5212,13],
            LocationName.WildebeestValleyMythrilGem   :[5213,14],
            LocationName.WildebeestValleyMythrilStone :[5214,15],
            LocationName.WildebeestValleyLucidGem     :[5215,16],
            LocationName.WastelandsMythrilShard       :[5216,17],
            LocationName.WastelandsSerenityGem        :[5217,18],
            LocationName.WastelandsMythrilStone       :[5218,19],
            LocationName.JungleSerenityGem            :[5219,20],
            LocationName.JungleMythrilStone           :[5220,21],
            LocationName.JungleSerenityCrystal        :[5221,22],
            LocationName.OasisMap                     :[5222,23],
            LocationName.OasisTornPages               :[5223,24],
            LocationName.OasisAPBoost                 :[5224,25],
            LocationName.CircleofLife                 :[5225,26],
            LocationName.Hyenas1                      :[5226,27],
            LocationName.Scar                         :[5227,28],
            LocationName.ScarFireElement              :[5228,29],
        }
    Pl_Region = create_region(world, player, active_locations, LocationName.Pl_Region,
                                       Pl_Region_locations, None)
    Pl2_Region_locations = {
            LocationName.Hyenas2             :[5229,1],
            LocationName.Groundshaker        :[5230,2],
            LocationName.SaixDataDefenseBoost:[5231,3],
        }
    Pl2_Region = create_region(world, player, active_locations, LocationName.Pl2_Region,
                                       Pl2_Region_locations, None)

    STT_Region_locations = {
            LocationName.TwilightTownMap                :[5232,1],
            LocationName.MunnyPouchOlette               :[5233,2],
            LocationName.StationDusks                   :[5234,3],
            LocationName.StationofSerenityPotion        :[5235,4],
            LocationName.StationofCallingPotion         :[5236,5],
            LocationName.TwilightThorn                  :[5237,6],
            LocationName.Axel1                          :[5238,7],
            LocationName.JunkChampionBelt               :[5239,8],
            LocationName.JunkMedal                      :[5240,9],
            LocationName.TheStruggleTrophy              :[5241,10],
            LocationName.CentralStationPotion1          :[5242,11],
            LocationName.STTCentralStationHiPotion      :[5243,12],
            LocationName.CentralStationPotion2          :[5244,13],
            LocationName.SunsetTerraceAbilityRing       :[5245,14],
            LocationName.SunsetTerraceHiPotion          :[5246,15],
            LocationName.SunsetTerracePotion1           :[5247,16],
            LocationName.SunsetTerracePotion2           :[5248,17],
            LocationName.MansionFoyerHiPotion           :[5249,18],
            LocationName.MansionFoyerPotion1            :[5250,19],
            LocationName.MansionFoyerPotion2            :[5251,20],
            LocationName.MansionDiningRoomElvenBandanna :[5252,21],
            LocationName.MansionDiningRoomPotion        :[5253,22],
            LocationName.NaminesSketches                :[5254,23],
            LocationName.MansionMap                     :[5255,24],
            LocationName.MansionLibraryHiPotion         :[5256,25],
            LocationName.Axel2                          :[5257,26],
            LocationName.MansionBasementCorridorHiPotion:[5258,27],
            LocationName.RoxasDataMagicBoost            :[5259,28],
        }
    STT_Region = create_region(world, player, active_locations, LocationName.STT_Region,
                                       STT_Region_locations, None)

    TT_Region_locations = {
            LocationName.OldMansionPotion              :[5260,1],
            LocationName.OldMansionMythrilShard        :[5261,2],
            LocationName.TheWoodsPotion                :[5262,3],
            LocationName.TheWoodsMythrilShard          :[5263,4],
            LocationName.TheWoodsHiPotion              :[5264,5],
            LocationName.TramCommonHiPotion            :[5265,6],
            LocationName.TramCommonAPBoost             :[5266,7],
            LocationName.TramCommonTent                :[5267,8],
            LocationName.TramCommonMythrilShard1       :[5268,9],
            LocationName.TramCommonPotion1             :[5269,10],
            LocationName.TramCommonMythrilShard2       :[5270,11],
            LocationName.TramCommonPotion2             :[5271,12],
            LocationName.StationPlazaSecretAnsemReport2:[5272,13],
            LocationName.MunnyPouchMickey              :[5273,14],
            LocationName.CrystalOrb                    :[5274,15],
            LocationName.CentralStationTent            :[5275,16],
            LocationName.TTCentralStationHiPotion      :[5276,17],
            LocationName.CentralStationMythrilShard    :[5277,18],
            LocationName.TheTowerPotion                :[5278,19],
            LocationName.TheTowerHiPotion              :[5279,2],
            LocationName.TheTowerEther                 :[5280,21],
            LocationName.TowerEntrywayEther            :[5281,22],
            LocationName.TowerEntrywayMythrilShard     :[5282,23],
            LocationName.SorcerersLoftTowerMap         :[5283,24],
            LocationName.TowerWardrobeMythrilStone     :[5284,25],
            LocationName.StarSeeker                    :[5285,26],
            LocationName.ValorForm                     :[5286,27],
        }
    TT_Region = create_region(world, player, active_locations, LocationName.TT_Region,
                                       TT_Region_locations, None)
    TT2_Region_locations = {
            LocationName.SeifersTrophy:[5287,1],
            LocationName.Oathkeeper   :[5288,2],
            LocationName.LimitForm    :[5289,3],
        }
    TT2_Region = create_region(world, player, active_locations, LocationName.TT2_Region,
                                       TT2_Region_locations, None)
    TT3_Region_locations = {
            LocationName.UndergroundConcourseMythrilGem       :[5290,1],
            LocationName.UndergroundConcourseAPBoost          :[5291,2],
            LocationName.UndergroundConcourseMythrilCrystal   :[5292,3],
            LocationName.TunnelwayOrichalcum                  :[5293,4],
            LocationName.TunnelwayMythrilCrystal              :[5294,5],
            LocationName.SunsetTerraceOrichalcumPlus          :[5295,6],
            LocationName.SunsetTerraceMythrilShard            :[5296,7],
            LocationName.SunsetTerraceMythrilCrystal          :[5297,8],
            LocationName.SunsetTerraceAPBoost                 :[5298,9],
            LocationName.MansionNobodies                      :[5299,10],
            LocationName.MansionFoyerMythrilCrystal           :[5300,11],
            LocationName.MansionFoyerMythrilStone             :[5301,12],
            LocationName.MansionFoyerSerenityCrystal          :[5302,13],
            LocationName.MansionDiningRoomMythrilCrystal      :[5303,14],
            LocationName.MansionDiningRoomMythrilStone        :[5304,15],
            LocationName.MansionLibraryOrichalcum             :[5305,16],
            LocationName.BeamSecretAnsemReport10              :[5306,17],
            LocationName.MansionBasementCorridorUltimateRecipe:[5307,18],
            LocationName.BetwixtandBetween                    :[5308,19],
            LocationName.BetwixtandBetweenBondofFlame         :[5309,20],
            LocationName.AxelDataMagicBoost                   :[5310,21],
        }
    TT3_Region = create_region(world, player, active_locations, LocationName.TT3_Region,
                                       TT3_Region_locations, None)

    Twtnw_Region_locations = {
            LocationName.FragmentCrossingMythrilStone   :[5311,1],
            LocationName.FragmentCrossingMythrilCrystal :[5312,2],
            LocationName.FragmentCrossingAPBoost        :[5313,3],
            LocationName.FragmentCrossingOrichalcum     :[5314,4],
            LocationName.Roxas                          :[5315,5],
            LocationName.RoxasSecretAnsemReport8        :[5316,6],
            LocationName.TwoBecomeOne                   :[5317,7],
            LocationName.MemorysSkyscaperMythrilCrystal :[5318,8],
            LocationName.MemorysSkyscaperAPBoost        :[5319,9],
            LocationName.MemorysSkyscaperMythrilStone   :[5320,10],
            LocationName.TheBrinkofDespairDarkCityMap   :[5321,11],
            LocationName.TheBrinkofDespairOrichalcumPlus:[5322,12],
            LocationName.NothingsCallMythrilGem         :[5323,13],
            LocationName.NothingsCallOrichalcum         :[5324,14],
            LocationName.TwilightsViewCosmicBelt        :[5325,15],
        }
    Twtnw_Region = create_region(world, player, active_locations, LocationName.Twtnw_Region,
                                       Twtnw_Region_locations, None)
    Twtnw2_Region_locations = {
            LocationName.XigbarBonus                          :[5326,1],
            LocationName.XigbarSecretAnsemReport3             :[5327,2],
            LocationName.NaughtsSkywayMythrilGem              :[5328,3],
            LocationName.NaughtsSkywayOrichalcum              :[5329,4],
            LocationName.NaughtsSkywayMythrilCrystal          :[5330,5],
            LocationName.Oblivion                             :[5331,6],
            LocationName.CastleThatNeverWasMap                :[5332,7],
            LocationName.LuxordBonus                          :[5333,8],
            LocationName.LuxordSecretAnsemReport9             :[5334,9],
            LocationName.SaixBonus                            :[5335,10],
            LocationName.SaixSecretAnsemReport12              :[5336,11],
            LocationName.PreXemnas1SecretAnsemReport11        :[5337,12],
            LocationName.RuinandCreationsPassageMythrilStone  :[5338,13],
            LocationName.RuinandCreationsPassageAPBoost       :[5339,14],
            LocationName.RuinandCreationsPassageMythrilCrystal:[5340,15],
            LocationName.RuinandCreationsPassageOrichalcum    :[5341,16],
            LocationName.Xemnas1Bonus                         :[5342,17],
            LocationName.Xemnas1SecretAnsemReport13           :[5343,18],
            LocationName.FinalXemnas                          :[5344,19],
            LocationName.XemnasDataPowerBoost                 :[5345,20],
        }
    Twtnw2_Region = create_region(world, player, active_locations, LocationName.Twtnw2_Region,
                                       Twtnw2_Region_locations, None)
    Forms_Region_locations={
            LocationName.Valorlvl1 :[5346,1],
            LocationName.Valorlvl2 :[5347,2],
            LocationName.Valorlvl3 :[5348,3],
            LocationName.Valorlvl4 :[5349,4],
            LocationName.Valorlvl5 :[5350,5],
            LocationName.Valorlvl6 :[5351,6],
            LocationName.Valorlvl7 :[5352,7],
            LocationName.Wisdomlvl1:[5353,8],
            LocationName.Wisdomlvl2:[5354,9],
            LocationName.Wisdomlvl3:[5355,10],
            LocationName.Wisdomlvl4:[5356,11],
            LocationName.Wisdomlvl5:[5357,12],
            LocationName.Wisdomlvl6:[5358,13],
            LocationName.Wisdomlvl7:[5359,14],
            LocationName.Limitlvl1 :[5360,15],
            LocationName.Limitlvl2 :[5361,16],
            LocationName.Limitlvl3 :[5362,17],
            LocationName.Limitlvl4 :[5363,18],
            LocationName.Limitlvl5 :[5364,19],
            LocationName.Limitlvl6 :[5365,20],
            LocationName.Limitlvl7 :[5366,21],
            LocationName.Masterlvl1:[5367,22],
            LocationName.Masterlvl2:[5368,23],
            LocationName.Masterlvl3:[5369,24],
            LocationName.Masterlvl4:[5370,25],
            LocationName.Masterlvl5:[5371,26],
            LocationName.Masterlvl6:[5372,27],
            LocationName.Masterlvl7:[5373,28],
            LocationName.Finallvl1 :[5374,29],
            LocationName.Finallvl2 :[5375,30],
            LocationName.Finallvl3 :[5376,31],
            LocationName.Finallvl4 :[5377,32],
            LocationName.Finallvl5 :[5378,33],
            LocationName.Finallvl6 :[5379,34],
            LocationName.Finallvl7 :[5380,35],
        }
    Forms_Region=create_region(world,player,active_locations,LocationName.Form_Region,
                               Forms_Region_locations,None)

    Level_Region_locations={
            LocationName.lvl2 :[5381,1],
            LocationName.lvl4 :[5382,2],
            LocationName.lvl7 :[5383,3],
            LocationName.lvl9 :[5384,4],
            LocationName.lvl10:[5385,5],
            LocationName.lvl12:[5386,6],
            LocationName.lvl14:[5387,7],
            LocationName.lvl15:[5388,8],
            LocationName.lvl17:[5389,9],
            LocationName.lvl20:[5390,10],
            LocationName.lvl23:[5391,11],
            LocationName.lvl25:[5392,12],
            LocationName.lvl28:[5393,13],
            LocationName.lvl30:[5394,14],
            LocationName.lvl32:[5395,15],
            LocationName.lvl34:[5396,16],
            LocationName.lvl36:[5397,17],
            LocationName.lvl39:[5398,18],
            LocationName.lvl41:[5399,19],
            LocationName.lvl44:[5400,20],
            LocationName.lvl46:[5401,21],
            LocationName.lvl48:[5402,22],
            LocationName.lvl50:[5403,23],
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
    HadesCups_Region    ,               
    Bc_Region          ,        
    Bc2_Region         , 
    Sp_Region          ,
    Sp2_Region         ,
    Ht_Region          ,        
    Ht2_Region         ,
    Hb_Region          ,        
    Hb2_Region         ,          
    CoR_Region         ,          
    FirstHalf_Region   ,                
    SecondHalf_Region  ,                
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
    Forms_Region,
    Level_Region,
    ]


def connect_regions (world: MultiWorld, player: int, self):
      #connecting every first visit to the GoA 
      names: typing.Dict[str, int] = {}
      connect(world, player, names, 'Menu', LocationName.GoA_Region)
      connect(world, player, names,LocationName.GoA_Region, LocationName.LoD_Region,
          lambda state: (state.has(ItemName.SwordoftheAncestor, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Oc_Region,
          lambda state: (state.has(ItemName.BattlefieldsofWar, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Ag_Region,
          lambda state: (state.has(ItemName.Scimitar, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Dc_Region,
          lambda state: (state.has(ItemName.CastleKey, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Pr_Region,
          lambda state: (state.has(ItemName.SkillandCrossbones, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Bc_Region,
          lambda state: (state.has(ItemName.BeastsClaw, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Sp_Region,
          lambda state: (state.has(ItemName.IdentityDisk, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Ht_Region,
          lambda state: (state.has(ItemName.BoneFist, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Hb_Region,
          lambda state: (state.has(ItemName.MembershipCard, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Pl_Region,
          lambda state: (state.has(ItemName.ProudFang, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.STT_Region,
          lambda state: (state.has(ItemName.NamineSketches, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.TT_Region,
          lambda state: (state.has(ItemName.Poster, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.Twtnw_Region,
          lambda state: (state.has(ItemName.WaytotheDawn, player)))
      connect(world, player, names,LocationName.GoA_Region, LocationName.HundredAcre1_Region,
          lambda state: (state.has(ItemName.TornPages, player)))
      


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
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)