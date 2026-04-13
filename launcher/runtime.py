from __future__ import annotations

import os
import sys
from typing import Any

import Utils
from Utils import local_path

from .models import LauncherEntry


def create_shortcut(button: Any, component: LauncherEntry) -> None:
    """Create a desktop shortcut for a launcher entry.

    Example::

        create_shortcut(button, component)
    """

    from pyshortcuts import make_shortcut

    env = os.environ
    if "APPIMAGE" in env:
        script = env["ARGV0"]
        wkdir = None
    else:
        script = sys.argv[0]
        wkdir = Utils.local_path()

    script = f"{script} \"{component.display_name}\""
    make_shortcut(
        script,
        name=f"Archipelago {component.display_name}",
        icon=local_path("data", "icon.ico"),
        startmenu=False,
        terminal=False,
        working_dir=wkdir,
        noexe=Utils.is_frozen(),
    )
    button.menu.dismiss()


def join_processes() -> None:
    """Preserve the launcher shutdown hook for compatibility.

    Example::

        join_processes()
    """

    return None
