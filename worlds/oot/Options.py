import typing
import random
from Options import Option, DefaultOnToggle, Toggle, Range, OptionList, OptionSet, DeathLink
from .LogicTricks import normalized_name_tricks
from .ColorSFXOptions import *


class TrackRandomRange(Range):
    """Overrides normal from_any behavior to track whether the option was randomized at generation time."""
    supports_weighting = False
    randomized: bool = False

    @classmethod
    def from_any(cls, data: typing.Any) -> Range:
        if type(data) is list:
            val = random.choices(data)[0]
            ret = super().from_any(val)
            if not isinstance(val, int) or len(data) > 1:
                ret.randomized = True
            return ret
        if type(data) is not dict:
            return super().from_any(data)
        if any(data.values()):
            val = random.choices(list(data.keys()), weights=list(map(int, data.values())))[0]
            ret = super().from_any(val)
            if not isinstance(val, int) or len(list(filter(bool, map(int, data.values())))) > 1:
                ret.randomized = True
            return ret
        raise RuntimeError(f"All options specified in \"{cls.display_name}\" are weighted as zero.")


class Logic(Choice): 
    """Set the logic used for the generator.
    Glitchless: Normal gameplay. Can enable more difficult logical paths using the Logic Tricks option.
    Glitched: Many powerful glitches expected, such as bomb hovering and clipping.
    Glitched is incompatible with the following settings:
    - All forms of entrance randomizer
    - MQ dungeons
    - Pot shuffle
    - Freestanding item shuffle
    - Crate shuffle
    - Beehive shuffle
    No Logic: No logic is used when placing items. Not recommended for most players."""
    display_name = "Logic Rules"
    option_glitchless = 0
    option_glitched = 1
    option_no_logic = 2


class NightTokens(Toggle):
    """When enabled, nighttime skulltulas logically require Sun's Song."""
    display_name = "Nighttime Skulltulas Expect Sun's Song"


class Forest(Choice): 
    """Set the state of Kokiri Forest and the path to Deku Tree.
    Open: Neither the forest exit nor the path to Deku Tree is blocked.
    Closed Deku: The forest exit is not blocked; the path to Deku Tree requires Kokiri Sword and Deku Shield.
    Closed: Path to Deku Tree requires sword and shield. The forest exit is blocked until Deku Tree is beaten.
    Closed forest will force child start, and becomes Closed Deku if interior entrances, overworld entrances, warp songs, or random spawn positions are enabled."""
    display_name = "Forest"
    option_open = 0
    option_closed_deku = 1
    option_closed = 2
    alias_open_forest = 0
    alias_closed_forest = 2


class Gate(Choice): 
    """Set the state of the Kakariko Village gate for child. The gate is always open as adult.
    Open: The gate starts open. Happy Mask Shop opens upon receiving Zelda's Letter.
    Zelda: The gate and Mask Shop open upon receiving Zelda's Letter, without needing to show it to the guard.
    Closed: Vanilla behavior; the gate and Mask Shop open upon showing Zelda's Letter to the gate guard."""
    display_name = "Kakariko Gate"
    option_open = 0
    option_zelda = 1
    option_closed = 2


class DoorOfTime(DefaultOnToggle):
    """When enabled, the Door of Time starts opened, without needing Song of Time."""
    display_name = "Open Door of Time"


class Fountain(Choice): 
    """Set the state of King Zora, blocking the way to Zora's Fountain.
    Open: King Zora starts moved as both ages. Ruto's Letter is removed.
    Adult: King Zora must be moved as child, but is always moved for adult.
    Closed: Vanilla behavior; King Zora must be shown Ruto's Letter as child to move him as both ages."""
    display_name = "Zora's Fountain"
    option_open = 0
    option_adult = 1
    option_closed = 2
    default = 2


class Fortress(Choice): 
    """Set the requirements for access to Gerudo Fortress.
    Normal: Vanilla behavior; all four carpenters must be rescued.
    Fast: Only one carpenter must be rescued, which is the one in the bottom-left of the fortress.
    Open: The Gerudo Valley bridge starts repaired. Gerudo Membership Card is given to start if not shuffled."""
    display_name = "Gerudo Fortress"
    option_normal = 0
    option_fast = 1
    option_open = 2
    default = 1


class Bridge(Choice): 
    """Set the requirements for the Rainbow Bridge.
    Open: The bridge is always present.
    Vanilla: Bridge requires Shadow Medallion, Spirit Medallion, and Light Arrows.
    Stones: Bridge requires a configurable amount of Spiritual Stones.
    Medallions: Bridge requires a configurable amount of medallions.
    Dungeons: Bridge requires a configurable amount of rewards (stones + medallions).
    Tokens: Bridge requires a configurable amount of gold skulltula tokens.
    Hearts: Bridge requires a configurable amount of hearts."""
    display_name = "Rainbow Bridge Requirement"
    option_open = 0
    option_vanilla = 1
    option_stones = 2
    option_medallions = 3
    option_dungeons = 4
    option_tokens = 5
    option_hearts = 6
    default = 3


class Trials(TrackRandomRange):
    """Set the number of required trials in Ganon's Castle."""
    display_name = "Ganon's Trials Count"
    range_start = 0
    range_end = 6


open_options: typing.Dict[str, type(Option)] = {
    "open_forest": Forest,
    "open_kakariko": Gate,
    "open_door_of_time": DoorOfTime,
    "zora_fountain": Fountain,
    "gerudo_fortress": Fortress, 
    "bridge": Bridge,
    "trials": Trials,
}


class StartingAge(Choice): 
    """Choose which age Link will start as."""
    display_name = "Starting Age"
    option_child = 0
    option_adult = 1


