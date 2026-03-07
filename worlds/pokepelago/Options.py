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
    """Include Generation 1 Pokémon (Kanto, #1–151, 151 Pokémon)."""
    display_name = "Include Kanto"
    default = 1


class IncludeJohto(Toggle):
    """Include Generation 2 Pokémon (Johto, #152–251, +100 Pokémon)."""
    display_name = "Include Johto"
    default = 0


class IncludeHoenn(Toggle):
    """Include Generation 3 Pokémon (Hoenn, #252–386, +135 Pokémon)."""
    display_name = "Include Hoenn"
    default = 0


class IncludeSinnoh(Toggle):
    """Include Generation 4 Pokémon (Sinnoh, #387–493, +107 Pokémon)."""
    display_name = "Include Sinnoh"
    default = 0


class IncludeUnova(Toggle):
    """Include Generation 5 Pokémon (Unova, #494–649, +156 Pokémon)."""
    display_name = "Include Unova"
    default = 0


class IncludeKalos(Toggle):
    """Include Generation 6 Pokémon (Kalos, #650–721, +72 Pokémon)."""
    display_name = "Include Kalos"
    default = 0


class IncludeAlola(Toggle):
    """Include Generation 7 Pokémon (Alola, #722–809, +88 Pokémon)."""
    display_name = "Include Alola"
    default = 0


class IncludeGalar(Toggle):
    """Include Generation 8 Pokémon (Galar, #810–898, +89 Pokémon)."""
    display_name = "Include Galar"
    default = 0


class IncludeHisui(Toggle):
    """Include Hisui-exclusive Pokémon (#899–905, +7 Pokémon). Note: Hisui has no traditional starters."""
    display_name = "Include Hisui"
    default = 0


class IncludePaldea(Toggle):
    """Include Generation 9 Pokémon (Paldea, #906–1025, +120 Pokémon)."""
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
    default = 5


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
        "small_shuffle": 10,
        "big_shuffle":   5,
        "derpy_mon":     25,
        "release":       25,
    }

    @classmethod
    def from_any(cls, data):
        if isinstance(data, dict):
            merged = dict(cls.default)
            merged.update(data)
            return cls(merged)
        return super().from_any(data)


class StarterRegion(Choice):
    """Which game region your adventure starts in.
    Determines which Pokémon starters are available and which Type Keys begin pre-collected.
    'any': a random active region is chosen each seed.
    Specific region: that region must also be active (include_X: true).
    If the chosen region is not active, falls back to a random active region."""
    display_name = "Starter Region"
    option_any    = 0
    option_kanto  = 1
    option_johto  = 2
    option_hoenn  = 3
    option_sinnoh = 4
    option_unova  = 5
    option_kalos  = 6
    option_alola  = 7
    option_galar  = 8
    option_hisui  = 9
    option_paldea = 10
    default = 0


class StarterPokemon(Choice):
    """Which starter Pokémon to begin with in the chosen region.
    'any': a random starter from the region's list is chosen each seed.
    'first'/'second'/'third': by position in the region's list.
    Kanto: first=Bulbasaur, second=Charmander, third=Squirtle.
    Johto: first=Chikorita, second=Cyndaquil, third=Totodile. Etc.
    Regions with no starters (Hisui) are unaffected."""
    display_name = "Starter Pokemon"
    option_any    = 0
    option_first  = 1
    option_second = 2
    option_third  = 3
    default = 0


class LegendaryLocks(Toggle):
    """Gate legendary Pokémon behind Gym Badge items.
    Collect 6 Badges for sub-legendaries (trios, regis, tapus, etc.),
    7 Badges for box legendaries (version mascots), and
    8 Badges for mythics (event-only Pokémon like Mew, Celebi, Arceus).
    8 Gym Badge items are added to the item pool when enabled."""
    display_name = "Legendary Locks"
    default = 0


class TradeLocks(Toggle):
    """Require a Link Cable item before guessing trade-evolved Pokémon
    (Alakazam, Machamp, Golem, Gengar, Scizor, Steelix, Conkeldurr, etc.)."""
    display_name = "Trade Evolution Lock"
    default = 0


class BabyLocks(Toggle):
    """Require Daycare item(s) before guessing baby Pokémon
    (Pichu, Cleffa, Igglybuff, Togepi, Tyrogue, Smoochum, Elekid, Magby, etc.)."""
    display_name = "Baby Pokemon Lock"
    default = 0


class DaycareCount(Range):
    """Number of Daycare items required to unlock baby Pokémon.
    Only used when Baby Pokemon Lock is enabled.
    Set higher for a more gradual unlock; all copies must be received."""
    display_name = "Daycare Items Required"
    range_start = 1
    range_end = 5
    default = 1


class FossilLocks(Toggle):
    """Require a Fossil Restorer item before guessing fossil-revived Pokémon
    (Omanyte, Omastar, Kabuto, Kabutops, Aerodactyl, Lileep, Cranidos, etc.)."""
    display_name = "Fossil Lock"
    default = 0


class UltraBeastLocks(Toggle):
    """Require an Ultra Wormhole item before guessing Ultra Beasts
    (Nihilego through Blacephalon, plus Necrozma which also originates from Ultra Space)."""
    display_name = "Ultra Beast Lock"
    default = 0


class ParadoxLocks(Toggle):
    """Require a Time Rift item before guessing Paradox Pokémon
    (Great Tusk, Roaring Moon, Iron Valiant, etc., plus Koraidon and Miraidon).
    Only relevant when Paldea or Galar/DLC regions are active."""
    display_name = "Paradox Lock"
    default = 0


class StoneLocks(Toggle):
    """Require the matching evolutionary stone item before guessing stone-only evolutions.
    Each stone type that gates at least one active Pokémon adds one stone item to the pool.
    Examples: Fire Stone → Arcanine/Ninetales/Flareon, Water Stone → Starmie/Vaporeon/Cloyster."""
    display_name = "Stone Evolution Lock"
    default = 0


class IncludeShinies(Toggle):
    """Add Shiny Token filler items to the item pool.
    Receiving a Shiny Token makes a random Pokémon in your caught list display
    its shiny sprite. Purely cosmetic — no gameplay effect."""
    display_name = "Include Shiny Tokens"
    default = 0


@dataclass
class PokepelagoOptions(PerGameCommonOptions):
    dexsanity: Dexsanity
    type_locks: EnableTypeLocks
    region_locks: RegionLocks
    starter_region: StarterRegion
    starter_pokemon: StarterPokemon
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
    legendary_locks: LegendaryLocks
    trade_locks: TradeLocks
    baby_locks: BabyLocks
    daycare_count: DaycareCount
    fossil_locks: FossilLocks
    ultra_beast_locks: UltraBeastLocks
    paradox_locks: ParadoxLocks
    stone_locks: StoneLocks
    include_shinies: IncludeShinies
    goal_type: GoalType
    goal_percentage: GoalPercentage
    goal_count: GoalCount
    trap_chance: TrapChance
    trap_weights: TrapWeights
    filler_weights: FillerWeights
