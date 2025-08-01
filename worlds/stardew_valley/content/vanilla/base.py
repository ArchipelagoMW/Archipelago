from ..game_content import ContentPack, StardewContent
from ...data.artisan import MachineSource
from ...data.game_item import ItemTag, CustomRuleSource, GameItem
from ...data.harvest import HarvestFruitTreeSource, HarvestCropSource
from ...data.skill import Skill
from ...strings.artisan_good_names import ArtisanGood
from ...strings.craftable_names import WildSeeds
from ...strings.crop_names import Fruit, Vegetable
from ...strings.flower_names import Flower
from ...strings.food_names import Beverage
from ...strings.forageable_names import all_edible_mushrooms, Mushroom, Forageable
from ...strings.fruit_tree_names import Sapling
from ...strings.machine_names import Machine
from ...strings.monster_names import Monster
from ...strings.season_names import Season
from ...strings.seed_names import Seed
from ...strings.skill_names import Skill as SkillName

all_fruits = (
    Fruit.ancient_fruit, Fruit.apple, Fruit.apricot, Fruit.banana, Forageable.blackberry, Fruit.blueberry, Forageable.cactus_fruit, Fruit.cherry,
    Forageable.coconut, Fruit.cranberries, Forageable.crystal_fruit, Fruit.grape, Fruit.hot_pepper, Fruit.mango, Fruit.melon, Fruit.orange, Fruit.peach,
    Fruit.pineapple, Fruit.pomegranate, Fruit.powdermelon, Fruit.qi_fruit, Fruit.rhubarb, Forageable.salmonberry, Forageable.spice_berry, Fruit.starfruit,
    Fruit.strawberry
)

all_vegetables = (
    Vegetable.amaranth, Vegetable.artichoke, Vegetable.beet, Vegetable.bok_choy, Vegetable.broccoli, Vegetable.carrot, Vegetable.cauliflower,
    Vegetable.corn, Vegetable.eggplant, Forageable.fiddlehead_fern, Vegetable.garlic, Vegetable.green_bean, Vegetable.hops, Vegetable.kale,
    Vegetable.parsnip, Vegetable.potato, Vegetable.pumpkin, Vegetable.radish, Vegetable.red_cabbage, Vegetable.summer_squash, Vegetable.taro_root,
    Vegetable.tea_leaves, Vegetable.tomato, Vegetable.unmilled_rice, Vegetable.wheat, Vegetable.yam
)

non_juiceable_vegetables = (Vegetable.hops, Vegetable.tea_leaves, Vegetable.wheat, Vegetable.tea_leaves)


