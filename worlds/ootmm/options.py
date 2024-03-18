from typing import Dict, Type

from Options import Choice, Option, DefaultOnToggle, Toggle, Range, OptionList, OptionSet, DeathLink

class Goal(Choice):
    display_name = "Goal"
    option_any = 1
    option_ganon = 2
    option_majora = 3
    option_both = 4
    option_triforce = 5
    option_triforce3 = 6
    
class TriforceGoal(Range):
    display_name = "Required Triforce Pieces"
    range_start = 1
    range_end = 999
    default = 20

class TriforcePieces(Range):
    display_name = "Total Triforce Pieces"
    range_start = 1
    range_end = 999
    default = 30
    
class ItemPool(Choice):
    display_name = "Goal"
    option_plentiful = 1
    option_normal = 2
    option_scarce = 3
    option_minimal = 4
    option_barren = 5
    
class HintImportance(Toggle):
    display_name = "Hint Importance"

class SongShuffle(Choice):
    display_name = "Song Shuffle"
    option_song_locations = 1
    option_anywhere = 2

class GoldSkulltulaTokensShuffle(Choice):
    display_name = "Gold Skulltula Tokens Shuffle"
    option_none = 1
    option_dungeons = 2
    option_overworld = 3
    option_all = 4

class HouseSkulltulaTokensShuffle(Choice):
    display_name = "House Skulltula Tokens Shuffle"
    option_none = 1
    option_cross = 2
    option_all = 3

class TingleMapsShuffle(Choice):
    display_name = "Tingle Map Shuffle"
    option_vanilla = 1
    option_anywhere = 2
    option_starting = 3
    option_removed = 4
    
class MapCompassShuffle(Choice):
    display_name = "Map/Compass Shuffle"
    option_own_dungeon = 1
    option_anywhere = 2
    option_starting = 3
    option_removed = 4

class SmallKeyShuffleOoT(Choice):
    display_name = "Small Key Shuffle (OoT)"
    option_own_dungeon = 1
    option_anywhere = 2
    option_removed = 3
    
class SmallKeyShuffleMM(Choice):
    display_name = "Small Key Shuffle (MM)"
    option_own_dungeon = 1
    option_anywhere = 2
    option_removed = 3

class HideoutSmallKeyShuffle(Choice):
    display_name = "Hideout Small Key Shuffle"
    option_ownDungeon = 1
    option_anywhere = 2
    option_removed = 3

class ChestGameSmallKeyShuffle(Choice):
    display_name = "Chest Game Small Key Shuffle"
    option_own_dungeon = 1
    option_anywhere = 2
    option_removed = 3

class BossKeyShuffleOoT(Choice):
    display_name = "Boss Key Shuffle (OoT)"
    option_own_dungeon = 1
    option_anywhere = 2
    option_removed = 3

class BossKeyShuffleMM(Choice):
    display_name = "Boss Key Shuffle (MM)"
    option_ownDungeon = 1
    option_anywhere = 2
    option_removed = 3

class SmallKeyRingOoT(Choice):
    display_name = "Small Key Ring (OoT)"
    option_none = 1
    option_all = 2
    option_specifc = 3
    option_random = 4
    
class KeyRingListOoT(OptionSet):
    """With key rings as Choose: select areas with key rings rather than individual small keys."""
    display_name = "Key Ring Areas (OoT)"
    valid_keys = {
        "Forest",
        "Fire",
        "Water",
        "Shadow",
        "Spirit",
        "BotW",
        "GTG",
        "GF",
        "TCG",
    }

class SmallKeyRingMM(Choice):
    display_name = "Small Key Ring (MM)"
    option_none = 1
    option_all = 2
    option_specifc = 3
    option_random = 4
    
class KeyRingListMM(OptionSet):
    """With key rings as Choose: select areas with key rings rather than individual small keys."""
    display_name = "Key Ring Areas (OoT)"
    valid_keys = {
        "WF",
        "SH",
        "GB",
        "ST",
    }

class SilverRupeeShuffle(Choice):
    display_name = "Silver Rupee Shuffle"
    option_vanilla = 1
    option_own_dungeon = 2
    option_anywhere = 3
    
