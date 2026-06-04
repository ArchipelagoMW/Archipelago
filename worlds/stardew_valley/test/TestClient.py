"""Pinning tests for StardewCommandProcessor and parse_explanation.

These tests fix the observable behavior of the explain / explain_item /
explain_missing / explain_how / more slash commands in client.py, so a
subsequent refactor that hoists this logic into an abstract base + two
subclasses can be verified input/output-preserving.
"""
from __future__ import annotations

import contextlib
import sys
import types
import unittest


@contextlib.contextmanager
def _scoped_client_import_stubs():
    """Install kvui + worlds.tracker.* stubs in sys.modules, yield, then
    restore the prior state.

    Scope is tight on purpose: stubs only need to exist while client.py is
    being imported for the first time. After that, sys.modules caches the
    real client.py module and later `from ..client import X` lookups don't
    re-resolve its imports. Restoring sys.modules means a later test in the
    same pytest process can import the real kvui / worlds.tracker.* (when
    they exist) without seeing our incomplete stubs.

    - kvui is stubbed because it boots up a Kivy Window on import
      (kvui.py:61 does `from kivy.core.window import Window`), which spawns
      a stray GUI window for every test process. client.py only uses one
      kvui symbol (CommandPromptTextInput) and only as a type annotation
      inside make_gui, so a dummy module satisfies the import without
      dragging in Kivy.

    - worlds.tracker.* is stubbed because the class-body
      `del _cmd_explain / _cmd_explain_missing` block at client.py:148-150
      strips those methods off the class in environments where Universal
      Tracker isn't installed -- which is the case for this fork.
    """
    keys = ("kvui", "worlds.tracker", "worlds.tracker.TrackerClient", "worlds.tracker.TrackerCore")
    saved = {k: sys.modules.get(k) for k in keys}

    if "kvui" not in sys.modules:
        kvui_mod = types.ModuleType("kvui")
        kvui_mod.CommandPromptTextInput = object
        sys.modules["kvui"] = kvui_mod

    if "worlds.tracker.TrackerClient" not in sys.modules:
        from CommonClient import ClientCommandProcessor

        sys.modules["worlds.tracker"] = types.ModuleType("worlds.tracker")

        tc = types.ModuleType("worlds.tracker.TrackerClient")
        tc.TrackerCommandProcessor = ClientCommandProcessor
        tc.TrackerGameContext = object
        tc.UT_VERSION = "test"
        sys.modules["worlds.tracker.TrackerClient"] = tc

        tcore = types.ModuleType("worlds.tracker.TrackerCore")
        tcore.TrackerCore = type
        sys.modules["worlds.tracker.TrackerCore"] = tcore

    try:
        yield
    finally:
        for k, prev in saved.items():
            if prev is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = prev


with _scoped_client_import_stubs():
    from ..client import StardewCommandProcessor, parse_explanation, tracker_loaded  # noqa: E402

from ..stardew_rule.rule_explain import RuleExplanation  # noqa: E402
from .bases import SVTestBase  # noqa: E402

BOGUS = "xxxxxxxxxxxxxxxx-zzzzzzzzzzzzzzz-not-a-real-thing"


class _StubUI:
    def __init__(self) -> None:
        self.printed: list[list[dict]] = []
        self.last_autofillable_command: str | None = None

    def print_json(self, parts) -> None:
        self.printed.append(list(parts))


class _StubCtx:
    """Mimics the StardewClientContext attributes the command processor reads."""

    def __init__(self, world, multiworld, player) -> None:
        self._world = world
        self._multiworld = multiworld
        self._player = player
        self.ui = _StubUI()
        self.outputs: list[str] = []
        self.previous_explanation: RuleExplanation | None = None

    @property
    def logic(self):
        return self._world.logic

    @property
    def current_state(self):
        return self._multiworld.state

    @property
    def all_locations(self):
        return self._multiworld.get_locations(self._player)


