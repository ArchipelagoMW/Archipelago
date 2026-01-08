from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PokemonPlatinumMapRandomizerArchipelagoOptions:
    pass


class PokemonPlatinumMapRandomizerGame(Game):
    name = "Pokémon Platinum Map Randomizer"
    platform = KeymastersKeepGamePlatforms.MOD

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = PokemonPlatinumMapRandomizerArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Choose STARTER as your starter",
                data={
                    "STARTER": (self.starters, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Run only with TYPE type Pokémon in your party (where possible)",
                data={
                    "TYPE": (self.types, 1)
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Find and beat in order: GYMS",
                data={
                    "GYMS": (self.gyms, 4)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find and beat in order: ELITE4",
                data={
                    "ELITE4": (self.elite_4, 3)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find and map: CITIES",
                data={
                    "CITIES": (self.cities, 4)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find and map: INTERIORS",
                data={
                    "INTERIORS": (self.interiors, 4)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Find and complete: STORY_BEATS",
                data={
                    "STORY_BEATS": (self.story_beats, 3)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Capture a Pokémon at ROUTE",
                data={
                    "ROUTE": (self.routes, 1)
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Capture one Pokémon from each of ROUTES and build a team to defeat ELITE4",
                data={
                    "ROUTES": (self.routes, 3),
                    "ELITE4": (self.elite_4, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Capture one Pokémon from each of ROUTES and build a team to defeat GYM",
                data={
                    "ROUTES": (self.routes, 3),
                    "GYM": (self.gyms, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find and unlock HM",
                data={
                    "HM": (self.hms, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def cities() -> List[str]:
        return [
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
            "SunyShore City",
            "Fight Area",
            "Survival Area",
            "Resort Area",
        ]

    @staticmethod
    def interiors() -> List[str]:
        return [
            "Sandgem PC",
            "Jubilife PC",
            "Oreburgh PC",
            "Floaroma PC",
            "Eterna PC",
            "Hearthome PC",
            "Solaceon PC",
            "Veilstone PC",
            "Pastoria PC",
            "Celestic PC",
            "Canalave PC",
            "Snowpoint PC",
            "SunyShore PC",
            "Fight Area PC",
            "Survival Area PC",
            "Resort Area PC",
            "League PC",
            "Victory Road PC",
            "Sandgem Mart",
            "Jubilife Mart",
            "Oreburgh Mart",
            "Floaroma Mart",
            "Eterna Mart",
            "Hearthome Mart",
            "Solaceon Mart",
            "Veilstone Department Store",
            "Pastoria Mart",
            "Celestic Shop",
            "Canalave Mart",
            "Snowpoint Mart",
            "SunyShore Mart",
            "Fight Area Mart",
            "Survival Area Mart",
            "Resort Area Mart",
            "Jubilife TV",
        ]

    @staticmethod
    def gyms() -> List[str]:
        return [
            "Oreburgh",
            "Eterna",
            "Hearthome",
            "Canalave",
            "Veilstone",
            "Pastoria",
            "Snowpoint",
            "Sunyshore",
        ]

    @staticmethod
    def elite_4() -> List[str]:
        return [
            "Aaron",
            "Bertha",
            "Flint",
            "Lucian",
            "Cynthia",
        ]

    @staticmethod
    def starters() -> List[str]:
        return [
            "Turtwig",
            "Chimchar",
            "Piplup",
        ]

    @staticmethod
    def routes() -> List[str]:
        return [
            "Route 201",
            "Route 202",
            "Route 203",
            "Route 204",
            "Route 205",
            "Route 206",
            "Route 207",
            "Route 208",
            "Route 209",
            "Route 210",
            "Route 211",
            "Route 212",
            "Route 213",
            "Route 214",
            "Route 215",
            "Route 216",
            "Route 217",
            "Route 218",
            "Route 219",
            "Route 220",
            "Route 221",
            "Route 222",
            "Route 223",
            "Route 224",
            "Route 225",
            "Route 226",
            "Route 227",
            "Route 228",
            "Route 229",
            "Route 230",
            "Lake Verity (Lakefront)",
            "Oreburgh Gate",
            "Oreburgh Mine",
            "Ravaged Path",
            "Valley Windworks",
            "Eterna Forest",
            "Old Chateau",
            "Wayward Cave",
            "Mount Coronet",
            "Lost Tower",
            "Solaceon Ruins",
            "Maniac Tunnel",
            "Lake Valor (Lakefront)",
            "Great Marsh",
            "Trophy Garden",
            "Fuego Ironworks",
            "Iron Island",
            "Lake Acuity (Lakefront)",
            "Victory Road",
            "Stark Mountain",
            "Snowpoint Temple",
            "Sendoff Spring",
        ]

    @staticmethod
    def story_beats() -> List[str]:
        return [
            "Rival Fight 2 (After Jubilife)",
            "Rival Fight 3 (Route 209)",
            "Rival Fight 4 (Pastoria City)",
            "Rival Fight 5 (Canalave)",
            "Rival Fight 6 (Pokemon League)",
            "Return Roark (Oreburgh Mine)",
            "Defeat the grunts on Floaroma Meadow",
            "Liberate Valley Windworks",
            "Escort Cheryl (Eterna Forest)",
            "Defeat Jupiter (Team Galactic Eterna Building)",
            "Escort Mira (Wayward Cave)",
            "Defeat Cyrus (Celestic Ruins)",
            "Escort Riley (Iron Island)",
            "Defeat Saturn (Valor Cavern)",
            "Defeat Mars (Lake Verity)",
            "Defeat Cyrus (Team Galactic HQ)",
            "Defeat Saturn (Team Galactic HQ)",
            "Defeat Mars and Jupiter (Spear Pillar)",
            "Catch or Defeat Dialga (Spear Pillar)",
            "Catch or Defeat Palkia (Spear Pillar)",
            "Catch or Defeat Giratina (Spear Pillar)",
            "Catch or Defeat Arceus (Spear Pillar)",
            "Catch or Defeat Regirock",
            "Catch or Defeat Regice",
            "Catch or Defeat Registeel",
            "Catch or Defeat Regigigas",
            "Catch or Defeat Darkrai",
            "Escort Marley (Victory Road)",
        ]

    @staticmethod
    def hms() -> List[str]:
        return [
            "HM01, Cut",
            "HM02, Fly",
            "HM03, Surf",
            "HM04, Strength",
            "HM05, Flash",
            "HM06, Rock Smash",
            "HM07, Waterfall",
        ]

    @staticmethod
    def types() -> List[str]:
        return [
            "Normal",
            "Fire",
            "Water",
            "Electric",
            "Grass",
            "Ice",
            "Fighting",
            "Poison",
            "Ground",
            "Flying",
            "Psychic",
            "Bug",
            "Rock",
            "Ghost",
            "Dragon",
            "Dark",
            "Steel",
        ]

# Archipelago Options
# ...
