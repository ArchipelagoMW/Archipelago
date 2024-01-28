from Options import Toggle, Choice, DefaultOnToggle, Range, PerGameCommonOptions
from dataclasses import dataclass


class Goal(Choice):
    """Elite Four: collect 8 badges and enter the Hall of Fame
        Red: collect 16 badges and defeat Red at Mt. Silver"""
    display_name = "Goal"
    default = 0
    option_elite_four = 0
    option_red = 1


class RandomizeHiddenItems(Toggle):
    """Shuffles hidden items into the pool"""
    display_name = "Randomize Hidden Items"
    default = 0


class RequireItemfinder(DefaultOnToggle):
    """Hidden items require Itemfinder in logic"""
    display_name = "Require Itemfinder"


class RandomizeStarters(Toggle):
    """Randomizes species of starter Pokemon"""
    display_name = "Randomize Starters"
    default = 0


class RandomizeWilds(Toggle):
    """Randomizes species of wild Pokemon"""
    display_name = "Randomize Wilds"
    default = 0


class NormalizeEncounterRates(Toggle):
    """Normalizes chance of encountering each wild Pokemon slot"""
    display_name = "Normalize Encounter Rates"
    default = 0


class RandomizeStaticPokemon(Toggle):
    """Randomizes species of static Pokemon encounters"""
    display_name = "Randomize Static Pokemon"


class RandomizeTrainerParties(Choice):
    """Randomizes Pokemon in emey trainer parties"""
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_completely_random = 2


class RandomizeLearnsets(Choice):
    """start_with_four_moves: Random movesets with 4 starting moves
    randomize: Random movesets
    vanilla: Vanilla movesets"""
    display_name = "Randomize Learnsets"
    default = 0
    option_vanilla = 0
    option_randomize = 1
    option_start_with_four_moves = 2


class FullTmHmCompatibility(Toggle):
    """All Pokemon can learn any TM/HM"""
    display_name = "Full TM/HM Compatibility"
    default = 0


class ReusableTMs(Toggle):
    """TMs can be used an infinite number of times"""
    display_name = "Reusable TMs"
    default = 0


class GuaranteedCatch(Toggle):
    """Balls have a 100% success rate"""
    display_name = "Guaranteed Catch"
    default = 0


class MinimumCatchRate(Range):
    """Sets a minimum catch rate for wild Pokemon"""
    display_name = "Minimum Catch Rate"
    default = 0
    range_start = 0
    range_end = 255


class BlindTrainers(Toggle):
    """Trainers have no vision and will not start battles unless interacted with"""
    display_name = "Blind Trainers"
    default = 0


class BetterMarts(Toggle):
    """Improves the selection of items at Pokemarts"""
    display_name = "Better Marts"
    default = 0


class ExpModifier(Range):
    """Scale the amount of Experience Points given in battle.
    Default is 20, for double set to 40, for half set to 10, etc.
    Must be between 1 and 255"""
    display_name = "Experience Modifier"
    default = 20
    range_start = 1
    range_end = 255


class ItemReceiveSound(DefaultOnToggle):
    """Play item received sound on receiving a remote item"""
    display_name = "Item Receive Sound"


@dataclass
class PokemonCrystalOptions(PerGameCommonOptions):
    goal: Goal
    randomize_hidden_items: RandomizeHiddenItems
    require_itemfinder: RequireItemfinder
    randomize_starters: RandomizeStarters
    randomize_wilds: RandomizeWilds
    normalize_encounter_rates: NormalizeEncounterRates
    randomize_static_pokemon: RandomizeStaticPokemon
    randomize_trainer_parties: RandomizeTrainerParties
    randomize_learnsets: RandomizeLearnsets
    full_tmhm_compatibility: FullTmHmCompatibility
    reusable_tms: ReusableTMs
    guaranteed_catch: GuaranteedCatch
    minimum_catch_rate: MinimumCatchRate
    blind_trainers: BlindTrainers
    better_marts: BetterMarts
    experience_modifier: ExpModifier
    item_receive_sound: ItemReceiveSound
