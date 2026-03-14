from .bundle_items_data import *
from ...bundles.bundle import DeepBundleTemplate, BundleTemplate, MoneyBundleTemplate
from ...bundles.bundle_item import BundleItem
from ...bundles.bundle_room import BundleRoomTemplate
from ...content.vanilla.base import all_fruits, all_vegetables
from ...strings.artisan_good_names import ArtisanGood
from ...strings.bundle_names import CCRoom, BundleName
from ...strings.fish_names import Fish
from ...strings.forageable_names import all_edible_mushrooms

# Giant Stump
from ...strings.quality_names import ArtisanQuality, FishQuality

all_specific_jellies = [BundleItem(ArtisanGood.jelly, flavor=fruit, source=BundleItem.Sources.content) for fruit in all_fruits]
all_specific_pickles = [BundleItem(ArtisanGood.pickles, flavor=vegetable, source=BundleItem.Sources.content) for vegetable in all_vegetables]
all_specific_dried_fruits = [*[BundleItem(ArtisanGood.dried_fruit, flavor=fruit, source=BundleItem.Sources.content) for fruit in all_fruits],
                             BundleItem(ArtisanGood.raisins, source=BundleItem.Sources.content)]
all_specific_juices = [BundleItem(ArtisanGood.juice, flavor=vegetable, source=BundleItem.Sources.content) for vegetable in all_vegetables]

raccoon_crab_pot_fish_items = [periwinkle.as_amount(5), snail.as_amount(5), crayfish.as_amount(5), mussel.as_amount(5),
                               oyster.as_amount(5), cockle.as_amount(5), clam.as_amount(5)]
raccoon_smoked_fish_items = [BundleItem(ArtisanGood.smoked_fish, flavor=fish) for fish in
                             [Fish.largemouth_bass, Fish.bream, Fish.bullhead, Fish.chub, Fish.ghostfish, Fish.flounder, Fish.shad,
                              Fish.rainbow_trout, Fish.tilapia, Fish.red_mullet, Fish.tuna, Fish.midnight_carp, Fish.salmon, Fish.perch]]

raccoon_artisan_items = [*all_specific_jellies, *all_specific_pickles, *all_specific_dried_fruits, *all_specific_juices]
raccoon_fish_items_deep = [raccoon_crab_pot_fish_items, raccoon_smoked_fish_items]

all_specific_dried_mushrooms = [BundleItem(ArtisanGood.dried_mushroom, flavor=mushroom, source=BundleItem.Sources.content) for mushroom in all_edible_mushrooms]
raccoon_food_items = [egg.as_amount(5), cave_carrot.as_amount(5), white_algae.as_amount(5)]

raccoon_foraging_items = [moss.as_amount(10), rusty_spoon, trash.as_amount(5), slime.as_amount(99), bat_wing.as_amount(10), geode.as_amount(8),
                          frozen_geode.as_amount(5), magma_geode.as_amount(3), coral.as_amount(4), sea_urchin.as_amount(2), bug_meat.as_amount(10),
                          diamond, topaz.as_amount(3), ghostfish.as_amount(3)]

raccoon_fish_bundle_vanilla = DeepBundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_fish, raccoon_fish_items_deep, 2, 2)
raccoon_artisan_bundle_vanilla = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_artisan, raccoon_artisan_items, 2, 2)
raccoon_food_items_vanilla = [all_specific_dried_mushrooms, raccoon_food_items]
raccoon_food_bundle_vanilla = DeepBundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_food, raccoon_food_items_vanilla, 2, 2)
raccoon_foraging_bundle_vanilla = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_foraging, raccoon_foraging_items, 2, 2)
giant_stump_bundles_vanilla = [raccoon_fish_bundle_vanilla, raccoon_artisan_bundle_vanilla, raccoon_food_bundle_vanilla, raccoon_foraging_bundle_vanilla]
giant_stump_vanilla = BundleRoomTemplate(CCRoom.raccoon_requests, giant_stump_bundles_vanilla, 8)

# Crafts Room
spring_foraging_items_vanilla = [wild_horseradish, daffodil, leek, dandelion]
spring_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.spring_foraging, spring_foraging_items_vanilla, 4, 4)

