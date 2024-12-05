import typing

from Options import Choice, Option, PerGameCommonOptions, Toggle, DefaultOnToggle, Range, ItemsAccessibility, StartInventoryPool
from dataclasses import dataclass

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
    Uncle - The sword will always be placed on Link's Uncle."""
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

    
class Goal(Choice):
    """This option decides what goal is required to finish the randomizer.
    Defeat Ganon and Mother Brain - Find the required crystals and boss tokens to kill both bosses.
    Fast Ganon and Defeat Mother Brain - The hole to ganon is open without having to defeat Agahnim in 
                                         Ganon's Tower and Ganon can be defeat as soon you have the required 
                                         crystals to make Ganon vulnerable. For keysanity, this mode also removes 
                                         the Crateria Boss Key requirement from Tourian to allow faster access.
    All Dungeons and Defeat Mother Brain -  Similar to "Defeat Ganon and Mother Brain", but also requires all dungeons 
                                            to be beaten including Castle Tower and Agahnim."""
    display_name = "Goal"
    option_DefeatBoth = 0
    option_FastGanonDefeatMotherBrain = 1
    option_AllDungeonsDefeatMotherBrain = 2
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

class OpenTower(Range):
    """The amount of crystals required to be able to enter Ganon's Tower. 
    If this is set to Random, the amount can be found in-game on a sign next to Ganon's Tower."""
    display_name = "Open Tower"
    range_start = 0
    range_end = 7
    default = 7

class GanonVulnerable(Range):
    """The amount of crystals required to be able to harm Ganon. The amount can be found 
    in-game on a sign near the top of the Pyramid."""
    display_name = "Ganon Vulnerable"
    range_start = 0
    range_end = 7
    default = 7

class OpenTourian(Range):
    """The amount of boss tokens required to enter Tourian. The amount can be found in-game 
    on a sign above the door leading to the Tourian entrance."""
    display_name = "Open Tourian"
    range_start = 0
    range_end = 4
    default = 4

class SpinJumpsAnimation(Toggle):
    """Enable separate space/screw jump animations"""
    display_name = "Spin Jumps Animation"

class HeartBeepSpeed(Choice):
    """Sets the speed of the heart beep sound in A Link to the Past."""
    display_name = "Heart Beep Speed"
    option_Off = 0
    option_Quarter = 1
    option_Half = 2
    option_Normal = 3
    option_Double = 4
    default = 3

class HeartColor(Choice):
    """Changes the color of the hearts in the HUD for A Link to the Past."""
    display_name = "Heart Color"
    option_Red = 0
    option_Green = 1
    option_Blue = 2
    option_Yellow = 3
    default = 0

class QuickSwap(Toggle):
    """When enabled, lets you switch items in ALTTP with L/R"""
    display_name = "Quick Swap"

class EnergyBeep(DefaultOnToggle):
    """Toggles the low health energy beep in Super Metroid."""
    display_name = "Energy Beep"

@dataclass
class SMZ3Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    accessibility: ItemsAccessibility
    sm_logic: SMLogic
    sword_location: SwordLocation
    morph_location: MorphLocation
    goal: Goal
    key_shuffle: KeyShuffle
    open_tower: OpenTower
    ganon_vulnerable: GanonVulnerable
    open_tourian: OpenTourian
    spin_jumps_animation: SpinJumpsAnimation
    heart_beep_speed: HeartBeepSpeed
    heart_color: HeartColor
    quick_swap: QuickSwap
    energy_beep: EnergyBeep
