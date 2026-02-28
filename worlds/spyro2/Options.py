import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions, OptionGroup

class GoalOptions():
    RIPTO = 0
    SIXTY_FOUR_ORB = 3
    HUNDRED_PERCENT = 4
    TEN_TOKENS = 5
    ALL_SKILLPOINTS = 6
    EPILOGUE = 7
    ORB_HUNT = 8

class LevelLockOptions():
    VANILLA = 0
    KEYS = 1
    ORBS = 2

class MoneybagsOptions():
    VANILLA = 0
    PRICE_SHUFFLE = 1
    MONEYBAGSSANITY = 2

class GemsanityOptions():
    OFF = 0
    PARTIAL = 1
    FULL = 2
    FULL_GLOBAL = 3

class SparxUpgradeOptions():
    OFF = 0
    BLUE = 1
    GREEN = 2
    SPARXLESS = 3
    TRUE_SPARXLESS = 4

class AbilityOptions():
    VANILLA = 0
    IN_POOL = 1
    OFF = 2
    START_WITH = 3

class BomboOptions():
    VANILLA = 0
    THIRD_ONLY = 1
    FIRST_ONLY = 2
    FIRST_ONLY_NO_ATTACK = 3

class PortalTextColorOptions():
    DEFAULT = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    PINK = 4
    WHITE = 5

class RandomizeGemColorOptions():
    DEFAULT = 0
    SHUFFLE = 1
    RANDOM = 2
    TRUE_RANDOM = 3


class GoalOption(Choice):
    """Lets the user choose the completion goal.
    Ripto - Collect enough orbs to open the arena, and beat Ripto. The game marks you as having defeated Ripto during the ensuing cutscene.
    64 Orb - Collect 64 orbs and beat Ripto.
    100 Percent - Collect all talismans, orbs, and gems and beat Ripto. In Open World mode, no talismans are required.
    10 Tokens - Collect 8000 gems and 55 orbs to unlock the theme park and collect all 10 tokens in Dragon Shores.
    All Skillpoints - Collect all 16 skill points in the game. Excluded locations are still required for this goal.
    Epilogue - Unlock the full epilogue by collecting all 16 skill points and defeating Ripto. Excluded locations are still required for this goal."""
    display_name = "Completion Goal"
    default = GoalOptions.RIPTO
    option_ripto = GoalOptions.RIPTO
    option_64_orb = GoalOptions.SIXTY_FOUR_ORB
    option_100_percent = GoalOptions.HUNDRED_PERCENT
    option_10_tokens = GoalOptions.TEN_TOKENS
    option_all_skillpoints = GoalOptions.ALL_SKILLPOINTS
    option_epilogue = GoalOptions.EPILOGUE
    # TODO: Allow this once edge cases are handled.
    # option_orb_hunt = GoalOptions.ORB_HUNT

class OrbHuntRequirement(Range):
    """Determines how many orbs are needed to complete the Orb Hunt goal.  Has no effect if any other goal is chosen."""
    display_name = "Orbs Required for Orb Hunt"
    range_start = 2
    range_end = 64
    default = 40

class RiptoDoorOrbs(Range):
    """Determines how many orbs are required to unlock the door to Ripto.
    NOTE: Due to limitations of Spyro 2, if you connect to Archipelago while in Winter Tundra, the game will default
    to 40 orbs until you exit Winter Tundra and return."""
    display_name = "Orbs to Unlock Ripto"
    range_start = 0
    range_end = 64
    default = 40

class TotalAvailableOrbs(Range):
    """Determines the number of orbs available.
    NOTE: If fewer than the amount required for the Ripto door ar an Orb Hunt goal, more will be added.
    Other orb requirements throughout the game will be adjusted according to the number available."""
    display_name = "Orbs Available"
    range_start = 2
    range_end = 64
    default = 64

class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

class EnableOpenWorld(Toggle):
    """If on, Crush and Gulp do not require talismans."""
    display_name = "Enable Open World"

class LevelLockOption(Choice):
    """Determines the rules for unlocking each level. Glimmer, Homeworlds, and bosses are bosses always have their
    vanilla requirements.
    Vanilla: Levels are available if you meet the vanilla requirements.
    Keys: Levels are unlocked by finding "Unlock" items. Note: you may need to increase the number of locations (for example,
      by adding gem checks) to add keys.
    """
    display_name = "Level Locks"
    default = LevelLockOptions.VANILLA
    option_vanilla = LevelLockOptions.VANILLA
    option_keys = LevelLockOptions.KEYS
    # option_orbs = LevelLockOptions.ORBS

