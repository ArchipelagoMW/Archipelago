"""Fill settings module for DK64 randomizer.

This module contains all the settings configuration logic
that was previously in the generate_early method.
"""

from randomizer.Settings import Settings
from randomizer.Enums.Settings import (
    ActivateAllBananaports,
    BananaportRando,
    BLockerSetting,
    CBRequirement,
    CrownEnemyDifficulty,
    DamageAmount,
    DKPortalRando,
    ExtraCutsceneSkips,
    FasterChecksSelected,
    FungiTimeSetting,
    GalleonWaterSetting,
    GlitchesSelected,
    HardBossesSelected,
    HardModeSelected,
    HelmBonuses,
    HelmDoorItem,
    HelmSetting,
    ItemRandoFiller,
    ItemRandoListSelected,
    KasplatRandoSetting,
    KongModels,
    LevelRandomization,
    LogicType,
    MicrohintsEnabled,
    MinigamesListSelected,
    MiscChangesSelected,
    ProgressiveHintItem,
    PuzzleRando,
    RandomPrices,
    RandomStartingRegion,
    RandomRequirement,
    RemovedBarriersSelected,
    ShufflePortLocations,
    SlamRequirement,
    SpoilerHints,
    SwitchsanityGone,
    SwitchsanityKong,
    TricksSelected,
    TroffSetting,
    WinConditionComplex,
    WrinklyHints,
    KroolInBossPool,
)
from randomizer.Enums.Items import Items as DK64RItems
from randomizer.Enums.Types import Types
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Enemies import Enemies
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Switches import Switches
from randomizer.Lists.Switches import SwitchInfo
from archipelago.Options import Goal, SwitchSanity, SelectStartingKong, GalleonWaterLevel
from archipelago.Goals import GOAL_MAPPING, QUANTITY_GOALS, calculate_quantity
from archipelago.Logic import logic_item_name_to_id


