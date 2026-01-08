from typing import Optional
import asyncio
import colorama
import time
import tkinter
import re

from .Bingo import (
    run_bingo_board,
    highlight_square,
    update_bingo_board,
)


from CommonClient import (
    CommonContext,
    ClientCommandProcessor,
    get_base_parser,
    logger,
    server_loop,
    gui_enabled,
)
from NetUtils import NetworkItem, ClientStatus


class BingoClientCommandProcessor(ClientCommandProcessor):

    def _cmd_bingo_check(self):
        """Tells you how many bingos you have, and how many you need to goal"""
        asyncio.create_task(self.ctx.get_bingo_info())


class BingoContext(CommonContext):
    """Bingo Game Context"""

    command_processor = BingoClientCommandProcessor

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)

        self.game = "APBingo"
        self.previous_received = []
        self.board_locations = []
        self.items_handling = 0b001 | 0b010 | 0b100  #Receive items from other worlds, starting inv, and own items
        self.location_ids = None
        self.location_name_to_ap_id = None
        self.location_ap_id_to_name = None
        self.item_name_to_ap_id = None
        self.item_ap_id_to_name = None
        self.found_checks = []
        self.missing_checks = []  # Stores all location checks found, for filtering
        self.prev_found = []
        self.seed_name = None
        self.options = None
        self.required_bingo = None
        self.board_size = None
        self.acquired_keys = []
        self.obtained_items_queue = asyncio.Queue()
        self.critical_section_lock = asyncio.Lock()
        self.player = None

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):

        if cmd == "Connected":

            self.missing_checks = args["missing_locations"]
            self.prev_found = args["checked_locations"]
            self.location_ids = set(args["missing_locations"] + args["checked_locations"])
            self.options = args["slot_data"]
            self.required_bingo = self.options["requiredBingoCount"]
            self.board_locations = self.options["boardLocations"]
            self.board_size = self.options["boardSize"]
            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["APBingo"]}]))

            # Use is_valid_color to determine whether to use the custom or default value
            board = self.options["customBoard"] if self.is_valid_color(self.options["customBoard"]) else "white"
            square = self.options["customSquare"] if self.is_valid_color(self.options["customSquare"]) else "white"
            hl_square = self.options["customHLSquare"] if self.is_valid_color(self.options["customHLSquare"]) else "green"
            text = self.options["customText"] if self.is_valid_color(self.options["customText"]) else "black"

            # Call run_bingo_board with pre-evaluated arguments
            run_bingo_board(self.board_size, board, square, hl_square, text)
            time.sleep(3)  # Give the board time to gen
            update_bingo_board(self.board_locations)

            # if we don't have the seed name from the RoomInfo packet, wait until we do.
            while not self.seed_name:
                time.sleep(1)

        if cmd == "ReceivedItems":
            # If receiving an item, only append that item
            asyncio.create_task(self.receive_item())

        if cmd == "RoomInfo":
            self.seed_name = args['seed_name']

        elif cmd == "DataPackage":
            if not self.location_ids:
                # Connected package not recieved yet, wait for datapackage request after connected package
                return

            self.previous_received = []
            self.location_name_to_ap_id = args["data"]["games"]["APBingo"]["location_name_to_id"]
            self.location_name_to_ap_id = {
                name: loc_id for name, loc_id in
                self.location_name_to_ap_id.items() if loc_id in self.location_ids
            }
            self.location_ap_id_to_name = {v: k for k, v in self.location_name_to_ap_id.items()}
            self.item_name_to_ap_id = args["data"]["games"]["APBingo"]["item_name_to_id"]
            self.item_ap_id_to_name = {v: k for k, v in self.item_name_to_ap_id.items()}

            # If receiving data package, resync previous items
            asyncio.create_task(self.receive_item())

        elif cmd == "LocationInfo":
            # request after an item is obtained
            asyncio.create_task(self.obtained_items_queue.put(args["locations"][0]))

    async def receive_item(self):
        async with self.critical_section_lock:

            if not self.item_ap_id_to_name:
                return

            for network_item in self.items_received:
                if network_item not in self.previous_received:
                    self.previous_received.append(network_item)
                    item_name = self.item_ap_id_to_name[network_item.item]
                    highlight_square(item_name)
                    self.acquired_keys.append(item_name)
                    self.bingo_check()

    def bingo_check(self):

        # Generate rows and columns dynamically
        rows = [chr(ord('A') + i) for i in range(self.board_size)]  # 'A', 'B', 'C', etc.
        columns = [str(i + 1) for i in range(self.board_size)]  # '1', '2', '3', etc.

        # Create a set for acquired keys for efficient lookup
        acquired_set = set(self.acquired_keys)

        # Initialize a list to hold achieved bingos
        achieved_bingos = []

        # Check rows for bingo
        for row in rows:
            if all(f"{row}{col}" in acquired_set for col in columns):
                achieved_bingos.append(f"Bingo ({row}1-{row}{self.board_size})")

            # Check columns for bingo
        for col in columns:
            if all(f"{row}{col}" in acquired_set for row in rows):
                achieved_bingos.append(f"Bingo (A{col}-{rows[-1]}{col})")

            # Check diagonals for bingo
        if all(f"{rows[i]}{columns[i]}" in acquired_set for i in range(self.board_size)):
            achieved_bingos.append(f"Bingo (A1-{rows[-1]}{self.board_size})")
        if all(f"{rows[i]}{columns[self.board_size - 1 - i]}" in acquired_set for i in range(self.board_size)):
            achieved_bingos.append(f"Bingo ({rows[-1]}1-A{self.board_size})")

        # Calculate the maximum number of possible bingos for the current board size
        if len(achieved_bingos) == 2 * self.board_size + 2:
            self.found_checks.append(self.location_name_to_ap_id["Bingo (ALL)"])

        # If goal no# of bingo's achieved, victory!
        if len(achieved_bingos) >= int(self.required_bingo):
            asyncio.create_task(self.end_goal())

        bingo_locs = []
        for bingo in achieved_bingos:
            bingo_locs.append(f"{bingo}-0")
            bingo_locs.append(f"{bingo}-1")
            bingo_locs.append(f"{bingo}-2")
            bingo_locs.append(f"{bingo}-3")
            bingo_locs.append(f"{bingo}-4")

        for location in bingo_locs:
            if location in self.location_name_to_ap_id:
                self.found_checks.append(self.location_name_to_ap_id[location])

        asyncio.create_task(self.send_checks())

    def is_valid_color(self, color_string):
        # Match patterns for hex color codes with 3, 4, 6, or 8 hex digits
        hex_pattern = r'^#([A-Fa-f0-9]{3}|[A-Fa-f0-9]{4}|[A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$'

        # Check if it's a valid hex code
        if re.match(hex_pattern, color_string):
            return True

        # Try to validate with Tkinter's color recognition
        try:
            tkinter.Tk().winfo_rgb(color_string)
            return True
        except tkinter.TclError:
            return False

    async def end_goal(self):
        message = [{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]
        await self.send_msgs(message)

    async def send_checks(self):
        message = [{"cmd": 'LocationChecks', "locations": self.found_checks}]
        await self.send_msgs(message)
        self.remove_found_checks()
        self.found_checks.clear()

    def remove_found_checks(self):
        self.prev_found += self.found_checks
        self.missing_checks = [item for item in self.missing_checks if item not in self.found_checks]

    async def get_bingo_info(self):
        logger.info("You need to get " + str(self.required_bingo) + " bingo's to win!")


def launch():
    """
    Launch a client instance (wrapper / args parser)
    """

    async def main(args):
        """
        Launch a client instance (threaded)
        """
        ctx = BingoContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await ctx.exit_event.wait()
        await ctx.shutdown()

    parser = get_base_parser(description="APBingo Client")
    args, _ = parser.parse_known_args()

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
