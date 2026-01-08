from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TetrisEffectConnectedArchipelagoOptions:
    pass


class TetrisEffectConnectedGame(Game):
    # Initial Proposal by @esther_emi on Discord
    # Expanded by SerpentAI

    name = "Tetris Effect: Connected"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = TetrisEffectConnectedArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use an Initial Speed LV. of LEVEL (when possible)",
                data={
                    "LEVEL": (self.initial_speed_level_range, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Score SCORE points in MODE mode. Stage: STAGE",
                data={
                    "SCORE": (self.score_marathon_range, 1),
                    "MODE": (self.modes_marathon, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Clear LINE lines in MODE mode. Stage: STAGE",
                data={
                    "LINE": (self.line_range, 1),
                    "MODE": (self.modes_marathon, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Achieve TETRIS Tetris line clears in Endless MODE mode. Stage: STAGE",
                data={
                    "TETRIS": (self.tetris_range, 1),
                    "MODE": (self.modes_marathon, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Perform TSPIN T-Spins in Endless MODE mode games. Stage: STAGE",
                data={
                    "TSPIN": (self.tspin_range, 1),
                    "MODE": (self.modes_marathon, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points in Ultra mode",
                data={
                    "SCORE": (self.score_ultra_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach level LEVEL in Classic Score Attack mode",
                data={
                    "LEVEL": (self.level_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play a round of MODE mode",
                data={
                    "MODE": (self.modes_others, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def initial_speed_level_range() -> List[int]:
        return list(range(1, 9))

    @staticmethod
    def modes_marathon() -> List[str]:
        return [
            "Marathon",
            "Zone Marathon",
        ]

    @staticmethod
    def modes_others() -> List[str]:
        return [
            "Sprint",
            "Master",
            "Countdown",
            "Mystery",
            "Purify",
        ]

    @staticmethod
    def stages() -> List[str]:
        return [
            "1989",
            "Aurora Peak",
            "Balloon High",
            "Celebration",
            "Da Vinci",
            "Deserted",
            "Dolphin Surf",
            "Downtown Jazz",
            "Forest Dawn",
            "Hula Soul",
            "Jellyfish Chorus",
            "Jeweled Veil",
            "Kaleidoscope",
            "Karma Wheel",
            "Mermaid Cove",
            "Metamorphosis",
            "Orbit",
            "Pharaoh's Code",
            "Prayer Circles",
            "Ritual Passion",
            "Spirit Canyon",
            "Starfall",
            "Stratosphere",
            "Sunset Breeze",
            "The Deep",
            "Turtle Dreams",
            "Yin & Yang",
            "Zen Blossoms",
        ]

    @staticmethod
    def score_marathon_range() -> range:
        return range(5000, 200000, 1000)

    @staticmethod
    def score_ultra_range() -> range:
        return range(1000, 15000, 100)

    @staticmethod
    def line_range() -> range:
        return range(50, 151)

    @staticmethod
    def tetris_range() -> range:
        return range(5, 21)

    @staticmethod
    def tspin_range() -> range:
        return range(5, 11)

    @staticmethod
    def level_range() -> range:
        return range(5, 21)

# Archipelago Options
# ...
