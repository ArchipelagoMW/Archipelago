from ...strings.craftable_names import WildSeeds
from ...strings.fruit_tree_names import Sapling
from ...strings.seed_names import Seed

pelican_town_seed_growth_times = {
    Seed.amaranth: 7,
    Seed.artichoke: 8,
    Seed.beet: 6,
    Seed.blueberry: 13,
    Seed.bok_choy: 4,
    Seed.broccoli: 8,
    Seed.cactus: 12,
    Seed.carrot: 3,
    Seed.cauliflower: 12,
    Seed.coffee: 10,
    Seed.corn: 14,
    Seed.cranberry: 7,
    Seed.eggplant: 5,
    Seed.fairy: 12,
    Seed.garlic: 4,
    Seed.grape: 10,
    Seed.bean: 10,
    Seed.hops: 11,
    Seed.pepper: 5,
    Seed.jazz: 7,
    Seed.kale: 6,
    Seed.melon: 12,
    Seed.parsnip: 4,
    Seed.poppy: 7,
    Seed.potato: 6,
    Seed.powdermelon: 7,
    Seed.pumpkin: 13,
    # Seed.qi_bean: 4, Can't randomize this... or the quest will become impossible I think?
    Seed.radish: 6,
    Seed.red_cabbage: 9,
    Seed.rhubarb: 13,
    Seed.starfruit: 13,
    Seed.strawberry: 8,
    Seed.spangle: 8,
    Seed.summer_squash: 6,
    Seed.sunflower: 8,
    Seed.rare_seed: 24,
    Seed.tomato: 11,
    Seed.tulip: 6,
    Seed.rice: 8,
    Seed.wheat: 4,
    Seed.yam: 10,
}

pelican_town_sapling_growth_times = {
    Sapling.apple: 28,
    Sapling.apricot: 28,
    Sapling.cherry: 28,
    Sapling.orange: 28,
    Sapling.peach: 28,
    Sapling.pomegranate: 28,
}

pelican_town_wild_seeds_growth_times = {
    WildSeeds.ancient: 28,
    WildSeeds.fall: 7,
    WildSeeds.fiber: 7,
    WildSeeds.spring: 7,
    WildSeeds.summer: 7,
    WildSeeds.tea_sapling: 20,
    WildSeeds.winter: 7,
}

ginger_island_seed_growth_times = {
    Seed.pineapple: 14,
    Seed.taro: 10,
}

ginger_island_sapling_growth_times = {
    Sapling.banana: 28,
    Sapling.mango: 28,
}

all_growth_times = dict()
all_growth_times.update(pelican_town_seed_growth_times)
all_growth_times.update(pelican_town_sapling_growth_times)
all_growth_times.update(pelican_town_wild_seeds_growth_times)
all_growth_times.update(ginger_island_seed_growth_times)
all_growth_times.update(ginger_island_sapling_growth_times)