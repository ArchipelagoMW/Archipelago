from dataclasses import dataclass

from . import fish_data
from .common_data import quality_dict
from .game_item import GameItem
from .museum_data import Mineral

@dataclass(frozen=True)
class BundleItem:
    item: GameItem
    amount: int
    quality: int

    @staticmethod
    def item_bundle(name: str, item_id: int, amount: int, quality: int):
        return BundleItem(GameItem(name, item_id), amount, quality)

    @staticmethod
    def money_bundle(amount: int):
        return BundleItem.item_bundle("Money", -1, amount, amount)

    def as_amount(self, amount: int):
        return BundleItem.item_bundle(self.item.name, self.item.item_id, amount, self.quality)

    def as_quality(self, quality: int):
        return BundleItem.item_bundle(self.item.name, self.item.item_id, self.amount, quality)

    def as_gold_quality(self):
        return self.as_quality(2)

    def as_quality_crop(self):
        amount = 5
        difficult_crops = ["Sweet Gem Berry", "Ancient Fruit"]
        if self.item.name in difficult_crops:
            amount = 1
        return self.as_gold_quality().as_amount(amount)

    def is_gold_quality(self) -> bool:
        return self.quality >= 2

    def __repr__(self):
        return f"{self.amount} {quality_dict[self.quality]} {self.item.name}"

    def __lt__(self, other):
        return self.item < other.item


wild_horseradish = BundleItem.item_bundle("Wild Horseradish", 16, 1, 0)
daffodil = BundleItem.item_bundle("Daffodil", 18, 1, 0)
leek = BundleItem.item_bundle("Leek", 20, 1, 0)
dandelion = BundleItem.item_bundle("Dandelion", 22, 1, 0)
morel = BundleItem.item_bundle("Morel", 257, 1, 0)
common_mushroom = BundleItem.item_bundle("Common Mushroom", 404, 1, 0)
salmonberry = BundleItem.item_bundle("Salmonberry", 296, 1, 0)
spring_onion = BundleItem.item_bundle("Spring Onion", 399, 1, 0)

grape = BundleItem.item_bundle("Grape", 398, 1, 0)
spice_berry = BundleItem.item_bundle("Spice Berry", 396, 1, 0)
sweet_pea = BundleItem.item_bundle("Sweet Pea", 402, 1, 0)
red_mushroom = BundleItem.item_bundle("Red Mushroom", 420, 1, 0)
fiddlehead_fern = BundleItem.item_bundle("Fiddlehead Fern", 259, 1, 0)

wild_plum = BundleItem.item_bundle("Wild Plum", 406, 1, 0)
hazelnut = BundleItem.item_bundle("Hazelnut", 408, 1, 0)
blackberry = BundleItem.item_bundle("Blackberry", 410, 1, 0)
chanterelle = BundleItem.item_bundle("Chanterelle", 281, 1, 0)

winter_root = BundleItem.item_bundle("Winter Root", 412, 1, 0)
crystal_fruit = BundleItem.item_bundle("Crystal Fruit", 414, 1, 0)
snow_yam = BundleItem.item_bundle("Snow Yam", 416, 1, 0)
crocus = BundleItem.item_bundle("Crocus", 418, 1, 0)
holly = BundleItem.item_bundle("Holly", 283, 1, 0)

coconut = BundleItem.item_bundle("Coconut", 88, 1, 0)
cactus_fruit = BundleItem.item_bundle("Cactus Fruit", 90, 1, 0)
cave_carrot = BundleItem.item_bundle("Cave Carrot", 78, 1, 0)
purple_mushroom = BundleItem.item_bundle("Purple Mushroom", 422, 1, 0)
maple_syrup = BundleItem.item_bundle("Maple Syrup", 724, 1, 0)
oak_resin = BundleItem.item_bundle("Oak Resin", 725, 1, 0)
pine_tar = BundleItem.item_bundle("Pine Tar", 726, 1, 0)
nautilus_shell = BundleItem.item_bundle("Nautilus Shell", 392, 1, 0)
coral = BundleItem.item_bundle("Coral", 393, 1, 0)
sea_urchin = BundleItem.item_bundle("Sea Urchin", 397, 1, 0)
rainbow_shell = BundleItem.item_bundle("Rainbow Shell", 394, 1, 0)
clam = BundleItem(fish_data.clam, 1, 0)
cockle = BundleItem(fish_data.cockle, 1, 0)
mussel = BundleItem(fish_data.mussel, 1, 0)
oyster = BundleItem(fish_data.oyster, 1, 0)
seaweed = BundleItem.item_bundle("Seaweed", 152, 1, 0)

