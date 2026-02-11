from dataclasses import dataclass
from typing import TYPE_CHECKING

from Options import (
    Choice,
    DeathLink,
    DefaultOnToggle,
    ItemDict,
    OptionGroup,
    OptionSet,
    PerGameCommonOptions,
    Range,
    StartInventoryPool,
    Toggle,
    Visibility,
)

from .constants import ALL_TRICKS, TMCItem, TMCTricks

if TYPE_CHECKING:
    from . import MinishCapWorld


class DungeonItem(Choice):
    value: int
    # EternalCode's note: I want to experiment with a `closed` for small/big keys to actually remove them from the pool
    #   entirely and keep the doors closed. All locations behind them would be removed & inaccessible.
    # Elements would need to be forced to be anywhere under this setting.
    # option_closed = 0 # New compared to TMCR (compass/map removed from pool, locations behind keys inaccessible,
    #   I doubt many would use this but it'd be relatively simple to implement)
    # option_open = 1 # TMCR Removed (compass/map start_inventory, keys removed from pool, doors are open at the
    #   start of the save)
    # option_vanilla = 2
    option_own_dungeon = 3
    # option_own_region = 4
    # option_any_dungeon = 5
    # option_any_region = 6
    # 7 reserved for option specific settings (small key = universal)
    option_anywhere = 8
    alias_true = 8
    alias_false = 3


class FusionAccess(Choice):
    visibility = Visibility.none  # Temporary until fusion logic is written
    value: int
    option_closed = 0
    option_vanilla = 1
    option_combined = 2
    option_open = 3


class RedFusionAccess(Choice):
    """How/when are the Red Kinstone Fusions accessible?

    - Closed: Red Kinstones aren't in the item pool and none of their fusions are accessible
    - Vanilla: Red Kinstones are added to the item pool and their fusions must be completed as normal
    - Combined: Same as Vanilla except all Red Fusions are changed to request only 'Kinstone Red W'
    - Open: Red Kinstones aren't in the item pool and all of their fusions are accessible
    """

    visibility = Visibility.none
    rich_text_doc = True
    value: int
    # option_closed = 0
    # option_vanilla = 1
    # option_combined = 2
    option_open = 3
    default = option_open


class BlueFusionAccess(Choice):
    """How/when are the Blue Kinstone Fusions accessible?

    - Closed: Blue Kinstones aren't in the item pool and none of their fusions are accessible
    - Vanilla: Blue Kinstones are added to the item pool and their fusions must be completed as normal
    - Combined: Same as Vanilla except all Blue Fusions are changed to request only 'Kinstone Blue L'
    - Open: Blue Kinstones aren't in the item pool and all of their fusions are accessible
    """

    visibility = Visibility.none
    rich_text_doc = True
    value: int
    # option_closed = 0
    # option_vanilla = 1
    # option_combined = 2
    option_open = 3
    default = option_open


class GreenFusionAccess(Choice):
    """How/when are the Green Kinstone Fusions accessible?

    - Closed: Green Kinstones aren't in the item pool and none of their fusions are accessible
    - Vanilla: Green Kinstones are added to the item pool and their fusions must be completed as normal
    - Combined: Same as Vanilla except all Green Fusions are changed to request only 'Green Kinstone ['
    - Open: Green Kinstones aren't in the item pool and all of their fusions are accessible
    """

    visibility = Visibility.none
    rich_text_doc = True
    value: int
    # option_closed = 0
    # option_vanilla = 1
    # option_combined = 2
    option_open = 3
    default = option_open


class GoldFusionAccess(Choice):
    """How/when are the Gold Kinstone Fusions accessible?

    - Closed: Gold Kinstones aren't in the item pool and none of their fusions are accessible
    - Vanilla: Gold Kinstones are added to the item pool and their fusions must be completed as normal
    - Combined: Same as Vanilla except all Gold Fusions are changed to request only 'Kinstone Cloud Tops'
    - Open: Gold Kinstones aren't in the item pool and all of their fusions are accessible
    """

    visibility = Visibility.none
    rich_text_doc = True
    value: int
    # option_closed = 0
    option_vanilla = 1
    # option_combined = 2
    # option_open = 3
    default = option_vanilla


class ProgressiveSword(DefaultOnToggle):
    """Should swords be given progressively? You'll receive the swords in the following order:

    - Smith's Sword
    - White Sword
    - White Sword (Two Elements)
    - White Sword (Three Elements)
    - Four Sword

    When disabled you'll need the exact sword to create its normal number of clones.
    E.g. You'll need White Sword (Two Elements) to only create 2 clones even if already have Four Sword.
    """

    display_name = "Progressive Sword"
    rich_text_doc = True


class ProgressiveBow(DefaultOnToggle):
    """Should bows be given progressively?"""

    display_name = "Progressive Bow"


class ProgressiveBoomerang(DefaultOnToggle):
    """Should boomerangs be given progressively?"""

    display_name = "Progressive Boomerang"


class ProgressiveShield(DefaultOnToggle):
    """Should shields be given progressively?"""

    display_name = "Progressive Shield"


class ProgressiveScroll(DefaultOnToggle):
    """Should spin scrolls be given progressively? You'll pick up the spin scrolls in the following order:

    - Spin Attack
    - Fast Spin
    - Fast Split
    - Great Spin
    - Long Spin
    """

    display_name = "Progressive Spin Scroll"
    rich_text_doc = True


