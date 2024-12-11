from ..bundles.bundle import BundleTemplate, IslandBundleTemplate, DeepBundleTemplate, CurrencyBundleTemplate, MoneyBundleTemplate, FestivalBundleTemplate
from ..bundles.bundle_item import BundleItem
from ..bundles.bundle_room import BundleRoomTemplate
from ..content import content_packs
from ..content.vanilla.base import all_fruits, all_vegetables, all_edible_mushrooms
from ..strings.animal_product_names import AnimalProduct
from ..strings.artisan_good_names import ArtisanGood
from ..strings.bundle_names import CCRoom, BundleName
from ..strings.craftable_names import Fishing, Craftable, Bomb, Consumable, Lighting
from ..strings.crop_names import Fruit, Vegetable
from ..strings.currency_names import Currency
from ..strings.fertilizer_names import Fertilizer, RetainingSoil, SpeedGro
from ..strings.fish_names import Fish, WaterItem, Trash
from ..strings.flower_names import Flower
from ..strings.food_names import Beverage, Meal
from ..strings.forageable_names import Forageable, Mushroom
from ..strings.geode_names import Geode
from ..strings.gift_names import Gift
from ..strings.ingredient_names import Ingredient
from ..strings.material_names import Material
from ..strings.metal_names import MetalBar, Artifact, Fossil, Ore, Mineral
from ..strings.monster_drop_names import Loot
from ..strings.quality_names import ForageQuality, ArtisanQuality, FishQuality
from ..strings.seed_names import Seed, TreeSeed

wild_horseradish = BundleItem(Forageable.wild_horseradish)
daffodil = BundleItem(Forageable.daffodil)
leek = BundleItem(Forageable.leek)
dandelion = BundleItem(Forageable.dandelion)
morel = BundleItem(Mushroom.morel)
common_mushroom = BundleItem(Mushroom.common)
salmonberry = BundleItem(Forageable.salmonberry)
spring_onion = BundleItem(Forageable.spring_onion)

grape = BundleItem(Fruit.grape)
spice_berry = BundleItem(Forageable.spice_berry)
sweet_pea = BundleItem(Forageable.sweet_pea)
red_mushroom = BundleItem(Mushroom.red)
fiddlehead_fern = BundleItem(Forageable.fiddlehead_fern)

wild_plum = BundleItem(Forageable.wild_plum)
hazelnut = BundleItem(Forageable.hazelnut)
blackberry = BundleItem(Forageable.blackberry)
chanterelle = BundleItem(Mushroom.chanterelle)

winter_root = BundleItem(Forageable.winter_root)
crystal_fruit = BundleItem(Forageable.crystal_fruit)
snow_yam = BundleItem(Forageable.snow_yam)
crocus = BundleItem(Forageable.crocus)
holly = BundleItem(Forageable.holly)

coconut = BundleItem(Forageable.coconut)
cactus_fruit = BundleItem(Forageable.cactus_fruit)
cave_carrot = BundleItem(Forageable.cave_carrot)
purple_mushroom = BundleItem(Mushroom.purple)
maple_syrup = BundleItem(ArtisanGood.maple_syrup)
oak_resin = BundleItem(ArtisanGood.oak_resin)
pine_tar = BundleItem(ArtisanGood.pine_tar)
nautilus_shell = BundleItem(WaterItem.nautilus_shell)
coral = BundleItem(WaterItem.coral)
sea_urchin = BundleItem(WaterItem.sea_urchin)
rainbow_shell = BundleItem(Forageable.rainbow_shell)
clam = BundleItem(Fish.clam)
cockle = BundleItem(Fish.cockle)
mussel = BundleItem(Fish.mussel)
oyster = BundleItem(Fish.oyster)
seaweed = BundleItem(WaterItem.seaweed, can_have_quality=False)

