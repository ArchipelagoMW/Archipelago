from dataclasses import dataclass

from .Items import item_groups
from .data.Trivia import trivia_data

from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, OptionList, OptionDict, PerGameCommonOptions, StartInventoryPool, DeathLink, Visibility, FreeText
from schema import Schema, Optional

from .Aesthetics import palette_set_offsets

class StartingLifeCount(Range):
    """
    How many lives to start the game with. 
    """
    display_name = "Starting Life Count"
    range_start = 0
    range_end = 99
    default = 15

class StartingKong(Choice):
    """
    Which Kongs will be available at the start
    """
    display_name = "Starting Kong"
    option_diddy = 1
    option_dixie = 2
    option_both = 3
    default = 3

class Logic(Choice):
    """
    Logic difficulty. May become irrelevant if not a lot of items are added to the item pool.
    - **Strict**: Ensures everything is reachable as the original devs intended. For beginners or people who want to go out of logic with some tricks.
    - **Loose**: Reaching locations may require some level of mastery about the game's mechanics.
    - **Expert**: Locations expects players to be extremely good at the game with minimal amount of abilities. Hard to go out of logic.
    """
    display_name = "Logic Difficulty"
    option_strict = 0
    option_loose = 1
    option_expert = 2
    default = 0

class RequiredGalleonLevels(Range):
    """
    How many levels in Gangplank Galleon need to be cleared to fight the area boss
    """
    display_name = "Galleon Levels Required"
    range_start = 0
    range_end = 5
    default = 4

class RequiredCauldronLevels(Range):
    """
    How many levels in Crocodile Cauldron need to be cleared to fight the area boss
    """
    display_name = "Cauldron Levels Required"
    range_start = 0
    range_end = 5
    default = 4

class RequiredQuayLevels(Range):
    """
    How many levels in Krem Quay need to be cleared to fight the area boss
    """
    display_name = "Quay Levels Required"
    range_start = 0
    range_end = 6
    default = 4

class RequiredKremlandLevels(Range):
    """
    How many levels in Krazy Kremland need to be cleared to fight the area boss
    """
    display_name = "Kremland Levels Required"
    range_start = 0
    range_end = 6
    default = 4

class RequiredGulchLevels(Range):
    """
    How many levels in Gloomy Gulch need to be cleared to fight the area boss
    """
    display_name = "Gulch Levels Required"
    range_start = 0
    range_end = 5
    default = 4

class RequiredKeepLevels(Range):
    """
    How many levels in K. Rool's Keep need to be cleared to fight the area boss
    """
    display_name = "Keep Levels Required"
    range_start = 0
    range_end = 6
    default = 4

class RequiredKrockLevels(Range):
    """
    How many levels in The Flying Krock need to be cleared to fight the area boss
    """
    display_name = "Krock Levels Required"
    range_start = 0
    range_end = 1
    default = 1

class ShuffleLevels(Toggle):
    """
    Shuffles levels and bosses around
    """
    display_name = "Shuffle Levels"

class Goal(Choice):
    """
    Which goal will be used to mark the game as completed
    - **Flying Krock:** Duel with K. Rool at the Flying Krock
    - **Lost World:** Duel with K. Rool at Lost World
    - **Kompletionist:** Duel with K. Rool at both Flying Krock and Lost World
    """
    display_name = "Goal"
    option_flying_krock = 1
    option_lost_world = 2
    option_kompletionist = 3
    default = 1

class FlyingKrockTokens(Range):
    """
    How many Boss Tokens are required to access the Flying Krock.

    If this value is set to 0, then the access will be a multiworld item.
    """
    display_name = "Flying Krock Tokens"
    range_start = 0
    range_end = 5
    default = 5

class LostWorldRocks(Range):
    """
    How many rocks are required to be found to be able to duel K. Rool at Lost World's Kore
    """
    display_name = "Lost World Rocks"
    range_start = 1
    range_end = 10
    default = 5

class ExtraLostWorldRocks(Range):
    """
    How many additional Lost World Rocks can be found in the multiworld
    """
    display_name = "Extra Lost World Rocks"
    range_start = 0
    range_end = 5
    default = 3

class LostWorldRockPlacement(Choice):
    """
    Determines how Lost World Rocks will be placed in the multiworld
    - **anywhere**: Placed anywhere in the multiworld
    - **lost_world_level_clear**: Forced in Level Clears found in Lost World
      This option always creates 5 rocks. Extra lost world rocks aren't created.
    - **lost_world_anywhere**: Forced in anywhere in Lost World

    These options listens to Excluded Locations, it won't force you to deal with levels you don't want to deal with.
    However, if it can place an item due to excluded locations AP will place them anywhere in the multiworld.
    """
    display_name = "Lost World Rock Behavior"
    option_anywhere = 0
    option_lost_world_level_clear = 1
    option_lost_world_anywhere = 2
    default = 1

