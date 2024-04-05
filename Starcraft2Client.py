from __future__ import annotations

import ModuleUpdate

ModuleUpdate.update()

import Utils
from worlds.sc2.Client import launch

if __name__ == "__main__":
    Utils.init_logging("Starcraft2Client", exception_logger="Client")
    launch()