class Rupeesanity(Toggle):
    """Add all rupees locations to the pool to be randomized.
    This setting will not shuffle Rupees that also belong to another pool such as underwater rupees.
    """

    display_name = "Rupee-sanity"
    rich_text_doc = True


class ShufflePots(Toggle):
    """Add all special pots that drop a unique item to the pool. Includes the LonLon Ranch Pot."""

    display_name = "Shuffle Pots"


class ShuffleDigging(Toggle):
    """Add all dig spots that drop a unique item to the pool."""

    display_name = "Shuffle Digging"


class ShuffleUnderwater(Toggle):
    """Add all underwater items to the pool. Includes the ToD underwater pot"""

    display_name = "Shuffle Underwater"


class ShuffleGoldEnemies(Toggle):
    """Add the drops from the 9 golden enemies to the pool."""

    display_name = "Shuffle Gold Enemy Drops"


class ObscureSpots(Toggle):
    """Add all special pots, dig spots, etc. that drop a unique item to the pool."""

    display_name = "Obscure Spots"


class ShuffleElements(Choice):
    # EternalCode's Note: I'd like to experiment with ElementShuffle extending DungeonItem choice, just for consistency.
    # The settings would be slightly repurposed to something like this
    # `closed`: elements removed from pool, goal_elements forced to 0
    # `open`: elements added to start inventory (pretty useless all things considered)
    # `vanilla`: elements in their usual dungeon prize location
    # `own_dungeon`: place an element anywhere in its usual dungeon
    # `own_region`: place element in the vicinity of its usual dungeon
    # `any_dungeon`: place elements anywhere in any dungeon
    # `any_region`: place elements anywhere in the vicinity of any dungeon
    # `dungeon_prize` (default): Elements are shuffled between the 6 dungeon prizes
    # `anywhere`: full random
    """Lock elements to specific locations.

    - 'Vanilla': Elements are in the same dungeons as vanilla
    - 'Dungeon Prize' (false/default): Elements are shuffled between the 6 dungeon prizes
    - 'Anywhere' (true): Elements are in completely random locations
    """

    display_name = "Element Shuffle"
    rich_text_doc = True
    default = 7
    option_vanilla = 2
    option_dungeon_prize = 7
    option_anywhere = 8
    alias_true = 8
    alias_false = 7

    @property
    def on_prize(self) -> bool:
        return self.value in {self.option_vanilla, self.option_dungeon_prize}


class SmallKeys(DungeonItem):
    """
    - 'Own Dungeon' (false/default): Randomized within the dungeon they're normally found in
    - 'Anywhere' (true): Items are in completely random locations

    *Note*: If using anything other than "anywhere" and you include small keys in start_inventory_from_pool,
    you may get the warning "tried to remove items from their pool that don't exist". This is expected, the keys
    have safely been added to your inventory from the pool.
    """

    display_name = "Small Key Shuffle"
    rich_text_doc = True
    default = DungeonItem.option_own_dungeon


class BigKeys(DungeonItem):
    """
    - 'Own Dungeon' (false/default): Randomized within the dungeon they're normally found in
    - 'Anywhere' (true): Items are in completely random locations

    *Note*: If using anything other than "anywhere" and you include big keys in start_inventory_from_pool,
    you may get the warning "tried to remove items from their pool that don't exist". This is expected, the keys
    have safely been added to your inventory from the pool.
    """

    display_name = "Big Key Shuffle"
    rich_text_doc = True
    default = DungeonItem.option_own_dungeon


class DungeonMaps(DungeonItem):
    """
    - 'Own Dungeon' (false/default): Randomized within the dungeon they're normally found in
    - 'Anywhere' (true): Items are in completely random locations
    - 'Start With': Items are automatically added to the start_inventory_from_pool

    *Note*: If using anything other than "anywhere" and you include dungeon maps in start_inventory_from_pool,
    you may get the warning "tried to remove items from their pool that don't exist". This is expected, the maps
    have safely been added to your inventory from the pool.
    """

    display_name = "Dungeon Maps Shuffle"
    rich_text_doc = True
    option_start_with = 1
    default = DungeonItem.option_own_dungeon


class DungeonCompasses(DungeonItem):
    """
    - 'Own Dungeon' (false/default): Randomized within the dungeon they're normally found in
    - 'Anywhere' (true): Items are in completely random locations
    - 'Start With': Items are automatically added to the start_inventory_from_pool

    *Note*: If using anything other than "anywhere" and you include dungeon compasses in start_inventory_from_pool,
    you may get the warning "tried to remove items from their pool that don't exist". This is expected, the compass
    has safely been added to your inventory from the pool.
    """

    display_name = "Dungeon Compasses Shuffle"
    rich_text_doc = True
    option_start_with = 1
    default = DungeonItem.option_own_dungeon


class DungeonWarp(Choice):
    option_none = 0
    option_blue = 0b01
    option_red = 0b10
    option_both = option_blue | option_red

    @property
    def has_blue(self) -> bool:
        return self.value & self.option_blue

    @property
    def has_red(self) -> bool:
        return self.value & self.option_red


class WarpDWS(DungeonWarp):
    """Whether you should start with the Blue/Red warps for DeepWood Shrine"""

    display_name = "DeepWood Shrine Warps"
    internal_abbr = "DWS"


