from logging import Logger
import struct
from worlds.metroidprime.DolphinClient import GC_GAME_ID_ADDRESS, DolphinClient, DolphinException
from enum import Enum
from enum import Enum
import py_randomprime
from .Items import ItemData, item_table

symbols = py_randomprime.symbols_for_version("0-00")
game_state_pointer = symbols["g_GameState"]
cstate_manager_global = symbols["g_StateManager"]
cplayer_vtable = 0x803d96e8
AREA_SIZE = 16
ITEM_SIZE = 0x8
RTSL_VECTOR_OFFSET = 0x4
METROID_PRIME_ID = b"GM8E01"
ARTIFACT_TEMPLE_ROOM_INDEX = 16


class MetroidPrimeSuit(Enum):
    Power = 0
    Gravity = 1
    Varia = 2
    Phazon = 3
    FusionPower = 4
    FusionGravity = 5
    FusionVaria = 6
    FusionPhazon = 7


class MetroidPrimeLevel(Enum):
    """Game worlds with their corresponding IDs in memory"""
    Impact_Crater = 3241871825
    Phendrana_Drifts = 2831049361
    Frigate_Orpheon = 361692695
    Magmoor_Caverns = 1056449404
    Phazon_Mines = 2980859237
    Tallon_Overworld = 972217896
    Chozo_Ruins = 2214002543
    End_of_Game = 332894565


def world_by_id(id) -> MetroidPrimeLevel:
    for world in MetroidPrimeLevel:
        if world.value == id:
            return world
    return None


class Area:
    layerCount: int
    startNameIdx: int
    layerBitsLo: int
    layerBitsHi: int

    def __init__(self, startNameIdx, layerCount, layerBitsHi, layerBitsLo):
        self.layerCount = layerCount
        self.startNameIdx = startNameIdx
        self.layerBitsHi = layerBitsHi
        self.layerBitsLo = layerBitsLo

    def __str__(self):
        return f"LayerCount: {self.layerCount}, LayerStartIndex: {self.startNameIdx}, LayerBitsHi: {self.layerBitsHi}, LayerBitsLo: {self.layerBitsLo}"


