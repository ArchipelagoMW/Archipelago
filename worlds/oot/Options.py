import typing
from Options import Option, DefaultOnToggle, Toggle, Range, OptionList, DeathLink
from .LogicTricks import normalized_name_tricks
from .ColorSFXOptions import *


class Logic(Choice): 
    """Set the logic used for the generator."""
    display_name = "Logic Rules"
    option_glitchless = 0
    option_glitched = 1
    option_no_logic = 2


class NightTokens(Toggle):
    """Nighttime skulltulas will logically require Sun's Song."""
    display_name = "Nighttime Skulltulas Expect Sun's Song"


class Forest(Choice): 
    """Set the state of Kokiri Forest and the path to Deku Tree."""
    display_name = "Forest"
    option_open = 0
    option_closed_deku = 1
    option_closed = 2
    alias_open_forest = 0
    alias_closed_forest = 2


class Gate(Choice): 
    """Set the state of the Kakariko Village gate."""
    display_name = "Kakariko Gate"
    option_open = 0
    option_zelda = 1
    option_closed = 2


class DoorOfTime(DefaultOnToggle):
    """Open the Door of Time by default, without the Song of Time."""
    display_name = "Open Door of Time"


class Fountain(Choice): 
    """Set the state of King Zora, blocking the way to Zora's Fountain."""
    display_name = "Zora's Fountain"
    option_open = 0
    option_adult = 1
    option_closed = 2
    default = 2


class Fortress(Choice): 
    """Set the requirements for access to Gerudo Fortress."""
    display_name = "Gerudo Fortress"
    option_normal = 0
    option_fast = 1
    option_open = 2
    default = 1


class Bridge(Choice): 
    """Set the requirements for the Rainbow Bridge."""
    display_name = "Rainbow Bridge Requirement"
    option_open = 0
    option_vanilla = 1
    option_stones = 2
    option_medallions = 3
    option_dungeons = 4
    option_tokens = 5
    default = 3


class Trials(Range):
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
    """Shuffles interior entrances. "Simple" shuffles houses and Great Fairies; "All" includes Windmill, Link's House, Temple of Time, and Kak potion shop."""
    display_name = "Shuffle Interior Entrances"
    option_off = 0
    option_simple = 1
    option_all = 2
    alias_false = 0
    alias_true = 2


class GrottoEntrances(Toggle):
    """Shuffles grotto and grave entrances."""
    display_name = "Shuffle Grotto/Grave Entrances"


class DungeonEntrances(Toggle):
    """Shuffles dungeon entrances, excluding Ganon's Castle. Opens Deku, Fire and BotW to both ages."""
    display_name = "Shuffle Dungeon Entrances"


class OverworldEntrances(Toggle):
    """Shuffles overworld loading zones."""
    display_name = "Shuffle Overworld Entrances"


class OwlDrops(Toggle):
    """Randomizes owl drops from Lake Hylia or Death Mountain Trail as child."""
    display_name = "Randomize Owl Drops"


class WarpSongs(Toggle):
    """Randomizes warp song destinations."""
    display_name = "Randomize Warp Songs"


class SpawnPositions(Toggle):
    """Randomizes the starting position on loading a save. Consistent between savewarps."""
    display_name = "Randomize Spawn Positions"


class MixEntrancePools(Choice):
    """Shuffles entrances into a mixed pool instead of separate ones. "indoor" keeps overworld entrances separate; "all" mixes them in."""
    display_name = "Mix Entrance Pools"
    option_off = 0
    option_indoor = 1
    option_all = 2
    alias_false = 0


class DecoupleEntrances(Toggle):
    """Decouple entrances when shuffling them. Also adds the one-way entrance from Gerudo Valley to Lake Hylia if overworld is shuffled."""
    display_name = "Decouple Entrances"


class TriforceHunt(Toggle):
    """Gather pieces of the Triforce scattered around the world to complete the game."""
    display_name = "Triforce Hunt"


class TriforceGoal(Range):
    """Number of Triforce pieces required to complete the game."""
    display_name = "Required Triforce Pieces"
    range_start = 1
    range_end = 100
    default = 20


class ExtraTriforces(Range):
    """Percentage of additional Triforce pieces in the pool, separate from the item pool setting."""
    display_name = "Percentage of Extra Triforce Pieces"
    range_start = 0
    range_end = 100
    default = 50


class LogicalChus(Toggle):
    """Bombchus are properly considered in logic. The first found pack will have 20 chus; Kokiri Shop and Bazaar sell refills; bombchus open Bombchu Bowling."""
    display_name = "Bombchus Considered in Logic"


