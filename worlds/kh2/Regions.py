import typing

from BaseClasses import Region

from . import Locations, RegionLocations
from .Subclasses import KH2Location
from .Names import LocationName, RegionName

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
puzzle_region_list = [
    RegionName.Tt1PuzzlePieces,
    RegionName.Tt2PuzzlePieces,
    RegionName.Tt3PuzzlePieces,
    RegionName.Hb1PuzzlePieces,
    RegionName.Hb2PuzzlePieces,
    RegionName.PostThousandHeartless,
    RegionName.CoRFirstFightPuzzlePieces,
    RegionName.CorSecondFightPuzzlePieces,
    RegionName.LoD1PuzzlePieces,
    RegionName.LoD2PuzzlePieces,
    RegionName.PostStormRiderPuzzlePieces,
    RegionName.Bc1PuzzlePieces,
    RegionName.Bc2PuzzlePieces,
    RegionName.Oc1PuzzlePieces,
    RegionName.DcPuzzlePieces,
    RegionName.TrPuzzlePieces,
    RegionName.Pr1PuzzlePieces,
    RegionName.Pr2PuzzlePieces,
    RegionName.Ag1PuzzlePieces,
    RegionName.Ag2PuzzlePieces,
    RegionName.Ht1PuzzlePieces,
    RegionName.PrisonKeeperPuzzlePieces,
    RegionName.OogieBoogiePuzzlePieces,
    RegionName.Pl1PuzzlePieces,
    RegionName.Sp1PuzzlePieces,
    RegionName.Sp2PuzzlePieces,
    RegionName.TwtnwPuzzlePostRoxas,
    RegionName.TwtnwPuzzlePostXigbar,
    RegionName.Twtnw3PuzzlePieces,
    RegionName.PoohsPuzzlePieces,
    RegionName.PigletsPuzzlePieces,
    RegionName.RabbitsPuzzlePieces,
    RegionName.KangasPuzzlePieces,
    RegionName.SpookyCavePuzzlePieces,
    RegionName.StarryHillPuzzlePieces,
    RegionName.At1PuzzlePieces,
    RegionName.PuzzleRegion,
]