class WarpCoF(DungeonWarp):
    """Whether you should start with the Blue/Red warps for Cave of Flames"""

    display_name = "Cave of Flames"
    internal_abbr = "CoF"


class WarpFoW(DungeonWarp):
    """Whether you should start with the Blue/Red warps for Fortress of Winds"""

    display_name = "Fortress of Winds"
    internal_abbr = "FoW"


class WarpToD(DungeonWarp):
    """Whether you should start with the Blue/Red warps for Temple of Droplets"""

    display_name = "Temple of Droplets"
    internal_abbr = "ToD"


class WarpPoW(DungeonWarp):
    """Whether you should start with the Blue/Red warps for Palace of Winds"""

    display_name = "Palace of Winds"
    internal_abbr = "PoW"


class WarpDHC(DungeonWarp):
    """Whether you should start with the Blue/Red warps for Dark Hyrule Castle"""

    display_name = "Dark Hyrule Castle"
    internal_abbr = "DHC"


class Traps(Toggle):
    """Traps may be placed around the world. Traps for local items will have their
    sprite randomized to a local item before pickup. When picked up it'll turn
    into an exclamation mark (!) and activate a specific trap such as spawning
    enemies, setting you on fire, freezing you, etc.
    """

    display_name = "Traps Enabled"


class Goal(Choice):
    """
    - 'Vaati' (default): Kill Vaati to goal. dhc_access and the ped requirements change how soon you can reach Vaati.
    - 'Pedestal': Complete Pedestal to goal. The ped requirements change what's needed.
    """

    display_name = "Goal"
    rich_text_doc = True
    option_vaati = 0
    option_pedestal = 1
    # option_requirements = 2  'Requirements': Goal the moment each ped requirement is met. No need to enter sanctuary.


class DHCAccess(Choice):
    """
    When should DHC be accessible?
    If your goal is Pedestal then dhc_access can't be pedestal and will default to closed instead.

    - 'Closed' (false): DHC is never accessible. If your goal is Vaati, the room after pedestal goes straight to Vaati.
    - 'Pedestal' (default): DHC is locked until pedestal is completed.
    - 'Open' (true): DHC is accessible from the beginning. If your goal is Pedestal, activate pedestal from within DHC.
    """

    display_name = "DHC Access"
    rich_text_doc = True
    option_closed = 0
    option_pedestal = 1
    option_open = 2
    alias_false = 0
    alias_true = 2
    default = 1


class PedDungeons(Range):
    """How many dungeons are required to activate Pedestal?"""

    display_name = "Required Dungeons to Pedestal"
    rich_text_doc = True
    default = 0
    range_start = 0
    range_end = 6


class PedElements(Range):
    """How many elements are required to activate Pedestal?"""

    display_name = "Required Elements to Pedestal"
    rich_text_doc = True
    default = 4
    range_start = 0
    range_end = 4


class PedSword(Range):
    """Which sword tier is required to activate Pedestal?
    When Progressive Sword is disabled, requires the exact tier listed here.

    Ex. If set to 3, pedestal would specifically require 'White Sword (Two Elements)',
    neither 'White Sword (Three Elements)' nor 'Four Sword' would count towards the pedestal."""

    display_name = "Required Swords to Pedestal"
    rich_text_doc = True
    default = 5
    range_start = 0
    range_end = 5


class PedFigurines(Range):
    """How many figurines are required to activate Pedestal?"""

    display_name = "Required Figurines to Pedestal"
    default = 0
    range_start = 0
    range_end = 136


class FigurineAmount(Range):
    """How many figurines are added to the pool?
    Should not be lower than ped_figurines, otherwise it will be overridden to match ped_figurines.
    """

    display_name = "Figurines in Pool"
    default = 0
    range_start = 0
    range_end = 136


class EarlyWeapon(Toggle):
    """Force a weapon to be in your sphere 1.
    The weapon placed will be random based off the enabled `weapon` options.
    Swords will always be one of the possible weapons placed.
    """

    display_name = "Early Weapon"


class RandomBottleContents(Toggle):
    """Put random contents into the shuffled bottles, these contents are never considered in logic"""

    display_name = "Random Bottles Contents"


class DeathLinkGameover(Toggle):
    """If disabled, deathlinks are sent when reaching 0HP, before a fairy is used. Received deathlinks will drop you to
    0HP, using a fairy if you have one.

    If enabled, deathlinks are only sent when reaching the gameover screen. Received deathlinks will also send you
    straight to a gameover, fairy or not.
    """

    display_name = "Deathlink is Gameover"


class WeaponBomb(Choice):
    """Bombs can damage nearly every enemy, Bombs are never considered for Simon Simulations, and Golden Enemies.

    - 'No': Bombs are not considered as Weapons.
    - 'Yes': Bombs are considered as weapons for most regular enemy fights.
    - 'Yes + Bosses': Bombs are considered as weapons for most enemy fights. Fighting Green/Blu Chu, Madderpillars
      and Darknuts require only 10 bomb bag. Gleerok, Mazaal and Scissor Beetles require at least 30 bomb bag.
      Octo and Gyorg cannot be defeated with bombs.
    """

    display_name = "Bombs are considered Weapons"
    rich_text_doc = True
    default = 0
    option_no = 0
    option_yes = 1
    option_yes_boss = 2
    alias_true = 1
    alias_false = 0


