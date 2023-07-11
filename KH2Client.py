import asyncio
import ModuleUpdate

ModuleUpdate.update()
from CommonClient import server_loop
from worlds.kh2.Client import launch

if __name__ == '__main__':
    launch()
