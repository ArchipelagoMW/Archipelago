from __future__ import annotations

import functools
import itertools
from typing import TYPE_CHECKING, Dict, Iterable, Iterator, List, Optional, Set

import Utils
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import Passage, encode_str, get_symbol
from .locations import get_level_locations, location_name_to_id, location_table

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


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


# itertools.batched from Python 3.12
# https://docs.python.org/3.11/library/itertools.html#itertools-recipes
def _batched(iterable, n):
    if n < 1:
        raise ValueError('n must be at least 1')
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch

def batches(iterable: Iterable, n: int):
    """Batch data into tuples of length n. The last batch may be shorter."""

    try:
        return itertools.batched(iterable, n)
    except AttributeError:
        return _batched(iterable, n)


# These flags are communicated to the tracker as a bitfield in this order, from
# least to most significant bit.
LEVEL_CLEAR_FLAGS = [
    'Hall of Hieroglyphs',
    None,
    None,
    None,
    'Spoiled Rotten',
    'Palm Tree Paradise',
    'Wildflower Fields',
    'Mystic Lake',
    'Monsoon Jungle',
    'Cractus',
    'The Curious Factory',
    'The Toxic Landfill',
    '40 Below Fridge',
    'Pinball Zone',
    'Cuckoo Condor',
    'Toy Block Tower',
    'The Big Board',
    'Doodle Woods',
    'Domino Row',
    'Aerodent',
    'Crescent Moon Village',
    'Arabian Night',
    'Fiery Cavern',
    'Hotel Horror',
    'Catbat',
    'Golden Passage',
    None,
    None,
    None,
    None,
]

TRACKER_EVENT_FLAGS = [
    *filter(None, LEVEL_CLEAR_FLAGS),
]


def cmd_deathlink(self):
    """Toggle death link from client. Overrides default setting."""

    client_handler = self.ctx.client_handler
    client_handler.death_link.client_override = True
    client_handler.death_link.enabled = not client_handler.death_link.enabled
    Utils.async_start(
        self.ctx.update_death_link(client_handler.death_link.enabled),
        name='Update Death Link'
    )


class DeathLinkCtx:
    enabled: bool = False
    update_pending: bool = False
    pending: bool = False
    sent_this_death: bool = False

    def __repr__(self):
        return (f'{type(self)} {{ enabled: {self.enabled}, '
                f'update_pending: {self.update_pending}, '
                f'pending: {self.pending}, '
                f'sent_this_death: {self.sent_this_death} }}')

    def __str__(self):
        return repr(self)


