from . import fish_data
from .museum_data import Mineral
from ..bundles.bundle_item import BundleItem, IslandBundleItem
from ..strings.animal_product_names import AnimalProduct
from ..strings.artisan_good_names import ArtisanGood
from ..strings.crop_names import Fruit, Vegetable
from ..strings.fish_names import Fish, WaterItem, Trash
from ..strings.flower_names import Flower
from ..strings.food_names import Beverage, Meal
from ..strings.forageable_names import Forageable
from ..strings.geode_names import Geode
from ..strings.gift_names import Gift
from ..strings.material_names import Material
from ..strings.metal_names import MetalBar, Artifact, Fossil
from ..strings.monster_drop_names import Loot
from ..strings.seed_names import Seed

wild_horseradish = BundleItem(Forageable.wild_horseradish)
daffodil = BundleItem(Forageable.daffodil)
leek = BundleItem(Forageable.leek)
dandelion = BundleItem(Forageable.dandelion)
morel = BundleItem(Forageable.morel)
common_mushroom = BundleItem(Forageable.common_mushroom)
salmonberry = BundleItem(Forageable.salmonberry)
spring_onion = BundleItem(Forageable.spring_onion)

grape = BundleItem(Fruit.grape)
spice_berry = BundleItem(Forageable.spice_berry)
sweet_pea = BundleItem(Forageable.sweet_pea)
red_mushroom = BundleItem(Forageable.red_mushroom)
fiddlehead_fern = BundleItem(Forageable.fiddlehead_fern)

wild_plum = BundleItem(Forageable.wild_plum)
hazelnut = BundleItem(Forageable.hazelnut)
blackberry = BundleItem(Forageable.blackberry)
chanterelle = BundleItem(Forageable.chanterelle)

winter_root = BundleItem(Forageable.winter_root)
crystal_fruit = BundleItem(Forageable.crystal_fruit)
snow_yam = BundleItem(Forageable.snow_yam)
crocus = BundleItem(Forageable.crocus)
holly = BundleItem(Forageable.holly)

coconut = BundleItem(Forageable.coconut)
cactus_fruit = BundleItem(Forageable.cactus_fruit)
cave_carrot = BundleItem(Forageable.cave_carrot)
purple_mushroom = BundleItem(Forageable.purple_mushroom)
maple_syrup = BundleItem(ArtisanGood.maple_syrup)
oak_resin = BundleItem(ArtisanGood.oak_resin)
pine_tar = BundleItem(ArtisanGood.pine_tar)
nautilus_shell = BundleItem(WaterItem.nautilus_shell)
coral = BundleItem(WaterItem.coral)
sea_urchin = BundleItem(WaterItem.sea_urchin)
rainbow_shell = BundleItem(Forageable.rainbow_shell)
clam = BundleItem(fish_data.clam)
cockle = BundleItem(fish_data.cockle)
mussel = BundleItem(fish_data.mussel)
oyster = BundleItem(fish_data.oyster)
seaweed = BundleItem(WaterItem.seaweed)

wood = BundleItem(Material.wood, 99)
stone = BundleItem(Material.stone, 99)
hardwood = BundleItem(Material.hardwood, 10)
clay = BundleItem(Material.clay, 10)
fiber = BundleItem(Material.fiber, 99)