wood = BundleItem(Material.wood, 99)
stone = BundleItem(Material.stone, 99)
hardwood = BundleItem(Material.hardwood, 10)
clay = BundleItem(Material.clay, 10)
fiber = BundleItem(Material.fiber, 99)
moss = BundleItem(Material.moss, 10)

mixed_seeds = BundleItem(Seed.mixed)
acorn = BundleItem(TreeSeed.acorn)
maple_seed = BundleItem(TreeSeed.maple)
pine_cone = BundleItem(TreeSeed.pine)
mahogany_seed = BundleItem(TreeSeed.mahogany)
mushroom_tree_seed = BundleItem(TreeSeed.mushroom, source=BundleItem.Sources.island)
mystic_tree_seed = BundleItem(TreeSeed.mystic, source=BundleItem.Sources.masteries)
mossy_seed = BundleItem(TreeSeed.mossy)

strawberry_seeds = BundleItem(Seed.strawberry)

blue_jazz = BundleItem(Flower.blue_jazz)
cauliflower = BundleItem(Vegetable.cauliflower)
green_bean = BundleItem(Vegetable.green_bean)
kale = BundleItem(Vegetable.kale)
parsnip = BundleItem(Vegetable.parsnip)
potato = BundleItem(Vegetable.potato)
strawberry = BundleItem(Fruit.strawberry, source=BundleItem.Sources.festival)
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
pineapple = BundleItem(Fruit.pineapple, source=BundleItem.Sources.content)
taro_root = BundleItem(Vegetable.taro_root, source=BundleItem.Sources.content)

carrot = BundleItem(Vegetable.carrot)
summer_squash = BundleItem(Vegetable.summer_squash)
broccoli = BundleItem(Vegetable.broccoli)
powdermelon = BundleItem(Fruit.powdermelon)

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
dinosaur_egg = BundleItem(AnimalProduct.dinosaur_egg)
void_egg = BundleItem(AnimalProduct.void_egg)
ostrich_egg = BundleItem(AnimalProduct.ostrich_egg, source=BundleItem.Sources.island, )
golden_egg = BundleItem(AnimalProduct.golden_egg)

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
roe = BundleItem(AnimalProduct.roe)
squid_ink = BundleItem(AnimalProduct.squid_ink)
coffee = BundleItem(Beverage.coffee)
green_tea = BundleItem(ArtisanGood.green_tea)
apple = BundleItem(Fruit.apple)
apricot = BundleItem(Fruit.apricot)
orange = BundleItem(Fruit.orange)
peach = BundleItem(Fruit.peach)
pomegranate = BundleItem(Fruit.pomegranate)
cherry = BundleItem(Fruit.cherry)
banana = BundleItem(Fruit.banana, source=BundleItem.Sources.content)
mango = BundleItem(Fruit.mango, source=BundleItem.Sources.content)

basic_fertilizer = BundleItem(Fertilizer.basic, 100)
quality_fertilizer = BundleItem(Fertilizer.quality, 20)
deluxe_fertilizer = BundleItem(Fertilizer.deluxe, 5, source=BundleItem.Sources.island)
basic_retaining_soil = BundleItem(RetainingSoil.basic, 80)
quality_retaining_soil = BundleItem(RetainingSoil.quality, 50)
deluxe_retaining_soil = BundleItem(RetainingSoil.deluxe, 20, source=BundleItem.Sources.island)
speed_gro = BundleItem(SpeedGro.basic, 40)
deluxe_speed_gro = BundleItem(SpeedGro.deluxe, 20)
hyper_speed_gro = BundleItem(SpeedGro.hyper, 5, source=BundleItem.Sources.island)
tree_fertilizer = BundleItem(Fertilizer.tree, 20)

lobster = BundleItem(Fish.lobster)
crab = BundleItem(Fish.crab)
shrimp = BundleItem(Fish.shrimp)
crayfish = BundleItem(Fish.crayfish)
snail = BundleItem(Fish.snail)
periwinkle = BundleItem(Fish.periwinkle)
trash = BundleItem(Trash.trash)
driftwood = BundleItem(Trash.driftwood)
soggy_newspaper = BundleItem(Trash.soggy_newspaper)
broken_cd = BundleItem(Trash.broken_cd)
broken_glasses = BundleItem(Trash.broken_glasses)