class WeaponBow(Toggle):
    """Bow can damage most enemies, many enemies are very resilient to damage. Chu Bosses and Darknuts are Immune.

    - 'false': Bows are not considered as Weapons.
    - 'true': Bows are considered as weapons for most enemy fights.

    Bows are never considered for Chu Bossfights, Darknuts, Scissor Beetles, Madderpillar, Wizzrobes, Simon Simulations,
    and Golden Enemies.
    """

    display_name = "Bows are considered Weapons"


class WeaponGust(Toggle):
    """Gust Jar can suck up various enemies like Ghini(Ghosts) and Beetles (The things that grab onto link).
    It can also grab objects and fire them like projectiles to kill enemies, some enemies or parts of enemies can be
    used as projectiles such as Helmasaurs and Stalfos.

    - 'false': Gust Jar is never considered for killing enemies.
    - 'true': Gust Jar is considered as weapons for all enemies that get sucked up by it, you are never expected to use
      objects as projectiles to kill enemies.
    """

    display_name = "Gust jar is considered a Weapon"


class WeaponLantern(Toggle):
    """The lit Lantern can instantly kill Wizzrobes by walking through them.

    - 'false': Lantern is not considered as a Weapon.
    - 'true': Lantern is considered as a weapon for fighting Wizzrobes.
    """

    display_name = "Lantern is considered a Weapon"


class Tricks(OptionSet):
    """
    - bombable_dust: Bombs may be required to blow away dust instead of Gust Jar
    - crenel_mushroom_gust_jar: The mushroom near the edge of a cliff on Mt Crenel may be required to be grabbed with
      the gust jar to climb higher
    - light_arrows_break_objects: A charged light arrow shot may be required to destroy obstacles like pots or small
      trees
    - bobombs_destroy_walls: Either a Sword or the Gust Jar may be required to blow up walls near Bobombs
    - like_like_cave_no_sword: Opening the chests in the digging cave in Minish Woods, guarded by a pair of LikeLikes,
      may be required without a weapon
    - boots_skip_town_guard: A very precise boot dash may be required to skip the guard blocking the west exit of town
    - beam_crenel_switch: A switch across a gap on Mt Crenel must be hit to extend a bridge to reach cave of flames,
      hitting it with a sword beam may be required
    - down_thrust_spikey_beetle: Spikey Beetles can be flipped over with a down thrust, which may be required to kill
      them
    - dark_rooms_no_lantern: Dark rooms may require being traversed without the lantern. Link always has a small light
      source revealing his surroundings
    - cape_extensions: Some larger gaps across water can be crossed by extending the distance you can jump (Release cape
      after the hop, then press and hold the glide)
    - lake_minish_no_boots: Lake hylia can be explored as minish without using the boots to bonk a tree by jumping down
      from the middle island
    - cabin_swim_no_lilypad: Lake Cabin has a path used to enter as minish, the screen transition can be touched by
      swimming into it
    - cloud_sharks_no_weapons: The Sharks in cloud tops can be killed by standing near the edge and watching them jump
      off
    - fow_pot_gust_jar: A pot near the end of Fortress can be grabbed with the gust jar through a wall from near the
      beginning of the dungeon
    - pow_2f_no_cane: After climbing the first clouds of Palace, a moving platform can be reached with a precise jump
    - pot_puzzle_no_bracelets: The Minish sized pot puzzle in Palace can be avoided by hitting the switch that drops the
      item at a later point in the dungeon
    - dhc_cannons_no_four_sword: The Cannon puzzle rooms of DHC can be completed without the four sword by using a well
      timed bomb strat and sword slash
    - dhc_pads_no_four_sword: The clone puzzles that press down four pads in DHC can be completed with less clones by
      shuffling across the pads
    - dhc_switches_no_four_sword: The clone puzzle that slashes 4 switches in DHC can be completed with a well placed
      spin attack
    """

    display_name = "Tricks"
    rich_text_doc = True
    valid_keys = ALL_TRICKS


class WindCrestCrenel(Toggle):
    """Whether you should start with the Mount Crenel Wind Crest"""

    display_name = "Mount Crenel Wind Crest"


class WindCrestFalls(Toggle):
    """Whether you should start with the Veil Falls Wind Crest"""

    display_name = "Veil Falls Wind Crest"


class WindCrestClouds(Toggle):
    """Whether you should start with the Cloud Tops Wind Crest"""

    display_name = "Cloud Tops Wind Crest"


class WindCrestSwamp(Toggle):
    """Whether you should start with the Castor Wilds Wind Crest"""

    display_name = "Castor Wilds Wind Crest"


class WindCrestTown(Toggle):
    """Whether you should start with the Hyrule Town Wind Crest"""

    display_name = "Hyrule Town Wind Crest"


class WindCrestLake(Toggle):
    """Whether you should start with the Hylia Lake Wind Crest"""

    display_name = "Hylia Lake Wind Crest"


class WindCrestSmith(Toggle):
    """Whether you should start with the South Field Wind Crest"""

    display_name = "South Field Wind Crest"


class WindCrestMinish(Toggle):
    """Whether you should start with the Minish Woods Wind Crest"""

    display_name = "Minish Woods Wind Crest"


