from typing import TYPE_CHECKING

from BaseClasses import ItemClassification as IC
from BaseClasses import LocationProgressType
from Fill import FillError
from Options import OptionError

from ..Items import ITEM_TABLE, CONSUMABLE_ITEMS
from ..Locations import LOCATION_TABLE, SSLocType, SSLocFlag
from ..Constants import *

if TYPE_CHECKING:
    from .. import SSWorld


def handle_itempool(world: "SSWorld") -> None:
    """
    Handles the item pool for the world.

    :param world: The SS game world.
    """

    # Create the base itempool.
    progression_pool, useful_pool, filler_pool = _create_base_itempool(world)
    pool = progression_pool + useful_pool
    world.starting_items = _handle_starting_items(world)

    # Add starting items to the multiworld's `precollected_items` list.
    # Then remove starting items from the item pool
    for itm in world.starting_items:
        world.multiworld.push_precollected(world.create_item(itm))

        adjusted_classification = item_classification(world, itm)
        classification = (
            ITEM_TABLE[itm].classification
            if adjusted_classification is None
            else adjusted_classification
        )
        if classification == IC.filler:
            assert itm in filler_pool, f"Could not remove filler item from pool: {itm}"
            filler_pool.remove(itm)
        else:
            assert itm in pool, f"Could not remove item from pool: {itm}"
            pool.remove(itm)
    
    # Place items and remove from the item pool
    placed = _handle_placements(world, pool)

    # Handle start inventory now, as these items are not removed from the pool
    start_inventory = []
    for itm, q in world.options.start_inventory.value.items():
        world.starting_items.extend([itm] * q)
        # No need to push these as precollected, AP already does that c:

    for itm in placed:
        adjusted_classification = item_classification(world, itm)
        classification = (
            ITEM_TABLE[itm].classification
            if adjusted_classification is None
            else adjusted_classification
        )
        if classification == IC.filler:
            assert itm in filler_pool, f"Could not remove filler item from pool: {itm}"
            filler_pool.remove(itm)
        else:
            assert itm in pool, f"Could not remove item from pool: {itm}"
            pool.remove(itm)
    
    pool = _fill_itempool(world, pool, filler_pool)

    # Create the pool of the remaining shuffled items.
    items = [world.create_item(itm) for itm in pool]
    world.random.shuffle(items)

    world.multiworld.itempool += items


def _create_base_itempool(world: "SSWorld") -> tuple[list[str], list[str], list[str]]:
    """
    Creates and fills the item pool and determines starting items.

    :param world: The SS game world.
    :return: A tuple of the progression, useful, and filler pools.
    """
    pool: list[str] = []
    starting_items: list[str] = []

    # Split items into three different pools: progression, useful, and filler.
    # Filler pool is adjusted to fill what's left, then replaced with rupoors depending on options, then added to pool.
    progression_pool: list[str] = []
    useful_pool: list[str] = []
    filler_pool: list[str] = []
    for item, data in ITEM_TABLE.items():
        if data.type in ["Item", "Small Key", "Boss Key", "Map"]:
            adjusted_classification = item_classification(world, item)
            classification = (
                data.classification
                if adjusted_classification is None
                else adjusted_classification
            )

            if classification == IC.progression or classification == IC.progression_skip_balancing:
                progression_pool.extend([item] * data.quantity)
            elif classification == IC.useful:
                useful_pool.extend([item] * data.quantity)
            else:
                filler_pool.extend([item] * data.quantity)

    if not world.options.rupeesanity:
        filler_pool.extend([data.vanilla_item for loc, data in LOCATION_TABLE.items() if data.flags & SSLocFlag.RUPEE])
            # Put all placed rupees in filler pool if rupeesanity is on
            # These will be removed from the pool and manually placed vanilla

    return progression_pool, useful_pool, filler_pool

