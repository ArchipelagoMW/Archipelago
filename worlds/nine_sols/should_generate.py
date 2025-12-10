import typing
from .options import LogicDifficulty

if typing.TYPE_CHECKING:
    from . import NineSolsWorld


def should_generate(category: str | None, world: "NineSolsWorld") -> bool:
    if category is None:  # this item/location/connection gets generated no matter what the player options are
        return True
    elif '&' in category:
        return all(should_generate(c, world) for c in category.split('&'))
    elif '|' in category:
        return any(should_generate(c, world) for c in category.split('|'))
    elif category == "medium_logic":
        return world.options.logic_difficulty >= LogicDifficulty.option_medium or world.using_ut
    raise ValueError(f'Invalid category: {category}')
