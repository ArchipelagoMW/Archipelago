from .vanilla_bundles import *
from ...bundles.bundle import BundleTemplate
from ...bundles.bundle_room import BundleRoomTemplate
from ...strings.bundle_names import CCRoom, BundleName

# Giant Stump
from ...strings.quality_names import ArtisanQuality, FishQuality

raccoon_fish_items_flat = [*raccoon_crab_pot_fish_items, *raccoon_smoked_fish_items]
raccoon_fish_bundle_thematic = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_fish, raccoon_fish_items_flat, 3, 2)
raccoon_artisan_bundle_thematic = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_artisan, raccoon_artisan_items, 3, 2)

raccoon_food_items_thematic = [*all_specific_dried_mushrooms, *raccoon_food_items, brown_egg.as_amount(5), large_egg.as_amount(2), large_brown_egg.as_amount(2),
                               green_algae.as_amount(10)]
raccoon_food_bundle_thematic = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_food, raccoon_food_items_thematic, 3, 2)

raccoon_foraging_bundle_thematic = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_foraging, raccoon_foraging_items, 3, 2)

giant_stump_bundles_thematic = [raccoon_fish_bundle_thematic, raccoon_artisan_bundle_thematic, raccoon_food_bundle_thematic, raccoon_foraging_bundle_thematic]
giant_stump_thematic = BundleRoomTemplate(CCRoom.raccoon_requests, giant_stump_bundles_thematic, 8)


# Crafts Room
spring_foraging_items_thematic = [*spring_foraging_items_vanilla, spring_onion, salmonberry, morel]
spring_foraging_bundle_thematic = BundleTemplate.extend_from(spring_foraging_bundle_vanilla, spring_foraging_items_thematic)

summer_foraging_items_thematic = [*summer_foraging_items_vanilla, fiddlehead_fern, red_mushroom, rainbow_shell]
summer_foraging_bundle_thematic = BundleTemplate.extend_from(summer_foraging_bundle_vanilla, summer_foraging_items_thematic)

fall_foraging_items_thematic = [*fall_foraging_items_vanilla, chanterelle]
fall_foraging_bundle_thematic = BundleTemplate.extend_from(fall_foraging_bundle_vanilla, fall_foraging_items_thematic)

winter_foraging_items_thematic = [*winter_foraging_items_vanilla, holly, nautilus_shell]
winter_foraging_bundle_thematic = BundleTemplate.extend_from(winter_foraging_bundle_vanilla, winter_foraging_items_thematic)

construction_items_thematic = [*construction_items_vanilla, clay.as_amount(10), fiber.as_amount(99), sap.as_amount(50)]
construction_bundle_thematic = BundleTemplate.extend_from(construction_bundle_vanilla, construction_items_thematic)

exotic_foraging_items_thematic = [*exotic_foraging_items_vanilla, coral, sea_urchin, clam, cockle, mussel, oyster, seaweed]
exotic_foraging_bundle_thematic = BundleTemplate.extend_from(exotic_foraging_bundle_vanilla, exotic_foraging_items_thematic)

crafts_room_bundles_thematic = [spring_foraging_bundle_thematic, summer_foraging_bundle_thematic, fall_foraging_bundle_thematic,
                                winter_foraging_bundle_thematic, construction_bundle_thematic, exotic_foraging_bundle_thematic]
crafts_room_thematic = BundleRoomTemplate(CCRoom.crafts_room, crafts_room_bundles_thematic, 6)

# Pantry
spring_crops_items_thematic = [*spring_crops_items_vanilla, blue_jazz, coffee_bean, garlic, kale, rhubarb, strawberry, tulip, unmilled_rice, carrot]
spring_crops_bundle_thematic = BundleTemplate.extend_from(spring_crops_bundle_vanilla, spring_crops_items_thematic)

summer_crops_items_thematic = [*summer_crops_items_vanilla, corn, hops, poppy, radish, red_cabbage, starfruit, summer_spangle, sunflower, wheat, summer_squash]
summer_crops_bundle_thematic = BundleTemplate.extend_from(summer_crops_bundle_vanilla, summer_crops_items_thematic)

fall_crops_items_thematic = [*fall_crops_items_vanilla, amaranth, artichoke, beet, bok_choy, cranberries, fairy_rose, grape,
                             sunflower, wheat, sweet_gem_berry, broccoli]
fall_crops_bundle_thematic = BundleTemplate.extend_from(fall_crops_bundle_vanilla, fall_crops_items_thematic)

