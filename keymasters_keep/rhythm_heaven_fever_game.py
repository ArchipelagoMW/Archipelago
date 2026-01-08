from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RhythmHeavenFeverArchipelagoOptions:
    rhythm_heaven_fever_perfects_enabled: RhythmHeavenFeverPerfectsEnabled


class RhythmHeavenFeverGame(Game):
    name = "Rhythm Heaven Fever"
    platform = KeymastersKeepGamePlatforms.WII

    platforms_other = [
        KeymastersKeepGamePlatforms.WIIU,
    ]

    is_adult_only_or_unrated = False

    options_cls = RhythmHeavenFeverArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Get RESULT in LEVEL",
                data={
                    "RESULT": (self.results, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ]

        if self.perfects_enabled:
            templates.extend([
                GameObjectiveTemplate(
                    label="Get Perfect in LEVEL",
                    data={
                        "LEVEL": (self.levels_without_night_walk, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        return templates

    @property
    def perfects_enabled(self) -> bool:
        return bool(self.archipelago_options.rhythm_heaven_fever_perfects_enabled.value)

    @staticmethod
    def results() -> List[str]:
        return [
            "OK or better",
            "Superb or better",
        ]

    @staticmethod
    def levels() -> List[str]:
        return [
            "Hole In One",
            "Screwbot Factory",
            "See-Saw",
            "Double Date",
            "Remix 1",
            "Fork Lifter",
            "Tambourine",
            "Board Meeting",
            "Monkey Watch",
            "Remix 2",
            "Working Dough",
            "Built to Scale",
            "Air Rally",
            "Figure Fighter",
            "Remix 3",
            "Ringside",
            "Packing Pests",
            "Micro-Row",
            "Samurai Slice",
            "Remix 4",
            "Catch of the Day",
            "Flipper-Flop",
            "Exhibition Match",
            "Flock Step",
            "Remix 5",
            "Launch Party",
            "Donk-Donk",
            "Bossa Nova",
            "Love Rap",
            "Remix 6",
            "Tap Troupe",
            "Shrimp Shuffle",
            "Cheer Readers",
            "Karate Man",
            "Remix 7",
            "Samurai Slice 2",
            "Working Dough 2",
            "Built to Scale 2",
            "Double Date 2",
            "Remix 8",
            "Love Rap 2",
            "Cheer Readers 2",
            "Hole in One 2",
            "Screwbot Factory 2",
            "Remix 9",
            "Figure Fighter 2",
            "Micro-Row 2",
            "Packing Pests 2",
            "Karate Man 2",
            "Remix 10",
            "Night Walk",
        ]

    def levels_without_night_walk(self) -> List[str]:
        levels: List[str] = self.levels()[:]

        if "Night Walk" in levels:
            levels.remove("Night Walk")

        return levels


# Archipelago Options
class RhythmHeavenFeverPerfectsEnabled(Toggle):
    """
    Indicates whether the player wants to have to get Rhythm Heaven Fever Perfect grades included in their objectives.
    """

    display_name = "Rhythm Heaven Fever Perfects Enabled"
