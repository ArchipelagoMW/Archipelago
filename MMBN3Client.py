import asyncio
import json
import os
import multiprocessing
import subprocess

from asyncio import StreamReader, StreamWriter

from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
from worlds import network_data_package
from worlds.mmbn3.GBAPatch import apply_patch_file
from worlds.mmbn3.Locations import location_data_table

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart mmbn3_connector.lua"
CONNECTION_REFUSED_STATUS = \
    "Connection refused. Please start your emulator and make sure mmbn3_connector.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart mmbn3_connector.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

"""
Payload: lua -> client
{
    playerName: string,
    locations: dict,
    gameComplete: bool
}

Payload: client -> lua
{
    items: list,
    playerNames: list
}
"""

mmbn3_loc_name_to_id = network_data_package["games"]["MegaMan Battle Network 3"]["location_name_to_id"]

script_version: int = 1

testingData = {}
items_sent = []
locations_checked = []

def get_item_value(ap_id):
    # TODO OOT had ap_id - 66000. I'm assuming this is because of the ROM offset, which for GBA is 8000000, let's try that?
    return ap_id - 8000000


class MMBN3CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_gba(self):
        """Check GBA Connection State"""
        if isinstance(self.ctx, MMBN3Context):
            logger.info(f"GBA Status: {self.ctx.gba_status}")

    def _cmd_debugchip(self, chip, code):
        global testingData
        logger.info("Sending test package")
        testingData["sender"] = "DebugTest"
        testingData["type"] = "chip"
        testingData["itemID"] = chip
        testingData["subItemID"] = code
        testingData["count"] = 1

    def _cmd_debugitem(self, item):
        global testingData
        logger.info("Sending test package")
        testingData["sender"] = "DebugTest"
        testingData["type"] = "key"
        testingData["itemID"] = item
        testingData["subItemID"] = -1
        testingData["count"] = 1

    def _cmd_debugsubchip(self, item):
        global testingData
        logger.info("Sending test package")
        testingData["sender"] = "DebugTest"
        testingData["type"] = "subchip"
        testingData["itemID"] = item
        testingData["subItemID"] = -1
        testingData["count"] = 1

    def _cmd_debugzenny(self, amt):
        global testingData
        logger.info("Sending test package")
        testingData["sender"] = "DebugTest"
        testingData["type"] = "zenny"
        testingData["itemID"] = -1
        testingData["subItemID"] = -1
        testingData["count"] = amt

    def _cmd_debugprogram(self, program, color):
        global testingData
        logger.info("Sending test package")
        testingData["sender"] = "DebugTest"
        testingData["type"] = "program"
        testingData["itemID"] = program
        testingData["subItemID"] = color
        testingData["count"] = 1

    def _cmd_debugbugfrag(self, amt):
        global testingData
        logger.info("Sending test package")
        testingData["sender"] = "DebugTest"
        testingData["type"] = "bugfrag"
        testingData["itemID"] = -1
        testingData["subItemID"] = -1
        testingData["count"] = amt


class MMBN3Context(CommonContext):
    command_processor = MMBN3CommandProcessor
    # TODO No idea what full local means or what this is. Ask espeon about it
    items_handling = 0b001  # full local

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = 'MegaMan Battle Network 3'
        self.gba_streams: (StreamReader, StreamWriter) = None
        self.gba_sync_task = None
        self.gba_status = CONNECTION_INITIAL_STATUS
        self.awaiting_rom = False
        self.location_table = {}
        self.version_warning = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(MMBN3Context, self).server_auth(password_requested)
        if not self.auth:
            self.awaiting_rom = True
            logger.info('Awaiting connection to Bizhawk to get player information')
            return

        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class MMBN3Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago MegaMan Battle Network 3 Client"

        self.ui = MMBN3Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

class item_info:
    id = 0x00
    sender = ""
    type = ""
    count = 1
    itemID = 0x00 #Item ID, Chip ID, etc.
    subItemID = 0x00 #Code for chips, color for programs

    def __init__(self,id,sender,type):
        self.id = id
        self.sender = sender
        self.type = type

    def get_json(self):
        json_data = {
            "id": self.id,
            "sender": self.sender,
            "type": self.type,
            "itemID": self.itemID,
            "subItemID": self.subItemID,
            "count": self.count
        }
        return json_data


