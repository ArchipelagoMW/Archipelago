from typing import (
    TYPE_CHECKING,
    Set,
    Callable,
    TypeVar,
    Awaitable,
    Any,
)
from enum import IntEnum
import struct

from NetUtils import ClientStatus

from .options import Goal
from .connector_config import (
    locations as locations_raw,
    EXPECTED_ROM_NAME,
    FLAGS_ADDR,
    ARCHIPELAGO_RECEIVED_ITEM_ADDR,
    ARCHIPELAGO_NUM_RECEIVED_ITEMS_ADDR,
    ARCHIPELAGO_DEATHLINK_IN,
    ARCHIPELAGO_DEATHLINK_OUT,
    ARCHIPELAGO_DEATHLINK_READY,
    DEATH_LINK_KIND_OFFS,
    SLOT_NAME_ADDR,
)
from .constants import (
    FE8_NAME,
    FE8_ID_PREFIX,
    ROM_BASE_ADDRESS,
    ROM_NAME_ADDR,
    PROC_SIZE,
    PROC_POOL_ADDR,
    TOTAL_NUM_PROCS,
    # TODO: world map item receiving
    # WM_PROC_ADDRESS,
    E_PLAYERPHASE_PROC_ADDRESS,
)

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

locations = dict(locations_raw)

FOMORTIIS_FLAG = locations["Defeat Formortiis"]
TIRADO_FLAG = locations["Complete Chapter 8"]
TOWER_CLEAR_FLAG = locations["Complete Tower of Valni 8"]
RUINS_CLEAR_FLAG = locations["Complete Lagdou Ruins 10"]

T = TypeVar("T")


DEATH_LINK_MSGS = [
    "{} sent a Death Link!",
    "{}'s army was defeated!",
    "{} suffered a casualty!",
]


class DeathLinkKind(IntEnum):
    _ignore_ = ["_msgs"]

    NONE = 0
    ON_GAME_OVER = 1
    ON_ANY_DEATH = 2

    def message(self):
        return DEATH_LINK_MSGS[self]


