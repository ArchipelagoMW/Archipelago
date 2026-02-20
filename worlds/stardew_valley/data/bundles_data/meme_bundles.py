from .bundle_data import all_bundle_items_by_name
from .meme_bundles_data.capitalist_bundle import capitalist_items
from .remixed_bundles import *
from ...bundles.bundle import BureaucracyBundleTemplate, RecursiveBundleTemplate, FixedPriceCurrencyBundleTemplate, \
    FixedPriceBundleTemplate, FixedPriceDeepBundleTemplate, FixedMultiplierBundleTemplate, FixedSlotsBundleTemplate
from ...strings.bundle_names import MemeBundleName
from ...strings.currency_names import MemeCurrency
from ...strings.flower_names import all_flowers
from ...strings.machine_names import Machine
from ...strings.meme_item_names import MemeItem
from ...strings.quality_names import AnimalProductQuality, CropQuality

burger_king_items = [survival_burger, joja_cola, apple_slices, ice_cream, strange_doll, strange_doll_green, hashbrowns, infinity_crown]
burger_king_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.burger_king, burger_king_items, 6, 3)

capitalist_bundle = FixedMultiplierBundleTemplate(CCRoom.vault, MemeBundleName.capitalist, capitalist_items, 12, 2)

romance_items = [lucky_purple_shorts, truffle_oil, super_cucumber, good_ol_cap]
romance_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.romance, romance_items, 4, 4)

hurricane_tortilla_items = [tortilla.as_amount(4)]
hurricane_tortilla_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.hurricane_tortilla, hurricane_tortilla_items, 6, 6)

AAAA_items = [battery_pack.as_amount(12), battery_pack.as_amount(8), battery_pack.as_amount(6)]
AAAA_bundle = BundleTemplate(CCRoom.crafts_room, MemeBundleName.AAAA, AAAA_items, 3, 3)

anything_for_beyonce_items = [beet]
anything_for_beyonce_bundle = BundleTemplate(CCRoom.crafts_room, MemeBundleName.anything_for_beyonce, anything_for_beyonce_items, 1, 1)

crab_rave_items = [crab.as_amount(8)]
crab_rave_bundle = BundleTemplate(CCRoom.fish_tank, MemeBundleName.crab_rave, crab_rave_items, 12, 8)

potato_items = [potato.as_amount(8)]
potato_bundle = BundleTemplate(CCRoom.crafts_room, MemeBundleName.potato, potato_items, 12, 8)

look_at_chickens_items = [duck_egg.as_amount(2)]
look_at_chickens_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.look_at_chickens, look_at_chickens_items, 10, 4)

lemonade_stand_items = [grape]
lemonade_stand_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.lemonade_stand, lemonade_stand_items, 3, 1)

what_the_rock_is_cooking_items = [stone.as_amount(1), cookout_kit, strange_bun]
what_the_rock_is_cooking_bundle = FixedPriceBundleTemplate(CCRoom.pantry, MemeBundleName.what_the_rock_is_cooking, what_the_rock_is_cooking_items, 3, 3)

amons_fall_items = [stone.as_amount(1)]
amons_fall_bundle = FixedPriceBundleTemplate(CCRoom.boiler_room, MemeBundleName.amons_fall, amons_fall_items, 7, 7)

screw_you_items = [tea_set, ostrich_egg.as_quality(AnimalProductQuality.iridium), snake_vertebrae.as_amount(5), mummified_bat.as_amount(5)]
screw_you_bundle = BundleTemplate(CCRoom.boiler_room, MemeBundleName.screw_you, screw_you_items, 4, 4)

sunmaid_items = [raisins.as_amount(28)]
sunmaid_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.sunmaid, sunmaid_items, 1, 1)

rick_items = [pickles]
rick_bundle = FixedPriceBundleTemplate(CCRoom.boiler_room, MemeBundleName.rick, rick_items, 1, 1)

minecraft_items = [coal, copper_ore, iron_ore, quartz, amethyst, emerald, gold_ore, diamond, obsidian]
minecraft_bundle = BundleTemplate(CCRoom.boiler_room, MemeBundleName.minecraft, minecraft_items, 9, 8)