summer_foraging_items_vanilla = [grape, spice_berry, sweet_pea]
summer_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.summer_foraging, summer_foraging_items_vanilla, 3, 3)

fall_foraging_items_vanilla = [common_mushroom, wild_plum, hazelnut, blackberry]
fall_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.fall_foraging, fall_foraging_items_vanilla, 4, 4)

winter_foraging_items_vanilla = [winter_root, crystal_fruit, snow_yam, crocus]
winter_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.winter_foraging, winter_foraging_items_vanilla, 4, 4)

construction_items_vanilla = [wood, stone, hardwood]
construction_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.construction, construction_items_vanilla, 4, 4)

exotic_foraging_items_vanilla = [coconut, cactus_fruit, cave_carrot, red_mushroom, purple_mushroom, maple_syrup, oak_resin, pine_tar, morel]
exotic_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.exotic_foraging, exotic_foraging_items_vanilla, 9, 5)

crafts_room_bundles_vanilla = [spring_foraging_bundle_vanilla, summer_foraging_bundle_vanilla, fall_foraging_bundle_vanilla,
                               winter_foraging_bundle_vanilla, construction_bundle_vanilla, exotic_foraging_bundle_vanilla]
crafts_room_vanilla = BundleRoomTemplate(CCRoom.crafts_room, crafts_room_bundles_vanilla, 6)

# Pantry
spring_crops_items_vanilla = [parsnip, green_bean, cauliflower, potato]
spring_crops_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.spring_crops, spring_crops_items_vanilla, 4, 4)

summer_crops_items_vanilla = [tomato, hot_pepper, blueberry, melon]
summer_crops_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.summer_crops, summer_crops_items_vanilla, 4, 4)

fall_crops_items_vanilla = [corn, eggplant, pumpkin, yam]
fall_crops_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.fall_crops, fall_crops_items_vanilla, 4, 4)

quality_crops_items_vanilla = [item.as_quality_crop() for item in [parsnip, melon, pumpkin, corn]]
quality_crops_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.quality_crops, quality_crops_items_vanilla, 4, 3)

animal_items_vanilla = [large_milk, large_brown_egg, large_egg, large_goat_milk, wool, duck_egg]
animal_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.animal, animal_items_vanilla, 6, 5)

artisan_items_vanilla = [truffle_oil, cloth, goat_cheese, cheese, honey, jelly, apple, apricot, orange, peach, pomegranate, cherry]
artisan_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.artisan, artisan_items_vanilla, 12, 6)

pantry_bundles_vanilla = [spring_crops_bundle_vanilla, summer_crops_bundle_vanilla, fall_crops_bundle_vanilla,
                          quality_crops_bundle_vanilla, animal_bundle_vanilla, artisan_bundle_vanilla]
pantry_vanilla = BundleRoomTemplate(CCRoom.pantry, pantry_bundles_vanilla, 6)

# Fish Tank
river_fish_items_vanilla = [sunfish, catfish, shad, tiger_trout]
river_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.river_fish, river_fish_items_vanilla, 4, 4)

lake_fish_items_vanilla = [largemouth_bass, carp, bullhead, sturgeon]
lake_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.lake_fish, lake_fish_items_vanilla, 4, 4)

ocean_fish_items_vanilla = [sardine, tuna, red_snapper, tilapia]
ocean_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.ocean_fish, ocean_fish_items_vanilla, 4, 4)

night_fish_items_vanilla = [walleye, bream, eel]
night_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.night_fish, night_fish_items_vanilla, 3, 3)

crab_pot_items_vanilla = [lobster, crayfish, crab, cockle, mussel, shrimp, snail, periwinkle, oyster, clam]
crab_pot_trash_items = [trash, driftwood, soggy_newspaper, broken_cd, broken_glasses]
crab_pot_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.crab_pot, crab_pot_items_vanilla, 10, 5)

specialty_fish_items_vanilla = [pufferfish, ghostfish, sandfish, woodskip]
specialty_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.specialty_fish, specialty_fish_items_vanilla, 4, 4)

