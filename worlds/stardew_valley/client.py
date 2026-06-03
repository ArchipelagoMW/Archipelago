from __future__ import annotations

import re

import Utils
from BaseClasses import CollectionState, Location
from NetUtils import JSONMessagePart
from . import StardewValleyWorld
from .logic.logic import StardewLogic
from .stardew_rule.rule_explain import explain, ExplainMode, RuleExplanation

try:
    from worlds.tracker.TrackerClient import TrackerGameContext, TrackerCommandProcessor as ClientCommandProcessor, UT_VERSION  # noqa
    from worlds.tracker.TrackerCore import TrackerCore

    tracker_loaded = True
except ImportError as e:
    tracker_loaded = False
    UT_VERSION = "Not found"


def cmd_explain(world: StardewValleyWorld, target_name: str, state: CollectionState) -> list[JSONMessagePart]:
    logic = world.logic

    if target_name.startswith("item "):
        is_item_explain = True
        target_name = target_name[len("item "):]
    else:
        is_item_explain = False

    if target_name.startswith("missing "):
        expected = True
        target_name = target_name[len("missing "):]
    elif target_name.startswith("how "):
        expected = False
        target_name = target_name[len("how "):]
    else:
        expected = None

    possible_answers = logic.registry.item_rules.keys() if is_item_explain else world.get_all_location_names()
    result, usable, response = Utils.get_intended_text(target_name, possible_answers)
    if usable:
        if is_item_explain:
            rule = logic.has(result)
        else:
            rule = logic.region.can_reach_location(result)
        expl = explain(rule, state, expected=expected, mode=ExplainMode.CLIENT)
        world.previous_explanation = expl
        return parse_explanation(expl)
    else:
        return [{"type": "color", "color": "salmon", "text": response}]


def cmd_more(world: StardewValleyWorld, index: str, state: CollectionState) -> list[JSONMessagePart]:
    logic = world.logic

    if world.previous_explanation is None:
        return [{"type": "color", "color": "salmon", "text": "No previous explanation found"}]

    try:
        expl = world.previous_explanation.more(int(index))
    except (ValueError, IndexError):
        return [{"type": "text", "text": "Which previous rule do you want to be explained?"}]

    world.previous_explanation = expl
    return parse_explanation(expl)


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