class StartingLevelCount(Range):
    """Determines how many level unlocks the player starts with.
    The player always has access to Glimmer, homeworlds, and boss fights.
    NOTE: Only has an effect when level locks are on."""
    display_name = "Starting Level Unlocks"
    range_start = 0
    range_end = 22
    default = 8

class StartWithAbilitiesAndWarps(Toggle):
    """If on in Open World mode, the player will start with swim, climb, headbash, and access to all 3 homeworlds.
    NOTE: Only has an effect in Open World mode."""
    display_name = "Open World Start With Abilities and Warps"

class Enable25PctGemChecksOption(Toggle):
    """Adds checks for getting 25% of the gems in a level"""
    display_name = "Enable 25% Gem Checks"

class Enable50PctGemChecksOption(Toggle):
    """Adds checks for getting 50% of the gems in a level"""
    display_name = "Enable 50% Gem Checks"

class Enable75PctGemChecksOption(Toggle):
    """Adds checks for getting 75% of the gems in a level"""
    display_name = "Enable 75% Gem Checks"

class EnableGemChecksOption(Toggle):
    """Adds checks for getting all gems in a level"""
    display_name = "Enable 100% Gem Checks"

class EnableTotalGemChecksOption(Toggle):
    """Adds checks for every 500 gems you collect total.
    NOTE: Gems currently paid to Moneybags do not count towards your total.
    Logic assumes you pay Moneybags everywhere you can so you cannot be locked out of checks."""
    display_name = "Enable Total Gem Count Checks"

class MaxTotalGemCheckOption(Range):
    """Sets the highest number of total gems that can be required for Total Gem Count checks.
    This has no effect if Enable Total Gem Count Checks is disabled."""
    display_name = "Max for Total Gem Count Checks"
    range_start = 500
    range_end = 10000
    default = 4000

class EnableSkillpointChecksOption(Toggle):
    """Adds checks for getting skill points"""
    display_name = "Enable Skillpoint Checks"

class EnableLifeBottleChecksOption(Toggle):
    """Adds checks for getting life bottles"""
    display_name = "Enable Life Bottle Checks"

class EnableSpiritParticleChecksOption(Toggle):
    """Adds checks for getting all spirit particles in a level.
    Some minigame enemies are counted as spirit particles, like Draclets in Crystal Glacier.
    NOTE: Some enemies will only release spirit particles while the camera is on them."""
    display_name = "Enable Spirit Particle Checks"

class EnableGemsanityOption(Choice):
    """Adds checks for each individual gem.
    WARNING: To avoid logic issues, this setting is meant for Moneybagssanity only.  If Moneybagssanity is off,
        all Moneybags prices will be set to 0 in game.
    WARNING: Both full and full global require the host to edit allow_full_gemsanity
        in their yaml file.
    Off: Individual gems are not checks.
    Partial: Every gem has a chance to be a check, but only 200 will be (chosen at random).  For every level with loose
        gems (not speedways), 8 items giving 50 gems for that level will be added to the pool.
    Full: All gems are checks.  Gem items will be shuffled only within your world.
    Full Global: All gems are checks.  Gem items can be anywhere."""
    display_name = "Enable Gemsanity"
    default = GemsanityOptions.OFF
    option_off = GemsanityOptions.OFF
    option_partial = GemsanityOptions.PARTIAL
    option_full = GemsanityOptions.FULL
    option_full_global = GemsanityOptions.FULL_GLOBAL

class MoneybagsSettings(Choice):
    """Determines settings for Moneybags unlocks.
    Vanilla - Pay Moneybags to progress as usual
    COMING SOON (tm): Price Shuffle - The prices Moneybags charges are randomized, while still allowing for beatable seeds.
    Moneybagssanity - You cannot pay Moneybags at all and must find unlock items to progress. Glimmer Bridge
    is excluded to avoid issues with early game randomization."""
    display_name = "Moneybags Settings"
    default = MoneybagsOptions.VANILLA
    option_vanilla = MoneybagsOptions.VANILLA
    # TODO: Implement.
    # option_price_shuffle = MoneybagsOptions.PRICE_SHUFFLE
    option_moneybagssanity = MoneybagsOptions.MONEYBAGSSANITY

class EnableDeathLink(DeathLink):
    """If enabled, Spyro will die when a DeathLink is received and will send them on his death.
    This is a beta feature and does not fully support all edge cases yet - not every death will trigger a DeathLink,
    and not every received DeathLink will kill Spyro."""
    display_name = "DeathLink"