chub = BundleItem(Fish.chub)
catfish = BundleItem(Fish.catfish)
rainbow_trout = BundleItem(Fish.rainbow_trout)
lingcod = BundleItem(Fish.lingcod)
walleye = BundleItem(Fish.walleye)
perch = BundleItem(Fish.perch)
pike = BundleItem(Fish.pike)
bream = BundleItem(Fish.bream)
salmon = BundleItem(Fish.salmon)
sunfish = BundleItem(Fish.sunfish)
tiger_trout = BundleItem(Fish.tiger_trout)
shad = BundleItem(Fish.shad)
smallmouth_bass = BundleItem(Fish.smallmouth_bass)
dorado = BundleItem(Fish.dorado)
carp = BundleItem(Fish.carp)
midnight_carp = BundleItem(Fish.midnight_carp)
largemouth_bass = BundleItem(Fish.largemouth_bass)
sturgeon = BundleItem(Fish.sturgeon)
bullhead = BundleItem(Fish.bullhead)
tilapia = BundleItem(Fish.tilapia)
pufferfish = BundleItem(Fish.pufferfish)
tuna = BundleItem(Fish.tuna)
super_cucumber = BundleItem(Fish.super_cucumber)
flounder = BundleItem(Fish.flounder)
anchovy = BundleItem(Fish.anchovy)
sardine = BundleItem(Fish.sardine)
red_mullet = BundleItem(Fish.red_mullet)
herring = BundleItem(Fish.herring)
eel = BundleItem(Fish.eel)
octopus = BundleItem(Fish.octopus)
red_snapper = BundleItem(Fish.red_snapper)
squid = BundleItem(Fish.squid)
sea_cucumber = BundleItem(Fish.sea_cucumber)
albacore = BundleItem(Fish.albacore)
halibut = BundleItem(Fish.halibut)
scorpion_carp = BundleItem(Fish.scorpion_carp)
sandfish = BundleItem(Fish.sandfish)
woodskip = BundleItem(Fish.woodskip)
lava_eel = BundleItem(Fish.lava_eel)
ice_pip = BundleItem(Fish.ice_pip)
stonefish = BundleItem(Fish.stonefish)
ghostfish = BundleItem(Fish.ghostfish)

bouquet = BundleItem(Gift.bouquet)
wilted_bouquet = BundleItem(Gift.wilted_bouquet)
copper_bar = BundleItem(MetalBar.copper)
iron_Bar = BundleItem(MetalBar.iron)
gold_bar = BundleItem(MetalBar.gold)
iridium_bar = BundleItem(MetalBar.iridium)
refined_quartz = BundleItem(MetalBar.quartz)
coal = BundleItem(Material.coal, 5)
iridium_ore = BundleItem(Ore.iridium)
gold_ore = BundleItem(Ore.gold)
iron_ore = BundleItem(Ore.iron)
copper_ore = BundleItem(Ore.copper)
battery_pack = BundleItem(ArtisanGood.battery_pack)

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

petrified_slime = BundleItem(Mineral.petrified_slime)
blue_slime_egg = BundleItem(Loot.blue_slime_egg)
red_slime_egg = BundleItem(Loot.red_slime_egg)
purple_slime_egg = BundleItem(Loot.purple_slime_egg)
green_slime_egg = BundleItem(Loot.green_slime_egg)
tiger_slime_egg = BundleItem(Loot.tiger_slime_egg, source=BundleItem.Sources.island)

