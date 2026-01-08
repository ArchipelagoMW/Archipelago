import random

from typing_extensions import TYPE_CHECKING

from BaseClasses import ItemClassification, Item
from .patching.Util import simple_hex
from .patching.text import normalize_text

if TYPE_CHECKING:
    from . import OracleOfSeasonsWorld

know_it_all_birds = [
    "TX_3200",  # "Know-It-All Bird #1",
    "TX_3201",  # "Know-It-All Bird #2",
    "TX_3202",  # "Know-It-All Bird #3",
    "TX_3203",  # "Know-It-All Bird #4",
    "TX_3204",  # "Know-It-All Bird #5",
    "TX_3205",  # "Know-It-All Bird #6",
    "TX_3206",  # "Know-It-All Bird #7",
    "TX_3207",  # "Know-It-All Bird #8",
    "TX_3208",  # "Know-It-All Bird #9",
    "TX_3209",  # "Know-It-All Bird #10"
]
owl_statues = [
    "TX_390d",  # "Dodongo Owl",
    "TX_390e",  # "Gohma Owl",
    "TX_390f",  # "Armos Owl",
    "TX_3910",  # "Silent Watch Owl",
    "TX_3911",  # "Magical Ice Owl",
    "TX_3914",  # "Mystery Owl",
    "TX_3915",  # "Omuai Owl",
    "TX_3916",  # "Poe Curse Owl",
    "TX_3917",  # "Spiked Beetles Owl",
    "TX_3918",  # "Trampoline Owl",
    "TX_3919",  # "Greater Distance Owl",
    "TX_391a",  # "Frypolar Owl",
    "TX_391c",  # "Shining Blue Owl",
    "TX_391d",  # "Floodgate Owl",
]

