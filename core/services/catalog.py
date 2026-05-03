from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Any, Callable

from ..components import ComponentDescriptor, ResolutionKind, ResolvedInput
from ..requests import BasicError, ComponentListData
from ..result import Err, Ok, Result
from .shared import _default_component_source_provider, _descriptor_from_component


@dataclass(slots=True)
class ComponentCatalogService:
    """Expose declarative component metadata and input resolution."""

    registry_provider: Callable[[], list[Any]] = _default_component_source_provider

    def _sources(self) -> dict[str, Any]:
        return {descriptor.id: source for source in self.registry_provider() if (descriptor := _descriptor_from_component(source))}

    def _descriptors(self) -> list[ComponentDescriptor]:
        return [_descriptor_from_component(source) for source in self.registry_provider()]

    async def list_components(self, include_hidden: bool = False) -> Result[ComponentListData, BasicError]:
        """Return declarative component descriptors for adapters."""

        descriptors = self._descriptors()
        if not include_hidden:
            descriptors = [descriptor for descriptor in descriptors if not descriptor.hidden]

        return Ok(ComponentListData(components=descriptors))

    def get_descriptor(self, component_id: str) -> ComponentDescriptor | None:
        """Return the descriptor for `component_id`, if known."""

        for descriptor in self._descriptors():
            if descriptor.id == component_id:
                return descriptor

        return None

    def get_source(self, component_id: str) -> Any | None:
        """Return the underlying legacy source component for `component_id`."""

        return self._sources().get(component_id)

    async def resolve_input(self, value: str) -> Result[ResolvedInput, BasicError]:
        """Resolve a path, component id, or `archipelago://` URL."""

        import urllib.parse

        descriptors = self._descriptors()
        if value.startswith("archipelago://"):
            url = urllib.parse.urlparse(value)
            queries = urllib.parse.parse_qs(url.query)
            game = queries.get("game", [None])[0]
            text_client = next((descriptor for descriptor in descriptors if descriptor.display_name == "Text Client"), None)
            candidates = [
                descriptor
                for descriptor in descriptors
                if descriptor.supports_uri and game is not None and descriptor.game_name == game
            ]
            return Ok(
                ResolvedInput(
                    raw_value=value,
                    component=text_client,
                    candidates=candidates,
                    launch_components=candidates,
                    launch_args=(value,),
                    kind=ResolutionKind.URI,
                )
            )

        for descriptor in descriptors:
            if descriptor.file_suffixes and any(value.endswith(suffix) for suffix in descriptor.file_suffixes):
                return Ok(ResolvedInput(raw_value=value, component=descriptor, file_path=value, kind=ResolutionKind.FILE))
            if value in {descriptor.id, descriptor.display_name, descriptor.script_name or ""}:
                return Ok(ResolvedInput(raw_value=value, component=descriptor, kind=ResolutionKind.COMPONENT))

        return Err(BasicError(f"Could not resolve component for {value}"))

    def resolve_command(self, component_id: str) -> list[str] | None:
        """Resolve an executable command for `component_id`."""

        from Utils import is_frozen, is_windows, local_path

        descriptor = self.get_descriptor(component_id)
        if descriptor is None:
            return None
        if is_frozen():
            suffix = ".exe" if is_windows else ""
            return [local_path(f"{descriptor.frozen_name}{suffix}")] if descriptor.frozen_name else None
        return [sys.executable, local_path(f"{descriptor.script_name}.py")] if descriptor.script_name else None