all_crops_items = sorted({*spring_crops_items_thematic, *summer_crops_items_thematic, *fall_crops_items_thematic, powdermelon})

quality_crops_items_thematic = [item.as_quality_crop() for item in all_crops_items]
quality_crops_bundle_thematic = BundleTemplate.extend_from(quality_crops_bundle_vanilla, quality_crops_items_thematic)

animal_items_thematic = [*animal_items_vanilla, egg, brown_egg, milk, goat_milk, truffle,
                         duck_feather, rabbit_foot, dinosaur_egg, void_egg, golden_egg, ostrich_egg]
animal_bundle_thematic = BundleTemplate.extend_from(animal_bundle_vanilla, animal_items_thematic)

artisan_items_thematic = [*artisan_items_vanilla, beer, juice, mead, pale_ale, wine, pickles, caviar, aged_roe, coffee, green_tea, banana, mango]
artisan_bundle_thematic = BundleTemplate.extend_from(artisan_bundle_vanilla, artisan_items_thematic)

pantry_bundles_thematic = [spring_crops_bundle_thematic, summer_crops_bundle_thematic, fall_crops_bundle_thematic,
                           quality_crops_bundle_thematic, animal_bundle_thematic, artisan_bundle_thematic]
pantry_thematic = BundleRoomTemplate(CCRoom.pantry, pantry_bundles_thematic, 6)

# Fish Tank
river_fish_items_thematic = [*river_fish_items_vanilla, chub, rainbow_trout, lingcod, walleye, perch, pike, bream, salmon, smallmouth_bass, dorado]
river_fish_bundle_thematic = BundleTemplate.extend_from(river_fish_bundle_vanilla, river_fish_items_thematic)

lake_fish_items_thematic = [*lake_fish_items_vanilla, chub, rainbow_trout, lingcod, walleye, perch, midnight_carp]
lake_fish_bundle_thematic = BundleTemplate.extend_from(lake_fish_bundle_vanilla, lake_fish_items_thematic)

ocean_fish_items_thematic = [*ocean_fish_items_vanilla, pufferfish, super_cucumber, flounder, anchovy, red_mullet,
                             herring, eel, octopus, squid, sea_cucumber, albacore, halibut]
ocean_fish_bundle_thematic = BundleTemplate.extend_from(ocean_fish_bundle_vanilla, ocean_fish_items_thematic)

night_fish_items_thematic = [*night_fish_items_vanilla, super_cucumber, squid, midnight_carp, midnight_squid]
night_fish_bundle_thematic = BundleTemplate.extend_from(night_fish_bundle_vanilla, night_fish_items_thematic)

crab_pot_items_thematic = [*crab_pot_items_vanilla, *crab_pot_trash_items]
crab_pot_bundle_thematic = BundleTemplate.extend_from(crab_pot_bundle_vanilla, crab_pot_items_thematic)

specialty_fish_items_thematic = [*specialty_fish_items_vanilla, scorpion_carp, eel, octopus, lava_eel, ice_pip,
                                 stonefish, void_salmon, stingray, spookfish, midnight_squid, slimejack, goby]
specialty_fish_bundle_thematic = BundleTemplate.extend_from(specialty_fish_bundle_vanilla, specialty_fish_items_thematic)

fish_tank_bundles_thematic = [river_fish_bundle_thematic, lake_fish_bundle_thematic, ocean_fish_bundle_thematic,
                              night_fish_bundle_thematic, crab_pot_bundle_thematic, specialty_fish_bundle_thematic]
fish_tank_thematic = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_thematic, 6)

# Boiler Room
blacksmith_items_thematic = [*blacksmith_items_vanilla, iridium_bar, refined_quartz.as_amount(3), wilted_bouquet]
blacksmith_bundle_thematic = BundleTemplate.extend_from(blacksmith_bundle_vanilla, blacksmith_items_thematic)

geologist_items_thematic = [*geologist_items_vanilla, emerald, aquamarine, ruby, amethyst, topaz, jade, diamond]
geologist_bundle_thematic = BundleTemplate.extend_from(geologist_bundle_vanilla, geologist_items_thematic)

adventurer_items_thematic = [*adventurer_items_vanilla, bug_meat, coal.as_amount(5), bone_fragment.as_amount(10)]
adventurer_bundle_thematic = BundleTemplate.extend_from(adventurer_bundle_vanilla, adventurer_items_thematic)

