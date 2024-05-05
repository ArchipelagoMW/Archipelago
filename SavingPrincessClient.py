import Utils
from worlds.saving_princess.Constants import CLIENT_NAME
from worlds.saving_princess.Client import launch

import ModuleUpdate
ModuleUpdate.update()

if __name__ == "__main__":
    Utils.init_logging(CLIENT_NAME, exception_logger="Client")
    launch()
