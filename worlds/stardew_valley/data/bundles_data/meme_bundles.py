from .bundle_data import all_bundle_items_by_name
from .meme_bundles_data.capitalist_bundle import capitalist_items
from .remixed_bundles import *
from ...bundles.bundle import BureaucracyBundleTemplate, RecursiveBundleTemplate, FixedPriceCurrencyBundleTemplate, \
    FixedPriceBundleTemplate
from ...strings.bundle_names import MemeBundleName
from ...strings.currency_names import MemeCurrency
from ...strings.flower_names import all_flowers
from ...strings.machine_names import Machine
from ...strings.meme_item_names import MemeItem
from ...strings.quality_names import AnimalProductQuality, CropQuality

burger_king_items = [survival_burger, joja_cola, apple_slices, ice_cream, strange_doll, strange_doll_green, hashbrowns, infinity_crown]
burger_king_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.burger_king, burger_king_items, 6, 3)

capitalist_bundle = BundleTemplate(CCRoom.vault, MemeBundleName.capitalist, capitalist_items, 12, 2)

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
sunmaid_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.sunmaid, sunmaid_items, 2, 2)

rick_items = [pickles]
rick_bundle = FixedPriceBundleTemplate(CCRoom.boiler_room, MemeBundleName.rick, rick_items, 1, 1)

minecraft_items = [coal.as_amount(1), copper_ore, iron_ore, quartz, amethyst, emerald, gold_ore, diamond, obsidian]
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

cap_items = [wood.as_amount(999), sap.as_amount(999), pine_cone.as_amount(100), acorn.as_amount(100), maple_seed.as_amount(100), moss.as_amount(500)]
cap_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.cap, cap_items, 6, 4)

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

chaos_emerald_items = [diamond, emerald, ruby, ghost_crystal, obsidian, kyanite, lemon_stone]
chaos_emerald_bundle = FixedPriceBundleTemplate(CCRoom.crafts_room, MemeBundleName.chaos_emerald, chaos_emerald_items, 7, 7)

not_the_bees_items = [BundleItem(ArtisanGood.specific_honey(flower)) for flower in all_flowers]
not_the_bees_bundle = BundleTemplate(CCRoom.pantry, MemeBundleName.not_the_bees, not_the_bees_items, 4, 4)

sappy_items = [golden_pumpkin, magic_rock_candy, pearl, prismatic_shard, rabbit_foot, stardrop_tea]
sappy_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.sappy, sappy_items, 4, 4)

honorable_items = [stone.as_amount(1), prismatic_shard.as_amount(10)]
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

all_simple_items = [bundle_item for bundle_item in all_bundle_items_by_name.values() if
                    bundle_item.amount == 1 and bundle_item.quality.startswith("Basic") and bundle_item.flavor is None]

permit_a38_items = [*all_simple_items]
permit_a38_bundle = BureaucracyBundleTemplate(CCRoom.vault, MemeBundleName.permit_a38, permit_a38_items, 1, 8)

journalist_items = [*all_simple_items]
journalist_bundle = FixedPriceBundleTemplate(CCRoom.bulletin_board, MemeBundleName.journalist, journalist_items, 1, 1)

trap_items = [BundleItem(MemeItem.trap)]
trap_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.trap, trap_items, 5, 5)

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
reverse_bundle = BundleTemplate(CCRoom.crafts_room, MemeBundleName.reverse, reverse_items, 4, 4)

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
schrodinger_bundle = FixedPriceBundleTemplate(CCRoom.fish_tank, MemeBundleName.schrodinger, schrodinger_items, 2, 2)

ikea_craftables = [Machine.mayonnaise_machine, Machine.bee_house, Machine.preserves_jar, Machine.cheese_press, Machine.keg, Machine.fish_smoker,
                   Machine.crystalarium, Machine.worm_bin, Furniture.tub_o_flowers]
ikea_items = [BundleItem(craftable) for craftable in ikea_craftables]
ikea_bundle = FixedPriceBundleTemplate(CCRoom.crafts_room, MemeBundleName.ikea, ikea_items, 1, 1)

this_is_fine_items = [coffee, fire_quartz, fire_quartz, fire_quartz, fire_quartz, fire_quartz, fire_quartz, fire_quartz]
this_is_fine_bundle = FixedPriceBundleTemplate(CCRoom.crafts_room, MemeBundleName.this_is_fine, this_is_fine_items, 8, 8)

shitty_items = [clay, mudstone, truffle, sunflower_seeds, roasted_hazelnuts, plum_pudding, rotten_plant, taro_root]
shitty_bundle = BundleTemplate(CCRoom.boiler_room, MemeBundleName.shitty, shitty_items, 4, 4)

emmalution_items = [garlic, bread, trash, goblin_mask, rain_totem]
emmalution_bundle = BundleTemplate(CCRoom.bulletin_board, MemeBundleName.emmalution, emmalution_items, 5, 5)

