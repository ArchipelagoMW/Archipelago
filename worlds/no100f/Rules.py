import typing
from typing import Callable, Dict, List, Tuple

from BaseClasses import MultiWorld, CollectionState, Entrance
from .Options import NO100FOptions
from .names import ConnectionNames, ItemNames, LocationNames, RegionNames
from worlds.generic.Rules import set_rule, add_rule, CollectionRule


upgrade_rules = [
    # connections
    {
        # Hub

        # Manor
        ConnectionNames.i020_i021: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.i003_b004: lambda player: lambda state: state.has(ItemNames.SoapPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.i004_o001: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
        ConnectionNames.i006_r001: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.i004_i003: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

        # Rooftops
        ConnectionNames.r021_r020: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

        # Balcony
        ConnectionNames.o001_o008: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.o002_o003: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.o001_r005: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.ProgressiveJump, player, 1),

        # Hedge
        ConnectionNames.e004_e005: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.e006_e005: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.e009_c001: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
        ConnectionNames.e009_e001: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

        # Fishing Village
        ConnectionNames.f003_f004: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.f003_p001: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
        ConnectionNames.f008_l011: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.f009_f008: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),

        # Graveyard
        ConnectionNames.g002_g003: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.g003_g004: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),

        # Coast
        ConnectionNames.c001_c002: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.c004_c003: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.c006_c007: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.c007_g001: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
        # ConnectionNames.c005_c006: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),

        # Passage
        ConnectionNames.p001_p002: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
        ConnectionNames.p005_p001: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) or state.has(ItemNames.ProgressiveJump, player, 2),

        # Secret Lab
        ConnectionNames.s001_s002: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.s002_s004: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),

        # Basement
        ConnectionNames.b001_b002: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1),

        # Lighthouse
        ConnectionNames.l017_l018: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
        ConnectionNames.l015_l017: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.l015_w020: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
        ConnectionNames.l014_l013: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.l015_l019: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),

        # Wrecked Ships
        ConnectionNames.w020_w021: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.w022_w021: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 2),
        ConnectionNames.w022_w023: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
        ConnectionNames.w025_w026: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
        ConnectionNames.w026_w028: lambda player: lambda state: state.has(ItemNames.ShockwavePower, player, 2),
        ConnectionNames.w026_w020: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
    },
    # locations
    {
        ItemNames.Upgrades:
        {
            # Hub

            # Manor

            # Rooftops
            LocationNames.soapammo_r005: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.gumammo_r020: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.blackknight_power_r004: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            # Balcony

            # Hedge
            LocationNames.soapammo_e007: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),

            # Fishing Village
            LocationNames.gumammo_f003: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.soapammo_f001: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) or (state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1))),
            # Cliffs
            LocationNames.gumammo_c003: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.shockwave_c007: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),

            # Passage

            # Secret Lab

            # Basement

            # Graveyard
            LocationNames.soapammo_g003: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),

            # Lighthouse
            LocationNames.soapammo_l019: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and (state.has(ItemNames.SoapPower, player, 1) or state.has(ItemNames.GumPower, player, 1)),
            LocationNames.gumammo_l011: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.PlungerPower, player, 1) or state.has(ItemNames.SoapPower, player, 1) or state.has(ItemNames.GumPower, player, 1)),
            LocationNames.pound_l017: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            # Wrecked Ships
            LocationNames.soapammo_w023: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.gumpower_w028: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1)
        },

        ItemNames.MonsterTokens:
        {
            # Hub

            # Manor
            LocationNames.headless_token_i001: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

            # Rooftops
            LocationNames.witchdoctor_token_r020: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),

            # Balcony
            LocationNames.creeper_token_o002: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),

            # Graveyard
            LocationNames.ghost_token_g005: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.scarecrow_token_g008: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            # Hedge
            LocationNames.wolfman_token_e001: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.witch_token_e003: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),

            # Fishing Village
            LocationNames.tarmonster_token_f004: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.ghostdiver_token_f007: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),

            # Coast
            LocationNames.greenghost_token_c005: lambda player: lambda state: state.has(ItemNames.SoapPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),

            # Passage

            # Secret Lab
            LocationNames.robot_token_s002: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.mastermind_token_s003: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and
                                                                              (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) ,

            # Basement

            # Lighthouse
            LocationNames.seacreature_token_l014: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) or state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.caveman_token_l013: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),

            # Wrecked Ships
            LocationNames.moody_token_w022: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.redbeard_token_w025: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
        },

        ItemNames.Keys:
            {
                # Hub
                LocationNames.hedgekey_h001: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
                LocationNames.fishingkey_h001: lambda player: lambda state: state.has(ItemNames.ShovelPower, player, 1),

                # Graveyard
                LocationNames.key_g007: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),

                # Passage
                LocationNames.key1_p003: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
                LocationNames.key2_p003: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
                LocationNames.key3_p003: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
                LocationNames.key_p004: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
                LocationNames.key1_p005: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
                LocationNames.key2_p005: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
                LocationNames.key3_p005: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
                LocationNames.key4_p005: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),

                # Balcony
                LocationNames.key1_o003: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
                LocationNames.key2_o003: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

                # Lighthouse
                LocationNames.key1_l011: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
                LocationNames.key2_l011: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
                LocationNames.key3_l011: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
                LocationNames.key4_l011: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),

                # Rooftops
                LocationNames.key3_r005: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

                # Basement
                LocationNames.key1_b002: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
                LocationNames.key2_b002: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
                LocationNames.key3_b002: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
                LocationNames.key1_b003: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
                LocationNames.key2_b003: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
                LocationNames.key3_b003: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
                LocationNames.key4_b003: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

                # Lighthouse
                LocationNames.key1_w027: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
                LocationNames.key2_w027: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
                LocationNames.key3_w027: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
                LocationNames.key4_w027: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            },

        ItemNames.Warps:
            {
                LocationNames.warp_gate_o001: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            },

        ItemNames.victory:
        {

        }
    }
]

monster_token_rules = [
    # connections
    {},
    # locations
    {}
]

key_rules = [
# connections
    {
        # Hub
        ConnectionNames.hub1_e001: lambda player: lambda state: state.has(ItemNames.Hedge_Key, player, 1) or state.has(ItemNames.Hedge_KeyRing, player, 1),
        ConnectionNames.hub1_f001: lambda player: lambda state: state.has(ItemNames.Fishing_Key, player, 1) or state.has(ItemNames.Fishing_KeyRing, player, 1),

        # Manor
        ConnectionNames.i001_i020: lambda player: lambda state: state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1),
        ConnectionNames.i003_i004: lambda player: lambda state: (state.has(ItemNames.Clamor4_Key, player, 1) or state.has(ItemNames.Clamor4_KeyRing, player, 1)) and state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.i005_i006: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),

        # Hedge
        ConnectionNames.e002_e003: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

        # Rooftop
        ConnectionNames.r005_o001: lambda player: lambda state: state.has(ItemNames.DLD_Key, player, 3) or state.has(ItemNames.DLD_KeyRing, player, 1),

        # Balcony
        ConnectionNames.o003_o004: lambda player: lambda state: state.has(ItemNames.Attic_Key, player, 3) or state.has(ItemNames.Attic_KeyRing, player, 1),
        ConnectionNames.o005_o006: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.o006_o005: lambda player: lambda state: state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1),
        ConnectionNames.o006_o008: lambda player: lambda state: (state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)) and state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.o008_o006: lambda player: lambda state: state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1),

        # Fishing Village
        ConnectionNames.f005_f006: lambda player: lambda state: state.has(ItemNames.FishyClues_Key, player, 4) or state.has(ItemNames.FishyClues_KeyRing, player, 1),

        # Coast
        ConnectionNames.c005_c006: lambda player: lambda state: (state.has(ItemNames.Cavein_Key, player, 4) or state.has(ItemNames.Cavein_KeyRing, player, 1)) and state.has(ItemNames.PlungerPower, player, 1),

        # Passage
        ConnectionNames.p002_s001: lambda player: lambda state: (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)) and state.has(ItemNames.SoapPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
        ConnectionNames.p002_p003: lambda player: lambda state: (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
        ConnectionNames.p003_p004: lambda player: lambda state: (state.has(ItemNames.Creepy3_Key, player, 3) or state.has(ItemNames.Creepy3_KeyRing, player, 1)) and state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
        ConnectionNames.p004_p005: lambda player: lambda state: (state.has(ItemNames.Gusts1_Key, player, 1) or state.has(ItemNames.Gusts1_KeyRing, player, 1))and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
        ConnectionNames.p005_b001: lambda player: lambda state: (state.has(ItemNames.Gusts2_Key, player, 4) or state.has(ItemNames.Gusts2_KeyRing, player, 1))and state.has(ItemNames.ProgressiveJump, player, 2),

        # Graveyard
        ConnectionNames.g001_g002: lambda player: lambda state: state.has(ItemNames.Graveplot_Key, player, 3) or state.has(ItemNames.Graveplot_KeyRing, player, 1),
        ConnectionNames.g007_g008: lambda player: lambda state: state.has(ItemNames.Tomb1_Key, player, 1) or state.has(ItemNames.Tomb1_KeyRing, player, 1),

        # Basement
        ConnectionNames.b002_b003: lambda player: lambda state: state.has(ItemNames.Cellar2_Key, player, 3) or state.has(ItemNames.Cellar2_KeyRing, player, 1),
        ConnectionNames.b003_b004: lambda player: lambda state: state.has(ItemNames.Cellar3_Key, player, 4) or state.has(ItemNames.Cellar3_KeyRing, player, 1),

        # Lighthouse
        ConnectionNames.l011_l013: lambda player: lambda state: state.has(ItemNames.Coast_Key, player, 4) or state.has(ItemNames.Coast_KeyRing, player, 1),

        # Wrecked Ships
        ConnectionNames.w027_w028: lambda player: lambda state: state.has(ItemNames.Shiver_Key, player, 4) or state.has(ItemNames.Shiver_KeyRing, player, 1),
    },
    # locations
    {
        ItemNames.Upgrades:
            {
                # Graveyard
                LocationNames.umbrella_g009: lambda player: lambda state: (state.has(ItemNames.Tomb3_Key, player, 2) or state.has(ItemNames.Tomb3_KeyRing, player, 1)) and state.has(ItemNames.PoundPower, player, 1),

                # Balcony
                LocationNames.gumammo_o001: lambda player: lambda state: (state.has(ItemNames.BootsPower, player, 1) or ((state.has(ItemNames.Attic_Key, player, 3) and state.has(ItemNames.Knight_Key, player, 4))) or state.has(ItemNames.Attic_KeyRing, player, 1) and state.has(ItemNames.Knight_KeyRing, player, 1)) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            },
        ItemNames.MonsterTokens:
            {
                # Manor
                LocationNames.geronimo_token_i005: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),

                # Balcony
                LocationNames.blackknight_token_o001: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1) or (state.has(ItemNames.Attic_Key, player, 3) and state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Attic_KeyRing, player, 1) and state.has(ItemNames.Knight_KeyRing, player, 1)),

                # Basement
                LocationNames.spacekook_token_b001: lambda player: lambda state: (state.has(ItemNames.Cellar2_Key, player, 3) or state.has(ItemNames.Cellar2_KeyRing, player, 1)) and state.has(ItemNames.SoapPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            },
        ItemNames.Keys:
            {
                # Passage
                LocationNames.key5_p002: lambda player: lambda state: (state.has(ItemNames.Creepy2_Key, player, 4) or state.has(ItemNames.Creepy2_KeyRing, player, 1)) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            },
        ItemNames.Warps:
            {

            },
     }
]