def _fill_itempool(world: "SSWorld", pool: list[str], filler_pool: list[str]) -> list[str]:
    """
    Fills the remainder of the itempool after starting items and placements are handled.
    Handles rupoors as well.

    :param world: The SS World.
    :param pool: The progression and useful pool.
    :param filler_pool: The filler pool.
    :return: The filled itempool.
    """
    num_items_needed = 0
    for loc in world.multiworld.get_locations(world.player):
        if not loc.item:
            num_items_needed += 1

    num_items_needed -= len(pool)
    num_items_needed -= len(filler_pool)

    consumable_pool = world.random.choices(
        list(CONSUMABLE_ITEMS.keys()),
        weights=list(CONSUMABLE_ITEMS.values()),
        k=num_items_needed,
    )
    filler_pool.extend(consumable_pool)
    world.random.shuffle(filler_pool)

    # Now fill rupoors
    if world.options.rupoor_mode == "added":
        if len(filler_pool) < 15:
            filler_pool = ["Rupoor"] * len(filler_pool)
            # Replace the entire filler pool with rupoors
        else:
            for i in range(15):
                filler_pool[i] = "Rupoor"
            # Replace the first 15 elements with rupoors
    elif world.options.rupoor_mode == "rupoor_mayhem":
        for i in range(round(len(filler_pool)/2)):
            filler_pool[i] = "Rupoor"
        # Replace the first half of the pool with rupoors
    elif world.options.rupoor_mode == "rupoor_insanity":
        filler_pool = ["Rupoor"] * len(filler_pool)
        # Replace the entire filler pool with rupoors

    pool.extend(filler_pool)
    world.random.shuffle(pool)

    return pool


def _handle_starting_items(world: "SSWorld") -> list[str]:
    """
    Handles starting items based on player's options.

    :return: A list of starting items.
    """
    options = world.options
    starting_items: list[str] = []

    # General Starting Items
    starting_items_option = options.starting_items
    for itm, q in starting_items_option.value.items():
        if itm in ITEM_TABLE:
            if q > ITEM_TABLE[itm].quantity:
                raise OptionError(
                    f"Too many starting items! Tried to give {q} {itm} but could only give {ITEM_TABLE[itm].quantity}"
                )
            else:
                starting_items.extend([itm] * q)
        else:
            raise OptionError(f"Unknown item in option `starting items`: {itm}")

    # Starting Sword
    starting_sword_option = options.starting_sword.value
    for _ in range(int(starting_sword_option)):
        starting_items.append("Progressive Sword")

    # Starting Tablets
    starting_tablet_option = options.starting_tablet_count.value
    tablets = ["Emerald Tablet", "Ruby Tablet", "Amber Tablet"]
    if starting_tablet_option == 0:
        pass
    else:
        randomized_tablets = world.random.sample(
            tablets, starting_tablet_option
        )
        starting_items.extend(randomized_tablets)

    # Starting Crystals
    starting_crystals_option = options.starting_crystal_packs.value
    for _ in range(int(starting_crystals_option)):
        starting_items.append("Gratitude Crystal Pack")

    # Starting Bottles
    starting_bottles_option = options.starting_bottles.value
    for _ in range(int(starting_bottles_option)):
        starting_items.append("Empty Bottle")

    # Starting HCs
    starting_hcs_option = options.starting_heart_containers.value
    for _ in range(int(starting_hcs_option)):
        starting_items.append("Heart Container")

    # Starting HPs
    starting_hps_option = options.starting_heart_pieces.value
    for _ in range(int(starting_hps_option)):
        starting_items.append("Heart Piece")

    # Starting Tadtones
    starting_tadtones_option = options.starting_tadtones.value
    for _ in range(int(starting_tadtones_option)):
        starting_items.append("Group of Tadtones")

    # Random Starting Item
    random_starting_item_option = bool(options.random_starting_item)
    if random_starting_item_option:
        possible_items_to_give = []
        for itm in POSSIBLE_RANDOM_STARTING_ITEMS:
            possible_items_to_give.extend([itm] * ITEM_TABLE[itm].quantity)
        for itm in starting_items:
            if itm in possible_items_to_give:
                # Here we make sure our starting items don't collide with the random starting item
                possible_items_to_give.remove(itm)
        if len(possible_items_to_give) == 0:
            raise OptionError("Tried to give a random starting item, but couldn't find any items to give.")
        rs_item = world.random.choice(possible_items_to_give)
        starting_items.append(rs_item)

    # Start with Hylian Shield
    starting_hylian_option = bool(options.start_with_hylian_shield)
    if starting_hylian_option:
        starting_items.append("Hylian Shield")

    # Start with Maps
    map_mode_option = options.map_mode
    if map_mode_option == "start_with":
        for itm, data in ITEM_TABLE.items():
            if data.type == "Map":
                starting_items.append(itm)

    # Start with Caves Key
    caves_key_option = options.lanayru_caves_small_key
    if caves_key_option == "start_with":
        starting_items.append("Lanayru Caves Small Key")

    return starting_items


