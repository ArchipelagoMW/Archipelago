import ModuleUpdate
import Utils
from worlds.kh1.Client import launch
ModuleUpdate.update()

if __name__ == '__main__':
    Utils.init_logging("KH1Client", exception_logger="Client")
    launch()
