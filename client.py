from __future__ import annotations

import functools
import itertools
from typing import TYPE_CHECKING, Any, Dict, Iterable, Iterator, List

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk import RequestFailedError
from worlds._bizhawk.client import BizHawkClient

from .data import encode_str, get_symbol
from .locations import get_level_locations, location_name_to_id, location_table
from .types import Passage

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkContext


def read(address: int, length: int, *, align: int = 1):
    assert address % align == 0, f'address: 0x{address:07x}, align: {align}'
    return (address, length, 'System Bus')

def read8(address: int):
    return read(address, 1)

def read16(address: int):
    return read(address, 2, align=2)

def read32(address: int):
    return read(address, 4, align=4)


def write(address: int, value: bytes, *, align: int = 1):
    assert address % align == 0, f'address: 0x{address:07x}, align: {align}'
    return (address, value, 'System Bus')

def write8(address: int, value: int):
    return write(address, value.to_bytes(1, 'little'))

def write16(address: int, value: int):
    return write(address, value.to_bytes(2, 'little'), align=2)

def write32(address: int, value: int):
    return write(address, value.to_bytes(4, 'little'), align=4)


guard8 = write8
guard16 = write16


def next_int(iterator: Iterator[bytes]) -> int:
    return int.from_bytes(next(iterator), 'little')


# https://docs.python.org/3.11/library/itertools.html#itertools-recipes
def batches(iterable: Iterable, n: int):
    '''Batch data into tuples of length n. The last batch may be shorter.'''

    if n < 1:
        raise ValueError('n must be at least 1')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


# class WL4CommandProcessor(BizHawkClientCommandProcessor):
#     def _cmd_deathlink(self):
#         '''Toggle death link from client. Overrides default setting.'''
#
#         from BizHawkClient import BizHawkClientContext
#         if isinstance(self.ctx, BizHawkClientContext):
#             self.ctx.death_link.client_override = True
#             self.ctx.death_link.enabled = not self.ctx.death_link.enabled
#             Utils.async_start(
#                 self.ctx.update_death_link(self.ctx.death_link.enabled),
#                 name='Update Death Link'
#             )


class DeathLinkCtx:
    enabled: bool = False
    client_override: bool = False
    pending: bool = False
    received_this_death: bool = False


def client_on_deathlink(ctx: BizHawkClientContext, data: Dict[str, Any]) -> None:
    ctx.death_link.pending = True
    type(ctx).on_deathlink(ctx, data)


