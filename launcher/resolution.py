from __future__ import annotations

from core import ComponentDescriptor, Err, ListComponents, Ok, ResolveInput

from .bridge import dispatch
from .models import LauncherEntry


def get_backend_components(include_hidden: bool = False) -> list[ComponentDescriptor]:
    """Return backend components exposed by the core catalog.

    Example::

        components = get_backend_components()
    """

    result = dispatch(ListComponents(include_hidden=include_hidden))
    match result:
        case Err():
            return []
        case Ok(value=value):
            return value.components


def resolve_input(value: str):
    """Resolve a launcher input through the core dispatcher.

    Example::

        result = resolve_input("Text Client")
    """

    return dispatch(ResolveInput(value=value))


def to_launcher_entry(component: ComponentDescriptor | str) -> LauncherEntry | None:
    """Convert a backend descriptor or id into a launcher entry.

    Example::

        entry = to_launcher_entry("text_client")
    """

    descriptor = component if isinstance(component, ComponentDescriptor) else None
    if descriptor is None:
        for candidate in get_backend_components(include_hidden=True):
            if candidate.id == component:
                descriptor = candidate
                break
    if descriptor is None:
        for candidate in get_launcher_entries():
            if candidate.id == component:
                return candidate
        return None

    return LauncherEntry(
        id=descriptor.id,
        display_name=descriptor.display_name,
        description=descriptor.description,
        kind=descriptor.kind,
        icon=descriptor.icon,
        core_component_id=descriptor.id,
        launch_mode=descriptor.launch_mode,
    )


def get_launcher_entries() -> list[LauncherEntry]:
    """Return launcher-local utility entries."""

    from .components.functions import get_launcher_entries as get_utility_entries

    return get_utility_entries()


def get_components() -> list[LauncherEntry]:
    """Return launcher-visible entries, combining core and local utilities.

    Example::

        names = [component.display_name for component in get_components()]
    """

    entries = list(get_launcher_entries())
    hidden_names = {entry.display_name for entry in entries}
    for component in get_backend_components():
        if component.display_name in hidden_names:
            continue
        entry = to_launcher_entry(component)
        if entry is not None:
            entries.append(entry)
    return entries


def handle_uri(path: str) -> tuple[list[LauncherEntry], LauncherEntry | None]:
    """Resolve an `archipelago://` URL into launcher entries.

    Example::

        launch_components, text_client = handle_uri(uri)
    """

    result = resolve_input(path)
    match result:
        case Err():
            return [], None
        case Ok(value=value):
            resolved = value.resolved
    launch_components: list[LauncherEntry] = []
    if resolved.component_id:
        direct = to_launcher_entry(resolved.component_id)
        if direct is not None and resolved.launch_components:
            launch_components.append(direct)
    launch_components.extend([entry for entry in (to_launcher_entry(component) for component in resolved.launch_components) if entry])
    direct_component = to_launcher_entry(resolved.component_id) if resolved.component_id else None
    return launch_components, direct_component


def identify(path: str | None) -> tuple[str | None, LauncherEntry | None]:
    """Resolve `path` to a launcher file target or entry.

    Example::

        file_path, component = identify("example.apworld")
    """

    if path is None:
        return None, None

    result = resolve_input(path)
    match result:
        case Err():
            return None, None
        case Ok(value=value):
            resolved = value.resolved
    component = to_launcher_entry(resolved.component_id) if resolved.component_id else None
    return resolved.file_path, component
