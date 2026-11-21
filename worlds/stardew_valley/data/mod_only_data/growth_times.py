from ...strings.craftable_names import WildSeeds
from ...strings.fruit_tree_names import Sapling
from ...strings.seed_names import Seed

# These should be added to content packs at some point
pelican_town_sapling_growth_times = {
    Sapling.apple: 28,
    Sapling.apricot: 28,
    Sapling.cherry: 28,
    Sapling.orange: 28,
    Sapling.peach: 28,
    Sapling.pomegranate: 28,
}

pelican_town_wild_seeds_growth_times = {
    # WildSeeds.ancient: 28,
    WildSeeds.fall: 7,
    WildSeeds.fiber: 7,
    WildSeeds.spring: 7,
    WildSeeds.summer: 7,
    WildSeeds.tea_sapling: 20,
    WildSeeds.winter: 7,
}

ginger_island_sapling_growth_times = {
    Sapling.banana: 28,
    Sapling.mango: 28,
}

all_growth_times = dict()
all_growth_times.update(pelican_town_sapling_growth_times)
all_growth_times.update(pelican_town_wild_seeds_growth_times)
all_growth_times.update(ginger_island_sapling_growth_times)

