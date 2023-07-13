import asyncio
import ModuleUpdate
import Utils

ModuleUpdate.update()
from CommonClient import server_loop
from worlds.kh2.Client import launch

if __name__ == '__main__':
    Utils.init_logging("KH2Client", exception_logger="Client")
    launch()
