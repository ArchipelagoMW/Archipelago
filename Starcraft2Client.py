from __future__ import annotations

import ModuleUpdate
ModuleUpdate.update()

from worlds.sc2.Client import launch
import Utils

if __name__ == "__main__":
    Utils.init_logging("Starcraft2Client", exception_logger="Client")
    launch()
