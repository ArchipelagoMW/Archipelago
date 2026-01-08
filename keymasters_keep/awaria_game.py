from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AwariaArchipelagoOptions:
    pass


class AwariaGame(Game):
    name = "Awaria"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = AwariaArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat STAGE on MODE",
                data={
                    "STAGE": (self.stages, 1),
                    "MODE": (self.modes, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Beat STAGE on HARD MODE",
                data={
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat STAGES consecutively and without failing on MODE",
                data={
                    "STAGES": (self.stages, 3),
                    "MODE": (self.modes, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat STAGES consecutively and without failing on HARD MODE",
                data={
                    "STAGES": (self.stages, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def stages() -> List[str]:
        return [
            "Chapter 1: Zmora",
            "Chapter 2: Zmora II",
            "Chapter 3: Cutwire",
            "Chapter 4: Cutwire II",
            "Chapter 5: Nikita",
            "Chapter 6: Nikita II",
            "Chapter 7: Zmora III",
            "Chapter 8: Zmora IV",
            "Chapter 9: Zmora V",
            "Chapter 10: ???",
            "Chapter 11: Dr. Striga",
            "Chapter 12: Dr. Striga II",
            "Chapter 13: Dr. Striga III",
        ]

    @staticmethod
    def modes() -> List[str]:
        return [
            "EASY MODE",
            "STANDARD MODE",
        ]


# Archipelago Options
# ...
