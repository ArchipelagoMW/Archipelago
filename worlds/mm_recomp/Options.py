from dataclasses import dataclass

from typing import Dict

from Options import Choice, Option, DefaultOnToggle, Toggle, Range, OptionList, StartInventoryPool, DeathLink, PerGameCommonOptions


class LogicDifficulty(Choice):
    """Set the logic difficulty used when generating."""
    display_name = "Logic Difficulty"
    # ~ option_easy = 0
    option_normal = 1
    #option_obscure_glitchless = 2
    #option_glitched = 3
    option_no_logic = 4
    # ~ alias_baby = option_easy
    default = 1


class MajoraRemainsRequired(Range):
    """Set the amount of boss remains required to fight Majora."""
    display_name = "Majora Boss Remains Required"
    range_start = 0
    range_end = 4
    default = 4


class MoonRemainsRequired(Range):
    """Set the amount of boss remains required to reach the Moon after playing Oath to Order."""
    display_name = "Moon Boss Remains Required"
    range_start = 0
    range_end = 4
    default = 4


class CAMC(DefaultOnToggle):
    """Set whether chest appearance matches contents."""
    display_name = "CAMC"


class Swordless(Toggle):
    """Start the game without a sword, and shuffle an extra Progressive Sword into the pool."""
    display_name = "Swordless"


class Shieldless(Toggle):
    """Start the game without a shield, and shuffle an extra Progressive Shield into the pool."""
    display_name = "Shieldless"


class StartWithSoaring(DefaultOnToggle):
    """Start the game with Song of Soaring."""
    display_name = "Start With Soaring"


class StartingHeartQuarters(Range):
    """The number of heart quarters Link starts with.
    If less than 12, extra heart items will be shuffled into the pool to accommodate."""
    display_name = "Starting Hearts"
    range_start = 4
    range_end = 12
    default = 12


class StartingHeartsAreContainersOrPieces(Choice):
    """Choose whether Link's starting hearts are shuffled into the pool as Heart Containers (plus the remainder as Heart Pieces) or as all Heart Pieces."""
    display_name = "Starting Hearts are Containers or Pieces"
    option_containers = 0
    option_pieces = 1
    default = 0


class ShuffleRegionalMaps(Choice):
    """Choose whether to shuffle every regional map from Tingle."""
    display_name = "Shuffle Regional Maps"
    option_vanilla = 0
    option_starting = 1
    option_anywhere = 2
    default = 1


class ShuffleBossRemains(Choice):
    """Choose whether to shuffle the Boss Remains received after beating a boss at the end of a dungeon.
    
    vanilla: Boss Remains are placed in their vanilla locations.
    anything: Any item can be given by any of the Boss Remains, and Boss Remains can be found anywhere in any world.
    bosses: Boss Remains are shuffled amongst themselves as the rewards for defeating bosses."""
    display_name = "Shuffle Boss Remains"
    option_vanilla = 0
    option_anywhere = 1
    option_bosses = 2
    default = 0


class BossWarpsWithRemains(DefaultOnToggle):
    """Choose whether to retain the vanilla ability to warp the boss of dungeons by having their vanilla remains.
    Getting the remains check for a dungeon will open its warp regardless."""
    display_name = "Warp to Bosses Using Remains"


class ShuffleSpiderHouseReward(Toggle):
    """Choose whether to shuffle the Mask of Truth given at the end of the Southern Spider House and the Wallet Upgrade at the end of the Ocean Spider House."""
    display_name = "Shuffle Spider House Rewards"


class RequiredSkullTokens(Range):
    """The number of Gold Skulltula Tokens needed to get the reward from their respective Spider House.
    All 30 Tokens from each Spider House are still shuffled into the item pool regardless of the selection.
    Valid amounts are within the range 0-30."""
    display_name = "Required Skulltula Tokens"
    range_start = 0
    range_end = 30
    default = 30


class Skullsanity(Choice):
    """Choose what items gold skulltulas can give.
    
    vanilla: Keep the Spider Houses in generation, but only place Skulltula tokens there.
    anything: Any item can be given by any Skulltula, and tokens can be found anywhere in any world.
    ignore: Remove the Spider Houses from generation entirely, lowering the hint percentage and removing them from the spoiler log."""
    display_name = "Skullsanity"
    option_vanilla = 0
    option_anything = 1
    option_ignore = 2
    default = 0


class Shopsanity(Choice):
    """Choose whether shops and their items are shuffled into the pool.
    This includes Trading Post, Bomb Shop, Goron Shop, and Zora Shop, along with the Gorman Ranch and Milk Bar purchases.
    
    vanilla: Shop items are not shuffled.
    enabled: Every item in shops are shuffled, with alternate shops sharing the same items.
    advanced: Every single item in shops are shuffled, including the alternate Night Trading Post and Spring Goron Shop."""
    display_name = "Shopsanity"
    option_vanilla = 0
    option_enabled = 1
    option_advanced = 2
    default = 0

class Scrubsanity(Toggle):
    """Choose whether to shuffle Business Scrub purchases."""
    display_name = "Shuffle Business Scrub Purchases"

