# -*- coding: utf-8 -*-
from PyMemoryEditor import __version__

from .main_application_window import ApplicationWindow
from .open_process_window import OpenProcessWindow

import sys


def main(*args, **kwargs):
    if len(sys.argv) > 1 and sys.argv[1].strip() in ["--version", "-v"]:
        return print(__version__)

    open_process_window = OpenProcessWindow()
    process = open_process_window.get_process()

    if not process: return

    try: ApplicationWindow(process)
    finally: process.close()


if __name__ == "__main__":
    main()
