from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CrushCrushArchipelagoOptions:
    crush_crush_additional_characters: CrushCrushAdditionalCharacters
    crush_crush_include_hobby_related_objectives: CrushCrushIncludeHobbyRelatedObjectives
    crush_crush_include_job_related_objectives: CrushCrushIncludeJobRelatedObjectives


class CrushCrushGame(Game):
    name = "Crush Crush"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.WEB,
    ]

    is_adult_only_or_unrated = True

    options_cls = CrushCrushArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Reach STATUS status with CHARACTER",
                data={
                    "STATUS": (self.relationship_statuses, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=10,
            ),
            GameObjectiveTemplate(
                label="Reach Lover status with Q-Pernikiss and pick the choice on the CHOICE",
                data={
                    "CHOICE": (self.endgame_choices, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

        if self.include_hobby_related_objectives:
            templates.append(
                GameObjectiveTemplate(
                    label="Reach Level LEVEL in the following Hobby: HOBBY",
                    data={
                        "LEVEL": (self.hobby_level_range, 1),
                        "HOBBY": (self.hobbies, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            )

        if self.include_job_related_objectives:
            templates.append(
                GameObjectiveTemplate(
                    label="Reach Level LEVEL in the following Job: JOB",
                    data={
                        "LEVEL": (self.job_level_range, 1),
                        "JOB": (self.jobs, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=3,
                ),
            )

        return templates

    @property
    def additional_characters(self) -> List[str]:
        return sorted(self.archipelago_options.crush_crush_additional_characters.value)

    @property
    def include_hobby_related_objectives(self) -> bool:
        return bool(self.archipelago_options.crush_crush_include_hobby_related_objectives.value)

    @property
    def include_job_related_objectives(self) -> bool:
        return bool(self.archipelago_options.crush_crush_include_job_related_objectives.value)

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Cassie",
            "Mio",
            "Quill",
            "Elle",
            "Nutaku",
            "Iro",
            "Bonnibel",
            "Ayeka",
            "Fumi",
            "Bearverly",
            "Nina",
            "Alpha",
            "Pamu",
            "Luna",
            "Eva",
            "Karma",
            "Sutra",
            "Dark one",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if len(self.additional_characters):
            characters.extend(self.additional_characters)

        return sorted(characters)

    @staticmethod
    def endgame_choices() -> List[str]:
        return [
            "left",
            "right",
        ]

    @staticmethod
    def relationship_statuses() -> List[str]:
        return [
            "Frenemy",
            "Acquaintance",
            "Friendzone",
            "Awkward Besties",
            "Crush",
            "Sweetheart",
            "Girlfriend",
            "Lover",
        ]

    @staticmethod
    def hobbies() -> List[str]:
        return [
            "Dancing",
            "Partying",
            "Surfing",
            "Computers",
            "Sketching",
            "Protesting",
            "Meditation",
            "Bow Hunting",
            "University",
            "Brooding",
            "Vigilantism",
            "Sky Diving",
        ]

    @staticmethod
    def hobby_level_range() -> range:
        return range(1, 76)

    @functools.cached_property
    def jobs_base(self) -> List[str]:
        return [
            "Fast Food",
            "Restaurant",
            "Cleaning",
            "Lifeguard",
            "Art",
            "Computers",
            "Zoo",
            "Hunting",
            "Casino",
            "Sports",
            "Legal",
            "Movies",
            "Space",
            "Slayer",
            "Love",
            "Wizard",
        ]

    def jobs(self) -> List[str]:
        jobs: List[str] = self.jobs_base[:]

        if "Charlotte" in self.additional_characters:
            jobs.append("Digger")
        if "Suzu" in self.additional_characters:
            jobs.append("Tree Planter")
        if "Yuki" in self.additional_characters or "Grace" in self.additional_characters:
            jobs.append("Zamphoney Driver")

        return sorted(jobs)

    @staticmethod
    def job_level_range() -> range:
        return range(1, 11)


# Archipelago Options
class CrushCrushAdditionalCharacters(OptionSet):
    """
    Indicates which additional characters the player has access to, if any.
    """

    display_name = "Crush Crush Additional Characters"
    valid_keys = [
        "Darya",
        "Jelle",
        "Quillzone",
        "Bonchovy",
        "Spectrum",
        "Charlotte",
        "Odango",
        "Shibuki",
        "Sirina",
        "Catara",
        "Vellatrix",
        "Peanut",
        "Roxxy",
        "Tessa",
        "Claudia",
        "Rosa",
        "Juliet",
        "Wendy",
        "Ruri",
        "Generica",
        "Suzu",
        "Lustat",
        "Sawyer",
        "Explora",
        "Esper",
        "Renée",
        "Mallory",
        "Lake",
        "Brie",
        "Ranma",
        "Lotus",
        "Cassia",
        "Yuki",
        "Nova",
        "Marybelle",
        "Babybelle",
        "Pepper",
        "Amelia",
        "Kira",
        "Miss Desirée",
        "Nightingale",
        "Grace",
        "Desdemona",
        "Abby",
        "Shelly",
        "Honey",
        "Karyn",
        "Myro",
        "Aurora",
        "Ginger & Wasabi",
    ]

    default = valid_keys


class CrushCrushIncludeHobbyRelatedObjectives(Toggle):
    """
    Indicates whether to include Crush Crush objectives related to hobbies.
    """

    display_name = "Crush Crush Include Hobby Related Objectives"


class CrushCrushIncludeJobRelatedObjectives(Toggle):
    """
    Indicates whether to include Crush Crush objectives related to jobs.
    """

    display_name = "Crush Crush Include Job Related Objectives"