def _handle_placements(world: "SSWorld", pool: list[str]) -> list[str]:
    """
    Handles forced placements for items in certain locations based on player's options.

    :param world: The SS game world.
    :param pool: The item pool.
    :return: A list of items that are placed, to later be removed from the item pool.
    """

    options = world.options
    placed: list[str] = []

    # Place a "Victory" item on "Defeat Demise" for AP.
    world.get_location("Hylia's Realm - Defeat Demise").place_locked_item(
        world.create_item("Victory")
    )

    # Place locked single crystals
    for loc, data in LOCATION_TABLE.items():
        if data.type == SSLocType.CRYST:
            world.get_location(loc).place_locked_item(
                world.create_item("Gratitude Crystal")
            )
            placed.append("Gratitude Crystal")

    if not options.treasuresanity_in_silent_realms:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.RELIC:
                world.get_location(loc).place_locked_item(
                    world.create_item("Dusk Relic")
                )
                placed.append("Dusk Relic")
    else:
        num_relics = options.trial_treasure_amount.value
        for trl in TRIAL_LIST:
            all_relics = [loc for loc in world.multiworld.get_locations(world.player) if loc.parent_region == world.get_region(trl) and loc.type == SSLocType.RELIC]
            relics_to_place = [rel for rel in all_relics if int(rel.name.split(" ")[-1]) > num_relics]
            for rel in relics_to_place:
                rel.place_locked_item(world.create_item("Dusk Relic"))
                placed.append("Dusk Relic")

    if not options.shopsanity:
        for loc, data in LOCATION_TABLE.items():
            if data.type == SSLocType.SHOP:
                if loc == "Beedle's Shop - 1600 Rupee Item" and int(options.starting_heart_pieces.value) == 24:
                    # Edge case where we cannot place the HP, just exclude the location
                    world.get_location(loc).progress_type = LocationProgressType.EXCLUDED
                else:
                    world.get_location(loc).place_locked_item(
                        world.create_item(data.vanilla_item)
                    )
                    placed.append(data.vanilla_item)

    if not options.tadtonesanity:
        num_tadtones = 17 - options.starting_tadtones.value
        all_tadtones = [loc for loc in world.multiworld.get_locations(world.player) if loc.type == SSLocType.CLEF]
        for i, tad in enumerate(all_tadtones):
            if i < num_tadtones:
                tad.place_locked_item(
                    world.create_item("Group of Tadtones")
                )
                placed.append("Group of Tadtones")
            else:
                # If we can't place any more tadtones, put a junk item here
                tad.progress_type = LocationProgressType.EXCLUDED

    if not options.rupeesanity:
        for loc, data in LOCATION_TABLE.items():
            if data.flags & SSLocFlag.RUPEE:
                world.get_location(loc).place_locked_item(
                    world.create_item(data.vanilla_item)
                )
                placed.append(data.vanilla_item)

    if not options.gondo_upgrades:
        placed.extend(GONDO_UPGRADES)
        # We're not actually going to place these in the world, the rando will patch them in
        # Still, remove them from the item pool

    ### DUNGEON PLACEMENTS

    # Place vanilla keys first to prevent location overlap
    if options.small_key_mode == "vanilla":
        placed.extend(world.dungeons.key_handler.place_small_keys())
    if options.boss_key_mode == "vanilla":
        placed.extend(world.dungeons.key_handler.place_boss_keys())
    if options.map_mode == "vanilla":
        placed.extend(world.dungeons.key_handler.place_dungeon_maps())

    # Sword Dungeon Reward
    if options.sword_dungeon_reward != "none":
        num_swords_to_place = pool.count("Progressive Sword")
        if num_swords_to_place == 5 or num_swords_to_place == 6:
            cap = 4
            num_swords_to_place = min(num_swords_to_place, cap)
        if num_swords_to_place < len(world.dungeons.required_dungeons):
            # More dungeons than swords to place, place as many as possible
            dungeons_to_place_swords = world.random.sample(
                world.dungeons.required_dungeons, num_swords_to_place
            )
        elif num_swords_to_place >= len(world.dungeons.required_dungeons):
            # More swords than dungeons, so place a sword in each required dungeon
            dungeons_to_place_swords = world.dungeons.required_dungeons.copy()

        for dun in dungeons_to_place_swords:
            if options.sword_dungeon_reward == "heart_container":
                loc = DUNGEON_HC_CHECKS[dun]
            else:
                loc = DUNGEON_FINAL_CHECKS[dun]
            world.get_location(loc).place_locked_item(
                world.create_item("Progressive Sword")
            )
            placed.append("Progressive Sword")

    # Vanilla Triforces
    if options.triforce_shuffle == "vanilla":
        world.get_location("Sky Keep - Sacred Power of Din").place_locked_item(world.create_item("Triforce of Power"))
        world.get_location("Sky Keep - Sacred Power of Nayru").place_locked_item(world.create_item("Triforce of Wisdom"))
        world.get_location("Sky Keep - Sacred Power of Farore").place_locked_item(world.create_item("Triforce of Courage"))
        placed.extend(["Triforce of Power", "Triforce of Wisdom", "Triforce of Courage"])
    
    # Place non-vanilla keys now
    if options.small_key_mode != "vanilla":
        placed.extend(world.dungeons.key_handler.place_small_keys())
    if options.lanayru_caves_small_key != "start_with":
        placed.extend(world.dungeons.key_handler.place_caves_key())
    if options.boss_key_mode != "vanilla":
        placed.extend(world.dungeons.key_handler.place_boss_keys())
    if options.map_mode != "start_with" and options.map_mode != "vanilla":
        placed.extend(world.dungeons.key_handler.place_dungeon_maps())

    # Non-vanilla Triforces
    if options.triforce_shuffle == "sky_keep":
        locations_to_place = [loc for loc in world.multiworld.get_locations(world.player) if world.region_to_hint_region(loc.parent_region) == "Sky Keep" and not loc.item]
        triforce_locations = world.random.sample(locations_to_place, 3)
        world.random.shuffle(triforce_locations)
        for i, tri in enumerate(["Triforce of Power", "Triforce of Wisdom", "Triforce of Courage"]):
            triforce_locations[i].place_locked_item(world.create_item(tri))
        placed.extend(["Triforce of Power", "Triforce of Wisdom", "Triforce of Courage"])

    return placed


