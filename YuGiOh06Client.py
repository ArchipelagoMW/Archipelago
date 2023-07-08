from __future__ import annotations
from worlds.yugioh06.Client import launch
import Utils

import ModuleUpdate
ModuleUpdate.update()


if __name__ == "__main__":
    Utils.init_logging("Yu-Gi-Oh!06 Client", exception_logger="Client")
    launch()
