
from BaseClasses import Item, ItemClassification

buildings_processing = {
    "Cutter": ItemClassification.progression,
    "Rotator": ItemClassification.progression,
    "Painter": ItemClassification.progression,
    "Rotator (CCW)": ItemClassification.useful,
    "Color Mixer": ItemClassification.progression,
    "Stacker": ItemClassification.progression,
    "Quad Cutter": ItemClassification.useful,
    "Double Painter": ItemClassification.useful,
    "Rotator (180°)": ItemClassification.useful,
    "Quad Painter": ItemClassification.useful
}

# Routing buildings are not needed to complete the game, but building factories without balancers and tunnels
# would be unreasonably complicated and time-consuming
buildings_routing = {
    "Balancer": ItemClassification.progression,
    "Tunnel": ItemClassification.progression,
    "Compact Merger": ItemClassification.useful,
    "Tunnel Tier II": ItemClassification.useful,
    "Compact Splitter": ItemClassification.useful
}

buildings_other = {
    "Trash": ItemClassification.progression,
    "Chaining Extractor": ItemClassification.useful
}

buildings_top_row = {
    "Belt Reader": ItemClassification.progression,
    "Storage": ItemClassification.progression,
    "Item Filter": ItemClassification.progression,
    "Display": ItemClassification.useful
}

buildings_wires = {
    "Wires": ItemClassification.progression,
    "Constant Signal": ItemClassification.useful,
    "Logic Gates": ItemClassification.progression,
    "Virtual Processing": ItemClassification.progression
}

gameplay_unlocks = {
    "Blueprints": ItemClassification.progression
}

upgrades = {
    "Big Routing Upgrade": ItemClassification.useful,
    "Big Extraction Upgrade": ItemClassification.useful,
    "Big Shape Processing Upgrade": ItemClassification.useful,
    "Big Color Processing Upgrade": ItemClassification.useful,
    "Small Routing Upgrade": ItemClassification.filler,
    "Small Extraction Upgrade": ItemClassification.filler,
    "Small Shape Processing Upgrade": ItemClassification.filler,
    "Small Color Processing Upgrade": ItemClassification.filler
}

bundles = {
    "Blueprint Shapes Bundle": ItemClassification.filler
}

traps = {
    "Inventory Draining Trap": ItemClassification.trap
}

item_table: dict[str, ItemClassification] = {
    **buildings_processing,
    **buildings_routing,
    **buildings_other,
    **buildings_top_row,
    **buildings_wires,
    **gameplay_unlocks,
    **upgrades,
    **bundles,
    **traps
}

big_upgrades = [
    "Big Routing Upgrade",
    "Big Extraction Upgrade",
    "Big Shape Processing Upgrade",
    "Big Color Processing Upgrade"
]

small_upgrades = [
    "Small Routing Upgrade",
    "Small Extraction Upgrade",
    "Small Shape Processing Upgrade",
    "Small Color Processing Upgrade"
]


def filler(random: float) -> str:
    """Returns a random filler item."""
    if random < 0.16:  # These float values are intentionally just estimates of 1/6 and 2/3
        return big_upgrades[int(random*4/0.16)]
    elif random < 0.66:
        return small_upgrades[int((random-0.16)*4/0.5)]  # Yes, I want this calculation to be written that way
    else:
        return "Blueprint Shapes Bundle"


item_descriptions = {  # TODO
    # Items
    "Balancer": "A routing building, that can merge two belts into one, split a belt in two, " +
                "or balance the items of two belts",
    "Tunnel": "A routing building consisting of two parts, that allows for gaps in belts",
    "Compact Merger": "A small routing building, that merges two belts into one",
    "Tunnel Tier II": "A routing building consisting of two parts, that allows for even longer gaps in belts",
    "Compact Splitter": "A small routing building, that splits a belt in two",
    "Cutter": "A processing building, that cuts shapes vertically in two halves",
    "Rotator": "A processing building, that rotates shapes 90 degrees clockwise",
    "Painter": "A processing building, that paints shapes in a given color",
    "Rotator (CCW)": "A processing building, that rotates shapes 90 degrees counter-clockwise",
    "Color Mixer": "A processing building, that mixes two colors together to create a new one",
    "Stacker": "A processing building, that combines two shapes with missing parts or puts one on top of the other",
    "Quad Cutter": "A processing building, that cuts shapes in four quarter parts",
    "Double Painter": "A processing building, that paints two shapes in a given color",
    "Rotator (180)": "A processing building, that rotates shapes 180 degrees",
    "Quad Painter": "A processing building, that paint each quarter of a shape in another given color and requires " +
                    "wire inputs for each color to work",
    "Trash": "A building, that destroys unused shapes",
    "Chaining Extractor": "An upgrade to extractors, that can increase the output without balancers or mergers",
    "Belt Reader": "TODO",
    "Storage": "TODO",
    "Item Filter": "TODO",
    "Display": "TODO",
    "Wires": "TODO",
    "Constant Signal": "TODO",
    "Logic Gates": "TODO",
    "Virtual Processing": "TODO",
    "Blueprints": "TODO",
    "Big Routing Upgrade": "An upgrade, that adds 1 to the speed multiplier of belts, distributors, and tunnels",
    "Big Extraction Upgrade": "TODO",
    "Big Shape Processing Upgrade": "TODO",
    "Big Color Processing Upgrade": "TODO",
    "Small Routing Upgrade": "TODO",
    "Small Extraction Upgrade": "TODO",
    "Small Shape Processing Upgrade": "TODO",
    "Small Color Processing Upgrade": "TODO",
    "Blueprint Shapes Bundle": "TODO",
    "Inventory Draining Trap": "TODO"
}


class ShapezItem(Item):
    game = "shapez"
