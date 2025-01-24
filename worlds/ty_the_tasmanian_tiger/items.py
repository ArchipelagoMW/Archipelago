from collections import namedtuple
from typing import Dict

from BaseClasses import Item, ItemClassification, MultiWorld
from worlds.ty_the_tasmanian_tiger.options import Ty1Options


class Ty1Item(Item):
    game: str = "Ty the Tasmanian Tiger"


def create_single(name: str, world: MultiWorld, player: int):
    world.itempool.append(Ty1Item(name, ty1_item_table[name].classification, ty1_item_table[name].id, player))

def create_multiple(name: str, amount: int, world: MultiWorld, player: int):
    for i in range(amount):
        create_single(name, world, player)

def create_items(world: MultiWorld, options: Ty1Options, player: int):
    # Generic
    create_multiple("Fire Thunder Egg", 21, world, player) # Drop 3 TEs for bilby redundancy
    create_multiple("Ice Thunder Egg", 21, world, player)
    create_multiple("Air Thunder Egg", 21, world, player)
    create_multiple("Golden Cog", 90, world, player)

    # Bilbies
    create_multiple("Bilby - Two Up", 5, world, player)
    create_multiple("Bilby - WitP", 5, world, player)
    create_multiple("Bilby - Ship Rex", 5, world, player)
    create_multiple("Bilby - BotRT", 5, world, player)
    create_multiple("Bilby - Snow Worries", 5, world, player)
    create_multiple("Bilby - Outback Safari", 5, world, player)
    create_multiple("Bilby - LLPoF", 5, world, player)
    create_multiple("Bilby - BtBS", 5, world, player)
    create_multiple("Bilby - RMtS", 5, world, player)

    # Stopwatches 
    create_single("Stopwatch - Two Up", world, player)
    create_single("Stopwatch - WitP", world, player)
    create_single("Stopwatch - Ship Rex", world, player)
    create_single("Stopwatch - BotRT", world, player)
    create_single("Stopwatch - Snow Worries", world, player)
    create_single("Stopwatch - Outback Safari", world, player)
    create_single("Stopwatch - LLPoF", world, player)
    create_single("Stopwatch - BtBS", world, player)
    create_single("Stopwatch - RMtS", world, player)

    # Attributes
    if options.progressive_elementals:
        if options.start_with_boom:
            create_multiple("Progressive Rang", 8, world, player)
        else:
            create_multiple("Progressive Rang", 9, world, player)
    else:
        create_single("Second Rang", world, player)
        create_single("Swim", world, player)
        create_single("Aquarang", world, player)
        create_single("Dive", world, player)
        create_single("Flamerang", world, player)
        create_single("Frostyrang", world, player)
        create_single("Zappyrang", world, player)
        create_single("Doomarang", world, player)
        create_single("Extra Health", world, player)
        create_single("Zoomerang", world, player)
        create_single("Multirang", world, player)
        create_single("Infrarang", world, player)
        create_single("Megarang", world, player)
        create_single("Kaboomarang", world, player)
        create_single("Chronorang", world, player)
    
    # Levels
    if options.level_unlock_style != 0:
        if options.progressive_level:
            level_count = 12 if options.level_unlock_style == 1 else 9
            create_multiple("Progressive Level", level_count, world, player)
        else:
            create_single("Portal - WitP", world, player)
            create_single("Portal - Ship Rex", world, player)
            create_single("Portal - BotRT", world, player)
            create_single("Portal - Snow Worries", world, player)
            create_single("Portal - Outback Safari", world, player)
            create_single("Portal - LLPoF", world, player)
            create_single("Portal - BtBS", world, player)
            create_single("Portal - RMtS", world, player)
            create_single("Portal - Cass' Pass", world, player)
            if options.level_unlock_style != 2:
                create_single("Portal - Bull's Pen", world, player)
                create_single("Portal - Crikey's Cove", world, player)
                create_single("Portal - Fluffy's Fjord", world, player)
    
    # Junk

class ItemData():
    def __init__(self, id: int, classification: ItemClassification):
        self.id = id
        self.classification = classification

