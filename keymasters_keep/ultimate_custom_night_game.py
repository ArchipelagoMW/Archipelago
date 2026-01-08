from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class UltimateCustomNightArchipelagoOptions:
    pass


class UltimateCustomNightGame(Game):
    name = "Ultimate Custom Night"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = UltimateCustomNightArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Add an Extra Animatronic at Difficulty 10",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="No Power-Ups",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Finish a night with 10 Animatronics including ANIMATRONICS.  Point Value: POINTS",
                data={
                    "ANIMATRONICS": (self.animatronics, 2),
                    "POINTS": (self.point_totals_first, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish a night with 15 Animatronics including ANIMATRONICS.  Point Value: POINTS",
                data={
                    "ANIMATRONICS": (self.animatronics, 3),
                    "POINTS": (self.point_totals_second, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish a night with 20 Animatronics including ANIMATRONICS.  Point Value: POINTS",
                data={
                    "ANIMATRONICS": (self.animatronics, 4),
                    "POINTS": (self.point_totals_third, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish a night with 25 Animatronics including ANIMATRONICS.  Point Value: POINTS",
                data={
                    "ANIMATRONICS": (self.animatronics, 5),
                    "POINTS": (self.point_totals_fourth, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish a night with 30 Animatronics including ANIMATRONICS.  Point Value: POINTS",
                data={
                    "ANIMATRONICS": (self.animatronics, 5),
                    "POINTS": (self.point_totals_fifth, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete the following Challenge: CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete the following Challenge: CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def animatronics() -> List[str]:
        return [
            "Freddy",
            "Bonnie",
            "Chica",
            "Foxy",
            "Toy Freddy",
            "Toy Bonnie",
            "Toy Chica",
            "Mangle",
            "BB",
            "JJ",
            "Withered Chica",
            "Withered Bonnie",
            "Marionette",
            "Golden Freddy",
            "Springtrap",
            "Phantom Mangle",
            "Phantom Freddy",
            "Phantom BB",
            "Nightmare Freddy",
            "Nightmare Bonnie",
            "Nightmare Fredbear",
            "Nightmare",
            "Jack-O-Chica",
            "Nightmare Mangle",
            "Nightmarionne",
            "Nightmare BB",
            "Old Man Consequences",
            "Circus Baby",
            "Ballora",
            "Funtime Foxy",
            "Ennard",
            "Trash and the Gang",
            "Helpy",
            "Happy Frog",
            "Mr. Hippo",
            "Pigpatch",
            "Nedd Bear",
            "Orville Elephant",
            "Rockstar Freddy",
            "Rockstar Bonnie",
            "Rockstar Chica",
            "Rockstar Foxy",
            "Music Man",
            "El Chip",
            "Funtime Chica",
            "Molten Freddy",
            "Scrap Baby",
            "Afton",
            "Lefty",
            "Phone Guy",
        ]

    @staticmethod
    def challenges() -> List[str]:
        return [
            "Bears Attack 1",
            "Bears Attack 2",
            "Pay Attention 1",
            "Ladies Night 1",
            "Ladies Night 2",
            "Creepy Crawlies 1",
            "Nightmares Attack",
            "Springtrapped",
            "Old Friends",
        ]

    @staticmethod
    def challenges_hard() -> List[str]:
        return [
            "Bears Attack 3",
            "Pay Attention 2",
            "Ladies Night 3",
            "Creepy Crawlies 2",
            "Chaos 1",
            "Chaos 2",
            "Chaos 3",
        ]

    @staticmethod
    def point_totals_first() -> range:
        return range(500, 1401, 100)

    @staticmethod
    def point_totals_second() -> range:
        return range(750, 2101, 150)

    @staticmethod
    def point_totals_third() -> range:
        return range(1000, 2801, 200)

    @staticmethod
    def point_totals_fourth() -> range:
        return range(1250, 4001, 250)

    @staticmethod
    def point_totals_fifth() -> range:
        return range(1500, 4801, 300)


# Archipelago Options
# ...