vampire_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.vampire, BundleItem(MemeCurrency.blood, 200))
exhaustion_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.exhaustion, BundleItem(MemeCurrency.energy, 400))
tick_tock_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.tick_tock, BundleItem(MemeCurrency.time, 1440))
archipela_go_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.archipela_go, BundleItem(MemeCurrency.steps, 5000))
clique_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.clique, BundleItem(MemeCurrency.clic, 1))
# cipher_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.cipher, BundleItem(MemeCurrency.code, 4))
cookie_clicker_bundle = CurrencyBundleTemplate(CCRoom.vault, MemeBundleName.cookie_clicker, BundleItem(MemeCurrency.cookies, 20000))  # ?
communist_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.communist, BundleItem.money_bundle(1))
death_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.death, death)
flashbang_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.flashbang, BundleItem.money_bundle(0))
connection_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.connection, BundleItem.money_bundle(0))
nft_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.nft, BundleItem.money_bundle(0))
firstborn_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.firstborn, BundleItem(MemeCurrency.child, 1))
restraint_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.restraint, BundleItem.money_bundle(0))
fast_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.fast, BundleItem.money_bundle(0))
floor_is_lava_bundle = FixedPriceCurrencyBundleTemplate(CCRoom.vault, MemeBundleName.floor_is_lava, BundleItem.money_bundle(0))
joetg_bundle = CurrencyBundleTemplate(CCRoom.bulletin_board, MemeBundleName.joetg, BundleItem(MemeCurrency.dead_pumpkins, 750))

# Stopped at 49 responses on the form

# Todo Bundles
#   Side Quest Bundle   (Sends you on side quests to talk to random NPCs several times)
#   Acrostic Bundle     (Asks for a specific word, you need to donate an item for each letter)
#   Cooperation Bundle  (Asks for normal items but can only be donated through gifting)
#   Clickbait Bundle    (Scouts a super critical progression item, but actually contains garbage)
#   ASMR Bundle         (Relaxing Bundle, it plays ASMR noise)
#   Gacha Bundle        (Open lootboxes until you get a T5 reward)
#   QA Bundle           (Some sort of bug, not sure yet)
#   Bad Farmer Bundle   (Dead Crops)
#   Humble Bundle       (Pay what you want, 3 rewards (useful, filler, trap). Other two are auto-checked when finishing the CC)
#   Crowdfunding Bundle (Purchase with Bank Money)
#   Relay Bundle        (Relay Stick passed around the multiworld)
#   Leaf Blower Bundle  (Leaf Blower Minigame, similar to the cookie clicker one)
#   Scavenger Bundle    (The bundle moves around the map and you need to keep finding it)
#   Sticky Bundle       (But it sticks, somehow?)


# Bundles that need special Mod Handling:
# Exhaustion Bundle
# Clique Bundle
# Cipher Bundle
# Communist Bundle
# Death Bundle (1 Death)

# Trap Bundle (Start filled with traps, have to take them out)
# Journalist Bundle (Accept literally anything)
# Mermaid song bundle (1-5-4-2-3)
# Commitment Bundle (Need to have doved and divorced)
# Bundle Bundle

pantry_bundles_meme = [hurricane_tortilla_bundle, look_at_chickens_bundle, lemonade_stand_bundle, what_the_rock_is_cooking_bundle, sunmaid_bundle,
                       big_grapes_bundle, eg_bundle, not_the_bees_bundle, speedrunners_bundle, bun_dle_bundle, animal_well_bundle]
pantry_meme = BundleRoomTemplate(CCRoom.pantry, pantry_bundles_meme, 6)

crafts_room_bundles_meme = [AAAA_bundle, anything_for_beyonce_bundle, potato_bundle, chaos_emerald_bundle, caffeinated_bundle, reverse_bundle,
                            ikea_bundle, this_is_fine_bundle]
crafts_room_meme = BundleRoomTemplate(CCRoom.crafts_room, crafts_room_bundles_meme, 6)

fish_tank_bundles_meme = [crab_rave_bundle, trout_bundle, doctor_angler_bundle, mermaid_bundle, legendairy_bundle, kent_c_bundle, bundle_bundle,
                          schrodinger_bundle]
fish_tank_meme = BundleRoomTemplate(CCRoom.fish_tank, fish_tank_bundles_meme, 6)

boiler_room_bundles_meme = [amons_fall_bundle, screw_you_bundle, rick_bundle, minecraft_bundle, balls_bundle, tilesanity_bundle, obelisks_bundle,
                            honorable_bundle, sisyphus_bundle, automation_bundle, shitty_bundle]
boiler_room_meme = BundleRoomTemplate(CCRoom.boiler_room, boiler_room_bundles_meme, 3)

bulletin_board_bundles_meme = [burger_king_bundle, romance_bundle, burger_king_revenge_bundle, smapi_bundle, sappy_bundle, hats_off_to_you_bundle,
                               snitch_bundle, commitment_bundle_bundle, journalist_bundle, trap_bundle, off_your_back_bundle, vocaloid_bundle, fruit_bundle,
                               celeste_bundle, cap_bundle, emmalution_bundle, joetg_bundle]
bulletin_board_meme = BundleRoomTemplate(CCRoom.bulletin_board, bulletin_board_bundles_meme, 5)

vault_bundles_meme = [capitalist_bundle, death_bundle, permit_a38_bundle, vampire_bundle, exhaustion_bundle, tick_tock_bundle, archipela_go_bundle,
                      clique_bundle, cookie_clicker_bundle, communist_bundle, flashbang_bundle, connection_bundle, nft_bundle, firstborn_bundle,
                      restraint_bundle, fast_bundle, floor_is_lava_bundle]  # cipher_bundle
vault_meme = BundleRoomTemplate(CCRoom.vault, vault_bundles_meme, 4)

all_cc_meme_bundles = [*pantry_bundles_meme, *crafts_room_bundles_meme, *fish_tank_bundles_meme,
                       *boiler_room_bundles_meme, *bulletin_board_bundles_meme, *vault_bundles_meme]
community_center_meme_bundles = BundleRoomTemplate("Community Center", all_cc_meme_bundles, 30)
