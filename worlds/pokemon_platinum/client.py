# client.py
#
# Copyright (C) 2025-2026 James Petersen <m@jamespetersen.ca>
# Licensed under MIT. See LICENSE

from collections.abc import Mapping, Set
from dataclasses import dataclass
from NetUtils import ClientStatus
from struct import unpack_from
from typing import TYPE_CHECKING, Tuple

import Utils

from .data.locations import FlagCheck, LocationCheck, locations, VarCheck, OnceCheck, maximal_required_locations
from .data.event_checks import event_checks
from .locations import raw_id_to_const_name
from .options import Goal, RemoteItems

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

AP_STRUCT_PTR_ADDRESS = 0x023DFFFC
AP_SUPPORTED_VERSIONS = {0}
AP_MAGIC = b' AP '
TRACKED_EVENTS = [
    "fen_badge",
    "met_oak_pal_park",
    "lake_verity_defeat_mars",
    "lake_explosion",
    "forest_badge",
    "cobble_badge",
    "galactic_hq_defeat_cyrus",
    "lake_valor_defeat_saturn",
    "lake_acuity_meet_jupiter",
    "icicle_badge",
    "eterna_defeat_team_galactic",
    "relic_badge",
    "coal_badge",
    "beacon_badge",
    "mine_badge",
    "beat_cynthia",
    "distortion_world",
    "valley_windworks_defeat_team_galactic",
]
TRACKED_UNRANDOMIZED_REQUIRED_LOCATIONS = sorted(maximal_required_locations)

@dataclass(frozen=True)
class VersionData:
    savedata_ptr_offset: int
    recv_item_id_offset: int
    vars_flags_offset_in_save: int
    vars_offset_in_vars_flags: int
    vars_flags_size: int
    flags_offset_in_vars_flags: int
    ap_save_offset: int
    recv_item_count_offset_in_ap_save: int
    once_loc_flags_offset_in_ap_save: int
    once_loc_flags_count: int
    player_pos_offset: int

AP_VERSION_DATA: Mapping[int, VersionData] = {
    0: VersionData(
        savedata_ptr_offset=16,
        recv_item_id_offset=20,
        vars_flags_offset_in_save=0xDC0,
        vars_offset_in_vars_flags=0,
        vars_flags_size=0x3E0,
        flags_offset_in_vars_flags=0x240,
        ap_save_offset=0xCF60,
        recv_item_count_offset_in_ap_save=0,
        once_loc_flags_offset_in_ap_save=10,
        once_loc_flags_count=16,
        player_pos_offset=24,
    ),
}

