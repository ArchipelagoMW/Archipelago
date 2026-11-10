from .thematic_bundles import *
from ...bundles.bundle import IslandBundleTemplate, FestivalBundleTemplate, CurrencyBundleTemplate
from ...bundles.bundle_room import BundleRoomTemplate
from ...content import content_packs
from ...strings.bundle_names import CCRoom

# Giant Stump
from ...strings.quality_names import ForageQuality, FishQuality

giant_stump_bundles_remixed = giant_stump_bundles_thematic
giant_stump_remixed = BundleRoomTemplate(CCRoom.raccoon_requests, giant_stump_bundles_remixed, 8)

# Crafts Room

beach_foraging_items = [nautilus_shell, coral, sea_urchin, rainbow_shell, clam, cockle, mussel, oyster, seaweed]
beach_foraging_bundle = BundleTemplate(CCRoom.crafts_room, BundleName.beach_foraging, beach_foraging_items, 4, 4)

mines_foraging_items = [quartz, earth_crystal, frozen_tear, fire_quartz, red_mushroom, purple_mushroom, cave_carrot]
mines_foraging_bundle = BundleTemplate(CCRoom.crafts_room, BundleName.mines_foraging, mines_foraging_items, 4, 4)

desert_foraging_items = [cactus_fruit.as_quality(ForageQuality.gold), cactus_fruit.as_amount(5), coconut.as_quality(ForageQuality.gold), coconut.as_amount(5)]
desert_foraging_bundle = BundleTemplate(CCRoom.crafts_room, BundleName.desert_foraging, desert_foraging_items, 2, 2)

island_foraging_items = [ginger.as_amount(5), magma_cap.as_quality(ForageQuality.gold), magma_cap.as_amount(5),
                         fiddlehead_fern.as_quality(ForageQuality.gold), fiddlehead_fern.as_amount(5)]
island_foraging_bundle = IslandBundleTemplate(CCRoom.crafts_room, BundleName.island_foraging, island_foraging_items, 2, 2)

sticky_items = [sap.as_amount(500), sap.as_amount(500)]
sticky_bundle = BundleTemplate(CCRoom.crafts_room, BundleName.sticky, sticky_items, 1, 1)

forest_items = [moss.as_amount(10), fiber.as_amount(200), acorn.as_amount(10), maple_seed.as_amount(10), pine_cone.as_amount(10), mahogany_seed,
                mushroom_tree_seed, mossy_seed.as_amount(5), mystic_tree_seed]
forest_bundle = BundleTemplate(CCRoom.crafts_room, BundleName.forest, forest_items, 4, 2)

wild_medicine_items = [item.as_amount(5) for item in [purple_mushroom, fiddlehead_fern, white_algae, hops, blackberry, dandelion]]
wild_medicine_bundle = BundleTemplate(CCRoom.crafts_room, BundleName.wild_medicine, wild_medicine_items, 4, 3)

quality_foraging_items = sorted({item.as_quality(ForageQuality.gold).as_amount(3)
                                 for item in
                                 [*spring_foraging_items_thematic, *summer_foraging_items_thematic, *fall_foraging_items_thematic,
                                  *winter_foraging_items_thematic, *beach_foraging_items, *desert_foraging_items, magma_cap] if item.can_have_quality})
quality_foraging_bundle = BundleTemplate(CCRoom.crafts_room, BundleName.quality_foraging, quality_foraging_items, 4, 3)

green_rain_items = [moss.as_amount(200), fiber.as_amount(200), mossy_seed.as_amount(20), fiddlehead_fern.as_amount(10)]
green_rain_bundle = BundleTemplate(CCRoom.crafts_room, BundleName.green_rain, green_rain_items, 4, 3)

totems_items = [warp_totem_beach.as_amount(5), warp_totem_mountains.as_amount(5), warp_totem_farm.as_amount(5), warp_totem_desert.as_amount(5),
                warp_totem_island.as_amount(5), rain_totem.as_amount(5), treasure_totem.as_amount(5)]
totems_bundle = BundleTemplate(CCRoom.crafts_room, BundleName.totems, totems_items, 4, 3)

crafts_room_bundles_remixed = [*crafts_room_bundles_thematic, beach_foraging_bundle, mines_foraging_bundle, desert_foraging_bundle,
                               island_foraging_bundle, sticky_bundle, forest_bundle, wild_medicine_bundle, quality_foraging_bundle, green_rain_bundle]
crafts_room_remixed = BundleRoomTemplate(CCRoom.crafts_room, crafts_room_bundles_remixed, 6)

# Pantry

rare_crops_items = [ancient_fruit, sweet_gem_berry]
rare_crops_bundle = BundleTemplate(CCRoom.pantry, BundleName.rare_crops, rare_crops_items, 2, 2)