location_by_region = {
    "North Horon": [
        "North Horon: Chest Across Bridge",
        "North Horon: Malon Trade",
        "North Horon: Yelling Old Man Trade",
        "North Horon: Old Man Near D1",
        "North Horon: Golden Beasts Old Man",
        "Eyeglass Lake: Chest in Dried Lake East Cave",
        "Eyeglass Lake: Chest in Dried Lake West Cave",
    ],
    "Horon Village": [
        "Horon Village: Maku Tree Gift",
        "Horon Village: Chest Behind Mushrooms",
        "Horon Village: Chest in Dr. Left's Backyard",
        "Horon Village: Shop #1",
        "Horon Village: Shop #2",
        "Horon Village: Shop #3",
        "Horon Village: Member's Shop #1",
        "Horon Village: Member's Shop #2",
        "Horon Village: Member's Shop #3",
        "Horon Village: Advance Shop #1",
        "Horon Village: Advance Shop #2",
        "Horon Village: Advance Shop #3",
        "Horon Village: Item Behind Small Tree",
        "Horon Village: Item Behind Cracked Wall in Mayor's House",
        "Horon Village: Mayor's Gift",
        "Horon Village: Vasu's Gift",
        "Horon Village: Dr. Left Reward",
        "Horon Village: Tick Tock Trade",
        "Horon Village: Old Man",
        "Horon Village: Seed Tree",
        "Horon Village: Item Inside Maku Tree (3+ Essences)",
        "Horon Village: Item Inside Maku Tree (5+ Essences)",
        "Horon Village: Item Inside Maku Tree (7+ Essences)",
        "Horon Village: Clock Shop Secret",
        "Horon Village: Mayor Secret",
    ],
    "Woods of Winter": [
        "Woods of Winter: Holly's Gift",
        "Woods of Winter: Chest on D2 Roof",
        "Woods of Winter: Chest in Autumn Cave Near D2",
        "Woods of Winter: Chest in Cave Behind Rockslide",
        "Woods of Winter: Chest in Waterfall Cave",
        "Woods of Winter: Item Below Lake",
        "Woods of Winter: Old Man",
        "Woods of Winter: Seed Tree",
    ],
    "Holodrum Plain": [
        "Holodrum Plain: Blaino's Gym Prize",
        "Holodrum Plain: Underwater Item Below Natzu Bridge",
        "Holodrum Plain: Old Man in Treehouse",
        "Holodrum Plain: Chest in Flooded Cave South of Mrs. Ruul",
        "Holodrum Plain: Chest in Flooded Cave Behind Mushrooms",
        "Holodrum Plain: Mrs. Ruul Trade",
        "Holodrum Plain: Old Man Near Blaino's Gym",
        "Holodrum Plain: Old Man Near Mrs. Ruul's House",
        "Holodrum Plain: Seed Tree",
    ],
    "Spool Swamp": [
        "Spool Swamp: Digging Spot Near Vasu's Sign",
        "Spool Swamp: Item in Floodgate Keeper's House",
        "Spool Swamp: Chest in Winter Cave",
        "Spool Swamp: Item Amidst Currents in Spring",
        "Spool Swamp: Seed Tree",
        "Spool Swamp: Business Scrub",
    ],
    "Natzu Region": [
        "Natzu Region: Chest after Moblin Keep",
        "Natzu Region: Chest in Northern Cave",
        "Natzu Region: Deku Secret",
    ],
    "Sunken City": [
        "Sunken City: Master Diver's Challenge Chest",
        "Sunken City: Master's Plaque Trade",
        "Sunken City: Chest in Master Diver's Cave",
        "Sunken City: Chest in Summer Cave",
        "Sunken City: Syrup Shop #1",
        "Sunken City: Syrup Shop #2",
        "Sunken City: Syrup Shop #3",
        "Sunken City: Ingo Trade",
        "Sunken City: Syrup Trade",
        "Sunken City: Seed Tree",
        "Sunken City: Diver Secret",
    ],
    "Mt. Cucco": [
        "Mt. Cucco: Spring Banana Tree",
        "Mt. Cucco: Moving Platform Cave",
        "Mt. Cucco: Diving Spot Outside D4",
        "Mt. Cucco: Chest Behind Talon",
        "Mt. Cucco: Item on Ledge",
        "Mt. Cucco: Talon Trade",
    ],
    "Goron Mountain": [
        "Goron Mountain: Item Across Pits",
        "Goron Mountain: Chest Across Lava",
        "Goron Mountain: Lonely Goron's Gift",
        "Goron Mountain: Biggoron Trade",
        "Goron Mountain: Old Man",
        "Goron Mountain: Biggoron Secret",
    ],
    "Western Coast": [
        "Western Coast: Black Beast's Chest",
        "Western Coast: Chest on Beach",
        "Western Coast: Chest in House",
        "Western Coast: Item in Graveyard",
        "Western Coast: Old Man",
        "Western Coast: Graveyard Secret",
    ],
    "South-East": [
        "Samasa Desert: Item in Quicksand Pit",
        "Samasa Desert: Chest on Cliff",
        "Samasa Desert: Business Scrub",
        "Eastern Suburbs: Chest in Spring Cave",
        "Eastern Suburbs: Item in Windmill Cave",
        "Eastern Suburbs: Guru-Guru Trade",
    ],
    "Tarm Ruins": [
        "Tarm Ruins: Chest in Rabbit Hole Under Tree",
        "Tarm Ruins: Old Man Near D6",
        "Tarm Ruins: Seed Tree",
        "Lost Woods: Pedestal Item",
    ],
    "Subrosian Volcanoes": [
        "Subrosia: Dance Hall Reward",
        "Subrosia: Northwest Open Cave",
        "Subrosia: Northwest Locked Cave",
        "Subrosia: Smithy Hard Ore Reforge",
        "Subrosia: Smithy Rusty Bell Reforge",
        "Subrosia: Northern Volcanoes Digging Spot",
        "Subrosia: Western Volcanoes Digging Spot",
        "Subrosia: Hot Bath Digging Spot",
        "Subrosia: D8 Portal Digging Spot",
        "Subrosia: Subrosian Secret",
    ],
    "Temple of Seasons": [
        "Subrosia: Tower of Winter",
        "Subrosia: Tower of Summer",
        "Subrosia: Tower of Autumn",
        "Subrosia: Temple of Seasons",
        "Subrosia: Temple Secret",
        "Subrosia: Temple of Seasons Digging Spot",
    ],
    "Subrosian Market": [
        "Subrosia: Market #1",
        "Subrosia: Market #2",
        "Subrosia: Market #3",
        "Subrosia: Market #4",
        "Subrosia: Market #5",
        "Subrosia: Seaside Digging Spot",
        "Subrosia: Market Portal Digging Spot",
        "Subrosia: Hard-Working Subrosian Digging Spot",
    ],
    "Subrosian Forge": [
        "Subrosia: Chest Above Magnet Cave",
        "Subrosia: Item Smelted in Great Furnace",
        "Subrosia: Buried Bomb Flower",
        "Subrosia: Sign-Loving Guy Reward",
        "Subrosia: Smith Secret",
    ],
    "Subrosian Village": [
        "Subrosia: Wilds Chest",
        "Subrosia: Wilds Digging Spot",
        "Subrosia: Subrosian Chef Trade",
        "Subrosia: Item in House Above Strange Brothers Portal",
        "Subrosia: Strange Brothers' Backyard Treasure",
        "Subrosia: Piratian Secret",
        "Subrosia: Item in Basement to Tower of Spring",
        "Subrosia: Tower of Spring",
    ],
}