def get_default_settings() -> dict:
    """Get the default settings dictionary."""
    return {
        "activate_all_bananaports": ActivateAllBananaports.isles,
        "alter_switch_allocation": True,
        "auto_keys": True,
        "bananaport_placement_rando": ShufflePortLocations.off,
        "bananaport_rando": BananaportRando.off,
        "blocker_0": 1,
        "blocker_1": 2,
        "blocker_2": 3,
        "blocker_3": 4,
        "blocker_4": 5,
        "blocker_5": 6,
        "blocker_6": 7,
        "blocker_7": 8,
        "blocker_selection_behavior": BLockerSetting.normal_random,
        "blocker_text": 60,
        "bosses_selected": [
            Maps.JapesBoss,
            Maps.AztecBoss,
            Maps.FactoryBoss,
            Maps.GalleonBoss,
            Maps.FungiBoss,
            Maps.CavesBoss,
            Maps.CastleBoss,
            Maps.KroolDonkeyPhase,
            Maps.KroolDiddyPhase,
            Maps.KroolLankyPhase,
            Maps.KroolTinyPhase,
            Maps.KroolChunkyPhase,
        ],
        "bonus_barrel_auto_complete": False,
        "boss_location_rando": True,
        "cannons_require_blast": True,
        "cb_medal_behavior_new": CBRequirement.pre_selected,
        "cb_rando_enabled": False,
        "chunky_phase_slam_req": SlamRequirement.green,
        "coin_door_item": HelmDoorItem.opened,
        "coin_door_item_count": 1,
        "coin_rando": False,
        "crown_door_item": HelmDoorItem.opened,
        "crown_door_item_count": 1,
        "crown_enemy_difficulty": CrownEnemyDifficulty.easy,
        "crown_placement_rando": False,
        "damage_amount": DamageAmount.default,
        "decouple_item_rando": False,
        "dim_solved_hints": False,
        "disable_hard_minigames": True,
        "disable_racing_patches": False,
        "disable_tag_barrels": False,
        "dk_portal_location_rando_v2": DKPortalRando.off,
        "dos_door_rando": False,
        "enable_shop_hints": True,
        "enable_tag_anywhere": True,
        "enemies_selected": [],
        "enemy_kill_crown_timer": True,
        "enemy_speed_rando": False,
        "fairy_queen_behavior": RandomRequirement.pre_selected,
        "fast_start_beginning_of_game_dummy": False,
        "fast_warps": True,
        "faster_checks_selected": [
            FasterChecksSelected.factory_toy_monster_fight,
            FasterChecksSelected.factory_piano_game,
            FasterChecksSelected.factory_diddy_rnd,
            FasterChecksSelected.factory_arcade_round_1,
            FasterChecksSelected.factory_car_race,
            FasterChecksSelected.galleon_seal_race,
            FasterChecksSelected.galleon_mech_fish,
            FasterChecksSelected.forest_mill_conveyor,
            FasterChecksSelected.forest_owl_race,
            FasterChecksSelected.forest_rabbit_race,
            FasterChecksSelected.caves_ice_tomato_minigame,
            FasterChecksSelected.castle_minecart,
            FasterChecksSelected.castle_car_race,
            FasterChecksSelected.jetpac,
            FasterChecksSelected.arcade,
        ],
        "filler_items_selected": [ItemRandoFiller.junkitem],
        "free_trade_setting": True,
        "fungi_time": FungiTimeSetting.dusk,
        "generate_spoilerlog": True,
        "hard_bosses_selected": [],
        "hard_mode_selected": [],
        "has_password": False,
        "helm_hurry": False,
        "helm_phase_count": 2,
        "helm_phase_order_rando": True,
        "helm_random": False,
        "helm_room_bonus_count": HelmBonuses.zero,
        "helm_setting": HelmSetting.skip_start,
        "ice_trap_count": 10,
        "ice_traps_damage": False,
        "item_rando_list_0": [],
        "item_rando_list_1": [],
        "item_rando_list_2": [],
        "item_rando_list_3": [],
        "item_rando_list_4": [],
        "item_rando_list_5": [],
        "item_rando_list_6": [
            ItemRandoListSelected.wrinkly,
            ItemRandoListSelected.gauntletbanana,
            ItemRandoListSelected.racebanana,
            ItemRandoListSelected.sniderewards,
            ItemRandoListSelected.arenas,
            ItemRandoListSelected.halfmedal,
            ItemRandoListSelected.enemies,
            ItemRandoListSelected.boulderitem,
            ItemRandoListSelected.shop,
            ItemRandoListSelected.bfi_gift,
            ItemRandoListSelected.banana_checks,
            ItemRandoListSelected.jetpac,
            ItemRandoListSelected.kasplat,
            ItemRandoListSelected.bosses,
            ItemRandoListSelected.endofhelm,
            ItemRandoListSelected.medal_checks,
            ItemRandoListSelected.medal_checks_helm,
            ItemRandoListSelected.arcade,
            ItemRandoListSelected.fairy_checks,
            ItemRandoListSelected.dirt_patches,
            ItemRandoListSelected.clams,
            ItemRandoListSelected.anthillreward,
            ItemRandoListSelected.kong_cages,
            ItemRandoListSelected.crateitem,
            ItemRandoListSelected.trainingbarrels,
        ],
        "item_rando_list_7": [],
        "item_rando_list_8": [],
        "item_rando_list_9": [],
        "item_reward_previews": True,
        "k_rool_vanilla_requirement": False,
        "kasplat_rando_setting": KasplatRandoSetting.off,
        "key_8_helm": True,
        "keys_random": False,
        "kong_model_chunky": KongModels.default,
        "kong_model_diddy": KongModels.default,
        "kong_model_dk": KongModels.default,
        "kong_model_lanky": KongModels.default,
        "kong_model_tiny": KongModels.default,
        "krool_access": False,
        "krool_in_boss_pool": False,
        "krool_key_count": 0,
        "krool_phase_count": 3,
        "krool_phase_order_rando": True,
        "krool_random": False,
        "less_fragile_boulders": True,
        "logic_type": LogicType.glitchless,
        "maximize_helm_blocker": True,
        "medal_cb_req": 40,
        "medal_jetpac_behavior": RandomRequirement.pre_selected,
        "medal_requirement": 9,
        "mermaid_gb_pearls": 1,
        "microhints_enabled": MicrohintsEnabled.all,
        "mirror_mode": False,
        "misc_changes_selected": [
            MiscChangesSelected.auto_dance_skip,
            MiscChangesSelected.fast_boot,
            MiscChangesSelected.calm_caves,
            MiscChangesSelected.animal_buddies_grab_items,
            MiscChangesSelected.reduced_lag,
            MiscChangesSelected.remove_extraneous_cutscenes,
            MiscChangesSelected.hint_textbox_hold,
            MiscChangesSelected.remove_wrinkly_puzzles,
            MiscChangesSelected.fast_picture_taking,
            MiscChangesSelected.hud_hotkey,
            MiscChangesSelected.ammo_swap,
            MiscChangesSelected.homing_balloons,
            MiscChangesSelected.fast_transform_animation,
            MiscChangesSelected.troff_n_scoff_audio_indicator,
            MiscChangesSelected.lowered_aztec_lobby_bonus,
            MiscChangesSelected.quicker_galleon_star,
            MiscChangesSelected.vanilla_bug_fixes,
            MiscChangesSelected.save_k_rool_progress,
            MiscChangesSelected.small_bananas_always_visible,
            MiscChangesSelected.fast_hints,
            MiscChangesSelected.brighten_mad_maze_maul_enemies,
            MiscChangesSelected.raise_fungi_dirt_patch,
            MiscChangesSelected.global_instrument,
            MiscChangesSelected.fast_pause_transitions,
            MiscChangesSelected.cannon_game_better_control,
            MiscChangesSelected.better_fairy_camera,
            MiscChangesSelected.remove_enemy_cabin_timer,
            MiscChangesSelected.remove_galleon_ship_timers,
            MiscChangesSelected.japes_bridge_permanently_extended,
            MiscChangesSelected.move_spring_cabin_rocketbarrel,
        ],
        "more_cutscene_skips": ExtraCutsceneSkips.auto,
        "no_healing": False,
        "no_melons": False,
        "open_lobbies": False,
        "pearl_mermaid_behavior": RandomRequirement.pre_selected,
        "perma_death": False,
        "portal_numbers": True,
        "prog_slam_level_1": SlamRequirement.green,
        "prog_slam_level_2": SlamRequirement.green,
        "prog_slam_level_3": SlamRequirement.green,
        "prog_slam_level_4": SlamRequirement.green,
        "prog_slam_level_5": SlamRequirement.blue,
        "prog_slam_level_6": SlamRequirement.blue,
        "prog_slam_level_7": SlamRequirement.red,
        "prog_slam_level_8": SlamRequirement.red,
        "progressive_hint_count": 1,
        "progressive_hint_item": ProgressiveHintItem.off,
        "puzzle_rando_difficulty": PuzzleRando.medium,
        "race_coin_rando": False,
        "random_crates": False,
        "random_fairies": False,
        "random_patches": False,
        "random_starting_region": False,
        "random_starting_region_new": RandomStartingRegion.off,
        "randomize_enemy_sizes": False,
        "randomize_pickups": False,
        "rareware_gb_fairies": 6,
        "remove_barriers_selected": [],
        "select_keys": False,
        "serious_hints": True,
        "shop_indicator": True,
        "shorten_boss": True,
        "shops_dont_cost": True,
        "shuffle_helm_location": False,
        "shuffle_shops": False,
        "smaller_shops": False,
        "spoiler_hints": SpoilerHints.off,
        "spoiler_include_level_order": False,
        "spoiler_include_woth_count": False,
        "starting_keys_list_selected": [],
        "starting_moves_list_1": [],
        "starting_moves_list_2": [],
        "starting_moves_list_3": [],
        "starting_moves_list_4": [],
        "starting_moves_list_5": [],
        "starting_moves_list_count_1": 0,
        "starting_moves_list_count_2": 0,
        "starting_moves_list_count_3": 0,
        "starting_moves_list_count_4": 0,
        "starting_moves_list_count_5": 0,
        "starting_random": False,
        "tns_location_rando": False,
        "tns_selection_behavior": TroffSetting.normal_random,
        "troff_0": 0,
        "troff_1": 0,
        "troff_2": 0,
        "troff_3": 0,
        "troff_4": 0,
        "troff_5": 0,
        "troff_6": 0,
        "troff_7": 0,
        "troff_text": 150,
        "vanilla_door_rando": False,
        "warp_level_list_selected": [],
        "warp_to_isles": True,
        "win_condition_count": 1,
        "wrinkly_available": True,
        "wrinkly_hints": WrinklyHints.standard,
        "wrinkly_location_rando": False,
    }


