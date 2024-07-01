from __future__ import annotations

import asyncio

from CommonClient import logger, get_base_parser, gui_enabled
from . import StardewLogic
from .stardew_rule.rule_explain import explain

try:
    from worlds.tracker.TrackerClient import TrackerGameContext as BaseContext, TrackerCommandProcessor as ClientCommandProcessor  # noqa

    tracker_loaded = True
except ImportError:
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


class StardewCommandProcessor(ClientCommandProcessor):
    ctx: StardewClientContext

    def _cmd_explain(self, item):
        """Coming soon.™"""
        if self.ctx.logic is None:
            logger.warning("Internal logic was not able to load, check your yamls and relaunch.")
            return

        rule = self.ctx.logic.has(item)
        expl = explain(rule, self.ctx.multiworld.state)
        logger.info(expl)

    def _cmd_explain_missing(self, item):
        """Coming soon.™"""
        if self.ctx.logic is None:
            logger.warning("Internal logic was not able to load, check your yamls and relaunch.")
            return

        rule = self.ctx.logic.has(item)
        state = self.ctx.multiworld.state
        simplified, _ = rule.evaluate_while_simplifying(state)
        expl = explain(simplified, state)
        logger.info(expl)

    if not tracker_loaded:
        del _cmd_explain
        del _cmd_explain_missing


class StardewClientContext(BaseContext):
    game = "Stardew Valley"
    command_processor = StardewCommandProcessor
    logic: StardewLogic = None

    def run_gui(self):
        from kvui import GameManager

        class StardewManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Stardew Valley Archipelago Tracker"
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

    def setup_logic(self):
        if self.multiworld is not None:
            self.logic = self.multiworld.worlds[self.player_id].logic

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(StardewClientContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()


def launch():
    async def main():
        parser = get_base_parser(description="Stardew Valley Archipelago Tracker")
        args = parser.parse_args()

        ctx = StardewClientContext(args.connect, args.password)

        if tracker_loaded:
            ctx.run_generator()
            # FIXME that's probably not legit, but it works when there is only one player
            if ctx.player_id is None:
                ctx.player_id = 1
            ctx.setup_logic()
        else:
            logger.warning("Could not find Universal Tracker.")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
