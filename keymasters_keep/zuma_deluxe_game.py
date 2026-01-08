from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ZumaDeluxeArchipelagoOptions:
    pass


class ZumaDeluxeGame(Game):
    name = "Zuma Deluxe"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.X360,
        KeymastersKeepGamePlatforms.XBOX,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = ZumaDeluxeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Ball Switching is not allowed",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Must obtain COUNT Bonus Coins when clearing a level",
                data={
                    "COUNT": (self.bonus_coin_count_range, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Clear the following Temple in Adventure Mode: TEMPLE",
                data={
                    "TEMPLE": (self.adventure_mode_temples, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In Gauntlet Survival, reach CLASSIFICATION on LEVEL",
                data={
                    "CLASSIFICATION": (self.gauntlet_classifications, 1),
                    "LEVEL": (self.gauntlet_levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="In Gauntlet Survival, score at least SCORE on LEVEL",
                data={
                    "SCORE": (self.gauntlet_score_range, 1),
                    "LEVEL": (self.gauntlet_levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="In Gauntlet Survival, reach CLASSIFICATION back-to-back on LEVELS",
                data={
                    "CLASSIFICATION": (self.gauntlet_classifications, 1),
                    "LEVELS": (self.gauntlet_levels, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In Gauntlet Survival, score at least SCORE back-to-back on LEVELS",
                data={
                    "SCORE": (self.gauntlet_score_range, 1),
                    "LEVELS": (self.gauntlet_levels, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def bonus_coin_count_range() -> range:
        return range(2, 5)

    @staticmethod
    def adventure_mode_temples() -> List[str]:
        return [
            "Temple of Zukulkan (Stage 1)",
            "Quetzal Quatl (Stage 2)",
            "Popo Poyolli (Stage 3)",
            "Secret Shrine of Zuma (Stage 4)",
        ]

    @staticmethod
    def gauntlet_levels() -> List[str]:
        return [
            "Spiral of Doom",
            "Osprey Talon",
            "Riverbed Mosaic",
            "Breath of Ehecatl",
            "Dark Vortex",
            "Switchback",
            "Long Range",
            "When Spirals Attack",
            "Mud Slide",
            "Rorschach",
            "Mouth of Centeotl",
            "Snake Pit",
            "Sand Garden",
            "Lair of the Mud Snake",
            "Landing Pad",
            "Altar of Tlaloc",
            "Codex of Mixtec",
            "Shrine of Quetzalcoatl",
            "Mirror Serpent",
            "Sun Stone",
            "Zumaic Exodus",
        ]

    @staticmethod
    def gauntlet_classifications() -> List[str]:
        return [
            "Rabbit 1",
            "Rabbit 2",
            "Rabbit 3",
            "Rabbit 4",
            "Rabbit 5",
            "Rabbit 6",
            "Rabbit 7",
            "Eagle 1",
            "Eagle 2",
            "Eagle 3",
            "Eagle 4",
            "Eagle 5",
            "Eagle 6",
            "Eagle 7",
            "Jaguar 1",
            "Jaguar 2",
            "Jaguar 3",
            "Jaguar 4",
            "Jaguar 5",
            "Jaguar 6",
            "Jaguar 7",
            "Sun God",
        ]

    @staticmethod
    def gauntlet_score_range() -> range:
        return range(20000, 100001, 5000)


# Archipelago Options
# ...
