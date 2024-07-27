from typing import Union
import settings


class Starcraft2Settings(settings.Group):
    class WindowWidth(int):
        """The starting width the client window in pixels"""
    class WindowHeight(int):
        """The starting height the client window in pixels"""
    class StartMaximized(settings.Bool):
        """Controls whether the client window should start maximized"""

    window_width = WindowWidth(1080)
    window_height = WindowHeight(720)
    window_maximized: Union[StartMaximized, bool] = False