cherry_bomb = BundleItem(Bomb.cherry_bomb, 5)
bomb = BundleItem(Bomb.bomb, 2)
mega_bomb = BundleItem(Bomb.mega_bomb)
explosive_ammo = BundleItem(Craftable.explosive_ammo, 5)

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
cookie = BundleItem(Meal.cookie)
ancient_doll = BundleItem(Artifact.ancient_doll)
ice_cream = BundleItem(Meal.ice_cream)
cranberry_candy = BundleItem(Meal.cranberry_candy)
ginger_ale = BundleItem(Beverage.ginger_ale, source=BundleItem.Sources.island)
pink_cake = BundleItem(Meal.pink_cake)
plum_pudding = BundleItem(Meal.plum_pudding)
chocolate_cake = BundleItem(Meal.chocolate_cake)
rhubarb_pie = BundleItem(Meal.rhubarb_pie)
shrimp_cocktail = BundleItem(Meal.shrimp_cocktail)
pina_colada = BundleItem(Beverage.pina_colada, source=BundleItem.Sources.island)
stuffing = BundleItem(Meal.stuffing)
magic_rock_candy = BundleItem(Meal.magic_rock_candy)
spicy_eel = BundleItem(Meal.spicy_eel)
crab_cakes = BundleItem(Meal.crab_cakes)
eggplant_parmesan = BundleItem(Meal.eggplant_parmesan)
pumpkin_soup = BundleItem(Meal.pumpkin_soup)
lucky_lunch = BundleItem(Meal.lucky_lunch)

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
bone_fragment = BundleItem(Fossil.bone_fragment)

golden_mask = BundleItem(Artifact.golden_mask)
golden_relic = BundleItem(Artifact.golden_relic)
dwarf_gadget = BundleItem(Artifact.dwarf_gadget)
dwarvish_helm = BundleItem(Artifact.dwarvish_helm)
prehistoric_handaxe = BundleItem(Artifact.prehistoric_handaxe)
bone_flute = BundleItem(Artifact.bone_flute)
anchor = BundleItem(Artifact.anchor)
prehistoric_tool = BundleItem(Artifact.prehistoric_tool)
chicken_statue = BundleItem(Artifact.chicken_statue)
rusty_cog = BundleItem(Artifact.rusty_cog)
rusty_spur = BundleItem(Artifact.rusty_spur)
rusty_spoon = BundleItem(Artifact.rusty_spoon)
ancient_sword = BundleItem(Artifact.ancient_sword)
ornamental_fan = BundleItem(Artifact.ornamental_fan)
chipped_amphora = BundleItem(Artifact.chipped_amphora)

prehistoric_scapula = BundleItem(Fossil.prehistoric_scapula)
prehistoric_tibia = BundleItem(Fossil.prehistoric_tibia)
prehistoric_skull = BundleItem(Fossil.prehistoric_skull)
skeletal_hand = BundleItem(Fossil.skeletal_hand)
prehistoric_rib = BundleItem(Fossil.prehistoric_rib)
prehistoric_vertebra = BundleItem(Fossil.prehistoric_vertebra)
skeletal_tail = BundleItem(Fossil.skeletal_tail)
nautilus_fossil = BundleItem(Fossil.nautilus_fossil)
amphibian_fossil = BundleItem(Fossil.amphibian_fossil)
palm_fossil = BundleItem(Fossil.palm_fossil)
trilobite = BundleItem(Fossil.trilobite)

dinosaur_mayo = BundleItem(ArtisanGood.dinosaur_mayonnaise)
void_mayo = BundleItem(ArtisanGood.void_mayonnaise)
prismatic_shard = BundleItem(Mineral.prismatic_shard)
diamond = BundleItem(Mineral.diamond)
ancient_fruit = BundleItem(Fruit.ancient_fruit)
void_salmon = BundleItem(Fish.void_salmon)
tea_leaves = BundleItem(Vegetable.tea_leaves)
blobfish = BundleItem(Fish.blobfish)
spook_fish = BundleItem(Fish.spook_fish)
lionfish = BundleItem(Fish.lionfish, source=BundleItem.Sources.island)
blue_discus = BundleItem(Fish.blue_discus, source=BundleItem.Sources.island)
stingray = BundleItem(Fish.stingray, source=BundleItem.Sources.island)
spookfish = BundleItem(Fish.spookfish)
midnight_squid = BundleItem(Fish.midnight_squid)

