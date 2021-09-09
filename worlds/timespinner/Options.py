import typing
from Options import Toggle

class StartWithMeyef(Toggle):
    "Start with Meyef, ideal for when you want to play multiplayer."
    display_name = "Start with Meyef"
    option_true = 1
    option_false = 0
    default = 0

class QuickSeed(Toggle):
    "Start with Talaria Attachment, Nyoom!"
    display_name = "Quick seed"
    option_true = 1
    option_false = 0
    default = 0

class StartWithJewelryBox(Toggle):
    "Start with Jewelry Box unlocked"
    display_name = "Start with Jewelry Box"
    option_true = 1
    option_false = 0
    default = 0

timespinner_options: typing.Dict[str, any] = {
    "start_with_jewerlybox": StartWithJewelryBox,
    "start_with_meyef": StartWithMeyef,
    "quickseed": QuickSeed,
}