class InteriorEntrances(Choice): 
    """Shuffles interior entrances.
    Simple: Houses and Great Fairies are shuffled.
    All: In addition to Simple, includes Windmill, Link's House, Temple of Time, and the Kakariko potion shop."""
    display_name = "Shuffle Interior Entrances"
    option_off = 0
    option_simple = 1
    option_all = 2
    alias_true = 2


class GrottoEntrances(Toggle):
    """Shuffles grotto and grave entrances."""
    display_name = "Shuffle Grotto/Grave Entrances"


class DungeonEntrances(Choice):
    """Shuffles dungeon entrances. When enabled, both ages will have access to Fire Temple, Bottom of the Well, and Deku Tree.
    Simple: Shuffle dungeon entrances except for Ganon's Castle.
    All: Include Ganon's Castle as well."""
    display_name = "Shuffle Dungeon Entrances"
    option_off = 0
    option_simple = 1
    option_all = 2
    alias_true = 1


class BossEntrances(Choice):
    """Shuffles boss entrances.
    Limited: Bosses will be limited to the ages that typically fight them.
    Full: Bosses may be fought as different ages than usual. Child can defeat Phantom Ganon and Bongo Bongo."""
    display_name = "Shuffle Boss Entrances"
    option_off = 0
    option_limited = 1
    option_full = 2


class OverworldEntrances(Toggle):
    """Shuffles overworld loading zones."""
    display_name = "Shuffle Overworld Entrances"


class OwlDrops(Toggle):
    """Randomizes owl drops from Lake Hylia or Death Mountain Trail as child."""
    display_name = "Randomize Owl Drops"


class WarpSongs(Toggle):
    """Randomizes warp song destinations."""
    display_name = "Randomize Warp Songs"


class SpawnPositions(Choice):
    """Randomizes the starting position on loading a save. Consistent between savewarps."""
    display_name = "Randomize Spawn Positions"
    option_off = 0
    option_child = 1
    option_adult = 2
    option_both = 3
    alias_true = 3


# class MixEntrancePools(Choice):
#     """Shuffles entrances into a mixed pool instead of separate ones. "indoor" keeps overworld entrances separate; "all"
#      mixes them in."""
#     display_name = "Mix Entrance Pools"
#     option_off = 0
#     option_indoor = 1
#     option_all = 2


# class DecoupleEntrances(Toggle):
#     """Decouple entrances when shuffling them. Also adds the one-way entrance from Gerudo Valley to Lake Hylia if
#     overworld is shuffled."""
#     display_name = "Decouple Entrances"


class TriforceHunt(Toggle):
    """Gather pieces of the Triforce scattered around the world to complete the game."""
    display_name = "Triforce Hunt"


class TriforceGoal(Range):
    """Number of Triforce pieces required to complete the game."""
    display_name = "Required Triforce Pieces"
    range_start = 1
    range_end = 80
    default = 20


class ExtraTriforces(Range):
    """Percentage of additional Triforce pieces in the pool. With high numbers, you may need to randomize additional
    locations to have enough items."""
    display_name = "Percentage of Extra Triforce Pieces"
    range_start = 0
    range_end = 100
    default = 50


class LogicalChus(Toggle):
    """Bombchus are properly considered in logic.
    The first found pack will always have 20 chus. 
    Kokiri Shop and Bazaar will sell refills at reduced cost.
    Bombchus open Bombchu Bowling."""
    display_name = "Bombchus Considered in Logic"


class DungeonShortcuts(Choice):
    """Shortcuts to dungeon bosses are available without any requirements.
    If enabled, this will impact the logic of dungeons where shortcuts are available.
    Choice: Use the option "dungeon_shortcuts_list" to choose shortcuts."""
    display_name = "Dungeon Boss Shortcuts Mode"
    option_off = 0
    option_choice = 1
    option_all = 2
    option_random_dungeons = 3


class DungeonShortcutsList(OptionSet):
    """Chosen dungeons to have shortcuts."""
    display_name = "Shortcut Dungeons"
    valid_keys = {
        "Deku Tree",
        "Dodongo's Cavern",
        "Jabu Jabu's Belly",
        "Forest Temple",
        "Fire Temple",
        "Water Temple",
        "Shadow Temple",
        "Spirit Temple",
    }


class MQDungeons(Choice):
    """Choose between vanilla and Master Quest dungeon layouts.
    Vanilla: All layouts are vanilla.
    MQ: All layouts are Master Quest.
    Specific: Use the option "mq_dungeons_list" to choose which dungeons are MQ.
    Count: Use the option "mq_dungeons_count" to choose a number of random dungeons as MQ."""
    display_name = "MQ Dungeon Mode"
    option_vanilla = 0
    option_mq = 1
    option_specific = 2
    option_count = 3


class MQDungeonList(OptionSet):
    """With MQ dungeons as Specific: chosen dungeons to be MQ layout."""
    display_name = "MQ Dungeon List"
    valid_keys = {
        "Deku Tree",
        "Dodongo's Cavern",
        "Jabu Jabu's Belly",
        "Forest Temple",
        "Fire Temple",
        "Water Temple",
        "Shadow Temple",
        "Spirit Temple",
        "Bottom of the Well",
        "Ice Cavern",
        "Gerudo Training Ground",
        "Ganon's Castle",
    }


class MQDungeonCount(TrackRandomRange):
    """With MQ dungeons as Count: number of randomly-selected dungeons to be MQ layout."""
    display_name = "MQ Dungeon Count"
    range_start = 0
    range_end = 12
    default = 0


