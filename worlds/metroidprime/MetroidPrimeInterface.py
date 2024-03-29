from logging import Logger
import struct
from BaseClasses import ItemClassification
from worlds.metroidprime.DolphinClient import GC_GAME_ID_ADDRESS, DolphinClient, DolphinException
from enum import Enum
from enum import Enum
import py_randomprime
from .Items import ItemData, item_table

symbols = py_randomprime.symbols_for_version("0-00")
game_state_pointer = symbols["g_GameState"]
cstate_manager_global = symbols["g_StateManager"]
cplayer_vtable = 0x803d96e8

METROID_PRIME_ID = b"GM8E01"


class MetroidPrimeArea(Enum):
    """Game worlds with their corresponding IDs in memory"""
    Impact_Crater = 3241871825
    Phendrana_Drifts = 2831049361
    Frigate_Orpheon = 361692695
    Magmoor_Caverns = 1056449404
    Phazon_Mines = 2980859237
    Tallon_Overworld = 972217896
    Chozo_Ruins = 2214002543
    End_of_Game = 332894565


def world_by_id(id) -> MetroidPrimeArea:
    for world in MetroidPrimeArea:
        if world.value == id:
            return world
    return None


class InventoryItemData(ItemData):
    """Class used to track the player'scurrent items and their quantities"""
    current_amount: int
    current_capacity: int

    def __init__(self, item_data: ItemData, current_amount: int, current_capacity: int) -> None:
        super().__init__(item_data.name, item_data.id, item_data.classification)
        self.current_amount = current_amount
        self.current_capacity = current_capacity


class MetroidPrimeInterface:
    """Interface sitting in front of the DolphinClient to provide higher level functions for interacting with Metroid Prime"""
    dolphin_client: DolphinClient
    connection_status: str
    logger: Logger

    def __init__(self, logger) -> None:
        self.logger = logger
        self.dolphin_client = DolphinClient(logger)

    def give_item_to_player(self, item_id):
        pass

    def check_for_new_locations(self):
        pass

    def get_item(self, item_id: int) -> InventoryItemData:
        for item in item_table.values():
            if item.id == item_id:
                return self.get_item(item)
        return None

    def get_item(self, item: ItemData) -> InventoryItemData:
        player_state_pointer = int.from_bytes(
            self.dolphin_client.read_address(cstate_manager_global + 0x8B8, 4), "big")
        result = self.dolphin_client.read_pointer(
            player_state_pointer, self.__calculate_item_offset(item.id), 8)
        if result is None:
            return None
        current_ammount, current_capacity = struct.unpack(">II", result)
        return InventoryItemData(item, current_ammount, current_capacity)

    def get_current_inventory(self) -> dict[str, InventoryItemData]:
        MAX_VANILLA_ITEM_ID = 40
        inventory: dict[str, InventoryItemData] = {}
        for item in item_table.values():
            if item.id <= MAX_VANILLA_ITEM_ID:
                inventory[item.name] = self.get_item(item)
        return inventory

    def get_current_area(self) -> MetroidPrimeArea:
        """Returns the world that the player is currently in"""
        world_bytes = self.dolphin_client.read_pointer(
            game_state_pointer, 0x84, struct.calcsize(">I"))
        if world_bytes is not None:
            world_asset_id = struct.unpack(">I", world_bytes)[0]
            return world_by_id(world_asset_id)
        return None

    def get_current_health(self) -> float:
        player_state_pointer = int.from_bytes(
            self.dolphin_client.read_address(cstate_manager_global + 0x8B8, 4), "big")
        result = self.dolphin_client.read_pointer(player_state_pointer, 0xC, 4)
        if result is None:
            return None
        return struct.unpack(">f", result)[0]

    def set_current_health(self, new_health_amount: float):
      player_state_pointer = int.from_bytes(self.dolphin_client.read_address(cstate_manager_global + 0x8B8, 4), "big")
      self.dolphin_client.write_pointer(player_state_pointer, 0xC, 4, struct.pack(">f", new_health_amount))
      return self.get_current_health()


    def connect_to_game(self):
        """Initializes the connection to dolphin and verifies it is connected to Metroid Prime"""
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
        return self.get_current_area() != None and self.__is_player_table_ready()

    def __is_player_table_ready(self) -> bool:
        """Check if the player table is ready to be read from memory, indicating the game is in a playable state"""
        player_table_bytes = self.dolphin_client.read_pointer(
            cstate_manager_global + 0x84C, 0, 4)
        player_table = struct.unpack(">I", player_table_bytes)[0]
        if player_table == cplayer_vtable:
            return True
        else:
            return False

    def __calculate_item_offset(self, item_id):
        return (0x24 + 0x4) + (item_id * 0x8)
