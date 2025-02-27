from __future__ import annotations

import functools
import struct
from typing import TYPE_CHECKING

import Utils
from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import ItemFlag, Passage, encode_str, get_symbol
from .locations import get_level_locations, location_name_to_id, location_table

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkContext


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

BOSS_LEVEL = 4

PASSAGE_SELECT_STATE = (1, 2)
LEVEL_SELECT_STATE = (1, 0x30)
WARIO_GAMEPLAY_STATE = (2, 2)
LEVEL_EJECTION_STATES = tuple((1, seq) for seq in range(0x16, 0x19))
END_OF_GAME_STATES = tuple((0, seq) for seq in range(0x1A, 0x20))

LOCAL_ITEMS = 0b001
CREATE_HINT_ONLY_NEW = 2

TRACKER_ROOM_NONE = (1 << 24) - 1

MULTIWORLD_IDLE = 0
MULTIWORLD_ITEM_QUEUED = 1


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

get_int = functools.partial(int.from_bytes, byteorder='little')


def cmd_toggle_deathlink(self):
    """Toggle death link from client. Overrides default setting."""

    client_handler = self.ctx.client_handler
    client_handler.death_link.client_override = True
    client_handler.death_link.enabled = not client_handler.death_link.enabled
    Utils.async_start(
        self.ctx.update_death_link(client_handler.death_link.enabled),
        name='Update Death Link'
    )