balls_items = [blue_jazz, cauliflower, blueberry, melon, red_cabbage, tomato, powdermelon, cranberries, fairy_rose, grape, pumpkin, ancient_fruit,
               solar_essence, cherry_bomb, bomb, mega_bomb, coal, iridium_ore, aquamarine, jamborite, geode, magma_geode, ancient_seed, crystal_ball,
               amethyst_crystal_ball, aquamarine_crystal_ball, emerald_crystal_ball, ruby_crystal_ball, topaz_crystal_ball, apple, pizza, explosive_ammo, peach,
               orange, apricot, tigerseye, coconut, gold_ore, golden_coconut, pufferfish, lucky_lunch, salad, cactus_fruit, radioactive_ore, opal, broken_cd,
               void_essence, wild_plum, pomegranate]
balls_items = [item.as_amount(1) for item in balls_items]
balls_bundle = BundleTemplate(CCRoom.boiler_room, MemeBundleName.balls, balls_items, 12, 6)

tilesanity_items = [wood_floor.as_amount(100), rustic_plank_floor.as_amount(100), straw_floor.as_amount(100), weathered_floor.as_amount(100),
                    crystal_floor.as_amount(100), stone_floor.as_amount(100), stone_walkway_floor.as_amount(100), brick_floor.as_amount(100),
                    wood_path.as_amount(100), gravel_path.as_amount(100), cobblestone_path.as_amount(100), stepping_stone_path.as_amount(100),
                    crystal_path.as_amount(100)]
tilesanity_bundle = BundleTemplate(CCRoom.boiler_room, MemeBundleName.tilesanity, tilesanity_items, 4, 4)

cap_items = [vacation_shirt, wood.as_amount(999), sap.as_amount(999), pine_cone.as_amount(100), acorn.as_amount(100),
             maple_seed.as_amount(100), moss.as_amount(500), exotic_double_bed.as_amount(1)]
cap_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.cap, cap_items, 8, 4)

big_grapes_items = [coconut]
big_grapes_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.big_grapes, big_grapes_items, 4, 4)

obelisks_items = [earth_crystal.as_amount(10), clam.as_amount(10), coral.as_amount(10), coconut.as_amount(10), cactus_fruit.as_amount(10),
                  banana.as_amount(10), dragon_tooth.as_amount(10), iridium_bar.as_amount(45)]
obelisks_bundle = FixedPriceBundleTemplate(CCRoom.boiler_room, MemeBundleName.obelisks, obelisks_items, 8, 8)

burger_king_revenge_items = [fossilized_tail, void_salmon, ostrich_egg.as_amount(3), tea_leaves.as_amount(10), purple_slime_egg,
                             moss_soup.as_amount(3), radioactive_ore.as_amount(5), mystic_syrup.as_amount(10), truffle, aged_crimsonfish_roe]
burger_king_revenge_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.burger_king_revenge, burger_king_revenge_items, 8, 8)

trout_items = [golden_tag.as_amount(10), golden_tag.as_amount(20), golden_tag.as_amount(30)]
trout_bundle = BundleTemplate(CCRoom.fish_tank, MemeBundleName.trout, trout_items, 1, 1)

eg_items = [egg, brown_egg, large_egg, large_brown_egg, duck_egg, void_egg, golden_egg, dinosaur_egg, fried_egg, ostrich_egg,
            thunder_egg, calico_egg, green_slime_egg, blue_slime_egg, purple_slime_egg, tiger_slime_egg, roe, aged_roe]
eg_items = [item.as_amount(57) for item in eg_items]
eg_bundle = FixedPriceBundleTemplate(CCRoom.pantry, MemeBundleName.eg, eg_items, 8, 2)

doctor_angler_items = [fish.as_quality(FishQuality.iridium) for fish in legendary_fish_items]
doctor_angler_bundle = BundleTemplate(CCRoom.fish_tank, MemeBundleName.doctor_angler, doctor_angler_items, 5, 5)

smapi_items = [camping_stove, decorative_pot, slime_crate, supply_crate, warp_totem_qis_arena,
               artifact_spot, twig, weeds, lumber, green_rain_weeds_0, seed_spot, pot_of_gold]
smapi_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.smapi, smapi_items, 4, 4)

chaos_emerald_items = [diamond, emerald, ruby, limestone, obsidian, kyanite, lemon_stone]
chaos_emerald_bundle = FixedPriceBundleTemplate(CCRoom.crafts_room, MemeBundleName.chaos_emerald, chaos_emerald_items, 7, 7)