class AbilityShuffle(OptionSet):
    """
    Which abilities will be added as items in the item pool
    If an ability is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Ability Shuffle"
    default = {ability for ability in item_groups["Abilities"]}
    valid_keys = {ability for ability in item_groups["Abilities"]}

class AnimalShuffle(OptionSet):
    """
    Which animal buddies will be added as items in the item pool
    If an animal buddy is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Animal Buddies Shuffle"
    default = {ability for ability in item_groups["Animals"]}
    valid_keys = {ability for ability in item_groups["Animals"]}

class BarrelShuffle(OptionSet):
    """
    Which kind of barrels will be added as items in the item pool
    If a barrel is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Barrel Kannons Shuffle"
    default = {ability for ability in item_groups["Barrels"]}
    valid_keys = {ability for ability in item_groups["Barrels"]}

class KONGChecks(DefaultOnToggle):
    """
    Whether collecting all KONG letters in each level will grant a check
    """
    display_name = "KONG Letters Checks"

class DKCoinChecks(DefaultOnToggle):
    """
    Whether collecting a DK Coin in each level will grant a check
    """
    display_name = "DK Coin Checks"

class BalloonChecks(Toggle):
    """
    Whether collecting a colored balloon in levels will grant a check

    Doesn't include balloons from the goal or Black Klobbers
    """
    display_name = "Balloonsanity"
    
class CoinChecks(Toggle):
    """
    Whether collecting a banana coin in levels will grant a check

    Doesn't include banana coins from the goal
    """
    display_name = "Coinsanity"
    
class BunchChecks(Toggle):
    """
    Whether collecting a banana bunch in levels will grant a check

    Doesn't include banana bunches from the goal, Yellow Klobbers or Rickety Race
    """
    display_name = "Bananasanity"
    
class SwankyChecks(DefaultOnToggle):
    """
    Whether completing a quiz will grant a check
    """
    display_name = "Swanky Quiz Checks"

class SwankyQuestionsPerQuiz(Range):
    """
    Whether completing a quiz will grant a check
    """
    display_name = "Swanky Questions Per Quiz"
    range_start = 1
    range_end = 6
    default = 1

class SwankyExcludeTopics(OptionList):
    """
    Which topics will be excluded from Swanky's Bonus Bonanza pool of questions.

    Swanky enforces questions from the multiworld. This will help you to remove topics from games you don't know/care about in the session.
    Donkey Kong Country 2 can't be excluded (can be put here, but it'll be forced anyway)

    Do note that if you remove way too many topics and set a very high question per quiz count an error may arise from the lack of questions available
    """
    display_name = "Swanky Excluded Topics"
    default = sorted([topic for topic in trivia_data.keys()])
    valid_keys = sorted([topic for topic in trivia_data.keys()])

class SwankyForceTopics(OptionList):
    """
    Which additional topics will be added to Swanky's Bonus Bonanza pool of questions.

    Swanky already enforces questions from games in the multiworld if they're on the database.

    This option has priority over the Excluded Topics option.
    """
    display_name = "Swanky Forced Topics"
    default = sorted([topic for topic in trivia_data.keys()])
    valid_keys = sorted([topic for topic in trivia_data.keys()])

class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0

class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2

class FreezeTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which freezes the controllable kong
    """
    display_name = "Freeze Trap Weight"

class ReverseTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which reverses the player's controls
    """
    display_name = "Reverse Trap Weight"

class HoneyTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which makes the floor (temporarily) sticky
    """
    display_name = "Honey Trap Weight"

class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which makes the level slightly slippery
    """
    display_name = "Ice Trap Weight"

class TNTBarrelTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which spawns an active TNT barrel above the player
    """
    display_name = "TNT Barrel Trap Weight"

class DamageTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which damages the player
    """
    display_name = "Damage Trap Weight"
    visibility = Visibility.spoiler
    default = 0

class InstaDeathTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which instantly kills the player
    """
    display_name = "Instant Death Trap Weight"
    visibility = Visibility.spoiler
    default = 0