def cmd_receive_death(self):
    """Debug tool: Send a death to the game to test death link is working."""
    client_handler = self.ctx.client_handler
    if client_handler.death_link.enabled:
        client_handler.death_link.pending = True


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
    local_checked_locations: set[int]
    local_hinted_locations: set[int]
    local_set_events: dict[str, bool]
    local_room: int
    rom_slot_name: str | None

    death_link: DeathLinkCtx

    dc_pending: bool

    def __init__(self):
        super().__init__()
        self.local_checked_locations = []
        self.local_hinted_locations = set()
        self.local_set_events = {}
        self.local_room = TRACKER_ROOM_NONE
        self.rom_slot_name = None
        self.death_link = DeathLinkCtx()

    async def validate_rom(self, client_ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        bizhawk_ctx = client_ctx.bizhawk_ctx
        try:
            read_result = await bizhawk.read(
                bizhawk_ctx,
                [
                    read(0x080000A0, 12),
                    read(get_symbol('PlayerName'), 64),
                    read(get_symbol('SeedName'), 64),
                ]
            )
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        game_name_bytes, slot_name_bytes, seed_name_bytes = read_result

        game_name = game_name_bytes.decode('ascii')
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
            self.rom_slot_name = slot_name_bytes.rstrip(b'\0').decode('utf-8')
        except UnicodeDecodeError:
            logger.info('Could not read slot name from ROM. Are you sure this ROM matches this client version?')
            return False

        client_ctx.game = self.game
        client_ctx.items_handling = LOCAL_ITEMS
        client_ctx.want_slot_data = True
        try:
            client_ctx.seed_name = seed_name_bytes.rstrip(b'\0').decode('utf-8')
        except UnicodeDecodeError:
            logger.info('Could not determine seed name from ROM. Are you sure this ROM matches this client version?')
            return False

        client_ctx.command_processor.commands['deathlink'] = cmd_toggle_deathlink
        # client_ctx.command_processor.commands['kill'] = cmd_receive_death

        self.dc_pending = False

        return True

    async def set_auth(self, client_ctx: BizHawkClientContext):
        client_ctx.auth = self.rom_slot_name

    async def get_game_state(self, bizhawk_ctx: BizHawkContext) -> tuple[int, int] | None:
        read_result = await bizhawk.read(
            bizhawk_ctx,
            [
                read16(game_mode_address),
                read16(game_state_address),
            ]
        )
        return tuple(map(get_int, read_result))

    @staticmethod
    def guard_game_state(game_state: tuple[int, int]):
        return [
            guard16(game_mode_address, game_state[0]),
            guard16(game_state_address, game_state[1]),
        ]

    @staticmethod
    def get_collected_locations(client_ctx: BizHawkClientContext, passage: int, level: int, collection: int):
        for location in get_level_locations(passage, level):
            location_id = location_name_to_id[location]
            if location_id not in client_ctx.server_locations:
                continue

            bit = location_table[location].flag
            if collection & bit:
                yield location_id

    async def handle_inventory(self, client_ctx: BizHawkClientContext):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        gameplay_state = await self.get_game_state(bizhawk_ctx)
        if gameplay_state not in (PASSAGE_SELECT_STATE, LEVEL_SELECT_STATE, WARIO_GAMEPLAY_STATE):
            return

        inventory_result = await bizhawk.guarded_read(
            bizhawk_ctx,
            [read(level_status_address, len(Passage) * 6 * 4)],
            self.guard_game_state(gameplay_state)
        )
        collection_result = await bizhawk.guarded_read(
            bizhawk_ctx,
            [
                read8(passage_address),
                read8(level_address),
                read32(collected_items_address),
            ],
            [
                *self.guard_game_state(WARIO_GAMEPLAY_STATE),
                guard8(multiworld_send_address, True)
            ]
        )

        if inventory_result is None:
            return
        inventory = struct.iter_unpack("<6I", inventory_result[0])

        locations: set[int] = set()
        events: dict[str, bool] = {}

        for passage, levels in zip(Passage, inventory, strict=True):
            for level, status_bits in enumerate(levels):
                locations.update(self.get_collected_locations(client_ctx, passage, level, status_bits >> 8))
                if level > 4:
                    continue
                level_name = LEVEL_CLEAR_FLAGS[passage * 5 + level]
                if level_name:
                    events[level_name] = bool(status_bits & ItemFlag.KEYZER)

        if collection_result is not None:
            passage, level, collection = map(get_int, collection_result)
            if level < BOSS_LEVEL:
                locations.update(self.get_collected_locations(client_ctx, passage, level, collection))

        if self.local_checked_locations != locations:
            self.local_checked_locations = locations
            await client_ctx.send_msgs([{
                'cmd': 'LocationChecks',
                'locations': locations
            }])

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

    async def handle_hints(self, client_ctx: BizHawkClientContext):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        gameplay_state = await self.get_game_state(bizhawk_ctx)
        if gameplay_state not in LEVEL_EJECTION_STATES:
            return

        read_result = await bizhawk.guarded_read(
            bizhawk_ctx,
            [
                read8(passage_address),
                read8(level_address),
                read32(collected_items_address),
            ],
            [
                *self.guard_game_state(gameplay_state),
                guard8(multiworld_send_address, False)
            ]
        )
        if read_result is None:
            return

        passage, level, collection = map(get_int, read_result)
        locations: set[int] = set(self.get_collected_locations(client_ctx, passage, level, collection))

        locations.difference_update(self.local_checked_locations)
        locations.difference_update(self.local_hinted_locations)
        if locations:
            self.local_hinted_locations.update(locations)
            await client_ctx.send_msgs([{
                'cmd': 'LocationScouts',
                'locations': locations,
                'create_as_hint': CREATE_HINT_ONLY_NEW
            }])

    async def handle_current_room(self, client_ctx: BizHawkClientContext):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        gameplay_state = await self.get_game_state(bizhawk_ctx)
        if gameplay_state not in (PASSAGE_SELECT_STATE, LEVEL_SELECT_STATE, WARIO_GAMEPLAY_STATE):
            return

        if gameplay_state == WARIO_GAMEPLAY_STATE:
            read_result = await bizhawk.read(bizhawk_ctx, [
                read8(passage_address),
                read8(level_address),
                read8(room_address),
            ])

            passage, level, room = map(get_int, read_result)
            current_room = passage << 16 | level << 8 | room
        else:
            current_room = TRACKER_ROOM_NONE

        if self.local_room != current_room and client_ctx.slot is not None:
            await client_ctx.send_msgs([{
                'cmd': 'Set',
                'key': f'wl4_room_{client_ctx.team}_{client_ctx.slot}',
                'default': TRACKER_ROOM_NONE,
                'want_reply': False,
                'operations': [{'operation': 'replace', 'value': current_room}]
            }])
            self.local_room = current_room

    async def handle_goal(self, client_ctx: BizHawkClientContext):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        gameplay_state = await self.get_game_state(bizhawk_ctx)
        if gameplay_state not in (WARIO_GAMEPLAY_STATE, *END_OF_GAME_STATES):
            return

        read_result = await bizhawk.guarded_read(
            bizhawk_ctx,
            [read32(level_status_address + 4 * (6 * Passage.GOLDEN + BOSS_LEVEL))],
            self.guard_game_state(gameplay_state)
        )

        if read_result is None or client_ctx.finished_game:
            return

        if get_int(read_result[0]) & ItemFlag.DIVA_CLEAR:
            await client_ctx.send_msgs([{
                'cmd': 'StatusUpdate',
                'status': ClientStatus.CLIENT_GOAL
            }])

    async def handle_death_link(self, client_ctx: BizHawkClientContext):
        if self.death_link.update_pending:
            await client_ctx.update_death_link(self.death_link.enabled)
            self.death_link.update_pending = False

        if not self.death_link.enabled:
            return

        bizhawk_ctx = client_ctx.bizhawk_ctx

        read_result = await bizhawk.guarded_read(
            bizhawk_ctx,
            [
                read8(wario_health_address),
                read8(timer_status_address),
            ],
            [
                *self.guard_game_state(WARIO_GAMEPLAY_STATE)
            ]
        )
        if read_result is None:
            return

        wario_health, timer_status = map(get_int, read_result)
        time_up = timer_status in range(4, 11)

        if wario_health == 0 or time_up:
            self.death_link.pending = False
            if not self.death_link.sent_this_death:
                self.death_link.sent_this_death = True
                death_text = f'{client_ctx.auth} timed out' if time_up else ''
                await client_ctx.send_death(death_text)
        else:
            self.death_link.sent_this_death = False

        if self.death_link.pending:
            await bizhawk.guarded_write(
                bizhawk_ctx,
                [write8(wario_health_address, 0)],
                [
                    *self.guard_game_state(WARIO_GAMEPLAY_STATE),
                    guard16(wario_stop_flag_address, 0),
                ]
            )
            self.death_link.sent_this_death = True

    async def handle_received_items(self, client_ctx: BizHawkClientContext):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        gameplay_state = await self.get_game_state(bizhawk_ctx)
        if gameplay_state not in (PASSAGE_SELECT_STATE, WARIO_GAMEPLAY_STATE):
            return

        read_result = await bizhawk.read(
            bizhawk_ctx,
            [read16(received_item_count_address)]
        )

        received_item_count = get_int(read_result[0])
        if received_item_count >= len(client_ctx.items_received):
            return

        next_item = client_ctx.items_received[received_item_count]
        next_item_id = next_item.item & 0xFF
        next_item_sender = encode_str(client_ctx.player_names[next_item.player]) + b'\xFE'
        await bizhawk.guarded_write(
            bizhawk_ctx,
            [
                write8(incoming_item_address, next_item_id),
                write(item_sender_address, next_item_sender),
                write8(multiworld_state_address, MULTIWORLD_ITEM_QUEUED),
            ],
            [
                *self.guard_game_state(gameplay_state),
                guard8(multiworld_state_address, MULTIWORLD_IDLE)
            ]
        )

    async def game_watcher(self, client_ctx: BizHawkClientContext):
        if self.dc_pending:
            await client_ctx.disconnect()
            return

        try:
            await self.handle_inventory(client_ctx)
            await self.handle_hints(client_ctx)
            await self.handle_current_room(client_ctx)
            await self.handle_received_items(client_ctx)
            await self.handle_death_link(client_ctx)
            await self.handle_goal(client_ctx)
        except bizhawk.RequestFailedError:
            pass

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == "Connected":
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
