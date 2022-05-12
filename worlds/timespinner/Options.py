from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict

class StartWithJewelryBox(Toggle):
    "Start with Jewelry Box unlocked"
    display_name = "Start with Jewelry Box"

#class ProgressiveVerticalMovement(Toggle):
#    "Always find vertical movement in the following order Succubus Hairpin -> Light Wall -> Celestial Sash"
#    display_name = "Progressive vertical movement"

#class ProgressiveKeycards(Toggle):
#    "Always find Security Keycard's in the following order D -> C -> B -> A"
#    display_name = "Progressive keycards"

class DownloadableItems(DefaultOnToggle):
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
#    "Require gasmask for Maw"
#    display_name = "Stinky Maw"

class GyreArchives(Toggle):
    "Gyre locations are in logic. New warps are gated by Merchant Crow and Kobo"
    display_name = "Gyre Archives"

class Cantoran(Toggle):
    "Cantoran's fight and check are available upon revisiting his room"
    display_name = "Cantoran"

class LoreChecks(Toggle):
    "Memories and journal entries contain items."
    display_name = "Lore Checks"

class DamageRando(Choice):
    "Randomly nerfs and buffs some orbs and their associated spells as well as some associated rings."
    display_name = "Damage Rando"
    option_off = 0
    option_allnerfs = 1
    option_mostlynerfs = 2
    option_balanced = 3
    option_mostlybuffs = 4
    option_allbuffs = 5
    option_manual = 6

class DamageRandoOverrides(OptionDict):
    "Manual +/-/normal odds for each orb. Put 0 if you don't want a certain nerf or buff to be a possibility."
    display_name = "Damage Rando Overrides"
    default = {
        "Blue": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Blade": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Fire": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Plasma": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Iron": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Ice": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Wind": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Gun": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Umbra": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Empire": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Eye": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Blood": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "ForbiddenTome": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Shattered": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Nether": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
        "Radiant": { "MinusOdds": 1, "NormalOdds": 1, "PlusOdds": 1 },
    }

class ShopFill(Choice):
    """Sets the items for sale in Merchant Crow's shops.
    Default: No sunglasses or trendy jacket, but sand vials for sale.
    Randomized: Up to 4 random items in each shop.
    Vanilla: Keep shops the same as the base game.
    Empty: Sell no items at the shop."""
    display_name = "Shop Inventory"
    option_default = 0
    option_randomized = 1
    option_vanilla = 2
    option_empty = 3

class ShopWarpShards(DefaultOnToggle):
    "Shops always sell warp shards (when keys possessed), ignoring inventory setting."
    display_name = "Always Sell Warp Shards"

class ShopMultiplier(Range):
    "Multiplier for the cost of items in the shop. Set to 0 for free shops."
    display_name = "Shop Price Multiplier"
    range_start = 0
    range_end = 10
    default = 1

class LootPool(Choice):
    """Sets the items that drop from enemies (does not apply to boss reward checks)
    Vanilla: Drops are the same as the base game
    Randomized: Each slot of every enemy's drop table is given a random use item or piece of equipment.
    Empty: Enemies drop nothing."""
    display_name = "Loot Pool"
    option_vanilla = 0
    option_randomized = 1
    option_empty = 2

class ShowBestiary(Toggle):
    "All entries in the bestiary are visible, without needing to kill one of a given enemy first"
    display_name = "Show Bestiary Entries"

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
    "DamageRandoOverrides": DamageRandoOverrides,
    "ShopFill": ShopFill,
    "ShopWarpShards": ShopWarpShards,
    "ShopMultiplier": ShopMultiplier,
    "LootPool": LootPool,
    "ShowBestiary": ShowBestiary,
    "DeathLink": DeathLink,
}

def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0

def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value