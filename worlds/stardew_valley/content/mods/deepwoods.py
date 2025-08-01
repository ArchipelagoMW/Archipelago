from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ...data.harvest import ForagingSource
from ...mods.mod_data import ModNames
from ...strings.crop_names import Fruit
from ...strings.flower_names import Flower
from ...strings.region_names import DeepWoodsRegion
from ...strings.season_names import Season

register_mod_content_pack(ContentPack(
    ModNames.deepwoods,
    harvest_sources={
        # Deep enough to have seen such a tree at least once
        Fruit.apple: (ForagingSource(regions=(DeepWoodsRegion.floor_10,)),),
        Fruit.apricot: (ForagingSource(regions=(DeepWoodsRegion.floor_10,)),),
        Fruit.cherry: (ForagingSource(regions=(DeepWoodsRegion.floor_10,)),),
        Fruit.orange: (ForagingSource(regions=(DeepWoodsRegion.floor_10,)),),
        Fruit.peach: (ForagingSource(regions=(DeepWoodsRegion.floor_10,)),),
        Fruit.pomegranate: (ForagingSource(regions=(DeepWoodsRegion.floor_10,)),),
        Fruit.mango: (ForagingSource(regions=(DeepWoodsRegion.floor_10,)),),

        Flower.tulip: (ForagingSource(seasons=Season.not_winter, regions=(DeepWoodsRegion.floor_10,)),),
        Flower.blue_jazz: (ForagingSource(regions=(DeepWoodsRegion.floor_10,)),),
        Flower.summer_spangle: (ForagingSource(seasons=Season.not_winter, regions=(DeepWoodsRegion.floor_10,)),),
        Flower.poppy: (ForagingSource(seasons=Season.not_winter, regions=(DeepWoodsRegion.floor_10,)),),
        Flower.fairy_rose: (ForagingSource(regions=(DeepWoodsRegion.floor_10,)),),
    }
))
