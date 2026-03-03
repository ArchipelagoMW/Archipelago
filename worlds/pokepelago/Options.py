from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle, Choice, Range, OptionCounter


class Dexsanity(Toggle):
    """If enabled, each Pokemon has its own location check ('Guess {Pokemon}').
    The location becomes accessible once that Pokemon's region is unlocked (via Region Pass).
    Disabling removes all per-Pokemon locations, leaving only milestone-based filler checks.
    Disabling dramatically reduces item pool size and works well for milestone-only games."""
    display_name = "Dexsanity"
    default = 1


class EnableTypeLocks(Toggle):
    """If true, guessing a Pokémon requires both its specific unlock item and its elemental Type Key."""
    display_name = "Enable Type Locks"
    default = 1


class RegionLocks(Toggle):
    """If enabled, non-starting regions require a Region Pass item to access.
    Disabling this makes all selected regions freely accessible from the start."""
    display_name = "Region Locks"
    default = 1


class IncludeStartingLocations(Toggle):
    """If enabled, 8 thematic 'Oak\'s Lab' checks are included as free starting locations
    (Oak\'s Parcel Delivery, Pokedex Received, etc.). Sent to the multiworld when you begin
    your adventure. Disable to remove these checks entirely."""
    display_name = "Include Starting Locations"
    default = 1


class IncludeKanto(Toggle):
    """Include Generation 1 Pokémon (Kanto, #1–151)."""
    display_name = "Include Kanto"
    default = 1


class IncludeJohto(Toggle):
    """Include Generation 2 Pokémon (Johto, #152–251)."""
    display_name = "Include Johto"
    default = 0


class IncludeHoenn(Toggle):
    """Include Generation 3 Pokémon (Hoenn, #252–386)."""
    display_name = "Include Hoenn"
    default = 0


class IncludeSinnoh(Toggle):
    """Include Generation 4 Pokémon (Sinnoh, #387–493)."""
    display_name = "Include Sinnoh"
    default = 0


class IncludeUnova(Toggle):
    """Include Generation 5 Pokémon (Unova, #494–649)."""
    display_name = "Include Unova"
    default = 0


class IncludeKalos(Toggle):
    """Include Generation 6 Pokémon (Kalos, #650–721)."""
    display_name = "Include Kalos"
    default = 0


class IncludeAlola(Toggle):
    """Include Generation 7 Pokémon (Alola, #722–809)."""
    display_name = "Include Alola"
    default = 0


class IncludeGalar(Toggle):
    """Include Generation 8 Pokémon (Galar, #810–898)."""
    display_name = "Include Galar"
    default = 0


class IncludeHisui(Toggle):
    """Include Hisui-exclusive Pokémon (#899–905). Note: Hisui has no traditional starters."""
    display_name = "Include Hisui"
    default = 0


class IncludePaldea(Toggle):
    """Include Generation 9 Pokémon (Paldea, #906–1025)."""
    display_name = "Include Paldea"
    default = 0


# Maps region name to the PokepelagoOptions attribute for that region's toggle
REGION_OPTION_ATTRS = {
    "Kanto": "include_kanto",
    "Johto": "include_johto",
    "Hoenn": "include_hoenn",
    "Sinnoh": "include_sinnoh",
    "Unova": "include_unova",
    "Kalos": "include_kalos",
    "Alola": "include_alola",
    "Galar": "include_galar",
    "Hisui": "include_hisui",
    "Paldea": "include_paldea",
}


class GoalType(Choice):
    """How the goal is defined.
    Percentage: guess a percentage of the selected generation (see 'Goal Percentage').
    Count: guess a fixed number of Pokémon (see 'Goal Count')."""
    display_name = "Goal Type"
    option_percentage = 0
    option_count = 1
    default = 0


class GoalPercentage(Range):
    """Percentage of the selected generation that must be guessed to complete the game.
    Only used when 'Goal Type' is set to 'percentage'.
    For example, 100 means guess every Pokémon in the selected generation."""
    display_name = "Goal Percentage"
    range_start = 1
    range_end = 100
    default = 100


class GoalCount(Range):
    """Fixed number of Pokémon that must be guessed to complete the game.
    Only used when 'Goal Type' is set to 'count'.
    Automatically capped to the total Pokémon available in the selected generation."""
    display_name = "Goal Count"
    range_start = 1
    range_end = 1025
    default = 151


class TrapChance(Range):
    """Percentage chance (0-100) that a filler item slot will be replaced by a trap item.
    0 means no traps; 100 means all filler items will be traps."""
    display_name = "Trap Chance"
    range_start = 0
    range_end = 100
    default = 25


class FillerWeights(OptionCounter):
    """Controls the relative weight of each filler item category.
    Higher values mean that category appears more often. Set a category to 0 to disable it entirely.
    Traps are controlled separately by the 'Trap Chance' option.
    Categories: master_ball, pokeballs, medicine, key_items, splash."""
    display_name = "Filler Item Weights"
    valid_keys = frozenset({"master_ball", "pokeballs", "medicine", "key_items", "splash"})
    default = {
        "master_ball": 50,
        "pokeballs":   150,
        "medicine":    150,
        "key_items":   100,
        "splash":      50,
    }

    @classmethod
    def from_any(cls, data):
        if isinstance(data, dict):
            merged = dict(cls.default)
            merged.update(data)
            return cls(merged)
        return super().from_any(data)


class TrapWeights(OptionCounter):
    """Controls the relative weight of each trap type when a trap slot is filled.
    Higher values mean that trap appears more often. Set a trap to 0 to disable it entirely.
    The overall chance of a trap appearing is controlled by 'Trap Chance'.
    Traps: small_shuffle, big_shuffle, derpy_mon, release."""
    display_name = "Trap Weights"
    valid_keys = frozenset({"small_shuffle", "big_shuffle", "derpy_mon", "release"})
    default = {
        "small_shuffle": 100,
        "big_shuffle":   100,
        "derpy_mon":     100,
        "release":       100,
    }

    @classmethod
    def from_any(cls, data):
        if isinstance(data, dict):
            merged = dict(cls.default)
            merged.update(data)
            return cls(merged)
        return super().from_any(data)


@dataclass
class PokepelagoOptions(PerGameCommonOptions):
    dexsanity: Dexsanity
    type_locks: EnableTypeLocks
    region_locks: RegionLocks
    include_starting_locations: IncludeStartingLocations
    include_kanto: IncludeKanto
    include_johto: IncludeJohto
    include_hoenn: IncludeHoenn
    include_sinnoh: IncludeSinnoh
    include_unova: IncludeUnova
    include_kalos: IncludeKalos
    include_alola: IncludeAlola
    include_galar: IncludeGalar
    include_hisui: IncludeHisui
    include_paldea: IncludePaldea
    goal_type: GoalType
    goal_percentage: GoalPercentage
    goal_count: GoalCount
    trap_chance: TrapChance
    trap_weights: TrapWeights
    filler_weights: FillerWeights