class PedReward(Choice):
    """What item should you get as soon as you complete the pedestal requirements?"""

    display_name = "Pedestal Requirement Reward"
    option_none = 0
    option_dhc_big_key = 1
    option_random_item = 2
    alias_false = option_none
    alias_true = option_dhc_big_key


class CuccoRounds(Range):
    """How many rounds of the cucco catching minigame will be shuffled and playable?
    Rounds 1-9 are accessible from Sphere 1, Round 10 is accessible with either Roc's Cape or Flippers.
    Rounds are always included from the end to ensure the Round 10 reward is always accessible.
    Ex, if you play with 3 rounds, Rounds 8-10 are playable.
    """

    display_name = "# of Cucco Rounds"
    range_start = 0
    range_end = 10
    default = 1


class GoronSets(Range):
    """
    How many sets of items do you want to purchase from the Goron Shop in town?
    There are 5 total sets with 3 items each.
    """

    display_name = "# of Goron Merchant Sets"
    range_start = 0
    range_end = 5
    default = 0


class GoronJPPrices(Toggle):
    """Should the Goron Merchant use JP/US prices instead of EU prices for the item sets. They are as follows:
    EU 1st set: 200/100/50
    EU 2nd set: 300/200/100
    EU 3rd set: 400/300/200
    EU 4th set: 500/400/300
    EU 5th set: 600/500/400
    JP all sets: 300/200/50
    """

    display_name = "Goron Merchant JP/US Prices"


class ExtraShopItem(Toggle):
    """Should Stockwell sell an extra item (same as the extra bomb bag from US/JP versions) for 600 rupees?"""

    display_name = "Extra Shop Item"


class NonElementDungeons(Choice):
    """Should dungeons that don't have elements restrict the items that can be placed in them?
    Only takes effect when shuffle_elements is dungeon_prize or vanilla and ped_dungeons is 4 or less.

    Standard: Non-Element dungeons are filled just like any other location with no restrictions.
    Excluded: Non-Element dungeons are automatically added to the excluded_locations list, only placing filler inside.
    """

    display_name = "Non-Element Dungeons"

    option_standard = 0
    # option_unrequired = 1
    option_excluded = 2
    # option_region_unrequired = 3
    # option_region_excluded = 4
    alias_true = option_standard
    alias_false = option_excluded
    default = option_standard


class StartingHearts(Range):
    """How much health should you start with?
    If you start with 10 hearts or more, Heart Containers & Piece of Hearts will be Useful instead of Progression."""

    display_name = "Starting Hearts"
    range_start = 1
    range_end = 20
    default = 3


class HeartContainerAmount(Range):
    """How many Heart Containers should be placed in the world?
    If there are enough Heart Containers to reach 10 Hearts without any Piece of Hearts,
    then Piece of Hearts will be marked Useful instead of Progression"""

    display_name = "Heart Containers"
    range_start = 0
    range_end = 20
    default = 6


class PieceOfHeartAmount(Range):
    """How many hearts worth of Piece of Hearts should be placed in the world?
    If there isn't enough Starting HP, Heart Containers & Piece of Hearts to reach 10 Hearts for the Lake Hylia Dojo,
    then Lake Hylia Dojo will be disabled.
    """

    display_name = "Piece of Hearts"
    range_start = 0
    range_end = 20
    default = 11


class Biggoron(Choice):
    """Should the biggoron location be enabled and if so what should the requirement be?"""

    display_name = "Shuffle Biggoron"
    option_disabled = 0
    option_shield = 1
    option_mirror_shield = 2
    default = 0
    alias_false = option_disabled
    alias_true = option_shield


class FillerItemsDistribution(ItemDict):
    """How frequently should each filler item appear? Traps will be removed automatically if they're disabled."""

    visibility = Visibility.complex_ui | Visibility.template
    display_name = "Filler Items Distribution"
    default = {
        TMCItem.RUPEES_1: 36,
        TMCItem.RUPEES_5: 49,
        TMCItem.RUPEES_20: 53,
        TMCItem.RUPEES_50: 25,
        TMCItem.RUPEES_100: 18,
        TMCItem.RUPEES_200: 15,
        TMCItem.HEART_REFILL: 29,
        TMCItem.BOMB_REFILL_5: 34,
        TMCItem.BOMB_REFILL_10: 22,
        TMCItem.BOMB_REFILL_30: 16,
        TMCItem.ARROW_REFILL_5: 34,
        TMCItem.ARROW_REFILL_10: 22,
        TMCItem.ARROW_REFILL_30: 16,
        TMCItem.TRAP_ICE: 8,
        TMCItem.TRAP_FIRE: 8,
        TMCItem.TRAP_ZAP: 8,
        TMCItem.TRAP_BOMB: 8,
        TMCItem.TRAP_MONEY: 5,
        TMCItem.TRAP_STINK: 8,
        TMCItem.TRAP_ROPE: 8,
        TMCItem.TRAP_BAT: 8,
        TMCItem.TRAP_LIKE: 8,
        TMCItem.TRAP_CURSE: 5,
    }


class ReplicaToDBossDoor(Toggle):
    """Add a replica Boss Door to the Temple of Droplets Main Hall.
    This only makes a difference if you have at least one ToD warp enabled or are using glitches.
    Disabling allows the Boss Door Clip and Octo Clip (if the Boss Door has not been opened) glitches to behave like they do in the vanilla game.
    """

    display_name = "Replica ToD Boss Door"
    rich_text_doc = True
    default = True


