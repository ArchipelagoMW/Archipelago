from worlds.jakanddaxter.Client import launch
import Utils
import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging("JakAndDaxterClient", exception_logger="Client")
    launch()
