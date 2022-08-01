import typing
from Options import Choice, Option, Toggle, DefaultOnToggle

class SMLogic(Choice):
    """This option selects what kind of logic to use for item placement inside
    Super Metroid.

    Normal - Normal logic includes only what Super Metroid teaches players
    itself. Anything that's not demonstrated in-game or by the intro cutscenes
    will not be required here.

    Hard - Hard logic is based upon the "no major glitches" ruleset and
    includes most tricks that are considered minor glitches, with some 
    restrictions. You'll want to be somewhat of a Super Metroid veteran for
    this logic.
    
    See https://samus.link/information for required moves."""
    display_name = "SMLogic"
    option_Normal = 0
    option_Hard = 1
    default = 0

class SwordLocation(Choice):
    """This option decides where the first sword will be placed.
    Randomized - The sword can be placed anywhere.
    Early - The sword will be placed in a location accessible from the start of
    the game.
    Unce assured - The sword will always be placed on Link's Uncle."""
    display_name = "Sword Location"
    option_Randomized = 0
    option_Early = 1
    option_Uncle = 2
    default = 0

class MorphLocation(Choice):
    """This option decides where the morph ball will be placed.
    Randomized - The morph ball can be placed anywhere.
    Early - The morph ball will be placed in a location accessible from the 
    start of the game.
    Original location - The morph ball will always be placed at its original 
    location."""
    display_name = "Morph Location"
    option_Randomized = 0
    option_Early = 1
    option_Original = 2
    default = 0

class KeyShuffle(Choice):
    """This option decides how dungeon items such as keys are shuffled.
    None - A Link to the Past dungeon items can only be placed inside the 
    dungeon they belong to, and there are no changes to Super Metroid.
    Keysanity - See https://samus.link/information"""
    display_name = "Key Shuffle"
    option_None = 0
    option_Keysanity = 1
    default = 0

class OpenTower(Choice):
    display_name = "Open Tower"
    option_NoCrystals = 0
    option_OneCrystal = 1
    option_TwoCrystals = 2
    option_ThreeCrystals = 3
    option_FourCrystals = 4
    option_FiveCrystals = 5
    option_SixCrystals = 6
    option_SevenCrystals = 7
    default = 7

class GanonVulnerable(Choice):
    display_name = "Ganon Vulnerable"
    option_NoCrystals = 0
    option_OneCrystal = 1
    option_TwoCrystals = 2
    option_ThreeCrystals = 3
    option_FourCrystals = 4
    option_FiveCrystals = 5
    option_SixCrystals = 6
    option_SevenCrystals = 7
    default = 7

class OpenTourian(Choice):
    display_name = "Open Tourian"
    option_NoBosses = 0
    option_OneBoss = 1
    option_TwoBosses = 2
    option_ThreeBosses = 3
    option_FourBosses = 4
    default = 4

class SpinJumpsAnimation(Toggle):
    """Enable separate space/screw jump animations"""
    display_name = "Spin Jumps Animation"

class HeartBeepSpeed(Choice):
    display_name = "Heart Beep Speed"
    option_Off = 0
    option_Quarter = 1
    option_Half = 2
    option_Normal = 3
    option_Double = 4
    default = 3

class HeartColor(Choice):
    display_name = "Heart Color"
    option_Red = 0
    option_Green = 1
    option_Blue = 2
    option_Yellow = 3
    default = 0

class QuickSwap(Toggle):
    display_name = "Quick Swap"

class EnergyBeep(DefaultOnToggle):
    display_name = "Energy Beep"


smz3_options: typing.Dict[str, type(Option)] = {
    "sm_logic": SMLogic,
    "sword_location": SwordLocation,
    "morph_location": MorphLocation,
    "key_shuffle": KeyShuffle,
    "open_tower": OpenTower, 
    "ganon_vulnerable": GanonVulnerable,
    "open_tourian": OpenTourian,
    "spin_jumps_animation": SpinJumpsAnimation,
    "heart_beep_speed": HeartBeepSpeed,
    "heart_color": HeartColor, 
    "quick_swap": QuickSwap,
    "energy_beep": EnergyBeep
    }