angler = BundleItem(Fish.angler)
crimsonfish = BundleItem(Fish.crimsonfish)
mutant_carp = BundleItem(Fish.mutant_carp)
glacierfish = BundleItem(Fish.glacierfish)
legend = BundleItem(Fish.legend)

spinner = BundleItem(Fishing.spinner)
dressed_spinner = BundleItem(Fishing.dressed_spinner)
trap_bobber = BundleItem(Fishing.trap_bobber)
sonar_bobber = BundleItem(Fishing.sonar_bobber)
cork_bobber = BundleItem(Fishing.cork_bobber)
lead_bobber = BundleItem(Fishing.lead_bobber)
treasure_hunter = BundleItem(Fishing.treasure_hunter)
barbed_hook = BundleItem(Fishing.barbed_hook)
curiosity_lure = BundleItem(Fishing.curiosity_lure)
quality_bobber = BundleItem(Fishing.quality_bobber)
bait = BundleItem(Fishing.bait, 100)
deluxe_bait = BundleItem(Fishing.deluxe_bait, 50)
magnet = BundleItem(Fishing.magnet)
wild_bait = BundleItem(Fishing.wild_bait, 20)
magic_bait = BundleItem(Fishing.magic_bait, 10, source=BundleItem.Sources.island)
pearl = BundleItem(Gift.pearl)
challenge_bait = BundleItem(Fishing.challenge_bait, 25, source=BundleItem.Sources.masteries)
targeted_bait = BundleItem(ArtisanGood.targeted_bait, 25, source=BundleItem.Sources.content)

ginger = BundleItem(Forageable.ginger, source=BundleItem.Sources.content)
magma_cap = BundleItem(Mushroom.magma_cap, source=BundleItem.Sources.content)

wheat_flour = BundleItem(Ingredient.wheat_flour)
sugar = BundleItem(Ingredient.sugar)
vinegar = BundleItem(Ingredient.vinegar)

jack_o_lantern = BundleItem(Lighting.jack_o_lantern)
prize_ticket = BundleItem(Currency.prize_ticket)
mystery_box = BundleItem(Consumable.mystery_box)
gold_mystery_box = BundleItem(Consumable.gold_mystery_box, source=BundleItem.Sources.masteries)
calico_egg = BundleItem(Currency.calico_egg)

raccoon_crab_pot_fish_items = [periwinkle.as_amount(5), snail.as_amount(5), crayfish.as_amount(5), mussel.as_amount(5),
                               oyster.as_amount(5), cockle.as_amount(5), clam.as_amount(5)]
raccoon_smoked_fish_items = [BundleItem(ArtisanGood.smoked_fish, flavor=fish) for fish in
                             [Fish.largemouth_bass, Fish.bream, Fish.bullhead, Fish.chub, Fish.ghostfish, Fish.flounder, Fish.shad,
                              Fish.rainbow_trout, Fish.tilapia, Fish.red_mullet, Fish.tuna, Fish.midnight_carp, Fish.salmon, Fish.perch]]
raccoon_fish_items_flat = [*raccoon_crab_pot_fish_items, *raccoon_smoked_fish_items]
raccoon_fish_items_deep = [raccoon_crab_pot_fish_items, raccoon_smoked_fish_items]
raccoon_fish_bundle_vanilla = DeepBundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_fish, raccoon_fish_items_deep, 2, 2)
raccoon_fish_bundle_thematic = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_fish, raccoon_fish_items_flat, 3, 2)