class MQDungeons(Range):
    """Number of MQ dungeons. The dungeons to replace are randomly selected."""
    display_name = "Number of MQ Dungeons"
    range_start = 0
    range_end = 12
    default = 0


world_options: typing.Dict[str, type(Option)] = {
    "starting_age": StartingAge,
    "shuffle_interior_entrances": InteriorEntrances,
    "shuffle_grotto_entrances": GrottoEntrances,
    "shuffle_dungeon_entrances": DungeonEntrances,
    "shuffle_overworld_entrances": OverworldEntrances,
    "owl_drops": OwlDrops,
    "warp_songs": WarpSongs,
    "spawn_positions": SpawnPositions,
    # "mix_entrance_pools": MixEntrancePools,
    # "decouple_entrances": DecoupleEntrances,
    "triforce_hunt": TriforceHunt, 
    "triforce_goal": TriforceGoal,
    "extra_triforce_percentage": ExtraTriforces,
    "bombchus_in_logic": LogicalChus,
    "mq_dungeons": MQDungeons,
}


class LacsCondition(Choice): 
    """Set the requirements for the Light Arrow Cutscene in the Temple of Time."""
    display_name = "Light Arrow Cutscene Requirement"
    option_vanilla = 0
    option_stones = 1
    option_medallions = 2
    option_dungeons = 3
    option_tokens = 4


class LacsStones(Range):
    """Set the number of Spiritual Stones required for LACS."""
    display_name = "Spiritual Stones Required for LACS"
    range_start = 0
    range_end = 3
    default = 3


class LacsMedallions(Range):
    """Set the number of medallions required for LACS."""
    display_name = "Medallions Required for LACS"
    range_start = 0
    range_end = 6
    default = 6


class LacsRewards(Range):
    """Set the number of dungeon rewards required for LACS."""
    display_name = "Dungeon Rewards Required for LACS"
    range_start = 0
    range_end = 9
    default = 9


class LacsTokens(Range):
    """Set the number of Gold Skulltula Tokens required for LACS."""
    display_name = "Tokens Required for LACS"
    range_start = 0
    range_end = 100
    default = 40


lacs_options: typing.Dict[str, type(Option)] = {
    "lacs_condition": LacsCondition,
    "lacs_stones": LacsStones, 
    "lacs_medallions": LacsMedallions, 
    "lacs_rewards": LacsRewards, 
    "lacs_tokens": LacsTokens,
}


class BridgeStones(Range):
    """Set the number of Spiritual Stones required for the rainbow bridge."""
    display_name = "Spiritual Stones Required for Bridge"
    range_start = 0
    range_end = 3
    default = 3


class BridgeMedallions(Range):
    """Set the number of medallions required for the rainbow bridge."""
    display_name = "Medallions Required for Bridge"
    range_start = 0
    range_end = 6
    default = 6


class BridgeRewards(Range):
    """Set the number of dungeon rewards required for the rainbow bridge."""
    display_name = "Dungeon Rewards Required for Bridge"
    range_start = 0
    range_end = 9
    default = 9


class BridgeTokens(Range):
    """Set the number of Gold Skulltula Tokens required for the rainbow bridge."""
    display_name = "Tokens Required for Bridge"
    range_start = 0
    range_end = 100
    default = 40


bridge_options: typing.Dict[str, type(Option)] = {
    "bridge_stones": BridgeStones,
    "bridge_medallions": BridgeMedallions,
    "bridge_rewards": BridgeRewards, 
    "bridge_tokens": BridgeTokens,
}


class SongShuffle(Choice): 
    """Set where songs can appear."""
    display_name = "Shuffle Songs"
    option_song = 0
    option_dungeon = 1
    option_any = 2


class ShopShuffle(Choice): 
    """Randomizes shop contents. "fixed_number" randomizes a specific number of items per shop; 
    "random_number" randomizes the value for each shop. """
    display_name = "Shopsanity"
    option_off = 0
    option_fixed_number = 1
    option_random_number = 2
    alias_false = 0


class ShopSlots(Range):
    """Number of items per shop to be randomized into the main itempool. 
    Only active if Shopsanity is set to "fixed_number." """
    display_name = "Shuffled Shop Slots"
    range_start = 0
    range_end = 4


class TokenShuffle(Choice): 
    """Token rewards from Gold Skulltulas are shuffled into the pool."""
    display_name = "Tokensanity"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3
    alias_false = 0


class ScrubShuffle(Choice): 
    """Shuffle the items sold by Business Scrubs, and set the prices."""
    display_name = "Scrub Shuffle"
    option_off = 0
    option_low = 1
    option_regular = 2
    option_random_prices = 3
    alias_false = 0
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