wood = BundleItem.item_bundle("Wood", 388, 99, 0)
stone = BundleItem.item_bundle("Stone", 390, 99, 0)
hardwood = BundleItem.item_bundle("Hardwood", 709, 10, 0)
clay = BundleItem.item_bundle("Clay", 330, 10, 0)
fiber = BundleItem.item_bundle("Fiber", 771, 99, 0)

blue_jazz = BundleItem.item_bundle("Blue Jazz", 597, 1, 0)
cauliflower = BundleItem.item_bundle("Cauliflower", 190, 1, 0)
green_bean = BundleItem.item_bundle("Green Bean", 188, 1, 0)
kale = BundleItem.item_bundle("Kale", 250, 1, 0)
parsnip = BundleItem.item_bundle("Parsnip", 24, 1, 0)
potato = BundleItem.item_bundle("Potato", 192, 1, 0)
strawberry = BundleItem.item_bundle("Strawberry", 400, 1, 0)
tulip = BundleItem.item_bundle("Tulip", 591, 1, 0)
unmilled_rice = BundleItem.item_bundle("Unmilled Rice", 271, 1, 0)
blueberry = BundleItem.item_bundle("Blueberry", 258, 1, 0)
corn = BundleItem.item_bundle("Corn", 270, 1, 0)
hops = BundleItem.item_bundle("Hops", 304, 1, 0)
hot_pepper = BundleItem.item_bundle("Hot Pepper", 260, 1, 0)
melon = BundleItem.item_bundle("Melon", 254, 1, 0)
poppy = BundleItem.item_bundle("Poppy", 376, 1, 0)
radish = BundleItem.item_bundle("Radish", 264, 1, 0)
summer_spangle = BundleItem.item_bundle("Summer Spangle", 593, 1, 0)
sunflower = BundleItem.item_bundle("Sunflower", 421, 1, 0)
tomato = BundleItem.item_bundle("Tomato", 256, 1, 0)
wheat = BundleItem.item_bundle("Wheat", 262, 1, 0)
hay = BundleItem.item_bundle("Hay", 178, 1, 0)
amaranth = BundleItem.item_bundle("Amaranth", 300, 1, 0)
bok_choy = BundleItem.item_bundle("Bok Choy", 278, 1, 0)
cranberries = BundleItem.item_bundle("Cranberries", 282, 1, 0)
eggplant = BundleItem.item_bundle("Eggplant", 272, 1, 0)
fairy_rose = BundleItem.item_bundle("Fairy Rose", 595, 1, 0)
pumpkin = BundleItem.item_bundle("Pumpkin", 276, 1, 0)
yam = BundleItem.item_bundle("Yam", 280, 1, 0)
sweet_gem_berry = BundleItem.item_bundle("Sweet Gem Berry", 417, 1, 0)
rhubarb = BundleItem.item_bundle("Rhubarb", 252, 1, 0)
beet = BundleItem.item_bundle("Beet", 284, 1, 0)
red_cabbage = BundleItem.item_bundle("Red Cabbage", 266, 1, 0)
artichoke = BundleItem.item_bundle("Artichoke", 274, 1, 0)

egg = BundleItem.item_bundle("Egg", 176, 1, 0)
large_egg = BundleItem.item_bundle("Large Egg", 174, 1, 0)
brown_egg = BundleItem.item_bundle("Egg (Brown)", 180, 1, 0)
large_brown_egg = BundleItem.item_bundle("Large Egg (Brown)", 182, 1, 0)
wool = BundleItem.item_bundle("Wool", 440, 1, 0)
milk = BundleItem.item_bundle("Milk", 184, 1, 0)
large_milk = BundleItem.item_bundle("Large Milk", 186, 1, 0)
goat_milk = BundleItem.item_bundle("Goat Milk", 436, 1, 0)
large_goat_milk = BundleItem.item_bundle("Large Goat Milk", 438, 1, 0)
truffle = BundleItem.item_bundle("Truffle", 430, 1, 0)
duck_feather = BundleItem.item_bundle("Duck Feather", 444, 1, 0)
duck_egg = BundleItem.item_bundle("Duck Egg", 442, 1, 0)
rabbit_foot = BundleItem.item_bundle("Rabbit's Foot", 446, 1, 0)