# class EmptyDungeons(Choice):
#     """Pre-completed dungeons are barren and rewards are given for free."""
#     display_name = "Pre-completed Dungeons Mode"
#     option_none = 0
#     option_specific = 1
#     option_count = 2


# class EmptyDungeonList(OptionSet):
#     """Chosen dungeons to be pre-completed."""
#     display_name = "Pre-completed Dungeon List"
#     valid_keys = {
#         "Deku Tree",
#         "Dodongo's Cavern",
#         "Jabu Jabu's Belly",
#         "Forest Temple",
#         "Fire Temple",
#         "Water Temple",
#         "Shadow Temple",
#         "Spirit Temple",
#     }


# class EmptyDungeonCount(Range):
#     display_name = "Pre-completed Dungeon Count"
#     range_start = 1
#     range_end = 8
#     default = 2


world_options: typing.Dict[str, type(Option)] = {
    "starting_age": StartingAge,
    "shuffle_interior_entrances": InteriorEntrances,
    "shuffle_grotto_entrances": GrottoEntrances,
    "shuffle_dungeon_entrances": DungeonEntrances,
    "shuffle_overworld_entrances": OverworldEntrances,
    "owl_drops": OwlDrops,
    "warp_songs": WarpSongs,
    "spawn_positions": SpawnPositions,
    "shuffle_bosses": BossEntrances,
    # "mix_entrance_pools": MixEntrancePools,
    # "decouple_entrances": DecoupleEntrances,
    "triforce_hunt": TriforceHunt, 
    "triforce_goal": TriforceGoal,
    "extra_triforce_percentage": ExtraTriforces,
    "bombchus_in_logic": LogicalChus,

    "dungeon_shortcuts": DungeonShortcuts,
    "dungeon_shortcuts_list": DungeonShortcutsList,

    "mq_dungeons_mode": MQDungeons,
    "mq_dungeons_list": MQDungeonList,
    "mq_dungeons_count": MQDungeonCount,

    # "empty_dungeons_mode": EmptyDungeons,
    # "empty_dungeons_list": EmptyDungeonList,
    # "empty_dungeon_count": EmptyDungeonCount,
}


class BridgeStones(Range):
    """With Stones bridge: set the number of Spiritual Stones required."""
    display_name = "Spiritual Stones Required for Bridge"
    range_start = 0
    range_end = 3
    default = 3


class BridgeMedallions(Range):
    """With Medallions bridge: set the number of medallions required."""
    display_name = "Medallions Required for Bridge"
    range_start = 0
    range_end = 6
    default = 6


class BridgeRewards(Range):
    """With Dungeons bridge: set the number of dungeon rewards required."""
    display_name = "Dungeon Rewards Required for Bridge"
    range_start = 0
    range_end = 9
    default = 9


class BridgeTokens(Range):
    """With Tokens bridge: set the number of Gold Skulltula Tokens required."""
    display_name = "Tokens Required for Bridge"
    range_start = 0
    range_end = 100
    default = 40


class BridgeHearts(Range):
    """With Hearts bridge: set the number of hearts required."""
    display_name = "Hearts Required for Bridge"
    range_start = 4
    range_end = 20
    default = 20


bridge_options: typing.Dict[str, type(Option)] = {
    "bridge_stones": BridgeStones,
    "bridge_medallions": BridgeMedallions,
    "bridge_rewards": BridgeRewards, 
    "bridge_tokens": BridgeTokens,
    "bridge_hearts": BridgeHearts,
}


class SongShuffle(Choice): 
    """Set where songs can appear.
    Song: Songs are shuffled into other song locations.
    Dungeon: Songs are placed into end-of-dungeon locations:
    - The 8 boss heart containers
    - Sheik in Ice Cavern
    - Lens of Truth chest in Bottom of the Well
    - Ice Arrows chest in Gerudo Training Ground
    - Impa at Hyrule Castle
    Any: Songs can appear anywhere in the multiworld."""
    display_name = "Shuffle Songs"
    option_song = 0
    option_dungeon = 1
    option_any = 2


class ShopShuffle(Choice): 
    """Randomizes shop contents.
    Off: Shops are not randomized at all.
    Fixed Number: Shop contents are shuffled, and a specific number of multiworld locations exist in each shop, controlled by the "shop_slots" option.
    Random Number: Same as Fixed Number, but the number of locations per shop is random and may differ between shops."""
    display_name = "Shopsanity"
    option_off = 0
    option_fixed_number = 1
    option_random_number = 2


class ShopSlots(Range):
    """With Shopsanity fixed number: quantity of multiworld locations per shop to be randomized."""
    display_name = "Shuffled Shop Slots"
    range_start = 0
    range_end = 4


class ShopPrices(Choice):
    """Controls prices of shop locations.
    Normal: Balanced distribution from 0 to 300.
    Affordable: Every shop location costs 10 rupees.
    Starting Wallet: Prices capped at 99 rupees.
    Adult's Wallet: Prices capped at 200 rupees.
    Giant's Wallet: Prices capped at 500 rupees.
    Tycoon's Wallet: Prices capped at 999 rupees."""
    display_name = "Shopsanity Prices"
    option_normal = 0
    option_affordable = 1
    option_starting_wallet = 2
    option_adults_wallet = 3
    option_giants_wallet = 4
    option_tycoons_wallet = 5


class TokenShuffle(Choice): 
    """Token rewards from Gold Skulltulas can be shuffled into the pool.
    Dungeons: Only skulltulas in dungeons are shuffled.
    Overworld: Only skulltulas on the overworld (all skulltulas not in dungeons) are shuffled.
    All: Every skulltula is shuffled."""
    display_name = "Tokensanity"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3


