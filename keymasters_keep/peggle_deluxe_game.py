from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PeggleDeluxeArchipelagoOptions:
    peggle_deluxe_include_challenges: PeggleDeluxeIncludeChallenges
    peggle_deluxe_include_insane_challenges: PeggleDeluxeIncludeInsaneChallenges


class PeggleDeluxeGame(Game):
    name = "Peggle Deluxe"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = PeggleDeluxeArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Character: CHARACTER  CPU Level: CPU_LEVEL",
                data={
                    "CHARACTER": (self.characters, 1),
                    "CPU_LEVEL": (self.cpu_levels, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete the following stage: STAGE",
                data={
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Achieve a SHOT Style Shot in STAGE",
                data={
                    "SHOT": (self.style_shots, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Achieve a SHOT Style Shot in STAGE and complete it",
                data={
                    "SHOT": (self.style_shots, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a Duel against CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Full Clear the following stage: STAGE",
                data={
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
        ]

        if self.include_challenges:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete the following challenge: CHALLENGE",
                    data={
                        "CHALLENGE": (self.challenges, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete the following challenge: CHALLENGE",
                    data={
                        "CHALLENGE": (self.challenges_hard, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        return templates

    @property
    def include_challenges(self) -> bool:
        return bool(self.archipelago_options.peggle_deluxe_include_challenges.value)

    @property
    def include_insane_challenges(self) -> bool:
        return bool(self.archipelago_options.peggle_deluxe_include_insane_challenges.value)

    @staticmethod
    def characters() -> List[str]:
        return [
            "Bjorn",
            "Jimmy Lightning",
            "Kat Tut",
            "Splork",
            "Claude",
            "Renfield",
            "Tula",
            "Warren",
            "Lord Cinderbottom",
            "Master Hu",
        ]

    @staticmethod
    def stages() -> List[str]:
        return [
            "1-1: Peggleland",
            "1-2: Slip and Slide",
            "1-3: Bjorn's Gazebo",
            "1-4: Das Bucket",
            "1-5: Snow Day",
            "2-1: Birdy's Crib",
            "2-2: Buffalo Wings",
            "2-3: Skate Park",
            "2-4: Spiral of Doom",
            "2-5: Mr. Peepers",
            "3-1: Scarab Crunch",
            "3-2: Infinite Cheese",
            "3-3: Ra Deal",
            "3-4: Croco-Gator Pit",
            "3-5: The Fever Level",
            "4-1: The Amoeban",
            "4-2: The Last Flower",
            "4-3: We Come in Peace",
            "4-4: Maid in Space",
            "4-5: Getting the Spare",
            "5-1: Pearl Clam",
            "5-2: Insane Aquarium",
            "5-3: Tasty Waves",
            "5-4: Our Favorite Eel",
            "5-5: Love Story",
            "6-1: Waves",
            "6-2: Spiderweb",
            "6-3: Blockers",
            "6-4: Baseball",
            "6-5: Vermin",
            "7-1: Holland Oats",
            "7-2: I Heart Flowers",
            "7-3: Workin From Home",
            "7-4: Tula's Ride",
            "7-5: 70 and Sunny",
            "8-1: Win a Monkey",
            "8-2: Dog Pinball",
            "8-3: Spin Again",
            "8-4: Roll 'em",
            "8-5: Five of a Kind",
            "9-1: The Love Moat",
            "9-2: Doom with a View",
            "9-3: Rhombi",
            "9-4: 9 Luft Balloons",
            "9-5: Twisted SIsters",
            "10-1: Spin Cycle",
            "10-2: The Dude Abides",
            "10-3: When Pigs Fly",
            "10-4: Yang, Yin",
            "10-5: Zen Frog",
            "11-1: Paw Reader",
            "11-2: End of Time",
            "11-3: Billions & Billions",
            "11-4: Don't Panic",
            "11-5: Beyond Reason",
        ]

    @staticmethod
    def cpu_levels() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
            "Master",
        ]

    @staticmethod
    def style_shots() -> List[str]:
        return [
            "Long Shot",
            "Super Long Shot",
            "Free Ball Skills",
            "Orange Attack",
        ]

    @staticmethod
    def challenges() -> List[str]:
        return [
            "1-1: 35 Orange Pegs",
            "1-2: 35 Orange Pets",
            "1-3: 35 Orange Pests",
            "1-4: 35 Orange Posts",
            "1-5: 35 Orange Clams",
            "2-1: 45 Little Victories",
            "2-2: 45 Croco-Gators",
            "2-3: 45 Orange Things",
            "2-4: Only 45 Calories",
            "2-5: 45 is the New 25",
            "4-1: 300,000 Points",
            "4-2: 300 Grand",
            "4-3: 300 Kilopoints",
            "4-4: 3000 Benjamins",
            "4-5: 300,000 Pointer",
            "12-1: 2 for the Road",
            "12-2: 3 for Luck",
            "12-3: 4 to Get Better",
            "12-4: 5 to Get Stuck",
            "12-5: 6 Times the Fun",
            "13-1: Normal Tri Duel",
            "14-1: 750,000 Points",
            "14-2: 800,000 Points",
            "14-3: 850,000 Points",
            "14-4: 900,000 Points",
        ]

    @functools.cached_property
    def challenges_base_hard(self) -> List[str]:
        return [
            "3-1: Fifty-Five",
            "3-2: 50 Plus 5",
            "3-3: 11 Times 5",
            "3-4: 1+2+3+...+10",
            "3-5: Two Fives",
            "5-1: 350,000 Points",
            "5-2: 350,000 Puntos",
            "5-3: 350,000 Punti",
            "5-4: 350,000 Punten",
            "5-5: 350,000 Punkte",
            "6-1: 400,000 Points",
            "6-2: 40,000 P-Babies",
            "6-3: 4,000 Pecans",
            "6-4: 400 P-Dogs",
            "6-5: 40 Peeps",
            "13-2: Hard Tri Duel",
            "13-5: Master Tri Duel",
            "14-5: One Million Points",
        ]

    @functools.cached_property
    def challenges_insane(self) -> List[str]:
        return [
            "15-1: 2 Balls Left",
            "15-2: Last Ball",
            "15-3: Ten Ball Trial",
            "15-4: 750,000?",
            "15-5: The Decathalon",
        ]

    def challenges_hard(self) -> List[str]:
        challenges: List[str] = self.challenges_base_hard[:]

        if self.include_insane_challenges:
            challenges.extend(self.challenges_insane)

        return sorted(challenges)


# Archipelago Options
class PeggleDeluxeIncludeChallenges(Toggle):
    """
    Indicates whether to include Peggle Deluxe challenges when generating objectives.
    """

    display_name = "Peggle Deluxe Include Challenges"


class PeggleDeluxeIncludeInsaneChallenges(Toggle):
    """
    Indicates whether to include Peggle Deluxe insane challenges when generating objectives.
    """

    display_name = "Peggle Deluxe Include Insane Challenges"
