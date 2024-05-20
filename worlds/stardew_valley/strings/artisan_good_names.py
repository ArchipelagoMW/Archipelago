class ArtisanGood:
    honey = "Honey"
    oak_resin = "Oak Resin"
    pine_tar = "Pine Tar"
    maple_syrup = "Maple Syrup"
    truffle_oil = "Truffle Oil"
    cheese = "Cheese"
    goat_cheese = "Goat Cheese"
    jelly = "Jelly"
    pickles = "Pickles"
    wine = "Wine"
    juice = "Juice"
    cloth = "Cloth"
    pale_ale = "Pale Ale"
    aged_roe = "Aged Roe"
    battery_pack = "Battery Pack"
    mayonnaise = "Mayonnaise"
    duck_mayonnaise = "Duck Mayonnaise"
    dinosaur_mayonnaise = "Dinosaur Mayonnaise"
    void_mayonnaise = "Void Mayonnaise"
    caviar = "Caviar"
    green_tea = "Green Tea"
    mead = "Mead"
    mystic_syrup = "Mystic Syrup"
    dried_fruit = "Dried Fruit"
    dried_mushroom = "Dried Mushrooms"
    raisins = "Raisins"
    stardrop_tea = "Stardrop Tea"
    smoked_fish = "Smoked Fish"
    targeted_bait = "Targeted Bait"

    @classmethod
    def specific_wine(cls, fruit: str) -> str:
        return f"Wine [{fruit}]"

    @classmethod
    def specific_juice(cls, vegetable: str) -> str:
        return f"Juice [{vegetable}]"

    @classmethod
    def specific_jelly(cls, fruit: str) -> str:
        return f"Jelly [{fruit}]"

    @classmethod
    def specific_pickles(cls, vegetable: str) -> str:
        return f"Pickles [{vegetable}]"

    @classmethod
    def specific_dried(cls, food: str) -> str:
        return f"Dried [{food}]"

    @classmethod
    def specific_smoked(cls, fish: str) -> str:
        return f"Smoked [{fish}]"


class ModArtisanGood:
    pterodactyl_egg = "Pterodactyl Egg"