class ShuffleEgg(Toggle):
    """Shuffle the Weird Egg from Malon at Hyrule Castle."""
    display_name = "Shuffle Weird Egg"


class ShuffleCard(Toggle):
    """Shuffle the Gerudo Membership Card into the item pool."""
    display_name = "Shuffle Gerudo Card"


class ShuffleBeans(Toggle):
    """Adds a pack of 10 beans to the item pool and changes the bean salesman to sell one item for 60 rupees."""
    display_name = "Shuffle Magic Beans"


class ShuffleMedigoronCarpet(Toggle):
    """Shuffle the items sold by Medigoron and the Haunted Wasteland Carpet Salesman."""
    display_name = "Shuffle Medigoron & Carpet Salesman"


shuffle_options: typing.Dict[str, type(Option)] = {
    "shuffle_song_items": SongShuffle,
    "shopsanity": ShopShuffle, 
    "shop_slots": ShopSlots,
    "tokensanity": TokenShuffle, 
    "shuffle_scrubs": ScrubShuffle,
    "shuffle_cows": ShuffleCows, 
    "shuffle_kokiri_sword": ShuffleSword,
    "shuffle_ocarinas": ShuffleOcarinas,
    "shuffle_weird_egg": ShuffleEgg,
    "shuffle_gerudo_card": ShuffleCard,
    "shuffle_beans": ShuffleBeans, 
    "shuffle_medigoron_carpet_salesman": ShuffleMedigoronCarpet,
}


class ShuffleMapCompass(Choice): 
    """Control where to shuffle dungeon maps and compasses."""
    display_name = "Maps & Compasses"
    option_remove = 0
    option_startwith = 1
    option_vanilla = 2
    option_dungeon = 3
    option_overworld = 4
    option_any_dungeon = 5
    option_keysanity = 6
    default = 1
    alias_anywhere = 6


class ShuffleKeys(Choice): 
    """Control where to shuffle dungeon small keys."""
    display_name = "Small Keys"
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_overworld = 4
    option_any_dungeon = 5
    option_keysanity = 6
    default = 3
    alias_keysy = 0
    alias_anywhere = 6


class ShuffleGerudoKeys(Choice): 
    """Control where to shuffle the Thieves' Hideout small keys."""
    display_name = "Thieves' Hideout Keys"
    option_vanilla = 0
    option_overworld = 1
    option_any_dungeon = 2
    option_keysanity = 3
    alias_anywhere = 3


class ShuffleBossKeys(Choice): 
    """Control where to shuffle boss keys, except the Ganon's Castle Boss Key."""
    display_name = "Boss Keys"
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_overworld = 4
    option_any_dungeon = 5
    option_keysanity = 6
    default = 3
    alias_keysy = 0
    alias_anywhere = 6


class ShuffleGanonBK(Choice):
    """Control where to shuffle the Ganon's Castle Boss Key."""
    display_name = "Ganon's Boss Key"
    option_remove = 0
    option_vanilla = 2
    option_dungeon = 3
    option_overworld = 4
    option_any_dungeon = 5
    option_keysanity = 6
    option_on_lacs = 7
    default = 0
    alias_keysy = 0
    alias_anywhere = 6


class EnhanceMC(Toggle):
    """Map tells if a dungeon is vanilla or MQ. Compass tells what the dungeon reward is."""
    display_name = "Maps and Compasses Give Information"


dungeon_items_options: typing.Dict[str, type(Option)] = {
    "shuffle_mapcompass": ShuffleMapCompass, 
    "shuffle_smallkeys": ShuffleKeys, 
    "shuffle_fortresskeys": ShuffleGerudoKeys, 
    "shuffle_bosskeys": ShuffleBossKeys,
    "shuffle_ganon_bosskey": ShuffleGanonBK,
    "enhance_map_compass": EnhanceMC,
}


class SkipChildZelda(Toggle):
    """Game starts with Zelda's Letter, the item at Zelda's Lullaby, and the relevant events already completed."""
    display_name = "Skip Child Zelda"


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
    """Reenables the Poe cutscene in Forest Temple, Darunia in Fire Temple, and Twinrova introduction. Mostly useful for glitched."""
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


timesavers_options: typing.Dict[str, type(Option)] = {
    "skip_child_zelda": SkipChildZelda, 
    "no_escape_sequence": SkipEscape, 
    "no_guard_stealth": SkipStealth, 
    "no_epona_race": SkipEponaRace, 
    "skip_some_minigame_phases": SkipMinigamePhases, 
    "complete_mask_quest": CompleteMaskQuest, 
    "useful_cutscenes": UsefulCutscenes, 
    "fast_chests": FastChests, 
    "free_scarecrow": FreeScarecrow, 
    "fast_bunny_hood": FastBunny,
    "chicken_count": ChickenCount,
    "big_poe_count": BigPoeCount,
}


