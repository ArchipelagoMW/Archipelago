import logging, os
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from typing import TYPE_CHECKING
from enum import Flag
from NetUtils import ClientStatus, NetworkItem
from collections import namedtuple
from Utils import messagebox, user_path
from pathlib import Path

from .Locations import ZoneData, enemy_locations, drop_locations, location_table, LocationData, zones_dict, get_location_data
from .Items import base_item_id, ItemData, item_table, IType
from .Traps import restore_ram, TrapData, apply_trap, trap_id_to_name

# TODO:
#  Sometimes RNO1 vase near Creature is missing. Research
#  Visual glitches on Richter dialog
#  Visual glitch on sliding door after defeating Lesser Demon
#  Exploration 10 and power of wolf share location_id
#  After killing Scylla taking 1 fall damage trigger death

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

logger = logging.getLogger("Client")

item_id_to_name = {value.index - base_item_id: key for key, value in item_table.items()}
loc_name_to_id = {k: v.location_id for k, v in location_table.items()}
loc_id_to_name = {value.location_id: key for key, value in location_table.items()}
Seed = namedtuple("Seed", ["file_name", "sanity", "goal", "bosses", "exp", "talisman", "total_tal"])


class STATUS(Flag):
    START = 1
    TITLE_SCREEN = 2
    RICHTER = 4
    ALUCARD = 8
    DIED = 16
    DEAD = 32


