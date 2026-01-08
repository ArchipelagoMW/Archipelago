from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DungeonDefendersArchipelagoOptions:
    dungeon_defenders_dlc_owned: DungeonDefendersDLCOwned


class DungeonDefendersGame(Game):
    name = "Dungeon Defenders"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS3,
        KeymastersKeepGamePlatforms.X360,
    ]

    is_adult_only_or_unrated = False

    options_cls = DungeonDefendersArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Hardcore Mode only",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="New Characters only",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY without using CHARACTER",
                data={
                    "LEVEL": (self.levels_act_1, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY without using CHARACTERS",
                data={
                    "LEVEL": (self.levels_act_2, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY without using CHARACTERS",
                data={
                    "LEVEL": (self.levels_act_3, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY without using CHARACTER",
                data={
                    "LEVEL": (self.levels_challenges, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY without using CHARACTERS",
                data={
                    "LEVEL": (self.levels_challenges, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY with only one of: CHARACTERS",
                data={
                    "LEVEL": (self.levels_challenges, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete Act 1 on DIFFICULTY with only one of: CHARACTERS",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete Act 2 on DIFFICULTY with only one of: CHARACTERS",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete Act 3 on DIFFICULTY with only one of: CHARACTERS",
                data={
                    "DIFFICULTY": (self.difficulties, 1),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVELS on INSANE with the following characters: CHARACTERS",
                data={
                    "LEVELS": (self.levels, 3),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY without using CHARACTER",
                data={
                    "LEVEL": (self.levels_act_1, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY without using CHARACTERS",
                data={
                    "LEVEL": (self.levels_act_2, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY without using CHARACTERS",
                data={
                    "LEVEL": (self.levels_act_3, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                    "CHARACTERS": (self.characters, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL on DIFFICULTY without using CHARACTER",
                data={
                    "LEVEL": (self.levels_challenges, 1),
                    "DIFFICULTY": (self.difficulties_hard, 1),
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.dungeon_defenders_dlc_owned.value)

    @property
    def has_dlc_new_hero_pack_1(self) -> bool:
        return "New Hero Pack 1" in self.dlc_owned

    @property
    def has_dlc_summoner_hero(self) -> bool:
        return "Summoner Hero" in self.dlc_owned

    @property
    def has_dlc_jester_hero(self) -> bool:
        return "Jester Hero" in self.dlc_owned

    @property
    def has_dlc_barbarian_hero(self) -> bool:
        return "Barbarian Hero" in self.dlc_owned

    @property
    def has_dlc_series_ev_hero(self) -> bool:
        return "Series EV Hero" in self.dlc_owned

    @property
    def has_dlc_hermit_hero(self) -> bool:
        return "Hermit Hero" in self.dlc_owned

    @property
    def has_dlc_gunwitch_hero(self) -> bool:
        return "GunWitch Hero" in self.dlc_owned

    @property
    def has_dlc_quest_for_the_lost_eternia_shards_part_1_4(self) -> bool:
        return "Quest for the Lost Eternia Shards (Part 1-4)" in self.dlc_owned

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Apprentice",
            "Squire",
            "Huntress",
            "Monk",
        ]

    @functools.cached_property
    def characters_new_hero_pack_1(self) -> List[str]:
        return [
            "Countess",
            "Ranger",
            "Initiate",
            "Adept",
        ]

    @functools.cached_property
    def characters_jester_hero(self) -> List[str]:
        return [
            "Jester",
        ]

    @functools.cached_property
    def characters_summoner_hero(self) -> List[str]:
        return [
            "Summoner",
        ]

    @functools.cached_property
    def characters_series_ev_hero(self) -> List[str]:
        return [
            "Series EV",
        ]

    @functools.cached_property
    def characters_barbarian_hero(self) -> List[str]:
        return [
            "Barbarian",
        ]

    @functools.cached_property
    def characters_hermit_hero(self) -> List[str]:
        return [
            "Hermit",
        ]

    @functools.cached_property
    def characters_gunwitch_hero(self) -> List[str]:
        return [
            "Gunwitch",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.has_dlc_new_hero_pack_1:
            characters.extend(self.characters_new_hero_pack_1)

        if self.has_dlc_jester_hero:
            characters.extend(self.characters_jester_hero)

        if self.has_dlc_summoner_hero:
            characters.extend(self.characters_summoner_hero)

        if self.has_dlc_series_ev_hero:
            characters.extend(self.characters_series_ev_hero)

        if self.has_dlc_barbarian_hero:
            characters.extend(self.characters_barbarian_hero)

        if self.has_dlc_hermit_hero:
            characters.extend(self.characters_hermit_hero)

        if self.has_dlc_gunwitch_hero:
            characters.extend(self.characters_gunwitch_hero)

        return sorted(characters)

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Medium",
            "Hard",
            "INSANE",
        ]

    @staticmethod
    def difficulties_hard() -> List[str]:
        return [
            "NIGHTMARE",
            "RUTHLESS",
        ]

    @staticmethod
    def levels_act_1() -> List[str]:
        return [
            "Deeper Well",
            "Foundries and Forges",
            "Magus Quarters",
            "Alchemical Labratory",
        ]

    @staticmethod
    def levels_act_2() -> List[str]:
        return [
            "Servants Quarters",
            "Castle Armory",
            "Hall of Court",
            "The Throne Room",
        ]

    @staticmethod
    def levels_act_3() -> List[str]:
        return [
            "Royal Gardens",
            "The Ramparts",
            "Endless Spires",
            "The Summit",
            "Bonus: Glitterhelm Caverns",
        ]

    @staticmethod
    def levels_quest_for_the_lost_eternia_shards() -> List[str]:
        return [
            "Mistymire Forest",
            "Moraggo Desert Town",
            "Aquanos",
            "Sky City",
            "Crystalline Dimension",
        ]

    @staticmethod
    def levels_challenges() -> List[str]:
        return [
            "No Towers Allowed",
            "Unlikely Allies",
            "Warping Core",
            "Raining Goblins",
            "Wizardry",
            "Ogre Crush",
            "Zippy Terror",
            "Chicken",
            "Moving Core",
            "Death From Above",
            "Assault",
            "Treasure Hunt",
            "Monster Fest",
        ]

    def levels(self) -> List[str]:
        levels: List[str] = (
            self.levels_act_1()
            + self.levels_act_2()
            + self.levels_act_3()
            + self.levels_challenges()
        )

        if self.has_dlc_quest_for_the_lost_eternia_shards_part_1_4:
            levels.extend(self.levels_quest_for_the_lost_eternia_shards())

        return sorted(levels)


# Archipelago Options
class DungeonDefendersDLCOwned(OptionSet):
    """
    Indicates which Dungeon Defenders DLC the player owns, if any.
    """

    display_name = "Dungeon Defenders DLC Owned"
    valid_keys = [
        "New Hero Pack 1",
        "Summoner Hero",
        "Jester Hero",
        "Barbarian Hero",
        "Series EV Hero",
        "Hermit Hero",
        "GunWitch Hero",
        "Quest for the Lost Eternia Shards (Part 1-4)",
    ]

    default = valid_keys
