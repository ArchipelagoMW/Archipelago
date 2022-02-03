import typing
from Options import Choice, Option

class SMLogic(Choice):
    displayname = "SMLogic"
    option_Normal = 0
    option_Hard = 1
    default = 0

class SwordLocation(Choice):
    displayname = "Sword Location"
    option_Randomized = 0
    option_Early = 1
    option_Uncle = 2
    default = 0

class MorphLocation(Choice):
    displayname = "Morph Location"
    option_Randomized = 0
    option_Early = 1
    option_Original = 2
    default = 0

class KeyShuffle(Choice):
    displayname = "Key Shuffle"
    option_None = 0
    option_Keysanity = 1
    default = 0

smz3_options: typing.Dict[str, type(Option)] = {
    "sm_logic": SMLogic,
    "sword_location": SwordLocation,
    "morph_location": MorphLocation,
    "key_shuffle": KeyShuffle
    }