@dataclass(frozen=True)
class VarsFlags:
    flags: bytes
    vars: bytes
    once_loc_flags: bytes

    def is_checked(self, check: LocationCheck) -> bool:
        if isinstance(check, FlagCheck):
            return self.get_flag(check.id) ^ check.invert
        elif isinstance(check, VarCheck):
            var = self.get_var(check.id)
            if var is not None:
                return check.op(var, check.value)
            else:
                return False
        elif isinstance(check, OnceCheck):
            return self.get_once_flag(check.id) ^ check.invert
        else:
            return False

    def get_once_flag(self, flag_id: int) -> bool:
        if flag_id // 8 < len(self.once_loc_flags):
            return self.once_loc_flags[flag_id // 8] & (1 << (flag_id & 7)) != 0
        else:
            return False

    def get_flag(self, flag_id: int) -> bool:
        if flag_id > 0 and flag_id // 8 < len(self.flags):
            return self.flags[flag_id // 8] & (1 << (flag_id & 7)) != 0
        else:
            return False

    def get_var(self, var_id: int) -> int | None:
        if var_id - 0x4000 < len(self.vars) // 2:
            var_id -= 0x4000
            return int.from_bytes(self.vars[2 * var_id:2 * (var_id + 1)], byteorder='little')

class PokemonPlatinumClient(BizHawkClient):
    game = "Pokemon Platinum"
    system = "NDS"
    patch_suffix = ".applatinum"
    ap_struct_address: int = 0
    rom_version: int = 0
    goal_flag: LocationCheck | None
    local_checked_locations: Set[int]
    expected_header: bytes
    current_map: int
    current_x: int
    current_z: int
    local_tracked_events: int
    local_tracked_unrandomized_prog_locs: int

    def initialize_client(self):
        self.goal_flag = None
        self.local_checked_locations = set()
        self.expected_header = AP_MAGIC * 3 + self.rom_version.to_bytes(length=4, byteorder='little')
        self.current_map = 0
        self.current_x = -1
        self.current_z = -1
        self.local_tracked_events = 0
        self.local_tracked_unrandomized_prog_locs = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0, 12, "ROM")]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name == "POKEMON PL":
                logger.info("ERROR: You appear to be running an unpatched version of Pokémon Platinum. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            elif rom_name.startswith("PLAP "):
                bad = True
                try:
                    version = int(rom_name[5:].strip(), 16)
                    if version in AP_SUPPORTED_VERSIONS:
                        self.rom_version = version
                        bad = False
                except ValueError:
                    pass
                if bad:
                    logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                                "this client. Double-check your client version against the version being "
                                "by the generator.")
                    return False
            else:
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001
        self.want_slot_data = True
        self.watcher_timeout = 0.125

        self.initialize_client()

        return True

    async def get_struct_addr(self, ctx: "BizHawkClientContext") -> None:
        try:
            addr = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(AP_STRUCT_PTR_ADDRESS, 4, "ARM9 System Bus")]))[0], byteorder='little')
            if 0x2000000 < addr and addr < AP_STRUCT_PTR_ADDRESS:
                header = (await bizhawk.read(ctx.bizhawk_ctx, [(addr, 16, "ARM9 System Bus")]))[0]
                if header == self.expected_header:
                    self.ap_struct_address = addr
                    print(f"found ap struct at addr {addr:X}")
        except bizhawk.RequestFailedError:
            pass

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        version_data = AP_VERSION_DATA[self.rom_version]

        if self.ap_struct_address == 0:
            await self.get_struct_addr(ctx)
            return

        if ctx.slot_data["goal"] == Goal.option_champion:
            self.goal_flag = event_checks["beat_cynthia"]

        if ctx.slot_data["remote_items"] == RemoteItems.option_true and not ctx.items_handling & 0b010: # type: ignore
            ctx.items_handling = 0b011
            Utils.async_start(ctx.send_msgs([{
                "cmd": "ConnectUpdate",
                "items_handling": ctx.items_handling
            }]))

        try:
            ap_struct_guard = (self.ap_struct_address, self.expected_header, "ARM9 System Bus")
            guards: Mapping[str, Tuple[int, bytes, str]] = {}
            guards["AP STRUCT VALID"] = ap_struct_guard

            actual_header = (await bizhawk.read(ctx.bizhawk_ctx, [(ap_struct_guard[0], 16, "ARM9 System Bus")]))[0]
            if actual_header != self.expected_header:
                self.ap_struct_address = 0
                return

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [
                    (self.ap_struct_address + version_data.savedata_ptr_offset, 4, "ARM9 System Bus"),
                ],
                [guards["AP STRUCT VALID"]]
            )

            if read_result is None:
                return

            guards["SAVEDATA PTR"] = (self.ap_struct_address + version_data.savedata_ptr_offset, read_result[0], "ARM9 System Bus")

            savedata_ptr = int.from_bytes(guards["SAVEDATA PTR"][1], byteorder='little')

            guards["READY TO RECV"] = (self.ap_struct_address + version_data.recv_item_id_offset, b'\xFF\xFF', "ARM9 System Bus")
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [
                    (savedata_ptr + version_data.ap_save_offset + version_data.recv_item_count_offset_in_ap_save, 4, "ARM9 System Bus"),
                    (self.ap_struct_address + version_data.recv_item_id_offset, 2, "ARM9 System Bus"),
                ],
                [guards["AP STRUCT VALID"], guards["SAVEDATA PTR"]]
            )

            if read_result is None:
                return

            recv_item_count = int.from_bytes(read_result[0], byteorder='little')
            recv_item_id = int.from_bytes(read_result[1], byteorder='little')
            if recv_item_id == 0xFFFF and recv_item_count < len(ctx.items_received):
                next_item = ctx.items_received[recv_item_count].item
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [
                        (self.ap_struct_address + version_data.recv_item_id_offset, next_item.to_bytes(length=2, byteorder='little'), "ARM9 System Bus"),
                    ]
                )

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [
                    (savedata_ptr + version_data.vars_flags_offset_in_save, version_data.vars_flags_size, "ARM9 System Bus"),
                    (savedata_ptr + version_data.ap_save_offset + version_data.once_loc_flags_offset_in_ap_save, version_data.once_loc_flags_count // 8, "ARM9 System Bus"),
                ],
                [guards["AP STRUCT VALID"], guards["SAVEDATA PTR"]],
            )
            if read_result is None:
                return
            vars_flags_bytes = read_result[0]
            vars_bytes = vars_flags_bytes[version_data.vars_offset_in_vars_flags:version_data.flags_offset_in_vars_flags]
            flags_bytes = vars_flags_bytes[version_data.flags_offset_in_vars_flags:]

            vars_flags = VarsFlags(flags=flags_bytes, vars=vars_bytes, once_loc_flags=read_result[1])

            local_checked_locations = set()
            game_clear = vars_flags.is_checked(self.goal_flag) # type: ignore
            local_tracked_events = 0
            local_tracked_unrandomized_prog_locs = 0

            for k, loc in map(lambda k : (k, locations[raw_id_to_const_name[k]]), ctx.missing_locations):
                if vars_flags.is_checked(loc.check):
                    local_checked_locations.add(k)

            for k, event in enumerate(TRACKED_EVENTS):
                if vars_flags.is_checked(event_checks[event]):
                    local_tracked_events |= 1 << k

            for k, loc in enumerate(TRACKED_UNRANDOMIZED_REQUIRED_LOCATIONS):
                if vars_flags.is_checked(locations[loc].check):
                    local_tracked_unrandomized_prog_locs |= 1 << k

            if local_checked_locations != self.local_checked_locations:
                await ctx.check_locations(local_checked_locations)

                self.local_checked_locations = local_checked_locations

            if local_tracked_events != self.local_tracked_events:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_platinum_tracked_events_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": local_tracked_events}],
                }])
                self.local_tracked_events = local_tracked_events

            if local_tracked_unrandomized_prog_locs != self.local_tracked_unrandomized_prog_locs:
                for chunk in range((len(TRACKED_UNRANDOMIZED_REQUIRED_LOCATIONS) + 31) >> 5):
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"pokemon_platinum_tracked_unrandomized_required_locations_{ctx.team}_{ctx.slot}_{chunk}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "or", "value": (local_tracked_unrandomized_prog_locs >> (chunk * 32)) & 0xFFFFFFFF}],
                    }])
                self.local_tracked_unrandomized_prog_locs = local_tracked_unrandomized_prog_locs

            if not ctx.finished_game and game_clear:
                ctx.finished_game = True
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL,
                }])

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [
                    (self.ap_struct_address + version_data.player_pos_offset, 12, "ARM9 System Bus"),
                ],
                [guards["AP STRUCT VALID"]]
            )
            if read_result is None:
                return

            current_x, current_z, current_map, pos_lock = unpack_from("<2IHB", read_result[0])
            if pos_lock == 0 and (current_map != self.current_map or current_x != self.current_x or current_z != self.current_z):
                self.current_map = current_map
                self.current_x = current_x
                self.current_z = current_z
                message = [{"cmd": "Bounce", "slots": [ctx.slot],
                           "data": {
                               "mapNumber": current_map,
                               "matrixX": current_x,
                               "matrixZ": current_z,
                           }}]
                await ctx.send_msgs(message)

        except bizhawk.RequestFailedError:
            pass