boiler_room_bundles_thematic = [blacksmith_bundle_thematic, geologist_bundle_thematic, adventurer_bundle_thematic]
boiler_room_thematic = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_thematic, 3)

# Bulletin Board

# More recipes?
chef_items_thematic = [maki_roll, fried_egg, omelet, pizza, hashbrowns, pancakes, bread, tortilla,
                       farmer_s_lunch, survival_burger, dish_o_the_sea, miner_s_treat, roots_platter, salad,
                       cheese_cauliflower, parsnip_soup, fried_mushroom, salmon_dinner, pepper_poppers, spaghetti,
                       sashimi, blueberry_tart, algae_soup, pale_broth, chowder]
chef_bundle_thematic = BundleTemplate.extend_from(chef_bundle_vanilla, chef_items_thematic)

dye_red_items = [cranberries, hot_pepper, radish, rhubarb, spaghetti, strawberry, tomato, tulip, red_mushroom]
dye_orange_items = [poppy, pumpkin, apricot, orange, spice_berry, winter_root]
dye_yellow_items = [corn, parsnip, summer_spangle, sunflower, starfruit]
dye_green_items = [fiddlehead_fern, kale, artichoke, bok_choy, green_bean, cactus_fruit, duck_feather, dinosaur_egg]
dye_blue_items = [blueberry, blue_jazz, blackberry, crystal_fruit, aquamarine]
dye_purple_items = [beet, crocus, eggplant, red_cabbage, sweet_pea, iridium_bar, sea_urchin, amaranth]
dye_items_thematic = [dye_red_items, dye_orange_items, dye_yellow_items, dye_green_items, dye_blue_items, dye_purple_items]
dye_bundle_thematic = DeepBundleTemplate(CCRoom.bulletin_board, BundleName.dye, dye_items_thematic, 6, 6)

field_research_items_thematic = [*field_research_items_vanilla, geode, magma_geode, omni_geode,
                                 rainbow_shell, amethyst, bream, carp]
field_research_bundle_thematic = BundleTemplate.extend_from(field_research_bundle_vanilla, field_research_items_thematic)

fodder_items_thematic = [*fodder_items_vanilla, kale.as_amount(3), corn.as_amount(3), green_bean.as_amount(3),
                         potato.as_amount(3), green_algae.as_amount(5), white_algae.as_amount(3)]
fodder_bundle_thematic = BundleTemplate.extend_from(fodder_bundle_vanilla, fodder_items_thematic)

enchanter_items_thematic = [*enchanter_items_vanilla, purple_mushroom, solar_essence,
                            super_cucumber, void_essence, fire_quartz, frozen_tear, jade]
enchanter_bundle_thematic = BundleTemplate.extend_from(enchanter_bundle_vanilla, enchanter_items_thematic)

bulletin_board_bundles_thematic = [chef_bundle_thematic, dye_bundle_thematic, field_research_bundle_thematic, fodder_bundle_thematic, enchanter_bundle_thematic]
bulletin_board_thematic = BundleRoomTemplate(CCRoom.bulletin_board, bulletin_board_bundles_thematic, 5)

# Abandoned Joja Mart
missing_bundle_items_thematic = [*missing_bundle_items_vanilla, pale_ale.as_quality(ArtisanQuality.silver), beer.as_quality(ArtisanQuality.silver),
                                 mead.as_quality(ArtisanQuality.silver),
                                 cheese.as_quality(ArtisanQuality.silver), goat_cheese.as_quality(ArtisanQuality.silver), void_mayo, cloth, green_tea,
                                 truffle_oil, diamond,
                                 sweet_gem_berry.as_quality_crop(), starfruit.as_quality_crop(),
                                 tea_leaves.as_amount(5), lava_eel.as_quality(FishQuality.gold), scorpion_carp.as_quality(FishQuality.gold),
                                 blobfish.as_quality(FishQuality.gold)]
missing_bundle_thematic = BundleTemplate.extend_from(missing_bundle_vanilla, missing_bundle_items_thematic)
abandoned_joja_mart_bundles_thematic = [missing_bundle_thematic]
abandoned_joja_mart_thematic = BundleRoomTemplate(CCRoom.abandoned_joja_mart, abandoned_joja_mart_bundles_thematic, 1)

# Vault
vault_bundles_thematic = vault_bundles_vanilla
vault_thematic = BundleRoomTemplate(CCRoom.vault, vault_bundles_thematic, 4)