class SotNClient(BizHawkClient):
    game = "Symphony of the Night"
    system = "PSX"
    patch_suffix = ".apsotn"

    def __init__(self) -> None:
        super().__init__()
        self.checked_locations = []
        self.sent_checked_locations = []
        self.player_status = STATUS.START
        self.last_player_status = STATUS.START
        self.patched = False
        self.cur_zone = ("UNK", "UNKNOWN")
        self.last_zone = ("UNK", "UNKNOWN")
        self.load_once = False
        self.last_item_received = 0
        self.last_misplaced = 0
        self.last_trap_processed = 0
        self.out_world_traps = 0
        self.dracula_dead = False
        self.dracula_door = False
        self.options = Seed("", 0, 0, 0, 0, 0, 0)
        self.misplaced_queue = []
        self.misplaced_load = []
        self.misplaced_changed = False
        self.traps = []
        self.ice_paused = []
        self.paused_trap = False
        self.paused_richter = False
        self.last_received_trap = 1
        self.hp_backup = 0
        self.equip_backup = b'\x00'
        self.hand_backup = b'\x00'
        self.shield_backup = b'\x00'
        self.already_active_trap = []
        self.new_items = []
        self.received_relics = []
        self.last_owned_relics = []
        self.message_queue = []
        self.received_queue = []
        self.goal_diplayed = False
        self.applied_axe = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            # @ ROM 0x00009340
            # 53 4C 55 53 5F 30 30 30 2E 36 37
            # SLUS_00067
            # Does not show on BIOS loading
            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(0x009334, 11, "MainRAM")],
                [(0x009334, b'\x53\x4c\x55\x53\x5f\x30\x30\x30\x2e\x36\x37', "MainRAM")])

            if read_result is not None:
                # This is a MYGAME ROM / Did finish loaded?
                read_result2 = await bizhawk.read(ctx.bizhawk_ctx,[(0x0dfaec, 12, "MainRAM")])

                if read_result2[0] != b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                    # First Maria Meeting
                    # 26 49 52 53 54 00 2d 41 52 49 47 00
                    # b'\x26\x49\x52\x53\x54\x00\x2d\x41\x52\x49\x47\x00'
                    if read_result2[0] == b'&IRST\x00-ARIA\x00':
                        # Vanilla ROM
                        messagebox("Error", "Looks like a vanilla ROM is loaded!", error=True)
                        return False
                    else:
                        ctx.game = self.game
                        ctx.items_handling = 0b101
                        ctx.want_slot_data = True
                        ctx.command_processor.commands["missing"] = cmd_missing
                        ctx.command_processor.commands["zones"] = cmd_zones
                        await self.read_options(ctx)
                        return True
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now
        return False

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk.context import AuthStatus
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        try:
            if ctx.auth_status == AuthStatus.AUTHENTICATED:
                room_id = await bizhawk.read(ctx.bizhawk_ctx, [(0x73084, 2, "MainRAM")])
                zone_value = await bizhawk.read(ctx.bizhawk_ctx, [(0x180000, 2, "MainRAM")])
                zone_data = ZoneData.get_zone_data(int.from_bytes(zone_value[0], "little"))
                area_value = await bizhawk.read(ctx.bizhawk_ctx, [(0x03c774, 2, "MainRAM")])
                area_data = ZoneData.get_zone_data(int.from_bytes(area_value[0], "little"))
                entered_cutscene = await bizhawk.read(ctx.bizhawk_ctx, [(0x03be20, 1, "MainRAM")])
                game_state_flag = await bizhawk.read(ctx.bizhawk_ctx, [(0x3c9a4, 1, "MainRAM")])

                if self.player_status == STATUS.START:
                    if room_id[0] == b'\x00\x00' or room_id[0] == b'\x00W':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.TITLE_SCREEN

                    if zone_value[0] == b'\x9c\x18' and room_id[0] == b'\xd0\xb2':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.RICHTER

                    if (entered_cutscene[0] == b'\x01' and game_state_flag[0] != b'\x04' and
                            zone_data[1].abrev not in ["UNK", "ST0"]):
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.ALUCARD

                if self.player_status == STATUS.TITLE_SCREEN:
                    self.load_once = False
                    if zone_value[0] == b'\x9c\x18' and room_id[0] == b'\xd0\xb2':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.RICHTER

                    if (entered_cutscene[0] == b'\x01' and game_state_flag[0] != b'\x04' and
                            zone_data[1].abrev not in ["UNK", "ST0"]):
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.ALUCARD

                    if self.patched:
                        # We got here after a reset
                        self.patched = False
                        self.load_once = False
                        self.traps = []
                        self.already_active_trap = []

                if self.player_status == STATUS.RICHTER:
                    if room_id[0] == b'\x00\x00':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.TITLE_SCREEN

                    if entered_cutscene[0] == b'\x01' and game_state_flag[0] != b'\x04':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.ALUCARD

                if self.player_status == STATUS.ALUCARD:
                    alucard_status = await bizhawk.read(ctx.bizhawk_ctx, [(0x073404, 1, "MainRAM")])

                    if room_id[0] == b'\x00\x00':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.TITLE_SCREEN

                    if alucard_status[0] == b'\x10':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.DIED

                if self.player_status == STATUS.DIED:
                    alucard_status = await bizhawk.read(ctx.bizhawk_ctx, [(0x073404, 1, "MainRAM")])
                    alucard_hp = await bizhawk.read(ctx.bizhawk_ctx, [(0x097ba0, 4, "MainRAM")])

                    if room_id[0] == b'\x00\x00':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.TITLE_SCREEN

                    if zone_value[0] == b'\x00\x00':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.DEAD
                        self.patched = False
                        self.load_once = False
                        self.traps = []
                        self.already_active_trap = []
                        await restore_ram(ctx, "Fall damage")
                        await restore_ram(ctx, "Ice floor")
                        await restore_ram(ctx, "Axe menu")

                    if alucard_status[0] == b'\x11':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.ALUCARD

                    if self.player_status == STATUS.DIED and alucard_hp[0] != b'\x00\x00\x00\x00':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.ALUCARD
                        self.load_once = False

                if self.player_status == STATUS.DEAD:
                    alucard_hp = await bizhawk.read(ctx.bizhawk_ctx, [(0x097ba0, 4, "MainRAM")])

                    if zone_value[0] == b'\xd8\xee':
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.TITLE_SCREEN

                    if alucard_hp[0] != b'\x00\x00\x00\x00' and zone_data[1].abrev not in ["UNK", "ST0"]:
                        self.last_player_status = self.player_status
                        self.player_status = STATUS.ALUCARD
                        self.load_once = False

                # Simple Clear Game Script - by Eigh7o
                if not self.patched and self.player_status in [STATUS.RICHTER, STATUS.ALUCARD]:
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x3bde0, b'\x02', "MainRAM")])
                    self.patched = True

                if self.player_status == STATUS.ALUCARD:
                    now = await self.elapse_time(ctx)
                    pause_screen = await bizhawk.read(ctx.bizhawk_ctx, [(0x09794c, 1, "MainRAM")])
                    self.cur_zone = (zone_data[1].abrev, zone_data[1].name)
                    sanity_option = self.options.sanity

                    if self.cur_zone != self.last_zone:
                        if self.cur_zone[0] == "UNK" and self.last_zone[0] == "BO6":
                            if "Ice floor" in self.already_active_trap and not self.paused_trap:
                                self.paused_trap = True
                                self.paused_richter = True
                                self.ice_paused.append(now)
                                await restore_ram(ctx, "Ice floor")
                        if self.cur_zone[0] == "RTOP" and self.last_zone[0] == "TOP":
                            if self.paused_trap:
                                if ("Axe Lord" not in self.already_active_trap and
                                        "Ice floor" in self.already_active_trap):
                                    self.paused_trap = False
                                    self.paused_richter = False
                                    self.ice_paused.append(now)
                                    await apply_trap(ctx, "Ice floor 5")

                        if self.last_zone[0] == "RNO0" and self.cur_zone[0] != "RNO0":
                            self.dracula_door = False
                            self.goal_diplayed = False

                    if not self.load_once:
                        self.load_once = True
                        self.last_item_received = await self.read_int(ctx, 0x03bf04, 2, "MainRAM")
                        self.last_misplaced = await self.read_int(ctx, 0x03bf1d, 2, "MainRAM")
                        self.last_trap_processed = await self.read_int(ctx, 0x03bf21, 2, "MainRAM")
                        self.populate_misplaced()
                        self.checked_locations = []
                        self.checked_locations.extend(list(ctx.checked_locations))
                        self.sent_checked_locations = self.checked_locations[:]
                        self.last_owned_relics = list(
                            (await bizhawk.read(ctx.bizhawk_ctx, [(0x097964, 30, "MainRAM")]))[0])
                        self.dracula_dead = False
                        await restore_ram(ctx, "Fall damage")
                        await restore_ram(ctx, "Ice floor")
                        await restore_ram(ctx, "Axe menu")

                    if zone_data[1].abrev == "RBO6" and area_data[1].abrev == "RBO6":
                        dracula_hp = await self.read_int(ctx, 0x076ed6, 2, "MainRAM")
                        if dracula_hp == 0 or dracula_hp > 60000:
                            self.dracula_dead = True

                    if zone_data[1].abrev == "RNO0" and area_data[1].abrev == "RNO0":
                        goal = self.check_completion()
                        rooms = int((self.options.exp * 10) / 0.107)
                        if not self.goal_diplayed:
                            logger.info(f"Secondary goal: {self.options.bosses} boss tokens / {rooms} rooms explored")
                            logger.info(f"Total: {goal[0]} / {goal[1]}")
                            if self.options.goal >= 4:
                                logger.info(f"Talisman -> Required: {self.options.talisman} Available:"
                                            f" {self.options.total_tal}")
                            self.goal_diplayed = True
                        rooms = int((self.options.exp * 10) / 0.107)
                        if not self.dracula_door and goal[0] >= self.options.bosses and goal[1] >= rooms:
                            if self.options.goal == 3:
                                await self.patch_dracula_door(ctx)
                            elif self.options.goal == 5:
                                total_talisman = await self.check_talisman(ctx)
                                if total_talisman >= self.options.talisman:
                                    await self.patch_dracula_door(ctx)

                    if not ctx.finished_game:
                        if self.dracula_dead:
                            total_talisman = await self.check_talisman(ctx)

                            if self.options.goal == 3:
                                await self.send_client_goal(ctx)
                            if self.options.goal == 5 and total_talisman >= self.options.talisman:
                                await self.send_client_goal(ctx)
                        if zone_data[1].abrev == "BO6" and area_data[1].abrev == "BO6":
                            game_end = False

                            if 0 <= self.options.goal <= 2:
                                if self.options.goal == 0:
                                    status = await bizhawk.read(ctx.bizhawk_ctx, [(0x03c0ec, 1, "MainRAM")])
                                    if status[0] == b'\x7f':
                                        game_end = True
                                elif self.options.goal == 1:
                                    shaft_ta = await bizhawk.read(ctx.bizhawk_ctx, [(0x03ca60, 2, "MainRAM")])
                                    if shaft_ta[0] != b'\x00\x00':
                                        game_end = True
                                elif self.options.goal == 2:
                                    status = await bizhawk.read(ctx.bizhawk_ctx, [(0x03c0ec, 1, "MainRAM")])
                                    shaft_ta = await bizhawk.read(ctx.bizhawk_ctx, [(0x03ca60, 2, "MainRAM")])
                                    if status[0] == b'\x7f' or shaft_ta[0] != b'\x00\x00':
                                        game_end = True

                                if game_end:
                                    await self.send_client_goal(ctx)
                        if self.options.goal == 4:
                            total_talisman = await self.check_talisman(ctx)
                            if total_talisman >= self.options.talisman:
                                await self.send_client_goal(ctx)

                    if self.cur_zone[0] not in ["UNK", "ST0", "RCEN", "RBO6"]:
                        await self.process_locations(ctx)
                        await self.process_sanity(ctx)
                        await self.process_misplaced(ctx)

                        if sanity_option & (1 << 4):
                            await self.process_multiple_traps(ctx, now)
                        else:
                            await self.process_traps(ctx, now)

                    if pause_screen[0] != b'\x00':
                        can_save = await self.read_int(ctx, 0x03C708, 1, "MainRAM")

                        if self.message_queue:
                            for _ in self.message_queue:
                                await bizhawk.display_message(ctx.bizhawk_ctx, self.message_queue.pop())
                        if self.received_queue:
                            for _ in self.received_queue:
                                await self.grant_item(self.received_queue.pop(), ctx)
                        if self.misplaced_queue:
                            for _ in self.misplaced_queue:
                                await self.grant_item(self.misplaced_queue.pop(), ctx)
                        if self.new_items:
                            await bizhawk.lock(ctx.bizhawk_ctx)
                            await self.sort_inventory(ctx)
                            await bizhawk.unlock(ctx.bizhawk_ctx)
                            self.new_items = []

                        if self.misplaced_changed:
                            await bizhawk.write(ctx.bizhawk_ctx,
                                                [(0x03bf1d, self.last_misplaced.to_bytes(2, "little"), "MainRAM")])
                            self.misplaced_changed = False

                        # Did we have received items
                        received_traps = 0
                        for i, item_received in enumerate(ctx.items_received):
                            received = ItemData.get_item_info(item_received.item)
                            if received[1].type == IType.TRAP:
                                if received_traps >= self.out_world_traps:
                                    self.out_world_traps += 1
                                    self.last_received_trap += 1
                                    self.add_misplaced(received[1].index + (self.last_received_trap * 1000) + 1000000)
                                    self.last_misplaced += 1
                                    self.misplaced_changed = True
                                    self.message_queue.append(f"Trap: {received[0]}")
                                    self.traps.append(TrapData(received[0], False, self.last_received_trap, -1))
                                received_traps += 1

                            if i + 1 > self.last_item_received:
                                if received[1].type != IType.TRAP:
                                    self.received_queue.append(received[1])
                                    self.message_queue.append(f"Granted: {received[0]}")
                                self.last_item_received = i + 1
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x03bf04, self.last_item_received.to_bytes(2, "little"), "MainRAM")])

                        if can_save & 0x20 == 0x20:
                            if sanity_option & (1 << 3) and "1 hit KO" not in self.already_active_trap:
                                max_hp = await self.read_int(ctx, 0x097ba4, 4, "MainRAM")
                                await bizhawk.write(ctx.bizhawk_ctx, [(0x97ba0, max_hp.to_bytes(4, "little"), "MainRAM")])
                                max_mp = await self.read_int(ctx, 0x097bb4, 4, "MainRAM")
                                await bizhawk.write(ctx.bizhawk_ctx, [(0x97bb0, max_mp.to_bytes(4, "little"), "MainRAM")])
                            if "Ice floor" in self.already_active_trap and not self.paused_trap:
                                self.paused_trap = True
                                self.ice_paused.append(now)
                                await restore_ram(ctx, "Ice floor")
                        else:
                            if self.paused_trap:
                                if ("Axe Lord" not in self.already_active_trap and
                                        "Ice floor" in self.already_active_trap and not self.paused_richter):
                                    self.paused_trap = False
                                    self.ice_paused.append(now)
                                    await apply_trap(ctx, "Ice floor 5")

                        if self.applied_axe == 1:
                            read_results = await bizhawk.guarded_read(ctx.bizhawk_ctx,
                                                                      [(0x17ae45, 1, "MainRAM")],
                                                                      [(0x17ae45, b'\x58', "MainRAM")])

                            if read_results is not None:
                                leap_stone = await bizhawk.read(ctx.bizhawk_ctx, [(0x097971, 1, "MainRAM")])
                                gravity_boots = await bizhawk.read(ctx.bizhawk_ctx, [(0x097970, 1, "MainRAM")])
                                # Thanks Wecoc from Long Library discord for the info on that
                                if leap_stone != b'\x00' or gravity_boots != b'\x00':
                                    await bizhawk.write(ctx.bizhawk_ctx, [(0x17ae45, b'\x10', "MainRAM")])
                                else:
                                    await bizhawk.write(ctx.bizhawk_ctx, [(0x17ae45, b'\x20', "MainRAM")])
                                await bizhawk.write(ctx.bizhawk_ctx, [(0x17ae40, b'\x20', "MainRAM")])
                                self.applied_axe = 2

                        if self.cur_zone != self.last_zone:
                            if self.cur_zone[0] != "UNK":
                                self.last_zone = self.cur_zone

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            print("ERROR")
            pass

    def on_package(self, ctx, cmd, args):
        if cmd == "PrintJSON":
            if 'item' in args:
                message_type: namedtuple = args['type']  # PrintJsonType of this message (optional)
                player: namedtuple = args['receiving']  # Destination player's ID
                received: NetworkItem = args['item']  # Source player's ID, location ID, item ID and item flags
                data: namedtuple = args['data']  # Textual content of this message

                if received.location == 127083080 or received.location == 127020003:
                    if int(data[0]['text']) == ctx.slot:
                        # Holy glasses and CAT - Mormegil, send a library card, so player won't get stuck
                        # If there are 2 SOTN players at the same time, both might receive a free library card
                        library_card = ItemData.get_item_info(166 + base_item_id)
                        self.misplaced_queue.append(library_card[1])

                if message_type == "ItemSend" and ctx.slot == player:
                    if base_item_id <= received.item <= base_item_id + 423:
                        # Check if the item came from offworld, Last location enemysanity Galamoth
                        if base_item_id <= received.location <= base_item_id + 490242:
                            loc_data: LocationData = get_location_data(received.location)
                        else:
                            loc_data = None

                        item_data = ItemData.get_item_info(received.item)

                        # Is an exploration item?
                        if 127110031 <= received.location <= 127110050:
                            self.message_queue.append(f"Exploration item: {item_data[0]}")
                            self.misplaced_queue.append(item_data[1])
                            self.add_misplaced(item_data[1].index)
                            self.last_misplaced += 1
                            self.misplaced_changed = True

                        if loc_data is not None:
                            if loc_data.can_be_relic:
                                # Item on a relic spot,  only bat card, skill of wolf, jewel of open and relics of vlad
                                if loc_data.game_id in [3074, 3141, 3142, 3211, 3221, 3252, 3261, 3305]:
                                    if item_data[1].type == IType.BOOST:
                                        self.message_queue.append(f"Boost: {item_data[0]}")
                                        self.misplaced_queue.append(item_data[1])
                                        self.add_misplaced(item_data[1].index)
                                        self.last_misplaced += 1
                                        self.misplaced_changed = True
                                    elif item_data[1].type == IType.TRAP:
                                        self.last_received_trap += 1
                                        self.message_queue.append(f"Trap: {item_data[0]}")
                                        self.add_misplaced(item_data[1].index + (self.last_received_trap * 1000))
                                        self.misplaced_changed = True
                                        self.traps.append(TrapData(item_data[0], False, self.last_received_trap, -1))
                                    elif item_data[1].type != IType.RELIC:
                                        self.message_queue.append(f"Misplaced item: {item_data[0]}")
                                        self.misplaced_queue.append(item_data[1])
                                        self.add_misplaced(item_data[1].index)
                                        self.last_misplaced += 1
                                        self.misplaced_changed = True
                                # Check for traps/boosts on relic spot
                                elif item_data[1].type == IType.BOOST:
                                    self.message_queue.append(f"Boost: {item_data[0]}")
                                    self.misplaced_queue.append(item_data[1])
                                    self.add_misplaced(item_data[1].index)
                                    self.last_misplaced += 1
                                    self.misplaced_changed = True
                                elif item_data[1].type == IType.TRAP:
                                    self.last_received_trap += 1
                                    self.message_queue.append(f"Trap: {item_data[0]}")
                                    self.add_misplaced(item_data[1].index + (self.last_received_trap * 1000))
                                    self.misplaced_changed = True
                                    self.traps.append(TrapData(item_data[0], False, self.last_received_trap, -1))
                            else:
                                # Check for Enemysanity
                                loc_name = loc_id_to_name[received.location]
                                if "Enemysanity" in loc_name:
                                    # Did we receive a trap
                                    if item_data[1].type == IType.TRAP:
                                        self.last_received_trap += 1
                                        self.message_queue.append(f"Trap: {item_data[0]}")
                                        self.add_misplaced(item_data[1].index + (self.last_received_trap * 1000))
                                        self.misplaced_changed = True
                                        self.traps.append(TrapData(item_data[0], False, self.last_received_trap, -1))
                                    else:
                                        self.message_queue.append(f"Enemysanity item: {item_data[0]}")
                                        self.misplaced_queue.append(item_data[1])
                                        self.add_misplaced(item_data[1].index)
                                        self.last_misplaced += 1
                                        self.misplaced_changed = True
                                elif "Dropsanity" in loc_name:
                                    # Did we receive a trap
                                    if item_data[1].type == IType.TRAP:
                                        self.last_received_trap += 1
                                        self.message_queue.append(f"Trap: {item_data[0]}")
                                        self.add_misplaced(item_data[1].index + (self.last_received_trap * 1000))
                                        self.misplaced_changed = True
                                        self.traps.append(TrapData(item_data[0], False, self.last_received_trap, -1))
                                    else:
                                        self.message_queue.append(f"Dropsanity item: {item_data[0]}")
                                        self.misplaced_queue.append(item_data[1])
                                        self.add_misplaced(item_data[1].index)
                                        self.last_misplaced += 1
                                        self.misplaced_changed = True
                                else:
                                    # Normal location
                                    if item_data[1].type == IType.RELIC:
                                        self.message_queue.append(f"Misplaced relic: {item_data[0]}")
                                        self.misplaced_queue.append(item_data[1])
                                        self.add_misplaced(item_data[1].index)
                                        self.last_misplaced += 1
                                        self.misplaced_changed = True
                                    elif item_data[1].type == IType.BOOST:
                                        self.message_queue.append(f"Boost: {item_data[0]}")
                                        self.misplaced_queue.append(item_data[1])
                                        self.add_misplaced(item_data[1].index)
                                        self.last_misplaced += 1
                                        self.misplaced_changed = True
                                    elif item_data[1].type == IType.TRAP:
                                        self.last_received_trap += 1
                                        self.message_queue.append(f"Trap: {item_data[0]}")
                                        self.add_misplaced(item_data[1].index + (self.last_received_trap * 1000))
                                        self.misplaced_changed = True
                                        self.traps.append(TrapData(item_data[0], False, self.last_received_trap, -1))
                elif message_type == "ItemSend" and ctx.slot != player and received.player == ctx.slot:
                    try:
                        player_name = ctx.player_names[player]
                    except KeyError:
                        player_name = "Unknown"
                    msg = f"Sent item to {player_name}"
                    self.message_queue.append(msg)
        super().on_package(ctx, cmd, args)

    @staticmethod
    async def elapse_time(ctx: "BizHawkClientContext") -> int:
        time_now = await bizhawk.read(ctx.bizhawk_ctx, [(0x097c30, 12, "MainRAM")])
        cur_time = list(bytes(time_now[0]))
        hour_now = cur_time[0] * 3600
        min_now = cur_time[4] * 60
        sec_now = cur_time[8]
        return hour_now + min_now + sec_now

    @staticmethod
    async def read_int(ctx: "BizHawkClientContext", address: int, size: int, domain: str) -> int:
        return int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(address, size, domain)]))[0], "little")

    async def read_options(self, ctx: "BizHawkClientContext"):
        read_value = await bizhawk.read(ctx.bizhawk_ctx, [(0x0dfaec, 108, "MainRAM")])
        read_list = list(bytes(read_value[0]))
        options = namedtuple("options", ["file_name", "sanity", "goal", "bosses", "exp", "talisman", "total_tal"])

        seed_list = read_list[0:10]
        pnum_list = read_list[10:11]
        sanity_list = read_list[11:12]
        luck_list = read_list[12:14]
        goal_list = read_list[14:15]
        bosses_list = read_list[15:16]
        exp_list = read_list[16:17]
        t_total_list = read_list[17:18]
        talisman_list = read_list[18:19]
        first_list = read_list[24:54]
        second_list = read_list[56:86]
        third_list = read_list[88:]
        seed = ""
        name = []
        name_read = False

        for b in seed_list:
            seed += str(b >> 4)
            seed += str(b & 0x0f)

        player = f"P{int(pnum_list[0])}"

        last_byte = 0x00
        for b in first_list:
            if b == 0x0a and last_byte == 0x0d:
                name_read = True
                break
            name.append(b)
            last_byte = b

        if not name_read:
            for b in second_list:
                if b == 0x0a and last_byte == 0x0d:
                    name_read = True
                    break
                name.append(b)
                last_byte = b

        if not name_read:
            for b in third_list:
                if b == 0x0a and last_byte == 0x0d:
                    break
                name.append(b)
                last_byte = b

        # Remove CR from the name
        name.pop()
        bytes_name = bytes(name)
        utf_name = bytes_name.decode("utf-8")

        misplaced_file_name = f"AP_{seed}_{player}_{utf_name}.txt"
        read_sanity = int(sanity_list[0])
        goal = int(goal_list[0])
        bosses = int(bosses_list[0])
        exp = int(exp_list[0])
        talisman = int(talisman_list[0])
        total_tal = int(t_total_list[0])
        self.options = Seed(misplaced_file_name, read_sanity, goal, bosses, exp, talisman, total_tal)
        ctx.username = utf_name

        logger.info(f"Running ROM seed: {seed} for player: {utf_name}")
        goal_str = "Kill "
        if goal == 0:
            goal_str += "Richter"
        elif goal == 1:
            goal_str += "Shaft"
        elif goal == 2:
            goal_str += "Shaft or Richter"
        elif goal == 3:
            goal_str += "Dracula"
        elif goal == 4:
            goal_str = f"{talisman} / {total_tal} Talisman farm"
        elif goal == 5:
            goal_str = f"{talisman} / {total_tal} Talisman farm and kill Dracula"
        logger.info(f"Goal: {goal_str}")
        if goal == 3 or goal == 5:
            rooms = int((exp * 10) / 0.107)
            logger.info(f"Bosses: {bosses} / Exploration: {exp} -> {rooms} rooms")
        logger.info("Have fun!")

    @staticmethod
    async def play_sfx(ctx: "BizHawkClientContext", snd_id: int):
        tries = 0

        while tries < 5:
            buffer_write = await bizhawk.read(ctx.bizhawk_ctx, [(0x80139000, 1, "System Bus")])
            buffer_write_int = int.from_bytes(buffer_write[0], "little")
            ring_buffer_pos = buffer_write_int * 6 + 0x801390dc

            await bizhawk.write(ctx.bizhawk_ctx, [(ring_buffer_pos, snd_id.to_bytes(1, "little"), "System Bus")])
            await bizhawk.write(ctx.bizhawk_ctx, [(ring_buffer_pos + 2, b'\xff\xff', "System Bus")])
            if buffer_write_int + 1 > 0xff:
                buffer_write_int = - 1
            results = await bizhawk.guarded_write(ctx.bizhawk_ctx,
                                                  [(0x80139000,
                                                    (buffer_write_int + 1).to_bytes(1, "little"), "System Bus")],
                                                  [(0x80139000, buffer_write[0], "System Bus")])

            if results:
                # We played sfx exit loop
                tries = 5
            else:
                # Some sfx played before try again
                tries += 1

    @staticmethod
    async def check_talisman(ctx: "BizHawkClientContext") -> int:
        equipped_1 = await bizhawk.read(ctx.bizhawk_ctx, [(0x97c14, 1, "MainRAM")])
        equipped_2 = await bizhawk.read(ctx.bizhawk_ctx, [(0x97c18, 1, "MainRAM")])
        qty_total = await bizhawk.read(ctx.bizhawk_ctx, [(0x097a86, 1, "MainRAM")])

        total = int.from_bytes(qty_total[0], "little")

        if equipped_1[0] == b'\x53':
            total += 1
        if equipped_2[0] == b'\x53':
            total += 1

        return total

    def check_completion(self) -> tuple:
        total_bosses = 0
        total_exp = 0

        bosses = [127143140, 127093091, 127073070, 127153154, 127053050, 127013010, 127103100, 127133130, 127133131,
                  127043041, 127023020, 127183180, 127193190, 127213210, 127223220, 127253251, 127263260, 127283280,
                  127293290, 127303304]
        exploration = [93, 186, 280, 373, 467, 560, 654, 747, 841, 934, 1028, 1121, 1214, 1308, 1401,
                       1495, 1588, 1682, 1775, 1869]

        for loc in self.checked_locations:
            if loc in bosses:
                total_bosses += 1
                bosses.remove(loc)
            if 127110011 <= loc <= 127110030:
                total_exp += 1

        return total_bosses, exploration[total_exp - 1]

    @staticmethod
    async def send_client_goal(ctx: "BizHawkClientContext"):
        ctx.finished_game = True
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

    async def patch_dracula_door(self, ctx: "BizHawkClientContext"):
        if self.dracula_door:
            return

        door_open = await bizhawk.read(ctx.bizhawk_ctx, [(0x3bed0, 1, "MainRAM")])

        if door_open[0] != b'\x00':
            self.dracula_door = True
            return

        write_result: bool = await bizhawk.guarded_write(
            ctx.bizhawk_ctx,
            [(0x001c132c, [0x18, 0x01, 0x40, 0x14], "System Bus")],
            [(0x001c132c, [0x18, 0x01, 0x00, 0x10], "System Bus")]
        )

        if write_result:
            self.dracula_door = True
            logger.info("Door instruction Patched")
            return

        write_result = await bizhawk.guarded_write(
            ctx.bizhawk_ctx,
            [(0x801c132c, [0x18, 0x01, 0x40, 0x14], "System Bus")],
            [(0x801c132c, [0x18, 0x01, 0x00, 0x10], "System Bus")]
        )

        if write_result:
            self.dracula_door = True
            logger.info("Door instruction Patched")
            return

    async def process_sanity(self, ctx: "BizHawkClientContext"):
        sanity_option = self.options.sanity

        if sanity_option & (1 << 0):
            enemy_flag = await bizhawk.read(ctx.bizhawk_ctx, [(0x03bf7c, 19, "MainRAM")])
            enemy_list = list(bytes(enemy_flag[0]))

            for k, v in enemy_locations.items():
                if loc_name_to_id[k] in self.checked_locations:
                    continue
                byte_check = 0 if v.game_id < 109 else int((v.game_id - 101) / 8)
                bit_check = (v.game_id - 101) % 8
                enemy = enemy_list[byte_check]

                if enemy & (1 << bit_check):
                    self.checked_locations.append(loc_name_to_id[k])
                    break
        if sanity_option & (1 << 1):
            drop_flag = await bizhawk.read(ctx.bizhawk_ctx, [(0x03bf9c, 19, "MainRAM")])
            drop_list = list(bytes(drop_flag[0]))

            for k, v in drop_locations.items():
                if loc_name_to_id[k] in self.checked_locations:
                    continue
                byte_check = 0 if v.game_id < 109 else int((v.game_id - 301) / 8)
                bit_check = (v.game_id - 301) % 8
                drop = drop_list[byte_check]

                if drop & (1 << bit_check):
                    self.checked_locations.append(loc_name_to_id[k])
                    break

    async def process_locations(self, ctx: "BizHawkClientContext"):
        zone_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x180000, 2, "MainRAM")]))[0], "little")

        try:
            zone_id, zone_data = ZoneData.get_zone_data(zone_value)
            if zone_data.loot_flag:
                loot_flag = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx,
                                        [(zone_data.loot_flag, zone_data.loot_size, "MainRAM")]))[0], "little")

            total_rooms = int.from_bytes(
                (await bizhawk.read(ctx.bizhawk_ctx, [(0x03c760, 2, "MainRAM")]))[0], "little")

            exploration = [93, 186, 280, 373, 467, 560, 654, 747, 841, 934, 1028, 1121, 1214, 1308, 1401,
                           1495, 1588, 1682, 1775, 1869]

            for i, e in enumerate(exploration):
                if total_rooms >= e:
                    loc_name = f"Exploration {(i * 10) + 10}"
                    loc_data = location_table[loc_name]
                    if loc_data.get_location_id() not in self.checked_locations:
                        self.checked_locations.append(loc_data.get_location_id())
                    loc_name = f"Exploration {(i * 10) + 10} item"
                    loc_data = location_table[loc_name]
                    if loc_data.get_location_id() not in self.checked_locations:
                        self.checked_locations.append(loc_data.get_location_id())

            for k, v in location_table.items():
                if (v.zone == zone_data.name or
                        (v.zone == "Colosseum" and zone_data.name == "Werewolf & Minotaur") or
                        (v.zone == "Catacombs" and zone_data.name == "Granfaloon") or
                        (v.zone == "Abandoned Mine" and zone_data.name == "Cerberus") or
                        (v.zone == "Royal Chapel" and zone_data.name == "Hippogryph") or
                        (v.zone == "Outer Wall" and zone_data.name == "Doppleganger10") or
                        (v.zone == "Olrox's Quarters" and zone_data.name == "Olrox") or
                        (v.zone == "Underground Caverns" and zone_data.name == "Scylla") or
                        (v.zone == "Reverse Colosseum" and zone_data.name == "Trio") or
                        (v.zone == "Floating Catacombs" and zone_data.name == "Galamoth") or
                        (v.zone == "Cave" and zone_data.name == "Death") or
                        (v.zone == "Anti-Chapel" and zone_data.name == "Medusa") or
                        (v.zone == "Reverse Outer Wall" and zone_data.name == "Creature") or
                        (v.zone == "Death Wing's Lair" and zone_data.name == "Akmodan II") or
                        (v.zone == "Reverse Caverns" and zone_data.name == "Doppleganger40") or
                        (v.zone == "Necromancy Laboratory" and zone_data.name == "Beezlebub") or
                        (v.zone == "Marble Gallery" and zone_data.name == "Center Cube")):
                    if v.game_id <= 3000:
                        # noinspection PyUnboundLocalVariable
                        if loot_flag & (1 << v.game_id):
                            if v.get_location_id() not in self.checked_locations:
                                self.checked_locations.append(v.get_location_id())
                    else:
                        await self.process_extra_locations(ctx, v.game_id, zone_data.abrev)

            if self.checked_locations != self.sent_checked_locations:
                self.sent_checked_locations = self.checked_locations[:]

                if self.sent_checked_locations is not None:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": self.sent_checked_locations
                    }])
        except TypeError as e:
            print(e)

    async def process_extra_locations(self, ctx: "BizHawkClientContext", game_id, zone_abbreviation):
        loc_data: LocationData
        check = []
        """
        check(type, name)
        boss,       name, kill time flag
        boss_relic, name, kill time flag
        relic,      name, offset, loot_flag, loot_size, relic_index, [relic pos()]
        wall,       name, flag, bit to check
        """

        if zone_abbreviation == "ARE" or zone_abbreviation == "BO2":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3010:
                check.append(("boss", "ARE - Minotaurus/Werewolf kill", 0x03ca38))
            if room == 0x2e90:
                check.append(("relic", "Form of Mist", 10, zones_dict[1].loot_flag, zones_dict[1].loot_size, 8,
                              [(222, 135)]))

        if zone_abbreviation == "CAT" or zone_abbreviation == "BO1":
            if game_id == 3020:
                check.append(("boss", "CAT - Granfaloon kill", 0x03ca34))

        if zone_abbreviation == "CHI" or zone_abbreviation == "BO7":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3040:
                check.append(("wall", "CHI - Turkey(Demon)", 0x03be3d, 0))
            elif game_id == 3041:
                check.append(("boss", "CHI - Cerberos kill", 0x03ca5c))
            if room == 0x19b8:
                check.append(("relic", "Demon Card", 10, zones_dict[4].loot_flag, zones_dict[4].loot_size, 13,
                              [(88, 167)]))

        if zone_abbreviation == "DAI" or zone_abbreviation == "BO5":
            if game_id == 3050:
                check.append(("boss", "DAI - Hippogryph kill", 0x03ca44))

        if zone_abbreviation == "LIB":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3070:
                check.append(("boss", "LIB - Lesser Demon kill", 0x03ca6c))
            if room == 0x2ec4:
                check.append(("relic", "Soul of Bat", 10, zones_dict[7].loot_flag, zones_dict[7].loot_size, 11,
                              [(1051, 919)]))
            elif room == 0x2f0c:
                check.append(("relic", "Faerie Scroll", 80, zones_dict[7].loot_flag, zones_dict[7].loot_size, 12,
                              [(1681, 167)]))
            elif room == 0x2ee4:
                check.append(("relic", "Jewel of Open", 10, 0, 0, 0, [(230, 135)]))
            elif room == 0x2efc:
                check.append(("relic", "Faerie Card", 10, zones_dict[7].loot_flag, zones_dict[7].loot_size, 13,
                              [(48, 167)]))

        if zone_abbreviation == "NO0" or zone_abbreviation == "CEN":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3080:
                check.append(("wall", "NO0 - Holy glasses", 0x03bec4, 0))
            if room == 0x27f4:
                check.append(("relic", "Spirit Orb", 10, zones_dict[8].loot_flag, zones_dict[8].loot_size, 14,
                              [(130, 1080)]))
            elif room == 0x2884:
                check.append(("relic", "Gravity Boots", 10, zones_dict[8].loot_flag, zones_dict[8].loot_size, 15,
                              [(1170, 167)]))

        if zone_abbreviation == "NO1" or zone_abbreviation == "BO4":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3090:
                check.append(("wall", "NO1 - Pot roast", 0x03bdfe, 0))
            elif game_id == 3091:
                check.append(("boss", "NO1 - Doppleganger 10 kill", 0x03ca30))
            if room == 0x34f4:
                check.append(("relic", "Soul of Wolf", 15, zones_dict[9].loot_flag, zones_dict[9].loot_size, 7,
                              [(360, 807), (375, 807)]))

        if zone_abbreviation == "NO2" or zone_abbreviation == "BO0":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3100:
                check.append(("boss", "NO2 - Olrox kill", 0x03ca2c))
            if room == 0x330c:
                check.append(("relic", "Echo of Bat", 10, zones_dict[10].loot_flag, zones_dict[10].loot_size, 13,
                              [(130, 135), (130, 165)]))
            elif room == 0x3314:
                check.append(("relic", "Sword Card", 10, zones_dict[10].loot_flag, zones_dict[10].loot_size, 14,
                              [(367, 135)]))

        if zone_abbreviation == "NO3":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3110:
                check.append(("wall", "NO3 - Pot roast", 0x03be1f, 0))
            elif game_id == 3111:
                check.append(("wall", "NO3 - Turkey", 0x03be24, 0))
            if room == 0x3d40 or room == 0x3af8:
                check.append(("relic", "Cube of Zoe", 10, zones_dict[11].loot_flag, zones_dict[11].loot_size, 10,
                              [(270, 103)]))
            elif room == 0x3cc8 or room == 0x3a80:
                check.append(("relic", "Power of Wolf", 10, zones_dict[11].loot_flag, zones_dict[11].loot_size, 11,
                              [(245, 183), (270, 183)]))

        if zone_abbreviation == "NO4" or zone_abbreviation == "BO3" or zone_abbreviation == "DRE":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3130:
                check.append(("boss", "NO4 - Scylla kill", 0x03ca3c))
            elif game_id == 3131:
                check.append(("boss", "NO4 - Succubus kill", 0x03ca4c))
            if room == 0x315c:
                check.append(("relic", "Holy Symbol", 10, zones_dict[13].loot_flag, zones_dict[13].loot_size, 37,
                              [(141, 167)]))
            elif room == 0x319c:
                check.append(("relic", "Merman Statue", 10, zones_dict[13].loot_flag, zones_dict[13].loot_size,
                              38, [(92, 167)]))

        if zone_abbreviation == "NZ0":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3140:
                check.append(("boss", "NZ0 - Slogra and Gaibon kill", 0x03ca40))
            if room == 0x2770:
                check.append(("relic", "Skill of Wolf", 25, 0, 0, 0, [(120, 167)]))
            elif room == 0x2730:
                check.append(("relic", "Bat Card", 25, 0, 0, 0, [(114, 167), (159, 119)]))

        if zone_abbreviation == "NZ1":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3150:
                check.append(("wall", "NZ1 - Bwaka knife", 0x03be8f, 2))
            elif game_id == 3151:
                check.append(("wall", "NZ1 - Pot roast", 0x03be8f, 0))
            elif game_id == 3152:
                check.append(("wall", "NZ1 - Shuriken", 0x03be8f, 1))
            elif game_id == 3153:
                check.append(("wall", "NZ1 - TNT", 0x03be8f, 3))
            elif game_id == 3154:
                check.append(("boss", "NZ1 - Karasuman kill", 0x03ca50))
            if room == 0x23a0:
                check.append(("relic", "Fire of Bat", 10, zones_dict[15].loot_flag, zones_dict[15].loot_size, 2,
                              [(198, 183)]))

        if zone_abbreviation == "TOP":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if room == 0x1b8c:
                check.append(("relic", "Leap Stone", 10, zones_dict[16].loot_flag, zones_dict[16].loot_size, 19,
                              [(424, 1815)]))
                check.append(("relic", "Power of Mist", 10, zones_dict[16].loot_flag, zones_dict[16].loot_size,
                              20, [(417, 1207)]))
            elif room == 0x1b94:
                check.append(("relic", "Ghost Card", 10, zones_dict[16].loot_flag, zones_dict[16].loot_size, 21,
                              [(350, 663)]))

        if zone_abbreviation == "RARE" or zone_abbreviation == "RBO0":
            if game_id == 3180:
                check.append(("boss", "RARE - Fake Trevor/Grant/Sypha kill", 0x03ca54))

        if zone_abbreviation == "RCAT" or zone_abbreviation == "RBO8":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3190:
                check.append(("boss", "RCAT - Galamoth kill", 0x03ca7c))
            if room == 0x2429 or room == 0x2490:
                check.append(("relic", "Gas Cloud", 10, zones_dict[19].loot_flag, zones_dict[19].loot_size, 18,
                              [(38, 173), (62, 190)]))

        if zone_abbreviation == "RCHI" or zone_abbreviation == "RBO2":
            if game_id == 3210 or game_id == 3211:
                check.append(("boss", "RCHI - Death kill", 0x03ca58))
                check.append(("boss_relic", "Eye of Vlad", 0x03ca58))

        if zone_abbreviation == "RDAI" or zone_abbreviation == "RBO3":
            if game_id == 3220 or game_id == 3221:
                check.append(("boss", "RDAI - Medusa kill", 0x03ca64))
                check.append(("boss_relic", "Heart of Vlad", 0x03ca64))

        if zone_abbreviation == "RNO1" or zone_abbreviation == "RBO4":
            if game_id == 3250:
                check.append(("wall", "RNO1 - Dim Sum set", 0x03be04, 0))
            elif game_id == 3251 or game_id == 3252:
                check.append(("boss", "RNO1 - Creature kill", 0x03ca68))
                check.append(("boss_relic", "Tooth of Vlad", 0x03ca68))

        if zone_abbreviation == "RNO2" or zone_abbreviation == "RBO7":
            if game_id == 3260 or game_id == 3261:
                check.append(("boss", "RNO2 - Akmodan II kill", 0x03ca74))
                check.append(("boss_relic", "Rib of Vlad", 0x03ca74))

        if zone_abbreviation == "RNO3":
            if game_id == 3270:
                check.append(("wall", "RNO3 - Pot roast", 0x03be27, 0))

        if zone_abbreviation == "RNO4" or zone_abbreviation == "RBO5":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3280:
                check.append(("boss", "RNO4 - Doppleganger40 kill", 0x03ca70))
            if room == 0x2c6c:
                check.append(("relic", "Force of Echo", 10, zones_dict[28].loot_flag, zones_dict[28].loot_size,
                              27, [(110, 167), (132, 167)]))

        if zone_abbreviation == "RNZ0" or zone_abbreviation == "RBO1":
            if game_id == 3290:
                check.append(("boss", "RNZ0 - Beezelbub kill", 0x03ca48))

        if zone_abbreviation == "RNZ1":
            if game_id == 3300:
                check.append(("wall", "RNZ1 - Bwaka knife", 0x03be97, 2))
            elif game_id == 3301:
                check.append(("wall", "RNZ1 - Pot roast", 0x03be97, 0))
            elif game_id == 3302:
                check.append(("wall", "RNZ1 - Shuriken", 0x03be97, 1))
            elif game_id == 3303:
                check.append(("wall", "RNZ1 - TNT", 0x03be97, 3))
            elif game_id == 3304 or game_id == 3305:
                check.append(("boss", "RNZ1 - Darkwing bat kill", 0x03ca78))
                check.append(("boss_relic", "Ring of Vlad", 0x03ca78))

        if check:
            for c in check:
                loc_data = location_table[c[1]]
                if c[0] == "boss" or c[0] == "boss_relic":
                    boss_kill = int.from_bytes(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(c[2], 2, "MainRAM")]))[0], "little")
                    if boss_kill != 0:
                        if loc_data.get_location_id() not in self.checked_locations:
                            self.checked_locations.append(loc_data.get_location_id())
                            # Add Doppleganger10 checks for good measure
                            if c[1] == "RNO4 - Doppleganger40 kill":
                                loc_data = location_table["NO1 - Doppleganger 10 kill"]
                                self.checked_locations.append(loc_data.get_location_id())
                                sanity_options = self.options.sanity

                                if sanity_options & (1 << 0):
                                    loc_data = location_table["Enemysanity: 34 - Doppleganger10"]
                                    self.checked_locations.append(loc_data.get_location_id())
                elif c[0] == "relic":
                    player_x = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x0973f0, 2, "MainRAM")]))[0],
                                              "little")
                    player_y = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x0973f4, 2, "MainRAM")]))[0],
                                              "little")

                    if loc_data.get_location_id() not in self.checked_locations:
                        if c[1] not in ["Jewel of Open", "Bat Card", "Skill of Wolf"]:
                            loot_flag = int.from_bytes(
                                (await bizhawk.read(ctx.bizhawk_ctx, [(c[3], c[4], "MainRAM")]))[0],
                                "little")
                            if loot_flag & (1 << c[5]):
                                # We get an item on relic location
                                self.checked_locations.append(loc_data.get_location_id())
                                self.message_queue.append(f"{c[1]} checked")
                            else:
                                owned_relics = await bizhawk.read(ctx.bizhawk_ctx, [(0x097964, 30, "MainRAM")])
                                # Are we close to a relic location?
                                for point in c[6]:
                                    x = abs(int(point[0]) - player_x)
                                    y = abs(int(point[1]) - player_y)
                                    if 0 <= x <= 50 and 0 <= y <= 50:
                                        result = await self.check_relic(owned_relics)
                                        if result:
                                            self.checked_locations.append(loc_data.get_location_id())
                                            self.message_queue.append(f"{c[1]} checked")
                                            break
                        else:
                            for point in c[6]:
                                o = c[2]
                                x = abs(int(point[0]) - player_x)
                                y = abs(int(point[1]) - player_y)
                                if 0 <= x <= o and 0 <= y <= o:
                                    self.checked_locations.append(loc_data.get_location_id())
                                    self.message_queue.append(f"{c[1]} checked")
                                    break
                elif c[0] == "wall":
                    loot_flag = int.from_bytes(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(c[2], 1, "MainRAM")]))[0], "little")
                    if loot_flag & (1 << c[3]):
                        if loc_data.get_location_id() not in self.checked_locations:
                            self.checked_locations.append(loc_data.get_location_id())

    def populate_misplaced(self):
        if self.options.file_name == "":
            messagebox("Error", "Looks like we don't have seed options", error=True)
            return
        self.misplaced_load = []
        self.traps = []
        self.last_received_trap = 0
        self.out_world_traps = 0

        filename = self.options.file_name
        filepath = Path(f"{user_path()}/{filename}")

        if not os.path.exists(filepath):
            with open(filepath, "w") as stream:
                stream.write(f"Save file for {self.options.file_name}\n")

        with open(filepath, "r") as stream:
            next(stream)
            for line in stream:
                if "Save" in line:
                    continue
                item_id = int(line[-4:])
                prefix = int(line[0:3])
                if 350 <= item_id <= 371:
                    if prefix == 128:
                        self.out_world_traps += 1
                    trap_received = int(line[3:6])
                    trap_name = trap_id_to_name[item_id]
                    self.traps.append(TrapData(trap_name, False, trap_received, -1))

                    if trap_received > self.last_received_trap:
                        self.last_received_trap = trap_received
                else:
                    self.misplaced_load.append(line)

        for trap in self.traps:
            if trap.received_position <= self.last_trap_processed:
                trap.trap_ended = True

    def add_misplaced(self, item_id: int):
        if self.options.file_name == "":
            messagebox("Error", "Looks like we don't have seed options", error=True)
            return
        filename = self.options.file_name
        filepath = Path(f"{user_path()}/{filename}")

        if not os.path.exists(filepath):
            with open(filepath, "w") as stream:
                stream.write(f"Save file for {self.options.file_name}\n")

        with open(filepath, "a") as stream:
            stream.write(f"{item_id}\n")

    async def process_misplaced(self, ctx: "BizHawkClientContext"):
        if self.last_misplaced < len(self.misplaced_load):
            for i, misplaced in enumerate(self.misplaced_load):
                if self.last_misplaced < i + 1:
                    misplaced_item = ItemData.get_item_info(int(misplaced))
                    self.misplaced_queue.append(misplaced_item[1])
                    self.last_misplaced = i + 1
            await bizhawk.write(
                ctx.bizhawk_ctx, [(0x03bf1d, self.last_misplaced.to_bytes(2, "little"), "MainRAM")])

    async def sort_inventory(self, ctx: "BizHawkClientContext"):
        # Inventory: 0x097a8e - 0x097b8e
        # Quantity: 0x09798b - 0x097a8b
        inventory = await bizhawk.read(ctx.bizhawk_ctx, [(0x097a8e, 258, "MainRAM")])
        quantity = await bizhawk.read(ctx.bizhawk_ctx, [(0x09798b, 258, "MainRAM")])
        inv_list = list(bytes(inventory[0]))
        qty_list = list(bytes(quantity[0]))

        for item in self.new_items:
            if (170 <= item <= 194) or item == 258:
                offset = 169
                start_byte = 0x00
            elif 196 <= item <= 216:
                offset = 195
                start_byte = 0x1a
            elif 218 <= item <= 225:
                offset = 217
                start_byte = 0x30
            elif 227 <= item <= 257:
                offset = 226
                start_byte = 0x39
            else:
                offset = 0
                start_byte = 0x00

            for i in range(offset, 257, 1):
                old_item = inv_list[i]
                old_qty = qty_list[(old_item - start_byte) + offset - 1]
                if old_qty == 0:
                    for k in range(offset, 259, 1):
                        if inv_list[k] == item - offset + start_byte:
                            inv_list[i] = item - offset + start_byte
                            qty_list[item - 1] = 1
                            inv_list[k] = old_item
                            break
                    break

        await bizhawk.write(ctx.bizhawk_ctx, [(0x097a8e, bytes(inv_list), "MainRAM")])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x09798b, bytes(qty_list), "MainRAM")])

    async def process_traps(self, ctx: "BizHawkClientContext", time: int):
        status = await bizhawk.read(ctx.bizhawk_ctx, [(0x073404, 1, "MainRAM")])
        pause_screen = await bizhawk.read(ctx.bizhawk_ctx, [(0x09794c, 1, "MainRAM")])
        if status[0] == b'\x0b' or pause_screen[0] == b'\x00':
            return
        trap_index = -1

        for i, trap in enumerate(self.traps):
            if not trap.trap_ended:
                trap_index = i
                break

        if trap_index == -1:
            return

        trap_data: TrapData = self.traps[trap_index]
        time_name = "minutes"
        if "1" in trap_data.trap_name and "10" not in trap_data.trap_name:
            time_name = "minute"

        if "Ice" in trap_data.trap_name:
            trap_type = "Ice floor"
        elif "Fall" in trap_data.trap_name:
            trap_type = "Fall damage"
        elif "1 hit KO" in trap_data.trap_name:
            trap_type = "1 hit KO"
            time_name = "seconds"
        elif "Axe Lord" in trap_data.trap_name:
            trap_type = "Axe Lord"
        else:
            trap_type = "Not timed"

        if not trap_data.trap_active:
            if trap_data.start_time == -1:
                trap_data.start_time = time

            if trap_type != "Axe Lord":
                await self.play_sfx(ctx, 0xf2)

            if trap_type == "Not timed":
                result_str = ""
                if "Teleport to zone entrance" in trap_data.trap_name:
                    safe_teleport = True
                    room = await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")])
                    if self.cur_zone[0] in ["UNK", "NO3", "RCEN", "RBO6", "DRE"]:
                        safe_teleport = False
                    if self.cur_zone[0] == "RTOP":
                        if self.last_zone[0] in ["TOP", "UNK", "RTOP"]:
                            safe_teleport = False
                    if "BO" in self.cur_zone[0]:
                        safe_teleport = False
                    if room[0] == b'\xc4\x2e' or room[0] == b'\x40\x23' or room[0] == b'\xc8\x24':
                        safe_teleport = False

                    if safe_teleport:
                        await apply_trap(ctx, trap_data.trap_name)
                        logger.info(f"Trap: {trap_data.trap_name} applied")
                    else:
                        logger.info(f"Not safe to teleport. Trap supressed!")
                else:
                    result_str = await apply_trap(ctx, trap_data.trap_name)
                    logger.info(f"Trap: {trap_data.trap_name} applied")

                trap_data.trap_ended = True
                trap_data.trap_announce = True
                trap_data.trap_active = False
                self.last_trap_processed += 1
                # Update last trap processed on RAM
                await bizhawk.write(ctx.bizhawk_ctx,
                                    [(0x03bf21, self.last_trap_processed.to_bytes(2, "little"), "MainRAM")])

                if result_str != "":
                    logger.info(result_str)
                return
            else:
                if trap_type in ["Ice floor", "Fall damage"]:
                    await apply_trap(ctx, trap_data.trap_name)
                elif trap_type in ["1 hit KO"]:
                    self.hp_backup = await self.read_int(ctx, 0x097ba0, 4, "MainRAM")
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x097ba0, b'\x01\x00\x00\x00', "MainRAM")])
                elif trap_type in ["Axe Lord"]:
                    status = await bizhawk.read(ctx.bizhawk_ctx, [(0x073404, 1, "MainRAM")])
                    if status[0] == b'\x0b':
                        return
                    if not await self.safe_axe_lord(ctx):
                        return

                    self.equip_backup = await bizhawk.read(ctx.bizhawk_ctx, [(0x97c0c, 1, "MainRAM")])
                    self.hand_backup = await bizhawk.read(ctx.bizhawk_ctx, [(0x97c00, 1, "MainRAM")])
                    self.shield_backup = await bizhawk.read(ctx.bizhawk_ctx, [(0x97c04, 1, "MainRAM")])
                    await apply_trap(ctx, trap_data.trap_name)
                    self.applied_axe = 1

                trap_data.trap_active = True
                trap_data.trap_announce = True
                self.already_active_trap.append(trap_type)
                logger.info(f"Trap: {trap_data.trap_name} {time_name} active")
        else:
            if "Ice floor" in trap_type and self.paused_trap:
                return

            total_paused = 0
            total_time = 0

            if "Ice" in trap_data.trap_name:
                for i in range(0, len(self.ice_paused) - 1, 2):
                    try:
                        total_paused += self.ice_paused[i + 1] - self.ice_paused[i]
                    except IndexError:
                        pass

            if "10" in trap_data.trap_name:
                total_time = 600
            elif "5" in trap_data.trap_name:
                total_time = 300
            elif "2" in trap_data.trap_name:
                total_time = 120
            elif "1" in trap_data.trap_name:
                total_time = 60

            if "1 hit KO" in trap_data.trap_name:
                if "60" in trap_data.trap_name:
                    total_time = 60
                elif "30" in trap_data.trap_name:
                    total_time = 30

            if time - trap_data.start_time - total_paused >= total_time:
                if "1 hit KO" in trap_data.trap_name:
                    await bizhawk.write(
                        ctx.bizhawk_ctx, [(0x097ba0, self.hp_backup.to_bytes(4, "little"), "MainRAM")])
                    self.hp_backup = 0
                elif "Axe Lord" in trap_data.trap_name:
                    await restore_ram(ctx, trap_data.trap_name)
                    # Wait returning to gameplay
                    menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
                    while menu_step[0] != b'\x0e':
                        menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
                    await bizhawk.lock(ctx.bizhawk_ctx)
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x3c9a4, b'\x02', "MainRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x978f8, b'\x00', "MainRAM")])
                    await bizhawk.unlock(ctx.bizhawk_ctx)
                    menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
                    while menu_step[0] != b'\x10':
                        menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x97c0c, self.equip_backup[0], "MainRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x97c00, self.hand_backup[0], "MainRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x97c04, self.shield_backup[0], "MainRAM")])
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x978f8, b'\x03', "MainRAM")])
                    self.applied_axe = 0
                elif "Ice floor" in trap_data.trap_name:
                    self.ice_paused = []
                    await restore_ram(ctx, trap_data.trap_name)
                elif "Fall damage" in trap_data.trap_name:
                    await restore_ram(ctx, trap_data.trap_name)

                self.already_active_trap = []
                trap_data.trap_ended = True
                logger.info(f"Trap: {trap_data.trap_name} {time_name} ended!")
                self.last_trap_processed += 1
                # Update last trap processed on RAM
                await bizhawk.write(ctx.bizhawk_ctx,
                                    [(0x03bf21, self.last_trap_processed.to_bytes(2, "little"), "MainRAM")])

                remaining_traps = ""
                total_traps = len(self.traps)
                if self.last_trap_processed < total_traps:
                    for i, traps in enumerate(self.traps):
                        if i >= self.last_trap_processed:
                            remaining_traps += traps.trap_name
                            if i != total_traps - 1:
                                remaining_traps += ", "
                if remaining_traps != "":
                    logger.info(f"Remaining traps: {remaining_traps}")
            else:
                if "1 hit KO" in trap_data.trap_name:
                    cur_hp = await self.read_int(ctx, 0x097ba0, 4, "MainRAM")

                    if cur_hp != 1:
                        await bizhawk.write(ctx.bizhawk_ctx, [(0x097ba0, b'\x01\x00\x00\x00', "MainRAM")])

    async def process_multiple_traps(self, ctx: "BizHawkClientContext", time: int):
        update_trap_data = False

        for trap in self.traps:
            pause_screen = await bizhawk.read(ctx.bizhawk_ctx, [(0x09794c, 1, "MainRAM")])
            if trap.trap_ended:
                continue
            if pause_screen[0] == b'\x00':
                return

            time_name = "minutes"
            if "1" in trap.trap_name and "10" not in trap.trap_name:
                time_name = "minute"

            if "stone" in trap.trap_name:
                status = await bizhawk.read(ctx.bizhawk_ctx, [(0x073404, 1, "MainRAM")])
                if status[0] == b'\x0b':
                    continue

            if "Ice" in trap.trap_name:
                trap_type = "Ice floor"
            elif "Fall" in trap.trap_name:
                trap_type = "Fall damage"
            elif "1 hit KO" in trap.trap_name:
                trap_type = "1 hit KO"
                time_name = "seconds"
            elif "Axe Lord" in trap.trap_name:
                trap_type = "Axe Lord"
            else:
                trap_type = "Not timed"

            if not trap.trap_active:
                if trap.start_time == -1:
                    trap.start_time = time

                if "Axe Lord" in self.already_active_trap:
                    if "Ice floor" in trap.trap_name or "stone" in trap.trap_name:
                        continue

                if "Ice" in trap.trap_name and not self.paused_trap:
                    if trap_type not in self.already_active_trap:
                        await self.play_sfx(ctx, 0xf2)
                        await apply_trap(ctx, trap.trap_name)
                        trap.trap_active = True
                        self.already_active_trap.append(trap_type)
                        if not trap.trap_announce:
                            trap.trap_announce = True
                            logger.info(f"Trap: {trap.trap_name} {time_name} active")
                else:
                    if "1 hit KO" in trap.trap_name:
                        if trap_type not in self.already_active_trap:
                            await self.play_sfx(ctx, 0xf2)
                            self.hp_backup = await self.read_int(ctx, 0x097ba0, 4, "MainRAM")
                            await bizhawk.write(ctx.bizhawk_ctx, [(0x097ba0, b'\x01\x00\x00\x00', "MainRAM")])
                            self.already_active_trap.append(trap_type)
                    elif "Axe Lord" in trap.trap_name:
                        if trap_type not in self.already_active_trap:
                            status = await bizhawk.read(ctx.bizhawk_ctx, [(0x073404, 1, "MainRAM")])
                            if status[0] == b'\x0b':
                                continue
                            if not await self.safe_axe_lord(ctx):
                                continue

                            self.applied_axe = 1
                            self.equip_backup = await bizhawk.read(ctx.bizhawk_ctx, [(0x97c0c, 1, "MainRAM")])
                            self.hand_backup = await bizhawk.read(ctx.bizhawk_ctx, [(0x97c00, 1, "MainRAM")])
                            self.shield_backup = await bizhawk.read(ctx.bizhawk_ctx, [(0x97c04, 1, "MainRAM")])
                            await apply_trap(ctx, trap.trap_name)
                            self.already_active_trap.append(trap_type)
                            if "Ice floor" in self.already_active_trap:
                                self.ice_paused.append(time)
                                self.paused_trap = True
                    else:
                        if trap_type not in self.already_active_trap:
                            if "Teleport to zone entrance" in trap.trap_name:
                                # Using on NO3 lock Alucard outside the gate, RTOP weird bugs
                                safe_teleport = True
                                status = await bizhawk.read(ctx.bizhawk_ctx, [(0x073404, 1, "MainRAM")])
                                if status[0] == b'\x0b':
                                    continue
                                room = await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")])
                                if self.cur_zone[0] in ["UNK", "NO3", "RCEN", "RBO6", "DRE"]:
                                    safe_teleport = False
                                if self.cur_zone[0] == "RTOP":
                                    if self.last_zone[0] in ["TOP", "UNK", "RTOP"]:
                                        safe_teleport = False
                                if "BO" in self.cur_zone[0]:
                                    safe_teleport = False
                                if room[0] == b'\xc4\x2e' or room[0] == b'\x40\x23' or room[0] == b'\xc8\x24':
                                    safe_teleport = False

                                if safe_teleport:
                                    await self.play_sfx(ctx, 0xf2)
                                    await apply_trap(ctx, trap.trap_name)
                                    trap.trap_ended = True
                                    trap.trap_announce = True
                                    self.last_trap_processed += 1
                                    update_trap_data = True
                                    result_str = ""
                                    logger.info(f"Trap: {trap.trap_name} applied")
                                else:
                                    result_str = "Not safe to teleport. Trap supressed!"
                            else:
                                await self.play_sfx(ctx, 0xf2)
                                result_str = await apply_trap(ctx, trap.trap_name)

                            if result_str != "":
                                logger.info(result_str)
                            if trap_type != "Not timed":
                                self.already_active_trap.append(trap_type)
                    trap.trap_active = True
                    if not trap.trap_announce:
                        trap.trap_announce = True
                        if "Not timed" in trap_type:
                            if "Teleport to zone entrance" not in trap.trap_name:
                                logger.info(f"Trap: {trap.trap_name} applied")
                                trap.trap_ended = True
                                self.last_trap_processed += 1
                                update_trap_data = True
                        else:
                            if "Ice" in trap.trap_name and self.paused_trap:
                                continue
                            logger.info(f"Trap: {trap.trap_name} {time_name} active")
            else:
                if "Ice" in trap.trap_name and self.paused_trap:
                    continue

                total_paused = 0
                total_time = 0
                remaining_time = 0

                if "Ice" in trap.trap_name:
                    for i in range(0, len(self.ice_paused) - 1, 2):
                        try:
                            total_paused += self.ice_paused[i + 1] - self.ice_paused[i]
                        except IndexError:
                            pass

                if "10" in trap.trap_name:
                    total_time = 600
                elif "5" in trap.trap_name:
                    total_time = 300
                elif "2" in trap.trap_name:
                    total_time = 120
                elif "1" in trap.trap_name:
                    total_time = 60

                if "1 hit KO" in trap.trap_name:
                    if "60" in trap.trap_name:
                        total_time = 60
                    elif "30" in trap.trap_name:
                        total_time = 30

                if time - trap.start_time - total_paused >= total_time:
                    if "Not timed" not in trap_type:
                        logger.info(f"Trap: {trap.trap_name} {time_name} ended!")
                        if "Ice floor" in trap_type:
                            self.ice_paused = []
                    last_trap = True
                    trap.trap_ended = True
                    for inner_trap in self.traps:
                        if inner_trap.trap_ended or "Not timed" in trap_type:
                            continue

                        if trap_type in inner_trap.trap_name:
                            last_trap = False
                            time_index = inner_trap.trap_name.rfind(' ') + 1
                            remaining_time += int(inner_trap.trap_name[time_index:])
                            inner_trap.start_time = time
                            if "Ice floor" in trap_type:
                                inner_trap.trap_active = True

                    if last_trap:
                        if "1 hit KO" in trap.trap_name:
                            max_hp = await self.read_int(ctx, 0x097ba4, 4, "MainRAM")
                            if self.hp_backup > max_hp:
                                self.hp_backup = max_hp
                            await bizhawk.write(
                                ctx.bizhawk_ctx, [(0x097ba0, self.hp_backup.to_bytes(4, "little"), "MainRAM")])
                            self.hp_backup = 0
                        elif "Axe Lord" in trap.trap_name:
                            await restore_ram(ctx, trap.trap_name)
                            # Wait returning to gameplay
                            menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
                            while menu_step[0] != b'\x0e':
                                menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
                            await bizhawk.lock(ctx.bizhawk_ctx)
                            await bizhawk.write(ctx.bizhawk_ctx, [(0x3c9a4, b'\x02', "MainRAM")])
                            await bizhawk.write(ctx.bizhawk_ctx, [(0x978f8, b'\x00', "MainRAM")])
                            await bizhawk.unlock(ctx.bizhawk_ctx)
                            menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
                            while menu_step[0] != b'\x10':
                                menu_step = await bizhawk.read(ctx.bizhawk_ctx, [(0x978f8, 1, "MainRAM")])
                            await bizhawk.write(ctx.bizhawk_ctx, [(0x97c0c, self.equip_backup[0], "MainRAM")])
                            await bizhawk.write(ctx.bizhawk_ctx, [(0x97c00, self.hand_backup[0], "MainRAM")])
                            await bizhawk.write(ctx.bizhawk_ctx, [(0x97c04, self.shield_backup[0], "MainRAM")])
                            await bizhawk.write(ctx.bizhawk_ctx, [(0x978f8, b'\x03', "MainRAM")])
                            self.applied_axe = 0
                            if self.paused_trap:
                                self.ice_paused.append(time)
                                self.paused_trap = False
                        else:
                            await restore_ram(ctx, trap.trap_name)

                        if trap_type != "Not timed":
                            self.already_active_trap.remove(trap_type)
                        last_ended = 0
                        for i, t in enumerate(self.traps, start=1):
                            if t.trap_ended:
                                last_ended = t.received_position
                            else:
                                break

                        if last_ended != 0 and last_ended > self.last_trap_processed:
                            self.last_trap_processed = last_ended
                            update_trap_data = True

                    if remaining_time != 0:
                        name_index = trap.trap_name.rfind(' ')
                        logger.info(f"{trap.trap_name[0:name_index]} -> {remaining_time} {time_name} remaining")
                else:
                    if "1 hit KO" in trap.trap_name:
                        cur_hp = await self.read_int(ctx, 0x097ba0, 4, "MainRAM")

                        if cur_hp != 1:
                            await bizhawk.write(ctx.bizhawk_ctx, [(0x097ba0, b'\x01\x00\x00\x00', "MainRAM")])

        if update_trap_data:
            # Update last trap processed on RAM
            await bizhawk.write(ctx.bizhawk_ctx,
                                [(0x03bf21, self.last_trap_processed.to_bytes(2, "little"), "MainRAM")])

    async def grant_item(self, item: ItemData, ctx: "BizHawkClientContext"):
        item_id = item.index - base_item_id
        address = item.address

        if 330 <= item_id < 370:
            boost_name = item_id_to_name[item_id]
            if "Experience boost" in boost_name:
                xp_boost = 0
                if boost_name == "Experience boost 1k":
                    xp_boost = 1000
                elif boost_name == "Experience boost 5k":
                    xp_boost = 5000
                elif boost_name == "Experience boost 10k":
                    xp_boost = 10000
                cur_xp = await self.read_int(ctx, address, 4, "MainRAM")
                new_xp = cur_xp + xp_boost
                await bizhawk.write(ctx.bizhawk_ctx, [(address, new_xp.to_bytes(4, "little"), "MainRAM")])
            elif "Max" in boost_name:
                boost = 0
                if "10" in boost_name:
                    boost = 10
                elif "50" in boost_name:
                    boost = 50
                cur_value = await self.read_int(ctx, address, 4, "MainRAM")
                new_value = cur_value + boost
                await bizhawk.write(ctx.bizhawk_ctx, [(address, new_value.to_bytes(4, "little"), "MainRAM")])
            elif "restore" in boost_name:
                max_value = await self.read_int(ctx, address + 4, 4, "MainRAM")
                await bizhawk.write(ctx.bizhawk_ctx, [(address, max_value.to_bytes(4, "little"), "MainRAM")])
        elif 300 <= item_id <= 329:
            relic = await self.read_int(ctx, address, 1, "MainRAM")
            self.received_relics.append(item_id)

            if relic == 0 or relic == 2 or relic > 3:
                if 318 <= item_id <= 322:
                    await bizhawk.write(ctx.bizhawk_ctx, [(address, b'\x01', "MainRAM")])
                else:
                    await bizhawk.write(ctx.bizhawk_ctx, [(address, b'\x03', "MainRAM")])
            owned_relics = await bizhawk.read(ctx.bizhawk_ctx, [(0x097964, 30, "MainRAM")])
            owned_list = list(bytes(owned_relics[0]))
            self.last_owned_relics = owned_list
        elif item_id == 412:
            cur_heart = await self.read_int(ctx, address, 4, "MainRAM")
            max_heart = await self.read_int(ctx, address + 4, 4, "MainRAM")
            cur_heart += 5
            max_heart += 5
            await bizhawk.write(ctx.bizhawk_ctx, [(address, cur_heart.to_bytes(4, "little"), "MainRAM")])
            await bizhawk.write(ctx.bizhawk_ctx, [(address + 4, max_heart.to_bytes(4, "little"), "MainRAM")])
        elif item_id == 423:
            max_hp = await self.read_int(ctx, address + 4, 4, "MainRAM")
            max_hp += 5
            await bizhawk.write(ctx.bizhawk_ctx, [(address, max_hp.to_bytes(4, "little"), "MainRAM")])
            await bizhawk.write(ctx.bizhawk_ctx, [(address + 4, max_hp.to_bytes(4, "little"), "MainRAM")])
        else:
            qty = await self.read_int(ctx, address, 1, "MainRAM")

            if qty < 255:
                qty += 1
            # First item, sort the inventory
            if qty == 1:
                self.new_items.append(item_id)
            else:
                await bizhawk.write(ctx.bizhawk_ctx, [(address, qty.to_bytes(1, "little"), "MainRAM")])

    async def check_relic(self, owned: list) -> bool:
        owned_list = list(bytes(owned[0]))

        if self.last_owned_relics:
            for i in range(30):
                if owned_list[i] != self.last_owned_relics[i] and self.last_owned_relics[i] == 0:
                    # Did we just receive a relic?
                    for relic in self.received_relics:
                        relic_index = 300 + i
                        if i > 22:
                            relic_index = 300 + i + 2
                        if relic_index == relic:
                            continue
                    # TODO: That might consider receive relic as looted.
                    self.last_owned_relics = owned_list
                    return True

        self.last_owned_relics = owned_list
        return False

    async def safe_axe_lord(self, ctx: "BizHawkClientContext") -> bool:
        pausable = await self.read_int(ctx, 0x3c8b8, 1, "MainRAM")
        cutscene_flag = await self.read_int(ctx, 0x72efc, 1, "MainRAM")

        if pausable == 1 and cutscene_flag == 0:
            return True
        else:
            return False


def cmd_missing(self, filter_text="") -> bool:
    """List all missing location checks, from your local game state.
    Can be given text, which will be used as filter."""
    if not self.ctx.game:
        self.output("No game set, cannot determine missing checks.")
        return False
    count = 0
    for loc_id in self.ctx.missing_locations:
        location = LocationData.get_location_name(loc_id)
        if filter_text and filter_text not in location:
            continue
        if loc_id < 0:
            continue
        if loc_id not in self.ctx.locations_checked:
            if loc_id in self.ctx.missing_locations:
                self.output('Missing: ' + location)
                count += 1

    if count:
        self.output(f"Found {count} missing location checks.")
    else:
        self.output("No missing location checks found.")
    return True


def cmd_zones(self):
    """List zones names"""
    if not self.ctx.game:
        self.output("No game set, cannot determine missing checks.")
        return False

    for key, value in zones_dict.items():
        zd: ZoneData = value
        if zd.abrev == "WRP" or zd.abrev == "RWRP" or zd.abrev == "ST0" or zd.abrev == "DRE" or "BO" in zd.abrev:
            continue
        self.output(f'{zd.abrev} - {zd.name}')
