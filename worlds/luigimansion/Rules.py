from BaseClasses import MultiWorld
from worlds.generic.Rules import set_rule, add_rule



# def set_rules(world: MultiWorld, player: int):
#     # Outset Island
#     set_rule(world.get_location("Outset Island - Underneath Link's House", player), lambda state: True)
#     set_rule(world.get_location("Outset Island - Mesa the Grasscutter's House", player), lambda state: True)
#     set_rule(
#         world.get_location("Outset Island - Orca - Give 10 Knight's Crests", player),
#         lambda state: state.has("Spoils Bag", player)
#                       and can_farm_knights_crests(state, player)
#                       and can_sword_fight_with_orca(state, player)
#                       and has_magic_meter(state, player),
#     )
#     # set_rule(
#     #     world.get_location("Outset Island - Orca - Hit 500 Times", player),
#     #     lambda state: can_sword_fight_with_orca(state, player),
#     # )
#     set_rule(
#         world.get_location("Outset Island - Great Fairy", player),
#         lambda state: can_access_outset_fairy_fountain(state, player),
#     )
#     set_rule(world.get_location("Outset Island - Jabun's Cave", player), lambda state: state.has("Bombs", player))
#     set_rule(
#         world.get_location("Outset Island - Dig up Black Soil", player),
#         lambda state: state.has("Bait Bag", player)
#                       and can_buy_bait(state, player)
#                       and state.has("Power Bracelets", player),
#     )
#     set_rule(
#         world.get_location("Outset Island - Savage Labyrinth - Floor 30", player),
#         lambda state: can_access_savage_labyrinth(state, player)
#                       and can_defeat_keese(state, player)
#                       and can_defeat_miniblins(state, player)
#                       and can_defeat_red_chuchus(state, player)
#                       and can_defeat_magtails(state, player)
#                       and can_defeat_fire_keese(state, player)
#                       and can_defeat_peahats(state, player)
#                       and can_defeat_green_chuchus(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and can_defeat_mothulas(state, player)
#                       and can_defeat_winged_mothulas(state, player)
#                       and can_defeat_wizzrobes(state, player)
#                       and can_defeat_armos(state, player)
#                       and can_defeat_yellow_chuchus(state, player)
#                       and can_defeat_red_bubbles(state, player)
#                       and can_defeat_darknuts(state, player)
#                       and can_play_winds_requiem(state, player)
#                       and (
#                               state.has("Grappling Hook", player) or has_heros_sword(state, player) or state.has(
#                           "Skull Hammer", player)
#                       ),
#     )
#     set_rule(
#         world.get_location("Outset Island - Savage Labyrinth - Floor 50", player),
#         lambda state: state.can_reach("Outset Island - Savage Labyrinth - Floor 30", "Location", player)
#                       and can_aim_mirror_shield(state, player)
#                       and can_defeat_redeads(state, player)
#                       and can_defeat_blue_bubbles(state, player)
#                       and can_defeat_dark_chuchus(state, player)
#                       and can_defeat_poes(state, player)
#                       and can_defeat_stalfos(state, player)
#                       and state.has("Skull Hammer", player),
#     )
#
#     # Windfall Island
#     set_rule(world.get_location("Windfall Island - Jail - Tingle - First Gift", player), lambda state: True)
#     set_rule(world.get_location("Windfall Island - Jail - Tingle - Second Gift", player), lambda state: True)
#     set_rule(world.get_location("Windfall Island - Jail - Maze Chest", player), lambda state: True)
#     set_rule(
#         world.get_location("Windfall Island - Chu Jelly Juice Shop - Give 15 Green Chu Jelly", player),
#         lambda state: can_farm_green_chu_jelly(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Chu Jelly Juice Shop - Give 15 Blue Chu Jelly", player),
#         lambda state: can_obtain_15_blue_chu_jelly(state, player),
#     )
#     set_rule(world.get_location("Windfall Island - Ivan - Catch Killer Bees", player), lambda state: True)
#     set_rule(world.get_location("Windfall Island - Mrs. Marie - Catch Killer Bees", player), lambda state: True)
#     set_rule(
#         world.get_location("Windfall Island - Mrs. Marie - Give 1 Joy Pendant", player),
#         lambda state: state.has("Spoils Bag", player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Mrs. Marie - Give 21 Joy Pendants", player),
#         lambda state: state.has("Spoils Bag", player) and can_farm_joy_pendants(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Mrs. Marie - Give 40 Joy Pendants", player),
#         lambda state: state.has("Spoils Bag", player) and can_farm_joy_pendants(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Lenzo's House - Left Chest", player),
#         lambda state: can_play_winds_requiem(state, player) and has_picto_box(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Lenzo's House - Right Chest", player),
#         lambda state: can_play_winds_requiem(state, player) and has_picto_box(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Lenzo's House - Become Lenzo's Assistant", player),
#         lambda state: has_picto_box(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Lenzo's House - Bring Forest Firefly", player),
#         lambda state: has_picto_box(state, player)
#                       and state.has("Empty Bottle", player)
#                       and can_access_forest_haven(state, player),
#     )
#     set_rule(world.get_location("Windfall Island - House of Wealth Chest", player), lambda state: True)
#     set_rule(
#         world.get_location("Windfall Island - Maggie's Father - Give 20 Skull Necklaces", player),
#         lambda state: rescued_aryll(state, player)
#                       and state.has("Spoils Bag", player)
#                       and can_farm_skull_necklaces(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Maggie - Free Item", player), lambda state: rescued_aryll(state, player)
#     )
#     set_rule(
#         world.get_location("Windfall Island - Maggie - Delivery Reward", player),
#         lambda state: rescued_aryll(state, player)
#                       and state.has("Delivery Bag", player)
#                       and state.has("Moblin's Letter", player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Cafe Bar - Postman", player),
#         lambda state: rescued_aryll(state, player)
#                       and state.has("Delivery Bag", player)
#                       and state.has("Maggie's Letter", player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Kreeb - Light Up Lighthouse", player),
#         lambda state: can_play_winds_requiem(state, player) and has_fire_arrows(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Transparent Chest", player),
#         lambda state: can_play_winds_requiem(state, player)
#                       and has_fire_arrows(state, player)
#                       and (can_fly_with_deku_leaf_outdoors(state, player) or state.has("Hookshot", player)),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Tott - Teach Rhythm", player),
#         lambda state: state.has("Wind Waker", player),
#     )
#     set_rule(world.get_location("Windfall Island - Pirate Ship", player), lambda state: True)
#     set_rule(world.get_location("Windfall Island - 5 Rupee Auction", player), lambda state: True)
#     set_rule(world.get_location("Windfall Island - 40 Rupee Auction", player), lambda state: True)
#     set_rule(world.get_location("Windfall Island - 60 Rupee Auction", player), lambda state: True)
#     set_rule(world.get_location("Windfall Island - 80 Rupee Auction", player), lambda state: True)
#     set_rule(
#         world.get_location("Windfall Island - Zunari - Stock Exotic Flower in Zunari's Shop", player),
#         lambda state: rescued_aryll(state, player) and state.has("Delivery Bag", player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Sam - Decorate the Town", player),
#         lambda state: rescued_aryll(state, player) and state.has("Delivery Bag", player),
#     )
#     # set_rule(
#     #     world.get_location("Windfall Island - Kane - Place Shop Guru Statue on Gate", player),
#     #     lambda state: rescued_aryll(state, player) and state.has("Delivery Bag", player),
#     # )
#     # set_rule(
#     #     world.get_location("Windfall Island - Kane - Place Postman Statue on Gate", player),
#     #     lambda state: rescued_aryll(state, player) and state.has("Delivery Bag", player),
#     # )
#     # set_rule(
#     #     world.get_location("Windfall Island - Kane - Place Six Flags on Gate", player),
#     #     lambda state: rescued_aryll(state, player) and state.has("Delivery Bag", player),
#     # )
#     # set_rule(
#     #     world.get_location("Windfall Island - Kane - Place Six Idols on Gate", player),
#     #     lambda state: rescued_aryll(state, player) and state.has("Delivery Bag", player),
#     # )
#     set_rule(
#         world.get_location("Windfall Island - Mila - Follow the Thief", player),
#         lambda state: rescued_aryll(state, player),
#     )
#     set_rule(world.get_location("Windfall Island - Battlesquid - First Prize", player), lambda state: True)
#     set_rule(world.get_location("Windfall Island - Battlesquid - Second Prize", player), lambda state: True)
#     set_rule(world.get_location("Windfall Island - Battlesquid - Under 20 Shots Prize", player), lambda state: True)
#     set_rule(
#         world.get_location("Windfall Island - Pompie and Vera - Secret Meeting Photo", player),
#         lambda state: can_play_winds_requiem(state, player) and has_picto_box(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Kamo - Full Moon Photo", player),
#         lambda state: has_deluxe_picto_box(state, player) and can_play_song_of_passing(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Minenco - Miss Windfall Photo", player),
#         lambda state: has_deluxe_picto_box(state, player),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Linda and Anton", player),
#         lambda state: has_deluxe_picto_box(state, player) and can_play_song_of_passing(state, player),
#     )
#
#     # Dragon Roost Island
#     set_rule(
#         world.get_location("Dragon Roost Island - Wind Shrine", player), lambda state: state.has("Wind Waker", player)
#     )
#     set_rule(
#         world.get_location("Dragon Roost Island - Rito Aerie - Give Hoskit 20 Golden Feathers", player),
#         lambda state: state.has("Spoils Bag", player) and can_farm_golden_feathers(state, player),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Island - Chest on Top of Boulder", player),
#         lambda state: has_heros_bow(state, player)
#                       or (state.has("Bait Bag", player) and can_buy_hyoi_pears(state, player))
#                       or state.has("Boomerang", player)
#                       or state.has("Bombs", player),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Island - Fly Across Platforms Around Island", player),
#         lambda state: can_fly_with_deku_leaf_outdoors(state, player)
#                       and (can_cut_grass(state, player) or has_magic_meter_upgrade(state, player)),
#     )
#     set_rule(world.get_location("Dragon Roost Island - Rito Aerie - Mail Sorting", player), lambda state: True)
#     set_rule(
#         world.get_location("Dragon Roost Island - Secret Cave", player),
#         lambda state: can_access_dragon_roost_island_secret_cave(state, player)
#                       and can_defeat_keese(state, player)
#                       and can_defeat_red_chuchus(state, player),
#     )
#
#     # Dragon Roost Cavern
#     set_rule(
#         world.get_location("Dragon Roost Cavern - First Room", player),
#         lambda state: can_access_dragon_roost_cavern(state, player),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Alcove With Water Jugs", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 1),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Water Jug on Upper Shelf", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 1),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Boarded Up Chest", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 1),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Chest Across Lava Pit", player),
#         lambda state: can_access_dragon_roost_cavern(state, player)
#                       and state.has("DRC Small Key", player, 2)
#                       and (
#                               state.has("Grappling Hook", player)
#                               or can_fly_with_deku_leaf_indoors(state, player)
#                               or (state.has("Hookshot", player) and state._tww_obscure_1(player))
#                       ),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Rat Room", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 2),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Rat Room Boarded Up Chest", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 2),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Bird's Nest", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 3),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Dark Room", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 4),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Tingle Chest in Hub Room", player),
#         lambda state: can_access_dragon_roost_cavern(state, player)
#                       and state.has("DRC Small Key", player, 4)
#                       and has_tingle_bombs(state, player),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Pot on Upper Shelf in Pot Room", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 4),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Pot Room Chest", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 4),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Miniboss", player),
#         lambda state: can_access_dragon_roost_cavern(state, player) and state.has("DRC Small Key", player, 4),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Under Rope Bridge", player),
#         lambda state: can_access_dragon_roost_cavern(state, player)
#                       and state.has("DRC Small Key", player, 4)
#                       and (state.has("Grappling Hook", player) or can_fly_with_deku_leaf_outdoors(state, player)),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Tingle Statue Chest", player),
#         lambda state: can_reach_dragon_roost_cavern_gaping_maw(state, player)
#                       and state.has("Grappling Hook", player)
#                       and has_tingle_bombs(state, player),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Big Key Chest", player),
#         lambda state: can_reach_dragon_roost_cavern_gaping_maw(state, player)
#                       and state.has("Grappling Hook", player)
#                       and can_stun_magtails(state, player),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Boss Stairs Right Chest", player),
#         lambda state: can_reach_dragon_roost_cavern_boss_stairs(state, player),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Boss Stairs Left Chest", player),
#         lambda state: can_reach_dragon_roost_cavern_boss_stairs(state, player),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Boss Stairs Right Pot", player),
#         lambda state: can_reach_dragon_roost_cavern_boss_stairs(state, player),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Cavern - Gohma Heart Container", player),
#         lambda state: can_access_gohma_boss_arena(state, player) and can_defeat_gohma(state, player),
#     )
#
#     # Forest Haven
#     set_rule(
#         world.get_location("Forest Haven - On Tree Branch", player),
#         lambda state: can_access_forest_haven(state, player)
#                       and (
#                               state.has("Grappling Hook", player)
#                               or (
#                                       can_fly_with_deku_leaf_indoors(state, player)
#                                       and can_fly_with_deku_leaf_outdoors(state, player)
#                                       and state._tww_obscure_1(player)
#                                       and (
#                                               (can_cut_grass(state, player) and state._tww_precise_1(player))
#                                               or (has_magic_meter_upgrade(state, player) and state._tww_precise_2(
#                                           player))
#                                       )
#                               )
#                       ),
#     )
#     set_rule(
#         world.get_location("Forest Haven - Small Island Chest", player),
#         lambda state: can_access_forest_haven(state, player)
#                       and (
#                               state.has("Grappling Hook", player)
#                               or (
#                                       can_fly_with_deku_leaf_indoors(state, player)
#                                       and can_fly_with_deku_leaf_outdoors(state, player)
#                                       and state._tww_obscure_1(player)
#                                       and (
#                                               (can_cut_grass(state, player) and state._tww_precise_1(player))
#                                               or (has_magic_meter_upgrade(state, player) and state._tww_precise_2(
#                                           player))
#                                       )
#                               )
#                       )
#                       and can_fly_with_deku_leaf_outdoors(state, player)
#                       and (can_cut_grass(state, player) or has_magic_meter_upgrade(state, player)),
#     )
#
#     # Forbidden Woods
#     set_rule(
#         world.get_location("Forbidden Woods - First Room", player),
#         lambda state: can_access_forbidden_woods(state, player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Inside Hollow Tree's Mouth", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and (can_defeat_door_flowers(state, player) or can_defeat_boko_babas(state, player)),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Climb to Top Using Boko Baba Bulbs", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_door_flowers(state, player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Pot High Above Hollow Tree", player),
#         lambda state: can_access_forbidden_woods(state, player) and can_fly_with_deku_leaf_indoors(state, player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Hole in Tree", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Morth Pit", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and state.has("Grappling Hook", player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Vine Maze Left Chest", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and state.has("Grappling Hook", player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Vine Maze Right Chest", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and state.has("Grappling Hook", player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Highest Pot in Vine Maze", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and state.has("Grappling Hook", player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Tall Room Before Miniboss", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and state.has("Grappling Hook", player)
#                       and state.has("FW Small Key", player, 1)
#                       and (can_defeat_peahats(state, player) or state._tww_precise_2(player)),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Mothula Miniboss Room", player),
#         lambda state: can_access_forbidden_woods_miniboss_arena(state, player)
#                       and can_defeat_winged_mothulas(state, player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Past Seeds Hanging by Vines", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and state.has("Grappling Hook", player)
#                       and state.has("FW Small Key", player, 1)
#                       and can_defeat_door_flowers(state, player)
#                       and (can_destroy_seeds_hanging_by_vines(state, player) or state._tww_precise_1(player)),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Chest Across Red Hanging Flower", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and state.has("Grappling Hook", player)
#                       and state.has("Boomerang", player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Tingle Statue Chest", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and state.has("Grappling Hook", player)
#                       and state.has("Boomerang", player)
#                       and (has_tingle_bombs(state, player) or can_activate_tingle_bomb_triggers_without_tingle_tuner(
#             state, player)),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Chest in Locked Tree Trunk", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and state.has("Grappling Hook", player)
#                       and state.has("Boomerang", player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Big Key Chest", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and state.has("Grappling Hook", player)
#                       and state.has("Boomerang", player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Double Mothula Room", player),
#         lambda state: can_access_forbidden_woods(state, player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and can_defeat_boko_babas(state, player)
#                       and (can_defeat_door_flowers(state, player) or state.has("Grappling Hook", player))
#                       and can_defeat_mothulas(state, player),
#     )
#     set_rule(
#         world.get_location("Forbidden Woods - Kalle Demos Heart Container", player),
#         lambda state: can_access_kalle_demos_boss_arena(state, player) and can_defeat_kalle_demos(state, player),
#     )
#
#     # Greatfish Isle
#     set_rule(
#         world.get_location("Greatfish Isle - Hidden Chest", player),
#         lambda state: can_fly_with_deku_leaf_outdoors(state, player),
#     )
#
#     # Tower of the Gods
#     set_rule(
#         world.get_location("Tower of the Gods - Chest Behind Bombable Walls", player),
#         lambda state: can_access_tower_of_the_gods(state, player) and state.has("Bombs", player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Pot Behind Bombable Walls", player),
#         lambda state: can_access_tower_of_the_gods(state, player) and state.has("Bombs", player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Hop Across Floating Boxes", player),
#         lambda state: can_access_tower_of_the_gods(state, player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Light Two Torches", player),
#         lambda state: can_access_tower_of_the_gods(state, player) and state.has("Bombs", player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Skulls Room Chest", player),
#         lambda state: can_access_tower_of_the_gods(state, player) and state.has("Bombs", player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Shoot Eye Above Skulls Room Chest", player),
#         lambda state: can_access_tower_of_the_gods(state, player)
#                       and state.has("Bombs", player)
#                       and has_heros_bow(state, player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Tingle Statue Chest", player),
#         lambda state: can_reach_tower_of_the_gods_second_floor(state, player) and has_tingle_bombs(state, player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - First Chest Guarded by Armos Knights", player),
#         lambda state: can_reach_tower_of_the_gods_second_floor(state, player) and has_heros_bow(state, player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Stone Tablet", player),
#         lambda state: can_reach_tower_of_the_gods_second_floor(state, player)
#                       and (
#                               can_bring_east_servant_of_the_tower(state, player)
#                               or can_bring_west_servant_of_the_tower(state, player)
#                               or can_bring_north_servant_of_the_tower(state, player)
#                       )
#                       and state.has("Wind Waker", player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Darknut Miniboss Room", player),
#         lambda state: can_access_tower_of_the_gods_miniboss_arena(state, player) and can_defeat_darknuts(state, player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Second Chest Guarded by Armos Knights", player),
#         lambda state: can_reach_tower_of_the_gods_second_floor(state, player)
#                       and state.has("Bombs", player)
#                       and can_play_winds_requiem(state, player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Floating Platforms Room", player),
#         lambda state: can_reach_tower_of_the_gods_second_floor(state, player)
#                       and (
#                               has_heros_bow(state, player)
#                               or (can_fly_with_deku_leaf_indoors(state, player) and state._tww_precise_1(player))
#                               or (state.has("Hookshot", player) and state._tww_obscure_1(player))
#                       ),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Top of Floating Platforms Room", player),
#         lambda state: can_reach_tower_of_the_gods_second_floor(state, player) and has_heros_bow(state, player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Eastern Pot in Big Key Chest Room", player),
#         lambda state: can_reach_tower_of_the_gods_third_floor(state, player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Big Key Chest", player),
#         lambda state: can_reach_tower_of_the_gods_third_floor(state, player),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods - Gohdan Heart Container", player),
#         lambda state: can_access_gohdan_boss_arena(state, player) and can_defeat_gohdan(state, player),
#     )
#
#     # Hyrule
#     set_rule(
#         world.get_location("Hyrule - Master Sword Chamber", player),
#         lambda state: can_access_master_sword_chamber(state, player) and can_defeat_mighty_darknuts(state, player),
#     )
#
#     # Forsaken Fortress
#     set_rule(
#         world.get_location("Forsaken Fortress - Phantom Ganon", player),
#         lambda state: can_reach_and_defeat_phantom_ganon(state, player),
#     )
#     set_rule(
#         world.get_location("Forsaken Fortress - Chest Outside Upper Jail Cell", player),
#         lambda state: can_get_inside_forsaken_fortress(state, player)
#                       and (
#                               can_fly_with_deku_leaf_indoors(state, player)
#                               or state.has("Hookshot", player)
#                               or state._tww_obscure_1(player)
#                       ),
#     )
#     set_rule(
#         world.get_location("Forsaken Fortress - Chest Inside Lower Jail Cell", player),
#         lambda state: can_get_inside_forsaken_fortress(state, player),
#     )
#     set_rule(
#         world.get_location("Forsaken Fortress - Chest Guarded By Bokoblin", player),
#         lambda state: can_get_inside_forsaken_fortress(state, player),
#     )
#     set_rule(
#         world.get_location("Forsaken Fortress - Chest on Bed", player),
#         lambda state: can_get_inside_forsaken_fortress(state, player),
#     )
#     set_rule(
#         world.get_location("Forsaken Fortress - Helmaroc King Heart Container", player),
#         lambda state: can_access_helmaroc_king_boss_arena(state, player) and can_defeat_helmaroc_king(state, player),
#     )
#
#     # Mother and Child Isles
#     set_rule(
#         world.get_location("Mother and Child Isles - Inside Mother Isle", player),
#         lambda state: can_play_ballad_of_gales(state, player),
#     )
#
#     # Fire Mountain
#     set_rule(
#         world.get_location("Fire Mountain - Cave - Chest", player),
#         lambda state: can_access_fire_mountain_secret_cave(state, player) and can_defeat_magtails(state, player),
#     )
#     set_rule(world.get_location("Fire Mountain - Lookout Platform Chest", player), lambda state: True)
#     set_rule(
#         world.get_location("Fire Mountain - Lookout Platform - Destroy the Cannons", player),
#         lambda state: can_destroy_cannons(state, player),
#     )
#     set_rule(
#         world.get_location("Fire Mountain - Big Octo", player),
#         lambda state: can_defeat_big_octos(state, player) and state.has("Grappling Hook", player),
#     )
#
#     # Ice Ring Isle
#     set_rule(world.get_location("Ice Ring Isle - Frozen Chest", player), lambda state: has_fire_arrows(state, player))
#     set_rule(
#         world.get_location("Ice Ring Isle - Cave - Chest", player),
#         lambda state: can_access_ice_ring_isle_secret_cave(state, player),
#     )
#     set_rule(
#         world.get_location("Ice Ring Isle - Inner Cave - Chest", player),
#         lambda state: can_access_ice_ring_isle_inner_cave(state, player) and has_fire_arrows(state, player),
#     )
#
#     # Headstone Island
#     set_rule(
#         world.get_location("Headstone Island - Top of the Island", player),
#         lambda state: state.has("Bait Bag", player) and can_buy_hyoi_pears(state, player),
#     )
#     set_rule(
#         world.get_location("Headstone Island - Submarine", player), lambda state: can_defeat_bombchus(state, player)
#     )
#
#     # Earth Temple
#     set_rule(
#         world.get_location("Earth Temple - Transparent Chest In Warp Pot Room", player),
#         lambda state: can_access_earth_temple(state, player) and can_play_command_melody(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Behind Curtain In Warp Pot Room", player),
#         lambda state: can_access_earth_temple(state, player)
#                       and can_play_command_melody(state, player)
#                       and has_fire_arrows(state, player)
#                       and (state.has("Boomerang", player) or state.has("Hookshot", player)),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Transparent Chest in First Crypt", player),
#         lambda state: can_reach_earth_temple_right_path(state, player)
#                       and state.has("Power Bracelets", player)
#                       and (can_play_command_melody(state, player) or has_mirror_shield(state, player)),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Chest Behind Destructible Walls", player),
#         lambda state: can_reach_earth_temple_right_path(state, player) and has_mirror_shield(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Chest In Three Blocks Room", player),
#         lambda state: can_reach_earth_temple_left_path(state, player)
#                       and has_fire_arrows(state, player)
#                       and state.has("Power Bracelets", player)
#                       and can_defeat_floormasters(state, player)
#                       and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player)),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Chest Behind Statues", player),
#         lambda state: can_reach_earth_temple_moblins_and_poes_room(state, player)
#                       and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player)),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Casket in Second Crypt", player),
#         lambda state: can_reach_earth_temple_moblins_and_poes_room(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Stalfos Miniboss Room", player),
#         lambda state: can_access_earth_temple_miniboss_arena(state, player)
#                       and (can_defeat_stalfos(state, player) or state.has("Hookshot", player)),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Tingle Statue Chest", player),
#         lambda state: can_reach_earth_temple_basement(state, player) and has_tingle_bombs(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - End of Foggy Room With Floormasters", player),
#         lambda state: can_reach_earth_temple_redead_hub_room(state, player)
#                       and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player)),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Kill All Floormasters in Foggy Room", player),
#         lambda state: can_reach_earth_temple_redead_hub_room(state, player)
#                       and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player))
#                       and can_defeat_floormasters(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Behind Curtain Next to Hammer Button", player),
#         lambda state: can_reach_earth_temple_redead_hub_room(state, player)
#                       and (can_play_command_melody(state, player) or can_aim_mirror_shield(state, player))
#                       and has_fire_arrows(state, player)
#                       and (state.has("Boomerang", player) or state.has("Hookshot", player)),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Chest in Third Crypt", player),
#         lambda state: can_reach_earth_temple_third_crypt(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Many Mirrors Room Right Chest", player),
#         lambda state: can_reach_earth_temple_many_mirrors_room(state, player)
#                       and can_play_command_melody(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Many Mirrors Room Left Chest", player),
#         lambda state: can_reach_earth_temple_many_mirrors_room(state, player)
#                       and state.has("Power Bracelets", player)
#                       and can_play_command_melody(state, player)
#                       and can_aim_mirror_shield(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Stalfos Crypt Room", player),
#         lambda state: can_reach_earth_temple_many_mirrors_room(state, player) and can_defeat_stalfos(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Big Key Chest", player),
#         lambda state: can_reach_earth_temple_many_mirrors_room(state, player)
#                       and state.has("Power Bracelets", player)
#                       and can_play_command_melody(state, player)
#                       and can_aim_mirror_shield(state, player)
#                       and (
#                               can_defeat_blue_bubbles(state, player)
#                               or (has_heros_bow(state, player) and state._tww_obscure_1(player))
#                               or (
#                                       (
#                                               has_heros_sword(state, player)
#                                               or has_any_master_sword(state, player)
#                                               or state.has("Skull Hammer", player)
#                                       )
#                                       and state._tww_obscure_1(player)
#                                       and state._tww_precise_1(player)
#                               )
#                       )
#                       and can_defeat_darknuts(state, player),
#     )
#     set_rule(
#         world.get_location("Earth Temple - Jalhalla Heart Container", player),
#         lambda state: can_access_jalhalla_boss_arena(state, player) and can_defeat_jalhalla(state, player),
#     )
#
#     # Wind Temple
#     set_rule(
#         world.get_location("Wind Temple - Chest Between Two Dirt Patches", player),
#         lambda state: can_access_wind_temple(state, player) and can_play_command_melody(state, player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Behind Stone Head in Hidden Upper Room", player),
#         lambda state: can_access_wind_temple(state, player)
#                       and can_play_command_melody(state, player)
#                       and state.has("Iron Boots", player)
#                       and can_fly_with_deku_leaf_indoors(state, player)
#                       and state.has("Hookshot", player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Tingle Statue Chest", player),
#         lambda state: can_reach_wind_temple_kidnapping_room(state, player) and has_tingle_bombs(state, player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Chest Behind Stone Head", player),
#         lambda state: can_reach_wind_temple_kidnapping_room(state, player)
#                       and state.has("Iron Boots", player)
#                       and state.has("Hookshot", player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Chest in Left Alcove", player),
#         lambda state: can_reach_wind_temple_kidnapping_room(state, player)
#                       and state.has("Iron Boots", player)
#                       and can_fan_with_deku_leaf(state, player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Big Key Chest", player),
#         lambda state: can_reach_wind_temple_kidnapping_room(state, player)
#                       and state.has("Iron Boots", player)
#                       and can_fan_with_deku_leaf(state, player)
#                       and can_play_wind_gods_aria(state, player)
#                       and can_defeat_darknuts(state, player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Chest In Many Cyclones Room", player),
#         lambda state: can_reach_wind_temple_kidnapping_room(state, player)
#                       and (
#                               (
#                                       state.has("Iron Boots", player)
#                                       and can_fan_with_deku_leaf(state, player)
#                                       and can_fly_with_deku_leaf_indoors(state, player)
#                                       and (can_cut_grass(state, player) or has_magic_meter_upgrade(state, player))
#                               )
#                               or (
#                                       state.has("Hookshot", player)
#                                       and can_defeat_blue_bubbles(state, player)
#                                       and can_fly_with_deku_leaf_indoors(state, player)
#                               )
#                               or (
#                                       state.has("Hookshot", player)
#                                       and can_fly_with_deku_leaf_indoors(state, player)
#                                       and state._tww_obscure_1(player)
#                                       and state._tww_precise_2(player)
#                               )
#                       ),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Behind Stone Head in Many Cyclones Room", player),
#         lambda state: can_reach_end_of_wind_temple_many_cyclones_room(state, player) and state.has("Hookshot", player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Chest In Middle Of Hub Room", player),
#         lambda state: can_open_wind_temple_upper_giant_grate(state, player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Spike Wall Room - First Chest", player),
#         lambda state: can_open_wind_temple_upper_giant_grate(state, player) and state.has("Iron Boots", player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Spike Wall Room - Destroy All Cracked Floors", player),
#         lambda state: can_open_wind_temple_upper_giant_grate(state, player) and state.has("Iron Boots", player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Wizzrobe Miniboss Room", player),
#         lambda state: can_access_wind_temple_miniboss_arena(state, player)
#                       and can_defeat_darknuts(state, player)
#                       and can_remove_peahat_armor(state, player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Chest at Top of Hub Room", player),
#         lambda state: can_activate_wind_temple_giant_fan(state, player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Chest Behind Seven Armos", player),
#         lambda state: can_activate_wind_temple_giant_fan(state, player) and can_defeat_armos(state, player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Kill All Enemies in Tall Basement Room", player),
#         lambda state: can_reach_wind_temple_tall_basement_room(state, player)
#                       and can_defeat_stalfos(state, player)
#                       and can_defeat_wizzrobes(state, player)
#                       and can_defeat_morths(state, player),
#     )
#     set_rule(
#         world.get_location("Wind Temple - Molgera Heart Container", player),
#         lambda state: can_access_molgera_boss_arena(state, player) and can_defeat_molgera(state, player),
#     )
#
#     # Ganon's Tower
#     set_rule(
#         world.get_location("Ganon's Tower - Maze Chest", player),
#         lambda state: can_reach_ganons_tower_phantom_ganon_room(state, player)
#                       and can_defeat_phantom_ganon(state, player),
#     )
#
#     # Mailbox
#     set_rule(
#         world.get_location("Mailbox - Letter from Hoskit's Girlfriend", player),
#         lambda state: state.has("Spoils Bag", player)
#                       and can_farm_golden_feathers(state, player)
#                       and can_play_song_of_passing(state, player),
#     )
#     set_rule(
#         world.get_location("Mailbox - Letter from Baito's Mother", player),
#         lambda state: state.has("Delivery Bag", player)
#                       and state.has("Note to Mom", player)
#                       and can_play_song_of_passing(state, player),
#     )
#     set_rule(
#         world.get_location("Mailbox - Letter from Baito", player),
#         lambda state: state.has("Delivery Bag", player)
#                       and state.has("Note to Mom", player)
#                       and state.can_reach("Earth Temple - Jalhalla Heart Container", "Location", player),
#     )
#     set_rule(
#         world.get_location("Mailbox - Letter from Komali's Father", player),
#         lambda state: state.has("Farore's Pearl", player),
#     )
#     set_rule(
#         world.get_location("Mailbox - Letter Advertising Bombs in Beedle's Shop", player),
#         lambda state: state.has("Bombs", player),
#     )
#     set_rule(
#         world.get_location("Mailbox - Letter Advertising Rock Spire Shop Ship", player),
#         lambda state: has_any_wallet_upgrade(state, player),
#     )
#     # set_rule(
#     #     world.get_location("Mailbox - Beedle's Silver Membership Reward", player),
#     #     lambda state: (
#     #         state.has("Bait Bag", player)
#     #         or state.has("Bombs", player)
#     #         or has_heros_bow(state, player)
#     #         or state.has("Empty Bottle", player)
#     #     )
#     #     and can_play_song_of_passing(state, player),
#     # )
#     # set_rule(
#     #     world.get_location("Mailbox - Beedle's Gold Membership Reward", player),
#     #     lambda state: (
#     #         state.has("Bait Bag", player)
#     #         or state.has("Bombs", player)
#     #         or has_heros_bow(state, player)
#     #         or state.has("Empty Bottle", player)
#     #     )
#     #     and can_play_song_of_passing(state, player),
#     # )
#     set_rule(
#         world.get_location("Mailbox - Letter from Orca", player),
#         lambda state: state.can_reach("Forbidden Woods - Kalle Demos Heart Container", "Location", player),
#     )
#     set_rule(
#         world.get_location("Mailbox - Letter from Grandma", player),
#         lambda state: state.has("Empty Bottle", player)
#                       and can_get_fairies(state, player)
#                       and can_play_song_of_passing(state, player),
#     )
#     set_rule(
#         world.get_location("Mailbox - Letter from Aryll", player),
#         lambda state: state.can_reach("Forsaken Fortress - Helmaroc King Heart Container", "Location", player)
#                       and can_play_song_of_passing(state, player),
#     )
#     set_rule(
#         world.get_location("Mailbox - Letter from Tingle", player),
#         lambda state: rescued_tingle(state, player)
#                       and has_any_wallet_upgrade(state, player)
#                       and state.can_reach("Forsaken Fortress - Helmaroc King Heart Container", "Location", player)
#                       and can_play_song_of_passing(state, player),
#     )
#
#     # The Great Sea
#     set_rule(world.get_location("The Great Sea - Beedle's Shop Ship - 20 Rupee Item", player), lambda state: True)
#     set_rule(world.get_location("The Great Sea - Salvage Corp Gift", player), lambda state: True)
#     set_rule(world.get_location("The Great Sea - Cyclos", player), lambda state: has_heros_bow(state, player))
#     set_rule(
#         world.get_location("The Great Sea - Goron Trading Reward", player),
#         lambda state: rescued_aryll(state, player) and state.has("Delivery Bag", player),
#     )
#     set_rule(
#         world.get_location("The Great Sea - Withered Trees", player),
#         lambda state: can_access_forest_haven(state, player)
#                       and state.has("Empty Bottle", player)
#                       and can_play_ballad_of_gales(state, player)
#                       and state.can_reach("Cliff Plateau Isles - Highest Isle", "Location", player),
#     )
#     set_rule(
#         world.get_location("The Great Sea - Ghost Ship", player),
#         lambda state: state.has("Ghost Ship Chart", player)
#                       and can_play_ballad_of_gales(state, player)
#                       and can_defeat_wizzrobes(state, player)
#                       and can_defeat_poes(state, player)
#                       and can_defeat_redeads(state, player)
#                       and can_defeat_stalfos(state, player),
#     )
#
#     # Private Oasis
#     set_rule(
#         world.get_location("Private Oasis - Chest at Top of Waterfall", player),
#         lambda state: state.has("Hookshot", player) or can_fly_with_deku_leaf_outdoors(state, player),
#     )
#     set_rule(
#         world.get_location("Private Oasis - Cabana Labyrinth - Lower Floor Chest", player),
#         lambda state: can_access_cabana_labyrinth(state, player) and state.has("Skull Hammer", player),
#     )
#     set_rule(
#         world.get_location("Private Oasis - Cabana Labyrinth - Upper Floor Chest", player),
#         lambda state: can_access_cabana_labyrinth(state, player)
#                       and state.has("Skull Hammer", player)
#                       and can_play_winds_requiem(state, player),
#     )
#     set_rule(
#         world.get_location("Private Oasis - Big Octo", player),
#         lambda state: can_defeat_big_octos(state, player) and state.has("Grappling Hook", player),
#     )
#
#     # Spectacle Island
#     set_rule(world.get_location("Spectacle Island - Barrel Shooting - First Prize", player), lambda state: True)
#     set_rule(world.get_location("Spectacle Island - Barrel Shooting - Second Prize", player), lambda state: True)
#
#     # Needle Rock Isle
#     set_rule(
#         world.get_location("Needle Rock Isle - Chest", player),
#         lambda state: state.has("Bait Bag", player) and can_buy_hyoi_pears(state, player),
#     )
#     set_rule(
#         world.get_location("Needle Rock Isle - Cave", player),
#         lambda state: can_access_needle_rock_isle_secret_cave(state, player) and has_fire_arrows(state, player),
#     )
#     set_rule(
#         world.get_location("Needle Rock Isle - Golden Gunboat", player),
#         lambda state: state.has("Bombs", player) and state.has("Grappling Hook", player),
#     )
#
#     # Angular Isles
#     set_rule(world.get_location("Angular Isles - Peak", player), lambda state: True)
#     set_rule(
#         world.get_location("Angular Isles - Cave", player),
#         lambda state: can_access_angular_isles_secret_cave(state, player)
#                       and can_aim_mirror_shield(state, player)
#                       and (can_fly_with_deku_leaf_indoors(state, player) or state.has("Hookshot", player)),
#     )
#
#     # Boating Course
#     set_rule(world.get_location("Boating Course - Raft", player), lambda state: True)
#     set_rule(
#         world.get_location("Boating Course - Cave", player),
#         lambda state: can_access_boating_course_secret_cave(state, player)
#                       and can_hit_diamond_switches_at_range(state, player)
#                       and (can_defeat_miniblins_easily(state, player) or state._tww_precise_2(player)),
#     )
#
#     # Stone Watcher Island
#     set_rule(
#         world.get_location("Stone Watcher Island - Cave", player),
#         lambda state: can_access_stone_watcher_island_secret_cave(state, player)
#                       and can_defeat_armos(state, player)
#                       and can_defeat_wizzrobes(state, player)
#                       and can_defeat_darknuts(state, player)
#                       and can_play_winds_requiem(state, player),
#     )
#     set_rule(world.get_location("Stone Watcher Island - Lookout Platform Chest", player), lambda state: True)
#     set_rule(
#         world.get_location("Stone Watcher Island - Lookout Platform - Destroy the Cannons", player),
#         lambda state: can_destroy_cannons(state, player),
#     )
#
#     # Islet of Steel
#     set_rule(
#         world.get_location("Islet of Steel - Interior", player),
#         lambda state: state.has("Bombs", player) and can_play_winds_requiem(state, player),
#     )
#     set_rule(
#         world.get_location("Islet of Steel - Lookout Platform - Defeat the Enemies", player),
#         lambda state: can_defeat_wizzrobes_at_range(state, player),
#     )
#
#     # Overlook Island
#     set_rule(
#         world.get_location("Overlook Island - Cave", player),
#         lambda state: can_access_overlook_island_secret_cave(state, player)
#                       and can_defeat_stalfos(state, player)
#                       and can_defeat_wizzrobes(state, player)
#                       and can_defeat_red_chuchus(state, player)
#                       and can_defeat_green_chuchus(state, player)
#                       and can_defeat_keese(state, player)
#                       and can_defeat_fire_keese(state, player)
#                       and can_defeat_morths(state, player)
#                       and can_defeat_kargarocs(state, player)
#                       and can_defeat_darknuts(state, player)
#                       and can_play_winds_requiem(state, player),
#     )
#
#     # Bird's Peak Rock
#     set_rule(
#         world.get_location("Bird's Peak Rock - Cave", player),
#         lambda state: can_access_birds_peak_rock_secret_cave(state, player) and can_play_winds_requiem(state, player),
#     )
#
#     # Pawprint Isle
#     set_rule(
#         world.get_location("Pawprint Isle - Chuchu Cave - Chest", player),
#         lambda state: can_access_pawprint_isle_chuchu_cave(state, player),
#     )
#     set_rule(
#         world.get_location("Pawprint Isle - Chuchu Cave - Behind Left Boulder", player),
#         lambda state: can_access_pawprint_isle_chuchu_cave(state, player) and can_move_boulders(state, player),
#     )
#     set_rule(
#         world.get_location("Pawprint Isle - Chuchu Cave - Behind Right Boulder", player),
#         lambda state: can_access_pawprint_isle_chuchu_cave(state, player) and can_move_boulders(state, player),
#     )
#     set_rule(
#         world.get_location("Pawprint Isle - Chuchu Cave - Scale the Wall", player),
#         lambda state: can_access_pawprint_isle_chuchu_cave(state, player) and state.has("Grappling Hook", player),
#     )
#     set_rule(
#         world.get_location("Pawprint Isle - Wizzrobe Cave", player),
#         lambda state: can_access_pawprint_isle_wizzrobe_cave(state, player)
#                       and can_defeat_wizzrobes_at_range(state, player)
#                       and can_defeat_fire_keese(state, player)
#                       and can_defeat_magtails(state, player)
#                       and can_defeat_red_chuchus(state, player)
#                       and can_defeat_green_chuchus(state, player)
#                       and can_defeat_yellow_chuchus(state, player)
#                       and can_defeat_red_bubbles(state, player)
#                       and can_remove_peahat_armor(state, player),
#     )
#     set_rule(world.get_location("Pawprint Isle - Lookout Platform - Defeat the Enemies", player), lambda state: True)
#
#     # Thorned Fairy Island
#     set_rule(
#         world.get_location("Thorned Fairy Island - Great Fairy", player),
#         lambda state: can_access_thorned_fairy_fountain(state, player),
#     )
#     set_rule(
#         world.get_location("Thorned Fairy Island - Northeastern Lookout Platform - Destroy the Cannons", player),
#         lambda state: can_destroy_cannons(state, player),
#     )
#     set_rule(
#         world.get_location("Thorned Fairy Island - Southwestern Lookout Platform - Defeat the Enemies", player),
#         lambda state: can_fly_with_deku_leaf_outdoors(state, player),
#     )
#
#     # Eastern Fairy Island
#     set_rule(
#         world.get_location("Eastern Fairy Island - Great Fairy", player),
#         lambda state: can_access_eastern_fairy_fountain(state, player),
#     )
#     set_rule(
#         world.get_location("Eastern Fairy Island - Lookout Platform - Defeat the Cannons and Enemies", player),
#         lambda state: can_destroy_cannons(state, player),
#     )
#
#     # Western Fairy Island
#     set_rule(
#         world.get_location("Western Fairy Island - Great Fairy", player),
#         lambda state: can_access_western_fairy_fountain(state, player),
#     )
#     set_rule(world.get_location("Western Fairy Island - Lookout Platform", player), lambda state: True)
#
#     # Southern Fairy Island
#     set_rule(
#         world.get_location("Southern Fairy Island - Great Fairy", player),
#         lambda state: can_access_southern_fairy_fountain(state, player),
#     )
#     set_rule(
#         world.get_location("Southern Fairy Island - Lookout Platform - Destroy the Northwest Cannons", player),
#         lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#     set_rule(
#         world.get_location("Southern Fairy Island - Lookout Platform - Destroy the Southeast Cannons", player),
#         lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#
#     # Northern Fairy Island
#     set_rule(
#         world.get_location("Northern Fairy Island - Great Fairy", player),
#         lambda state: can_access_northern_fairy_fountain(state, player),
#     )
#     set_rule(world.get_location("Northern Fairy Island - Submarine", player), lambda state: True)
#
#     # Tingle Island
#     set_rule(
#         world.get_location("Tingle Island - Ankle - Reward for All Tingle Statues", player),
#         lambda state: state.has_group("Tingle Statues", player, 5),
#     )
#     set_rule(
#         world.get_location("Tingle Island - Big Octo", player),
#         lambda state: can_defeat_12_eye_big_octos(state, player) and state.has("Grappling Hook", player),
#     )
#
#     # Diamond Steppe Island
#     set_rule(
#         world.get_location("Diamond Steppe Island - Warp Maze Cave - First Chest", player),
#         lambda state: can_access_diamond_steppe_island_warp_maze_cave(state, player),
#     )
#     set_rule(
#         world.get_location("Diamond Steppe Island - Warp Maze Cave - Second Chest", player),
#         lambda state: can_access_diamond_steppe_island_warp_maze_cave(state, player),
#     )
#     set_rule(
#         world.get_location("Diamond Steppe Island - Big Octo", player),
#         lambda state: can_defeat_big_octos(state, player) and state.has("Grappling Hook", player),
#     )
#
#     # Bomb Island
#     set_rule(
#         world.get_location("Bomb Island - Cave", player),
#         lambda state: can_access_bomb_island_secret_cave(state, player) and can_stun_magtails(state, player),
#     )
#     set_rule(world.get_location("Bomb Island - Lookout Platform - Defeat the Enemies", player), lambda state: True)
#     set_rule(world.get_location("Bomb Island - Submarine", player), lambda state: True)
#
#     # Rock Spire Isle
#     set_rule(
#         world.get_location("Rock Spire Isle - Cave", player),
#         lambda state: can_access_rock_spire_isle_secret_cave(state, player),
#     )
#     set_rule(
#         world.get_location("Rock Spire Isle - Beedle's Special Shop Ship - 500 Rupee Item", player),
#         lambda state: has_any_wallet_upgrade(state, player) and can_farm_lots_of_rupees(state, player),
#     )
#     set_rule(
#         world.get_location("Rock Spire Isle - Beedle's Special Shop Ship - 950 Rupee Item", player),
#         lambda state: has_any_wallet_upgrade(state, player) and can_farm_lots_of_rupees(state, player),
#     )
#     set_rule(
#         world.get_location("Rock Spire Isle - Beedle's Special Shop Ship - 900 Rupee Item", player),
#         lambda state: has_any_wallet_upgrade(state, player) and can_farm_lots_of_rupees(state, player),
#     )
#     set_rule(
#         world.get_location("Rock Spire Isle - Western Lookout Platform - Destroy the Cannons", player),
#         lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#     set_rule(
#         world.get_location("Rock Spire Isle - Eastern Lookout Platform - Destroy the Cannons", player),
#         lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#     set_rule(world.get_location("Rock Spire Isle - Center Lookout Platform", player), lambda state: True)
#     set_rule(
#         world.get_location("Rock Spire Isle - Southeast Gunboat", player),
#         lambda state: state.has("Bombs", player) and state.has("Grappling Hook", player),
#     )
#
#     # Shark Island
#     set_rule(
#         world.get_location("Shark Island - Cave", player),
#         lambda state: can_access_shark_island_secret_cave(state, player) and can_defeat_miniblins(state, player),
#     )
#
#     # Cliff Plateau Isles
#     set_rule(
#         world.get_location("Cliff Plateau Isles - Cave", player),
#         lambda state: can_access_cliff_plateau_isles_secret_cave(state, player)
#                       and (
#                               can_defeat_boko_babas(state, player)
#                               or (state.has("Grappling Hook", player) and state._tww_obscure_1(
#                           player) and state._tww_precise_1(player))
#                       ),
#     )
#     set_rule(
#         world.get_location("Cliff Plateau Isles - Highest Isle", player),
#         lambda state: can_access_cliff_plateau_isles_inner_cave(state, player),
#     )
#     set_rule(world.get_location("Cliff Plateau Isles - Lookout Platform", player), lambda state: True)
#
#     # Crescent Moon Island
#     set_rule(world.get_location("Crescent Moon Island - Chest", player), lambda state: True)
#     set_rule(
#         world.get_location("Crescent Moon Island - Submarine", player),
#         lambda state: can_defeat_miniblins(state, player),
#     )
#
#     # Horseshoe Island
#     set_rule(
#         world.get_location("Horseshoe Island - Play Golf", player),
#         lambda state: can_fan_with_deku_leaf(state, player)
#                       and (can_fly_with_deku_leaf_outdoors(state, player) or state.has("Hookshot", player)),
#     )
#     set_rule(
#         world.get_location("Horseshoe Island - Cave", player),
#         lambda state: can_access_horseshoe_island_secret_cave(state, player)
#                       and can_defeat_mothulas(state, player)
#                       and can_defeat_winged_mothulas(state, player),
#     )
#     set_rule(world.get_location("Horseshoe Island - Northwestern Lookout Platform", player), lambda state: True)
#     set_rule(world.get_location("Horseshoe Island - Southeastern Lookout Platform", player), lambda state: True)
#
#     # Flight Control Platform
#     set_rule(
#         world.get_location("Flight Control Platform - Bird-Man Contest - First Prize", player),
#         lambda state: can_fly_with_deku_leaf_outdoors(state, player) and has_magic_meter_upgrade(state, player),
#     )
#     set_rule(
#         world.get_location("Flight Control Platform - Submarine", player),
#         lambda state: can_defeat_wizzrobes(state, player)
#                       and can_defeat_red_chuchus(state, player)
#                       and can_defeat_green_chuchus(state, player)
#                       and can_defeat_miniblins(state, player)
#                       and can_defeat_wizzrobes_at_range(state, player),
#     )
#
#     # Star Island
#     set_rule(
#         world.get_location("Star Island - Cave", player),
#         lambda state: can_access_star_island_secret_cave(state, player) and can_defeat_magtails(state, player),
#     )
#     set_rule(world.get_location("Star Island - Lookout Platform", player), lambda state: True)
#
#     # Star Belt Archipelago
#     set_rule(world.get_location("Star Belt Archipelago - Lookout Platform", player), lambda state: True)
#
#     # Five-Star Isles
#     set_rule(
#         world.get_location("Five-Star Isles - Lookout Platform - Destroy the Cannons", player),
#         lambda state: can_destroy_cannons(state, player),
#     )
#     set_rule(world.get_location("Five-Star Isles - Raft", player), lambda state: True)
#     set_rule(world.get_location("Five-Star Isles - Submarine", player), lambda state: True)
#
#     # Seven-Star Isles
#     set_rule(world.get_location("Seven-Star Isles - Center Lookout Platform", player), lambda state: True)
#     set_rule(world.get_location("Seven-Star Isles - Northern Lookout Platform", player), lambda state: True)
#     set_rule(
#         world.get_location("Seven-Star Isles - Southern Lookout Platform", player),
#         lambda state: can_defeat_wizzrobes_at_range(state, player),
#     )
#     set_rule(
#         world.get_location("Seven-Star Isles - Big Octo", player),
#         lambda state: can_defeat_12_eye_big_octos(state, player) and state.has("Grappling Hook", player),
#     )
#
#     # Cyclops Reef
#     set_rule(
#         world.get_location("Cyclops Reef - Destroy the Cannons and Gunboats", player),
#         lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#     set_rule(world.get_location("Cyclops Reef - Lookout Platform - Defeat the Enemies", player), lambda state: True)
#
#     # Two-Eye Reef
#     set_rule(
#         world.get_location("Two-Eye Reef - Destroy the Cannons and Gunboats", player),
#         lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#     set_rule(world.get_location("Two-Eye Reef - Lookout Platform", player), lambda state: True)
#     set_rule(
#         world.get_location("Two-Eye Reef - Big Octo Great Fairy", player),
#         lambda state: can_defeat_big_octos(state, player),
#     )
#
#     # Three-Eye Reef
#     set_rule(
#         world.get_location("Three-Eye Reef - Destroy the Cannons and Gunboats", player),
#         lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#
#     # Four-Eye Reef
#     set_rule(
#         world.get_location("Four-Eye Reef - Destroy the Cannons and Gunboats", player),
#         lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#
#     # Five-Eye Reef
#     set_rule(
#         world.get_location("Five-Eye Reef - Destroy the Cannons", player),
#         lambda state: can_destroy_cannons(state, player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#     set_rule(world.get_location("Five-Eye Reef - Lookout Platform", player), lambda state: True)
#
#     # Six-Eye Reef
#     set_rule(
#         world.get_location("Six-Eye Reef - Destroy the Cannons and Gunboats", player),
#         lambda state: state.has("Bombs", player) and can_fly_with_deku_leaf_outdoors(state, player),
#     )
#     set_rule(
#         world.get_location("Six-Eye Reef - Lookout Platform - Destroy the Cannons", player),
#         lambda state: can_destroy_cannons(state, player),
#     )
#     set_rule(world.get_location("Six-Eye Reef - Submarine", player), lambda state: True)
#
#     # Sunken Treasure
#     set_rule(
#         world.get_location("Forsaken Fortress Sector - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 1),
#     )
#     set_rule(
#         world.get_location("Star Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 2),
#     )
#     set_rule(
#         world.get_location("Northern Fairy Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 3),
#     )
#     set_rule(
#         world.get_location("Gale Isle - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 4),
#     )
#     set_rule(
#         world.get_location("Crescent Moon Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 5),
#     )
#     set_rule(
#         world.get_location("Seven-Star Isles - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player)
#                       and state._tww_has_chart_for_island(player, 6)
#                       and (state.has("Bombs", player) or state._tww_precise_1(player)),
#     )
#     set_rule(
#         world.get_location("Overlook Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 7),
#     )
#     set_rule(
#         world.get_location("Four-Eye Reef - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player)
#                       and state._tww_has_chart_for_island(player, 8)
#                       and (
#                               state.has("Bombs", player)
#                               or state._tww_precise_1(player)
#                               or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
#                       ),
#     )
#     set_rule(
#         world.get_location("Mother and Child Isles - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 9),
#     )
#     set_rule(
#         world.get_location("Spectacle Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 10),
#     )
#     set_rule(
#         world.get_location("Windfall Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 11),
#     )
#     set_rule(
#         world.get_location("Pawprint Isle - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 12),
#     )
#     set_rule(
#         world.get_location("Dragon Roost Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 13),
#     )
#     set_rule(
#         world.get_location("Flight Control Platform - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 14),
#     )
#     set_rule(
#         world.get_location("Western Fairy Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 15),
#     )
#     set_rule(
#         world.get_location("Rock Spire Isle - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 16),
#     )
#     set_rule(
#         world.get_location("Tingle Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 17),
#     )
#     set_rule(
#         world.get_location("Northern Triangle Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 18),
#     )
#     set_rule(
#         world.get_location("Eastern Fairy Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 19),
#     )
#     set_rule(
#         world.get_location("Fire Mountain - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 20),
#     )
#     set_rule(
#         world.get_location("Star Belt Archipelago - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 21),
#     )
#     set_rule(
#         world.get_location("Three-Eye Reef - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player)
#                       and state._tww_has_chart_for_island(player, 22)
#                       and (
#                               state.has("Bombs", player)
#                               or state._tww_precise_1(player)
#                               or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
#                       ),
#     )
#     set_rule(
#         world.get_location("Greatfish Isle - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 23),
#     )
#     set_rule(
#         world.get_location("Cyclops Reef - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player)
#                       and state._tww_has_chart_for_island(player, 24)
#                       and (
#                               state.has("Bombs", player)
#                               or state._tww_precise_1(player)
#                               or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
#                       ),
#     )
#     set_rule(
#         world.get_location("Six-Eye Reef - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player)
#                       and state._tww_has_chart_for_island(player, 25)
#                       and (
#                               state.has("Bombs", player)
#                               or state._tww_precise_1(player)
#                               or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
#                       ),
#     )
#     set_rule(
#         world.get_location("Tower of the Gods Sector - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 26),
#     )
#     set_rule(
#         world.get_location("Eastern Triangle Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 27),
#     )
#     set_rule(
#         world.get_location("Thorned Fairy Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 28),
#     )
#     set_rule(
#         world.get_location("Needle Rock Isle - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 29),
#     )
#     set_rule(
#         world.get_location("Islet of Steel - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 30),
#     )
#     set_rule(
#         world.get_location("Stone Watcher Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 31),
#     )
#     set_rule(
#         world.get_location("Southern Triangle Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player)
#                       and state._tww_has_chart_for_island(player, 32)
#                       and (can_defeat_seahats(state, player) or state._tww_precise_1(player)),
#     )
#     set_rule(
#         world.get_location("Private Oasis - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 33),
#     )
#     set_rule(
#         world.get_location("Bomb Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 34),
#     )
#     set_rule(
#         world.get_location("Bird's Peak Rock - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 35),
#     )
#     set_rule(
#         world.get_location("Diamond Steppe Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 36),
#     )
#     set_rule(
#         world.get_location("Five-Eye Reef - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player)
#                       and state._tww_has_chart_for_island(player, 37)
#                       and can_destroy_cannons(state, player),
#     )
#     set_rule(
#         world.get_location("Shark Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 38),
#     )
#     set_rule(
#         world.get_location("Southern Fairy Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 39),
#     )
#     set_rule(
#         world.get_location("Ice Ring Isle - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 40),
#     )
#     set_rule(
#         world.get_location("Forest Haven - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 41),
#     )
#     set_rule(
#         world.get_location("Cliff Plateau Isles - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 42),
#     )
#     set_rule(
#         world.get_location("Horseshoe Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 43),
#     )
#     set_rule(
#         world.get_location("Outset Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 44),
#     )
#     set_rule(
#         world.get_location("Headstone Island - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 45),
#     )
#     set_rule(
#         world.get_location("Two-Eye Reef - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player)
#                       and state._tww_has_chart_for_island(player, 46)
#                       and (
#                               state.has("Bombs", player)
#                               or state._tww_precise_1(player)
#                               or (can_use_magic_armor(state, player) and state._tww_obscure_1(player))
#                       ),
#     )
#     set_rule(
#         world.get_location("Angular Isles - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 47),
#     )
#     set_rule(
#         world.get_location("Boating Course - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 48),
#     )
#     set_rule(
#         world.get_location("Five-Star Isles - Sunken Treasure", player),
#         lambda state: state.has("Grappling Hook", player) and state._tww_has_chart_for_island(player, 49),
#     )
#
#     set_rule(
#         world.get_location("Defeat Ganondorf", player), lambda state: can_reach_and_defeat_ganondorf(state, player)
#     )
#
#     world.completion_condition[player] = lambda state: state.has("Victory", player)