snack_rules = [
    # connections
    {
        ConnectionNames.s002_s004: lambda player: lambda state: state.has(ItemNames.Snack, player, 850),
        ConnectionNames.w026_w027: lambda player: lambda state: state.has(ItemNames.Snack, player, 750),
        ConnectionNames.g005_g007: lambda player: lambda state: state.has(ItemNames.Snack, player, 600),
        ConnectionNames.c004_c005: lambda player: lambda state: state.has(ItemNames.Snack, player, 550),
        ConnectionNames.l014_l015: lambda player: lambda state: state.has(ItemNames.Snack, player, 500),
        ConnectionNames.l018_p001: lambda player: lambda state: state.has(ItemNames.Snack, player, 500),
        ConnectionNames.f007_f008: lambda player: lambda state: state.has(ItemNames.Snack, player, 450),
        ConnectionNames.o004_o005: lambda player: lambda state: state.has(ItemNames.Snack, player, 400),
        ConnectionNames.r003_r004: lambda player: lambda state: state.has(ItemNames.Snack, player, 350),
        ConnectionNames.i003_i004: lambda player: lambda state: state.has(ItemNames.Snack, player, 200),
        ConnectionNames.e006_e007: lambda player: lambda state: state.has(ItemNames.Snack, player, 175),
        ConnectionNames.e004_e005: lambda player: lambda state: state.has(ItemNames.Snack, player, 150),
        ConnectionNames.hub1_hub3: lambda player: lambda state: state.has(ItemNames.Snack, player, 150),
        ConnectionNames.f003_f009: lambda player: lambda state: state.has(ItemNames.Snack, player, 50),
        ConnectionNames.hub1_i001: lambda player: lambda state: state.has(ItemNames.Snack, player, 25),
    },
    # locations
    {
        ItemNames.Upgrades:
        {
            # Hedge
            LocationNames.e001_SNACK__253: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),
            LocationNames.e001_SNACK__252: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),
            LocationNames.e001_SNACK__251: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),
            LocationNames.e001_SNACK__250: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),
            LocationNames.e001_SNACK__25: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),
            LocationNames.e001_SNACK__255: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),
            LocationNames.e001_SNACK__256: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),
            LocationNames.e001_SNACK__257: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),
            LocationNames.e001_SNACK__258: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),
            LocationNames.e001_SNACK__259: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.e009, "Region", player),

            LocationNames.e002_SNACK01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK010: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK011: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK012: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK013: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK014: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK015: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACKBOX__5: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK09 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK10 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK31 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK310: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK311: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK312: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK313: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK314: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK315: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK32 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK320: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK321: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK322: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK323: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK324: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK325: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK326: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK33 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK330: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK331: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK332: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK333: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK334: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK335: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK35 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK36 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK360: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK361: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK362: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK363: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK364: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK37 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK370: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK371: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK372: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK373: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK__374: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK40 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK400: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK401: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK402: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK403: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.e002_SNACK404: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),

            LocationNames.e003_SNACK__120: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__121: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__122: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__123: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__124: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__03 : lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__030: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__031: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__032: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__033: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.e003_SNACK__034: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),

            LocationNames.e004_SNACK21301: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e004_SNACK21303: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e004_SNACKBOX__2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e004_SNACK081: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e004_SNACK09301: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e004_SNACK09303: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e004_SNACKBOX__1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e004_SNACK__30301: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e004_SNACKBOX__3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

            LocationNames.e005_SNACK__13 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__130: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__131: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__132: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__133: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__143: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__142: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__141: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__140: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__14 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__11 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__110: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__111: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e005_SNACK__112: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e005_SNACK__15 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.e005_SNACK__114: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.ProgressiveJump, player, 1),

            LocationNames.e007_DIG__2__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ShovelPower, player, 1),
            LocationNames.e007_SNACK__220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__223: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__23 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__230: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__231: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__232: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__233: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__16 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__160: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__161: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__162: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__163: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__164: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__17 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__170: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__171: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__172: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__173: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__18 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__180: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__181: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__182: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__183: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__20 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__200: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__201: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__202: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__203: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__204: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__21 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__210: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__211: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__212: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__213: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__214: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__19 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__190: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__191: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__192: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__193: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__194: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e007_SNACK__195: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),

            LocationNames.e008_SNACK__300: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__301: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__302: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__090: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__091: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__092: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__25: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__250: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__251: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__252: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__2520: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__2521: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__2522: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__2523: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__25221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__25222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__252220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__252221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__252222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__2522220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__2522221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__2522222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__25222220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__25222221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__25222222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__252222220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__252222221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__252222222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__30: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__3020: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__3021: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__3022: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__30220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__30221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__30222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__32: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__320: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__321: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__322: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__3220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__3221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__3222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__32220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__32221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__32222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__322220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__322221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__322222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__330: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__331: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__332: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__3320: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__3321: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACK__3322: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),
            LocationNames.e008_SNACKBOX__2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)),

            LocationNames.e009_CRATE__SNACKBOX__1: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e009_CRATE__SNACKBOX__2: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e009_CRATE__SNACKBOX__3: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.e009_CRATE__SNACKBOX__4: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            # Cliffs
            LocationNames.c001_SS44: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS5: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS550: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS551: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS552: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS553: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS554: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS555: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS556: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS557: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS558: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS559: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS5510: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS5511: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS5512: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS16: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_BOX__OF__SNACKS__2: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS19: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS190: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS191: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS192: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS193: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS194: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS195: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS22: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS274: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS275: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS28: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS280: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS29: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_BOX__OF__SNACKS__4: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS387: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS386: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS385: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS384: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS383: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS382: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS381: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS380: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS38: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS35: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS350: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS351: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS352: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS353: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS36: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS373: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS372: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS371: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS370: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS37: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS1053: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS1052: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS1051: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS1050: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c001_SS105: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),


            LocationNames.c003_SNACK__246: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__245: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__244: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__243: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__231: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__230: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__23: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__1310: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__139: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__138: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__130: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__131: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__132: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__13: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__30: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__3010: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__3011: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__3012: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__3013: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__3014: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__300: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__301: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__302: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__303: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__304: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__305: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__306: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__307: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__308: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c003_SNACK__309: lambda player: lambda state: (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.c004_SNACK__07: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__071: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__073: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__075: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__076: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_BOX__OF__SNACKS__01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__061: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__064: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__066: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__068: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__0610: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__12: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__121: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__123: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__13: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__14: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__380: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__381: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__382: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__383: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__150: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__151: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__152: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__390: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__391: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__392: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__393: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_BOX__OF__SNACKS__02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__171: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__172: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__173: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__174: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__175: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__176: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__177: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__178: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__180: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__182: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__184: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__186: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__188: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__19: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_BOX__OF__SNACKS__03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__32: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__321: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__323: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__325: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__327: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__329: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__3211: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__3213: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_BOX__OF__SNACKS__06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__260: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__262: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__264: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__266: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__268: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__2610: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__2612: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__2620: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__2622: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.c004_SNACK__31: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__310: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__311: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__312: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__313: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__3130: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__31300: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__31301: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__31302: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__313030: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__31303: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__313031: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__313032: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__313033: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__355: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__3550: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__3552: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__3554: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__3556: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__340: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__341: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__342: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__343: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__344: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__345: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__346: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__347: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__348: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__349: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__3410: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c004_SNACK__60: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__600: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__602: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__603: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__606: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__608: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__70: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__700: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__701: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__702: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__703: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__704: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__705: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__706: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__36: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__361: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__363: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_SNACK__41: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_BOX__OF__SNACKS__05: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c004_BOX__OF__SNACKS__04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),

            LocationNames.c006_SNACK__02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c006_SNACK__020: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c006_SNACK__021: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c006_SNACK__022: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c006_SNACK__023: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c006_SNACK__024: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.c006_CRATE__SNACKBOX__1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and ((ItemNames.PoundPower, player, 1) or (ItemNames.HelmetPower, player, 1)),
            LocationNames.c006_CRATE__SNACKBOX__2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and ((ItemNames.PoundPower, player, 1) or (ItemNames.HelmetPower, player, 1)),
            LocationNames.c006_SNACK__804: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__803: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__802: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__801: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__800: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__80: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__805: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__806: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__807: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__808: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__809: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACKBOX__3: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.c006_SNACK__BOX__2: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.c007_SNACK__04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__040: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__041: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__042: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__043: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__044: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__045: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_BOX__OF__SNACKS__3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__074: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__073: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__072: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__071: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__070: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__07: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__075: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__076: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__077: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__078: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__079: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__0790: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__0791: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__0792: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__0793: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__0794: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__10: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__100: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__101: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__102: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__103: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__104: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__105: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__106: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__12: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__120: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__121: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__122: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__123: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__124: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__125: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__164: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__163: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__162: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__161: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__160: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__16: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__17: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__174: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__175: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__176: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__177: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__178: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_BOX__OF__SNACKS__4: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__180: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__181: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__182: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__183: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__184: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__185: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__186: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__187: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__188: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__189: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__193: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__192: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__191: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__190: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__19: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__194: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__195: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__196: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__197: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__198: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_BOX__OF__SNACKS__2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__204: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__203: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__202: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__201: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__200: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__20 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__213: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__212: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__211: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__210: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__21: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__223: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__222: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_SNACK__22: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_CRATE__PRIZE__1 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.c007_CRATE__PRIZE__10: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),

            # Graveyard
            LocationNames.g001_BOX__OF__SNACKS__1: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_BOX__OF__SNACKS__2: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_BOX__OF__SNACKS__3: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS10: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS11: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS110 : lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1100: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1101: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1102: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1103: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1104: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1105: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1106: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1107: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS1109: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS12: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS13: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS15: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS16: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS17: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS18: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g001_SS19: lambda player: lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),

            LocationNames.g003_SS111: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS112: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS110: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS19: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS18: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS17: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS16: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS15: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS14: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS13: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS12: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS11: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS10: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SS1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SNACK__17: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SNACK__18: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SNACK__170: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SNACK__171: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SNACK__172: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g003_SNACKBOX__3: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_BOX__OF__SNACKS__1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__05: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__07: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__08: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__09: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__11: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__14: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__15: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__050: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__060: lambda player:  lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__070: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__080: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__090: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__091: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__092: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__093: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__110: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__111: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__112: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__113: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__160: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__1130: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g003_SNACK__1131: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.g006_URN__1__PRIZE: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_URN__2__PRIZE: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__070: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g006_SNACK__071: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g006_SNACK__072: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.g006_SNACK__10 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__100: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__101: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__102: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__103: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__104: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__14: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__140: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__141: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__142: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__143: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__17: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__170: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__171: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__172: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__173: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACK__174: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.g006_SNACKBOX__3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.g008_SNACKBOX__0: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__1__1: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__1__10: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__1__11: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__1__12: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__2__1: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__2__10: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__2__11: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__2__12: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__3__1: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__3__10: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__3__11: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__3__12: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__4__1: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__4__10: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__4__11: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACKBOX__4__12: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.g008_SNACK__183: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g008_SNACK__184: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g008_SNACK__185: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g008_SNACK__186: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g008_SNACK__187: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g008_SNACK__188: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.g008_SNACK__189: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),

            # Fishing Village
            LocationNames.f001_FOOD12: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_FOOD11: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f001_SS116: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f001_SS1163: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f001_SS114_COUNT70: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f001_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f001_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f001_S31: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_S32: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_S33: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_S34_COUNT30: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_S37: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_S39: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_S40: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_S41: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_S43: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f001_S44: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),

            LocationNames.f003_S11: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f003_S12: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f003_S13: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f003_S14: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f003_S15: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f003_SS1500: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f003_SS150000: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f003_S01: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f003_SS15: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f003_SS162: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f003_SS16222: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f003_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f003_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f003_S8: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),

            LocationNames.f004_S91: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f004_S02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f004_S021: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f004_S023: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f004_S90: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f004_SS32: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f004_SS010: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f004_SS012: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f004_S94: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f004_S21: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f004_S23: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f004_S25: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f004_S27: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f004_S29: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f004_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f004_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.f005_SSBOX01: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.f005_SSBOX02: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),

            LocationNames.f007_S311: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S312: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S314: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S315: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S316: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S317: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S41: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S42: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S43: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S44: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S45: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_S450: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_SS03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_SSBOX03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_SSBOX04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.f007_SS05: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),

            LocationNames.f008_S031: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f008_S16: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f008_S19: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f008_S20: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f008_SS13: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f008_SS22: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),

            LocationNames.f009_S010: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S05: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f009_S07: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f009_S08: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f009_S09: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f009_S11: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f009_S12: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S13: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S14: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f009_S15: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.f009_S33: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S330: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S331: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S332: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S333: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S334: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S335: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3350: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3351: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3352: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3353: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3354: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S34: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S340: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S341: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S342: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S343: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S344: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S345: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S346: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3460: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3461: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3462: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3463: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_S3464: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS010: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS011: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS012: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS013: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS014: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS015: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS016: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS017: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS018: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS21: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS23: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS25: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS26: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS27: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS28: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS30: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS31: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SS32: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f009_SSBOX03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),

            LocationNames.f010_SS20: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_UPPERDECK_SSBOX04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f010_UPPERDECK_SSBOX06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.f010_CRATE_SNACK01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_CRATE_SSBOX07: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_BP_SS03: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_BP_SS04: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_BP_SS05: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_BP_SSBOX01: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_BP_SSBOX04: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_CRATE_SNACK02: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_CRATE_SNACK03: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_CRATE_SNACK04: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_CRATE_SNACK05: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_CRATE_SNACK06: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_CRATE_SNACK08: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_CRATE_SNACK09: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS18: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS180: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS181: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS1811: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS182: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS183: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS184: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS185: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS1851: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS1853: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS1855: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS187: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS189: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.f010_SS8: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),

            # Lighthouse
            LocationNames.l011_BOX10__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l011_BOX11__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l011_BOX13__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l011_BOX2__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l011_BOX3__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l011_BOX5__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l011_BOX6__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l011_BOX8__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l011_CLIFF_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_CLIFF_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_CLIFF_SSBOX03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_CLIFF_SSBOX04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_CLIFF_SSBOX05: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_CLIFF_SSBOX06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_LASTFLOAT_SS02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_LASTFLOAT_SS03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_LASTFLOAT_SS04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SS01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SS02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SS03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SS05: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SS06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SS07: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SS09: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SS10: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SSBOX04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SLOPE_SSBOX08: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK__090: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK__11 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK__15 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK__150: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK__151: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK__16 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK__18 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK__19 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK39: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK43: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK51: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.l011_SNACK52: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK53: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK54: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK55: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK57: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK58: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK59: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK60: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK61: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK62: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK63: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK64: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK65: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK67: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK69: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK70: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.l011_SNACK72: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SNACK73: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.l011_SS01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS010: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS011: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS0110: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS0111: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS012: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS013: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS014: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS015: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS016: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS017: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS018: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS019: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SS04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SSBOX04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_SSBOX05: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.l011_SSBOX06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.l011_UPPER_SS01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_UPPER_SS02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_UPPER_SS03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_UPPER_SS04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_UPPER_SS05: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_UPPER_SS06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_UPPER_SS08: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_UPPER_SS09: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l011_UPPER_SS10: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

            LocationNames.l013_SS03: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l013_SSBOX11: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),

            LocationNames.l014_SS10: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SS11: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS110: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS111: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS112: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS113: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS114: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS115: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS12: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS120: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS121: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS122: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS123: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS124: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS125: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS13: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS130: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS131: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS132: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS133: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS134: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS135: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS14: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS15: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS16: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS17: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS18: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SS2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SS200: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS201: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS2010: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS2011: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS202: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS203: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS204: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS205: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS206: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS207: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS208: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS209: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS210: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS211: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS212: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS213: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS214: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS215: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS216: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SS30: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS300: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS301: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS302: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS303: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS304: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS305: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.l014_SS4: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SS5: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SS6: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SS7: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SS8: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SS9: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SSBOX04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SSBOX06: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SSBOX07: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SSBOX08: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l014_SSBOX09: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

            LocationNames.l015_SS030: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS031: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS032: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS033: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS034: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS11: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS12: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS13: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS15: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS16: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS17: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS18: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS19: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS20: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS21: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS22: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS23: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS24: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS25: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS26: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS27: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS270: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS271: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS2711: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS28: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS60: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS600: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS601: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS602: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS6020: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS60200: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS6021: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS6022: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS7: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS9: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SSBOX03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SSBOX04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS300: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS301: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3010: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3011: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3012: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3013: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3014: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS302: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS303: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3030: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3031: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3032: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3033: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS3034: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS40: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS400: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS401: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS4010: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SSBOX05: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player),
            LocationNames.l015_SS4011: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS4012: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS4014: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS4015: lambda player: lambda state: state.can_reach(RegionNames.l018, "Region", player) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.l015_SS500: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.l015_SS501: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),

            LocationNames.l017_CRATE02__SNACKBOX: lambda player: lambda state: (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l017_CRATE03__SNACKBOX: lambda player: lambda state: (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l017_CRATE04__SNACKBOX: lambda player: lambda state: (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l017_CRATE06__SNACKBOX: lambda player: lambda state: (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l017_CRATE07__SNACKBOX: lambda player: lambda state: (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.l017_CRATE08__SNACKBOX: lambda player: lambda state: (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),

            LocationNames.l018_SSBOX03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

            # Wrecked Ships
            LocationNames.w020_SS910: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w020_SS911: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w020_SS912: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w020_SS913: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w020_SS914: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w020_SS55: lambda player: lambda state: state.can_reach(RegionNames.w026, "Region", player),

            LocationNames.w022_SS010: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS011: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS012: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS020: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS021: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS022: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS030: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS040: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS041: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS042: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS05: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS050: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS051: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS07: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS070: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS071: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS072: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS08 : lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS080: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS081: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS09: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS090: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS091: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS10: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS100: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS101: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS102: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS16: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS17: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS18: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS20: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS200: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS201: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS21: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS210: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS211: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS22: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS221: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS23: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS230: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS231: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS24: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS241: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS25: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS250: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS251: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS27: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS271: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS272: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS28: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS281: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS31: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS32: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SS33: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SSBOX12: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SSBOX13: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w022_SSBOX14: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),

            LocationNames.w025_SSBOX01: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.w025_SSBOX02: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.w025_SSBOX04: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.w025_SSBOX06: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.w025_SS090: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.w025_SS0410: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0411: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0412: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS048: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS049: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS05: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS051: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS055: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS057: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS058: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS06: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS061: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS063: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS065: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS067: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS068: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS07: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS071: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0711: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0713: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0715: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0717: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0719: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0721: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0723: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS0725: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS073: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS075: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS077: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS079: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS08: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS080: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS081: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS09: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS091: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS092: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS093: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS100: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS101: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS104: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS105: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS106: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS107: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS110: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS112: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS113: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS114: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS115: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS12: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS120: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS121: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS122: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS124: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS125: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS126: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS13: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS130: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS131: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS132: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS133: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS134: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS135: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SS136: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SSBOX03: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SSBOX07: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SSBOX08: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SSBOX09: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w025_SSBOX10: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1),

            LocationNames.w027_SS113: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.w027_SS115: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.w027_SSBOX_GD01A: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.w027_SSBOX_GD01B: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.w027_SSBOX_GD02A: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.w027_SSBOX_GD02B: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.w027_SS03B: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SS03B1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SS03B3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SS03B5: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SS03B7: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SS04B: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SS04B1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SS04B3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SS04B5: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SS04B7: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.w027_SSCONV: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV11: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV13: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV15: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV151: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV1511: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV1513: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV153: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV155: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV157: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV159: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV5: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV7: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.w027_SSCONV9: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),

            # Manor
            LocationNames.i001_SN12: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN19: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN20: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN21: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN22: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN23: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN24: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN25: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN26: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN27: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN4: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN48: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SN6: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i001_SNACKBOX__CHAND__2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

            LocationNames.i020_SN1: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN10: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN11: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN12: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN13: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN14: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN15: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN16: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN17: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN18: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN19: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN20: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN21: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN22: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN23: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN24: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN25: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN26: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN32: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN33: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN34: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN35: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN36: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN37: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN40: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN41: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN42: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN48: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SN49: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SNACKBOX1: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SNACKBOX2: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i020_SNACKBOX3: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SNACK__BOX__OVER__PIT: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SNACK__BOX__OVER__PIT__2: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i020_SS1: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.i003_EX__CLUE__SNACKBOX4: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i003_SNACK__BOX__10: lambda player: lambda state: state.can_reach(RegionNames.i004, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i003_SN52: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i003_SN53: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i003_SN54: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.i004_EX__CLUE__SNACK__BOX__4: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.i004_EX__CLUE__SNACK__BOX__1: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.i004_SN7: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.i004_EX__CLUE__SNACK__BOX__3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i004_NEW__SNACKBOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i004_NEW__SNACKBOX__2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i004_SN15: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i004_SN16: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i004_SN17: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i004_SN18: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i004_SN9: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i006_FOOD1: lambda player: lambda state: state.has(ItemNames.SoapPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.i006_SNACKBOX__3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

            # Rooftops
            LocationNames.r001_SS68: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r001_SS69: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r001_SS70: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r001_SS71: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r001_CRATE__2__PRIZE: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r001_SS31: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r001_SS32: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r001_SS33: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r001_SS34: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r001_SS35: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r001_SS36: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r001_SS37: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.r020_SN51: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN52: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN53: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN54: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN55: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN56: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN57: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN58: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN93: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN94: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN95: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN96: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r020_SN19: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.r020_SN20: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.r020_SN21: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.r020_SN97: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.r020_SN98: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.r020_SN84: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r020_SN85: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r020_SN86: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r020_SN87: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r020_SN88: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r020_SN89: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r020_SN90: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r020_SN26: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r020_SN27: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.r021_CRATE__2__PRIZE: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_CRATE__3__PRIZE: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN1: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN10: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN100: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN11: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN12: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN13: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN14: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN15: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN16: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN17: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN18: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN19: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN2: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN20 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN21 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN22 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN23 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN24 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN25 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN26 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN27 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN28 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN29 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN3: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN30 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN31 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN32 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN33 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN34 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN35 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN36 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN37 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN38 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN39 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN4: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN40 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN41 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN42 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN43 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN44 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN45 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN46 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN47 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN48 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN49 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN5: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN50 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN51 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN52 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN53 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN54 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN55 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN56 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN57 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN58 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN59 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN6: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN60 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN61 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN62 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN63 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN64 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN65 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN66 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN67 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN68 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN69 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN7: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN70 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN71 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN72 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN73 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN74 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN75 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN8: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN84: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN840: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN841: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN842: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN843: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN844: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN845: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN846: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN847: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN85 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN86 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN87 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN88 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN89 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN9: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN90 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN91 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN92 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN93 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN94 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN95 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN96 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN97 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.r021_SN98 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SN99 : lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SNACKBOX: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r021_SNACKBOX2: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.r003_CRATE__2__PRIZE: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.r003_CRATE__3__PRIZE: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.r003_SNACKBOX__1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

            LocationNames.r005_SS13: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.r005_SS14: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            # Balcony
            LocationNames.o001_SN57: lambda player: lambda state: state.can_reach(RegionNames.o008, "Region", player),
            LocationNames.o001_SN49: lambda player: lambda state: state.can_reach(RegionNames.o008, "Region", player),
            LocationNames.o001_SN44: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.o001_SN45: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.o001_SN46: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.o001_SN47: lambda player: lambda state: state.has(ItemNames.BootsPower, player, 1),
            LocationNames.o001_SSBOX01: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o001_SSBOX02: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o001_SSBOX03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o001_SSBOX04: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.o002_SS28: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o002_SS29: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o002_SS30: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o002_SSBOX03: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o002_SS31: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o002_SS32: lambda player: lambda state: state.has(ItemNames.PlungerPower, player,1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o002_SS34: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o002_SS35: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o002_SS36: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o002_SS39: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o002_SS40: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.o003_SN43: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o003_SN44: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o003_SN74: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o003_SN75: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.o003_SSBOX01: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.o004_SN42: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),

            LocationNames.o005_SM100: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM68: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM69: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM70: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM76: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM77: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM78: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM79: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM80: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM81: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM82: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM83: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM84: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM85: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM86: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM87: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM88: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM89: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM90: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM91: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM92: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM93: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM94: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM95: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM96: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM97: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM98: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM99: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN33: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN4: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN40: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN41: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN42: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN43: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN44: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN45: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN46: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN47: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN48: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN49: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN50: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN51: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN52: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN53: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN54: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN55: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN56: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN58: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN59: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN60: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN61: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN62: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN63: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN64: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN65: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN66: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SN67: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SSBOX02: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SSBOX03: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SSBOX04: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SSBOX06: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.o005_SM71: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.o005_SM72: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.o005_SM73: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.o005_SM74: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.o005_SM75: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.o005_SSBOX05: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PlungerPower, player, 1),

            LocationNames.o006_SSBOX05: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S100: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S89: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S90: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S91: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S92: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S93: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S94: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S95: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S96: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S97: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S98: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_S99: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN1: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN10: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN11: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN12: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN13: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN14: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN15: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN16: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN17: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN18: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN19: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN2: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN20: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN21: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN22: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN23: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN24: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN25: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN26: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN27: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN28: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN29: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN3: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN30: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN31: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN32: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN33: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN34: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN35: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN38: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN39: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN4: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN42: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN44: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN45: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN46: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN47: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN48: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN49: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN5: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN50: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN51: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN52: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN53: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN54: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN55: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN56: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN57: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN58: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN59: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN6: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN60: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN61: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN62: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN63: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN64: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN65: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN66: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN67: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN68: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN69: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN7: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN70: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN71: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN72: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN73: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN74: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN75: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN76: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN77: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN78: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN79: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN8: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN80: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN81: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN82: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN83: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN84: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN85: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN86: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN87: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN88: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SN9: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SSBOX01: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SSBOX02: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SSBOX03: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),
            LocationNames.o006_SSBOX04: lambda player: lambda state: ((state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1)) or state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)),

            # Passage
            LocationNames.p001_SS16: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS160: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS17: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS170: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS171: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS172: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS173: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS174: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS175: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS18: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS180: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS181: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS182: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS183: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_SS1600: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_HIGH__SNACK__BOX: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.p001_EX__CLUE__SNACKBOX__2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.p001_EX__CLUE__SNACKBOX__1: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p001_SNACK__BOX__LEFT__CORRIDOR__2: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.PlungerPower, player, 1),

            LocationNames.p002_SNACKBOX3: lambda player: lambda state: state.can_reach(RegionNames.s001, "Region", player),

            LocationNames.p003_SS2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.p003_SS20: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.p003_SS2000: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.p003_SS20000: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.p003_SS200000: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.p003_SS2000000: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.p003_SS20000000: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.p003_SS200000000: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.p003_SS4: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),

            LocationNames.p003_SS192: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SS1920: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SS1921: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SS3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SWINGER__SNACK__LINE: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SWINGER__SNACK__LINE0: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SWINGER__SNACK__LINE00: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SWINGER__SNACK__LINE1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SWINGER__SNACK__LINE10: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SWINGER__SNACK__LINE100: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_BOX__O__SNACKS__UNDER__SWINGER: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_BOX__O__SNACKS__UNDER__SWINGER0: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_BOX__O__SNACKS__UNDER__SWINGER00: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_EXCLUE__SNACKBOX__1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),
            LocationNames.p003_SNACKBOX0: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.GumPower, player, 1),

            LocationNames.p004_SNACKBOX1: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.p004_S4: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.can_reach(RegionNames.p005, "Region", player),
            LocationNames.p004_S40: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.can_reach(RegionNames.p005, "Region", player),
            LocationNames.p004_S43: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.can_reach(RegionNames.p005, "Region", player),
            LocationNames.p004_S44: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.can_reach(RegionNames.p005, "Region", player),
            LocationNames.p004_S471: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.can_reach(RegionNames.p005, "Region", player),
            LocationNames.p004_S472: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.can_reach(RegionNames.p005, "Region", player),
            LocationNames.p004_S475: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.can_reach(RegionNames.p005, "Region", player),
            LocationNames.p004_S476: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.can_reach(RegionNames.p005, "Region", player),

            LocationNames.p005_SS1: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS110: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS111: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS112: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS113: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS114: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS115: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS4: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS40: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS42: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS43: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS44: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS45: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_SS46: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),
            LocationNames.p005_EX__CLUE__SNACKBOX__4: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1),

            LocationNames.p005_SS18: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.p005_SS19: lambda player: lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.p005_EX__CLUE__SNACKBOX__2: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.p005_EX__CLUE__SNACKBOX__3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS52: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS50: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS22: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS220: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS8: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS9: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS10: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS11: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS12: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS13: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS5: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS51: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS53: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),
            LocationNames.p005_SS55: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2),

            # Basement
            LocationNames.b001_EX__CLUE__SNACKBOX4: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1),
            LocationNames.b001_EX__CLUE__SNACKBOX2: lambda player: lambda state: state.can_reach(RegionNames.b003, "Region", player) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.b001_EX__CLUE__SNACKBOX3: lambda player: lambda state: state.can_reach(RegionNames.b003, "Region", player) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.b001_EX__CLUE__SNACKBOX30: lambda player: lambda state: state.can_reach(RegionNames.b003, "Region", player) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),
            LocationNames.b001_EX__CLUE__SNACKBOX300: lambda player: lambda state: state.can_reach(RegionNames.b003, "Region", player) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1)),

            LocationNames.b002_EX__CLUE__SNACKBOX__2: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.b002_SS601: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.b002_SS60: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.b002_SS6: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.b002_SS600: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.b002_EX__CLUE__SNACKBOX__3: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.b002_EX__CLUE__SNACKBOX__1: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),

            LocationNames.b003_SS__999: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b003_EX__CLUE__SNACKBOX3: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b003_SS190: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b003_SS191: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b003_SS192: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b003_EX__CLUE__SNACKBOX5: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b003_SS1972: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b003_SS1974: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b003_EX__CLUE__SNACKBOX4: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.b004_SNACK10: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK12: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK14: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK16: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK18: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK110: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK1120: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK1122: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK1124: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK1126: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK1128: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACK11210: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS20: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS21: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS22: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS23: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACKBOX2: lambda player: lambda state: state.can_reach(RegionNames.p005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_DRYER__SNACKBOX__1: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_DRYER__SNACKBOX__2: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.b004_SS6: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS7: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS70: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS24: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACKBOX3: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS5: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS1: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS8: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS2400: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS4: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS2: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS3: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SNACKBOX5: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS100: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS9: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.b004_SS10: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.can_reach(RegionNames.b003, "Region", player) and state.has(ItemNames.HelmetPower, player, 1),

            # Secret Lab
            LocationNames.s002_SS26: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.s002_SS261: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.s002_SS263: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.s002_SS265: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.s002_SS267: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.s002_SS268: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.s002_SS2681: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.s002_SS2683: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.s002_SS2685: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
            LocationNames.s002_SS2687: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1),

            LocationNames.s002_SNACK__1__MIL: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_SS2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_SS3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_SS4: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_SS5: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_SS7: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_SS8: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_EX__CLUE__SNACK__BOX5: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_SS9103: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_SS9105: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1),
            LocationNames.s002_EX__CLUE__SNACK__BOX2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s002_EX__CLUE__SNACK__BOX3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1),

            LocationNames.s003_SNACK111: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK113: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK115: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK117: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK119: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SS6: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SS7: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACKBOX__2ND__LEVEL__1: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACKBOX__2ND__LEVEL__2: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK110101: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK110103: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK110105: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK110107: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK110109: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK19: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACKBOX00: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACKBOX0: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SS10: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SS11: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK1103: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK1105: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK1107: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK1109: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK11: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK1101: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK13: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK15: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACK17: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),
            LocationNames.s003_SNACKBOX: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1),

        },

        ItemNames.Keys:
        {
            # Manor
            LocationNames.i001_SN43: lambda player: lambda state: state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1),
            LocationNames.i001_SN44: lambda player: lambda state: state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1),
            LocationNames.i001_SN45: lambda player: lambda state: state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1),
            LocationNames.i001_SN46: lambda player: lambda state: state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1),
            LocationNames.i001_SN47: lambda player: lambda state: state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1),
            LocationNames.i001_SNACKBOX2: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1)),
            LocationNames.i001_SNACKBOX3: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1)),
            LocationNames.i001_SN7: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1)),
            LocationNames.i001_SN8: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1)),
            LocationNames.i001_SN29: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1)),
            LocationNames.i001_SN30: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1)),
            LocationNames.i001_SN11: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1)),
            LocationNames.i001_SNACKBOX__SECRET__AREA: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Clamor1_Key, player, 1) or state.has(ItemNames.Clamor1_KeyRing, player, 1)),

            LocationNames.i003_SN92: lambda player: lambda state: state.has(ItemNames.Clamor4_Key, player, 1) or state.has(ItemNames.Clamor4_KeyRing, player, 1),
            LocationNames.i003_SN93: lambda player: lambda state: state.has(ItemNames.Clamor4_Key, player, 1) or state.has(ItemNames.Clamor4_KeyRing, player, 1),
            LocationNames.i003_SN94: lambda player: lambda state: state.has(ItemNames.Clamor4_Key, player, 1) or state.has(ItemNames.Clamor4_KeyRing, player, 1),
            LocationNames.i003_SN95: lambda player: lambda state: state.has(ItemNames.Clamor4_Key, player, 1) or state.has(ItemNames.Clamor4_KeyRing, player, 1),
            LocationNames.i003_EX__CLUE__SNACKBOX1: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.Clamor4_Key, player, 1) or state.has(ItemNames.Clamor4_KeyRing, player, 1)),
            LocationNames.i003_EX__CLUE__SNACKBOX5: lambda player: lambda state: state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Clamor4_Key, player, 1) or state.has(ItemNames.Clamor4_KeyRing, player, 1)),

            LocationNames.i005_BOX__OVER__WITCH: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN13: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN17: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN18: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN25: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN26: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN27: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN30: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN4: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN45: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN46: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN47: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN48: lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1)),
            LocationNames.i005_SN480: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN5: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN50: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN51: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN53: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN54: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN55: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN6: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN60: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN63: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN64: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN68: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN680: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN6800: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN75: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN76: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN77: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN8: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN80: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN81: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN82: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN83: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN84: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN85: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN86: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN87: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN89: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN9: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN90: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN91: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SN92: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),
            LocationNames.i005_SNACKBOX2: lambda player: lambda state: state.has(ItemNames.MYM_Key, player, 4) or state.has(ItemNames.MYM_KeyRing, player, 1),

            # Rooftops

            # Balcony

            # Graveyard

            LocationNames.g007_BOX__OF__SNACKS__5: lambda player: lambda state: state.has(ItemNames.Tomb1_Key, player, 1) or state.has(ItemNames.Tomb1_KeyRing, player, 1),

            # Hedge

            # Fishing Village

            # Coast

            # Passage
            LocationNames.p002_SNACK12: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SNACK120: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SNACK14: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SNACK16: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SNACK18: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_EX__CLUE__SNACKBOX__3: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SS12: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SS15: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SS18: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SS180: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SS181: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SS182: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SNACKBOX30: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SS13: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),
            LocationNames.p002_SS14: lambda player: lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and (state.has(ItemNames.Creepy2_Key, player, 5) or state.has(ItemNames.Creepy2_KeyRing, player, 1)),

            # Secret Lab

            # Basement

            # Lighthouse

            # Wrecked Ships
        },
    }
]

