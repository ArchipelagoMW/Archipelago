from ..game_content import ContentPack, StardewContent
from ...data.artisan import MachineSource
from ...data.game_item import ItemTag, CustomSource
from ...data.harvest import HarvestFruitTreeSource, HarvestCropSource
from ...strings.artisan_good_names import ArtisanGood
from ...strings.craftable_names import WildSeeds
from ...strings.crop_names import Fruit, Vegetable, all_vegetables
from ...strings.flower_names import Flower
from ...strings.forageable_names import all_edible_mushrooms, Mushroom, Forageable
from ...strings.fruit_tree_names import Sapling
from ...strings.machine_names import Machine
from ...strings.season_names import Season
from ...strings.seed_names import Seed

all_fruits = (
    Fruit.ancient_fruit, Fruit.apple, Fruit.apricot, Fruit.banana, Forageable.blackberry, Fruit.blueberry, Forageable.cactus_fruit, Fruit.cherry,
    Forageable.coconut, Fruit.cranberries, Forageable.crystal_fruit, Fruit.grape, Fruit.hot_pepper, Fruit.mango, Fruit.melon, Fruit.orange, Fruit.peach,
    Fruit.pineapple, Fruit.pomegranate, Fruit.powdermelon, Fruit.qi_fruit, Fruit.rhubarb, Forageable.salmonberry, Forageable.spice_berry, Fruit.starfruit,
    Fruit.strawberry
)


# This will hold items, skills and stuff that is available everywhere across the game, but not directly needing pelican town (crops, ore, foraging, etc.)
class BaseGameContentPack(ContentPack):

    def harvest_source_hook(self, content: StardewContent):
        # TODO should make a fake item sourced on primary coffee bean sources (monsters & travelling merchant) and real coffee bean sourced harvesting so this
        #  tag is not needed
        content.tag_item(Seed.coffee, ItemTag.CROPSANITY, ItemTag.CROPSANITY_SEED)
        content.source_item(Seed.coffee, CustomSource())

        content.untag_item(WildSeeds.ancient, ItemTag.CROPSANITY_SEED)

        for fruit in all_fruits:
            content.tag_item(fruit, ItemTag.FRUIT)

        # TODO add Fiddlehead fern to vegetables
        for vegetable in all_vegetables:
            if vegetable == Vegetable.taro_root:
                continue

            content.tag_item(vegetable, ItemTag.VEGETABLE)

        for edible_mushroom in all_edible_mushrooms:
            if edible_mushroom == Mushroom.magma_cap:
                continue

            content.tag_item(edible_mushroom, ItemTag.EDIBLE_MUSHROOM)

    def finalize_hook(self, content: StardewContent):
        # FIXME I hate this design. A listener design pattern would be more appropriate so artisan good are register at the exact moment a FRUIT tag is added.
        for fruit in tuple(content.find_tagged_items(ItemTag.FRUIT)):
            wine = ArtisanGood.specific_wine(fruit.name)
            content.source_item(wine, MachineSource(item=fruit.name, machine=Machine.keg))
            content.source_item(ArtisanGood.wine, MachineSource(item=fruit.name, machine=Machine.keg))

            dried = ArtisanGood.specific_dried(fruit.name)
            content.source_item(dried, MachineSource(item=fruit.name, machine=Machine.dehydrator))

            jelly = ArtisanGood.specific_jelly(fruit.name)
            content.source_item(jelly, MachineSource(item=fruit.name, machine=Machine.preserves_jar))

        for vegetable in tuple(content.find_tagged_items(ItemTag.VEGETABLE)):
            juice = ArtisanGood.specific_juice(vegetable.name)
            content.source_item(juice, MachineSource(item=vegetable.name, machine=Machine.keg))

            pickles = ArtisanGood.specific_pickles(vegetable.name)
            content.source_item(pickles, MachineSource(item=vegetable.name, machine=Machine.preserves_jar))

        for mushroom in tuple(content.find_tagged_items(ItemTag.EDIBLE_MUSHROOM)):
            dried = ArtisanGood.specific_dried(mushroom.name)
            content.source_item(dried, MachineSource(item=mushroom.name, machine=Machine.dehydrator))