all_specific_jellies = [BundleItem(ArtisanGood.jelly, flavor=fruit, source=BundleItem.Sources.content) for fruit in all_fruits]
all_specific_pickles = [BundleItem(ArtisanGood.pickles, flavor=vegetable, source=BundleItem.Sources.content) for vegetable in all_vegetables]
all_specific_dried_fruits = [*[BundleItem(ArtisanGood.dried_fruit, flavor=fruit, source=BundleItem.Sources.content) for fruit in all_fruits],
                             BundleItem(ArtisanGood.raisins, source=BundleItem.Sources.content)]
all_specific_juices = [BundleItem(ArtisanGood.juice, flavor=vegetable, source=BundleItem.Sources.content) for vegetable in all_vegetables]
raccoon_artisan_items = [*all_specific_jellies, *all_specific_pickles, *all_specific_dried_fruits, *all_specific_juices]
raccoon_artisan_bundle_vanilla = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_artisan, raccoon_artisan_items, 2, 2)
raccoon_artisan_bundle_thematic = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_artisan, raccoon_artisan_items, 3, 2)

all_specific_dried_mushrooms = [BundleItem(ArtisanGood.dried_mushroom, flavor=mushroom, source=BundleItem.Sources.content) for mushroom in all_edible_mushrooms]
raccoon_food_items = [egg.as_amount(5), cave_carrot.as_amount(5), white_algae.as_amount(5)]
raccoon_food_items_vanilla = [all_specific_dried_mushrooms, raccoon_food_items]
raccoon_food_items_thematic = [*all_specific_dried_mushrooms, *raccoon_food_items, brown_egg.as_amount(5), large_egg.as_amount(2), large_brown_egg.as_amount(2),
                               green_algae.as_amount(10)]
raccoon_food_bundle_vanilla = DeepBundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_food, raccoon_food_items_vanilla, 2, 2)
raccoon_food_bundle_thematic = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_food, raccoon_food_items_thematic, 3, 2)

raccoon_foraging_items = [moss, rusty_spoon, trash.as_amount(5), slime.as_amount(99), bat_wing.as_amount(10), geode.as_amount(8),
                          frozen_geode.as_amount(5), magma_geode.as_amount(3), coral.as_amount(4), sea_urchin.as_amount(2), bug_meat.as_amount(10),
                          diamond, topaz.as_amount(3), ghostfish.as_amount(3)]
raccoon_foraging_bundle_vanilla = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_foraging, raccoon_foraging_items, 2, 2)
raccoon_foraging_bundle_thematic = BundleTemplate(CCRoom.raccoon_requests, BundleName.raccoon_foraging, raccoon_foraging_items, 3, 2)

raccoon_bundles_vanilla = [raccoon_fish_bundle_vanilla, raccoon_artisan_bundle_vanilla, raccoon_food_bundle_vanilla, raccoon_foraging_bundle_vanilla]
raccoon_bundles_thematic = [raccoon_fish_bundle_thematic, raccoon_artisan_bundle_thematic, raccoon_food_bundle_thematic, raccoon_foraging_bundle_thematic]
raccoon_bundles_remixed = raccoon_bundles_thematic
raccoon_vanilla = BundleRoomTemplate(CCRoom.raccoon_requests, raccoon_bundles_vanilla, 8)
raccoon_thematic = BundleRoomTemplate(CCRoom.raccoon_requests, raccoon_bundles_thematic, 8)
raccoon_remixed = BundleRoomTemplate(CCRoom.raccoon_requests, raccoon_bundles_remixed, 8)

# Crafts Room
spring_foraging_items_vanilla = [wild_horseradish, daffodil, leek, dandelion]
spring_foraging_items_thematic = [*spring_foraging_items_vanilla, spring_onion, salmonberry, morel]
spring_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.spring_foraging, spring_foraging_items_vanilla, 4, 4)
spring_foraging_bundle_thematic = BundleTemplate.extend_from(spring_foraging_bundle_vanilla, spring_foraging_items_thematic)

