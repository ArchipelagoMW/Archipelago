from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SonicManiaArchipelagoOptions:
    sonic_mania_dlc_owned: SonicManiaDLCOwned


class SonicManiaGame(Game):
    name = "Sonic Mania"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = SonicManiaArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Find at least 1 Giant Ring",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Restart trial after losing a life",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use Shield Power-up (unless it cannot be avoided)",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Complete both Acts of ZONE as CHARACTER",
                data={
                    "ZONE": (self.zones, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete ZONE ACT_NUMBER as CHARACTER in Time Attack",
                data={
                    "ZONE": (self.zones, 1),
                    "ACT_NUMBER": (self.acts, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

        if self.has_dlc_encore:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete both Acts of ZONE in Encore Mode",
                    data={
                        "ZONE": (self.zones, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete ZONE ACT_NUMBER as CHARACTER in Time Attack Encore Mode",
                    data={
                        "ZONE": (self.zones, 1),
                        "ACT_NUMBER": (self.acts, 1),
                        "CHARACTER": (self.characters, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return templates

    @property
    def dlc_owned(self) -> bool:
        return self.archipelago_options.sonic_mania_dlc_owned.value

    @property
    def has_dlc_encore(self) -> bool:
        return "Encore" in self.dlc_owned

    @staticmethod
    def zones() -> List[str]:
        return [
            "Green Hill Zone",
            "Chemical Plant Zone",
            "Studiopolis Zone",
            "Flying Battery Zone",
            "Press Garden Zone",
            "Stardust Speedway Zone",
            "Hydrocity Zone",
            "Mirage Saloon Zone",
            "Oil Ocean Zone",
            "Lava Reef Zone",
            "Metallic Madness Zone",
            "Titanic Monarch Zone",
        ]

    @staticmethod
    def acts() -> List[str]:
        return [
            "Act 1",
            "Act 2",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = [
            "Sonic",
            "Tails",
            "Knuckles",
        ]

        if self.has_dlc_encore:
            characters.extend([
                "Mighty",
                "Ray",
            ])

        return sorted(characters)


# Archipelago Options
class SonicManiaDLCOwned(OptionSet):
    """
    Indicates which Sonic Mania DLC the player owns, if any.
    """

    display_name = "Sonic Mania DLC Owned"
    valid_keys = [
        "Encore",
    ]

    default = valid_keys