class OcarinaOnSelect(Toggle):
    """Should your Select button be bound to use the Ocarina? Prevents Ezlo Buffering glitches"""

    display_name = "Ocarina on Select"
    rich_text_doc = True
    default = True


class BootsOnL(Toggle):
    """Should your L button be bound to use the Pegasus Boots?"""

    display_name = "Boots on L"
    rich_text_doc = True
    default = True


class BootsAsMinish(Toggle):
    """Should the Pegasus Boots still work while you're minish size?"""

    display_name = "Boots as Minish"
    rich_text_doc = True
    default = False


class BigOctorokManipulation(Toggle):
    """Should Big Octorok automatically skip the Ink & Charge phases.
    This is meant to produce a similar result to the speedrunning RNG manipulation.
    Performing the RNG manipulation trick may be more difficult while receiving items from other worlds.
    """

    display_name = "Big Octorok Manipulation"
    rich_text_doc = True
    default = True


class RemoteItems(Toggle):
    """
    Should all randomized items be handled through AP? This will require a connection to a server during all gameplay.
    If you crash or lose your savefile, all items should be sent back to you. (Dungeons still have to re-cleared)
    When finding items placed in world, your items will use the remote item sprite instead of their usual sprite.
    """

    display_name = "Remote Items"
    rich_text_doc = True


@dataclass
class MinishCapOptions(PerGameCommonOptions):
    # AP settings / DL settings
    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink
    death_link_gameover: DeathLinkGameover
    # Goal Settings
    goal: Goal
    dhc_access: DHCAccess
    ped_elements: PedElements
    ped_swords: PedSword
    ped_dungeons: PedDungeons
    ped_figurines: PedFigurines
    figurine_amount: FigurineAmount
    # Fusion Settings
    gold_fusion_access: GoldFusionAccess
    red_fusion_access: RedFusionAccess
    green_fusion_access: GreenFusionAccess
    blue_fusion_access: BlueFusionAccess
    # Pool Settings
    dungeon_small_keys: SmallKeys
    dungeon_big_keys: BigKeys
    dungeon_maps: DungeonMaps
    dungeon_compasses: DungeonCompasses
    ped_reward: PedReward
    shuffle_elements: ShuffleElements
    non_element_dungeons: NonElementDungeons
    rupeesanity: Rupeesanity
    shuffle_pots: ShufflePots
    shuffle_digging: ShuffleDigging
    shuffle_underwater: ShuffleUnderwater
    shuffle_gold_enemies: ShuffleGoldEnemies
    shuffle_biggoron: Biggoron
    cucco_rounds: CuccoRounds
    goron_sets: GoronSets
    goron_jp_prices: GoronJPPrices
    extra_shop_item: ExtraShopItem
    traps_enabled: Traps
    random_bottle_contents: RandomBottleContents
    filler_items_distribution: FillerItemsDistribution
    # Weapon Settings
    early_weapon: EarlyWeapon
    weapon_bomb: WeaponBomb
    weapon_bow: WeaponBow
    weapon_gust: WeaponGust
    weapon_lantern: WeaponLantern
    progressive_sword: ProgressiveSword
    progressive_bow: ProgressiveBow
    progressive_boomerang: ProgressiveBoomerang
    progressive_shield: ProgressiveShield
    progressive_scroll: ProgressiveScroll
    # Difficulty
    starting_hearts: StartingHearts
    heart_containers: HeartContainerAmount
    piece_of_hearts: PieceOfHeartAmount
    # Logic Settings
    dungeon_warp_dws: WarpDWS
    dungeon_warp_cof: WarpCoF
    dungeon_warp_fow: WarpFoW
    dungeon_warp_tod: WarpToD
    dungeon_warp_pow: WarpPoW
    dungeon_warp_dhc: WarpDHC
    wind_crest_crenel: WindCrestCrenel
    wind_crest_falls: WindCrestFalls
    wind_crest_clouds: WindCrestClouds
    wind_crest_castor: WindCrestSwamp
    wind_crest_south_field: WindCrestSmith
    wind_crest_minish_woods: WindCrestMinish
    # wind_crest_town: WindCrestTown
    # wind_crest_lake: WindCrestLake
    tricks: Tricks
    remote_items: RemoteItems
    ocarina_on_select: OcarinaOnSelect
    boots_on_l: BootsOnL
    boots_as_minish: BootsAsMinish
    big_octo_manipulation: BigOctorokManipulation
    replica_tod_boss_door: ReplicaToDBossDoor


