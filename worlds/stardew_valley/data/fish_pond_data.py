from typing import Dict

from ..strings.animal_product_names import AnimalProduct
from ..strings.artisan_good_names import ArtisanGood
from ..strings.crop_names import Fruit
from ..strings.fish_names import Fish, WaterItem
from ..strings.food_names import Meal
from ..strings.forageable_names import Forageable
from ..strings.metal_names import Mineral, Ore
from ..strings.monster_drop_names import Loot
from ..strings.seed_names import Seed

# Some of these are commented out, because they shouldn't be used, because they cause a loop on themselves, even if the loop is one of many ways to complete the quest
# I don't know the correct architectural way to fix this. So in the meantime, obtaining these items from fish ponds is not in logic

# Dictionary of fish pond requests, in the format of Dict[fish_name, Dict[population, Dict[item_name, item_amount]]]
fish_pond_quests: Dict[str, Dict[int, Dict[str, int]]] = {
    Fish.blobfish: {
        1: {WaterItem.coral: 3, Mineral.frozen_tear: 2, WaterItem.sea_urchin: 2, },
        3: {Seed.coffee: 5, ArtisanGood.mayonnaise: 1, Meal.pizza: 1, },
        5: {Meal.cookie: 1, ArtisanGood.green_tea: 1, ArtisanGood.wine: 1, },
        7: {Forageable.rainbow_shell: 1, Meal.rice_pudding: 1, },
    },
    # Fish.lava_eel: {
    #     1: {Mineral.fire_quartz: 3, },
    #     3: {"Basalt": 1, Mineral.diamond: 2, Artifact.dwarf_scroll_iii: 1, },
    #     5: {Bomb.mega_bomb: 2, },
    #     7: {MetalBar.iridium: 1, },
    # },
    Fish.lionfish: {
        3: {Forageable.ginger: 3, Fruit.pineapple: 1, },
        5: {Fruit.mango: 1, },
    },
    # Fish.octopus: {
    #     3: {WaterItem.coral: 3, ArtisanGood.honey: 1, Fish.oyster: 1, MetalBar.quartz: 3, },
    #     5: {Fossil.dried_starfish: 1, Mineral.emerald: 2, Geode.omni: 2, Mushroom.purple: 2, },
    #     7: {ArtisanGood.green_tea: 1, },
    # },
    # Fish.super_cucumber: {
    #     3: {WaterItem.coral: 3, ArtisanGood.honey: 1, Fish.oyster: 1, Trash.driftwood: 3, MetalBar.quartz: 3, },
    #     5: {Fossil.dried_starfish: 1, Mineral.emerald: 2, Geode.omni: 2, Mushroom.purple: 2 },
    #     7: {Mineral.diamond: 1, MetalBar.gold: 3, Ore.iridium: 1, ArtisanGood.jelly: 1, ArtisanGood.pickles: 1, WaterItem.sea_urchin: 2 },
    # },
    Fish.void_salmon: {
        1: {Loot.void_essence: 5, },
        3: {Loot.bat_wing: 10, },
        5: {Mineral.diamond: 1, AnimalProduct.void_egg: 1, },
        7: {Ore.iridium: 1, },
    },
}
