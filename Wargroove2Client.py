from __future__ import annotations

import ModuleUpdate
ModuleUpdate.update()

from worlds.wargroove2.Client import launch
import Utils

if __name__ == "__main__":
    Utils.init_logging("Wargroove2Client", exception_logger="Client")
    launch()
