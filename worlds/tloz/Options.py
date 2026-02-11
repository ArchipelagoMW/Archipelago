from dataclasses import dataclass
from Options import DefaultOnToggle, Choice, PerGameCommonOptions, Toggle, ItemSet
from .Items import item_names, default_shop_items


class ExpandedPool(DefaultOnToggle):
    """Puts room clear drops and take any caves into the pool of items and locations."""
    display_name = "Expanded Item Pool"


class TriforceLocations(Choice):
    """Where Triforce fragments can be located. Note that Triforce pieces
    obtained in a dungeon will heal and warp you out, while overworld Triforce pieces obtained will appear to have
    no immediate effect. This is normal."""
    display_name = "Triforce Locations"
    option_vanilla = 0
    option_dungeons = 1
    option_anywhere = 2


class StartingPosition(Choice):
    """How easy is the start of the game.
    Safe means a weapon is guaranteed in Starting Sword Cave.
    Unsafe means that a weapon is guaranteed between Starting Sword Cave, Letter Cave, and Armos Knight.
    Dangerous adds these level locations to the unsafe pool (if they exist):
#       Level 1 Compass, Level 2 Bomb Drop (Keese), Level 3 Key Drop (Zols Entrance), Level 3 Compass
    Very Dangerous is the same as dangerous except it doesn't guarantee a weapon. It will only mean progression
    will be there in single player seeds. In multi worlds, however, this means all bets are off and after checking
    the dangerous spots, you could be stuck until someone sends you a weapon"""
    display_name = "Starting Position"
    option_safe = 0
    option_unsafe = 1
    option_dangerous = 2
    option_very_dangerous = 3

class WeaponLogic(Choice):
    """What level of offensive power is logically required for later dungeons.
    Easy means the Sword will be required for level 1 and later, the White Sword for levels 4 and later,
    and the Magical Sword for levels 6, 8, and 9.
    Moderate means the Swrod for level 1 and later and the White Sword or Magical Rod for levels 4 and later.
    Hard means no safety logic is added. You may be required to defeat enemies with weak or unusual weaponry, such as
    Wizzrobes with the basic Sword or Darknuts with the Magical Rod."""
    display_name = "Weapon Logic"
    option_easy = 0
    option_moderate = 1
    option_hard = 2

class DefenseLogic(Choice):
    """What level of defensive power is logically required for later dungeons.
    Easy means you're guaranteed to have one Heart Container per previous dungeon level plus three additional,
    and the Blue Ring is guaranteed to be available before levels 5 and later.
    Moderate means you're guaranteed to have one extra heart per previous dungeon level,
    taking into account available Rings.
    Hard means no safety logic is added, so all hearts and rings could be in any location."""
    display_name = "Defense Logic"
    option_easy = 0
    option_moderate = 1
    option_hard = 2

class EntranceShuffle(Choice):
    """Shuffle entrances around.
    Dungeons means only dungeon entrances will be shuffled with each other.
    Major means that dungeon entrances and major item locations (sword caves, take any caves, letter cave)
    will be shuffled with each other
    Open means that only dungeon entrances and open caves will be shuffled with each other.
    Major Open is a combination combines and shuffles both Major and Open locations.
    All means all entrances will be shuffled amongst each other.
    Warp Caves will be included as major locations if the Randomize Warp Caves setting is turned on.
    On Open, Major Open, and All, Starting Sword Cave will be in an open location and have a weapon,
    and the Blue Ring Shop will be in an open location.
    """
    display_name = "Entrance Shuffle"
    option_off = 0
    option_dungeons = 1
    option_major = 2
    option_open = 3
    option_major_open = 4
    option_all = 5
    default = 0

class RandomizeWarpCaves(Toggle):
    """Include the Take Any Road caves in entrance randomization"""
    display_name = "Randomize Warp Caves"

class ShopItems(ItemSet):
    """Items that are guarnateed to be in a shop somewhere. If more items than the number of shop slots
    (fourteen) are picked, then a random remainder will be excluded. Small Keys are always included in an open shop.
    All items except Triforce Fragments are valid options."""
    valid_keys = item_names
    default = default_shop_items



@dataclass
class TlozOptions(PerGameCommonOptions):
    ExpandedPool: ExpandedPool
    TriforceLocations: TriforceLocations
    StartingPosition: StartingPosition
    WeaponLogic: WeaponLogic
    DefenseLogic: DefenseLogic
    EntranceShuffle: EntranceShuffle
    RandomizeWarpCaves: RandomizeWarpCaves
    ShopItems: ShopItems


def is_open_cave_shuffled(option_value) -> bool:
    # A couple of things care if Starting Sword Cave is in the shuffle. This centralizes the check for that.
    # This also applies for the Blue Ring Shop.
    check_list = [EntranceShuffle.option_open, EntranceShuffle.option_major_open, EntranceShuffle.option_all]
    return option_value in check_list
