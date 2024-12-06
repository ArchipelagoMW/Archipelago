import typing
from dataclasses import dataclass

import Options
from Options import Choice
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle

DefaultOffToggle = Options.Toggle


class IllFated(DefaultOffToggle):
    """Adds locations related to your ship sinking
    """
    display_name = "Shuffle Ill-Fated Checks"