class EnableFillerExtraLives(DefaultOnToggle):
    """Allows filler items to include extra lives"""
    display_name = "Enable Extra Lives Filler"

class EnableFillerDestructiveSpyro(Toggle):
    """Allows filler items to include temporarily powering up Spyro so anything destructible he touches is destroyed.
    Affects enemies, strong chests, breakable walls, etc."""
    display_name = "Enable Temporary Destructive Spyro Filler"

# Likely possible but check for side effects.
#class EnableFillerInvincibility(Toggle):
#    """Allows filler items to include temporary invincibility"""
#    display_name = "Enable Temporary Invincibility Filler"

class EnableFillerColorChange(Toggle):
    """Allows filler items to include changing Spyro's color"""
    display_name = "Enable Changing Spyro's Color Filler"

class EnableFillerBigHeadMode(Toggle):
    """Allows filler items to include turning on Big Head Mode and Flat Spyro Mode"""
    display_name = "Enable Big Head and Flat Spyro Filler"

class EnableFillerHealSparx(Toggle):
    """Allows filler items to include healing Sparx."""
    display_name = "Enable healing Sparx Filler"

class TrapFillerPercent(Range):
    """Determines the percentage of filler items that will be traps."""
    display_name = "Trap Percentage of Filler"
    range_start = 0
    range_end = 100
    default = 0

class EnableTrapDamageSparx(Toggle):
    """Allows filler items to include damaging Sparx. Cannot directly kill Spyro."""
    display_name = "Enable Hurting Sparx Trap"

class EnableTrapSparxless(Toggle):
    """Allows filler items to include removing Sparx."""
    display_name = "Enable Sparxless Trap"

class EnableTrapInvisible(Toggle):
    """Allows filler items to turn Spyro invisible briefly.
    NOTE: Duckstation must be run in Interpreter mode for this to have any effect."""
    display_name = "Enable Invisibility Trap"

class EnableTrapRemappedController(Toggle):
    """Allows filler items to "remap" your controller briefly.
    NOTE: Duckstation must be run in Interpreter mode for this to have any effect."""
    display_name = "Enable Remapped Controller"

class EnableProgressiveSparxHealth(Choice):
    """Start the game with lower max health and add items to the pool to increase your max health.
    Off - The game behaves normally.
    Blue - Your max health starts at blue Sparx, and 1 upgrade is added to the pool.
    Green - Your max health starts at green Sparx, and 2 upgrades are added to the pool.
    Sparxless - Your max health starts at no Sparx, and 3 upgrades are added to the pool.
    True Sparxless - Your max health is permanently Sparxless.  No upgrades are added to the pool."""
    display_name = "Enable Progressive Sparx Health Upgrades"
    default = SparxUpgradeOptions.OFF
    option_off = SparxUpgradeOptions.OFF
    option_blue = SparxUpgradeOptions.BLUE
    option_green = SparxUpgradeOptions.GREEN
    option_sparxless = SparxUpgradeOptions.SPARXLESS
    option_true_sparxless = SparxUpgradeOptions.TRUE_SPARXLESS

class ProgressiveSparxHealthLogic(Toggle):
    """Ensures that sufficient max Sparx health is in logic before various required checks.
    Entering Aquaria Towers and Crush logically requires green Sparx.  Entering Skelos Badlands and Gulp
    logically requires blue Sparx, and entering Ripto logically requires gold Sparx.
    Note: This does nothing unless Enable Progressive Sparx Health Upgrades is set to blue, green, or Sparxless,"""
    display_name = "Enable Progressive Sparx Health Logic"

class DoubleJumpAbility(Choice):
    """By default, Spyro 2 supports a double jump ability, where jumping then pressing square without letting go of jump
    gains extra height.  This allows many sequence breaks within the game.
    Note that most skips possible with double jump can be done in other, harder ways.
    This option affects how the game plays, but does not directly impact logic.
    The logic impact of the tricks below may be impacted by whether you can double jump.
    NOTE: Duckstation must be run in Interpreter mode for this to have any effect.
    Vanilla - Double Jump behaves normally.
    In Pool - Adds Double Jump to the item pool.  The ability is disabled until you acquire the item.
    Off - Double Jump is disabled."""
    display_name = "Double Jump Ability"
    default = AbilityOptions.VANILLA
    option_vanilla = AbilityOptions.VANILLA
    option_in_pool = AbilityOptions.IN_POOL
    option_off = AbilityOptions.OFF

