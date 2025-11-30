from .options import NineSolsGameOptions, LogicDifficulty


def should_generate(category: str | None, options: NineSolsGameOptions) -> bool:
    if category is None:  # this item/location/connection gets generated no matter what the player options are
        return True
    elif '&' in category:
        return all(should_generate(c, options) for c in category.split('&'))
    elif '|' in category:
        return any(should_generate(c, options) for c in category.split('|'))
    elif category == "medium_logic":
        return options.logic_difficulty >= LogicDifficulty.option_medium
    raise ValueError(f'Invalid category: {category}')