# all_specific_roes = [BundleItem(AnimalProduct.roe, flavor=fruit, source=BundleItem.Sources.content) for fruit in all_fish]
fish_farmer_items = [roe.as_amount(15), aged_roe.as_amount(5), squid_ink, caviar.as_amount(5)]
fish_farmer_bundle = BundleTemplate(CCRoom.pantry, BundleName.fish_farmer, fish_farmer_items, 3, 2)

garden_items = [tulip, blue_jazz, summer_spangle, sunflower, fairy_rose, poppy, bouquet]
garden_bundle = BundleTemplate(CCRoom.pantry, BundleName.garden, garden_items, 5, 4)

brewer_items = [mead, pale_ale, wine, juice, green_tea, beer]
brewer_bundle = BundleTemplate(CCRoom.pantry, BundleName.brewer, brewer_items, 5, 4)

orchard_items = [apple, apricot, orange, peach, pomegranate, cherry, banana, mango]
orchard_bundle = BundleTemplate(CCRoom.pantry, BundleName.orchard, orchard_items, 6, 4)

island_crops_items = [pineapple, taro_root, banana, mango]
island_crops_bundle = IslandBundleTemplate(CCRoom.pantry, BundleName.island_crops, island_crops_items, 3, 3)

agronomist_items = [basic_fertilizer, quality_fertilizer, deluxe_fertilizer,
                    basic_retaining_soil, quality_retaining_soil, deluxe_retaining_soil,
                    speed_gro, deluxe_speed_gro, hyper_speed_gro, tree_fertilizer]
agronomist_bundle = BundleTemplate(CCRoom.pantry, BundleName.agronomist, agronomist_items, 4, 3)

slime_farmer_items = [slime.as_amount(99), petrified_slime.as_amount(10), blue_slime_egg, red_slime_egg,
                      purple_slime_egg, green_slime_egg, tiger_slime_egg]
slime_farmer_bundle = BundleTemplate(CCRoom.pantry, BundleName.slime_farmer, slime_farmer_items, 4, 3)

sommelier_items = [BundleItem(ArtisanGood.wine, flavor=fruit, source=BundleItem.Sources.content) for fruit in all_fruits]
sommelier_bundle = BundleTemplate(CCRoom.pantry, BundleName.sommelier, sommelier_items, 6, 3)

dry_items = [*[BundleItem(ArtisanGood.dried_fruit, flavor=fruit, source=BundleItem.Sources.content) for fruit in all_fruits],
             *[BundleItem(ArtisanGood.dried_mushroom, flavor=mushroom, source=BundleItem.Sources.content) for mushroom in all_edible_mushrooms],
             BundleItem(ArtisanGood.raisins, source=BundleItem.Sources.content)]
dry_bundle = BundleTemplate(CCRoom.pantry, BundleName.dry, dry_items, 6, 3)

pantry_bundles_remixed = [*pantry_bundles_thematic, rare_crops_bundle, fish_farmer_bundle, garden_bundle,
                          brewer_bundle, orchard_bundle, island_crops_bundle, agronomist_bundle, slime_farmer_bundle, sommelier_bundle, dry_bundle]
pantry_remixed = BundleRoomTemplate(CCRoom.pantry, pantry_bundles_remixed, 6)

# Fish Tank
trash_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.trash, crab_pot_trash_items, 4, 4)

spring_fish_items = [herring, halibut, shad, flounder, sunfish, sardine, catfish, anchovy, smallmouth_bass, eel, legend]
spring_fish_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.spring_fish, spring_fish_items, 4, 4)

summer_fish_items = [tuna, pike, red_mullet, sturgeon, red_snapper, super_cucumber, tilapia, pufferfish, rainbow_trout,
                     octopus, dorado, halibut, shad, flounder, sunfish, crimsonfish]
summer_fish_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.summer_fish, summer_fish_items, 4, 4)

fall_fish_items = [red_snapper, super_cucumber, tilapia, shad, sardine, catfish, anchovy, smallmouth_bass, eel, midnight_carp,
                   walleye, sea_cucumber, tiger_trout, albacore, salmon, angler]
fall_fish_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.fall_fish, fall_fish_items, 4, 4)

winter_fish_items = [perch, squid, lingcod, tuna, pike, red_mullet, sturgeon, red_snapper, herring, halibut, sardine,
                     midnight_carp, sea_cucumber, tiger_trout, albacore, glacierfish]
winter_fish_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.winter_fish, winter_fish_items, 4, 4)

rain_fish_items = [red_snapper, shad, catfish, eel, walleye]
rain_fish_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.rain_fish, rain_fish_items, 3, 3)

