from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class OriAndTheWillOfTheWispsArchipelagoOptions:
    pass


class OriAndTheWillOfTheWispsGame(Game):
    name = "Ori and the Will of the Wisps"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = OriAndTheWillOfTheWispsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Navigate between the following wells without being hit: WELLS",
                data={
                    "WELLS": (self.wells, 2)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete the RACE Spirit Trial",
                data={
                    "RACE": (self.shrines_race, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete the COMBAT Spirit Shrine",
                data={
                    "COMBAT": (self.shrines_combat, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete the COMBAT Spirit Shrine with only the following abilities: ABILITIES",
                data={
                    "COMBAT": (self.shrines_combat, 1),
                    "ABILITIES": (self.abilities, 3)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ]

    @staticmethod
    def wells() -> List[str]:
        return [
            "West Luma Pools",
            "East Luma Pools",
            "Wellspring",
            "Midnight Burrows",
            "Upper Inkwater Marsh",
            "Howl's Den",
            "Baur's Reach",
            "Kwolok's Hollow",
            "Wellspring Glades",
            "Mouldwood Depths",
            "Willow's End",
            "West Silent Woods",
            "East Silent Woods",
            "Feeding Grounds",
            "Lower Windswept Wastes",
            "Upper Windswept Wastes",
            "Windtorn Ruins",
        ]

    @staticmethod
    def shrines_race() -> List[str]:
        return [
            "Luma Pools",
            "Wellspring",
            "Inkwater Marsh",
            "Kwolok's Hollow",
            "Baur's Reach",
            "Mouldwood Depths",
            "Silent Woods",
            "Windswept Wastes",
        ]

    @staticmethod
    def shrines_combat() -> List[str]:
        return [
            "Wellspring",
            "Upper Inkwater Marsh",
            "Howl's Den",
            "Mouldwood Depths",
            "Silent Woods",
        ]

    @staticmethod
    def abilities() -> List[str]:
        return [
            "Spirit Edge",
            "Spirit Smash",
            "Spirit Arc",
            "Light Burst",
            "Flash",
            "Sentry",
            "Spirit Star",
            "Spike",
            "Blaze",
            "Regenerate",
            "Launch",
            "Flap",
        ]


# Archipelago Options
# ...
