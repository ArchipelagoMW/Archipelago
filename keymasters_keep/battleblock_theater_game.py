from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BattleBlockTheaterArchipelagoOptions:
    pass


class BattleBlockTheaterGame(Game):
    name = "BattleBlock Theater"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.X360,
    ]

    is_adult_only_or_unrated = False

    options_cls = BattleBlockTheaterArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Insane",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat STAGE",
                data={
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat STAGE with WEAPONS",
                data={
                    "STAGE": (self.stages, 1),
                    "WEAPONS": (self.weapons, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat STAGE without weapons",
                data={
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat STAGE with an RANK rank",
                data={
                    "STAGE": (self.stages, 1),
                    "RANK": (self.ranks, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a match of ARENA",
                data={
                    "ARENA": (self.arena, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def stages() -> List[str]:
        stages: List[str] = list()

        for chapter in range(1, 9):
            for act in range(1, 10):
                stages.append(f"Chapter {chapter} - Act {act}")

            stages.append(f"Chapter {chapter} - Boss")

            for encore in range(1, 4):
                stages.append(f"Chapter {chapter} - Encore {encore}")

        return stages

    @staticmethod
    def ranks() -> List[str]:
        return [
            "A",
            "A++",
        ]

    @staticmethod
    def weapons() -> List[str]:
        return [
            "Forceball",
            "Grenade",
            "Acid Bubble",
            "Disc",
            "Dodgeball",
            "Vacuum",
            "Boomerang",
            "Airplane",
            "Fan",
            "Ice Cannon",
            "Fireball",
            "Dart Gun",
            "Frog",
        ]

    @staticmethod
    def arena() -> List[str]:
        return [
            "Soul Snatcher",
            "Muckle",
            "Challenge",
            "King of the Hill",
            "Color The World",
            "Grab The Gold",
            "Ball Game",
            "Capture The Horse",
        ]


# Archipelago Options
# ...
