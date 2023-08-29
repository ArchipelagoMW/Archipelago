from __future__ import annotations

from typing import TYPE_CHECKING, List

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


async def read_single_sequence(ctx: BizHawkContext, address: int, length: int) -> bytes:
    return (await bizhawk.read(ctx, [read(address, length)]))[0]


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
            game_name = (await read_single_sequence(bizhawk_ctx, 0x080000A0, 10)).decode('ascii')
            if game_name != 'WARIOLANDE':
                return False

            # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
            # validating a ROM where there's no slot name to read.
            try:
                slot_name_bytes = await read_single_sequence(bizhawk_ctx, get_symbol('PlayerName'), 64)
                self.rom_slot_name = bytes(filter(None, slot_name_bytes)).decode('utf-8')
            except UnicodeDecodeError:
                logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
                return False
        except UnicodeDecodeError:
            return False
        except RequestFailedError:
            return False  # Should verify on the next pass

        client_ctx.game = self.game
        client_ctx.items_handling = 0b101
        client_ctx.want_slot_data = True
        return True

    async def set_auth(self, client_ctx: BizHawkClientContext) -> None:
        client_ctx.auth = self.rom_slot_name

    async def game_watcher(self, client_ctx: BizHawkClientContext) -> None:
        bizhawk_ctx = client_ctx.bizhawk_ctx
        try:
            game_mode_address = get_symbol('GlobalGameMode')
            game_state_address = get_symbol('sGameSeq')
            wario_stop_flag_address = get_symbol('usWarStopFlg')
            level_status_address = get_symbol('LevelStatusTable')
            received_item_count_address = level_status_address + 14  # Collection status for unused Entry level
            multiworld_state_address = get_symbol('MultiworldState')
            incoming_item_address = get_symbol('IncomingItemID')
            item_sender_address = get_symbol('IncomingItemSender')

            read_result = await bizhawk.read(bizhawk_ctx, [
                read8(game_mode_address),
                read8(game_state_address),
                read16(wario_stop_flag_address),
                read(level_status_address, 6 * 6 * 4),
                read8(multiworld_state_address),
                read16(received_item_count_address),
            ])
            game_mode = read_result[0][0]
            game_state = read_result[1][0]
            wario_stop_flag = int.from_bytes(read_result[2], 'little')
            item_status = [int.from_bytes(read_result[3][i:i+4], 'little')
                           for i in range(0, 36*4, 4)]
            multiworld_state = read_result[4][0]
            received_item_count = int.from_bytes(read_result[5], 'little')

            # Ensure safe state
            gameplay_state = (game_mode, game_state)
            safe_states = [
                (1, 2),  # Passage select
                (2, 2),  # Playing level
            ]
            if gameplay_state not in safe_states:
                return

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

            # TODO: Send deathlink

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

            # TODO: Receive deathlink

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

            await bizhawk.guarded_write(bizhawk_ctx, write_list, guard_list)

        except RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass
