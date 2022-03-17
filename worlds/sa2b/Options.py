import typing

from Options import Choice, Range, Option, Toggle, DeathLink, DefaultOnToggle, OptionList


class IncludeMission2(Toggle):
    """
    Allows logic to place items in Second Missions (100 Rings Missions)
    """
    displayname = "Include Second Missions"

class IncludeMission3(Toggle):
    """
    Allows logic to place items in Third Missions (Lost Chao Missions)
    """
    displayname = "Include Third Missions"

class IncludeMission4(Toggle):
    """
    Allows logic to place items in Fourth Missions (Timer Missions)
    """
    displayname = "Include Fourth Missions"

class IncludeMission5(Toggle):
    """
    Allows logic to place items in Fifth Missions (Hard Mode Missions)
    """
    displayname = "Include Fifth Missions"

class IncludeChaoEmblems(Toggle):
    """
    Allows logic to place items in Chao Races and Karate
    """
    displayname = "Include Chao Emblems"



sa2b_options: typing.Dict[str, type(Option)] = {
    "DeathLink": DeathLink,

    "IncludeMission2":    IncludeMission2,
    "IncludeMission3":    IncludeMission3,
    "IncludeMission4":    IncludeMission4,
    "IncludeMission5":    IncludeMission5,
    "IncludeChaoEmblems": IncludeChaoEmblems,
}
