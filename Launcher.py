"""
Archipelago Launcher compatibility entrypoint.

The launcher implementation lives in the `launcher` package. This module remains
as the public script entrypoint for source runs, frozen builds, and file
associations.
"""

from __future__ import annotations

import multiprocessing

if __name__ == "__main__":
    import ModuleUpdate

    ModuleUpdate.update()

from Utils import init_logging
from launcher.main import cli, main


__all__ = ["cli", "main"]


if __name__ == "__main__":
    init_logging("Launcher")
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")
    cli()