def get_payload(ctx: MMBN3Context):
    global testingData
    if len(testingData) > 0:
        test_item = item_info(len(items_sent), testingData["sender"], testingData["type"])
        test_item.itemID = int(testingData["itemID"])
        test_item.subItemID = int(testingData["subItemID"])
        test_item.count = int(testingData["count"])
        items_sent.append(test_item)
        testingData = {}

    return json.dumps({
        "items": [item.get_json() for item in items_sent]
        })


async def parse_payload(payload: dict, ctx: MMBN3Context, force: bool):
    # Game completion handling
    if payload['gameComplete'] and not ctx.finished_game:
        await ctx.send_msgs([{
            "cmd": "StatusUpdate",
            "status": 30
        }])
        ctx.finished_game = True

    # Locations handling
    if ctx.location_table != payload['locations']:
        ctx.location_table = payload['locations']
        await ctx.send_msgs([{
            "cmd": "LocationChecks",
            "locations": [mmbn3_loc_name_to_id[loc] for loc in ctx.location_table
                          if check_item_packet(loc, ctx.location_table[loc])]
        }])


def check_item_packet(name,packet):
    locData = location_data_table[name]
    if packet & locData.flag_mask:
        logger.info("You found the item at location "+name)
    return packet & locData.flag_mask


async def gba_sync_task(ctx: MMBN3Context):
    global testingData

    logger.info("Starting GBA connector. Use /gba for status information.")
    while not ctx.exit_event.is_set():
        error_status = None
        if ctx.gba_streams:
            (reader, writer) = ctx.gba_streams
            msg = get_payload(ctx).encode()
            testingData = {}
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    # Data will return a dict with up to four fields
                    # 1. str: player name (always)
                    # 2. int: script version (always)
                    # 3. dict[str, byte]: value of location's memory byte
                    # 4. bool: whether the game currently registers as complete
                    data = await asyncio.wait_for(reader.readline(), timeout=10)
                    data_decoded = json.loads(data.decode())
                    reported_version = data_decoded.get('scriptVersion', 0)
                    if reported_version >= script_version:
                        if ctx.game is not None and 'locations' in data_decoded:
                            # Not just a keep alive ping, parse
                            asyncio.create_task((parse_payload(data_decoded, ctx, False)))
                        if not ctx.auth:
                            ctx.auth = data_decoded['playerName']
                            if ctx.awaiting_rom:
                                await ctx.server_auth(False)
                    else:
                        if not ctx.version_warning:
                            logger.warning(f"Your Lua script is version {reported_version}, expected {script_version}."
                                           "Please update to the latest version."
                                           "Your connection to the Archipelago server will not be accepted.")
                            ctx.version_warning = True
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.gba_streams = None
                except ConnectionResetError:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.gba_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.gba_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.gba_streams = None
            if ctx.gba_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to GBA")
                    ctx.gba_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.gba_status = f"Was tentatively connected but error occurred: {error_status}"
            elif error_status:
                ctx.gba_status = error_status
                logger.info("Lost connection to GBA and attempting to reconnect. Use /gba for status updates")
        else:
            try:
                logger.info("Attempting to connect to GBA")
                ctx.gba_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 28922), timeout=10)
                ctx.gba_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.gba_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.gba_status = CONNECTION_REFUSED_STATUS
                continue


async def run_game(romfile):
    auto_start = Utils.get_options()["mmbn3_options"].get("rom_start", True)
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(apmmbn3_file):
    base_name = os.path.splitext(apmmbn3_file)[0]
    decomp_path = base_name + '-decomp.gba'
    comp_path = base_name + '.gba'
    # Load vanilla ROM, patch file, compress ROM
    #rom = Rom(Utils.local_path(Utils.get_options()["mmbn3_options"]["rom_file"]))
    #apply_patch_file(rom, apmmbn3_file)
    #rom.write_to_file(decomp_path)
    #os.chdir(data_path("Compress"))
    #compress_rom_file(decomp_path, comp_path)
    os.remove(decomp_path)
    asyncio.create_task(run_game(comp_path))

if __name__ == '__main__':
    Utils.init_logging("MMBN3Client")

    async def main():
        multiprocessing.freeze_support()
        parser = get_base_parser()
        parser.add_argument('apmmbn3_file', default="", type=str, nargs="?",
                            help='Path to an APMMBN3 file')
        args = parser.parse_args()

        if args.apmmbn3_file:
            logger.info("APMMBN3 file supplied, beginning patching process...")
            asyncio.create_task(patch_and_run_game(args.apmmbn3_file))

        ctx = MMBN3Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        ctx.gba_sync_task = asyncio.create_task(gba_sync_task(ctx), name="GBA Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.gba_sync_task:
            await ctx.gba_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()
