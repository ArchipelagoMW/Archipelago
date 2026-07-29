import struct
from logging import Logger
from typing import Optional, Dict

from .consts import ADDRESSES, GameState, CharacterPurchaseAmounts, CHARACTER_OPTION_TO_VALUE_IN_GAME, YES_DEBUG, \
    NO_DEBUG, DEFAULT_EXP_STRING, DEFAULT_EXP_FMT, MESSAGE_EXP_FMT

from .pcsx2_interface.pine import Pine


class GameInterface:
    """
    Base class for connecting with a pcsx2 game
    taken from https://github.com/hoppel16/ArchipelagoBranchSly1/blob/main/worlds/sly1/Sly1Interface.py
    """

    pcsx2_interface: Pine = Pine()
    logger: Logger
    game_id_error: Optional[str] = None
    current_game: Optional[str] = None
    addresses: Dict = {}

    def __init__(self, logger) -> None:
        self.logger = logger

    def _read8(self, address: int):
        return self.pcsx2_interface.read_int8(address)

    def _read16(self, address: int):
        return self.pcsx2_interface.read_int16(address)

    def _read32(self, address: int):
        return self.pcsx2_interface.read_int32(address)

    def _read_bytes(self, address: int, n: int):
        return self.pcsx2_interface.read_bytes(address, n)

    def _read_float(self, address: int):
        return struct.unpack("f", self.pcsx2_interface.read_bytes(address, 4))[0]

    def _write8(self, address: int, value: int):
        self.pcsx2_interface.write_int8(address, value)

    def _write16(self, address: int, value: int):
        self.pcsx2_interface.write_int16(address, value)

    def _write32(self, address: int, value: int):
        self.pcsx2_interface.write_int32(address, value)

    def _write_bytes(self, address: int, value: bytes):
        self.pcsx2_interface.write_bytes(address, value)

    def _write_float(self, address: int, value: float):
        self.pcsx2_interface.write_float(address, value)

    def _write_u32(self, address: int, value: int):
        value = value & 0xFFFFFFFF  # truncate to 32-bit unsigned
        value_bytes = value.to_bytes(4, byteorder='little', signed=False)
        self._write_bytes(address, value_bytes)

    def _write_u64(self, address: int, value: int):
        if value < 0 or value > 0xFFFFFFFFFFFFFFFF:
            raise ValueError(f"Value {value} out of range for unsigned 64-bit write.")
        value_bytes = value.to_bytes(8, byteorder='little', signed=False)
        self._write_bytes(address, value_bytes)

    def connect_to_game(self):
        """
        Initializes the connection to PCSX2 and verifies it is connected to the
        right game
        """
        if not self.pcsx2_interface.is_connected():
            self.pcsx2_interface.connect()
            if not self.pcsx2_interface.is_connected():
                return
            self.logger.info("Connected to PCSX2 Emulator")
        try:
            game_id = self.pcsx2_interface.get_game_id()
            print(f"game_id: {game_id!r}")
            # The first read of the address will be null if the client is faster than the emulator
            self.current_game = None
            if game_id in ADDRESSES.keys():
                self.current_game = game_id
                self.addresses = ADDRESSES[game_id]
            if self.current_game is None and self.game_id_error != game_id and game_id != b'\x00\x00\x00\x00\x00\x00':
                self.logger.warning(
                    f"Connected to the wrong game ({game_id})")
                self.game_id_error = game_id
        except RuntimeError:
            pass
        except ConnectionError:
            pass

    def disconnect_from_game(self):
        self.pcsx2_interface.disconnect()
        self.current_game = None
        self.logger.info("Disconnected from PCSX2 Emulator")

    def get_connection_state(self) -> bool:
        try:
            connected = self.pcsx2_interface.is_connected()
            return connected and self.current_game is not None
        except RuntimeError:
            return False


