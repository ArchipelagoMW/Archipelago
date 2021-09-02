import typing
from Options import Option, DefaultOnToggle, Toggle, Choice, Range, OptionList
from .Colors import *
import worlds.oot.Sounds as sfx


class Logic(Choice): 
    """Set the logic used for the generator."""
    displayname = "Logic Rules"
    option_glitchless = 0
    option_glitched = 1
    option_no_logic = 2


class NightTokens(Toggle):
    """Nighttime skulltulas will logically require Sun's Song."""
    displayname = "Nighttime Skulltulas Expect Sun's Song"


class Forest(Choice): 
    """Set the state of Kokiri Forest and the path to Deku Tree."""
    displayname = "Forest"
    option_open = 0
    option_closed_deku = 1
    option_closed = 2
    alias_open_forest = 0
    alias_closed_forest = 2


class Gate(Choice): 
    """Set the state of the Kakariko Village gate."""
    displayname = "Kakariko Gate"
    option_open = 0
    option_zelda = 1
    option_closed = 2


class DoorOfTime(DefaultOnToggle):
    """Open the Door of Time by default, without the Song of Time."""
    displayname = "Open Door of Time"


class Fountain(Choice): 
    """Set the state of King Zora, blocking the way to Zora's Fountain."""
    displayname = "Zora's Fountain"
    option_open = 0
    option_adult = 1
    option_closed = 2
    default = 2


class Fortress(Choice): 
    """Set the requirements for access to Gerudo Fortress."""
    displayname = "Gerudo Fortress"
    option_normal = 0
    option_fast = 1
    option_open = 2
    default = 1


class Bridge(Choice): 
    """Set the requirements for the Rainbow Bridge."""
    displayname = "Rainbow Bridge Requirement"
    option_open = 0
    option_vanilla = 1
    option_stones = 2
    option_medallions = 3
    option_dungeons = 4
    option_tokens = 5
    default = 3


class Trials(Range):
    """Set the number of required trials in Ganon's Castle."""
    displayname = "Ganon's Trials Count"
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
    displayname = "Starting Age"
    option_child = 0
    option_adult = 1


# TODO: document and name ER options
class InteriorEntrances(Choice): 
    option_off = 0
    option_simple = 1
    option_all = 2
    alias_false = 0


class TriforceHunt(Toggle):
    """Gather pieces of the Triforce scattered around the world to complete the game."""
    displayname = "Triforce Hunt"


class TriforceGoal(Range):
    """Number of Triforce pieces required to complete the game. Total number placed determined by the Item Pool setting."""
    displayname = "Required Triforce Pieces"
    range_start = 1
    range_end = 50
    default = 20


class LogicalChus(Toggle):
    """Bombchus are properly considered in logic. The first found pack will have 20 chus; Kokiri Shop and Bazaar sell refills; bombchus open Bombchu Bowling."""
    displayname = "Bombchus Considered in Logic"


world_options: typing.Dict[str, type(Option)] = {
    "starting_age": StartingAge,
    # "shuffle_interior_entrances": InteriorEntrances,
    # "shuffle_grotto_entrances": Toggle,
    # "shuffle_dungeon_entrances": Toggle,
    # "shuffle_overworld_entrances": Toggle,
    # "owl_drops": Toggle,
    # "warp_songs": Toggle,
    # "spawn_positions": Toggle,
    "triforce_hunt": TriforceHunt, 
    "triforce_goal": TriforceGoal,
    "bombchus_in_logic": LogicalChus,
    # "mq_dungeons": make_range(0, 12),
}


class LacsCondition(Choice): 
    """Set the requirements for the Light Arrow Cutscene in the Temple of Time."""
    displayname = "Light Arrow Cutscene Requirement"
    option_vanilla = 0
    option_stones = 1
    option_medallions = 2
    option_dungeons = 3
    option_tokens = 4


class LacsStones(Range):
    """Set the number of Spiritual Stones required for LACS."""
    displayname = "Spiritual Stones Required for LACS"
    range_start = 0
    range_end = 3
    default = 3


class LacsMedallions(Range):
    """Set the number of medallions required for LACS."""
    displayname = "Medallions Required for LACS"
    range_start = 0
    range_end = 6
    default = 6


