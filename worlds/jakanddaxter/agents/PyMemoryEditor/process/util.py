# -*- coding: utf-8 -*-

import psutil
import sys

if "win" in sys.platform:
    from ..win32.functions import GetProcessIdByWindowTitle


def get_process_id_by_process_name(process_name: str) -> int:
    """
    Get a process name and return its process ID.
    """
    for process in psutil.process_iter():
        if process.name() == process_name:
            return process.pid


def get_process_id_by_window_title(window_title: str) -> int:
    """
    Get a window title and return its process ID.
    """
    if "win" not in sys.platform:
        raise OSError("This function is compatible only with Windows OS.")

    return GetProcessIdByWindowTitle(window_title)


def pid_exists(pid: int) -> bool:
    """
    Check if the process ID exists.
    """
    return psutil.pid_exists(pid)
