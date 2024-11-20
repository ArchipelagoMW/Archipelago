from . import SVContentPackTestBase
from ...data.artisan import MachineSource
from ...strings.artisan_good_names import ArtisanGood
from ...strings.crop_names import Vegetable, Fruit
from ...strings.food_names import Beverage
from ...strings.forageable_names import Forageable
from ...strings.machine_names import Machine
from ...strings.seed_names import Seed

wine_base_fruits = [
    Fruit.ancient_fruit, Fruit.apple, Fruit.apricot, Forageable.blackberry, Fruit.blueberry, Forageable.cactus_fruit, Fruit.cherry,
    Forageable.coconut, Fruit.cranberries, Forageable.crystal_fruit, Fruit.grape, Fruit.hot_pepper, Fruit.melon, Fruit.orange, Fruit.peach,
    Fruit.pomegranate, Fruit.powdermelon, Fruit.rhubarb, Forageable.salmonberry, Forageable.spice_berry, Fruit.starfruit, Fruit.strawberry
]

juice_base_vegetables = (
    Vegetable.amaranth, Vegetable.artichoke, Vegetable.beet, Vegetable.bok_choy, Vegetable.broccoli, Vegetable.carrot, Vegetable.cauliflower,
    Vegetable.corn, Vegetable.eggplant, Forageable.fiddlehead_fern, Vegetable.garlic, Vegetable.green_bean, Vegetable.kale, Vegetable.parsnip, Vegetable.potato,
    Vegetable.pumpkin, Vegetable.radish, Vegetable.red_cabbage, Vegetable.summer_squash, Vegetable.tomato, Vegetable.unmilled_rice, Vegetable.yam
)

non_juice_base_vegetables = (
    Vegetable.hops, Vegetable.tea_leaves, Vegetable.wheat
)


class TestArtisanEquipment(SVContentPackTestBase):

    def test_keg_special_recipes(self):
        self.assertIn(MachineSource(item=Vegetable.wheat, machine=Machine.keg), self.content.game_items[Beverage.beer].sources)
        # self.assertIn(MachineSource(item=Ingredient.rice, machine=Machine.keg), self.content.game_items[Ingredient.vinegar].sources)
        self.assertIn(MachineSource(item=Seed.coffee, machine=Machine.keg), self.content.game_items[Beverage.coffee].sources)
        self.assertIn(MachineSource(item=Vegetable.tea_leaves, machine=Machine.keg), self.content.game_items[ArtisanGood.green_tea].sources)
        self.assertIn(MachineSource(item=ArtisanGood.honey, machine=Machine.keg), self.content.game_items[ArtisanGood.mead].sources)
        self.assertIn(MachineSource(item=Vegetable.hops, machine=Machine.keg), self.content.game_items[ArtisanGood.pale_ale].sources)

    def test_fruits_can_be_made_into_wines(self):

        for fruit in wine_base_fruits:
            with self.subTest(fruit):
                self.assertIn(MachineSource(item=fruit, machine=Machine.keg), self.content.game_items[ArtisanGood.specific_wine(fruit)].sources)
                self.assertIn(MachineSource(item=fruit, machine=Machine.keg), self.content.game_items[ArtisanGood.wine].sources)

    def test_vegetables_can_be_made_into_juices(self):
        for vegetable in juice_base_vegetables:
            with self.subTest(vegetable):
                self.assertIn(MachineSource(item=vegetable, machine=Machine.keg), self.content.game_items[ArtisanGood.specific_juice(vegetable)].sources)
                self.assertIn(MachineSource(item=vegetable, machine=Machine.keg), self.content.game_items[ArtisanGood.juice].sources)

    def test_non_juice_vegetables_cannot_be_made_into_juices(self):
        for vegetable in non_juice_base_vegetables:
            with self.subTest(vegetable):
                self.assertNotIn(ArtisanGood.specific_juice(vegetable), self.content.game_items)
                self.assertNotIn(MachineSource(item=vegetable, machine=Machine.keg), self.content.game_items[ArtisanGood.juice].sources)
