"""
Import this before importing client_gui.py to set window defaults from world settings.
"""
from .settings import Starcraft2Settings
from typing import List

def apply_window_defaults() -> List[str]:
    """
    Set the kivy config keys from the sc2world user settings.
    Returns a list of warnings to be printed once the GUI is started.
    """
    from . import SC2World
    # This is necessary to prevent kivy from failing because it got invalid command-line args,
    # or from spamming the logs.
    # Must happen before importing kivy.config
    import os
    import Utils
    os.environ["KIVY_NO_CONSOLELOG"] = "1"
    os.environ["KIVY_NO_FILELOG"] = "1"
    os.environ["KIVY_NO_ARGS"] = "1"
    os.environ["KIVY_LOG_ENABLE"] = "0"
    if Utils.is_frozen():
        os.environ["KIVY_DATA_DIR"] = Utils.local_path("data")

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

    # from kivy.config import Config
    # Config.set('graphics', 'width', str(window_width))
    # Config.set('graphics', 'height', str(window_height))
    # if SC2World.settings.window_maximized:
    #     Config.set('graphics', 'window_state', 'maximized')
    return warnings
