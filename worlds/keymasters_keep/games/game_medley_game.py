from __future__ import annotations

from typing import Any, List, Set, Tuple, Type

from dataclasses import dataclass
from random import Random

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class GameMedleyArchipelagoOptions:
    pass


class GameMedleyGame(Game):
    name = "Game Medley"
    platform = KeymastersKeepGamePlatforms.META

    platforms_other = None

    is_adult_only_or_unrated = False

    should_autoregister = False

    options_cls = GameMedleyArchipelagoOptions

    game_selection: List[Type[Game]]

    def __init__(
        self,
        random: Random = None,
        include_time_consuming_objectives: bool = False,
        include_difficult_objectives: bool = False,
        archipelago_options: Any = None,
        game_selection: List[Type[Game]] = None,
    ) -> None:
        super().__init__(
            random=random,
            include_time_consuming_objectives=include_time_consuming_objectives,
            include_difficult_objectives=include_difficult_objectives,
            archipelago_options=archipelago_options,
        )

        self.game_selection = game_selection

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def generate_objectives(
        self,
        count: int = 1,
        include_difficult: bool = False,
        include_time_consuming: bool = False,
        excluded_games_time_consuming: List[str] = None,
        excluded_games_difficult: List[str] = None,
        objectives_in_use: Set[str] = None,
    ) -> Tuple[List[str], List[str], Set[str]]:
        excluded_games_time_consuming = excluded_games_time_consuming or list()
        excluded_games_difficult = excluded_games_difficult or list()

        objectives_in_use = objectives_in_use or set()

        optional_constraints: List[str] = list()
        objectives: List[str] = list()

        passes_templates: int = 0

        while len(objectives) < count:
            passes_templates += 1

            game: Type[Game] = self.random.choice(self.game_selection)

            is_in_time_consuming_exclusions: bool = game.game_name_with_platforms() in excluded_games_time_consuming
            include_time_consuming = include_time_consuming and not is_in_time_consuming_exclusions

            is_in_difficult_exclusions: bool = game.game_name_with_platforms() in excluded_games_difficult
            include_difficult = include_difficult and not is_in_difficult_exclusions

            game_instance: Game = game(
                random=self.random,
                include_time_consuming_objectives=include_time_consuming,
                include_difficult_objectives=include_difficult,
                archipelago_options=self.archipelago_options,
            )

            # This appears to completely ignore the passed 'include_difficult' value, but in reality, a game that
            # only implements difficult objectives would already be filtered out in the constructor when
            # 'include_difficult' is False, so we are only forcing it on when it's in the excluded list.
            if game_instance.only_has_difficult_objectives and not include_difficult:
                include_difficult = True

            # Same as above, but for time-consuming objectives
            if game_instance.only_has_time_consuming_objectives and not include_time_consuming:
                include_time_consuming = True

            filtered_templates: List[GameObjectiveTemplate] = game_instance.filter_game_objective_templates(
                include_difficult=include_difficult,
                include_time_consuming=include_time_consuming,
            )

            if not len(filtered_templates):
                filtered_templates = game_instance.game_objective_templates()

            weights: List[int] = [template.weight for template in filtered_templates]

            template: GameObjectiveTemplate = self.random.choices(filtered_templates, weights=weights, k=1)[0]

            passes: int = 0

            while True:
                passes += 1

                objective: str = template.generate_game_objective(self.random)

                if objective not in objectives_in_use:
                    objective = f"{game.name} -> {objective}"

                    objectives.append(objective)
                    objectives_in_use.add(objective)

                    break

                if passes_templates > 50:
                    objective = f"{game.name} -> {objective}"
                    objectives.append(objective)

                    break

                if passes > 10:
                    break

        return optional_constraints, objectives, objectives_in_use


# Archipelago Options
# ...