class FireballAbility(Choice):
    """Spyro 2 has a permanent fireball powerup in Dragon Shores, which makes gameplay much easier.
    With glitches, it is possible to get here without 100% completion.
    Exiting a 100% save file and entering a new game without resetting Duckstation also carries it over to the new save.
    This option affects how the game plays, not game logic.
    Vanilla - The fireball powerup in Dragon Shores behaves normally.
    In Pool - Adds Permanent Fireball to the item pool.  The Dragon Shores powerup does not work.
    Off - Permanent Fireball is disabled. The Dragon Shores powerup does not work.
    Start With - You begin the game with fireball, as in New Game Plus."""
    display_name = "Permanent Fireball Ability"
    default = AbilityOptions.VANILLA
    option_vanilla = AbilityOptions.VANILLA
    option_in_pool = AbilityOptions.IN_POOL
    option_off = AbilityOptions.OFF
    option_start_with = AbilityOptions.START_WITH

class ColossusStartingGoals(Range):
    """Determines how many goals you start with in both Colossus orb challenges."""
    display_name = "Colossus Starting Goals"
    range_start = 0
    range_end = 4
    default = 0

class IdolEasyFish(Toggle):
    """Makes it so red fish behave the same as other types of fish in Idol Springs."""
    display_name = "Idol Easy Fish"

class HurricosEasyLightningOrbs(Toggle):
    """Makes it so lightning thieves do not steal the orbs in Hurricos."""
    display_name = "Hurricos Easy Lightning Orbs"

class BreezeRequiredGears(Range):
    """Determines how many gears you must collect to complete the trolley orb."""
    display_name = "Breeze Required Gears"
    range_start = 1
    range_end = 50
    default = 50

class ScorchBomboSettings(Choice):
    """Determines how the Bombo orb works in Scorch.
    NOTE: This is a beta option. Multiple Bombos may appear, and interacting with the wrong one may softlock Bombo.
    Vanilla - Bombo behaves as normal.
    First Only - Complete the first (shortest) path to complete the orb.
    Attackless First Only - Complete the first (shortest) path to complete the orb. Bombo will not attack."""
    display_name = "Scorch Bombo Settings"
    default = BomboOptions.VANILLA
    option_vanilla = BomboOptions.VANILLA
    option_first_only = BomboOptions.FIRST_ONLY
    option_attackless_first_only = BomboOptions.FIRST_ONLY_NO_ATTACK

class FractureRequireHeadbash(DefaultOnToggle):
    """Determines if Hunter requires headbash to start Earthshaper Bash.
    Without headbash, this orb can be completed with fireball or the Fracture Easy Earthshapers setting.
    This does not change the orb's logic or change how it plays."""
    display_name = "Fracture Require Headbash"

class FractureEasyEarthshapers(Toggle):
    """Removes the 7 earthshapers from the Alchemist area and reduces the maximum number of spirit particles in the level
    accordingly.
    Removes the headbash requirement from the Fracture Hills all spirit particles check.
    The second orb still requires headbash, unless Fracture Require Headbash is disabled."""
    display_name = "Fracture Easy Earthshapers"

class MagmaSpyroStartingPopcorn(Range):
    """Determines how many popcorn crystals you start with in each Hunter orb challenge."""
    display_name = "Magma Spyro Starting Popcorn"
    range_start = 0
    range_end = 9
    default = 0

class MagmaHunterStartingPopcorn(Range):
    """Determines how many popcorn crystals Hunter starts with in each Hunter orb challenge."""
    display_name = "Magma Hunter Starting Popcorn"
    range_start = 0
    range_end = 9
    default = 0

class ShadyRequireHeadbash(DefaultOnToggle):
    """Determines if Free Hippos in Shady Oasis requires headbash to start.
    Without headbash, this orb can be completed with fireball.
    This does not change the orb's logic or change how it plays."""
    display_name = "Shady Require Headbash"

class EasyGulp(Toggle):
    """If turned on, Spyro does double damage to Gulp."""
    display_name = "Easy Gulp"

class PortalAndGemCollectionColor(Choice):
    """Changes the color of the number that appears when gems are collected,
    as well as the text on portals."""
    display_name = "Portal and Gem Collection Text Color"
    default = PortalTextColorOptions.DEFAULT
    option_default = PortalTextColorOptions.DEFAULT
    option_red = PortalTextColorOptions.RED
    option_green = PortalTextColorOptions.GREEN
    option_blue = PortalTextColorOptions.BLUE
    option_pink = PortalTextColorOptions.PINK
    option_white = PortalTextColorOptions.WHITE

