"""
Import this before importing client_gui.py to set window defaults from world settings.
"""
from .settings import Starcraft2Settings
from typing import List

def get_window_defaults() -> List[str]:
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
