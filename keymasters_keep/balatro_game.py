from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BalatroArchipelagoOptions:
    balatro_include_difficult_stakes: BalatroIncludeDifficultStakes


class BalatroGame(Game):
    name = "Balatro"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = True

    options_cls = BalatroArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run with the DECK deck",
                data={
                    "DECK": (self.decks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a run on STAKE stake",
                data={
                    "STAKE": (self.stakes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a run with the DECK deck on STAKE stake",
                data={
                    "DECK": (self.decks, 1),
                    "STAKE": (self.stakes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play HAND COUNT times in a single run",
                data={
                    "HAND": (self.poker_hands, 1),
                    "COUNT": (self.poker_hand_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Skip COUNT Blinds in a single run",
                data={
                    "COUNT": (self.skip_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Score COUNT Chips in a single hand",
                data={
                    "COUNT": (self.chip_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Reach Ante ANTE",
                data={
                    "ANTE": (self.endless_ante_range, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete the 'CHALLENGE' Challenge",
                data={
                    "CHALLENGE": (self.challenges, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Play a HAND",
                data={
                    "HAND": (self.secret_poker_hands, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def include_difficult_stakes(self) -> bool:
        return bool(self.archipelago_options.balatro_include_difficult_stakes.value)

    @staticmethod
    def decks() -> List[str]:
        return [
            "Red",
            "Blue",
            "Yellow",
            "Green",
            "Black",
            "Magic",
            "Nebula",
            "Ghost",
            "Abandoned",
            "Checkered",
            "Zodiac",
            "Painted",
            "Anaglyph",
            "Plasma",
            "Erratic",
        ]

    @staticmethod
    def challenges() -> List[str]:
        return [
            "The Omelette",
            "15 Minute City",
            "Rich get Richer",
            "On a Knife's Edge",
            "X-Ray Vision",
            "Mad World",
            "Luxury Tax",
            "Non-Perishable",
            "Medusa",
            "Double or Nothing",
            "Typecast",
            "Inflation",
            "Bram Poker",
            "Fragile",
            "Monolith",
            "Blast Off",
            "Five-Card Draw",
            "Golden Needle",
            "Cruelty",
            "Jokerless",
        ]

    @staticmethod
    def poker_hands() -> List[str]:
        return [
            "High Card",
            "Pair",
            "Two Pair",
            "Three of a Kind",
            "Straight",
            "Flush",
            "Full House",
            "Four of a Kind",
            "Straight Flush",
        ]

    @staticmethod
    def poker_hand_count_range() -> range:
        return range(10, 21)

    @staticmethod
    def secret_poker_hands() -> List[str]:
        return [
            "Royal Flush",
            "Five of a Kind",
            "Flush House",
            "Flush Five",
        ]

    @functools.cached_property
    def stakes_base(self) -> List[str]:
        return [
            "White",
            "Red",
            "Green",
            "Black",
            "Blue",
        ]

    @functools.cached_property
    def stakes_difficult(self) -> List[str]:
        return [
            "Purple",
            "Orange",
            "Gold",
        ]

    def stakes(self) -> List[str]:
        stakes: List[str] = self.stakes_base[:]

        if self.include_difficult_stakes:
            stakes.extend(self.stakes_difficult[:])

        return sorted(stakes)

    @staticmethod
    def endless_ante_range() -> range:
        return range(9, 13)

    @staticmethod
    def skip_count_range() -> range:
        return range(3, 9)

    @staticmethod
    def chip_count_range() -> range:
        return range(80000, 120001, 1000)


# Archipelago Options
class BalatroIncludeDifficultStakes(Toggle):
    """
    Indicates whether to include difficult stakes when generating Balatro objectives.
    """

    display_name = "Balatro Include Difficult Stakes"