def apply_archipelago_settings(settings_dict: dict, options, multiworld) -> None:
    """Apply Archipelago-specific settings modifications."""
    # Core Archipelago settings
    settings_dict["krool_access"] = True
    settings_dict["archipelago"] = True
    settings_dict["starting_kongs_count"] = options.starting_kong_count.value
    settings_dict["open_lobbies"] = options.open_lobbies.value
    if options.krool_in_boss_pool.value:
        settings_dict["krool_in_boss_pool_v2"] = KroolInBossPool.full_shuffle
    else:
        settings_dict["krool_in_boss_pool_v2"] = KroolInBossPool.off
    settings_dict["helm_phase_count"] = options.helm_phase_count.value
    settings_dict["krool_phase_count"] = options.krool_phase_count.value
    settings_dict["level_randomization"] = LevelRandomization.loadingzone if options.loading_zone_rando.value else LevelRandomization.level_order_complex

    # Medal distribution settings
    if options.medal_distribution.value == 0:  # pre_selected
        settings_dict["medal_cb_req"] = options.cbs_required_for_medal.value
    elif options.medal_distribution.value == 4:  # progressive
        settings_dict["medal_cb_req"] = options.cbs_required_for_medal.value

    settings_dict["medal_requirement"] = options.jetpac_requirement.value
    settings_dict["rareware_gb_fairies"] = options.fairies_required_for_bfi.value
    settings_dict["mirror_mode"] = options.mirror_mode.value
    settings_dict["key_8_helm"] = options.helm_key_lock.value
    settings_dict["shuffle_helm_location"] = options.shuffle_helm_level_order.value
    settings_dict["mermaid_gb_pearls"] = options.pearls_required_for_mermaid.value
    settings_dict["cb_medal_behavior_new"] = options.medal_distribution.value
    settings_dict["smaller_shops"] = options.smaller_shops.value and not hasattr(multiworld, "generation_is_fake")
    settings_dict["puzzle_rando_difficulty"] = options.puzzle_rando.value
    if options.enable_cutscenes.value:
        settings_dict["more_cutscene_skips"] = ExtraCutsceneSkips.press
    settings_dict["alt_minecart_mayhem"] = options.alternate_minecart_mayhem.value
    if options.galleon_water_level == GalleonWaterLevel.option_lowered:
        settings_dict["galleon_water"] = GalleonWaterSetting.lowered
    elif options.galleon_water_level == GalleonWaterLevel.option_raised:
        settings_dict["galleon_water"] = GalleonWaterSetting.raised
    else:
        settings_dict["galleon_water"] = GalleonWaterSetting.vanilla
    settings_dict["no_consumable_upgrades"] = options.remove_bait_potions.value


def apply_blocker_settings(settings_dict: dict, options) -> None:
    """Apply level blocker settings."""
    blocker_options = [
        options.level_blockers.value.get("level_1", 0),
        options.level_blockers.value.get("level_2", 0),
        options.level_blockers.value.get("level_3", 0),
        options.level_blockers.value.get("level_4", 0),
        options.level_blockers.value.get("level_5", 0),
        options.level_blockers.value.get("level_6", 0),
        options.level_blockers.value.get("level_7", 0),
        options.level_blockers.value.get("level_8", 64),
    ]

    # Blocker settings - prioritize chaos blockers, then randomization setting
    settings_dict["maximize_helm_blocker"] = options.maximize_level8_blocker.value

    if options.enable_chaos_blockers.value:
        settings_dict["blocker_text"] = options.chaos_ratio.value
        settings_dict["blocker_selection_behavior"] = BLockerSetting.chaos
    elif options.randomize_blocker_required_amounts.value:
        settings_dict["blocker_text"] = options.blocker_max.value
        settings_dict["blocker_selection_behavior"] = BLockerSetting.normal_random
    else:  # randomize_blocker_required_amounts is False and chaos blockers is False
        settings_dict["blocker_text"] = options.blocker_max.value
        settings_dict["blocker_selection_behavior"] = BLockerSetting.pre_selected
        # When using pre-selected, we need to set the blocker values
        for i, blocker in enumerate(blocker_options):
            settings_dict[f"blocker_{i}"] = blocker