truffle_oil = BundleItem.item_bundle("Truffle Oil", 432, 1, 0)
cloth = BundleItem.item_bundle("Cloth", 428, 1, 0)
goat_cheese = BundleItem.item_bundle("Goat Cheese", 426, 1, 0)
cheese = BundleItem.item_bundle("Cheese", 424, 1, 0)
honey = BundleItem.item_bundle("Honey", 340, 1, 0)
beer = BundleItem.item_bundle("Beer", 346, 1, 0)
juice = BundleItem.item_bundle("Juice", 350, 1, 0)
mead = BundleItem.item_bundle("Mead", 459, 1, 0)
pale_ale = BundleItem.item_bundle("Pale Ale", 303, 1, 0)
wine = BundleItem.item_bundle("Wine", 348, 1, 0)
jelly = BundleItem.item_bundle("Jelly", 344, 1, 0)
pickles = BundleItem.item_bundle("Pickles", 342, 1, 0)
caviar = BundleItem.item_bundle("Caviar", 445, 1, 0)
aged_roe = BundleItem.item_bundle("Aged Roe", 447, 1, 0)
apple = BundleItem.item_bundle("Apple", 613, 1, 0)
apricot = BundleItem.item_bundle("Apricot", 634, 1, 0)
orange = BundleItem.item_bundle("Orange", 635, 1, 0)
peach = BundleItem.item_bundle("Peach", 636, 1, 0)
pomegranate = BundleItem.item_bundle("Pomegranate", 637, 1, 0)
cherry = BundleItem.item_bundle("Cherry", 638, 1, 0)
lobster = BundleItem(fish_data.lobster, 1, 0)
crab = BundleItem(fish_data.crab, 1, 0)
shrimp = BundleItem(fish_data.shrimp, 1, 0)
crayfish = BundleItem(fish_data.crayfish, 1, 0)
snail = BundleItem(fish_data.snail, 1, 0)
periwinkle = BundleItem(fish_data.periwinkle, 1, 0)
trash = BundleItem.item_bundle("Trash", 168, 1, 0)
driftwood = BundleItem.item_bundle("Driftwood", 169, 1, 0)
soggy_newspaper = BundleItem.item_bundle("Soggy Newspaper", 172, 1, 0)
broken_cd = BundleItem.item_bundle("Broken CD", 171, 1, 0)
broken_glasses = BundleItem.item_bundle("Broken Glasses", 170, 1, 0)

chub = BundleItem(fish_data.chub, 1, 0)
catfish = BundleItem(fish_data.catfish, 1, 0)
rainbow_trout = BundleItem(fish_data.rainbow_trout, 1, 0)
lingcod = BundleItem(fish_data.lingcod, 1, 0)
walleye = BundleItem(fish_data.walleye, 1, 0)
perch = BundleItem(fish_data.perch, 1, 0)
pike = BundleItem(fish_data.pike, 1, 0)
bream = BundleItem(fish_data.bream, 1, 0)
salmon = BundleItem(fish_data.salmon, 1, 0)
sunfish = BundleItem(fish_data.sunfish, 1, 0)
tiger_trout = BundleItem(fish_data.tiger_trout, 1, 0)
shad = BundleItem(fish_data.shad, 1, 0)
smallmouth_bass = BundleItem(fish_data.smallmouth_bass, 1, 0)
dorado = BundleItem(fish_data.dorado, 1, 0)
carp = BundleItem(fish_data.carp, 1, 0)
midnight_carp = BundleItem(fish_data.midnight_carp, 1, 0)
largemouth_bass = BundleItem(fish_data.largemouth_bass, 1, 0)
sturgeon = BundleItem(fish_data.sturgeon, 1, 0)
bullhead = BundleItem(fish_data.bullhead, 1, 0)
tilapia = BundleItem(fish_data.tilapia, 1, 0)
pufferfish = BundleItem(fish_data.pufferfish, 1, 0)
tuna = BundleItem(fish_data.tuna, 1, 0)
super_cucumber = BundleItem(fish_data.super_cucumber, 1, 0)
flounder = BundleItem(fish_data.flounder, 1, 0)
anchovy = BundleItem(fish_data.anchovy, 1, 0)
sardine = BundleItem(fish_data.sardine, 1, 0)
red_mullet = BundleItem(fish_data.red_mullet, 1, 0)
herring = BundleItem(fish_data.herring, 1, 0)
eel = BundleItem(fish_data.eel, 1, 0)
octopus = BundleItem(fish_data.octopus, 1, 0)
red_snapper = BundleItem(fish_data.red_snapper, 1, 0)
squid = BundleItem(fish_data.squid, 1, 0)
sea_cucumber = BundleItem(fish_data.sea_cucumber, 1, 0)
albacore = BundleItem(fish_data.albacore, 1, 0)
halibut = BundleItem(fish_data.halibut, 1, 0)
scorpion_carp = BundleItem(fish_data.scorpion_carp, 1, 0)
sandfish = BundleItem(fish_data.sandfish, 1, 0)
woodskip = BundleItem(fish_data.woodskip, 1, 0)
lava_eel = BundleItem(fish_data.lava_eel, 1, 0)
ice_pip = BundleItem(fish_data.ice_pip, 1, 0)
stonefish = BundleItem(fish_data.stonefish, 1, 0)
ghostfish = BundleItem(fish_data.ghostfish, 1, 0)