not_the_bees_items = [BundleItem(ArtisanGood.specific_honey(flower)) for flower in all_flowers]
not_the_bees_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.not_the_bees, not_the_bees_items, 4, 4)

sappy_items = [golden_pumpkin, magic_rock_candy, pearl, prismatic_shard, rabbit_foot, stardrop_tea]
sappy_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.sappy, sappy_items, 4, 4)

honorable_items = [stone.as_amount(1), prismatic_shard.as_amount(1)]
honorable_bundle = FixedPriceBundleTemplate(CCRoom.boiler_room, MemeBundleName.honorable, honorable_items, 2, 1)

caffeinated_items = [coffee_bean.as_amount(500)]
caffeinated_bundle = BundleTemplate(CCRoom.crafts_room, MemeBundleName.caffeinated, caffeinated_items, 1, 1)

hats_off_to_you_items = [living_hat, garbage_hat, golden_helmet, laurel_wreath_crown, joja_cap,
                         deluxe_pirate_hat, dark_cowboy_hat, tiger_hat, mystery_hat, dark_ballcap]
hats_off_to_you_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.hats_off_to_you, hats_off_to_you_items, 8, 2)

speedrunners_items = [parsnip, wine, cheese, sea_urchin, lucky_purple_shorts, mayonnaise]
speedrunners_bundle = FixedPriceBundleTemplate(CCRoom.pantry, MemeBundleName.speedrunners, speedrunners_items, 6, 6)

snitch_items = [lucky_purple_shorts]
snitch_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.snitch, snitch_items, 1, 1)

mermaid_items = [pearl, clam.as_amount(2), mermaid_pendant, mermaid_boots, flute_block.as_amount(5)]
mermaid_bundle = FixedPriceBundleTemplate(CCRoom.fish_tank, MemeBundleName.mermaid, mermaid_items, 5, 5)

commitment_items = [bouquet, mermaid_pendant, wilted_bouquet, ancient_doll.as_amount(2)]
commitment_bundle_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.commitment, commitment_items, 4, 4)

all_simple_items = [all_bundle_items_by_name[bundle_item_name] for bundle_item_name in all_bundle_items_by_name if
                    all_bundle_items_by_name[bundle_item_name].amount == 1 and
                    all_bundle_items_by_name[bundle_item_name].quality.startswith("Basic") and
                    all_bundle_items_by_name[bundle_item_name].flavor is None and
                    bundle_item_name != "Honey"]

permit_a38_items = [*all_simple_items]
permit_a38_bundle = BureaucracyBundleTemplate(CCRoom.vault, MemeBundleName.permit_a38, permit_a38_items, 1, 8)

journalist_items = [*all_simple_items]
journalist_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.journalist, journalist_items, 1, 1)

trap_items = [BundleItem(MemeItem.trap)]
trap_bundle = FixedSlotsBundleTemplate(CCRoom.bulletin_board, MemeBundleName.trap, trap_items, 4, 4)

off_your_back_items = [BundleItem(MemeItem.worn_hat), BundleItem(MemeItem.worn_shirt), BundleItem(MemeItem.worn_pants),
                       BundleItem(MemeItem.worn_boots), BundleItem(MemeItem.worn_left_ring), BundleItem(MemeItem.worn_right_ring)]
off_your_back_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.off_your_back, off_your_back_items, 6, 6)

sisyphus_items = [stone.as_amount(1)]
sisyphus_bundle = FixedPriceBundleTemplate(CCRoom.boiler_room, MemeBundleName.sisyphus, sisyphus_items, 12, 12)

vocaloid_items = [spring_onion, orange, banana, tuna, wine, ice_cream, carrot, bread, eggplant]
vocaloid_items = [item.as_amount(10) for item in vocaloid_items]
vocaloid_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.vocaloid, vocaloid_items, 6, 6)

legendairy_items = [legend, legend_roe, legend_bait, smoked_legend, aged_legend_roe,
                    milk.as_amount(10), cheese.as_amount(10), goat_milk.as_amount(10), goat_cheese.as_amount(10)]
legendairy_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.legendairy, legendairy_items, 6, 4)

kent_c_items = [broken_glasses.as_amount(5), refined_quartz.as_amount(10)]
kent_c_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.kent_c, kent_c_items, 2, 2)