summer_foraging_items_vanilla = [grape, spice_berry, sweet_pea]
summer_foraging_items_thematic = [*summer_foraging_items_vanilla, fiddlehead_fern, red_mushroom, rainbow_shell]
summer_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.summer_foraging, summer_foraging_items_vanilla, 3, 3)
summer_foraging_bundle_thematic = BundleTemplate.extend_from(summer_foraging_bundle_vanilla, summer_foraging_items_thematic)

fall_foraging_items_vanilla = [common_mushroom, wild_plum, hazelnut, blackberry]
fall_foraging_items_thematic = [*fall_foraging_items_vanilla, chanterelle]
fall_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.fall_foraging, fall_foraging_items_vanilla, 4, 4)
fall_foraging_bundle_thematic = BundleTemplate.extend_from(fall_foraging_bundle_vanilla, fall_foraging_items_thematic)

winter_foraging_items_vanilla = [winter_root, crystal_fruit, snow_yam, crocus]
winter_foraging_items_thematic = [*winter_foraging_items_vanilla, holly, nautilus_shell]
winter_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.winter_foraging, winter_foraging_items_vanilla, 4, 4)
winter_foraging_bundle_thematic = BundleTemplate.extend_from(winter_foraging_bundle_vanilla, winter_foraging_items_thematic)

construction_items_vanilla = [wood, stone, hardwood]
construction_items_thematic = [*construction_items_vanilla, clay, fiber, sap.as_amount(50)]
construction_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.construction, construction_items_vanilla, 4, 4)
construction_bundle_thematic = BundleTemplate.extend_from(construction_bundle_vanilla, construction_items_thematic)

exotic_foraging_items_vanilla = [coconut, cactus_fruit, cave_carrot, red_mushroom, purple_mushroom, maple_syrup, oak_resin, pine_tar, morel]
exotic_foraging_items_thematic = [*exotic_foraging_items_vanilla, coral, sea_urchin, clam, cockle, mussel, oyster, seaweed]
exotic_foraging_bundle_vanilla = BundleTemplate(CCRoom.crafts_room, BundleName.exotic_foraging, exotic_foraging_items_vanilla, 9, 5)
exotic_foraging_bundle_thematic = BundleTemplate.extend_from(exotic_foraging_bundle_vanilla, exotic_foraging_items_thematic)

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

crafts_room_bundles_vanilla = [spring_foraging_bundle_vanilla, summer_foraging_bundle_vanilla, fall_foraging_bundle_vanilla,
                               winter_foraging_bundle_vanilla, construction_bundle_vanilla, exotic_foraging_bundle_vanilla]
crafts_room_bundles_thematic = [spring_foraging_bundle_thematic, summer_foraging_bundle_thematic, fall_foraging_bundle_thematic,
                                winter_foraging_bundle_thematic, construction_bundle_thematic, exotic_foraging_bundle_thematic]
crafts_room_bundles_remixed = [*crafts_room_bundles_thematic, beach_foraging_bundle, mines_foraging_bundle, desert_foraging_bundle,
                               island_foraging_bundle, sticky_bundle, forest_bundle, wild_medicine_bundle, quality_foraging_bundle, green_rain_bundle]
crafts_room_vanilla = BundleRoomTemplate(CCRoom.crafts_room, crafts_room_bundles_vanilla, 6)
crafts_room_thematic = BundleRoomTemplate(CCRoom.crafts_room, crafts_room_bundles_thematic, 6)
crafts_room_remixed = BundleRoomTemplate(CCRoom.crafts_room, crafts_room_bundles_remixed, 6)

# Pantry
spring_crops_items_vanilla = [parsnip, green_bean, cauliflower, potato]
spring_crops_items_thematic = [*spring_crops_items_vanilla, blue_jazz, coffee_bean, garlic, kale, rhubarb, strawberry, tulip, unmilled_rice, carrot]
spring_crops_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.spring_crops, spring_crops_items_vanilla, 4, 4)
spring_crops_bundle_thematic = BundleTemplate.extend_from(spring_crops_bundle_vanilla, spring_crops_items_thematic)

