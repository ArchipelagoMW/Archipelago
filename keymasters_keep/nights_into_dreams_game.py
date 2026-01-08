from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import Toggle


@dataclass
class NightsIntoDreamsArchipelagoOptions:
    nights_into_dreams_enable_christmas: NightsIntoDreamsEnableChristmas


class NightsIntoDreamsGame(Game):
    name = "NiGHTS into Dreams..."
    platform = KeymastersKeepGamePlatforms.SAT

    platforms_other = [
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.PS2,
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.X360
    ]

    is_adult_only_or_unrated = False
    options_cls = NightsIntoDreamsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(label="No Acrobatics!", data={})
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Clear STAGE with RANK rank or greater",
                data={"STAGE": (self.stages, 1), "RANK": (self.ranks, 1)},
                weight=8
            ),
            GameObjectiveTemplate(
                label="Lead the lost car to the garage in the Mystic Forest",
                data={},
                weight=1
            ),
            GameObjectiveTemplate(
                label="Paraloop all of Gillwing's tail in a single hit",
                data={},
                weight=1,
                is_difficult=True,
            ),
            GameObjectiveTemplate(
                label="Achieve a RATING rating while NiGHTS has a Trick Ribbon",
                data={"RATING": (self.acrobat_ratings, 1)},
            )
        ]

    def stages(self):
        stages = [
            "Spring Valley",
            "Mystic Forest",
            "Soft Museum",
            "Splash Garden",
            "Frozen Bell",
            "Stick Canyon",
            "Twin Seeds"
        ]

        if self.archipelago_options.nights_into_dreams_enable_christmas:
            stages.append("Christmas Spring Valley")
        return stages

    @staticmethod
    def ranks():
        return ["E", "D", "C", "B", "A"]

    @staticmethod
    def acrobat_ratings():
        return [
            "-DO NOT MIND!-",
            "-NICE ONE-",
            "-NICE TWO-",
            "-NICE THREE-",
            "-WONDERFUL FOUR-",
            "-WONDERFUL FIVE!-",
            "-FANTASTIC SIX!!-",
            "-EXCELLENT SEVEN!!-",
            "-COOL EIGHT!!-",
            "-MARVELOUS NINE!!-",
            "-SUPERB TEN!!-",
            "-DREAMY !!!-",
        ]


class NightsIntoDreamsEnableChristmas(Toggle):
    """
    Whether objectives involving the Christmas version of Spring Valley should be included
    """

    display_name = "NiGHTS into Dreams... Enable Christmas"
