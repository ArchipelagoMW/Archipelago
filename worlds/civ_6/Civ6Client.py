import asyncio
import logging
import traceback
from typing import Dict, List

from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, logger, server_loop, gui_enabled
from .Data import get_progressive_districts_data
from .DeathLink import handle_check_deathlink
from NetUtils import ClientStatus
import Utils
from .CivVIInterface import CivVIInterface, ConnectionState
from .Enum import CivVICheckType
from .Items import CivVIItemData, generate_item_table, get_item_by_civ_name
from .Locations import generate_era_location_table
from .TunerClient import TunerErrorException, TunerTimeoutException


class CivVICommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, CivVIContext):
            self.ctx.death_link_enabled = not self.ctx.death_link_enabled
            self.ctx.death_link_just_changed = True
            Utils.async_start(self.ctx.update_death_link(
                self.ctx.death_link_enabled), name="Update Deathlink")
            self.ctx.logger.info(
                f"Deathlink is now {'enabled' if self.ctx.death_link_enabled else 'disabled'}")

    def _cmd_resync(self):
        """Resends all items to client, and has client resend all locations to server. This can take up to a minute if the player has received a lot of items"""
        if isinstance(self.ctx, CivVIContext):
            logger.info("Resyncing...")
            asyncio.create_task(self.ctx.resync())

    def _cmd_toggle_progressive_eras(self):
        """If you get stuck for some reason and unable to continue your game, you can run this command to disable the defeat that comes from pushing past the max unlocked era """
        if isinstance(self.ctx, CivVIContext):
            print("Toggling progressive eras, stand by...")
            self.ctx.is_pending_toggle_progressive_eras = True


