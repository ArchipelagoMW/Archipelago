from worlds.khbbs.Client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("KHBBSClient", exception_logger="Client")
    launch()
