from __future__ import annotations

from core import Err, ExecutionMode, Ok, RunComponent

from launcher.bridge import dispatch
from launcher.models import LauncherEntry


def run_script_component(component: LauncherEntry, *args: str) -> None:
    """Run a backend-backed launcher entry directly.

    Example::

        run_script_component(component, "example")
    """

    if component.core_component_id is None:
        return
    dispatch(RunComponent(component_id=component.core_component_id, args=args, execution_mode=ExecutionMode.DIRECT))


def launch_script_component(component: LauncherEntry, *args: str) -> bool:
    """Launch a backend-backed launcher entry with its preferred mode.

    Example::

        launch_script_component(component)
    """

    if component.core_component_id is None:
        return False
    result = dispatch(
        RunComponent(component_id=component.core_component_id, args=args, execution_mode=component.launch_mode)
    )
    return isinstance(result, Ok) and result.value.message == "Opening in a new window..."
