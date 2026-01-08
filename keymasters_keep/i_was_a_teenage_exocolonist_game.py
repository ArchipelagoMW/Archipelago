from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class IWasATeenageExocolonistArchipelagoOptions:
    pass


class IWasATeenageExocolonistGame(Game):
    name = "I Was a Teenage Exocolonist"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = IWasATeenageExocolonistArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Gift CHARACTER a loved gift",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Gift CHARACTER a cake on their birthday",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Gift CHARACTER a COLLECTIBLE",
                data={
                    "CHARACTER": (self.characters, 1),
                    "COLLECTIBLE": (self.collectibles, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Max out the SKILL skill",
                data={
                    "SKILL": (self.skills, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Get Perk #COUNT from the following Skills: SKILLS",
                data={
                    "COUNT": (self.perk_count_range, 1),
                    "SKILLS": (self.skills, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach 100 friendship with FRIEND",
                data={
                    "FRIEND": (self.friends_easy, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Date DATE",
                data={
                    "DATE": (self.dates_easy, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Max out all COLOR skills",
                data={
                    "COLOR": (self.colors, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach 100 friendship with CHARACTERS at the same time",
                data={
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach 100 friendship with FRIEND",
                data={
                    "FRIEND": (self.friends_hard, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Date DATE",
                data={
                    "DATE": (self.dates_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="CHALLENGE",
                data={
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Have a deck with only COLOR and wildcard cards",
                data={
                    "COLOR": (self.colors, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Achieve the ENDING ending",
                data={
                    "ENDING": (self.special_endings, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def friends_easy() -> List[str]:
        return [
            "Dys",
            "Tangent",
            "Tammy",
            "Cal",
            "Marz",
            "Anemone",
            "Rex",
        ]

    @staticmethod
    def friends_hard() -> List[str]:
        return [
            "Vace",
            "Nomi",
            "Sym",
        ]

    @staticmethod
    def dates_easy() -> List[str]:
        return [
            "Dys",
            "Tangent",
            "Marz",
            "Anemone",
            "Rex",
        ]

    @staticmethod
    def dates_hard() -> List[str]:
        return [
            "Vace",
            "Nomi",
            "Sym",
            "Tammy",
            "Cal",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Dys",
            "Tangent",
            "Tammy",
            "Cal",
            "Marz",
            "Anemone",
            "Rex",
            "Vace",
            "Nomi",
            "Sym",
        ]

    @staticmethod
    def collectibles() -> List[str]:
        return [
            "Yellow Flower",
            "Blue Bobberfruit",
            "Xeno Egg",
            "Mushwood Log",
            "Medicinal Roots",
            "Crystal Cluster",
            "Strange Device",
            "Cake",
        ]

    @staticmethod
    def skills() -> List[str]:
        return [
            "Empathy",
            "Persuasion",
            "Creativity",
            "Bravery",
            "Reasoning",
            "Organizing",
            "Engineering",
            "Biology",
            "Toughness",
            "Perception",
            "Combat",
            "Animals",
        ]

    @staticmethod
    def colors() -> List[str]:
        return [
            "Yellow",
            "Blue",
            "Red",
        ]

    @staticmethod
    def challenges() -> List[str]:
        return [
            "Save Tammy",
            "Save Hal",
            "Save Tobin",
            "Save the Governor",
            "Save dad",
            "Save mom",
            "Solve the famine",
            "Become the Governor",
            "Overthrow the Governor",
        ]

    @staticmethod
    def special_endings() -> List[str]:
        return [
            "Destroy the colony",
            "Make peace",
            "Join the Gardeners",
            "Run away",
            "Blow up the stratos",
            "Transcend times",
            "Unleash the plague",
        ]

    @staticmethod
    def perk_count_range() -> range:
        return range(1, 4)


# Archipelago Options
# ...