class TownStrayFairyShuffle(Choice):
    display_name = "Town Stray Fairy Shuffle"
    option_vanilla = 1
    option_anywhere = 2
    
class DungeonChestFairyShuffle(Choice):
    display_name = "Dungeon Chest Fairy Shuffle"
    option_vanilla = 1
    option_own_dungeon = 2
    option_anywhere = 3
    option_starting = 4
    
class DungeonFreestandingFairyShuffle(Choice):
    display_name = "Dungeon Freestanding Fairy Shuffle"
    option_vanilla = 1
    option_own_dungeon = 2
    option_anywhere = 3
    option_starting = 4
    option_removed = 5

class DungeonRewardShuffle(Choice):
    display_name = "Dungeon Reward Shuffle"
    option_dungeons_blue_warps = 1
    option_dungeons_limited = 2
    option_dungeons = 3
    option_anywhere = 4

class ShopShuffleOoT(Choice):
    display_name = "Shop Shuffle (OoT)"
    option_none = 1
    option_full = 2

class ShopShuffleMM(Choice):
    display_name = "Shop Shuffle (MM)"
    option_none = 1
    option_full = 2

class OwlStatueShuffle(Choice):
    display_name = "Owl Statue Shuffle"
    option_none = 1
    option_anywhere = 2

class ScrubShuffleOoT(Toggle):
    display_name = "Scrub Shuffle (OoT)"

class ScrubShuffleMM(Toggle):
    display_name = "Scrub Shuffle (MM)"

class CowShuffleOoT(Toggle):
    display_name = "Cow Shuffle (OoT)"

class CowShuffleMM(Toggle):
    display_name = "Cow Shuffle (MM)"

class PotsShuffleOoT(Toggle):
    display_name = "Pots Shuffle (OoT)"

class PotsShuffleMM(Toggle):
    display_name = "Pots Shuffle (MM)"

class GrassShuffleOoT(Toggle):
    display_name = "Grass Shuffle (OoT)"

class GrassShuffleMM(Toggle):
    display_name = "Grass Shuffle (MM)"

class FreestandingRupeesShuffleOoT(Toggle):
    display_name = "Freestanding Rupees Shuffle (OoT)"

class FreestandingRupeesShuffleMM(Toggle):
    display_name = "Freestanding Rupees Shuffle (MM)"

class FreestandingHeartsShuffleOoT(Toggle):
    display_name = "Freestanding Hearts Shuffle (Oot)"

class FreestandingHeartsShuffleMM(Toggle):
    display_name = "Freestanding Hearts Shuffle (MM)"

class OcarinaShuffleOoT(Toggle):
    display_name = "Ocarina Shuffle (OoT)"

class MasterSwordShuffle(Toggle):
    display_name = "Master Sword Shuffle"

class GerudoCardShuffle(Toggle):
    display_name = "Gerudo Card Shuffle"

class MerchantsShuffleMM(Toggle):
    display_name = "Merchants Shuffle (MM)"

class FishingPondFishShuffle(Toggle):
    display_name = "Fishing Pond Fish Shuffle"

class DivingGameRupeeShuffle(Toggle):
    display_name = "Diving Game Rupee Shuffle"

class FairyFountainFairyShuffleOoT(Toggle):
    display_name = "Fairy Fountain Fairy Shuffle (OoT)"

class FairyFountainFairyShuffleMM(Toggle):
    display_name = "Fairy Fountain Fairy Shuffle (MM)"

class FairySpotShuffleOoT(Toggle):
    display_name = "Fairy Spot Shuffle (OoT)"

class WeirdPocketEggContentShuffle(Toggle):
    display_name = "Weird Pocket Egg Content Shuffle"

class OoTShopsPrices(Choice):
    display_name = "OoT Shops Prices"
    option_affordable = 1
    option_vanilla = 2
    option_weighted = 3
    option_random = 4

class OoTScrubsPrices(Choice):
    display_name = "OoT Scrubs Prices"
    option_affordable = 1
    option_vanilla = 2
    option_weighted = 3
    option_random = 4

class MMShopsPrices(Choice):
    display_name = "MM Shops Prices"
    option_affordable = 1
    option_vanilla = 2
    option_weighted = 3
    option_random = 4

