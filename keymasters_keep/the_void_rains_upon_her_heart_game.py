from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TheVoidRainsUponHerHeartArchipelagoOptions:
    pass


class TheVoidRainsUponHerHeartGame(Game):
    name = "The Void Rains Upon Her Heart"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = TheVoidRainsUponHerHeartArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Increase the difficulty to Torrential (Radiant Medal goal for quickplay)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Always take burdens when available, prioritizing highest level (+1 monster level for quickplay)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="You must PANICYODA",
                data={
                    "PANICYODA": (self.panicyoda, 1),
                },
            ),
            GameObjectiveTemplate(
                label="YODA use charge shots",
                data={
                    "YODA": (self.yoda, 1),
                },
            ),
            GameObjectiveTemplate(
                label="YODA use focus",
                data={
                    "YODA": (self.yoda, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Find and defeat at least 1 Special monster (Change monster type to Special for quickplay)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Swap hand placement on your keyboard",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win an altered story run with HEART",
                data={
                    "HEART": (self.hearts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Earn a gold or higher medal against a level LEVEL TYPE in quickplay with HEART",
                data={
                    "HEART": (self.hearts, 1),
                    "LEVEL": (self.levels, 1),
                    "TYPE": (self.types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a tower run with HEART",
                data={
                    "HEART": (self.hearts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def yoda() -> List[str]:
        return [
            "You can only",
            "You can not",
        ]
    
    @staticmethod
    def panicyoda() -> List[str]:
        return [
            "use at least one panic attack per fight",
            "not use any panic attacks",
        ]
    
    @staticmethod
    def levels() -> List[str]:
        return [
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ]
        
    @staticmethod
    def types() -> List[str]:
        return [
            "Shamble",
            "Guardian",
            "Eyeric Glyph",
            "Glass Flora",
            "Zaramech",
            "Veyeral",
        ]
        
    @staticmethod
    def hearts() -> List[str]:
        return [
            "Her Heart",
            "Defect",
            "Twin Heart",
            "The Devil",
            "Alter Heart",
            "Alter Defect",
            "Alter Twin",
            "Alter Devil",
            "any heart",
        ]
    

# Archipelago Options
# ...
