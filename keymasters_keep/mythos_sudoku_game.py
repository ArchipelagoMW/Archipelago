from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MythosSudokuArchipelagoOptions:
    pass


class MythosSudokuGame(Game):
    # Initial implementation by JCBoorgo

    name = "Mythos: Sudoku"
    platform = KeymastersKeepGamePlatforms.PC

    is_adult_only_or_unrated = False

    options_cls = MythosSudokuArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete a TYPE VARIANT sudoku on DIFFICULTY",
                data={"TYPE": (self.game_type, 1), "VARIANT": (self.variants, 1), "DIFFICULTY": (self.difficulties, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=23,
            ),
            GameObjectiveTemplate(
                label="Complete a Temple trial on DIFFICULTY",
                data={"DIFFICULTY": (self.difficulties, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete a Chaos trial on DIFFICULTY",
                data={"DIFFICULTY": (self.difficulties, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]
    
    @staticmethod
    def variants() -> List[str]:
        return [
            "Dark (1)",
            "Soul (2)",
            "Sky (3)",
            "Sea (4)",
            "Time (5)",
            "Power (6)",
            "Land (7)",
            "Sound (8)",
            "Light (9)",
        ]
    
    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
        ]
    
    @staticmethod
    def game_type() -> List[str]:
        return [
            "Standard",
            "Duel",
            "Discovery",
        ]


# Archipelago Options
# ...
