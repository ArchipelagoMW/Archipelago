from test.bases import WorldTestBase


class PokemonBWTestBase(WorldTestBase):
    game = "Pokemon Black and White"


###################################################
# Goal                                            #
###################################################


class TestGoalChampion(PokemonBWTestBase):
    options = {"goal": "champion"}


class TestGoalCynthia(PokemonBWTestBase):
    options = {"goal": "cynthia"}


class TestGoalCobalion(PokemonBWTestBase):
    options = {"goal": "cobalion"}


class TestGoalTMHMHunt(PokemonBWTestBase):
    options = {"goal": "tmhm_hunt"}


class TestGoalSevenSagesHunt(PokemonBWTestBase):
    options = {"goal": "seven_sages_hunt"}


class TestGoalLegendaryHunt(PokemonBWTestBase):
    options = {"goal": "legendary_hunt"}


class TestGoalPokemonMaster(PokemonBWTestBase):
    options = {"goal": "pokemon_master"}


###################################################
# Randomize Trainer Pokemon                       #
###################################################


class TestRandomizeTrainerPokemonSimple(PokemonBWTestBase):
    options = {
        "randomize_trainer_pokemon": ["Randomize"],
    }


class TestRandomizeTrainerPokemonStats(PokemonBWTestBase):
    options = {
        "randomize_trainer_pokemon": ["Randomize", "Similar base stats"],
    }


###################################################
# Encounter Plando                                #
###################################################


class TestEncounterPlandoEmpty(PokemonBWTestBase):
    options = {"encounter_plando": []}


class TestEncounterPlandoAllParameters(PokemonBWTestBase):
    options = {
        "encounter_plando": [
            {
                "map": "Route 1",
                "method": "Grass",
                "species": "Kyogre",
            },
            {
                "map": "Route 8",
                "seasons": "Summer",
                "method": "Surfing",
                "slots": 1,
                "species": ["Charmander", "Squirtle", "Bulbasaur"],
            },
            {
                "map": "Icirrus City",
                "seasons": ["Summer", "Winter"],
                "method": "Surfing",
                "slots": [1, 3, 4],
                "species": "Blastoise",
            },
            {
                "map": "Route 16",
                "method": "Grass",
                "species": "None",
            },
        ],
    }


class TestEncounterPlandoRandomize(PokemonBWTestBase):
    options = {
        "encounter_plando": [
            {
                "map": "Route 1",
                "method": "Grass",
                "species": "Kyogre",
            },
            {
                "map": "Route 2",
                "method": "Rustling grass",
                "species": "Groudon",
            },
        ],
        "randomize_wild_pokemon": ["Randomize"],
    }


class TestEncounterPlandoRandomizeAllObtainable(PokemonBWTestBase):
    options = {
        "encounter_plando": [
            {
                "map": "Route 1",
                "method": "Grass",
                "species": "Kyogre",
            },
            {
                "map": "Route 2",
                "method": "Rustling grass",
                "species": "Groudon",
            },
        ],
        "randomize_wild_pokemon": ["Randomize", "Ensure all obtainable"],
    }


###################################################
# Shuffle Badges                                  #
###################################################


class TestShuffleBadgesVanilla(PokemonBWTestBase):
    options = {"shuffle_badges": "vanilla"}


class TestShuffleBadgesAnybadge(PokemonBWTestBase):
    options = {"shuffle_badges": "any_badge"}


class TestShuffleBadgesAnything(PokemonBWTestBase):
    options = {"shuffle_badges": "anything"}


###################################################
# Shuffle TM/HM                                   #
###################################################


class TestShuffleTMHMHMWithBadge(PokemonBWTestBase):
    options = {"shuffle_tm_hm": "hm_with_badge"}


class TestShuffleTMHMAnyTMHM(PokemonBWTestBase):
    options = {"shuffle_tm_hm": "any_tm_hm"}


class TestShuffleTMHMAnything(PokemonBWTestBase):
    options = {"shuffle_tm_hm": "anything"}


###################################################
# Dexsanity                                       #
###################################################


class TestDexsanityPartial(PokemonBWTestBase):
    options = {"dexsanity": 100}


class TestDexsanityFull(PokemonBWTestBase):
    options = {
        "dexsanity": 649,
        "randomize_wild_pokemon": ["Randomize", "Ensure all obtainable"],
    }


###################################################
# Season Control                                  #
###################################################


class TestSeasonControlChangeable(PokemonBWTestBase):
    options = {"season_control": "changeable"}


class TestSeasonControlRandomized(PokemonBWTestBase):
    options = {"season_control": "randomized"}


###################################################
# Modify Encounter Rates                          #
###################################################


class TestModifyEncounterRatesTryNormalized(PokemonBWTestBase):
    options = {"modify_encounter_rates": "try_normalized"}


class TestModifyEncounterRatesTryNormalizedAlt(PokemonBWTestBase):
    options = {"modify_encounter_rates": "try_normalized_alt"}


class TestModifyEncounterRatesInvasive(PokemonBWTestBase):
    options = {"modify_encounter_rates": "invasive"}


class TestModifyEncounterRatesRandomized12(PokemonBWTestBase):
    options = {"modify_encounter_rates": "randomized_12"}


class TestModifyEncounterRatesCustom(PokemonBWTestBase):
    options = {"modify_encounter_rates": {
        "Grass": [12, 23, 4, 6, 18, 1, 6, 5, 5, 7, 7, 6],
        "Fishing": [21, 19, 22, 18, 20],
    }}


###################################################
# Modify Item Pool                                #
###################################################


class TestModifyItemPoolAll(PokemonBWTestBase):
    options = {"modify_item_pool": ["Useless key items", "Useful filler", "Ban bad filler"]}


###################################################
# Modify Logic                                    #
###################################################


class TestModifyLogicNone(PokemonBWTestBase):
    options = {"modify_logic": []}