class ShopPrices(Choice):
    """Choose how expensive shop items are.
    These only apply to the main shops of the game.
    This has no effect if shopsanity is disabled.
    
    vanilla: Shop items have their normal prices.
    free: All shop items are free and cost 0 Rupees.
    cheap: Shop items vary in price but can all be purchased with the starting wallet.
    expensive: Shop items vary in price but may require the Adult's Wallet. No shop items will require the Giant's Wallet.
    offensive: Shop items vary in price but may require the Adult's Wallet and sometimes even the Giant's Wallet."""
    display_name = "Shop Prices"
    option_vanilla = 0
    option_free = 1
    option_cheap = 2
    option_expensive = 3
    option_offensive = 4
    default = 0


class Cowsanity(Toggle):
    """Choose whether to shuffle Cows."""
    display_name = "Shuffle Cows"


class ShuffleGreatFairyRewards(Toggle):
    """Choose whether to shuffle Great Fairy rewards."""
    display_name = "Shuffle Great Fairy Rewards"


class RequiredStrayFairies(Range):
    """The number of Stray Fairies needed to get the reward from their respective Great Fairy (excluding North Clock Town's Great Fairy of Magic).
    All 15 Stray Fairies from each dungeon are still shuffled into the item pool regardless of the selection.
    Valid amounts are within the range 0-15."""
    display_name = "Required Stray Fairies"
    range_start = 0
    range_end = 15
    default = 15


class Fairysanity(Toggle):
    """Choose whether Stray Fairies are shuffled into the pool."""
    display_name = "Fairysanity"


class Keysanity(Toggle):
    """Choose whether Small Keys are shuffled into the pool or placed in their vanilla locations."""
    display_name = "Keysanity"

class BossKeysanity(Toggle):
    """Choose whether Boss Keys are shuffled into the pool or placed in their vanilla locations."""
    display_name = "BossKeysanity"    


class CuriostityShopTrades(Toggle):
    """Choose whether to shuffle the rupees given for trading bottled items at the Curiostity Shop."""
    display_name = "Curiostity Shop Trades"


class IntroChecks(Toggle):
    """Choose whether to shuffle the checks normally found before entering the Clock Tower.
    
    A way backwards through these areas has been added through the stone door at the bottom of the Clock Tower Interior."""
    display_name = "Enable Intro Checks"


class StartWithConsumables(DefaultOnToggle):
    """Choose whether to start with basic consumables (99 rupees, 10 deku sticks, 20 deku nuts)."""
    display_name = "Start With Consumables"


class PermanentChateauRomani(DefaultOnToggle):
    """Choose whether the Chateau Romani stays even after a reset."""
    display_name = "Permanent Chateau Romani"


class StartWithInvertedTime(Toggle):
    """Choose whether time starts out inverted at Day 1, even after a reset."""
    display_name = "Reset With Inverted Time"


class ReceiveFilledWallets(DefaultOnToggle):
    """Choose whether you receive wallets pre-filled (not including the starting wallet)."""
    display_name = "Receive Filled Wallets"


class MagicIsATrap(Toggle):
    """Set whether to preserve the vanilla bug where you are able to use certain magic items and abilities without magic.
    Once you receive magic, those items and abilities will begin to reduce magic normally.
    
    (No logical implications)"""
    display_name = "Magic Is a Trap"


class DamageMultiplier(Choice):
    """Adjust the amount of damage taken."""
    display_name = "Damage Multiplier"
    option_half = 0
    option_normal = 1
    option_double = 2
    option_quad = 3
    option_ohko = 4
    default = 1

class DeathBehavior(Choice):
    """Change what happens when you die.
    
    vanilla: The normal death cutscene plays when you die.
    fast: The death cutscene is massively sped up.
    moon_crash: Triggers a moon crash and restarts the current cycle."""
    display_name = "Death Behavior"
    option_vanilla = 0
    option_fast = 1
    option_instant = 2
    option_moon_crash = 3
    default = 0


class LinkTunicColor(OptionList):
    """Choose a color for Link's tunic."""
    display_name = "Link Tunic Color"
    default = [30, 105, 27]


@dataclass
class MMROptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    logic_difficulty: LogicDifficulty
    majora_remains_required: MajoraRemainsRequired
    moon_remains_required: MoonRemainsRequired
    camc: CAMC
    swordless: Swordless
    shieldless: Shieldless
    start_with_soaring: StartWithSoaring
    starting_hearts: StartingHeartQuarters
    starting_hearts_are_containers_or_pieces: StartingHeartsAreContainersOrPieces
    shuffle_regional_maps: ShuffleRegionalMaps
    shuffle_boss_remains: ShuffleBossRemains
    remains_allow_boss_warps: BossWarpsWithRemains
    shuffle_spiderhouse_reward: ShuffleSpiderHouseReward
    required_skull_tokens: RequiredSkullTokens
    skullsanity: Skullsanity
    shopsanity: Shopsanity
    scrubsanity: Scrubsanity
    shop_prices: ShopPrices
    cowsanity: Cowsanity
    shuffle_great_fairy_rewards: ShuffleGreatFairyRewards
    required_stray_fairies: RequiredStrayFairies
    fairysanity: Fairysanity
    keysanity: Keysanity
    bosskeysanity: BossKeysanity
    curiostity_shop_trades: CuriostityShopTrades
    intro_checks: IntroChecks
    start_with_consumables: StartWithConsumables
    permanent_chateau_romani: PermanentChateauRomani
    start_with_inverted_time: StartWithInvertedTime
    receive_filled_wallets: ReceiveFilledWallets
    magic_is_a_trap: MagicIsATrap
    damage_multiplier: DamageMultiplier
    death_behavior: DeathBehavior
    death_link: DeathLink
    link_tunic_color: LinkTunicColor
