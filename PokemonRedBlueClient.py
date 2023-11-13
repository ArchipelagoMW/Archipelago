from __future__ import annotations

import ModuleUpdate
ModuleUpdate.update()

from worlds.pokemon_rb.client import launch
import Utils

if __name__ == "__main__":
    Utils.init_logging("PokemonRedBlueClient", exception_logger="Client")
    launch()
