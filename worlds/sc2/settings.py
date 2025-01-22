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
    class DisableForcedCamera(str):
        """Overrides the disable forced-camera slot option. Possible values: `true`, `false`, `default`. Default uses slot value"""
    class SkipCutscenes(str):
        """Overrides the skip cutscenes slot option. Possible values: `true`, `false`, `default`. Default uses slot value"""
    class GameDifficulty(str):
        """Overrides the slot's difficulty setting. Possible values: `casual`, `normal`, `hard`, `brutal`, `default`. Default uses slot value"""
    class GameSpeed(str):
        """Overrides the slot's gamespeed setting. Possible values: `slower`, `slow`, `normal`, `fast`, `faster`, `default`. Default uses slot value"""

    window_width = WindowWidth(1080)
    window_height = WindowHeight(720)
    game_windowed_mode: Union[GameWindowedMode, bool] = False
    disable_forced_camera = DisableForcedCamera("default")
    skip_cutscenes = SkipCutscenes("default")
    game_difficulty = GameDifficulty("default")
    game_speed = GameSpeed("default")
    terran_button_color = TerranButtonColor([0.0838, 0.2898, 0.2346])
    zerg_button_color = ZergButtonColor([0.345, 0.22425, 0.12765])
    protoss_button_color = ProtossButtonColor([0.18975, 0.2415, 0.345])
