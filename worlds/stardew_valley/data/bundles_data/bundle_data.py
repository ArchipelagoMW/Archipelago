from .remixed_bundles import *
from ...bundles.bundle import BundleTemplate, DeepBundleTemplate, CurrencyBundleTemplate, MoneyBundleTemplate
from ...bundles.bundle_item import BundleItem
from ...bundles.bundle_room import BundleRoomTemplate
from ...strings.bundle_names import CCRoom, BundleName
from ...strings.currency_names import Currency
from ...strings.quality_names import ArtisanQuality, FishQuality

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
                       *giant_stump_bundles_remixed]
for bundle in all_remixed_bundles:
    all_bundle_items_except_money.extend(bundle.items)

all_bundle_items_by_name = {item.item_name: item for item in all_bundle_items_except_money}
