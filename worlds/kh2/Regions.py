import typing

from BaseClasses import MultiWorld, Region, Entrance

from .Locations import *
from .Names import LocationName, ItemName, RegionName


def create_regions(world, player: int, active_locations):
    KH2REGIONS: typing.Dict[str, typing.List[str]] = {
        "Menu":                           [],
        RegionName.GoA:                   [
            location for locations in
            [GoA_Checks,
             [LocationName.DonaldStarting1,
              LocationName.DonaldStarting2,
              LocationName.GoofyStarting1,
              LocationName.GoofyStarting2]]
            for location in locations
        ],
        RegionName.LoD:                   [
            location for location in LoD_Checks.keys()
        ],
        RegionName.ShanYu:                [
            location for location in Shan_Yu_Checks.keys()
        ],
        RegionName.LoD2:                  [],
        RegionName.AnsemRiku:             [
            location for location in LoD2_Checks.keys()
        ],
        RegionName.StormRider:            [
            location for location in Storm_Rider_Checks.keys()
        ],
        RegionName.DataXigbar:            [
            LocationName.XigbarDataDefenseBoost
        ],
        RegionName.Ag:                    [
           location for location in AG_Checks.keys()
        ],
        RegionName.TwinLords:             [
            location for location in Twin_Lords_Checks.keys()
        ],
        RegionName.Ag2:                   [
            location for location in AG2_Checks.keys()
        ],
        RegionName.GenieJafar:            [
            location for location in Genie_Jafar_Checks.keys()
        ],
        RegionName.DataLexaeus:           [
            LocationName.LexaeusBonus,
            LocationName.LexaeusASStrengthBeyondStrength,
            LocationName.LexaeusDataLostIllusion
        ],
        RegionName.Dc:                    [
            location for location in DC_Checks.keys()
        ],
        RegionName.Tr:                    [
            location for location in TR_Checks.keys()
        ],
        RegionName.OldPete:               [
            location for location in Old_Pete_Checks.keys()
        ],
        RegionName.FuturePete:            [
            location for location in Future_Pete_Checks.keys()
        ],
        RegionName.DataMarluxia:          [
            LocationName.MarluxiaGetBonus,
            LocationName.MarluxiaASEternalBlossom,
            LocationName.MarluxiaDataLostIllusion
        ],
        RegionName.Terra:                 [
            LocationName.LingeringWillBonus,
            LocationName.LingeringWillProofofConnection,
            LocationName.LingeringWillManifestIllusion
        ],
        RegionName.Ha1:                   [
            location for location in HundredAcre1_Checks.keys()
        ],
        RegionName.Ha2:                   [
            location for location in HundredAcre2_Checks.keys()
        ],
        RegionName.Ha3:                   [
            location for location in HundredAcre3_Checks.keys()
        ],
        RegionName.Ha4:                   [
            location for location in HundredAcre4_Checks.keys()
        ],
        RegionName.Ha5:                   [
            location for location in HundredAcre5_Checks.keys()
        ],
        RegionName.Ha6:                   [
            location for location in HundredAcre6_Checks.keys()
        ],
        RegionName.Pr:                    [
            location for location in PR2_Checks.keys()
        ],
        RegionName.Barbosa:               [
            LocationName.Barbossa,
            LocationName.BarbossaGetBonus,
            LocationName.FollowtheWind,
            LocationName.GoofyBarbossa,
            LocationName.GoofyBarbossaGetBonus,
        ],
        RegionName.Pr2:                   [],
        RegionName.GrimReaper1:           [
            location for location in PR2_Checks.keys()
        ],
        RegionName.GrimReaper2:           [
            LocationName.DonaladGrimReaper2,
            LocationName.GrimReaper2,
            LocationName.SecretAnsemReport6,
        ],
        RegionName.DataLuxord:            [
            LocationName.LuxordDataAPBoost
        ],
        RegionName.Oc:                    [
            location for location in Oc_Checks.keys()
        ],
        RegionName.Cerberus:              [
            location for location in Cerberus_Checks.keys()
        ],
        RegionName.OlympusPete:           [
            location for location in Olympus_Pete_Checks.keys()
        ],
        RegionName.Hydra:                 [
            location for location in Hydra_Checks.keys()
        ],
        RegionName.Oc2:                   [
            LocationName.AuronsStatue,
        ],
        RegionName.Hades:                 [
            location for location in Hades_Checks.keys()
        ],
        RegionName.Oc_pain_and_panic_cup: [
            LocationName.ProtectBeltPainandPanicCup,
            LocationName.SerenityGemPainandPanicCup
        ],
        RegionName.Oc_cerberus_cup:       [
            LocationName.RisingDragonCerberusCup,
            LocationName.SerenityCrystalCerberusCup
        ],
        RegionName.Oc2_titan_cup:         [
            LocationName.GenjiShieldTitanCup,
            LocationName.SkillfulRingTitanCup
        ],
        RegionName.Oc2_gof_cup:           [
            LocationName.FatalCrestGoddessofFateCup,
            LocationName.OrichalcumPlusGoddessofFateCup,
        ],
        RegionName.HadesCups:             [
            LocationName.HadesCupTrophyParadoxCups
        ],
        RegionName.DataZexion:            [
            LocationName.ZexionBonus,
            LocationName.ZexionASBookofShadows,
            LocationName.ZexionDataLostIllusion,
            LocationName.GoofyZexion
        ],
        RegionName.Bc:                    [
            location for location in BC_Checks.keys()
        ],
        RegionName.Thresholder:           [
            location for location in Thresholder_Checks.keys()
        ],
        RegionName.Beast:                 [
            location for location in Beast_Checks.keys()
        ],
        RegionName.DarkThorn:             [
            location for location in Dark_Thorn_Checks.keys()
        ],
        RegionName.Bc2:                   [
            location for location in BC2_Checks.keys()
        ],
        RegionName.Xaldin:                [
           location for location in Xaldin_Checks.keys()
        ],
        RegionName.DataXaldin:            [
            LocationName.XaldinDataDefenseBoost
        ],
        RegionName.Sp:                    [
            location for location in SP_Checks.keys()
        ],
        RegionName.HostileProgram:        [
            location for location in Hostile_Program_Checks.keys()
        ],
        RegionName.Sp2:                   [
            location for location in SP2_Checks.keys()
        ],
        RegionName.Mcp:                   [
            location for location in MCP_Checks.keys()
        ],
        RegionName.DataLarxene:           [
            LocationName.LarxeneBonus,
            LocationName.LarxeneASCloakedThunder,
            LocationName.LarxeneDataLostIllusion
        ],
        RegionName.Ht:                    [
            location for location in HT_Checks.keys()
        ],
        RegionName.PrisonKeeper:          [
            location for location in Prison_Keeper_Checks.keys()
        ],
        RegionName.OogieBoogie:           [
            location for location in Oogie_Boogie_Checks.keys()
        ],
        RegionName.Ht2:                   [
            location for location in HT2_Checks.keys()
        ],
        RegionName.Experiment:            [
            location for location in Experiment_Checks.keys()
        ],
        RegionName.DataVexen:             [
            LocationName.VexenBonus,
            LocationName.VexenASRoadtoDiscovery,
            LocationName.VexenDataLostIllusion
        ],
        RegionName.Hb:                    [
            location for location in HB_Checks.keys()
        ],
        RegionName.Hb2:                   [
            location for location in HB2_Checks.keys()
        ],
        RegionName.HBDemyx:               [
            location for location in HB_Demyx_Checks.keys()
        ],
        RegionName.ThousandHeartless:     [
            location for location in Thousand_Heartless_Checks.keys()
        ],
        RegionName.DataDemyx:             [
            LocationName.DemyxDataAPBoost
        ],
        RegionName.Mushroom13:            [
            LocationName.WinnersProof,
            LocationName.ProofofPeace
        ],
        RegionName.Sephi:                 [
            LocationName.SephirothBonus,
            LocationName.SephirothFenrir
        ],
        RegionName.CoR:                   [
            location for location in CoR_Checks.keys()
        ],
        RegionName.CorFirstFight:         [
            location for location in CoR_First_Fight_Checks.keys()
        ],
        RegionName.CorSecondFight:        [
            location for location in CoR_Second_Fight_Checks
        ],
        RegionName.Transport:             [
            location for location in Transport_Checks.keys()
        ],
        RegionName.Pl:                    [
            location for location in PL_Checks.keys()
        ],
        RegionName.Scar:                  [
            location for location in Scar_Checks.keys()
        ],
        RegionName.Pl2:                   [
            location for location in PL2_Checks.keys()
        ],
        RegionName.GroundShaker:          [
            location for location in Groundshaker_Checks.keys()
        ],
        RegionName.DataSaix:              [
            LocationName.SaixDataDefenseBoost,
        ],
        RegionName.Stt:                   [
            location for location in STT_Checks.keys()
        ],
        RegionName.TwilightThorn:         [
            LocationName.TwilightThorn,
        ],
        RegionName.Axel1:                 [
            location for location in Axel1_Checks.keys()
        ],
        RegionName.Axel2:                 [
            location for location in Axel2_Checks.keys()
        ],
        RegionName.DataRoxas:             [
            LocationName.RoxasDataMagicBoost
        ],
        RegionName.Tt:                    [
            location for location in TT_Checks.keys()
        ],
        RegionName.Tt2:                   [
            location for location in TT2_Checks.keys()
        ],
        RegionName.Tt3:                   [
            location for location in TT3_Checks.keys()
        ],
        RegionName.DataAxel:              [
            LocationName.AxelDataMagicBoost,
        ],
        RegionName.Twtnw:                 [
            location for location in TWTNW_Checks.keys()
        ],
        RegionName.Roxas:                 [
            location for location in Roxas_Checks.keys()
        ],
        RegionName.Xigbar:                [
            location for location in Xigbar_Checks.keys()
        ],
        RegionName.Luxord:                [
            location for location in Luxord_Checks.keys()
        ],
        RegionName.Saix:                  [
            location for location in Saix_Checks.keys()
        ],
        RegionName.Twtnw2:                [
            location for location in TWTNW2_Checks.keys()
        ],
        RegionName.Xemnas:                [
            location for location in Xemnas_Checks.keys()
        ],
        RegionName.ArmoredXemnas:         [],
        RegionName.ArmoredXemnas2:        [],
        RegionName.FinalXemnas:           [
            LocationName.FinalXemnas
        ],
        RegionName.DataXemnas:            [
            LocationName.XemnasDataPowerBoost
        ],
        RegionName.Valor:                 [
            LocationName.Valorlvl2,
            LocationName.Valorlvl3,
            LocationName.Valorlvl4,
            LocationName.Valorlvl5,
            LocationName.Valorlvl6,
            LocationName.Valorlvl7
        ],
        RegionName.Wisdom:                [
            LocationName.Wisdomlvl2,
            LocationName.Wisdomlvl3,
            LocationName.Wisdomlvl4,
            LocationName.Wisdomlvl5,
            LocationName.Wisdomlvl6,
            LocationName.Wisdomlvl7
        ],
        RegionName.Limit:                 [
            LocationName.Limitlvl2,
            LocationName.Limitlvl3,
            LocationName.Limitlvl4,
            LocationName.Limitlvl5,
            LocationName.Limitlvl6,
            LocationName.Limitlvl7
        ],
        RegionName.Master:                [
            LocationName.Masterlvl2,
            LocationName.Masterlvl3,
            LocationName.Masterlvl4,
            LocationName.Masterlvl5,
            LocationName.Masterlvl6,
            LocationName.Masterlvl7
        ],
        RegionName.Final:                 [
            LocationName.Finallvl2,
            LocationName.Finallvl3,
            LocationName.Finallvl4,
            LocationName.Finallvl5,
            LocationName.Finallvl6,
            LocationName.Finallvl7
        ],
        RegionName.Keyblade:              [
            location for weapon in [Keyblade_Slots.keys(),
                                    Donald_Checks.keys(),
                                    Goofy_Checks.keys()]
            for location in weapon

        ],
        RegionName.LevelsVS1:             [],
        RegionName.LevelsVS3:             [],
        RegionName.LevelsVS6:             [],
        RegionName.LevelsVS9:             [],
        RegionName.LevelsVS12:            [],
        RegionName.LevelsVS15:            [],
        RegionName.LevelsVS18:            [],
        RegionName.LevelsVS21:            [],
        RegionName.LevelsVS24:            [],
        RegionName.LevelsVS26:            [],

    }
    # Level region depends on level depth.
    # for every 5 levels there should be +3 visit locking

    # level 50
    if world.LevelDepth[player] == "level_50":
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
    elif world.LevelDepth[player] == "level_99":
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
    elif world.LevelDepth[player] in ["level_50_sanity", "level_99_sanity"]:
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
        if world.LevelDepth[player] == "level_99_sanity":
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
                                                 LocationName.Lvl98,
                                                 LocationName.Lvl99]

    for region, locations in KH2REGIONS.items():
        world.regions += [create_region(world, player, active_locations, region, locations)]