quality_fish_items = sorted({
    item.as_quality(FishQuality.gold).as_amount(2)
    for item in [*river_fish_items_thematic, *lake_fish_items_thematic, *ocean_fish_items_thematic]
})
quality_fish_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.quality_fish, quality_fish_items, 4, 3)

master_fisher_items = [lava_eel, scorpion_carp, octopus, blobfish, lingcod, ice_pip, super_cucumber, stingray, void_salmon, pufferfish]
master_fisher_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.master_fisher, master_fisher_items, 4, 2)

legendary_fish_items = [angler, legend, mutant_carp, crimsonfish, glacierfish]
legendary_fish_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.legendary_fish, legendary_fish_items, 4, 2)

island_fish_items = [lionfish, blue_discus, stingray]
island_fish_bundle = IslandBundleTemplate(CCRoom.fish_tank, BundleName.island_fish, island_fish_items, 3, 3)

tackle_items = [spinner, dressed_spinner, trap_bobber, sonar_bobber, cork_bobber, lead_bobber, treasure_hunter, barbed_hook, curiosity_lure, quality_bobber]
tackle_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.tackle, tackle_items, 3, 2)

bait_items = [bait, magnet, wild_bait, magic_bait, challenge_bait, deluxe_bait, targeted_bait]
bait_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.bait, bait_items, 3, 2)

# This bundle could change based on content packs, once the fish are properly in it. Until then, I'm not sure how, so pelican town only
specific_bait_items = [BundleItem(ArtisanGood.targeted_bait, flavor=fish.name).as_amount(10) for fish in content_packs.pelican_town.fishes]
specific_bait_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.specific_bait, specific_bait_items, 6, 3)

deep_fishing_items = [blobfish, spook_fish, midnight_squid, sea_cucumber, super_cucumber, octopus, pearl, seaweed]
deep_fishing_bundle = FestivalBundleTemplate(CCRoom.fish_tank, BundleName.deep_fishing, deep_fishing_items, 4, 3)

smokeable_fish = [Fish.largemouth_bass, Fish.bream, Fish.bullhead, Fish.chub, Fish.ghostfish, Fish.flounder, Fish.shad, Fish.rainbow_trout, Fish.tilapia,
                  Fish.red_mullet, Fish.tuna, Fish.midnight_carp, Fish.salmon, Fish.perch]
fish_smoker_items = [BundleItem(ArtisanGood.smoked_fish, flavor=fish) for fish in smokeable_fish]
fish_smoker_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.fish_smoker, fish_smoker_items, 6, 3)

fish_tank_bundles_remixed = [*fish_tank_bundles_thematic, spring_fish_bundle, summer_fish_bundle,
                             fall_fish_bundle, winter_fish_bundle, trash_bundle, rain_fish_bundle,
                             quality_fish_bundle, master_fisher_bundle, legendary_fish_bundle,
                             tackle_bundle, bait_bundle, specific_bait_bundle, deep_fishing_bundle,
                             fish_smoker_bundle]

# In Remixed, the trash items are in the recycling bundle, so we don't use the thematic version of the crab pot bundle that added trash items to it
fish_tank_bundles_remixed.remove(crab_pot_bundle_thematic)
fish_tank_bundles_remixed.append(crab_pot_bundle_vanilla)

fish_tank_remixed = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_remixed, 6)

# Boiler Room

# Where to put radioactive bar?
treasure_hunter_items = [emerald, aquamarine, ruby, amethyst, topaz, jade, diamond]
treasure_hunter_bundle = BundleTemplate(CCRoom.boiler_room, BundleName.treasure_hunter, treasure_hunter_items, 6, 5)

engineer_items = [iridium_ore.as_amount(5), battery_pack, refined_quartz.as_amount(5), diamond]
engineer_bundle = BundleTemplate(CCRoom.boiler_room, BundleName.engineer, engineer_items, 3, 3)

demolition_items = [cherry_bomb, bomb, mega_bomb, explosive_ammo]
demolition_bundle = BundleTemplate(CCRoom.boiler_room, BundleName.demolition, demolition_items, 3, 3)

recycling_items = [stone, coal, iron_ore, wood, cloth, refined_quartz]
recycling_bundle = BundleTemplate(CCRoom.boiler_room, BundleName.recycling, recycling_items, 4, 4)

archaeologist_items = [golden_mask, golden_relic, ancient_drum, dwarf_gadget, dwarvish_helm, prehistoric_handaxe, bone_flute, anchor, prehistoric_tool,
                       chicken_statue, rusty_cog, rusty_spur, rusty_spoon, ancient_sword, ornamental_fan, elvish_jewelry, ancient_doll, chipped_amphora]
archaeologist_bundle = BundleTemplate(CCRoom.boiler_room, BundleName.archaeologist, archaeologist_items, 6, 3)