def apply_item_randomization_settings(settings_dict: dict, options) -> None:
    """Apply item randomization settings."""
    settings_dict["item_rando_list_selected"] = []

    # Reset item randomization list to ensure it starts empty
    settings_dict["item_rando_list_1"] = []

    # Always enabled item categories
    always_enabled_categories = [
        ItemRandoListSelected.shop,
        ItemRandoListSelected.moves,
        ItemRandoListSelected.banana,
        ItemRandoListSelected.racebanana,
        ItemRandoListSelected.gauntletbanana,
        ItemRandoListSelected.crown,
        ItemRandoListSelected.blueprint,
        ItemRandoListSelected.key,
        ItemRandoListSelected.medal,
        ItemRandoListSelected.nintendocoin,
        ItemRandoListSelected.kong,
        ItemRandoListSelected.fairy,
        ItemRandoListSelected.rainbowcoin,
        ItemRandoListSelected.bean,
        ItemRandoListSelected.pearl,
        ItemRandoListSelected.crateitem,
        ItemRandoListSelected.rarewarecoin,
        ItemRandoListSelected.shockwave,
        ItemRandoListSelected.trainingmoves,
    ]
    settings_dict["item_rando_list_1"].extend(always_enabled_categories)
    settings_dict["decouple_item_rando"] = False

    # Set a default filler list for compatibility with core randomizer
    settings_dict["filler_items_selected"] = [ItemRandoFiller.junkitem]

    # Conditional item categories
    if options.hints_in_item_pool.value:
        settings_dict["item_rando_list_1"].append(ItemRandoListSelected.hint)
    if options.boulders_in_pool.value:
        settings_dict["item_rando_list_1"].append(ItemRandoListSelected.boulderitem)
    if options.dropsanity:
        settings_dict["item_rando_list_1"].append(ItemRandoListSelected.enemies)
    if options.shopowners_in_pool.value:
        settings_dict["item_rando_list_1"].append(ItemRandoListSelected.shopowners)
    if options.half_medals_in_pool.value:
        settings_dict["item_rando_list_1"].append(ItemRandoListSelected.halfmedal)
    if options.snide_turnins_to_pool.value:
        settings_dict["item_rando_list_1"].append(ItemRandoListSelected.blueprintbanana)


def apply_hard_mode_settings(settings_dict: dict, options) -> None:
    """Apply hard mode settings."""
    settings_dict["hard_mode_selected"] = []
    hard_mode_mapping = {
        "hard_enemies": HardModeSelected.hard_enemies,
        "shuffled_jetpac_enemies": HardModeSelected.shuffled_jetpac_enemies,
        "strict_helm_timer": HardModeSelected.strict_helm_timer,
        "donk_in_the_dark_world": HardModeSelected.donk_in_the_dark_world,
        "donk_in_the_sky": HardModeSelected.donk_in_the_sky,
    }

    for hard in options.hard_mode_selected:
        if hard in hard_mode_mapping:
            settings_dict["hard_mode_selected"].append(hard_mode_mapping[hard])


def apply_kong_settings(settings_dict: dict, options) -> None:
    """Apply Kong settings."""
    # Key settings
    settings_dict["krool_key_count"] = options.pregiven_keys.value
    settings_dict["win_condition_spawns_ship"] = 1 if options.require_beating_krool.value else 0

    # Kong mapping
    kong_mapping = {
        SelectStartingKong.option_donkey: Kongs.donkey,
        SelectStartingKong.option_diddy: Kongs.diddy,
        SelectStartingKong.option_lanky: Kongs.lanky,
        SelectStartingKong.option_tiny: Kongs.tiny,
        SelectStartingKong.option_chunky: Kongs.diddy,
        SelectStartingKong.option_any: Kongs.any,
    }

    settings_dict["starting_kong"] = kong_mapping[options.select_starting_kong.value]


