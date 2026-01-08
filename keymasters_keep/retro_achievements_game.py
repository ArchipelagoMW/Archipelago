from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RetroAchievementsArchipelagoOptions:
    retroachievements_games: RetroAchievementsGames


class RetroAchievementsGame(Game):
    name = "RetroAchievements"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = RetroAchievementsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Use Hardcore Mode",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat GAME",
                data={"GAME": (self.games, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Unlock at least X% of the achievements in GAME",
                data={"GAME": (self.games, 1), "X": (self.percentages, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=9,
            ),
            GameObjectiveTemplate(
                label="Unlock all the achievements in GAME",
                data={"GAME": (self.games, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    def games(self) -> List[str]:
        return sorted(self.archipelago_options.retroachievements_games.value)

    @staticmethod
    def percentages() -> range:
        return range(10, 76)


# Archipelago Options
class RetroAchievementsGames(OptionSet):
    """
    Indicates which games the players owns and wants to hunt achievements for on RetroAchievements.
    """

    display_name = "RetroAchievements Games"
    default = [
        "[PLATFORM] Game 1",
        "[PLATFORM] Game 2",
        "[PLATFORM] Game 3",
    ]