class LacsRewards(Range):
    """Set the number of dungeon rewards required for LACS."""
    displayname = "Dungeon Rewards Required for LACS"
    range_start = 0
    range_end = 9
    default = 9


class LacsTokens(Range):
    """Set the number of Gold Skulltula Tokens required for LACS."""
    displayname = "Tokens Required for LACS"
    range_start = 0
    range_end = 100
    default = 100


lacs_options: typing.Dict[str, type(Option)] = {
    "lacs_condition": LacsCondition,
    "lacs_stones": LacsStones, 
    "lacs_medallions": LacsMedallions, 
    "lacs_rewards": LacsRewards, 
    "lacs_tokens": LacsTokens,
}


class BridgeStones(Range):
    """Set the number of Spiritual Stones required for the rainbow bridge."""
    displayname = "Spiritual Stones Required for Bridge"
    range_start = 0
    range_end = 3
    default = 3


class BridgeMedallions(Range):
    """Set the number of medallions required for the rainbow bridge."""
    displayname = "Medallions Required for Bridge"
    range_start = 0
    range_end = 6
    default = 6


class BridgeRewards(Range):
    """Set the number of dungeon rewards required for the rainbow bridge."""
    displayname = "Dungeon Rewards Required for Bridge"
    range_start = 0
    range_end = 9
    default = 9


class BridgeTokens(Range):
    """Set the number of Gold Skulltula Tokens required for the rainbow bridge."""
    displayname = "Tokens Required for Bridge"
    range_start = 0
    range_end = 100
    default = 100


bridge_options: typing.Dict[str, type(Option)] = {
    "bridge_stones": BridgeStones,
    "bridge_medallions": BridgeMedallions,
    "bridge_rewards": BridgeRewards, 
    "bridge_tokens": BridgeTokens,
}


class SongShuffle(Choice): 
    """Set where songs can appear."""
    displayname = "Shuffle Songs"
    option_song = 0
    option_dungeon = 1
    option_any = 2


class ShopShuffle(Choice): 
    """Randomizes shop contents. Set to "off" to not shuffle shops; "0" shuffles shops but does not allow multiworld items in shops."""
    displayname = "Shopsanity"
    option_0 = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_4 = 4
    option_random_value = 5
    option_off = 6
    default = 6
    alias_false = 6


class TokenShuffle(Choice): 
    """Token rewards from Gold Skulltulas are shuffled into the pool."""
    displayname = "Tokensanity"
    option_off = 0
    option_dungeons = 1
    option_overworld = 2
    option_all = 3
    alias_false = 0


class ScrubShuffle(Choice): 
    """Shuffle the items sold by Business Scrubs, and set the prices."""
    displayname = "Scrub Shuffle"
    option_off = 0
    option_low = 1
    option_regular = 2
    option_random_prices = 3
    alias_false = 0
    alias_affordable = 1
    alias_expensive = 2


class ShuffleCows(Toggle):
    """Cows give items when Epona's Song is played."""
    displayname = "Shuffle Cows"


class ShuffleSword(Toggle):
    """Shuffle Kokiri Sword into the item pool."""
    displayname = "Shuffle Kokiri Sword"


class ShuffleOcarinas(Toggle):
    """Shuffle the Fairy Ocarina and Ocarina of Time into the item pool."""
    displayname = "Shuffle Ocarinas"


class ShuffleEgg(Toggle):
    """Shuffle the Weird Egg from Malon at Hyrule Castle."""
    displayname = "Shuffle Weird Egg"


class ShuffleCard(Toggle):
    """Shuffle the Gerudo Membership Card into the item pool."""
    displayname = "Shuffle Gerudo Card"


class ShuffleBeans(Toggle):
    """Adds a pack of 10 beans to the item pool and changes the bean salesman to sell one item for 60 rupees."""
    displayname = "Shuffle Magic Beans"


class ShuffleMedigoronCarpet(Toggle):
    """Shuffle the items sold by Medigoron and the Haunted Wasteland Carpet Salesman."""
    displayname = "Shuffle Medigoron & Carpet Salesman"


