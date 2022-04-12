import typing
from Options import Choice, Option

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

smz3_options: typing.Dict[str, type(Option)] = {
    "sm_logic": SMLogic,
    "sword_location": SwordLocation,
    "morph_location": MorphLocation,
    "key_shuffle": KeyShuffle
    }