fruit_items = [tomato, pumpkin, summer_squash, eggplant, hot_pepper]
fruit_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.fruit, fruit_items, 5, 5)

reverse_items = [*all_simple_items]
reverse_bundle = FixedSlotsBundleTemplate(CCRoom.crafts_room, MemeBundleName.reverse, reverse_items, 4, 4)

bundle_items = [*all_simple_items]
bundle_bundle = RecursiveBundleTemplate(CCRoom.fish_tank, MemeBundleName.bundle, bundle_items, 16, 16, 4)

bun_dle_items = [strange_bun, bread, tortilla, rabbit_foot]
bun_dle_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.bun_dle, bun_dle_items, 4, 4)

celeste_items = [strawberry.as_amount(175), strawberry_seeds.as_amount(4), strawberry.as_quality(CropQuality.gold).as_amount(26)]
celeste_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.celeste, celeste_items, 3, 3)

automation_items = [copper_bar.as_amount(15), iron_bar.as_amount(36), iron_bar.as_amount(20), copper_bar.as_amount(10)]
automation_bundle = FixedPriceBundleTemplate(CCRoom.boiler_room, MemeBundleName.automation, automation_items, 4, 4)

animal_well_items = [rare_disc, bone_flute, ruby_crystal_ball, cherry_bomb.as_amount(1), candle_lamp, modern_lamp, advanced_tv_remote]
animal_well_bundle = FixedPriceBundleTemplate(CCRoom.pantry, MemeBundleName.animal_well, animal_well_items, 7, 7)

schrodinger_items = [*all_simple_items]
schrodinger_bundle = FixedPriceBundleTemplate(CCRoom.fish_tank, MemeBundleName.schrodinger, schrodinger_items, 2, 1)

ikea_craftables = [Machine.mayonnaise_machine, Machine.bee_house, Machine.preserves_jar, Machine.cheese_press, Machine.keg, Machine.fish_smoker,
                   Machine.crystalarium, Machine.worm_bin, Furniture.tub_o_flowers]
ikea_items = [BundleItem(craftable) for craftable in ikea_craftables]
ikea_bundle = FixedPriceBundleTemplate(CCRoom.crafts_room, MemeBundleName.ikea, ikea_items, 1, 1)

this_is_fine_items = [coffee, fire_quartz, fire_quartz, fire_quartz, fire_quartz, fire_quartz, fire_quartz, fire_quartz]
this_is_fine_bundle = FixedPriceBundleTemplate(CCRoom.crafts_room, MemeBundleName.this_is_fine, this_is_fine_items, 8, 8)

crap_pot_items = [clay, mudstone, truffle, sunflower_seeds, roasted_hazelnuts, plum_pudding, rotten_plant, taro_root]
crap_pot_bundle = BundleTemplate(CCRoom.boiler_room, MemeBundleName.crap_pot, crap_pot_items, 4, 4)

emmalution_items = [garlic, bread, trash, goblin_mask, rain_totem]
emmalution_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.emmalution, emmalution_items, 5, 5)

unused_balls = [fairy_rose, melon, grape, geode, ancient_seed, crystal_ball, peach]
yellow_pool_balls = [item.as_amount(1) for item in [solar_essence, topaz_crystal_ball, pizza, apricot, gold_ore, golden_coconut, pufferfish, lucky_lunch]]
blue_pool_balls = [item.as_amount(2) for item in [blue_jazz, blueberry, powdermelon, ancient_fruit, iridium_ore, aquamarine, opal, broken_cd]]
red_pool_balls = [item.as_amount(3) for item in [tomato, mega_bomb, magma_geode, apple, explosive_ammo, cranberries, cherry_bomb]]
purple_pool_balls = [item.as_amount(4) for item in [red_cabbage, pomegranate, void_essence, wild_plum]]
orange_pool_balls = [item.as_amount(5) for item in [pumpkin, orange, tigerseye]]
green_pool_balls = [item.as_amount(6) for item in [cauliflower, jamborite, salad, cactus_fruit, radioactive_ore]]
brown_pool_balls = [item.as_amount(7) for item in [acorn, coconut, hazelnut, maple_bar, maple_syrup, potato, truffle, yam]]
black_pool_balls = [item.as_amount(8) for item in [bomb, coal, void_egg]]
pool_items = [yellow_pool_balls, blue_pool_balls, red_pool_balls, purple_pool_balls, orange_pool_balls, green_pool_balls, brown_pool_balls, black_pool_balls]
pool_bundle = FixedPriceDeepBundleTemplate(CCRoom.boiler_room, MemeBundleName.pool, pool_items, 8, 8)

