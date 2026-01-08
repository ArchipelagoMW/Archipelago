from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class CupheadArchipelagoOptions:
    cuphead_dlc_owned: CupheadDLCOwned


class CupheadGame(Game):
    name = "Cuphead"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = CupheadArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use only one of the two allowed Weapons",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Beat bosses in Expert Mode",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat BOSS.  Weapons: WEAPONS  Charm: CHARM  Super: SUPER",
                data={
                    "BOSS": (self.bosses, 1),
                    "WEAPONS": (self.weapons, 2),
                    "CHARM": (self.charms, 1),
                    "SUPER": (self.super_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat BOSS.  Charm: CHARM",
                data={
                    "BOSS": (self.bosses_air, 1),
                    "CHARM": (self.charms, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.cuphead_dlc_owned.value)

    @property
    def has_dlc_the_delicious_last_course(self) -> bool:
        return "The Delicious Last Course" in self.dlc_owned

    @functools.cached_property
    def bosses_base(self) -> List[str]:
        return [
            "The Root Pack",
            "Goopy Le Grande",
            "Cagney Carnation",
            "Ribby And Croaks",
            "Baroness Von Bon Bon",
            "Beppi The Clown",
            "Grim Matchstick",
            "Rumor Honeybottoms",
            "Captain Brineybeard",
            "Sally Stageplay",
            "Werner Werman",
            "Phantom Express",
            "King Dice",
            "The Devil",
        ]

    @functools.cached_property
    def bosses_dlc_the_delicious_last_course(self) -> List[str]:
        return [
            "Glumstone The Giant",
            "Moonshine Mob",
            "The Howling Aces",
            "Mortimer Freeze",
            "Chef Saltbaker",
        ]

    def bosses(self) -> List[str]:
        bosses: List[str] = self.bosses_base[:]

        if self.has_dlc_the_delicious_last_course:
            bosses.extend(self.bosses_dlc_the_delicious_last_course)

        return sorted(bosses)

    @functools.cached_property
    def bosses_air_base(self) -> List[str]:
        return [
            "Djimmi The Great",
            "Wally Warbles",
            "Dr. Kahl's Robot",
            "Cala Maria",
        ]

    @functools.cached_property
    def bosses_air_dlc_the_delicious_last_course(self) -> List[str]:
        return [
            "Esther Winchester",
        ]

    def bosses_air(self) -> List[str]:
        bosses_air: List[str] = self.bosses_air_base[:]

        if self.has_dlc_the_delicious_last_course:
            bosses_air.extend(self.bosses_air_dlc_the_delicious_last_course)

        return sorted(bosses_air)

    @staticmethod
    def weapons() -> List[str]:
        return [
            "Peashooter",
            "Spread",
            "Chaser",
            "Lobber",
            "Charge",
            "Roundabout",
            "Crackshot",
            "Converge",
            "Twist-Up",
        ]

    @staticmethod
    def charms() -> List[str]:
        return [
            "Heart",
            "Smoke Bomb",
            "P. Sugar",
            "Coffee",
            "Twin Heart",
            "Whetstone",
            "Astral Cookie",
            "Heart Ring",
        ]

    @staticmethod
    def super_count_range() -> range:
        return range(1, 4)


# Archipelago Options
class CupheadDLCOwned(OptionSet):
    """
    Indicates which Cuphead DLC the player owns, if any.
    """

    display_name = "Cuphead DLC Owned"
    valid_keys = [
        "The Delicious Last Course",
    ]

    default = valid_keys
