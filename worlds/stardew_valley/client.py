from __future__ import annotations

import asyncio
import re
# webserver imports
import urllib.parse
from collections import Counter

import Utils
from BaseClasses import MultiWorld, CollectionState, ItemClassification
from CommonClient import logger, get_base_parser, gui_enabled, server_loop
from MultiServer import mark_raw
from NetUtils import JSONMessagePart
from .logic.logic import StardewLogic
from .stardew_rule.rule_explain import explain, ExplainMode, RuleExplanation

try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION  # noqa

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
        if self.ctx.logic is None:
            logger.warning("Internal logic was not able to load, check your yamls and relaunch.")
            return

        try:
            rule = self.ctx.logic.region.can_reach_location(location)
            expl = explain(rule, get_updated_state(self.ctx), expected=None, mode=ExplainMode.CLIENT)
        except KeyError:

            result, usable, response = Utils.get_intended_text(location, [loc.name for loc in self.ctx.multiworld.get_locations(1)])
            if usable:
                rule = self.ctx.logic.region.can_reach_location(result)
                expl = explain(rule, get_updated_state(self.ctx), expected=None, mode=ExplainMode.CLIENT)
            else:
                logger.warning(response)
                return

        self.ctx.previous_explanation = expl
        logger.info(str(expl).strip())

    @mark_raw
    def _cmd_explain_item(self, item: str = ""):
        """Explain the logic behind a game item."""
        if self.ctx.logic is None:
            logger.warning("Internal logic was not able to load, check your yamls and relaunch.")
            return

        result, usable, response = Utils.get_intended_text(item, self.ctx.logic.registry.item_rules.keys())
        if usable:
            rule = self.ctx.logic.has(result)
            expl = explain(rule, get_updated_state(self.ctx), expected=None, mode=ExplainMode.CLIENT)
        else:
            logger.warning(response)
            return

        self.ctx.previous_explanation = expl
        logger.info(str(expl).strip())

    @mark_raw
    def _cmd_explain_missing(self, location: str = ""):
        """Explain the logic behind a location, while skipping the rules that are already satisfied."""
        if self.ctx.logic is None:
            logger.warning("Internal logic was not able to load, check your yamls and relaunch.")
            return

        try:
            rule = self.ctx.logic.region.can_reach_location(location)
            state = get_updated_state(self.ctx)
            simplified, _ = rule.evaluate_while_simplifying(state)
            expl = explain(simplified, state, mode=ExplainMode.CLIENT)
        except KeyError:

            result, usable, response = Utils.get_intended_text(location, [loc.name for loc in self.ctx.multiworld.get_locations(1)])
            if usable:
                rule = self.ctx.logic.region.can_reach_location(result)
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

        logger.info(str(expl).strip())

    if not tracker_loaded:
        del _cmd_explain
        del _cmd_explain_missing


class StardewClientContext(TrackerGameContext):
    game = "Stardew Valley"
    command_processor = StardewCommandProcessor
    logic: StardewLogic | None = None
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

    def setup_logic(self):
        if self.multiworld is not None:
            self.logic = self.multiworld.worlds[1].logic


def parse_explanation(explanation: RuleExplanation) -> list[JSONMessagePart]:
    result_regex = r"(\(|\)| & | -> | \| | \[.*\]\s*| \(\w+\)|\n\s*)"
    splits = re.split(result_regex, str(explanation))

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
            messages.append({"type": "item_name", "text": s[9:]})
        elif s.startswith(" ["):
            if len(s) <= 50:
                messages.append({"type": "text", "text": s})
            else:
                messages.append({"type": "text", "text": " [ ... ] "})
        else:
            messages.append({"text": s, "type": "text"})

    return messages


# Don't mind me I just copy-pasted that from UT because it was too complicated to access their updated state.
def get_updated_state(ctx: TrackerGameContext) -> CollectionState:
    if ctx.player_id is None or ctx.multiworld is None:
        logger.error("Player YAML not installed or Generator failed")
        ctx.log_to_tab("Check Player YAMLs for error", False)
        ctx.tracker_failed = True
        raise ValueError("Player YAML not installed or Generator failed")

    state = CollectionState(ctx.multiworld)
    state.sweep_for_advancements(
        locations=(location for location in ctx.multiworld.get_locations() if (not location.address)))
    prog_items = Counter()
    all_items = Counter()

    item_id_to_name = ctx.multiworld.worlds[ctx.player_id].item_id_to_name
    for item_name in [item_id_to_name[item[0]] for item in ctx.items_received] + ctx.manual_items:
        try:
            world_item = ctx.multiworld.create_item(item_name, ctx.player_id)
            state.collect(world_item, True)
            if world_item.classification == ItemClassification.progression or world_item.classification == ItemClassification.progression_skip_balancing:
                prog_items[world_item.name] += 1
            if world_item.code is not None:
                all_items[world_item.name] += 1
        except:
            ctx.log_to_tab("Item id " + str(item_name) + " not able to be created", False)
    state.sweep_for_advancements(
        locations=(location for location in ctx.multiworld.get_locations() if (not location.address)))

    return state


async def main(args):
    ctx = StardewClientContext(args.connect, args.password)

    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if tracker_loaded:
        ctx.run_generator()
        ctx.setup_logic()
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