base_game = BaseGameContentPack(
    "Base game (Vanilla)",
    harvest_sources={
        # Fruit tree
        Fruit.apple: (HarvestFruitTreeSource(sapling=Sapling.apple, seasons=(Season.fall,)),),
        Fruit.apricot: (HarvestFruitTreeSource(sapling=Sapling.apricot, seasons=(Season.spring,)),),
        Fruit.cherry: (HarvestFruitTreeSource(sapling=Sapling.cherry, seasons=(Season.spring,)),),
        Fruit.orange: (HarvestFruitTreeSource(sapling=Sapling.orange, seasons=(Season.summer,)),),
        Fruit.peach: (HarvestFruitTreeSource(sapling=Sapling.peach, seasons=(Season.summer,)),),
        Fruit.pomegranate: (HarvestFruitTreeSource(sapling=Sapling.pomegranate, seasons=(Season.fall,)),),

        # Crops
        Vegetable.parsnip: (HarvestCropSource(seed=Seed.parsnip, seasons=(Season.spring,)),),
        Vegetable.green_bean: (HarvestCropSource(seed=Seed.bean, seasons=(Season.spring,)),),
        Vegetable.cauliflower: (HarvestCropSource(seed=Seed.cauliflower, seasons=(Season.spring,)),),
        Vegetable.potato: (HarvestCropSource(seed=Seed.potato, seasons=(Season.spring,)),),
        Flower.tulip: (HarvestCropSource(seed=Seed.tulip, seasons=(Season.spring,)),),
        Vegetable.kale: (HarvestCropSource(seed=Seed.kale, seasons=(Season.spring,)),),
        Flower.blue_jazz: (HarvestCropSource(seed=Seed.jazz, seasons=(Season.spring,)),),
        Vegetable.garlic: (HarvestCropSource(seed=Seed.garlic, seasons=(Season.spring,)),),
        Vegetable.unmilled_rice: (HarvestCropSource(seed=Seed.rice, seasons=(Season.spring,)),),

        Fruit.melon: (HarvestCropSource(seed=Seed.melon, seasons=(Season.summer,)),),
        Vegetable.tomato: (HarvestCropSource(seed=Seed.tomato, seasons=(Season.summer,)),),
        Fruit.blueberry: (HarvestCropSource(seed=Seed.blueberry, seasons=(Season.summer,)),),
        Fruit.hot_pepper: (HarvestCropSource(seed=Seed.pepper, seasons=(Season.summer,)),),
        Vegetable.wheat: (HarvestCropSource(seed=Seed.wheat, seasons=(Season.summer, Season.fall)),),
        Vegetable.radish: (HarvestCropSource(seed=Seed.radish, seasons=(Season.summer,)),),
        Flower.poppy: (HarvestCropSource(seed=Seed.poppy, seasons=(Season.summer,)),),
        Flower.summer_spangle: (HarvestCropSource(seed=Seed.spangle, seasons=(Season.summer,)),),
        Vegetable.hops: (HarvestCropSource(seed=Seed.hops, seasons=(Season.summer,)),),
        Vegetable.corn: (HarvestCropSource(seed=Seed.corn, seasons=(Season.summer, Season.fall)),),
        Flower.sunflower: (HarvestCropSource(seed=Seed.sunflower, seasons=(Season.summer, Season.fall)),),
        Vegetable.red_cabbage: (HarvestCropSource(seed=Seed.red_cabbage, seasons=(Season.summer,)),),

        Vegetable.eggplant: (HarvestCropSource(seed=Seed.eggplant, seasons=(Season.fall,)),),
        Vegetable.pumpkin: (HarvestCropSource(seed=Seed.pumpkin, seasons=(Season.fall,)),),
        Vegetable.bok_choy: (HarvestCropSource(seed=Seed.bok_choy, seasons=(Season.fall,)),),
        Vegetable.yam: (HarvestCropSource(seed=Seed.yam, seasons=(Season.fall,)),),
        Fruit.cranberries: (HarvestCropSource(seed=Seed.cranberry, seasons=(Season.fall,)),),
        Flower.fairy_rose: (HarvestCropSource(seed=Seed.fairy, seasons=(Season.fall,)),),
        Vegetable.amaranth: (HarvestCropSource(seed=Seed.amaranth, seasons=(Season.fall,)),),
        Fruit.grape: (HarvestCropSource(seed=Seed.grape, seasons=(Season.fall,)),),
        Vegetable.artichoke: (HarvestCropSource(seed=Seed.artichoke, seasons=(Season.fall,)),),

        Vegetable.broccoli: (HarvestCropSource(seed=Seed.broccoli, seasons=(Season.fall,)),),
        Vegetable.carrot: (HarvestCropSource(seed=Seed.carrot, seasons=(Season.spring,)),),
        Fruit.powdermelon: (HarvestCropSource(seed=Seed.powdermelon, seasons=(Season.summer,)),),
        Vegetable.summer_squash: (HarvestCropSource(seed=Seed.summer_squash, seasons=(Season.summer,)),),

        Fruit.strawberry: (HarvestCropSource(seed=Seed.strawberry, seasons=(Season.spring,)),),
        Fruit.sweet_gem_berry: (HarvestCropSource(seed=Seed.rare_seed, seasons=(Season.fall,)),),
        Fruit.ancient_fruit: (HarvestCropSource(seed=WildSeeds.ancient, seasons=(Season.spring, Season.summer, Season.fall,)),),
    }
)