argonmatrix_items = [radish.as_amount(32), radish.as_amount(87), melon.as_amount(127), chocolate_cake.as_amount(3), cactus_fruit.as_amount(1)]
argonmatrix_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.argonmatrix, argonmatrix_items, 5, 5)

frazzleduck_items = [duck_egg, duck_feather, eggplant, green_jacket_shirt]
frazzleduck_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.frazzleduck, frazzleduck_items, 4, 4)

loser_club_items = [tuna]
loser_club_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.loser_club, loser_club_items, 1, 1)

ministry_items = [item.as_amount(999) for item in [trash, joja_cola, broken_glasses, broken_cd, soggy_newspaper]]
ministry_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.ministry_of_madness, ministry_items, 4, 1)

pomnut_items = [pomegranate, hazelnut, carrot]
pomnut_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.pomnut, pomnut_items, 3, 3)

blossom_garden_items = [banana.as_amount(18), pizza.as_amount(32), spaghetti, single_bed, pink_cake, wood_floor, triple_shot_espresso, maple_bar, bug_steak, void_essence.as_amount(10), crystal_ball, solar_essence.as_amount(10)]
blossom_garden_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.blossom_garden, blossom_garden_items, 12, 6)

cooperation_items = [*all_simple_items]
cooperation_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.cooperation, cooperation_items, 4, 4)

doctor_items = [apple.as_amount(365)]
doctor_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.doctor, doctor_items, 1, 1)

very_sticky_items = [sap.as_amount(125), sap.as_amount(125), sap.as_amount(125), sap.as_amount(125)]
very_sticky_bundle = FixedPriceBundleTemplate(CCRoom.crafts_room, MemeBundleName.very_sticky, very_sticky_items, 4, 4)

square_hole_items = [*all_simple_items]
square_hole_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.square_hole, square_hole_items, 6, 6)

distracted_items = [*all_simple_items] # (If you bring more than one item for it, the rest get sent home)
distracted_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.distracted, distracted_items, 4, 4)

algorerhythm_items =[item.as_amount(2) for item in
                     [midnight_squid_roe, tea_set, statue_of_endless_fortune, golden_bobber, dried_qi_fruit, cursed_mannequin,
                      statue_of_blessings, crane_house_plant, book_of_mysteries, far_away_stone, void_ghost_pendant, trimmed_purple_shorts]]
algorerhythm_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.algorerhythm, algorerhythm_items, 12, 4)


red_fish_items = [red_mullet, red_snapper, lava_eel, crimsonfish]
blue_fish_items = [anchovy, tuna, sardine, bream, squid, ice_pip, albacore, blue_discus, midnight_squid, spook_fish, glacierfish]
other_fish = [pufferfish, largemouth_bass, smallmouth_bass, rainbow_trout, walleye, perch, carp, catfish, pike, sunfish, herring, eel, octopus, sea_cucumber,
              super_cucumber, ghostfish, stonefish, sandfish, scorpion_carp, flounder, midnight_carp, tigerseye, bullhead, tilapia, chub, dorado, shad,
              lingcod, halibut, slimejack, stingray, goby, blobfish, angler, legend, mutant_carp]
dr_seuss_items = [other_fish, [fish.as_amount(2) for fish in other_fish], red_fish_items, blue_fish_items]
dr_seuss_bundle = FixedPriceDeepBundleTemplate(CCRoom.crafts_room, MemeBundleName.dr_seuss, dr_seuss_items, 4, 4)

pollution_items = [trash, broken_cd, broken_glasses, joja_cola, soggy_newspaper, battery_pack]
pollution_bundle = BundleTemplate(CCRoom.fish_tank, MemeBundleName.pollution, pollution_items, 4, 4)

all_fish_item_names = sorted(list(set([item.item_name for item in [*spring_fish_items, *summer_fish_items, *fall_fish_items, *winter_fish_items]])))
all_fish_items = [BundleItem(item).as_amount(1).as_quality(FishQuality.basic) for item in all_fish_item_names]
catch_and_release_items = [*all_fish_items]
catch_and_release_bundle = BundleTemplate(CCRoom.fish_tank, MemeBundleName.catch_and_release, catch_and_release_items, 4, 4)

