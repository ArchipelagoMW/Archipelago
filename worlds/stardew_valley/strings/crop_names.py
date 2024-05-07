all_fruits = []
all_vegetables = []


def veggie(name: str) -> str:
    all_vegetables.append(name)
    return name


def fruity(name: str) -> str:
    all_fruits.append(name)
    return name


class Fruit:
    sweet_gem_berry = fruity("Sweet Gem Berry")
    any = "Any Fruit"
    blueberry = fruity("Blueberry")
    melon = fruity("Melon")
    apple = fruity("Apple")
    apricot = fruity("Apricot")
    cherry = fruity("Cherry")
    orange = fruity("Orange")
    peach = fruity("Peach")
    pomegranate = fruity("Pomegranate")
    banana = fruity("Banana")
    mango = fruity("Mango")
    pineapple = fruity("Pineapple")
    ancient_fruit = fruity("Ancient Fruit")
    strawberry = fruity("Strawberry")
    starfruit = fruity("Starfruit")
    rhubarb = fruity("Rhubarb")
    grape = fruity("Grape")
    cranberries = fruity("Cranberries")
    hot_pepper = fruity("Hot Pepper")


class Vegetable:
    any = "Any Vegetable"
    parsnip = veggie("Parsnip")
    garlic = veggie("Garlic")
    bok_choy = "Bok Choy"
    wheat = "Wheat"
    potato = veggie("Potato")
    corn = veggie("Corn")
    tomato = veggie("Tomato")
    pumpkin = veggie("Pumpkin")
    unmilled_rice = veggie("Unmilled Rice")
    beet = veggie("Beet")
    hops = "Hops"
    cauliflower = veggie("Cauliflower")
    amaranth = veggie("Amaranth")
    kale = veggie("Kale")
    artichoke = veggie("Artichoke")
    tea_leaves = "Tea Leaves"
    eggplant = veggie("Eggplant")
    green_bean = veggie("Green Bean")
    red_cabbage = veggie("Red Cabbage")
    yam = veggie("Yam")
    radish = veggie("Radish")
    taro_root = veggie("Taro Root")


class SVEFruit:
    slime_berry = "Slime Berry"
    monster_fruit = "Monster Fruit"
    salal_berry = "Salal Berry"


class SVEVegetable:
    monster_mushroom = "Monster Mushroom"
    void_root = "Void Root"
    ancient_fiber = "Ancient Fiber"


class DistantLandsCrop:
    void_mint = "Void Mint Leaves"
    vile_ancient_fruit = "Vile Ancient Fruit"


all_vegetables = tuple(all_vegetables)
all_fruits = tuple(all_fruits)
