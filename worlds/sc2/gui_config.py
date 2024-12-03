"""
Import this before importing client_gui.py to set window defaults from world settings.
"""
from .settings import Starcraft2Settings
from typing import List, Tuple, Any


def get_window_defaults() -> Tuple[List[str], int, int]:
    """
    Gets the window size options from the sc2 settings.
    Returns a list of warnings to be printed once the GUI is started, followed by the window width and height
    """
    from . import SC2World

    # validate settings
    warnings: List[str] = []
    if isinstance(SC2World.settings.window_height, int) and SC2World.settings.window_height > 0:
        window_height = SC2World.settings.window_height
    else:
        warnings.append(f"Invalid value for options.yaml key sc2_options.window_height: '{SC2World.settings.window_height}'. Expected a positive integer.")
        window_height = Starcraft2Settings.window_height
    if isinstance(SC2World.settings.window_width, int) and SC2World.settings.window_width > 0:
        window_width = SC2World.settings.window_width
    else:
        warnings.append(f"Invalid value for options.yaml key sc2_options.window_width: '{SC2World.settings.window_width}'. Expected a positive integer.")
        window_width = Starcraft2Settings.window_width

    return warnings, window_width, window_height


def validate_colour(colour: Any, default: Tuple[float, float, float]) -> Tuple[Tuple[str, ...], Tuple[float, float, float]]:
    if isinstance(colour, int):
        if colour < 0:
            return ('Integer colour was negative; expected a value from 0 to 0xffffff',), default
        return (), (
            ((colour >> 8) & 0xff) / 255,
            ((colour >> 4) & 0xff) / 255,
            ((colour >> 0) & 0xff) / 255,
        )
    elif colour == 'default':
        return (), default
    elif colour == 'white':
        return (), (0.9, 0.9, 0.9)
    elif colour == 'black':
        return (), (0.0, 0.0, 0.0)
    elif colour == 'grey':
        return (), (0.345, 0.345, 0.345)
    elif colour == 'red':
        return (), (0.85, 0.2, 0.1)
    elif colour == 'orange':
        return (), (1.0, 0.65, 0.37)
    elif colour == 'green':
        return (), (0.24, 0.84, 0.55)
    elif colour == 'blue':
        return (), (0.3, 0.4, 1.0)
    elif colour == 'pink':
        return (), (0.886, 0.176, 0.843)
    elif not isinstance(colour, list):
        return (f'Invalid type {type(colour)}; expected 3-element list or integer',), default
    elif len(colour) != 3:
        return (f'Wrong number of elements in colour; expected 3, got {len(colour)}',), default
    result: list[float] = [0.0, 0.0, 0.0]
    errors: List[str] = []
    expected = 'expected a number from 0 to 1'
    for index, element in enumerate(colour):
        if isinstance(element, int):
            element = float(element)
        if not isinstance(element, float):
            errors.append(f'Invalid type {type(element)} at index {index}; {expected}')
            continue
        if element < 0:
            errors.append(f'Negative element {element} at index {index}; {expected}')
            continue
        if element > 1:
            errors.append(f'Element {element} at index {index} is greater than 1; {expected}')
            result[index] = 1.0
            continue
        result[index] = element
    return tuple(errors), tuple(result)


def get_button_colour(race: str) -> Tuple[Tuple[str, ...], Tuple[float, float, float]]:
    from . import SC2World
    baseline_colour = 0.345  # the button graphic is grey, with this value in each colour channel
    if race == 'TERRAN':
        user_colour = SC2World.settings.terran_button_colour
    elif race == 'PROTOSS':
        user_colour = SC2World.settings.protoss_button_colour
    elif race == 'ZERG':
        user_colour = SC2World.settings.zerg_button_colour
    else:
        user_colour = [baseline_colour, baseline_colour, baseline_colour]
    default_colours = {
        'TERRAN': (0.0838, 0.2898, 0.2346),
        'ZERG': (0.345, 0.22425, 0.12765),
        'PROTOSS': (0.18975, 0.2415, 0.345),
    }
    errors, colour = validate_colour(user_colour, default_colours.get(race, (baseline_colour, baseline_colour, baseline_colour)))
    return errors, tuple(x / baseline_colour for x in colour)