vampire_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.vampire, BundleItem(MemeCurrency.blood, 200))
exhaustion_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.exhaustion, BundleItem(MemeCurrency.energy, 400))
tick_tock_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.tick_tock, BundleItem(MemeCurrency.time, 1440))
archipela_go_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.archipela_go, BundleItem(MemeCurrency.steps, 20000))
clique_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.clique, BundleItem(MemeCurrency.clic, 1))
cookie_clicker_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.cookie_clicker, BundleItem(MemeCurrency.cookies, 200000))
communism_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.communism, BundleItem.money_bundle(1))
death_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.death, death)
flashbang_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.flashbang, BundleItem.money_bundle(0))
connection_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.connection, BundleItem.money_bundle(0))
reconnection_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.reconnection, BundleItem.money_bundle(0))
nft_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.nft, BundleItem.money_bundle(0))
firstborn_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.firstborn, BundleItem(MemeCurrency.child, 1))
restraint_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.restraint, BundleItem.money_bundle(0))
fast_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.fast, BundleItem(MemeCurrency.time_elapsed, 1000))
floor_is_lava_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.floor_is_lava, BundleItem.money_bundle(0))
joetg_bundle = CurrencyBundleTemplate(CCRoom.bulletin_board, MemeBundleName.joetg, BundleItem(MemeCurrency.dead_pumpkins, 750))
bad_farmer_bundle = CurrencyBundleTemplate(CCRoom.pantry, MemeBundleName.bad_farmer, BundleItem(MemeCurrency.dead_crops, 400))
bad_fisherman_bundle = CurrencyBundleTemplate(CCRoom.fish_tank, MemeBundleName.bad_fisherman, BundleItem(MemeCurrency.missed_fish, 20))
honeywell_bundle = CurrencyBundleTemplate(CCRoom.bulletin_board, MemeBundleName.honeywell, BundleItem(MemeCurrency.honeywell, 1))
gacha_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.gacha, BundleItem.money_bundle(10000))
hibernation_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.hibernation, BundleItem(MemeCurrency.sleep_days, 60))
crowdfunding_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.crowdfunding, BundleItem(MemeCurrency.bank_money, 10000))
clickbait_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.clickbait, BundleItem.money_bundle(100))
puzzle_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.puzzle, BundleItem.money_bundle(10))
asmr_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.asmr, BundleItem.money_bundle(0))
humble_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.humble, BundleItem.money_bundle(5000))
deathlink_bundle = CurrencyBundleTemplate(CCRoom.boiler_room, MemeBundleName.deathlink, BundleItem(MemeCurrency.deathlinks, 10))
investment_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.scam, BundleItem.money_bundle(10000))
stanley_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.stanley, BundleItem.money_bundle(9999999))
hairy_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.hairy, BundleItem.money_bundle(0))
# colored_crystals_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.boiler_room, MemeBundleName.colored_crystals, BundleItem.money_bundle(10))
hint_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.bulletin_board, MemeBundleName.hint, BundleItem.money_bundle(10))
sacrifice_bundle = CurrencyBundleTemplate(CCRoom.boiler_room, MemeBundleName.sacrifice, BundleItem(MemeCurrency.goat, 1))

# Stopped at 49 responses on the form

# Todo Bundles
#   Acrostic Bundle     (Asks for a specific word, you need to donate an item for each letter)
#   Bubbles Bundle
#   Cipher Bundle       (Some sort of code?)
#   DLC Bundle
#   Doom Bundle
#   Dragonball Bundle
#   Empty Bundle (donate empty inventory spot)
#   Friendship Bundle   (Show some NPCs, gotta donate a loved gift for each of them)
#   GeoGessr Bundle
#   Ghost Bundle (it ghosts you)
#   Joja/Morris Bundle
#   Leaf Blower Bundle  (Leaf Blower Minigame, similar to the cookie clicker one)
#   Lingo Bundle
#   Lost Axe Bundle (Donate your axe then talk to Robin)
#   Maguffin Bundle (Ap items)
#   Millibelle Bundle (money, run away, find at spa)
#   Minesweeper bundle (donate bombs on correct spots)
#   Pico-8 Bundle
#   Pollution Bundle
#   QA Bundle           (Some sort of bug, not sure yet)
#   Relay Bundle        (Relay Stick passed around the multiworld)
#   Robin's Lost Axe Bundle (Give your axe, then Robin brings it back to you)
#   Scavenger Bundle    (The bundle moves around the map and you need to keep finding it)
#   Side Quest Bundle   (Sends you on side quests to talk to random NPCs several times)
#   Therapy Bundle
#   Torrent Bundle (someone must seed it for you)
#   Witness Bundle
#   Change Cap Bundle to forgetting something at home



