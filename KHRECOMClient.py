from worlds.khrecom.Client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("KHRECOMClient", exception_logger="Client")
    launch()
