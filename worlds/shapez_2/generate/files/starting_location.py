from typing import Any

from ...output import Shapez2ScenarioContainer


def get_fixed_patches(container: "Shapez2ScenarioContainer") -> list[dict[str, Any]]:
    shapes_order = ["RuRuRuRu", "SuSuSuSu", "CuCuCuCu", "WuWuWuWu"]
    container.world.random.shuffle(shapes_order)
    return [
        {
            "Shape": shapes_order[0],
            "Position_LC":{"x":31,"y":30},
            "LocalTiles":[{},{"x":-1,"y":-2},{"y":-1},{"x":-1,"y":-1}]
        },
        {
            "Shape": shapes_order[1],
            "Position_LC":{"x":31,"y":34},
            "LocalTiles":[{},{"y":1},{"x":-1,"y":1},{"x":-1,"y":2}]
        },
        {
            "Shape": shapes_order[2],
            "Position_LC":{"x":29,"y":32},
            "LocalTiles":[{},{"x":-1},{"x":-1,"y":-1},{"x":-2}]
        },
        {
            "Shape": shapes_order[3],
            "Position_LC":{"x":33,"y":32},
            "LocalTiles":[{},{"x":1},{"y":1},{"y":-1}]
        }
    ]


def get_starting_chunks(container: "Shapez2ScenarioContainer") -> list[dict[str, Any]]:
    return [
        {
            "GuaranteedShapePatches": ["CuCuCuCu", "RuRuRuRu", "SuSuSuSu", "WuWuWuWu"],
            "GuaranteedColorPatches": ["r", "b", "g"]
        }
    ]
