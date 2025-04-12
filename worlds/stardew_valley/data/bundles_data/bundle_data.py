from .bundle_items_data import *
from ...bundles.bundle import BundleTemplate, IslandBundleTemplate, DeepBundleTemplate, CurrencyBundleTemplate, MoneyBundleTemplate, FestivalBundleTemplate
from ...bundles.bundle_item import BundleItem
from ...bundles.bundle_room import BundleRoomTemplate
from ...content import content_packs
from ...strings.artisan_good_names import ArtisanGood
from ...strings.bundle_names import CCRoom, BundleName
from ...strings.currency_names import Currency
from ...strings.fish_names import Fish
from ...strings.quality_names import ArtisanQuality, FishQuality


# Crafts Room

# Fish Tank
river_fish_items_vanilla = [sunfish, catfish, shad, tiger_trout]
river_fish_items_thematic = [*river_fish_items_vanilla, chub, rainbow_trout, lingcod, walleye, perch, pike, bream, salmon, smallmouth_bass, dorado]
river_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.river_fish, river_fish_items_vanilla, 4, 4)
river_fish_bundle_thematic = BundleTemplate.extend_from(river_fish_bundle_vanilla, river_fish_items_thematic)

lake_fish_items_vanilla = [largemouth_bass, carp, bullhead, sturgeon]
lake_fish_items_thematic = [*lake_fish_items_vanilla, chub, rainbow_trout, lingcod, walleye, perch, midnight_carp]
lake_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.lake_fish, lake_fish_items_vanilla, 4, 4)
lake_fish_bundle_thematic = BundleTemplate.extend_from(lake_fish_bundle_vanilla, lake_fish_items_thematic)

ocean_fish_items_vanilla = [sardine, tuna, red_snapper, tilapia]
ocean_fish_items_thematic = [*ocean_fish_items_vanilla, pufferfish, super_cucumber, flounder, anchovy, red_mullet,
                             herring, eel, octopus, squid, sea_cucumber, albacore, halibut]
ocean_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.ocean_fish, ocean_fish_items_vanilla, 4, 4)
ocean_fish_bundle_thematic = BundleTemplate.extend_from(ocean_fish_bundle_vanilla, ocean_fish_items_thematic)

night_fish_items_vanilla = [walleye, bream, eel]
night_fish_items_thematic = [*night_fish_items_vanilla, super_cucumber, squid, midnight_carp, midnight_squid]
night_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.night_fish, night_fish_items_vanilla, 3, 3)
night_fish_bundle_thematic = BundleTemplate.extend_from(night_fish_bundle_vanilla, night_fish_items_thematic)

crab_pot_items_vanilla = [lobster, crayfish, crab, cockle, mussel, shrimp, snail, periwinkle, oyster, clam]
crab_pot_trash_items = [trash, driftwood, soggy_newspaper, broken_cd, broken_glasses]
crab_pot_items_thematic = [*crab_pot_items_vanilla, *crab_pot_trash_items]
crab_pot_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.crab_pot, crab_pot_items_vanilla, 10, 5)
crab_pot_bundle_thematic = BundleTemplate.extend_from(crab_pot_bundle_vanilla, crab_pot_items_thematic)
trash_bundle = BundleTemplate(CCRoom.fish_tank, BundleName.trash, crab_pot_trash_items, 4, 4)

specialty_fish_items_vanilla = [pufferfish, ghostfish, sandfish, woodskip]
specialty_fish_items_thematic = [*specialty_fish_items_vanilla, scorpion_carp, eel, octopus, lava_eel, ice_pip,
                                 stonefish, void_salmon, stingray, spookfish, midnight_squid]
specialty_fish_bundle_vanilla = BundleTemplate(CCRoom.fish_tank, BundleName.specialty_fish, specialty_fish_items_vanilla, 4, 4)
specialty_fish_bundle_thematic = BundleTemplate.extend_from(specialty_fish_bundle_vanilla, specialty_fish_items_thematic)

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

fish_tank_bundles_vanilla = [river_fish_bundle_vanilla, lake_fish_bundle_vanilla, ocean_fish_bundle_vanilla,
                             night_fish_bundle_vanilla, crab_pot_bundle_vanilla, specialty_fish_bundle_vanilla]
fish_tank_bundles_thematic = [river_fish_bundle_thematic, lake_fish_bundle_thematic, ocean_fish_bundle_thematic,
                              night_fish_bundle_thematic, crab_pot_bundle_thematic, specialty_fish_bundle_thematic]
