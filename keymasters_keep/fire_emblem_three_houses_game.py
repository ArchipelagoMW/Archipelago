from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FireEmblemThreeHousesArchipelagoOptions:
    fire_emblem_three_houses_dlc_owned: FireEmblemThreeHousesDLCOwned


class FireEmblemThreeHousesGame(Game):
    name = "Fire Emblem: Three Houses"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = FireEmblemThreeHousesArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Lead the HOUSE on DIFFICULTY Difficulty or higher",
                data={
                    "HOUSE": (self.houses, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Use RECRUITABLE as your Main Unit as often as possible",
                data={
                    "RECRUITABLE": (self.recruitables, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Make RECRUITABLE your dancer",
                data={
                    "RECRUITABLE": (self.recruitables, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Recruit RECRUITABLE to your House",
                data={
                    "RECRUITABLE": (self.recruitables, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Recruit RECRUITABLE to your House",
                data={
                    "RECRUITABLE": (self.later_recruits, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat CHAPTER with RECRUITABLE on the field",
                data={
                    "CHAPTER": (self.chapters_early, 1),
                    "RECRUITABLE": (self.recruitables, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Beat CHAPTER with RECRUITABLE on the field",
                data={
                    "CHAPTER": (self.chapters_late, 1),
                    "RECRUITABLE": (self.later_recruits, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Turn RECRUITABLE into the following class: CLASS",
                data={
                    "RECRUITABLE": (self.recruitables, 1),
                    "CLASS": (self.classes_intermediate, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Turn RECRUITABLE into the following class: CLASS",
                data={
                    "RECRUITABLE": (self.recruitables, 1),
                    "CLASS": (self.classes_advanced, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get a Perfect Tea Time with RECRUITABLE",
                data={
                    "RECRUITABLE": (self.recruitables, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get a Perfect Tea Time with RECRUITABLE",
                data={
                    "RECRUITABLE": (self.later_recruits, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> bool:
        return sorted(self.archipelago_options.fire_emblem_three_houses_dlc_owned.value)

    @property
    def has_ashen_wolves_dlc(self) -> bool:
        return "Ashen Wolves" in self.dlc_owned

    @staticmethod
    def houses() -> List[str]:
        return [
            "Black Eagles",
            "Blue Lions",
            "Golden Deer",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Normal",
            "Hard",
            "Maddening",
        ]

    @functools.cached_property
    def recruitables_base(self) -> List[str]:
        return [
            "Ashe",
            "Bernadetta",
            "Caspar",
            "Dorothea",
            "Felix",
            "Ferdinand",
            "Ingrid",
            "Leonie",
            "Linhardt",
            "Lorenz",
            "Lysithea",
            "Marianne",
            "Mercedes",
            "Petra",
            "Raphael",
            "Sylvain",
        ]

    @functools.cached_property
    def recruitables_ashen_wolves(self) -> List[str]:
        return [
            "Balthus",
            "Constance",
            "Hapi",
            "Yuri",
        ]

    def recruitables(self) -> List[str]:
        recruitables = self.recruitables_base[:]

        if self.has_ashen_wolves_dlc:
            recruitables.extend(self.recruitables_ashen_wolves)

        return recruitables

    @staticmethod
    def later_recruits() -> List[str]:
        return [
            "Flayn",
            "Hanneman",
            "Manuela",
            "Shamir",
        ]

    @staticmethod
    def classes_intermediate() -> List[str]:
        return [
            "Archer",
            "Armored Knight",
            "Brigand",
            "Cavalier",
            "Mage",
            "Mercenary",
            "Priest",
            "Thief",
        ]

    @staticmethod
    def classes_advanced() -> List[str]:
        return [
            "Assassin",
            "Bishop",
            "Fortress Knight",
            "Paladin",
            "Sniper",
            "Swordmaster",
            "Warlock",
            "Warrior",
            "Wyvern Rider",
        ]

    @staticmethod
    def chapters_early() -> List[str]:
        return [
            "Chapter 3: Mutiny in the Mist",
            "Chapter 4: The Goddess's Rite of Rebirth",
            "Chapter 5: Tower of Black Winds",
            "Chapter 6: Rumors of a Reaper",
            "Chapter 7: Field of the Eagle and Lion",
        ]

    @staticmethod
    def chapters_late() -> List[str]:
        return [
            "Chapter 8: The Flame in the Darkness",
            "Chapter 9: The Cause of Sorrow",
            "Chapter 10: Where the Goddess Dwells",
            "Chapter 11: Throne of Knowledge",
        ]


# Archipelago Options
class FireEmblemThreeHousesDLCOwned(OptionSet):
    """
    Indicates which Fire Emblem: Three Houses DLC the player owns, if any.
    """

    display_name = "Fire Emblem: Three Houses DLC Owned"
    valid_keys = [
        "Ashen Wolves",
    ]

    default = valid_keys
