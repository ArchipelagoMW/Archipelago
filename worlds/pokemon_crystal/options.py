from dataclasses import dataclass

from Options import Toggle, Choice, DefaultOnToggle, Range, PerGameCommonOptions, NamedRange


class Goal(Choice):
    """
    Elite Four: collect 8 badges and enter the Hall of Fame
    Red: collect 16 badges and defeat Red at Mt. Silver
    """
    display_name = "Goal"
    default = 0
    option_elite_four = 0
    option_red = 1


class JohtoOnly(Choice):
    """
    Excludes all of Kanto, disables early Kanto access
    Forces Goal to Elite Four unless Silver Cave is included
    Goal badges will be limited to 8 if badges are shuffled or vanilla
    """
    display_name = "Johto Only"
    default = 0
    option_off = 0
    option_on = 1
    option_include_silver_cave = 2


class EliteFourBadges(Range):
    """
    Number of badges required to enter Victory Road
    """
    display_name = "Elite Four Badges"
    default = 8
    range_start = 1
    range_end = 16


class RedBadges(Range):
    """
    Number of badges required to open Silver Cave
    """
    display_name = "Red Badges"
    default = 16
    range_start = 1
    range_end = 16


class RandomizeBadges(Choice):
    """
    Shuffles gym badge locations into the pool
    Vanilla: Does not randomize gym badges
    Shuffle: Randomizes gym badges between gym leaders
    Completely Random: Randomizes badges with all other items
    """
    display_name = "Randomize Badges"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class RandomizeHiddenItems(Toggle):
    """
    Shuffles hidden item locations into the pool
    """
    display_name = "Randomize Hidden Items"


class RequireItemfinder(DefaultOnToggle):
    """
    Hidden items require Itemfinder in logic
    """
    display_name = "Require Itemfinder"


class Trainersanity(Toggle):
    """
    Adds checks for defeating trainers
    """
    display_name = "Trainersanity"


class TrainersanityAlerts(Choice):
    """
    Shows a message box or plays a sound for Trainersanity checks
    """
    display_name = "Trainersanity Alerts"
    default = 1
    option_no_alerts = 0
    option_message_box = 1
    option_sound_only = 2


class RandomizePokegear(Toggle):
    """
    Shuffles the Pokegear and cards into the pool
    """
    display_name = "Randomize Pokegear"


class RandomizeBerryTrees(Toggle):
    """
    Shuffles berry tree locations into the pool
    """
    display_name = "Randomize Berry Trees"


class RandomizeStarters(Choice):
    """
    Randomizes species of starter Pokemon
    """
    display_name = "Randomize Starters"
    default = 0
    option_vanilla = 0
    option_unevolved_only = 1
    option_completely_random = 2


class RandomizeWilds(Toggle):
    """
    Randomizes species of wild Pokemon
    """
    display_name = "Randomize Wilds"


class NormalizeEncounterRates(Toggle):
    """
    Normalizes the chance of encountering each wild Pokemon in a given area
    """
    display_name = "Normalize Encounter Rates"


class RandomizeStaticPokemon(Toggle):
    """
    Randomizes species of static Pokemon encounters
    """
    display_name = "Randomize Static Pokemon"


class RandomizeTrainerParties(Choice):
    """
    Randomizes Pokemon in enemy trainer parties
    """
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_completely_random = 2


class RandomizeLearnsets(Choice):
    """
    Vanilla: Vanilla movesets
    Randomize: Random movesets
    Start With Four Moves: Random movesets with 4 starting moves
    """
    display_name = "Randomize Learnsets"
    default = 0
    option_vanilla = 0
    option_randomize = 1
    option_start_with_four_moves = 2


class RandomizeTMMoves(Toggle):
    """
    Randomizes the moves available as TMs
    """
    display_name = "Randomize TM Moves"


class TMCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with a TM
    """
    display_name = "TM Compatibility"
    default = 0
    range_start = 1
    range_end = 100
    special_range_names = {
        "vanilla": 0,
        "fully_compatible": 100
    }


class HMCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with a HM
    """
    display_name = "HM Compatibility"
    default = 0
    range_start = 1
    range_end = 100
    special_range_names = {
        "vanilla": 0,
        "fully_compatible": 100
    }


class RandomizeBaseStats(Choice):
    """
    Vanilla: Vanilla base stats
    Keep BST: Random base stats, but base stat total is preserved
    Completely Random: Base stats and BST are completely random
    """
    display_name = "Randomize Base Stats"
    default = 0
    option_vanilla = 0
    option_keep_bst = 1
    option_completely_random = 2


class RandomizeTypes(Choice):
    """
    Vanilla: Vanilla Pokemon types
    Follow Evolutions: Types are randomized but preserved when evolved
    Completely Random: Types are completely random
    """
    display_name = "Randomize Types"
    default = 0
    option_vanilla = 0
    option_follow_evolutions = 1
    option_completely_random = 2


class RandomizePalettes(Choice):
    """
    Vanilla: Vanilla Pokemon color palettes
    Match Types: Color palettes match Pokemon Type
    Completely Random: Color palettes are completely random
    """
    display_name = "Randomize Palettes"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_completely_random = 2