wilted_bouquet = BundleItem.item_bundle("Wilted Bouquet", 277, 1, 0)
copper_bar = BundleItem.item_bundle("Copper Bar", 334, 2, 0)
iron_Bar = BundleItem.item_bundle("Iron Bar", 335, 2, 0)
gold_bar = BundleItem.item_bundle("Gold Bar", 336, 1, 0)
iridium_bar = BundleItem.item_bundle("Iridium Bar", 337, 1, 0)
refined_quartz = BundleItem.item_bundle("Refined Quartz", 338, 2, 0)
coal = BundleItem.item_bundle("Coal", 382, 5, 0)

quartz = BundleItem(Mineral.quartz, 1, 0)
fire_quartz = BundleItem(Mineral.fire_quartz, 1, 0)
frozen_tear = BundleItem(Mineral.frozen_tear, 1, 0)
earth_crystal = BundleItem(Mineral.earth_crystal, 1, 0)
emerald = BundleItem(Mineral.emerald, 1, 0)
aquamarine = BundleItem(Mineral.aquamarine, 1, 0)
ruby = BundleItem(Mineral.ruby, 1, 0)
amethyst = BundleItem(Mineral.amethyst, 1, 0)
topaz = BundleItem(Mineral.topaz, 1, 0)
jade = BundleItem(Mineral.jade, 1, 0)

slime = BundleItem.item_bundle("Slime", 766, 99, 0)
bug_meat = BundleItem.item_bundle("Bug Meat", 684, 10, 0)
bat_wing = BundleItem.item_bundle("Bat Wing", 767, 10, 0)
solar_essence = BundleItem.item_bundle("Solar Essence", 768, 1, 0)
void_essence = BundleItem.item_bundle("Void Essence", 769, 1, 0)