class MMTinglePrices(Choice):
    display_name = "MM Tingle Prices"
    option_affordable = 1
    option_vanilla = 2
    option_weighted = 3
    option_random = 4

class GanonTrials(Choice):
    display_name = "Ganon Trials"
    option_none = 1
    option_all = 2
    option_specifc = 3
    option_random = 4
    
class GanonTrialsList(OptionSet):
    """With key rings as Choose: select areas with key rings rather than individual small keys."""
    display_name = "Key Ring Areas (OoT)"
    valid_keys = {
        "Light",
        "Forest",
        "Fire",
        "Water",
        "Shadow",
        "Spirit",
    }

class MoonCrashBehavior(Choice):
    display_name = "Moon Crash Behavior"
    option_reset = 1
    option_cycle = 2

class StartingAge(Choice):
    display_name = "Starting Age"
    option_child = 1
    option_adult = 2
    option_random = 2

class DoorOfTime(Choice):
    display_name = "Door of Time"
    option_closed = 1
    option_open = 2

class AgeChangeUponSongOfTime(Choice):
    display_name = "Age Change upon Song of Time"
    option_none = 1
    option_oot = 2
    option_always = 3

class DekuTree(Choice):
    display_name = "Deku Tree"
    option_closed = 1
    option_open = 2

class OpenDungeonsMM(Choice):
    display_name = "Open Dungeons (MM)"
    option_none = 1
    option_all = 2
    option_specifc = 3
    option_random = 4

class OpenDungeonsMMList(OptionSet):
    display_name = "Open Dungeons"
    valid_keys = {
        "WF",
        "SH",
        "GB",
        "ST",
    }

class ClearStateDungeonsMM(Choice):
    display_name = "ClearState Dungeons (MM)"
    option_none = 1
    option_wf = 2
    option_gb = 3
    option_both = 4

class KakarikoGate(Choice):
    display_name = "Kakariko Gate"
    option_closed = 1
    option_open = 2

class KingZora(Choice):
    display_name = "King Zora"
    option_vanilla = 1
    option_adult = 2
    option_open = 3

class GerudoFortress(Choice):
    display_name = "Gerudo Fortress"
    option_vanilla = 1
    option_sinlge = 2
    option_open = 3

class LightArrowCutscene(Choice):
    display_name = "Light Arrow Cutscene"
    option_vanilla = 1
    option_custom = 2

class RainbowBridge(Choice):
    display_name = "Rainbow Bridge"
    option_open = 1
    option_vanilla = 2
    option_medallions = 3
    option_custom = 4
    
class BossWarpPads(Choice):
    display_name = "Boss Warp Pads"
    option_boss_beaten = 1
    option_remains = 2

class DekuTreeAsAdult(Toggle):
    display_name = "Deku Tree as Adult"

class WellAsAdult(Toggle):
    display_name = "Well as Adult"

class FireTempleAsChild(Toggle):
    display_name = "Fire Temple as Child"

class OpenZorasDomainShortcut(Toggle):
    display_name = "Open Zoras Domain Shortcut"

class SkipChildZelda(Toggle):
    display_name = "Skip Child Zelda"

class SkipOathToOrder(Toggle):
    display_name = "Skip Oath to Order"

class FreeScarecrowOoT(Toggle):
    display_name = "Free Scarecrow (OoT)"

class PreCompletedDungeons(Toggle):
    display_name = "Pre-completed Dungeons"

class OpenMaskShopAtNight(Toggle):
    display_name = "Open Mask Shop at Night"

class CrossGamesMMSongOfSoaring(Choice):
    display_name = "Cross Games MM Song of Soaring"
    option_none = 1
    option_child_only = 2
    option_full = 3

class CrossGamesOoTWarpSongs(Toggle):
    display_name = "Cross Games OoT Warp Songs"

class ContainerAppearanceMatchesContent(Choice):
    display_name = "Container Appearance Matches Content"
    option_never = 1
    option_agony = 2
    option_always = 3

class BlastMaskCooldown(Choice):
    display_name = "Blast Mask Cooldown"
    option_instant = 1
    option_very_short = 2
    option_short = 3
    option_default = 4
    option_long = 5
    option_verylong = 6

