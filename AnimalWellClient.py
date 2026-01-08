from worlds.animal_well.client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("AnimalWellClient", exception_logger="Client")
    launch()
