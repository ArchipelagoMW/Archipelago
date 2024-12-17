from __future__ import annotations

import asyncio
import re
# webserver imports
import urllib.parse

import Utils
from BaseClasses import MultiWorld, CollectionState
from CommonClient import logger, get_base_parser, gui_enabled, server_loop
from MultiServer import mark_raw
from NetUtils import JSONMessagePart
from .logic.logic import StardewLogic
from .stardew_rule.rule_explain import explain, ExplainMode, RuleExplanation

try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION, updateTracker  # noqa

    tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext, ClientCommandProcessor


    class TrackerGameContextMixin:
        """Expecting the TrackerGameContext to have these methods."""
        multiworld: MultiWorld
        player_id: int

        def build_gui(self, manager):
            ...

        def run_generator(self):
            ...

        def load_kv(self):
            ...


    class TrackerGameContext(CommonContext, TrackerGameContextMixin):
        pass


    tracker_loaded = False
    UT_VERSION = "Not found"


class StardewCommandProcessor(ClientCommandProcessor):
    ctx: StardewClientContext

    @mark_raw
    def _cmd_explain(self, location: str = ""):
        """Explain the logic behind a location."""
        logic = self.ctx.get_logic()
        if logic is None:
            return

        try:
            rule = logic.region.can_reach_location(location)
            expl = explain(rule, get_updated_state(self.ctx), expected=None, mode=ExplainMode.CLIENT)
        except KeyError:

            result, usable, response = Utils.get_intended_text(location, [loc.name for loc in self.ctx.multiworld.get_locations(1)])
            if usable:
                rule = logic.region.can_reach_location(result)
                expl = explain(rule, get_updated_state(self.ctx), expected=None, mode=ExplainMode.CLIENT)
            else:
                logger.warning(response)
                return

        self.ctx.previous_explanation = expl
        self.ctx.ui.print_json(parse_explanation(expl))

    @mark_raw
    def _cmd_explain_item(self, item: str = ""):
        """Explain the logic behind a game item."""
        logic = self.ctx.get_logic()
        if logic is None:
            return

        result, usable, response = Utils.get_intended_text(item, logic.registry.item_rules.keys())
        if usable:
            rule = logic.has(result)
            expl = explain(rule, get_updated_state(self.ctx), expected=None, mode=ExplainMode.CLIENT)
        else:
            logger.warning(response)
            return

        self.ctx.previous_explanation = expl
        self.ctx.ui.print_json(parse_explanation(expl))

    @mark_raw
    def _cmd_explain_missing(self, location: str = ""):
        """Explain the logic behind a location, while skipping the rules that are already satisfied."""
        logic = self.ctx.get_logic()
        if logic is None:
            return
        try:
            rule = logic.region.can_reach_location(location)
            state = get_updated_state(self.ctx)
            simplified, _ = rule.evaluate_while_simplifying(state)
            expl = explain(simplified, state, mode=ExplainMode.CLIENT)
        except KeyError:

            result, usable, response = Utils.get_intended_text(location, [loc.name for loc in self.ctx.multiworld.get_locations(1)])
            if usable:
                rule = logic.region.can_reach_location(result)
                state = get_updated_state(self.ctx)
                simplified, _ = rule.evaluate_while_simplifying(state)
                expl = explain(simplified, state, mode=ExplainMode.CLIENT)
            else:
                logger.warning(response)
                return

        self.ctx.previous_explanation = expl
        self.ctx.ui.print_json(parse_explanation(expl))

    @mark_raw
    def _cmd_more(self, index: str = ""):
        """Will tell you what's missing to consider a location in logic."""
        if self.ctx.previous_explanation is None:
            logger.warning("No previous explanation found.")
            return

        try:
            expl = self.ctx.previous_explanation.more(int(index))
        except (ValueError, IndexError):
            logger.info("Which previous rule do you want to explained?")
            for i, rule in enumerate(self.ctx.previous_explanation.more_explanations):
                logger.info(f"/more {i} -> {str(rule)})")
            return

        self.ctx.previous_explanation = expl
        self.ctx.ui.print_json(parse_explanation(expl))

    if not tracker_loaded:
        del _cmd_explain
        del _cmd_explain_missing


class StardewClientContext(TrackerGameContext):
    game = "Stardew Valley"
    command_processor = StardewCommandProcessor
    previous_explanation: RuleExplanation | None = None

    def make_gui(self):
        ui = super().make_gui()  # before the kivy imports so kvui gets loaded first

        class StardewManager(ui):
            base_title = f"Stardew Valley Tracker with UT {UT_VERSION} for AP version"  # core appends ap version so this works
            ctx: StardewClientContext

            def build(self):
                container = super().build()
                if not tracker_loaded:
                    logger.info("To enable the tracker page, install Universal Tracker.")

                return container

        return StardewManager

    def get_logic(self) -> StardewLogic | None:
        if self.player_id is None:
            logger.warning("Internal logic was not able to load, check your yamls and relaunch.")
            return

        if self.game != "Stardew Valley":
            logger.warning(f"Please connect to a slot with explainable logic (not {self.game}).")
            return

        return self.multiworld.worlds[self.player_id].logic


def parse_explanation(explanation: RuleExplanation) -> list[JSONMessagePart]:
    result_regex = r"(\(|\)| & | -> | \| |\d+x | \[|\](?: ->)?\s*| \(\w+\)|\n\s*)"
    splits = re.split(result_regex, str(explanation).strip())

    messages = []
    for s in splits:
        if len(s) == 0:
            continue

        if s == "True":
            messages.append({"type": "color", "color": "green", "text": s})
        elif s == "False":
            messages.append({"type": "color", "color": "salmon", "text": s})
        elif s.startswith("Reach Location "):
            messages.append({"type": "text", "text": "Reach Location "})
            messages.append({"type": "location_name", "text": s[15:]})
        elif s.startswith("Reach Entrance "):
            messages.append({"type": "text", "text": "Reach Entrance "})
            messages.append({"type": "entrance_name", "text": s[15:]})
        elif s.startswith("Reach Region "):
            messages.append({"type": "text", "text": "Reach Region "})
            messages.append({"type": "color", "color": "yellow", "text": s[13:]})
        elif s.startswith("Received event "):
            messages.append({"type": "text", "text": "Received event "})
            messages.append({"type": "item_name", "text": s[15:]})
        elif s.startswith("Received "):
            messages.append({"type": "text", "text": "Received "})
            messages.append({"type": "item_name", "flags": 0b001, "text": s[9:]})
        elif s.startswith("Has "):
            if s[4].isdigit():
                messages.append({"type": "text", "text": "Has "})
                digit_end = re.search(r"\D", s[4:])
                digit = s[4:4 + digit_end.start()]
                messages.append({"type": "color", "color": "cyan", "text": digit})
                messages.append({"type": "text", "text": s[4 + digit_end.start():]})

            else:
                messages.append({"text": s, "type": "text"})
        else:
            messages.append({"text": s, "type": "text"})

    return messages


def get_updated_state(ctx: TrackerGameContext) -> CollectionState:
    return updateTracker(ctx).state


async def main(args):
    ctx = StardewClientContext(args.connect, args.password)

    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if tracker_loaded:
        ctx.run_generator()
    else:
        logger.warning("Could not find Universal Tracker.")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch(*args):
    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    asyncio.run(main(args))
