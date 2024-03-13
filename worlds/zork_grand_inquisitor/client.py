import asyncio

import CommonClient
import NetUtils
import Utils

from typing import Any, Dict, List, Optional, Set, Tuple

from .data_funcs import item_names_to_id, location_names_to_id, id_to_items, id_to_locations, id_to_goals
from .enums import ZorkGrandInquisitorItems, ZorkGrandInquisitorLocations
from .game_controller import GameController


class ZorkGrandInquisitorCommandProcessor(CommonClient.ClientCommandProcessor):
    def _cmd_zork(self) -> None:
        """Attach to an open Zork Grand Inquisitor process."""
        result: bool = self.ctx.game_controller.open_process_handle()

        if result:
            self.ctx.process_attached_at_least_once = True
            self.output("Successfully attached to Zork Grand Inquisitor process.")
        else:
            self.output("Failed to attach to Zork Grand Inquisitor process.")

    def _cmd_brog(self) -> None:
        """List received Brog items."""
        self.ctx.game_controller.list_received_brog_items()

    def _cmd_griff(self) -> None:
        """List received Griff items."""
        self.ctx.game_controller.list_received_griff_items()

    def _cmd_lucy(self) -> None:
        """List received Lucy items."""
        self.ctx.game_controller.list_received_lucy_items()

    def _cmd_hotspots(self) -> None:
        """List received Hotspots."""
        self.ctx.game_controller.list_received_hotspots()


class ZorkGrandInquisitorContext(CommonClient.CommonContext):
    tags: Set[str] = {"AP"}
    game: str = "Zork Grand Inquisitor"
    command_processor: CommonClient.ClientCommandProcessor = ZorkGrandInquisitorCommandProcessor
    items_handling: int = 0b111
    want_slot_data: bool = True

    item_name_to_id: Dict[str, int] = item_names_to_id()
    location_name_to_id: Dict[str, int] = location_names_to_id()

    id_to_items: Dict[int, ZorkGrandInquisitorItems] = id_to_items()
    id_to_locations: Dict[int, ZorkGrandInquisitorLocations] = id_to_locations()

    game_controller: GameController

    controller_task: Optional[asyncio.Task]

    process_attached_at_least_once: bool
    can_display_process_message: bool

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)

        self.game_controller = GameController(logger=CommonClient.logger)

        self.controller_task = None

        self.process_attached_at_least_once = False
        self.can_display_process_message = True

    def run_gui(self) -> None:
        from kvui import GameManager

        class TextManager(GameManager):
            logging_pairs: List[Tuple[str, str]] = [("Client", "Archipelago")]
            base_title: str = "Archipelago Zork Grand Inquisitor Client"

        self.ui = TextManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, _args: Any) -> None:
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game

            # Options
            self.game_controller.option_goal = id_to_goals()[_args["slot_data"]["goal"]]
            self.game_controller.option_deathsanity = _args["slot_data"]["deathsanity"] == 1

            self.game_controller.option_grant_missable_location_checks = (
                _args["slot_data"]["grant_missable_location_checks"] == 1
            )

    async def controller(self):
        while not self.exit_event.is_set():
            await asyncio.sleep(0.1)

            # Enqueue Received Item Delta
            network_item: NetUtils.NetworkItem
            for network_item in self.items_received:
                item: ZorkGrandInquisitorItems = self.id_to_items[network_item.item]

                if item not in self.game_controller.received_items:
                    if item not in self.game_controller.received_items_queue:
                        self.game_controller.received_items_queue.append(item)

            # Game Controller Update
            if self.game_controller.is_process_running():
                self.game_controller.update()
                self.can_display_process_message = True
            else:
                process_message: str

                if self.process_attached_at_least_once:
                    process_message = (
                        "Lost connection to Zork Grand Inquisitor process. Please restart the game and use the /zork "
                        "command to reattach."
                    )
                else:
                    process_message = (
                        "Please use the /zork command to attach to a running Zork Grand Inquisitor process."
                    )

                if self.can_display_process_message:
                    CommonClient.logger.info(process_message)
                    self.can_display_process_message = False

            # Send Checked Locations
            checked_location_ids: List[int] = list()

            while len(self.game_controller.completed_locations_queue) > 0:
                location: ZorkGrandInquisitorLocations = self.game_controller.completed_locations_queue.popleft()
                location_id: int = self.location_name_to_id[location.value]

                checked_location_ids.append(location_id)

            await self.send_msgs([
                {
                    "cmd": "LocationChecks",
                    "locations": checked_location_ids
                }
            ])

            # Check for Goal Completion
            if self.game_controller.goal_completed:
                await self.send_msgs([
                    {
                        "cmd": "StatusUpdate",
                        "status": CommonClient.ClientStatus.CLIENT_GOAL
                    }
                ])


def main() -> None:
    Utils.init_logging("ZorkGrandInquisitorClient", exception_logger="Client")

    async def _main():
        ctx: ZorkGrandInquisitorContext = ZorkGrandInquisitorContext(None, None)

        ctx.server_task = asyncio.create_task(CommonClient.server_loop(ctx), name="server loop")
        ctx.controller_task = asyncio.create_task(ctx.controller(), name="ZorkGrandInquisitorController")

        if CommonClient.gui_enabled:
            ctx.run_gui()

        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    colorama.init()

    asyncio.run(_main())

    colorama.deinit()


if __name__ == "__main__":
    main()