maki_roll = BundleItem.item_bundle("Maki Roll", 228, 1, 0)
fried_egg = BundleItem.item_bundle("Fried Egg", 194, 1, 0)
omelet = BundleItem.item_bundle("Omelet", 195, 1, 0)
pizza = BundleItem.item_bundle("Pizza", 206, 1, 0)
hashbrowns = BundleItem.item_bundle("Hashbrowns", 210, 1, 0)
pancakes = BundleItem.item_bundle("Pancakes", 211, 1, 0)
bread = BundleItem.item_bundle("Bread", 216, 1, 0)
tortilla = BundleItem.item_bundle("Tortilla", 229, 1, 0)
triple_shot_espresso = BundleItem.item_bundle("Triple Shot Espresso", 253, 1, 0)
farmer_s_lunch = BundleItem.item_bundle("Farmer's Lunch", 240, 1, 0)
survival_burger = BundleItem.item_bundle("Survival Burger", 241, 1, 0)
dish_o_the_sea = BundleItem.item_bundle("Dish O' The Sea", 242, 1, 0)
miner_s_treat = BundleItem.item_bundle("Miner's Treat", 243, 1, 0)
roots_platter = BundleItem.item_bundle("Roots Platter", 244, 1, 0)
salad = BundleItem.item_bundle("Salad", 196, 1, 0)
cheese_cauliflower = BundleItem.item_bundle("Cheese Cauliflower", 197, 1, 0)
parsnip_soup = BundleItem.item_bundle("Parsnip Soup", 199, 1, 0)
fried_mushroom = BundleItem.item_bundle("Fried Mushroom", 205, 1, 0)
salmon_dinner = BundleItem.item_bundle("Salmon Dinner", 212, 1, 0)
pepper_poppers = BundleItem.item_bundle("Pepper Poppers", 215, 1, 0)
spaghetti = BundleItem.item_bundle("Spaghetti", 224, 1, 0)
sashimi = BundleItem.item_bundle("Sashimi", 227, 1, 0)
blueberry_tart = BundleItem.item_bundle("Blueberry Tart", 234, 1, 0)
algae_soup = BundleItem.item_bundle("Algae Soup", 456, 1, 0)
pale_broth = BundleItem.item_bundle("Pale Broth", 457, 1, 0)
chowder = BundleItem.item_bundle("Chowder", 727, 1, 0)
green_algae = BundleItem.item_bundle("Green Algae", 153, 1, 0)
white_algae = BundleItem.item_bundle("White Algae", 157, 1, 0)
geode = BundleItem.item_bundle("Geode", 535, 1, 0)
frozen_geode = BundleItem.item_bundle("Frozen Geode", 536, 1, 0)
magma_geode = BundleItem.item_bundle("Magma Geode", 537, 1, 0)
omni_geode = BundleItem.item_bundle("Omni Geode", 749, 1, 0)

spring_foraging_items = [wild_horseradish, daffodil, leek, dandelion, salmonberry, spring_onion]
summer_foraging_items = [grape, spice_berry, sweet_pea, fiddlehead_fern, rainbow_shell]
fall_foraging_items = [common_mushroom, wild_plum, hazelnut, blackberry]
winter_foraging_items = [winter_root, crystal_fruit, snow_yam, crocus, holly, nautilus_shell]
exotic_foraging_items = [coconut, cactus_fruit, cave_carrot, red_mushroom, purple_mushroom,
                         maple_syrup, oak_resin, pine_tar, morel, coral,
                         sea_urchin, clam, cockle, mussel, oyster, seaweed]
construction_items = [wood, stone, hardwood, clay, fiber]

# TODO coffee_bean, garlic, rhubarb, tea_leaves
spring_crop_items = [blue_jazz, cauliflower, green_bean, kale, parsnip, potato, strawberry, tulip, unmilled_rice]
# TODO red_cabbage, starfruit, ancient_fruit, pineapple, taro_root
summer_crops_items = [blueberry, corn, hops, hot_pepper, melon, poppy,
                      radish, summer_spangle, sunflower, tomato, wheat]
# TODO artichoke, beet
fall_crops_items = [corn, sunflower, wheat, amaranth, bok_choy, cranberries,
                    eggplant, fairy_rose, grape, pumpkin, yam, sweet_gem_berry]
all_crops_items = sorted({*spring_crop_items, *summer_crops_items, *fall_crops_items})
quality_crops_items = [item.as_quality_crop() for item in all_crops_items]
# TODO void_egg, dinosaur_egg, ostrich_egg, golden_egg
animal_product_items = [egg, large_egg, brown_egg, large_brown_egg, wool, milk, large_milk,
                        goat_milk, large_goat_milk, truffle, duck_feather, duck_egg, rabbit_foot]
# TODO coffee, green_tea
artisan_goods_items = [truffle_oil, cloth, goat_cheese, cheese, honey, beer, juice, mead, pale_ale, wine, jelly,
                       pickles, caviar, aged_roe, apple, apricot, orange, peach, pomegranate, cherry]

river_fish_items = [chub, catfish, rainbow_trout, lingcod, walleye, perch, pike, bream,
                    salmon, sunfish, tiger_trout, shad, smallmouth_bass, dorado]