class CSMC(Toggle):
    """Changes chests containing progression into large chests, and nonprogression into small chests."""
    display_name = "Chest Size Matches Contents"


class Hints(Choice): 
    """Gossip Stones can give hints about item locations."""
    display_name = "Gossip Stones"
    option_none = 0
    option_mask = 1
    option_agony = 2
    option_always = 3
    default = 3
    alias_false = 0


class MiscHints(DefaultOnToggle):
    """Controls whether the Temple of Time altar gives dungeon prize info and whether Ganondorf hints the Light Arrows."""
    display_name = "Misc Hints"


class HintDistribution(Choice):
    """Choose the hint distribution to use. Affects the frequency of strong hints, which items are always hinted, etc."""
    display_name = "Hint Distribution"
    option_balanced = 0
    option_ddr = 1
    option_league = 2
    option_mw2 = 3
    option_scrubs = 4
    option_strong = 5
    option_tournament = 6
    option_useless = 7
    option_very_strong = 8
    option_async = 9


class TextShuffle(Choice): 
    """Randomizes text in the game for comedic effect."""
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


class HeroMode(Toggle):
    """Hearts will not drop from enemies or objects."""
    display_name = "Hero Mode"


class StartingToD(Choice):
    """Change the starting time of day."""
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


class ConsumableStart(Toggle):
    """Start the game with full Deku Sticks and Deku Nuts."""
    display_name = "Start with Consumables"


class RupeeStart(Toggle):
    """Start with a full wallet. Wallet upgrades will also fill your wallet."""
    display_name = "Start with Rupees"


misc_options: typing.Dict[str, type(Option)] = {
    "correct_chest_sizes": CSMC,
    "hints": Hints,
    "misc_hints": MiscHints,
    "hint_dist": HintDistribution,
    "text_shuffle": TextShuffle,
    "damage_multiplier": DamageMultiplier,
    "no_collectible_hearts": HeroMode,
    "starting_tod": StartingToD,
    "start_with_consumables": ConsumableStart, 
    "start_with_rupees": RupeeStart,
}

class ItemPoolValue(Choice): 
    """Changes the number of items available in the game."""
    display_name = "Item Pool"
    option_plentiful = 0
    option_balanced = 1
    option_scarce = 2
    option_minimal = 3
    default = 1


class IceTraps(Choice): 
    """Adds ice traps to the item pool."""
    display_name = "Ice Traps"
    option_off = 0
    option_normal = 1
    option_on = 2
    option_mayhem = 3
    option_onslaught = 4
    default = 1
    alias_false = 0
    alias_true = 2
    alias_extra = 2


class IceTrapVisual(Choice): 
    """Changes the appearance of ice traps as freestanding items."""
    display_name = "Ice Trap Appearance"
    option_major_only = 0
    option_junk_only = 1
    option_anything = 2


class AdultTradeItem(Choice): 
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


class EarlyTradeItem(AdultTradeItem):
    """Earliest item that can appear in the adult trade sequence."""
    display_name = "Adult Trade Sequence Earliest Item"
    default = 6


class LateTradeItem(AdultTradeItem):
    """Latest item that can appear in the adult trade sequence."""
    display_name = "Adult Trade Sequence Latest Item"
    default = 9


itempool_options: typing.Dict[str, type(Option)] = {
    "item_pool_value": ItemPoolValue, 
    "junk_ice_traps": IceTraps,
    "ice_trap_appearance": IceTrapVisual, 
    "logic_earliest_adult_trade": EarlyTradeItem, 
    "logic_latest_adult_trade": LateTradeItem,
}

# Start of cosmetic options

class Targeting(Choice): 
    """Default targeting option."""
    display_name = "Default Targeting Option"
    option_hold = 0
    option_switch = 1


class DisplayDpad(DefaultOnToggle):
    """Show dpad icon on HUD for quick actions (ocarina, hover boots, iron boots)."""
    display_name = "Display D-Pad HUD"


class CorrectColors(DefaultOnToggle):
    """Makes in-game models match their HUD element colors."""
    display_name = "Item Model Colors Match Cosmetics"


class Music(Choice): 
    option_normal = 0
    option_off = 1
    option_randomized = 2
    alias_false = 1


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
A full list of supported tricks can be found at https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/oot/LogicTricks.py"""
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
    **lacs_options,
    **shuffle_options,
    **timesavers_options,
    **misc_options, 
    **itempool_options,
    **cosmetic_options,
    **sfx_options,
    "logic_tricks": LogicTricks,
    "death_link": DeathLink,
}
