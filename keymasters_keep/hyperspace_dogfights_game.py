from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HyperspaceDogfightsArchipelagoOptions:
    pass


class HyperspaceDogfightsGame(Game):
    name = "Hyperspace Dogfights"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = HyperspaceDogfightsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Don't purchase the leftmost 2 shop items",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't open tier X chests",
                data={
                    "X": (self.chesttiers, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Once you find a DAMAGETYPE weapon, you must exclusively use DAMAGETYPE weapons",
                data={
                    "DAMAGETYPE": (self.damagetypes, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Don't use strafe or reverse thrusters",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Enable Iron Dog",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Enable Hardgrade",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Enable Control, but you can only take 2 items/weapons per zone",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Enable Time Killer. You must beat the run in under 30 minutes",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run with JET",
                data={
                    "JET": (self.jets, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a run with STRAY",
                data={
                    "STRAY": (self.strays, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a run with any of JET with PHAGE",
                data={
                    "JET": (self.jets, 3),
                    "PHAGE": (self.phages, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get to Endless wave WAVE with JET",
                data={
                    "WAVE": (self.endlesswaves, 1),
                    "JET": (self.jets, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a run with 3 different jets with PHAGES",
                data={
                    "PHAGES": (self.phages, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def chesttiers() -> range:
        return range(1, 5)

    @staticmethod
    def damagetypes() -> List[str]:
        return [
            "Kinetic",
            "Explosive",
            "Melee",
            "Photon",
        ]

    @staticmethod
    def jets() -> List[str]:
        return [
            "Paw MK1",
            "Paw MK2",
            "Fur MK1",
            "Fur MK2",
            "Fang MK1",
            "Fang MK2",
            "Eye MK1",
            "Eye MK2",
            "Tail MK1",
            "Tail MK2",
            "Collar MK1",
            "Collar MK2",
            "Nose MK1",
            "Nose MK2",
        ]

    @staticmethod
    def strays() -> List[str]:
        return [
            "Paw Stray",
            "Fur Stray",
            "Fang Stray",
            "Eye Stray",
            "Tail Stray",
            "Collar Stray",
            "Nose Stray",
        ]

    @staticmethod
    def phages() -> List[str]:
        return [
            "Hardgrade",
            "Iron Dog",
            "Regicide",
            "Time Killer",
            "Control",
            "Friction Fury",
            "Datacide",
            "Plate Flood",
            "Deconstruct",
            "True DMZ",
            "Field-Parasite",
            "Repli-Parasite",
        ]

    @staticmethod
    def endlesswaves() -> List[str]:
        return [
            "4",
            "5",
            "6",
            "9",
            "10",
            "15",
            "20",
        ]

# Archipelago Options
# ...
