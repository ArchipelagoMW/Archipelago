from dataclasses import dataclass
from Options import PerGameCommonOptions, Toggle, Choice, Range, NamedRange, OptionCounter, OptionSet, OptionGroup
from .data import GAME_REGIONS


class Dexsanity(Toggle):
    """If enabled, each Pokemon has its own location check ('Guess {Pokemon}').
    The location becomes accessible once that Pokemon's region is unlocked (via Region Pass).
    Disabling removes all per-Pokemon locations, leaving only milestone-based filler checks.
    Disabling dramatically reduces item pool size and works well for milestone-only games."""
    display_name = "Dexsanity"
    default = 1


class EnableTypeLocks(Toggle):
    """If true, guessing a Pokemon requires both its specific unlock item and its elemental Type Key."""
    display_name = "Enable Type Locks"
    default = 1


class RegionLocks(Toggle):
    """If enabled, non-starting regions require a Region Pass item to access.
    Disabling this makes all selected regions freely accessible from the start."""
    display_name = "Region Locks"
    default = 1


class StartingLocationCount(Range):
    """Number of free 'Oak\'s Lab' starting locations to include (0-8).
    These are immediately accessible checks (Oak\'s Parcel Delivery, Pokedex Received, etc.)
    that kickstart your adventure. Set to 0 to disable them entirely."""
    display_name = "Starting Location Count"
    range_start = 0
    range_end = 8
    default = 8


class Regions(OptionSet):
    """Which game regions to include. Each region adds its Pokemon to the pool.
    At least one region is always active (defaults to Kanto if empty).
    Valid regions: Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar, Hisui, Paldea."""
    display_name = "Regions"
    valid_keys = frozenset(GAME_REGIONS)
    default = frozenset({"Kanto"})


class RandomRegionCount(NamedRange):
    """Override the Regions option with a random selection.
    Set to 0 (or disabled) to use the manual Regions list.
    Set to 1-10 to randomly pick that many regions.
    Set to random to also randomize how many regions are picked."""
    display_name = "Random Region Count"
    range_start = 0
    range_end = 10
    special_range_names = {"disabled": 0, "random": -1}
    default = 0


class GoalType(Choice):
    """How the goal is defined.
    Percentage: guess a percentage of the selected generation (see 'Goal Percentage').
    Count: guess a fixed number of Pokemon (see 'Goal Count')."""
    display_name = "Goal Type"
    option_percentage = 0
    option_count = 1
    default = 0


class GoalPercentage(Range):
    """Percentage of the selected generation that must be guessed to complete the game.
    Only used when 'Goal Type' is set to 'percentage'.
    For example, 100 means guess every Pokemon in the selected generation."""
    display_name = "Goal Percentage"
    range_start = 1
    range_end = 100
    default = 100


class GoalCount(Range):
    """Fixed number of Pokemon that must be guessed to complete the game.
    Only used when 'Goal Type' is set to 'count'.
    Automatically capped to the total Pokemon available in the selected generation."""
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
    Determines which Pokemon starters are available and which Type Keys begin pre-collected.
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
    """Which starter Pokemon to begin with in the chosen region.
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
    """Gate legendary Pokemon behind Gym Badge items.
    Collect 6 Badges for sub-legendaries (trios, regis, tapus, etc.),
    7 Badges for box legendaries (version mascots), and
    8 Badges for mythics (event-only Pokemon like Mew, Celebi, Arceus).
    8 Gym Badge items are added to the item pool when enabled."""
    display_name = "Legendary Locks"
    default = 0


class TradeLocks(Toggle):
    """Require a Link Cable item before guessing trade-evolved Pokemon
    (Alakazam, Machamp, Golem, Gengar, Scizor, Steelix, Conkeldurr, etc.)."""
    display_name = "Trade Evolution Lock"
    default = 0


class BabyLocks(Toggle):
    """Require Daycare item(s) before guessing baby Pokemon
    (Pichu, Cleffa, Igglybuff, Togepi, Tyrogue, Smoochum, Elekid, Magby, etc.)."""
    display_name = "Baby Pokemon Lock"
    default = 0


class DaycareCount(Range):
    """Number of Daycare items required to unlock baby Pokemon.
    Only used when Baby Pokemon Lock is enabled.
    Set higher for a more gradual unlock; all copies must be received."""
    display_name = "Daycare Items Required"
    range_start = 1
    range_end = 5
    default = 1


class FossilLocks(Toggle):
    """Require a Fossil Restorer item before guessing fossil-revived Pokemon
    (Omanyte, Omastar, Kabuto, Kabutops, Aerodactyl, Lileep, Cranidos, etc.)."""
    display_name = "Fossil Lock"
    default = 0


class UltraBeastLocks(Toggle):
    """Require an Ultra Wormhole item before guessing Ultra Beasts
    (Nihilego through Blacephalon, plus Necrozma which also originates from Ultra Space)."""
    display_name = "Ultra Beast Lock"
    default = 0


class ParadoxLocks(Toggle):
    """Require a Time Rift item before guessing Paradox Pokemon
    (Great Tusk, Roaring Moon, Iron Valiant, etc., plus Koraidon and Miraidon).
    Only relevant when Paldea or Galar/DLC regions are active."""
    display_name = "Paradox Lock"
    default = 0


class StoneLocks(Toggle):
    """Require the matching evolutionary stone item before guessing stone-only evolutions.
    Each stone type that gates at least one active Pokemon adds one stone item to the pool.
    Examples: Fire Stone → Arcanine/Ninetales/Flareon, Water Stone → Starmie/Vaporeon/Cloyster."""
    display_name = "Stone Evolution Lock"
    default = 0


class IncludeShinies(Toggle):
    """Add Shiny Charm filler items to the item pool.
    Receiving a Shiny Charm makes a random Pokemon in your caught list display
    its shiny sprite. Purely cosmetic — no gameplay effect."""
    display_name = "Include Shiny Charms"
    default = 1


@dataclass
class PokepelagoOptions(PerGameCommonOptions):
    dexsanity: Dexsanity
    type_locks: EnableTypeLocks
    region_locks: RegionLocks
    regions: Regions
    random_region_count: RandomRegionCount
    starter_region: StarterRegion
    starter_pokemon: StarterPokemon
    starting_location_count: StartingLocationCount
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


pokepelago_option_groups: list[OptionGroup] = [
    OptionGroup("Regions", [Regions, RandomRegionCount, RegionLocks, StarterRegion, StarterPokemon]),
    OptionGroup("Lock Gates", [EnableTypeLocks, LegendaryLocks, TradeLocks, BabyLocks, DaycareCount,
                               FossilLocks, UltraBeastLocks, ParadoxLocks, StoneLocks], start_collapsed=True),
    OptionGroup("Items", [IncludeShinies, TrapChance, TrapWeights, FillerWeights], start_collapsed=True),
]
