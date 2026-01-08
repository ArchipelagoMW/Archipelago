from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HotlineMiamiArchipelagoOptions:
    pass


class HotlineMiamiGame(Game):
    name = "Hotline Miami"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.VITA,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = True

    options_cls = HotlineMiamiArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Get an A rank",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Clear Chapter CHAPTER",
                data={
                    "CHAPTER": (self.chapters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear Chapter CHAPTER, wearing the following Mask: MASK",
                data={
                    "CHAPTER": (self.chapters, 1),
                    "MASK": (self.masks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def chapters() -> List[str]:
        return [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
        ]
        
    @staticmethod
    def masks() -> List[str]:
        return [
            "Richard",
            "Rasmus",
            "Tony",
            "Aubrey",
            "Don Juan",
            "Graham",
            "Dennis",
            "George",
            "Ted",
            "Rufus",
            "Rami",
            "Willem",
            "Peter",
            "Zack",
            "Oscar",
            "Rick",
            "Brandon",
            "Charlie",
            "Louie",
            "Phil",
            "Nigel",
            "Earl",
            "Jones",
            "Carl",
            "Jake",
            "Richter",
        ]


# Archipelago Options
# ...
