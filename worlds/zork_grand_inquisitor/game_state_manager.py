from typing import Optional, Tuple

from pymem import Pymem
from pymem.process import close_handle


class GameStateManager:
    process_name = "scummvm.exe"

    def __init__(self) -> None:
        self.process: Optional[Pymem] = None
        self.is_process_running: bool = False

        self.game_state_struct_address: int = 0x0
        self.script_manager_struct_address: int = 0x0

        self.game_location: Optional[str] = None
        self.game_location_offset: Optional[int] = None

    @property
    def game_state_storage_pointer_address(self) -> int:
        return self.game_state_struct_address + 0x80

    @property
    def game_state_storage_address(self) -> int:
        return self.process.read_longlong(self.game_state_storage_pointer_address)

    @property
    def game_state_hashmap_size_address(self) -> int:
        return self.game_state_struct_address + 0x88

    @property
    def game_state_key_count_address(self) -> int:
        return self.game_state_struct_address + 0x8C

    @property
    def game_state_deleted_key_count_address(self) -> int:
        return self.game_state_struct_address + 0x90

    @property
    def script_manager_current_location_address(self) -> int:
        return self.script_manager_struct_address + 0x400

    @property
    def script_manager_current_location_offset_address(self) -> int:
        return self.script_manager_struct_address + 0x404

    @property
    def script_manager_next_location_address(self) -> int:
        return self.script_manager_struct_address + 0x408

    @property
    def script_manager_next_location_offset_address(self) -> int:
        return self.script_manager_struct_address + 0x40C

    def open_process_handle(self) -> bool:
        try:
            self.process = Pymem(self.process_name)
            self.is_process_running = True

            self.game_state_struct_address = self._resolve_address(0x5276600, (0xC8, 0x8,))
            self.script_manager_struct_address = self._resolve_address(0x5276600, (0xC8, 0x0))
        except Exception:
            return False

        return True

    def close_process_handle(self) -> bool:
        if close_handle(self.process.process_handle):
            self.is_process_running = False
            self.process = None

            self.game_state_struct_address = 0x0
            self.script_manager_struct_address = 0x0

            return True

        return False

    def is_process_still_running(self) -> bool:
        try:
            self.process.read_int(self.process.base_address)
        except Exception:
            self.is_process_running = False
            self.process = None

            self.game_state_struct_address = 0x0
            self.script_manager_struct_address = 0x0

            return False

        return True

    def read_game_state_value_for(self, key: int) -> Optional[int]:
        if self.is_process_running:
            offset: int = self._get_game_state_address_read_offset_for(key)

            address: int = self.game_state_storage_address + offset
            address_value: int = self.process.read_longlong(address)

            if address_value == 0:
                return 0

            game_state_value: int = self.process.read_int(address_value + 0x0)
            game_state_key: int = self.process.read_int(address_value + 0x4)

            assert game_state_key == key

            return game_state_value

        return None

    def write_game_state_value_for(self, key: int, value: int) -> Optional[bool]:
        if self.is_process_running:
            offset: int
            is_existing_node: bool
            is_reused_dummy_node: bool
            offset, is_existing_node, is_reused_dummy_node = self._get_game_state_address_write_offset_for(key)

            game_state_key_count: int = self.process.read_int(self.game_state_key_count_address)
            game_state_deleted_key_count: int = self.process.read_int(self.game_state_deleted_key_count_address)

            if value == 0:
                if is_existing_node is False:
                    return False

                self.process.write_longlong(self.game_state_storage_address + offset, 1)

                self.process.write_int(self.game_state_key_count_address, game_state_key_count - 1)
                self.process.write_int(self.game_state_deleted_key_count_address, game_state_deleted_key_count + 1)
            else:
                if is_existing_node:
                    address_value: int = self.process.read_longlong(self.game_state_storage_address + offset)
                    self.process.write_int(address_value + 0x0, value)
                else:
                    write_address: int = self.process.allocate(0x8)

                    self.process.write_int(write_address + 0x0, value)
                    self.process.write_int(write_address + 0x4, key)

                    self.process.write_longlong(self.game_state_storage_address + offset, write_address)

                    self.process.write_int(self.game_state_key_count_address, game_state_key_count + 1)

                    if is_reused_dummy_node:
                        self.process.write_int(self.game_state_deleted_key_count_address, game_state_deleted_key_count - 1)

            return True

        return None

    def refresh_game_location(self) -> Optional[bool]:
        if self.is_process_running:
            game_location_bytes: bytes = self.process.read_bytes(self.script_manager_current_location_address, 4)

            self.game_location = game_location_bytes.decode("ascii")
            self.game_location_offset = self.process.read_int(self.script_manager_current_location_offset_address)

            return True

        return None

    def set_game_location(self, game_location: str, offset: int) -> Optional[bool]:
        if self.is_process_running:
            game_location_bytes: bytes = game_location.encode("ascii")

            self.process.write_bytes(self.script_manager_next_location_address, game_location_bytes, 4)
            self.process.write_int(self.script_manager_next_location_offset_address, offset)

            return True

        return None

    def _resolve_address(self, base_offset: int, offsets: Tuple[int, ...]):
        address: int = self.process.read_longlong(self.process.base_address + base_offset)

        for offset in offsets[:-1]:
            address = self.process.read_longlong(address + offset)

        return address + offsets[-1]

    def _get_game_state_address_read_offset_for(self, key: int):
        game_state_hashmap_size: int = self.process.read_int(self.game_state_hashmap_size_address)

        perturb: int = key
        perturb_shift: int = 0x5

        index: int = key & game_state_hashmap_size
        offset: int = index * 0x8

        while True:
            offset_value: int = self.process.read_longlong(self.game_state_storage_address + offset)

            if offset_value == 0:  # Null Pointer
                break
            elif offset_value == 1:  # Dummy Node
                pass
            elif offset_value > 1:  # Existing Node
                if self.process.read_int(offset_value + 0x4) == key:
                    break

            index = ((0x5 * index) + perturb + 0x1) & game_state_hashmap_size
            offset = index * 0x8

            perturb >>= perturb_shift

        return offset

    def _get_game_state_address_write_offset_for(self, key: int) -> Tuple[int, bool, bool]:
        game_state_hashmap_size: int = self.process.read_int(self.game_state_hashmap_size_address)

        perturb: int = key
        perturb_shift: int = 0x5

        index: int = key & game_state_hashmap_size
        offset: int = index * 0x8

        node_found: bool = False

        dummy_node_found: bool = False
        dummy_node_offset: Optional[int] = None

        while True:
            offset_value: int = self.process.read_longlong(self.game_state_storage_address + offset)

            if offset_value == 0:  # Null Pointer
                break
            elif offset_value == 1:  # Dummy Node
                if dummy_node_found is False:
                    dummy_node_offset = offset
                    dummy_node_found = True
            elif offset_value > 1:  # Existing Node
                if self.process.read_int(offset_value + 0x4) == key:
                    node_found = True
                    break

            index = ((0x5 * index) + perturb + 0x1) & game_state_hashmap_size
            offset = index * 0x8

            perturb >>= perturb_shift

        if node_found is False and dummy_node_found is True:  # We should reuse the dummy node
            return dummy_node_offset, False, True
        elif node_found is False and dummy_node_found is False:  # We should allocate a new node
            return offset, False, False

        return offset, True, False  # We should update the existing node