fish_tank_bundles_remixed = [*fish_tank_bundles_thematic, spring_fish_bundle, summer_fish_bundle, fall_fish_bundle, winter_fish_bundle, trash_bundle,
                             rain_fish_bundle, quality_fish_bundle, master_fisher_bundle, legendary_fish_bundle, tackle_bundle, bait_bundle,
                             specific_bait_bundle, deep_fishing_bundle, fish_smoker_bundle]

# In Remixed, the trash items are in the recycling bundle, so we don't use the thematic version of the crab pot bundle that added trash items to it
fish_tank_bundles_remixed.remove(crab_pot_bundle_thematic)
fish_tank_bundles_remixed.append(crab_pot_bundle_vanilla)
fish_tank_vanilla = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_vanilla, 6)
fish_tank_thematic = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_thematic, 6)
fish_tank_remixed = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_remixed, 6)

# Boiler Room
blacksmith_items_vanilla = [copper_bar, iron_Bar, gold_bar]
blacksmith_items_thematic = [*blacksmith_items_vanilla, iridium_bar, refined_quartz.as_amount(3), wilted_bouquet]
blacksmith_bundle_vanilla = BundleTemplate(CCRoom.boiler_room, BundleName.blacksmith, blacksmith_items_vanilla, 3, 3)
blacksmith_bundle_thematic = BundleTemplate.extend_from(blacksmith_bundle_vanilla, blacksmith_items_thematic)

geologist_items_vanilla = [quartz, earth_crystal, frozen_tear, fire_quartz]
geologist_items_thematic = [*geologist_items_vanilla, emerald, aquamarine, ruby, amethyst, topaz, jade, diamond]
geologist_bundle_vanilla = BundleTemplate(CCRoom.boiler_room, BundleName.geologist, geologist_items_vanilla, 4, 4)
geologist_bundle_thematic = BundleTemplate.extend_from(geologist_bundle_vanilla, geologist_items_thematic)

adventurer_items_vanilla = [slime, bat_wing, solar_essence, void_essence]
adventurer_items_thematic = [*adventurer_items_vanilla, bug_meat, coal, bone_fragment.as_amount(10)]
adventurer_bundle_vanilla = BundleTemplate(CCRoom.boiler_room, BundleName.adventurer, adventurer_items_vanilla, 4, 2)
adventurer_bundle_thematic = BundleTemplate.extend_from(adventurer_bundle_vanilla, adventurer_items_thematic)

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

boiler_room_bundles_vanilla = [blacksmith_bundle_vanilla, geologist_bundle_vanilla, adventurer_bundle_vanilla]
boiler_room_bundles_thematic = [blacksmith_bundle_thematic, geologist_bundle_thematic, adventurer_bundle_thematic]
boiler_room_bundles_remixed = [*boiler_room_bundles_thematic, treasure_hunter_bundle, engineer_bundle,
                               demolition_bundle, recycling_bundle, archaeologist_bundle, paleontologist_bundle]
boiler_room_vanilla = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_vanilla, 3)
boiler_room_thematic = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_thematic, 3)
boiler_room_remixed = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_remixed, 3)

# Bulletin Board
chef_items_vanilla = [maple_syrup, fiddlehead_fern, truffle, poppy, maki_roll, fried_egg]
# More recipes?
chef_items_thematic = [maki_roll, fried_egg, omelet, pizza, hashbrowns, pancakes, bread, tortilla,
                       farmer_s_lunch, survival_burger, dish_o_the_sea, miner_s_treat, roots_platter, salad,
                       cheese_cauliflower, parsnip_soup, fried_mushroom, salmon_dinner, pepper_poppers, spaghetti,
                       sashimi, blueberry_tart, algae_soup, pale_broth, chowder]
chef_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.chef, chef_items_vanilla, 6, 6)
chef_bundle_thematic = BundleTemplate.extend_from(chef_bundle_vanilla, chef_items_thematic)

