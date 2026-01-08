"""
Classes and functions related to interfacing with the BizHawk Client for Metroid: Zero Mission
"""

from __future__ import annotations

import itertools
import struct
from typing import TYPE_CHECKING, Dict, Iterable, Iterator, NamedTuple, Optional, Set, Tuple

from NetUtils import ClientStatus, NetworkItem
import Utils
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .items import ItemData, item_data_table, major_item_data_table
from .locations import (brinstar_location_table, kraid_location_table, norfair_location_table,
                        ridley_location_table, tourian_location_table, crateria_location_table,
                        chozodia_location_table)
from .options import FullyPoweredSuit
from .patcher.constants import Event, ItemType
from .patcher.items import ItemData as ZMItemData
from .patcher.symbols import get_symbol
from .patcher.text import Message, make_item_message

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


def read(address: int, length: int, *, align: int = 1):
    assert address % align == 0, f"address: 0x{address:07x}, align: {align}"
    return (address, length, "System Bus")

def read8(address: int):
    return read(address, 1)

def read16(address: int):
    return read(address, 2, align=2)

def read32(address: int):
    return read(address, 4, align=4)


def write(address: int, value: bytes, *, align: int = 1):
    assert address % align == 0, f"address: 0x{address:07x}, align: {align}"
    return (address, value, "System Bus")

def write8(address: int, value: int):
    return write(address, value.to_bytes(1, "little"))

def write16(address: int, value: int):
    return write(address, value.to_bytes(2, "little"), align=2)

def write32(address: int, value: int):
    return write(address, value.to_bytes(4, "little"), align=4)


guard = write
guard8 = write8
guard16 = write16
guard32 = write32


def get_int(b: bytes) -> int:
    return int.from_bytes(b, "little")


def next_int(iterator: Iterator[bytes]) -> int:
    return get_int(next(iterator))


# itertools.batched from Python 3.12
# https://docs.python.org/3.11/library/itertools.html#itertools-recipes
def batched(iterable, n):
    if n < 1:
        raise ValueError("n must be at least 1")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


# DEOREM_KILLED and RUINS_TEST_PASSED are out of order to maintain tracker compatibility. DEOREM_KILLED was before any
# of the vanilla events, and RUINS_TEST_PASSED replaces the vanilla FULLY_POWERED_SUIT_OBTAINED.
EVENT_FLAGS = [
    Event.DEOREM_KILLED,
    Event.ACID_WORM_KILLED,
    Event.KRAID_KILLED,
    Event.IMAGO_COCOON_KILLED,
    Event.IMAGO_KILLED,
    Event.RIDLEY_KILLED,
    Event.MOTHER_BRAIN_KILLED,
    Event.ESCAPED_ZEBES,
    Event.RUINS_TEST_PASSED,
    Event.MECHA_RIDLEY_KILLED,
    Event.ESCAPED_CHOZODIA,
]


def cmd_deathlink(self):
    """Toggle death link from client. Overrides default setting."""

    client_handler = self.ctx.client_handler
    client_handler.death_link.enabled = not client_handler.death_link.enabled
    Utils.async_start(
        self.ctx.update_death_link(client_handler.death_link.enabled),
        name="Update Death Link"
    )


def cmd_kill(self):
    """Receive a death link on command."""
    self.ctx.client_handler.death_link.pending = True


class DeathLinkCtx:
    enabled: bool = False
    update_pending = False
    pending: bool = False
    sent_this_death: bool = False

    def __repr__(self):
        return (f"{type(self)} {{ enabled: {self.enabled}, "
                f"update_pending: {self.update_pending}, "
                f"pending: {self.pending}, "
                f"sent_this_death: {self.sent_this_death} }}")

    def __str__(self):
        return repr(self)


class TankList(NamedTuple):
    energy: int
    missile: int
    super_missile: int
    power_bomb: int


