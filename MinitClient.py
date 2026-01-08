from worlds.minit.MinitClient import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("MinitClient", exception_logger="Client")
    launch()
