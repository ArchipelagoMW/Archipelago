import functools

from .vendor.pymem import Pymem


class GameStateManager:
    process_name = "scummvm.exe"

    def __init__(self):
        self.process = None
        self.is_process_running = False

        self.game_location = None
        self.game_location_offset = None

    @functools.cached_property
    def game_state_struct_address(self):
        return self._resolve_address(0x5276600, (0xC8, 0x8,))

    @functools.cached_property
    def game_state_storage_pointer_address(self):
        return self.game_state_struct_address + 0x80

    @property
    def game_state_storage_address(self):
        return self.process.read_longlong(self.game_state_storage_pointer_address)

    @functools.cached_property
    def game_state_hashmap_size_address(self):
        return self.game_state_struct_address + 0x88

    @functools.cached_property
    def game_state_key_count_address(self):
        return self.game_state_struct_address + 0x8C

    @functools.cached_property
    def game_state_deleted_key_count_address(self):
        return self.game_state_struct_address + 0x90

    @functools.cached_property
    def script_manager_struct_address(self):
        return self._resolve_address(0x5276600, (0xC8, 0x0))

    @functools.cached_property
    def script_manager_current_location_address(self):
        return self.script_manager_struct_address + 0x400

    @functools.cached_property
    def script_manager_current_location_offset_address(self):
        return self.script_manager_struct_address + 0x404

    @functools.cached_property
    def script_manager_next_location_address(self):
        return self.script_manager_struct_address + 0x408

    @functools.cached_property
    def script_manager_next_location_offset_address(self):
        return self.script_manager_struct_address + 0x40C

    def open_process_handle(self):
        try:
            self.process = Pymem(self.process_name)
            self.is_process_running = True
        except Exception:
            return False

        return True

    def close_process_handle(self):
        self.process.process_handle.close()

        if self.process.process_handle.closed:
            self.is_process_running = False
            self.process = None

            return True

        return False

    def get_game_state_address_offset_for(self, key):
        game_state_hashmap_size = self.process.read_int(self.game_state_hashmap_size_address)

        perturb = key
        perturb_shift = 5

        index = key & game_state_hashmap_size
        offset = index * 0x8

        is_new_offset = False

        while True:
            offset_value = self.process.read_longlong(self.game_state_storage_address + offset)

            if offset_value > 1:
                if self.process.read_int(offset_value + 0x4) == key:
                    break
            elif offset_value == 0:
                is_new_offset = True
                break

            index = ((5 * index) + perturb + 1) & game_state_hashmap_size
            offset = index * 0x8

            perturb >>= perturb_shift

        return offset, is_new_offset

    def read_game_state_value_for(self, key):
        offset, is_new_offset = self.get_game_state_address_offset_for(key)

        if is_new_offset:
            return 0, offset

        address = self.game_state_storage_address + offset
        address_value = self.process.read_longlong(address)

        if address_value <= 1:
            return 0, offset

        game_state_value = self.process.read_int(address_value + 0x0)
        game_state_key = self.process.read_int(address_value + 0x4)

        assert game_state_key == key

        return game_state_value, offset

    def write_game_state_value_for(self, key, value):
        current_value, offset = self.read_game_state_value_for(key)

        game_state_key_count = self.process.read_int(self.game_state_key_count_address)
        game_state_deleted_key_count = self.process.read_int(self.game_state_deleted_key_count_address)

        if value == 0:
            if current_value == 0:
                return False

            self.process.write_longlong(self.game_state_storage_address + offset, 1)

            self.process.write_int(self.game_state_key_count_address, game_state_key_count - 1)
            self.process.write_int(self.game_state_deleted_key_count_address, game_state_deleted_key_count + 1)
        else:
            if current_value > 0:
                address_value = self.process.read_longlong(self.game_state_storage_address + offset)
                self.process.write_int(address_value + 0x0, value)
            else:
                write_address = self.process.allocate(8)

                self.process.write_int(write_address + 0x0, value)
                self.process.write_int(write_address + 0x4, key)

                self.process.write_longlong(self.game_state_storage_address + offset, write_address)

                self.process.write_int(self.game_state_key_count_address, game_state_key_count + 1)

        return True

    def refresh_game_location(self):
        game_location_bytes = self.process.read_bytes(self.script_manager_current_location_address, 4)

        self.game_location = game_location_bytes.decode("ascii")
        self.game_location_offset = self.process.read_int(self.script_manager_current_location_offset_address)

        return True

    def set_game_location(self, game_location, offset):
        game_location_bytes = game_location.encode("ascii")

        self.process.write_bytes(self.script_manager_next_location_address, game_location_bytes, 4)
        self.process.write_int(self.script_manager_next_location_offset_address, offset)

        return True

    def _resolve_address(self, base_offset, offsets):
        address = self.process.read_longlong(self.process.base_address + base_offset)

        for offset in offsets[:-1]:
            address = self.process.read_longlong(address + offset)

        return address + offsets[-1]