blue_jazz = BundleItem(Flower.blue_jazz)
cauliflower = BundleItem(Vegetable.cauliflower)
green_bean = BundleItem(Vegetable.green_bean)
kale = BundleItem(Vegetable.kale)
parsnip = BundleItem(Vegetable.parsnip)
potato = BundleItem(Vegetable.potato)
strawberry = BundleItem(Fruit.strawberry)
tulip = BundleItem(Flower.tulip)
unmilled_rice = BundleItem(Vegetable.unmilled_rice)
coffee_bean = BundleItem(Seed.coffee)
garlic = BundleItem(Vegetable.garlic)
blueberry = BundleItem(Fruit.blueberry)
corn = BundleItem(Vegetable.corn)
hops = BundleItem(Vegetable.hops)
hot_pepper = BundleItem(Fruit.hot_pepper)
melon = BundleItem(Fruit.melon)
poppy = BundleItem(Flower.poppy)
radish = BundleItem(Vegetable.radish)
summer_spangle = BundleItem(Flower.summer_spangle)
sunflower = BundleItem(Flower.sunflower)
tomato = BundleItem(Vegetable.tomato)
wheat = BundleItem(Vegetable.wheat)
hay = BundleItem(Forageable.hay)
amaranth = BundleItem(Vegetable.amaranth)
bok_choy = BundleItem(Vegetable.bok_choy)
cranberries = BundleItem(Fruit.cranberries)
eggplant = BundleItem(Vegetable.eggplant)
fairy_rose = BundleItem(Flower.fairy_rose)
pumpkin = BundleItem(Vegetable.pumpkin)
yam = BundleItem(Vegetable.yam)
sweet_gem_berry = BundleItem(Fruit.sweet_gem_berry)
rhubarb = BundleItem(Fruit.rhubarb)
beet = BundleItem(Vegetable.beet)
red_cabbage = BundleItem(Vegetable.red_cabbage)
starfruit = BundleItem(Fruit.starfruit)
artichoke = BundleItem(Vegetable.artichoke)

egg = BundleItem(AnimalProduct.egg)
large_egg = BundleItem(AnimalProduct.large_egg)
brown_egg = BundleItem(AnimalProduct.brown_egg)
large_brown_egg = BundleItem(AnimalProduct.large_brown_egg)
wool = BundleItem(AnimalProduct.wool)
milk = BundleItem(AnimalProduct.milk)
large_milk = BundleItem(AnimalProduct.large_milk)
goat_milk = BundleItem(AnimalProduct.goat_milk)
large_goat_milk = BundleItem(AnimalProduct.large_goat_milk)
truffle = BundleItem(AnimalProduct.truffle)
duck_feather = BundleItem(AnimalProduct.duck_feather)
duck_egg = BundleItem(AnimalProduct.duck_egg)
rabbit_foot = BundleItem(AnimalProduct.rabbit_foot)

truffle_oil = BundleItem(ArtisanGood.truffle_oil)
cloth = BundleItem(ArtisanGood.cloth)
goat_cheese = BundleItem(ArtisanGood.goat_cheese)
cheese = BundleItem(ArtisanGood.cheese)
honey = BundleItem(ArtisanGood.honey)
beer = BundleItem(Beverage.beer)
juice = BundleItem(ArtisanGood.juice)
mead = BundleItem(ArtisanGood.mead)
pale_ale = BundleItem(ArtisanGood.pale_ale)
wine = BundleItem(ArtisanGood.wine)
jelly = BundleItem(ArtisanGood.jelly)
pickles = BundleItem(ArtisanGood.pickles)
caviar = BundleItem(ArtisanGood.caviar)
aged_roe = BundleItem(ArtisanGood.aged_roe)
coffee = BundleItem(Beverage.coffee)
green_tea = BundleItem(ArtisanGood.green_tea)
apple = BundleItem(Fruit.apple)
apricot = BundleItem(Fruit.apricot)
orange = BundleItem(Fruit.orange)
peach = BundleItem(Fruit.peach)
pomegranate = BundleItem(Fruit.pomegranate)
cherry = BundleItem(Fruit.cherry)
lobster = BundleItem(fish_data.lobster)
crab = BundleItem(fish_data.crab)
shrimp = BundleItem(fish_data.shrimp)
crayfish = BundleItem(fish_data.crayfish)
snail = BundleItem(fish_data.snail)
periwinkle = BundleItem(fish_data.periwinkle)
trash = BundleItem(Trash.trash)
driftwood = BundleItem(Trash.driftwood)
soggy_newspaper = BundleItem(Trash.soggy_newspaper)
broken_cd = BundleItem(Trash.broken_cd)
broken_glasses = BundleItem(Trash.broken_glasses)

