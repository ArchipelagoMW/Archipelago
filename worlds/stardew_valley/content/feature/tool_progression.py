from abc import ABC
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import cache
from types import MappingProxyType
from typing import ClassVar

from .base import FeatureBase
from ...strings.tool_names import Tool


def to_progressive_item_name(tool: str) -> str:
    """Return the name of the progressive item."""
    return f"Progressive {tool}"


def to_upgrade_location_name(tool: str, material: str) -> str:
    return f"{material} {tool} Upgrade"


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

VANILLA_STARTING_TOOLS_DISTRIBUTION = MappingProxyType({
    Tool.scythe: 1,
    Tool.axe: 1,
    Tool.hoe: 1,
    Tool.pickaxe: 1,
    Tool.pan: 0,
    Tool.trash_can: 1,
    Tool.watering_can: 1,
    Tool.fishing_rod: 0,
})

# Masteries add another tier to the scythe and the fishing rod
SKILL_MASTERIES_TOOL_DISTRIBUTION = MappingProxyType({
    Tool.scythe: 1,
    Tool.fishing_rod: 1,
})


@cache
def get_tools_distribution(progressive_tools_enabled: bool, skill_masteries_enabled: bool, no_starting_tools_enabled: bool) \
        -> tuple[Mapping[str, int], Mapping[str, int]]:
    distribution = Counter(VANILLA_TOOL_DISTRIBUTION)
    starting = Counter(VANILLA_STARTING_TOOLS_DISTRIBUTION)

    if progressive_tools_enabled:
        distribution += PROGRESSIVE_TOOL_DISTRIBUTION

    if skill_masteries_enabled:
        distribution += SKILL_MASTERIES_TOOL_DISTRIBUTION

    if no_starting_tools_enabled:
        distribution += VANILLA_STARTING_TOOLS_DISTRIBUTION
        starting.clear()

    return MappingProxyType(starting), MappingProxyType(distribution)


@dataclass(frozen=True)
class ToolProgressionFeature(FeatureBase, ABC):
    is_progressive: ClassVar[bool]
    starting_tools: Mapping[str, int]
    tool_distribution: Mapping[str, int]

    to_progressive_item_name = staticmethod(to_progressive_item_name)
    to_upgrade_location_name = staticmethod(to_upgrade_location_name)

    def get_tools_distribution(self) -> tuple[Mapping[str, int], Mapping[str, int]]:
        return self.starting_tools, self.tool_distribution


@dataclass(frozen=True)
class ToolProgressionVanilla(ToolProgressionFeature):
    is_progressive = False
    # FIXME change the default_factory to a simple default when python 3.11 is no longer supported
    starting_tools: Mapping[str, int] = field(default_factory=lambda: VANILLA_STARTING_TOOLS_DISTRIBUTION)
    tool_distribution: Mapping[str, int] = field(default_factory=lambda: VANILLA_TOOL_DISTRIBUTION)


class ToolProgressionProgressive(ToolProgressionFeature):
    is_progressive = True