def apply_switchsanity_settings(settings_dict: dict, options) -> None:
    """Apply switchsanity settings."""
    settings_dict["switchsanity_enabled"] = options.switchsanity.value != SwitchSanity.option_off

    if options.switchsanity.value == SwitchSanity.option_all:
        # All switches randomized
        switch_settings = {
            "switchsanity_switch_isles_to_kroc_top": SwitchsanityKong.random,
            "switchsanity_switch_isles_helm_lobby": SwitchsanityGone.random,
            "switchsanity_switch_isles_aztec_lobby_back_room": SwitchsanityKong.random,
            "switchsanity_switch_isles_fungi_lobby_fairy": SwitchsanityKong.random,
            "switchsanity_switch_isles_spawn_rocketbarrel": SwitchsanityKong.random,
            "switchsanity_switch_japes_to_hive": SwitchsanityKong.random,
            "switchsanity_switch_japes_to_rambi": SwitchsanityKong.random,
            "switchsanity_switch_japes_to_painting_room": SwitchsanityKong.random,
            "switchsanity_switch_japes_to_cavern": SwitchsanityKong.random,
            "switchsanity_switch_japes_free_kong": SwitchsanityKong.random,
            "switchsanity_switch_aztec_to_kasplat_room": SwitchsanityKong.random,
            "switchsanity_switch_aztec_llama_front": SwitchsanityKong.random,
            "switchsanity_switch_aztec_llama_side": SwitchsanityKong.random,
            "switchsanity_switch_aztec_llama_back": SwitchsanityKong.random,
            "switchsanity_switch_aztec_sand_tunnel": SwitchsanityKong.random,
            "switchsanity_switch_aztec_to_connector_tunnel": SwitchsanityKong.random,
            "switchsanity_switch_aztec_free_lanky": SwitchsanityKong.random,
            "switchsanity_switch_aztec_free_tiny": SwitchsanityKong.random,
            "switchsanity_switch_factory_free_kong": SwitchsanityKong.random,
            "switchsanity_switch_galleon_to_lighthouse_side": SwitchsanityKong.random,
            "switchsanity_switch_galleon_to_shipwreck_side": SwitchsanityKong.random,
            "switchsanity_switch_galleon_to_cannon_game": SwitchsanityKong.random,
            "switchsanity_switch_fungi_yellow_tunnel": SwitchsanityKong.random,
            "switchsanity_switch_fungi_green_tunnel_near": SwitchsanityKong.random,
            "switchsanity_switch_fungi_green_tunnel_far": SwitchsanityKong.random,
        }
        settings_dict.update(switch_settings)
    elif options.switchsanity.value == SwitchSanity.option_helm_access:
        # Helm switchsanity now has to have each of its switches set
        helm_switch_settings = {
            "switchsanity_switch_isles_to_kroc_top": SwitchsanityKong.random,
            "switchsanity_switch_isles_helm_lobby": SwitchsanityGone.random,
            "switchsanity_switch_isles_aztec_lobby_back_room": SwitchsanityKong.tiny,
            "switchsanity_switch_isles_fungi_lobby_fairy": SwitchsanityKong.tiny,
            "switchsanity_switch_isles_spawn_rocketbarrel": SwitchsanityKong.lanky,
            "switchsanity_switch_japes_to_hive": SwitchsanityKong.tiny,
            "switchsanity_switch_japes_to_rambi": SwitchsanityKong.donkey,
            "switchsanity_switch_japes_to_painting_room": SwitchsanityKong.diddy,
            "switchsanity_switch_japes_to_cavern": SwitchsanityKong.diddy,
            "switchsanity_switch_japes_free_kong": SwitchsanityKong.donkey,
            "switchsanity_switch_aztec_to_kasplat_room": SwitchsanityKong.donkey,
            "switchsanity_switch_aztec_llama_front": SwitchsanityKong.donkey,
            "switchsanity_switch_aztec_llama_side": SwitchsanityKong.lanky,
            "switchsanity_switch_aztec_llama_back": SwitchsanityKong.tiny,
            "switchsanity_switch_aztec_sand_tunnel": SwitchsanityKong.donkey,
            "switchsanity_switch_aztec_to_connector_tunnel": SwitchsanityKong.diddy,
            "switchsanity_switch_aztec_free_lanky": SwitchsanityKong.donkey,
            "switchsanity_switch_aztec_free_tiny": SwitchsanityKong.diddy,
            "switchsanity_switch_factory_free_kong": SwitchsanityKong.lanky,
            "switchsanity_switch_galleon_to_lighthouse_side": SwitchsanityKong.donkey,
            "switchsanity_switch_galleon_to_shipwreck_side": SwitchsanityKong.diddy,
            "switchsanity_switch_galleon_to_cannon_game": SwitchsanityKong.chunky,
            "switchsanity_switch_fungi_yellow_tunnel": SwitchsanityKong.lanky,
            "switchsanity_switch_fungi_green_tunnel_near": SwitchsanityKong.tiny,
            "switchsanity_switch_fungi_green_tunnel_far": SwitchsanityKong.chunky,
        }
        settings_dict.update(helm_switch_settings)
    elif options.switchsanity.value == SwitchSanity.option_off:
        settings_dict["switchsanity_enabled"] = False


def apply_logic_and_barriers_settings(settings_dict: dict, options) -> None:
    """Apply logic and barriers configuration."""
    settings_dict["logic_type"] = options.logic_type.value
    settings_dict["remove_barriers_selected"] = []

    # Barrier removal mapping
    barrier_mapping = {
        "japes_coconut_gates": RemovedBarriersSelected.japes_coconut_gates,
        "japes_shellhive_gate": RemovedBarriersSelected.japes_shellhive_gate,
        "aztec_tunnel_door": RemovedBarriersSelected.aztec_tunnel_door,
        "aztec_5dtemple_switches": RemovedBarriersSelected.aztec_5dtemple_switches,
        "aztec_llama_switches": RemovedBarriersSelected.aztec_llama_switches,
        "aztec_tiny_temple_ice": RemovedBarriersSelected.aztec_tiny_temple_ice,
        "factory_testing_gate": RemovedBarriersSelected.factory_testing_gate,
        "factory_production_room": RemovedBarriersSelected.factory_production_room,
        "galleon_lighthouse_gate": RemovedBarriersSelected.galleon_lighthouse_gate,
        "galleon_shipyard_area_gate": RemovedBarriersSelected.galleon_shipyard_area_gate,
        "castle_crypt_doors": RemovedBarriersSelected.castle_crypt_doors,
        "galleon_seasick_ship": RemovedBarriersSelected.galleon_seasick_ship,
        "forest_green_tunnel": RemovedBarriersSelected.forest_green_tunnel,
        "forest_yellow_tunnel": RemovedBarriersSelected.forest_yellow_tunnel,
        "caves_igloo_pads": RemovedBarriersSelected.caves_igloo_pads,
        "caves_ice_walls": RemovedBarriersSelected.caves_ice_walls,
        "galleon_treasure_room": RemovedBarriersSelected.galleon_treasure_room,
        "helm_star_gates": RemovedBarriersSelected.helm_star_gates,
        "helm_punch_gates": RemovedBarriersSelected.helm_punch_gates,
    }

    for barrier in options.remove_barriers_selected:
        if barrier in barrier_mapping:
            settings_dict["remove_barriers_selected"].append(barrier_mapping[barrier])


