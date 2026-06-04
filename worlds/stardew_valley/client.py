from __future__ import annotations

import asyncio
import re
import typing
# webserver imports
import urllib.parse
from collections.abc import Iterable

import Utils
from BaseClasses import CollectionState, Location
from CommonClient import logger, get_base_parser, gui_enabled, server_loop
from MultiServer import mark_raw
from NetUtils import JSONMessagePart
from . import StardewValleyWorld
from .logic.logic import StardewLogic
from .stardew_rule.rule_explain import explain, ExplainMode, RuleExplanation

# kvui boots up a Kivy Window on import (kvui.py:61). Only the custom-client
# launcher path (StardewClientContext.make_gui) actually needs it; tests and
# the Universal Tracker world hooks don't. Keep this under TYPE_CHECKING so
# importing client.py never spawns a stray window. With
# `from __future__ import annotations`, the type annotation referencing
# CommandPromptTextInput is never evaluated at runtime.
if typing.TYPE_CHECKING:
    from kvui import CommandPromptTextInput

try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION  # noqa
    from worlds.tracker.TrackerCore import TrackerCore

    tracker_loaded = True
except ImportError as e:
    logger.error(e)
    from CommonClient import CommonContext, ClientCommandProcessor

    TrackerCore = object


    class TrackerGameContextMixin:
        """Expecting the TrackerGameContext to have these methods."""
        tracker_core: TrackerCore

        def make_gui(self, manager):
            ...

        def run_generator(self):
            ...


    class TrackerGameContext(CommonContext, TrackerGameContextMixin):
        pass


    tracker_loaded = False
    UT_VERSION = "Not found"


class StardewCommandProcessor(ClientCommandProcessor):
    """The custom Stardew Tracker launcher's slash-command processor.

    Data access is funneled through small `_get_*` / `_set_*` / `_print_json`
    / `_set_autofillable_command` helpers so that StardewUTCommandProcessor
    (below) can swap them for World-instance access and buffered JSON output
    when called from Universal Tracker's `/explain` and `/explain_more` world
    hooks -- without copying the `_cmd_*` bodies.

    The class attribute `more_command` controls which command name gets
    rendered in drill-down hints ("[use `/more 0` to explain]" vs
    "[use `/explain_more 0` to explain]"). StardewUTCommandProcessor
    overrides it.
    """
    ctx: StardewClientContext
    more_command: str = "/more"

    @mark_raw
    def _cmd_explain(self, location: str = ""):
        """Explain the logic behind a location."""
        logic = self._get_logic()
        if logic is None:
            return

        try:
            rule = logic.region.can_reach_location(location)
            expl = explain(rule, self._get_current_state(), expected=None, mode=ExplainMode.CLIENT, more_command=self.more_command)
        except KeyError:

            result, usable, response = Utils.get_intended_text(location, [loc.name for loc in self._get_all_locations()])
            if usable:
                rule = logic.region.can_reach_location(result)
                expl = explain(rule, self._get_current_state(), expected=None, mode=ExplainMode.CLIENT, more_command=self.more_command)
            else:
                self._set_autofillable_command("/explain")
                self.output(response)
                return

        self._set_previous_explanation(expl)
        self._print_json(parse_explanation(expl))

    @mark_raw
    def _cmd_explain_item(self, item: str = ""):
        """Explain the logic behind a game item."""
        logic = self._get_logic()
        if logic is None:
            return

        result, usable, response = Utils.get_intended_text(item, logic.registry.item_rules.keys())
        if usable:
            rule = logic.has(result)
            expl = explain(rule, self._get_current_state(), expected=None, mode=ExplainMode.CLIENT, more_command=self.more_command)
        else:
            self._set_autofillable_command("/explain_item")
            self.output(response)
            return

        self._set_previous_explanation(expl)
        self._print_json(parse_explanation(expl))

    @mark_raw
    def _cmd_explain_missing(self, location: str = ""):
        """Explain what is missing for a location to be in logic. It explains the logic behind a location, while skipping the rules that are already satisfied."""
        self.__explain("/explain_missing", location, expected=True)

    @mark_raw
    def _cmd_explain_how(self, location: str = ""):
        """Explain how a location is in logic. It explains the logic behind the location, while skipping the rules that are not satisfied."""
        self.__explain("/explain_how", location, expected=False)

    def __explain(self, command: str, location: str, expected: bool | None = None):
        logic = self._get_logic()
        if logic is None:
            return

        try:
            rule = logic.region.can_reach_location(location)
            expl = explain(rule, self._get_current_state(), expected=expected, mode=ExplainMode.CLIENT, more_command=self.more_command)
        except KeyError:

            result, usable, response = Utils.get_intended_text(location, [loc.name for loc in self._get_all_locations()])
            if usable:
                rule = logic.region.can_reach_location(result)
                expl = explain(rule, self._get_current_state(), expected=expected, mode=ExplainMode.CLIENT, more_command=self.more_command)
            else:
                self._set_autofillable_command(command)
                self.output(response)
                return

        self._set_previous_explanation(expl)
        self._print_json(parse_explanation(expl))

    @mark_raw
    def _cmd_more(self, index: str = ""):
        """Will tell you what's missing to consider a location in logic."""
        previous = self._get_previous_explanation()
        if previous is None:
            self.output("No previous explanation found.")
            return

        try:
            expl = previous.more(int(index))
        except (ValueError, IndexError):
            self.output("Which previous rule do you want to explained?")
            self._set_autofillable_command(self.more_command)
            for i, rule in enumerate(previous.more_explanations):
                # TODO handle autofillable commands
                self.output(f"{self.more_command} {i} -> {str(rule)})")
            return

        self._set_previous_explanation(expl)
        self._print_json(parse_explanation(expl))

    # --- data-access helpers: defaults are ctx-based (custom-client path); ---
    # --- StardewUTCommandProcessor overrides these for the UT hook path.   ---

    def _get_logic(self) -> StardewLogic | None:
        return self.ctx.logic

    def _get_current_state(self) -> CollectionState:
        return self.ctx.current_state

    def _get_all_locations(self) -> Iterable[Location]:
        return self.ctx.all_locations

    def _get_previous_explanation(self) -> RuleExplanation | None:
        return self.ctx.previous_explanation

    def _set_previous_explanation(self, expl: RuleExplanation | None) -> None:
        self.ctx.previous_explanation = expl

    def _print_json(self, parts: list[JSONMessagePart]) -> None:
        self.ctx.ui.print_json(parts)

    def _set_autofillable_command(self, command: str | None) -> None:
        self.ctx.ui.last_autofillable_command = command

    if not tracker_loaded:
        del _cmd_explain
        del _cmd_explain_missing


