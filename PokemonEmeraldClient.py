from Utils import init_logging
from worlds.pokemon_emerald.client import launch

if __name__ == "__main__":
    init_logging("PokemonEmeraldClient")
    launch()