class WL4Client(BizHawkClient):
    game = 'Wario Land 4'
    system = 'GBA'
    local_checked_locations: List[int]
    rom_slot_name: str

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = []

    async def validate_rom(self, client_ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        bizhawk_ctx = client_ctx.bizhawk_ctx
        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read(0x080000A0, 10),
                read(get_symbol('PlayerName'), 64)
            ]))
        except RequestFailedError:
            return False  # Should verify on the next pass

        game_name = next(read_result).decode('ascii')
        slot_name_bytes = bytes(filter(None, next(read_result)))

        if game_name != 'WARIOLANDE':
            return False

        # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
        # validating a ROM where there's no slot name to read.
        try:
            self.rom_slot_name = slot_name_bytes.decode('utf-8')
        except UnicodeDecodeError:
            logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
            return False

        client_ctx.game = self.game
        client_ctx.items_handling = 0b101
        client_ctx.want_slot_data = True

        # bizhawk_ctx.command_processor = WL4CommandProcessor(client_ctx)
        client_ctx.death_link = DeathLinkCtx()

        bound_method = client_on_deathlink.__get__(client_ctx, client_ctx.__class__)
        setattr(client_ctx, "on_deathlink", bound_method)

        return True

    async def set_auth(self, client_ctx: BizHawkClientContext) -> None:
        client_ctx.auth = self.rom_slot_name

    async def game_watcher(self, client_ctx: BizHawkClientContext) -> None:
        get_int = functools.partial(int.from_bytes, byteorder='little')
        bizhawk_ctx = client_ctx.bizhawk_ctx

        game_mode_address = get_symbol('GlobalGameMode')
        game_state_address = get_symbol('sGameSeq')
        wario_stop_flag_address = get_symbol('usWarStopFlg')
        level_status_address = get_symbol('LevelStatusTable')
        received_item_count_address = level_status_address + 14  # Collection status for unused Entry level
        multiworld_state_address = get_symbol('MultiworldState')
        incoming_item_address = get_symbol('IncomingItemID')
        item_sender_address = get_symbol('IncomingItemSender')
        death_link_address = get_symbol('DeathLinkEnabled')
        wario_health_address = get_symbol('WarioHeart')

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read8(game_mode_address),
                read8(game_state_address),
                read16(wario_stop_flag_address),
                read(level_status_address, 6 * 6 * 4),
                read8(multiworld_state_address),
                read16(received_item_count_address),
                read8(death_link_address),
                read8(wario_health_address),
            ]))
        except RequestFailedError:
            return

        game_mode = next_int(read_result)
        game_state = next_int(read_result)
        wario_stop_flag = next_int(read_result)
        item_status = tuple(map(get_int, batches(next(read_result), 4)))
        multiworld_state = next_int(read_result)
        received_item_count = next_int(read_result)
        death_link_flag = next_int(read_result)
        wario_health = next_int(read_result)

        # Ensure safe state
        gameplay_state = (game_mode, game_state)
        safe_states = [
            (1, 2),  # Passage select
            (2, 2),  # Playing level
        ]
        if gameplay_state not in safe_states:
            return

        # Turn on death link if it is on, and if the client hasn't overriden it
        if (death_link_flag
                and not client_ctx.death_link.enabled
                and not client_ctx.death_link.client_override):
            await client_ctx.update_death_link(True)
            client_ctx.death_link.enabled = True

        locations = []
        game_clear = False

        # Parse item status bits
        for passage in range(6):
            for level in range(4):
                status_bits = item_status[passage * 6 + level] >> 8
                for location in get_level_locations(passage, level):
                    bit = location_table[location].flag()
                    location_id = location_name_to_id[location]
                    if status_bits & bit and location_id in client_ctx.server_locations:
                        locations.append(location_id)

            # TODO: Boss event flags

        if item_status[Passage.GOLDEN * 6 + 4] & 0x10:
            game_clear = True

        # Send locations
        if self.local_checked_locations != locations:
            self.local_checked_locations = locations
            await client_ctx.send_msgs([{
                'cmd': 'LocationChecks',
                'locations': locations
            }])

        # Send game clear
        if game_clear and not client_ctx.finished_game:
            await client_ctx.send_msgs([{
                'cmd': 'StatusUpdate',
                'status': ClientStatus.CLIENT_GOAL
            }])

        # TODO: Send tracker event flags

        # Send death link
        if client_ctx.death_link.enabled:
            if gameplay_state == (2, 2) and wario_health == 0:
                client_ctx.death_link.pending = False
                if not client_ctx.death_link.sent_this_death:
                    client_ctx.death_link.sent_this_death = True
                    await client_ctx.send_death()
            else:
                client_ctx.death_link.sent_this_death = False

        write_list = []
        guard_list = [
            # Ensure game state hasn't changed
            guard8(game_mode_address, game_mode),
            guard8(game_state_address, game_state),
        ]

        if gameplay_state == (2, 2):
            if wario_stop_flag != 0:
                return
            guard_list.append(guard16(wario_stop_flag_address, 0))

        # Receive death link
        if client_ctx.death_link.enabled and client_ctx.death_link.pending:
            client_ctx.death_link.sent_this_death = True
            write_list.append(write8(wario_health_address, 0))

        # If the game hasn't received all items yet and the game isn't showing the player
        # another item, then set up the next item message
        if received_item_count < len(client_ctx.items_received) and multiworld_state == 0:
            next_item = client_ctx.items_received[received_item_count]
            next_item_id = next_item.item & 0xFF
            next_item_sender = encode_str(client_ctx.player_names[next_item.player]) + b'\xFE'

            write_list += [
                write8(incoming_item_address, next_item_id),
                write(item_sender_address, next_item_sender),
                write8(multiworld_state_address, 1),
            ]
            guard_list.append(guard8(multiworld_state_address, 0))

        try:
            await bizhawk.guarded_write(bizhawk_ctx, write_list, guard_list)
        except RequestFailedError:
            return
