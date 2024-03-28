from logging import Logger
import struct
from worlds.metroidprime.DolphinClient import GC_GAME_ID_ADDRESS, DolphinClient, DolphinException
from enum import Enum
from enum import Enum
import py_randomprime

symbols = py_randomprime.symbols_for_version("0-00")
game_state_pointer = symbols["g_GameState"]
cstate_manager_global = symbols["g_StateManager"]
cplayer_vtable = 0x803d96e8

METROID_PRIME_ID = b"GM8E01"


class World(Enum):
    """Game worlds with their corresponding IDs in memory"""
    Impact_Crater = 3241871825
    Phendrana_Drifts = 2831049361
    Frigate_Orpheon = 361692695
    Magmoor_Caverns = 1056449404
    Phazon_Mines = 2980859237
    Tallon_Overworld = 972217896
    Chozo_Ruins = 2214002543
    End_of_Game = 332894565


def world_by_id(id) -> World:
    for world in World:
        if world.value == id:
            return world
    return None


class MetroidPrimeInterface:
    dolphin_client: DolphinClient
    connection_status: str
    logger: Logger

    def __init__(self, logger) -> None:
        self.logger = logger
        self.dolphin_client = DolphinClient(logger)

    def connect_to_game(self):
        self.dolphin_client.connect()
        self.logger.info("Connected to Dolphin Emulator")
        if self.dolphin_client.read_address(GC_GAME_ID_ADDRESS, 6) != METROID_PRIME_ID:
            self.logger.error(
                f"Connected to the wrong game, please connect to Metroid Prime V1 English ({METROID_PRIME_ID})")
            self.disconnect_from_game()

    def disconnect_from_game(self):
        self.dolphin_client.disconnect()
        self.logger.info("Disconnected from Dolphin Emulator")

    def is_connected(self):
        return self.dolphin_client.is_connected()

    def is_in_playable_state(self) -> bool:
        """ Check if the player is in the actual game rather than the main menu """
        return self.get_current_world() != None and self.__is_player_table_ready()

    def get_current_region(self):
        pass

    def give_item_to_player(self, item_id):
        pass

    def check_for_new_locations(self):
        pass

    def get_current_world(self) -> World:
        world_bytes = self.dolphin_client.read_pointer(
            game_state_pointer, 0x84, struct.calcsize(">I"))
        if world_bytes is not None:
            world_asset_id = struct.unpack(">I", world_bytes)[0]
            return world_by_id(world_asset_id)
        return None

    def __is_player_table_ready(self) -> bool:
        player_table_bytes = self.dolphin_client.read_pointer(
            cstate_manager_global + 0x84C, 0, 4)
        player_table = struct.unpack(">I", player_table_bytes)[0]
        if player_table == cplayer_vtable:
            return True
        else:
            return False
