
from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk
from ..data.items import all_main_items, all_key_items, all_berries, badges, seasons, all_items_dict_view, all_medicine, all_tm_hm, medicine

if TYPE_CHECKING:
    from ..bizhawk_client import PokemonBWClient
    from worlds._bizhawk.context import BizHawkClientContext


async def receive_items(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> None:

    received_items_count = await client.read_var(ctx, 0x126, 4)

    if received_items_count >= len(ctx.items_received):
        return

    main_items_bag_buffer: bytearray | None = None
    key_items_bag_buffer: bytearray | None = None
    medicine_bag_buffer: bytearray | None = None
    berry_bag_buffer: bytearray | None = None
    tm_hm_bag_buffer: bytearray | None = None

    new_received = received_items_count
    for index in range(received_items_count, len(ctx.items_received)):
        network_item = ctx.items_received[index]
        name = ctx.item_names.lookup_in_game(network_item.item)
        internal_id = all_items_dict_view[name].item_id
        match name:
            case x if x in all_main_items:
                if main_items_bag_buffer is None:
                    main_items_bag_buffer = await read_bag(client, ctx,
                                                           client.main_items_bag_offset, client.main_items_bag_size)
                if not await write_to_bag(client, ctx, main_items_bag_buffer, client.main_items_bag_offset,
                                          client.main_items_bag_size, internal_id, False):
                    client.logger.warning(f"Could not add {name} to main items bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            case x if x in all_key_items:
                if key_items_bag_buffer is None:
                    key_items_bag_buffer = await read_bag(client, ctx,
                                                          client.key_items_bag_offset, client.key_items_bag_size)
                if not await write_to_bag(client, ctx, key_items_bag_buffer, client.key_items_bag_offset,
                                          client.key_items_bag_size, internal_id, False):
                    client.logger.warning(f"Could not add {name} to key items bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            case x if x in all_berries:
                if berry_bag_buffer is None:
                    berry_bag_buffer = await read_bag(client, ctx, client.berry_bag_offset, client.berry_bag_size)
                if not await write_to_bag(client, ctx, berry_bag_buffer, client.berry_bag_offset,
                                          client.berry_bag_size, internal_id, False):
                    client.logger.warning(f"Could not add {name} to key items bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            case x if x in badges.table:
                read = await bizhawk.read(
                    ctx.bizhawk_ctx, (
                        (client.save_data_address+client.badges_offset, 1, client.ram_read_write_domain),
                    )
                )
                new_state = read[0][0] | (1 << badges.table[name].bit)
                await bizhawk.write(
                    ctx.bizhawk_ctx, (
                        (client.save_data_address+client.badges_offset, [new_state], client.ram_read_write_domain),
                    )
                )
            case x if x in all_medicine:
                if medicine_bag_buffer is None:
                    medicine_bag_buffer = await read_bag(client, ctx,
                                                         client.medicine_bag_offset, client.medicine_bag_size)
                if not await write_to_bag(client, ctx, medicine_bag_buffer, client.medicine_bag_offset,
                                          client.medicine_bag_size, internal_id, False):
                    client.logger.warning(f"Could not add {name} to medicine bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            case x if x in seasons.table:
                await client.write_set_flag(ctx, seasons.table[name].flag_id)
            case x if x in all_tm_hm:
                if tm_hm_bag_buffer is None:
                    tm_hm_bag_buffer = await read_bag(client, ctx, client.tm_hm_bag_offset, client.tm_hm_bag_size)
                if not await write_to_bag(client, ctx, tm_hm_bag_buffer, client.tm_hm_bag_offset,
                                          client.tm_hm_bag_size, internal_id, False):
                    client.logger.warning(f"Could not add {name} to TM/HM bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            case _:
                client.logger.warning(f"Bad item name: {name}")
        new_received += 1

    if new_received > received_items_count:
        await client.write_var(ctx, 0x126, new_received, 4)


async def reload_key_items(client: "PokemonBWClient", ctx: "BizHawkClientContext") -> None:

    read = await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.save_data_address + client.var_offset + (2*0x126), 4, client.ram_read_write_domain),
        )
    )
    received_items_count = int.from_bytes(read[0], "little")

    key_items_bag_buffer: bytearray | None = None
    medicine_bag_buffer: bytearray | None = None
    tm_hm_bag_buffer: bytearray | None = None

    for index in range(received_items_count):
        network_item = ctx.items_received[index]
        name = ctx.item_names.lookup_in_game(network_item.item)
        internal_id = all_items_dict_view[name].item_id
        match name:
            case x if x in all_key_items:
                if key_items_bag_buffer is None:
                    key_items_bag_buffer = await read_bag(client, ctx,
                                                          client.key_items_bag_offset, client.key_items_bag_size)
                if not await write_to_bag(client, ctx, key_items_bag_buffer, client.key_items_bag_offset,
                                          client.key_items_bag_size, internal_id, True):
                    client.logger.warning(f"Could not add {name} to key items bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            case x if x in badges.table:
                read = await bizhawk.read(
                    ctx.bizhawk_ctx, (
                        (client.save_data_address+client.badges_offset, 1, client.ram_read_write_domain),
                    )
                )
                new_state = read[0][0] | (1 << badges.table[name].bit)
                await bizhawk.write(
                    ctx.bizhawk_ctx, (
                        (client.save_data_address+client.badges_offset, [new_state], client.ram_read_write_domain),
                    )
                )
            case x if x in medicine.important:
                if medicine_bag_buffer is None:
                    medicine_bag_buffer = await read_bag(client, ctx,
                                                         client.medicine_bag_offset, client.medicine_bag_size)
                if not await write_to_bag(client, ctx, medicine_bag_buffer, client.medicine_bag_offset,
                                          client.medicine_bag_size, internal_id, True):
                    client.logger.warning(f"Could not add {name} to medicine bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            case x if x in seasons.table:
                await client.write_set_flag(ctx, seasons.table[name].flag_id)
            case x if x in all_tm_hm:
                if tm_hm_bag_buffer is None:
                    tm_hm_bag_buffer = await read_bag(client, ctx, client.tm_hm_bag_offset, client.tm_hm_bag_size)
                if not await write_to_bag(client, ctx, tm_hm_bag_buffer, client.tm_hm_bag_offset,
                                          client.tm_hm_bag_size, internal_id, True):
                    client.logger.warning(f"Could not add {name} to TM/HM bag, no space left. "
                                          f"Please report this to the developers.")
                    break
            case _:
                # Other bags are irrelevant for this part
                pass


async def read_bag(client: "PokemonBWClient", ctx: "BizHawkClientContext", bag_offset: int, bag_size: int) -> bytearray:
    return bytearray((await bizhawk.read(
        ctx.bizhawk_ctx, (
            (client.save_data_address + bag_offset, bag_size * 4, client.ram_read_write_domain),
        )
    ))[0])


async def write_to_bag(client: "PokemonBWClient", ctx: "BizHawkClientContext",
                       buffer: bytearray, bag_offset: int, bag_size: int, internal_id: int, only_once: bool) -> bool:

    # go through all slots in bag
    for slot in range(bag_size):
        id_bytes_in_slot = buffer[slot*4:(slot*4)+2]
        id_in_slot = int.from_bytes(id_bytes_in_slot, "little")

        # slot which already has that item or first empty slot found
        if id_in_slot == internal_id or id_in_slot == 0:
            old_amount_bytes = buffer[(slot*4)+2:(slot*4)+4]
            old_amount = int.from_bytes(old_amount_bytes, "little")
            if only_once and old_amount > 0:
                return True  # Only when key items get reloaded

            internal_id_bytes = internal_id.to_bytes(2, "little")
            new_amount_bytes = min(old_amount + 1, 995).to_bytes(2, "little")
            # write item id and new amount to slot
            if await bizhawk.guarded_write(
                ctx.bizhawk_ctx, ((
                    client.save_data_address+bag_offset+(slot*4),
                    internal_id_bytes + new_amount_bytes,
                    client.ram_read_write_domain
                ),), ((
                    client.save_data_address+bag_offset+(slot*4),
                    id_bytes_in_slot + old_amount_bytes,
                    client.ram_read_write_domain
                ),)
            ):
                buffer[slot*4:(slot*4)+4] = internal_id_bytes + new_amount_bytes
                return True
            else:
                return await write_to_bag(client, ctx, buffer, bag_offset, bag_size, internal_id, only_once)

    else:
        # went through all slots and none can be written to
        return False
