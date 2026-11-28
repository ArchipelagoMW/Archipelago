from dataclasses import dataclass, field
from functools import cached_property
from typing import Optional, Tuple

from .game_item import Source


def get_tool_upgrade_name(tool_name: str, tool_material: str) -> str:
    return f"{tool_material} {tool_name}"


@dataclass(frozen=True)
class ToolUpgrade:
    tool_name: str
    sources: Tuple[Source, ...] = field(kw_only=True)
    upgrade_from: Optional[str] = field(default=None, kw_only=True)
    tool_material: str = None
    full_name: str = None

    @cached_property
    def tool_upgrade_name(self):
        if self.full_name:
            return self.full_name
        return get_tool_upgrade_name(self.tool_name, self.tool_material)

    @cached_property
    def is_upgrade(self) -> bool:
        return self.upgrade_from is not None


@dataclass(frozen=True, kw_only=True)
class StartingToolSource(Source):

    def __repr__(self):
        return f"Starting Tool Source"
