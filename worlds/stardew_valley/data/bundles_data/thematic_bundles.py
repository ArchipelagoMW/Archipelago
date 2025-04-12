from .vanilla_bundles import *
from ...bundles.bundle import BundleTemplate
from ...bundles.bundle_room import BundleRoomTemplate
from ...strings.bundle_names import CCRoom, BundleName

# Giant Stump
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

construction_items_thematic = [*construction_items_vanilla, clay, fiber, sap.as_amount(50)]
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
                                 stonefish, void_salmon, stingray, spookfish, midnight_squid]
specialty_fish_bundle_thematic = BundleTemplate.extend_from(specialty_fish_bundle_vanilla, specialty_fish_items_thematic)

fish_tank_bundles_thematic = [river_fish_bundle_thematic, lake_fish_bundle_thematic, ocean_fish_bundle_thematic,
                              night_fish_bundle_thematic, crab_pot_bundle_thematic, specialty_fish_bundle_thematic]
fish_tank_thematic = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_thematic, 6)

# Boiler Room
blacksmith_items_thematic = [*blacksmith_items_vanilla, iridium_bar, refined_quartz.as_amount(3), wilted_bouquet]
blacksmith_bundle_thematic = BundleTemplate.extend_from(blacksmith_bundle_vanilla, blacksmith_items_thematic)

geologist_items_thematic = [*geologist_items_vanilla, emerald, aquamarine, ruby, amethyst, topaz, jade, diamond]
geologist_bundle_thematic = BundleTemplate.extend_from(geologist_bundle_vanilla, geologist_items_thematic)

adventurer_items_thematic = [*adventurer_items_vanilla, bug_meat, coal, bone_fragment.as_amount(10)]
adventurer_bundle_thematic = BundleTemplate.extend_from(adventurer_bundle_vanilla, adventurer_items_thematic)

boiler_room_bundles_thematic = [blacksmith_bundle_thematic, geologist_bundle_thematic, adventurer_bundle_thematic]
boiler_room_thematic = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_thematic, 3)