import asyncio
import typing

from typing import TYPE_CHECKING, Any

import Utils
from CommonClient import ClientCommandProcessor, CommonContext, get_base_parser, gui_enabled, logger, server_loop

import dolphin_memory_engine

from ..strings.client_strings import ConnectionStatus

if TYPE_CHECKING:
    import kvui

class PSOCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for Phantasy Star Online Episode I&II Plus client commands

    Handles commands specific to Phantasy Star Online Episode I&II Plus
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with specific context

        :param ctx: the Context object from CommonClient for PSO
        """
        super().__init__(ctx)

    def _cmd_dolphin(self) -> None:
        """
        Display the current Dolphin emulator connection status
        """
        if isinstance(self.ctx, PSOContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class PSOContext(CommonContext):
    """
    The context object for Phantasy Star Online Episode I&II Plus from CommonClient

    Manages all interactions with the Dolphin emulator and the Archipelago server for PSO
    """
    command_processor = PSOCommandProcessor
    game = "PSO"

    def __init__(self, server_address: str | None, password: str | None) -> None:
        """
        Initialize the PSO context

        :param server_address: the address of the Archipelago server
        :param password: the password for authenticating to the Archipelago server
        """
        super().__init__(server_address, password)
        self.dolphin_sync_task: asyncio.Task[None] | None = None
        self.dolphin_status: str = ConnectionStatus.INITIAL
        self.awaiting_rom: bool = False
        self.has_send_death: bool = False

        self.current_stage_name: str = ""

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        """
        Disconnect the client from the server and reset game state variables

        :param allow_autoreconnect: whether the client should auto-reconnect to the server; defaults to `False`
         """
        self.auth = None
        self.current_stage_name = None
        await super().disconnect(*args, **kwargs)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server

        :param password_requested: whether the server requires a password; defaults to `False`
        """
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information.")
            return
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server

        :param cmd: the command received from the server
        :param args: the arguments for the received command
        """
        if cmd == "Connected":
            super().on_package(cmd, args)
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))


    def on_deathlink(self, data: dict[str, Any]) -> None:
        """
        Handle a DeathLink events from the server

        :param data: the data associated with the DeathLink event
        """
        super().on_deathlink(data)
        _give_death(self)

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for The Wind Waker client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = "Archipelago The Wind Waker Client"
        return ui
#
#     async def update_visited_stages(self, newly_visited_stage_name: str) -> None:
#         """
#         Update the server's data storage of the visited stage names to include the newly visited stage name.
#
#         :param newly_visited_stage_name: The name of the stage recently visited.
#         """
#         if self.slot is not None:
#             visited_stages_key = AP_VISITED_STAGE_NAMES_KEY_FORMAT % self.slot
#             await self.send_msgs(
#                 [
#                     {
#                         "cmd": "Set",
#                         "key": visited_stages_key,
#                         "default": {},
#                         "want_reply": False,
#                         "operations": [{"operation": "update", "value": {newly_visited_stage_name: True}}],
#                     }
#                 ]
#             )
#
#     def update_salvage_locations_map(self) -> None:
#         """
#         Update the client's mapping of salvage locations to their bitfield bit.
#
#         This is necessary for the client to handle randomized charts correctly.
#         """
#         self.salvage_locations_map = {}
#         for offset in range(49):
#             island_name = ISLAND_NUMBER_TO_NAME[offset + 1]
#             salvage_bit = ISLAND_NAME_TO_SALVAGE_BIT[island_name]
#
#             shuffled_island_number = read_short(CHARTS_MAPPING_ADDR + offset * 2)
#             shuffled_island_name = ISLAND_NUMBER_TO_NAME[shuffled_island_number]
#             salvage_location_name = f"{shuffled_island_name} - Sunken Treasure"
#
#             self.salvage_locations_map[salvage_location_name] = salvage_bit

def _give_death(ctx: PSOContext) -> None:
    """
    Trigger a player character death in-game by setting their current health to zero

    :param ctx: the Context object from CommonClient for PSO
    """
    # TODO: Implement DeathLink (below code is from TWW)
    # if (
    #     ctx.slot is not None
    #     and dolphin_memory_engine.is_hooked()
    #     and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
    #     and check_ingame()
    # ):
    #     ctx.has_send_death = True
    #     write_short(CURR_HEALTH_ADDR, 0)