chub = BundleItem(fish_data.chub)
catfish = BundleItem(fish_data.catfish)
rainbow_trout = BundleItem(fish_data.rainbow_trout)
lingcod = BundleItem(fish_data.lingcod)
walleye = BundleItem(fish_data.walleye)
perch = BundleItem(fish_data.perch)
pike = BundleItem(fish_data.pike)
bream = BundleItem(fish_data.bream)
salmon = BundleItem(fish_data.salmon)
sunfish = BundleItem(fish_data.sunfish)
tiger_trout = BundleItem(fish_data.tiger_trout)
shad = BundleItem(fish_data.shad)
smallmouth_bass = BundleItem(fish_data.smallmouth_bass)
dorado = BundleItem(fish_data.dorado)
carp = BundleItem(fish_data.carp)
midnight_carp = BundleItem(fish_data.midnight_carp)
largemouth_bass = BundleItem(fish_data.largemouth_bass)
sturgeon = BundleItem(fish_data.sturgeon)
bullhead = BundleItem(fish_data.bullhead)
tilapia = BundleItem(fish_data.tilapia)
pufferfish = BundleItem(fish_data.pufferfish)
tuna = BundleItem(fish_data.tuna)
super_cucumber = BundleItem(fish_data.super_cucumber)
flounder = BundleItem(fish_data.flounder)
anchovy = BundleItem(fish_data.anchovy)
sardine = BundleItem(fish_data.sardine)
red_mullet = BundleItem(fish_data.red_mullet)
herring = BundleItem(fish_data.herring)
eel = BundleItem(fish_data.eel)
octopus = BundleItem(fish_data.octopus)
red_snapper = BundleItem(fish_data.red_snapper)
squid = BundleItem(fish_data.squid)
sea_cucumber = BundleItem(fish_data.sea_cucumber)
albacore = BundleItem(fish_data.albacore)
halibut = BundleItem(fish_data.halibut)
scorpion_carp = BundleItem(fish_data.scorpion_carp)
sandfish = BundleItem(fish_data.sandfish)
woodskip = BundleItem(fish_data.woodskip)
lava_eel = BundleItem(fish_data.lava_eel)
ice_pip = BundleItem(fish_data.ice_pip)
stonefish = BundleItem(fish_data.stonefish)
ghostfish = BundleItem(fish_data.ghostfish)

wilted_bouquet = BundleItem(Gift.wilted_bouquet)
copper_bar = BundleItem(MetalBar.copper)
iron_Bar = BundleItem(MetalBar.iron)
gold_bar = BundleItem(MetalBar.gold)
iridium_bar = BundleItem(MetalBar.iridium)
refined_quartz = BundleItem(MetalBar.quartz)
coal = BundleItem(Material.coal, 5)

quartz = BundleItem(Mineral.quartz)
fire_quartz = BundleItem(Mineral.fire_quartz)
frozen_tear = BundleItem(Mineral.frozen_tear)
earth_crystal = BundleItem(Mineral.earth_crystal)
emerald = BundleItem(Mineral.emerald)
aquamarine = BundleItem(Mineral.aquamarine)
ruby = BundleItem(Mineral.ruby)
amethyst = BundleItem(Mineral.amethyst)
topaz = BundleItem(Mineral.topaz)
jade = BundleItem(Mineral.jade)

slime = BundleItem(Loot.slime, 99)
bug_meat = BundleItem(Loot.bug_meat, 10)
bat_wing = BundleItem(Loot.bat_wing, 10)
solar_essence = BundleItem(Loot.solar_essence)
void_essence = BundleItem(Loot.void_essence)

