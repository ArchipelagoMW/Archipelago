import asyncio

import Utils
from CommonClient import logger, get_base_parser, gui_enabled

try:
    from worlds.tracker.TrackerClient import TrackerGameContext as BaseContext, TrackerCommandProcessor as ClientCommandProcessor  # noqa

    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext, ClientCommandProcessor


    class TrackerGameContextMixin:
        """Expecting the TrackerGameContext to have these methods."""

        def build_gui(self, manager):
            ...

        def run_generator(self):
            ...

        def load_kv(self):
            ...


    class BaseContext(CommonContext, TrackerGameContextMixin):
        pass


    tracker_loaded = False

DEBUG = False


class StardewCommandProcessor(ClientCommandProcessor):

    def _cmd_explain(self):
        """Coming soon.™"""
        logger.info("Coming soon.™")


class StardewClientContext(BaseContext):
    game = "Stardew Valley"
    command_processor = StardewCommandProcessor

    def run_gui(self):
        from kvui import GameManager

        class StardewManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Stardew Valley Archipelago Tracking Client"
            ctx: StardewClientContext

            def build(self):
                container = super().build()
                if tracker_loaded:
                    self.ctx.build_gui(self)
                else:
                    logger.info("To enable the tracker page, install Universal Tracker.")

                return container

        self.ui = StardewManager(self)
        if tracker_loaded:
            self.load_kv()

        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(StardewClientContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()


def launch():
    async def main():
        parser = get_base_parser(description="Stardew Valley Archipelago Tracking Client")
        args = parser.parse_args()

        ctx = StardewClientContext(args.connect, args.password)

        if tracker_loaded:
            ctx.run_generator()
        else:
            logger.warning("Could not find Universal Tracker.")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("StardewClient")
    # options = Utils.get_options()

    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
