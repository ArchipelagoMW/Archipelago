all_vegetables = []


def veggie(name: str) -> str:
    all_vegetables.append(name)
    return name


class Fruit:
    sweet_gem_berry = "Sweet Gem Berry"
    any = "Any Fruit"
    blueberry = "Blueberry"
    melon = "Melon"
    apple = "Apple"
    apricot = "Apricot"
    cherry = "Cherry"
    orange = "Orange"
    peach = "Peach"
    pomegranate = "Pomegranate"
    banana = "Banana"
    mango = "Mango"
    pineapple = "Pineapple"
    ancient_fruit = "Ancient Fruit"
    strawberry = "Strawberry"
    starfruit = "Starfruit"
    rhubarb = "Rhubarb"
    grape = "Grape"
    cranberries = "Cranberries"
    hot_pepper = "Hot Pepper"
    powdermelon = "Powdermelon"
    qi_fruit = "Qi Fruit"


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
    carrot = veggie("Carrot")
    summer_squash = veggie("Summer Squash")
    broccoli = veggie("Broccoli")


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