warpgate_rules = [
    # connections
    {
        ConnectionNames.hub1_b004: lambda player: lambda state: state.has(ItemNames.Cellar4_Warp, player, 1),
        ConnectionNames.hub1_c004: lambda player: lambda state: state.has(ItemNames.Cliff4_Warp, player, 1),
        ConnectionNames.hub1_e004: lambda player: lambda state: state.has(ItemNames.Hedge4_Warp, player, 1),
        ConnectionNames.hub1_e006: lambda player: lambda state: state.has(ItemNames.Hedge6_Warp, player, 1),
        ConnectionNames.hub1_e009: lambda player: lambda state: state.has(ItemNames.Hedge9_Warp, player, 1),
        ConnectionNames.hub1_f003: lambda player: lambda state: state.has(ItemNames.Fish3_Warp, player, 1),
        ConnectionNames.hub1_f007: lambda player: lambda state: state.has(ItemNames.Fish7_Warp, player, 1),
        ConnectionNames.hub1_o001: lambda player: lambda state: state.has(ItemNames.Balc1_Warp, player, 1),
        ConnectionNames.hub1_o004: lambda player: lambda state: state.has(ItemNames.Balc4_Warp, player, 1),
        ConnectionNames.hub1_o006: lambda player: lambda state: state.has(ItemNames.Balc6_Warp, player, 1),
        ConnectionNames.hub1_g001: lambda player: lambda state: state.has(ItemNames.Grave1_Warp, player, 1),
        ConnectionNames.hub1_g005: lambda player: lambda state: state.has(ItemNames.Grave5_Warp, player, 1),
        ConnectionNames.hub1_g008: lambda player: lambda state: state.has(ItemNames.Grave8_Warp, player, 1),
        ConnectionNames.hub1_i003: lambda player: lambda state: state.has(ItemNames.Manor3_Warp, player, 1),
        ConnectionNames.hub1_i006: lambda player: lambda state: state.has(ItemNames.Manor6_Warp, player, 1),
        ConnectionNames.hub1_l014: lambda player: lambda state: state.has(ItemNames.LH14_Warp, player, 1),
        ConnectionNames.hub1_l015: lambda player: lambda state: state.has(ItemNames.LH15_Warp, player, 1),
        ConnectionNames.hub1_l018: lambda player: lambda state: state.has(ItemNames.LH18_Warp, player, 1),
        ConnectionNames.hub1_p003: lambda player: lambda state: state.has(ItemNames.SP3_Warp, player, 1),
        ConnectionNames.hub1_p005: lambda player: lambda state: state.has(ItemNames.SP5_Warp, player, 1),
        ConnectionNames.hub1_r003: lambda player: lambda state: state.has(ItemNames.Roof3_Warp, player, 1),
        ConnectionNames.hub1_s002: lambda player: lambda state: state.has(ItemNames.SL2_Warp, player, 1),
        ConnectionNames.hub1_w022: lambda player: lambda state: state.has(ItemNames.Wreck22_Warp, player, 1),
        ConnectionNames.hub1_w026: lambda player: lambda state: state.has(ItemNames.Wreck26_Warp, player, 1),

        ConnectionNames.o001_o008: lambda player: lambda state: state.has(ItemNames.Balc1_Warp, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
        ConnectionNames.o006_o008: lambda player: lambda state: state.has(ItemNames.Balc6_Warp, player, 1) and state.has(ItemNames.HelmetPower, player, 1),
    },
    # locations
    {
        ItemNames.Upgrades:
            {
                # Balcony
                LocationNames.gumammo_o001: lambda player: lambda state: state.has(ItemNames.Balc1_Warp, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1))
            },
        ItemNames.Warps:
            {
                LocationNames.warp_gate_i003: lambda player: lambda state: state.has(ItemNames.Manor3_Warp, player, 1),
                LocationNames.warp_gate_o001: lambda player: lambda state: state.has(ItemNames.Balc1_Warp, player, 1),
            },
        ItemNames.MonsterTokens:
            {
                LocationNames.geronimo_token_i005: lambda player: lambda state: state.has(ItemNames.Manor6_Warp, player, 1) or (state.has(ItemNames.HelmetPower, player, 1)
                                                                                 and (state.has(ItemNames.Roof3_Warp, player, 1) or state.has(ItemNames.Balc1_Warp, player, 1)
                                                                                 or state.has(ItemNames.Balc4_Warp, player, 1) or state.has(ItemNames.Balc6_Warp, player, 1))),

                # Balcony
                LocationNames.blackknight_token_o001: lambda player: lambda state: state.has(ItemNames.Balc1_Warp, player, 1) and (state.has(ItemNames.HelmetPower, player, 1) or state.has(ItemNames.PoundPower, player, 1))
            },
        ItemNames.Keys:
            {
                LocationNames.key1_o006:  lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.o005, "Region", player)
                                                                        or (state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)) and state.has(ItemNames.Balc6_Warp, player, 1),
                LocationNames.key2_o006:  lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.o005, "Region", player)
                                                                        or (state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)) and state.has(ItemNames.Balc6_Warp, player, 1),
                LocationNames.key3_o006:  lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.o005, "Region", player)
                                                                        or (state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)) and state.has(ItemNames.Balc6_Warp, player, 1),
                LocationNames.key4_o006:  lambda player: lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.o005, "Region", player)
                                                                        or (state.has(ItemNames.Knight_Key, player, 4) or state.has(ItemNames.Knight_KeyRing, player, 1)) and state.has(ItemNames.Balc6_Warp, player, 1),
            }
    }
]