class ClockSpeed(Choice):
    display_name = "Clock Speed"
    option_very_slow = 1
    option_slow = 2
    option_default = 3
    option_fast = 4
    option_superfast = 5

class AutoInvertTimeMM(Choice):
    display_name = "Auto Invert Time (MM)"
    option_never = 1
    option_first_cycle = 2
    option_always = 3

class CAMCForHeartPiecesContainers(Toggle):
    display_name = "CAMC for Heart Pieces Containers"

class SkulltulaCAMC(Toggle):
    display_name = "Skulltula CAMC"

class FierceDeityAnywhereInMM(Toggle):
    display_name = "Fierce Deity Anywhere in MM"

class HookshotAnywhereOoT(Toggle):
    display_name = "Hookshot Anywhere (OoT)"

class HookshotAnywhereMM(Toggle):
    display_name = "Hookshot Anywhere (MM)"

class ClimbMostSurfacesOoT(Toggle):
    display_name = "Climb Most Surfaces (OoT)"

class ClimbMostSurfacesMM(Toggle):
    display_name = "Climb Most Surfaces (MM)"

class FastBunnyHood(Toggle):
    display_name = "Fast Bunny Hood"

class DefaultHoldTarget(Toggle):
    display_name = "Default Hold Target"

class DisableCritWiggle(Toggle):
    display_name = "Disable CritWiggle"

class RestoreBrokenActors(Toggle):
    display_name = "Restore Broken Actors"

class AlterLostWoodsExits(Toggle):
    display_name = "Alter Lost Woods Exits"

class VoidWarpInMM(Toggle):
    display_name = "Void Warp in MM"


