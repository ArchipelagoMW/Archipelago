from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class KirbysReturnToDreamLandArchipelagoOptions:
    kirbys_return_to_dream_land_include_deluxe_content: KirbysReturnToDreamLandIncludeDeluxeContent


class KirbysReturnToDreamLandGame(Game):
    name = "Kirby's Return to Dream Land"
    platform = KeymastersKeepGamePlatforms.WII

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.WIIU,
    ]

    is_adult_only_or_unrated = False

    options_cls = KirbysReturnToDreamLandArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Extra Mode",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use the ABILITY copy ability to complete STAGE",
                data={
                    "ABILITY": (self.copy_abilities, 1),
                    "STAGE": (self.stages, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete the Arena using the ABILITY copy ability",
                data={
                    "ABILITY": (self.copy_abilities, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete the CHALLENGE challenge with a Gold Medal",
                data={
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def include_deluxe_content(self) -> bool:
        return bool(self.archipelago_options.kirbys_return_to_dream_land_include_deluxe_content.value)

    @functools.cached_property
    def copy_abilities_base(self) -> List[str]:
        return [
            "Beam",
            "Bomb",
            # "Crash",
            "Cutter",
            "Fighter",
            "Fire",
            "Hammer",
            "Hi-Jump",
            "Ice",
            "Leaf",
            # "Mike",
            "Needle",
            "Ninja",
            "Parasol",
            # "Sleep",
            "Spark",
            "Spear",
            "Stone",
            "Sword",
            "Tornado",
            "Water",
            "Whip",
            "Wing",
        ]

    @functools.cached_property
    def copy_abilities_deluxe(self) -> List[str]:
        return [
            "Mecha",
            "Sand",
        ]

    def copy_abilities(self) -> List[str]:
        copy_abilities: List[str] = self.copy_abilities_base[:]

        if self.include_deluxe_content:
            copy_abilities.extend(self.copy_abilities_deluxe)

        return sorted(copy_abilities)

    @staticmethod
    def stages() -> List[str]:
        return [
            "Cookie Country Stage 1",
            "Cookie Country Stage 2",
            "Cookie Country Stage 3",
            "Cookie Country Stage 4",
            "Cookie Country Boss Stage 5",
            "Raisin Ruins Stage 1",
            "Raisin Ruins Stage 2",
            "Raisin Ruins Stage 3",
            "Raisin Ruins Stage 4",
            "Raisin Ruins Boss Stage 5",
            "Onion Ocean Stage 1",
            "Onion Ocean Stage 2",
            "Onion Ocean Stage 3",
            "Onion Ocean Stage 4",
            "Onion Ocean Boss Stage 5",
            "White Wafers Stage 1",
            "White Wafers Stage 2",
            "White Wafers Stage 3",
            "White Wafers Stage 4",
            "White Wafers Stage 5",
            "White Wafers Boss Stage 6",
            "Nutty Noon Stage 1",
            "Nutty Noon Stage 2",
            "Nutty Noon Stage 3",
            "Nutty Noon Stage 4",
            "Nutty Noon Stage 5",
            "Nutty Noon Boss Stage 6 (Use Super Abilities when required)",
            "Egg Engines Stage 1",
            "Egg Engines Stage 2",
            "Egg Engines Stage 3",
            "Egg Engines Stage 4",
            "Egg Engines Stage 5",
            "Egg Engines Boss Stage 6",
            "Dangerous Dinner Stage 1",
            "Dangerous Dinner Stage 2",
            "Dangerous Dinner Stage 3",
            "Dangerous Dinner Boss Stage 4 (Starting at Landia and using Super Abilities when required)",
        ]

    @functools.cached_property
    def challenges_base(self) -> List[str]:
        return [
            "Bomb",
            "Hi-Jump",
            "Item",
            "Sword",
            "Water",
            "Whip",
            "Wing",
        ]

    @functools.cached_property
    def challenges_deluxe(self) -> List[str]:
        return [
            "Mecha",
            "Sand",
        ]

    def challenges(self) -> List[str]:
        challenges: List[str] = self.challenges_base[:]

        if self.include_deluxe_content:
            challenges.extend(self.challenges_deluxe)

        return sorted(challenges)


# Archipelago Options
class KirbysReturnToDreamLandIncludeDeluxeContent(Toggle):
    """
    Indicates whether to include Kirby's Return to Dream Land Deluxe content when generating objectives.
    """

    display_name = "Kirby's Return to Dream Land Include Deluxe Content"
