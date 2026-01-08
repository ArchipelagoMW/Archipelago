import ModuleUpdate
import Utils
from worlds.ff12_open_world.Client import launch
ModuleUpdate.update()

if __name__ == '__main__':
    Utils.init_logging("FF12Client", exception_logger="Client")
    launch()
