import logging
import math
from typing import TYPE_CHECKING, Any, Coroutine, Callable

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from .client.locations import check_flag_locations, check_dex_locations
from .client.items import receive_items
from .client.setup import early_setup, late_setup
from .client.tracker import set_map, set_dex_caught_seen, set_goal_bitmap

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


def register_client():
    """This is just a placeholder function to remind new (and old) world devs to import the client file"""
    pass


class PokemonBWClient(BizHawkClient):
    game = "Pokemon Black and White"
    system = "NDS"
    patch_suffix = (".apblack", ".apwhite")

    ram_read_write_domain = "Main RAM"
    rom_read_only_domain = "ROM"  # Only works on BizHawk 2.10+
    flags_amount = 2912
    flag_bytes_amount = math.ceil(flags_amount/8)
    dex_amount = 650
    dex_bytes_amount = math.ceil(dex_amount/8)
    main_items_bag_size = 1240//4  # 310
    key_items_bag_size = 332//4  # 83
    tm_hm_bag_size = 436//4  # 109
    medicine_bag_size = 192//4  # 48
    berry_bag_size = 256//4  # 64

    data_address_address = 0x000024  # says 0x21B310 in vanilla W
    ingame_state_address = 0x000034
    header_address = 0x3ffa80
    var_offset = 0x209BC  # 0x23BCCC in vanilla W
    flags_offset = 0x20C38  # 0x23BF48 in vanilla W
    dex_offset = 0x21EC4  # 0x23D1D4 in vanilla W
    dex_seen_offset = dex_offset + 0x54
    main_items_bag_offset = 0x18cbc  # 0x233FCC in vanilla W
    key_items_bag_offset = 0x19194  # 0x2344A4 in vanilla W
    tm_hm_bag_offset = 0x192e0  # 0x2345F0 in vanilla W
    medicine_bag_offset = 0x19494  # 0x2347A4 in vanilla W
    berry_bag_offset = 0x19554  # 0x234864 in vanilla W
    badges_offset = 0x21ac0  # 0x23CDD0 in vanilla W
    map_id_offset = 0x3461c  # 0x24f92c in vanilla W

    def __init__(self):
        super().__init__()
        self.flags_cache: bytearray = bytearray(self.flag_bytes_amount)
        self.dex_cache: bytearray = bytearray(self.dex_bytes_amount)
        self.tracker_caught_cache: bytearray = bytearray(self.dex_bytes_amount)
        self.tracker_seen_cache: bytearray = bytearray(self.dex_bytes_amount)
        self.goal_bitmap: int = 0
        self.dexsanity_included: bool = True
        self.player_name: str | None = None
        self.missing_flag_loc_ids: list[list[int]] = [[] for _ in range(self.flags_amount)]
        self.missing_dex_flag_loc_ids: list[list[int]] = [[] for _ in range(self.dex_amount)]
        self.save_data_address = 0
        self.current_map = -1
        self.game_version = -1  # 0 for black, 1 for white
        self.goal_checking_method: Callable[["PokemonBWClient", "BizHawkClientContext"],
                                            Coroutine[Any, Any, bool]] | None = None
        self.logger = logging.getLogger("Client")
        self.debug_halt = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        """Should return whether the currently loaded ROM should be handled by this client. You might read the game name
        from the ROM header, for example. This function will only be asked to validate ROMs from the system set by the
        client class, so you do not need to check the system yourself.

        Once this function has determined that the ROM should be handled by this client, it should also modify `ctx`
        as necessary (such as setting `ctx.game = self.game`, modifying `ctx.items_handling`, etc...)."""

        header = await bizhawk.read(
            ctx.bizhawk_ctx, (
                (self.header_address, 0xc0, self.ram_read_write_domain),
            )
        )
        if header[0][:18] not in (b'POKEMON B\0\0\0IRBO01', b'POKEMON W\0\0\0IRAO01'):
            return False

        self.player_name = header[0][0xa0:].strip(b'\0').decode()
        if header[0][8] == b'B'[0]:
            self.game_version = 0
        else:
            self.game_version = 1
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 1
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        """Should set ctx.auth in anticipation of sending a `Connected` packet. You may override this if you store slot
        name in your patched ROM. If ctx.auth is not set after calling, the player will be prompted to enter their
        username."""

        if self.player_name is not None:
            ctx.auth = self.player_name

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        """For handling packages from the server. Called from `BizHawkClientContext.on_package`."""

        if cmd == 'Connected':
            from .data.locations import all_item_locations, dexsanity
            for loc_id in ctx.missing_locations:
                loc_name = ctx.location_names.lookup_in_game(loc_id)
                if loc_name in all_item_locations:
                    self.missing_flag_loc_ids[all_item_locations[loc_name].flag_id].append(loc_id)
                elif loc_name in dexsanity.location_table:
                    self.missing_dex_flag_loc_ids[dexsanity.location_table[loc_name].dex_number].append(loc_id)
                else:
                    self.logger.warning(f"Missing location \"{loc_name}\" neither flag nor dex location")
        elif cmd == "RoomInfo":
            ctx.seed_name = args["seed_name"]

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        """Runs on a loop with the approximate interval `ctx.watcher_timeout`. The currently loaded ROM is guaranteed
        to have passed your validator when this function is called, and the emulator is very likely to be connected."""

        try:
            if (
                not ctx.server or
                not ctx.server.socket.open or
                ctx.server.socket.closed or
                ctx.slot_data is None or
                self.debug_halt
            ):
                return
            read = await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (self.ingame_state_address, 1, self.ram_read_write_domain),
                )
            )
            if read[0][0] == 0:
                return
            setup_needed = False
            if self.save_data_address == 0:
                await early_setup(self, ctx)
                setup_needed = True

            locations_to_check: list[int] = (
                await check_flag_locations(self, ctx) +
                await check_dex_locations(self, ctx)
            )
            if len(locations_to_check) != 0:
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locations_to_check)}])

            await set_map(self, ctx)
            await set_dex_caught_seen(self, ctx)
            await set_goal_bitmap(self, ctx)

            await receive_items(self, ctx)

            if self.flags_cache[0x190//8] & 1 != 0:
                self.logger.warning("An error occurred while receiving an item ingame. "
                                    "Please report this and what you just received to the devs.")

            if await self.goal_checking_method(self, ctx):
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

            if setup_needed:
                await late_setup(self, ctx)

        except bizhawk.RequestFailedError:
            pass

        except bizhawk.ConnectorError:
            pass

    def get_flag(self, flag: int) -> bool:
        return (self.flags_cache[flag//8] & (2 ** (flag % 8))) != 0

    async def write_set_flag(self, ctx: "BizHawkClientContext", flag: int) -> None:
        while not await bizhawk.guarded_write(
            ctx.bizhawk_ctx, ((
                self.save_data_address + self.flags_offset + (flag//8),
                [self.flags_cache[flag//8] | (2 ** (flag % 8))],
                self.ram_read_write_domain
            ),), ((
                self.save_data_address + self.flags_offset + (flag//8),
                [self.flags_cache[flag//8]],
                self.ram_read_write_domain
            ),)
        ):
            self.flags_cache[flag//8] = (await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (self.save_data_address + self.flags_offset + (flag//8), 1, self.ram_read_write_domain),
                )
            ))[0][0]
        self.flags_cache[flag // 8] |= (2 ** (flag % 8))

    async def write_unset_flag(self, ctx: "BizHawkClientContext", flag: int) -> None:
        while not await bizhawk.guarded_write(
            ctx.bizhawk_ctx, ((
                self.save_data_address + self.flags_offset + (flag//8),
                [self.flags_cache[flag//8] & (255 - (2 ** (flag % 8)))],
                self.ram_read_write_domain
            ),), ((
                self.save_data_address + self.flags_offset + (flag//8),
                [self.flags_cache[flag//8]],
                self.ram_read_write_domain
            ),)
        ):
            self.flags_cache[flag//8] = (await bizhawk.read(
                ctx.bizhawk_ctx, (
                    (self.save_data_address + self.flags_offset + (flag//8), 1, self.ram_read_write_domain),
                )
            ))[0][0]
        self.flags_cache[flag // 8] &= (255 - (2 ** (flag % 8)))

    async def write_var(self, ctx: "BizHawkClientContext", var: int, value: int, length=2) -> None:
        await bizhawk.write(
            ctx.bizhawk_ctx, ((
                self.save_data_address + self.var_offset + (2 * var),
                value.to_bytes(length, "little"),
                self.ram_read_write_domain
            ),)
        )

    async def read_var(self, ctx: "BizHawkClientContext", var: int, length=2) -> int:
        return int.from_bytes((await bizhawk.read(
            ctx.bizhawk_ctx, (
                (self.save_data_address + self.var_offset + (2 * var), length, self.ram_read_write_domain),
            )
        ))[0], "little")
