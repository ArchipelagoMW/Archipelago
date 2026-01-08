from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SohWorld


def setup_options_from_slot_data(world: "SohWorld") -> None:
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "Ship of Harkinian" in world.multiworld.re_gen_passthrough:
            world.using_ut = True
            world.passthrough = world.multiworld.re_gen_passthrough["Ship of Harkinian"]
            world.options.closed_forest.value = world.passthrough["closed_forest"]
            world.options.kakariko_gate.value = world.passthrough["kakariko_gate"]
            world.options.door_of_time.value = world.passthrough["door_of_time"]
            world.options.zoras_fountain.value = world.passthrough["zoras_fountain"]
            world.options.sleeping_waterfall.value = world.passthrough["sleeping_waterfall"]
            world.options.jabu_jabu.value = world.passthrough["jabu_jabu"]
            world.options.lock_overworld_doors.value = world.passthrough["lock_overworld_doors"]
            world.options.fortress_carpenters.value = world.passthrough["fortress_carpenters"]
            world.options.rainbow_bridge.value = world.passthrough["rainbow_bridge"]
            world.options.rainbow_bridge_greg_modifier.value = world.passthrough["rainbow_bridge_greg_modifier"]
            world.options.rainbow_bridge_stones_required.value = world.passthrough["rainbow_bridge_stones_required"]
            world.options.rainbow_bridge_medallions_required.value = world.passthrough["rainbow_bridge_medallions_required"]
            world.options.rainbow_bridge_dungeon_rewards_required.value = world.passthrough["rainbow_bridge_dungeon_rewards_required"]

            world.options.rainbow_bridge_dungeons_required.value = world.passthrough["rainbow_bridge_dungeons_required"]
            world.options.rainbow_bridge_skull_tokens_required.value = world.passthrough["rainbow_bridge_skull_tokens_required"]
            world.options.skip_ganons_trials.value = world.passthrough["skip_ganons_trials"]
            world.options.triforce_hunt.value = world.passthrough["triforce_hunt"]
            world.options.triforce_hunt_pieces_total.value = world.passthrough["triforce_hunt_pieces_total"]
            # triforce_pieces_required is handled at the end of create_triforce_pieces
            world.options.shuffle_skull_tokens.value = world.passthrough["shuffle_skull_tokens"]
            world.options.skulls_sun_song.value = world.passthrough["skulls_sun_song"]
            world.options.shuffle_master_sword.value = world.passthrough["shuffle_master_sword"]
            world.options.shuffle_childs_wallet.value = world.passthrough["shuffle_childs_wallet"]
            world.options.shuffle_ocarina_buttons.value = world.passthrough["shuffle_ocarina_buttons"]
            world.options.shuffle_swim.value = world.passthrough["shuffle_swim"]
            world.options.shuffle_weird_egg.value = world.passthrough["shuffle_weird_egg"]
            world.options.shuffle_fishing_pole.value = world.passthrough["shuffle_fishing_pole"]
            world.options.shuffle_deku_stick_bag.value = world.passthrough["shuffle_deku_stick_bag"]
            world.options.shuffle_deku_nut_bag.value = world.passthrough["shuffle_deku_nut_bag"]
            world.options.shuffle_freestanding_items.value = world.passthrough["shuffle_freestanding_items"]
            world.options.shuffle_shops.value = world.passthrough["shuffle_shops"]
            world.options.shuffle_shops_item_amount.value = world.passthrough["shuffle_shops_item_amount"]
            # shop_prices and shop_vanilla_items are handled in pre_fill
            world.options.shuffle_fish.value = world.passthrough["shuffle_fish"]
            world.options.shuffle_scrubs.value = world.passthrough["shuffle_scrubs"]
            # scrub_prices is handled in generate_scrub_prices
            world.options.shuffle_beehives.value = world.passthrough["shuffle_beehives"]
            world.options.shuffle_cows.value = world.passthrough["shuffle_cows"]
            world.options.shuffle_pots.value = world.passthrough["shuffle_pots"]
            world.options.shuffle_crates.value = world.passthrough["shuffle_crates"]
            world.options.shuffle_trees.value = world.passthrough["shuffle_trees"]
            world.options.shuffle_merchants.value = world.passthrough["shuffle_merchants"]
            world.options.shuffle_frog_song_rupees.value = world.passthrough["shuffle_frog_song_rupees"]
            world.options.shuffle_adult_trade_items.value = world.passthrough["shuffle_adult_trade_items"]
            world.options.shuffle_boss_souls.value = world.passthrough["shuffle_boss_souls"]
            world.options.shuffle_fountain_fairies.value = world.passthrough["shuffle_fountain_fairies"]
            world.options.shuffle_stone_fairies.value = world.passthrough["shuffle_stone_fairies"]
            world.options.shuffle_bean_fairies.value = world.passthrough["shuffle_bean_fairies"]
            world.options.shuffle_song_fairies.value = world.passthrough["shuffle_song_fairies"]
            world.options.shuffle_grass.value = world.passthrough["shuffle_grass"]
            world.options.shuffle_dungeon_rewards.value = world.passthrough["shuffle_dungeon_rewards"]
            world.options.maps_and_compasses.value = world.passthrough["maps_and_compasses"]
            world.options.ganons_castle_boss_key.value = world.passthrough["ganons_castle_boss_key"]
            world.options.ganons_castle_boss_key_greg_modifier.value = world.passthrough["ganons_castle_boss_key_greg_modifier"]
            world.options.ganons_castle_boss_key_stones_required.value = world.passthrough["ganons_castle_boss_key_stones_required"]
            world.options.ganons_castle_boss_key_medallions_required.value = world.passthrough["ganons_castle_boss_key_medallions_required"]
            world.options.ganons_castle_boss_key_dungeon_rewards_required.value = world.passthrough["ganons_castle_boss_key_dungeon_rewards_required"]
            world.options.ganons_castle_boss_key_dungeons_required.value = world.passthrough["ganons_castle_boss_key_dungeons_required"]
            world.options.ganons_castle_boss_key_skull_tokens_required.value = world.passthrough["ganons_castle_boss_key_skull_tokens_required"]
            world.options.key_rings.value = world.passthrough["key_rings"]
            world.options.big_poe_target_count.value = world.passthrough["big_poe_target_count"]
            world.options.skip_child_zelda.value = world.passthrough["skip_child_zelda"]
            world.options.skip_epona_race.value = world.passthrough["skip_epona_race"]
            world.options.complete_mask_quest.value = world.passthrough["complete_mask_quest"]
            world.options.skip_scarecrows_song.value = world.passthrough["skip_scarecrows_song"]
            world.options.full_wallets.value = world.passthrough["full_wallets"]
            world.options.bombchu_bag.value = world.passthrough["bombchu_bag"]
            world.options.bombchu_drops.value = world.passthrough["bombchu_drops"]
            world.options.blue_fire_arrows.value = world.passthrough["blue_fire_arrows"]
            world.options.sunlight_arrows.value = world.passthrough["sunlight_arrows"]
            world.options.infinite_upgrades.value = world.passthrough["infinite_upgrades"]
            world.options.skeleton_key.value = world.passthrough["skeleton_key"]
            world.options.slingbow_break_beehives.value = world.passthrough["slingbow_break_beehives"]
            world.options.starting_age.value = world.passthrough["starting_age"]
            world.options.true_no_logic = world.passthrough["no_logic"]
            # world.options.tricks_in_logic.value = world.passthrough["tricks_in_logic"]
            # uncomment above and delete this line when tricks in logic is put in
            # the below do not need to be handled in UT at all, since they do not affect logic
            # shuffle_100_gs_reward, ice_trap_count, ice_trap_filler_replacement, and apworld_version
        else:
            world.using_ut = False
    else:
        world.using_ut = False