def get_option_data(world: "MinishCapWorld"):
    world_version = None
    options = world.options
    """Template for the options that will likely be added in the future.
    Intended for trackers to properly match the logic between the standalone randomizer (TMCR) and AP
    """
    vaati_dhc_map = {
        (Goal.option_vaati, DHCAccess.option_closed): 0,
        (Goal.option_vaati, DHCAccess.option_pedestal): 1,
        (Goal.option_vaati, DHCAccess.option_open): 2,
        (Goal.option_pedestal, DHCAccess.option_closed): 3,
        (Goal.option_pedestal, DHCAccess.option_open): 5,
    }

    try:
        world_version = world.world_version.as_simple_string()
    except AttributeError:
        world_version = "0.3.0"

    return {
        "version": world_version,
        "goal_vaati": int(options.goal.value == Goal.option_vaati),
        "goal_dungeons": options.ped_dungeons.value,  # 0-6
        "goal_swords": options.ped_swords.value,  # 0-5
        "goal_elements": options.ped_elements.value,  # 0-4
        "goal_figurines": options.ped_figurines.value,  # 0-136
        "goal_vaati_dhc": vaati_dhc_map[(options.goal.value, options.dhc_access.value)],
        "shuffle_heart_pieces": 1,
        "shuffle_rupees": options.rupeesanity.value,
        "shuffle_pedestal": 0,
        "shuffle_biggoron": options.shuffle_biggoron.value,  # 0 = Disabled, 1 = Requires Shield, 2 = Requires Mirror Shield
        "kinstones_gold": options.gold_fusion_access.value,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_red": options.red_fusion_access.value,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_blue": options.blue_fusion_access.value,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "kinstones_green": options.green_fusion_access.value,  # 0 = Closed, 1 = Vanilla, 2 = Combined, 3 = Open
        "grabbables": 1,  # 0 = Not Allowed, 1 = Allowed, 2 = Required, 3 = Required (Hard)
        "open_world": 0,  # No, Yes
        "open_wind_tribe": 0,
        "open_tingle_brothers": 0,
        "open_library": 0,
        "extra_shop_item": options.extra_shop_item.value,
        "wind_crest_town": 1,
        "wind_crest_lake": 1,
        "weapon_bombs": options.weapon_bomb.value,  # No, Yes, Yes + Bosses
        "weapon_bows": options.weapon_bow.value,
        "weapon_gust_jar": options.weapon_gust.value,  # No, Yes
        "weapon_lantern": options.weapon_lantern.value,
        "weapon_mirror": 0,
        "entrance_rando": 0,  # 0 = Disabled, 1 = Dungeons, 2 = Regions?, 3 = Rooms? (? = subject to change)
        "trick_mitts_farm_rupees": 0,  # No, Yes
        "trick_bombable_dust": int(TMCTricks.BOMB_DUST in options.tricks),
        "trick_crenel_mushroom_gust_jar": int(TMCTricks.MUSHROOM in options.tricks),
        "trick_light_arrows_break_objects": int(TMCTricks.ARROWS_BREAK in options.tricks),
        "trick_bobombs_destroy_walls": int(TMCTricks.BOBOMB_WALLS in options.tricks),
        "trick_like_like_cave_no_sword": int(TMCTricks.LIKELIKE_SWORDLESS in options.tricks),
        "trick_boots_skip_town_guard": int(TMCTricks.BOOTS_GUARDS in options.tricks),
        "trick_beam_crenel_switch": int(TMCTricks.BEAM_CRENEL_SWITCH in options.tricks),
        "trick_down_thrust_spikey_beetle": int(TMCTricks.DOWNTHRUST_BEETLE in options.tricks),
        "trick_dark_rooms_no_lantern": int(TMCTricks.DARK_ROOMS in options.tricks),
        "trick_cape_extensions": int(TMCTricks.CAPE_EXTENSIONS in options.tricks),
        "trick_lake_minish_no_boots": int(TMCTricks.LAKE_MINISH in options.tricks),
        "trick_cabin_swim_no_lilypad": int(TMCTricks.CABIN_SWIM in options.tricks),
        "trick_cloud_sharks_no_weapons": int(TMCTricks.SHARKS_SWORDLESS in options.tricks),
        "trick_pow_2f_no_cane": int(TMCTricks.POW_NOCANE in options.tricks),
        "trick_pot_puzzle_no_bracelets": int(TMCTricks.POT_PUZZLE in options.tricks),
        "trick_fow_pot_gust_jar": int(TMCTricks.FOW_POT in options.tricks),
        "trick_dhc_cannons_no_four_sword": int(TMCTricks.DHC_CANNONS in options.tricks),
        "trick_dhc_pads_no_four_sword": int(TMCTricks.DHC_CLONES in options.tricks),
        "trick_dhc_switches_no_four_sword": int(TMCTricks.DHC_SPIN in options.tricks),
        "trick_clone_movement": 0,
        "trick_pow_switches_without_clones": 0,
    }


SLOT_DATA_OPTIONS = [
    "death_link",
    "death_link_gameover",
    "remote_items",
    "goal",
    "dhc_access",
    "ped_elements",
    "ped_swords",
    "ped_dungeons",
    "shuffle_elements",
    "dungeon_small_keys",
    "dungeon_big_keys",
    "dungeon_maps",
    "dungeon_compasses",
    "rupeesanity",
    "shuffle_pots",
    "shuffle_digging",
    "shuffle_underwater",
    "shuffle_gold_enemies",
    "cucco_rounds",
    "goron_sets",
    "goron_jp_prices",
    "random_bottle_contents",
    "traps_enabled",
    "early_weapon",
    "starting_hearts",
    "weapon_bomb",
    "weapon_bow",
    "weapon_gust",
    "weapon_lantern",
    "progressive_sword",
    "progressive_bow",
    "progressive_boomerang",
    "progressive_shield",
    "progressive_scroll",
    "dungeon_warp_dws",
    "dungeon_warp_cof",
    "dungeon_warp_fow",
    "dungeon_warp_tod",
    "dungeon_warp_pow",
    "dungeon_warp_dhc",
    "wind_crest_crenel",
    "wind_crest_falls",
    "wind_crest_clouds",
    "wind_crest_castor",
    "wind_crest_south_field",
    "wind_crest_minish_woods",
    "tricks",
]
"""The yaml options that'll be transfered into slot_data for the tracker"""