class GemColor(Choice):
    """Changes the color of gem types (and some other items in game).
    Default: No changes.
    Shuffle: Mixes up the colors of gem types.
    Random Choice: Gem colors are randomly selected from a curated set of options.
    True Random: Gem colors are completely random.  This probably won't look great.
    """
    display_name = "Gem Color"
    default = RandomizeGemColorOptions.DEFAULT
    option_default = RandomizeGemColorOptions.DEFAULT
    option_shuffle = RandomizeGemColorOptions.SHUFFLE
    option_random_choice = RandomizeGemColorOptions.RANDOM
    option_true_random = RandomizeGemColorOptions.TRUE_RANDOM

@dataclass
class Spyro2Option(PerGameCommonOptions):
    goal: GoalOption
    guaranteed_items: GuaranteedItemsOption
    # TODO: Enable.
    # orb_hunt_requirement: OrbHuntRequirement
    ripto_door_orbs: RiptoDoorOrbs
    # TODO: Handle edge cases and enable.
    # available_orbs: TotalAvailableOrbs
    enable_open_world: EnableOpenWorld
    open_world_ability_and_warp_unlocks: StartWithAbilitiesAndWarps
    level_lock_options: LevelLockOption
    level_unlocks: StartingLevelCount
    enable_25_pct_gem_checks: Enable25PctGemChecksOption
    enable_50_pct_gem_checks: Enable50PctGemChecksOption
    enable_75_pct_gem_checks: Enable75PctGemChecksOption
    enable_gem_checks: EnableGemChecksOption
    enable_total_gem_checks: EnableTotalGemChecksOption
    max_total_gem_checks: MaxTotalGemCheckOption
    enable_skillpoint_checks: EnableSkillpointChecksOption
    enable_life_bottle_checks: EnableLifeBottleChecksOption
    enable_spirit_particle_checks: EnableSpiritParticleChecksOption
    enable_gemsanity: EnableGemsanityOption
    moneybags_settings: MoneybagsSettings
    death_link: EnableDeathLink
    enable_filler_extra_lives: EnableFillerExtraLives
    enable_destructive_spyro_filler: EnableFillerDestructiveSpyro
    enable_filler_color_change: EnableFillerColorChange
    enable_filler_big_head_mode: EnableFillerBigHeadMode
    enable_filler_heal_sparx: EnableFillerHealSparx
    trap_filler_percent: TrapFillerPercent
    enable_trap_damage_sparx: EnableTrapDamageSparx
    enable_trap_sparxless: EnableTrapSparxless
    enable_trap_invisibility: EnableTrapInvisible
    enable_progressive_sparx_health: EnableProgressiveSparxHealth
    enable_progressive_sparx_logic: ProgressiveSparxHealthLogic
    double_jump_ability: DoubleJumpAbility
    permanent_fireball_ability: FireballAbility
    colossus_starting_goals: ColossusStartingGoals
    idol_easy_fish: IdolEasyFish
    hurricos_easy_lightning_orbs: HurricosEasyLightningOrbs
    breeze_required_gears: BreezeRequiredGears
    scorch_bombo_settings: ScorchBomboSettings
    fracture_require_headbash: FractureRequireHeadbash
    fracture_easy_earthshapers: FractureEasyEarthshapers
    magma_spyro_starting_popcorn: MagmaSpyroStartingPopcorn
    magma_hunter_starting_popcorn: MagmaHunterStartingPopcorn
    shady_require_headbash: ShadyRequireHeadbash
    easy_gulp: EasyGulp
    portal_gem_collection_color: PortalAndGemCollectionColor
    gem_color: GemColor


# Group logic/trick options together, especially for the local WebHost.
spyro_options_groups = [
    OptionGroup(
        "Difficulty",
        [
            ColossusStartingGoals,
            IdolEasyFish,
            HurricosEasyLightningOrbs,
            BreezeRequiredGears,
            ScorchBomboSettings,
            FractureRequireHeadbash,
            FractureEasyEarthshapers,
            MagmaSpyroStartingPopcorn,
            MagmaHunterStartingPopcorn,
            ShadyRequireHeadbash,
            EasyGulp
        ],
        True
    ),
    OptionGroup(
        "Cosmetics",
        [
            PortalAndGemCollectionColor,
            GemColor
        ],
        True
    ),
]
