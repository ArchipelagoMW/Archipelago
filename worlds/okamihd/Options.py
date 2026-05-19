from typing import List, TYPE_CHECKING, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Range, Toggle, Choice, OptionGroup

if TYPE_CHECKING:
    from . import OkamiWorld


def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in okami_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list


class NightTimeChecksRequireCrescent(Toggle):
    """Makes all nighttime checks logically require Crescent.

    Currently included:
    - All buried chests
    - Bakigami
    - Hayabusa"""
    display_name = "Night time checks require crescent"
    default = 1


class ProgressiveWeapons(Toggle):
    """With this option you'll find progressive weapons for each type instead of every weapon being in the item pool."""
    display_name = "Progressive Weapons"
    default = 0


class KarmicTransformers(Choice):
    """Karmic Transformers are Cosmetic items that changes Amaterasu's appearance:

    Excluded: Won't appear
    Precollected: You'll start with them already collected
    In item pool: They will be placed in item pool. You'll start with the Karmic Returner"""
    display_name = "Karmic Transformers Placement"
    option_excluded = 0
    option_precollected = 1
    option_in_item_pool = 2
    default = 1

class OpenGameStart(Toggle):
    """ NOT IMPLEMENTED IN CLIENT YET - USE AT YOUR OWN RISK !!
        Remove some early events for a more open game start:
            - Restoring the river of the Heavens
            - Cutting the peach containing the villagers in Kamiki
            - Restoring Kamiki Village with Sunrise
            - Fixing Kushi's Water Mill
            - Waking Up Susano
            - Saving the Merchant in Kamiki
            - Opening the boulder to Shinshu field
            - Mr. Orange fight after restoring Kamiki Villagers"""
    display_name = "Remove some events for a more open start"
    default = 0


class BloomGuardianSaplings(Toggle):
    """ NOT IMPLEMENTED IN CLIENT YET - USE AT YOUR OWN RISK !!
    Bloom every guardian sapling except Kamiki Village and Hana Valley
    """
    display_name = "Bloom all guardian saplings"
    default = 0


class RemoveBlockHead(Toggle):
    """ NOT IMPLEMENTED IN CLIENT YET - USE AT YOUR OWN RISK !!
    Removes all 3 instances of Blockhead"""
    display_name = "Removes all 3 instances of Blockhead"
    default = 0


class RequiredDoggorbs(Range):
    """Number of Required Canine Warriors/Orbs to open Gale Shrine"""
    display_name = "Number of Required Canine Warriors/Orbs to open Gale Shrine"
    default = 1
    range_start = 1
    range_end = 8


class CanineRewards(Choice):
    """Rewards given by the 8 Canine Warriors checks:

    Vanilla: Won't randomise their quest rewards.
    Randomized: they will give random rewards, Dogs and orbs will be placed in the item pool.
    Junk: They won't give anything useful, Dogs and orbs will be placed in the item pool."""
    display_name = "Rewards given by the 8 Canine Warriors checks"
    option_vanilla = 0
    option_randomized = 1
    option_junk = 2
    default = 1


class MoonCaveAccess(Choice):
    """What does trigger access to moon cave ?

    Serpent Crystal: You need to find the Serpent Crystal item to open Moon cave
    Crimson Helm: You need to defeat Crimson Helm to open moon cave.
    Open: Moon Cave is open from start"""
    display_name = "What does trigger access to moon cave ?"
    option_serpent_crystal = 0
    option_crimson_helm = 1
    option_open = 2
    default = 0


class RandomizeContainers(Toggle):
    """Randomize items found in chests, bloom pods, and other containers."""
    display_name = "Randomize Containers"
    default = 1


class RandomizeShops(Toggle):
    """Randomize items sold in shops. (Not yet implemented)"""
    display_name = "Randomize Shops"
    default = 0


class RandomizeBrushes(Toggle):
    """Randomize brush technique acquisitions from constellations."""
    display_name = "Randomize Brush Techniques"
    default = 1


class ShopSlots(Range):
    """Number of item slots available in each randomized shop."""
    display_name = "Shop Slots"
    range_start = 1
    range_end = 12
    default = 6


#
# class PraiseSanity(Choice):
#    """Randomize Praise Rewards"""
#    display_name = "Randomise Praise Rewards"
#    default = 0
#    options = {
#        "None" :0,
#        "Exclude Animals":1,
#        "Full":2 # 607 Locations, Total of 7724 praise, but you need less to max everything(6020)
#    }
#
#
@dataclass
class OkamiOptions(PerGameCommonOptions):
    RandomizeContainers: RandomizeContainers
    RandomizeShops: RandomizeShops
    RandomizeBrushes: RandomizeBrushes
    ShopSlots: ShopSlots
    NightTimeChecksRequireCrescent: NightTimeChecksRequireCrescent
    KarmicTransformers: KarmicTransformers
    OpenGameStart: OpenGameStart
    ProgressiveWeapons: ProgressiveWeapons
    RemoveBlockHead: RemoveBlockHead
    RequiredDoggorbs: RequiredDoggorbs
    CanineRewards: CanineRewards
    MoonCaveAccess: MoonCaveAccess
    BloomGuardianSaplings: BloomGuardianSaplings


#    PraiseSanity:PraiseSanity


okami_option_groups: Dict[str, List[Any]] = {
    "Randomization": [
        RandomizeContainers,
        RandomizeShops,
        RandomizeBrushes,
        ShopSlots,
    ],
    "General Options": [
        NightTimeChecksRequireCrescent,
        KarmicTransformers,
        OpenGameStart,
        ProgressiveWeapons,
        RemoveBlockHead,
        BloomGuardianSaplings

        # PraiseSanity
    ],
    "Orochi Arc Options": [
        RequiredDoggorbs,
        CanineRewards,
        MoonCaveAccess
    ]

}

slot_data_options = {
    "RandomizeContainers",
    "RandomizeShops",
    "RandomizeBrushes",
    "ShopSlots",
    "NightTimeChecksRequireCrescent",
    "KarmicTransformers",
    "OpenGameStart",
    "ProgressiveWeapons",
    "RemoveBlockHead",
    "RequiredDoggorbs",
    "CanineRewards",
    "MoonCaveAccess",
    "BloomGuardianSaplings"
    #    "PraiseSanity"
}