@unittest.skipUnless(tracker_loaded, "tracker stubs failed to install before client import")
class TestStardewCommandProcessor(SVTestBase):
    """Pins the observable behavior of every _cmd_* slash command in
    StardewCommandProcessor against a real Stardew Valley world."""

    def setUp(self) -> None:
        super().setUp()
        self.ctx = _StubCtx(self.world, self.multiworld, self.player)
        self.proc = StardewCommandProcessor(self.ctx)
        # ClientCommandProcessor.output forwards to logger.info; redirect to a
        # list so we can assert against it.
        self.proc.output = self.ctx.outputs.append

    # --- success path: command produced a rendered explanation ---

    def test_explain_valid_location(self):
        self.proc._cmd_explain(self._a_location())
        self._assert_emitted_explanation(expected=None)

    def test_explain_close_typo_resolves_via_fuzzy_match(self):
        # one-char typo: Utils.get_intended_text should still resolve usable=True
        self.proc._cmd_explain(self._a_location() + "x")
        self._assert_emitted_explanation(expected=None)

    def test_explain_item_valid(self):
        self.proc._cmd_explain_item(self._an_item())
        self._assert_emitted_explanation(expected=None)

    def test_explain_missing_keeps_expected_true(self):
        # /explain_missing surfaces only unsatisfied rules
        self.proc._cmd_explain_missing(self._a_location())
        self._assert_emitted_explanation(expected=True)

    def test_explain_how_keeps_expected_false(self):
        # /explain_how surfaces only satisfied rules
        self.proc._cmd_explain_how(self._a_location())
        self._assert_emitted_explanation(expected=False)

    # --- failure path: bogus target produces a suggestion + autofill key ---

    def test_bogus_target_emits_suggestion_and_sets_autofill(self):
        cases = [
            (self.proc._cmd_explain, "/explain"),
            (self.proc._cmd_explain_item, "/explain_item"),
            (self.proc._cmd_explain_missing, "/explain_missing"),
            (self.proc._cmd_explain_how, "/explain_how"),
        ]
        for cmd, autofill_key in cases:
            with self.subTest(autofill_key):
                self._reset_captures()
                cmd(BOGUS)
                self.assertEqual(self.ctx.ui.printed, [])
                self.assertEqual(self.ctx.ui.last_autofillable_command, autofill_key)
                self.assertEqual(len(self.ctx.outputs), 1)
                self.assertIsNone(self.ctx.previous_explanation)

    # --- /more drill-down chain ---

    def test_more_with_no_previous_explanation_emits_text_only(self):
        self.proc._cmd_more("")

        self.assertEqual(self.ctx.outputs, ["No previous explanation found."])
        self.assertEqual(self.ctx.ui.printed, [])
        self.assertIsNone(self.ctx.ui.last_autofillable_command)

    def test_more_with_no_index_lists_drill_down_candidates(self):
        prev = self._seed_previous_explanation_with_drill_down()
        if prev is None:
            self.skipTest("no location in this seed produces drill-down candidates")
        self._reset_captures()

        self.proc._cmd_more("")

        self.assertEqual(self.ctx.ui.printed, [])
        self.assertEqual(self.ctx.ui.last_autofillable_command, "/more")
        # header line + one per candidate
        self.assertEqual(len(self.ctx.outputs), 1 + len(prev.more_explanations))
        for line in self.ctx.outputs[1:]:
            self.assertTrue(line.startswith("/more "))

    def test_more_with_index_drills_into_sub_rule(self):
        prev = self._seed_previous_explanation_with_drill_down()
        if prev is None:
            self.skipTest("no location in this seed produces drill-down candidates")
        self._reset_captures()

        self.proc._cmd_more("0")

        self.assertEqual(len(self.ctx.ui.printed), 1)
        self.assertIsNotNone(self.ctx.previous_explanation)
        self.assertIsNot(self.ctx.previous_explanation, prev)

    def test_more_with_invalid_index_falls_back_to_listing(self):
        prev = self._seed_previous_explanation_with_drill_down()
        if prev is None:
            self.skipTest("no location in this seed produces drill-down candidates")
        self._reset_captures()

        self.proc._cmd_more("9999")

        self.assertEqual(self.ctx.ui.printed, [])
        self.assertEqual(self.ctx.ui.last_autofillable_command, "/more")

    # --- helpers ---

    def _a_location(self) -> str:
        return sorted(loc.name for loc in self.multiworld.get_locations(self.player))[0]

    def _an_item(self) -> str:
        return sorted(self.world.logic.registry.item_rules.keys())[0]

    def _assert_emitted_explanation(self, expected: bool | None) -> None:
        """Asserts the success-path observable contract: one print_json call
        with a non-empty list of typed message-part dicts, a RuleExplanation
        stored as previous_explanation whose `expected` field matches, and
        no plain output or autofill side effects."""
        self.assertEqual(len(self.ctx.ui.printed), 1, "expected exactly one print_json call")
        parts = self.ctx.ui.printed[0]
        self.assertGreater(len(parts), 0)
        for part in parts:
            self.assertIsInstance(part, dict)
            self.assertIn("type", part)
            self.assertIn("text", part)
        self.assertIsInstance(self.ctx.previous_explanation, RuleExplanation)
        self.assertEqual(self.ctx.previous_explanation.expected, expected)
        self.assertIsNone(self.ctx.ui.last_autofillable_command)
        self.assertEqual(self.ctx.outputs, [])

    def _reset_captures(self) -> None:
        """Clear capture buffers between calls. Does NOT touch
        previous_explanation so post-seed resets stay safe for /more tests."""
        self.ctx.ui.printed.clear()
        self.ctx.ui.last_autofillable_command = None
        self.ctx.outputs.clear()

    def _seed_previous_explanation_with_drill_down(self) -> RuleExplanation | None:
        """Walk locations in name order until /explain produces a previous
        explanation with a non-empty more_explanations list. Returns it (or
        None if no such location exists under this seed)."""
        for loc_name in sorted(loc.name for loc in self.multiworld.get_locations(self.player)):
            self._reset_captures()
            self.ctx.previous_explanation = None
            self.proc._cmd_explain(loc_name)
            prev = self.ctx.previous_explanation
            if prev is None:
                continue
            _ = prev.explained_sub_rules  # populate lazy more_explanations
            if prev.more_explanations:
                return prev
        return None


