import logging, time, os
from typing import TYPE_CHECKING, NamedTuple
from enum import Enum

from NetUtils import ClientStatus, NetworkItem

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .Locations import ZoneData, LocationData, location_table, get_location_data, zones_dict
from .Items import ItemData, IType, base_item_id


if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")


class STATUS(Enum):
    START = -1
    BIZ_CONNECT = 0
    SERVER_CONNECT = 1
    UNKNOWN = 2
    ON_RICHTER = 3
    ALUCARD_LOAD = 4
    ON_ALUCARD = 5
    RESET = 7


class HEALTH(Enum):
    UNKNOWN = 0
    ALIVE = 1
    DEAD = 2


class SotNClient(BizHawkClient):
    game = "Symphony of the Night"
    system = "PSX"
    patch_suffix = ".apsotn"

    def __init__(self) -> None:
        super().__init__()
        self.checked_locations = list()
        self.sent_checked_locations = list()
        self.missing_command = None
        self.last_zone = ("UNK", "UNKNOWN")
        self.cur_zone = ("UNK", "UNKNOWN")
        self.just_died = False
        self.title_screen = False
        self.dracula_loaded = False
        self.zone_loaded = False
        self.door_patched = False
        self.last_item_received = 0
        self.last_misplaced = 0
        self.misplaced_changed = False
        self.message_queue = []
        self.player_status = STATUS.START
        self.player_health = HEALTH.UNKNOWN
        self.received_queue = []
        self.misplaced_queue = []
        self.misplaced_load = []
        self.last_time = 0
        self.not_patched = True
        self.load_timer = 0
        self.new_items = []
        self.goal_boss = 0
        self.goal_room = 0
        self.goal_complete = False
        self.dracula_dead = False
        self.update_variables = False
        self.received_relics = []
        self.last_owned = []

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
                # This is a MYGAME ROM
                ctx.game = self.game
                ctx.items_handling = 0b101
                ctx.want_slot_data = True
                ctx.command_processor.commands["missing"] = cmd_missing
                ctx.command_processor.commands["zones"] = cmd_zones

                self.player_status = STATUS.BIZ_CONNECT
                return True
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now
        return False

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk.context import AuthStatus

        try:
            # Read save data
            if ctx.auth_status == AuthStatus.AUTHENTICATED:
                zone_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x180000, 2, "MainRAM")]))[0],
                                            "little")
                player_hp = 100
                pause_screen = 0
                if self.player_status == STATUS.ON_ALUCARD or self.player_status == STATUS.ON_RICHTER:
                    local_player_hp = int.from_bytes(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(0x097ba0, 4, "MainRAM")]))[0],"little")
                    pause_screen = int.from_bytes(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(0x09794c, 1, "MainRAM")]))[0], "little")
                    if self.player_health == HEALTH.ALIVE:
                        player_hp = local_player_hp
                    elif self.player_health == HEALTH.UNKNOWN and local_player_hp != 0:
                        self.player_health = HEALTH.ALIVE

                self.cur_zone = (ZoneData.get_zone_data(zone_value)[1].abrev,
                                 ZoneData.get_zone_data(zone_value)[1].name)

                if self.not_patched and (self.player_status == STATUS.ON_RICHTER or
                                         self.player_status == STATUS.ON_ALUCARD):
                    await bizhawk.write(ctx.bizhawk_ctx, [(0x3BDE0, b'\x02', "MainRAM")])
                    self.not_patched = False
                    print("DEBUG: Patch applied")

                if self.player_status == STATUS.BIZ_CONNECT:
                    print("DEBUG: Connect to the server")
                    self.player_status = STATUS.SERVER_CONNECT

                if self.player_status == STATUS.SERVER_CONNECT:
                    if self.cur_zone[0] == "ST0":
                        print("DEBUG: On Richter")
                        self.player_status = STATUS.ON_RICHTER
                        self.title_screen = False
                        # It's a fresh game. Create a misplaced save file
                        # update_variable is set if we died. In case of dying before saving we might lose our
                        # misplaced file
                        if not self.update_variables:
                            filepath = f"{os.getcwd()}\\AP_{ctx.seed_name}_P{ctx.slot}_{ctx.username}.txt"
                            with open(filepath, "w") as stream:
                                stream.write(f"Save file for AP_{ctx.seed_name}_P{ctx.slot}_{ctx.username}\n")

                    if self.cur_zone[0] != "ST0" and self.cur_zone[0] != "UNK":
                        if self.load_timer == 0:
                            self.load_timer = time.time()
                        if (self.player_status != STATUS.ON_ALUCARD and self.load_timer != 0 and
                                time.time() - self.load_timer >= 15):
                            self.player_status = STATUS.ON_ALUCARD
                            self.load_timer = 0
                            self.last_item_received = (
                                int.from_bytes((await bizhawk.read(
                                    ctx.bizhawk_ctx, [(0x03bf04, 2, "MainRAM")]))[0], "little"))
                            self.last_misplaced = (
                                int.from_bytes((await bizhawk.read(
                                    ctx.bizhawk_ctx, [(0x03bf1d, 2, "MainRAM")]))[0], "little"))
                            self.populate_misplaced(ctx)
                            self.checked_locations = []
                            self.checked_locations.extend(list(ctx.checked_locations))
                            self.sent_checked_locations = self.checked_locations[:]
                            self.title_screen = False
                            print(f"DEBUG: On Alucard loaded game {self.last_item_received} / {self.last_misplaced}")

                if self.player_status == STATUS.ON_RICHTER and self.cur_zone[0] != "ST0":
                    self.player_status = STATUS.ALUCARD_LOAD
                    self.load_timer = time.time()
                    self.title_screen = False
                    print(f"DEBUG: On Alucard moat cross")

                if self.player_status == STATUS.ALUCARD_LOAD:
                    if time.time() - self.load_timer >= 15:
                        print("DEBUG: On Alucard fresh game.")
                        self.player_status = STATUS.ON_ALUCARD
                        self.load_timer = 0
                        self.title_screen = False

                if self.cur_zone[0] != "UNK" and not self.just_died and player_hp <= 0:
                    if self.player_status == STATUS.ON_RICHTER or self.player_status == STATUS.ON_ALUCARD:
                        print("DEBUG: Just died!")
                        self.player_status = STATUS.SERVER_CONNECT
                        self.player_health = HEALTH.DEAD
                        self.just_died = True
                        self.dracula_loaded = False
                        self.not_patched = True
                        # We might have died without a save. Flag to read received from the memory
                        self.update_variables = True

                if not self.title_screen and self.just_died and self.cur_zone[0] == "UNK":
                    print(f"DEBUG: At title screen")
                    self.title_screen = True
                    self.player_status = STATUS.SERVER_CONNECT
                    self.player_health = HEALTH.UNKNOWN

                if self.title_screen and self.cur_zone[0] != "UNK":
                    print("DEBUG: Reload game.")
                    self.just_died = False
                    self.title_screen = False
                    if self.cur_zone[0] == "ST0":
                        self.player_status = STATUS.ON_RICHTER
                    else:
                        self.player_status = STATUS.ON_ALUCARD
                        self.update_variables = True

                if not self.dracula_loaded and not self.just_died and self.cur_zone[0] == "RBO6":
                    read_result = await bizhawk.guarded_read(
                        ctx.bizhawk_ctx,
                        [(0x076ed6, 2, "MainRAM")],
                        [(0x076ed6, b'\x10\x27', "MainRAM")])

                    if read_result is not None:
                        self.dracula_loaded = True
                        print(f"DEBUG: Dracula loaded")

                if not self.just_died and not self.dracula_dead and self.dracula_loaded:
                    dracula_hp = int.from_bytes(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(0x076ed6, 2, "MainRAM")]))[0], "little")
                    if dracula_hp == 0 or dracula_hp > 60000:
                        print("DEBUG: Dracula dead")
                        self.dracula_dead = True
                        if not ctx.finished_game:
                            ctx.finished_game = True
                            await ctx.send_msgs([{
                                "cmd": "StatusUpdate",
                                "status": ClientStatus.CLIENT_GOAL
                            }])

                if not self.zone_loaded and self.load_timer != 0 and self.cur_zone[0] == "RNO0":
                    # Give 20 seconds to assure zone is loaded
                    if time.time() - self.load_timer >= 20:
                        print(f"DEBUG: Zone loaded {self.load_timer} / {time.time()}")
                        self.goal_boss = (int.from_bytes((await bizhawk.read
                        (ctx.bizhawk_ctx, [(0x180f8b, 1, "MainRAM")]))[0], "little"))
                        self.goal_room = (int.from_bytes((await bizhawk.read
                        (ctx.bizhawk_ctx, [(0x180f89, 2, "MainRAM")]))[0], "little"))
                        goal = self.check_completion()
                        logger.info(
                            f"Secondary goal: {self.goal_boss} Boss tokens / {self.goal_room} Rooms explored")
                        logger.info(f"Total: {goal[0]} / {goal[1]}")
                        self.zone_loaded = True
                        self.load_timer = 0
                        if goal[0] >= self.goal_boss and goal[1] >= self.goal_room:
                            print("DEBUG: Secondary goal completed")
                            self.goal_complete = True
                        else:
                            print("DEBUG: Goal not completed")

                if self.cur_zone[0] == "RNO0" and self.zone_loaded and self.goal_complete and not self.door_patched:
                    first_patch = False
                    write_result: bool = await bizhawk.guarded_write(
                        ctx.bizhawk_ctx,
                        [(0x001c132c, [0x18, 0x01, 0x40, 0x14], "System Bus")],
                        [(0x001c132c, [0x18, 0x01, 0x00, 0x10], "System Bus")]
                    )
                    if write_result:
                        print("DEBUG: Instruction patched at 0x001c132c")
                        logger.info("Instruction patched at 0x001c132c")
                        self.door_patched = True
                        first_patch = True
                    else:
                        print(f"DEBUG: Error could not found instruction at 001c132c")
                        logger.info("ERROR could not found instruction at 0x001c132c")

                    write_result = await bizhawk.guarded_write(
                            ctx.bizhawk_ctx,
                            [(0x801c132c, [0x18, 0x01, 0x40, 0x14], "System Bus")],
                            [(0x801c132c, [0x18, 0x01, 0x00, 0x10], "System Bus")]
                        )
                    if write_result:
                        print("DEBUG: Instruction patched at 0x801c132c")
                        logger.info("Instruction patched at 0x801c132c")
                        self.door_patched = True
                    else:
                        if not first_patch:
                            print("DEBUG: Error could not found instruction at 0x801c132c")
                            logger.info("ERROR could not found instruction at 0x801c132c")

                if self.last_zone != self.cur_zone:
                    if self.cur_zone[0] == "UNK" and self.last_zone[0] != "BO6":
                        if self.player_status == STATUS.ON_ALUCARD or self.player_status == STATUS.ON_RICHTER:
                            print(f"DEBUG: Reset detected")
                            self.player_status = STATUS.SERVER_CONNECT
                            self.player_health = HEALTH.UNKNOWN
                            self.load_timer = 0
                            self.last_time = 0
                    else:
                        if self.cur_zone[0] == "RNO0" and self.last_zone[0] != "RNO0":
                            print(f"DEBUG: Entered RNO0")
                            self.load_timer = time.time()
                            self.zone_loaded = False
                        if self.last_zone[0] == "RNO0" and self.cur_zone[0] != "RNO0":
                            # We left Black Marble Gallery reset variables
                            print("DEBUG: Left RNO0")
                            self.door_patched = False
                            self.zone_loaded = False
                        print(f"DEBUG: {self.cur_zone[0]} - {self.cur_zone[1]}")
                    self.last_zone = self.cur_zone

                if self.player_status == STATUS.ON_ALUCARD:
                    if self.update_variables:
                        self.last_item_received = (
                            int.from_bytes((await bizhawk.read(
                                ctx.bizhawk_ctx, [(0x03bf04, 2, "MainRAM")]))[0], "little"))
                        self.last_misplaced = (
                            int.from_bytes((await bizhawk.read(
                                ctx.bizhawk_ctx, [(0x03bf1d, 2, "MainRAM")]))[0], "little"))

                    if self.cur_zone[0] not in ["UNK", "ST0", "RCEN", "RBO6"]:
                        await self.process_locations(ctx)
                    if self.last_misplaced < len(self.misplaced_load):
                        for i, misplaced in enumerate(self.misplaced_load):
                            if self.last_misplaced < i + 1:
                                misplaced_item = ItemData.get_item_info(int(misplaced))
                                print(f"{misplaced_item[0]} from load added to queue. Last: {self.last_misplaced}")
                                self.misplaced_queue.append(misplaced_item[1])
                                self.last_misplaced = i + 1
                        await bizhawk.write(
                                ctx.bizhawk_ctx, [(0x03bf1d, self.last_misplaced.to_bytes(2, "little"), "MainRAM")])
                    if pause_screen == 2:
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
                            print("DEBUG: New items added. Sort inventory!")
                            await bizhawk.lock(ctx.bizhawk_ctx)
                            await self.sort_inventory(ctx)
                            await bizhawk.unlock(ctx.bizhawk_ctx)
                            self.new_items = []

                    # Check game_time
                    time_now = await bizhawk.read(ctx.bizhawk_ctx, [(0x097c30, 12, "MainRAM")])
                    cur_time = list(bytes(time_now[0]))
                    hour_now = cur_time[0] * 3600
                    min_now = cur_time[4] * 60
                    sec_now = cur_time[8]
                    now = hour_now + min_now + sec_now

                    if ((self.cur_zone[0] != "UNK" and self.last_time != 0 and self.last_time - now > 2) or
                            (self.player_health == HEALTH.DEAD and self.cur_zone[0] != "UNK")):
                        print(f"DEBUG: Load state! {self.last_time} / {now}")
                        self.last_item_received = (
                            int.from_bytes((await bizhawk.read(
                                ctx.bizhawk_ctx, [(0x03bf04, 2, "MainRAM")]))[0], "little"))
                        self.last_misplaced = (
                            int.from_bytes((await bizhawk.read(
                                ctx.bizhawk_ctx, [(0x03bf1d, 2, "MainRAM")]))[0], "little"))
                        self.populate_misplaced(ctx)
                    self.last_time = now
                    self.just_died = False

                    if self.misplaced_changed:
                        print("DEBUG: Misplaced changed")
                        await bizhawk.write(ctx.bizhawk_ctx,
                                            [(0x03bf1d, self.last_misplaced.to_bytes(2, "little"), "MainRAM")])
                        self.misplaced_changed = False

                    # Did we have received items
                    for i, item_received in enumerate(ctx.items_received):
                        if i + 1 > self.last_item_received:
                            received = ItemData.get_item_info(item_received.item)
                            self.received_queue.append(received[1])
                            self.message_queue.append(f"Granted: {received[0]}")
                            self.last_item_received = i + 1
                            await bizhawk.write(
                                ctx.bizhawk_ctx, [(0x03bf04, self.last_item_received.to_bytes(2, "little"), "MainRAM")])

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            print("ERROR")
            pass

    def on_package(self, ctx, cmd, args):
        if cmd == "PrintJSON":
            if 'item' in args:
                message_type: NamedTuple = args['type']  # PrintJsonType of this message (optional)
                player: NamedTuple = args['receiving']  # Destination player's ID
                received: NetworkItem = args['item']  # Source player's ID, location ID, item ID and item flags
                data: NamedTuple = args['data']  # Textual content of this message

                print(f"Type: {message_type} Player: {player} Received: {received} Data: {data}")
                print(ctx.slot_data)
                print(ctx.slot)
                print(data[0]['text'])
                print(type(data[0]['text']))
                if received.location == 127083080 or received.location == 127020003:
                    if int(data[0]['text']) == ctx.slot:
                        # Holy glasses and CAT - Mormegil, send a library card, so player won't get stuck
                        # If there are 2 SOTN players at the same time, both might receive a free library card
                        library_card = ItemData.get_item_info(166 + base_item_id)
                        self.misplaced_queue.append(library_card[1])
                        print("DEBUG: Sending Library Card")

                if message_type == "ItemSend" and ctx.slot == player:
                    print(f"DEBUG: Inside {ctx.slot} / {player}")
                    print(f"DEBUG: Inside 2 {type(ctx.slot)} / {type(player)}")
                    if base_item_id <= received.item <= base_item_id + 423:
                        # Check if the item came from offworld
                        if base_item_id <= received.location <= base_item_id + 310024:
                            loc_data: LocationData = get_location_data(received.location)
                        else:
                            loc_data = None

                        item_data = ItemData.get_item_info(received.item)

                        # Is a exploration item?
                        if 127110031 <= received.location <= 127110050:
                            self.message_queue.append(f"Exploration item: {item_data[0]}")
                            self.misplaced_queue.append(item_data[1])
                            self.add_misplaced(ctx, item_data[1].index)
                            self.last_misplaced += 1
                            self.misplaced_changed = True
                            print("DEBUG: Exploration item")

                        if loc_data is not None:
                            if loc_data.can_be_relic:
                                # Item on a relic spot,  only bat card, skill of wolf, jewel of open and relics of vlad
                                if loc_data.game_id in [3074, 3141, 3142, 3211, 3221, 3252, 3261, 3305]:
                                    if item_data[1].type != IType.RELIC:
                                        self.message_queue.append(f"Misplaced item: {item_data[0]}")
                                        self.misplaced_queue.append(item_data[1])
                                        self.add_misplaced(ctx, item_data[1].index)
                                        self.last_misplaced += 1
                                        self.misplaced_changed = True
                            else:
                                # Normal location containing a relic
                                if item_data[1].type == IType.RELIC:
                                    self.message_queue.append(f"Misplaced relic: {item_data[0]}")
                                    self.misplaced_queue.append(item_data[1])
                                    self.add_misplaced(ctx, item_data[1].index)
                                    self.last_misplaced += 1
                                    self.misplaced_changed = True
        elif cmd == "RoomInfo":
            ctx.seed_name = args['seed_name']

        super().on_package(ctx, cmd, args)

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
                        (v.zone == "Catacombs" and zone_data.name == "Legion") or
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
                                print(f"DEBUG: New check {k}")
                                self.checked_locations.append(v.get_location_id())
                    else:
                        await self.process_extra_locations(ctx, v.game_id, zone_data.abrev)

            if self.checked_locations != self.sent_checked_locations:
                print("DEBUG: Sending new check")
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
                check.append(("boss", "CAT - Legion kill", 0x03ca34))

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
                check.append(("wall", "NO1 - Pot Roast", 0x03bdfe, 0))
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
                check.append(("wall", "NO3 - Pot Roast", 0x03be1f, 0))
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
                check.append(("relic", "Fire of Bat", 10, zones_dict[15].loot_flag, zones_dict[15].loot_size, 12,
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
                check.append(("wall", "RNZ1 - Turkey", 0x03be97, 0))
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
                                print("DEBUG: Checked by item")
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

    async def check_relic(self, owned: list) -> bool:
        owned_list = list(bytes(owned[0]))

        if self.last_owned:
            for i in range(30):
                if owned_list[i] != self.last_owned[i] and self.last_owned[i] == 0:
                    # Did we just receive a relic?
                    print(f"DEBUG: Testing relic {i}")
                    for relic in self.received_relics:
                        relic_index = 300 + i
                        print(f"DEBUG: Relic testing {i}/{relic_index}/{relic}")
                        if i > 22:
                            relic_index = 300 + i + 2
                        if relic_index == relic:
                            continue
                    print(f"DEBUG: Relic changed in {i}")
                    self.last_owned = owned_list
                    return True

        self.last_owned = owned_list
        return False

    def add_misplaced(self, ctx: "BizHawkClientContext", item_id: int):
        filename = f"{os.getcwd()}\\AP_{ctx.seed_name}_P{ctx.slot}_{ctx.username}.txt"

        print(f"Added misplaced {item_id}")
        # Add to file and list
        self.misplaced_load.append(item_id)
        with open(filename, "a") as stream:
            stream.write(f"{item_id}\n")

    def populate_misplaced(self, ctx: "BizHawkClientContext"):
        filename = f"{os.getcwd()}\\AP_{ctx.seed_name}_P{ctx.slot}_{ctx.username}.txt"
        self.misplaced_load = []

        if not os.path.exists(filename):
            with open(filename, "w") as stream:
                stream.write(f"Save file for AP_{ctx.seed_name}_P{ctx.slot}_{ctx.username}\n")

        with open(filename, "r") as stream:
            next(stream)
            for line in stream:
                self.misplaced_load.append(line)
                print(f"DEBUG: Added line {line}")

    async def grant_item(self, item: ItemData, ctx: "BizHawkClientContext"):
        item_id = item.index - base_item_id
        address = item.address

        print(f"DEBUG: grant_item-> {item_id} : {address}")

        if 300 <= item_id < 400:
            relic = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address, 1, "MainRAM")]))[0], "little")
            self.received_relics.append(item_id)

            if relic == 0 or relic == 2 or relic > 3:
                if 318 <= item_id <= 322:
                    await bizhawk.write(ctx.bizhawk_ctx, [(address, b'\x01', "MainRAM")])
                else:
                    await bizhawk.write(ctx.bizhawk_ctx, [(address, b'\x03', "MainRAM")])
            owned_relics = await bizhawk.read(ctx.bizhawk_ctx, [(0x097964, 30, "MainRAM")])
            owned_list = list(bytes(owned_relics[0]))
            self.last_owned = owned_list
            print("Relic granted")
        elif item_id == 412:
            cur_heart = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address, 4, "MainRAM")]))[0], "little")
            max_heart = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address + 4, 4, "MainRAM")]))[0],
                                       "little")
            cur_heart += 5
            max_heart += 5
            await bizhawk.write(ctx.bizhawk_ctx, [(address, cur_heart.to_bytes(4, "little"), "MainRAM")])
            await bizhawk.write(ctx.bizhawk_ctx, [(address + 4, max_heart.to_bytes(4, "little"), "MainRAM")])
            print("Hearth Vessel granted")
        elif item_id == 423:
            max_hp = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address + 4, 4, "MainRAM")]))[0], "little")
            max_hp += 5
            await bizhawk.write(ctx.bizhawk_ctx, [(address, max_hp.to_bytes(4, "little"), "MainRAM")])
            await bizhawk.write(ctx.bizhawk_ctx, [(address + 4, max_hp.to_bytes(4, "little"), "MainRAM")])
            print("Life Vessel granted")
        else:
            qty = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address, 1, "MainRAM")]))[0], "little")

            if qty < 255:
                qty += 1
            # First item, sort the inventory
            if qty == 1:
                self.new_items.append(item_id)
            else:
                await bizhawk.write(ctx.bizhawk_ctx, [(address, qty.to_bytes(1, "little"), "MainRAM")])

    async def sort_inventory(self, ctx: "BizHawkClientContext"):
        print(f"DEBUG: Sorting inventory - {self.new_items}")
        # Inventory: 0x097a8e - 0x097b8e
        # Quantity: 0x09798b - 0x097a8b
        inventory = await bizhawk.read(ctx.bizhawk_ctx, [(0x097a8e, 258, "MainRAM")])
        quantity = await bizhawk.read(ctx.bizhawk_ctx, [(0x09798b, 258, "MainRAM")])
        inv_list = list(bytes(inventory[0]))
        qty_list = list(bytes(quantity[0]))

        for item in self.new_items:
            print(f"Sorting {item}")
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
                    print(f"DEBUG: {old_item} Free found at {i} for {item}")
                    for k in range(offset, 259, 1):
                        if inv_list[k] == item - offset + start_byte:
                            inv_list[i] = item - offset + start_byte
                            qty_list[item - 1] = 1
                            inv_list[k] = old_item
                            break
                    break

        await bizhawk.write(ctx.bizhawk_ctx, [(0x097a8e, bytes(inv_list), "MainRAM")])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x09798b, bytes(qty_list), "MainRAM")])

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
                print(f"DEBUG: Boss: {loc} found")
                total_bosses += 1
                bosses.remove(loc)
            if 127110011 <= loc <= 127110030:
                print(f"DEBUG: Exploration: {loc} found")
                total_exp += 1

        return total_bosses, exploration[total_exp - 1]


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