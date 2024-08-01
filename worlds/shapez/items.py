from BaseClasses import Item

item_descriptions = {
    # Items
    "Big Belt Upgrade": "An upgrade, that adds 1 to the speed multiplier of belts, distributors, and tunnels",
    # Item groups
    "Buildings": "The objects, that you place on the grid to modify your shapes in different ways"
}


class ShapezItem(Item):
    game: str = "Shapez"
