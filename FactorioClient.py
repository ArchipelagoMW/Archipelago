from __future__ import annotations

import ModuleUpdate

ModuleUpdate.update()

import Utils
from worlds.factorio.Client import check_stdin, launch

if __name__ == "__main__":
    Utils.init_logging("FactorioClient", exception_logger="Client")
    check_stdin()
    launch()
