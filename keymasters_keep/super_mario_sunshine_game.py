from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SuperMarioSunshineArchipelagoOptions:
    pass


class SuperMarioSunshineGame(Game):
    name = "Super Mario Sunshine"
    platform = KeymastersKeepGamePlatforms.GC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = SuperMarioSunshineArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Get the 'SHINE' Shine in Bianco Hills",
                data={
                    "SHINE": (self.shines_bianco_hills, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get COUNT Shines in Bianco Hills",
                data={
                    "COUNT": (self.areas_shine_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get the 'SHINE' Shine in Delfino Plaza",
                data={
                    "SHINE": (self.shines_delfino_plaza, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get COUNT Shines in Delfino Plaza",
                data={
                    "COUNT": (self.delfino_shine_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get the 'SHINE' Shine in Ricco Harbor",
                data={
                    "SHINE": (self.shines_ricco_harbor, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get COUNT Shines in Ricco Harbor",
                data={
                    "COUNT": (self.areas_shine_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get the 'SHINE' Shine in Gelato Beach",
                data={
                    "SHINE": (self.shines_gelato_beach, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get COUNT Shines in Gelato Beach",
                data={
                    "COUNT": (self.areas_shine_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get the 'SHINE' Shine in Pinna Park",
                data={
                    "SHINE": (self.shines_pinna_park, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get COUNT Shines in Pinna Park",
                data={
                    "COUNT": (self.areas_shine_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get the 'SHINE' Shine in Sirena Beach",
                data={
                    "SHINE": (self.shines_sirena_beach, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get COUNT Shines in Sirena Beach",
                data={
                    "COUNT": (self.areas_shine_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get the 'SHINE' Shine in Noki Bay",
                data={
                    "SHINE": (self.shines_noki_bay, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get COUNT Shines in Noki Bay",
                data={
                    "COUNT": (self.areas_shine_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get the 'SHINE' Shine in Pianta Village",
                data={
                    "SHINE": (self.shines_pianta_village, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get COUNT Shines in Pianta Village",
                data={
                    "COUNT": (self.areas_shine_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish COUNT Missions in AREA",
                data={
                    "COUNT": (self.mission_count_range, 1),
                    "AREA": (self.area_zones, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish the game with at least COUNT Shines",
                data={
                    "COUNT": (self.total_shine_count_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def shines_delfino_plaza() -> List[str]:
        return [
            "Beach Treasure",
            "The Slide Mini-Game",
            "The First Dirty Bell",
            "The Box Smashing Mini-Game pt.1",
            "The Box Smashing Mini-Game pt.2",
            "Chuckster on the Roof",
            "The Pachinko Mini-Game",
            "The Gold Bird",
            "The Lily Pad Mini-Game",
            "Turbo Nozzle Fun",
            "The Waterslide Mini-Game",
            "The Lighthouse",
            "Cleaning the Shine Gate",
            "Cleaning the Second Bell",
            "The Tall Grass Mini-Game",
            "Defeating Bowser",
            "100-Coin",
        ]

    @staticmethod
    def shines_bianco_hills() -> List[str]:
        return [
            "Road to the Big Windmill",
            "Down with Petey Piranha!",
            "The Hillside Cave",
            "Red Coins of Windmill Village",
            "Petey Piranha Strikes Back",
            "The Secret of the Dirty Lake",
            "Shadow Mario on the Loose",
            "Red Coins of the Lake",
            "The Hillside Cave Red Coins (Secret)",
            "Red Coins of the Dirty Lake (Secret)",
            "100-Coin",
        ]

    @staticmethod
    def shines_ricco_harbor() -> List[str]:
        return [
            "Gooper Blooper Breaks Out",
            "Blooper Surfing Safari",
            "The Caged Shine Sprite",
            "The Secret of Ricco Tower",
            "Gooper Blooper Returns",
            "Red Coins in the Water",
            "Shadow Mario Revisited",
            "Yoshi's Fruit Adventure",
            "Blooper Speed Run (Secret)",
            "Red Coins of Ricco Tower (Secret)",
            "100-Coin",
        ]

    @staticmethod
    def shines_gelato_beach() -> List[str]:
        return [
            "Dune Bud Sand Castle Secret",
            "Mirror Madness! Tilt, Slam, Bam!",
            "Wiggler Ahoy! Full Steam Ahead!",
            "The Sand Bird is Born",
            "Il Piantissimo's Sand Sprint",
            "Red Coins in the Coral Reef",
            "It's Shadow Mario! After Him!",
            "The Watermelon Festival",
            "Dune Bud Sand Castle Red Coins (Secret)",
            "Dune Bud (Secret)",
            "100-Coin",
        ]

    @staticmethod
    def shines_pinna_park() -> List[str]:
        return [
            "Mecha-Bowser Appears!",
            "The Beach Cannon's Secret",
            "Red Coins of the Pirate Ships",
            "The Wilted Sunflowers",
            "The Runaway Ferris Wheel",
            "The Yoshi-Go-Round's Secret",
            "Shadow Mario in the Park",
            "Rollar Coaster Balloons",
            "The Beach Cannon's Red Coins (Secret)",
            "The Yoshi-Go-Round's Red Coins (Secret)",
            "100-Coin",
        ]

    @staticmethod
    def shines_sirena_beach() -> List[str]:
        return [
            "The Manta Storm",
            "The Hotel Lobby's Secret",
            "Mysterious Hotel Delfino",
            "The Secret of Casino Delfino",
            "King Boo Down Below",
            "Scrubbing Sirena Beach",
            "Shadow Mario Checks In",
            "Red Coins in the Hotel",
            "The Hotel Lobby's Red Coins (Secret)",
            "The Red Coins of Casino Delfino (Secret)",
            "100-Coin",
        ]

    @staticmethod
    def shines_noki_bay() -> List[str]:
        return [
            "Uncork the Waterfall",
            "The Boss of Tricky Ruins",
            "Red Coins in a Bottle",
            "Eely-Mouth's Dentist",
            "Il Piantissimo's Surf Swim",
            "The Shell's Secret",
            "Hold it, Shadow Mario!",
            "The Red Coin Fish",
            "The Shell's Red Coins (Secret)",
            "Gold Bird of Noki Bay (Secret)",
            "100-Coin",
        ]

    @staticmethod
    def shines_pianta_village() -> List[str]:
        return [
            "Chain Chomplets Unchained",
            "Il Piantissimo's Crazy Climb",
            "The Goopy Inferno",
            "Chain Chomp's Bath",
            "Secret of the Village Underside",
            "Piantas in Need",
            "Shadow Mario Runs Wild",
            "Fluff Festival Coin Hunt",
            "Red Coins of the Village Underside (Secret)",
            "Brighter than the Sun (Secret)",
            "100-Coin",
        ]

    @staticmethod
    def shines_delfino_airstrip() -> List[str]:
        return [
            "First Shine",
            "Second Shine",
        ]

    @staticmethod
    def area_zones() -> List[str]:
        return [
            "Bianco Hills",
            "Ricco Harbor",
            "Gelato Beach",
            "Pinna Park",
            "Sirena Beach",
            "Noki Bay",
            "Pianta Village",
            "Delfino Airstrip",
        ]

    @staticmethod
    def mission_count_range() -> range:
        return range(1, 9)

    @staticmethod
    def delfino_shine_count_range() -> range:
        return range(1, 18)

    @staticmethod
    def areas_shine_count_range() -> range:
        return range(1, 12)

    @staticmethod
    def total_shine_count_range() -> range:
        return range(50, 121)


# Archipelago Options
# ...
