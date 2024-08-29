# options.py
from dataclasses import dataclass

from Options import Toggle, Range, Choice, PerGameCommonOptions, ItemSet, DefaultOnToggle


class DarkMatterHunt(Toggle):
    """Find the Dark Matter to win."""
    display_name = "Dark Matter Hunt"

class NoFreeCharacters(Toggle):
    display_name = "No Free Characters"

class NoEarnedCharacters(Toggle):
    display_name = "No Earned Characters"

class HeroChallenge(Choice):
    display_name = "Hero Challenge"
    option_none = 0
    option_cecil = 1
    option_kain = 2
    option_rydia = 3
    option_tellah = 4
    option_edward = 5
    option_rosa = 6
    option_yang = 7
    option_palom = 8
    option_porom = 9
    option_cid = 10
    option_edge = 11
    option_fusoya = 12
    option_random_character = 13
    default = 0

class PassEnabled(Toggle):
    display_name = "Pass In Key Item Pool"

class UsefulPercentage(Range):
    display_name = "Useful Item Percentage"
    range_start = 25
    range_end = 100
    default = 35

class UnsafeKeyItemPlacement(Toggle):
    """Normally, underground access is guaranteed to be available without taking a trip to the moon.
    Toggling this on disables this check."""
    display_name = "Unsafe Key Item Placement"

class PassInShops(Toggle):
    """Can the pass show up in shops? This is a convenience feature and will never be required by the logic."""
    display_name = "Enable Pass in Shops"

# Not implemented yet


class AllowedCharacters(ItemSet):
    """Not implemented yet"""
    display_name = "Allowed Characters"
    default = ["Cecil", "Kain", "Rydia", "Tellah", "Edward", "Rosa", "Yang", "Palom", "Porom", "Cid", "Edge", "Fusoya"]

class EnsureAllCharacters(DefaultOnToggle):
    """Not implemented yet"""
    display_name = "Ensure All Characters"

class AllowDuplicateCharacters(DefaultOnToggle):
    """Not implemented yet"""
    display_name = "Allow Duplicate Characters"

class RestrictedCharacters(ItemSet):
    """Not implemented yet"""
    display_name = "Restricted Characters"
    default = ["Edge", "Fusoya"]

class PartySize(Range):
    """Not implemented yet"""
    display_name = "Party Size"
    range_start = 1
    range_end = 5
    default = 5

class CharactersPermajoin(Toggle):
    """Not implemented yet"""
    display_name = "Characters Permanently Join"

class CharactersPermadie(Choice):
    """Not implemented yet"""
    display_name = "Characters Permanently Die"
    option_no = 0
    option_yes = 1
    option_extreme = 2
    default = 0

class MinTier(Range):
    """Not implemented yet"""
    display_name = "Minimum Treasure Tier"
    range_start = 1
    range_end = 5
    default = 1

class MaxTier(Range):
    """Not implemented yet"""
    display_name = "Maximum Treasure Tier"
    range_start = 3
    range_end = 8
    default = 8

class JunkTier(Range):
    """Not implemented yet"""
    display_name = "Junk Tier"
    range_start = 0
    range_end = 8
    default = 1





@dataclass
class FF4FEOptions(PerGameCommonOptions):
    DarkMatterHunt: DarkMatterHunt
    NoFreeCharacters: NoFreeCharacters
    NoEarnedCharacters: NoEarnedCharacters
    HeroChallenge: HeroChallenge
    PassEnabled: PassEnabled
    UsefulPercentage: UsefulPercentage
    UnsafeKeyItemPlacement: UnsafeKeyItemPlacement
    PassInShops: PassInShops
    AllowedCharacters: AllowedCharacters
    EnsureAllCharacters: EnsureAllCharacters
    AllowDuplicateCharacters: AllowDuplicateCharacters
    RestrictedCharacters: RestrictedCharacters
    PartySize: PartySize
    CharactersPermajoin: CharactersPermadie
    CharactersPermadie: CharactersPermadie
    MinTier: MinTier
    MaxTier: MaxTier
    JunkTier: JunkTier
