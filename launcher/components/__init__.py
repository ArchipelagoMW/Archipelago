from __future__ import annotations

import logging
from collections.abc import Callable

from core import Err, ExecutionMode, Ok, RunComponent

from launcher.bridge import dispatch
from launcher.models import LauncherEntry


refresh_components: Callable[[], None] | None = None


def set_refresh_components(callback: Callable[[], None] | None) -> None:
    """Register the launcher GUI refresh callback.

    Example::

        set_refresh_components(refresh)
    """

    global refresh_components
    refresh_components = callback


def activate_component(component: LauncherEntry) -> str:
    """Activate a launcher entry from the GUI card view.

    Example::

        message = activate_component(component)
    """

    logging.info("Activating launcher component '%s' (id=%s).", component.display_name, component.id)
    if component.action is not None:
        message = component.action() or "Opening in a new window..."
        logging.info("Launcher component '%s' completed adapter-local action: %s", component.display_name, message)
        return message
    if component.core_component_id is None:
        logging.warning(f"Component {component} does not appear to be executable.")
        return "Opening in a new window..."

    result = dispatch(
        RunComponent(
            component_id=component.core_component_id,
            args=(),
            execution_mode=component.launch_mode,
        )
    )
    if isinstance(result, Err):
        logging.error("Launcher component '%s' failed: %s", component.display_name, result.error.message)
        return result.error.message
    assert isinstance(result, Ok)
    if result.value.job_id:
        logging.info(
            "Launcher component '%s' accepted as job %s.",
            component.display_name,
            result.value.job_id,
        )
    logging.info("Launcher component '%s' returned message: %s", component.display_name, result.value.message)
    return result.value.message


def run_component(component: LauncherEntry, *args: str) -> None:
    """Run a launcher entry through the blocking execution path.

    Example::

        run_component(component, "example.apworld")
    """

    logging.info("Running launcher component '%s' (id=%s) with args=%s.", component.display_name, component.id, args)
    if component.action is not None:
        message = component.action(*args)
        if message:
            logging.info("Launcher component '%s' adapter-local result: %s", component.display_name, message)
        if refresh_components:
            refresh_components()
        return
    if component.core_component_id is None:
        logging.warning(f"Component {component} does not appear to be executable.")
        return

    result = dispatch(
        RunComponent(
            component_id=component.core_component_id,
            args=args,
            execution_mode=ExecutionMode.DIRECT,
        )
    )
    if isinstance(result, Err):
        logging.error("Launcher component '%s' failed: %s", component.display_name, result.error.message)
    else:
        assert isinstance(result, Ok)
        if result.value.job_id:
            logging.info(
                "Launcher component '%s' accepted as job %s.",
                component.display_name,
                result.value.job_id,
            )
        logging.info("Launcher component '%s' returned message: %s", component.display_name, result.value.message)
    if refresh_components:
        refresh_components()


__all__ = [
    "activate_component",
    "run_component",
    "set_refresh_components",
]
