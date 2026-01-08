import struct


def setup_gamevars(world):
    if world.options.early_candle:
        world.multiworld.local_early_items[world.player]["Candle"] = 1


def place_static_items(world):
    if world.options.key_shuffle == 0:
        world.get_location("Parapa Palace: Stairwell").place_locked_item(world.create_item("Parapa Palace Key"))
        world.get_location("Parapa Palace: Guarded Item").place_locked_item(world.create_item("Parapa Palace Key"))

        world.get_location("Midoro Palace: B2F Hall").place_locked_item(world.create_item("Midoro Palace Key"))
        world.get_location("Midoro Palace: Floating Block Hall").place_locked_item(world.create_item("Midoro Palace Key"))
        world.get_location("Midoro Palace: Guarded Item").place_locked_item(world.create_item("Midoro Palace Key"))
        world.get_location("Midoro Palace: Lava Blocks Item").place_locked_item(world.create_item("Midoro Palace Key"))

        world.get_location("Island Palace: Buried Item Left").place_locked_item(world.create_item("Island Palace Key"))
        world.get_location("Island Palace: Outside").place_locked_item(world.create_item("Island Palace Key"))
        world.get_location("Island Palace: Precarious Item").place_locked_item(world.create_item("Island Palace Key"))
        world.get_location("Island Palace: Block Mountain").place_locked_item(world.create_item("Island Palace Key"))

        world.get_location("Maze Palace: Sealed Item").place_locked_item(world.create_item("Maze Palace Key"))
        world.get_location("Maze Palace: Block Mountain Left").place_locked_item(world.create_item("Maze Palace Key"))
        world.get_location("Maze Palace: West Hall of Fire").place_locked_item(world.create_item("Maze Palace Key"))
        world.get_location("Maze Palace: East Hall of Fire").place_locked_item(world.create_item("Maze Palace Key"))
        world.get_location("Maze Palace: Basement Hall of Fire").place_locked_item(world.create_item("Maze Palace Key"))
        world.get_location("Maze Palace: Block Mountain Basement").place_locked_item(world.create_item("Maze Palace Key"))

        world.get_location("Palace on the Sea: Ledge Item").place_locked_item(world.create_item("Sea Palace Key"))
        world.get_location("Palace on the Sea: Falling Blocks").place_locked_item(world.create_item("Sea Palace Key"))
        world.get_location("Palace on the Sea: West Wing").place_locked_item(world.create_item("Sea Palace Key"))
        world.get_location("Palace on the Sea: Skeleton Key").place_locked_item(world.create_item("Sea Palace Key"))
        world.get_location("Palace on the Sea: Knuckle Alcove").place_locked_item(world.create_item("Sea Palace Key"))

        world.get_location("Three-Eye Rock Palace: Return of Helmethead").place_locked_item(world.create_item("Three-Eye Rock Palace Key"))
        world.get_location("Three-Eye Rock Palace: Helmethead III: The Revengening").place_locked_item(world.create_item("Three-Eye Rock Palace Key"))
    
    if world.options.key_shuffle < 2:
        world.get_location("Parapa Palace: 1F West Hall").place_locked_item(world.create_item("Parapa Palace Key"))

    if not world.options.spell_locations:
        world.get_location("Sage of Rauru").place_locked_item(world.create_item("Shield Spell"))
        world.get_location("Sage of Ruto").place_locked_item(world.create_item("Jump Spell"))
        world.get_location("Sage of Saria").place_locked_item(world.create_item("Life Spell"))
        world.get_location("Sage of Mido").place_locked_item(world.create_item("Fairy Spell"))
        world.get_location("Sage of Nabooru").place_locked_item(world.create_item("Fire Spell"))
        world.get_location("Sage of Darunia").place_locked_item(world.create_item("Reflect Spell"))
        world.get_location("Sage of Kasuto").place_locked_item(world.create_item("Thunder Spell"))
        world.get_location("Sage of New Kasuto").place_locked_item(world.create_item("Spell Spell"))

    world.get_location("Parapa Palace: Statue").place_locked_item(world.create_item("Crystal Returned"))
    world.get_location("Midoro Palace: Statue").place_locked_item(world.create_item("Crystal Returned"))
    world.get_location("Island Palace: Statue").place_locked_item(world.create_item("Crystal Returned"))
    world.get_location("Maze Palace: Statue").place_locked_item(world.create_item("Crystal Returned"))
    world.get_location("Palace on the Sea: Statue").place_locked_item(world.create_item("Crystal Returned"))
    world.get_location("Three-Eye Rock Palace: Statue").place_locked_item(world.create_item("Crystal Returned"))
    world.get_location("Dark Link").place_locked_item(world.create_item("Triforce of Courage"))


def add_keys(world):
    if not world.options.remove_magical_key:
        world.extra_items.append(world.set_classifications("Magical Key"))
        three_eye_keys = 2
    else:
        three_eye_keys = 7

    if world.options.key_shuffle == 2:

        for i in range(3):
            world.multiworld.itempool.append(world.create_item("Parapa Palace Key"))

        for i in range(4):
            world.multiworld.itempool.append(world.create_item("Midoro Palace Key"))

        for i in range(4):
            world.multiworld.itempool.append(world.create_item("Island Palace Key"))

        for i in range(6):
            world.multiworld.itempool.append(world.create_item("Maze Palace Key"))

        for i in range(5):
            world.multiworld.itempool.append(world.create_item("Sea Palace Key"))

        for i in range(three_eye_keys):
            world.multiworld.itempool.append(world.create_item("Three-Eye Rock Palace Key"))

    if world.options.spell_locations == 2:
        world.multiworld.itempool+= [
        world.create_item("Shield Spell"),
        world.create_item("Jump Spell"),
        world.create_item("Life Spell"),
        world.create_item("Fairy Spell"),
        world.create_item("Fire Spell"),
        world.create_item("Reflect Spell"),
        world.create_item("Spell Spell"),
        world.create_item("Thunder Spell"),
        ]