# This will hold items, skills and stuff that is available everywhere across the game, but not directly needing pelican town (crops, ore, foraging, etc.)
class BaseGameContentPack(ContentPack):

    def harvest_source_hook(self, content: StardewContent):
        coffee_starter = content.game_items[Seed.coffee_starter]
        content.game_items[Seed.coffee_starter] = GameItem(Seed.coffee, sources=coffee_starter.sources, tags=coffee_starter.tags)

        content.untag_item(WildSeeds.ancient, ItemTag.CROPSANITY_SEED)

        for fruit in all_fruits:
            content.tag_item(fruit, ItemTag.FRUIT)

        for vegetable in all_vegetables:
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

            if fruit.name == Fruit.grape:
                content.source_item(ArtisanGood.raisins, MachineSource(item=fruit.name, machine=Machine.dehydrator))
            else:
                dried_fruit = ArtisanGood.specific_dried_fruit(fruit.name)
                content.source_item(dried_fruit, MachineSource(item=fruit.name, machine=Machine.dehydrator))
                content.source_item(ArtisanGood.dried_fruit, MachineSource(item=fruit.name, machine=Machine.dehydrator))

            jelly = ArtisanGood.specific_jelly(fruit.name)
            content.source_item(jelly, MachineSource(item=fruit.name, machine=Machine.preserves_jar))
            content.source_item(ArtisanGood.jelly, MachineSource(item=fruit.name, machine=Machine.preserves_jar))

        for vegetable in tuple(content.find_tagged_items(ItemTag.VEGETABLE)):
            if vegetable.name not in non_juiceable_vegetables:
                juice = ArtisanGood.specific_juice(vegetable.name)
                content.source_item(juice, MachineSource(item=vegetable.name, machine=Machine.keg))
                content.source_item(ArtisanGood.juice, MachineSource(item=vegetable.name, machine=Machine.keg))

            pickles = ArtisanGood.specific_pickles(vegetable.name)
            content.source_item(pickles, MachineSource(item=vegetable.name, machine=Machine.preserves_jar))
            content.source_item(ArtisanGood.pickles, MachineSource(item=vegetable.name, machine=Machine.preserves_jar))

        for mushroom in tuple(content.find_tagged_items(ItemTag.EDIBLE_MUSHROOM)):
            dried_mushroom = ArtisanGood.specific_dried_mushroom(mushroom.name)
            content.source_item(dried_mushroom, MachineSource(item=mushroom.name, machine=Machine.dehydrator))
            content.source_item(ArtisanGood.dried_mushroom, MachineSource(item=mushroom.name, machine=Machine.dehydrator))

        # for fish in tuple(content.find_tagged_items(ItemTag.FISH)):
        #     smoked_fish = ArtisanGood.specific_smoked_fish(fish.name)
        #     content.source_item(smoked_fish, MachineSource(item=fish.name, machine=Machine.fish_smoker))
        #     content.source_item(ArtisanGood.smoked_fish, MachineSource(item=fish.name, machine=Machine.fish_smoker))


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
        Fruit.powdermelon: (HarvestCropSource(seed=Seed.powdermelon, seasons=(Season.winter,)),),
        Vegetable.summer_squash: (HarvestCropSource(seed=Seed.summer_squash, seasons=(Season.summer,)),),

        Fruit.strawberry: (HarvestCropSource(seed=Seed.strawberry, seasons=(Season.spring,)),),
        Fruit.sweet_gem_berry: (HarvestCropSource(seed=Seed.rare_seed, seasons=(Season.fall,)),),
        Fruit.ancient_fruit: (HarvestCropSource(seed=WildSeeds.ancient, seasons=(Season.spring, Season.summer, Season.fall,)),),

        Seed.coffee_starter: (CustomRuleSource(lambda logic: logic.traveling_merchant.has_days(3) & logic.monster.can_kill_many(Monster.dust_sprite)),),
        Seed.coffee: (HarvestCropSource(seed=Seed.coffee_starter, seasons=(Season.spring, Season.summer,)),),

        Vegetable.tea_leaves: (
        CustomRuleSource(lambda logic: logic.has(WildSeeds.tea_sapling) & logic.time.has_lived_months(2) & logic.season.has_any_not_winter()),),
    },
    artisan_good_sources={
        Beverage.beer: (MachineSource(item=Vegetable.wheat, machine=Machine.keg),),
        # Ingredient.vinegar: (MachineSource(item=Ingredient.rice, machine=Machine.keg),),
        Beverage.coffee: (MachineSource(item=Seed.coffee, machine=Machine.keg),
                          CustomRuleSource(lambda logic: logic.has(Machine.coffee_maker)),
                          CustomRuleSource(lambda logic: logic.has("Hot Java Ring"))),
        ArtisanGood.green_tea: (MachineSource(item=Vegetable.tea_leaves, machine=Machine.keg),),
        ArtisanGood.mead: (MachineSource(item=ArtisanGood.honey, machine=Machine.keg),),
        ArtisanGood.pale_ale: (MachineSource(item=Vegetable.hops, machine=Machine.keg),),
    },
    skills=(
        Skill(SkillName.farming, has_mastery=True),
        Skill(SkillName.foraging, has_mastery=True),
        Skill(SkillName.fishing, has_mastery=True),
        Skill(SkillName.mining, has_mastery=True),
        Skill(SkillName.combat, has_mastery=True),
    )
)
