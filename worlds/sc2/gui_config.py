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


def validate_color(color: Any, default: Tuple[float, float, float]) -> Tuple[Tuple[str, ...], Tuple[float, float, float]]:
    if isinstance(color, int):
        if color < 0:
            return ('Integer color was negative; expected a value from 0 to 0xffffff',), default
        return (), (
            ((color >> 8) & 0xff) / 255,
            ((color >> 4) & 0xff) / 255,
            ((color >> 0) & 0xff) / 255,
        )
    elif color == 'default':
        return (), default
    elif color == 'white':
        return (), (0.9, 0.9, 0.9)
    elif color == 'black':
        return (), (0.0, 0.0, 0.0)
    elif color == 'grey':
        return (), (0.345, 0.345, 0.345)
    elif color == 'red':
        return (), (0.85, 0.2, 0.1)
    elif color == 'orange':
        return (), (1.0, 0.65, 0.37)
    elif color == 'green':
        return (), (0.24, 0.84, 0.55)
    elif color == 'blue':
        return (), (0.3, 0.4, 1.0)
    elif color == 'pink':
        return (), (0.886, 0.176, 0.843)
    elif not isinstance(color, list):
        return (f'Invalid type {type(color)}; expected 3-element list or integer',), default
    elif len(color) != 3:
        return (f'Wrong number of elements in color; expected 3, got {len(color)}',), default
    result: List[float] = [0.0, 0.0, 0.0]
    errors: List[str] = []
    expected = 'expected a number from 0 to 1'
    for index, element in enumerate(color):
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


def get_button_color(race: str) -> Tuple[Tuple[str, ...], Tuple[float, float, float]]:
    from . import SC2World
    baseline_color = 0.345  # the button graphic is grey, with this value in each color channel
    if race == 'TERRAN':
        user_color: list = SC2World.settings.terran_button_color
        default_color = (0.0838, 0.2898, 0.2346)
    elif race == 'PROTOSS':
        user_color = SC2World.settings.protoss_button_color
        default_color = (0.345, 0.22425, 0.12765)
    elif race == 'ZERG':
        user_color = SC2World.settings.zerg_button_color
        default_color = (0.18975, 0.2415, 0.345)
    else:
        user_color = [baseline_color, baseline_color, baseline_color]
        default_color = (baseline_color, baseline_color, baseline_color)
    errors, color = validate_color(user_color, default_color)
    return errors, tuple(x / baseline_color for x in color)