maki_roll = BundleItem(Meal.maki_roll)
fried_egg = BundleItem(Meal.fried_egg)
omelet = BundleItem(Meal.omelet)
pizza = BundleItem(Meal.pizza)
hashbrowns = BundleItem(Meal.hashbrowns)
pancakes = BundleItem(Meal.pancakes)
bread = BundleItem(Meal.bread)
tortilla = BundleItem(Meal.tortilla)
triple_shot_espresso = BundleItem(Beverage.triple_shot_espresso)
farmer_s_lunch = BundleItem(Meal.farmer_lunch)
survival_burger = BundleItem(Meal.survival_burger)
dish_o_the_sea = BundleItem(Meal.dish_o_the_sea)
miner_s_treat = BundleItem(Meal.miners_treat)
roots_platter = BundleItem(Meal.roots_platter)
salad = BundleItem(Meal.salad)
cheese_cauliflower = BundleItem(Meal.cheese_cauliflower)
parsnip_soup = BundleItem(Meal.parsnip_soup)
fried_mushroom = BundleItem(Meal.fried_mushroom)
salmon_dinner = BundleItem(Meal.salmon_dinner)
pepper_poppers = BundleItem(Meal.pepper_poppers)
spaghetti = BundleItem(Meal.spaghetti)
sashimi = BundleItem(Meal.sashimi)
blueberry_tart = BundleItem(Meal.blueberry_tart)
algae_soup = BundleItem(Meal.algae_soup)
pale_broth = BundleItem(Meal.pale_broth)
chowder = BundleItem(Meal.chowder)
green_algae = BundleItem(WaterItem.green_algae)
white_algae = BundleItem(WaterItem.white_algae)
geode = BundleItem(Geode.geode)
frozen_geode = BundleItem(Geode.frozen)
magma_geode = BundleItem(Geode.magma)
omni_geode = BundleItem(Geode.omni)
sap = BundleItem(Material.sap)

dwarf_scroll_1 = BundleItem(Artifact.dwarf_scroll_i)
dwarf_scroll_2 = BundleItem(Artifact.dwarf_scroll_ii)
dwarf_scroll_3 = BundleItem(Artifact.dwarf_scroll_iii)
dwarf_scroll_4 = BundleItem(Artifact.dwarf_scroll_iv)
elvish_jewelry = BundleItem(Artifact.elvish_jewelry)
ancient_drum = BundleItem(Artifact.ancient_drum)
dried_starfish = BundleItem(Fossil.dried_starfish)

dinosaur_mayo = BundleItem(ArtisanGood.dinosaur_mayonnaise)
void_mayo = BundleItem(ArtisanGood.void_mayonnaise)
prismatic_shard = BundleItem(Mineral.prismatic_shard)
diamond = BundleItem(Mineral.diamond)
ancient_fruit = BundleItem(Fruit.ancient_fruit)
void_salmon = BundleItem(Fish.void_salmon)
tea_leaves = BundleItem(Vegetable.tea_leaves)
blobfish = BundleItem(Fish.blobfish)

ginger = IslandBundleItem(Forageable.ginger)
magma_cap = IslandBundleItem(Forageable.magma_cap)

spring_foraging_items_vanilla = [wild_horseradish, daffodil, leek, dandelion]
spring_foraging_items_thematic = [*spring_foraging_items_vanilla, spring_onion, salmonberry, morel]
spring_foraging_bundle_vanilla = Bundle()

summer_foraging_items_vanilla = [grape, spice_berry, sweet_pea]
summer_foraging_items_thematic = [*summer_foraging_items_vanilla, fiddlehead_fern, red_mushroom, rainbow_shell]

fall_foraging_items_vanilla = [common_mushroom, wild_plum, hazelnut, blackberry]
fall_foraging_items_thematic = [*fall_foraging_items_vanilla, chanterelle]

winter_foraging_items_vanilla = [winter_root, crystal_fruit, snow_yam, crocus]
winter_foraging_items_thematic = [*winter_foraging_items_vanilla, holly, nautilus_shell]

construction_items_vanilla = [wood, stone, hardwood]
construction_items_thematic = [*construction_items_vanilla, clay, fiber, sap.as_amount(50)]

exotic_foraging_items_vanilla = [coconut, cactus_fruit, cave_carrot, red_mushroom, purple_mushroom, maple_syrup, oak_resin, pine_tar, morel]
exotic_foraging_items_thematic = [*exotic_foraging_items_vanilla, coral, sea_urchin, clam, cockle, mussel, oyster, seaweed]