class ScrubShuffle(Choice): 
    """Shuffle the items sold by Business Scrubs, and set the prices.
    Off: Only the three business scrubs that sell one-time upgrades in vanilla will have items at their vanilla prices.
    Low/"Affordable": All scrub prices are 10 rupees.
    Regular/"Expensive": All scrub prices are vanilla.
    Random Prices: All scrub prices are randomized between 0 and 99 rupees."""
    display_name = "Scrub Shuffle"
    option_off = 0
    option_low = 1
    option_regular = 2
    option_random_prices = 3
    alias_affordable = 1
    alias_expensive = 2


class ShuffleCows(Toggle):
    """Cows give items when Epona's Song is played."""
    display_name = "Shuffle Cows"


class ShuffleSword(Toggle):
    """Shuffle Kokiri Sword into the item pool."""
    display_name = "Shuffle Kokiri Sword"


class ShuffleOcarinas(Toggle):
    """Shuffle the Fairy Ocarina and Ocarina of Time into the item pool."""
    display_name = "Shuffle Ocarinas"


class ShuffleChildTrade(Choice):
    """Controls the behavior of the start of the child trade quest.
    Vanilla: Malon will give you the Weird Egg at Hyrule Castle.
    Shuffle: Malon will give you a random item, and the Weird Egg is shuffled.
    Skip Child Zelda: The game starts with Zelda already met, Zelda's Letter obtained, and the item from Impa obtained.
    """
    display_name = "Shuffle Child Trade Item"
    option_vanilla = 0
    option_shuffle = 1
    option_skip_child_zelda = 2
    alias_false = 0
    alias_true = 1


class ShuffleCard(Toggle):
    """Shuffle the Gerudo Membership Card into the item pool."""
    display_name = "Shuffle Gerudo Card"


class ShuffleBeans(Toggle):
    """Adds a pack of 10 beans to the item pool and changes the bean salesman to sell one item for 60 rupees."""
    display_name = "Shuffle Magic Beans"


class ShuffleMedigoronCarpet(Toggle):
    """Shuffle the items sold by Medigoron and the Haunted Wasteland Carpet Salesman."""
    display_name = "Shuffle Medigoron & Carpet Salesman"


class ShuffleFreestanding(Choice):
    """Shuffles freestanding rupees, recovery hearts, Shadow Temple Spinning Pots, and Goron Pot drops.
    Dungeons: Only freestanding items in dungeons are shuffled.
    Overworld: Only freestanding items in the overworld are shuffled.
    All: All freestanding items are shuffled."""
    display_name = "Shuffle Rupees & Hearts"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3


class ShufflePots(Choice):
    """Shuffles pots and flying pots which normally contain an item.
    Dungeons: Only pots in dungeons are shuffled.
    Overworld: Only pots in the overworld are shuffled.
    All: All pots are shuffled."""
    display_name = "Shuffle Pots"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3


class ShuffleCrates(Choice):
    """Shuffles large and small crates containing an item.
    Dungeons: Only crates in dungeons are shuffled.
    Overworld: Only crates in the overworld are shuffled.
    All: All crates are shuffled."""
    display_name = "Shuffle Crates"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3


class ShuffleBeehives(Toggle):
    """Beehives drop an item when destroyed by an explosion, the Hookshot, or the Boomerang."""
    display_name = "Shuffle Beehives"


class ShuffleFrogRupees(Toggle):
    """Shuffles the purple rupees received from the Zora's River frogs."""
    display_name = "Shuffle Frog Song Rupees"


shuffle_options: typing.Dict[str, type(Option)] = {
    "shuffle_song_items": SongShuffle,
    "shopsanity": ShopShuffle,
    "shop_slots": ShopSlots,
    "shopsanity_prices": ShopPrices,
    "tokensanity": TokenShuffle,
    "shuffle_scrubs": ScrubShuffle,
    "shuffle_child_trade": ShuffleChildTrade,
    "shuffle_freestanding_items": ShuffleFreestanding,
    "shuffle_pots": ShufflePots,
    "shuffle_crates": ShuffleCrates,
    "shuffle_cows": ShuffleCows,
    "shuffle_beehives": ShuffleBeehives,
    "shuffle_kokiri_sword": ShuffleSword,
    "shuffle_ocarinas": ShuffleOcarinas,
    "shuffle_gerudo_card": ShuffleCard,
    "shuffle_beans": ShuffleBeans,
    "shuffle_medigoron_carpet_salesman": ShuffleMedigoronCarpet,
    "shuffle_frog_song_rupees": ShuffleFrogRupees,
}


class ShuffleMapCompass(Choice): 
    """Control where to shuffle dungeon maps and compasses.
    Remove: There will be no maps or compasses in the itempool.
    Startwith: You start with all maps and compasses.
    Vanilla: Maps and compasses remain vanilla.
    Dungeon: Maps and compasses are shuffled within their original dungeon.
    Regional: Maps and compasses are shuffled only in regions near the original dungeon.
    Overworld: Maps and compasses are shuffled locally outside of dungeons.
    Any Dungeon: Maps and compasses are shuffled locally in any dungeon.
    Keysanity: Maps and compasses can be anywhere in the multiworld."""
    display_name = "Maps & Compasses"
    option_remove = 0
    option_startwith = 1
    option_vanilla = 2
    option_dungeon = 3
    option_regional = 4
    option_overworld = 5
    option_any_dungeon = 6
    option_keysanity = 7
    default = 1
    alias_anywhere = 7


