import logging
import re
import tempfile
from pathlib import Path
from typing import Callable, Iterable

from ..AoE2ScenarioParser import settings
from ..AoE2ScenarioParser.datasets.effects import EffectId
from ..AoE2ScenarioParser.datasets.object_support import StartingAge
from ..AoE2ScenarioParser.datasets.players import PlayerId
from ..AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario
from ..locations.Locations import Age2ScenarioLocationData

settings.PRINT_STATUS_UPDATES = False
settings.ENABLE_XS_CHECK_INTEGRATION = False

logger = logging.getLogger("Client")

Step = Callable[[AoE2DEScenario], bool]

CALL_REGEX = re.compile(r"([A-Za-z_]\w*)\s*\(\s*\)")
def effect_script_call(effect) -> set[str]:
    return set(CALL_REGEX.findall(effect.message or ""))

def trigger_calls_xs_script(trigger) -> set[str]:
    triggers = set()
    for effect in trigger.effects:
        if effect.effect_type == EffectId.SCRIPT_CALL:
            triggers |= effect_script_call(effect)
    return triggers

def disable_triggers(disabled: Iterable[Age2ScenarioLocationData]) -> Step:
    disabled_trigger_calls = frozenset(location.trigger_call for location in disabled)

    def step(scenario: AoE2DEScenario) -> bool:
        changed = False
        for trigger in scenario.trigger_manager.triggers:
            if not trigger.enabled:
                continue
            if not trigger_calls_xs_script(trigger).isdisjoint(disabled_trigger_calls):
                trigger.enabled = 0
                changed = True
        return changed
    return step

def rebase_to_dark(scenario: AoE2DEScenario) -> bool:
    player = scenario.player_manager.players[PlayerId.ONE]
    if player.starting_age == StartingAge.DARK_AGE:
        return False
    player.starting_age = StartingAge.DARK_AGE
    return True

def _object_classes() -> list[type]:
    # The parser's own modules import it as the top-level AoE2ScenarioParser, which its vendored
    # __init__ registers - so the classes it reads into are those, not this package's relative ones.
    from AoE2ScenarioParser.objects.aoe2_object import AoE2Object
    found, todo = [], [AoE2Object]
    while todo:
        cls = todo.pop()
        found.append(cls)
        todo += cls.__subclasses__()
    return found

def restore_unsupported_properties() -> None:
    """The parser disables a property a scenario's version lacks by replacing it on the class, so
    it stays disabled for every scenario read after (its own TODO in retriever_object_link): a 1.59
    scenario read after a 1.58 one can't write its units' capture flags. Put each one back before
    the next scenario is read; that scenario disables what it lacks again."""
    from AoE2ScenarioParser.sections.retrievers.retriever_object_link import RetrieverObjectLink
    from AoE2ScenarioParser.sections.retrievers.retriever_object_link_group import RetrieverObjectLinkGroup
    for cls in _object_classes():
        for link in cls.__dict__.get("_link_list", ()):
            for each in (link.group if isinstance(link, RetrieverObjectLinkGroup) else [link]):
                if not isinstance(each, RetrieverObjectLink) or not each.disabled:
                    continue
                target = each.destination_object or cls
                if isinstance(target.__dict__.get(each.name), property):
                    delattr(target, each.name)
                each.disabled = False

def apply(body: bytes, steps: Iterable[Step], name: str = "",
          progress: tuple[int, int] = (0, 0), report: Callable[[str], None] = None) -> bytes:
    steps = tuple(steps)
    if not steps:
        return body
    done, total = progress
    percent = round(done * 100 / total) if total else 100
    (report or logger.info)(f"Parsing {name} ........ {percent}%")
    with tempfile.TemporaryDirectory() as folder:
        source = Path(folder, "in.aoe2scenario")
        source.write_bytes(body)
        restore_unsupported_properties()
        scenario: AoE2DEScenario = AoE2DEScenario.from_file(str(source))
        changed = [step(scenario) for step in steps]
        if not any(changed):
            return body
        target = Path(folder, "out.aoe2scenario")
        scenario.write_to_file(str(target))
        return target.read_bytes()
