from .options import NineSolsGameOptions


def should_generate(category: str | None, options: NineSolsGameOptions) -> bool:
    if category is None:  # this item/location/connection gets generated no matter what the player options are
        return True
    elif '&' in category:
        return all(should_generate(c, options) for c in category.split('&'))
    elif '|' in category:
        return any(should_generate(c, options) for c in category.split('|'))
    # no concrete categories have been implemented yet, but I'm sure we'll want some in the future
    raise ValueError(f'Invalid category: {category}')