class WL4Client(BizHawkClient):
    game = 'Wario Land 4'
    system = 'GBA'
    patch_suffix = '.apwl4'
    local_checked_locations: List[int]
    local_hinted_locations: Set[int]
    local_set_events: Dict[str, bool]
    local_room: int
    rom_slot_name: Optional[str]

    death_link: DeathLinkCtx

    dc_pending: bool

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = []
        self.local_hinted_locations = set()
        self.local_set_events = {}
        self.local_room = (1 << 24) - 1
        self.rom_slot_name = None
        self.death_link = DeathLinkCtx()

    async def validate_rom(self, client_ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        bizhawk_ctx = client_ctx.bizhawk_ctx
        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read(0x080000A0, 12),
                read(get_symbol('PlayerName'), 64),
                read(get_symbol('SeedName'), 64),
            ]))
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        game_name = next(read_result).decode('ascii')
        slot_name_bytes = next(read_result).rstrip(b'\0')
        seed_name_bytes = next(read_result).rstrip(b'\0')

        if not game_name.startswith('WARIOLAND'):
            return False
        if game_name in ('WARIOLANDE\0\0', 'WARIOLAND\0\0\0'):
            logger.info('You appear to be running an unpatched version of Wario Land 4. You need '
                        'to generate a patch file and use it to create a patched ROM.')
            return False
        if game_name not in ('WARIOLANDAPE', 'WARIOLANDAPJ'):
            logger.info('The patch file used to create this ROM is not compatible with this client. '
                        'Double check your client version against the version being used by the generator.')
            return False

        # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
        # validating a ROM where there's no slot name to read.
        try:
            self.rom_slot_name = slot_name_bytes.decode('utf-8')
        except UnicodeDecodeError:
            logger.info('Could not read slot name from ROM. Are you sure this ROM matches this client version?')
            return False

        client_ctx.game = self.game
        client_ctx.items_handling = 0b001
        client_ctx.want_slot_data = True
        try:
            client_ctx.seed_name = seed_name_bytes.decode('utf-8')
        except UnicodeDecodeError:
            logger.info('Could not determine seed name from ROM. Are you sure this ROM matches this client version?')
            return False

        client_ctx.command_processor.commands['deathlink'] = cmd_deathlink

        self.dc_pending = False

        return True

    async def set_auth(self, client_ctx: BizHawkClientContext) -> None:
        client_ctx.auth = self.rom_slot_name

    async def game_watcher(self, client_ctx: BizHawkClientContext) -> None:
        if self.dc_pending:
            await client_ctx.disconnect()
            return

        if self.death_link.update_pending:
            await client_ctx.update_death_link(self.death_link.enabled)
            self.death_link.update_pending = False

        get_int = functools.partial(int.from_bytes, byteorder='little')
        bizhawk_ctx = client_ctx.bizhawk_ctx

        game_mode_address = get_symbol('GlobalGameMode')
        game_state_address = get_symbol('sGameSeq')
        wario_stop_flag_address = get_symbol('usWarStopFlg')
        level_status_address = get_symbol('W4ItemStatus')
        received_item_count_address = level_status_address + 14  # Collection status for unused Entry level
        multiworld_state_address = get_symbol('MultiworldState')
        incoming_item_address = get_symbol('IncomingItemID')
        item_sender_address = get_symbol('IncomingItemSender')
        wario_health_address = get_symbol('WarioHeart')
        timer_status_address = get_symbol('ucTimeUp')
        multiworld_send_address = get_symbol('SendMultiworldItemsImmediately')
        passage_address = get_symbol('PassageID')
        level_address = get_symbol('InPassageLevelID')
        room_address = get_symbol('CurrentRoomId')
        collected_items_address = get_symbol('CollectedItems')

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read8(game_mode_address),
                read8(game_state_address),
                read16(wario_stop_flag_address),
                read(level_status_address, 6 * 6 * 4),
                read8(multiworld_state_address),
                read16(received_item_count_address),
                read8(wario_health_address),
                read8(timer_status_address),
                read8(multiworld_send_address),
                read8(passage_address),
                read8(level_address),
                read8(room_address),
                read32(collected_items_address),
            ]))
        except bizhawk.RequestFailedError:
            return

        game_mode = next_int(read_result)
        game_state = next_int(read_result)
        wario_stop_flag = next_int(read_result)
        item_status = tuple(map(get_int, batches(next(read_result), 4)))
        multiworld_state = next_int(read_result)
        received_item_count = next_int(read_result)
        wario_health = next_int(read_result)
        timer_status = next_int(read_result)
        send_level_locations = next_int(read_result)
        passage_id = next_int(read_result)
        in_passage_level_id = next_int(read_result)
        room_id = next_int(read_result)
        level_item_flags = next_int(read_result)

        # Ensure safe state
        gameplay_state = (game_mode, game_state)
        write_safe_states = [
            (1, 2),  # Passage select
            (2, 2),  # Playing level
        ]
        read_safe_states = [
            *write_safe_states,
            (1, 0x31),  # Level select in passage
            *((1, seq) for seq in range(0x16, 0x19)),  # Died/gave up
            *((0, seq) for seq in range(0x1A, 0x20)),  # End of game cutscene
        ]

        if gameplay_state not in read_safe_states:
            return

        locations = []
        hint_locations = set()
        events = {flag: False for flag in TRACKER_EVENT_FLAGS}
        game_clear = False

        if in_passage_level_id >= 4 or gameplay_state != (2, 2):
            level_item_flags = 0

        # Parse item status bits
        for passage in Passage:
            for level in range(5):
                status_bits = item_status[passage * 6 + level] >> 8
                hint_bits = 0

                if (passage, level) == (passage_id, in_passage_level_id):
                    if send_level_locations:
                        status_bits |= level_item_flags
                    elif game_mode == 1 and game_state in range(0x16, 0x19):
                        hint_bits = level_item_flags & ~status_bits

                for location in get_level_locations(passage, level):
                    location_id = location_name_to_id[location]
                    if location_id not in client_ctx.server_locations:
                        continue

                    bit = location_table[location].flag
                    if status_bits & bit:
                        locations.append(location_id)
                    if hint_bits & bit:
                        hint_locations.add(location_id)

                keyzer_bit = item_status[passage * 6 + level] & (1 << 5)
                level_name = LEVEL_CLEAR_FLAGS[passage * 5 + level]
                if level_name:
                    level_clear = bool(keyzer_bit)
                    events[level_name] = level_clear

        if item_status[Passage.GOLDEN * 6 + 4] & 0x10:
            game_clear = True

        # Send locations
        if self.local_checked_locations != locations:
            self.local_checked_locations = locations
            await client_ctx.send_msgs([{
                'cmd': 'LocationChecks',
                'locations': locations
            }])

        # Send hints
        hint_locations.difference_update(self.local_hinted_locations)
        if hint_locations:
            self.local_hinted_locations.update(hint_locations)
            await client_ctx.send_msgs([{
                'cmd': 'LocationScouts',
                'locations': hint_locations,
                'create_as_hint': 2
            }])

        # Send game clear
        if game_clear and not client_ctx.finished_game:
            await client_ctx.send_msgs([{
                'cmd': 'StatusUpdate',
                'status': ClientStatus.CLIENT_GOAL
            }])

        # Send tracker event flags
        if self.local_set_events != events and client_ctx.slot is not None:
            event_bitfield = 0
            for i, flag in enumerate(TRACKER_EVENT_FLAGS):
                if events[flag]:
                    event_bitfield |= 1 << i
            await client_ctx.send_msgs([{
                'cmd': 'Set',
                'key': f'wl4_events_{client_ctx.team}_{client_ctx.slot}',
                'default': 0,
                'want_reply': False,
                'operations': [{'operation': 'or', 'value': event_bitfield}]
            }])
            self.local_set_events = events

        # Send Wario's location
        if game_mode not in (2, 4):
            room = (1 << 24) - 1
        else:
            room = (passage_id << 16) | (in_passage_level_id << 8) | room_id
        if self.local_room != room and client_ctx.slot is not None:
            await client_ctx.send_msgs([{
                'cmd': 'Set',
                'key': f'wl4_room_{client_ctx.team}_{client_ctx.slot}',
                'default': 0,
                'want_reply': False,
                'operations': [{'operation': 'replace', 'value': room}]
            }])
            self.local_room = room

        # Send death link
        if self.death_link.enabled:
            time_up = timer_status in range(4, 11)
            if gameplay_state == (2, 2) and (wario_health == 0 or time_up):
                self.death_link.pending = False
                if not self.death_link.sent_this_death:
                    self.death_link.sent_this_death = True
                    death_text = f'{client_ctx.auth} timed out' if time_up else ''
                    await client_ctx.send_death(death_text)
            else:
                self.death_link.sent_this_death = False

        if gameplay_state not in write_safe_states:
            return

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
        if self.death_link.enabled and self.death_link.pending:
            self.death_link.sent_this_death = True
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
        except bizhawk.RequestFailedError:
            return

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            self.local_checked_locations = []
            self.local_hinted_locations = set()
            self.local_set_events = {}
            self.local_room = (1 << 24) - 1
            if args["slot_data"].get("death_link"):
                self.death_link.enabled = True
                self.death_link.update_pending = True
        if cmd == 'RoomInfo':
            if ctx.seed_name and ctx.seed_name != args['seed_name']:
                # CommonClient's on_package displays an error to the user in this case, but connection is not cancelled.
                self.dc_pending = True
        if cmd == 'Bounced':
            tags = args.get('tags', [])
            if 'DeathLink' in tags and args['data']['source'] != ctx.auth:
                self.death_link.pending = True
