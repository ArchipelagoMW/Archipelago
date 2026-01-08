from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Persona4ArenaUltimaxArchipelagoOptions:
    pass


class Persona4ArenaUltimaxGame(Game):
    name = "Persona 4 Arena Ultimax"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.ARC,
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.X360,
    ]

    is_adult_only_or_unrated = False

    options_cls = Persona4ArenaUltimaxArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete Arcade Mode using CHARACTER on DIFFICULTY difficulty",
                data={
                    "CHARACTER": (self.characters, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete Arcade Mode using CHARACTER on Hard difficulty",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In Versus Mode, play as CHARACTER and fight OPPONENT on MODE",
                data={
                    "CHARACTER": (self.characters, 1),
                    "OPPONENT": (self.characters, 1),
                    "MODE": (self.modes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="In Challenge Mode, complete Challenge #CHALLENGE as CHARACTER",
                data={
                    "CHALLENGE": (self.challenge_range_count_low, 1),
                    "CHARACTER": (self.characters_non_shadow, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="In Challenge Mode, complete Challenge #CHALLENGE as CHARACTER",
                data={
                    "CHALLENGE": (self.challenge_range_count_high, 1),
                    "CHARACTER": (self.characters_non_shadow, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In Score Attack Mode, complete Course COURSE on DIFFICULTY as CHARACTER",
                data={
                    "COURSE": (self.courses, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTER": (self.characters_non_shadow, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In Score Attack Mode, complete Course COURSE on Hard as CHARACTER",
                data={
                    "COURSE": (self.courses, 1),
                    "CHARACTER": (self.characters_non_shadow, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Margaret",
            "Sho Minazuki",
            "Naoto Shirogane (Normal Type)",
            "Teddie (Normal Type)",
            "Yukiko Amagi (Normal Type)",
            "Yu Narukami (Normal Type)",
            "Yosuke Hanamura (Normal Type)",
            "Chie Satonaka (Normal Type)",
            "Kanji Tatsumi (Normal Type)",
            "Sho Minazuki (With Persona)",
            "Marie",
            "Ken Amada & Koromaru (Normal Type)",
            "Yukari Takeba (Normal Type)",
            "Labrys (Normal Type)",
            "Mitsuru Kirijo (Normal Type)",
            "Aigis (Normal Type)",
            "Tohru Adachi",
            "Elizabeth",
            "Akihiko Sanada (Normal Type)",
            "Shadow Labrys",
            "Junpei Iori (Normal Type)",
            "Rise Kujikawa (Normal Type)",
            "Naoto Shirogane (Shadow Type)",
            "Teddie (Shadow Type)",
            "Yukiko Amagi (Shadow Type)",
            "Yu Narukami (Shadow Type)",
            "Yosuke Hanamura (Shadow Type)",
            "Chie Satonaka (Shadow Type)",
            "Kanji Tatsumi (Shadow Type)",
            "Ken Amada & Koromaru (Shadow Type)",
            "Yukari Takeba (Shadow Type)",
            "Labrys (Shadow Type)",
            "Mitsuru Kirijo (Shadow Type)",
            "Aigis (Shadow Type)",
            "Akihiko Sanada (Shadow Type)",
            "Junpei Iori (Shadow Type)",
            "Rise Kujikawa (Shadow Type)",
        ]

    @staticmethod
    def characters_non_shadow() -> List[str]:
        return [
            "Margaret",
            "Sho Minazuki",
            "Naoto Shirogane (Normal Type)",
            "Teddie (Normal Type)",
            "Yukiko Amagi (Normal Type)",
            "Yu Narukami (Normal Type)",
            "Yosuke Hanamura (Normal Type)",
            "Chie Satonaka (Normal Type)",
            "Kanji Tatsumi (Normal Type)",
            "Sho Minazuki (With Persona)",
            "Marie",
            "Ken Amada & Koromaru (Normal Type)",
            "Yukari Takeba (Normal Type)",
            "Labrys (Normal Type)",
            "Mitsuru Kirijo (Normal Type)",
            "Aigis (Normal Type)",
            "Tohru Adachi",
            "Elizabeth",
            "Akihiko Sanada (Normal Type)",
            "Shadow Labrys",
            "Junpei Iori (Normal Type)",
            "Rise Kujikawa (Normal Type)",
        ]

    @staticmethod
    def challenge_range_count_low() -> range:
        return range(11, 16)

    @staticmethod
    def challenge_range_count_high() -> range:
        return range(16, 21)

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
        ]

    @staticmethod
    def courses() -> List[str]:
        return [
            "A",
            "B",
            "C",
            "D",
        ]

    @staticmethod
    def modes() -> List[str]:
        return [
            "Regular",
            "Boss",
        ]


# Archipelago Options
# ...