shuffle_options: typing.Dict[str, type(Option)] = {
    "shuffle_song_items": SongShuffle,
    "shopsanity": ShopShuffle, 
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
    displayname = "Maps & Compasses"
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
    displayname = "Small Keys"
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
    """Control where to shuffle the Gerudo Fortress small keys."""
    displayname = "Gerudo Fortress Keys"
    option_vanilla = 0
    option_overworld = 1
    option_any_dungeon = 2
    option_keysanity = 3
    alias_anywhere = 3


class ShuffleBossKeys(Choice): 
    """Control where to shuffle boss keys, except the Ganon's Castle Boss Key."""
    displayname = "Boss Keys"
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
    displayname = "Ganon's Boss Key"
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
    displayname = "Maps and Compasses Give Information"


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
    displayname = "Skip Child Zelda"


class SkipEscape(DefaultOnToggle):
    """Skips the tower collapse sequence between the Ganondorf and Ganon fights."""
    displayname = "Skip Tower Escape Sequence"


class SkipStealth(DefaultOnToggle):
    """The crawlspace into Hyrule Castle skips straight to Zelda."""
    displayname = "Skip Child Stealth"


class SkipEponaRace(DefaultOnToggle):
    """Epona can always be summoned with Epona's Song."""
    displayname = "Skip Epona Race"


class SkipMinigamePhases(DefaultOnToggle):
    """Dampe Race and Horseback Archery give both rewards if the second condition is met on the first attempt."""
    displayname = "Skip Some Minigame Phases"


class CompleteMaskQuest(Toggle):
    """All masks are immediately available to borrow from the Happy Mask Shop."""
    displayname = "Complete Mask Quest"


class UsefulCutscenes(Toggle):
    """Reenables the Poe cutscene in Forest Temple, Darunia in Fire Temple, and Twinrova introduction. Mostly useful for glitched."""
    displayname = "Enable Useful Cutscenes"


class FastChests(DefaultOnToggle):
    """All chest animations are fast. If disabled, major items have a slow animation."""
    displayname = "Fast Chest Cutscenes"


class FreeScarecrow(Toggle):
    """Pulling out the ocarina near a scarecrow spot spawns Pierre without needing the song."""
    displayname = "Free Scarecrow's Song"


class FastBunny(Toggle):
    """Bunny Hood lets you move 1.5x faster like in Majora's Mask."""
    displayname = "Fast Bunny Hood"


class ChickenCount(Range):
    """Controls the number of Cuccos for Anju to give an item as child."""
    displayname = "Cucco Count"
    range_start = 0
    range_end = 7
    default = 7


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
    # "big_poe_count": make_range(1, 10, 1),
}


class Hints(Choice): 
    """Gossip Stones can give hints about item locations."""
    displayname = "Gossip Stones"
    option_none = 0
    option_mask = 1
    option_agony = 2
    option_always = 3
    default = 3
    alias_false = 0


class HintDistribution(Choice):
    """Choose the hint distribution to use. Affects the frequency of strong hints, which items are always hinted, etc."""
    displayname = "Hint Distribution"
    option_balanced = 0
    option_ddr = 1
    option_league = 2
    option_mw2 = 3
    option_scrubs = 4
    option_strong = 5
    option_tournament = 6
    option_useless = 7
    option_very_strong = 8


class TextShuffle(Choice): 
    """Randomizes text in the game for comedic effect."""
    displayname = "Text Shuffle"
    option_none = 0
    option_except_hints = 1
    option_complete = 2
    alias_false = 0


class DamageMultiplier(Choice): 
    """Controls the amount of damage Link takes."""
    displayname = "Damage Multiplier"
    option_half = 0
    option_normal = 1
    option_double = 2
    option_quadruple = 3
    option_ohko = 4
    default = 1


class HeroMode(Toggle):
    """Hearts will not drop from enemies or objects."""
    displayname = "Hero Mode"


class StartingToD(Choice):
    """Change the starting time of day."""
    displayname = "Starting Time of Day"
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
    displayname = "Start with Consumables"


class RupeeStart(Toggle):
    """Start with a full wallet. Wallet upgrades will also fill your wallet."""
    displayname = "Start with Rupees"