class ZMConstants:
    # Constants
    GM_INGAME = 4
    GM_GAMEOVER = 6
    GM_CHOZODIA_ESCAPE = 7
    GM_CREDITS = 8
    SUB_GAME_MODE_PLAYING = 2
    SUB_GAME_MODE_DYING = 5
    AREA_MAX = 7
    ITEM_NONE = 0xFF
    SUIT_FULLY_POWERED = 1
    SUIT_SUITLESS = 2
    SPOSE_SAVING_LOADING_GAME = 44

    # Statics
    sStartingHealthAmmo = TankList(99, 0, 0, 0)
    sTankIncreaseAmount = [
        TankList(100, 5, 2, 2),
        TankList(100, 5, 2, 2),
        TankList(50, 2, 1, 1),
    ]

    # Variable addresses
    gMainGameMode = get_symbol("gMainGameMode")
    gGameModeSub1 = get_symbol("gGameModeSub1")
    gPreventMovementTimer = get_symbol("gPreventMovementTimer")
    gDifficulty = get_symbol("gDifficulty")
    gSamusData = get_symbol("gSamusData")
    gEquipment = get_symbol("gEquipment")
    gRandoEquipment = get_symbol("gRandoEquipment")
    gEventsTriggered = get_symbol("gEventsTriggered")
    gCurrentArea = get_symbol("gCurrentArea")
    gRandoLocationBitfields = get_symbol("gRandoLocationBitfields")
    gIncomingMessage = get_symbol("gIncomingMessage")