KH2REGIONS: typing.Dict[str, list] = {
    "Menu":                        [],
    RegionName.GoA:                RegionLocations.GoALocations,
    RegionName.LoD:                RegionLocations.LoD1Locations,
    RegionName.ShanYu:             RegionLocations.ShanYuLocations,
    RegionName.LoD2:               RegionLocations.LoD2Locations,
    RegionName.AnsemRiku:          RegionLocations.AnsemRikuLocations,
    RegionName.StormRider:         RegionLocations.StormRiderLocations,
    RegionName.DataXigbar:         RegionLocations.DataXigbarLocations,
    RegionName.Ag:                 RegionLocations.Ag1Locations,
    RegionName.TwinLords:          RegionLocations.TwinLordsLocations,
    RegionName.Ag2:                RegionLocations.Ag2Locations,
    RegionName.GenieJafar:         RegionLocations.GenieJafarLocations,
    RegionName.DataLexaeus:        RegionLocations.DataLexaeusLocations,
    RegionName.Dc:                 RegionLocations.DcLocations,
    RegionName.Tr:                 RegionLocations.TrLocations,
    RegionName.OldPete:            RegionLocations.OldPeteLocations,
    RegionName.FuturePete:         RegionLocations.FuturePeteLocations,
    RegionName.DataMarluxia:       RegionLocations.DataMarluxiaLocations,
    RegionName.Terra:              RegionLocations.TerraLocations,
    RegionName.Ha1:                RegionLocations.Ha1Locations,
    RegionName.Ha2:                RegionLocations.Ha2Locations,
    RegionName.Ha3:                RegionLocations.Ha3Locations,
    RegionName.Ha4:                RegionLocations.Ha4Locations,
    RegionName.Ha5:                RegionLocations.Ha5Locations,
    RegionName.Ha6:                RegionLocations.Ha6Locations,
    RegionName.Pr:                 RegionLocations.Pr1Locations,
    RegionName.Barbosa:            RegionLocations.BarbosaLocations,
    RegionName.Pr2:                RegionLocations.Pr2Locations,
    RegionName.GrimReaper1:        RegionLocations.GrimReaper1Locations,
    RegionName.GrimReaper2:        RegionLocations.GrimReaper2Locations,
    RegionName.DataLuxord:         RegionLocations.DataLuxordLocations,
    RegionName.Oc:                 RegionLocations.Oc1Locations,
    RegionName.Cerberus:           RegionLocations.CerberusLocations,
    RegionName.OlympusPete:        RegionLocations.OlympusPeteLocations,
    RegionName.Hydra:              RegionLocations.HydraLocations,
    RegionName.Oc2:                RegionLocations.Oc2Locations,
    RegionName.Hades:              RegionLocations.HadesLocations,
    RegionName.OcPainAndPanicCup:  RegionLocations.OcPainAndPanicCupLocations,
    RegionName.OcCerberusCup:      RegionLocations.OcCerberusCupLocations,
    RegionName.Oc2TitanCup:        RegionLocations.Oc2TitanCupLocations,
    RegionName.Oc2GofCup:          RegionLocations.Oc2GofCupLocations,
    RegionName.HadesCups:          RegionLocations.HadesCupsLocations,
    RegionName.DataZexion:         RegionLocations.DataZexionLocations,
    RegionName.Bc:                 RegionLocations.Bc1Locations,
    RegionName.Thresholder:        RegionLocations.ThresholderLocations,
    RegionName.Beast:              RegionLocations.BeastLocations,
    RegionName.DarkThorn:          RegionLocations.DarkThornLocations,
    RegionName.Bc2:                RegionLocations.Bc2Locations,
    RegionName.Xaldin:             RegionLocations.XaldinLocations,
    RegionName.DataXaldin:         RegionLocations.DataXaldinLocations,
    RegionName.Sp:                 RegionLocations.Sp1Locations,
    RegionName.HostileProgram:     RegionLocations.HostileProgramLocations,
    RegionName.Sp2:                RegionLocations.Sp2Locations,
    RegionName.Mcp:                RegionLocations.McpLocations,
    RegionName.DataLarxene:        RegionLocations.DataLarxeneLocations,
    RegionName.Ht:                 RegionLocations.Ht1Locations,
    RegionName.PrisonKeeper:       RegionLocations.PrisonKeeperLocations,
    RegionName.OogieBoogie:        RegionLocations.OogieBoogieLocations,
    RegionName.Ht2:                RegionLocations.Ht2Locations,
    RegionName.Experiment:         RegionLocations.ExperimentLocations,
    RegionName.DataVexen:          RegionLocations.DataVexenLocations,
    RegionName.Hb:                 RegionLocations.Hb1Locations,
    RegionName.Hb2:                RegionLocations.Hb2Locations,
    RegionName.HBDemyx:            RegionLocations.HBDemyxLocations,
    RegionName.ThousandHeartless:  RegionLocations.ThousandHeartlessLocations,
    RegionName.DataDemyx:          RegionLocations.DataDemyxLocations,
    RegionName.Mushroom13:         RegionLocations.Mushroom13Locations,
    RegionName.Sephi:              RegionLocations.SephiLocations,
    RegionName.CoR:                RegionLocations.CoRLocations,
    RegionName.CorFirstFight:      RegionLocations.CorFirstFightLocations,
    RegionName.CorSecondFight:     RegionLocations.CorSecondFightLocations,
    RegionName.Transport:          RegionLocations.TransportLocations,
    RegionName.Pl:                 RegionLocations.Pl1Locations,
    RegionName.Scar:               RegionLocations.ScarLocations,
    RegionName.Pl2:                RegionLocations.Pl2Locations,
    RegionName.GroundShaker:       RegionLocations.GroundShakerLocations,
    RegionName.DataSaix:           RegionLocations.DataSaixLocations,
    RegionName.Stt:                RegionLocations.SttLocations,
    RegionName.TwilightThorn:      RegionLocations.TwilightThornLocations,
    RegionName.Axel1:              RegionLocations.Axel1Locations,
    RegionName.Axel2:              RegionLocations.Axel2Locations,
    RegionName.DataRoxas:          RegionLocations.DataRoxasLocations,
    RegionName.Tt:                 RegionLocations.Tt1Locations,
    RegionName.Tt2:                RegionLocations.Tt2Locations,
    RegionName.Tt3:                RegionLocations.Tt3Locations,
    RegionName.DataAxel:           RegionLocations.DataAxelLocations,
    RegionName.Twtnw:              RegionLocations.TwtnwLocations,
    RegionName.Roxas:              RegionLocations.RoxasLocations,
    RegionName.Xigbar:             RegionLocations.XigbarLocations,
    RegionName.Luxord:             RegionLocations.LuxordLocations,
    RegionName.Saix:               RegionLocations.SaixLocations,
    RegionName.Twtnw2:             RegionLocations.Twtnw2Locations,
    RegionName.Xemnas:             RegionLocations.XemnasLocations,
    RegionName.ArmoredXemnas:      RegionLocations.ArmoredXemnasLocations,
    RegionName.ArmoredXemnas2:     RegionLocations.ArmoredXemnas2Locations,
    RegionName.FinalXemnas:        RegionLocations.FinalXemnasLocations,
    RegionName.DataXemnas:         RegionLocations.DataXemnasLocations,
    RegionName.AtlanticaSongOne:   RegionLocations.AtlanticaSongOneLocations,
    RegionName.AtlanticaSongTwo:   RegionLocations.AtlanticaSongTwoLocations,
    RegionName.AtlanticaSongThree: RegionLocations.AtlanticaSongThreeLocations,
    RegionName.AtlanticaSongFour:  RegionLocations.AtlanticaSongFourLocations,
    RegionName.Valor:              RegionLocations.ValorLocations,
    RegionName.Wisdom:             RegionLocations.WisdomLocations,
    RegionName.Limit:              RegionLocations.LimitLocations,
    RegionName.Master:             RegionLocations.MasterLocations,
    RegionName.Final:              RegionLocations.FinalLocations,
    RegionName.Keyblade:           RegionLocations.KeybladeLocations,
}


