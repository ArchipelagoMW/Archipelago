from typing import Dict
from BaseClasses import MultiWorld
from Options import Toggle

class StartWithJewelryBox(Toggle):
    "Start with Jewelry Box unlocked"
    display_name = "Start with Jewelry Box"

#class ProgressiveVerticalMovement(Toggle):
#    "Always find vertical movement in the following order Succubus Hairpin -> Light Wall -> Celestial Sash"
#    display_name = "Progressive vertical movement"

#class ProgressiveKeycards(Toggle):
#    "Always find Security Keycard's in the following order D -> C -> B -> A"
#    display_name = "Progressive keycards"

class DownloadableItems(Toggle):
    "With the tablet you will be able to download items at terminals"
    display_name = "Downloadable items"

class FacebookMode(Toggle):
    "Requires Oculus Rift(ng) to spot the weakspots in walls and floors"
    display_name = "Facebook mode"

class StartWithMeyef(Toggle):
    "Start with Meyef, ideal for when you want to play multiplayer."
    display_name = "Start with Meyef"

class QuickSeed(Toggle):
    "Start with Talaria Attachment, Nyoom!"
    display_name = "Quick seed"

class SpecificKeycards(Toggle):
    "Keycards can only open corresponding doors"
    display_name = "Specific Keycards"

class Inverted(Toggle):
    "Start in the past"
    display_name = "Inverted"

#class StinkyMaw(Toggle):
#    "Require gassmask for Maw"
#    display_name = "Stinky Maw"

# Some options that are available in the timespinner randomizer arent currently implemented
timespinner_options: Dict[str, Toggle] = {
    "StartWithJewelryBox": StartWithJewelryBox,
    #"ProgressiveVerticalMovement": ProgressiveVerticalMovement,
    #"ProgressiveKeycards": ProgressiveKeycards,
    "DownloadableItems": DownloadableItems,
    "FacebookMode": FacebookMode,
    "StartWithMeyef": StartWithMeyef,
    "QuickSeed": QuickSeed,
    "SpecificKeycards": SpecificKeycards,
    "Inverted": Inverted,
    #"StinkyMaw": StinkyMaw
}

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    option = getattr(world, name, None)

    if option == None:
        return False

    return int(option[player].value) > 0