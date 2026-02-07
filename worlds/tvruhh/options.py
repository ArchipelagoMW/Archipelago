from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle, OptionSet, DefaultOnToggle



class DisabledDreams(OptionSet):
    """Disable any Dreams that you do not want to complete in the multiworld.
    
    To add a Dream to the list, add this inside the square brackets: "[Dream of choice]"
    Make sure that it looks something like this: ["Love at First Shot", "Trypophobia", "God Run"]

    Dreams are the same things as the Steam Achievements of TVRUHH"""

    display_name = "Disabled Dreams"

    default = []

class GrindyDreams(DefaultOnToggle):
    """Enables Dreams that are considered grindy.

    Keep in mind that some grindy Dreams are technically available from the start.
    (That means every check that will be placed early can land on these Dreams during generation)

    Dreams are equivalent to achievements in this game."""

    display_name = "Grindy Dreams"

class ExtremelyGrindyDreams(Toggle):
    """Enables Dreams that are considered extremely grindy.

    Keep in mind that some extremely grindy Dreams are technically available from the start.
    (That means every check that will be placed early can land on these Dreams during generation)

    Dreams are equivalent to achievements in this game."""

    display_name = "Extremely Grindy Dreams"

class TediousDreams(DefaultOnToggle):
    """Enables Dreams that are considered tedious.

    Keep in mind that some tedious Dreams are technically available from the start.
    (That means every check that will be placed early can land on these Dreams during generation)
    
    Dreams are equivalent to achievements in this game."""

    display_name = "Tedious Dreams"

class ExtremelyTediousDreams(Toggle):
    """Enables Dreams that are considered tedious.

    Keep in mind that some extremely tedious Dreams are technically available from the start.
    (That means every check that will be placed early can land on these Dreams during generation)
    
    Dreams are equivalent to achievements in this game."""

    display_name = "Extremely Tedious Dreams"





@dataclass
class TVRUHHOptions(PerGameCommonOptions):
    #grindy_dreams: GrindyDreams
    #tedious_dreams: TediousDreams
    #extremely_grindy_dreams: ExtremelyGrindyDreams
    #extremely_tedious_dreams: ExtremelyTediousDreams
    disabled_dreams: DisabledDreams





option_groups = [
    OptionGroup(
        "Dream Options",
        [
            GrindyDreams, 
            ExtremelyGrindyDreams, 
            TediousDreams, 
            ExtremelyTediousDreams,
            DisabledDreams
        ]
    )
]

option_presets = {
    "intended": {
        "grindy_dreams": True,
        "extremely_grindy_dreams": False,
        "tedious_dreams": True,
        "extremely_tedious_dreams": False,
        "disabled_dreams": []
    }
}