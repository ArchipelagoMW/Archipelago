from typing import Dict, List


class Catalogue:
    wizard = "Wizard Catalogue"
    furniture = "Furniture Catalogue"


items_by_catalogue: Dict[str, List[str]] = dict()


def catalogue_item(item: str, catalogue: str) -> str:
    if catalogue not in items_by_catalogue:
        items_by_catalogue[catalogue] = []
    items_by_catalogue[catalogue].append(item)
    return item


def wizard_catalogue_item(item: str) -> str:
    return catalogue_item(item, Catalogue.wizard)


def furniture_catalogue_item(item: str) -> str:
    return catalogue_item(item, Catalogue.furniture)


class CatalogueItem:
    wizard_bed = wizard_catalogue_item("Wizard Bed")
    wizard_dresser = wizard_catalogue_item("Wizard Dresser")
    wizard_chair = wizard_catalogue_item("Wizard Chair")
    wizard_stool = wizard_catalogue_item("Wizard Stool")
    wizard_table = wizard_catalogue_item("Wizard Table")
    wizard_tea_table = wizard_catalogue_item("Wizard Tea Table")
    wizard_end_table = wizard_catalogue_item("Wizard End Table")
    wizard_bookcase = wizard_catalogue_item("Wizard Bookcase")
    large_wizard_bookcase = wizard_catalogue_item("Large Wizard Bookcase")
    short_wizard_bookcase = wizard_catalogue_item("Short Wizard Bookcase")
    small_wizard_bookcase = wizard_catalogue_item("Small Wizard Bookcase")
    wizard_study = wizard_catalogue_item("Wizard Study")
    wizard_bookshelf = wizard_catalogue_item("Wizard Bookshelf")
    elixir_shelf = wizard_catalogue_item("Elixir Shelf")
    small_elixir_shelf = wizard_catalogue_item("Small Elixir Shelf")
    stacked_elixir_shelf = wizard_catalogue_item("Stacked Elixir Shelf")
    small_stacked_elixir_shelf = wizard_catalogue_item("Small Stacked Elixir Shelf")
    elixir_table = wizard_catalogue_item("Elixir Table")
    long_elixir_table = wizard_catalogue_item("Long Elixir Table")
    two_elixirs = wizard_catalogue_item("Two Elixirs")
    elixir_bundle = wizard_catalogue_item("Elixir Bundle")
    cauldron = wizard_catalogue_item("Cauldron")
    wizard_fireplace = wizard_catalogue_item("Wizard Fireplace")
    crystal_ball = wizard_catalogue_item("Crystal Ball")
    amethyst_crystal_ball = wizard_catalogue_item("Amethyst Crystal Ball")
    aquamarine_crystal_ball = wizard_catalogue_item("Aquamarine Crystal Ball")
    emerald_crystal_ball = wizard_catalogue_item("Emerald Crystal Ball")
    ruby_crystal_ball = wizard_catalogue_item("Ruby Crystal Ball")
    topaz_crystal_ball = wizard_catalogue_item("Topaz Crystal Ball")
    blue_book = wizard_catalogue_item("Blue Book")
    fallen_blue_book = wizard_catalogue_item("Fallen Blue Book")
    brown_book = wizard_catalogue_item("Brown Book")
    fallen_brown_book = wizard_catalogue_item("Fallen Brown Book")
    green_book = wizard_catalogue_item("Green Book")
    fallen_green_book = wizard_catalogue_item("Fallen Green Book")
    purple_book = wizard_catalogue_item("Purple Book")
    fallen_purple_book = wizard_catalogue_item("Fallen Purple Book")
    red_book = wizard_catalogue_item("Red Book")
    fallen_red_book = wizard_catalogue_item("Fallen Red Book")
    yellow_book = wizard_catalogue_item("Yellow Book")
    fallen_yellow_book = wizard_catalogue_item("Fallen Yellow Book")
    book_pile = wizard_catalogue_item("Book Pile")
    large_book_pile = wizard_catalogue_item("Large Book Pile")
    small_book_pile = wizard_catalogue_item("Small Book Pile")
    book_stack = wizard_catalogue_item("Book Stack")
    large_book_stack = wizard_catalogue_item("Large Book Stack")
    small_book_stack = wizard_catalogue_item("Small Book Stack")
    decorative_wizard_door = wizard_catalogue_item("Decorative Wizard Door")
    glyph = wizard_catalogue_item("Glyph")
    runes = wizard_catalogue_item("'Runes'")
    void_swirlds = wizard_catalogue_item("'Void Swirlds'")
    wizards_tower = wizard_catalogue_item("'Wizard's Tower'")
    witchs_broom = wizard_catalogue_item("Witch's Broom")
    rune_rug = wizard_catalogue_item("Rune Rug")
    starry_moon_rug = wizard_catalogue_item("Starry Moon Rug")
    swirld_rug = wizard_catalogue_item("Swirld Rug")
    wizard_cushion = wizard_catalogue_item("Wizard Cushion")
    dark_wizard_cushion = wizard_catalogue_item("Dark Wizard Cushion")
    wizard_lamp = wizard_catalogue_item("Wizard Lamp")
    potted_red_mushroom = wizard_catalogue_item("Potted Red Mushroom")
    curly_tree = wizard_catalogue_item("Curly Tree")
    swamp_plant = wizard_catalogue_item("Swamp Plant")
    stone_flooring = wizard_catalogue_item("Stone Flooring")

    stone_flooring = furniture_catalogue_item("Country Lamp")
    box_lamp = furniture_catalogue_item("Box Lamp")
    modern_lamp = furniture_catalogue_item("Modern Lamp")
    classic_lamp = furniture_catalogue_item("Classic Lamp")
    candle_lamp = furniture_catalogue_item("Candle Lamp")
    ornate_lamp = furniture_catalogue_item("Ornate Lamp")
