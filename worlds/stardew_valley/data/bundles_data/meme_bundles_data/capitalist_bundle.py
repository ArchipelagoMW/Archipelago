import math
from typing import Dict, List

from ..bundle_items_data import *
from ....bundles.bundle_item import BundleItem
from ....strings.quality_names import ArtisanQuality

capitalist_value = 1000000
ancient_fruit_wines = {ArtisanQuality.basic: 2310, ArtisanQuality.silver: 2886, ArtisanQuality.gold: 3465, ArtisanQuality.iridium: 4620}
starfruit_wines = {ArtisanQuality.basic: 3150, ArtisanQuality.silver: 3936, ArtisanQuality.gold: 4725, ArtisanQuality.iridium: 6300}
rhubarb_wines = {ArtisanQuality.silver: 1155, ArtisanQuality.gold: 1386, ArtisanQuality.iridium: 1848}
melon_wines = {ArtisanQuality.basic: 1050, ArtisanQuality.silver: 1311, ArtisanQuality.gold: 1575, ArtisanQuality.iridium: 2100}
pineapple_wines = {ArtisanQuality.basic: 1260, ArtisanQuality.silver: 1575, ArtisanQuality.gold: 1890, ArtisanQuality.iridium: 2520}
starfruits = {ArtisanQuality.silver: 1030, ArtisanQuality.gold: 1237, ArtisanQuality.iridium: 1650}
sweet_gem_berries = {ArtisanQuality.basic: 3000, ArtisanQuality.silver: 3750, ArtisanQuality.gold: 4500, ArtisanQuality.iridium: 6000}

# These are just too rude I think
# cherry_saplings = {ArtisanQuality.silver: 1062, ArtisanQuality.gold: 1275, ArtisanQuality.iridium: 1700}
# banana_saplings = {ArtisanQuality.silver: 1062, ArtisanQuality.gold: 1275, ArtisanQuality.iridium: 1700}
# mango_saplings = {ArtisanQuality.silver: 1062, ArtisanQuality.gold: 1275, ArtisanQuality.iridium: 1700}
# orange_saplings = {ArtisanQuality.silver: 1250, ArtisanQuality.gold: 1500, ArtisanQuality.iridium: 2000}
# peach_saplings = {ArtisanQuality.basic: 1500, ArtisanQuality.silver: 1875, ArtisanQuality.gold: 2250, ArtisanQuality.iridium: 3000}
# apple_saplings = {ArtisanQuality.silver: 1250, ArtisanQuality.gold: 1500, ArtisanQuality.iridium: 2000}
# pomegranate_saplings = {ArtisanQuality.basic: 1500, ArtisanQuality.silver: 1875, ArtisanQuality.gold: 2250, ArtisanQuality.iridium: 3000}


def get_capitalist_item(item: BundleItem, quality: str, value: int) -> BundleItem:
    amount = math.ceil(capitalist_value / value)
    assert amount < 1000
    return item.as_quality(quality).as_amount(amount)


def get_capitalist_items(item: BundleItem, values_by_quality: Dict[str, int]) -> List[BundleItem]:
    return [get_capitalist_item(item, quality, values_by_quality[quality]) for quality in values_by_quality]


capitalist_items = [
    *get_capitalist_items(ancient_fruit_wine, ancient_fruit_wines),
    get_capitalist_item(dried_ancient_fruit, ArtisanQuality.basic, 5810),
    get_capitalist_item(ancient_fruit_jelly, ArtisanQuality.basic, 1610),
    get_capitalist_item(ancient_fruit, ArtisanQuality.iridium, 1210),

    *get_capitalist_items(starfruit_wine, starfruit_wines),
    get_capitalist_item(dried_starfruit, ArtisanQuality.basic, 7910),
    get_capitalist_item(starfruit_jelly, ArtisanQuality.basic, 2170),
    *get_capitalist_items(starfruit, starfruits),

    *get_capitalist_items(rhubarb_wine, rhubarb_wines),
    get_capitalist_item(dried_rhubarb, ArtisanQuality.basic, 2345),
    *get_capitalist_items(melon_wine, melon_wines),
    get_capitalist_item(dried_melon, ArtisanQuality.basic, 2660),
    *get_capitalist_items(pineapple_wine, pineapple_wines),

    get_capitalist_item(dried_pineapple, ArtisanQuality.basic, 3185),
    get_capitalist_item(dried_banana, ArtisanQuality.basic, 1610),
    get_capitalist_item(strawberry_wine, ArtisanQuality.iridium, 1008),
    get_capitalist_item(dried_strawberry, ArtisanQuality.basic, 1295),

    *get_capitalist_items(sweet_gem_berry, sweet_gem_berries),
    get_capitalist_item(pumpkin_juice, ArtisanQuality.basic, 1008),

    get_capitalist_item(goat_cheese, ArtisanQuality.iridium, 1120),
    get_capitalist_item(golden_egg, ArtisanQuality.iridium, 1200),
    get_capitalist_item(dinosaur_mayo, ArtisanQuality.basic, 1120),
    get_capitalist_item(truffle_oil, ArtisanQuality.basic, 1491),
    get_capitalist_item(truffle, ArtisanQuality.iridium, 1250),

    get_capitalist_item(aged_lava_eel_roe, ArtisanQuality.basic, 1064),
    get_capitalist_item(aged_crimsonfish_roe, ArtisanQuality.basic, 2184),
    get_capitalist_item(aged_angler_roe, ArtisanQuality.basic, 1344),
    get_capitalist_item(legend_roe, ArtisanQuality.basic, 2530),
    get_capitalist_item(aged_legend_roe, ArtisanQuality.basic, 7084),
    get_capitalist_item(aged_glacierfish_roe, ArtisanQuality.basic, 1484),
    get_capitalist_item(aged_mutant_carp_roe, ArtisanQuality.basic, 1484),

    get_capitalist_item(iridium_bar, ArtisanQuality.basic, 1500),
    get_capitalist_item(radioactive_bar, ArtisanQuality.basic, 4500),
    get_capitalist_item(prismatic_shard, ArtisanQuality.basic, 2600),

    get_capitalist_item(mystic_syrup, ArtisanQuality.basic, 1250),

    # *get_capitalist_items(cherry_sapling, cherry_saplings),
    # *get_capitalist_items(banana_sapling, banana_saplings),
    # *get_capitalist_items(mango_sapling, mango_saplings),
    # *get_capitalist_items(orange_sapling, orange_saplings),
    # *get_capitalist_items(peach_sapling, peach_saplings),
    # *get_capitalist_items(apple_sapling, apple_saplings),
    # *get_capitalist_items(pomegranate_sapling, pomegranate_saplings),

    bowler_hat,
    sombrero,
]