def create_regions(self):
    # Level region depends on level depth.
    # for every 5 levels there should be +3 visit locking
    # level 50
    multiworld = self.multiworld
    player = self.player
    active_locations = self.location_name_to_id

    for level_region_name in level_region_list:
        KH2REGIONS[level_region_name] = []

    for puzzle_region_name in puzzle_region_list:
        KH2REGIONS[puzzle_region_name] = []

    if multiworld.LevelDepth[player] == "level_50":
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
    elif multiworld.LevelDepth[player] == "level_99":
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
    elif multiworld.LevelDepth[player] in ["level_50_sanity", "level_99_sanity"]:
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
        if multiworld.LevelDepth[player] == "level_99_sanity":
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
    if multiworld.SummonLevelLocationToggle[player]:
        KH2REGIONS[RegionName.Summon] = RegionLocations.SummonRegionLocations

    if self.options.PuzzlePiecesLocationToggle:
        KH2REGIONS[RegionName.Tt1PuzzlePieces] = RegionLocations.Tt1PuzzlePiecesLocations
        KH2REGIONS[RegionName.Tt2PuzzlePieces] = RegionLocations.Tt2PuzzlePiecesLocations
        KH2REGIONS[RegionName.Tt3PuzzlePieces] = RegionLocations.Tt3PuzzlePiecesLocations
        KH2REGIONS[RegionName.Hb1PuzzlePieces] = RegionLocations.Hb1PuzzlePiecesLocations
        KH2REGIONS[RegionName.Hb2PuzzlePieces] = RegionLocations.Hb2PuzzlePiecesLocations
        KH2REGIONS[RegionName.PostThousandHeartless] = RegionLocations.PostThousandHeartlessPuzzlePiecesLocations
        KH2REGIONS[RegionName.CoRFirstFightPuzzlePieces] = RegionLocations.CoRFirstFightPuzzlePiecesLocations
        KH2REGIONS[RegionName.CorSecondFightPuzzlePieces] = RegionLocations.CorSecondFightPuzzlePiecesLocations
        KH2REGIONS[RegionName.LoD1PuzzlePieces] = RegionLocations.LoD1PuzzlePiecesLocations
        KH2REGIONS[RegionName.LoD2PuzzlePieces] = RegionLocations.LoD2PuzzlePiecesLocations
        KH2REGIONS[RegionName.PostStormRiderPuzzlePieces] = RegionLocations.PostStormRiderPuzzlePiecesLocations
        KH2REGIONS[RegionName.Bc1PuzzlePieces] = RegionLocations.Bc1PuzzlePiecesLocations
        KH2REGIONS[RegionName.Bc2PuzzlePieces] = RegionLocations.Bc2PuzzlePiecesLocations
        KH2REGIONS[RegionName.Oc1PuzzlePieces] = RegionLocations.Oc1PuzzlePiecesLocations
        KH2REGIONS[RegionName.DcPuzzlePieces] = RegionLocations.DcPuzzlePiecesLocations
        KH2REGIONS[RegionName.TrPuzzlePieces] = RegionLocations.TrPuzzlePiecesLocations
        KH2REGIONS[RegionName.Pr1PuzzlePieces] = RegionLocations.Pr1PuzzlePiecesLocations
        KH2REGIONS[RegionName.Pr2PuzzlePieces] = RegionLocations.Pr2PuzzlePiecesLocations
        KH2REGIONS[RegionName.Ag1PuzzlePieces] = RegionLocations.Ag1PuzzlePiecesLocations
        KH2REGIONS[RegionName.Ag2PuzzlePieces] = RegionLocations.Ag2PuzzlePiecesLocations
        KH2REGIONS[RegionName.Ht1PuzzlePieces] = RegionLocations.Ht1PuzzlePiecesLocations
        KH2REGIONS[RegionName.PrisonKeeperPuzzlePieces] = RegionLocations.PrisonKeeperPuzzlePiecesLocations
        KH2REGIONS[RegionName.OogieBoogiePuzzlePieces] = RegionLocations.OogieBoogiePuzzlePiecesLocations
        KH2REGIONS[RegionName.Pl1PuzzlePieces] = RegionLocations.Pl1PuzzlePiecesLocations
        KH2REGIONS[RegionName.Sp1PuzzlePieces] = RegionLocations.Sp1PuzzlePiecesLocations
        KH2REGIONS[RegionName.Sp2PuzzlePieces] = RegionLocations.Sp2PuzzlePiecesLocations
        KH2REGIONS[RegionName.TwtnwPuzzlePostRoxas] = RegionLocations.TwtnwPuzzlePostRoxasLocations
        KH2REGIONS[RegionName.TwtnwPuzzlePostXigbar] = RegionLocations.TwtnwPuzzlePostXigbarLocations
        KH2REGIONS[RegionName.Twtnw3PuzzlePieces] = RegionLocations.Twtnw3PuzzlePiecesLocations
        KH2REGIONS[RegionName.PoohsPuzzlePieces] = RegionLocations.PoohsPuzzlePiecesLocations
        KH2REGIONS[RegionName.PigletsPuzzlePieces] = RegionLocations.PigletsPuzzlePiecesLocations
        KH2REGIONS[RegionName.RabbitsPuzzlePieces] = RegionLocations.RabbitsPuzzlePiecesLocations
        KH2REGIONS[RegionName.KangasPuzzlePieces] = RegionLocations.KangasPuzzlePiecesLocations
        KH2REGIONS[RegionName.SpookyCavePuzzlePieces] = RegionLocations.SpookyCavePuzzlePiecesLocations
        KH2REGIONS[RegionName.StarryHillPuzzlePieces] = RegionLocations.StarryHillPuzzlePiecesLocations
        if self.options.AtlanticaToggle:
            KH2REGIONS[RegionName.At1PuzzlePieces] = RegionLocations.At1PuzzlePiecesLocations
    # for region_name in [Heart_Checks.keys(), Duality_Checks.keys(), Frontier_Checks.keys(), Sunset_Checks.keys(), Daylight_Checks.keys()]:
    #    for location in region_name:
    #        KH2REGIONS[RegionName.PuzzlePieces].append(location)

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
                                        RegionName.Final, RegionName.Summon, RegionName.AtlanticaSongOne, RegionName.PuzzleRegion},
        RegionName.LoD:                {RegionName.LoD1PuzzlePieces, RegionName.ShanYu},
        RegionName.ShanYu:             {RegionName.LoD2},
        RegionName.LoD2:               {RegionName.AnsemRiku},
        RegionName.AnsemRiku:          {RegionName.LoD2PuzzlePieces, RegionName.StormRider},
        RegionName.StormRider:         {RegionName.PostStormRiderPuzzlePieces, RegionName.DataXigbar},
        RegionName.Ag:                 {RegionName.Ag1PuzzlePieces, RegionName.TwinLords},
        RegionName.TwinLords:          {RegionName.Ag2},
        RegionName.Ag2:                {RegionName.Ag2PuzzlePieces, RegionName.GenieJafar},
        RegionName.GenieJafar:         {RegionName.DataLexaeus},
        RegionName.Dc:                 {RegionName.DcPuzzlePieces, RegionName.Tr},
        RegionName.Tr:                 {RegionName.TrPuzzlePieces, RegionName.OldPete},
        RegionName.OldPete:            {RegionName.FuturePete},
        RegionName.FuturePete:         {RegionName.Terra, RegionName.DataMarluxia},
        RegionName.Ha1:                {RegionName.PoohsPuzzlePieces, RegionName.Ha2},
        RegionName.Ha2:                {RegionName.PigletsPuzzlePieces, RegionName.Ha3},
        RegionName.Ha3:                {RegionName.RabbitsPuzzlePieces, RegionName.Ha4},
        RegionName.Ha4:                {RegionName.KangasPuzzlePieces, RegionName.Ha5},
        RegionName.Ha5:                {RegionName.SpookyCavePuzzlePieces, RegionName.Ha6},
        RegionName.Ha6:                {RegionName.StarryHillPuzzlePieces},
        RegionName.Pr:                 {RegionName.Pr1PuzzlePieces, RegionName.Barbosa},
        RegionName.Barbosa:            {RegionName.Pr2},
        RegionName.Pr2:                {RegionName.Pr2PuzzlePieces, RegionName.GrimReaper1},
        RegionName.GrimReaper1:        {RegionName.GrimReaper2},
        RegionName.GrimReaper2:        {RegionName.DataLuxord},
        RegionName.Oc:                 {RegionName.Cerberus},
        RegionName.Cerberus:           {RegionName.Oc1PuzzlePieces, RegionName.OlympusPete},
        RegionName.OlympusPete:        {RegionName.Hydra},
        RegionName.Hydra:              {RegionName.OcPainAndPanicCup, RegionName.OcCerberusCup, RegionName.Oc2},
        RegionName.Oc2:                {RegionName.Hades},
        RegionName.Hades:              {RegionName.Oc2TitanCup, RegionName.Oc2GofCup, RegionName.DataZexion},
        RegionName.Oc2GofCup:          {RegionName.HadesCups},
        RegionName.Bc:                 {RegionName.Thresholder},
        RegionName.Thresholder:        {RegionName.Bc1PuzzlePieces, RegionName.Beast},
        RegionName.Beast:              {RegionName.DarkThorn},
        RegionName.DarkThorn:          {RegionName.Bc2},
        RegionName.Bc2:                {RegionName.Xaldin},
        RegionName.Xaldin:             {RegionName.Bc2PuzzlePieces, RegionName.DataXaldin},
        RegionName.Sp:                 {RegionName.Sp1PuzzlePieces, RegionName.HostileProgram},
        RegionName.HostileProgram:     {RegionName.Sp2},
        RegionName.Sp2:                {RegionName.Sp2PuzzlePieces, RegionName.Mcp},
        RegionName.Mcp:                {RegionName.DataLarxene},
        RegionName.Ht:                 {RegionName.Ht1PuzzlePieces, RegionName.PrisonKeeper},
        RegionName.PrisonKeeper:       {RegionName.PrisonKeeperPuzzlePieces, RegionName.OogieBoogie},
        RegionName.OogieBoogie:        {RegionName.OogieBoogiePuzzlePieces, RegionName.Ht2},
        RegionName.Ht2:                {RegionName.Experiment},
        RegionName.Experiment:         {RegionName.DataVexen},
        RegionName.Hb:                 {RegionName.Hb1PuzzlePieces, RegionName.Hb2},
        RegionName.Hb2:                {RegionName.Hb2PuzzlePieces, RegionName.CoR, RegionName.HBDemyx},
        RegionName.HBDemyx:            {RegionName.ThousandHeartless},
        RegionName.ThousandHeartless:  {RegionName.PostThousandHeartless, RegionName.Mushroom13, RegionName.DataDemyx, RegionName.Sephi},
        RegionName.CoR:                {RegionName.CorFirstFight},
        RegionName.CorFirstFight:      {RegionName.CoRFirstFightPuzzlePieces, RegionName.CorSecondFight},
        RegionName.CorSecondFight:     {RegionName.CorSecondFightPuzzlePieces, RegionName.Transport},
        RegionName.Pl:                 {RegionName.Pl1PuzzlePieces, RegionName.Scar},
        RegionName.Scar:               {RegionName.Pl2},
        RegionName.Pl2:                {RegionName.GroundShaker},
        RegionName.GroundShaker:       {RegionName.DataSaix},
        RegionName.Stt:                {RegionName.TwilightThorn},
        RegionName.TwilightThorn:      {RegionName.Axel1},
        RegionName.Axel1:              {RegionName.Axel2},
        RegionName.Axel2:              {RegionName.DataRoxas},
        RegionName.Tt:                 {RegionName.Tt1PuzzlePieces, RegionName.Tt2},
        RegionName.Tt2:                {RegionName.Tt2PuzzlePieces, RegionName.Tt3},
        RegionName.Tt3:                {RegionName.Tt3PuzzlePieces, RegionName.DataAxel},
        RegionName.Twtnw:              {RegionName.Roxas},
        RegionName.Roxas:              {RegionName.TwtnwPuzzlePostRoxas, RegionName.Xigbar},
        RegionName.Xigbar:             {RegionName.TwtnwPuzzlePostXigbar, RegionName.Luxord},
        RegionName.Luxord:             {RegionName.Saix},
        RegionName.Saix:               {RegionName.Twtnw2},
        RegionName.Twtnw2:             {RegionName.Twtnw3PuzzlePieces, RegionName.Xemnas},
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
        RegionName.AtlanticaSongOne:   {RegionName.At1PuzzlePieces, RegionName.AtlanticaSongTwo},
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
