from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import DefaultOnToggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class FortuneStreetArchipelagoOptions:
    fortune_street_include_unlockable_content: FortuneStreetIncludeUnlockableContent


class FortuneStreetGame(Game):
    name = "Fortune Street"
    platform = KeymastersKeepGamePlatforms.WII

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = FortuneStreetArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Increase the default Target Amount by AMOUNT_MODIFIERg",
                data={
                    "AMOUNT_MODIFIER": (self.amount_modifier_range, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Only play on Standard Rules",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="SET COUNT CPU(s) to S Rank",
                data={
                    "COUNT": (self.s_count_range, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on BOARD against OPPONENTS and place 1st",
                data={
                    "BOARD": (self.boards, 1),
                    "OPPONENTS": (self.characters, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play on BOARD against OPPONENTS and place 2nd or higher",
                data={
                    "BOARD": (self.boards, 1),
                    "OPPONENTS": (self.characters, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Play on BOARD against OPPONENTS and place 3rd or higher",
                data={
                    "BOARD": (self.boards, 1),
                    "OPPONENTS": (self.characters, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
        ]

    @property
    def include_unlockable_content(self) -> bool:
        return bool(self.archipelago_options.fortune_street_include_unlockable_content.value)

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Mario",
            "Luigi",
            "Yoshi",
            "Bowser",
            "Toad",
            "Donkey Kong",
            "Wario",
            "Waluigi",
            "Daisy",
            "Birdo",
            "Diddy Kong",
            "Bowser Jr.",
            "Slime",
            "Princessa",
            "Kiryl",
            "Yangus",
            "Angelo",
            "Platypunk",
            "Bianca",
            "Alena",
            "Carver",
            "Stella",
        ]

    @functools.cached_property
    def characters_unlockable(self) -> List[str]:
        return [
            "Peach",
            "Jessica",
            "Dragonlord",
            "Patty",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.include_unlockable_content:
            characters.extend(self.characters_unlockable)

        return sorted(characters)

    @functools.cached_property
    def boards_base(self) -> List[str]:
        return [
            "Castle Trodain",
            "The Observatory",
            "Ghost Ship",
            "Slimenia",
            "Mt. Magmageddon",
            "Robbin' Hood Ruins",
            "Mario Stadium",
            "Starship Mario",
            "Mario Circuit",
            "Yoshi's Island",
            "Delfino Plaza",
            "Peach's Castle",
        ]

    @functools.cached_property
    def boards_unlockable(self) -> List[str]:
        return [
            "Alefgard",
            "Super Mario Bros.",
            "Bowser's Castle",
            "Good Egg Galaxy",
            "Colossus",
            "Alltrades Abbey",
        ]

    def boards(self) -> List[str]:
        boards: List[str] = self.boards_base[:]

        if self.include_unlockable_content:
            boards.extend(self.boards_unlockable)

        return sorted(boards)

    @staticmethod
    def amount_modifier_range() -> range:
        return range(3000, 5001, 1000)

    @staticmethod
    def s_count_range() -> range:
        return range(1, 4)


# Archipelago Options
class FortuneStreetIncludeUnlockableContent(DefaultOnToggle):
    """
    Whether to include Fortune Street unlockable content in objectives.
    """

    display_name = "Fortune Street Include Unlockable Content"
