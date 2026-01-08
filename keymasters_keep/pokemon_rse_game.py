from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PokemonRSEKeymastersKeepOptions:
    pokemon_rse_owned_games: PokemonRSEOwnedGames
    pokemon_rse_objectives: PokemonRSEObjectives
    pokemon_rse_allow_one_offs: PokemonRSEAllowOneOffs
    pokemon_rse_allow_event_items: PokemonRSEAllowEventItems


class PokemonRSEGame(Game):
    # Initial implementation by soopercool101

    name = "Pokémon Ruby, Sapphire, and Emerald Versions"
    platform = KeymastersKeepGamePlatforms.GBA

    is_adult_only_or_unrated = False

    options_cls = PokemonRSEKeymastersKeepOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use POKEMON as your lead whenever possible",
                data={
                    "POKEMON": (self.wild_pokemon, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Use POKEMON as your lead whenever possible",
                data={
                    "POKEMON": (self.wild_pokemon, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Use POKEMON as your lead whenever possible",
                data={
                    "POKEMON": (self.available_pokemon, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Use POKEMON as your lead whenever possible",
                data={
                    "POKEMON": (self.difficult_pokemon, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Only use the following Pokémon (unless otherwise needed for HMs or specific challenges): PKMON",
                data={
                    "PKMON": (self.wild_pokemon, 6),
                },
            ),
            GameObjectiveTemplate(
                label="Only use the following Pokémon (unless otherwise needed for HMs or specific challenges): PKMON",
                data={
                    "PKMON": (self.available_pokemon, 6),
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
        if len(objectives) == 0:  # Fallback default objectives. Better versions of these exist in other categories
            objectives += [
                GameObjectiveTemplate(
                    label="Without using Fly, travel between the following cities: CITY",
                    data={
                        "CITY": (self.cities, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=200,
                ),
                GameObjectiveTemplate(
                    label="Without using Fly, travel between the following locations: LOCATION",
                    data={
                        "LOCATION": (self.locations, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=100,
                ),
                GameObjectiveTemplate(
                    label="Encounter a wild POKEMON",
                    data={
                        "POKEMON": (self.wild_pokemon, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=700,
                ),
                GameObjectiveTemplate(
                    label="Encounter a wild Pokémon in LOCATION",
                    data={
                        "LOCATION": (self.encounter_locations, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=700,
                ),
                GameObjectiveTemplate(
                    label="Encounter a wild RAREPOKEMON",
                    data={
                        "RAREPOKEMON": (self.rare_wild_pokemon, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=self.rare_pokemon_objective_weight(),
                ),
            ]

        return objectives

    def catching_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Catch a wild POKEMON CONDITION",
                data={
                    "POKEMON": (self.wild_pokemon, 1),
                    "CONDITION": (self.pokemon_catch_conditions, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=900,
            ),
            GameObjectiveTemplate(
                label="Catch a wild Pokémon in LOCATION CONDITION",
                data={
                    "LOCATION": (self.encounter_locations, 1),
                    "CONDITION": (self.pokemon_catch_conditions, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=900,
            ),
            GameObjectiveTemplate(
                label="Catch a wild RAREPOKEMON CONDITION",
                data={
                    "RAREPOKEMON": (self.rare_wild_pokemon, 1),
                    "CONDITION": (self.pokemon_catch_conditions, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=self.rare_pokemon_objective_weight(),
            ),
            GameObjectiveTemplate(
                label="Catch a wild POKEMON in the Safari Zone CONDITION",
                data={
                    "POKEMON": (self.safari_pokemon, 1),
                    "CONDITION": (self.safari_catch_conditions, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=250,
            ),
        ]

    def contest_objectives(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Make COLOR Pokéblock",
                data={
                    "COLOR": (self.common_pokeblock_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=500,
            ),
            GameObjectiveTemplate(
                label="Make COLOR Pokéblock",
                data={
                    "COLOR": (self.rare_pokeblock_types, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Win a RANKING Rank TYPE",
                data={
                    "RANKING": (self.base_contest_ranks, 1),
                    "TYPE": (self.contest_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=300,
            ),
            GameObjectiveTemplate(
                label="Win a Hyper Rank TYPE",
                data={
                    "TYPE": (self.contest_types, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=150,
            ),
            GameObjectiveTemplate(
                label="Win a Master Rank TYPE",
                data={
                    "TYPE": (self.contest_types, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=100,
            ),
            GameObjectiveTemplate(
                label="Get your Pokémon painted after winning a Master Rank TYPE",
                data={
                    "TYPE": (self.contest_types, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=40,
            ),
        ]

    def battle_objectives(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Defeat the Pokémon League and enter the Hall of Fame CONDITION",
                data={
                    "CONDITION": (self.pokemon_league_battle_conditions, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=500,
            ),
            GameObjectiveTemplate(
                label="Defeat a wild POKEMON CONDITION",
                data={
                    "POKEMON": (self.wild_pokemon, 1),
                    "CONDITION": (self.easy_wild_battle_conditions, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=700,
            ),
            GameObjectiveTemplate(
                label="Defeat a wild RAREPOKEMON CONDITION",
                data={
                    "RAREPOKEMON": (self.rare_wild_pokemon, 1),
                    "CONDITION": (self.base_wild_battle_conditions, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=self.rare_pokemon_objective_weight(),
            ),
            GameObjectiveTemplate(
                label="Without using Fly, items, or a Pokémon Center, travel between the following cities "
                      "and defeat every wild encounter you see: CITY",
                data={
                    "CITY": (self.cities, 2),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=350,
            ),
            GameObjectiveTemplate(
                label="Without using Fly, items, or a Pokémon Center, travel between the following locations "
                      "and defeat every wild encounter you see: LOCATION",
                data={
                    "LOCATION": (self.locations, 2),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=250,
            ),
        ]

        if self.has_emerald:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Win any Match Call rematch CONDITION",
                    data={
                        "CONDITION": (self.easy_trainer_battle_conditions, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=350,
                ),
                GameObjectiveTemplate(
                    label="Win a Match Call rematch against a Gym Leader CONDITION",
                    data={
                        "CONDITION": (self.pokemon_league_battle_conditions, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=50,
                ),
                GameObjectiveTemplate(
                    label="Defeat Steven in Meteor Falls CONDITION",
                    data={
                        "CONDITION": (self.steven_battle_conditions, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=100,
                ),
            ])

        if self.allow_oneoffs:
            objectives.append(GameObjectiveTemplate(
                label="Defeat Gym Leader LEADER CONDITION",
                data={
                    "LEADER": (self.gym_leaders_and_level_caps, 1),
                    "CONDITION": (self.base_trainer_battle_conditions, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=150,
            ))

        return objectives

    def battle_frontier_objectives(self) -> List[GameObjectiveTemplate]:
        if self.has_emerald:
            return [
                GameObjectiveTemplate(
                    label="Win 3 battles in a row in the FACILITY",
                    data={
                        "FACILITY": (self.battle_tents, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=300,
                ),
                GameObjectiveTemplate(
                    label="Win 7 battles in a row in the FACILITY",
                    data={
                        "FACILITY": (self.battle_frontier_facilities, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=600,
                ),
                GameObjectiveTemplate(
                    label="Complete 7 floors in a row in the Battle Pyramid",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=100,
                ),
                GameObjectiveTemplate(
                    label="Win a battle against BRAIN",
                    data={
                        "BRAIN": (self.battle_frontier_brains, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=50,
                ),
                GameObjectiveTemplate(
                    label="Complete the MODE in Trainer Hill TIME",
                    data={
                        "MODE": (self.trainer_hill_modes, 1),
                        "TIME": (self.trainer_hill_times, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=300,
                ),
            ]
        else:
            return [
                GameObjectiveTemplate(
                    label="Win 7 battles in a row in the Battle Tower",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=200,
                ),
            ]

    def shiny_hunting_objectives(self) -> List[GameObjectiveTemplate]:
        objectives : List [GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Encounter or obtain a shiny POKEMON",
                data={
                    "POKEMON": (self.available_pokemon, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=15,
            ),
            GameObjectiveTemplate(
                label="Encounter a wild shiny Pokémon in LOCATION",
                data={
                    "LOCATION": (self.encounter_locations_with_safari, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=25,
            ),
        ]
        if self.allow_oneoffs:
            objectives.append(GameObjectiveTemplate(
                label="UNOBTAINABLE",
                data={
                    "UNOBTAINABLE": (self.unobtainable_shinies, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ))
        return objectives

    @property
    def allow_oneoffs(self) -> bool:
        return bool(self.archipelago_options.pokemon_rse_allow_one_offs.value)

    @property
    def allow_events(self) -> bool:
        return bool(self.archipelago_options.pokemon_rse_allow_event_items.value)

    @property
    def games_owned(self) -> Set[str]:
        return self.archipelago_options.pokemon_rse_owned_games.value

    @property
    def has_ruby(self) -> bool:
        return "Ruby" in self.games_owned

    @property
    def has_sapphire(self) -> bool:
        return "Sapphire" in self.games_owned

    @property
    def has_emerald(self) -> bool:
        return "Emerald" in self.games_owned

    @property
    def objectives(self) -> Set[str]:
        return self.archipelago_options.pokemon_rse_objectives.value

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
    def objective_shiny_hunting(self) -> bool:
        return "Shiny Hunting" in self.objectives

    def unobtainable_shinies(self) -> List[str]:
        pokemon: List[str] = [
            "Have Wally encounter a shiny Ralts"
        ][:]
        if self.has_ruby or self.has_sapphire:
            pokemon.append("Save Professor Birch from a shiny Poochyena")
        if self.has_emerald:
            pokemon.append("Save Professor Birch from a shiny Zigzagoon")
            if self.objective_battle_frontier:
                pokemon.append("Rent a shiny Pokémon in the Battle Factory") # Not a one-off, but works best here
        return pokemon

    def available_pokemon(self) -> List[str]:
        pokemon: List[str] = self.wild_pokemon()[:]
        pokemon.extend(self.difficult_pokemon()[:])
        return pokemon

    def wild_pokemon(self) -> List[str]:
        # List fully in common with all three games
        pokemon: List[str] = self.wild_rse()[:]

        # Full version exclusives
        if self.has_ruby:
            pokemon.extend(self.wild_r()[:])
        if self.has_sapphire:
            pokemon.extend(self.wild_s()[:])
        if self.has_emerald:
            pokemon.extend(self.wild_e()[:])

        # Exclusive to two games
        if self.has_ruby or self.has_sapphire:
            pokemon.extend(self.wild_rs()[:])
        if self.has_ruby or self.has_emerald:
            pokemon.extend(self.wild_re()[:])
        if self.has_sapphire or self.has_emerald:
            pokemon.extend(self.wild_se()[:])

        return pokemon

    def rare_pokemon_objective_weight(self) -> int:
        if self.allow_oneoffs:
            if self.allow_events:
                return 100
            return 80
        return 30

    def rare_wild_pokemon(self) -> List[str]:
        pokemon: List[str] = ["Feebas"][:]

        if self.allow_oneoffs:
            pokemon.extend([
                "Regirock",
                "Regice",
                "Registeel",
                "Rayquaza",
            ][:])
            if self.has_ruby or self.has_emerald:
                pokemon.extend([
                    "Latios",
                    "Groudon",
                ][:])
            if self.has_sapphire or self.has_emerald:
                pokemon.extend([
                    "Latias",
                    "Kyogre",
                ][:])
            if self.has_emerald:
                pokemon.append("Sudowoodo")
            if self.allow_events:
                if self.has_emerald:
                    pokemon.extend([
                        "Deoxys",   # AuroraTicket
                        "Mew",      # Old Sea Map
                        "Lugia",    # MysticTicket
                        "Ho-Oh",    # MysticTicket
                    ][:])
                else:
                    if not self.has_sapphire:
                        pokemon.append("Latias")  # Eon Ticket
                    if not self.has_ruby:
                        pokemon.append("Latios")  # Eon Ticket

        return pokemon

    def difficult_pokemon(self) -> List[str]:
        pokemon: List[str] = self.rare_wild_pokemon()[:]

        # Evolutions, Breeding, and other rare repeatable Pokémon
        pokemon.extend([
            # Evolution exclusive
            "Beautifly",
            "Dustox",
            "Kirlia",
            "Gardevoir",
            "Breloom",
            "Vigoroth",
            "Slaking",
            "Kadabra",
            "Ninjask",
            "Shedinja",
            "Exploud",
            "Azumarill",
            "Crobat",
            "Aggron",
            "Machoke",
            "Swalot",
            "Camerupt",
            "Magcargo",
            "Muk",
            "Weezing",
            "Grumpig",
            "Sandslash",
            "Vibrava",
            "Flygon",
            "Cacturne",
            "Crawdaunt",
            "Milotic",
            "Glalie",
            "Sealeo",
            "Walrein",
            "Lanturn",
            "Seadra",
            "Shelgon",
            "Salamence",
            
            # Breeding exclusive
            "Azurill",
            "Igglybuff",
            "Pichu",
            "Wynaut",

            # Safari Zone exclusives (and their evolutions)
            "Seaking",
            "Doduo",
            "Dodrio",
            "Pikachu",
            "Psyduck",
            "Golduck",
            "Wobbuffet",
            "Natu",
            "Xatu",
            "Girafarig",
            "Phanpy",
            "Donphan",
            "Pinsir",
            "Heracross",
            "Rhyhorn",
            "Rhydon",
        ][:])

        if not self.has_ruby:
            pokemon.append("Dusclops")  # Evolution-only in all other games
        if not self.has_sapphire and not self.has_emerald:
            pokemon.append("Banette")  # Evolution-only in Ruby
        if not self.has_emerald:
            pokemon.append("Mightyena")  # Evolution-only outside of Emerald

        if self.has_ruby or self.has_sapphire:
            pokemon.append("Masquerain")

        if self.has_emerald:
            pokemon.extend([
                "Hoothoot",
                "Noctowl",
                "Ledyba",
                "Ledian",
                "Spinarak",
                "Ariados",
                "Mareep",
                "Flaaffy",
                "Ampharos",
                "Aipom",
                "Sunkern",
                "Wooper",
                "Quagsire",
                "Pineco",
                "Forretress",
                "Gligar",
                "Snubbull",
                "Granbull",
                "Shuckle",
                "Teddiursa",
                "Ursaring",
                "Remoraid",
                "Octillery",
                "Houndour",
                "Houndoom",
                "Stantler",
                "Smeargle",
                "Miltank",
            ][:])

        if self.allow_oneoffs:
            pokemon.extend([
                # Starters. Mutually exclusive, one family per game
                "Treecko",
                "Grovyle",
                "Sceptile",
                "Torchic",
                "Combusken",
                "Blaziken",
                "Mudkip",
                "Marshtomp",
                "Swampert",
                # Stone evolution
                "Delcatty",
                "Vileplume",
                "Bellossom",
                "Wigglytuff",
                "Starmie",
                "Ninetales",
                "Raichu",
                # Fossils. Mutually exclusive, one family per game
                "Lileep",
                "Cradily",
                "Anorith",
                "Armaldo",
                # Only one given as a gift
                "Castform",
                "Beldum",
                "Metang",
                "Metagross",
            ][:])
            if self.has_sapphire or self.has_emerald:
                pokemon.append("Ludicolo") # Stone evolution
            if self.has_ruby or self.has_emerald:
                pokemon.append("Shiftry") # Stone evolution
            if self.has_emerald:
                pokemon.extend([
                    # In-game trade only
                    "Meowth",
                    "Persian",
                    # Stone evolution
                    "Sunflora",
                ][:])
        return pokemon

    def safari_pokemon(self) -> List[str]:
        pokemon: List[str] = self.safari_rse()[:]

        if self.has_emerald:
            pokemon.extend(self.safari_e()[:])

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
            "without using False Swipe",
            "without using status moves",
            "without damaging it",
            "without damaging it or using status moves",
            "in a Poké Ball",
            "in a Great Ball",
            "in a Ultra Ball",
            "in a Net Ball",
            "in a Dive Ball",
            "in a Nest Ball",
            "in a Repeat Ball",
            "in a Timer Ball",
            "in a Premier Ball",
            # Luxury and Master Balls *can* be found infinitely, but are too annoying
        ]

    @staticmethod
    def safari_catch_conditions() -> List[str]:
        return [
            "",
            "",
            "",
            "",
            "",
            "",
            "without using Pokéblocks",
            "without going near",
            "without using Sweet Scent",
        ]

    def gym_leaders_and_level_caps(self) -> List[str]:
        leaders: List[str] = [
            "Roxanne",
            "Roxanne (using level cap: 15)",
            "Brawly",
            "Wattson",
            "Norman",
            "Norman (using level cap: 31)",
            "Winona",
            "Winona (using level cap: 33)",
            "Tate & Liza",
            "Tate & Liza (using level cap: 42)",
        ][:]
        if self.has_ruby or self.has_sapphire:
            leaders.extend([
                "Brawly (using level cap: 18)",
                "Wattson (using level cap: 23)",
                "Flannery (using level cap: 28)",
                "Wallace",
                "Wallace (using level cap: 43)",
            ][:])
        if self.has_emerald:
            leaders.extend([
                "Brawly (using level cap: 19)",
                "Wattson (using level cap: 24)",
                "Flannery (using level cap: 29)",
                "Juan",
                "Juan (using level cap: 46)",
            ][:])
        return leaders

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
            "using only one Pokémon (two if it's a double battle)",
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
            "using no more Pokémon than your opponent",
        ]

    def easy_trainer_battle_conditions(self) -> List[str]:
        conditions : List[str] = self.base_trainer_battle_conditions()[:]
        conditions.extend([
            "without taking damage",
            "without using any Pokémon higher than level 30",
            "without using any Pokémon with a Base Stat Total over 400",
            "only using Pokémon that can still evolve twice",
        ][:])
        return conditions

    def pokemon_league_battle_conditions(self) -> List[str]:
        conditions : List[str] = self.base_trainer_battle_conditions()[:]
        conditions.extend([
            "without taking damage",
            "without using any Pokémon higher than level 50",
            "without using any Pokémon higher than level 60",
        ][:])
        return conditions

    def steven_battle_conditions(self) -> List[str]:
        conditions : List[str] = self.base_trainer_battle_conditions()[:]
        conditions.extend([
            "without using any Pokémon higher than level 60",
            "without using any Pokémon higher than level 70",
            "without using any Pokémon higher than level 80",
        ][:])
        return conditions

    @staticmethod
    def base_wild_battle_conditions() -> List[str]:
        return [
            "",
            "",
            "",
            "without taking damage",
            "without using STAB moves",
            "without using Super-Effective moves",
            "without using any moves over 40 Power",
            "without using any moves with 100 accuracy or moves that bypass accuracy checks",
            "only using Pokémon that can still evolve",
        ]

    def easy_wild_battle_conditions(self) -> List[str]:
        conditions : List[str] = self.base_wild_battle_conditions()[:]
        conditions.extend([
            "without using any Pokémon higher than level 30",
            "only using Pokémon that can still evolve twice",
        ][:])
        return conditions

    @staticmethod
    def wild_rse() -> List[str]:
        return [
            "Poochyena",
            "Zigzagoon",
            "Linoone",
            "Wurmple",
            "Silcoon",
            "Cascoon",
            "Taillow",
            "Swellow",
            "Wingull",
            "Pelipper",
            "Ralts",
            "Shroomish",
            "Slakoth",
            "Abra",
            "Nincada",
            "Whismur",
            "Loudred",
            "Makuhita",
            "Hariyama",
            "Goldeen",
            "Magikarp",
            "Gyarados",
            "Marill",
            "Geodude",
            "Graveler",
            "Nosepass",
            "Skitty",
            "Zubat",
            "Golbat",
            "Tentacool",
            "Tentacruel",
            "Aron",
            "Lairon",
            "Machop",
            "Electrike",
            "Manectric",
            "Plusle",
            "Minun",
            "Magnemite",
            "Magneton",
            "Voltorb",
            "Electrode",
            "Volbeat",
            "Illumise",
            "Oddish",
            "Gloom",
            "Gulpin",
            "Carvanha",
            "Sharpedo",
            "Wailmer",
            "Wailord",
            "Numel",
            "Slugma",
            "Torkoal",
            "Grimer",
            "Koffing",
            "Spoink",
            "Sandshrew",
            "Spinda",
            "Skarmory",
            "Trapinch",
            "Cacnea",
            "Swablu",
            "Altaria",
            "Barboach",
            "Whiscash",
            "Corphish",
            "Baltoy",
            "Claydol",
            "Jigglypuff",
            # "Feebas", # Absolutely a difficult objective
            "Staryu",
            "Kecleon",
            "Shuppet",
            "Duskull",
            "Tropius",
            "Chimecho",
            "Absol",
            "Vulpix",
            # "Wynaut", # Mirage Island exclusive, not even a good difficult objective
            "Snorunt",
            "Spheal",
            "Clamperl",
            "Relicanth",
            "Corsola",
            "Chinchou",
            "Luvdisc",
            "Horsea",
            "Bagon",
        ]

    @staticmethod
    def wild_rs() -> List[str]:
        return [
            "Surskit",
            "Meditite",
            "Medicham",
            "Roselia",
        ]

    @staticmethod
    def wild_r() -> List[str]:
        return [
            "Zangoose",
            "Dusclops",
        ]

    @staticmethod
    def wild_re() -> List[str]:
        return [
            "Seedot",
            "Nuzleaf",
            "Mawile",
            "Solrock",
        ]

    @staticmethod
    def wild_s() -> List[str]:
        return [
            "Lunatone",
        ]

    @staticmethod
    def wild_se() -> List[str]:
        return [
            "Lotad",
            "Lombre",
            "Sableye",
            "Seviper",
            "Banette",
        ]

    @staticmethod
    def wild_e() -> List[str]:
        return [
            # Hoenn Dex
            "Mightyena",
            # National Dex
            "Ditto",
            "Smeargle"
        ]

    @staticmethod
    def safari_rse() -> List[str]:
        return [
            "Goldeen",
            "Seaking",
            "Magikarp",
            "Geodude",
            "Oddish",
            "Gloom",
            "Doduo",
            "Dodrio",
            "Pikachu",
            "Psyduck",
            "Golduck",
            "Wobbuffet",
            "Natu",
            "Xatu",
            "Girafarig",
            "Phanpy",
            "Pinsir",
            "Heracross",
            "Rhyhorn",
        ]

    @staticmethod
    def safari_e() -> List[str]:
        return [
            # Hoenn Dex
            "Marill",
            # National Dex
            "Hoothoot",
            "Ledyba",
            "Spinarak",
            "Mareep",
            "Aipom",
            "Sunkern",
            "Wooper",
            "Quagsire",
            "Pineco",
            "Gligar",
            "Snubbull",
            "Shuckle",
            "Teddiursa",
            "Remoraid",
            "Octillery",
            "Houndour",
            "Stantler",
            "Smeargle",
            "Miltank",
        ]

    @staticmethod
    def common_pokeblock_types() -> List[str]:
        return [
            "a Red",
            "a Blue",
            "a Pink",
            "a Green",
            "a Yellow",
        ]

    @staticmethod
    def rare_pokeblock_types() -> List[str]:
        return [
            # "a Black", # Impossible in single player
            "a Gold",
            "a Purple",
            "an Indigo",
            "a Brown",
            "a LiteBlue",
            "an Olive",
            "a Gray",
            # "a White", # Impossible in single player
        ]

    @staticmethod
    def base_contest_ranks() -> List[str]:
        return [
            "Normal",
            "Super",
            # "Hyper",  # Hyper is separated out as time-consuming
            # "Master", # Master is separated out as difficult and time-consuming
        ]

    @staticmethod
    def contest_types() -> List[str]:
        return [
            "Contest",
            "Cool Contest",
            "Beauty Contest",
            "Cute Contest",
            "Smart Contest",
            "Tough Contest",
        ]

    @staticmethod
    def cities() -> List[str]:
        return [
            "Littleroot Town",
            "Oldale Town",
            "Petalburg City",
            "Rustboro City",
            "Dewford Town",
            "Slateport City",
            "Mauville City",
            "Verdanturf Town",
            "Fallarbor Town",
            "Lavaridge Town",
            "Fortree City",
            "Lilycove City",
            "Mossdeep City",
            "Sootopolis City",
            "Pacifidlog Town",
            "Ever Grande City (South)",
            "Ever Grande City (North)",
        ]

    @staticmethod
    def battle_tents() -> List[str]:
        return [
            "Battle Tent Slateport Site",
            "Battle Tent Verdanturf Site",
            "Battle Tent Fallarbor Site",
        ]

    @staticmethod
    def battle_frontier_facilities() -> List[str]:
        return [
            "Battle Factory",
            "Battle Arena",
            "Battle Dome",
            "Battle Pike",
            "Battle Palace",
            # "Battle Pyramid", # Different objective than the others
            "Battle Tower",
        ]

    @staticmethod
    def battle_frontier_brains() -> List[str]:
        return [
            "Factory Head Noland",
            "Arena Tycoon Greta",
            "Dome Ace Tucker",
            "Pike Queen Lucy",
            "Palace Maven Spenser",
            "Pyramid King Brandon",
            "Salon Maiden Anabel"
        ]

    @staticmethod
    def trainer_hill_modes() -> List[str]:
        return [
            "Normal Mode",
            "Variety Mode",
            "Unique Mode",
            "Expert Mode",
        ]

    @staticmethod
    def trainer_hill_times() -> List [str]:
        return [
            "",
            "",
            "under 12 minutes to win the Grand Prize",
            "within 12-13 minutes to win an Ether",
            "within 13-14 minutes to win a Max Potion",
            "within 14-16 minutes to win a Revive",
            "within 16-18 minutes to win a Fluffy Tail",
            "in over 18 minutes to win a Great Ball",
        ]

    def encounter_locations(self) -> List[str]:
        encounters = self.encounter_locations_rse()[:]

        if self.has_emerald:
            encounters.extend(self.encounter_locations_e()[:])

        return encounters

    def encounter_locations_with_safari(self) -> List[str]:
        encounters = self.encounter_locations()[:]

        encounters.extend([
            "Safari Zone Area 1",
            "Safari Zone Area 2",
            "Safari Zone Area 3",
            "Safari Zone Area 4",
        ][:])

        if self.has_emerald:
            encounters.extend([
                "Safari Zone Area 5",
                "Safari Zone Area 6",
            ][:])

        return encounters

    def locations(self) -> List[str]:
        locations = self.encounter_locations_with_safari()[:]

        locations.extend([
            "Littleroot Town", # No encounters
            "Oldale Town", # No encounters
            "Lavaridge Town", # No encounters
            "Fallarbor Town", # No encounters
            "Verdanturf Town", # No encounters
            "Mauville City", # No encounters
            "Rustboro City", # No encounters
            "Fortree City", # No encounters
            "Ever Grande City (North)", # No encounters
            "Underwater (Route 127)", # No encounters
            "Underwater (Route 128)", # No encounters
            "Underwater (Sootopolis City)", # No encounters
            "Mt. Chimney",  # No encounters
            "Battle Tower/Battle Frontier",  # No encounters
            "Underwater (Seafloor Cavern)",  # No encounters
            "Sealed Chamber", # No encounters
            "Underwater (Route 134)", # No encounters
            "Scorched Slab", # No encounters
            "Island Cave", # Only one encounter, not repeatable
            "Desert Ruins", # Only one encounter, not repeatable
            "Ancient Tomb", # Only one encounter, not repeatable
            "S.S. Tidal",  # No encounters
            "Sky Pillar 2F", # No encounters
            "Sky Pillar 4F", # No encounters
            "Sky Pillar Apex", # Only one encounter, not repeatable
        ][:])

        return locations

    @staticmethod
    def encounter_locations_rse() -> List[str]:
        return [
            # "Littleroot Town", # No encounters
            # "Oldale Town", # No encounters
            "Dewford Town",
            # "Lavaridge Town", # No encounters
            # "Fallarbor Town", # No encounters
            # "Verdanturf Town", # No encounters
            "Pacifidlog Town",
            "Petalburg City",
            "Slateport City",
            # "Mauville City", # No encounters
            # "Rustboro City", # No encounters
            # "Fortree City", # No encounters
            "Lilycove City",
            "Mossdeep City",
            "Sootopolis City",
            "Ever Grande City (South)",
            # "Ever Grande City (North)", # No encounters
            "Route 101",
            "Route 102",
            "Route 103",
            "Route 104",
            "Route 105",
            "Route 106",
            "Route 107",
            "Route 108",
            "Route 109",
            "Route 110",
            "Route 111",
            "Route 112",
            "Route 113",
            "Route 114",
            "Route 115",
            "Route 116",
            "Route 117",
            "Route 118",
            "Route 119",
            "Route 120",
            "Route 121",
            "Route 122",
            "Route 123",
            "Route 124",
            "Route 125",
            "Route 126",
            "Route 127",
            "Route 128",
            "Route 129",
            "Route 130",
            "Route 131",
            "Route 132",
            "Route 133",
            "Route 134",
            "Underwater (Route 124)",
            "Underwater (Route 126)",
            # "Underwater (Route 127)", # No encounters
            # "Underwater (Route 128)", # No encounters
            # "Underwater (Sootopolis City)", # No encounters
            "Granite Cave 1F",
            "Granite Cave B1F",
            "Granite Cave B2F",
            "Granite Cave Steven's Room",
            # "Mt. Chimney", # No encounters
            # "Safari Zone Area 1", # Incompatible with most encounter objectives
            # "Safari Zone Area 2", # Incompatible with most encounter objectives
            # "Safari Zone Area 3", # Incompatible with most encounter objectives
            # "Safari Zone Area 4", # Incompatible with most encounter objectives
            # "Battle Tower", # No encounters
            "Petalburg Woods",
            "Rusturf Tunnel",
            "Abandoned Ship",
            "New Mauville Entrance",
            "New Mauville Basement",
            "Meteor Falls 1F 1R",
            "Meteor Falls 1F 2R",
            "Meteor Falls B1F 1R",
            "Meteor Falls B1F 2R",
            "Mt. Pyre 1F",
            "Mt. Pyre 2F",
            "Mt. Pyre 3F",
            "Mt. Pyre 4F",
            "Mt. Pyre 5F",
            "Mt. Pyre 6F",
            "Mt. Pyre Exterior",
            "Mt. Pyre Summit",
            # "Hideout", # Closed after badge 7
            "Shoal Cave",
            # "Shoal Cave (Ice Room)", # Only available at low tide, not worth making players wait for
            "Seafloor Cavern",
            # "Underwater (Seafloor Cavern)", # No encounters
            "Victory Road 1F",
            "Victory Road B1F",
            "Victory Road B2F",
            # "Mirage Island", # Way too rare
            "Cave of Origin",
            # "Southern Island", # Event only, only one encounter
            "Fiery Path",
            "Jagged Pass",
            # "Sealed Chamber", # No encounters
            # "Underwater (Route 134)", # No encounters
            # "Scorched Slab", # No encounters
            # "Island Cave", # Only one encounter, not repeatable
            # "Desert Ruins", # Only one encounter, not repeatable
            # "Ancient Tomb", # Only one encounter, not repeatable
            # "Inside of Truck", # No encounters, can't be returned to
            "Sky Pillar 1F",
            # "Sky Pillar 2F", # No encounters
            "Sky Pillar 3F",
            # "Sky Pillar 4F", # No encounters
            "Sky Pillar 5F",
            # "Sky Pillar Apex", # Only one encounter, not repeatable
            # "S.S. Tidal", # No encounters
        ]

    @staticmethod
    def encounter_locations_e() -> List[str]:
        return [
            # "Safari Zone Area 5", # Incompatible with most encounter objectives
            # "Safari Zone Area 6", # Incompatible with most encounter objectives
            "Meteor Falls Steven's Room",
            # "Battle Frontier", Only one encounter, not repeatable
            # "Aqua Hideout", # Closed after badge 7
            "Magma Hideout",
            # "Mirage Tower", # Disappears after collecting a fossil
            # "Birth Island", # Event only, only one encounter
            # "Faraway Island", # Event only, only one encounter
            "Artisan Cave",
            # "Marine Cave", # Only one encounter, disappears after catching Kyogre
            # "Underwater (Marine Cave)", # No encounters, disappears after catching Kyogre
            # "Terra Cave", # Only one encounter, disappears after catching Groudon
            # "Underwater (Route 105)", # No encounters, only appears when Marine Cave appears
            # "Underwater (Route 125)", # No encounters, only appears when Marine Cave appears
            # "Underwater (Route 129)", # No encounters, only appears when Marine Cave appears
            "Desert Underpass",
            "Altering Cave",
            # "Navel Rock", # Only two encounters, disappears after catching Lugia or Ho-Oh
            # "Trainer Hill", # No encounters
        ]


# Archipelago Options
class PokemonRSEOwnedGames(OptionSet):
    """
    Indicates which versions of the games the player owns between Pokémon Ruby/Sapphire/Emerald.
    """

    display_name = "Pokémon Ruby/Sapphire/Emerald Owned Games"
    valid_keys = [
        "Ruby",
        "Sapphire",
        "Emerald"
    ]

    default = valid_keys


class PokemonRSEObjectives(OptionSet):
    """
    Indicates which types of trial objectives the player would like to engage in for Pokémon Ruby/Sapphire/Emerald.
    """

    display_name = "Pokémon Ruby/Sapphire/Emerald Objective Types"
    valid_keys = [
        "Catching",
        "Contests",
        "Battles",
        "Battle Frontier",
        "Shiny Hunting"
    ]

    default = valid_keys

class PokemonRSEAllowOneOffs(Toggle):
    """
    If true, adds additional challenges that are only available once in a save file. May require starting a new game!
    """

    display_name = "Pokémon Ruby/Sapphire/Emerald Allow One-Offs"


class PokemonRSEAllowEventItems(Toggle):
    """
    Adds Pokémon acquired through event items into the pool. One-offs are required for this setting to have any effect.
    """

    display_name = "Pokémon Ruby/Sapphire/Emerald Allow Event Items"
