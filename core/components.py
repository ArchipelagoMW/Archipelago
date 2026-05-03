from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ComponentKind(str, Enum):
    """Stable component group names used by adapters."""

    TOOL = "tool"
    MISC = "misc"
    CLIENT = "client"
    ADJUSTER = "adjuster"
    HIDDEN = "hidden"


class ExecutionMode(str, Enum):
    """Execution behavior requested for a component run."""

    DIRECT = "direct"
    BACKGROUND = "background"
    TERMINAL = "terminal"


class HandlerId(str, Enum):
    """Stable handler identifiers used by the component executor."""

    PROCESS = "process"
    HOST = "host"
    INSTALL_APWORLD = "install_apworld"
    EXPORT_DATAPACKAGE = "export_datapackage"
    GENERATE_TEMPLATES = "generate_templates"
    LEGACY_FUNCTION = "legacy_function"


class ResolutionKind(str, Enum):
    """Kinds of resolved launcher input."""

    COMPONENT = "component"
    FILE = "file"
    URI = "uri"


@dataclass(slots=True)
class ComponentDescriptor:
    """Declarative metadata for a launcher-visible component.

    Example::

        descriptor = ComponentDescriptor(
            id="text-client",
            display_name="Text Client",
            description="Connect with the text client.",
            kind="client",
            handler_id=HandlerId.PROCESS,
            launch_mode=ExecutionMode.BACKGROUND,
            script_name="CommonClient",
        )
    """

    id: str
    display_name: str
    description: str
    kind: ComponentKind
    handler_id: str
    launch_mode: ExecutionMode
    script_name: str | None = None
    frozen_name: str | None = None
    game_name: str | None = None
    supports_uri: bool = False
    file_suffixes: tuple[str, ...] = ()
    icon: str = "icon"
    cli: bool = False
    hidden: bool = False
    adapter_local: bool = False


@dataclass(slots=True)
class ResolvedInput:
    """Resolved launcher input for a path, component id, or `archipelago://` URL."""

    raw_value: str = ""
    component: ComponentDescriptor | None = None
    component_id: str | None = None
    file_path: str | None = None
    candidates: list[ComponentDescriptor] = field(default_factory=list)
    launch_components: list[ComponentDescriptor] = field(default_factory=list)
    launch_args: tuple[str, ...] = ()
    kind: ResolutionKind = ResolutionKind.COMPONENT

    def __post_init__(self) -> None:
        if self.component_id is None and self.component is not None:
            self.component_id = self.component.id
        if self.launch_components and not self.candidates:
            self.candidates = list(self.launch_components)
        elif self.candidates and not self.launch_components:
            self.launch_components = list(self.candidates)
