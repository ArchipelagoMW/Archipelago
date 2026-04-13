from __future__ import annotations

from launcher.models import LauncherEntry

from .process import launch_script_component, run_script_component


def is_host_component(component: LauncherEntry) -> bool:
    """Return whether `component` is the launcher host entry.

    Example::

        is_host_component(component)
    """

    return component.core_component_id == "host" or component.display_name == "Host"


def activate_host_component(component: LauncherEntry) -> str:
    """Launch the host component using launcher GUI semantics."""

    launch_script_component(component)
    return "Opening in a new window..."


def run_host_component(component: LauncherEntry, *args: str) -> None:
    """Run the host component using the launcher's blocking execution path."""

    run_script_component(component, *args)