class BaseDiddyPalette(Choice):
    """
    Base class for palettes
    """
    option_original = 0
    option_original_inactive = 1
    option_original_invincible = 2
    option_original_frozen = 3
    option_original_reversed = 4
    option_original_slow = 5
    option_original_team_2 = 6
    option_original_team_2_inactive = 7
    option_dkc_alt = 8
    option_dkc3_kiddy = 9
    option_dkc3_kiddy_alt = 10
    option_gb_green = 11
    option_gb_gray = 12
    option_gbc_retro_blast = 13
    option_golden = 14
    option_monochrome = 15
    option_sepia = 16
    option_smb_mario = 17
    option_smb_luigi = 18
    option_toothpaste = 19
    option_whatsapp = 20
    option_bubblegum = 21
    option_retro_frozen = 22
    option_retro_reversed = 23
    option_retro_slow = 24
    option_rottytops = 25

class BaseDixiePalette(Choice):
    """
    Base class for palettes
    """
    option_original = 0
    option_original_inactive = 1
    option_original_invincible = 2
    option_original_frozen = 3
    option_original_reversed = 4
    option_original_slow = 5
    option_original_team_2 = 6
    option_original_team_2_inactive = 7
    option_dkc2_inverted = 8
    option_dkc2_team_2_inverted = 9
    option_dkc3_alt = 10
    option_dkc3_alt_inverted = 11
    option_gb_green = 12
    option_gb_grey = 13
    option_gbc_retro_blast = 14
    option_gba_blue = 15
    option_gba_green = 16
    option_smb_mario = 17
    option_smb_luigi = 18
    option_golden = 19
    option_monochrome = 20
    option_sepia = 21
    option_rottytops = 22
    option_miku = 23
    option_teto = 24
    option_sakura = 25
    option_nagisa = 26
    option_gothic = 27
    option_toothpaste = 28
    option_whatsapp = 29
    option_boca = 30
    option_bubblegum = 31
    option_retro_frozen = 32
    option_retro_reversed = 33
    option_retro_slow = 34

class DiddyActive(BaseDiddyPalette):
    """
    Which color to use for Diddy's active color
    """
    display_name = "Diddy Active Palette"
    default = 0

class DiddyInactive(BaseDiddyPalette):
    """
    Which color to use for Diddy's inactive color
    """
    display_name = "Diddy Inactive Palette"
    default = 1

class DiddyInvincible(BaseDiddyPalette):
    """
    Which color to use for Diddy's invincible color
    """
    display_name = "Diddy Invincible Palette"
    default = 2

class DiddyFrozen(BaseDiddyPalette):
    """
    Which color to use for Diddy's frozen color
    """
    display_name = "Diddy Frozen Palette"
    default = 3

class DiddyReversed(BaseDiddyPalette):
    """
    Which color to use for Diddy's reversed color
    """
    display_name = "Diddy Reversed Palette"
    default = 4

class DiddySlow(BaseDiddyPalette):
    """
    Which color to use for Diddy's slow color
    """
    display_name = "Diddy Slow Palette"
    default = 5

class DixieActive(BaseDixiePalette):
    """
    Which color to use for Dixie's active color
    """
    display_name = "Dixie Active Palette"
    default = 0

class DixieInactive(BaseDixiePalette):
    """
    Which color to use for Dixie's inactive color
    """
    display_name = "Dixie Inactive Palette"
    default = 1

class DixieInvincible(BaseDixiePalette):
    """
    Which color to use for Dixie's invincible color
    """
    display_name = "Dixie Invincible Palette"
    default = 2

class DixieFrozen(BaseDixiePalette):
    """
    Which color to use for Dixie's frozen color
    """
    display_name = "Dixie Frozen Palette"
    default = 3

class DixieReversed(BaseDixiePalette):
    """
    Which color to use for Dixie's reversed color
    """
    display_name = "Dixie Reversed Palette"
    default = 4

class DixieSlow(BaseDixiePalette):
    """
    Which color to use for Dixie's slow color
    """
    display_name = "Dixie Slow Palette"
    default = 5

class RambiPalette(Choice):
    """
    Which color to use for Rambi
    """
    display_name = "Rambi Palette"
    default = 0
    option_original = 0
    option_gray = 1
    option_blue = 2
    option_green = 3
    option_red = 4
    option_dkc2_frozen = 5
    option_dkc2_reversed = 6
    option_dkc2_slow = 7
    option_golden = 8
    option_pink = 9
    option_whatsapp = 10

class EnguardePalette(Choice):
    """
    Which color to use for Enguarde
    """
    display_name = "Enguarde Palette"
    default = 0
    option_original = 0
    option_red = 1
    option_purple = 2
    option_silver = 3
    option_blue_white_belly = 4
    option_golden = 5
    option_dkc2_frozen = 6
    option_dkc2_reversed = 7
    option_whatsapp = 8
    option_black = 9

