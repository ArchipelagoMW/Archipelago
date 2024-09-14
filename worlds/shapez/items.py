from typing import Dict

from BaseClasses import Item, ItemClassification

buildings_processing = {
    "Cutter": ItemClassification.progression,
    "Rotator": ItemClassification.progression,
    "Painter": ItemClassification.progression,
    "Rotator (CCW)": ItemClassification.progression,
    "Color Mixer": ItemClassification.progression,
    "Stacker": ItemClassification.progression,
    "Quad Cutter": ItemClassification.progression,
    "Double Painter": ItemClassification.progression,
    "Rotator (180°)": ItemClassification.useful,
    "Quad Painter": ItemClassification.progression
}

# Routing buildings are not needed to complete the game, but building factories without balancers and tunnels
# would be unreasonably complicated and time-consuming
buildings_routing = {
    "Balancer": ItemClassification.progression,
    "Tunnel": ItemClassification.progression,
    "Compact Merger": ItemClassification.progression,
    "Tunnel Tier II": ItemClassification.progression,
    "Compact Splitter": ItemClassification.progression
}

buildings_other = {
    "Trash": ItemClassification.progression,
    "Chaining Extractor": ItemClassification.useful
}

buildings_top_row = {
    "Belt Reader": ItemClassification.progression,
    "Storage": ItemClassification.progression,
    "Switch": ItemClassification.progression,
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
    "Big Belt Upgrade": ItemClassification.progression,
    "Big Miner Upgrade": ItemClassification.useful,
    "Big Processors Upgrade": ItemClassification.useful,
    "Big Painting Upgrade": ItemClassification.useful,
    "Small Belt Upgrade": ItemClassification.filler,
    "Small Miner Upgrade": ItemClassification.filler,
    "Small Processors Upgrade": ItemClassification.filler,
    "Small Painting Upgrade": ItemClassification.filler
}

bundles = {
    "Blueprint Shapes Bundle": ItemClassification.filler,
    "Level Shapes Bundle": ItemClassification.filler,
    "Upgrade Shapes Bundle": ItemClassification.filler
}

standard_traps = {
    "Locked Building Trap": ItemClassification.trap,
    "Throttled Building Trap": ItemClassification.trap,
    "Malfunctioning Trap": ItemClassification.trap
}

random_draining_trap = {
    "Inventory Draining Trap": ItemClassification.trap
}

split_draining_traps = {
    "Blueprint Shapes Draining Trap": ItemClassification.trap,
    "Level Shapes Draining Trap": ItemClassification.trap,
    "Upgrade Shapes Draining Trap": ItemClassification.trap
}

belt_and_extractor = {
    "Belt": ItemClassification.progression,
    "Extractor": ItemClassification.progression
}

item_table: Dict[str, ItemClassification] = {
    **buildings_processing,
    **buildings_routing,
    **buildings_other,
    **buildings_top_row,
    **buildings_wires,
    **gameplay_unlocks,
    **upgrades,
    **bundles,
    **standard_traps,
    **random_draining_trap,
    **split_draining_traps,
    **belt_and_extractor
}

big_upgrades = [
    "Big Belt Upgrade",
    "Big Miner Upgrade",
    "Big Processors Upgrade",
    "Big Painting Upgrade"
]

small_upgrades = [
    "Small Belt Upgrade",
    "Small Miner Upgrade",
    "Small Processors Upgrade",
    "Small Painting Upgrade"
]


def trap(random: float, split_draining: bool) -> str:
    """Returns a random trap item."""
    random_value = (len(standard_traps)+1)*random
    if random_value >= 1:
        return list(standard_traps.keys())[int(random_value)-1]
    else:
        return "Inventory Draining Trap" \
            if not split_draining else list(split_draining_traps.keys())[int(random_value*3)]


def filler(random: float) -> str:
    """Returns a random filler item."""
    if random < 0.16:  # These float values are intentionally just estimates of 1/6 and 2/3
        return big_upgrades[int(random*4/0.16)]
    elif random < 0.66:
        return small_upgrades[int((random-0.16)*4/0.5)]  # Yes, I want this calculation to be written that way
    else:
        return list(bundles.keys())[int((random-0.66)*len(bundles)/0.34)]


item_descriptions = {
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
    "Rotator (180°)": "A processing building, that rotates shapes 180 degrees",
    "Quad Painter": "A processing building, that paint each quarter of a shape in another given color and requires " +
                    "wire inputs for each color to work",
    "Trash": "A building, that destroys unused shapes",
    "Chaining Extractor": "An upgrade to extractors, that can increase the output without balancers or mergers",
    "Belt Reader": "A wired building, that shows the average amount of items passing through per second",
    "Storage": "A building, that stores up to 5000 of a certain shape",
    "Switch": "A building, that sends a constant boolean signal",
    "Item Filter": "A wired building, that filters items based on wire input",
    "Display": "A wired building, that displays a shape or color based on wire input",
    "Wires": "The main building of the wires layer, that carries signals between other buildings",
    "Constant Signal": "A building on the wires layer, that sends a constant shape, color, or boolean signal",
    "Logic Gates": "Multiple buildings on the wires layer, that perform logical operations on wire signals",
    "Virtual Processing": "Multiple buildings on the wires layer, that process wire signals like processor buildings",
    "Blueprints": "A game mechanic, that allows copy-pasting multiple buildings at once",
    "Big Belt Upgrade": "An upgrade, that adds 1 to the speed multiplier of belts, distributors, and tunnels",
    "Big Miner Upgrade": "An upgrade, that adds 1 to the speed multiplier of extractors",
    "Big Processors Upgrade": "An upgrade, that adds 1 to the speed multiplier of cutters, rotators, and stackers",
    "Big Painting Upgrade": "An upgrade, that adds 1 to the speed multiplier of painters and color mixers",
    "Small Belt Upgrade": "An upgrade, that adds 0.1 to the speed multiplier of belts, distributors, and tunnels",
    "Small Miner Upgrade": "An upgrade, that adds 1 to the speed multiplier of extractors",
    "Small Processors Upgrade": "An upgrade, that adds 1 to the speed multiplier of cutters, rotators, and stackers",
    "Small Painting Upgrade": "An upgrade, that adds 1 to the speed multiplier of painters and color mixers",
    "Blueprint Shapes Bundle": "A bundle with 1000 blueprint shapes, instantly delivered to the hub",
    "Level Shapes Bundle": "A bundle with some shapes needed for the current level, " +
                           "instantly delivered to the hub",
    "Upgrade Shapes Bundle": "A bundle with some shapes needed for a random upgrade, " +
                           "instantly delivered to the hub",
    "Inventory Draining Trap": "Randomly drains either blueprint shapes, current level requirement shapes, " +
                               "or random upgrade requirement shapes, by half",
    "Blueprint Shapes Draining Trap": "Drains the stored blueprint shapes by half",
    "Level Shapes Draining Trap": "Drains the current level requirement shapes by half",
    "Upgrade Shapes Draining Trap": "Drains a random upgrade requirement shape by half",
    "Locked Building Trap": "Locks a random building from being placed for 15-60 seconds",
    "Throttled Building Trap": "Halves the speed of a random building for 15-60 seconds",
    "Malfunctioning Trap": "Makes a random building process items incorrectly for 15-60 seconds",
    "Belt": "One of the most important buildings in the game, that transports your shapes and colors from one " +
            "place to another",
    "Extractor": "One of the most important buildings in the game, that extracts shapes from those randomly " +
                 "generated patches"
}


class ShapezItem(Item):
    game = "shapez"
