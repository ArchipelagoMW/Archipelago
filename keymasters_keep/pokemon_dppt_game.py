from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PokemonDPPtArchipelagoOptions:
    pokemon_dppt_owned_games: PokemonDPPtOwnedGames
    pokemon_dppt_objectives: PokemonDPPtObjectives
    pokemon_dppt_daily_encounters: PokemonDPPtDailyEncounters


class PokemonDPPtGame(Game):
    # Initial implementation by Seafo
    # Based on soopercool101's Pokémon RSE implementation

    name = "Pokémon Diamond, Pearl, and Platinum Versions"
    platform = KeymastersKeepGamePlatforms.NDS

    is_adult_only_or_unrated = False

    options_cls = PokemonDPPtArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use POKEMON as your lead whenever possible",
                data={
                    "POKEMON": (self.wild_pokemon, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Use POKEMON as your lead whenever possible",
                data={
                    "POKEMON": (self.wild_pokemon, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Use POKEMON as your lead whenever possible",
                data={
                    "POKEMON": (self.available_pokemon, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Use POKEMON as your lead whenever possible",
                data={
                    "POKEMON": (self.difficult_pokemon, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Only use the following Pokémon (unless otherwise needed for HMs or specific challenges): PKMON",
                data={
                    "PKMON": (self.wild_pokemon, 6)
                },
            ),
            GameObjectiveTemplate(
                label="Only use the following Pokémon (unless otherwise needed for HMs or specific challenges): PKMON",
                data={
                    "PKMON": (self.available_pokemon, 6)
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = list()
        if self.objective_catching:
            objectives += self.catching_objectives()
        if self.objective_contests:
            objectives += self.contest_objectives()
        if self.objective_battles:
            objectives += self.battle_objectives()
        if self.objective_battle_frontier:
            objectives += self.battle_frontier_objectives()
        if self.objective_shiny_hunting:
            objectives += self.shiny_hunting_objectives()
        if self.objective_underground:
            objectives += self.underground_objectives()
        if len(objectives) == 0:  # Fallback default objectives. Better versions of these exist in other categories
            objectives += [
                GameObjectiveTemplate(
                    label="Without using Fly, travel between the following cities: CITY",
                    data={
                        "CITY": (self.cities, 2)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=20
                ),
                GameObjectiveTemplate(
                    label="Without using Fly, travel between the following locations: LOCATION",
                    data={
                        "LOCATION": (self.locations, 2)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=10
                ),
                GameObjectiveTemplate(
                    label="Encounter a wild POKEMON",
                    data={
                        "POKEMON": (self.wild_pokemon, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Encounter a wild Pokémon in LOCATION",
                    data={
                        "LOCATION": (self.encounter_locations, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=70
                ),
                GameObjectiveTemplate(
                    label="Encounter a wild HONEYPOKEMON",
                    data={
                        "HONEYPOKEMON": (self.wild_honey_tree, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=10
                ),
                GameObjectiveTemplate(
                    label="Encounter a wild RAREPOKEMON",
                    data={
                        "RAREPOKEMON": (self.rare_wild_pokemon, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=3
                )
            ]

            if self.daily_encounters:
                objectives.extend([
                    GameObjectiveTemplate(
                        label="Encounter a wild DAILYPOKEMON",
                        data={
                            "DAILYPOKEMON": (self.daily_wild_pokemon, 1)
                        },
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=3
                    ),
                    GameObjectiveTemplate(
                        label="Encounter a wild Drifloon",
                        data=dict(),
                        is_time_consuming=True,
                        is_difficult=False,
                        weight=1
                    ),
                ])

        return objectives

    def catching_objectives(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Catch a wild POKEMON CONDITION",
                data={
                    "POKEMON": (self.wild_pokemon, 1),
                    "CONDITION": (self.pokemon_catch_conditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=90,
            ),
            GameObjectiveTemplate(
                label="Catch a wild HONEYPOKEMON CONDITION",
                data={
                    "HONEYPOKEMON": (self.wild_honey_tree, 1),
                    "CONDITION": (self.pokemon_catch_conditions, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5
            ),
            GameObjectiveTemplate(
                label="Catch a wild RAREPOKEMON CONDITION",
                data={
                    "RAREPOKEMON": (self.rare_wild_pokemon, 1),
                    "CONDITION": (self.pokemon_catch_conditions, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Catch a wild Pokémon in LOCATION CONDITION",
                data={
                    "LOCATION": (self.encounter_locations, 1),
                    "CONDITION": (self.pokemon_catch_conditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=90,
            ),
            GameObjectiveTemplate(
                label="Catch a swarming wild Pokémon CONDITION",
                data={
                    "CONDITION": (self.pokemon_catch_conditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=30,
            ),
            GameObjectiveTemplate(
                label="Catch a wild POKEMON in the Great Marsh CONDITION",
                data={
                    "POKEMON": (self.marsh_pokemon, 1),
                    "CONDITION": (self.marsh_catch_conditions, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=35,
            ),
            GameObjectiveTemplate(
                label="Catch a wild Pokémon on a Honey Tree CONDITION",
                data={
                    "CONDITION": (self.pokemon_catch_conditions, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=25,
            ),
        ]

        if self.daily_encounters:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Catch a wild DAILYPOKEMON CONDITION",
                    data={
                        "DAILYPOKEMON": (self.daily_wild_pokemon, 1),
                        "CONDITION": (self.pokemon_catch_conditions, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3
                ),
                GameObjectiveTemplate(
                    label="Catch a wild Drifloon CONDITION",
                    data={
                        "CONDITION": (self.pokemon_catch_conditions, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1
                ),
                GameObjectiveTemplate(
                    label="Catch a wild DAILYPOKEMON in the Great Marsh CONDITION",
                    data={
                        "DAILYPOKEMON": (self.daily_marsh_pokemon, 1),
                        "CONDITION": (self.marsh_catch_conditions, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            ])

        return objectives

    def contest_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Make a TYPE Poffin",
                data={
                    "TYPE": (self.common_poffin_types, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=50,
            ),
            GameObjectiveTemplate(
                label="Make a TYPE Poffin",
                data={
                    "TYPE": (self.rare_poffin_types, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Win a Normal Rank TYPE",
                data={
                    "TYPE": (self.contest_types, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=30,
            ),
            GameObjectiveTemplate(
                label="Win a Great Rank TYPE",
                data={
                    "TYPE": (self.contest_types, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=20,
            ),
            GameObjectiveTemplate(
                label="Win an Ultra Rank TYPE",
                data={
                    "TYPE": (self.contest_types, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Win a Master Rank TYPE",
                data={
                    "TYPE": (self.contest_types, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=10,
            ),
        ]

    def battle_objectives(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Defeat a wild POKEMON CONDITION",
                data={
                    "POKEMON": (self.wild_pokemon, 1),
                    "CONDITION": (self.wild_battle_conditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=70,
            ),
            GameObjectiveTemplate(
                label="Defeat a wild HONEYPOKEMON CONDITION",
                data={
                    "HONEYPOKEMON": (self.wild_honey_tree, 1),
                    "CONDITION": (self.wild_battle_conditions, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=10
            ),
            GameObjectiveTemplate(
                label="Without using Fly, items, or a Pokémon Center, travel between the following cities "
                      "and defeat every wild encounter you see: CITY",
                data={
                    "CITY": (self.cities, 2)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=35,
            ),
            GameObjectiveTemplate(
                label="Without using Fly, items, or a Pokémon Center, travel between the following locations "
                      "and defeat every wild encounter you see: LOCATION",
                data={
                    "LOCATION": (self.locations, 2)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=25,
            ),
            GameObjectiveTemplate(
                label="Win any Vs. Seeker rematch CONDITION",
                data={
                    "CONDITION": (self.easy_trainer_battle_conditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=35,
            ),
            GameObjectiveTemplate(
                label="Defeat the Pokémon League and enter the Hall of Fame CONDITION",
                data={
                    "CONDITION": (self.pokemon_league_battle_conditions, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=50,
            ),
        ]

        if self.has_platinum:
            objectives.append(
                GameObjectiveTemplate(
                    label="Win any battle in the Battleground CONDITION",
                    data={
                        "CONDITION": (self.hard_trainer_battle_conditions, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=5,
                ),
            )

        return objectives

    def battle_frontier_objectives(self) -> List[GameObjectiveTemplate]:
        if self.has_platinum:
            return [
                GameObjectiveTemplate(
                    label="Win 7 battles in a row in the FACILITY",
                    data={
                        "FACILITY": (self.battle_frontier_facilities, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=60,
                ),
                GameObjectiveTemplate(
                    label="Win 10 battles in a row in the Battle Hall",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=15,
                ),
                GameObjectiveTemplate(
                    label="Win a battle against BRAIN",
                    data={
                        "BRAIN": (self.battle_frontier_brains, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=5,
                ),
            ]
        else:
            return [
                GameObjectiveTemplate(
                    label="Win 7 battles in a row in the Battle Tower",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=15,
                ),
                GameObjectiveTemplate(
                    label="Win a battle against Tower Tycoon Palmer",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ]

    def underground_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Mine ITEM in the Underground CONDITION",
                data={
                    "ITEM": (self.underground_items, 1),
                    "CONDITION": (self.underground_conditions, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=70,
            ),
            GameObjectiveTemplate(
                label="Mine RAREITEM in the Underground CONDITION",
                data={
                    "RAREITEM": (self.rare_underground_items, 1),
                    "CONDITION": (self.underground_conditions, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=30,
            ),
            GameObjectiveTemplate(
                label="Without using Fly, travel from LOCATION to the REGION area of the Underground",
                data={
                    "LOCATION": (self.locations, 1),
                    "REGION": (self.underground_areas, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=20,
            ),
            # Might add additional conditions to these in the future
            GameObjectiveTemplate(
                label="Obtain a decoration and put it in your Secret Base",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Purchase something from a trader in the Underground",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Dig up a trap in the Underground",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
        ]

    def shiny_hunting_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Encounter or obtain a shiny POKEMON",
                data={
                    "POKEMON": (self.wild_pokemon, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Encounter a shiny Pokémon in LOCATION",
                data={
                    "LOCATION": (self.encounter_locations_with_marsh, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Catch any wild shiny Pokémon",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
        ]

    @property
    def games_owned(self) -> Set[str]:
        return self.archipelago_options.pokemon_dppt_owned_games.value

    @property
    def has_diamond(self) -> bool:
        return "Diamond" in self.games_owned

    @property
    def has_pearl(self) -> bool:
        return "Pearl" in self.games_owned

    @property
    def has_platinum(self) -> bool:
        return "Platinum" in self.games_owned

    @property
    def objectives(self) -> Set[str]:
        return self.archipelago_options.pokemon_dppt_objectives.value

    @property
    def objective_catching(self) -> bool:
        return "Catching" in self.objectives

    @property
    def objective_contests(self) -> bool:
        return "Contests" in self.objectives

    @property
    def objective_battles(self) -> bool:
        return "Battles" in self.objectives

    @property
    def objective_battle_frontier(self) -> bool:
        return "Battle Frontier" in self.objectives

    @property
    def objective_underground(self) -> bool:
        return "Underground" in self.objectives

    @property
    def objective_shiny_hunting(self) -> bool:
        return "Shiny Hunting" in self.objectives

    @property
    def time_consuming(self) -> bool:
        if (self.include_time_consuming_objectives
            and "Pokémon Diamond, Pearl, and Platinum Versions (NDS)"
                not in self.archipelago_options.excluded_games_time_consuming_objectives):
            return True
        else:
            return False

    # Unused
    # @property
    # def difficult(self) -> bool:
    #     if (self.include_time_consuming_objectives
    #         and "Pokémon Diamond, Pearl, and Platinum Versions (NDS)"
    #             not in self.archipelago_options.excluded_games_difficult_objectives):
    #         return True
    #     else:
    #         return False

    @property
    def daily_encounters(self) -> bool:
        return bool(self.archipelago_options.pokemon_dppt_daily_encounters.value)

    def available_pokemon(self) -> List[str]:
        pokemon: List[str] = self.wild_pokemon()[:]
        pokemon.extend(self.difficult_pokemon()[:])
        return pokemon

    def wild_pokemon(self) -> List[str]:
        # List fully in common with all three games
        pokemon: List[str] = self.wild_dppt()[:]

        # Full version exclusives
        if self.has_diamond:
            pokemon.extend(self.wild_d()[:])
        if self.has_pearl:
            pokemon.extend(self.wild_p()[:])
        if self.has_platinum:
            pokemon.extend(self.wild_pt()[:])

        # Exclusive to two games
        if self.has_diamond or self.has_pearl:
            pokemon.extend(self.wild_dp()[:])
        if self.has_diamond or self.has_platinum:
            pokemon.extend(self.wild_dpt()[:])
        if self.has_pearl or self.has_platinum:
            pokemon.extend(self.wild_ppt()[:])

        # Locked behind a certain time of day
        if self.time_consuming:
            pokemon.extend(self.wild_time_dppt()[:])
        if self.has_diamond and self.time_consuming:
            pokemon.append("Murkrow")
        if self.has_pearl and self.time_consuming:
            pokemon.extend("Misdreavus")
        # Everything uniquely time-locked in Platinum isn't time-locked in Diamond and Pearl
        if not self.has_diamond and not self.has_pearl and self.time_consuming:
            pokemon.extend(self.wild_time_pt()[:])

        return pokemon

    def daily_wild_pokemon(self) -> List[str]:
        pokemon: List[str] = self.wild_daily_dppt()[:]

        # Platinum makes a lot of Pokémon that were Swarm/Trophy Garden exclusives into regular encounters
        if not self.has_platinum:
            pokemon.extend(self.wild_daily_dp()[:])
        # Special cases for individual Pokémon
        if self.has_diamond or self.has_pearl:
            pokemon.append("Porygon")  # Trophy Garden encounter; not in Platinum
        if not self.has_diamond and not self.has_pearl:
            pokemon.append("Ditto")  # PokéRadar in Diamond and Pearl; Trophy Garden in Platinum
        if not self.has_diamond:
            pokemon.append("Mime Jr.")  # Wild in Diamond; Trophy Garden in Pearl and Platinum
        if not self.has_pearl:
            pokemon.append("Bonsly")  # Wild in Pearl; Trophy Garden in Diamond and Platinum
        if not self.has_diamond and self.has_platinum:
            pokemon.append("Larvitar")  # PokéRadar in Diamond; Swarm in Platinum; not in Pearl
        if not self.has_pearl and self.has_platinum:
            pokemon.append("Pinsir")  # Wild in Pearl; Swarm in Platinum; not in Diamond
        # Extra special case; handled separately
        # if self.difficult:
        #     pokemon.append("Drifloon")  # Only one available each Friday

        return pokemon

    @staticmethod
    def rare_wild_pokemon() -> List[str]:
        pokemon: List[str] = [
            "Munchlax",
            "Heracross",
            "Feebas",
        ]

        return pokemon

    def difficult_pokemon(self) -> List[str]:
        pokemon: List[str] = self.daily_wild_pokemon()[:]
        pokemon.extend(self.rare_wild_pokemon()[:])
        # Evolutions, Breeding, and other rare repeatable Pokémon
        pokemon.extend([
            # Evolution exclusive
            "Pidgeotto",
            "Pidgeot",
            "Raichu",
            "Nidoqueen",
            "Nidoking",
            "Clefable",
            "Wigglytuff",
            "Crobat",
            "Vileplume",
            "Bellossom",
            "Parasect",
            "Persian",
            "Poliwrath",
            "Victreebel",
            "Rapidash",
            "Magnezone",
            "Dodrio",
            "Muk",
            "Cloyster",
            "Hypno",
            "Kingler",
            "Electrode",
            "Exeggutor",
            "Marowak",
            "Hitmonlee",
            "Hitmonchan",
            "Hitmontop",
            "Lickilicky",
            "Blissey",
            "Starmie",
            "Vaporeon",
            "Jolteon",
            "Flareon",
            "Espeon",
            "Umbreon",
            "Leafeon",
            "Glaceon",
            "Omastar",
            "Kabutops",
            "Snorlax",
            "Dragonite",
            "Furret",
            "Togetic",
            "Togekiss",
            "Xatu",
            "Ampharos",
            "Jumpluff",
            "Ambipom",
            "Sunflora",
            "Yanmega",
            "Granbull",
            "Weavile",
            "Mamoswine",
            "Mantine",
            "Donphan",
            "Linoone",
            "Gardevoir",
            "Gallade",
            "Breloom",
            "Vigoroth",
            "Slaking",
            "Ninjask",
            "Shedinja",
            "Exploud",
            "Hariyama",
            "Probopass",
            "Delcatty",
            "Manectric",
            "Roserade",
            "Swalot",
            "Grumpig",
            "Altaria",
            "Claydol",
            "Cradily",
            "Armaldo",
            "Milotic",
            "Glalie",
            "Froslass",
            "Metang",
            "Metagross",
            "Staraptor",
            "Luxray",
            "Wormadam",
            "Mothim",
            "Vespiquen",
            "Cherrim",
            "Drifblim",
            "Lopunny",
            "Garchomp",

            # Daily Great Marsh encounters
            "Paras",
            "Exeggcute",
            "Kangaskhan",
            "Shroomish",
            "Gulpin",
            "Skorupi",
            "Drapion",
            "Toxicroak",
            "Carnivine",

            # Revived from a fossil
            "Omanyte",
            "Kabuto",
            "Aerodactyl",
            "Lileep",
            "Anorith",

            # Breeding exclusive
            "Ledyba",
            "Spinarak",
            # "Wynaut",  # Technically not obtainable if you sell the Lax Incense
            "Taillow",
            "Whismur",
            "Shuppet",

            # Great Marsh exclusives
            "Yanma",
            "Carvanha",

            # Date-based
            "Drifloon",
        ][:])

        if not self.time_consuming:
            pokemon.extend([
                # Time-based
                "Hoothoot",
                "Noctowl",
                "Ledian",
                "Ariados",
                "Banette",
                "Kricketot",
                "Chatot",
            ][:])

        if self.has_diamond:
            pokemon.extend([
                # Evolution-only
                "Honchkrow",
                "Rampardos",
                # Fossil-only; unreliable availability in Platinum
                "Cranidos",
            ][:])

        if self.has_diamond and not self.time_consuming:
            pokemon.append("Murkrow")  # Time-based

        if self.has_pearl:
            pokemon.extend([
                # Evolution-only
                "Mismagius",
                "Bastiodon",
                # Fossil-only; unreliable availability in Platinum
                "Shieldon",
            ][:])

        if self.has_pearl and not self.time_consuming:
            pokemon.append("Misdreavus")  # Time-based

        if self.has_diamond or self.has_pearl:
            pokemon.append("Flygon")  # Evolution-only

        if self.has_diamond or self.has_platinum:
            pokemon.extend([
                # Evolution-only
                "Pupitar",
                "Tyranitar",
                "Lairon",
                "Aggron",
            ][:])

        if self.has_pearl or self.has_platinum:
            pokemon.extend([
                # Evolution-only
                "Slowbro",
                "Walrein",
                "Shelgon",
                "Salamence",
            ][:])

        if self.has_platinum:
            pokemon.extend([
                # Great Marsh-only
                "Tangela",
                "Tropius",
                # Evolution-only
                "Tangrowth",
                # Breeding exclusive
                "Elekid",
                "Magby",
            ][:])

        if not self.has_diamond and not self.has_pearl:
            pokemon.extend([
                # Evolution-only in Platinum
                "Lanturn",
                "Skiploom",  # PokéRadar in Diamond and Pearl
                "Sharpedo",
                # Great Marsh-only in Platinum
                "Wooper",
            ][:])

        if not self.has_diamond and not self.has_pearl and not self.time_consuming:
            pokemon.extend([
                # Time-based in Platinum
                "Cleffa",
                "Clefairy",
                "Oddish",
                "Bellsprout",
                "Wurmple",
                "Kricketune",
            ][:])

        if not self.has_diamond and not self.has_platinum:
            pokemon.extend([
                # Evolution-only in Pearl
                "Mr. Mime",
                "Silcoon",
            ][:])

        if not self.has_pearl and not self.has_platinum:
            pokemon.extend([
                # Evolution-only in Diamond
                "Sudowoodo",
                "Cascoon",
                "Dustox",
            ][:])

        if not self.has_platinum:
            pokemon.extend([
                # Evolution-only outside of Platinum
                "Magneton",
                "Jynx",
                "Azumarill",
                "Piloswine",  # PokéRadar in Platinum
                "Masquerain",
                "Gabite",
                # Breeding exclusive outside of Platinum
                "Koffing",
                # Great Marsh-only outside of Platinum
                "Croagunk",
            ][:])

        if self.has_diamond and not self.has_platinum:
            pokemon.append("Poochyena")  # Breeding exclusive in Diamond; PokéRadar in Platinum

        if self.has_pearl and not self.has_platinum:
            pokemon.append("Houndour")  # Breeding exclusive in Pearl

        if not self.has_diamond and self.has_platinum:
            pokemon.extend([
                "Seel",  # Breeding exclusive in Platinum
                "Mightyena",  # PokéRader exclusive in Diamond; Evolution-only in Platinum
                "Kecleon",  # PokéRader exclusive in Diamond; Great Marsh-only in Platinum
            ][:])

        if not self.has_pearl and self.has_platinum:
            pokemon.extend([
                "Houndoom",  # PokéRader exclusive in Diamond; Evolution-only in Platinum
                "Spheal",  # Breeding exclusive in Platinum
            ][:])

        return pokemon

    def marsh_pokemon(self) -> List[str]:
        pokemon: List[str] = self.marsh_dppt()[:]

        if self.has_diamond or self.has_pearl:
            pokemon.extend(self.marsh_dp())

        if self.has_platinum:
            pokemon.extend(self.marsh_pt()[:])

        return pokemon

    def daily_marsh_pokemon(self) -> List[str]:
        pokemon: List[str] = self.marsh_daily_dppt()[:]

        if self.has_diamond or self.has_pearl:
            pokemon.extend(self.marsh_daily_dp()[:])

        if not self.has_platinum:
            pokemon.append("Yanma")

        if self.has_platinum:
            pokemon.append("Kecleon")

        return pokemon

    @staticmethod
    def pokemon_catch_conditions() -> List[str]:
        return [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "without using False Swipe",
            "without using status moves",
            "without damaging it",
            "without damaging it or using status moves",
            "in a Poké Ball",
            "in a Great Ball",
            "in a Ultra Ball",
            "in a Net Ball",
            # "in a Dive Ball",
            "in a Nest Ball",
            "in a Repeat Ball",
            "in a Timer Ball",
            "in a Luxury Ball",
            "in a Premier Ball",
            "in a Dusk Ball",
            "in a Heal Ball",
            "in a Quick Ball",
            # Dive and Master Balls *can* be found infinitely, but are too annoying
        ]

    @staticmethod
    def marsh_catch_conditions() -> List[str]:
        return [
            "",
            "",
            "",
            "",
            "",
            "",
            "without throwing bait",
            "without throwing mud",
            "without using Sweet Scent",
        ]

    @staticmethod
    def base_trainer_battle_conditions() -> List[str]:
        return [
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "using only one Pokémon",
            "without using items in battle",
            "without using healing items",
            "without any of your Pokémon fainting",
            "without using STAB moves",
            "without using Super-Effective moves",
            "without using status moves",
            "without using physical moves",
            "without using special moves",
            "without using any moves over 40 Power",
            "without using any moves over 60 Power",
            "without using any moves with 100 accuracy or moves that bypass accuracy checks",
            "without using any Pokémon with a Base Stat Total over 500",
            "without using legendary Pokémon",
            "only using Pokémon that can still evolve",
            "using no more Pokémon than your opponent"
        ]

    def easy_trainer_battle_conditions(self) -> List[str]:
        conditions: List[str] = self.base_trainer_battle_conditions()[:]
        conditions.extend([
            "without taking damage",
            "without using any Pokémon higher than level 30",
            "without using any Pokémon with a Base Stat Total over 400",
            "only using Pokémon that can still evolve twice",
        ][:])
        return conditions

    def hard_trainer_battle_conditions(self) -> List[str]:
        conditions: List[str] = self.base_trainer_battle_conditions()[:]
        conditions.extend([
            "without taking damage",
            "without using any Pokémon higher than level 50",
            "without using any Pokémon higher than level 60",
        ][:])
        return conditions

    def pokemon_league_battle_conditions(self) -> List[str]:
        conditions: List[str] = self.base_trainer_battle_conditions()[:]
        conditions.extend([
            "without taking damage",
            "without using any Pokémon higher than level 60",
        ][:])

        if self.has_diamond or self.has_pearl:
            conditions.append("without using any Pokémon higher than level 50")

        if self.has_platinum:
            conditions.append("without using any Pokémon higher than level 70")

        return conditions

    @staticmethod
    def wild_battle_conditions() -> List[str]:
        return [
            "",
            "",
            "",
            "without using a Pokémon higher than level 30",
            "without taking damage",
            "without using STAB moves",
            "without using Super-Effective moves",
            "without using any moves over 40 Power",
            "without using any moves with 100 accuracy or moves that bypass accuracy checks",
            "only using Pokémon that can still evolve",
            "only using Pokémon that can still evolve twice",
        ]

    @staticmethod
    def underground_conditions() -> List[str]:
        return [
            "",
            "",
            "",
            "",
            "",
            "without letting the wall collapse",
            "while only using the Pick",
            "while only using the Hammer",
        ]

    def underground_items(self) -> List[str]:
        items: List[str] = [
            "two items",
            "three items",
            "four items",
            "a Prism Sphere",
            "a Pale Sphere",
            "a Red Sphere",
            "a Blue Sphere",
            "a Green Sphere",
            "a Hard Stone",
            "an Everstone",
            "a Red Shard",
            "a Blue Shard",
            "a Yellow Shard",
            "a Green Shard",
            "a Heart Scale",
            # Might move to rare?
            "a Star Piece",
            "a Rare Bone",
            "a Revive",
        ]

        if self.has_diamond:
            items.extend([
                "a Sun Stone",
                "a Thunder Stone",
                "a Fire Stone",
            ][:])

        if self.has_pearl:
            items.extend([
                "a Moon Stone",
                "a Leaf Stone",
                "a Water Stone",
                "a Damp Rock",
            ][:])

        return items

    def rare_underground_items(self) -> List[str]:
        items: List[str] = [
            "an Odd Keystone",
            "a Helix Fossil",
            "a Dome Fossil",
            "a Claw Fossil",
            "a Root Fossil",
            "an Old Amber",
            "a Max Revive",
            "a Light Clay",
            "an Iron Ball",
            "a Smooth Rock",
            "an Icy Rock",
            "a Smooth Rock",
            "a Heat Rock",
        ]

        if not self.has_diamond:
            items.extend([
                "a Sun Stone",
                "a Thunder Stone",
                "a Fire Stone",
            ][:])

        if not self.has_pearl:
            items.extend([
                "a Moon Stone",
                "a Leaf Stone",
                "a Water Stone",
                "a Damp Rock",
            ][:])

        if self.has_diamond:
            items.append("a Skull Fossil")

        if self.has_pearl:
            items.append("an Armor Fossil")

        return items

    @staticmethod
    def wild_dppt() -> List[str]:
        return [
            "Rattata",
            "Raticate",
            "Spearow",
            "Fearow",
            "Pichu",
            "Pikachu",
            "Female Nidoran",  # PokéRader
            "Nidorina",  # PokéRader
            "Male Nidoran",  # PokéRader
            "Nidorino",  # PokéRader
            "Zubat",
            "Golbat",
            "Gloom",
            "Venonat",  # PokéRader
            "Venomoth",  # PokéRader
            "Diglett",
            "Dugtrio",
            "Psyduck",
            "Golduck",
            "Mankey",  # PokéRader
            "Primeape",  # PokéRader
            "Poliwag",
            "Poliwhirl",
            "Abra",
            "Kadabra",
            "Machop",
            "Machoke",
            "Weepinbell",
            "Tentacool",
            "Tentacruel",
            "Geodude",
            "Graveler",
            "Ponyta",
            "Grimer",  # PokéRader
            "Shellder",
            "Gastly",
            "Haunter",
            "Onix",
            "Steelix",
            "Tyrogue",  # PokéRader
            "Weezing",
            "Rhyhorn",
            "Rhydon",
            "Chansey",
            "Horsea",
            "Seadra",
            "Goldeen",
            "Seaking",
            "Staryu",
            "Tauros",  # PokéRader
            "Magikarp",
            "Gyarados",
            "Lapras",
            "Dratini",
            "Dragonair",
            "Sentret",  # PokéRader
            "Chinchou",
            "Togepi",  # PokéRader
            "Mareep",  # PokéRader
            "Flaaffy",  # PokéRader
            "Hoppip",  # PokéRader
            "Sunkern",  # PokéRader
            "Quagsire",
            "Unown",
            "Wobbuffet",  # PokéRader
            "Girafarig",
            "Qwilfish",
            "Sneasel",
            "Slugma",
            "Magcargo",
            "Remoraid",
            "Octillery",
            "Mantyke",
            "Skarmory",
            "Smeargle",  # PokéRader
            "Miltank",  # PokéRader
            "Beautifly",
            "Swellow",  # PokéRader
            "Wingull",
            "Pelipper",
            "Ralts",  # PokéRader in Diamond and Pearl
            "Kirlia",  # PokéRader in Diamond and Pearl
            "Nincada",  # PokéRader
            "Loudred",  # PokéRader
            "Meditite",
            "Medicham",
            "Volbeat",
            "Illumise",
            "Budew",
            "Roselia",
            "Wailmer",
            "Wailord",
            "Numel",
            "Camerupt",
            "Torkoal",  # PokéRader
            "Cacnea",
            "Cacturne",
            "Swablu",  # PokéRader in Diamond and Pearl
            "Barboach",
            "Whiscash",
            "Corphish",
            "Crawdaunt",
            "Baltoy",  # PokéRader
            "Duskull",  # PokéRader in Diamond and Pearl
            "Dusclops",  # PokéRader in Diamond and Pearl
            "Chingling",
            "Chimecho",
            "Snorunt",  # PokéRader in Diamond and Pearl
            "Relicanth",
            "Luvdisc",
            "Starly",
            "Staravia",
            "Bidoof",
            "Bibarel",
            "Shinx",
            "Luxio",
            "Pachirisu",
            "Buizel",
            "Floatzel",
            "West Sea Shellos",
            "East Sea Shellos",
            "West Sea Gastrodon",
            "East Sea Gastrodon",
            "Buneary",
            "Bronzor",
            "Bronzong",
            "Gible",
            "Hippopotas",
            "Hippowdon",
            "Finneon",
            "Lumineon",
            "Snover",
            "Abomasnow",
        ]

    @staticmethod
    def wild_dp() -> List[str]:
        return [
            "Cleffa",
            "Clefairy",
            "Oddish",
            "Bellsprout",
            "Ditto",  # PokéRader
            "Lanturn",
            "Skiploom",  # PokéRader
            "Wurmple",
            "Sharpedo",
            "Trapinch",  # PokéRader
            "Vibrava",  # PokéRader
            "Clamperl",
            "Kricketune",
        ]

    @staticmethod
    def wild_d() -> List[str]:
        return [
            "Seel",
            "Mime Jr.",
            "Larvitar",  # PokéRader
            "Mightyena",  # PokéRader
            "Kecleon",  # PokéRader
            "Stunky",
            "Skuntank",
        ]

    @staticmethod
    def wild_dpt() -> List[str]:
        return [
            "Dewgong",
            "Mr. Mime",
            "Scyther",
            "Silcoon",
        ]

    @staticmethod
    def wild_p() -> List[str]:
        return [
            "Pinsir",
            "Bonsly",
            "Houndoom",  # PokéRader
            "Spheal",
            "Glameow",
            "Purugly",
        ]

    @staticmethod
    def wild_ppt() -> List[str]:
        return [
            "Slowpoke",  # PokéRader
            "Sudowoodo",
            "Stantler",  # PokéRader
            "Cascoon",
            "Dustox",
            "Sealeo",
            "Bagon",  # PokéRader
        ]

    @staticmethod
    def wild_pt() -> List[str]:
        return [
            "Pidgey",
            "Magnemite",
            "Magneton",
            "Lickitung",
            "Koffing",
            "Smoochum",
            "Jynx",
            "Electabuzz",
            "Magmar",
            "Marill",
            "Azumarill",
            "Gligar",
            "Swinub",
            "Piloswine",  # PokéRader
            "Houndour",
            "Poochyena",  # PokéRader
            "Surskit",
            "Masquerain",
            "Nosepass",
            "Absol",
            "Gabite",
            "Croagunk",
        ]

    @staticmethod
    def wild_time_dppt() -> List[str]:
        return [
            "Hoothoot",
            "Noctowl",
            "Ledian",
            "Ariados",
            "Banette",
            "Kricketot",
            "Chatot",
        ]

    @staticmethod
    def wild_time_pt() -> List[str]:
        return [
            "Cleffa",
            "Clefairy",
            "Oddish",
            "Bellsprout",
            "Wurmple",
            "Kricketune",
        ]

    @staticmethod
    def wild_honey_tree() -> List[str]:
        return [
            "Aipom",
            "Burmy",
            "Combee",
            "Cherubi",
        ]

    @staticmethod
    def wild_rare_dppt() -> List[str]:
        return [
            # Rare Honey Tree encounters
            "Munchlax",
            "Heracross",
            # Absurd encounter method
            "Feebas",
        ]

    @staticmethod
    def wild_daily_dppt() -> List[str]:
        return [
            # Daily Trophy Garden encounters
            "Igglybuff",
            "Jigglypuff",
            "Meowth",
            "Happiny",
            "Eevee",
            "Azurill",
            "Plusle",
            "Minun",
            "Castform",
            # Swarm encounters
            "Farfetch'd",
            "Doduo",
            "Drowzee",
            "Krabby",
            "Voltorb",
            "Cubone",
            "Natu",
            "Dunsparce",
            "Snubbull",
            "Corsola",
            "Delibird",
            "Phanpy",
            "Zigzagoon",
            "Slakoth",
            "Makuhita",
            "Skitty",
            "Electrike",
            "Spoink",
            "Spinda",
            "Beldum",
        ]

    @staticmethod
    def wild_daily_dp() -> List[str]:
        return [
            # Swarm encounters
            "Pidgey",
            "Magnemite",
            "Lickitung",
            "Smoochum",
            "Swinub",
            "Surskit",
            "Nosepass",
            "Absol",
            # Daily Trophy Garden encounter
            "Marill",
        ]

    @staticmethod
    def marsh_dppt() -> List[str]:
        return [
            "Magikarp",
            "Gyarados",
            "Hoothoot",  # Time-based
            "Noctowl",  # Time-based
            "Wooper",
            "Quagsire",
            "Carvanha",
            "Barboach",
            "Whiscash",
            "Bibarel",
        ]

    @staticmethod
    def marsh_dp() -> List[str]:
        return [
            "Psyduck",
            "Azurill",
            "Marill",
            "Budew",  # Time-based
            "Starly",  # Time-based
            "Bidoof",
        ]

    @staticmethod
    def marsh_pt() -> List[str]:
        return [
            "Tangela",
            "Yanma",
            "Tropius",  # Time-based
        ]

    @staticmethod
    def marsh_daily_dppt() -> List[str]:
        return [
            "Paras",
            "Exeggcute",
            "Kangaskhan",
            "Shroomish",
            "Gulpin",
            "Skorupi",
            "Drapion",
            "Toxicroak",
            "Carnivine",
        ]

    @staticmethod
    def marsh_daily_dp() -> List[str]:
        return [
            "Golduck",
            "Roselia",
            "Staravia",
        ]

    @staticmethod
    def common_poffin_types() -> List[str]:
        return [
            "Spicy",
            "Dry",
            "Sweet",
            "Bitter",
            "Sour",
        ]

    @staticmethod
    def rare_poffin_types() -> List[str]:
        return [
            "Spicy-Dry",
            "Spicy-Sweet",
            "Spicy-Bitter",
            "Spicy-Sour",
            "Dry-Sweet",
            "Dry-Bitter",
            "Dry-Sour",
            "Sweet-Spicy",
            "Sweet-Bitter",
            "Sweet-Sour",
            "Bitter-Spicy",
            "Bitter-Dry",
            "Bitter-Sour",
            "Sour-Spicy",
            "Sour-Dry",
            "Sour-Sweet",
        ]

    # Contest ranks are currently all handled individually, so they don't really need to be defined here.
    # @staticmethod
    # def base_contest_ranks() -> List[str]:
    #     return [
    #         "Normal",
    #         "Great",
    #         "Hyper",
    #         "Master",
    #     ]

    @staticmethod
    def contest_types() -> List[str]:
        return [
            "Super Contest",
            "Cool Super Contest",
            "Beauty Super Contest",
            "Cute Super Contest",
            "Smart Super Contest",
            "Tough Super Contest"
        ]

    @staticmethod
    def cities() -> List[str]:
        return [
            "Twinleaf Town",
            "Sandgem Town",
            "Jubilife City",
            "Oreburgh City",
            "Floaroma Town",
            "Eterna City",
            "Hearthome City",
            "Solaceon Town",
            "Veilstone City",
            "Pastoria City",
            "Celestic Town",
            "Canalave City",
            "Snowpoint City",
            "Sunyshore City",
            "Pokémon League (South)",
            "Pokémon League (North)",
            "Battle Area",
            "Survival Area",
            "Resort Area",
        ]

    @staticmethod
    def battle_frontier_facilities() -> List[str]:
        return [
            "Battle Tower",
            "Battle Factory",
            "Battle Arcade",
            "Battle Castle",
            # "Battle Hall",  # Slightly different objective than the others
        ]

    @staticmethod
    def battle_frontier_brains() -> List[str]:
        return [
            "Tower Tycoon Palmer",
            "Factory Head Thorton",
            "Arcade Star Dahlia",
            "Castle Valet Darach",
            "Hall Matron Argenta",
        ]

    def encounter_locations(self) -> List[str]:
        encounters = self.encounter_locations_dppt()[:]

        # Commented out since I don't think Platinum has any unique encounter locations
        # if self.has_platinum:
        #     encounters.extend(self.encounter_locations_pt()[:])

        return encounters

    def encounter_locations_with_marsh(self) -> List[str]:
        encounters = self.encounter_locations()[:]

        encounters.extend([
            "Great Marsh Area 1",
            "Great Marsh Area 2",
            "Great Marsh Area 3",
            "Great Marsh Area 4",
            "Great Marsh Area 5",
            "Great Marsh Area 6",
        ][:])

        return encounters

    def locations(self) -> List[str]:
        locations = self.encounter_locations_with_marsh()[:]

        locations.extend([
            "Verity Lakefront",  # No encounters
            "Sandgem Town",  # No encounters
            "Jubilife City",  # No encounters
            "Oreburgh City",  # No encounters
            "Floaroma Town",  # No encounters
            "Floaroma Meadow"  # Only Honey Tree encounters
            "Hearthome City",  # No encounters
            "Amity Square",  # No encounters
            "Solaceon Town",  # No encounters
            "Veilstone City",  # No encounters
            "Pokémon Mansion",  # No encounters
            "Snowpoint City",  # No encounters
            "Spear Pillar",  # No encounters
            "Spring Path",  # No encounters
            "Fight Area",  # No encounters
            "Fullmoon Island",  # No encounters
            "Survival Area",  # No encounters
        ][:])

        return locations

    @staticmethod
    def encounter_locations_dppt() -> List[str]:
        return [
            "Twinleaf Town",
            "Route 201",
            # "Verity Lakefront",  # No encounters
            "Lake Verity",
            # "Sandgem Town",  # No encounters
            "Route 202",
            # "Jubilife City",  # No encounters
            "Route 203",
            "Oreburgh Gate 1F",
            "Oreburgh Gate B1F",
            # "Oreburgh City",  # No encounters
            "Oreburgh Mine",
            "Route 204 (South)",
            "Route 204 (North)",
            "Ravaged Path",
            # "Floaroma Town",  # No encounters
            "Route 205",
            "Valley Windworks",
            # "Floaroma Meadow"  # Only Honey Tree encounters
            "Eterna Forest",
            "Eterna City",
            "Route 211 (West)",
            "Route 211 (East)",
            "Old Chateau",
            "Route 206",
            "Route 207",
            "Mt. Coronet 1F (Eterna-Celestic)",
            "Mt. Coronet 1F (Rt. 207-208)",
            "Mt. Coronet B1F",
            "Mt. Coronet (Rt. 216)",
            "Mt. Coronet 2F",
            "Mt. Coronet 3F",
            "Mt. Coronet (Snowy)",
            "Mt. Coronet 4F",
            "Mt. Coronet (1F-Snow Connector)",
            "Mt. Coronet 5F",
            "Mt. Coronet 6F",
            "Wayward Cave 1F",
            "Wayward Cave B1F",
            "Route 208",
            # "Hearthome City",  # No encounters
            # "Amity Square",  # No encounters
            "Route 209",
            "Lost Tower 1F",
            "Lost Tower 2F",
            "Lost Tower 3F",
            "Lost Tower 4F",
            "Lost Tower 5F",
            # "Solaceon Town",  # No encounters
            "Solaceon Ruins",
            "Route 210",
            "Route 215",
            # "Veilstone City",  # No encounters
            "Route 214",
            "Maniac Tunnel",
            "Valor Lakefront",
            "Route 213",
            "Pastoria City",
            # "Great Marsh",  # Special case
            "Route 212 (South)",
            "Route 212 (North)",
            # "Pokémon Mansion",  # No encounters
            "Trophy Garden",
            "Celestic Town",
            "Fuego Ironworks",
            "Route 219",
            "Route 220",
            "Route 221",
            "Route 218",
            "Canalave City",
            "Iron Island 1F",
            "Iron Island B1F (Left)",
            "Iron Island B1F (Right)",
            "Iron Island B2F (Left)",
            "Iron Island B2F (Right)",
            "Iron Island B3F",
            "Lake Valor",
            "Route 216",
            "Route 217",
            "Acuity Lakefront",
            # "Snowpoint City",  # No encounters
            "Lake Acuity",
            # "Spear Pillar",  # No encounters
            "Sendoff Spring",
            # "Spring Path",  # No encounters
            "Route 222",
            "Sunyshore City",
            "Route 223",
            "Pokémon League (South)",
            "Pokémon League (North)",
            "Victory Road 1F",
            "Victory Road B1F",
            "Victory Road 2F",
            "Victory Road (Rt. 224)",
            # "Fight Area",  # No encounters
            # "Fullmoon Island",  # No encounters
            "Snowpoint Temple 1F",
            "Snowpoint Temple B1F",
            "Snowpoint Temple B2F",
            "Snowpoint Temple B3F",
            "Snowpoint Temple B4F",
            "Snowpoint Temple B5F",
            "Turnback Cave",
            "Route 224",
            "Route 225",
            # "Survival Area",  # No encounters
            "Route 226",
            "Route 227",
            "Stark Mountain (Ext.)",
            "Stark Mountain (Front Int.)",
            "Stark Mountain (Back Int.)",
            "Route 228",
            "Route 229",
            "Route 230",
            "Resort Area",
        ]

    # @staticmethod
    # def encounter_locations_pt() -> List[str]:
    #     return [
    #     ]

    @staticmethod
    def underground_areas() -> List[str]:
        return [
            "upper left",
            "upper right",
            "lower left",
            "lower right",
            "large central",
            "small center",
        ]


# Archipelago Options
class PokemonDPPtOwnedGames(OptionSet):
    """
    Indicates which versions of the games the player owns between Pokémon Diamond/Pearl/Platinum.
    """

    display_name = "Pokémon Diamond/Pearl/Platinum Owned Games"
    valid_keys = [
        "Diamond",
        "Pearl",
        "Platinum"
    ]

    default = valid_keys


class PokemonDPPtObjectives(OptionSet):
    """
    Indicates which types of trial objectives the player would like to engage in for Pokémon Diamond/Pearl/Platinum.
    """

    display_name = "Pokémon Diamond/Pearl/Platinum Objective Types"
    valid_keys = [
        "Catching",
        "Contests",
        "Battles",
        "Battle Frontier",
        "Underground",
        "Shiny Hunting"
    ]

    default = valid_keys


class PokemonDPPtDailyEncounters(Toggle):
    """
    Allow for conditions to require catching/encountering Pokémon that may require waiting several days to appear.
    Does not apply to optional conditions.
    """

    display_name = "Pokémon Diamond/Pearl/Platinum Daily Encounters"