class ShuffleKeys(Choice): 
    """Control where to shuffle dungeon small keys.
    Remove/"Keysy": There will be no small keys in the itempool. All small key doors are automatically unlocked.
    Vanilla: Small keys remain vanilla. You may start with extra small keys in some dungeons to prevent softlocks.
    Dungeon: Small keys are shuffled within their original dungeon.
    Regional: Small keys are shuffled only in regions near the original dungeon.
    Overworld: Small keys are shuffled locally outside of dungeons.
    Any Dungeon: Small keys are shuffled locally in any dungeon.
    Keysanity: Small keys can be anywhere in the multiworld."""
    display_name = "Small Keys"
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_regional = 4
    option_overworld = 5
    option_any_dungeon = 6
    option_keysanity = 7
    default = 3
    alias_keysy = 0
    alias_anywhere = 7


class ShuffleGerudoKeys(Choice): 
    """Control where to shuffle the Thieves' Hideout small keys.
    Vanilla: Hideout keys remain vanilla.
    Regional: Hideout keys are shuffled only in the Gerudo Valley/Desert Colossus area.
    Overworld: Hideout keys are shuffled locally outside of dungeons.
    Any Dungeon: Hideout keys are shuffled locally in any dungeon.
    Keysanity: Hideout keys can be anywhere in the multiworld."""
    display_name = "Thieves' Hideout Keys"
    option_vanilla = 0
    option_regional = 1
    option_overworld = 2
    option_any_dungeon = 3
    option_keysanity = 4
    alias_anywhere = 4


class ShuffleBossKeys(Choice): 
    """Control where to shuffle boss keys, except the Ganon's Castle Boss Key.
    Remove/"Keysy": There will be no boss keys in the itempool. All boss key doors are automatically unlocked.
    Vanilla: Boss keys remain vanilla. You may start with extra small keys in some dungeons to prevent softlocks.
    Dungeon: Boss keys are shuffled within their original dungeon.
    Regional: Boss keys are shuffled only in regions near the original dungeon.
    Overworld: Boss keys are shuffled locally outside of dungeons.
    Any Dungeon: Boss keys are shuffled locally in any dungeon.
    Keysanity: Boss keys can be anywhere in the multiworld."""
    display_name = "Boss Keys"
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_regional = 4
    option_overworld = 5
    option_any_dungeon = 6
    option_keysanity = 7
    default = 3
    alias_keysy = 0
    alias_anywhere = 7


class ShuffleGanonBK(Choice):
    """Control how to shuffle the Ganon's Castle Boss Key (GCBK).
    Remove: GCBK is removed, and the boss key door is automatically unlocked.
    Vanilla: GCBK remains vanilla.
    Dungeon: GCBK is shuffled within its original dungeon.
    Regional: GCBK is shuffled only in Hyrule Field, Market, and Hyrule Castle areas.
    Overworld: GCBK is shuffled locally outside of dungeons.
    Any Dungeon: GCBK is shuffled locally in any dungeon.
    Keysanity: GCBK can be anywhere in the multiworld.
    On LACS: GCBK is on the Light Arrow Cutscene, which requires Shadow and Spirit Medallions.
    Stones: GCBK will be awarded when reaching the target number of Spiritual Stones.
    Medallions: GCBK will be awarded when reaching the target number of medallions.
    Dungeons: GCBK will be awarded when reaching the target number of dungeon rewards.
    Tokens: GCBK will be awarded when reaching the target number of Gold Skulltula Tokens.
    Hearts: GCBK will be awarded when reaching the target number of hearts.
    """
    display_name = "Ganon's Boss Key"
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_regional = 4
    option_overworld = 5
    option_any_dungeon = 6
    option_keysanity = 7
    option_on_lacs = 8
    option_stones = 9
    option_medallions = 10
    option_dungeons = 11
    option_tokens = 12
    option_hearts = 13
    default = 0
    alias_keysy = 0
    alias_anywhere = 7


class EnhanceMC(Toggle):
    """Map tells if a dungeon is vanilla or MQ. Compass tells what the dungeon reward is."""
    display_name = "Maps and Compasses Give Information"


class GanonBKMedallions(Range):
    """With medallions GCBK: set how many medallions are required to receive GCBK."""
    display_name = "Medallions Required for Ganon's BK"
    range_start = 1
    range_end = 6
    default = 6


class GanonBKStones(Range):
    """With stones GCBK: set how many Spiritual Stones are required to receive GCBK."""
    display_name = "Spiritual Stones Required for Ganon's BK"
    range_start = 1
    range_end = 3
    default = 3


class GanonBKRewards(Range):
    """With dungeons GCBK: set how many dungeon rewards are required to receive GCBK."""
    display_name = "Dungeon Rewards Required for Ganon's BK"
    range_start = 1
    range_end = 9
    default = 9


class GanonBKTokens(Range):
    """With tokens GCBK: set how many Gold Skulltula Tokens are required to receive GCBK."""
    display_name = "Tokens Required for Ganon's BK"
    range_start = 1
    range_end = 100
    default = 40


class GanonBKHearts(Range):
    """With hearts GCBK: set how many hearts are required to receive GCBK."""
    display_name = "Hearts Required for Ganon's BK"
    range_start = 4
    range_end = 20
    default = 20


class KeyRings(Choice):
    """A key ring grants all dungeon small keys at once, rather than individually.
    Choose: Use the option "key_rings_list" to choose which dungeons have key rings.
    All: All dungeons have key rings instead of small keys."""
    display_name = "Key Rings Mode"
    option_off = 0
    option_choose = 1
    option_all = 2
    option_random_dungeons = 3


class KeyRingList(OptionSet):
    """With key rings as Choose: select areas with key rings rather than individual small keys."""
    display_name = "Key Ring Areas"
    valid_keys = {
        "Thieves' Hideout",
        "Forest Temple",
        "Fire Temple",
        "Water Temple",
        "Shadow Temple",
        "Spirit Temple",
        "Bottom of the Well",
        "Gerudo Training Ground",
        "Ganon's Castle"
    }


