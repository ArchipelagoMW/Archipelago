from typing import Optional, Tuple

from pymem import Pymem
from pymem.process import close_handle


class GameStateManager:
    process_name = "scummvm.exe"

    process: Optional[Pymem]
    is_process_running: bool

    script_manager_struct_address: int
    render_manager_struct_address: int

    game_location: Optional[str]
    game_location_offset: Optional[int]

    def __init__(self) -> None:
        self.process = None
        self.is_process_running = False

        self.script_manager_struct_address = 0x0
        self.render_manager_struct_address = 0x0

        self.game_location = None
        self.game_location_offset = None

    @property
    def game_state_storage_pointer_address(self) -> int:
        return self.script_manager_struct_address + 0x88

    @property
    def game_state_storage_address(self) -> int:
        return self.process.read_longlong(self.game_state_storage_pointer_address)

    @property
    def game_state_hashmap_size_address(self) -> int:
        return self.script_manager_struct_address + 0x90

    @property
    def game_state_key_count_address(self) -> int:
        return self.script_manager_struct_address + 0x94

    @property
    def game_state_deleted_key_count_address(self) -> int:
        return self.script_manager_struct_address + 0x98

    @property
    def game_flags_storage_pointer_address(self) -> int:
        return self.script_manager_struct_address + 0x120

    @property
    def game_flags_storage_address(self) -> int:
        return self.process.read_longlong(self.game_flags_storage_pointer_address)

    @property
    def game_flags_hashmap_size_address(self) -> int:
        return self.script_manager_struct_address + 0x128

    @property
    def game_flags_key_count_address(self) -> int:
        return self.script_manager_struct_address + 0x12C

    @property
    def game_flags_deleted_key_count_address(self) -> int:
        return self.script_manager_struct_address + 0x130

    @property
    def current_location_address(self) -> int:
        return self.script_manager_struct_address + 0x400

    @property
    def current_location_offset_address(self) -> int:
        return self.script_manager_struct_address + 0x404

    @property
    def next_location_address(self) -> int:
        return self.script_manager_struct_address + 0x408

    @property
    def next_location_offset_address(self) -> int:
        return self.script_manager_struct_address + 0x40C

    @property
    def panorama_reversed_address(self) -> int:
        return self.render_manager_struct_address + 0x1C

    def open_process_handle(self) -> bool:
        try:
            self.process = Pymem(self.process_name)
            self.is_process_running = True

            self.script_manager_struct_address = self._resolve_address(0x5276600, (0xC8, 0x0))
            self.render_manager_struct_address = self._resolve_address(0x5276600, (0xD0, 0x120))
        except Exception:
            return False

        return True

    def close_process_handle(self) -> bool:
        if close_handle(self.process.process_handle):
            self.is_process_running = False
            self.process = None

            self.script_manager_struct_address = 0x0
            self.render_manager_struct_address = 0x0

            return True

        return False

    def is_process_still_running(self) -> bool:
        try:
            self.process.read_int(self.process.base_address)
        except Exception:
            self.is_process_running = False
            self.process = None

            self.script_manager_struct_address = 0x0
            self.render_manager_struct_address = 0x0

            return False

        return True

    def read_game_state_value_for(self, key: int) -> Optional[int]:
        return self.read_statemap_value_for(key, scope="game_state")

    def read_game_flags_value_for(self, key: int) -> Optional[int]:
        return self.read_statemap_value_for(key, scope="game_flags")

    def read_statemap_value_for(self, key: int, scope: str = "game_state") -> Optional[int]:
        if self.is_process_running:
            offset: int

            address: int
            address_value: int

            if scope == "game_state":
                offset = self._get_game_state_address_read_offset_for(key)

                address = self.game_state_storage_address + offset
                address_value = self.process.read_longlong(address)
            elif scope == "game_flags":
                offset = self._get_game_flags_address_read_offset_for(key)

                address = self.game_flags_storage_address + offset
                address_value = self.process.read_longlong(address)
            else:
                raise ValueError(f"Invalid scope: {scope}")

            if address_value == 0:
                return 0

            statemap_value: int = self.process.read_int(address_value + 0x0)
            statemap_key: int = self.process.read_int(address_value + 0x4)

            assert statemap_key == key

            return statemap_value

        return None

    def write_game_state_value_for(self, key: int, value: int) -> Optional[bool]:
        return self.write_statemap_value_for(key, value, scope="game_state")

    def write_game_flags_value_for(self, key: int, value: int) -> Optional[bool]:
        return self.write_statemap_value_for(key, value, scope="game_flags")

    def write_statemap_value_for(self, key: int, value: int, scope: str = "game_state") -> Optional[bool]:
        if self.is_process_running:
            offset: int
            is_existing_node: bool
            is_reused_dummy_node: bool

            key_count_address: int
            deleted_key_count_address: int

            storage_address: int

            if scope == "game_state":
                offset, is_existing_node, is_reused_dummy_node = self._get_game_state_address_write_offset_for(key)

                key_count_address = self.game_state_key_count_address
                deleted_key_count_address = self.game_state_deleted_key_count_address

                storage_address = self.game_state_storage_address
            elif scope == "game_flags":
                offset, is_existing_node, is_reused_dummy_node = self._get_game_flags_address_write_offset_for(key)

                key_count_address = self.game_flags_key_count_address
                deleted_key_count_address = self.game_flags_deleted_key_count_address

                storage_address = self.game_flags_storage_address
            else:
                raise ValueError(f"Invalid scope: {scope}")

            statemap_key_count: int = self.process.read_int(key_count_address)
            statemap_deleted_key_count: int = self.process.read_int(deleted_key_count_address)

            if value == 0:
                if not is_existing_node:
                    return False

                self.process.write_longlong(storage_address + offset, 1)

                self.process.write_int(key_count_address, statemap_key_count - 1)
                self.process.write_int(deleted_key_count_address, statemap_deleted_key_count + 1)
            else:
                if is_existing_node:
                    address_value: int = self.process.read_longlong(storage_address + offset)
                    self.process.write_int(address_value + 0x0, value)
                else:
                    write_address: int = self.process.allocate(0x8)

                    self.process.write_int(write_address + 0x0, value)
                    self.process.write_int(write_address + 0x4, key)

                    self.process.write_longlong(storage_address + offset, write_address)

                    self.process.write_int(key_count_address, statemap_key_count + 1)

                    if is_reused_dummy_node:
                        self.process.write_int(deleted_key_count_address, statemap_deleted_key_count - 1)

            return True

        return None

    def refresh_game_location(self) -> Optional[bool]:
        if self.is_process_running:
            game_location_bytes: bytes = self.process.read_bytes(self.current_location_address, 4)

            self.game_location = game_location_bytes.decode("ascii")
            self.game_location_offset = self.process.read_int(self.current_location_offset_address)

            return True

        return None

    def set_game_location(self, game_location: str, offset: int) -> Optional[bool]:
        if self.is_process_running:
            game_location_bytes: bytes = game_location.encode("ascii")

            self.process.write_bytes(self.next_location_address, game_location_bytes, 4)
            self.process.write_int(self.next_location_offset_address, offset)

            return True

        return None

    def set_panorama_reversed(self, is_reversed: bool) -> Optional[bool]:
        if self.is_process_running:
            self.process.write_int(self.panorama_reversed_address, 1 if is_reversed else 0)

            return True

        return None

    def _resolve_address(self, base_offset: int, offsets: Tuple[int, ...]):
        address: int = self.process.read_longlong(self.process.base_address + base_offset)

        for offset in offsets[:-1]:
            address = self.process.read_longlong(address + offset)

        return address + offsets[-1]

    def _get_game_state_address_read_offset_for(self, key: int):
        return self._get_statemap_address_read_offset_for(key, scope="game_state")

    def _get_game_flags_address_read_offset_for(self, key: int):
        return self._get_statemap_address_read_offset_for(key, scope="game_flags")

    def _get_statemap_address_read_offset_for(self, key: int, scope: str = "game_state") -> int:
        hashmap_size_address: int
        storage_address: int

        if scope == "game_state":
            hashmap_size_address = self.game_state_hashmap_size_address
            storage_address = self.game_state_storage_address
        elif scope == "game_flags":
            hashmap_size_address = self.game_flags_hashmap_size_address
            storage_address = self.game_flags_storage_address
        else:
            raise ValueError(f"Invalid scope: {scope}")

        statemap_hashmap_size: int = self.process.read_int(hashmap_size_address)

        perturb: int = key
        perturb_shift: int = 0x5

        index: int = key & statemap_hashmap_size
        offset: int = index * 0x8

        while True:
            offset_value: int = self.process.read_longlong(storage_address + offset)

            if offset_value == 0:  # Null Pointer
                break
            elif offset_value == 1:  # Dummy Node
                pass
            elif offset_value > 1:  # Existing Node
                if self.process.read_int(offset_value + 0x4) == key:
                    break

            index = ((0x5 * index) + perturb + 0x1) & statemap_hashmap_size
            offset = index * 0x8

            perturb >>= perturb_shift

        return offset

    def _get_game_state_address_write_offset_for(self, key: int) -> Tuple[int, bool, bool]:
        return self._get_statemap_address_write_offset_for(key, scope="game_state")

    def _get_game_flags_address_write_offset_for(self, key: int) -> Tuple[int, bool, bool]:
        return self._get_statemap_address_write_offset_for(key, scope="game_flags")

    def _get_statemap_address_write_offset_for(self, key: int, scope: str = "game_state") -> Tuple[int, bool, bool]:
        hashmap_size_address: int
        storage_address: int

        if scope == "game_state":
            hashmap_size_address = self.game_state_hashmap_size_address
            storage_address = self.game_state_storage_address
        elif scope == "game_flags":
            hashmap_size_address = self.game_flags_hashmap_size_address
            storage_address = self.game_flags_storage_address
        else:
            raise ValueError(f"Invalid scope: {scope}")

        statemap_hashmap_size: int = self.process.read_int(hashmap_size_address)

        perturb: int = key
        perturb_shift: int = 0x5

        index: int = key & statemap_hashmap_size
        offset: int = index * 0x8

        node_found: bool = False

        dummy_node_found: bool = False
        dummy_node_offset: Optional[int] = None

        while True:
            offset_value: int = self.process.read_longlong(storage_address + offset)

            if offset_value == 0:  # Null Pointer
                break
            elif offset_value == 1:  # Dummy Node
                if not dummy_node_found:
                    dummy_node_offset = offset
                    dummy_node_found = True
            elif offset_value > 1:  # Existing Node
                if self.process.read_int(offset_value + 0x4) == key:
                    node_found = True
                    break

            index = ((0x5 * index) + perturb + 0x1) & statemap_hashmap_size
            offset = index * 0x8

            perturb >>= perturb_shift

        if not node_found and dummy_node_found:  # We should reuse the dummy node
            return dummy_node_offset, False, True
        elif not node_found and not dummy_node_found:  # We should allocate a new node
            return offset, False, False

        return offset, True, False  # We should update the existing node
