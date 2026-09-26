from typing import Set, List
from .generator_main import EBItem


def get_excluded_items(world) -> Set[str]:
    excluded_items: Set[str] = set()
    excluded_items.add(world.starting_character)
    starting_area_to_teleport = ["Onett Teleport", "Onett Teleport", "Twoson Teleport", "Happy-Happy Village Teleport",
                                 "Threed Teleport", "Saturn Valley Teleport", "Fourside Teleport", "Winters Teleport",
                                 "Summers Teleport", "Dalaam Teleport", "Scaraba Teleport", "Deep Darkness Teleport",
                                 "Tenda Village Teleport", "Lost Underworld Teleport", "Magicant Teleport"]
    world.starting_area_teleport = starting_area_to_teleport[world.start_location]
    excluded_items.add(world.starting_area_teleport)
    if world.options.random_start_location:
        excluded_items.add(world.starting_teleport)

    if world.options.magicant_mode not in [0, 3]:
        excluded_items.add("Magicant Teleport")

    if not world.options.character_shuffle:
        excluded_items.add("Ness")
        excluded_items.add("Paula")
        excluded_items.add("Jeff")
        excluded_items.add("Poo")
        excluded_items.add("Flying Man")

    if world.options.progressive_weapons:
        excluded_items.add("Magicant Bat")
        excluded_items.add("Legendary Bat")
        excluded_items.add("Pop Gun")
        excluded_items.add("Stun Gun")
        excluded_items.add("Death Ray")
        excluded_items.add("Moon Beam Gun")

    if world.options.progressive_armor:
        excluded_items.add("Platinum Band")
        excluded_items.add("Diamond Band")
        excluded_items.add("Pixie's Bracelet")
        excluded_items.add("Cherub's Band")
        excluded_items.add("Goddess Band")
        excluded_items.add("Coin of Slumber")
        excluded_items.add("Souvenir Coin")
        excluded_items.add("Mr. Saturn Coin")

    if not world.options.no_free_sanctuaries:
        excluded_items.add("Tiny Key")
        excluded_items.add("Tenda Lavapants")

    return excluded_items


def fill_item_pool(world, pool: List[EBItem]) -> None:
    item_to_counts = {
        "Progressive Bat": world.progressive_filler_bats,
        "Progressive Fry Pan": world.progressive_filler_pans,
        "Progressive Gun": world.progressive_filler_guns,
        "Progressive Bracelet": world.progressive_filler_bracelets,
        "Progressive Other": world.progressive_filler_other
    }

    max_filler_counts = {
        "Progressive Bat": 8,
        "Progressive Fry Pan": 9,
        "Progressive Gun": 6,
        "Progressive Bracelet": 6,
        "Progressive Other": 10
    }

    for _ in range(len(world.multiworld.get_unfilled_locations(world.player)) - len(pool) - world.pre_fill_count):
        from .generator_main import set_classifications
        item = set_classifications(world, world.get_filler_item_name())
        if item.name in ["Progressive Bat", "Progressive Fry Pan", "Progressive Other",
                         "Progressive Gun", "Progressive Bracelet"]:
            item_to_counts[item.name] += 1

            if item_to_counts[item.name] >= max_filler_counts[item.name]:
                world.common_gear = [x for x in world.common_gear if x != item.name]
                world.uncommon_gear = [x for x in world.uncommon_gear if x != item.name]
                world.rare_gear = [x for x in world.rare_gear if x != item.name]
        pool.append(item)


def get_item_pool(world, excluded_items: Set[str]) -> List[EBItem]:
    from .Items import item_table
    from .generator_main import set_classifications
    pool: List[EBItem] = []

    for name, data in item_table.items():
        if name not in excluded_items:
            for _ in range(data.amount):
                item = set_classifications(world, name)
                pool.append(item)

    if world.options.progressive_weapons:
        for i in range(2):
            pool.append(set_classifications(world, "Progressive Bat"))
        for i in range(4):
            pool.append(set_classifications(world, "Progressive Gun"))

    if world.options.progressive_armor:
        for i in range(5):
            pool.append(set_classifications(world, "Progressive Bracelet"))
        for i in range(3):
            pool.append(set_classifications(world, "Progressive Other"))

    return pool
