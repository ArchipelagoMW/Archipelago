from dataclasses import dataclass

from Options import FreeText, OptionDict, OptionList, Range, Toggle, PerGameCommonOptions


class Locations(OptionList):
    """List of locations chosen by the randomizer to hold key items"""
    display_name = "locations"


class RegionList(OptionDict):
    """List of regions and their locations"""
    display_name = "regions"


class CharLocations(OptionList):
    """Character recruitment locations"""
    display_name = "char locations"


class Items(OptionList):
    """List of key items to be randomized"""
    display_name = "items"


class Rules(OptionDict):
    """Access rules for the chosen locations"""
    display_name = "rules"


class Victory(OptionList):
    """Victory conditions for the chosen game mode"""
    display_name = "victory"


class GameMode(FreeText):
    """Game mode chosen by the user."""
    display_name = "Game Mode"


class ItemDifficulty(FreeText):
    """Game mode chosen by the user."""
    display_name = "Item Difficulty"


class TabTreasures(Toggle):
    """All treasures are replaced with tabs."""
    display_name = "All treasures are tabs"


class BucketFragments(Toggle):
    """Enable the placement of Bucket Fragments."""
    display_name = "Enable Bucket Fragments"


class FragmentCount(Range):
    """Total number of bucket fragments to place"""
    range_start = 0
    range_end = 100
    default = 15
    display_name = "Fragment Count"


class SeedShareLink(FreeText):
    """Game share link from the ctjot web generator"""
    display_name = "Seed Share Link"


@dataclass
class CTJoTOptions(PerGameCommonOptions):
    seed_share_link: SeedShareLink
    game_mode: GameMode
    item_difficulty: ItemDifficulty
    tab_treasures: TabTreasures
    bucket_fragments: BucketFragments
    fragment_count: FragmentCount
    items: Items
    region_list: RegionList
    char_locations: CharLocations
    rules: Rules
    victory: Victory