dye_items_vanilla = [red_mushroom, sea_urchin, sunflower, duck_feather, aquamarine, red_cabbage]
dye_red_items = [cranberries, hot_pepper, radish, rhubarb, spaghetti, strawberry, tomato, tulip, red_mushroom]
dye_orange_items = [poppy, pumpkin, apricot, orange, spice_berry, winter_root]
dye_yellow_items = [corn, parsnip, summer_spangle, sunflower, starfruit]
dye_green_items = [fiddlehead_fern, kale, artichoke, bok_choy, green_bean, cactus_fruit, duck_feather, dinosaur_egg]
dye_blue_items = [blueberry, blue_jazz, blackberry, crystal_fruit, aquamarine]
dye_purple_items = [beet, crocus, eggplant, red_cabbage, sweet_pea, iridium_bar, sea_urchin, amaranth]
dye_items_thematic = [dye_red_items, dye_orange_items, dye_yellow_items, dye_green_items, dye_blue_items, dye_purple_items]
dye_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.dye, dye_items_vanilla, 6, 6)
dye_bundle_thematic = DeepBundleTemplate(CCRoom.bulletin_board, BundleName.dye, dye_items_thematic, 6, 6)

field_research_items_vanilla = [purple_mushroom, nautilus_shell, chub, frozen_geode]
field_research_items_thematic = [*field_research_items_vanilla, geode, magma_geode, omni_geode,
                                 rainbow_shell, amethyst, bream, carp]
field_research_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.field_research, field_research_items_vanilla, 4, 4)
field_research_bundle_thematic = BundleTemplate.extend_from(field_research_bundle_vanilla, field_research_items_thematic)

fodder_items_vanilla = [wheat.as_amount(10), hay.as_amount(10), apple.as_amount(3)]
fodder_items_thematic = [*fodder_items_vanilla, kale.as_amount(3), corn.as_amount(3), green_bean.as_amount(3),
                         potato.as_amount(3), green_algae.as_amount(5), white_algae.as_amount(3)]
fodder_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.fodder, fodder_items_vanilla, 3, 3)
fodder_bundle_thematic = BundleTemplate.extend_from(fodder_bundle_vanilla, fodder_items_thematic)

enchanter_items_vanilla = [oak_resin, wine, rabbit_foot, pomegranate]
enchanter_items_thematic = [*enchanter_items_vanilla, purple_mushroom, solar_essence,
                            super_cucumber, void_essence, fire_quartz, frozen_tear, jade]
enchanter_bundle_vanilla = BundleTemplate(CCRoom.bulletin_board, BundleName.enchanter, enchanter_items_vanilla, 4, 4)
enchanter_bundle_thematic = BundleTemplate.extend_from(enchanter_bundle_vanilla, enchanter_items_thematic)

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
                pumpkin_soup.as_amount(5), lucky_lunch.as_amount(5)]
calico_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.calico, calico_items, 2, 2)

raccoon_bundle = BundleTemplate(CCRoom.bulletin_board, BundleName.raccoon, raccoon_foraging_items, 4, 4)

bulletin_board_bundles_vanilla = [chef_bundle_vanilla, dye_bundle_vanilla, field_research_bundle_vanilla, fodder_bundle_vanilla, enchanter_bundle_vanilla]
bulletin_board_bundles_thematic = [chef_bundle_thematic, dye_bundle_thematic, field_research_bundle_thematic, fodder_bundle_thematic, enchanter_bundle_thematic]
bulletin_board_bundles_remixed = [*bulletin_board_bundles_thematic, children_bundle, forager_bundle, home_cook_bundle,
                                  helper_bundle, spirit_eve_bundle, winter_star_bundle, bartender_bundle, calico_bundle, raccoon_bundle]
bulletin_board_vanilla = BundleRoomTemplate(CCRoom.bulletin_board, bulletin_board_bundles_vanilla, 5)
bulletin_board_thematic = BundleRoomTemplate(CCRoom.bulletin_board, bulletin_board_bundles_thematic, 5)
bulletin_board_remixed = BundleRoomTemplate(CCRoom.bulletin_board, bulletin_board_bundles_remixed, 5)

missing_bundle_items_vanilla = [wine.as_quality(ArtisanQuality.silver), dinosaur_mayo, prismatic_shard, caviar,
                                ancient_fruit.as_quality_crop(), void_salmon.as_quality(FishQuality.gold)]
missing_bundle_items_thematic = [*missing_bundle_items_vanilla, pale_ale.as_quality(ArtisanQuality.silver), beer.as_quality(ArtisanQuality.silver),
                                 mead.as_quality(ArtisanQuality.silver),
                                 cheese.as_quality(ArtisanQuality.silver), goat_cheese.as_quality(ArtisanQuality.silver), void_mayo, cloth, green_tea,
                                 truffle_oil, diamond,
                                 sweet_gem_berry.as_quality_crop(), starfruit.as_quality_crop(),
                                 tea_leaves.as_amount(5), lava_eel.as_quality(FishQuality.gold), scorpion_carp.as_quality(FishQuality.gold),
                                 blobfish.as_quality(FishQuality.gold)]