class MKSMInterface(GameInterface):
    def get_checked_red_koins(self) -> set[str]:
        """Reads game memory once and returns every red koin location name
        currently flagged as collected."""
        game_state = self.get_game_state()
        if game_state != GameState.GAMEPLAY:
            return set()

        koin_addrs = self.addresses.get("RED_KOINS", {})
        if not koin_addrs:
            return set()

        all_addrs = {addr for bits in koin_addrs.values() for addr in bits}
        start, end = min(all_addrs), max(all_addrs)
        block = self._read_bytes(start, end - start + 1)

        checked = set()
        for location_name, addr_bits in koin_addrs.items():
            if all(
                    (block[addr - start] & self._mask(bits)) == self._mask(bits)
                    for addr, bits in addr_bits.items()
            ):
                checked.add(location_name)
        return checked

    @staticmethod
    def _mask(bits: list[int]) -> int:
        return sum(1 << b for b in bits)

    @staticmethod
    def _split_num_to_two_digits(num: int):
        assert len(str(num)) <= 2

        second = str(num)[-1]
        first = str(num)[-2] if len(str(num)) == 2 else '0'

        return first, second

    def clear_uncollected_red_koins(self, checked_names: set[str]) -> None:
        """Zero out every red koin's bits in game memory except for the ones in
        `checked_names`. Used once on connect so a stale save state (leftover
        bits from before this seed, debug saves, etc.) can't desync from what
        the AP server currently considers checked, or get reported as a check
        that never actually happened this run."""
        koin_addrs = self.addresses.get("RED_KOINS", {})
        if not koin_addrs:
            return

        all_addrs = {addr for bits in koin_addrs.values() for addr in bits}
        start, end = min(all_addrs), max(all_addrs)
        block = bytearray(self._read_bytes(start, end - start + 1))

        for location_name, addr_bits in koin_addrs.items():
            if location_name in checked_names:
                continue  # AP already has this checked; leave its bits alone
            for addr, bits in addr_bits.items():
                block[addr - start] &= ~self._mask(bits) & 0xFF

        self._write_bytes(start, bytes(block))

    def get_game_state(self) -> GameState:
        state_addr = self.addresses.get("GAME_STATE")
        return GameState(self._read8(state_addr))

    def is_paused(self) -> bool:
        return bool(self._read8(self.addresses.get("PAUSE_FLAG")))

    def clear_event_log(self, event_data: bytes) -> None:
        # print(event_data)

        # total_bytes = total_events * 8
        # self._write_bytes(self.addresses.get("EVENT_LOG_ARRAY"), bytes([0] * total_bytes))
        buffer = bytearray(16000)
        buffer[0:len(event_data)] = event_data
        self._write_bytes(self.addresses.get("EVENT_LOG_ARRAY"), buffer)
        self._write32(self.addresses.get("TOTAL_EVENTS"), len(event_data) // 8)

    def get_event_block(self) -> bytes:
        total_events = self._read32(self.addresses.get("TOTAL_EVENTS"))
        total_bytes = total_events * 8
        raw = self._read_bytes(self.addresses.get("EVENT_LOG_ARRAY"), total_bytes)

        # TOTAL_EVENTS occasionally reads back garbage/oversized (e.g. a boot/reset race) -
        # no real room is ever 0x0, so a trailing run of all-zero 8-byte records means the
        # count lied about the array's real length, not that those events actually happened.
        # Trim them here so every caller of get_event_block gets a sane buffer, instead of
        # treating that padding as real event-log growth and pushing it to the server.
        trimmed = len(raw)
        while trimmed >= 8 and raw[trimmed - 8:trimmed] == b"\x00" * 8:
            trimmed -= 8
        return raw[:trimmed]

    def get_upgrade_amounts(self) -> CharacterPurchaseAmounts:
        square = self._read8(self.addresses.get("SQUARE_UPGRADE"))
        triangle = self._read8(self.addresses.get("TRIANGLE_UPGRADE"))
        circle = self._read8(self.addresses.get("CIRCLE_UPGRADE"))
        r2 = self._read8(self.addresses.get("R2_UPGRADE"))
        combo = self._read8(self.addresses.get("COMBO_1"))
        combo += self._read8(self.addresses.get("COMBO_2"))
        combo += self._read8(self.addresses.get("COMBO_3"))
        combo += self._read8(self.addresses.get("COMBO_4"))
        combo += self._read8(self.addresses.get("COMBO_5"))

        return CharacterPurchaseAmounts(square=square,
                                        triangle=triangle,
                                        circle=circle,
                                        r2=r2,
                                        combo=combo)

    def set_move_upgrades(self, square: int, triangle: int, circle: int, r2: int):
        # adding 1 because the game has the first upgrade already unlocked.
        # setting upgrades to 0 prevents buying future upgrades.
        self._write8(self.addresses.get("SQUARE_UPGRADE"), square + 1)
        self._write8(self.addresses.get("TRIANGLE_UPGRADE"), triangle + 1)
        self._write8(self.addresses.get("CIRCLE_UPGRADE"), circle + 1)
        self._write8(self.addresses.get("R2_UPGRADE"), r2 + 1)

    def set_combos(self, combo_1: bool, combo_2: bool, combo_3: bool, combo_4: bool, combo_5: bool):
        self._write8(self.addresses.get("COMBO_1"), int(combo_1))
        self._write8(self.addresses.get("COMBO_2"), int(combo_2))
        self._write8(self.addresses.get("COMBO_3"), int(combo_3))
        self._write8(self.addresses.get("COMBO_4"), int(combo_4))
        self._write8(self.addresses.get("COMBO_5"), int(combo_5))

    def set_abilities(self, wall_climb, wall_run, wall_jump, double_jump, long_jump, swing, fist_of_ruin):
        self._write8(self.addresses.get("WALL_CLIMB"), wall_climb)
        self._write8(self.addresses.get("WALL_RUN"), wall_run)
        self._write8(self.addresses.get("WALL_JUMP"), wall_jump)
        self._write8(self.addresses.get("DOUBLE_JUMP"), double_jump)
        self._write8(self.addresses.get("LONG_JUMP"), long_jump)
        self._write8(self.addresses.get("SWING"), swing)
        self._write8(self.addresses.get("FIST_OF_RUIN"), fist_of_ruin)

    def add_exp(self, exp_to_add):
        addr = self.addresses.get("EXP")
        current_exp = self._read32(addr)
        current_exp += exp_to_add
        self._write32(addr, current_exp)

    def set_health_upgrades(self, health_upgrades: int) -> None:
        max_health = health_upgrades * 100 + 200
        health_upgrades_addr = self.addresses.get("HEALTH_UPGRADES")

        max_health_addr_1, max_health_addr_2 = self.addresses.get("MAX_HEALTH")

        self._write8(health_upgrades_addr, health_upgrades)
        self._write32(max_health_addr_1, max_health)
        self._write32(max_health_addr_2, max_health)

    def health_status(self) -> str:
        health_upgrades_addr = self.addresses.get("HEALTH_UPGRADES")
        cur_health_addr = self.addresses.get("CUR_HEALTH")
        max_health_addr_1, max_health_addr_2 = self.addresses.get("MAX_HEALTH")

        health_upgrades = self._read8(health_upgrades_addr)
        cur_health = self._read32(cur_health_addr)
        max_health_addr_1 = self._read32(max_health_addr_1)
        max_health_addr_2 = self._read32(max_health_addr_2)

        return f"{health_upgrades=}, {cur_health=}, {max_health_addr_1=}, {max_health_addr_2=}"

    def set_full_health(self, health_upgrades):
        cur_health_addr = self.addresses.get("CUR_HEALTH")
        max_health = health_upgrades * 100 + 200

        self._write32(cur_health_addr, max_health)

    def set_blood_bar(self, blood_bar):
        blood_bar_addr = self.addresses.get("BLOOD_BAR")
        self._write8(blood_bar_addr, blood_bar)

    def get_current_animation(self) -> int:
        animation_addr = self.addresses.get("CURRENT_ANIMATION")
        return self._read32(animation_addr)

    def set_koin_string(self, have, needed, total):
        have_1, have_2 = self._split_num_to_two_digits(have)
        needed_1, needed_2 = self._split_num_to_two_digits(needed)
        total_1, total_2 = self._split_num_to_two_digits(total)
        #                 %      d   space  /    space  %     d     NULL
        # orginal_fmt = [0x25, 0x64, 0x20, 0x2f, 0x20, 0x25, 0x64, 0x0]

        # clearing the original %d / %d format to be a clear space, injecting our own string instead
        only_spaces = [0x20] * 7
        fmt_addr = self.addresses.get("KOIN_FORMAT_STRING")
        self._write_bytes(fmt_addr, bytes(only_spaces))

        koin_string_addr = self.addresses.get("RED_KOIN_STRING")
        koin_str = f"RED KOINS:               {have_1}{have_2} / {needed_1}{needed_2} / {total_1}{total_2}\0"
        self._write_bytes(koin_string_addr, bytes(koin_str, encoding="ASCII"))

    def set_character(self, current_character_option):
        character_value = CHARACTER_OPTION_TO_VALUE_IN_GAME[current_character_option]
        character_addr = self.addresses.get("CURRENT_CHARACTER")
        self._write8(character_addr, character_value)

    def get_current_exp(self) -> int:
        addr = self.addresses.get("EXP")
        return self._read32(addr)

    def set_exp(self, exp: int) -> None:
        addr = self.addresses.get("EXP")
        self._write32(addr, exp)

    def toggle_debug_menu(self) -> bool:
        debug_1, debug_2 = self.addresses.get("DEBUG_MENU")
        current_1, current_2 = self._read32(debug_1), self._read32(debug_2)

        assert (current_1, current_2) in (YES_DEBUG, NO_DEBUG)

        if (current_1, current_2) == YES_DEBUG:
            self._write32(debug_1, NO_DEBUG[0])
            self._write32(debug_2, NO_DEBUG[1])
            return False
        else:  # (current_1, current_2) == NO_DEBUG:
            self._write32(debug_1, YES_DEBUG[0])
            self._write32(debug_2, YES_DEBUG[1])
            return True

    def kill_player(self):
        cur_health_addr = self.addresses.get("CUR_HEALTH")
        self._write32(cur_health_addr, 0)

    def is_dead(self):
        cur_health_addr = self.addresses.get("CUR_HEALTH")
        return self._read32(cur_health_addr) <= 0

    def set_default_exp_string(self):
        self.set_message(DEFAULT_EXP_STRING, default_fmt=True)

    def set_message(self, message: str, default_fmt: bool = False):
        message = message.encode("ASCII", errors="ignore")
        fmt = DEFAULT_EXP_FMT if default_fmt else MESSAGE_EXP_FMT
        fmt = fmt.encode("ASCII", errors="ignore")

        exp_str_addr = self.addresses.get("EXP_STRING")
        exp_fmt_addr = self.addresses.get("EXP_FMT")
        str_arr = bytearray(127)
        message = message[:127]
        str_arr[0:len(message)] = message
        self._write_bytes(exp_str_addr, bytes(str_arr))

        fmt_arr = bytearray(6)
        fmt_arr[0:len(fmt)] = fmt
        self._write_bytes(exp_fmt_addr, bytes(fmt_arr))

    def force_ui(self):
        inst_addr = self.addresses.get("FORCE_UI_INST")

        self._write32(inst_addr, 0)

    def get_current_area(self):
        area_addr = self.addresses.get("CURRENT_AREA")

        return self._read32(area_addr)

    def is_currently_saving(self):
        saving_addr = self.addresses.get("IS_CURRENTLY_SAVING")

        return bool(self._read8(saving_addr))