fish_tank_bundles_vanilla = [river_fish_bundle_vanilla, lake_fish_bundle_vanilla, ocean_fish_bundle_vanilla,
                             night_fish_bundle_vanilla, crab_pot_bundle_vanilla, specialty_fish_bundle_vanilla]
fish_tank_vanilla = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_vanilla, 6)

# Boiler Room
blacksmith_items_vanilla = [copper_bar, iron_bar, gold_bar]
blacksmith_bundle_vanilla = BundleTemplate(CCRoom.boiler_room, BundleName.blacksmith, blacksmith_items_vanilla, 3, 3)

geologist_items_vanilla = [quartz, earth_crystal, frozen_tear, fire_quartz]
geologist_bundle_vanilla = BundleTemplate(CCRoom.boiler_room, BundleName.geologist, geologist_items_vanilla, 4, 4)

adventurer_items_vanilla = [slime, bat_wing, solar_essence, void_essence]
adventurer_bundle_vanilla = BundleTemplate(CCRoom.boiler_room, BundleName.adventurer, adventurer_items_vanilla, 4, 2)

boiler_room_bundles_vanilla = [blacksmith_bundle_vanilla, geologist_bundle_vanilla, adventurer_bundle_vanilla]
boiler_room_vanilla = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_vanilla, 3)

# Bulletin Board
chef_items_vanilla = [maple_syrup, fiddlehead_fern, truffle, poppy, maki_roll, fried_egg]
chef_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.chef, chef_items_vanilla, 6, 6)

dye_items_vanilla = [red_mushroom, sea_urchin, sunflower, duck_feather, aquamarine, red_cabbage]
dye_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.dye, dye_items_vanilla, 6, 6)

field_research_items_vanilla = [purple_mushroom, nautilus_shell, chub, frozen_geode]
field_research_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.field_research, field_research_items_vanilla, 4, 4)

fodder_items_vanilla = [wheat.as_amount(10), hay.as_amount(10), apple.as_amount(3)]
fodder_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.fodder, fodder_items_vanilla, 3, 3)

enchanter_items_vanilla = [oak_resin, wine, rabbit_foot, pomegranate]
enchanter_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.enchanter, enchanter_items_vanilla, 4, 4)

bulletin_board_bundles_vanilla = [chef_bundle_vanilla, dye_bundle_vanilla, field_research_bundle_vanilla, fodder_bundle_vanilla, enchanter_bundle_vanilla]
bulletin_board_vanilla = BundleRoomTemplate(CCRoom.bulletin_board, bulletin_board_bundles_vanilla, 5)

# Abandoned Joja Mart
missing_bundle_items_vanilla = [wine.as_quality(ArtisanQuality.silver), dinosaur_mayo, prismatic_shard, caviar,
                                ancient_fruit.as_quality_crop(), void_salmon.as_quality(FishQuality.gold)]
missing_bundle_vanilla = BundleTemplate(CCRoom.abandoned_joja_mart, BundleName.missing_bundle, missing_bundle_items_vanilla, 6, 5)

abandoned_joja_mart_bundles_vanilla = [missing_bundle_vanilla]
abandoned_joja_mart_vanilla = BundleRoomTemplate(CCRoom.abandoned_joja_mart, abandoned_joja_mart_bundles_vanilla, 1)


# Vault
vault_2500_gold = BundleItem.money_bundle(2500)
vault_5000_gold = BundleItem.money_bundle(5000)
vault_10000_gold = BundleItem.money_bundle(10000)
vault_25000_gold = BundleItem.money_bundle(25000)

vault_2500_bundle = MoneyBundleTemplate(CCRoom.vault, BundleName.money_2500, vault_2500_gold)
vault_5000_bundle = MoneyBundleTemplate(CCRoom.vault, BundleName.money_5000, vault_5000_gold)
vault_10000_bundle = MoneyBundleTemplate(CCRoom.vault, BundleName.money_10000, vault_10000_gold)
vault_25000_bundle = MoneyBundleTemplate(CCRoom.vault, BundleName.money_25000, vault_25000_gold)

vault_bundles_vanilla = [vault_2500_bundle, vault_5000_bundle, vault_10000_bundle, vault_25000_bundle]
vault_vanilla = BundleRoomTemplate(CCRoom.vault, vault_bundles_vanilla, 4)