misc_options: typing.Dict[str, type(Option)] = {
    # "clearer_hints": DefaultOnToggle,
    "hints": Hints,
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
    displayname = "Item Pool"
    option_plentiful = 0
    option_balanced = 1
    option_scarce = 2
    option_minimal = 3
    default = 1


class IceTraps(Choice): 
    """Adds ice traps to the item pool."""
    displayname = "Ice Traps"
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
    displayname = "Ice Trap Appearance"
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
    displayname = "Adult Trade Sequence Earliest Item"
    default = 6


class LateTradeItem(AdultTradeItem):
    """Latest item that can appear in the adult trade sequence."""
    displayname = "Adult Trade Sequence Latest Item"
    default = 9


itempool_options: typing.Dict[str, type(Option)] = {
    "item_pool_value": ItemPoolValue, 
    "junk_ice_traps": IceTraps,
    "ice_trap_appearance": IceTrapVisual, 
    "logic_earliest_adult_trade": EarlyTradeItem, 
    "logic_latest_adult_trade": LateTradeItem,
}

# Start of cosmetic options

def assemble_color_option(func, display_name: str, default_option: str, outer=False): 
    color_options = func()
    if outer:
        color_options.append("Match Inner")
    format_color = lambda color: color.replace(' ', '_').lower()
    color_to_id = {format_color(color): index for index, color in enumerate(color_options)}
    class ColorOption(Choice):
        """Choose a color. "random_choice" selects a random option. "completely_random" generates a random hex code."""
        displayname = display_name
        default = color_options.index(default_option)
    ColorOption.options.update(color_to_id)
    ColorOption.name_lookup.update({id: color for (color, id) in color_to_id.items()})
    return ColorOption


class Targeting(Choice): 
    """Default targeting option."""
    displayname = "Default Targeting Option"
    option_hold = 0
    option_switch = 1


class DisplayDpad(DefaultOnToggle):
    """Show dpad icon on HUD for quick actions (ocarina, hover boots, iron boots)."""
    displayname = "Display D-Pad HUD"


class CorrectColors(DefaultOnToggle):
    """Makes in-game models match their HUD element colors."""
    displayname = "Item Model Colors Match Cosmetics"


class Music(Choice): 
    option_normal = 0
    option_off = 1
    option_randomized = 2
    alias_false = 1


class BackgroundMusic(Music):
    """Randomize or disable background music."""
    displayname = "Background Music"


class Fanfares(Music):
    """Randomize or disable item fanfares."""
    displayname = "Fanfares"


class OcarinaFanfares(Toggle):
    """Enable ocarina songs as fanfares. These are longer than usual fanfares. Does nothing without fanfares randomized."""
    displayname = "Ocarina Songs as Fanfares"


class SwordTrailDuration(Range):
    """Set the duration for sword trails."""
    displayname = "Sword Trail Duration"
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
    "kokiri_color": assemble_color_option(get_tunic_color_options, "Kokiri Tunic", "Kokiri Green"),
    "goron_color":  assemble_color_option(get_tunic_color_options, "Goron Tunic", "Goron Red"),
    "zora_color":   assemble_color_option(get_tunic_color_options, "Zora Tunic", "Zora Blue"),
    "silver_gauntlets_color":   assemble_color_option(get_gauntlet_color_options, "Silver Gauntlets Color", "Silver"),
    "golden_gauntlets_color":   assemble_color_option(get_gauntlet_color_options, "Golden Gauntlets Color", "Gold"),
    "mirror_shield_frame_color": assemble_color_option(get_shield_frame_color_options, "Mirror Shield Frame Color", "Red"),
    "navi_color_default_inner": assemble_color_option(get_navi_color_options, "Navi Idle Inner", "White"),
    "navi_color_default_outer": assemble_color_option(get_navi_color_options, "Navi Idle Outer", "Match Inner", outer=True),
    "navi_color_enemy_inner":   assemble_color_option(get_navi_color_options, "Navi Targeting Enemy Inner", "Yellow"),
    "navi_color_enemy_outer":   assemble_color_option(get_navi_color_options, "Navi Targeting Enemy Outer", "Match Inner", outer=True),
    "navi_color_npc_inner":     assemble_color_option(get_navi_color_options, "Navi Targeting NPC Inner", "Light Blue"),
    "navi_color_npc_outer":     assemble_color_option(get_navi_color_options, "Navi Targeting NPC Outer", "Match Inner", outer=True),
    "navi_color_prop_inner":    assemble_color_option(get_navi_color_options, "Navi Targeting Prop Inner", "Green"),
    "navi_color_prop_outer":    assemble_color_option(get_navi_color_options, "Navi Targeting Prop Outer", "Match Inner", outer=True),
    "sword_trail_duration": SwordTrailDuration,
    "sword_trail_color_inner": assemble_color_option(get_sword_trail_color_options, "Sword Trail Inner", "White"),
    "sword_trail_color_outer": assemble_color_option(get_sword_trail_color_options, "Sword Trail Outer", "Match Inner", outer=True),
    "bombchu_trail_color_inner": assemble_color_option(get_bombchu_trail_color_options, "Bombchu Trail Inner", "Red"),
    "bombchu_trail_color_outer": assemble_color_option(get_bombchu_trail_color_options, "Bombchu Trail Outer", "Match Inner", outer=True),
    "boomerang_trail_color_inner": assemble_color_option(get_boomerang_trail_color_options, "Boomerang Trail Inner", "Yellow"),
    "boomerang_trail_color_outer": assemble_color_option(get_boomerang_trail_color_options, "Boomerang Trail Outer", "Match Inner", outer=True),
    "heart_color":          assemble_color_option(get_heart_color_options, "Heart Color", "Red"),
    "magic_color":          assemble_color_option(get_magic_color_options, "Magic Color", "Green"),
    "a_button_color":       assemble_color_option(get_a_button_color_options, "A Button Color", "N64 Blue"),
    "b_button_color":       assemble_color_option(get_b_button_color_options, "B Button Color", "N64 Green"),
    "c_button_color":       assemble_color_option(get_c_button_color_options, "C Button Color", "Yellow"),
    "start_button_color":   assemble_color_option(get_start_button_color_options, "Start Button Color", "N64 Red"),
}