def apply_glitches_and_tricks_settings(settings_dict: dict, options) -> None:
    """Apply glitches and tricks configuration."""
    # Prevents tricks and glitches from being added twice
    settings_dict["glitches_selected"] = []
    settings_dict["tricks_selected"] = []

    # Tricks mapping
    tricks_mapping = {
        "monkey_maneuvers": TricksSelected.monkey_maneuvers,
        "hard_shooting": TricksSelected.hard_shooting,
        "advanced_grenading": TricksSelected.advanced_grenading,
        "slope_resets": TricksSelected.slope_resets,
    }

    for trick in options.tricks_selected:
        if trick in tricks_mapping:
            settings_dict["tricks_selected"].append(tricks_mapping[trick])

    # Glitches mapping
    glitches_mapping = {
        "moonkicks": GlitchesSelected.moonkicks,
        "phase_swimming": GlitchesSelected.phase_swimming,
        "swim_through_shores": GlitchesSelected.swim_through_shores,
        "troff_n_scoff_skips": GlitchesSelected.troff_n_scoff_skips,
        "moontail": GlitchesSelected.moontail,
    }

    for glitch in options.glitches_selected:
        if glitch in glitches_mapping:
            settings_dict["glitches_selected"].append(glitches_mapping[glitch])


def apply_enemies(settings_dict: dict, options) -> None:
    """Apply Enemy settings."""
    settings_dict["enemies_selected"] = []

    enemy_mapping = {
        "Bat": Enemies.Bat,
        "BeaverBlue": Enemies.BeaverBlue,
        "BeaverGold": Enemies.BeaverGold,
        "Bug": Enemies.Bug,
        "FireballGlasses": Enemies.FireballGlasses,
        "GetOut": Enemies.GetOut,
        "Ghost": Enemies.Ghost,
        "Gimpfish": Enemies.Gimpfish,
        "Kaboom": Enemies.Kaboom,
        "ChunkyKasplat": Enemies.KasplatChunky,
        "DKKasplat": Enemies.KasplatDK,
        "DiddyKasplat": Enemies.KasplatDiddy,
        "LankyKasplat": Enemies.KasplatLanky,
        "TinyKasplat": Enemies.KasplatTiny,
        "GreenKlaptrap": Enemies.KlaptrapGreen,
        "PurpleKlaptrap": Enemies.KlaptrapPurple,
        "RedKlaptrap": Enemies.KlaptrapRed,
        "Klobber": Enemies.Klobber,
        "Klump": Enemies.Klump,
        "Kop": Enemies.Guard,
        "Kosha": Enemies.Kosha,
        "Kremling": Enemies.Kremling,
        "Krossbones": Enemies.Krossbones,
        "GreenDice": Enemies.MrDice0,
        "RedDice": Enemies.MrDice1,
        "MushroomMan": Enemies.MushroomMan,
        "Pufftup": Enemies.Pufftup,
        "RoboKremling": Enemies.RoboKremling,
        "ZingerRobo": Enemies.ZingerRobo,
        "Ruler": Enemies.Ruler,
        "Shuri": Enemies.Shuri,
        "SirDomino": Enemies.SirDomino,
        "SpiderSmall": Enemies.SpiderSmall,
        "ZingerCharger": Enemies.ZingerCharger,
        "ZingerLime": Enemies.ZingerLime,
        "DisableAKop": Enemies.GuardDisableA,
        "DisableZKop": Enemies.GuardDisableZ,
        "DisableTaggingKop": Enemies.GuardTag,
        "GetOutKop": Enemies.GuardGetOut,
    }

    for enemy in options.enemies_selected:
        if enemy in enemy_mapping:
            settings_dict["enemies_selected"].append(enemy_mapping[enemy])


def apply_boss_and_key_settings(settings_dict: dict, options) -> None:
    """Apply boss and key settings."""
    # Starting keys configuration
    settings_dict["starting_keys_list_selected"] = []

    # Hard Boss mapping
    hard_boss_mapping = {
        "fast_mad_jack": HardBossesSelected.fast_mad_jack,
        "alternative_mad_jack_kongs": HardBossesSelected.alternative_mad_jack_kongs,
        "pufftoss_star_rando": HardBossesSelected.pufftoss_star_rando,
        "pufftoss_star_raised": HardBossesSelected.pufftoss_star_raised,
        "kut_out_phase_rando": HardBossesSelected.kut_out_phase_rando,
        "k_rool_toes_rando": HardBossesSelected.k_rool_toes_rando,
        "beta_lanky_phase": HardBossesSelected.beta_lanky_phase,
    }

    for hardboss in options.harder_bosses:
        if hardboss in hard_boss_mapping:
            settings_dict["hard_bosses_selected"].append(hard_boss_mapping[hardboss])

    # Key mapping for starting inventory
    key_mapping = {
        "Key 1": DK64RItems.JungleJapesKey,
        "Key 2": DK64RItems.AngryAztecKey,
        "Key 3": DK64RItems.FranticFactoryKey,
        "Key 4": DK64RItems.GloomyGalleonKey,
        "Key 5": DK64RItems.FungiForestKey,
        "Key 6": DK64RItems.CrystalCavesKey,
        "Key 7": DK64RItems.CreepyCastleKey,
        "Key 8": DK64RItems.HideoutHelmKey,
    }

    for item in options.start_inventory:
        if item in key_mapping:
            settings_dict["starting_keys_list_selected"].append(key_mapping[item])

    if settings_dict["starting_keys_list_selected"]:
        settings_dict["select_keys"] = True