def connect_regions(world: MultiWorld, player: int):
    # connecting every first visit to the GoA
    KH2RegionConnections: typing.Dict[str, typing.Set[str]] = {
        "Menu":                       {RegionName.GoA},
        RegionName.GoA:               {RegionName.Sp, RegionName.Pr, RegionName.Tt, RegionName.Oc, RegionName.Ht,
                                       RegionName.LoD,
                                       RegionName.Twtnw, RegionName.Bc, RegionName.Ag, RegionName.Pl, RegionName.Hb,
                                       RegionName.Dc, RegionName.Stt,
                                       RegionName.Ha1, RegionName.Keyblade, RegionName.LevelsVS1,
                                       RegionName.Valor, RegionName.Wisdom, RegionName.Limit, RegionName.Master,
                                       RegionName.Final},
        RegionName.LoD:               {RegionName.ShanYu},
        RegionName.ShanYu:            {RegionName.LoD2},
        RegionName.LoD2:              {RegionName.AnsemRiku},
        RegionName.AnsemRiku:         {RegionName.StormRider},
        RegionName.StormRider:        {RegionName.DataXigbar},
        RegionName.Ag:                {RegionName.TwinLords},
        RegionName.TwinLords:         {RegionName.Ag2},
        RegionName.Ag2:               {RegionName.GenieJafar},
        RegionName.GenieJafar:        {RegionName.DataLexaeus},
        RegionName.Dc:                {RegionName.Tr},
        RegionName.Tr:                {RegionName.OldPete},
        RegionName.OldPete:           {RegionName.FuturePete},
        RegionName.FuturePete:        {RegionName.Terra, RegionName.DataMarluxia},
        RegionName.Ha1:               {RegionName.Ha2},
        RegionName.Ha2:               {RegionName.Ha3},
        RegionName.Ha3:               {RegionName.Ha4},
        RegionName.Ha4:               {RegionName.Ha5},
        RegionName.Ha5:               {RegionName.Ha6},
        RegionName.Pr:                {RegionName.Barbosa},
        RegionName.Barbosa:           {RegionName.Pr2},
        RegionName.Pr2:               {RegionName.GrimReaper1},
        RegionName.GrimReaper1:       {RegionName.GrimReaper2},
        RegionName.GrimReaper2:       {RegionName.DataLuxord},
        RegionName.Oc:                {RegionName.Cerberus},
        RegionName.Cerberus:          {RegionName.OlympusPete},
        RegionName.OlympusPete:       {RegionName.Hydra},
        RegionName.Hydra:             {RegionName.Oc_pain_and_panic_cup, RegionName.Oc_cerberus_cup, RegionName.Oc2},
        RegionName.Oc2:               {RegionName.Hades},
        RegionName.Hades:             {RegionName.Oc2_titan_cup, RegionName.Oc2_gof_cup, RegionName.DataZexion},
        RegionName.Oc2_gof_cup:       {RegionName.HadesCups},
        RegionName.Bc:                {RegionName.Thresholder},
        RegionName.Thresholder:       {RegionName.Beast},
        RegionName.Beast:             {RegionName.DarkThorn},
        RegionName.DarkThorn:         {RegionName.Bc2},
        RegionName.Bc2:               {RegionName.Xaldin},
        RegionName.Xaldin:            {RegionName.DataXaldin},
        RegionName.Sp:                {RegionName.HostileProgram},
        RegionName.HostileProgram:    {RegionName.Sp2},
        RegionName.Sp2:               {RegionName.Mcp},
        RegionName.Mcp:               {RegionName.DataLarxene},
        RegionName.Ht:                {RegionName.PrisonKeeper},
        RegionName.PrisonKeeper:      {RegionName.OogieBoogie},
        RegionName.OogieBoogie:       {RegionName.Ht2},
        RegionName.Ht2:               {RegionName.Experiment},
        RegionName.Experiment:        {RegionName.DataVexen},
        RegionName.Hb:                {RegionName.Hb2},
        RegionName.Hb2:               {RegionName.CoR, RegionName.HBDemyx},
        RegionName.HBDemyx:           {RegionName.ThousandHeartless},
        RegionName.ThousandHeartless: {RegionName.Mushroom13, RegionName.DataDemyx, RegionName.Sephi},
        RegionName.CoR:               {RegionName.CorFirstFight},
        RegionName.CorFirstFight:     {RegionName.CorSecondFight},
        RegionName.CorSecondFight:    {RegionName.Transport},
        RegionName.Pl:                {RegionName.Scar},
        RegionName.Scar:              {RegionName.Pl2},
        RegionName.Pl2:               {RegionName.GroundShaker},
        RegionName.GroundShaker:      {RegionName.DataSaix},
        RegionName.Stt:               {RegionName.TwilightThorn},
        RegionName.TwilightThorn:     {RegionName.Axel1},
        RegionName.Axel1:             {RegionName.Axel2},
        RegionName.Axel2:             {RegionName.DataRoxas},
        RegionName.Tt:                {RegionName.Tt2},
        RegionName.Tt2:               {RegionName.Tt3},
        RegionName.Tt3:               {RegionName.DataAxel},
        RegionName.Twtnw:             {RegionName.Roxas},
        RegionName.Roxas:             {RegionName.Xigbar},
        RegionName.Xigbar:            {RegionName.Luxord},
        RegionName.Luxord:            {RegionName.Saix},
        RegionName.Saix:              {RegionName.Twtnw2},
        RegionName.Twtnw2:            {RegionName.Xemnas},
        RegionName.Xemnas:            {RegionName.ArmoredXemnas, RegionName.DataXemnas},
        RegionName.ArmoredXemnas:     {RegionName.ArmoredXemnas2},
        RegionName.ArmoredXemnas2:    {RegionName.FinalXemnas},
        RegionName.LevelsVS1:         {RegionName.LevelsVS3},
        RegionName.LevelsVS3:         {RegionName.LevelsVS6},
        RegionName.LevelsVS6:         {RegionName.LevelsVS9},
        RegionName.LevelsVS9:         {RegionName.LevelsVS12},
        RegionName.LevelsVS12:        {RegionName.LevelsVS15},
        RegionName.LevelsVS15:        {RegionName.LevelsVS18},
        RegionName.LevelsVS18:        {RegionName.LevelsVS21},
        RegionName.LevelsVS21:        {RegionName.LevelsVS24},
        RegionName.LevelsVS24:        {RegionName.LevelsVS26},
    }

    names: typing.Dict[str, int] = {}
    for source, target in KH2RegionConnections.items():
        for region in target:
            connect(world, player, names, source, region)


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
                location = KH2Location(player, location, loc_id, ret)
                ret.locations.append(location)

    return ret
