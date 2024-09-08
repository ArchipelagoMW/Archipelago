import ModuleUpdate
import Utils
from worlds.kh2.Client import launch
ModuleUpdate.update()

if __name__ == '__main__':
    Utils.init_logging("KH2Client", exception_logger="Client")
    launch()