beach_foraging_items = [nautilus_shell, coral, sea_urchin, rainbow_shell, clam, cockle, mussel, oyster, seaweed]
mines_foraging_items = [quartz, earth_crystal, frozen_tear, fire_quartz, red_mushroom, purple_mushroom, cave_carrot]
desert_foraging_items = [cactus_fruit.as_gold_quality(), cactus_fruit.as_amount(5), coconut.as_gold_quality(), coconut.as_amount(5)]
island_foraging_items = [ginger.as_amount(5), magma_cap.as_gold_quality(), magma_cap.as_amount(5)]
sticky_items = [sap.as_amount(500), sap.as_amount(500)]
wild_medicine_items = [item.as_amount(5) for item in [purple_mushroom, fiddlehead_fern, white_algae, hops, blackberry, dandelion]]
quality_foraging_items = sorted({item.as_gold_quality().as_amount(1)
                                 for item in
                                 [*spring_foraging_items_thematic, *summer_foraging_items_thematic, *fall_foraging_items_thematic,
                                  *winter_foraging_items_thematic, *beach_foraging_items, *desert_foraging_items, *island_foraging_items]})

spring_crop_items_vanilla = [parsnip, green_bean, cauliflower, potato]
spring_crop_items_thematic = [*spring_crop_items_vanilla, blue_jazz, coffee_bean, garlic, kale, rhubarb, strawberry, tulip, unmilled_rice]

summer_crops_items_vanilla = [tomato, hot_pepper, blueberry, melon]
summer_crops_items_thematic = [*summer_crops_items_vanilla, corn, hops, poppy, radish, red_cabbage, starfruit, summer_spangle, sunflower, wheat]

fall_crops_items_vanilla = [corn, eggplant, pumpkin, yam]
fall_crops_items_thematic = [*fall_crops_items_vanilla, amaranth, artichoke, beet, bok_choy, cranberries, fairy_rose, grape, sunflower, wheat, sweet_gem_berry]

all_crops_items = sorted({*spring_crop_items_thematic, *summer_crops_items_thematic, *fall_crops_items_thematic})

quality_crops_items_vanilla = [item.as_quality_crop() for item in [parsnip, melon, pumpkin, corn]]
quality_crops_items_thematic = [item.as_quality_crop() for item in all_crops_items]

animal_product_items_vanilla = [large_milk, large_brown_egg, large_egg, large_goat_milk, wool, duck_egg]
animal_product_items_thematic = [*animal_product_items_vanilla, egg, brown_egg, milk, goat_milk, truffle, duck_feather, rabbit_foot, dinosaur_egg, void_egg, golden_egg]

artisan_goods_items_vanilla = [truffle_oil, cloth, goat_cheese, cheese, honey, jelly, apple, apricot, orange, peach, pomegranate, cherry]
artisan_goods_items_thematic = [*artisan_goods_items_vanilla, beer, juice, mead, pale_ale, wine, pickles, caviar, aged_roe, coffee, green_tea, banana, mango]

# Where to put Tea Leaves and Fiber?
rare_crops_items = [ancient_fruit, sweet_gem_berry]
fish_farmer_items = [row.as_amount(15), aged_roe.as_amount(15), squid_ink]
garden_items = [tulip, blue_jazz, summer_spangle, sunflower, fairy_rose]
brewer_items = [mead, pale_ale, wine, juice, green_tea]
orchard_items = [apple, apricot, orange, peach, pomegranate, cherry, banana, mango]
island_crops_items = [pineapple, taro_root, banana, mango]


river_fish_items_vanilla = [sunfish, catfish, shad, tiger_trout]
river_fish_items_thematic = [*river_fish_items_vanilla, chub, rainbow_trout, lingcod, walleye, perch, pike, bream, salmon, smallmouth_bass, dorado]

lake_fish_items_vanilla = [largemouth_bass, carp, bullhead, sturgeon]
lake_fish_items_thematic = [*lake_fish_items_vanilla, chub, rainbow_trout, lingcod, walleye, perch, midnight_carp]

ocean_fish_items_vanilla = [sardine, tuna, red_snapper, tilapia]
ocean_fish_items_thematic = [*ocean_fish_items_vanilla, pufferfish, super_cucumber, flounder, anchovy, red_mullet, herring, eel, octopus, squid, sea_cucumber, albacore, halibut]