# Bundles that need special Mod Handling:
#     None

pantry_bundles_meme = [hurricane_tortilla_bundle, look_at_chickens_bundle, lemonade_stand_bundle, what_the_rock_is_cooking_bundle, sunmaid_bundle,
                       big_grapes_bundle, eg_bundle, not_the_bees_bundle, speedrunners_bundle, bun_dle_bundle, animal_well_bundle, bad_farmer_bundle]
pantry_meme = BundleRoomTemplate(CCRoom.pantry, pantry_bundles_meme, 6)

crafts_room_bundles_meme = [AAAA_bundle, anything_for_beyonce_bundle, potato_bundle, chaos_emerald_bundle, caffeinated_bundle, reverse_bundle,
                            ikea_bundle, this_is_fine_bundle, very_sticky_bundle, dr_seuss_bundle]
crafts_room_meme = BundleRoomTemplate(CCRoom.crafts_room, crafts_room_bundles_meme, 6)

fish_tank_bundles_meme = [crab_rave_bundle, trout_bundle, doctor_angler_bundle, mermaid_bundle, legendairy_bundle, kent_c_bundle, bundle_bundle,
                          schrodinger_bundle, bad_fisherman_bundle, pollution_bundle, catch_and_release_bundle]
fish_tank_meme = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_meme, 6)

boiler_room_bundles_meme = [amons_fall_bundle, screw_you_bundle, rick_bundle, minecraft_bundle, balls_bundle, tilesanity_bundle, obelisks_bundle,
                            honorable_bundle, sisyphus_bundle, automation_bundle, crap_pot_bundle, deathlink_bundle, pool_bundle, # colored_crystals_bundle,
                            sacrifice_bundle]
boiler_room_meme = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_meme, 3)

bulletin_board_bundles_meme = [burger_king_bundle, romance_bundle, burger_king_revenge_bundle, smapi_bundle, sappy_bundle, hats_off_to_you_bundle,
                               snitch_bundle, commitment_bundle_bundle, journalist_bundle, trap_bundle, off_your_back_bundle, vocaloid_bundle, fruit_bundle,
                               celeste_bundle, cap_bundle, emmalution_bundle, joetg_bundle, honeywell_bundle, cooperation_bundle, square_hole_bundle,
                               ministry_bundle, loser_club_bundle, frazzleduck_bundle, argonmatrix_bundle, pomnut_bundle, blossom_garden_bundle, doctor_bundle,
                               hint_bundle, algorerhythm_bundle, distracted_bundle]
bulletin_board_meme = BundleRoomTemplate(CCRoom.bulletin_board, bulletin_board_bundles_meme, 5)

vault_bundles_meme = [capitalist_bundle, death_bundle, permit_a38_bundle, vampire_bundle, exhaustion_bundle,
                      tick_tock_bundle, archipela_go_bundle, clique_bundle, cookie_clicker_bundle, communism_bundle,
                      flashbang_bundle, connection_bundle, reconnection_bundle, nft_bundle, firstborn_bundle, restraint_bundle, fast_bundle,
                      floor_is_lava_bundle, gacha_bundle, hibernation_bundle, crowdfunding_bundle, clickbait_bundle,
                      humble_bundle, puzzle_bundle, asmr_bundle, investment_bundle, stanley_bundle, hairy_bundle]
vault_meme = BundleRoomTemplate(CCRoom.vault, vault_bundles_meme, 4)

all_cc_meme_bundles = [*pantry_bundles_meme, *crafts_room_bundles_meme, *fish_tank_bundles_meme,
                       *boiler_room_bundles_meme, *bulletin_board_bundles_meme, *vault_bundles_meme]
community_center_meme_bundles = BundleRoomTemplate("Community Center", all_cc_meme_bundles, 30)
