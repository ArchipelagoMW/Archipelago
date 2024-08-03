import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class DaysAtSeaOptions(DefaultOffToggle):
    """Adds 'Spend Day at Sea'
    """
    display_name = "Days at Sea"
