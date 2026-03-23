import sys
from worlds.ahit.Client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("AHITClient", exception_logger="Client")
    launch(*sys.argv[1:])
