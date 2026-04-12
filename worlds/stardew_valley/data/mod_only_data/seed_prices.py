from ...strings.craftable_names import WildSeeds
from ...strings.fruit_tree_names import Sapling
from ...strings.seed_names import Seed

pelican_town_seed_prices = {
    Seed.amaranth: 35,
    Seed.artichoke: 15,
    Seed.beet: 10,
    Seed.blueberry: 40,
    Seed.bok_choy: 25,
    Seed.broccoli: 40,
    Seed.cactus: 75,
    Seed.carrot: 15,
    Seed.cauliflower: 40,
    Seed.coffee: 15,
    Seed.corn: 75,
    Seed.cranberry: 120,
    Seed.eggplant: 10,
    Seed.fairy: 100,
    Seed.garlic: 20,
    Seed.grape: 30,
    Seed.bean: 30,
    Seed.hops: 30,
    Seed.pepper: 20,
    Seed.jazz: 15,
    Seed.kale: 35,
    Seed.melon: 40,
    Seed.parsnip: 10,
    Seed.poppy: 50,
    Seed.potato: 25,
    Seed.powdermelon: 20,
    Seed.pumpkin: 50,
    Seed.qi_bean: 1,
    Seed.radish: 20,
    Seed.red_cabbage: 50,
    Seed.rhubarb: 50,
    Seed.starfruit: 200,
    Seed.strawberry: 50,
    Seed.spangle: 25,
    Seed.summer_squash: 20,
    Seed.sunflower: 100,
    Seed.rare_seed: 500,
    Seed.tomato: 25,
    Seed.tulip: 10,
    Seed.rice: 20,
    Seed.wheat: 5,
    Seed.yam: 30,
}

pelican_town_sapling_prices = {
    Sapling.apple: 1000,
    Sapling.apricot: 500,
    Sapling.cherry: 850,
    Sapling.orange: 1000,
    Sapling.peach: 1500,
    Sapling.pomegranate: 1500,
}

pelican_town_wild_seeds_prices = {
    WildSeeds.ancient: 30,
    WildSeeds.fall: 45,
    WildSeeds.fiber: 5,
    WildSeeds.spring: 35,
    WildSeeds.summer: 55,
    WildSeeds.tea_sapling: 250,
    WildSeeds.winter: 30,
}

ginger_island_seed_prices = {
    Seed.pineapple: 240,
    Seed.taro: 20,
}

ginger_island_sapling_prices = {
    Sapling.banana: 850,
    Sapling.mango: 850,
}

all_seed_prices = dict()
all_seed_prices.update(pelican_town_seed_prices)
all_seed_prices.update(pelican_town_sapling_prices)
all_seed_prices.update(pelican_town_wild_seeds_prices)
all_seed_prices.update(ginger_island_seed_prices)
all_seed_prices.update(ginger_island_sapling_prices)