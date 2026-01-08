from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SuperHexagonArchipelagoOptions:
    pass


class SuperHexagonGame(Game):
    name = "Super Hexagon"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
    ]

    is_adult_only_or_unrated = False

    options_cls = SuperHexagonArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete each objective by surviving TIME seconds in STAGE immediately after",
                data={
                    "TIME": (self.survival_time_range_low, 1),
                    "STAGE": (self.stages, 1)
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete the STAGE stage",
                data={"STAGE": (self.stages, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME seconds in STAGE",
                data={
                    "TIME": (self.survival_time_range_low, 1),
                    "STAGE": (self.stages, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME seconds in STAGE",
                data={
                    "TIME": (self.survival_time_range_high, 1),
                    "STAGE": (self.stages, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME seconds in STAGE",
                data={
                    "TIME": (self.survival_time_range_hyper_low, 1),
                    "STAGE": (self.stages_hyper, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME seconds in STAGE",
                data={
                    "TIME": (self.survival_time_range_hyper_high, 1),
                    "STAGE": (self.stages_hyper, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME Seconds in STAGE, then SECOND Seconds in OTHER consecutively",
                data={
                    "TIME": (self.survival_time_range_low, 1),
                    "STAGE": (self.stages, 1),
                    "SECOND": (self.survival_time_range_low, 1),
                    "OTHER": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME Seconds in STAGE, then SECOND Seconds in OTHER consecutively",
                data={
                    "TIME": (self.survival_time_range_low, 1),
                    "STAGE": (self.stages, 1),
                    "SECOND": (self.survival_time_range_hyper_low, 1),
                    "OTHER": (self.stages_hyper, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME Seconds in STAGE, then SECOND Seconds in OTHER consecutively",
                data={
                    "TIME": (self.survival_time_range_high, 1),
                    "STAGE": (self.stages, 1),
                    "SECOND": (self.survival_time_range_low, 1),
                    "OTHER": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME Seconds in STAGE, then SECOND Seconds in OTHER consecutively",
                data={
                    "TIME": (self.survival_time_range_high, 1),
                    "STAGE": (self.stages, 1),
                    "SECOND": (self.survival_time_range_hyper_low, 1),
                    "OTHER": (self.stages_hyper, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME Seconds in STAGE, then SECOND Seconds in OTHER consecutively",
                data={
                    "TIME": (self.survival_time_range_hyper_low, 1),
                    "STAGE": (self.stages_hyper, 1),
                    "SECOND": (self.survival_time_range_low, 1),
                    "OTHER": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Survive for TIME Seconds in STAGE, then SECOND Seconds in OTHER consecutively",
                data={
                    "TIME": (self.survival_time_range_hyper_low, 1),
                    "STAGE": (self.stages_hyper, 1),
                    "SECOND": (self.survival_time_range_hyper_low, 1),
                    "OTHER": (self.stages_hyper, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def stages() -> List[str]:
        return [
            "Hexagon",
            "Hexagoner",
            "Hexagonest",
        ]

    @staticmethod
    def stages_hyper() -> List[str]:
        return [
            "Hyper Hexagon",
            "Hyper Hexagoner",
            "Hyper Hexagonest",
        ]

    @staticmethod
    def survival_time_range_low() -> range:
        return range(10, 26)

    @staticmethod
    def survival_time_range_high() -> range:
        return range(26, 51)

    @staticmethod
    def survival_time_range_hyper_low() -> range:
        return range(5, 11)

    @staticmethod
    def survival_time_range_hyper_high() -> range:
        return range(11, 21)


# Archipelago Options
# ...
