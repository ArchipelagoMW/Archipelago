from typing import Dict, Union
from BaseClasses import MultiWorld
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict

# Will look into feasability of options later.


class StartWithBetterVacuum(Toggle):
    "Start with Poltergust 4000"
    display_name = "Better Vacuum"

# These might end up being the same
class StartHiddenMansion(Toggle):
    "Begin in the Hidden Mansion"
    display_name = "Hidden Mansion"


class MoneyGhosts(Toggle):
    "Adds Blue Ghosts and Gold Mice to location pool"
    display_name = "Money Ghosts"


class StartWithBooRadar(Toggle):
    "Start with Boo Radar"
    display_name = "Boo Radar"

#class DoorRando(Toggle):
#   "Keys wil open different doors than normal, and doors may require elements instead of keys"
#   display_name = "Door Randomization"
# Heavy logic editing required

class Toadsanity(Toggle):
    "Adds Toads to location pool"
    display_name = "Toadsanity"

class Plants(Toggle):
    "Adds all plants to location pool"
    display_name = "Plantsanity"

class Interactables(Toggle):
    "Adds every interactable, such a dressers and light fixtures, to the location pool"
    display_name = "Interactables"

class MarioItems(Range):
    "How many Mario Items it takes to capture the Fortune-Teller. 0 = Starts Capturable"
    display_name = "Fortune-Teller Requirements"
    range_start = 0
    range_end = 5
    default = 5

class WashroomBooCount(Range):
    "Set the number of Boos required to reach the 1F Washroom. 0 = Starts Open"
    display_name = "Washroom Boo Count"
    range_start = 0
    range_end = 50
    default = 5

class BalconyBooCount(Range):
    "Set the number of Boos required to reach the Balcony. 0 = Starts Open"
    display_name = "Washroom Boo Count"
    range_start = 0
    range_end = 50
    default = 20

class FinalBooCount(Range):
    "Set the number of Boos required to reach the Secret Altar. 0 = Starts Open"
    display_name = "Altar Boo Count"
    range_start = 0
    range_end = 50
    default = 40

class Boosanity(Toggle):
    "Turns Boos into Items and Locations"
    display_name = "Boosanity"

class PortraitGhosts(Toggle):
    "Turn Portrait Ghosts into checks in addition to their clear chests"
    display_name = "Portrait Ghosts"

# Old Timespinner Options
class Enemizer(Toggle):
    "Ghosts in room encounters have random elements."
    display_name = "Enemizer"


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


class DropRateCategory(Choice):
    """Sets the drop rate when 'Loot Pool' is set to 'Random'
    Tiered: Based on item rarity/value
    Vanilla: Based on bestiary slot the item is placed into
    Random: Assigned a random tier/drop rate
    Fixed: Set by the 'Fixed Drop Rate' setting
    """
    display_name = "Drop Rate Category"
    option_tiered = 0
    option_vanilla = 1
    option_randomized = 2
    option_fixed = 3


class FixedDropRate(Range):
    "Base drop rate percentage when 'Drop Rate Category' is set to 'Fixed'"
    display_name = "Fixed Drop Rate"
    range_start = 0
    range_end = 100
    default = 5


class LootTierDistro(Choice):
    """Sets how often items of each rarity tier are placed when 'Loot Pool' is set to 'Random'
    Default Weight: Rarer items will be assigned to enemy drop slots less frequently than common items
    Full Random: Any item has an equal chance of being placed in an enemy's drop slot
    Inverted Weight: Rarest items show up the most frequently, while common items are the rarest
    """
    display_name = "Loot Tier Distrubution"
    option_default_weight = 0
    option_full_random = 1
    option_inverted_weight = 2


class ShowBestiary(Toggle):
    "All entries in the bestiary are visible, without needing to kill one of a given enemy first"
    display_name = "Show Bestiary Entries"


class ShowDrops(Toggle):
    "All item drops in the bestiary are visible, without needing an enemy to drop one of a given item first"
    display_name = "Show Bestiary Item Drops"


class EnterSandman(Toggle):
    "The Ancient Pyramid is unlocked by the Twin Pyramid Keys, but the final boss door opens if you have all 5 Timespinner pieces"
    display_name = "Enter Sandman"


# Some options that are available in the timespinner randomizer arent currently implemented
luigimansion_options: Dict[str, Option] = {
    "EyeSpy": EyeSpy,
    "StartWithMeyef": StartWithMeyef,
    "QuickSeed": QuickSeed,
    "SpecificKeycards": SpecificKeycards,
    "Inverted": Inverted,
    "GyreArchives": GyreArchives,
    "Cantoran": Cantoran,
    "LoreChecks": LoreChecks,
    "BossRando": BossRando,
    "BossScaling": BossScaling,
    "FinalBooCount": FinalBooCount,
    "BossHealing": BossHealing,
    "ShopFill": ShopFill,
    "ShopWarpShards": ShopWarpShards,
    "ShopMultiplier": ShopMultiplier,
    "LootPool": LootPool,
    "DropRateCategory": DropRateCategory,
    "FixedDropRate": FixedDropRate,
    "LootTierDistro": LootTierDistro,
    "ShowBestiary": ShowBestiary,
    "ShowDrops": ShowDrops,
    "EnterSandman": EnterSandman,
    "DeathLink": DeathLink,
}


def is_option_enabled(world: MultiWorld, player: int, name: str) -> bool:
    return get_option_value(world, player, name) > 0


def get_option_value(world: MultiWorld, player: int, name: str) -> Union[int, dict]:
    option = getattr(world, name, None)
    if option == None:
        return 0

    return option[player].value