def _add_rules(multiworld: MultiWorld, player: int, rules: List, allowed_loc_types: List[str]):
    for name, rule_factory in rules[0].items():
        if type(rule_factory) == tuple and len(rule_factory) > 1 and rule_factory[1]:  # force override
            rule_factory = rule_factory[0]
            set_rule(multiworld.get_entrance(name, player), rule_factory(player))
        else:
            add_rule(multiworld.get_entrance(name, player), rule_factory(player))
    for loc_type, type_rules in rules[1].items():
        if loc_type not in allowed_loc_types:
            continue
        for name, rule_factory in type_rules.items():
            if type(rule_factory) == tuple and len(rule_factory) > 1 and rule_factory[1]:  # force override
                rule_factory = rule_factory[0]
                set_rule(multiworld.get_location(name, player), rule_factory(player))
            else:
                add_rule(multiworld.get_location(name, player), rule_factory(player))

def _set_rules(multiworld: MultiWorld, player: int, rules: List, allowed_loc_types: List[str]):
    for name, rule_factory in rules[0].items():
        set_rule(multiworld.get_entrance(name, player), rule_factory(player))
    for loc_type, type_rules in rules[1].items():
        if loc_type not in allowed_loc_types:
            continue
        for name, rule_factory in type_rules.items():
            set_rule(multiworld.get_location(name, player), rule_factory(player))

