from __future__ import annotations

import ModuleUpdate
ModuleUpdate.update()

from worlds.factorio.Client import check_stdin, launch
import Utils

if __name__ == "__main__":
    Utils.init_logging("FactorioClient", exception_logger="Client")
    check_stdin()
    launch()
