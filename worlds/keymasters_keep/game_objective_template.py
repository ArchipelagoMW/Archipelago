from random import Random
from typing import Any, Callable, Dict, List, Sequence, Tuple, Union


GameObjectiveTemplateData = Dict[
    str,
    Tuple[Callable[[], Union[List[Any], range]], Union[int, Sequence, Callable[[], int]]]
]


class GameObjectiveTemplate:
    label: str
    data: GameObjectiveTemplateData
    is_time_consuming: bool = False
    is_difficult: bool = False
    weight: int = 1

    def __init__(
        self, label=None, data=None, is_time_consuming: bool = False, is_difficult: bool = False, weight: int = 1
    ) -> None:
        self.label = label
        self.data = data
        self.is_time_consuming = is_time_consuming
        self.is_difficult = is_difficult
        self.weight = weight

    def generate_game_objective(self, random: Random) -> str:
        game_objective = self.label

        key: str
        collection: Tuple[Callable[[], Union[List[Any], range]], Union[int, Sequence[int], Callable[[], int]]]
        for key, collection in self.data.items():
            k: int

            if isinstance(collection[1], Sequence):
                k = random.choice(collection[1])
            elif callable(collection[1]):
                k = collection[1]()
            else:
                k = collection[1]

            game_objective = game_objective.replace(
                key,
                ", ".join(str(value) for value in random.sample(*(collection[0](), k)))
            )

        return game_objective
