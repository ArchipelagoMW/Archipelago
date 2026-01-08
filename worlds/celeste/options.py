# pylint: disable=missing-class-docstring, missing-module-docstring, fixme, unused-import

from enum import Enum
from typing import Dict, Union

from BaseClasses import MultiWorld
from Options import Choice, DefaultOnToggle, Range, Toggle


class BerriesRequired(Range):
    """Number of Strawberries required to access the goal level."""

    display_name = "Strawberry Requirement"
    range_start = 0
    range_end = 175
    default = 0


class CassettesRequired(Range):
    """Number of Cassettes required to access the goal level."""

    display_name = "Cassette Requirement"
    range_start = 0
    range_end = 8
    default = 0


class HeartsRequired(Range):
    """Number of Crystal Hearts required to access the goal level."""

    display_name = "Crystal Heart Requirement"
    range_start = 0
    range_end = 24
    default = 0


class LevelsRequired(Range):
    """Number of Level Completions required to access the goal level."""

    display_name = "Level Completion Requirement"
    range_start = 0
    range_end = 24
    default = 0


class VictoryConditionEnum(Enum):
    CHAPTER_7_SUMMIT = 0
    CHAPTER_8_CORE = 1
    CHAPTER_9_FAREWELL = 2


class VictoryCondition(Choice):
    """Selects the Chapter whose Completion is the Victory Condition for the World."""

    display_name = "Victory Condition"
    option_chapter_7_summit = VictoryConditionEnum.CHAPTER_7_SUMMIT.value
    option_chapter_8_core = VictoryConditionEnum.CHAPTER_8_CORE.value
    option_chapter_9_farewell = VictoryConditionEnum.CHAPTER_9_FAREWELL.value
    default = VictoryConditionEnum.CHAPTER_7_SUMMIT.value


class ProgressionSystemEnum(Enum):
    DEFAULT_PROGRESSION = 0


class ProgressionSystem(Choice):
    """Selects the Progression System for the World."""

    display_name = "Progression System"
    option_default_progression = ProgressionSystemEnum.DEFAULT_PROGRESSION.value
    default = ProgressionSystemEnum.DEFAULT_PROGRESSION.value


celeste_options: Dict[str, type] = {
    "berries_required": BerriesRequired,
    "cassettes_required": CassettesRequired,
    "hearts_required": HeartsRequired,
    "levels_required": LevelsRequired,
    "victory_condition": VictoryCondition,
    "progression_system": ProgressionSystem,
}


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[bool, int]:
    option = getattr(world, name, None)

    if option is None:
        return 0

    if issubclass(celeste_options[name], Toggle) or issubclass(celeste_options[name], DefaultOnToggle):
        return bool(option[player].value)
    return option[player].value
