from __future__ import annotations

import functools

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GuiltyGearStriveArchipelagoOptions:
    guilty_gear_strive_dlc_owned: GuiltyGearStriveDLCOwned


class GuiltyGearStriveGame(Game):
    name = "GUILTY GEAR -STRIVE-"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = GuiltyGearStriveArchipelagoOptions

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
                label="Win a VERSUS match against CHARACTER",
                data={"CHARACTER": (self.characters, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a VERSUS match against CHARACTER without the use of any Tension gauge",
                data={"CHARACTER": (self.characters, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win VERSUS matches against CHARACTERS",
                data={"CHARACTERS": (self.characters, 3)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Win a round with a Perfect in a VERSUS match against CHARACTER",
                data={"CHARACTER": (self.characters, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear Stage STAGE of Survival Mode",
                data={"STAGE": (self.survival_stage, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete the mission CHARACTER Match-up Tutorial NUM",
                data={"CHARACTER": (self.characters, 1), "NUM": (self.tutorial_range, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @property
    def dlc_owned(self) -> Set[str]:
        return self.archipelago_options.guilty_gear_strive_dlc_owned.value

    @property
    def has_dlc_season_1_character_pass(self) -> bool:
        return "GUILTY GEAR -STRIVE- Season Pass 1" in self.dlc_owned

    @property
    def has_dlc_season_2_character_pass(self) -> bool:
        return "GUILTY GEAR -STRIVE- Season Pass 2" in self.dlc_owned

    @property
    def has_dlc_season_3_character_pass(self) -> bool:
        return "GUILTY GEAR -STRIVE- Season Pass 3" in self.dlc_owned

    @property
    def has_dlc_season_4_character_pass(self) -> bool:
        return "GUILTY GEAR -STRIVE- Season Pass 4" in self.dlc_owned
    
    @property
    def has_dlc_character_goldlewis(self) -> bool:
        return ("GGST Additional Character 1 - Goldlewis Dickinson" in self.dlc_owned or
                self.has_dlc_season_1_character_pass)
    
    @property
    def has_dlc_character_jacko(self) -> bool:
        return ("GGST Additional Character 2 - Jack-O" in self.dlc_owned or
                self.has_dlc_season_1_character_pass)
    
    @property
    def has_dlc_character_happy_chaos(self) -> bool:
        return ("GGST Additional Character 3 - Happy Chaos" in self.dlc_owned or
                self.has_dlc_season_1_character_pass)
    
    @property
    def has_dlc_character_baiken(self) -> bool:
        return ("GGST Additional Character 4 - Baiken" in self.dlc_owned or
                self.has_dlc_season_1_character_pass)
    
    @property
    def has_dlc_character_testament(self) -> bool:
        return ("GGST Additional Character 5 - Testament" in self.dlc_owned or
                self.has_dlc_season_1_character_pass)
    
    @property
    def has_dlc_character_bridget(self) -> bool:
        return ("GGST Additional Character 6 - Bridget" in self.dlc_owned or
                self.has_dlc_season_2_character_pass)
        
    @property
    def has_dlc_character_sin(self) -> bool:
        return ("GGST Additional Character 7 - Sin Kiske" in self.dlc_owned or
                self.has_dlc_season_2_character_pass)
    
    @property
    def has_dlc_character_bedman(self) -> bool:
        return ("GGST Additional Character 8 - Bedman?" in self.dlc_owned or
                self.has_dlc_season_2_character_pass)
    
    @property
    def has_dlc_character_asuka(self) -> bool:
        return ("GGST Additional Character 9 - Asuka" in self.dlc_owned or
                self.has_dlc_season_2_character_pass)
    
    @property
    def has_dlc_character_johnny(self) -> bool:
        return ("GGST Additional Character 10 - Johnny" in self.dlc_owned or
                self.has_dlc_season_3_character_pass)
    
    @property
    def has_dlc_character_elphelt(self) -> bool:
        return ("GGST Additional Character 11 - Elphelt Valentine" in self.dlc_owned or
                self.has_dlc_season_3_character_pass)
    
    @property
    def has_dlc_character_aba(self) -> bool:
        return ("GGST Additional Character 12 - A.B.A" in self.dlc_owned or
                self.has_dlc_season_3_character_pass)
    
    @property
    def has_dlc_character_slayer(self) -> bool:
        return ("GGST Additional Character 13 - Slayer" in self.dlc_owned or
                self.has_dlc_season_3_character_pass)
    
    @property
    def has_dlc_character_dizzy(self) -> bool:
        return ("GGST Additional Character 14 - Queen Dizzy" in self.dlc_owned or
                self.has_dlc_season_4_character_pass)

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Sol",
            "Ky",
            "May",
            "Axl",
            "Chipp",
            "Potemkin",
            "Faust",
            "Millia",
            "Zato",
            "Ramlethal",
            "Leo",
            "Nagoriyuki",
            "Giovanna",
            "Anji",
            "I-No",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        # Season 1
        if self.has_dlc_character_goldlewis:
            characters.append("Goldlewis")

        if self.has_dlc_character_jacko:
            characters.append("Jack-O'")

        if self.has_dlc_character_happy_chaos:
            characters.append("Happy Chaos")

        if self.has_dlc_character_baiken:
            characters.append("Baiken")

        if self.has_dlc_character_testament:
            characters.append("Testament")

        # Season 2
        if self.has_dlc_character_bridget:
            characters.append("Bridget")

        if self.has_dlc_character_sin:
            characters.append("Sin")

        if self.has_dlc_character_bedman:
            characters.append("Bedman?")

        if self.has_dlc_character_asuka:
            characters.append("Asuka R#")

        # Season 3
        if self.has_dlc_character_johnny:
            characters.append("Johnny")

        if self.has_dlc_character_elphelt:
            characters.append("Elphelt")

        if self.has_dlc_character_aba:
            characters.append("A.B.A")

        if self.has_dlc_character_slayer:
            characters.append("Slayer")

        # Season 4
        if self.has_dlc_character_dizzy:
            characters.append("Dizzy")

        return characters

    @staticmethod
    def cpu_levels() -> List[str]:
        return [
            "Beginner",
            "Easy",
            "Normal",
            "Hard",
            "Very Hard",
            "Maniac",
        ]
    
    @staticmethod
    def survival_stage() -> range:
        return range(5,31)
    
    @staticmethod
    def tutorial_range() -> range:
        return range(1,3)


# Archipelago Options
class GuiltyGearStriveDLCOwned(OptionSet):
    """
    Indicates which GUILTY GEAR -STRIVE- DLC the player owns, if any.
    """

    display_name = "GUILTY GEAR -STRIVE- DLC Owned"
    valid_keys = [
        "GUILTY GEAR -STRIVE- Season Pass 1",
        "GGST Additional Character 1 - Goldlewis Dickinson",
        "GGST Additional Character 2 - Jack-O",
        "GGST Additional Character 3 - Happy Chaos",
        "GGST Additional Character 4 - Baiken",
        "GGST Additional Character 5 - Testament",
        "GUILTY GEAR -STRIVE- Season Pass 2",
        "GGST Additional Character 6 - Bridget",
        "GGST Additional Character 7 - Sin Kiske",
        "GGST Additional Character 8 - Bedman?",
        "GGST Additional Character 9 - Asuka",
        "GUILTY GEAR -STRIVE- Season Pass 3",
        "GGST Additional Character 10 - Johnny",
        "GGST Additional Character 11 - Elphelt Valentine",
        "GGST Additional Character 12 - A.B.A",
        "GGST Additional Character 13 - Slayer",
        "GUILTY GEAR -STRIVE- Season Pass 4",
        "GGST Additional Character 14 - Queen Dizzy",
    ]

    default = valid_keys