paleontologist_items = [prehistoric_scapula, prehistoric_tibia, prehistoric_skull, skeletal_hand, prehistoric_rib, prehistoric_vertebra, skeletal_tail,
                        nautilus_fossil, amphibian_fossil, palm_fossil, trilobite]
paleontologist_bundle = BundleTemplate(CCRoom.boiler_room, BundleName.paleontologist, paleontologist_items, 6, 3)

boiler_room_bundles_remixed = [*boiler_room_bundles_thematic, treasure_hunter_bundle, engineer_bundle,
                               demolition_bundle, recycling_bundle, archaeologist_bundle, paleontologist_bundle]
boiler_room_remixed = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_remixed, 3)

# Bulletin Board
children_items = [salmonberry.as_amount(10), cookie, ancient_doll, ice_cream, cranberry_candy, ginger_ale,
                  grape.as_amount(10), pink_cake, snail, fairy_rose, plum_pudding]
children_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.children, children_items, 4, 3)

forager_items = [salmonberry.as_amount(50), blackberry.as_amount(50), wild_plum.as_amount(20), snow_yam.as_amount(20),
                 common_mushroom.as_amount(20), grape.as_amount(20), spring_onion.as_amount(20)]
forager_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.forager, forager_items, 3, 2)

home_cook_items = [egg.as_amount(10), milk.as_amount(10), wheat_flour.as_amount(100), sugar.as_amount(100), vinegar.as_amount(100),
                   chocolate_cake, pancakes, rhubarb_pie]
home_cook_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.home_cook, home_cook_items, 3, 3)

helper_items = [prize_ticket, mystery_box.as_amount(5), gold_mystery_box]
helper_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.helper, helper_items, 2, 2)

spirit_eve_items = [jack_o_lantern, corn.as_amount(10), bat_wing.as_amount(10)]
spirit_eve_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.spirit_eve, spirit_eve_items, 3, 3)

winter_star_items = [holly.as_amount(5), plum_pudding, stuffing, powdermelon.as_amount(5)]
winter_star_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.winter_star, winter_star_items, 2, 2)

bartender_items = [shrimp_cocktail, triple_shot_espresso, ginger_ale, cranberry_candy, beer, pale_ale, pina_colada]
bartender_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.bartender, bartender_items, 3, 3)

calico_items = [calico_egg.as_amount(200), calico_egg.as_amount(200), calico_egg.as_amount(200), calico_egg.as_amount(200),
                magic_rock_candy, mega_bomb.as_amount(10), mystery_box.as_amount(10), mixed_seeds.as_amount(50),
                strawberry_seeds.as_amount(20),
                spicy_eel.as_amount(5), crab_cakes.as_amount(5), eggplant_parmesan.as_amount(5),
                pumpkin_soup.as_amount(5), lucky_lunch.as_amount(5) ]
calico_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.calico, calico_items, 2, 2)

raccoon_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.raccoon, raccoon_foraging_items, 4, 4)

bulletin_board_bundles_remixed = [*bulletin_board_bundles_thematic, children_bundle, forager_bundle, home_cook_bundle,
                                  helper_bundle, spirit_eve_bundle, winter_star_bundle, bartender_bundle, calico_bundle, raccoon_bundle]
bulletin_board_remixed = BundleRoomTemplate(CCRoom.bulletin_board, bulletin_board_bundles_remixed, 5)

# Abandoned Joja Mart
abandoned_joja_mart_remixed = abandoned_joja_mart_thematic

# Vault
vault_gambler_items = BundleItem(Currency.qi_coin, 10000)
vault_gambler_bundle = CurrencyBundleTemplate(CCRoom.vault, BundleName.gambler, vault_gambler_items)

vault_carnival_items = BundleItem(Currency.star_token, 2500, source=BundleItem.Sources.festival)
vault_carnival_bundle = CurrencyBundleTemplate(CCRoom.vault, BundleName.carnival, vault_carnival_items)

vault_walnut_hunter_items = BundleItem(Currency.golden_walnut, 25)
vault_walnut_hunter_bundle = CurrencyBundleTemplate(CCRoom.vault, BundleName.walnut_hunter, vault_walnut_hunter_items)

vault_qi_helper_items = BundleItem(Currency.qi_gem, 25, source=BundleItem.Sources.island)
vault_qi_helper_bundle = CurrencyBundleTemplate(CCRoom.vault, BundleName.qi_helper, vault_qi_helper_items)

vault_bundles_remixed = [*vault_bundles_vanilla, vault_gambler_bundle, vault_qi_helper_bundle, vault_carnival_bundle]  # , vault_walnut_hunter_bundle
vault_remixed = BundleRoomTemplate(CCRoom.vault, vault_bundles_remixed, 4)
