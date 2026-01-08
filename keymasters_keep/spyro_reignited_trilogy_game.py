from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SpyroReignitedTrilogyArchipelagoOptions:
    spyro_reignited_trilogy_games: SpyroReignitedTrilogyGames
    spyro_reignited_trilogy_include_speedrun_challenges: SpyroReignitedTrilogyIncludeSpeedrunChallenges


class SpyroReignitedTrilogyGame(Game):
    name = "Spyro Reignited Trilogy"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = SpyroReignitedTrilogyArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        objectives: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={
                    "BOSS": (self.bosses, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS without taking damage",
                data={
                    "BOSS": (self.bosses, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

        if bool(self.archipelago_options.spyro_reignited_trilogy_include_speedrun_challenges.value):
            objectives.extend([
                GameObjectiveTemplate(
                    label="Complete the following speedrun: SPEEDRUN",
                    data={
                        "SPEEDRUN": (self.speedrun_challenges, 1)
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        games: List[str] = self.games()

        if "Spyro the Dragon" in games:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Complete FLIGHT",
                    data={
                        "FLIGHT": (self.flights_spyro_1, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        if "Spyro 2: Ripto's Rage!" in games:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Complete FLIGHT in under 1:15",
                    data={
                        "FLIGHT": (self.flights_spyro_2, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
            ])

        if "Spyro: Year of the Dragon" in games:
            objectives.extend([
                GameObjectiveTemplate(
                    label="Complete a FLIGHT time trial",
                    data={
                        "FLIGHT": (self.flights_spyro_3, 1)
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Win a RACE race",
                    data={
                        "RACE": (self.flights_races_spyro_3, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return objectives

    def games(self) -> List[str]:
        return sorted(self.archipelago_options.spyro_reignited_trilogy_games.value)

    def bosses(self) -> List[str]:
        bosses: List[str] = list()
        games: List[str] = self.games()

        if "Spyro the Dragon" in games:
            bosses.extend([
                "Toasty (Spyro 1)",
                "Doctor Shemp (Spyro 1)",
                "Blowhard (Spyro 1)",
                "Metalhead (Spyro 1)",
                "Jacques (Spyro 1)",
                "Gnasty Gnorc (Spyro 1)",
            ])

        if "Spyro 2: Ripto's Rage!" in games:
            bosses.extend([
                "Crush (Spyro 2)",
                "Gulp (Spyro 2)",
                "Ripto (Spyro 2)",
            ])

        if "Spyro: Year of the Dragon" in games:
            bosses.extend([
                "Buzz (Spyro 3)",
                "Spike (Spyro 3)",
                "Scorch (Spyro 3)",
                "The Sorceress (Spyro 3)",
            ])

        return sorted(bosses)

    def speedrun_challenges(self) -> List[str]:
        speedrun_challenges: List[str] = list()
        games: List[str] = self.games()

        if "Spyro the Dragon" in games:
            speedrun_challenges.extend([
                "Any% No Balloonist Skip (Spyro 1)",
                "Neo Vortex (Spyro 1)",
                "12 Egg No Ballonist Skip (Spyro 1)",
            ])

        if "Spyro 2: Ripto's Rage!" in games:
            speedrun_challenges.extend([
                "14 Talisman (Spyro 2)",
                "40 Orb (Spyro 2)",
                "Bone Dance (Spyro 2)",
                "Neo Portals (Spyro 2)",
                "True Love (Spyro 2)",
            ])

        if "Spyro: Year of the Dragon" in games:
            speedrun_challenges.extend([
                "Any% (Spyro 3)",
                "Bone Dance (Spyro 3)",
                "Neo Portals (Spyro 3)",
            ])

        return sorted(speedrun_challenges)

    @staticmethod
    def flights_spyro_1() -> List[str]:
        return [
            "Sunny Flight (Spyro 1)",
            "Night Flight (Spyro 1)",
            "Crystal Flight (Spyro 1)",
            "Wild Flight (Spyro 1)",
            "Icy Flight (Spyro 1)",
        ]

    @staticmethod
    def flights_spyro_2() -> List[str]:
        return [
            "Ocean Speedway (Spyro 2)",
            "Metro Speedway (Spyro 2)",
            "Icy Speedway (Spyro 2)",
            "Canyon Speedway (Spyro 2)",
        ]

    @staticmethod
    def flights_spyro_3() -> List[str]:
        return [
            "Mushroom Speedway (Spyro 3)",
            "Country Speedway (Spyro 3)",
            "Honey Speedway (Spyro 3)",
            "Harbor Speedway (Spyro 3)",
        ]

    @staticmethod
    def races_spyro_3() -> List[str]:
        return [
            "Lost Fleet (Spyro 3)",
            "Super Bonus Round (Spyro 3)",
        ]

    def flights_races_spyro_3(self) -> List[str]:
        return sorted(self.flights_spyro_3() + self.races_spyro_3())


# Archipelago Options
class SpyroReignitedTrilogyGames(OptionSet):
    """
    Indicates which Spyro Reignited Trilogy games to use when generating objectives.
    """

    display_name = "Spyro Reignited Trilogy Games"
    valid_keys = [
        "Spyro the Dragon",
        "Spyro 2: Ripto's Rage!",
        "Spyro: Year of the Dragon",
    ]

    default = valid_keys


class SpyroReignitedTrilogyIncludeSpeedrunChallenges(Toggle):
    """
    Indicates whether to include speedrun objectives for Spyro Reignited Trilogy.

    Requires knowledge of the speedrun categories for each game and how to execute them.
    """

    display_name = "Spyro Reignited Trilogy Include Speedrun Challenges"
