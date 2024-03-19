import logging, time, os
from typing import TYPE_CHECKING, NamedTuple
from enum import Enum

from NetUtils import ClientStatus, NetworkItem

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .Locations import ZoneData, LocationData, location_table, get_location_data
from .Items import ItemData, IType, base_item_id
from .Rom import pos_patch


if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

EXPECTED_ROM_NAME = "Castlevania"
logger = logging.getLogger("Client")


class STATUS(Enum):
    START = -1
    BIZ_CONNECT = 0
    SERVER_CONNECT = 1
    UNKNOWN = 2
    ON_RICHTER = 3
    ALUCARD_LOAD = 4
    ON_ALUCARD = 5
    DEAD = 6


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
        self.last_item_received = 0
        self.last_misplaced = 0
        self.message_queue = []
        self.player_status = STATUS.START
        self.received_queue = []
        self.misplaced_queue = []
        self.misplaced_load = []
        self.last_time = 0
        self.not_patched = True
        self.load_timer = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x0de19c, 11, "MainRAM")]))[0]).decode("ascii")

            if rom_name != EXPECTED_ROM_NAME:
                logger.info("Unexpected read value")
                return False  # Not a MYGAME ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        # This is a MYGAME ROM
        ctx.game = self.game
        ctx.items_handling = 0b101
        ctx.want_slot_data = True
        ctx.command_processor.commands["missing"] = cmd_missing
        ctx.command_processor.commands["patch"] = cmd_patch

        self.player_status = STATUS.BIZ_CONNECT

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        from worlds._bizhawk.context import AuthStatus

        try:
            # Read save data
            if ctx.auth_status == AuthStatus.AUTHENTICATED:
                zone_value = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x180000, 2, "MainRAM")]))[0],
                                            "little")
                player_hp = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x097ba0, 4, "MainRAM")]))[0],
                                           "little")
                pause_screen = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(0x09794c, 1, "MainRAM")]))[0], "little")
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
                        # It's a fresh game. Create a misplaced save file
                        filepath = f"{os.getcwd()}\\AP_{ctx.seed_name}_P{ctx.slot}_{ctx.username}.txt"
                        with open(filepath, "w") as stream:
                            stream.write(f"Save file for AP_{ctx.seed_name}_P{ctx.slot}_{ctx.username}\n")

                    if self.cur_zone[0] != "ST0" and self.cur_zone[0] != "UNK":
                        self.player_status = STATUS.ON_ALUCARD
                        self.last_item_received = (
                            int.from_bytes((await bizhawk.read(
                                ctx.bizhawk_ctx, [(0x03bf04, 2, "MainRAM")]))[0], "little"))
                        self.last_misplaced = (
                            int.from_bytes((await bizhawk.read(
                                ctx.bizhawk_ctx, [(0x03bf1d, 2, "MainRAM")]))[0], "little"))
                        self.populate_misplaced(ctx)
                        print(f"DEBUG: On Alucard loaded game {self.last_item_received} / {self.last_misplaced}")

                if self.player_status == STATUS.ON_RICHTER and self.cur_zone[0] != "ST0":
                    self.player_status = STATUS.ALUCARD_LOAD
                    self.load_timer = time.time()
                    print(f"DEBUG: On Alucard moat cross")

                if self.player_status == STATUS.ALUCARD_LOAD:
                    if time.time() - self.load_timer >= 15:
                        print("DEBUG: On Alucard fresh game.")
                        self.player_status = STATUS.ON_ALUCARD

                if self.just_died and player_hp <= 0:
                    print("DEBUG: Just died!")
                    self.player_status = STATUS.DEAD
                    self.just_died = True
                    self.dracula_loaded = False

                if self.just_died and self.cur_zone[0] == "UNK":
                    print(f"DEBUG: At title screen {self.just_died}")
                    self.title_screen = True

                if self.title_screen and self.cur_zone[0] != "UNK":
                    print("DEBUG: Reload. TODO: update variables")
                    self.just_died = False
                    self.title_screen = False
                    if self.cur_zone[0] == "ST0":
                        self.player_status = STATUS.ON_RICHTER
                    else:
                        self.player_status = STATUS.ON_ALUCARD
                        self.last_item_received = (
                            int.from_bytes((await bizhawk.read(
                                ctx.bizhawk_ctx, [(0x03bf04, 2, "MainRAM")]))[0], "little"))

                if not self.dracula_loaded and not self.just_died and self.cur_zone[0] == "RBO6":
                    read_result = await bizhawk.guarded_read(
                        ctx.bizhawk_ctx,
                        [(0x076ed6, 2, "MainRAM")],
                        [(0x076ed6, b'\x10\x27', "MainRAM")])

                    if read_result is not None:
                        self.dracula_loaded = True
                        print(f"DEBUG: Dracula loaded: {read_result}")

                if not self.just_died and self.dracula_loaded:
                    dracula_hp = int.from_bytes(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(0x076ed6, 2, "MainRAM")]))[0], "little")
                    if dracula_hp == 0:
                        print("DEBUG: Dracula dead")
                        if not ctx.finished_game:
                            await ctx.send_msgs([{
                                "cmd": "StatusUpdate",
                                "status": ClientStatus.CLIENT_GOAL
                            }])

                if self.last_zone != self.cur_zone:
                    print(f"DEBUG: {self.cur_zone[0]} - {self.cur_zone[1]}")
                    self.last_zone = self.cur_zone

                if self.player_status == STATUS.ON_ALUCARD:
                    if self.cur_zone[0] not in ["UNK", "ST0", "RCEN", "RBO6"]:
                        await self.process_locations(ctx)
                    if self.last_misplaced < len(self.misplaced_load):
                        print(f"{self.last_misplaced} < {len(self.misplaced_load)}")
                        for i, misplaced in enumerate(self.misplaced_load):
                            if self.last_misplaced < i + 1:
                                misplaced_item = ItemData.get_item_info(int(misplaced))
                                print(f"{misplaced_item[0]} from load added to queue")
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
                            await grant_item(self.received_queue.pop(), ctx)
                    if self.misplaced_queue:
                        for _ in self.misplaced_queue:
                            await grant_item(self.misplaced_queue.pop(), ctx)

                    # Check game_time
                    hour_now = int.from_bytes(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(0x097c30, 4, "MainRAM")]))[0], "little")
                    min_now = int.from_bytes(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(0x097c34, 4, "MainRAM")]))[0], "little")
                    sec_now = int.from_bytes(
                        (await bizhawk.read(ctx.bizhawk_ctx, [(0x097c38, 4, "MainRAM")]))[0], "little")
                    now = ((60 * hour_now) + min_now) * 60 + sec_now

                    if self.last_time != 0 and self.last_time - now > 10:
                        print(f"Load state! {self.last_time} / {now}")
                        self.last_item_received = (
                            int.from_bytes((await bizhawk.read(
                                ctx.bizhawk_ctx, [(0x03bf04, 2, "MainRAM")]))[0], "little"))
                    self.last_time = now

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
                if received.location == 127083080 or received.location == 127020003:
                    if data[0]['text'] == ctx.slot:
                        # Holy glasses and CAT - Mormegil, send a library card, so player won't get stuck
                        # If there are 2 SOTN players at the same time, both might receive a free library card
                        self.misplaced_queue.append(166 + base_item_id)
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
                            print("DEBUG: Exploration item")

                        if loc_data is not None:
                            if loc_data.can_be_relic:
                                # There is a item on a relic spot, send it to the player
                                if item_data[1].type != IType.RELIC:
                                    self.message_queue.append(f"Misplaced item: {item_data[0]}")
                                    self.misplaced_queue.append(item_data[1])
                                    self.add_misplaced(ctx, item_data[1].index)
                                    self.last_misplaced += 1
                            else:
                                # Normal location containing a relic
                                if item_data[1].type == IType.RELIC:
                                    self.message_queue.append(f"Misplaced relic: {item_data[0]}")
                                    self.misplaced_queue.append(item_data[1])
                                    self.add_misplaced(ctx, item_data[1].index)
                                    self.last_misplaced += 1
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
                (await bizhawk.read(ctx.bizhawk_ctx, [(0x3c760, 2, "MainRAM")]))[0], "little")

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
                        (v.zone == "Necromancy Laboratory" and zone_data.name == "Beezlebub")):
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
        relic,      name, offset, [relic pos()]
        wall,       name, flag, bit to check
        """

        if zone_abbreviation == "ARE" or zone_abbreviation == "BO2":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3010:
                check.append(("boss", "ARE - Minotaurus/Werewolf kill", 0x03ca38))
            if room == 0x2e90:
                check.append(("relic", "Form of Mist", 10, [(222, 135)]))

        if zone_abbreviation == "CAT" or zone_abbreviation == "BO1":
            if game_id == 3020:
                check.append(("boss", "CAT - Legion kill", 0x03ca34))

        if zone_abbreviation == "CHI" or zone_abbreviation == "BO7":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3040:
                check.append(("wall", "CHI - Turkey(Demon)", 0x03be1f, 0))
            elif game_id == 3041:
                check.append(("boss", "CHI - Cerberos kill", 0x03be3d))
            if room == 0x19b8:
                check.append(("relic", "Demon Card", 10, [(88, 167)]))

        if zone_abbreviation == "DAI" or zone_abbreviation == "BO5":
            if game_id == 3050:
                check.append(("boss", "DAI - Hippogryph kill", 0x03ca44))

        if zone_abbreviation == "LIB":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3070:
                check.append(("boss", "LIB - Lesser Demon kill", 0x03ca6c))
            if room == 0x2ec4:
                check.append(("relic", "Soul of Bat", 10, [(1051, 919)]))
            elif room == 0x2f0c:
                check.append(("relic", "Faerie Scroll", 80, [(1681, 167)]))
            elif room == 0x2ee4:
                check.append(("relic", "Jewel of Open", 10, [(230, 135)]))
            elif room == 0x2efc:
                check.append(("relic", "Faerie Card", 10, [(48, 167)]))

        if zone_abbreviation == "NO0" or zone_abbreviation == "CEN":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3080:
                check.append(("wall", "NO0 - Holy glasses", 0x03bec4, 0))
            if room == 0x27f4:
                check.append(("relic", "Spirit Orb", 10, [(130, 1080)]))
            elif room == 0x2884:
                check.append(("relic", "Gravity Boots", 10, [(1170, 167)]))

        if zone_abbreviation == "NO1" or zone_abbreviation == "BO4":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3090:
                check.append(("wall", "NO1 - Pot Roast", 0x03bdfe, 0))
            elif game_id == 3091:
                check.append(("boss", "NO1 - Doppleganger 10 kill", 0x03ca30))
            if room == 0x34f4:
                check.append(("relic", "Soul of Wolf", 10, [(360, 807)]))

        if zone_abbreviation == "NO2" or zone_abbreviation == "BO0":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3100:
                check.append(("boss", "NO2 - Olrox kill", 0x03ca2c))
            if room == 0x330c:
                check.append(("relic", "Echo of Bat", 10, [(130, 165)]))
            elif room == 0x3314:
                check.append(("relic", "Sword Card", 10, [(367, 135)]))

        if zone_abbreviation == "NO3":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3110:
                check.append(("wall", "NO3 - Pot Roast", 0x03be1f, 0))
            elif game_id == 3111:
                check.append(("wall", "NO3 - Turkey", 0x03be24, 0))
            if room == 0x3d40 or room == 0x3af8:
                check.append(("relic", "Cube of Zoe", 10, [(270, 103)]))
            elif room == 0x3cc8 or room == 0x3a80:
                check.append(("relic", "Power of Wolf", 10, [(245, 183), (270, 183)]))

        if zone_abbreviation == "NO4" or zone_abbreviation == "BO3" or zone_abbreviation == "DRE":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3130:
                check.append(("boss", "NO4 - Scylla kill", 0x03ca3c))
            elif game_id == 3131:
                check.append(("boss", "NO4 - Succubus kill", 0x03ca4c))
            if room == 0x315c:
                check.append(("relic", "Holy Symbol", 10, [(141, 167)]))
            elif room == 0x319c:
                check.append(("relic", "Merman Statue", 10, [(92, 167)]))

        if zone_abbreviation == "NZ0":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3140:
                check.append(("boss", "NZ0 - Slogra and Gaibon kill", 0x03ca40))
            if room == 0x2770:
                check.append(("relic", "Skill of Wolf", 25, [(120, 167)]))
            elif room == 0x2730:
                check.append(("relic", "Bat Card", 25, [(114, 167)]))

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
                check.append(("relic", "Fire of Bat", 10, [(198, 183)]))

        if zone_abbreviation == "TOP":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if room == 0x1b8c:
                check.append(("relic", "Leap Stone", 10, [(424, 1815)]))
                check.append(("relic", "Power of Mist", 10, [(417, 1207)]))
            elif room == 0x1b94:
                check.append(("relic", "Ghost Card", 10, [(350, 663)]))

        if zone_abbreviation == "RARE" or zone_abbreviation == "RBO0":
            if game_id == 3180:
                check.append(("boss", "RARE - Fake Trevor/Grant/Sypha kill", 0x03ca54))

        if zone_abbreviation == "RCAT" or zone_abbreviation == "RBO8":
            room = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(0x1375bc, 2, "MainRAM")]))[0], "little")
            if game_id == 3190:
                check.append(("boss", "RCAT - Galamoth kill", 0x03ca7c))
            if room == 0x2429 or room == 0x2490:
                check.append(("relic", "Gas Cloud", 10, [(38, 173)]))

        if zone_abbreviation == "RCHI" or zone_abbreviation == "RBO2":
            if game_id == 3210 or game_id == 3211:
                check.append(("boss", "RCHI - Death kill", 0x03ca58))
                check.append(("boss_relic", "Eye of Vlad", 0x03ca58))

        if zone_abbreviation == "RDAI" or zone_abbreviation == "RBO3":
            if game_id == 3220 or game_id == 3221:
                check.append(("boss", "RDAI - Medusa kill", 0x03ca64))
                check.append(("boss_relic", "Heart of Vlad", 0x03ca64))

        if zone_abbreviation == "RNO1" or zone_abbreviation == "RBO4":
            if game_id == 3240:
                check.append(("wall", "RNO1 - Dim Sum set", 0x03be04, 0))
            elif game_id == 3241 or game_id == 3242:
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
                check.append(("relic", "Force of Echo", 10, [(110, 167)]))

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
                        for point in c[3]:
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

    def add_misplaced(self, ctx: "BizHawkClientContext", item_id: int):
        filename = f"{os.getcwd()}\\AP_{ctx.seed_name}_P{ctx.slot}_{ctx.username}.txt"

        print(f"Added misplaced {item_id}")
        # Add to file and list
        self.misplaced_load.append(item_id)
        with open(filename, "a") as stream:
            stream.write(f"{item_id}\n")

    def populate_misplaced(self, ctx: "BizHawkClientContext"):
        filename = f"{os.getcwd()}\\AP_{ctx.seed_name}_P{ctx.slot}_{ctx.username}.txt"

        with open(filename, "r") as stream:
            next(stream)
            for line in stream:
                self.misplaced_load.append(line)
                print(f"DEBUG: Added line {line}")


async def grant_item(item: ItemData, ctx: "BizHawkClientContext"):
    item_id = item.index - base_item_id
    address = item.address

    print(f"{item_id} : {address}")

    if 300 <= item_id < 400:
        relic = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address, 1, "MainRAM")]))[0], "little")
        if relic == 0 or relic == 2 or relic > 3:
            if 318 <= item_id <= 322:
                await bizhawk.write(ctx.bizhawk_ctx, [(address, b'\x01', "MainRAM")])
            else:
                await bizhawk.write(ctx.bizhawk_ctx, [(address, b'\x03', "MainRAM")])
        print("Relic granted")
    elif item_id == 412:
        cur_heart = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address, 4, "MainRAM")]))[0], "little")
        max_heart = int.from_bytes((await bizhawk.read(ctx.bizhawk_ctx, [(address + 4, 4, "MainRAM")]))[0], "little")
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
        await bizhawk.write(ctx.bizhawk_ctx, [(address, qty.to_bytes(1, "little"), "MainRAM")])
        # First item, sort the inventory
        if qty == 1:
            print("Sorting inventory")
            start_address = 0
            max_index = 0
            item_offset = 0
            start_byte = 0x00
            if item.type == IType.ARMOR:
                start_address = 0x097b36
                max_index = 27
                item_offset = 169
            elif item.type == IType.HELMET:
                start_address = 0x097b50
                max_index = 21
                item_offset = 195
                start_byte = 0x1a
            elif item.type == IType.CLOAK:
                start_address = 0x097b66
                max_index = 8
                item_offset = 217
                start_byte = 0x30
            elif item.type == IType.ACCESSORY:
                start_address = 0x097b6f
                max_index = 31
                item_offset = 226
                start_byte = 0x39
            else:
                start_address = 0x097a8d
                max_index = 168

            for i in range(1, max_index, 1):
                read_address = start_address + i
                old_byte = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(read_address, 1, "MainRAM")]))[0], "little")
                old_item = ItemData.get_item_info((old_byte - start_byte) + item_offset + base_item_id)
                old_qty = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(old_item[1].address, 1, "MainRAM")]))[0], "little")

                if old_qty == 0:
                    print(f"DEBUG: Found empty slot at {i}")
                    new_value = item_id - item_offset + start_byte
                    for j in range(i, max_index, 1):
                        new_address = start_address + j
                        new_byte = int.from_bytes(
                            (await bizhawk.read(ctx.bizhawk_ctx, [(new_address, 1, "MainRAM")]))[0], "little")
                        if new_byte == new_value:
                            print(f"DEBUG: {new_byte} = {new_value} at {j}")
                            await bizhawk.write(ctx.bizhawk_ctx,
                                                [(read_address, new_value.to_bytes(1, "little"), "MainRAM")])
                            await bizhawk.write(ctx.bizhawk_ctx,
                                                [(new_address, old_byte.to_bytes(1, "little"), "MainRAM")])
                            break
                    break


def diff_handler(diff_file: str):
    logger.info("Handling patch")
    if diff_file:
        try:
            logger.info("Patching game")
            source1 = os.path.splitext(diff_file)[0]
            try:
                name_start = source1.rindex("AP_")
            except ValueError:
                logger.info("File not an AP format ")
                return
            source1 = source1[name_start:] + ".bin"
            source2 = "Castlevania - Symphony of the Night (USA) (Track 2).bin"
            destination = os.path.splitext(diff_file)[0] + ".cue"

            logger.info(pos_patch(os.path.splitext(diff_file)[0]))

            cue_file = f'FILE "{source1}" BINARY\n  TRACK 01 MODE2/2352\n\tINDEX 01 00:00:00\n'
            cue_file += f'FILE "{source2}" BINARY\n  TRACK 02 AUDIO\n'
            cue_file += f'\tINDEX 00 00:00:00\n\tINDEX 01 00:02:00'
            with open(destination, 'wb') as outfile:
                outfile.write(bytes(cue_file, 'utf-8'))
        except Exception as e:
            logger.info(f"Error: {e}")
            raise
        logger.info("All done!")


def cmd_patch(self, patch_dir: str):
    """Patch the ROM with the provided .apsotn(ONLY NAME)"""
    if not os.path.exists(patch_dir + ".apsotn"):
        logger.info(".apsotn not found!")
        return
    if os.path.exists(patch_dir + ".bin"):
        logger.info("Patched ROM found!")
        return
    logger.info("Start patching. Please wait!")
    diff_handler(patch_dir)


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