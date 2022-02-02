from typing import Dict
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option

class StartWithJewelryBox(Toggle):
    "Start with Jewelry Box unlocked"
    displayname = "Start with Jewelry Box"

#class ProgressiveVerticalMovement(Toggle):
#    "Always find vertical movement in the following order Succubus Hairpin -> Light Wall -> Celestial Sash"
#    displayname = "Progressive vertical movement"

#class ProgressiveKeycards(Toggle):
#    "Always find Security Keycard's in the following order D -> C -> B -> A"
#    displayname = "Progressive keycards"

class DownloadableItems(DefaultOnToggle):
    "With the tablet you will be able to download items at terminals"
    displayname = "Downloadable items"

class FacebookMode(Toggle):
    "Requires Oculus Rift(ng) to spot the weakspots in walls and floors"
    displayname = "Facebook mode"

class StartWithMeyef(Toggle):
    "Start with Meyef, ideal for when you want to play multiplayer."
    displayname = "Start with Meyef"

class QuickSeed(Toggle):
    "Start with Talaria Attachment, Nyoom!"
    displayname = "Quick seed"

class SpecificKeycards(Toggle):
    "Keycards can only open corresponding doors"
    displayname = "Specific Keycards"

class Inverted(Toggle):
    "Start in the past"
    displayname = "Inverted"

#class StinkyMaw(Toggle):
#    "Require gasmask for Maw"
#    displayname = "Stinky Maw"

class GyreArchives(Toggle):
    "Gyre locations are in logic. New warps are gated by Merchant Crow and Kobo"
    displayname = "Gyre Archives"

class Cantoran(Toggle):
    "Cantoran's fight and check are available upon revisiting his room"
    displayname = "Cantoran"

class LoreChecks(Toggle):
    "Memories and journal entries contain items."
    displayname = "Lore Checks"

class DamageRando(Toggle):
    "Each orb has a high chance of having lower base damage and a low chance of having much higher base damage."
    displayname = "Damage Rando"

class ShopFill(Choice):
    """Sets the items for sale in Merchant Crow's shops.
    Default: No sunglasses or trendy jacket, but sand vials for sale.
    Randomized: Up to 4 random items in each shop.
    Vanilla: Keep shops the same as the base game.
    Empty: Sell no items at the shop."""
    displayname = "Shop Inventory"
    option_default = 0
    option_randomized = 1
    option_vanilla = 2
    option_empty = 3

class ShopWarpShards(DefaultOnToggle):
    "Shops always sell warp shards (when keys possessed), ignoring inventory setting."
    displayname = "Always Sell Warp Shards"

class ShopMultiplier(Range):
    "Multiplier for the cost of items in the shop. Set to 0 for free shops."
    displayname = "Shop Price Multiplier"
    range_start = 0
    range_end = 10
    default = 1

# Some options that are available in the timespinner randomizer arent currently implemented
timespinner_options: Dict[str, Option] = {
    "StartWithJewelryBox": StartWithJewelryBox,
    #"ProgressiveVerticalMovement": ProgressiveVerticalMovement,
    #"ProgressiveKeycards": ProgressiveKeycards,
    "DownloadableItems": DownloadableItems,
    "FacebookMode": FacebookMode,
    "StartWithMeyef": StartWithMeyef,
    "QuickSeed": QuickSeed,
    "SpecificKeycards": SpecificKeycards,
    "Inverted": Inverted,
    #"StinkyMaw": StinkyMaw,
    "GyreArchives": GyreArchives,
    "Cantoran": Cantoran,
    "LoreChecks": LoreChecks,
    "DamageRando": DamageRando,
    "ShopFill": ShopFill,
    "ShopWarpShards": ShopWarpShards,
    "ShopMultiplier": ShopMultiplier,
    "DeathLink": DeathLink,
}

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0

def get_option_value(world: MultiWorld, player: int, name: str) -> int:
    option = getattr(world, name, None)

    if option == None:
        return 0

    return int(option[player].value)