class SquitterPalette(Choice):
    """
    Which color to use for Squitter
    """
    display_name = "Squitter Palette"
    default = 0
    option_original = 0
    option_blue = 1
    option_green = 2
    option_pink = 3
    option_aqua = 4
    option_purple = 5
    option_gray = 6
    option_golden = 7
    option_dkc2_frozen = 8
    option_dkc2_reversed = 9
    option_whatsapp = 10

class RattlyPalette(Choice):
    """
    Which color to use for Rattly
    """
    display_name = "Rattly Palette"
    default = 0
    option_original = 0
    option_black = 1
    option_blue = 2
    option_white = 3
    option_golden = 4
    option_dkc2_frozen = 5
    option_dkc2_reversed = 6
    option_whatsapp = 7

class SquawksPalette(Choice):
    """
    Which color to use for Squawks
    """
    display_name = "Squawks Palette"
    default = 0
    option_original = 0
    option_quawks = 1
    option_red = 2
    option_blue = 3
    option_black = 4
    option_white = 5
    option_purple = 6
    option_dkc2_reversed = 7
    option_dkc2_frozen = 8
    option_whatsapp = 9
    option_golden = 10

class QuawksPalette(Choice):
    """
    Which color to use for Quawks
    """
    display_name = "Quawks Palette"
    default = 0
    option_original = 0
    option_squawks = 1
    option_red = 2
    option_blue = 3
    option_black = 4
    option_white = 5
    option_purple = 6
    option_dkc2_reversed = 7
    option_dkc2_frozen = 8
    option_whatsapp = 9
    option_golden = 10

class PaletteFilter(OptionDict):
    """
    Applies a filter that can brighten or darken your selected palette
    Doesn't produce results similar to the original ones, but it's good enough
    
    Positive numbers create a brighter color palette (the higher the number, the brighter the palette)
    Negative numbers create a darker color palette (the higher (or lower lol) the negative number, the darker the palette)
    
    Treat the values as percentages
    """
    display_name = "Palette Filters"
    schema = Schema({
        Optional(color_set): int for color_set in palette_set_offsets.keys()
    })
    default = {color_set: 0 for color_set in palette_set_offsets.keys()}


class SetPalettes(OptionDict):
    """
    Allows you to create colors for each Kong status and Animal Buddies.
    This will override the option preset
    
    Each one expects 15 values which are mapped to the Kongs colors
    The values can be in SNES RGB (bgr555) with the $ prefix or PC RGB (rgb888) with the # prefix
    """
    display_name = "Set Custom Palettes"
    schema = Schema({
        Optional(color_set): list for color_set in palette_set_offsets.keys()
    })
    default = {}


class EnergyLink(Toggle):
    """
    EnergyLink allows players to deposit energy extracted from collected bananas into a shared pool across games in the session.

    You can exchange energy for Instant DK Barrels. Great for players that find the base game hard.
    There's an additional item in the item pool that allows for better energy extraction from bananas.
    """
    display_name = "Energy Link"


class TrapLink(Toggle):
    """
    Whether your received traps are linked to other players
    """
    display_name = "Trap Link"


class DisplayMessages(Choice):
    """
    The game may summon a pop up message on items sent and received
    Messages are considerably delayed from the actual effect, you actually receive and send items quite fast

    This feature is highly experimental, use it if you don't mind some visual bugs under certain scenarios,
    mainly during lag frames and pausing in certain moments
    """
    display_name = "Message Display"
    option_off = 0
    option_on_only_sent = 1
    option_on_only_received = 2
    option_on_everything = 3
    default = 3

class ReceivedMessageFilter(OptionList):
    """
    Applies an item classification filter on RECEIVED items

    Only the items with the classifications listed below will be included
    """
    display_name = "Received Message Filter"
    valid_keys = [
        "Progression",
        "Useful",
        "Filler",
        "Trap",
    ]
    default = valid_keys

class SentMessageFilter(OptionList):
    """
    Applies an item classification filter on SENT items

    Only the items with the classifications listed below will be included
    """
    display_name = "Sent Message Filter"
    valid_keys = [
        "Progression",
        "Useful",
        "Filler",
        "Trap",
    ]
    default = valid_keys

