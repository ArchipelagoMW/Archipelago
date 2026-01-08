from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class HarryPotterQuidditchWorldCupArchipelagoOptions:
    harry_potter_quidditch_world_cup_bulgaria_unlocked: HarryPotterQuidditchWorldCupBulgariaUnlocked


class HarryPotterQuidditchWorldCupGame(Game):
    name = "Harry Potter: Quidditch World Cup"
    platform = KeymastersKeepGamePlatforms.PS2

    platforms_other = [
        KeymastersKeepGamePlatforms.GBA,
        KeymastersKeepGamePlatforms.GC,
        KeymastersKeepGamePlatforms.PC,
        KeymastersKeepGamePlatforms.XBOX,
    ]

    is_adult_only_or_unrated = False

    options_cls = HarryPotterQuidditchWorldCupArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use the BROOM in World Cup Related Challenges",
                data={
                    "BROOM": (self.brooms, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win the Hogwarts house cup as TEAM",
                data={
                    "TEAM": (self.teams_hogwarts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete the following Challenge as TEAM: CHALLENGE",
                data={
                    "TEAM": (self.teams_hogwarts, 1),
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win COUNT Game(s) as TEAM",
                data={
                    "COUNT": (self.game_count_range, 1),
                    "TEAM": (self.teams_hogwarts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win COUNT Game(s) as TEAM",
                data={
                    "COUNT": (self.game_count_range, 1),
                    "TEAM": (self.teams_international, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win The Quiditch World Cup as TEAM",
                data={
                    "TEAM": (self.teams_international, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win The Quiditch World Cup as TEAM with HOUSE as supporting Hogwarts house",
                data={
                    "TEAM": (self.teams_international, 1),
                    "HOUSE": (self.teams_hogwarts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def bulgaria_unlocked(self) -> bool:
        return bool(self.archipelago_options.harry_potter_quidditch_world_cup_bulgaria_unlocked.value)

    @staticmethod
    def teams_hogwarts() -> List[str]:
        return [
            "Gryffindor",
            "Hufflepuff",
            "Ravenclaw",
            "Slytherin",
        ]

    def teams_international(self) -> List[str]:
        teams: List[str] = [
            "England",
            "France",
            "Germany",
            "Nordic",
            "USA",
            "Japan",
            "Australia",
            "Spain",
        ]

        if self.bulgaria_unlocked:
            teams.append("Bulgaria")

        return sorted(teams)

    @staticmethod
    def challenges() -> List[str]:
        return [
            "Passing",
            "Tackle and Shoot",
            "Seeker",
            "Beaters and Bludgers",
            "Special Moves",
            "Combos",
        ]

    @staticmethod
    def brooms() -> List[str]:
        return [
            "Comet 260",
            "Nimbus 2000",
            "Nimbus 2001",
            "Firebolt",
        ]

    @staticmethod
    def game_count_range() -> range:
        return range(1, 4)


# Archipelago Options
class HarryPotterQuidditchWorldCupBulgariaUnlocked(Toggle):
    """
    Indicates whether the Bulgaria team is unlocked in Harry Potter: Quidditch World Cup
    """

    display_name = "Harry Potter: Quidditch World Cup Bulgaria Unlocked"