night_fish_items_vanilla = [walleye, bream, eel]
night_fish_items_thematic = [*night_fish_items_vanilla, super_cucumber, squid, midnight_carp]

specialty_fish_items_vanilla = [pufferfish, ghostfish, sandfish, woodskip]
specialty_fish_items_thematic = [*specialty_fish_items_vanilla, scorpion_carp, eel, octopus, lava_eel, ice_pip, stonefish, void_salmon, stingray, spookfish, midnight_squid]

crab_pot_items_vanilla = [lobster, crayfish, crab, cockle, mussel, shrimp, snail, periwinkle, oyster, clam]
crab_pot_items_thematic = [*crab_pot_items_vanilla, trash, driftwood, soggy_newspaper, broken_cd, broken_glasses]

quality_fish_items = sorted({item.as_gold_quality() for item in [*river_fish_items_thematic, *lake_fish_items_thematic, *ocean_fish_items_thematic]})
master_fisher_items = [lava_eel, scorpion_carp, octopus, blobfish, lingcod, ice_pip, super_cucumber, stingray, void_salmon, pufferfish]
legendary_fish_items = [angler, legend, mutant carp, crimsonfish, glacierfish]


blacksmith_items_vanilla = [copper_bar, iron_Bar, gold_bar]
blacksmith_items_thematic = [*blacksmith_items_vanilla, iridium_bar, refined_quartz.as_amount(3), wilted_bouquet]

geologist_items_vanilla = [quartz, earth_crystal, frozen_tear, fire_quartz]
geologist_items_thematic = [*geologist_items_vanilla, emerald, aquamarine, ruby, amethyst, topaz, jade, diamond]

adventurer_items_vanilla = [slime, bat_wing, solar_essence, void_essence]
adventurer_items_thematic = [*adventurer_items_vanilla, bug_meat, coal, bone_fragment.as_amount(10)]

# Where to put radioactive bar?
treasure_hunter_items = [emerald, aquamarine, ruby, amethyst, topaz, jade, diamond]
engineer_items = [iridium_ore.as_amount(5), battery_pack, refined_quartz.as_amount(5), diamond]

chef_items_vanilla = [maple_syrup, fiddlehead_fern, truffle, poppy, maki_roll, fried_egg]
# More recipes?
chef_items_thematic = [maki_roll, fried_egg, omelet, pizza, hashbrowns, pancakes, bread, tortilla,
              farmer_s_lunch, survival_burger, dish_o_the_sea, miner_s_treat, roots_platter, salad,
              cheese_cauliflower, parsnip_soup, fried_mushroom, salmon_dinner, pepper_poppers, spaghetti,
              sashimi, blueberry_tart, algae_soup, pale_broth, chowder]

dye_items_vanilla = [red_mushroom, sea_urchin, sunflower, duck_feather, aquamarine, red_cabbage]
dye_red_items = [cranberries, hot_pepper, radish, rhubarb, spaghetti, strawberry, tomato, tulip]
dye_orange_items = [poppy, pumpkin, apricot, orange, spice_berry, winter_root]
dye_yellow_items = [corn, parsnip, summer_spangle, sunflower]
dye_green_items = [fiddlehead_fern, kale, artichoke, bok_choy, green_bean]
dye_blue_items = [blueberry, blue_jazz, blackberry, crystal_fruit]
dye_purple_items = [beet, crocus, eggplant, red_cabbage, sweet_pea]
dye_items_thematic = [dye_red_items, dye_orange_items, dye_yellow_items, dye_green_items, dye_blue_items, dye_purple_items]

field_research_items_vanilla = [purple_mushroom, nautilus_shell, chub, frozen_geode]
field_research_items_thematic = [*field_research_items_vanilla, geode, magma_geode, omni_geode,
                        rainbow_shell, amethyst, bream, carp]

fodder_items_vanilla = [wheat.as_amount(10), hay.as_amount(10), apple.as_amount(3)]
fodder_items_thematic = [*fodder_items_vanilla, kale.as_amount(3), corn.as_amount(3), green_bean.as_amount(3),
                         potato.as_amount(3), green_algae.as_amount(5), white_algae.as_amount(3)]

