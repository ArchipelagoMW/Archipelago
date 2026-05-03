from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from core import ComponentKind, ExecutionMode


@dataclass(slots=True)
class LauncherEntry:
    """Unified launcher view model for backend and utility entries.

    Example::

        entry = LauncherEntry(
            id="text_client",
            display_name="Text Client",
            description="Connect to a room.",
            kind=ComponentKind.CLIENT,
            core_component_id="text_client",
        )
    """

    id: str
    display_name: str
    description: str
    kind: ComponentKind
    icon: str = "icon"
    core_component_id: str | None = None
    launch_mode: ExecutionMode = ExecutionMode.BACKGROUND
    action: Callable[..., str | None] | None = None