def apply_goal_settings(settings_dict: dict, options, random_obj) -> None:
    """Apply goal and win condition settings."""
    settings_dict["win_condition_item"] = GOAL_MAPPING[options.goal]

    # Krool's Challenge always requires beating K. Rool otherwise wheres the challenge
    if options.goal == Goal.option_krools_challenge:
        settings_dict["win_condition_spawns_ship"] = True
    # The rabbit is too powerful to allow this
    elif options.goal == Goal.option_kill_the_rabbit:
        settings_dict["win_condition_spawns_ship"] = False

    if options.goal in QUANTITY_GOALS.keys():
        goal_name = QUANTITY_GOALS[options.goal]
        settings_dict["win_condition_count"] = calculate_quantity(goal_name, options.goal_quantity.value, random_obj)

    # Treasure hurry settings
    if options.goal == Goal.option_treasure_hurry:
        settings_dict["helm_hurry"] = True
        settings_dict["helmhurry_list_starting_time"] = 60000
        settings_dict["helmhurry_list_golden_banana"] = -60
        settings_dict["helmhurry_list_blueprint"] = -120
        settings_dict["helmhurry_list_company_coins"] = -3600
        settings_dict["helmhurry_list_move"] = 0
        settings_dict["helmhurry_list_banana_medal"] = -300
        settings_dict["helmhurry_list_rainbow_coin"] = 0
        settings_dict["helmhurry_list_boss_key"] = -900
        settings_dict["helmhurry_list_battle_crown"] = -1200
        settings_dict["helmhurry_list_bean"] = -5400
        settings_dict["helmhurry_list_pearl"] = -1800
        settings_dict["helmhurry_list_kongs"] = 0
        settings_dict["helmhurry_list_fairies"] = -600
        settings_dict["helmhurry_list_colored_bananas"] = -2
        settings_dict["helmhurry_list_ice_traps"] = 120


def apply_starting_moves_settings(settings_dict: dict, options) -> None:
    """Apply starting moves settings."""
    from randomizer.Lists import Item as DK64RItem

    settings_dict["starting_moves_list_1"] = []

    for item in options.start_inventory:
        item_obj = DK64RItem.ItemList[logic_item_name_to_id.get(item)]
        if item_obj.type not in [Types.Key, Types.Shop, Types.Shockwave, Types.TrainingBarrel, Types.Climbing, Types.Cranky, Types.Funky, Types.Candy, Types.Snide]:
            # Ensure that the items in the start inventory are only keys, shops, shockwaves, training barrels, climbing items, or shop owners
            raise ValueError(f"Invalid item type for starting inventory: {item}. Starting inventory can only contain keys, shopkeepers, or moves.")
        elif options.shopowners_in_pool.value and item_obj.type in [Types.Cranky, Types.Funky, Types.Candy, Types.Snide]:
            settings_dict["starting_moves_list_1"].append(logic_item_name_to_id.get(item))

    settings_dict["starting_moves_list_count_1"] = len(settings_dict["starting_moves_list_1"])


def apply_hint_settings(settings_dict: dict, options) -> None:
    """Apply hint settings."""
    if options.hint_style == 0:
        settings_dict["wrinkly_hints"] = WrinklyHints.off


def apply_minigame_settings(settings_dict: dict, options, multiworld) -> None:
    """Apply minigame and bonus barrel settings."""
    settings_dict["minigames_list_selected"] = [MinigamesListSelected[minigame] for minigame in options.shuffled_bonus_barrels]
    settings_dict["disable_hard_minigames"] = not options.hard_minigames.value
    settings_dict["bonus_barrel_auto_complete"] = options.auto_complete_bonus_barrels.value and options.goal.value != Goal.option_bonuses
    settings_dict["helm_room_bonus_count"] = HelmBonuses(options.helm_room_bonus_count.value)

    # Map door item type to the key name in helm_door_item_count dict
    door_item_to_key = {
        HelmDoorItem.req_gb: "golden_bananas",
        HelmDoorItem.req_bp: "blueprints",
        HelmDoorItem.req_companycoins: "company_coins",
        HelmDoorItem.req_key: "keys",
        HelmDoorItem.req_medal: "medals",
        HelmDoorItem.req_crown: "crowns",
        HelmDoorItem.req_fairy: "fairies",
        HelmDoorItem.req_rainbowcoin: "rainbow_coins",
        HelmDoorItem.req_bean: "bean",
        HelmDoorItem.req_pearl: "pearls",
    }

    settings_dict["crown_door_item"] = HelmDoorItem(options.crown_door_item.value)
    # Get count from dict based on selected item, default to 1 if not found
    crown_item_key = door_item_to_key.get(settings_dict["crown_door_item"])
    settings_dict["crown_door_item_count"] = options.helm_door_item_count.value.get(crown_item_key, 1) if crown_item_key else 1

    settings_dict["coin_door_item"] = HelmDoorItem(options.coin_door_item.value)
    # Get count from dict based on selected item, default to 1 if not found
    coin_item_key = door_item_to_key.get(settings_dict["coin_door_item"])
    settings_dict["coin_door_item_count"] = options.helm_door_item_count.value.get(coin_item_key, 1) if coin_item_key else 1

    if hasattr(multiworld, "generation_is_fake"):
        if hasattr(multiworld, "re_gen_passthrough"):
            if "Donkey Kong 64" in multiworld.re_gen_passthrough:
                passthrough = multiworld.re_gen_passthrough["Donkey Kong 64"]
                settings_dict["bonus_barrel_auto_complete"] = passthrough["Autocomplete"]
                settings_dict["helm_room_bonus_count"] = HelmBonuses(passthrough["HelmBarrelCount"])


