from __future__ import annotations

import ModuleUpdate
ModuleUpdate.update()

from worlds.sc2.client import launch
import Utils

# This is deprecated, replaced with the client hooked from the Launcher
# Will be removed in a following release
if __name__ == "__main__":
    Utils.init_logging("Starcraft2Client", exception_logger="Client")
    launch()