class InventoryItemData(ItemData):
    """Class used to track the player'scurrent items and their quantities"""
    current_amount: int
    current_capacity: int

    def __init__(self, item_data: ItemData, current_amount: int, current_capacity: int) -> None:
        super().__init__(item_data.name, item_data.id,
                         item_data.classification, item_data.max_capacity)
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

    def give_item_to_player(self, item_id: int, new_amount: int, new_capacity: int):
        """Gives the player an item with the specified amount and capacity"""
        self.dolphin_client.write_pointer(self.__get_player_state_pointer(),
                                          self.__calculate_item_offset(item_id), struct.pack(">II", new_amount, new_capacity))
        if item_id > 20 and item_id <= 23:
          current_suit = self.get_current_suit()
          if current_suit == MetroidPrimeSuit.Phazon:
            return
          elif item_id == 23:
            self.set_current_suit(MetroidPrimeSuit.Phazon)
          elif item_id == 21:
            self.set_current_suit(MetroidPrimeSuit.Gravity)
          elif item_id == 22 and current_suit != MetroidPrimeSuit.Gravity:
            self.set_current_suit(MetroidPrimeSuit.Varia)


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
            self.__get_player_state_pointer(), self.__calculate_item_offset(item.id), 8)
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

    def get_current_suit(self) -> MetroidPrimeSuit:
        player_state_pointer = self.__get_player_state_pointer()
        result = self.dolphin_client.read_pointer(
            player_state_pointer, 0x20, 4)
        suit_id = struct.unpack(">I", result)[0]
        return MetroidPrimeSuit(suit_id)

    def set_current_suit(self, suit: MetroidPrimeSuit):
        player_state_pointer = self.__get_player_state_pointer()
        self.dolphin_client.write_pointer(
            player_state_pointer, 0x20, struct.pack(">I", suit.value))

    def get_alive(self) -> bool:
        player_state_pointer = self.__get_player_state_pointer()
        value = struct.unpack(">I", self.dolphin_client.read_pointer(
            player_state_pointer, 0, 4))[0]
        return bool(value & (1 << 31))

    def set_alive(self, alive: bool):
        player_state_pointer = self.__get_player_state_pointer()
        value = struct.unpack(">I", self.dolphin_client.read_pointer(
            player_state_pointer, 0, 4))[0]
        if alive:
            value |= (1 << 31)
        else:
            value &= ~(1 << 31)
        self.dolphin_client.write_pointer(
            player_state_pointer, 0, struct.pack(">I", value))


    def get_current_level(self) -> MetroidPrimeLevel:
        """Returns the world that the player is currently in"""
        world_bytes = self.dolphin_client.read_pointer(
            game_state_pointer, 0x84, struct.calcsize(">I"))
        if world_bytes is not None:
            world_asset_id = struct.unpack(">I", world_bytes)[0]
            return world_by_id(world_asset_id)
        return None

    def get_current_health(self) -> float:
        result = self.dolphin_client.read_pointer(
            self.__get_player_state_pointer(), 0xC, 4)
        if result is None:
            return None
        return struct.unpack(">f", result)[0]

    def set_current_health(self, new_health_amount: float):
        self.dolphin_client.write_pointer(
            self.__get_player_state_pointer(), 0xC, struct.pack(">f", new_health_amount))
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
        return self.get_current_level() != None and self.__is_player_table_ready()

    def __is_player_table_ready(self) -> bool:
        """Check if the player table is ready to be read from memory, indicating the game is in a playable state"""
        player_table_bytes = self.dolphin_client.read_pointer(
            cstate_manager_global + 0x84C, 0, 4)
        if(player_table_bytes is None):
            return False
        player_table = struct.unpack(">I", player_table_bytes)[0]
        if player_table == cplayer_vtable:
            return True
        else:
            return False

    def __get_player_state_pointer(self):
        return int.from_bytes(self.dolphin_client.read_address(cstate_manager_global + 0x8B8, 4), "big")

    def __calculate_item_offset(self, item_id):
        return (0x24 + RTSL_VECTOR_OFFSET) + (item_id * ITEM_SIZE)

    def __get_world_layer_state_pointer(self):
        return int.from_bytes(self.dolphin_client.read_address(cstate_manager_global + 0x8c8, 4), "big")

    def __get_vector_item_offset(self):
        # Calculate the address of the Area at index area_idx
        vector_offset = 4
        vector_item_ptr = (0x0 + vector_offset)
        return vector_item_ptr

    def __get_area_address(self, area_index: int):
        """Gets the address of an area from the world layer state areas vector"""
        vector_bytes = self.dolphin_client.read_pointer(self.__get_world_layer_state_pointer(),
                                                        self.__get_vector_item_offset(), 12)  # 0x4 is count, 0x8 is max, 0xC is start address of the items in the vector
        # Unpack the bytes into the fields of the Area
        _count, _max, start_address = struct.unpack(
            ">iiI", vector_bytes)
        return start_address + AREA_SIZE * area_index

    def __get_area(self, area_index: int) -> Area:
        """Loads an area at the given index for the level the player is currently in"""
        address = self.__get_area_address(area_index)
        item_bytes = self.dolphin_client.read_address(address, AREA_SIZE)
        return Area(*struct.unpack(
            ">IIII", item_bytes))

    def set_layer_active(self, area_index: int, layer_id: int, active: bool):
        area = self.__get_area(area_index)
        if active:
            flag = 1 << layer_id
            area.layerBitsLo = area.layerBitsLo | flag
            area.layerBitsHi = area.layerBitsHi | (flag >> 0x1f)
        else:
            flag = ~(1 << layer_id)
            area.layerBitsLo = area.layerBitsLo & flag
            area.layerBitsHi = area.layerBitsHi & (flag >> 0x1f)

        new_bytes = struct.pack(
            ">IIII", area.startNameIdx, area.layerCount, area.layerBitsHi, area.layerBitsLo)

        self.dolphin_client.write_address(
            self.__get_area_address(area_index), new_bytes)

    def get_artifact_layer(self, item_id):
        # Artifact of truth is handled differently since it is the first thing you interact with in the room
        return item_id - 28 if item_id > 29 else 23

    def get_layer_active(self, area_index: int, layer_id: int):
        area = self.__get_area(area_index)
        return area.layerBitsLo & (1 << layer_id) != 0

    def sync_artifact_layers(self) -> bool:
        """Looks at the artifacts the player currently has and updates the layers in the artifact temple to match, only works if the player is in Tallon Overworld"""
        if self.get_current_level() == MetroidPrimeLevel.Tallon_Overworld:
            current_inventory = self.get_current_inventory()
            # for each item in the inventory, check if it is an artifact and update the layer
            for item in current_inventory.values():
                if item.id >= 29 and item.id <= 40:
                    layer_id = self.get_artifact_layer(item.id)
                    active = self.get_layer_active(
                        ARTIFACT_TEMPLE_ROOM_INDEX, layer_id)
                    if active != (item.current_amount > 0):
                        self.logger.debug(
                            f"Setting Artifact layer for {item.name} to {item.current_amount > 0}")
                        self.set_layer_active(
                            ARTIFACT_TEMPLE_ROOM_INDEX, layer_id, item.current_amount > 0)
                        changed = True
