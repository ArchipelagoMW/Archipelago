import logging, os
import worlds._bizhawk as bizhawk
import struct
from worlds._bizhawk.client import BizHawkClient
from typing import TYPE_CHECKING
from enum import Flag
from NetUtils import ClientStatus
from collections import namedtuple
from Utils import messagebox, user_path
from pathlib import Path


from .Items import items, id_to_item, base_item_id
from .data.Zones import zones, AREA_FLAG_TO_ZONE
from .Locations import ZONE_LOCATIONS, BREAKABLE_LOCATIONS, locations, AP_ID_TO_NAME

# TODO:
#  Visual glitches on Richter dialog
#  Visual glitch on sliding door after defeating Lesser Demon

# Ideas:
# Check seed before sending checks
# Lock red doors for progression
# Chairsanity
# Enemysanity need faerie scroll -Seraphin Eveles Patch bestiality
# # No-logic rules


if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
else:
    BizHawkClientContext = object

logger = logging.getLogger("Client")

item_id_to_name = {value["id"]: key for key, value in items.items()}
Seed = namedtuple("Seed", ["file_name", "sanity", "goal", "bosses", "exp", "talisman", "total_tal"])

ITEM_SAVE = 0x03bf04


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
        self.cur_zone = None
        self.last_zone = None
        self.load_once = False
        self.last_item_received = 0
        self.new_items = []
        self.received_relics = []
        self.relic_placement = []
        self.breakable_items = {}
        self.jewel_item_qty = -1
        self.message_queue = []
        self.received_queue = []
        self.goal_diplayed = False
        self.applied_axe = 0
        self.player_name = None

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

                if read_result2[0].hex() != b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'.hex():
                    # First Maria Meeting
                    # 26 49 52 53 54 00 2d 41 52 49 47 00
                    if read_result2[0].hex() == b'\x26\x49\x52\x53\x54\x00\x2d\x41\x52\x49\x47\x00'.hex():
                        # Vanilla ROM
                        messagebox("Error", "Looks like a vanilla ROM is loaded!", error=True)
                        return False
                    else:
                        ctx.game = self.game
                        ctx.items_handling = 0b101
                        ctx.want_slot_data = True
                        ctx.command_processor.commands["missing"] = cmd_missing
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
                room_id = (await bizhawk.read(ctx.bizhawk_ctx, [(0x73084, 2, "MainRAM")]))[0]
                area_value = (await bizhawk.read(ctx.bizhawk_ctx, [(0x03c774, 2, "MainRAM")]))[0]
                entered_cutscene = (await bizhawk.read(ctx.bizhawk_ctx, [(0x03be20, 1, "MainRAM")]))[0]

                dracula_dead = False

                try:
                    temp_zone = self.cur_zone
                    cur_area = struct.unpack("<H", area_value)[0]
                    self.cur_zone = AREA_FLAG_TO_ZONE[cur_area]
                    self.last_zone = temp_zone
                except KeyError:
                    self.cur_zone = None

                if self.cur_zone and entered_cutscene == b'\x01':
                    if not self.load_once:
                        self.load_once = True
                        self.checked_locations = []
                        self.checked_locations.extend(list(ctx.checked_locations))
                        self.sent_checked_locations = self.checked_locations[:]
                        await self.populate_once(ctx)

                    game_state_flag = (await bizhawk.read(ctx.bizhawk_ctx, [(0x03c9a4, 1, "MainRAM")]))[0]
                    pause_screen = (await bizhawk.read(ctx.bizhawk_ctx, [(0x09794c, 1, "MainRAM")]))[0]
                    # Process items
                    try:
                        loot_flag = await self.read_int(ctx, self.cur_zone["loot_flag"], self.cur_zone["loot_size"],
                                                        "MainRAM")
                    except KeyError:
                        # We are at an WRP zone?
                        loot_flag = None

                    try:
                        cur_locations = ZONE_LOCATIONS[self.cur_zone["zone"]]
                    except KeyError:
                        # Zone without locations
                        cur_locations = []

                    # Are our variables update?
                    cur_last_item_received = await self.read_int(ctx, ITEM_SAVE, 2, "MainRAM")
                    if cur_last_item_received != self.last_item_received:
                        print("Last item received changed. Did we died or load state?")
                        self.last_item_received = cur_last_item_received

                    # Are we fighting Dracula
                    if self.cur_zone["name"] == "Shaft/Dracula":
                        dracula_hp = await self.read_int(ctx, 0x076ed6, 2, "MainRAM")
                        if dracula_hp == 0 or dracula_hp > 60000:
                            dracula_dead = True

                    # Are we safe to process items?
                    if pause_screen != b'\x00' and game_state_flag == b'\x01':
                        # Process Queues
                        if self.message_queue:
                            for _ in self.message_queue:
                                await bizhawk.display_message(ctx.bizhawk_ctx, self.message_queue.pop())
                        if self.received_queue:
                            for _ in self.received_queue:
                                await self.grant_item(id_to_item[self.received_queue.pop()], ctx)
                        if self.new_items:
                            await bizhawk.lock(ctx.bizhawk_ctx)
                            await self.sort_inventory(ctx)
                            await bizhawk.unlock(ctx.bizhawk_ctx)
                            self.new_items = []

                        # Did we receive and item?
                        for i, item_received in enumerate(ctx.items_received):
                            if i + 1 > self.last_item_received:
                                self.received_queue.append(item_received.item)
                                self.message_queue.append(f"Granted: {item_id_to_name[item_received.item]}")
                                self.last_item_received = i + 1
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(ITEM_SAVE, self.last_item_received.to_bytes(2, "little"), "MainRAM")])

                    for location in cur_locations:
                        for name, loc in location.items():
                            if loc["ap_id"] + base_item_id in self.checked_locations:
                                continue

                            # Did we change area during location loop?
                            cur_area = (await bizhawk.read(ctx.bizhawk_ctx, [(0x03c774, 2, "MainRAM")]))[0]
                            if cur_area != area_value:
                                continue

                            if "bin_addresses" in loc:
                                break_flag = await self.read_int(ctx, loc["break_flag"], 1, "MainRAM")
                                if break_flag & loc["break_mask"]:
                                    self.checked_locations.append(loc["ap_id"] + base_item_id)
                            elif "kill_time" in loc:
                                kill_time = await self.read_int(ctx, loc["kill_time"], 2, "MainRAM")
                                if kill_time != 0:
                                    self.checked_locations.append(loc["ap_id"] + base_item_id)
                            elif loc["vanilla_item"] == "Jewel of open":
                                jewel_item = (await bizhawk.read(ctx.bizhawk_ctx, [(0x0dfd42, 2, "MainRAM")]))[0]
                                jewel_item = int.from_bytes(jewel_item)

                                if jewel_item <= 257:
                                    item_data = id_to_item[jewel_item]
                                    item_qty = await self.read_int(ctx, item_data["address"], 1, "MainRAM")
                                    if self.jewel_item_qty == -1:
                                        self.jewel_item_qty = item_qty
                                    if item_qty > self.jewel_item_qty:
                                        # Assume we bought item on librarian
                                        self.checked_locations.append(loc["ap_id"] + base_item_id)
                                elif 300 <= jewel_item <= 329:
                                    relic_to_check = jewel_item - 300
                                    if await self.check_relic(relic_to_check, ctx):
                                        # Assume we bought the relic
                                        self.checked_locations.append(loc["ap_id"] + base_item_id)
                            elif loc["vanilla_item"] == "Holy glasses":
                                break_flag = await self.read_int(ctx, loc["break_flag"], 1, "MainRAM")
                                if break_flag & loc["break_mask"]:
                                    self.checked_locations.append(loc["ap_id"] + base_item_id)
                            elif loc["ap_id"] in self.relic_placement:
                                # This location is a relic?
                                relic_to_check = self.relic_placement.index(loc["ap_id"])
                                if await self.check_relic(relic_to_check, ctx):
                                    self.checked_locations.append(loc["ap_id"] + base_item_id)
                            else:
                                if loot_flag & (1 << loc["index"]):
                                    self.checked_locations.append(loc["ap_id"] + base_item_id)

                    if self.checked_locations != self.sent_checked_locations:
                        self.sent_checked_locations = self.checked_locations[:]

                        if self.sent_checked_locations is not None:
                            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": self.sent_checked_locations}])

                    # Did we kill dracula?
                    if not ctx.finished_game:
                        if dracula_dead:
                            await self.send_client_goal(ctx)

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            print("ERROR")
            pass

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

    async def populate_once(self, ctx: "BizHawkClientContext") -> None:
        # Read relic placement on the ROM
        relic_placement = (await bizhawk.read(ctx.bizhawk_ctx, [(0x0dfd10, 22, "MainRAM")]))[0]
        placement_list = list(relic_placement)

        # Def Dopp10
        for i in range(0, len(placement_list), 2):
            value = (placement_list[i] << 8) + placement_list[i+1]
            self.relic_placement.append(value)

        relic_placement = (await bizhawk.read(ctx.bizhawk_ctx, [(0x0dfd28, 14, "MainRAM")]))[0]
        placement_list = list(relic_placement)

        # Def Olroxx
        for i in range(0, len(placement_list), 2):
            value = (placement_list[i] << 8) + placement_list[i + 1]
            self.relic_placement.append(value)

        relic_placement = (await bizhawk.read(ctx.bizhawk_ctx, [(0x0dfd38, 24, "MainRAM")]))[0]
        placement_list = list(relic_placement)

        # Def Dracula
        for i in range(0, len(placement_list), 2):
            value = (placement_list[i] << 8) + placement_list[i + 1]
            self.relic_placement.append(value)

        # Non-used relic slots
        self.relic_placement[23] = -1
        self.relic_placement[24] = -1

        # Breakable locations
        for k, v in BREAKABLE_LOCATIONS.items():
            item = (await bizhawk.read(ctx.bizhawk_ctx, [(v["rom_address"], 2, "MainRAM")]))[0]
            item_list = list(item)
            item_id = (item_list[0] << 8) + item_list[1]
            self.breakable_items[k] = item_id

        # Break RCHI - Demon wall 03be45
        await bizhawk.write(ctx.bizhawk_ctx, [(0x03be45, b'\x01', "MainRAM")])

        # Check all locations
        region_loot = {}
        for k, v in locations.items():
            if v["zones"][0] in region_loot:
                loot_flag = region_loot[v["zones"][0]]
            else:
                region = zones[v["zones"][0]]
                loot_flag = await self.read_int(ctx, region["loot_flag"], region["loot_size"], "MainRAM")
                region_loot[v["zones"][0]] = loot_flag

            if v["ap_id"] + base_item_id not in self.checked_locations:
                if "bin_addresses" in v:
                    # Breakable without a relic
                    if v["ap_id"] not in self.relic_placement:
                        break_flag = await self.read_int(ctx, v["break_flag"], 1, "MainRAM")
                        if break_flag & v["break_mask"]:
                            self.checked_locations.append(v["ap_id"] + base_item_id)
                            # Do we need to grant a powerup to player?
                            item = self.breakable_items[k]
                            if item == 412:
                                await self.grant_item(items["Heart Vessel"], ctx)
                            elif item == 423:
                                await self.grant_item(items["Life Vessel"], ctx)
                elif "kill_time" in v:
                    kill_time = await self.read_int(ctx, v["kill_time"], 2, "MainRAM")
                    if kill_time != 0:
                        self.checked_locations.append(v["ap_id"] + base_item_id)
                elif v["vanilla_item"] == "Jewel of open":
                    # We could test for relic, but item would be hard. Ignore for now
                    pass
                elif v["vanilla_item"] == "Holy glasses":
                    break_flag = await self.read_int(ctx, v["break_flag"], 1, "MainRAM")
                    if break_flag & v["break_mask"]:
                        self.checked_locations.append(v["ap_id"] + base_item_id)
                elif v["ap_id"] in self.relic_placement:
                    owned_relics = list(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(0x097964, 30, "MainRAM")]))[0])
                    i = self.relic_placement.index(v["ap_id"])
                    if owned_relics[i] != 0:
                        # We already got a relic that was in this location
                        self.checked_locations.append(v["ap_id"] + base_item_id)
                else:
                    if loot_flag & (1 << v["index"]):
                        self.checked_locations.append(v["ap_id"] + base_item_id)

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
        ctx.auth = utf_name

        # logger.info(f"Running ROM seed: {seed} for player: {utf_name}")
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
        # logger.info(f"Goal: {goal_str}")
        if goal == 3 or goal == 5:
            rooms = int((exp * 10) / 0.107)
            # logger.info(f"Bosses: {bosses} / Exploration: {exp} -> {rooms} rooms")
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

    async def grant_item(self, item: dict, ctx: "BizHawkClientContext"):
        item_id = item["id"]
        address = item["address"]

        # TODO Boosts and traps
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
        # Relics
        elif 300 <= item_id <= 329:
            relic = await self.read_int(ctx, address, 1, "MainRAM")
            if relic == 0:
                if 318 <= item_id <= 322:
                    await bizhawk.write(ctx.bizhawk_ctx, [(address, b'\x01', "MainRAM")])
                else:
                    await bizhawk.write(ctx.bizhawk_ctx, [(address, b'\x03', "MainRAM")])
        # Heart Vessel
        elif item_id == 412:
            cur_heart = await self.read_int(ctx, address, 4, "MainRAM")
            max_heart = await self.read_int(ctx, address + 4, 4, "MainRAM")
            cur_heart += 5
            max_heart += 5
            await bizhawk.write(ctx.bizhawk_ctx, [(address, cur_heart.to_bytes(4, "little"), "MainRAM")])
            await bizhawk.write(ctx.bizhawk_ctx, [(address + 4, max_heart.to_bytes(4, "little"), "MainRAM")])
        # Life Vessel
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

    async def check_relic(self, relic_id: int, ctx: "BizHawkClientContext") -> bool:
        # Relic start address 0x097964
        relic = await self.read_int(ctx, 0x097964 + relic_id, 1, "MainRAM")

        if relic == 1 or relic == 3:
            return True

        return False

    async def safe_axe_lord(self, ctx: "BizHawkClientContext") -> bool:
        pausable = await self.read_int(ctx, 0x3c8b8, 1, "MainRAM")
        cutscene_flag = await self.read_int(ctx, 0x72efc, 1, "MainRAM")

        if pausable == 1 and cutscene_flag == 0:
            return True
        else:
            return False


def cmd_missing(self, filter_text="") -> bool:
    # List all missing location checks, from your local game state.
    # Can be given text, which will be used as filter.
    if not self.ctx.game:
        self.output("No game set, cannot determine missing checks.")
        return False
    count = 0
    for loc_id in self.ctx.missing_locations:
        location = AP_ID_TO_NAME[loc_id]
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
