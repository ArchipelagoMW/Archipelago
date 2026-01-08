from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class OldTVArchipelagoOptions:
    pass


class OldTVGame(Game):
    name = "OldTV"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = OldTVArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Lose to a COLOR-colored word in CONTINENT",
                data={
                    "COLOR": (self.colors, 1),
                    "CONTINENT": (self.continents, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach FREQUENCY Frequency",
                data={
                    "FREQUENCY": (self.frequencies, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish CONTINENT",
                data={
                    "CONTINENT": (self.continents, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Lose to MECHANIC D10 time(s)",
                data={
                    "MECHANIC": (self.mechanics, 1),
                    "D10": (self.d10_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Encounter a COLOR-colored OTHER",
                data={
                    "COLOR": (self.colors, 1),
                    "OTHER": (self.colors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Acquire D200 CP",
                data={
                    "D200": (self.d200_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach Channel D100 on Saturn",
                data={
                    "D100": (self.d100_range, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Lose to MECHANIC D10 time(s) in Saturn",
                data={
                    "MECHANIC": (self.saturn_mechanics, 1),
                    "D10": (self.d10_range, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Encounter a COLOR-colored OTHER in Saturn",
                data={
                    "COLOR": (self.saturn_colors, 1),
                    "OTHER": (self.saturn_colors, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach channel D10 with a language you do not know",
                data={
                    "D10": (self.d10_range, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
        ]

    @staticmethod
    def colors() -> List[str]:
        return [
            "Cyan",
            "Blue",
            "Green",
            "Red",
            "Yellow",
            "Purple",
        ]

    @staticmethod
    def saturn_colors() -> List[str]:
        return [
            "Cyan",
            "Blue",
            "Green",
            "Red",
            "Yellow",
            "Purple",
            "Pink",
            "Orange,"
        ]

    @staticmethod
    def mechanics() -> List[str]:
        return [
            "Colored Background",
            "Don't Switch",
            "Reversed Controls",
            "Lost Connection",
            "Upside Down",
            "Scrambled",
        ]

    @staticmethod
    def saturn_mechanics() -> List[str]:
        return [
            "Colored Background",
            "Don't Switch",
            "Reversed Controls",
            "Lost Connection",
            "Upside Down",
            "Scrambled",
            "Equals",
        ]

    @staticmethod
    def continents() -> List[str]:
        return [
            "Oceania",
            "Asia",
            "Europe",
            "Americas",
            "Africa",
        ]

    @staticmethod
    def frequencies() -> List[str]:
        return [
            "20 or better",
            "30 or better",
            "40 or better",
        ]

    @staticmethod
    def d10_range() -> range:
        return range(1, 11)

    @staticmethod
    def d100_range() -> range:
        return range(1, 101)

    @staticmethod
    def d200_range() -> range:
        return range(1, 201)

# Archipelago Options
# ...