class CivVIContext(CommonContext):
    is_pending_death_link_reset = False
    is_pending_toggle_progressive_eras = False
    command_processor = CivVICommandProcessor
    game = "Civilization VI"
    items_handling = 0b111
    tuner_sync_task = None
    game_interface: CivVIInterface
    location_name_to_civ_location = {}
    location_name_to_id = {}
    item_id_to_civ_item: Dict[int, CivVIItemData] = {}
    item_table: Dict[str, CivVIItemData] = {}
    processing_multiple_items = False
    received_death_link = False
    death_link_message = ""
    death_link_enabled = False

    death_link_just_changed = False
    # Used to prevent the deathlink from triggering when someone re enables it

    logger = logger
    progressive_items_by_type = get_progressive_districts_data()
    item_name_to_id = {
        item.name: item.code for item in generate_item_table().values()}
    connection_state = ConnectionState.DISCONNECTED

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game_interface = CivVIInterface(logger)
        location_by_era = generate_era_location_table()
        self.item_table = generate_item_table()

        # Get tables formatted in a way that is easier to use here
        for era, locations in location_by_era.items():
            for item_name, location in locations.items():
                self.location_name_to_id[location.name] = location.code
                self.location_name_to_civ_location[location.name] = location

        for item_name, item in self.item_table.items():
            self.item_id_to_civ_item[item.code] = item

    async def resync(self):
        if self.processing_multiple_items:
            logger.info(
                "Waiting for items to finish processing, try again later")
            return
        await self.game_interface.resync()
        await handle_receive_items(self, -1)
        logger.info("Resynced")

    def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
        super().on_deathlink(data)
        text = data.get("cause", "")
        if text:
            message = text
        else:
            message = f"Received from {data['source']}"
        self.death_link_message = message
        self.received_death_link = True

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(CivVIContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def run_gui(self):
        from kvui import GameManager

        class CivVIManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Civlization VI Client"

        self.ui = CivVIManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            if "death_link" in args["slot_data"]:
                self.death_link_enabled = bool(args["slot_data"]["death_link"])
                Utils.async_start(self.update_death_link(
                    bool(args["slot_data"]["death_link"])))


def update_connection_status(ctx: CivVIContext, status):
    if ctx.connection_state == status:
        return
    elif status == ConnectionState.IN_GAME:
        ctx.logger.info("Connected to Civ VI")
    elif status == ConnectionState.IN_MENU:
        ctx.logger.info("Connected to Civ VI, waiting for game to start")
    elif status == ConnectionState.DISCONNECTED:
        ctx.logger.info("Disconnected from Civ VI, attempting to reconnect...")

    ctx.connection_state = status


async def tuner_sync_task(ctx: CivVIContext):
    logger.info("Starting CivVI connector")
    while not ctx.exit_event.is_set():
        if not ctx.slot:
            await asyncio.sleep(3)
            continue
        else:
            try:
                if ctx.processing_multiple_items == True:
                    logger.debug("Waiting for items to finish processing")
                    await asyncio.sleep(3)
                else:
                    state = await ctx.game_interface.is_in_game()
                    update_connection_status(ctx, state)
                    if state == ConnectionState.IN_GAME:
                        await _handle_game_ready(ctx)
                    else:
                        await asyncio.sleep(3)
            except TunerTimeoutException:
                logger.error(
                    "Timeout occurred while receiving data from Civ VI, this usually isn't a problem unless you see it repeatedly")
                await asyncio.sleep(3)
            except Exception as e:
                if isinstance(e, TunerErrorException):
                    logger.debug(str(e))
                else:
                    logger.debug(traceback.format_exc())

                await asyncio.sleep(3)
                continue


async def handle_toggle_progressive_eras(ctx: CivVIContext):
    if ctx.is_pending_toggle_progressive_eras:
        ctx.is_pending_toggle_progressive_eras = False
        current = await ctx.game_interface.get_max_allowed_era()
        if current > -1:
            await ctx.game_interface.set_max_allowed_era(-1)
            logger.info("Disabled progressive eras")
        else:
            count = 0
            for _, network_item in enumerate(ctx.items_received):
                item: CivVIItemData = ctx.item_id_to_civ_item[network_item.item]
                if item.item_type == CivVICheckType.ERA:
                    count += 1
            await ctx.game_interface.set_max_allowed_era(count)
            logger.info(f"Enabled progressive eras, set to {count}")


async def handle_checked_location(ctx: CivVIContext):
    checked_locations = await ctx.game_interface.get_checked_locations()
    checked_location_ids = [location.code for location_name, location in ctx.location_name_to_civ_location.items(
    ) if location_name in checked_locations]

    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": checked_location_ids}])


async def handle_receive_items(ctx: CivVIContext, last_received_index_override: int = None):
    try:
        last_received_index = last_received_index_override or await ctx.game_interface.get_last_received_index()
        if len(ctx.items_received) - last_received_index > 1:
            logger.debug("Multiple items received")
            ctx.processing_multiple_items = True

        progressive_districts: List[CivVIItemData] = []
        progressive_eras: List[CivVIItemData] = []
        for index, network_item in enumerate(ctx.items_received):

            # Track these separately so if we replace "PROGRESSIVE_DISTRICT" with a specific tech, we can still check if need to add it to the list of districts
            item: CivVIItemData = ctx.item_id_to_civ_item[network_item.item]
            item_to_send: CivVIItemData = ctx.item_id_to_civ_item[network_item.item]
            if index > last_received_index:
                if item.item_type == CivVICheckType.PROGRESSIVE_DISTRICT:
                    # if the item is progressive, then check how far in that progression type we are and send the appropriate item
                    count = sum(
                        1 for count_item in progressive_districts if count_item.civ_name == item.civ_name)

                    if count >= len(ctx.progressive_items_by_type[item.civ_name]):
                        logger.error(
                            f"Received more progressive items than expected for {item.civ_name}")
                        continue

                    item_civ_name = ctx.progressive_items_by_type[item.civ_name][count]
                    actual_item_name = get_item_by_civ_name(item_civ_name, ctx.item_table).name
                    item_to_send = ctx.item_table[actual_item_name]

                sender = ctx.player_names[network_item.player]
                if item.item_type == CivVICheckType.ERA:
                    count = len(progressive_eras) + 1
                    await ctx.game_interface.give_item_to_player(item_to_send, sender, count)
                elif item.item_type == CivVICheckType.GOODY:
                    item_to_send.civ_vi_id = item_to_send.civ_name
                    await ctx.game_interface.give_item_to_player(item_to_send, sender)
                else:
                    await ctx.game_interface.give_item_to_player(item_to_send, sender)
                await asyncio.sleep(0.02)

            if item.item_type == CivVICheckType.PROGRESSIVE_DISTRICT:
                progressive_districts.append(item)
            elif item.item_type == CivVICheckType.ERA:
                progressive_eras.append(item)

        if ctx.processing_multiple_items:
            logger.debug("DONE")
        ctx.processing_multiple_items = False
    finally:
        # If something errors out, then unblock item processing
        ctx.processing_multiple_items = False


async def handle_check_goal_complete(ctx: CivVIContext):
    # logger.debug("Sending Goal Complete")
    result = await ctx.game_interface.check_victory()
    if result:
        logger.info("Sending Victory to server!")
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


async def _handle_game_ready(ctx: CivVIContext):
    if ctx.server:
        if not ctx.slot:
            await asyncio.sleep(3)
            return

        await handle_receive_items(ctx)
        await handle_checked_location(ctx)
        await handle_check_goal_complete(ctx)

        if ctx.death_link_enabled:
            await handle_check_deathlink(ctx)

        # process pending commands
        await handle_toggle_progressive_eras(ctx)
        await asyncio.sleep(3)
    else:
        logger.info("Waiting for player to connect to server")
        await asyncio.sleep(3)


def main(connect=None, password=None, name=None):
    Utils.init_logging("Civilization VI Client")

    async def _main(connect, password, name):
        ctx = CivVIContext(connect, password)
        ctx.auth = name
        ctx.server_task = asyncio.create_task(
            server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        await asyncio.sleep(1)

        ctx.tuner_sync_task = asyncio.create_task(
            tuner_sync_task(ctx), name="TunerSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.tuner_sync_task:
            await asyncio.sleep(3)
            await ctx.tuner_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password, name))
    colorama.deinit()


def debug_main():
    parser = get_base_parser()
    parser.add_argument('--name', default=None,
                        help="Slot Name to connect as.")
    parser.add_argument('--debug', default=None,
                        help="debug mode, additional logging")
    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    main(args.connect, args.password, args.name)