class MZMClient(BizHawkClient):
    game = "Metroid Zero Mission"
    system = "GBA"
    patch_suffix = ".apmzm"

    local_checked_locations: Set[int]
    local_set_events: Dict[Event, bool]
    local_area: int

    rom_slot_name: Optional[str]

    death_link: DeathLinkCtx

    dc_pending: bool

    def __init__(self) -> None:
        super().__init__()
        self.local_checked_locations = set()
        self.local_set_events = {flag: False for flag in EVENT_FLAGS}
        self.local_area = 0
        self.ignore_locals_written = False
        self.rom_slot_name = None

    async def validate_rom(self, client_ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        bizhawk_ctx = client_ctx.bizhawk_ctx
        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read(0x80000A0, 12),
                read(get_symbol("sRandoSeed", 0), 64),
                read(get_symbol("sRandoSeed", 64), 64),
            ]))
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        game_name = next(read_result).decode("ascii")
        slot_name_bytes = next(read_result).rstrip(b"\0")
        seed_name_bytes = next(read_result).rstrip(b"\0")

        if game_name != "ZEROMISSIONE":
            return False

        # Check if we can read the slot name. Doing this here instead of set_auth as a protection against
        # validating a ROM where there's no slot name to read.
        try:
            self.rom_slot_name = slot_name_bytes.decode("utf-8")
        except UnicodeDecodeError:
            logger.info("Could not read slot name from ROM. Are you sure this ROM matches this client version?")
            return False

        client_ctx.game = self.game
        client_ctx.items_handling = 0b111
        client_ctx.want_slot_data = True
        try:
            client_ctx.seed_name = seed_name_bytes.decode("utf-8")
        except UnicodeDecodeError:
            logger.info("Could not determine seed name from ROM. Are you sure this ROM matches this client version?")
            return False

        client_ctx.command_processor.commands["deathlink"] = cmd_deathlink
        # client_ctx.command_processor.commands["kill"] = cmd_kill
        self.death_link = DeathLinkCtx()

        self.dc_pending = False
        return True

    async def set_auth(self, client_ctx: BizHawkClientContext) -> None:
        client_ctx.auth = self.rom_slot_name

    @staticmethod
    def is_state_write_safe(main_game_mode: int, game_mode_sub: int):
        if main_game_mode == ZMConstants.GM_GAMEOVER:
            return True
        if main_game_mode == ZMConstants.GM_INGAME:
            return game_mode_sub == ZMConstants.SUB_GAME_MODE_PLAYING
        return False

    @staticmethod
    def is_state_read_safe(main_game_mode: int, game_mode_sub: int):
        if MZMClient.is_state_write_safe(main_game_mode, game_mode_sub):
            return True
        if main_game_mode in (ZMConstants.GM_CHOZODIA_ESCAPE, ZMConstants.GM_CREDITS):
            return True
        return (main_game_mode, game_mode_sub) == (ZMConstants.GM_INGAME, ZMConstants.SUB_GAME_MODE_DYING)

    async def send_game_state(self, client_ctx: BizHawkClientContext, gameplay_state: Tuple[int, int]):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read8(ZMConstants.gCurrentArea),
                read(ZMConstants.gEventsTriggered, 4 * 3),
                read(ZMConstants.gRandoLocationBitfields, 4 * ZMConstants.AREA_MAX),
            ]))
        except bizhawk.RequestFailedError:
            return

        gMainGameMode = gameplay_state[0]
        gCurrentArea = next_int(read_result)
        gEventsTriggered = struct.unpack(f"<3I", next(read_result))
        gRandoLocationBitfields = struct.unpack(f"<{ZMConstants.AREA_MAX}I", next(read_result))

        checked_locations = set()
        set_events = {flag: False for flag in EVENT_FLAGS}

        if gMainGameMode == ZMConstants.GM_INGAME:
            for location_flags, location_table in zip(
                gRandoLocationBitfields,
                (brinstar_location_table, kraid_location_table, norfair_location_table,
                 ridley_location_table, tourian_location_table, crateria_location_table,
                 chozodia_location_table)
            ):
                for location in location_table.values():
                    if location_flags & 1:
                        checked_locations.add(location.code)
                    location_flags >>= 1

        for event in EVENT_FLAGS:
            block = gEventsTriggered[event.block_number()]
            if block & event.bit_mask():
                set_events[event] = True

        if self.local_checked_locations != checked_locations:
            self.local_checked_locations = checked_locations
            await client_ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(checked_locations)
            }])

        if ((set_events[Event.ESCAPED_CHOZODIA] or gMainGameMode in (ZMConstants.GM_CHOZODIA_ESCAPE, ZMConstants.GM_CREDITS))
            and not client_ctx.finished_game):
            await client_ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

        if self.local_set_events != set_events and client_ctx.slot is not None:
            self.local_set_events = set_events
            event_bitfield = 0
            for i, flag in enumerate(EVENT_FLAGS):
                if set_events[flag]:
                    event_bitfield |= 1 << i
            await client_ctx.send_msgs([{
                "cmd": "Set",
                "key": f"mzm_events_{client_ctx.team}_{client_ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "or", "value": event_bitfield}]
            }])

        if self.local_area != gCurrentArea and client_ctx.slot is not None:
            self.local_area = gCurrentArea
            await client_ctx.send_msgs([{
                "cmd": "Set",
                "key": f"mzm_area_{client_ctx.team}_{client_ctx.slot}",
                "default": 0,
                "want_reply": False,
                "operations": [{"operation": "replace", "value": gCurrentArea}]
            }])

    def received_items(self, client_ctx: BizHawkClientContext) -> Iterable[NetworkItem]:
        """Iterate over the player's received items, skipping local ones if items aren't remote."""

        for item in client_ctx.items_received:
            if (item.player == client_ctx.slot and item.location > 0 and
                item.location not in self.local_checked_locations and not client_ctx.slot_data.get("remote_items")):
                continue
            yield item

    def count_received_item(self, client_ctx: BizHawkClientContext, item_data: ItemData) -> tuple[int, NetworkItem | None]:
        """Get the number of times an item has been received as well as the most recent copy received."""

        count: int = 0
        last: NetworkItem | None = None
        for item in self.received_items(client_ctx):
            if item.item == item_data.code:
                count += 1
                last = item
        return count, last

    @staticmethod
    def make_received_message(client_ctx: BizHawkClientContext, item_name: str, item: NetworkItem) -> Message:
        player_name = client_ctx.player_names[item.player]
        return make_item_message(item_name, f"received from {player_name}")

    async def send_message_and_item(self, client_ctx: BizHawkClientContext,
                                item_data: ZMItemData, message: Message | None, single_line: bool):
        try:
            write_list = [write(
                get_symbol("gIncomingItem"),
                struct.pack("<BBH", item_data.type, message is not None, item_data.bits)
            )]
            if message is not None:
                write_list.append(write(get_symbol("gDynamicMessageBuffer"), message.to_bytes()))
                write_list.append(write(
                    get_symbol("gIncomingMessage"),
                    struct.pack("<IHBB", get_symbol("gDynamicMessageBuffer"), item_data.sound, item_data.acquisition,
                                single_line)
                ))
            await bizhawk.guarded_write(client_ctx.bizhawk_ctx, write_list, [
                guard16(ZMConstants.gMainGameMode, ZMConstants.GM_INGAME),
                guard16(ZMConstants.gGameModeSub1, ZMConstants.SUB_GAME_MODE_PLAYING),
                guard32(get_symbol("gIncomingMessage"), 0),  # Null text data pointer
            ])
        except bizhawk.RequestFailedError:
            return

    async def handle_received_items(self, client_ctx: BizHawkClientContext, gameplay_state: Tuple[int, int]):
        bizhawk_ctx = client_ctx.bizhawk_ctx

        if gameplay_state != (ZMConstants.GM_INGAME, ZMConstants.SUB_GAME_MODE_PLAYING):
            return

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read32(ZMConstants.gIncomingMessage),
                read8(ZMConstants.gDifficulty),
                read(ZMConstants.gEquipment, struct.calcsize("<HHBB6xBxB")),
                read(ZMConstants.gRandoEquipment, struct.calcsize("<BB")),
            ]))
        except bizhawk.RequestFailedError:
            return

        gIncomingMessage_data = next_int(read_result)
        if gIncomingMessage_data != 0:
            return

        gDifficulty = next_int(read_result)
        energy, missiles, supers, powerbombs, beams, majors = struct.unpack("<HHBB6xBxB", next(read_result))
        customs, metroid_dna = struct.unpack("<BB", next(read_result))

        # Energy tanks
        item = item_data_table["Energy Tank"]
        current_tanks = (energy - ZMConstants.sStartingHealthAmmo.energy) // ZMConstants.sTankIncreaseAmount[gDifficulty].energy
        network_tanks, most_recent = self.count_received_item(client_ctx, item)
        to_receive = network_tanks - current_tanks
        if to_receive > 0:
            if to_receive == 1:
                message = (self.make_received_message(client_ctx, "Energy Tank", most_recent)
                           if most_recent.player != client_ctx.slot or most_recent.location <= 0
                           else None)
            else:
                message = make_item_message(
                    "Energy Tanks received.",
                    f"Energy capacity increased by {ZMConstants.sTankIncreaseAmount[gDifficulty].energy * to_receive}."
                )
            await self.send_message_and_item(client_ctx, item.game_data._replace(bits=to_receive), message,
                                             to_receive == 1 and most_recent.player == client_ctx.slot)
            return

        # Missiles
        item = item_data_table["Missile Tank"]
        current_tanks = (missiles - ZMConstants.sStartingHealthAmmo.missile) // ZMConstants.sTankIncreaseAmount[gDifficulty].missile
        network_tanks, most_recent = self.count_received_item(client_ctx, item)
        to_receive = network_tanks - current_tanks
        if to_receive > 0:
            if to_receive == 1:
                message = (self.make_received_message(client_ctx, "Missile Tank", most_recent)
                           if most_recent.player != client_ctx.slot or most_recent.location <= 0
                           else None)
            else:
                message = make_item_message(
                    "Missile Tanks received.",
                    f"Missile capacity increased by {ZMConstants.sTankIncreaseAmount[gDifficulty].missile * to_receive}."
                )
            await self.send_message_and_item(client_ctx, item.game_data._replace(bits=to_receive), message,
                                             to_receive == 1 and most_recent.player == client_ctx.slot)
            return

        # Supers
        item = item_data_table["Super Missile Tank"]
        current_tanks = (supers - ZMConstants.sStartingHealthAmmo.super_missile) // ZMConstants.sTankIncreaseAmount[gDifficulty].super_missile
        network_tanks, most_recent = self.count_received_item(client_ctx, item)
        to_receive = network_tanks - current_tanks
        if to_receive > 0:
            if to_receive == 1:
                message = (self.make_received_message(client_ctx, "Super Missile Tank", most_recent)
                           if most_recent.player != client_ctx.slot or most_recent.location <= 0
                           else None)
            else:
                message = make_item_message(
                    "Super Missile Tanks received.",
                    f"Super Missile capacity increased by {ZMConstants.sTankIncreaseAmount[gDifficulty].super_missile * to_receive}."
                )
            await self.send_message_and_item(client_ctx, item.game_data._replace(bits=to_receive), message,
                                             to_receive == 1 and most_recent.player == client_ctx.slot)
            return

        # PBs
        item = item_data_table["Power Bomb Tank"]
        current_tanks = (powerbombs - ZMConstants.sStartingHealthAmmo.power_bomb) // ZMConstants.sTankIncreaseAmount[gDifficulty].power_bomb
        network_tanks, most_recent = self.count_received_item(client_ctx, item)
        to_receive = network_tanks - current_tanks
        if to_receive > 0:
            if to_receive == 1:
                message = (self.make_received_message(client_ctx, "Power Bomb Tank", most_recent)
                           if most_recent.player != client_ctx.slot or most_recent.location <= 0
                           else None)
            else:
                message = make_item_message(
                    "Power Bomb Tanks received.",
                    f"Power Bomb capacity increased by {ZMConstants.sTankIncreaseAmount[gDifficulty].power_bomb * to_receive}."
                )
            await self.send_message_and_item(client_ctx, item.game_data._replace(bits=to_receive), message,
                                             to_receive == 1 and most_recent.player == client_ctx.slot)
            return

        # Metroid DNA
        item = item_data_table["Metroid DNA"]
        current_tanks = metroid_dna
        network_tanks, most_recent = self.count_received_item(client_ctx, item)
        to_receive = network_tanks - current_tanks
        if to_receive > 0:
            if to_receive == 1:
                message = (self.make_received_message(client_ctx, f"Metroid DNA {network_tanks}", most_recent)
                           if most_recent.player != client_ctx.slot or most_recent.location <= 0
                           else None)
            else:
                message = make_item_message(
                    "Metroid DNA received.",
                    f"{to_receive} samples acquired."
                )
            await self.send_message_and_item(client_ctx, item.game_data._replace(bits=to_receive), message,
                                             to_receive == 1 and most_recent.player == client_ctx.slot)
            return

        # Majors
        acquired_majors: dict[int, bool] = {}
        for item in major_item_data_table.values():
            game_data = item.game_data
            if game_data.type == ItemType.BEAM:
                has_item = beams & game_data.bits
            elif game_data.type == ItemType.MAJOR:
                has_item = majors & game_data.bits
            elif game_data.type == ItemType.CUSTOM:
                has_item = customs & game_data.bits
            acquired_majors[item.code] = bool(has_item)
        for item in self.received_items(client_ctx):
            acquired = acquired_majors.get(item.item)
            if acquired is None or acquired:
                continue
            name = client_ctx.item_names.lookup_in_game(item.item)
            game_data = item_data_table[name].game_data
            message = (self.make_received_message(client_ctx, name, item)
                       if item.player != client_ctx.slot or item.location <= 0
                       else None)
            await self.send_message_and_item(client_ctx, game_data, message, item.player == client_ctx.slot)
            break

        # Vanilla Fully Powered Suit
        if (client_ctx.slot_data.get("unknown_items_usable") == FullyPoweredSuit.option_ruins_test
            and self.local_set_events[Event.RUINS_TEST_PASSED]
            and not acquired_majors[item_data_table["Fully Powered Suit"].code]):
            await self.send_message_and_item(client_ctx, item_data_table["Fully Powered Suit"].game_data, None, False)

    async def game_watcher(self, client_ctx: BizHawkClientContext) -> None:
        if self.dc_pending:
            await client_ctx.disconnect()
            return

        if client_ctx.server is None or client_ctx.server.socket.closed or client_ctx.slot_data is None:
            return

        if self.death_link.update_pending:
            await client_ctx.update_death_link(self.death_link.enabled)
            self.death_link.update_pending = False

        bizhawk_ctx = client_ctx.bizhawk_ctx

        if client_ctx.slot_data.get("remote_items"):
            await bizhawk.write(bizhawk_ctx, [write8(get_symbol("gIgnoreLocalItems"), True)])

        try:
            read_result = iter(await bizhawk.read(bizhawk_ctx, [
                read16(ZMConstants.gMainGameMode),
                read16(ZMConstants.gGameModeSub1),
            ]))
        except bizhawk.RequestFailedError:
            return

        gMainGameMode = next_int(read_result)
        gGameModeSub1 = next_int(read_result)

        gameplay_state = (gMainGameMode, gGameModeSub1)

        if not self.is_state_read_safe(gMainGameMode, gGameModeSub1):
            return

        await self.send_game_state(client_ctx, gameplay_state)

        if self.death_link.enabled:
            if (gameplay_state == (ZMConstants.GM_INGAME, ZMConstants.SUB_GAME_MODE_DYING)
                or gMainGameMode == ZMConstants.GM_GAMEOVER):
                self.death_link.pending = False
                if not self.death_link.sent_this_death:
                    self.death_link.sent_this_death = True
                    # TODO: Text for failed Tourian/Chozodia escape
                    await client_ctx.send_death()
            else:
                self.death_link.sent_this_death = False

        if not self.is_state_write_safe(gMainGameMode, gGameModeSub1):
            return

        guard_list = [
            # Ensure game state hasn't changed
            guard16(ZMConstants.gMainGameMode, gMainGameMode),
            guard16(ZMConstants.gGameModeSub1, gGameModeSub1),
        ]

        # Receive death link
        if self.death_link.enabled and self.death_link.pending:
            self.death_link.sent_this_death = True
            try:
                samus_pose = next_int(iter(await bizhawk.read(
                    bizhawk_ctx,
                    [read8(ZMConstants.gSamusData + 0)]  # gSamusData.pose
                )))
                if samus_pose != ZMConstants.SPOSE_SAVING_LOADING_GAME:
                    await bizhawk.guarded_write(
                        bizhawk_ctx,
                        [write16(ZMConstants.gEquipment + 6, 0)],  # gEquipment.currentEnergy
                        guard_list + [guard8(ZMConstants.gSamusData + 0, samus_pose)]  # gSamusData.pose
                    )
            except bizhawk.RequestFailedError:
                return

        await self.handle_received_items(client_ctx, gameplay_state)

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict) -> None:
        if cmd == "Connected":
            if args["slot_data"].get("death_link"):
                self.death_link.enabled = True
                self.death_link.update_pending = True
        if cmd == "RoomInfo":
            if ctx.seed_name and ctx.seed_name != args["seed_name"]:
                # CommonClient's on_package displays an error to the user in this case, but connection is not cancelled.
                self.dc_pending = True
        if cmd == "Bounced":
            tags = args.get("tags", [])
            if "DeathLink" in tags:
                self.death_link.pending = True