missing_bundle_vanilla = BundleTemplate(CCRoom.abandoned_joja_mart, BundleName.missing_bundle, missing_bundle_items_vanilla, 6, 5)
missing_bundle_thematic = BundleTemplate.extend_from(missing_bundle_vanilla, missing_bundle_items_thematic)

abandoned_joja_mart_bundles_vanilla = [missing_bundle_vanilla]
abandoned_joja_mart_bundles_thematic = [missing_bundle_thematic]
abandoned_joja_mart_vanilla = BundleRoomTemplate(CCRoom.abandoned_joja_mart, abandoned_joja_mart_bundles_vanilla, 1)
abandoned_joja_mart_thematic = BundleRoomTemplate(CCRoom.abandoned_joja_mart, abandoned_joja_mart_bundles_thematic, 1)
abandoned_joja_mart_remixed = abandoned_joja_mart_thematic

vault_2500_gold = BundleItem.money_bundle(2500)
vault_5000_gold = BundleItem.money_bundle(5000)
vault_10000_gold = BundleItem.money_bundle(10000)
vault_25000_gold = BundleItem.money_bundle(25000)

vault_2500_bundle = MoneyBundleTemplate(CCRoom.vault, BundleName.money_2500, vault_2500_gold)
vault_5000_bundle = MoneyBundleTemplate(CCRoom.vault, BundleName.money_5000, vault_5000_gold)
vault_10000_bundle = MoneyBundleTemplate(CCRoom.vault, BundleName.money_10000, vault_10000_gold)
vault_25000_bundle = MoneyBundleTemplate(CCRoom.vault, BundleName.money_25000, vault_25000_gold)

vault_gambler_items = BundleItem(Currency.qi_coin, 10000)
vault_gambler_bundle = CurrencyBundleTemplate(CCRoom.vault, BundleName.gambler, vault_gambler_items)

vault_carnival_items = BundleItem(Currency.star_token, 2500, source=BundleItem.Sources.festival)
vault_carnival_bundle = CurrencyBundleTemplate(CCRoom.vault, BundleName.carnival, vault_carnival_items)

vault_walnut_hunter_items = BundleItem(Currency.golden_walnut, 25)
vault_walnut_hunter_bundle = CurrencyBundleTemplate(CCRoom.vault, BundleName.walnut_hunter, vault_walnut_hunter_items)

vault_qi_helper_items = BundleItem(Currency.qi_gem, 25, source=BundleItem.Sources.island)
vault_qi_helper_bundle = CurrencyBundleTemplate(CCRoom.vault, BundleName.qi_helper, vault_qi_helper_items)

vault_bundles_vanilla = [vault_2500_bundle, vault_5000_bundle, vault_10000_bundle, vault_25000_bundle]
vault_bundles_thematic = vault_bundles_vanilla
vault_bundles_remixed = [*vault_bundles_vanilla, vault_gambler_bundle, vault_qi_helper_bundle, vault_carnival_bundle]  # , vault_walnut_hunter_bundle
vault_vanilla = BundleRoomTemplate(CCRoom.vault, vault_bundles_vanilla, 4)
vault_thematic = BundleRoomTemplate(CCRoom.vault, vault_bundles_thematic, 4)
vault_remixed = BundleRoomTemplate(CCRoom.vault, vault_bundles_remixed, 4)

all_cc_remixed_bundles = [*crafts_room_bundles_remixed, *pantry_bundles_remixed, *fish_tank_bundles_remixed,
                          *boiler_room_bundles_remixed, *bulletin_board_bundles_remixed]
community_center_remixed_anywhere = BundleRoomTemplate("Community Center", all_cc_remixed_bundles, 26)

all_bundle_items_except_money = []
all_remixed_bundles = [*crafts_room_bundles_remixed, *pantry_bundles_remixed, *fish_tank_bundles_remixed,
                       *boiler_room_bundles_remixed, *bulletin_board_bundles_remixed, missing_bundle_thematic,
                       *raccoon_bundles_remixed]
for bundle in all_remixed_bundles:
    all_bundle_items_except_money.extend(bundle.items)

all_bundle_items_by_name = {item.item_name: item for item in all_bundle_items_except_money}
