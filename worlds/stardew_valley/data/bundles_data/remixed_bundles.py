from .thematic_bundles import *
from ...bundles.bundle import IslandBundleTemplate
from ...bundles.bundle_room import BundleRoomTemplate
from ...strings.bundle_names import CCRoom

# Giant Stump
from ...strings.quality_names import ForageQuality

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

forest_items = [moss, fiber.as_amount(200), acorn.as_amount(10), maple_seed.as_amount(10), pine_cone.as_amount(10), mahogany_seed,
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