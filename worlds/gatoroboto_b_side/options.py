from dataclasses import dataclass

from Options import OptionGroup, PerGameCommonOptions, Toggle, DefaultOnToggle, Choice


# Flymech (off)
# Randomize Aqueduct Quest (on)
# Randomize Heater Core Quest (off)
# Randomize Ventilation Quest (on) (Reminder that it can only be ventilation quest off with progressive)
# Ultrahard (off)
# Upwarp (on)

class GlitchSmallmech(DefaultOnToggle):
    """
    Includes logic for the Smallmech glitch.
    In "Vanilla" difficulty, this will force the Lava Cooled event to be at Cooler
    """
    display_name = "Use Smallmech"

class GlitchWatermech(DefaultOnToggle):
    """
    Includes logic for the Watermech glitch.
    """
    display_name = "Use Watermech"

class GlitchGatoTech(Choice):
    """
    Difficulty of strategies
    Easy is recommended for normal players
    Hard includes a bunch of unique strategies, which require advanced knowledge
    Vanilla is a special difficulty, which:
    - removes the crash fixes in heater core
    - includes the logic for the standard cat vent skip and vent mashing
    - assumes that you can avoid a hardlock in ventilation by either routing properly or resetting the savefile.
    """
    display_name = "Gato Tech"
    option_easy = 1
    option_hard = 2
    option_vanilla = 3

    default = option_easy

class NexusStart(DefaultOnToggle):
    """
    Start in the Nexus instead of the Landing Site.
    Allows for some logic checks without rocket.
    """
    display_name = "Nexus Start"

class UnlockAllWarps(Toggle):
    """
    Allows you to warp to every main area (Landing Site, Aqueducts, Heater Core and Ventilation).
    IT IS CURRENTLY NOT FUNCTIONAL! :/
    """
    display_name = "Unlock all warps"

class ForceLocalStart(DefaultOnToggle):
    """
    Makes the Rocket (or if possible, Spin Jump + Dash) a local drop, preventing an early BK.
    """
    display_name = "Force Local Start"

@dataclass
class GatoRobotoOptions(PerGameCommonOptions):
    use_smallmech: GlitchSmallmech
    use_watermech: GlitchWatermech
    gato_tech: GlitchGatoTech
    nexus_start: NexusStart
    local_start: ForceLocalStart
    unlock_all_warps: UnlockAllWarps

option_groups = [
    OptionGroup(
        "Expert Logic",
        [GlitchSmallmech, GlitchWatermech, GlitchGatoTech, NexusStart],
    ),
    OptionGroup(
        "Technical Stuff",
        [ForceLocalStart],
    ),
]