dungeon_items_options: typing.Dict[str, type(Option)] = {
    "shuffle_mapcompass": ShuffleMapCompass, 
    "shuffle_smallkeys": ShuffleKeys, 
    "shuffle_hideoutkeys": ShuffleGerudoKeys,
    "shuffle_bosskeys": ShuffleBossKeys,
    "enhance_map_compass": EnhanceMC,
    "shuffle_ganon_bosskey": ShuffleGanonBK,
    "ganon_bosskey_medallions": GanonBKMedallions,
    "ganon_bosskey_stones": GanonBKStones,
    "ganon_bosskey_rewards": GanonBKRewards,
    "ganon_bosskey_tokens": GanonBKTokens,
    "ganon_bosskey_hearts": GanonBKHearts,
    "key_rings": KeyRings,
    "key_rings_list": KeyRingList,
}


class SkipEscape(DefaultOnToggle):
    """Skips the tower collapse sequence between the Ganondorf and Ganon fights."""
    display_name = "Skip Tower Escape Sequence"


class SkipStealth(DefaultOnToggle):
    """The crawlspace into Hyrule Castle skips straight to Zelda."""
    display_name = "Skip Child Stealth"


class SkipEponaRace(DefaultOnToggle):
    """Epona can always be summoned with Epona's Song."""
    display_name = "Skip Epona Race"


class SkipMinigamePhases(DefaultOnToggle):
    """Dampe Race and Horseback Archery give both rewards if the second condition is met on the first attempt."""
    display_name = "Skip Some Minigame Phases"


class CompleteMaskQuest(Toggle):
    """All masks are immediately available to borrow from the Happy Mask Shop."""
    display_name = "Complete Mask Quest"


class UsefulCutscenes(Toggle):
    """Reenables the Poe cutscene in Forest Temple, Darunia in Fire Temple, and Twinrova introduction. Mostly useful for
     glitched."""
    display_name = "Enable Useful Cutscenes"


class FastChests(DefaultOnToggle):
    """All chest animations are fast. If disabled, major items have a slow animation."""
    display_name = "Fast Chest Cutscenes"


class FreeScarecrow(Toggle):
    """Pulling out the ocarina near a scarecrow spot spawns Pierre without needing the song."""
    display_name = "Free Scarecrow's Song"


class FastBunny(Toggle):
    """Bunny Hood lets you move 1.5x faster like in Majora's Mask."""
    display_name = "Fast Bunny Hood"


class PlantBeans(Toggle):
    """Pre-plants all 10 magic beans in the soft soil spots."""
    display_name = "Plant Magic Beans"


class ChickenCount(Range):
    """Controls the number of Cuccos for Anju to give an item as child."""
    display_name = "Cucco Count"
    range_start = 0
    range_end = 7
    default = 7


class BigPoeCount(Range):
    """Number of Big Poes required for the Poe Collector's item."""
    display_name = "Big Poe Count"
    range_start = 1
    range_end = 10
    default = 1


class FAETorchCount(Range):
    """Number of lit torches required to open Shadow Temple.
    Does not affect logic; use the trick Shadow Temple Entry with Fire Arrows if desired."""
    display_name = "Fire Arrow Entry Torch Count"
    range_start = 1
    range_end = 24
    default = 24


timesavers_options: typing.Dict[str, type(Option)] = {
    "no_escape_sequence": SkipEscape, 
    "no_guard_stealth": SkipStealth, 
    "no_epona_race": SkipEponaRace, 
    "skip_some_minigame_phases": SkipMinigamePhases, 
    "complete_mask_quest": CompleteMaskQuest, 
    "useful_cutscenes": UsefulCutscenes, 
    "fast_chests": FastChests, 
    "free_scarecrow": FreeScarecrow, 
    "fast_bunny_hood": FastBunny,
    "plant_beans": PlantBeans,
    "chicken_count": ChickenCount,
    "big_poe_count": BigPoeCount,
    "fae_torch_count": FAETorchCount,
}


class CorrectChestAppearance(Choice):
    """Changes chest textures and/or sizes to match their contents.
    Off: All chests have their vanilla size/appearance.
    Textures: Chest textures reflect their contents.
    Both: Like Textures, but progression items and boss keys get big chests, and other items get small chests.
    Classic: Old behavior of CSMC; textures distinguish keys from non-keys, and size distinguishes importance."""
    display_name = "Chest Appearance Matches Contents"
    option_off = 0
    option_textures = 1
    option_both = 2
    option_classic = 3


class MinorInMajor(Toggle):
    """Hylian Shield, Deku Shield, and Bombchus appear in big/gold chests."""
    display_name = "Minor Items in Big/Gold Chests"


class InvisibleChests(Toggle):
    """Chests visible only with Lens of Truth. Logic is not changed."""
    display_name = "Invisible Chests"


class CorrectPotCrateAppearance(Choice):
    """Changes the appearance of pots, crates, and beehives that contain items.
    Off: Vanilla appearance for all containers.
    Textures (Content): Unchecked pots and crates have a texture reflecting their contents. Unchecked beehives with progression items will wiggle.
    Textures (Unchecked): Unchecked pots and crates are golden. Unchecked beehives will wiggle.
    """
    display_name = "Pot, Crate, and Beehive Appearance"
    option_off = 0
    option_textures_content = 1
    option_textures_unchecked = 2
    default = 2