dkc2_option_groups = [
    OptionGroup("Goal", [
        Goal,
        FlyingKrockTokens,
        RequiredGalleonLevels,
        RequiredCauldronLevels,
        RequiredQuayLevels,
        RequiredKremlandLevels,
        RequiredGulchLevels,
        RequiredKeepLevels,
        RequiredKrockLevels,
        LostWorldRocks,
        ExtraLostWorldRocks,
        LostWorldRockPlacement,
    ]),
    OptionGroup("Locations", [
        Logic,
        KONGChecks,
        DKCoinChecks,
        BalloonChecks,
        CoinChecks,
        BunchChecks,
        SwankyChecks,
    ]),
    OptionGroup("Shuffle", [
        StartingKong,
        ShuffleLevels,
        AbilityShuffle,
        AnimalShuffle,
        BarrelShuffle,
    ]),
    OptionGroup("Trivia", [
        SwankyQuestionsPerQuiz,
        SwankyForceTopics,
        SwankyExcludeTopics,
    ]),
    OptionGroup("Traps", [
        TrapFillPercentage,
        FreezeTrapWeight,
        ReverseTrapWeight,
        HoneyTrapWeight,
        IceTrapWeight,
        TNTBarrelTrapWeight,
        DamageTrapWeight,
        InstaDeathTrapWeight,
    ]),
    OptionGroup("Aesthetics", [
        SetPalettes,
        PaletteFilter,
        DiddyActive,
        DiddyInactive,
        DiddyInvincible,
        DiddyFrozen,
        DiddyReversed,
        DiddySlow,
        DixieActive,
        DixieInactive,
        DixieInvincible,
        DixieFrozen,
        DixieReversed,
        DixieSlow,
        RambiPalette,
        EnguardePalette,
        SquitterPalette,
        RattlyPalette,
        SquawksPalette,
        QuawksPalette,
    ]),
]

@dataclass
class DKC2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    energy_link: EnergyLink
    trap_link: TrapLink
    display_messages: DisplayMessages
    received_message_filter: ReceivedMessageFilter
    sent_message_filter: SentMessageFilter
    starting_life_count: StartingLifeCount
    starting_kong: StartingKong
    goal: Goal
    krock_boss_tokens: FlyingKrockTokens
    lost_world_rocks: LostWorldRocks
    extra_lost_world_rocks: ExtraLostWorldRocks
    lost_world_rock_placement: LostWorldRockPlacement
    logic: Logic
    required_galleon_levels: RequiredGalleonLevels
    required_cauldron_levels: RequiredCauldronLevels
    required_quay_levels: RequiredQuayLevels
    required_kremland_levels: RequiredKremlandLevels
    required_gulch_levels: RequiredGulchLevels
    required_keep_levels: RequiredKeepLevels
    required_krock_levels: RequiredKrockLevels
    shuffle_levels: ShuffleLevels
    shuffle_abilities: AbilityShuffle
    shuffle_animals: AnimalShuffle
    shuffle_barrels: BarrelShuffle
    kong_checks: KONGChecks
    dk_coin_checks: DKCoinChecks
    balloonsanity: BalloonChecks
    coinsanity: CoinChecks
    bananasanity: BunchChecks
    swanky_checks: SwankyChecks
    swanky_questions_per_quiz: SwankyQuestionsPerQuiz
    swanky_forced_topics: SwankyForceTopics
    swanky_excluded_topics: SwankyExcludeTopics
    trap_fill_percentage: TrapFillPercentage
    freeze_trap_weight: FreezeTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    honey_trap_weight: HoneyTrapWeight
    ice_trap_weight: IceTrapWeight
    tnt_barrel_trap_weight: TNTBarrelTrapWeight
    damage_trap_weight: DamageTrapWeight
    insta_death_trap_weight: InstaDeathTrapWeight
    palettes: SetPalettes
    palette_filters: PaletteFilter
    palette_diddy_active: DiddyActive
    palette_diddy_inactive: DiddyInactive
    palette_diddy_invincible: DiddyInvincible
    palette_diddy_frozen: DiddyFrozen
    palette_diddy_reversed: DiddyReversed
    palette_diddy_slow: DiddySlow
    palette_dixie_active: DixieActive
    palette_dixie_inactive: DixieInactive
    palette_dixie_invincible: DixieInvincible
    palette_dixie_frozen: DixieFrozen
    palette_dixie_reversed: DixieReversed
    palette_dixie_slow: DixieSlow
    palette_rambi: RambiPalette
    palette_enguarde: EnguardePalette
    palette_squitter: SquitterPalette
    palette_rattly: RattlyPalette
    palette_squawks: SquawksPalette
    palette_quawks: QuawksPalette