def get_region_hint_text(region_name: str, region_category: str) -> str:
    region_name = f"🟦{region_name}⬜"
    hint_text = f"Did you know? "
    if region_category == "Foolish":
        hint_text += f"It is foolish to search {region_name}."
    elif region_category == "Golden":
        hint_text += f"Everything in {region_name} is precious!"
    else:
        hint_text += f"There are 🟩{region_category}⬜ precious treasures in {region_name}."
    return normalize_text(hint_text)


def get_random_joke_text(owl_id: int) -> tuple[str, str]:
    match random.randrange(5):
        case 0:
            location = [
                "Snake's Remains",
                "Dancing Dragon Dungeon",
                "Unicorn's Cave",
                "Sword & Shield Dungeon",
                "Sword & Shield Dungeon",
                "Woods of Winter",
                "Poison Moth's Lair",
                "Explorer's Crypt",
                "Poison Moth's Lair",
                "Poison Moth's Lair",
                "Dancing Dragon Dungeon",
                "Sword & Shield Dungeon",
                "Explorer's Crypt",
                "Spool Swamp"
            ][owl_id]
            return "\\link_name", location
        case 1:
            return "Onox", "Onox's Castle"
        case 2:
            return "Princess Zelda", "Another Castle"
        case 3:
            return "Maku Tree", "Horon Village"
        case 4:
            return "Maple", "the airs"


def make_hint_texts(texts: dict[str, str], patch_data) -> None:
    region_hints = patch_data["region_hints"]
    if len(region_hints):
        i = 0
        for region, category in region_hints:
            texts[know_it_all_birds[i]] = get_region_hint_text(region, category)
            i += 1

        # Remove the extra bird text
        for i in range(0x0a, 0x14):
            del texts[f"TX_32{simple_hex(i)}"]

    item_hints = patch_data["item_hints"]
    if len(item_hints):
        for i in range(0x00, 0x1c):
            texts[f"TX_39{simple_hex(i)}"] = ""

        i = 0
        for hint in item_hints:
            if hint is None:
                item, location = get_random_joke_text(i)
            else:
                item, location, player = hint
                if player:
                    location = f"{player}'s {location}"
            text = f"They say that 🟥{item}⬜ can be found in 🟦{location}"
            text = normalize_text(text)

            texts[owl_statues[i]] = text
            i += 1


def create_region_hints(world: "OracleOfSeasonsWorld") -> list[tuple[str, str | int]]:
    hinted_regions: list[str] = world.random.sample([*location_by_region], k=len(know_it_all_birds))
    hint_data: list[tuple[str, str | int]] = []
    for region in hinted_regions:
        num_locations = 0
        num_progression = 0
        for location_name in location_by_region[region]:
            try:
                location = world.get_location(location_name)
                num_locations += 1
                if location.advancement:
                    num_progression += 1
            except KeyError:
                pass
        ratio = num_progression / num_locations
        if ratio == 0:
            region_type = "Foolish"
        elif ratio == 1:
            region_type = "Golden"
        else:
            region_type = num_progression
        hint_data.append([region, region_type])
    return hint_data


def create_item_hints(world: "OracleOfSeasonsWorld") -> list[Item | None]:
    hint_data: list[tuple[str, str, int | None]] = []
    hintable_items: list[Item | None] = [location.item for location in world.multiworld.get_filled_locations()
                                         if location.item.player == world.player
                                         and location.item.advancement
                                         and not location.item.classification & ItemClassification.deprioritized
                                         and not location.is_event
                                         and not location.locked]
    hintable_items.append(None)

    hinted_items: list[Item | None] = world.random.choices(hintable_items, k=len(owl_statues))
    for hinted_item in hinted_items:
        if hinted_item is None:
            hint_data.append(None)
            continue
        hint_data.append(hinted_item)
    return hint_data
