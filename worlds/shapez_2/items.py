from random import Random
from typing import TYPE_CHECKING, Any

from BaseClasses import Item
from .data.items import buildings, all_items

if TYPE_CHECKING:
    from . import Shapez2World


class Shapez2Item(Item):
    game = "shapez 2"


def lookup_table() -> dict[str, int]:
    return {
        name: data.item_id
        for table in all_items.maps
        for name, data in table.items()
    }


def generate_item(name: str, world: "Shapez2World") -> Shapez2Item:
    data = all_items[name]
    # Item id from lookup table is used instead of id from data for safety purposes
    return Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)


def get_item_lookup_table() -> dict[str, int]:
    return {name: data.item_id for name, data in all_items.items()}


def get_main_item_pool(world: "Shapez2World") -> list[Shapez2Item]:
    from .generate.items import buildings, island_buildings, mechanics, task_lines, operator_lines

    return [
        *buildings.generate_default(world),
        *island_buildings.generate_default(world),
        *mechanics.generate_default(world),
        *task_lines.generate_default(world),
        *operator_lines.generate_default(world),
    ]


def get_starting_items(world: "Shapez2World") -> list[str]:
    from .generate.items import buildings, island_buildings, mechanics, task_lines

    return [
        *buildings.generate_starting(world),
        *island_buildings.generate_starting(world),
        *mechanics.generate_starting(world),
        *task_lines.generate_starting(world),
        *world.options.start_inventory.value.keys(),
        *world.options.start_inventory_from_pool.value.keys(),
    ]


def pre_generate_logic(world: "Shapez2World") -> None:
    if "Random starting processor" in world.options.item_pool_modifiers:
        processors = list(buildings.simple_processors)
        world.starting_processor = world.random.choice(processors)


def generate_filler(world: "Shapez2World") -> str:
    if world.filler_nested is None:
        steps = [1, 2, 5, 10, 10, 20, 50, 100, 1000, 1000]
        if "Arbitrary research points" in world.options.item_pool_modifiers:
            steps[:4] = [1, 1, 1, 1]
        if "Arbitrary platform items" in world.options.item_pool_modifiers:
            steps[4:8] = [1, 1, 1, 1]
        if "Arbitrary blueprint points" in world.options.item_pool_modifiers:
            steps[8:] = [100, 100]
        world.filler_nested = [
            *(f"{x} Research Points" for x in range(1, 7, steps[0])),
            [
                *(f"{x} Research Points" for x in range(8, 13, steps[1])),
                [
                    *(f"{x} Research Points" for x in range(15, 31, steps[2])),
                    [
                        *(f"{x} Research Points" for x in range(40, 101, steps[3])),
                    ],
                ],
            ],
            *(f"{x} Platforms" for x in range(10, 41, steps[4])),
            [
                *(f"{x} Platforms" for x in range(60, 121, steps[5])),
                [
                    *(f"{x} Platforms" for x in range(150, 251, steps[6])),
                    [
                        *(f"{x} Platforms" for x in range(300, 501, steps[7])),
                    ],
                ],
            ],
        ]
        if "Include blueprint points" in world.options.item_pool_modifiers:
            world.filler_nested.extend([
                *(f"{x} Blueprint Points" for x in range(1000, 3000, steps[8])),
                [
                    *(f"{x} Blueprint Points" for x in range(3000, 10000, steps[9])),
                ],
            ])
    return random_choice_nested(world.random, world.filler_nested)


def random_choice_nested(random: Random, nested: list[Any | list | dict]) -> Any:
    """Helper function for getting a random element from a nested list."""
    current: Any | list | dict = nested
    while isinstance(current, list | dict):
        if isinstance(current, list):
            current = random.choice(current)
        else:
            current = random.choice(tuple(current.keys()))
    return current
