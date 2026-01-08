from typing import TYPE_CHECKING

from NetUtils import NetworkItem
from . import Rac2World, ItemPool
from .TextManager import colorize_item_name
from .data import Items
from .data.Items import EquipmentData, CoordData, ProgressiveUpgradeData

if TYPE_CHECKING:
    from .Rac2Client import Rac2Context


def show_item_reception_message(ctx: 'Rac2Context', item: NetworkItem, item_name: str = None, qty: int = 1):
    """
    Queues an in-game message which informs the player they received an item.

    :param ctx: The client context
    :param item: The NetworkItem that was received
    :param item_name: The name to use for the item (if unspecified, it is obtained from the NetworkItem)
    :param qty: The amount obtained
    """
    item_data = Items.from_id(item.item)
    item_classification = item.flags
    if item_name is None:
        item_name = ctx.item_names.lookup_in_slot(item.item, ctx.slot)
    if item.location < 0:
        # For some reason, starting items don't have their classification flags set properly
        item_classification = ItemPool.get_classification(item_data).as_flag()
    if qty > 1:
        item_name += f" x{qty}"
    item_name = colorize_item_name(item_name, item_classification)

    if item.location == -2:
        # This is a starting item, mention it in the message
        if isinstance(item_data, CoordData):
            message = f"Received {item_name} (Starting Planet)"
        else:
            message = f"Received {item_name} (Starting Item)"
    elif qty > 1:
        # This is a group of packed collectables, don't indicate where they come from
        message = f"Received {item_name}"
    elif item.player == ctx.slot:
        # This is an item we found by ourselves
        message = f"Found {item_name}"
    else:
        # This is an item we received from someone
        player_name = ctx.player_names.get(item.player, "???")
        message = f"Received {item_name} from {player_name}"
    ctx.notification_manager.queue_notification(message)


async def handle_received_items(ctx: 'Rac2Context', current_items: dict[str, int]):
    for network_item in ctx.items_received:
        item = Items.from_id(network_item.item)

        if isinstance(item, EquipmentData) and current_items[item.name] == 0:
            ctx.game_interface.give_equipment_to_player(item)
            show_item_reception_message(ctx, network_item)

        if isinstance(item, CoordData) and current_items[item.name] == 0:
            ctx.game_interface.unlock_planet(item.planet_number)
            show_item_reception_message(ctx, network_item)

        if isinstance(item, ProgressiveUpgradeData):
            current_level = item.get_level_func(ctx.game_interface)
            max_level = len(item.progressive_names)
            received_count = len([recv for recv in ctx.items_received if recv.item == item.item_id])
            new_level = min(received_count, max_level)
            if current_level != new_level:
                item.set_level_func(ctx.game_interface, new_level)
            if current_level < new_level:
                show_item_reception_message(ctx, network_item, item.progressive_names[new_level - 1])

    handle_received_collectables(ctx, current_items)
    resync_problem_items(ctx)


def handle_received_collectables(ctx: 'Rac2Context', current_items: dict[str, int]):
    for item in Items.COLLECTABLES:
        item_id = Rac2World.item_name_to_id[item.name]
        received_collectables = [received_item for received_item in ctx.items_received if received_item.item == item_id]
        in_game_amount = current_items[item.name]
        received_amount = len(received_collectables)
        if received_amount < 1:
            continue

        diff = received_amount - in_game_amount
        if diff > 0 and in_game_amount < item.max_capacity:
            new_amount = min(received_amount, item.max_capacity)
            ctx.game_interface.give_collectable_to_player(item, new_amount, in_game_amount)
            show_item_reception_message(ctx, received_collectables[-1], None, diff)


def resync_problem_items(ctx: 'Rac2Context'):
    # Clank
    ctx.game_interface.pcsx2_interface.write_int8(ctx.game_interface.addresses.clank_disabled, 0)
    ctx.game_interface.pcsx2_interface.write_int8(ctx.game_interface.addresses.inventory + 4, 1)
    received_item_ids = [item.item for item in ctx.items_received]
    ctx.game_interface.pcsx2_interface.write_int8(ctx.game_interface.addresses.inventory + Items.HELI_PACK.offset,
                                                  Items.HELI_PACK.item_id in received_item_ids)
    ctx.game_interface.pcsx2_interface.write_int8(ctx.game_interface.addresses.inventory + Items.THRUSTER_PACK.offset,
                                                  Items.THRUSTER_PACK.item_id in received_item_ids)

    # Charge Boots
    ctx.game_interface.pcsx2_interface.write_int8(ctx.game_interface.addresses.inventory + Items.CHARGE_BOOTS.offset,
                                                  Items.CHARGE_BOOTS.item_id in received_item_ids)

