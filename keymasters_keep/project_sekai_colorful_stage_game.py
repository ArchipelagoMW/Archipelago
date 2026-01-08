from __future__ import annotations

from typing import List
from math import ceil

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

from Options import Choice, OptionSet


@dataclass
class ProjectSekaiColorfulStageArchipelagoOptions:
    project_sekai_colorful_stage_additional_songs: ProjectSekaiColorfulStageAdditionalSongs
    project_sekai_colorful_stage_minimum_difficulty: ProjectSekaiColorfulStageMinimumDifficulty
    project_sekai_colorful_stage_maximum_difficulty: ProjectSekaiColorfulStageMaximumDifficulty


# Pair setup

virtual_singers = [
    "Hatsune Miku",
    "Kagamine Rin",
    "Kagamine Len",
    "Megurine Luka",
    "MEIKO",
    "KAITO"
]

leo_need = [
    "Ichika Hoshino",
    "Saki Tenma",
    "Shiho Hinomori",
    "Honami Mochizuki"
]

more_more_jump = [
    "Minori Hanasato",
    "Haruka Kiritani",
    "Airi Momoi",
    "Shizuku Hinomori"
]

vivid_bad_squad = [
    "Kohane Azusawa",
    "An Shiraishi",
    "Akito Shinonome",
    "Toya Aoyagi"
]

wonderlands_x_showtime = [
    "Tsukasa Tenma",
    "Emu Otori",
    "Rui Kamishiro",
    "Nene Kusanagi"
]

nightcord_at_2500 = [
    "Kanade Yoisaki",
    "Mafuyu Asahina",
    "Ena Shinonome",
    "Mizuki Akiyama"
]

pairs = [
    # intra-group pairs
    "Shiho Hinomori and Shizuku Hinomori",
    "Saki Tenma and Tsukasa Tenma",
    "Akito Shinonome and Ena Shinonome",
    # cross-leader pairs
    "Ichika Hoshino and Minori Hanasato",
    "Ichika Hoshino and Kohane Azusawa",
    "Ichika Hoshino and Tsukasa Tenma",
    "Ichika Hoshino and Kanade Yoisaki",
    "Minori Hanasato and Kohane Azusawa",
    "Minori Hanasato and Tsukasa Tenma",
    "Minori Hanasato and Kanade Yoisaki",
    "Kohane Azusawa and Tsukasa Tenma",
    "Kohane Azusawa and Kanade Yoisaki",
    "Tsukasa Tenma and Kanade Yoisaki",
    # one singular song, not including April Fools for now
    "Robo-Nene and Mikudayo"
]
for group in [leo_need, more_more_jump, vivid_bad_squad, wonderlands_x_showtime, nightcord_at_2500, virtual_singers]:
    for member in group:
        for secondary in sorted({*group, *virtual_singers}):
            if member == secondary:
                pairs.append(member)
            else:
                pairs.append(f"{member} and {secondary}")


