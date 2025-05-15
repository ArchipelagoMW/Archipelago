import threading

from BaseClasses import MultiWorld
from worlds.AutoWorld import World


class DragonWarriorWorld(World):
    """
    """
    game = "Dragon Warrior"
    item_name_to_id = []
    location_name_to_id = []
    item_name_groups = []
    location_name_groups = []
    rom_name: bytearray

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name = bytearray()
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)
