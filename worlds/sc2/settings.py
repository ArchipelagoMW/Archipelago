from typing import Union
import settings


class Starcraft2Settings(settings.Group):
    class WindowWidth(int):
        """The starting width the client window in pixels"""
    class WindowHeight(int):
        """The starting height the client window in pixels"""
    class GameWindowedMode(settings.Bool):
        """Controls whether the game should start in windowed mode"""
    class TerranButtonColor(list):
        """Defines the colour of terran mission buttons in the launcher in rgb format (3 elements ranging from 0 to 1)"""
    class ZergButtonColor(list):
        """Defines the colour of zerg mission buttons in the launcher in rgb format (3 elements ranging from 0 to 1)"""
    class ProtossButtonColor(list):
        """Defines the colour of protoss mission buttons in the launcher in rgb format (3 elements ranging from 0 to 1)"""

    window_width = WindowWidth(1080)
    window_height = WindowHeight(720)
    game_windowed_mode: Union[GameWindowedMode, bool] = False
    terran_button_color = TerranButtonColor([0.0838, 0.2898, 0.2346])
    zerg_button_color = ZergButtonColor([0.345, 0.22425, 0.12765])
    protoss_button_color = ProtossButtonColor([0.18975, 0.2415, 0.345])
