from __future__ import annotations

import functools
from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RhythmDoctorArchipelagoOptions:
    rhythm_doctor_custom_levels: RhythmDoctorCustomLevels


class RhythmDoctorGame(Game):
    # Initial Proposal by @im_not_original on Discord

    name = "Rhythm Doctor"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = RhythmDoctorArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on DIFFICULTY difficulty",
                data={"DIFFICULTY": (self.difficulties, 1)},
            ),
            GameObjectiveTemplate(
                label="Play with 2 players enabled",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Get a RANK rank or above in LEVEL",
                data={
                    "RANK": (self.ranks, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Get an A rank or above in LEVEL",
                data={
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Get a RANK rank or above in LEVEL while on SPEED",
                data={
                    "RANK": (self.ranks, 1),
                    "LEVEL": (self.levels, 1),
                    "SPEED": (self.speeds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get an A rank or above in LEVEL while on SPEED",
                data={
                    "LEVEL": (self.levels, 1),
                    "SPEED": (self.speeds, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get a RANK rank or above in LEVEL",
                data={
                    "RANK": (self.ranks, 1),
                    "LEVEL": (self.levels_night, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Get an A rank or above in LEVEL",
                data={
                    "LEVEL": (self.levels_night, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get a RANK rank or above in LEVEL while on SPEED",
                data={
                    "RANK": (self.ranks, 1),
                    "LEVEL": (self.levels_night, 1),
                    "SPEED": (self.speeds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get an A rank or above in LEVEL while on SPEED",
                data={
                    "LEVEL": (self.levels_night, 1),
                    "SPEED": (self.speeds, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete BOSS",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Perfect BOSS",
                data={
                    "BOSS": (self.bosses, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete BOSS while on SPEED",
                data={
                    "BOSS": (self.bosses, 1),
                    "SPEED": (self.speeds, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Perfect BOSS while on SPEED",
                data={
                    "BOSS": (self.bosses, 1),
                    "SPEED": (self.speeds, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get a RANK rank or above in LEVEL",
                data={
                    "RANK": (self.ranks, 1),
                    "LEVEL": (self.levels_bonus, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Get an A rank or above in LEVEL",
                data={
                    "LEVEL": (self.levels_bonus, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get a RANK rank or above in LEVEL while on SPEED",
                data={
                    "RANK": (self.ranks, 1),
                    "LEVEL": (self.levels_bonus, 1),
                    "SPEED": (self.speeds, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get an A rank or above in LEVEL while on SPEED",
                data={
                    "LEVEL": (self.levels_bonus, 1),
                    "SPEED": (self.speeds, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def custom_tracks(self) -> Set[str]:
        return sorted(self.archipelago_options.rhythm_doctor_custom_levels.value)

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
        ]

    @staticmethod
    def ranks() -> List[str]:
        return [
            "D",
            "C",
            "B",
        ]

    @staticmethod
    def speeds() -> List[str]:
        return [
            "doublespeed (chili)",
            "halfspeed/slowdown (ice)",
        ]

    @functools.cached_property
    def levels_base(self) -> List[str]:
        return [
            "1-1: Samurai Techno",
            "1-2: Intimate",
            "2-1: Loft Hip-Hop Beats To Treat Patients To",
            "2-2: Supraventricular Tachycardia",
            "2-3: Puff Piece",
            "2-4: Song of the Sea",
            "3-1: Sleepy Garden",
            "3-2: Classy",
            "3-3: Distant Duet",
            "4-1: Training Doctor's Train Ride Performance",
            "4-2: Invisible",
            "4-3: Steinway",
            "4-4: Know you",
            "5-1: Lucky Break",
            "5-2: Lo-fi Beats For Patients To Chill To",
            "5-3: Seventh-Inning Stretch",
        ]

    def levels(self) -> List[str]:
        levels: List[str] = self.levels_base[:]

        if len(self.custom_tracks):
            levels.extend(self.custom_tracks)

        return sorted(levels)

    @staticmethod
    def levels_night() -> List[str]:
        return [
            "1-1N: Samurai Dubstep",
            "1-2N: Intimate (Night)",
            "2-1N: wish i could care less",
            "2-2N: Unreachable",
            "2-3N: Bomb-Sniffing Pomeranian",
            "2-4N: Song of the Sea (Night)",
            "3-1N: Lounge",
            "3-2N: Classy (Night)",
            "3-3N: Distant Duet (Night)",
            "4-1N: Rollerdisco Rumble",
            "4-2N: Invisible (Night)",
            "4-3N: Steinway Reprise",
            "4-4N: Murmurs",
            "5-1N: One Slip Too Late",
            "5-2N: Unsustainable Inconsolable",
        ]

    @staticmethod
    def levels_bonus() -> List[str]:
        return [
            "X-0: Helping Hands",
            "X-1: Art Exercise",
            "X-MAT: Meet and Tweet",
            "X-WOT: Worn Out Tapes",
            "X-KOB: Kingdom of Balloons",
            "X-FTS: Fixations Towards the Stars",
            "MD-1: Blackest Luxury Car",
            "MD-2: tape/stop/night",
            "MD-3: The 90's Decision",
            "2-B1: Beans Hopper",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "1-X: Battleworn Insomniac",
            "2-X: All The Times",
            "3-X: One Shift More",
            "1-XN: Super Battleworn Insomniac",
            "5-X: Dreams Don't Stop",
        ]


# Archipelago Options
class RhythmDoctorCustomLevels(OptionSet):
    """
    Indicates which Rhythm Doctor custom levels the player has installed.
    """

    display_name = "Rhythm Doctor Custom Levels"
    default = list()
