all_edible_mushrooms = []


def mushroom(name: str) -> str:
    all_edible_mushrooms.append(name)
    return name


class Mushroom:
    any_edible = "Any Edible Mushroom"
    chanterelle = mushroom("Chanterelle")
    common = mushroom("Common Mushroom")
    morel = mushroom("Morel")
    purple = mushroom("Purple Mushroom")
    red = "Red Mushroom"  # Not in all mushrooms, as it can't be dried
    magma_cap = mushroom("Magma Cap")


class Forageable:
    blackberry = "Blackberry"
    cactus_fruit = "Cactus Fruit"
    cave_carrot = "Cave Carrot"
    coconut = "Coconut"
    crocus = "Crocus"
    crystal_fruit = "Crystal Fruit"
    daffodil = "Daffodil"
    dandelion = "Dandelion"
    fiddlehead_fern = "Fiddlehead Fern"
    ginger = "Ginger"
    hay = "Hay"
    hazelnut = "Hazelnut"
    holly = "Holly"
    journal_scrap = "Journal Scrap"
    leek = "Leek"
    secret_note = "Secret Note"
    spice_berry = "Spice Berry"
    sweet_pea = "Sweet Pea"
    wild_horseradish = "Wild Horseradish"
    wild_plum = "Wild Plum"
    winter_root = "Winter Root"
    dragon_tooth = "Dragon Tooth"
    rainbow_shell = "Rainbow Shell"
    salmonberry = "Salmonberry"
    snow_yam = "Snow Yam"
    spring_onion = "Spring Onion"


class SVEForage:
    ferngill_primrose = "Ferngill Primrose"
    goldenrod = "Goldenrod"
    winter_star_rose = "Winter Star Rose"
    bearberry = "Bearberry"
    poison_mushroom = "Poison Mushroom"
    red_baneberry = "Red Baneberry"
    conch = "Conch"
    dewdrop_berry = "Dewdrop Berry"
    sand_dollar = "Sand Dollar"
    golden_ocean_flower = "Golden Ocean Flower"
    four_leaf_clover = "Four Leaf Clover"
    mushroom_colony = "Mushroom Colony"
    rusty_blade = "Rusty Blade"
    rafflesia = "Rafflesia"
    thistle = "Thistle"


class DistantLandsForageable:
    brown_amanita = "Brown Amanita"
    swamp_herb = "Swamp Herb"


all_edible_mushrooms = tuple(all_edible_mushrooms)
