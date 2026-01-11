from worlds.Bingo.Client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("APBingoClient", exception_logger="Client")
    launch()
