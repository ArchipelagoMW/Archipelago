from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MagesOfMystraliaArchipelagoOptions:
    pass


class MagesOfMystraliaGame(Game):
    name = "Mages of Mystralia"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = MagesOfMystraliaArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play the game on DIFFICULTY difficulty",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Play the game with the WAND, whenever possible",
                data={
                    "WAND": (self.wands, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete the Hall of Trials. Spells -> Behaviors: BEHAVIORS  Augments: AUGMENTS  Trigger: TRIGGER",
                data={
                    "BEHAVIORS": (self.behaviors, 3),
                    "AUGMENTS": (self.augments, 2),
                    "TRIGGER": (self.triggers, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete the Hall of Trials. Spells -> Types: TYPES  Elements: ELEMENTS   Behaviors: BEHAVIORS  Augments: AUGMENTS  Trigger: TRIGGER",
                data={
                    "TYPES": (self.types, 2),
                    "ELEMENTS": (self.elements, 2),
                    "BEHAVIORS": (self.behaviors, 3),
                    "AUGMENTS": (self.augments, 2),
                    "TRIGGER": (self.triggers, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play the Adventure and get the following Story Elixer: ELIXER",
                data={
                    "ELIXER": (self.elixirs, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play the Adventure and get the following Story Essence: ESSENCE. Spells -> Behaviors: BEHAVIORS (whenever possible)",
                data={
                    "ESSENCE": (self.essences, 1),
                    "BEHAVIORS": (self.behaviors, 4),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Play the Adventure and get the following Side Quest Elixer: ELIXER. Spells -> Behaviors: BEHAVIORS (whenever possible)",
                data={
                    "ELIXER": (self.elixirs_optional, 1),
                    "BEHAVIORS": (self.behaviors, 4),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Play the Adventure and get the following  Behaviors: BEHAVIORS  Augment: AUGMENTS  Trigger: TRIGGER",
                data={
                    "BEHAVIORS": (self.behaviors, 2),
                    "AUGMENTS": (self.augments, 1),
                    "TRIGGER": (self.triggers, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Mage",
            "Archmage",
            "Hardcore",
        ]

    @staticmethod
    def wands() -> List[str]:
        return [
            "Apprentice Stick",
            "Aqua Wand",
            "Aura Wand",
            "Gaea Wand",
            "Igni Wand",
            "Life Staff",
            "Negation Scepter",
            "Rod of the Berserker",
            "Soul Scepter",
            "Trial Wand",
        ]

    @staticmethod
    def behaviors() -> List[str]:
        return [
            "Bounce",
            "Detonate",
            "Duplicate",
            "Ether",
            "Homing",
            "Mastery",
            "Mastery",
            "Move",
            "Overcharge",
            "Push",
            "Rain",
            "Swift",
            "Teleport",
        ]

    @staticmethod
    def augments() -> List[str]:
        return [
            "Inverse",
            "Left",
            "Random",
            "Right",
            "Size",
            "Time",
        ]

    @staticmethod
    def triggers() -> List[str]:
        return [
            "At Once",
            "Expire",
            "Impact",
            "Periodic",
            "Proximity",
        ]

    @staticmethod
    def types() -> List[str]:
        return [
            "Actus",
            "Creo",
            "Ego",
            "Immedi",
        ]

    @staticmethod
    def elements() -> List[str]:
        return [
            "Aqua",
            "Aura",
            "Gaea",
            "Igni",
        ]

    @staticmethod
    def elixirs() -> List[str]:
        return [
            "Ghost Queen Elixer",
            "Ice Lizard Elixer",
            "Wood Wretch Elixer",
        ]

    @staticmethod
    def essences() -> List[str]:
        return [
            "Essence of Aqua",
            "Essence of Aura",
            "Essence of Gaea",
            "Essence of Igni",
        ]

    @staticmethod
    def elixirs_optional() -> List[str]:
        return [
            "Afterlife Elixer",
            "Mystralian Elixer",
        ]


# Archipelago Options
# ...
