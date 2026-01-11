import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions, OptionGroup

class GoalOptions():
    RIPTO = 0
    FOURTEEN_TALISMAN = 1
    FORTY_ORB = 2
    SIXTY_FOUR_ORB = 3
    HUNDRED_PERCENT = 4
    TEN_TOKENS = 5
    ALL_SKILLPOINTS = 6
    EPILOGUE = 7

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

class LogicTrickOptions():
    OFF = 0
    ON_WITH_DOUBLE_JUMP = 1
    ALWAYS_ON = 2

class PortalTextColorOptions():
    DEFAULT = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    PINK = 4
    WHITE = 5


class GoalOption(Choice):
    """Lets the user choose the completion goal.  Regardless of choice, the door to Ripto requires 40 orbs to open.
    Unless you are using glitches to enter boss fights, the first three goals should be equivalent.
    Ripto - Beat Ripto. The goal triggers during the ensuing cutscene.
    14 Talisman - Collect 6 Summer Forest Talismans and 8 Autumn Plains Talismans and beat Ripto. In Open World mode, defaults to Ripto.
    40 Orb - Collect 40 orbs and beat Ripto.
    64 Orb - Collect 64 orbs and beat Ripto.
    100 Percent - Collect all talismans, orbs, and gems and beat Ripto. In Open World mode, no talismans are required.
    10 Tokens - Collect all 10 tokens in Dragon Shores.
    All Skillpoints - Collect all 16 skill points in the game. Excluded locations are still required for this goal.
    Epilogue - Unlock the full epilogue by collecting all 16 skill points and defeating Ripto. Excluded locations are still required for this goal."""
    display_name = "Completion Goal"
    default = GoalOptions.FORTY_ORB
    option_ripto = GoalOptions.RIPTO
    option_14_talisman = GoalOptions.FOURTEEN_TALISMAN
    option_40_orb = GoalOptions.FORTY_ORB
    option_64_orb = GoalOptions.SIXTY_FOUR_ORB
    option_100_percent = GoalOptions.HUNDRED_PERCENT
    option_10_tokens = GoalOptions.TEN_TOKENS
    option_all_skillpoints = GoalOptions.ALL_SKILLPOINTS
    option_epilogue = GoalOptions.EPILOGUE

class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

class EnableOpenWorld(Toggle):
    """If on, Crush and Gulp do not require talismans.  Every level is unlocked by items.
    You start with Glimmer and 3 other unlocks."""
    display_name = "Enable Open World"

class StartingLevelCount(Range):
    """Determines how many level unlocks the player starts with.
    The player always has access to Glimmer, homeworlds, and boss fights.
    Starting with fewer than 8 unlocks requires you to add extra locations to the item pool.
    NOTE: Only has an effect in Open World mode."""
    display_name = "Open World Starting Level Unlocks"
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
    Off: Individual gems are not checks.
    Partial: Every gem has a chance to be a check, but only 200 will be (chosen at random).  For every level with loose
        gems (not speedways), 8 items giving 50 gems for that level will be added to the pool."""
    display_name = "Enable Gemsanity"
    default = GemsanityOptions.OFF
    option_off = GemsanityOptions.OFF
    option_partial = GemsanityOptions.PARTIAL
    #option_full = GemsanityOptions.FULL
    #option_full_global = GemsanityOptions.FULL_GLOBAL
    #Full: All gems are checks.  Gem items will be shuffled only within your world.
    #Full Global: All gems are checks.  Gem items can be anywhere.

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

# TODO: Support more granular tricks.
class LogicCrushEarly(Choice):
    """Puts entering the Crush fight without all 6 Summer Forest Talismans into logic.
    Requires one of numerous out-of-bounds glitches.
    Off: Requires 6 summer forest talismans, like normal.
    On With Double Jump: If the player has access to double jump, skipping into Crush is in logic.
    Always On: Skipping into Crush is always in logic."""
    display_name = "Enter Crush Early"
    default = LogicTrickOptions.OFF
    option_off = LogicTrickOptions.OFF
    option_on_with_double_jump = LogicTrickOptions.ON_WITH_DOUBLE_JUMP
    option_always_on = LogicTrickOptions.ALWAYS_ON

class LogicGulpEarly(Choice):
    """Puts entering the Gulp fight without all 14 Talismans into logic.
    See https://www.youtube.com/watch?v=zkIq-2g8x8U.
    Off: Requires 14 talismans, like normal.
    On With Double Jump: If the player has access to double jump, skipping into Gulp is in logic.
    Always On: Skipping into Gulp is always in logic."""
    display_name = "Enter Gulp Early"
    default = LogicTrickOptions.OFF
    option_off = LogicTrickOptions.OFF
    option_on_with_double_jump = LogicTrickOptions.ON_WITH_DOUBLE_JUMP
    option_always_on = LogicTrickOptions.ALWAYS_ON

# TODO: Add Swim/Theater and Sproder logic.
class LogicRiptoEarly(Choice):
    """Puts entering the Ripto fight without 40 orbs into logic.
    Off: Requires 40 orbs, like normal.
    On With Double Jump: If the player has access to double jump, skipping into Ripto is in logic.
    Always On: Skipping into Ripto is always in logic."""
    display_name = "Enter Gulp Early"
    default = LogicTrickOptions.OFF
    option_off = LogicTrickOptions.OFF
    option_on_with_double_jump = LogicTrickOptions.ON_WITH_DOUBLE_JUMP
    option_always_on = LogicTrickOptions.ALWAYS_ON

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


@dataclass
class Spyro2Option(PerGameCommonOptions):
    goal: GoalOption
    guaranteed_items: GuaranteedItemsOption
    enable_open_world: EnableOpenWorld
    open_world_level_unlocks: StartingLevelCount
    open_world_ability_and_warp_unlocks: StartWithAbilitiesAndWarps
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
    logic_crush_early: LogicCrushEarly
    logic_gulp_early: LogicGulpEarly
    logic_ripto_early: LogicRiptoEarly
    portal_gem_collection_color: PortalAndGemCollectionColor


# Group logic/trick options together, especially for the local WebHost.
spyro_options_groups = [
    OptionGroup(
        "Tricks",
        [
            LogicCrushEarly,
            LogicGulpEarly,
            LogicRiptoEarly
        ],
        True
    ),
    OptionGroup(
        "Cosmetics",
        [
            PortalAndGemCollectionColor
        ],
        True
    ),
]