class ProjectSekaiColorfulStageGame(Game):
    name = "Project Sekai: Colorful Stage"
    platform = KeymastersKeepGamePlatforms.AND

    platforms_other = [KeymastersKeepGamePlatforms.IOS]

    is_adult_only_or_unrated = False

    options_cls = ProjectSekaiColorfulStageArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives = [
            GameObjectiveTemplate(
                label="Complete a show featuring PAIR",
                data={"PAIR": (self.characters, 1)},
                weight=10
            ),
            GameObjectiveTemplate(
                label="Complete a show featuring PAIR with 7 or less GOOD/BAD/MISS",
                data={"PAIR": (self.characters, 1)},
                weight=4
            ),
            GameObjectiveTemplate(
                label="Complete a show featuring PAIR on DIFF difficulty (or higher)",
                data={"PAIR": (self.characters, 1), "DIFF": (self.difficulties, 1)},
                weight=6
            ),
            GameObjectiveTemplate(
                label="Complete a show featuring PAIR on DIFF difficulty (or higher) with 7 or less GOOD/BAD/MISS",
                data={"PAIR": (self.characters, 1), "DIFF": (self.difficulties, 1)},
                is_difficult=True,  # arguable but it is asking a bit more out of you
                weight=2
            ),
            GameObjectiveTemplate(
                label="Complete NUM shows with 3DMVs",
                data={"NUM": ((lambda: list(range(3, 11))), 1)},
                weight=2
            ),
            GameObjectiveTemplate(
                label="Complete NUM shows with 2DMVs/Original MVs",
                data={"NUM": ((lambda: list(range(3, 11))), 1)},
                weight=2
            ),
            GameObjectiveTemplate(
                label="Complete NUM Co-op/Cheerful Shows",
                data={"NUM": ((lambda: list(range(3, 11))), 1)},
                weight=4
            ),
            GameObjectiveTemplate(
                label="Complete NUM shows featuring songs from the following groups: GROUP",
                data={"GROUP": (self.groups, range(1, 4)), "NUM": ((lambda: list(range(3, 11))), 1)},
                weight=6
            ),
            GameObjectiveTemplate(
                label="Complete NUM shows with Mirror Mode enabled",
                data={"NUM": ((lambda: list(range(3, 11))), 1)},
                weight=3
            ),
            GameObjectiveTemplate(
                label="Achieve 3 Full Combos during shows",
                data={},
                is_difficult=self.archipelago_options.project_sekai_colorful_stage_maximum_difficulty.value < ProjectSekaiColorfulStageMaximumDifficulty.option_hard,
                weight=3
            ),
            GameObjectiveTemplate(
                label="Achieve a Full Combo during a show featuring PAIR",
                data={"PAIR": (self.characters, 1)},
                is_difficult= self.archipelago_options.project_sekai_colorful_stage_maximum_difficulty.value < ProjectSekaiColorfulStageMaximumDifficulty.option_hard,
                weight=3
            ),
            GameObjectiveTemplate(
                label="Achieve a Full Combo during a show on DIFF difficulty",
                data={"DIFF": (self.difficulties, 1)},
                is_difficult=self.archipelago_options.project_sekai_colorful_stage_maximum_difficulty.value < ProjectSekaiColorfulStageMaximumDifficulty.option_hard,
                weight=3
            ),
            GameObjectiveTemplate(
                label="Achieve an All Perfect during a show",
                data={},
                is_difficult=True,
                weight=1
            )
        ]

        if self.archipelago_options.project_sekai_colorful_stage_maximum_difficulty in ("expert", "master"):
            objectives.extend([
                GameObjectiveTemplate(
                    label="Complete a show on APPEND difficulty",
                    data={},
                    weight=4
                ),
                GameObjectiveTemplate(
                    label="Complete a show on APPEND difficulty with 7 or less GOOD/BAD/MISS",
                    data={},
                    is_difficult=True,
                    is_time_consuming=True,
                    weight=2
                ),
            ])
        else:
            objectives.append(GameObjectiveTemplate(
                label="Finish a show on APPEND difficulty",
                data={},
                weight=2
            ))

        if self.archipelago_options.project_sekai_colorful_stage_additional_songs:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Play SONG on DIFF difficulty (or higher)",
                    data={"SONG": (self.songs, 1), "DIFF": (self.difficulties, 1)},
                    weight=min(10, max(1, ceil(len(self.songs()) / 4)))
                ),
                GameObjectiveTemplate(
                    label="Play SONG on DIFF difficulty (or higher) with 7 or less GOOD/BAD/MISS",
                    data={"SONG": (self.songs, 1), "DIFF": (self.difficulties, 1)},
                    weight=min(10, max(1, ceil(len(self.songs()) / 4) - 2))
                ),
            ])

        return objectives

    @staticmethod
    def characters():
        return pairs

    def difficulties(self):
        difficulties = [
            "Easy",
            "Normal",
            "Hard",
            "Expert",
            "Master"
        ]
        return difficulties[self.archipelago_options.project_sekai_colorful_stage_minimum_difficulty.value:
                            self.archipelago_options.project_sekai_colorful_stage_maximum_difficulty.value + 1]

    def songs(self):
        return sorted(self.archipelago_options.project_sekai_colorful_stage_additional_songs.value)

    @staticmethod
    def groups():
        return [
            "VIRTUAL SINGERs",
            "Leo/need",
            "MORE MORE JUMP!",
            "Vivid BAD Squad",
            "Wonderlands X Showtime",
            "Nightcord at 25:00"
        ]


class ProjectSekaiColorfulStageAdditionalSongs(OptionSet):
    """
    Additional songs that can be rolled as objectives in Project Sekai: Colorful Stage
    """

    display_name = "Project Sekai: Colorful Stage Additional Songs"


class ProjectSekaiColorfulStageMinimumDifficulty(Choice):
    """
    The minimum difficulty that should be rolled for objectives in Project Sekai: Colorful Stage
    """

    display_name = "Project Sekai: Colorful Stage Minimum Difficulty"

    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    option_master = 4

    default = 1


class ProjectSekaiColorfulStageMaximumDifficulty(Choice):
    """
    The maximum difficulty that should be rolled for objectives in Project Sekai: Colorful Stage (excluding APPEND)
    """
    display_name = "Project Sekai: Colorful Stage Maximum Difficulty"

    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_expert = 3
    option_master = 4

    default = 2
