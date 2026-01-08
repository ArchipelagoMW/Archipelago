"""Item table for Donkey Kong 64."""

import math
import typing

from BaseClasses import Item, ItemClassification
from worlds.AutoWorld import World
from types import SimpleNamespace

from randomizer.Enums.Levels import Levels
from randomizer.Lists import Item as DK64RItem
from randomizer.Enums.Items import Items as DK64RItems
from randomizer.Enums.Types import Types as DK64RTypes, BarrierItems
import randomizer.ItemPool as DK64RItemPoolUtility

BASE_ID = 0xD64000


class ItemData(typing.NamedTuple):
    """Data for an item."""

    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    event: bool = False


class DK64Item(Item):
    """A DK64 item."""

    game: str = "Donkey Kong 64"


# Separate tables for each type of item.
junk_table = {}

collectable_table = {}

event_table = {
    "Victory": ItemData(0xD64000, True),  # Temp
}

# Complete item table
full_item_table = {item.name: ItemData(int(BASE_ID + index), item.playthrough) for index, item in DK64RItem.ItemList.items()}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in full_item_table.items()}

full_item_table.update(event_table)  # Temp for generating goal item


def setup_items(world: World) -> typing.List[DK64Item]:
    """Set up the item table for the world."""
    item_table = []

    def get_progression_counts_for_barrier_types():
        """Calculate how many items of each barrier type should be marked as progression."""
        barrier_progression_counts = {}

        # Track the maximum requirement for each barrier type across all B. Lockers
        for level in range(8):
            barrier_type = world.spoiler.settings.BLockerEntryItems[level]
            requirement = world.spoiler.settings.BLockerEntryCount[level]
            if barrier_type not in barrier_progression_counts:
                barrier_progression_counts[barrier_type] = requirement
            else:
                barrier_progression_counts[barrier_type] = max(barrier_progression_counts[barrier_type], requirement)

        return barrier_progression_counts

    # Get progression requirements for barrier types used in B. Lockers
    barrier_progression_counts = get_progression_counts_for_barrier_types()

    # Define all barrier item types and their max quantities and only add them if they're used
    all_barrier_types = {
        BarrierItems.GoldenBanana: (DK64RItems.GoldenBanana, 161, DK64RTypes.Banana),
        BarrierItems.Medal: (DK64RItems.BananaMedal, 40, DK64RTypes.Medal),
        BarrierItems.Fairy: (DK64RItems.BananaFairy, 20, DK64RTypes.Fairy),
        BarrierItems.Crown: (DK64RItems.BattleCrown, 10, DK64RTypes.Crown),
        BarrierItems.RainbowCoin: (DK64RItems.RainbowCoin, 16, DK64RTypes.RainbowCoin),
    }

    # Types that donk'll handle directly and exclude from GetItemsNeedingToBeAssumed
    types_handled_directly = []

    # Always handle Golden Bananas, Medals, Fairies, Bean, and Pearl for core progression
    always_handle = [BarrierItems.GoldenBanana, BarrierItems.Medal, BarrierItems.Fairy, BarrierItems.Bean, BarrierItems.Pearl]

    # Determine which barrier types to handle directly
    barrier_types_to_handle = set(always_handle)  # Always include the core types
    # Only add barrier types that are actually used for B. Lockers
    for barrier_type in barrier_progression_counts.keys():
        if barrier_type not in always_handle:  # Don't add duplicates
            barrier_types_to_handle.add(barrier_type)

    # Handle each barrier type that we need to process
    for barrier_type in barrier_types_to_handle:
        # Handle Company Coins specially first (not in all_barrier_types)
        if barrier_type == BarrierItems.CompanyCoin:
            nintendo_item = DK64RItem.ItemList[DK64RItems.NintendoCoin]
            rareware_item = DK64RItem.ItemList[DK64RItems.RarewareCoin]
            item_table.append(DK64Item(nintendo_item.name, ItemClassification.progression_skip_balancing, full_item_table[nintendo_item.name].code, world.player))
            item_table.append(DK64Item(rareware_item.name, ItemClassification.progression_skip_balancing, full_item_table[rareware_item.name].code, world.player))
            types_handled_directly.extend([DK64RTypes.NintendoCoin, DK64RTypes.RarewareCoin])
            continue

        if barrier_type in all_barrier_types:
            item_id, max_quantity, dk64_type = all_barrier_types[barrier_type]
            item_obj = DK64RItem.ItemList[item_id]

            # Determine how many should be progression
            progression_count = barrier_progression_counts.get(barrier_type, 0)

            # For medals and fairies, also consider non-B. Locker progression requirements
            if barrier_type == BarrierItems.Medal:
                medal_requirement = world.spoiler.settings.medal_requirement if world.spoiler.settings.medal_requirement > 0 else 0
                progression_count = max(progression_count, medal_requirement)
            elif barrier_type == BarrierItems.Fairy:
                fairy_requirement = world.spoiler.settings.rareware_gb_fairies if world.spoiler.settings.rareware_gb_fairies > 0 else 0
                progression_count = max(progression_count, fairy_requirement)

            # Cap at maximum available
            progression_count = min(progression_count, max_quantity)

            # Add progression items
            for i in range(progression_count):
                item_table.append(DK64Item(item_obj.name, ItemClassification.progression_skip_balancing, full_item_table[item_obj.name].code, world.player))

            # Add remaining items as useful
            for i in range(max_quantity - progression_count):
                item_table.append(DK64Item(item_obj.name, ItemClassification.useful, full_item_table[item_obj.name].code, world.player))

            # Track that we've handled this type
            if dk64_type not in types_handled_directly:
                types_handled_directly.append(dk64_type)

            # Special case: If we handle either Bean or Pearl as barrier items,
            # we need to exclude Bean type from GetItemsNeedingToBeAssumed since
            # MiscItemRandoItems() includes both bean and pearls together
            if barrier_type in (BarrierItems.Bean, BarrierItems.Pearl):
                if DK64RTypes.Bean not in types_handled_directly:
                    types_handled_directly.append(DK64RTypes.Bean)
                # Also ensure Pearl type is tracked to prevent double addition
                if DK64RTypes.Pearl not in types_handled_directly:
                    types_handled_directly.append(DK64RTypes.Pearl)

    # Handle Company Coins specially if used for B. Lockers
    # if BarrierItems.CompanyCoin in barrier_progression_counts:
    #     nintendo_item = DK64RItem.ItemList[DK64RItems.NintendoCoin]
    #     rareware_item = DK64RItem.ItemList[DK64RItems.RarewareCoin]
    #     item_table.append(DK64Item(nintendo_item.name, ItemClassification.progression_skip_balancing, full_item_table[nintendo_item.name].code, world.player))
    #     item_table.append(DK64Item(rareware_item.name, ItemClassification.progression_skip_balancing, full_item_table[rareware_item.name].code, world.player))
    #     types_handled_directly.extend([DK64RTypes.NintendoCoin, DK64RTypes.RarewareCoin])

    # Always include ToughBanana in types handled directly
    types_handled_directly.append(DK64RTypes.ToughBanana)

    # Get remaining items from the assumption method, excluding types we handled directly
    all_shuffled_items = DK64RItemPoolUtility.GetItemsNeedingToBeAssumed(world.spoiler.settings, types_handled_directly, [])
    # Due to some latent (harmless) bugs in the above method, it isn't precise enough for our purposes and we need to manually add a few things
    # The Bean and Pearls are handled correctly by GetItemsNeedingToBeAssumed via MiscItemRandoItems(), so no manual addition needed
    # Junk moves are never assumed because they're just not needed for anything
    all_shuffled_items.extend(DK64RItemPoolUtility.JunkSharedMoves)
    # Key 8 may not be included from the assumption method, but we need it in this list to complete the item table. It won't count towards the item pool size if it is statically placed later.
    if DK64RItems.HideoutHelmKey not in all_shuffled_items:
        all_shuffled_items.append(DK64RItems.HideoutHelmKey)

    for seed_item in all_shuffled_items:
        item = DK64RItem.ItemList[seed_item]
        if item.type in [DK64RItems.JunkCrystal, DK64RItems.JunkMelon, DK64RItems.JunkAmmo, DK64RItems.JunkFilm, DK64RItems.JunkOrange, DK64RItems.CrateMelon]:
            classification = ItemClassification.filler
        elif item.type in [DK64RItems.IceTrapBubble, DK64RItems.IceTrapReverse, DK64RItems.IceTrapSlow]:
            classification = ItemClassification.trap
        elif item.type == DK64RTypes.Key:
            classification = ItemClassification.progression
        # Only mark Bean/Pearl as progression if they weren't handled directly as barrier items
        elif item.type in (DK64RTypes.Pearl, DK64RTypes.Bean) and DK64RTypes.Bean not in types_handled_directly:
            classification = ItemClassification.progression_skip_balancing
        # The playthrough tag doesn't quite 1-to-1 map to Archipelago's "progression" type - some items we don't consider "playthrough" can affect logic
        elif item.playthrough is True or item.type == DK64RTypes.Blueprint:
            classification = ItemClassification.progression_skip_balancing
        # Ensure certain item types that affect logic are marked as progression
        elif item.type in (DK64RTypes.Kong, DK64RTypes.Shop, DK64RTypes.TrainingBarrel, DK64RTypes.Shockwave, DK64RTypes.Climbing) and item.name not in [
            DK64RItem.ItemList[x].name for x in DK64RItemPoolUtility.JunkSharedMoves
        ]:
            classification = ItemClassification.progression
        else:  # double check jetpac, eh?
            classification = ItemClassification.useful
        if seed_item == DK64RItems.HideoutHelmKey and world.spoiler.settings.key_8_helm:
            world.multiworld.get_location("The End of Helm", world.player).place_locked_item(DK64Item("Key 8", ItemClassification.progression, full_item_table[item.name].code, world.player))
            world.spoiler.settings.location_pool_size -= 1
            continue
        item_table.append(DK64Item(item.name, classification, full_item_table[item.name].code, world.player))
        # print("Adding item: " + seed_item.name + " | " + str(classification))

    # Extract starting moves from the item table - these items will be placed in your starting inventory directly
    for move in world.options.start_inventory:
        for i in range(world.options.start_inventory[move]):
            for item in item_table[:]:
                if item.name == move:
                    item_table.remove(item)
                    break

    # Handle starting Kong list here
    for kong in world.spoiler.settings.starting_kong_list:
        kong_item = DK64RItemPoolUtility.ItemFromKong(kong)
        if kong == world.spoiler.settings.starting_kong or not world.spoiler.settings.kong_rando:
            world.multiworld.push_precollected(DK64Item(kong_item.name, ItemClassification.progression, full_item_table[DK64RItem.ItemList[kong_item].name].code, world.player))
        for item in item_table[:]:
            if item.name == kong_item.name:
                # Conveniently, this guarantees we have at least one precollected item!
                world.multiworld.push_precollected(DK64Item(item.name, ItemClassification.progression, full_item_table[DK64RItem.ItemList[kong_item].name].code, world.player))
                item_table.remove(item)
                break

    # Handle starting Keys list here
    for key_item in world.spoiler.settings.starting_key_list:
        world.multiworld.push_precollected(DK64Item(DK64RItem.ItemList[key_item].name, ItemClassification.progression, full_item_table[DK64RItem.ItemList[key_item].name].code, world.player))
        for item in item_table[:]:
            if item.name == DK64RItem.ItemList[key_item].name:
                item_table.remove(item)
                break

    # Handle starting move alterations here
    all_eligible_starting_moves = DK64RItemPoolUtility.AllKongMoves()
    all_eligible_starting_moves.extend(DK64RItemPoolUtility.TrainingBarrelAbilities())
    # Either include Climbing as an eligible starting move or place it in the starting inventory
    if world.options.climbing_shuffle:
        all_eligible_starting_moves.extend(DK64RItemPoolUtility.ClimbingAbilities())
    else:
        world.multiworld.push_precollected(DK64Item("Climbing", ItemClassification.progression, full_item_table[DK64RItem.ItemList[DK64RItems.Climbing].name].code, world.player))
        for item in item_table[:]:
            if item.name == "Climbing":
                item_table.remove(item)
                break

    world.random.shuffle(all_eligible_starting_moves)
    for i in range(world.options.starting_move_count):
        if len(all_eligible_starting_moves) == 0:
            break
        move_id = all_eligible_starting_moves.pop()
        move = DK64RItem.ItemList[move_id]
        # We don't want to pick anything we're already starting with. As an aside, the starting inventory move name may or may not have spaces in it.
        if move_id.name in world.options.start_inventory.options or move.name in world.options.start_inventory.options:
            # If we were to choose a move we're forcibly starting with, pick another
            i = -1
            continue
        for item in item_table[:]:
            if item.name == move_id.name or item.name == move.name:
                world.multiworld.push_precollected(item)
                item_table.remove(item)
                break

    # Simple check for now - just raise error with details
    available_slots = world.spoiler.settings.location_pool_size - 1  # minus 1 for Banana Hoard
    if len(item_table) > available_slots:
        raise Exception(f"Too many DK64 items to be placed in too few DK64 locations: {len(item_table)} items for {available_slots} slots (excess: {len(item_table) - available_slots})")

    # If there's too many locations and not enough items, add some junk
    filler_item_count: int = world.spoiler.settings.location_pool_size - len(item_table) - 1  # The last 1 is for the Banana Hoard

    trap_weights = []
    trap_weights += [DK64RItems.IceTrapBubble] * world.options.bubble_trap_weight.value
    trap_weights += [DK64RItems.IceTrapReverse] * world.options.reverse_trap_weight.value
    trap_weights += [DK64RItems.IceTrapSlow] * world.options.slow_trap_weight.value

    trap_count = 0 if (len(trap_weights) == 0) else math.ceil(filler_item_count * (world.options.trap_fill_percentage.value / 100.0))
    filler_item_count -= trap_count

    possible_junk = [DK64RItems.JunkMelon]
    # possible_junk = [DK64RItems.JunkCrystal, DK64RItems.JunkMelon, DK64RItems.JunkAmmo, DK64RItems.JunkFilm, DK64RItems.JunkOrange] # Someday...

    for i in range(filler_item_count):
        junk_enum = world.random.choice(possible_junk)
        junk_item = DK64RItem.ItemList[junk_enum]
        item_table.append(DK64Item(junk_item.name, ItemClassification.filler, full_item_table[junk_item.name].code, world.player))

    possible_traps = [DK64RItems.IceTrapBubble, DK64RItems.IceTrapReverse, DK64RItems.IceTrapSlow]

    for i in range(trap_count):
        trap_enum = world.random.choice(trap_weights)
        trap_item = DK64RItem.ItemList[trap_enum]
        item_table.append(DK64Item(trap_item.name, ItemClassification.trap, full_item_table[trap_item.name].code, world.player))

    # print("projected available locations: " + str(world.spoiler.settings.location_pool_size - 1))
    # print("projected items to place: " + str(len(item_table)))

    # Example of accessing Option result
    if world.options.goal == "krool":
        pass

    # DEBUG
    # for k, v in full_item_table.items():
    #    print(k + ": " + hex(v.code) + " | " + str(v.progression))

    return item_table