enchanter_items_vanilla = [oak_resin, wine, rabbit_foot, pomegranate]
enchanter_items_thematic = [*enchanter_items_vanilla, purple_mushroom, solar_essence,
                   super_cucumber, void_essence, fire_quartz, frozen_tear, jade]

children_items = [salmonberry.as_amount(10), cookie, ancient_doll, ice_cream, cranberry_candy, ginger_ale,
                  grape.as_amount(10), pink_cake, snail, fairy_rose, plum_pudding]
forager_items = [salmonberry.as_amount(50), blackberry.as_amount(50), wild_plum.as_amount(20), snow_yam.as_amount(20),
                 common_mushroom.as_amount(20), grape.as_amount(20), spring_onion.as_amount(20)]
home_cook_items = [egg.as_amount(10), milk.as_amount(10), wheat_flour.as_amount(100), sugar.as_amount(100), vinegar.as_amount(100),
                   chocolate_cake, pancakes, rhubarb_pie]


missing_bundle_items = [wine.as_silver_quality(), pale_ale.as_silver_quality(), beer.as_silver_quality(), mead.as_silver_quality(), cheese.as_silver_quality(),
                        goat_cheese.as_silver_quality(), dinosaur_mayo, void_mayo, cloth, green_tea, truffle_oil, caviar, prismatic_shard, diamond,
                        ancient_fruit.as_gold_quality().as_amount(5), sweet_gem_berry.as_gold_quality().as_amount(5), starfruit.as_gold_quality().as_amount(5),
                        tea_leaves.as_amount(5),
                        void_salmon.as_gold_quality(), lava_eel.as_gold_quality(), scorpion_carp.as_gold_quality(), blobfish.as_gold_quality()]

# Make thematic with other currencies
vault_2500_items = [BundleItem.money_bundle(2500)]
vault_5000_items = [BundleItem.money_bundle(5000)]
vault_10000_items = [BundleItem.money_bundle(10000)]
vault_25000_items = [BundleItem.money_bundle(25000)]

crafts_room_bundle_items = [
    *spring_foraging_items,
    *summer_foraging_items,
    *fall_foraging_items,
    *winter_foraging_items,
    *exotic_foraging_items,
    *construction_items,
]

pantry_bundle_items = sorted({
    *spring_crop_items,
    *summer_crops_items,
    *fall_crops_items,
    *quality_crops_items,
    *animal_product_items,
    *artisan_goods_items,
})

fish_tank_bundle_items = sorted({
    *river_fish_items,
    *lake_fish_items,
    *ocean_fish_items,
    *night_fish_items,
    *crab_pot_items,
    *specialty_fish_items,
})

boiler_room_bundle_items = sorted({
    *blacksmith_items,
    *geologist_items,
    *adventurer_items,
})

bulletin_board_bundle_items = sorted({
    *chef_items,
    *[item for dye_color_items in dye_items for item in dye_color_items],
    *field_research_items,
    *fodder_items,
    *enchanter_items
})

vault_bundle_items = [
    *vault_2500_items,
    *vault_5000_items,
    *vault_10000_items,
    *vault_25000_items,
]

all_bundle_items_except_money = sorted({
    *crafts_room_bundle_items,
    *pantry_bundle_items,
    *fish_tank_bundle_items,
    *boiler_room_bundle_items,
    *bulletin_board_bundle_items,
    *missing_bundle_items,
}, key=lambda x: x.item.name)

all_bundle_items = sorted({
    *crafts_room_bundle_items,
    *pantry_bundle_items,
    *fish_tank_bundle_items,
    *boiler_room_bundle_items,
    *bulletin_board_bundle_items,
    *vault_bundle_items,
    *missing_bundle_items,
}, key=lambda x: x.item.name)

all_bundle_items_by_name = {item.item.name: item for item in all_bundle_items}
all_bundle_items_by_id = {item.item.item_id: item for item in all_bundle_items}
