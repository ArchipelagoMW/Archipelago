from ...strings.crop_names import Fruit, Vegetable
from ...strings.fish_names import WaterItem
from ...strings.flower_names import Flower
from ...strings.forageable_names import Mushroom, Forageable
from ...strings.material_names import Material
from ...strings.seed_names import Seed

pelican_town_fruit_sell_prices = {
    Fruit.ancient_fruit: 550,
    Fruit.apple: 100,
    Fruit.apricot: 50,
    Fruit.blueberry: 50,
    Fruit.cherry: 80,
    Fruit.cranberries: 75,
    Fruit.grape: 80,
    Fruit.hot_pepper: 40,
    Fruit.melon: 250,
    Fruit.orange: 100,
    Fruit.peach: 140,
    Fruit.pineapple: 300,
    Fruit.pomegranate: 140,
    Fruit.powdermelon: 60,
    Fruit.qi_fruit: 1,
    Fruit.rhubarb: 220,
    Fruit.starfruit: 750,
    Fruit.strawberry: 120,
    Fruit.sweet_gem_berry: 3000,
}

pelican_town_vegetable_sell_prices = {
    Vegetable.amaranth: 150,
    Vegetable.artichoke: 160,
    Vegetable.beet: 100,
    Vegetable.bok_choy: 80,
    Vegetable.broccoli: 70,
    Vegetable.carrot: 35,
    Vegetable.cauliflower: 175,
    Seed.coffee: 15,
    Vegetable.corn: 50,
    Vegetable.eggplant: 60,
    Vegetable.garlic: 60,
    Vegetable.green_bean: 40,
    Vegetable.hops: 25,
    Vegetable.kale: 110,
    Vegetable.parsnip: 35,
    Vegetable.potato: 80,
    Vegetable.pumpkin: 320,
    Vegetable.radish: 90,
    Vegetable.red_cabbage: 260,
    Vegetable.summer_squash: 45,
    Vegetable.tea_leaves: 50,
    Vegetable.tomato: 60,
    Vegetable.unmilled_rice: 30,
    Vegetable.wheat: 25,
    Vegetable.yam: 160,
}

pelican_town_flowers_sell_prices = {
    Flower.blue_jazz: 50,
    Flower.fairy_rose: 290,
    Flower.poppy: 140,
    Flower.summer_spangle: 90,
    Flower.sunflower: 80,
    Flower.tulip: 30,
}

pelican_town_forage_sell_prices = {
    Forageable.blackberry: 20,
    Forageable.cactus_fruit: 75,
    Forageable.cave_carrot: 25,
    Forageable.coconut: 100,
    Forageable.crocus: 60,
    Forageable.crystal_fruit: 150,
    Forageable.daffodil: 30,
    Forageable.dandelion: 40,
    Forageable.fiddlehead_fern: 90,
    Forageable.hazelnut: 90,
    Forageable.holly: 80,
    Forageable.leek: 60,
    Forageable.salmonberry: 5,
    Forageable.snow_yam: 100,
    Forageable.spice_berry: 80,
    Forageable.spring_onion: 8,
    Forageable.sweet_pea: 50,
    Forageable.wild_horseradish: 50,
    Forageable.wild_plum: 80,
    Forageable.winter_root: 70,
    Material.sap: 2,
    Mushroom.chanterelle: 160,
    Mushroom.common: 40,
    Mushroom.morel: 150,
    Mushroom.purple: 250,
    Mushroom.red: 75,
    WaterItem.coral: 80,
    WaterItem.nautilus_shell: 120,
    WaterItem.sea_urchin: 160,
}

ginger_island_fruit_sell_prices = {
    Fruit.banana: 150,
    Fruit.mango: 130,
}

ginger_island_vegetable_sell_prices = {
    Vegetable.taro_root: 100,
}

ginger_island_forage_sell_prices = {
    Forageable.ginger: 60,
    Mushroom.magma_cap: 400,
}

all_crop_sell_prices = dict()
all_crop_sell_prices.update(pelican_town_fruit_sell_prices)
all_crop_sell_prices.update(pelican_town_vegetable_sell_prices)
all_crop_sell_prices.update(pelican_town_flowers_sell_prices)
all_crop_sell_prices.update(pelican_town_forage_sell_prices)
all_crop_sell_prices.update(ginger_island_fruit_sell_prices)
all_crop_sell_prices.update(ginger_island_vegetable_sell_prices)
all_crop_sell_prices.update(ginger_island_forage_sell_prices)