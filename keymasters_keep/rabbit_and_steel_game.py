from __future__ import annotations

import functools

from typing import List

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RabbitAndSteelArchipelagoOptions:
    rabbit_and_steel_unlocked_characters: RabbitAndSteelUnlockedCharacters
    rabbit_and_steel_allow_lunar: RabbitAndSteelAllowLunar


class RabbitAndSteelGame(Game):
    name = "Rabbit & Steel"
    platform = KeymastersKeepGamePlatforms.PC

    is_adult_only_or_unrated = False

    options_cls = RabbitAndSteelArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete the STAGE on DIFF difficulty",
                data={"STAGE": (self.stages, 1), "DIFF": (self.difficulties, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3
            ),
            GameObjectiveTemplate(
                label="Complete the STAGE as the CHARACTER",
                data={"STAGE": (self.stages, 1), "CHARACTER": (self.characters, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3
            ),
            GameObjectiveTemplate(
                label="Complete the STAGE on DIFF difficulty as the CHARACTER",
                data={"STAGE": (self.stages, 1), "DIFF": (self.difficulties, 1), "CHARACTER": (self.characters, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2
            ),
            GameObjectiveTemplate(
                label="Scale the Moonlit Pinnacle and defeat Shira, Rabbit of the Moon on DIFF difficulty",
                data={"DIFF": (self.difficulties, 1)},
                is_time_consuming=True,
                is_difficult=False, # Depends on optional factors, very easy on Easy
                weight=2
            ),
            GameObjectiveTemplate(
                label="Scale the Moonlit Pinnacle and defeat Shira, Rabbit of the Moon as the CHARACTER",
                data={"CHARACTER": (self.characters, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2
            ),
            GameObjectiveTemplate(
                label="Scale the Moonlit Pinnacle and defeat Shira, Rabbit of the Moon on DIFF difficulty "
                      "as the CHARACTER",
                data={"DIFF": (self.difficulties, 1), "CHARACTER": (self.characters, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2
            ),
            GameObjectiveTemplate(
                # I'm pretty sure this is impossible on Lunar...
                label="Complete the STAGE while skipping on all loot rolls on DIFF difficulty",
                data={"STAGE": (self.stages, 1), "DIFF": (self.base_difficulties, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=2
            ),
            GameObjectiveTemplate(
                label="Complete 5 stages while playing as the CHARACTER",
                data={"CHARACTER": (self.characters, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3
            ),
            GameObjectiveTemplate(
                label="Complete 5 stages on DIFF difficulty",
                data={"DIFF": (self.difficulties, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=3
            ),
            GameObjectiveTemplate(
                label="Pet Asha, the Shopkeeper",
                data={},
                is_time_consuming=False,
                is_difficult=False,
                weight=1
            )
        ]

    @functools.cached_property
    def characters_base(self):
        return [
            "Wizard Rabbit",
            "Assassin Rabbit",
            "Heavyblade Rabbit",
            "Dancer Rabbit",
            "Druid Rabbit"
        ]

    def characters(self):
        characters = self.characters_base[:]
        characters.extend(self.archipelago_options.rabbit_and_steel_unlocked_characters.value)

        return characters

    @staticmethod
    def base_difficulties():
        return [
            "Cute",
            "Normal",
            "Hard"
        ]

    def difficulties(self):
        difficulties = self.base_difficulties()
        if self.archipelago_options.rabbit_and_steel_allow_lunar:
            difficulties.append("Lunar")
        return difficulties

    @functools.cached_property
    def base_stages(self):
        return [
            "Kingdom Outskirts",
            "Scholar's Nest",
            "King's Arsenal",
            "Red Darkhouse",
            "Churchmouse Streets",
            "Emerald Lakeside",
            # Leaving out the Pale Keep for time constraints
        ]

    @functools.cached_property
    def dlc_stages(self):
        return [
            "Crack in the Geode",
            "Darkhouse Depths",
        ]

    def stages(self):
        stages = self.base_stages[:]
        # Some prep for the upcoming DLC
        # if self.archipelago_options.rabbit_and_steel_dlc_owned:
            # stages.extend(self.dlc_stages[:])
        return stages


class RabbitAndSteelUnlockedCharacters(OptionSet):
    """Indicates which unlockable characters in Rabbit & Steel the player has obtained"""
    display_name = "Rabbit & Steel Unlocked Characters"
    valid_keys = {
        "Spellsword Rabbit",
        "Sniper Rabbit",
        "Bruiser Rabbit",
        "Defender Rabbit",
        "Ancient Rabbit"
    }

    default = valid_keys


class RabbitAndSteelAllowLunar(Toggle):
    """Whether the Lunar difficulty should be an option for objectives in Rabbit & Steel"""
    display_name = "Rabbit & Steel Allow Lunar Difficulty"
