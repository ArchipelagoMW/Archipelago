from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class BizHawkShufflerArchipelagoOptions:
    bizhawk_shuffler_games: BizHawkShufflerGames


class BizHawkShufflerGame(Game):
    name = "BizHawk Shuffler"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = BizHawkShufflerArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat one of the following games: GAMES  Swap Times: MIN-MAX  Order: ORDER",
                data={
                    "GAMES": (self.games, 2),
                    "MIN": (self.swap_time_minimum_range, 1),
                    "MAX": (self.swap_time_maximum_range, 1),
                    "ORDER": (self.orders, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat one of the following games: GAMES  Swap Times: MIN-MAX  Order: ORDER",
                data={
                    "GAMES": (self.games, 3),
                    "MIN": (self.swap_time_minimum_range, 1),
                    "MAX": (self.swap_time_maximum_range, 1),
                    "ORDER": (self.orders, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat one of the following games: GAMES  Swap Times: MIN-MAX  Order: ORDER",
                data={
                    "GAMES": (self.games, 4),
                    "MIN": (self.swap_time_minimum_range, 1),
                    "MAX": (self.swap_time_maximum_range, 1),
                    "ORDER": (self.orders, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat one of the following games: GAMES  Swap Times: MIN-MAX  Order: ORDER",
                data={
                    "GAMES": (self.games, 5),
                    "MIN": (self.swap_time_minimum_range, 1),
                    "MAX": (self.swap_time_maximum_range, 1),
                    "ORDER": (self.orders, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat all of the following games: GAMES  Swap Times: MIN-MAX  Order: ORDER",
                data={
                    "GAMES": (self.games, 2),
                    "MIN": (self.swap_time_minimum_range, 1),
                    "MAX": (self.swap_time_maximum_range, 1),
                    "ORDER": (self.orders, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat all of the following games: GAMES  Swap Times: MIN-MAX  Order: ORDER",
                data={
                    "GAMES": (self.games, 3),
                    "MIN": (self.swap_time_minimum_range, 1),
                    "MAX": (self.swap_time_maximum_range, 1),
                    "ORDER": (self.orders, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
        ]

    def games(self) -> List[str]:
        return sorted(self.archipelago_options.bizhawk_shuffler_games.value)

    @staticmethod
    def swap_time_minimum_range() -> range:
        return range(15, 41)

    @staticmethod
    def swap_time_maximum_range() -> range:
        return range(41, 121)

    @staticmethod
    def orders() -> List[str]:
        return [
            "Fixed",
            "Random",
        ]


# Archipelago Options
class BizHawkShufflerGames(OptionSet):
    """
    Indicates which games the players owns and wants to consider for BizHawk Shuffler.

    A minimum of 5 games is required.
    """

    display_name = "BizHawk Shuffler Games"
    default = [
        "[PLATFORM] Game 1",
        "[PLATFORM] Game 2",
        "[PLATFORM] Game 3",
        "[PLATFORM] Game 4",
        "[PLATFORM] Game 5",
        "...",
    ]