class StardewUTCommandProcessor(StardewCommandProcessor):
    """Universal Tracker variant: constructed per-call by StardewValleyWorld's
    `explain_rule` and `explain_more` hooks.

    Reads from the World instance plus the CollectionState UT passes in, and
    buffers JSON output into `self.buffered_parts` for the hook to return.
    Drill-down state for /explain_more lives on the World instance so it
    survives across hook calls.
    """

    more_command: str = "/explain_more"

    def __init__(self, world: StardewValleyWorld, state: CollectionState) -> None:
        # Intentionally bypass ClientCommandProcessor.__init__ -- that wants a
        # CommonContext and we don't have (or need) one in the UT hook path.
        self.world = world
        self.state = state
        self.buffered_parts: list[JSONMessagePart] = []

    def output(self, text: str) -> None:
        # ClientCommandProcessor.output forwards to logger.info, which UT
        # users never see. Buffer plain text as a text-typed JSONMessagePart
        # instead so the hook return value carries it back to UT for rendering.
        self.buffered_parts.append({"type": "text", "text": text})

    def _get_logic(self) -> StardewLogic | None:
        return self.world.logic

    def _get_current_state(self) -> CollectionState:
        return self.state

    def _get_all_locations(self) -> Iterable[Location]:
        return self.world.multiworld.get_locations(self.world.player)

    def _get_previous_explanation(self) -> RuleExplanation | None:
        return getattr(self.world, "_ut_previous_explanation", None)

    def _set_previous_explanation(self, expl: RuleExplanation | None) -> None:
        self.world._ut_previous_explanation = expl

    def _print_json(self, parts: list[JSONMessagePart]) -> None:
        self.buffered_parts.extend(parts)

    def _set_autofillable_command(self, command: str | None) -> None:
        # UT's generic UI doesn't expose an autofill hook to worlds; the
        # suggestion text emitted via output() already conveys the hint.
        pass


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

                # Until self.ctx.ui.last_autofillable_command allows for / commands, this is needed to remove the "!" before the /commands when using intended text autofill.
                def on_text_remove_hardcoded_exclamation_mark_garbage(textinput: CommandPromptTextInput, text: str) -> None:
                    if text.startswith("!/"):
                        textinput.text = text[1:]

                self.textinput.bind(text=on_text_remove_hardcoded_exclamation_mark_garbage)

                return container

        return StardewManager

    @property
    def logic(self) -> StardewLogic | None:
        if self.tracker_core.get_current_world() is None:
            logger.warning("Internal logic was not able to load, check your yamls and relaunch.")
            return None

        if self.game != "Stardew Valley":
            logger.warning(f"Please connect to a slot with explainable logic (not {self.game}).")
            return None

        return self.tracker_core.get_current_world().logic

    @property
    def current_state(self) -> CollectionState:
        return self.tracker_core.updateTracker().state

    @property
    def world(self) -> StardewValleyWorld:
        return self.tracker_core.get_current_world()

    @property
    def all_locations(self) -> Iterable[Location]:
        return self.tracker_core.multiworld.get_locations(self.tracker_core.player_id)


def parse_explanation(explanation: RuleExplanation) -> list[JSONMessagePart]:
    # Split the explanation in parts, by isolating all the delimiters, being \(, \), & , -> , | , \d+x , \[ , \] , \(\w+\), \n\s*
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