class FE8Client(BizHawkClient):
    game = FE8_NAME
    system = "GBA"
    patch_suffix = ".apfe8"
    local_checked_locations: Set[int]
    game_state_safe = False
    deathlink_kind: DeathLinkKind
    pending_deathlink = False
    pending_deathlink_deaths = 0
    goal_flag: int

    def __init__(self):
        super().__init__()
        self.local_checked_locations = set()
        self.goal_flag = FOMORTIIS_FLAG

    async def validate_rom(self, ctx: BizHawkClientContext) -> bool:
        from CommonClient import logger

        try:
            # logger.info("FE8 Client: validating")
            rom_name_bytes, deathlink_kind_bytes = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (ROM_NAME_ADDR, 16, "System Bus"),
                    (DEATH_LINK_KIND_OFFS + ROM_BASE_ADDRESS, 1, "System Bus"),
                ],
            )
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode(
                "ascii"
            )
            # logger.info("FE8 Client: rom name is {rom_name}")
            if rom_name == "FIREEMBLEM2EBE8E":
                logger.error(
                    "ERROR: You seem to be running an unpatched version of FE8. "
                    "Please generate a patch file and use it to create a patched ROM."
                )
                return False
            if not rom_name.startswith("FE8AP"):
                return False
            if rom_name != EXPECTED_ROM_NAME:
                logger.error(
                    "ERROR: The patch file used to create this ROM is not compatible "
                    "with this client. Double check your client version against the "
                    "version used by the generator."
                )
                return False
        except UnicodeDecodeError:
            # logger.error("FE8 Client: unicode error")
            return False
        except bizhawk.RequestFailedError:
            # logger.error("FE8 Client: bizhawk request failed")
            return False

        ctx.game = self.game
        ctx.items_handling = 1
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.deathlink_kind = DeathLinkKind(deathlink_kind_bytes[0])
        await ctx.update_death_link(bool(self.deathlink_kind))

        return True

    async def run_locked(
        self,
        ctx: BizHawkClientContext,
        f: Callable[[BizHawkClientContext], Awaitable[T]],
    ) -> T:
        await bizhawk.lock(ctx.bizhawk_ctx)
        result = await f(ctx)
        await bizhawk.unlock(ctx.bizhawk_ctx)
        return result

    async def update_game_state(self, ctx: BizHawkClientContext) -> None:
        active_procs = [
            int.from_bytes(i, byteorder="little")
            for i in await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (PROC_POOL_ADDR + i * PROC_SIZE, 4, "System Bus")
                    for i in range(TOTAL_NUM_PROCS)
                ],
            )
        ]

        if any(proc in (E_PLAYERPHASE_PROC_ADDRESS,) for proc in active_procs):
            self.game_state_safe = True
        else:
            self.game_state_safe = False

    def on_package(self, ctx: BizHawkClientContext, cmd: str, args: dict[str, Any]):
        if cmd == "Bounced":
            if "tags" in args:
                if ctx.slot is None:
                    return
                # This will, in theory, cause us to receive our own deathlinks.
                # However, because the game itself will be in the middle of a
                # GameOver, it won't be able to receive it anyway.
                if "DeathLink" in args["tags"] and self.deathlink_kind:
                    self.pending_deathlink = True


    async def handle_pending_deathlink(self, ctx: BizHawkClientContext):
        self.pending_deathlink = False
        if not self.deathlink_kind:
            return
        await self.run_locked(ctx, self.run_deathlink)

    # requires: locked
    async def run_deathlink(self, ctx: BizHawkClientContext):
        ready = (
            await bizhawk.read(
                ctx.bizhawk_ctx, [(ARCHIPELAGO_DEATHLINK_READY, 1, "System Bus")]
            )
        )[0][0]
        if not ready:
            return
        await bizhawk.write(
            ctx.bizhawk_ctx, [(ARCHIPELAGO_DEATHLINK_IN, bytes([1]), "System Bus")]
        )
        self.pending_deathlink_deaths += 1

    async def set_auth(self, ctx: BizHawkClientContext) -> None:
        slot_name_bytes = (
            await bizhawk.read(ctx.bizhawk_ctx, [(SLOT_NAME_ADDR, 64, "System Bus")])
        )[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode(
            "utf-8"
        )

    # requires: locked and game_state_safe
    async def maybe_write_next_item(self, ctx: BizHawkClientContext) -> None:
        # from CommonClient import logger

        is_filled_byte, num_items_received_bytes = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (ARCHIPELAGO_RECEIVED_ITEM_ADDR + 2, 1, "System Bus"),
                (ARCHIPELAGO_NUM_RECEIVED_ITEMS_ADDR, 4, "System Bus"),
            ],
        )

        is_filled = is_filled_byte[0]

        num_items_received = max(
            int.from_bytes(num_items_received_bytes, byteorder="little"), 0
        )

        if is_filled:
            return

        if num_items_received < len(ctx.items_received):
            next_item = ctx.items_received[num_items_received]
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [
                    (
                        ARCHIPELAGO_RECEIVED_ITEM_ADDR + 0,
                        (next_item.item - FE8_ID_PREFIX).to_bytes(2, "little"),
                        "System Bus",
                    ),
                    (
                        ARCHIPELAGO_RECEIVED_ITEM_ADDR + 2,
                        b"\x01",
                        "System Bus",
                    ),
                ],
            )

    async def game_watcher(self, ctx: BizHawkClientContext) -> None:
        if ctx.slot_data is not None:
            match ctx.slot_data["goal"]:
                case Goal.option_DefeatFormortiis:
                    self.goal_flag = FOMORTIIS_FLAG
                case Goal.option_ClearValni:
                    self.goal_flag = TOWER_CLEAR_FLAG
                case Goal.option_DefeatTirado:
                    self.goal_flag = TIRADO_FLAG
                case Goal.option_ClearLagdou:
                    self.goal_flag = RUINS_CLEAR_FLAG

        try:
            await self.update_game_state(ctx)

            if self.game_state_safe:
                await self.run_locked(ctx, self.maybe_write_next_item)

            flag_bytes, deathlink_out_bytes = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (FLAGS_ADDR, 8, "System Bus"),
                    (ARCHIPELAGO_DEATHLINK_OUT, 1, "System Bus"),
                ],
            )
            local_checked_locations = set()
            game_clear = False

            if self.pending_deathlink:
                await self.handle_pending_deathlink(ctx)

            (deathlink_out,) = struct.unpack("<1b", deathlink_out_bytes)
            if deathlink_out > 0:
                deathlink_out -= 1
                if self.pending_deathlink_deaths:
                    self.pending_deathlink_deaths -= 1
                else:
                    name = (
                        ctx.player_names[ctx.slot]
                        if ctx.slot is not None
                        else "<Unknown Player>"
                    )
                    await ctx.send_death(self.deathlink_kind.message().format(name))
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (
                            ARCHIPELAGO_DEATHLINK_OUT,
                            bytes([max(deathlink_out, 0)]),
                            "System Bus",
                        )
                    ],
                )

            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    if byte & (1 << i) != 0:
                        flag_id = byte_i * 8 + i
                        location_id = flag_id + FE8_ID_PREFIX

                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

                        if flag_id == self.goal_flag:
                            game_clear = True

            if local_checked_locations != self.local_checked_locations:
                self.local_checked_locations = local_checked_locations

                if local_checked_locations is not None:
                    await ctx.send_msgs(
                        [
                            {
                                "cmd": "LocationChecks",
                                "locations": list(local_checked_locations),
                            }
                        ]
                    )

            if not ctx.finished_game and game_clear:
                await ctx.send_msgs(
                    [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
                )
        except bizhawk.RequestFailedError:
            pass
