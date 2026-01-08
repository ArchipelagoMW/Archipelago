import logging

from random import Random
from typing import Any, List, Set, Tuple, Type, Union

from .enums import KeymastersKeepGamePlatforms

from .game import Game
from .games import AutoGameRegister

from .games.game_medley_game import GameMedleyGame


GameObjectiveGeneratorData = List[Tuple[Type[Game], List[str], List[str]]]


class GameObjectiveGeneratorException(Exception):
    pass


class GameObjectiveGenerator:
    games: List[Type[Game]]
    games_medley: List[Type[Game]]

    archipelago_options: Any

    def __init__(
        self,
        allowable_games: List[str] = None,
        allowable_games_medley: List[str] = None,
        game_medley_mode: bool = False,
        include_adult_only_or_unrated_games: bool = False,
        include_modern_console_games: bool = False,
        include_difficult_objectives: bool = False,
        include_time_consuming_objectives: bool = False,
        archipelago_options: Any = None,
    ) -> None:
        self.archipelago_options = archipelago_options

        self.games = self._filter_games(
            allowable_games,
            include_adult_only_or_unrated_games,
            include_modern_console_games,
            include_difficult_objectives,
            include_time_consuming_objectives,
        )

        if not len(self.games):
            raise GameObjectiveGeneratorException("No games are left after game / objective filtering")

        if game_medley_mode:
            self.games_medley = self._filter_games(
                allowable_games_medley,
                include_adult_only_or_unrated_games,
                include_modern_console_games,
                include_difficult_objectives,
                include_time_consuming_objectives,
            )

            if not len(self.games_medley):
                logging.warning(
                    "Keymaster's Keep: No medley games are left after game / objective filtering. Using all games."
                )

                self.games_medley = self.games[:]
        else:
            self.games_medley = self.games[:]

    def generate_from_plan(
        self,
        plan: List[int] = None,
        random: Random = None,
        include_difficult: bool = False,
        excluded_games_difficult: List[str] = None,
        include_time_consuming: bool = False,
        excluded_games_time_consuming: List[str] = None,
        game_medley_mode: bool = False,
        game_medley_percentage_chance: int = 100,
    ) -> GameObjectiveGeneratorData:
        if plan is None or not len(plan):
            return list()

        plan_length: int = len(plan)
        random = random or Random()

        game_selection: List[Type[Game]] = list()

        if plan_length <= len(self.games):
            game_selection = random.sample(self.games, plan_length)
        else:
            for _ in range(plan_length):
                game_selection.append(random.choice(self.games))

        if game_medley_mode:
            for i in range(len(game_selection)):
                if random.randint(1, 100) <= game_medley_percentage_chance:
                    game_selection[i] = GameMedleyGame

        data: GameObjectiveGeneratorData = list()
        objectives_in_use: Set[str] = set()

        i: int
        count: int
        for i, count in enumerate(plan):
            game_class: Type[Union[Game, GameMedleyGame]] = game_selection[i]

            if game_class == GameMedleyGame:
                game: GameMedleyGame = game_class(
                    random=random,
                    include_time_consuming_objectives=include_time_consuming,
                    include_difficult_objectives=include_difficult,
                    archipelago_options=self.archipelago_options,
                    game_selection=self.games_medley,
                )

                optional_constraints: List[str]
                objectives: List[str]

                optional_constraints, objectives, objectives_in_use = game.generate_objectives(
                    count=count,
                    include_difficult=include_difficult,
                    include_time_consuming=include_time_consuming,
                    excluded_games_time_consuming=excluded_games_time_consuming,
                    excluded_games_difficult=excluded_games_difficult,
                    objectives_in_use=objectives_in_use,
                )

                data.append((game, optional_constraints, objectives))
            else:
                is_in_time_consuming_exclusions: bool = (
                    game_class.game_name_with_platforms() in excluded_games_time_consuming
                )

                include_time_consuming = include_time_consuming and not is_in_time_consuming_exclusions

                is_in_difficult_exclusions: bool = game_class.game_name_with_platforms() in excluded_games_difficult
                include_difficult = include_difficult and not is_in_difficult_exclusions

                game: Game = game_class(
                    random=random,
                    include_time_consuming_objectives=include_time_consuming,
                    include_difficult_objectives=include_difficult,
                    archipelago_options=self.archipelago_options,
                )

                # This appears to completely ignore the passed 'include_difficult' value, but in reality, a game that
                # only implements difficult objectives would already be filtered out in the constructor when
                # 'include_difficult' is False, so we are only forcing it on when it's in the excluded list.
                if game.only_has_difficult_objectives and not include_difficult:
                    include_difficult = True

                # Same as above, but for time-consuming objectives
                if game.only_has_time_consuming_objectives and not include_time_consuming:
                    include_time_consuming = True

                optional_constraints: List[str]
                objectives: List[str]
                optional_constraints, objectives, objectives_in_use = game.generate_objectives(
                    count=count,
                    include_difficult=include_difficult,
                    include_time_consuming=include_time_consuming,
                    objectives_in_use=objectives_in_use,
                )

                data.append((game, optional_constraints, objectives))

        return data

    def _filter_games(
        self,
        allowable_games: List[str],
        include_adult_only_or_unrated_games: bool,
        include_modern_console_games: bool,
        include_difficult_objectives: bool,
        include_time_consuming_objectives: bool,
    ) -> List[Type[Game]]:
        filtered_games: List[Type[Game]] = list()

        modern_consoles: List[KeymastersKeepGamePlatforms] = [
            KeymastersKeepGamePlatforms.PS5,
            KeymastersKeepGamePlatforms.SW,
            KeymastersKeepGamePlatforms.XSX,
        ]

        game_name: str
        for game_name in allowable_games:
            if game_name not in AutoGameRegister.games:
                continue

            game: Type[Game] = AutoGameRegister.games[game_name]

            game_instance: Game = game(archipelago_options=self.archipelago_options)

            if not include_adult_only_or_unrated_games and game.is_adult_only_or_unrated:
                continue

            # We only want to filter out games that are exclusive to modern consoles, hence the primary platform check
            if not include_modern_console_games and game.platform in modern_consoles:
                continue

            if not include_difficult_objectives and game_instance.only_has_difficult_objectives:
                continue

            if not include_time_consuming_objectives and game_instance.only_has_time_consuming_objectives:
                continue

            filtered_games.append(game)

        return filtered_games
