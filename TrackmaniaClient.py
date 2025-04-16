from worlds.trackmania.client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("TrackmaniaClient", exception_logger="Client")
    launch()