OPTION_GROUPS = [
    OptionGroup("Goal", [Goal, DHCAccess, PedElements, PedSword, PedDungeons, PedFigurines, FigurineAmount]),
    # OptionGroup(
    #     "Fusions",
    #     [GoldFusionAccess, RedFusionAccess, GreenFusionAccess, BlueFusionAccess],
    # ),
    OptionGroup(
        "Dungeon Shuffle",
        [
            ShuffleElements,
            SmallKeys,
            BigKeys,
            DungeonMaps,
            DungeonCompasses,
            NonElementDungeons,
        ],
    ),
    OptionGroup(
        "Location Shuffle",
        [
            PedReward,
            Rupeesanity,
            ShufflePots,
            ShuffleDigging,
            ShuffleUnderwater,
            ShuffleGoldEnemies,
            CuccoRounds,
            GoronSets,
            ExtraShopItem,
            Biggoron,
        ],
    ),
    OptionGroup("Difficulty", [StartingHearts, EarlyWeapon, WeaponBomb, WeaponBow, WeaponGust, WeaponLantern]),
    OptionGroup(
        "Item Pool",
        [
            ProgressiveSword,
            ProgressiveBow,
            ProgressiveBoomerang,
            ProgressiveShield,
            ProgressiveScroll,
            HeartContainerAmount,
            PieceOfHeartAmount,
            RandomBottleContents,
            Traps,
        ],
    ),
    OptionGroup(
        "Fast Travel",
        [
            WarpDWS,
            WarpCoF,
            WarpFoW,
            WarpToD,
            WarpPoW,
            WarpDHC,
            WindCrestCrenel,
            WindCrestFalls,
            WindCrestClouds,
            WindCrestSwamp,
            WindCrestSmith,
            WindCrestMinish,
        ],
    ),
    OptionGroup(
        "Quality of Life",
        [GoronJPPrices, OcarinaOnSelect, BootsOnL, BootsAsMinish, BigOctorokManipulation, ReplicaToDBossDoor],
    ),
    OptionGroup("Advanced", [Tricks, FillerItemsDistribution]),
]

PRESETS: dict[str, dict[str, any]] = {
    "Expert": {
        "goal": Goal.option_vaati,
        "dhc_access": DHCAccess.option_open,
        "ped_elements": 4,
        "ped_swords": 5,
        "ped_dungeons": 6,
        "ped_figurines": 1,
        "figurine_amount": 1,
        # "gold_fusion_access": GoldFusionAccess,
        # "red_fusion_access": RedFusionAccess,
        # "green_fusion_access": GreenFusionAccess,
        # "blue_fusion_access": BlueFusionAccess,
        "dungeon_small_keys": SmallKeys.option_anywhere,
        "dungeon_big_keys": BigKeys.option_anywhere,
        "dungeon_maps": DungeonMaps.option_start_with,
        "dungeon_compasses": DungeonCompasses.option_start_with,
        "ped_reward": PedReward.option_dhc_big_key,
        "shuffle_elements": ShuffleElements.option_dungeon_prize,
        "non_element_dungeons": NonElementDungeons.option_excluded,
        "rupeesanity": Rupeesanity.option_true,
        "shuffle_pots": ShufflePots.option_true,
        "shuffle_digging": ShuffleDigging.option_true,
        "shuffle_underwater": ShuffleUnderwater.option_true,
        "shuffle_gold_enemies": ShuffleGoldEnemies.option_true,
        "shuffle_biggoron": Biggoron.option_shield,
        "cucco_rounds": 10,
        "goron_sets": 5,
        "goron_jp_prices": False,
        "extra_shop_item": True,
        "traps_enabled": True,
        "random_bottle_contents": True,
        "early_weapon": False,
        "weapon_bomb": WeaponBomb.option_yes_boss,
        "weapon_bow": WeaponBow.option_true,
        "weapon_gust": WeaponGust.option_true,
        "weapon_lantern": WeaponLantern.option_true,
        "progressive_sword": True,
        "progressive_bow": False,
        "progressive_boomerang": False,
        "progressive_shield": False,
        "progressive_scroll": False,
        "starting_hearts": 3,
        "heart_containers": 0,
        "piece_of_hearts": 11,
        "dungeon_warp_dws": WarpDWS.option_red,
        "dungeon_warp_cof": WarpCoF.option_blue,
        "dungeon_warp_fow": WarpFoW.option_red,
        "dungeon_warp_tod": WarpToD.option_none,
        "dungeon_warp_pow": WarpPoW.option_none,
        "dungeon_warp_dhc": WarpDHC.option_blue,
        "wind_crest_crenel": False,
        "wind_crest_falls": False,
        "wind_crest_clouds": False,
        "wind_crest_castor": False,
        "wind_crest_south_field": False,
        "wind_crest_minish_woods": False,
        # wind_crest_town: False
        # wind_crest_lake: True
        "tricks": ALL_TRICKS,
        "remote_items": True,
        "boots_on_l": True,
        "ocarina_on_select": False,
        "big_octo_manipulation": False,
        "replica_tod_boss_door": False,
    }
}