class RandomizeMusic(Toggle):
    """
    Randomize all music
    """
    display_name = "Randomize Music"


# class RandomizeSFX(Toggle):
#     """
#     Randomize all sound effects
#     """
#     display_name = "Randomize SFX"
#     default = 0


class FreeFlyLocation(Choice):
    """
    If enabled, unlocks a random fly location for free
    If Free Fly And Map Card is selected, an extra fly location
    is unlocked when the Pokegear and Map Card are obtained
    """
    display_name = "Free Fly Location"
    default = 0
    option_off = 0
    option_free_fly = 1
    option_free_fly_and_map_card = 2


class EarlyFly(Toggle):
    """
    HM02 Fly will be placed early in the game
    """
    display_name = "Early Fly"


class HMBadgeRequirements(Choice):
    """
    Vanilla: HMs require their vanilla badges
    No Badges: HMs do not require a badge to use
    Add Kanto: HMs can be used with the Johto or Kanto badge
    """
    display_name = "HM Badge Requirements"
    default = 0
    option_vanilla = 0
    option_no_badges = 1
    option_add_kanto = 2


class ReusableTMs(Toggle):
    """
    TMs can be used an infinite number of times
    """
    display_name = "Reusable TMs"


class GuaranteedCatch(Toggle):
    """
    Balls have a 100% success rate
    """
    display_name = "Guaranteed Catch"


class MinimumCatchRate(Range):
    """
    Sets a minimum catch rate for wild Pokemon
    """
    display_name = "Minimum Catch Rate"
    default = 0
    range_start = 0
    range_end = 255


class BlindTrainers(Toggle):
    """
    Trainers have no vision and will not start battles unless interacted with
    """
    display_name = "Blind Trainers"


class BetterMarts(Toggle):
    """
    Improves the selection of items at Pokemarts
    """
    display_name = "Better Marts"


class ExpModifier(Range):
    """
    Scale the amount of Experience Points given in battle
    Default is 20, for double set to 40, for half set to 10, etc
    """
    display_name = "Experience Modifier"
    default = 20
    range_start = 1
    range_end = 255


class PhoneTrapWeight(Range):
    """
    Adds random Pokegear calls that acts as traps
    Weight is a percentage of filler items to replace
    """
    display_name = "Phone Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class SleepTrapWeight(Range):
    """
    Trap that causes Sleep status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Sleep Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class PoisonTrapWeight(Range):
    """
    Trap that causes Poison status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Poison Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class BurnTrapWeight(Range):
    """
    Trap that causes Burn status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Burn Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class FreezeTrapWeight(Range):
    """
    Trap that causes Freeze status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Freeze Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class ParalysisTrapWeight(Range):
    """
    Trap that causes Paralysis status on your party
    Weight is a percentage of filler items to replace
    """
    display_name = "Paralysis Trap Weight"
    default = 0
    range_start = 0
    range_end = 8


class ItemReceiveSound(DefaultOnToggle):
    """
    Play item received sound on receiving a remote item
    """
    display_name = "Item Receive Sound"


class EnableMischief(Toggle):
    """
    If I told you what this does, it would ruin the surprises :)
    """
    display_name = "Enable Mischief"


@dataclass
class PokemonCrystalOptions(PerGameCommonOptions):
    goal: Goal
    johto_only: JohtoOnly
    elite_four_badges: EliteFourBadges
    red_badges: RedBadges
    randomize_badges: RandomizeBadges
    randomize_hidden_items: RandomizeHiddenItems
    require_itemfinder: RequireItemfinder
    trainersanity: Trainersanity
    trainersanity_alerts: TrainersanityAlerts
    randomize_pokegear: RandomizePokegear
    randomize_berry_trees: RandomizeBerryTrees
    randomize_starters: RandomizeStarters
    randomize_wilds: RandomizeWilds
    normalize_encounter_rates: NormalizeEncounterRates
    randomize_static_pokemon: RandomizeStaticPokemon
    randomize_trainer_parties: RandomizeTrainerParties
    randomize_learnsets: RandomizeLearnsets
    randomize_tm_moves: RandomizeTMMoves
    tm_compatibility: TMCompatibility
    hm_compatibility: HMCompatibility
    randomize_base_stats: RandomizeBaseStats
    randomize_types: RandomizeTypes
    randomize_palettes: RandomizePalettes
    randomize_music: RandomizeMusic
    # randomize_sfx: RandomizeSFX
    free_fly_location: FreeFlyLocation
    early_fly: EarlyFly
    hm_badge_requirements: HMBadgeRequirements
    reusable_tms: ReusableTMs
    guaranteed_catch: GuaranteedCatch
    minimum_catch_rate: MinimumCatchRate
    blind_trainers: BlindTrainers
    better_marts: BetterMarts
    experience_modifier: ExpModifier
    phone_trap_weight: PhoneTrapWeight
    sleep_trap_weight: SleepTrapWeight
    poison_trap_weight: PoisonTrapWeight
    burn_trap_weight: BurnTrapWeight
    freeze_trap_weight: FreezeTrapWeight
    paralysis_trap_weight: ParalysisTrapWeight
    item_receive_sound: ItemReceiveSound
    enable_mischief: EnableMischief