lake_fish_items = [chub, rainbow_trout, lingcod, walleye, perch, carp, midnight_carp, largemouth_bass, sturgeon, bullhead]
ocean_fish_items = [tilapia, pufferfish, tuna, super_cucumber, flounder, anchovy, sardine, red_mullet,
                    herring, eel, octopus, red_snapper, squid, sea_cucumber, albacore, halibut]
night_fish_items = [walleye, bream, super_cucumber, eel, squid, midnight_carp]
# TODO void_salmon
specialty_fish_items = [scorpion_carp, sandfish, woodskip, pufferfish, eel, octopus,
                        squid, lava_eel, ice_pip, stonefish, ghostfish, dorado]
crab_pot_items = [lobster, clam, crab, cockle, mussel, shrimp, oyster, crayfish, snail,
                  periwinkle, trash, driftwood, soggy_newspaper, broken_cd, broken_glasses]

# TODO radioactive_bar
blacksmith_items = [wilted_bouquet, copper_bar, iron_Bar, gold_bar, iridium_bar, refined_quartz, coal]
geologist_items = [quartz, earth_crystal, frozen_tear, fire_quartz, emerald, aquamarine, ruby, amethyst, topaz, jade]
adventurer_items = [slime, bug_meat, bat_wing, solar_essence, void_essence, coal]

chef_items = [maki_roll, fried_egg, omelet, pizza, hashbrowns, pancakes, bread, tortilla, triple_shot_espresso,
              farmer_s_lunch, survival_burger, dish_o_the_sea, miner_s_treat, roots_platter, salad,
              cheese_cauliflower, parsnip_soup, fried_mushroom, salmon_dinner, pepper_poppers, spaghetti,
              sashimi, blueberry_tart, algae_soup, pale_broth, chowder]

dwarf_scroll_1 = BundleItem.item_bundle("Dwarf Scroll I", 96, 1, 0)
dwarf_scroll_2 = BundleItem.item_bundle("Dwarf Scroll II", 97, 1, 0)
dwarf_scroll_3 = BundleItem.item_bundle("Dwarf Scroll III", 98, 1, 0)
dwarf_scroll_4 = BundleItem.item_bundle("Dwarf Scroll IV", 99, 1, 0)
elvish_jewelry = BundleItem.item_bundle("Elvish Jewelry", 104, 1, 0)
ancient_drum = BundleItem.item_bundle("Ancient Drum", 123, 1, 0)
dried_starfish = BundleItem.item_bundle("Dried Starfish", 116, 1, 0)

dye_red_items = [cranberries, hot_pepper, radish, rhubarb, spaghetti, strawberry, tomato, tulip]
dye_orange_items = [poppy, pumpkin, apricot, orange, spice_berry, winter_root]
dye_yellow_items = [corn, parsnip, summer_spangle, sunflower]
dye_green_items = [fiddlehead_fern, kale, artichoke, bok_choy, green_bean]
dye_blue_items = [blueberry, blue_jazz, blackberry, crystal_fruit]
dye_purple_items = [beet, crocus, eggplant, red_cabbage, sweet_pea]
dye_items = [dye_red_items, dye_orange_items, dye_yellow_items, dye_green_items, dye_blue_items, dye_purple_items]
field_research_items = [purple_mushroom, nautilus_shell, chub, geode, frozen_geode, magma_geode, omni_geode,
                        rainbow_shell, amethyst, bream, carp]
fodder_items = [wheat.as_amount(10), hay.as_amount(10), apple.as_amount(3), kale.as_amount(3), corn.as_amount(3),
                green_bean.as_amount(3), potato.as_amount(3), green_algae.as_amount(5), white_algae.as_amount(3)]
enchanter_items = [oak_resin, wine, rabbit_foot, pomegranate, purple_mushroom, solar_essence,
                   super_cucumber, void_essence, fire_quartz, frozen_tear, jade]

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
}, key=lambda x: x.item.name)

all_bundle_items = sorted({
    *crafts_room_bundle_items,
    *pantry_bundle_items,
    *fish_tank_bundle_items,
    *boiler_room_bundle_items,
    *bulletin_board_bundle_items,
    *vault_bundle_items,
}, key=lambda x: x.item.name)

all_bundle_items_by_name = {item.item.name: item for item in all_bundle_items}
all_bundle_items_by_id = {item.item.item_id: item for item in all_bundle_items}