class TestParseExplanation(unittest.TestCase):
    """Direct unit tests of parse_explanation's tokenizer.

    We feed it RuleExplanation-shaped stand-ins whose __str__ produces a known
    string, so the tokenizer's behavior is pinned independently of which
    rules are in play at any seed.
    """

    @staticmethod
    def _expl(s: str):
        class _FakeExplanation:
            def __str__(self_inner) -> str:
                return s
        return _FakeExplanation()

    def test_true_renders_as_green(self):
        self.assertIn({"type": "color", "color": "green", "text": "True"},
                      parse_explanation(self._expl("True")))

    def test_false_renders_as_salmon(self):
        self.assertIn({"type": "color", "color": "salmon", "text": "False"},
                      parse_explanation(self._expl("False")))

    def test_typed_name_tokens(self):
        cases = [
            ("Reach Location Beach", "Reach Location ", "location_name", "Beach"),
            ("Reach Entrance Bus Stop", "Reach Entrance ", "entrance_name", "Bus Stop"),
            ("Received event Spring", "Received event ", "item_name", "Spring"),
        ]
        for src, prefix, typed, name in cases:
            with self.subTest(src):
                parts = parse_explanation(self._expl(src))
                shape = [(p.get("type"), p.get("text")) for p in parts]
                self.assertIn(("text", prefix), shape)
                self.assertIn((typed, name), shape)

    def test_reach_region_emits_yellow_color_token(self):
        self.assertIn({"type": "color", "color": "yellow", "text": "Farm"},
                      parse_explanation(self._expl("Reach Region Farm")))

    def test_received_item_emits_flagged_item_name_token(self):
        parts = parse_explanation(self._expl("Received Stardrop"))
        item_parts = [p for p in parts if p.get("type") == "item_name"]
        self.assertEqual(len(item_parts), 1)
        self.assertEqual(item_parts[0]["text"], "Stardrop")
        self.assertEqual(item_parts[0]["flags"], 0b001)

    def test_has_with_count_splits_digit_into_cyan_token(self):
        parts = parse_explanation(self._expl("Has 3 Stardrop"))
        shape = [(p.get("type"), p.get("text"), p.get("color")) for p in parts]
        self.assertIn(("text", "Has ", None), shape)
        self.assertIn(("color", "3", "cyan"), shape)