ootmm_main_options: Dict[str, Type[Option]] = {
    "goal": Goal,
    "triforce_goal": TriforceGoal,
    "triforce_pieces": TriforcePieces,
    "item_pool": ItemPool,
    "hint_importance": HintImportance,
    "song_shuffle": SongShuffle,
    "gold_skulltula_tokens_shuffle": GoldSkulltulaTokensShuffle,
    "house_skulltula_tokens_shuffle": HouseSkulltulaTokensShuffle,
    "tingle_maps_shuffle": TingleMapsShuffle,
    "map_compass_shuffle": MapCompassShuffle,
    "small_key_shuffle_oot": SmallKeyShuffleOoT,
    "small_key_shuffle_mm": SmallKeyShuffleMM,
    "hideout_small_key_shuffle": HideoutSmallKeyShuffle,
    "chest_game_small_key_shuffle": ChestGameSmallKeyShuffle,
    "boss_key_shuffle_oot": BossKeyShuffleOoT,
    "boss_key_shuffle_mm": BossKeyShuffleMM,
    "small_key_ring_oot": SmallKeyRingOoT,
    "key_ring_list_oot": KeyRingListOoT,
    "small_key_ring_mm": SmallKeyRingMM,
    "key_ring_list_mm": KeyRingListMM,
    "silver_rupee_shuffle": SilverRupeeShuffle,
    "town_stray_fairy_shuffle": TownStrayFairyShuffle,
    "dungeon_chest_fairy_shuffle": DungeonChestFairyShuffle,
    "dungeon_freestanding_fairy_shuffle": DungeonFreestandingFairyShuffle,
    "dungeon_reward_shuffle": DungeonRewardShuffle,
    "shop_shuffle_oot": ShopShuffleOoT,
    "shop_shuffle_mm": ShopShuffleMM,
    "owl_statue_shuffle": OwlStatueShuffle,
    "scrub_shuffle_oot": ScrubShuffleOoT,
    "scrub_shuffle_mm": ScrubShuffleMM,
    "cow_shuffle_oot": CowShuffleOoT,
    "cow_shuffle_mm": CowShuffleMM,
    "pots_shuffle_oot": PotsShuffleOoT,
    "pots_shuffle_mm": PotsShuffleMM,
    "grass_shuffle_oot": GrassShuffleOoT,
    "grass_shuffle_mm": GrassShuffleMM,
    "freestanding_rupees_shuffle_oot": FreestandingRupeesShuffleOoT,
    "freestanding_rupees_shuffle_mm": FreestandingRupeesShuffleMM,
    "freestanding_hearts_shuffle_oot": FreestandingHeartsShuffleOoT,
    "freestanding_hearts_shuffle_mm": FreestandingHeartsShuffleMM,
    "ocarina_shuffle_oot": OcarinaShuffleOoT,
    "master_sword_shuffle": MasterSwordShuffle,
    "gerudo_card_shuffle": GerudoCardShuffle,
    "merchants_shuffle_mm": MerchantsShuffleMM,
    "fishing_pond_fish_shuffle": FishingPondFishShuffle,
    "diving_game_rupee_shuffle": DivingGameRupeeShuffle,
    "fairy_fountain_fairy_shuffle_oot": FairyFountainFairyShuffleOoT,
    "fairy_fountain_fairy_shuffle_mm": FairyFountainFairyShuffleMM,
    "fairy_spot_shuffle_oot": FairySpotShuffleOoT,
    "weird_pocket_egg_content_shuffle": WeirdPocketEggContentShuffle,
    "oot_shops_prices": OoTShopsPrices,
    "oot_scrubs_prices": OoTScrubsPrices,
    "mm_shops_prices": MMShopsPrices,
    "mm_tingle_prices": MMTinglePrices,
    "ganon_trials": GanonTrials,
    "ganon_trials_list": GanonTrialsList,
    "moon_crash_behavior": MoonCrashBehavior,
    "starting_age": StartingAge,
    "door_of_time": DoorOfTime,
    "age_change_upon_song_of_time": AgeChangeUponSongOfTime,
    "deku_tree": DekuTree,
    "open_dungeons_mm": OpenDungeonsMM,
    "open_dungeon_list_mm": OpenDungeonsMMList,
    "clear_state_dungeons_mm": ClearStateDungeonsMM,
    "kakariko_gate": KakarikoGate,
    "king_zora": KingZora,
    "gerudo_fortress": GerudoFortress,
    "light_arrow_cutscene": LightArrowCutscene,
    "rainbow_bridge": RainbowBridge,
    "boss_warp_pads": BossWarpPads,
    "deku_tree_as_adult": DekuTreeAsAdult,
    "well_as_adult": WellAsAdult,
    "fire_temple_as_child": FireTempleAsChild,
    "open_zora's_domain_shortcut": OpenZorasDomainShortcut,
    "skip_child_zelda": SkipChildZelda,
    "skip_oath_to_order": SkipOathToOrder,
    "free_scarecrow_oot": FreeScarecrowOoT,
    "pre-completed_dungeons": PreCompletedDungeons,
    "open_mask_shop_at_night": OpenMaskShopAtNight,
    "cross-games_mm_song_of_soaring": CrossGamesMMSongOfSoaring,
    "cross-games_oot_warp_songs": CrossGamesOoTWarpSongs,
    "container_appearance_matches_content": ContainerAppearanceMatchesContent,
    "blast_mask_cooldown": BlastMaskCooldown,
    "clock_speed": ClockSpeed,
    "auto-invert_time_mm": AutoInvertTimeMM,
    "camc_for_heart_piecescontainers": CAMCForHeartPiecesContainers,
    "skulltula_camc": SkulltulaCAMC,
    "fierce_deity_anywhere_in_mm": FierceDeityAnywhereInMM,
    "hookshot_anywhere_oot": HookshotAnywhereOoT,
    "hookshot_anywhere_mm": HookshotAnywhereMM,
    "climb_most_surfaces_oot": ClimbMostSurfacesOoT,
    "climb_most_surfaces_mm": ClimbMostSurfacesMM,
    "fast_bunny_hood": FastBunnyHood,
    "default_hold_target": DefaultHoldTarget,
    "disable_crit_wiggle": DisableCritWiggle,
    "restore_broken_actors": RestoreBrokenActors,
    "alter_lost_woods_exits": AlterLostWoodsExits,
    "void_warp_in_mm": VoidWarpInMM,
    # "death_link": DeathLink, 
}

ootmm_options: Dict[str, Type[Option]] = {
    **ootmm_main_options
}