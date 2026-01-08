from __future__ import annotations

import functools

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class StreetFighter6ArchipelagoOptions:
    street_fighter_6_dlc_owned: StreetFighter6DLCOwned


class StreetFighter6Game(Game):
    name = "Street Fighter 6"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = StreetFighter6ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play as CHARACTER, Set CPU level to LEVEL",
                data={"CHARACTER": (self.characters, 1), "LEVEL": (self.cpu_levels, 1)}
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a VERSUS match against CHARACTER in STAGE",
                data={"CHARACTER": (self.characters, 1), "STAGE": (self.stages, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win VERSUS matches against CHARACTERS in STAGE",
                data={"CHARACTERS": (self.characters, 3), "STAGE": (self.stages, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win with a Perfect KO in a VERSUS match against CHARACTER in STAGE",
                data={"CHARACTER": (self.characters, 1), "STAGE": (self.stages, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win an Extreme Battle against CHARACTER in STAGE. Rule: RULES. Gimmick: GIMMICK",
                data={
                    "CHARACTER": (self.characters, 1),
                    "STAGE": (self.stages, 1),
                    "RULES": (self.extreme_battle_rules, 1),
                    "GIMMICK": (self.extreme_battle_gimmicks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Clear the COMBO_TRIAL_DIFFICULTY Combo Trials for CHARACTER",
                data={"CHARACTER": (self.characters, 1), "COMBO_TRIAL_DIFFICULTY": (self.combo_trial_difficulties, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear the Advanced Combo Trials for CHARACTER",
                data={"CHARACTER": (self.characters, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> Set[str]:
        return self.archipelago_options.street_fighter_6_dlc_owned.value

    @property
    def has_dlc_year_1_character_pass(self) -> bool:
        return "Year 1 Character Pass" in self.dlc_owned

    @property
    def has_dlc_year_1_ultimate_pass(self) -> bool:
        return "Year 1 Ultimate Pass" in self.dlc_owned

    @property
    def has_dlc_year_2_character_pass(self) -> bool:
        return "Year 2 Character Pass" in self.dlc_owned

    @property
    def has_dlc_year_2_ultimate_pass(self) -> bool:
        return "Year 2 Ultimate Pass" in self.dlc_owned

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Blanka",
            "Cammy",
            "Chun-Li",
            "Dee Jay",
            "Dhalsim",
            "E. Honda",
            "Guile",
            "Jamie",
            "JP",
            "Juri",
            "Ken",
            "Kimberly",
            "Lily",
            "Luke",
            "Manon",
            "Marisa",
            "Ryu",
            "Zangief",
        ]

    @functools.cached_property
    def characters_year_1(self) -> List[str]:
        return [
            "A.K.I.",
            "Akuma",
            "Ed",
            "Rashid",
        ]

    @functools.cached_property
    def characters_year_2(self) -> List[str]:
        return [
            # "Elena",  # Unreleased
            "M. Bison",
            # "Mai",  # Unreleased
            "Terry",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.has_dlc_year_1_character_pass or self.has_dlc_year_1_ultimate_pass:
            characters.extend(self.characters_year_1[:])

        if self.has_dlc_year_2_character_pass or self.has_dlc_year_2_ultimate_pass:
            characters.extend(self.characters_year_2[:])

        return characters

    @functools.cached_property
    def stages_base(self) -> List[str]:
        return [
            "Metro City Downtown",
            "Carrier Byron Taylor",
            "Thunderfoot Settlement",
            "Barmaley Steelworks",
            "Bathers Beach",
            "Ranger's Hut",
            "King Street",
            "Fete Foraine",
            "Colosseo",
            "Genbu Temple",
            "Tian Hong Yuan",
            "Dhalsimer Temple",
            "Old Town Market",
            "Suval'hal Arena",
            "The Macho Ring",
            "Training Room",
        ]

    @functools.cached_property
    def stages_year_1(self) -> List[str]:
        return [
            "Ruined Lab",
            "Enma's Hollow",
        ]

    @functools.cached_property
    def stages_year_2(self) -> List[str]:
        return [
            "Pao Pao Cafe 6",
            # "Aokigahara",  # Unreleased
        ]

    def stages(self) -> List[str]:
        stages: List[str] = self.stages_base[:]

        if self.has_dlc_year_1_ultimate_pass:
            stages.extend(self.stages_year_1[:])

        if self.has_dlc_year_2_ultimate_pass:
            stages.extend(self.stages_year_2[:])

        return stages

    @staticmethod
    def cpu_levels() -> range:
        return range(1, 9)

    @staticmethod
    def extreme_battle_rules() -> List[str]:
        return [
            "Down & Out",
            "Back & Forth",
            "Rules & Regulations",
            "Heaven & Hell",
            "Smash & Grab",
        ]

    @staticmethod
    def extreme_battle_gimmicks() -> List[str]:
        return [
            "Bull Run",
            "Bombs Away",
            "Shock Zone",
            "Mecha Friend",
            "Lucky Drone",
            "No Gimmicks",
        ]

    @staticmethod
    def combo_trial_difficulties() -> List[str]:
        return [
            "Beginner",
            "Intermediate",
        ]


# Archipelago Options
class StreetFighter6DLCOwned(OptionSet):
    """
    Indicates which Street Fighter 6 DLC the player owns, if any.
    """

    display_name = "Street Fighter 6 DLC Owned"
    valid_keys = [
        "Year 1 Character Pass",
        "Year 1 Ultimate Pass",
        "Year 2 Character Pass",
        "Year 2 Ultimate Pass",
    ]

    default = valid_keys
