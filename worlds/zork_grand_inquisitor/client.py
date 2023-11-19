import asyncio

import CommonClient
import Utils

from .data_funcs import item_names_to_id, location_names_to_id, id_to_items, id_to_locations
from .game_controller import GameController


class ZorkGrandInquisitorCommandProcessor(CommonClient.ClientCommandProcessor):
    def _cmd_zork(self):
        """Attach to an open Zork Grand Inquisitor process."""
        result = self.ctx.game_controller.open_process_handle()

        if result:
            self.output("Successfully attached to Zork Grand Inquisitor process.")
        else:
            self.output("Failed to attach to Zork Grand Inquisitor process.")


class ZorkGrandInquisitorContext(CommonClient.CommonContext):
    tags = {"AP"}
    game = "Zork Grand Inquisitor"
    command_processor = ZorkGrandInquisitorCommandProcessor
    items_handling = 0b111
    want_slot_data = True

    option_skip_old_scratch_minigame = False
    option_deathsanity = False

    item_name_to_id = item_names_to_id()
    location_name_to_id = location_names_to_id()

    id_to_items = id_to_items()
    id_to_locations = id_to_locations()

    def __init__(self, server_address, password):
        super().__init__(server_address, password)

        self.game_controller = GameController(logger=CommonClient.logger)

    def run_gui(self):
        from kvui import GameManager

        class TextManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]

            base_title = "Archipelago Zork Grand Inquisitor Client"

        self.ui = TextManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def server_auth(self, password_requested=False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd, _args):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game

        CommonClient.async_start(process_package(self, cmd, _args))


async def controller(ctx):
    while not ctx.exit_event.is_set():
        # Update Completed Locations
        completed_locations = set()

        for location_id in ctx.checked_locations:
            location = ctx.id_to_locations[location_id]
            completed_locations.add(location)

        ctx.game_controller.completed_locations = completed_locations

        # Enqueue Received Item Delta
        for network_item in ctx.items_received:
            item = ctx.id_to_items[network_item.item]

            if item not in ctx.game_controller.received_items:
                if item not in ctx.game_controller.received_items_queue:
                    ctx.game_controller.received_items_queue.append(item)

        # Game Controller Update
        ctx.game_controller.update()

        # Send Checked Locations
        checked_location_ids = list()

        while len(ctx.game_controller.completed_locations_queue) > 0:
            location = ctx.game_controller.completed_locations_queue.popleft()
            location_id = ctx.location_name_to_id[location.value]

            checked_location_ids.append(location_id)

        await ctx.send_msgs([
            {
                "cmd": "LocationChecks",
                "locations": checked_location_ids
            }
        ])

        # Check for Goal Completion
        if ctx.game_controller.goal_completed:
            await ctx.send_msgs([
                {
                    "cmd": "StatusUpdate",
                    "status": CommonClient.ClientStatus.CLIENT_GOAL
                }
            ])

        await asyncio.sleep(0.2)


async def process_package(ctx: ZorkGrandInquisitorContext, cmd, _args):
    if cmd == "Connected":
        # Slot Data - Options
        ctx.game_controller.option_skip_old_scratch_minigame = _args["slot_data"]["skip_old_scratch_minigame"] == 1
        ctx.game_controller.option_deathsanity = _args["slot_data"]["deathsanity"] == 1


def main():
    Utils.init_logging("ZorkGrandInquisitorClient", exception_logger="Client")

    async def _main():
        ctx = ZorkGrandInquisitorContext(None, None)
        ctx.server_task = asyncio.create_task(CommonClient.server_loop(ctx), name="server loop")

        asyncio.create_task(controller(ctx), name="ZorkGrandInquisitorController")

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
    parser = CommonClient.get_base_parser(description="Zork Grand Inquisitor Client, for text interfacing.")
    args = parser.parse_args()
    main()