def set_rules(multiworld: MultiWorld, options: NO100FOptions, player: int):
    allowed_loc_types = [ItemNames.Upgrades,ItemNames.victory]
    if options.include_monster_tokens.value:
        allowed_loc_types += [ItemNames.MonsterTokens]
    if options.include_keys.value:
        allowed_loc_types += [ItemNames.Keys]
    if options.include_warpgates.value:
        allowed_loc_types += [ItemNames.Warps]
    if options.include_snacks.value:
        allowed_loc_types += [ItemNames.Snacks]

    _add_rules(multiworld, player, upgrade_rules, allowed_loc_types)
    if options.include_monster_tokens.value:
        _add_rules(multiworld, player, monster_token_rules, allowed_loc_types)
    if options.include_keys.value:
        _add_rules(multiworld, player, key_rules, allowed_loc_types)
    if options.include_warpgates.value:
        _add_rules(multiworld, player, warpgate_rules, allowed_loc_types)
    if options.include_snacks.value:
        _add_rules(multiworld, player, snack_rules, allowed_loc_types)

    goal = options.completion_goal.value
    if goal == 0:
        add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.s004, "Region", player))
    if goal == 1:
        add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))
    if goal == 2:
        if options.include_monster_tokens.value:
            add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.has(ItemNames.MT_PROGRESSIVE, player, options.token_count) and state.can_reach(RegionNames.s004, "Region", player))
        else:
            add_rule(multiworld.get_location(LocationNames.Credits, player),lambda state: state.can_reach(RegionNames.o001, "Region", player) and
                state.can_reach(RegionNames.w022, "Region", player) and state.can_reach(RegionNames.l013, "Region", player) and
                state.can_reach(RegionNames.o002, "Region", player) and                                    
                state.can_reach(RegionNames.i005, "Region", player) and state.can_reach(RegionNames.g005, "Region", player) and
                state.can_reach(RegionNames.f007, "Region", player) and state.can_reach(RegionNames.c005, "Region", player) and
                state.can_reach(RegionNames.i001, "Region", player) and state.can_reach(RegionNames.s003, "Region", player) and
                state.can_reach(RegionNames.s002, "Region", player) and state.can_reach(RegionNames.w025, "Region", player) and
                state.can_reach(RegionNames.g008, "Region", player) and state.can_reach(RegionNames.l014, "Region", player) and
                state.can_reach(RegionNames.b003, "Region", player) and state.can_reach(RegionNames.f004, "Region", player) and
                state.can_reach(RegionNames.e003, "Region", player) and state.can_reach(RegionNames.r020, "Region", player) and
                state.can_reach(RegionNames.e001, "Region", player) and state.can_reach(RegionNames.g002, "Region", player) and
                state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.SoapPower, player, 1) and
                state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.BootsPower, player, 1) and state.can_reach(RegionNames.s004, "Region", player))
    if goal == 3:
        if options.include_monster_tokens.value:
            add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.has(ItemNames.MT_PROGRESSIVE, player, options.token_count) and
                state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))
        else:
            add_rule(multiworld.get_location(LocationNames.Credits, player),lambda state: state.can_reach(RegionNames.o001, "Region", player) and
                state.can_reach(RegionNames.w022, "Region", player) and state.can_reach(RegionNames.l013, "Region", player) and
                state.can_reach(RegionNames.o002, "Region", player) and
                state.can_reach(RegionNames.i005, "Region", player) and state.can_reach(RegionNames.g005, "Region", player) and
                state.can_reach(RegionNames.f007, "Region", player) and state.can_reach(RegionNames.c005, "Region", player) and
                state.can_reach(RegionNames.i001, "Region", player) and state.can_reach(RegionNames.s003, "Region", player) and
                state.can_reach(RegionNames.s002, "Region", player) and state.can_reach(RegionNames.w025, "Region", player) and
                state.can_reach(RegionNames.g008, "Region", player) and state.can_reach(RegionNames.l014, "Region", player) and
                state.can_reach(RegionNames.b003, "Region", player) and state.can_reach(RegionNames.f004, "Region", player) and
                state.can_reach(RegionNames.e003, "Region", player) and state.can_reach(RegionNames.r020, "Region", player) and
                state.can_reach(RegionNames.e001, "Region", player) and state.can_reach(RegionNames.g002, "Region", player) and
                state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.SoapPower, player, 1) and
                state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.BootsPower, player, 1) and
                state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and
                state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))
    if goal == 4:
        if options.include_snacks.value:
            add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.has(ItemNames.Snack, player, options.snack_count) and state.can_reach(RegionNames.s004, "Region", player))
        else:
            add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1) and state.can_reach(RegionNames.s004, "Region", player))
    if goal == 5:
        if options.include_snacks.value:
            add_rule(multiworld.get_location(LocationNames.Credits, player),
                     lambda state: state.has(ItemNames.Snack, player, options.snack_count) and state.can_reach(LocationNames.boots_o008, "Location", player) and
                                   state.can_reach(LocationNames.umbrella_g009, "Location", player) and state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))
        else:
            add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))
    if goal == 6:
        if options.include_monster_tokens.value:
            if options.include_snacks.value:
                add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.has(ItemNames.MT_PROGRESSIVE, player, options.token_count) and state.has(ItemNames.Snack, player, options.snack_count) and state.can_reach(RegionNames.s004, "Region", player))
            else:
                add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.has(ItemNames.MT_PROGRESSIVE, player, options.token_count) and state.can_reach(RegionNames.s004, "Region", player))

        else:
            if options.include_snacks.value:
                add_rule(multiworld.get_location(LocationNames.Credits, player),lambda state: state.can_reach(RegionNames.o001, "Region", player) and
                    state.can_reach(RegionNames.w022, "Region", player) and state.can_reach(RegionNames.l013, "Region", player) and
                    state.can_reach(RegionNames.o002, "Region", player) and
                    state.can_reach(RegionNames.i005, "Region", player) and state.can_reach(RegionNames.g005, "Region", player) and
                    state.can_reach(RegionNames.f007, "Region", player) and state.can_reach(RegionNames.c005, "Region", player) and
                    state.can_reach(RegionNames.i001, "Region", player) and state.can_reach(RegionNames.s003, "Region", player) and
                    state.can_reach(RegionNames.s002, "Region", player) and state.can_reach(RegionNames.w025, "Region", player) and
                    state.can_reach(RegionNames.g008, "Region", player) and state.can_reach(RegionNames.l014, "Region", player) and
                    state.can_reach(RegionNames.b003, "Region", player) and state.can_reach(RegionNames.f004, "Region", player) and
                    state.can_reach(RegionNames.e003, "Region", player) and state.can_reach(RegionNames.r020, "Region", player) and
                    state.can_reach(RegionNames.e001, "Region", player) and state.can_reach(RegionNames.g002, "Region", player) and
                    state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.SoapPower, player, 1) and
                    state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.BootsPower, player, 1) and
                    state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and
                    state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.has(ItemNames.Snack, player, options.snack_count) and state.can_reach(RegionNames.s004, "Region", player))
            else:
                add_rule(multiworld.get_location(LocationNames.Credits, player),lambda state: state.can_reach(RegionNames.o001, "Region", player) and
                    state.can_reach(RegionNames.w022, "Region", player) and state.can_reach(RegionNames.l013, "Region", player) and
                    state.can_reach(RegionNames.o002, "Region", player) and
                    state.can_reach(RegionNames.i005, "Region", player) and state.can_reach(RegionNames.g005, "Region", player) and
                    state.can_reach(RegionNames.f007, "Region", player) and state.can_reach(RegionNames.c005, "Region", player) and
                    state.can_reach(RegionNames.i001, "Region", player) and state.can_reach(RegionNames.s003, "Region", player) and
                    state.can_reach(RegionNames.s002, "Region", player) and state.can_reach(RegionNames.w025, "Region", player) and
                    state.can_reach(RegionNames.g008, "Region", player) and state.can_reach(RegionNames.l014, "Region", player) and
                    state.can_reach(RegionNames.b003, "Region", player) and state.can_reach(RegionNames.f004, "Region", player) and
                    state.can_reach(RegionNames.e003, "Region", player) and state.can_reach(RegionNames.r020, "Region", player) and
                    state.can_reach(RegionNames.e001, "Region", player) and state.can_reach(RegionNames.g002, "Region", player) and
                    state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.SoapPower, player, 1) and
                    state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.BootsPower, player, 1) and
                    state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and
                    state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))
    if goal == 7:
        if options.include_monster_tokens.value:
            if options.include_snacks.value:
                add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.has(ItemNames.MT_PROGRESSIVE, player, options.token_count) and state.has(ItemNames.Snack, player, options.snack_count) and
                         state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))
            else:
                add_rule(multiworld.get_location(LocationNames.Credits, player), lambda state: state.has(ItemNames.MT_PROGRESSIVE, player, options.token_count) and
                state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))

        else:
            if options.include_snacks.value:
                add_rule(multiworld.get_location(LocationNames.Credits, player),lambda state: state.can_reach(RegionNames.o001, "Region", player) and
                    state.can_reach(RegionNames.w022, "Region", player) and state.can_reach(RegionNames.l013, "Region", player) and
                    state.can_reach(RegionNames.o002, "Region", player) and
                    state.can_reach(RegionNames.i005, "Region", player) and state.can_reach(RegionNames.g005, "Region", player) and
                    state.can_reach(RegionNames.f007, "Region", player) and state.can_reach(RegionNames.c005, "Region", player) and
                    state.can_reach(RegionNames.i001, "Region", player) and state.can_reach(RegionNames.s003, "Region", player) and
                    state.can_reach(RegionNames.s002, "Region", player) and state.can_reach(RegionNames.w025, "Region", player) and
                    state.can_reach(RegionNames.g008, "Region", player) and state.can_reach(RegionNames.l014, "Region", player) and
                    state.can_reach(RegionNames.b003, "Region", player) and state.can_reach(RegionNames.f004, "Region", player) and
                    state.can_reach(RegionNames.e003, "Region", player) and state.can_reach(RegionNames.r020, "Region", player) and
                    state.can_reach(RegionNames.e001, "Region", player) and state.can_reach(RegionNames.g002, "Region", player) and
                    state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.SoapPower, player, 1) and
                    state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.BootsPower, player, 1) and
                    state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and
                    state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.has(ItemNames.Snack, player, options.snack_count) and
                    state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))
            else:
                add_rule(multiworld.get_location(LocationNames.Credits, player),lambda state: state.can_reach(RegionNames.o001, "Region", player) and
                    state.can_reach(RegionNames.w022, "Region", player) and state.can_reach(RegionNames.l013, "Region", player) and
                    state.can_reach(RegionNames.o002, "Region", player) and
                    state.can_reach(RegionNames.i005, "Region", player) and state.can_reach(RegionNames.g005, "Region", player) and
                    state.can_reach(RegionNames.f007, "Region", player) and state.can_reach(RegionNames.c005, "Region", player) and
                    state.can_reach(RegionNames.i001, "Region", player) and state.can_reach(RegionNames.s003, "Region", player) and
                    state.can_reach(RegionNames.s002, "Region", player) and state.can_reach(RegionNames.w025, "Region", player) and
                    state.can_reach(RegionNames.g008, "Region", player) and state.can_reach(RegionNames.l014, "Region", player) and
                    state.can_reach(RegionNames.b003, "Region", player) and state.can_reach(RegionNames.f004, "Region", player) and
                    state.can_reach(RegionNames.e003, "Region", player) and state.can_reach(RegionNames.r020, "Region", player) and
                    state.can_reach(RegionNames.e001, "Region", player) and state.can_reach(RegionNames.g002, "Region", player) and
                    state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.SoapPower, player, 1) and
                    state.has(ItemNames.PlungerPower, player, 1) and state.has(ItemNames.BootsPower, player, 1) and
                    state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and
                    state.can_reach(LocationNames.gumpower_w028, "Location", player) and
                    state.can_reach(LocationNames.boots_o008, "Location", player) and state.can_reach(LocationNames.umbrella_g009, "Location", player) and state.can_reach(LocationNames.gumpower_w028, "Location", player) and state.can_reach(RegionNames.s004, "Region", player))

    if ItemNames.Keys not in allowed_loc_types:
        if ItemNames.MonsterTokens in allowed_loc_types:
            add_rule(multiworld.get_location(LocationNames.spacekook_token_b001, player), lambda state: state.has(ItemNames.SoapPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
        if ItemNames.Warps in allowed_loc_types:
            add_rule(multiworld.get_location(LocationNames.warp_gate_i003, player), lambda state: state.has(ItemNames.HelmetPower, player, 1))
        if ItemNames.Snacks in allowed_loc_types:
            add_rule(multiworld.get_location(LocationNames.i003_EX__CLUE__SNACKBOX1, player), lambda state: state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.i003_EX__CLUE__SNACKBOX5, player), lambda state: state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.i005_SN480, player), lambda state: state.has(ItemNames.ProgressiveJump, player, 1))

            add_rule(multiworld.get_location(LocationNames.p002_SNACK12, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SNACK120, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SNACK14, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SNACK16, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SNACK18, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_EX__CLUE__SNACKBOX__3, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SS12, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SS15, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SS18, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SS180, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SS181, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SS182, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SNACKBOX30, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SS13, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.p002_SS14, player), lambda state: state.has(ItemNames.PoundPower, player, 1) and state.has(ItemNames.HelmetPower, player, 1))


            add_rule(multiworld.get_location(LocationNames.o006_SSBOX05, player), lambda state: state.has(ItemNames.PlungerPower, player, 1) and state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S100, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S89, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S90, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S91, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S92, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S93, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S94, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S95, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S96, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S97, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S98, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_S99, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN1, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN10, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN11, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN12, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN13, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN14, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN15, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN16, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN17, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN18, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN19, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN2, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN20, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN21, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN22, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN23, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN24, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN25, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN26, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN27, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN28, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN29, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN3, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN30, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN31, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN32, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN33, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN34, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN35, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN38, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN39, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN4, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN42, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN44, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN45, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN46, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN47, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN48, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN49, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN5, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN50, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN51, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN52, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN53, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN54, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN55, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN56, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN57, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN58, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN59, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN6, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN60, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN61, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN62, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN63, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN64, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN65, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN66, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN67, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN68, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN69, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN7, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN70, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN71, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN72, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN73, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN74, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN75, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN76, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN77, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN78, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN79, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN8, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN80, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN81, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN82, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN83, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN84, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN85, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN86, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN87, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN88, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SN9, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SSBOX01, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SSBOX02, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SSBOX03, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SSBOX04, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
            add_rule(multiworld.get_location(LocationNames.o006_SSBOX05, player), lambda state: state.can_reach(RegionNames.o005, "Region", player) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))

        add_rule(multiworld.get_location(LocationNames.umbrella_g009, player), lambda state: state.has(ItemNames.PoundPower, player, 1))

        add_rule(multiworld.get_entrance(ConnectionNames.hub1_e001, player), lambda state: state.has(ItemNames.ProgressiveJump, player, 1))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_f001, player), lambda state: state.has(ItemNames.ShovelPower, player, 1))
        add_rule(multiworld.get_entrance(ConnectionNames.i003_i004, player), lambda state: state.has(ItemNames.HelmetPower, player, 1))
        add_rule(multiworld.get_entrance(ConnectionNames.g007_g008, player), lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
        add_rule(multiworld.get_entrance(ConnectionNames.c005_c006, player), lambda state: state.has(ItemNames.PlungerPower, player, 1))
        add_rule(multiworld.get_entrance(ConnectionNames.p002_p003, player), lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1))
        add_rule(multiworld.get_entrance(ConnectionNames.p003_p004, player), lambda state: state.has(ItemNames.GumPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 1))
        add_rule(multiworld.get_entrance(ConnectionNames.p004_p005, player), lambda state: state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PlungerPower, player, 1))
        add_rule(multiworld.get_entrance(ConnectionNames.p005_b001, player), lambda state: state.has(ItemNames.ProgressiveJump, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.p002_s001, player), lambda state: state.has(ItemNames.SoapPower, player, 1) and state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.HelmetPower, player, 1) and state.has(ItemNames.PoundPower, player, 1)),

    if ItemNames.Warps not in allowed_loc_types:
        # Warps, but not accessible logically
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_b004, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_c004, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_e004, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_e006, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_e009, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_f003, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_f007, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_o001, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_o004, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_o006, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_g001, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_g005, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_g008, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_i003, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_i006, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_l014, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_l015, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_l018, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_p003, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_p005, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_r003, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_s002, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_w022, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))
        add_rule(multiworld.get_entrance(ConnectionNames.hub1_w026, player), lambda state: state.has(ItemNames.ShockwavePower, player, 2))

    if options.advanced_logic.value:
        add_rule(multiworld.get_entrance(ConnectionNames.e004_e005, player), lambda state: state.can_reach(RegionNames.e004, "Region", player))
        add_rule(multiworld.get_entrance(ConnectionNames.e006_e005, player), lambda state: state.can_reach(RegionNames.e006, "Region", player))
        add_rule(multiworld.get_entrance(ConnectionNames.e003_c005, player), lambda state: state.can_reach(RegionNames.e003, "Region", player))
        add_rule(multiworld.get_entrance(ConnectionNames.w026_w028, player), lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.GumPower, player, 1))

        if options.include_monster_tokens.value:
            add_rule(multiworld.get_location(LocationNames.moody_token_w022, player), lambda state: state.has(ItemNames.ProgressiveJump, player, 2) and state.has(ItemNames.PoundPower, player, 1))
            add_rule(multiworld.get_location(LocationNames.moody_token_w022, player), lambda state: state.has(ItemNames.ProgressiveJump, player, 1) and (state.has(ItemNames.GumPower, player, 1) or state.has(ItemNames.SoapPower, player, 1)))
            add_rule(multiworld.get_location(LocationNames.headless_token_i001, player), lambda state: state.can_reach(RegionNames.i001, "Region", player))
            add_rule(multiworld.get_location(LocationNames.ghost_token_g005, player), lambda state: state.can_reach(RegionNames.g005, "Region", player))
            add_rule(multiworld.get_location(LocationNames.scarecrow_token_g008, player), lambda state: state.can_reach(RegionNames.g008, "Region", player))

        if options.include_keys.value:
            add_rule(multiworld.get_location(LocationNames.key1_w027, player), lambda state: state.can_reach(RegionNames.w027, "Region", player))
            add_rule(multiworld.get_location(LocationNames.key2_w027, player), lambda state: state.can_reach(RegionNames.w027, "Region", player))
            add_rule(multiworld.get_location(LocationNames.key3_w027, player), lambda state: state.can_reach(RegionNames.w027, "Region", player))
            add_rule(multiworld.get_location(LocationNames.key4_w027, player), lambda state: state.has(ItemNames.PoundPower, player, 1))

    else:
        add_rule(multiworld.get_entrance(ConnectionNames.b004_i003, player), lambda state: state.has(ItemNames.HelmetPower, player, 1))
        add_rule(multiworld.get_entrance(ConnectionNames.e003_c005, player), lambda state: state.can_reach(RegionNames.c005, "Region", player))
        
    if options.expert_logic.value:
        add_rule(multiworld.get_entrance(ConnectionNames.e002_e003, player), lambda state: state.can_reach(RegionNames.e002, "Region", player))
        add_rule(multiworld.get_entrance(ConnectionNames.w026_w028, player), lambda state: state.has(ItemNames.ProgressiveJump, player, 2))

    if options.creepy_early.value:
        add_rule(multiworld.get_entrance(ConnectionNames.f003_p001, player), lambda state: state.has(ItemNames.ProgressiveJump, player, 1))
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)