class Hints(Choice): 
    """Gossip Stones can give hints about item locations.
    None: Gossip Stones do not give hints.
    Mask: Gossip Stones give hints with Mask of Truth.
    Agony: Gossip Stones give hints wtih Stone of Agony.
    Always: Gossip Stones always give hints."""
    display_name = "Gossip Stones"
    option_none = 0
    option_mask = 1
    option_agony = 2
    option_always = 3
    default = 3


class MiscHints(DefaultOnToggle):
    """The Temple of Time altar hints dungeon rewards, bridge info, and Ganon BK info; Ganondorf hints the Light Arrows; Dampe's diary hints a local Hookshot if one exists; Skulltula House locations hint their item."""
    display_name = "Misc Hints"


class HintDistribution(Choice):
    """Choose the hint distribution to use. Affects the frequency of strong hints, which items are always hinted, etc.
    Detailed documentation on hint distributions can be found on the Archipelago GitHub or OoTRandomizer.com.
    The Async hint distribution is intended for async multiworlds. It removes Way of the Hero hints to improve generation times, since they are not very useful in asyncs."""
    display_name = "Hint Distribution"
    option_balanced = 0
    option_ddr = 1
    # option_league = 2
    # option_mw3 = 3
    option_scrubs = 4
    option_strong = 5
    # option_tournament = 6
    option_useless = 7
    option_very_strong = 8
    option_async = 9
    default = 9


class TextShuffle(Choice): 
    """Randomizes text in the game for comedic effect.
    Except Hints: does not randomize important text such as hints, small/boss key information, and item prices.
    Complete: randomizes every textbox, including the useful ones."""
    display_name = "Text Shuffle"
    option_none = 0
    option_except_hints = 1
    option_complete = 2
    alias_false = 0


class DamageMultiplier(Choice): 
    """Controls the amount of damage Link takes."""
    display_name = "Damage Multiplier"
    option_half = 0
    option_normal = 1
    option_double = 2
    option_quadruple = 3
    option_ohko = 4
    default = 1


class DeadlyBonks(Choice):
    """Bonking on a wall or object will hurt Link. "Normal" is a half heart of damage."""
    display_name = "Bonks Do Damage"
    option_none = 0
    option_half = 1
    option_normal = 2
    option_double = 3
    option_quadruple = 4
    option_ohko = 5


class HeroMode(Toggle):
    """Hearts will not drop from enemies or objects."""
    display_name = "Hero Mode"


class StartingToD(Choice):
    """Change the starting time of day.
    Daytime starts at Sunrise and ends at Sunset. Default is between Morning and Noon."""
    display_name = "Starting Time of Day"
    option_default = 0
    option_sunrise = 1
    option_morning = 2
    option_noon = 3
    option_afternoon = 4
    option_sunset = 5
    option_evening = 6
    option_midnight = 7
    option_witching_hour = 8


class BlueFireArrows(Toggle):
    """Ice arrows can melt red ice and break the mud walls in Dodongo's Cavern."""
    display_name = "Blue Fire Arrows"


class FixBrokenDrops(Toggle):
    """Fixes two broken vanilla drops: deku shield in child Spirit Temple, and magic drop on GTG eye statue."""
    display_name = "Fix Broken Drops"


class ConsumableStart(Toggle):
    """Start the game with full Deku Sticks and Deku Nuts."""
    display_name = "Start with Consumables"


class RupeeStart(Toggle):
    """Start with a full wallet. Wallet upgrades will also fill your wallet."""
    display_name = "Start with Rupees"


misc_options: typing.Dict[str, type(Option)] = {
    "correct_chest_appearances": CorrectChestAppearance,
    "minor_items_as_major_chest": MinorInMajor,
    "invisible_chests": InvisibleChests,
    "correct_potcrate_appearances": CorrectPotCrateAppearance,
    "hints": Hints,
    "misc_hints": MiscHints,
    "hint_dist": HintDistribution,
    "text_shuffle": TextShuffle,
    "damage_multiplier": DamageMultiplier,
    "deadly_bonks": DeadlyBonks,
    "no_collectible_hearts": HeroMode,
    "starting_tod": StartingToD,
    "blue_fire_arrows": BlueFireArrows,
    "fix_broken_drops": FixBrokenDrops,
    "start_with_consumables": ConsumableStart, 
    "start_with_rupees": RupeeStart,
}

class ItemPoolValue(Choice): 
    """Changes the number of items available in the game.
    Plentiful: One extra copy of every major item.
    Balanced: Original item pool.
    Scarce: Extra copies of major items are removed. Heart containers are removed.
    Minimal: All major item upgrades not used for locations are removed. All health is removed."""
    display_name = "Item Pool"
    option_plentiful = 0
    option_balanced = 1
    option_scarce = 2
    option_minimal = 3
    default = 1


class IceTraps(Choice): 
    """Adds ice traps to the item pool.
    Off: All ice traps are removed.
    Normal: The vanilla quantity of ice traps are placed.
    On/"Extra": There is a chance for some extra ice traps to be placed.
    Mayhem: All added junk items are ice traps.
    Onslaught: All junk items are replaced by ice traps, even those in the base pool."""
    display_name = "Ice Traps"
    option_off = 0
    option_normal = 1
    option_on = 2
    option_mayhem = 3
    option_onslaught = 4
    default = 1
    alias_extra = 2


class IceTrapVisual(Choice): 
    """Changes the appearance of traps, including other games' traps, as freestanding items."""
    display_name = "Trap Appearance"
    option_major_only = 0
    option_junk_only = 1
    option_anything = 2


class AdultTradeStart(Choice):
    """Choose the item that starts the adult trade sequence."""
    display_name = "Adult Trade Sequence Start"
    option_pocket_egg = 0
    option_pocket_cucco = 1
    option_cojiro = 2
    option_odd_mushroom = 3
    option_poachers_saw = 4
    option_broken_sword = 5
    option_prescription = 6
    option_eyeball_frog = 7
    option_eyedrops = 8
    option_claim_check = 9
    default = 9


