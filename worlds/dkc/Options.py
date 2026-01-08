from dataclasses import dataclass

from .Items import item_groups
from .Aesthetics import player_palette_set_offsets

from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, OptionDict, PerGameCommonOptions, StartInventoryPool, FreeText
from schema import Schema, Optional

class StartingLifeCount(Range):
    """
    How many lives to start the game with. 
    """
    display_name = "Starting Life Count"
    range_start = 0
    range_end = 99
    default = 5

class StartingKong(Choice):
    """
    Which Kongs will be available at the start
    """
    display_name = "Starting Kong"
    option_donkey = 1
    option_diddy = 2
    option_both = 3
    default = 1

class GangplankTokens(Range):
    """
    How many Big Bananas are required to unlock Gang-Plank Galleon
    """
    display_name = "Big Bananas Required"
    range_start = 1
    range_end = 6
    default = 4

class Logic(Choice):
    """
    Logic difficulty. May become irrelevant if not a lot of items are added to the item pool.
    - **Strict**: Ensures everything is reachable as the original devs intended. For beginners or people who want to go out of logic with some tricks.
    - **Loose**: Reaching locations may require some level of mastery about the game's mechanics.
    - **Expert**: Locations expects players to be extremely good at the game with minimal amount of abilities. Hard to go out of logic. (NOT IMPLEMENTED YET)
    """
    display_name = "Logic Difficulty"
    option_strict = 0
    option_loose = 1
    option_expert = 2
    default = 0

class GlitchedWorldAccess(Toggle):
    """
    Level warping across worlds via glitches will be in logic
    """
    display_name = "Glitched World Access"

class RequiredJungleLevels(Range):
    """
    How many levels in Kongo Jungle need to be cleared to fight Very Gnawty
    """
    display_name = "Jungle Levels Required"
    range_start = 1
    range_end = 5
    default = 4

class RequiredMinesLevels(Range):
    """
    How many levels in Monkey Mines need to be cleared to fight Master Necky
    """
    display_name = "Mines Levels Required"
    range_start = 1
    range_end = 5
    default = 4

class RequiredValleyLevels(Range):
    """
    How many levels in Vine Valley need to be cleared to fight Queen B.
    """
    display_name = "Valley Levels Required"
    range_start = 1
    range_end = 6
    default = 4

class RequiredGlacierLevels(Range):
    """
    How many levels in Gorilla Glacier need to be cleared to fight Really Gnawty
    """
    display_name = "Glacier Levels Required"
    range_start = 1
    range_end = 6
    default = 4

class RequiredIndustriesLevels(Range):
    """
    How many levels in Kremkroc Industries Inc. need to be cleared to fight Dumb Drum
    """
    display_name = "Industries Levels Required"
    range_start = 1
    range_end = 6
    default = 4

class RequiredCavernsLevels(Range):
    """
    How many levels in Chimp Caverns need to be cleared to fight Master Necky Snr.
    """
    display_name = "Caverns Levels Required"
    range_start = 1
    range_end = 5
    default = 4

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

class ObjectShuffle(OptionSet):
    """
    Which kind of objects will be added as items in the item pool
    If an object is not present in the list they will be treated as unlocked from the start
    """
    display_name = "Object Shuffle"
    default = {ability for ability in item_groups["Objects"]}
    valid_keys = {ability for ability in item_groups["Objects"]}

class StartingWorld(Choice):
    """
    Which world you will start in
    """
    display_name = "Starting World"
    option_kongo_jungle = 0
    option_monkey_mines = 1
    option_vine_valley = 2
    option_gorilla_glacier = 3
    option_kremkroc_industries = 4
    option_chimp_caverns = 5
    default = "random"

class KONGChecks(Toggle):
    """
    Whether collecting all KONG letters in each level will grant a check
    """
    display_name = "KONG Letters Checks"

class TokenChecks(Toggle):
    """
    Whether collecting an animal token in levels will grant a check

    Doesn't include tokens inside bonuses
    """
    display_name = "Animal Token Checks"

class BananaChecks(Toggle):
    """
    Whether collecting banana bunches in levels will grant a check

    Doesn't include banana bunches inside bonuses
    """
    display_name = "Banana Bunches Checks"

class BalloonChecks(Toggle):
    """
    Whether collecting balloons in levels will grant a check

    Doesn't include balloons inside bonuses
    """
    display_name = "Balloon Checks"

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

class JumpTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which makes the player jump uncontrollably
    """
    display_name = "Jump Trap Weight"

class StickyFloorTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which makes the player unable to walk or roll in the ground
    """
    display_name = "Sticky Floor Trap Weight"

class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which makes the floor slippery
    """
    display_name = "Stun Trap Weight"

class StunTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which freezes the player in place for a few seconds
    """
    display_name = "Stun Trap Weight"

class NutTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which spawns a nut on top of the player
    """
    display_name = "Nut Trap Weight"

class ArmyTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which spawns an Army on top of the player
    """
    display_name = "Army Trap Weight"

class BonusTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which sends the player to an Animal Bonus level
    """
    display_name = "Animal Bonus Trap Weight"

class KONGLetters(FreeText):
    """
    Which word will be displayed by the KONG letters.
    Limited to 4 characters from A to Z.
    """
    display_name = "KONG Letters"
    default = "KONG"

class BaseDonkeyPalette(Choice):
    """
    Base class for palettes
    """
    option_original = 0
    option_original_inactive = 1
    option_original_team_2 = 2
    option_original_team_2_inactive = 3
    option_dkc2_diddy_alt = 4
    option_dkc3_kiddy = 5
    option_dkc3_kiddy_alt = 6
    option_purple_tie = 7
    option_black_tie = 8
    option_white_tie = 9
    option_dkc2_frozen = 10
    option_dkc2_reversed = 11
    option_dkc2_slow = 12
    option_golden = 13
    option_monochrome = 14
    option_gb_green = 15
    option_gb_gray = 16
    option_gbc_retro_blast = 17

class BaseDiddyPalette(Choice):
    """
    Base class for palettes
    """
    option_original = 0
    option_original_inactive = 1
    option_original_team_2 = 2
    option_original_team_2_inactive = 3
    option_dkc2_invincible = 4
    option_dkc2_team_2 = 5
    option_dkc2_team_2_inactive = 6
    option_dkc2_frozen = 7
    option_dkc2_reversed = 8
    option_dkc2_slow = 9
    option_dkc3_kiddy = 10
    option_dkc3_kiddy_alt = 11
    option_gb_green = 12
    option_gb_gray = 13
    option_gbc_retro_blast = 14
    option_golden = 15
    option_monochrome = 16
    option_sepia = 17
    option_smb_mario = 18
    option_smb_luigi = 19
    option_toothpaste = 20
    option_whatsapp = 21
    option_bubblegum = 22
    option_retro_frozen = 23
    option_retro_reversed = 24
    option_retro_slow = 25
    option_rottytops = 26

class DonkeyActive(BaseDonkeyPalette):
    """
    Which color to use for Donkey's active color
    """
    display_name = "Donkey Active Palette"
    default = 0

class DonkeyInactive(BaseDonkeyPalette):
    """
    Which color to use for Donkey's inactive color
    """
    display_name = "Donkey Inactive Palette"
    default = 1

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
        Optional(color_set): int for color_set in player_palette_set_offsets.keys()
    })
    default = {color_set: 0 for color_set in player_palette_set_offsets.keys()}


class SetPalettes(OptionDict):
    """
    Allows you to create colors for each Kong status. Includes K.Rool effects and the invincibility barrel
    This will override the option preset
    
    Each one expects 15 values which are mapped to the Kongs colors
    The values can be in SNES RGB (bgr555) with the $ prefix or PC RGB (rgb888) with the # prefix
    """
    display_name = "Set Custom Palettes"
    schema = Schema({
        Optional(color_set): list for color_set in player_palette_set_offsets.keys()
    })
    default = {}


dkc_option_groups = [
    OptionGroup("Goal", [
        GangplankTokens,
        RequiredJungleLevels,
        RequiredMinesLevels,
        RequiredValleyLevels,
        RequiredGlacierLevels,
        RequiredIndustriesLevels,
        RequiredCavernsLevels,
    ]),
    OptionGroup("Locations", [
        Logic,
        GlitchedWorldAccess,
        KONGChecks,
        BalloonChecks,
        BananaChecks,
        TokenChecks,
    ]),
    OptionGroup("Shuffle", [
        StartingWorld,
        StartingKong,
        AbilityShuffle,
        AnimalShuffle,
        ObjectShuffle,
    ]),
    OptionGroup("Traps", [
        TrapFillPercentage,
        JumpTrapWeight,
        IceTrapWeight,
        StunTrapWeight,
        NutTrapWeight,
        ArmyTrapWeight,
        BonusTrapWeight,
        StickyFloorTrapWeight,
    ]),
    OptionGroup("Aesthetics", [
        SetPalettes,
        PaletteFilter,
        DonkeyActive,
        DonkeyInactive,
        DiddyActive,
        DiddyInactive,
        KONGLetters,
    ]),
]

@dataclass
class DKCOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    #death_link: DeathLink
    energy_link: EnergyLink
    trap_link: TrapLink
    starting_life_count: StartingLifeCount
    starting_kong: StartingKong
    logic: Logic
    glitched_world_access: GlitchedWorldAccess
    gangplank_tokens: GangplankTokens
    required_jungle_levels: RequiredJungleLevels
    required_mines_levels: RequiredMinesLevels
    required_valley_levels: RequiredValleyLevels
    required_glacier_levels: RequiredGlacierLevels
    required_industries_levels: RequiredIndustriesLevels
    required_caverns_levels: RequiredCavernsLevels
    starting_world: StartingWorld
    shuffle_abilities: AbilityShuffle
    shuffle_animals: AnimalShuffle
    shuffle_objects: ObjectShuffle
    kong_checks: KONGChecks
    balloon_checks: BalloonChecks
    banana_checks: BananaChecks
    token_checks: TokenChecks
    trap_fill_percentage: TrapFillPercentage
    jump_trap_weight: JumpTrapWeight
    sticky_floor_trap_weight: StickyFloorTrapWeight
    stun_trap_weight: StunTrapWeight
    ice_trap_weight: IceTrapWeight
    nut_trap_weight: NutTrapWeight
    army_trap_weight: ArmyTrapWeight
    animal_bonus_trap_weight: BonusTrapWeight
    player_palettes: SetPalettes
    player_palette_filters: PaletteFilter
    palette_donkey_active: DonkeyActive
    palette_donkey_inactive: DonkeyInactive
    palette_diddy_active: DiddyActive
    palette_diddy_inactive: DiddyInactive
    kong_letters: KONGLetters