def item_classification(world: "SSWorld", name: str) -> IC | None:
    """
    Determine the item classification based on player's options.
    If no adjustment to classification, return None and use the classification specified in the item table.

    :param name: Name of the item
    :return: New IC of the item or None
    """
    adjusted_classification = None
    item_type = ITEM_TABLE[name].type

    # Dungeon Entrance Access Items
    if (
        world.options.randomize_entrances == "none"
        and world.options.empty_unrequired_dungeons
    ):
        if "Earth Temple" not in world.dungeons.required_dungeons:
            if name == "Key Piece":
                adjusted_classification = IC.filler
        if "Sandship" not in world.dungeons.required_dungeons:
            if name == "Sea Chart":
                adjusted_classification = IC.filler
        if not world.dungeons.sky_keep_required:
            if name == "Stone of Trials":
                adjusted_classification = IC.filler
    
    # Dungeon Items
    if (
        world.options.empty_unrequired_dungeons
        and item_type in ["Map", "Small Key", "Boss Key"]
    ):
        if item_type == "Map":
            item_dungeon = name[:-4]
            if item_dungeon == "Sky Keep":
                adjusted_classification = IC.filler if not world.dungeons.sky_keep_required else None
            elif not item_dungeon in world.dungeons.required_dungeons:
                adjusted_classification = IC.filler
                # If map not a required dungeon, make it filler
                # Otherwise, it will be useful
        if item_type == "Small Key":
            item_dungeon = name[:-10]
            if item_dungeon == "Sky Keep":
                adjusted_classification = IC.filler if not world.dungeons.sky_keep_required else None
            elif item_dungeon == "Lanayru Caves":
                pass
                # Caves key will always stay progression
            elif not item_dungeon in world.dungeons.required_dungeons:
                adjusted_classification = IC.filler
                # If small key not a required dungeon, make it filler
                # Otherwise, it will be progression
        if item_type == "Boss Key":
            item_dungeon = name[:-9]
            if not item_dungeon in world.dungeons.required_dungeons:
                adjusted_classification = IC.filler
                # If boss key not a required dungeon, make it filler
                # Otherwise, it will be progression

    # Triforces
    if not world.options.triforce_required:
        if "Triforce" in name:
            adjusted_classification = IC.useful
            # If Triforce is not required, make it useful

    # Items for single checks
    if "Upper Skyloft - Ghost/Pipit's Crystals" in world.options.exclude_locations:
        if name == "Cawlin's Letter":
            adjusted_classification = IC.filler
    if "Skyloft Village - Bertie's Crystals" in world.options.exclude_locations:
        if name == "Baby Rattle":
            adjusted_classification = IC.filler
    if "Sky - Beedle's Crystals" in world.options.exclude_locations:
        if name == "Horned Colossus Beetle":
            adjusted_classification = IC.filler
    if "Lanayru Gorge - Thunder Dragon's Reward" in world.options.exclude_locations:
        if name == "Life Tree Fruit":
            adjusted_classification = IC.filler
    if "Flooded Faron Woods - Water Dragon's Reward" in world.options.exclude_locations:
        if name == "Group of Tadtones":
            adjusted_classification = IC.filler

    return adjusted_classification