ty1_item_table: Dict[str, ItemData] = {
    # IDs
    # Generic - 0
    # Attribute - 1
    # Bilby - 2
    # Level - 3
    # Progressive - 7
    # Junk - 8

    # Generic
    "Fire Thunder Egg": ItemData(0x8750000, ItemClassification.progression_skip_balancing),
    "Ice Thunder Egg": ItemData(0x8750001, ItemClassification.progression_skip_balancing),
    "Air Thunder Egg": ItemData(0x8750002, ItemClassification.progression_skip_balancing),
    "Golden Cog":  ItemData(0x8750003, ItemClassification.skip_balancing),

    # Attributes
    "Progressive Rang": ItemData(0x8750070, ItemClassification.progression_skip_balancing),
    "Swim": ItemData(0x8750010, ItemClassification.progression),
    "Dive": ItemData(0x8750011, ItemClassification.progression),
    "Second Rang": ItemData(0x8750012, ItemClassification.progression),
    "Extra Health": ItemData(0x8750013, ItemClassification.filler),
    "Boomerang": ItemData(0x8750014, ItemClassification.progression),
    "Flamerang": ItemData(0x8750015, ItemClassification.progression),
    "Frostyrang": ItemData(0x8750016, ItemClassification.progression),
    "Zappyrang": ItemData(0x8750017, ItemClassification.progression),
    "Aquarang": ItemData(0x8750018, ItemClassification.progression),
    "Zoomerang": ItemData(0x8750019, ItemClassification.useful),
    "Multirang": ItemData(0x875001A, ItemClassification.filler),
    "Infrarang": ItemData(0x875001B, ItemClassification.useful),
    "Megarang": ItemData(0x875001C, ItemClassification.filler),
    "Kaboomarang": ItemData(0x875001D, ItemClassification.filler),
    "Chronorang": ItemData(0x875001E, ItemClassification.trap),
    "Doomarang": ItemData(0x875001F, ItemClassification.progression),

    # Bilby
    "Bilby - Two Up": ItemData(0x8750020, ItemClassification.useful),
    "Bilby - WitP": ItemData(0x8750021, ItemClassification.useful),
    "Bilby - Ship Rex": ItemData(0x8750022, ItemClassification.useful),
    "Bilby - BotRT": ItemData(0x8750023, ItemClassification.useful),
    "Bilby - Snow Worries": ItemData(0x8750024, ItemClassification.useful),
    "Bilby - Outback Safari": ItemData(0x8750025, ItemClassification.useful),
    "Bilby - LLPoF": ItemData(0x8750026, ItemClassification.useful),
    "Bilby - BtBS": ItemData(0x8750027, ItemClassification.useful),
    "Bilby - RMtS": ItemData(0x8750028, ItemClassification.useful),

    # Levels
    "Progressive Level": ItemData(0x8750071, ItemClassification.progression_skip_balancing),
    "Portal - Two Up": ItemData(0x8750030, ItemClassification.progression_skip_balancing),
    "Portal - WitP": ItemData(0x8750031, ItemClassification.progression_skip_balancing),
    "Portal - Ship Rex": ItemData(0x8750032, ItemClassification.progression_skip_balancing),
    "Portal - Bull's Pen": ItemData(0x8750033, ItemClassification.progression_skip_balancing),
    "Portal - BotRT": ItemData(0x8750034, ItemClassification.progression_skip_balancing),
    "Portal - Snow Worries": ItemData(0x8750035, ItemClassification.progression_skip_balancing),
    "Portal - Outback Safari": ItemData(0x8750036, ItemClassification.progression_skip_balancing),
    "Portal - Crikey's Cove": ItemData(0x8750037, ItemClassification.progression_skip_balancing),
    "Portal - LLPoF": ItemData(0x8750038, ItemClassification.progression_skip_balancing),
    "Portal - BtBS": ItemData(0x8750039, ItemClassification.progression_skip_balancing),
    "Portal - RMtS": ItemData(0x875003A, ItemClassification.progression_skip_balancing),
    "Portal - Fluffy's Fjord": ItemData(0x875003B, ItemClassification.progression_skip_balancing),
    "Portal - Cass' Pass": ItemData(0x875003C, ItemClassification.progression_skip_balancing),

    "Stopwatch - Two Up": ItemData(0x875040, ItemClassification.useful),
    "Stopwatch - WitP": ItemData(0x875041, ItemClassification.useful),
    "Stopwatch - Ship Rex": ItemData(0x875042, ItemClassification.useful),
    "Stopwatch - BotRT": ItemData(0x875043, ItemClassification.useful),
    "Stopwatch - Snow Worries": ItemData(0x875044, ItemClassification.useful),
    "Stopwatch - Outback Safari": ItemData(0x875045, ItemClassification.useful),
    "Stopwatch - LLPoF": ItemData(0x875046, ItemClassification.useful),
    "Stopwatch - BtBS": ItemData(0x875047, ItemClassification.useful),
    "Stopwatch - RMtS": ItemData(0x875048, ItemClassification.useful),

    # Junk
    "Picture Frame":  ItemData(0x8750080, ItemClassification.filler),
    "Talisman": ItemData(0x8750081, ItemClassification.filler),
    "Extra Life": ItemData(0x8750082, ItemClassification.filler),
    "Opal Magnet": ItemData(0x8750083, ItemClassification.filler),
}