summer_crops_items_vanilla = [tomato, hot_pepper, blueberry, melon]
summer_crops_items_thematic = [*summer_crops_items_vanilla, corn, hops, poppy, radish, red_cabbage, starfruit, summer_spangle, sunflower, wheat, summer_squash]
summer_crops_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.summer_crops, summer_crops_items_vanilla, 4, 4)
summer_crops_bundle_thematic = BundleTemplate.extend_from(summer_crops_bundle_vanilla, summer_crops_items_thematic)

fall_crops_items_vanilla = [corn, eggplant, pumpkin, yam]
fall_crops_items_thematic = [*fall_crops_items_vanilla, amaranth, artichoke, beet, bok_choy, cranberries, fairy_rose, grape,
                             sunflower, wheat, sweet_gem_berry, broccoli]
fall_crops_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.fall_crops, fall_crops_items_vanilla, 4, 4)
fall_crops_bundle_thematic = BundleTemplate.extend_from(fall_crops_bundle_vanilla, fall_crops_items_thematic)

all_crops_items = sorted({*spring_crops_items_thematic, *summer_crops_items_thematic, *fall_crops_items_thematic, powdermelon})

quality_crops_items_vanilla = [item.as_quality_crop() for item in [parsnip, melon, pumpkin, corn]]
quality_crops_items_thematic = [item.as_quality_crop() for item in all_crops_items]
quality_crops_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.quality_crops, quality_crops_items_vanilla, 4, 3)
quality_crops_bundle_thematic = BundleTemplate.extend_from(quality_crops_bundle_vanilla, quality_crops_items_thematic)

animal_items_vanilla = [large_milk, large_brown_egg, large_egg, large_goat_milk, wool, duck_egg]
animal_items_thematic = [*animal_items_vanilla, egg, brown_egg, milk, goat_milk, truffle,
                         duck_feather, rabbit_foot, dinosaur_egg, void_egg, golden_egg, ostrich_egg]
animal_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.animal, animal_items_vanilla, 6, 5)
animal_bundle_thematic = BundleTemplate.extend_from(animal_bundle_vanilla, animal_items_thematic)

artisan_items_vanilla = [truffle_oil, cloth, goat_cheese, cheese, honey, jelly, apple, apricot, orange, peach, pomegranate, cherry]
artisan_items_thematic = [*artisan_items_vanilla, beer, juice, mead, pale_ale, wine, pickles, caviar, aged_roe, coffee, green_tea, banana, mango]
artisan_bundle_vanilla = BundleTemplate(CCRoom.pantry, BundleName.artisan, artisan_items_vanilla, 12, 6)
artisan_bundle_thematic = BundleTemplate.extend_from(artisan_bundle_vanilla, artisan_items_thematic)

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

pantry_bundles_vanilla = [spring_crops_bundle_vanilla, summer_crops_bundle_vanilla, fall_crops_bundle_vanilla,
                          quality_crops_bundle_vanilla, animal_bundle_vanilla, artisan_bundle_vanilla]
pantry_bundles_thematic = [spring_crops_bundle_thematic, summer_crops_bundle_thematic, fall_crops_bundle_thematic,
                           quality_crops_bundle_thematic, animal_bundle_thematic, artisan_bundle_thematic]
pantry_bundles_remixed = [*pantry_bundles_thematic, rare_crops_bundle, fish_farmer_bundle, garden_bundle,
                          brewer_bundle, orchard_bundle, island_crops_bundle, agronomist_bundle, slime_farmer_bundle, sommelier_bundle, dry_bundle]
pantry_vanilla = BundleRoomTemplate(CCRoom.pantry, pantry_bundles_vanilla, 6)
pantry_thematic = BundleRoomTemplate(CCRoom.pantry, pantry_bundles_thematic, 6)
pantry_remixed = BundleRoomTemplate(CCRoom.pantry, pantry_bundles_remixed, 6)

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