itempool_options: typing.Dict[str, type(Option)] = {
    "item_pool_value": ItemPoolValue, 
    "junk_ice_traps": IceTraps,
    "ice_trap_appearance": IceTrapVisual, 
    "adult_trade_start": AdultTradeStart,
}

# Start of cosmetic options

class Targeting(Choice): 
    """Default targeting option."""
    display_name = "Default Targeting Option"
    option_hold = 0
    option_switch = 1


class DisplayDpad(DefaultOnToggle):
    """Show dpad icon on HUD for quick actions (ocarina, hover boots, iron boots, mask)."""
    display_name = "Display D-Pad HUD"


class DpadDungeonMenu(DefaultOnToggle):
    """Show separated menus on the pause screen for dungeon keys, rewards, and Vanilla/MQ info."""
    display_name = "Display D-Pad Dungeon Info"


class CorrectColors(DefaultOnToggle):
    """Makes in-game models match their HUD element colors."""
    display_name = "Item Model Colors Match Cosmetics"


class Music(Choice): 
    option_normal = 0
    option_off = 1
    option_randomized = 2


class BackgroundMusic(Music):
    """Randomize or disable background music."""
    display_name = "Background Music"


class Fanfares(Music):
    """Randomize or disable item fanfares."""
    display_name = "Fanfares"


class OcarinaFanfares(Toggle):
    """Enable ocarina songs as fanfares. These are longer than usual fanfares. Does nothing without fanfares randomized."""
    display_name = "Ocarina Songs as Fanfares"


class SwordTrailDuration(Range):
    """Set the duration for sword trails."""
    display_name = "Sword Trail Duration"
    range_start = 4
    range_end = 20
    default = 4


cosmetic_options: typing.Dict[str, type(Option)] = {
    "default_targeting": Targeting,
    "display_dpad": DisplayDpad,
    "dpad_dungeon_menu": DpadDungeonMenu,
    "correct_model_colors": CorrectColors,
    "background_music": BackgroundMusic,
    "fanfares": Fanfares,
    "ocarina_fanfares": OcarinaFanfares,
    "kokiri_color": kokiri_color,
    "goron_color":  goron_color,
    "zora_color":   zora_color,
    "silver_gauntlets_color":   silver_gauntlets_color,
    "golden_gauntlets_color":   golden_gauntlets_color,
    "mirror_shield_frame_color": mirror_shield_frame_color,
    "navi_color_default_inner": navi_color_default_inner,
    "navi_color_default_outer": navi_color_default_outer,
    "navi_color_enemy_inner":   navi_color_enemy_inner,
    "navi_color_enemy_outer":   navi_color_enemy_outer,
    "navi_color_npc_inner":     navi_color_npc_inner,
    "navi_color_npc_outer":     navi_color_npc_outer,
    "navi_color_prop_inner":    navi_color_prop_inner,
    "navi_color_prop_outer":    navi_color_prop_outer,
    "sword_trail_duration": SwordTrailDuration,
    "sword_trail_color_inner": sword_trail_color_inner,
    "sword_trail_color_outer": sword_trail_color_outer,
    "bombchu_trail_color_inner": bombchu_trail_color_inner,
    "bombchu_trail_color_outer": bombchu_trail_color_outer,
    "boomerang_trail_color_inner": boomerang_trail_color_inner,
    "boomerang_trail_color_outer": boomerang_trail_color_outer,
    "heart_color":          heart_color,
    "magic_color":          magic_color,
    "a_button_color":       a_button_color,
    "b_button_color":       b_button_color,
    "c_button_color":       c_button_color,
    "start_button_color":   start_button_color,
}

class SfxOcarina(Choice):
    """Change the sound of the ocarina."""
    display_name = "Ocarina Instrument"
    option_ocarina = 1
    option_malon = 2
    option_whistle = 3
    option_harp = 4
    option_grind_organ = 5
    option_flute = 6
    default = 1

sfx_options: typing.Dict[str, type(Option)] = {
    "sfx_navi_overworld":   sfx_navi_overworld,
    "sfx_navi_enemy":       sfx_navi_enemy,
    "sfx_low_hp":           sfx_low_hp,
    "sfx_menu_cursor":      sfx_menu_cursor,
    "sfx_menu_select":      sfx_menu_select,
    "sfx_nightfall":        sfx_nightfall,
    "sfx_horse_neigh":      sfx_horse_neigh,
    "sfx_hover_boots":      sfx_hover_boots,
    "sfx_ocarina":          SfxOcarina,
}


class LogicTricks(OptionList):
    """Set various tricks for logic in Ocarina of Time. 
    Format as a comma-separated list of "nice" names: ["Fewer Tunic Requirements", "Hidden Grottos without Stone of Agony"].
    A full list of supported tricks can be found at:
    https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/oot/LogicTricks.py
    """
    display_name = "Logic Tricks"
    valid_keys = frozenset(normalized_name_tricks)
    valid_keys_casefold = True


# All options assembled into a single dict
oot_options: typing.Dict[str, type(Option)] = {
    "logic_rules": Logic, 
    "logic_no_night_tokens_without_suns_song": NightTokens, 
    **open_options, 
    **world_options, 
    **bridge_options,
    **dungeon_items_options,
    **shuffle_options,
    **timesavers_options,
    **misc_options, 
    **itempool_options,
    **cosmetic_options,
    **sfx_options,
    "logic_tricks": LogicTricks,
    "death_link": DeathLink,
}
