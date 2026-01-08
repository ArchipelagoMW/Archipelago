from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FinalFantasyXVIArchipelagoOptions:
    final_fantasy_xvi_dlc_owned: FinalFantasyXVIDLCOwned


class FinalFantasyXVIGame(Game):
    # Initial implementation by @delcake on Discord

    name = "Final Fantasy XVI"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS5,
    ]

    is_adult_only_or_unrated = True

    options_cls = FinalFantasyXVIArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Only utilize abilities from the following Eikons: EIKONS (excluding Chronolith objectives)",
                data={"EIKONS": (self.eikons, 3)},
            ),
        ]
    
    @functools.cached_property
    def objectives_base(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete LEVEL in Arcade Mode",
                data={"LEVEL": (self.levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Achieve an S rating on LEVEL in Arcade Mode",
                data={"LEVEL": (self.levels, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear Chronolith Trial: TRIAL",
                data={"TRIAL": (self.trials_normal, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear Final Chronolith Trial: TRIAL",
                data={"TRIAL": (self.trials_final, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]
    
    @functools.cached_property
    def objectives_the_rising_tide(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Clear Circle X in Kairos Gate",
                data={"X": (self.kairos_gate_low_range, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear Circle X in Kairos Gate",
                data={"X": (self.kairos_gate_high_range, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
        ]
    
    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = self.objectives_base[:]

        if self.has_dlc_the_rising_tide:
            objectives.extend(self.objectives_the_rising_tide)

        return objectives
    
    @property
    def dlc_owned(self) -> bool:
        return self.archipelago_options.final_fantasy_xvi_dlc_owned.value
    
    @property
    def has_dlc_echoes_of_the_fallen(self) -> bool:
        return "Echoes of the Fallen" in self.dlc_owned
    
    @property
    def has_dlc_the_rising_tide(self) -> bool:
        return "The Rising Tide" in self.dlc_owned
    
    @functools.cached_property
    def levels_base(self) -> List[str]:
        return [
            "Caer Norvent",
            "Drake's Breath",
            "Drake's Fang",
            "Drake's Head",
            "Drake's Spine",
            "Kostnice",
            "Origin",
            "Phoenix Gate Ruins",
            "Reverie",
            "Rosalith",
            "The Crystalline Dominion",
            "The Eye of the Tempest",
            "The Free Cities of Kanver",
            "The Greatwood",
            "The Ironworks",
            "The Kingsfall",
            "The Naldia Narrow",
        ]
    
    @functools.cached_property
    def levels_echoes_of_the_fallen(self) -> List[str]:
        return [
            "The Sagespire",
        ]
    
    @functools.cached_property
    def levels_the_rising_tide(self) -> List[str]:
        return [
            "The Aire of Hours",
        ]
    
    def levels(self) -> List[str]:
        levels: List[str] = self.levels_base[:]

        if self.has_dlc_echoes_of_the_fallen:
            levels.extend(self.levels_echoes_of_the_fallen)
        
        if self.has_dlc_the_rising_tide:
            levels.extend(self.levels_the_rising_tide)
        
        return levels

    @functools.cached_property
    def eikons_base(self) -> List[str]:
        return [
            "Bahamut",
            "Garuda",
            "Odin",
            "Phoenix",
            "Ramuh",
            "Shiva",
            "Titan",
        ]
    
    @functools.cached_property
    def eikons_the_rising_tide(self) -> List[str]:
        return [
            "Leviathan",
            "Ultima",
        ]
    
    def eikons(self) -> List[str]:
        eikons: List[str] = self.eikons_base[:]

        if self.has_dlc_the_rising_tide:
            eikons.extend(self.eikons_the_rising_tide)
        
        return eikons
    
    @staticmethod
    def kairos_gate_low_range() -> List[str]:
        return range(1,11)
    
    @staticmethod
    def kairos_gate_high_range() -> List[str]:
        return range(11,21)
    
    @staticmethod
    def trials_normal() -> List[str]:
        return [
            "Trial by Darkness",
            "Trial by Earth",
            "Trial by Fire",
            "Trial by Ice",
            "Trial by Light",
            "Trial by Thunder",
            "Trial by Wind",
        ]
    
    @staticmethod
    def trials_final() -> List[str]:
        return [
            "Final Trial by Darkness",
            "Final Trial by Earth",
            "Final Trial by Fire",
            "Final Trial by Ice",
            "Final Trial by Light",
            "Final Trial by Thunder",
            "Final Trial by Wind",
        ]


# Archipelago Options
class FinalFantasyXVIDLCOwned(OptionSet):
    """
    Indicates which Final Fantasy XVI DLC the player owns, if any.
    """

    display_name = "Final Fantasy XVI DLC Owned"
    valid_keys = [
        "Echoes of the Fallen",
        "The Rising Tide",
    ]

    default = valid_keys