def handle_fake_generation_settings(settings: Settings, multiworld) -> None:
    """Handle settings for fake generation (UT mode)."""
    if hasattr(multiworld, "generation_is_fake"):
        if hasattr(multiworld, "re_gen_passthrough"):
            if "Donkey Kong 64" in multiworld.re_gen_passthrough:
                passthrough = multiworld.re_gen_passthrough["Donkey Kong 64"]
                settings.level_order = passthrough["LevelOrder"]

                # Switch logic lifted out of level shuffle due to static levels for UT
                if settings.alter_switch_allocation:
                    for x in range(8):
                        settings.switch_allocation[x] = passthrough["SlamLevels"][x]

                settings.starting_kong_list = passthrough["StartingKongs"]
                settings.starting_kong = settings.starting_kong_list[0]  # fake a starting kong so that we don't force a different kong
                settings.medal_requirement = passthrough["JetpacReq"]
                settings.rareware_gb_fairies = passthrough["FairyRequirement"]
                settings.BLockerEntryItems = passthrough["BLockerEntryItems"]
                settings.BLockerEntryCount = passthrough["BLockerEntryCount"]
                settings.medal_cb_req = passthrough["MedalCBRequirement"]
                settings.medal_cb_req_level = [settings.medal_cb_req] * 8

                for level, value in enumerate(passthrough["MedalCBRequirementLevel"]):
                    settings.medal_cb_req_level[Levels(level)] = int(value)

                settings.mermaid_gb_pearls = passthrough["MermaidPearls"]
                settings.BossBananas = passthrough["BossBananas"]
                settings.boss_maps = passthrough["BossMaps"]
                settings.boss_kongs = passthrough["BossKongs"]
                settings.lanky_freeing_kong = passthrough["LankyFreeingKong"]
                settings.helm_order = passthrough["HelmOrder"]
                settings.logic_type = LogicType[passthrough["LogicType"]]
                settings.tricks_selected = passthrough["TricksSelected"]
                settings.glitches_selected = passthrough["GlitchesSelected"]
                settings.open_lobbies = passthrough["OpenLobbies"]
                settings.starting_key_list = passthrough["StartingKeyList"]
                settings.galleon_water = GalleonWaterSetting[passthrough["GalleonWater"]]
                settings.galleon_water_internal = GalleonWaterSetting[passthrough["GalleonWater"]]

                # There's multiple sources of truth for helm order.
                settings.helm_donkey = 0 in settings.helm_order
                settings.helm_diddy = 4 in settings.helm_order
                settings.helm_lanky = 3 in settings.helm_order
                settings.helm_tiny = 2 in settings.helm_order
                settings.helm_chunky = 1 in settings.helm_order

                # Switchsanity
                for switch, data in passthrough["SwitchSanity"].items():
                    needed_kong = Kongs[data["kong"]]
                    switch_type = SwitchType[data["type"]]
                    settings.switchsanity_data[Switches[switch]] = SwitchInfo(switch, needed_kong, switch_type, 0, 0, [])

                if passthrough["Shopkeepers"]:
                    settings.shuffled_location_types.append(Types.Cranky)
                    settings.shuffled_location_types.append(Types.Funky)
                    settings.shuffled_location_types.append(Types.Candy)
                    settings.shuffled_location_types.append(Types.Snide)


def fillsettings(options, multiworld, random_obj):
    """Fill and configure all DK64 settings."""
    # Start with default settings
    settings_dict = get_default_settings()

    # Apply all setting categories
    apply_archipelago_settings(settings_dict, options, multiworld)
    apply_blocker_settings(settings_dict, options)
    apply_item_randomization_settings(settings_dict, options)
    apply_hard_mode_settings(settings_dict, options)
    apply_kong_settings(settings_dict, options)
    apply_switchsanity_settings(settings_dict, options)
    apply_logic_and_barriers_settings(settings_dict, options)
    apply_glitches_and_tricks_settings(settings_dict, options)
    apply_boss_and_key_settings(settings_dict, options)
    apply_goal_settings(settings_dict, options, random_obj)
    apply_starting_moves_settings(settings_dict, options)
    apply_hint_settings(settings_dict, options)
    apply_minigame_settings(settings_dict, options, multiworld)
    apply_enemies(settings_dict, options)

    # Handle fake generation keys if needed
    if hasattr(multiworld, "generation_is_fake"):
        # If gen is fake, don't pick random keys to start with, trust the slot data
        settings_dict["krool_key_count"] = 8

    # Create settings object
    settings = Settings(settings_dict, random_obj)

    # Archipelago really wants the number of locations to match the number of items. Keep track of how many locations we've made here
    settings.location_pool_size = 0

    # Handle fake generation additional settings
    handle_fake_generation_settings(settings, multiworld)

    return settings