def assemble_sfx_option(sound_hook: sfx.SoundHooks, display_name: str):
    options = sfx.get_setting_choices(sound_hook).keys()
    sfx_to_id = {sfx.replace('-', '_'): index for index, sfx in enumerate(options)}
    class SfxOption(Choice):
        """Choose a sound effect. "random_choice" selects a random option. "random_ear_safe" selects a random safe option. "completely_random" selects any random sound."""
        displayname = display_name
    SfxOption.options.update(sfx_to_id)
    SfxOption.name_lookup.update({id: sfx for (sfx, id) in sfx_to_id.items()})
    return SfxOption

class SfxOcarina(Choice):
    """Change the sound of the ocarina."""
    displayname = "Ocarina Instrument"
    option_ocarina = 1
    option_malon = 2
    option_whistle = 3
    option_harp = 4
    option_grind_organ = 5
    option_flute = 6
    default = 1

sfx_options: typing.Dict[str, type(Option)] = {
    "sfx_navi_overworld":   assemble_sfx_option(sfx.SoundHooks.NAVI_OVERWORLD, "Navi Overworld"),
    "sfx_navi_enemy":       assemble_sfx_option(sfx.SoundHooks.NAVI_ENEMY, "Navi Enemy"),
    "sfx_low_hp":           assemble_sfx_option(sfx.SoundHooks.HP_LOW, "Low HP"),
    "sfx_menu_cursor":      assemble_sfx_option(sfx.SoundHooks.MENU_CURSOR, "Menu Cursor"),
    "sfx_menu_select":      assemble_sfx_option(sfx.SoundHooks.MENU_SELECT, "Menu Select"),
    "sfx_nightfall":        assemble_sfx_option(sfx.SoundHooks.NIGHTFALL, "Nightfall"),
    "sfx_horse_neigh":      assemble_sfx_option(sfx.SoundHooks.HORSE_NEIGH, "Horse"),
    "sfx_hover_boots":      assemble_sfx_option(sfx.SoundHooks.BOOTS_HOVER, "Hover Boots"),
    "sfx_ocarina":          SfxOcarina,
}


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
    "logic_tricks": OptionList,
}
