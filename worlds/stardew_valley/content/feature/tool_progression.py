from abc import ABC
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import cache
from types import MappingProxyType
from typing import ClassVar

from ...strings.tool_names import Tool


def to_progressive_item(tool: str) -> str:
    """Return the name of the progressive item."""
    return f"Progressive {tool}"


# The golden scythe is always randomized
VANILLA_TOOL_DISTRIBUTION = MappingProxyType({
    Tool.scythe: 1,
})

PROGRESSIVE_TOOL_DISTRIBUTION = MappingProxyType({
    Tool.axe: 4,
    Tool.hoe: 4,
    Tool.pickaxe: 4,
    Tool.pan: 4,
    Tool.trash_can: 4,
    Tool.watering_can: 4,
    Tool.fishing_rod: 4,
})

# Masteries add another tier to the scythe and the fishing rod
SKILL_MASTERIES_TOOL_DISTRIBUTION = MappingProxyType({
    Tool.scythe: 1,
    Tool.fishing_rod: 1,
})


@cache
def get_tools_distribution(progressive_tools_enabled: bool, skill_masteries_enabled: bool) -> Mapping[str, int]:
    distribution = Counter(VANILLA_TOOL_DISTRIBUTION)

    if progressive_tools_enabled:
        distribution += PROGRESSIVE_TOOL_DISTRIBUTION

    if skill_masteries_enabled:
        distribution += SKILL_MASTERIES_TOOL_DISTRIBUTION

    return MappingProxyType(distribution)


@dataclass(frozen=True)
class ToolProgressionFeature(ABC):
    is_progressive: ClassVar[bool]
    tool_distribution: Mapping[str, int]

    to_progressive_item = staticmethod(to_progressive_item)


@dataclass(frozen=True)
class ToolProgressionVanilla(ToolProgressionFeature):
    is_progressive = False
    # FIXME change the default_factory to a simple default when python 3.11 is no longer supported
    tool_distribution: Mapping[str, int] = field(default_factory=lambda: VANILLA_TOOL_DISTRIBUTION)


class ToolProgressionProgressive(ToolProgressionFeature):
    is_progressive = True
