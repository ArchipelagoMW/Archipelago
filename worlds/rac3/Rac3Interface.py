import random
import struct
from dataclasses import dataclass
from enum import IntEnum
from logging import Logger
from typing import Dict, Optional

from Rac3Addresses import (DEATH_FROM_ACTION, GADGET_LIST, PLANET_FROM_INFOBOT, PROGRESSIVE_DICT, QUICK_SELECT_LIST,
                           RAC3_REGION_DATA_TABLE,
                           RAC3_STATUS_DATA_TABLE, RAC3OPTION, RAC3STATUS, UPGRADE_DICT, WEAPON_LIST)
from . import Locations
from .pcsx2_interface.pine import Pine
from .Rac3Addresses import (CHECK_TYPE, COMPARE_TYPE, EQUIP_LIST, ITEM_FROM_AP_CODE, ITEM_NAME_FROM_ID, LOCATIONS,
                            INFOBOT_LIST, PLANET_NAME_FROM_ID, RAC3_ITEM_DATA_TABLE, RAC3ITEM, RAC3REGION, SHIP_SLOTS,
                            VIDCOMIC_LIST)


class Dummy(IntEnum):
    test = 0


class GameInterface:
    """
    Base class for connecting with a pcsx2 game
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
        return struct.unpack('f', self.pcsx2_interface.read_bytes(address, 4))[0]

    def _write8(self, address: int, value: int):
        self.pcsx2_interface.write_int8(address, value)

    def _write16(self, address: int, value: int):
        self.pcsx2_interface.write_int16(address, value)

    def _write32(self, address: int, value: int):
        self.pcsx2_interface.write_int32(address, value)

    def _write_bytes(self, address: int, value: bytes):
        self.pcsx2_interface.write_bytes(address, value)

    def connect_to_game(self):
        """
        Initializes the connection to PCSX2 and verifies it is connected to the
        right game
        """
        if not self.pcsx2_interface.is_connected():
            self.pcsx2_interface.connect()
            if not self.pcsx2_interface.is_connected():
                return
            self.logger.info('Connected to PCSX2 Emulator')
        try:
            game_id = self.pcsx2_interface.get_game_id()
            # The first read of the address will be null if the client is faster than the emulator
            self.current_game = None
            if game_id == RAC3STATUS.GAME_ID:
                self.current_game = game_id
            if self.current_game is None and self.game_id_error != game_id and game_id != b'\x00\x00\x00\x00\x00\x00':
                self.logger.warning(f'Connected to the wrong game ({game_id})')
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


@dataclass
class UnlockData:
    def __init__(self,
                 status: int = 0,
                 unlock_delay: int = 0):
        self.status = status
        self.unlock_delay = unlock_delay


class Rac3Interface(GameInterface):
    ########################################
    # Mandatory functions                  #
    ########################################

    UnlockItem = None
    weaponLevelLockFlag = None
    boltAndXPMultiplier = None
    boltAndXPMultiplierValue = None
    ship = 0
    ship_skin = 0
    skin = 0

    # Called at once when client started
    def init(self):
        self.init_variables()

    def reset_file(self):
        self.remove_all_items()
        self.undo_collections()

    # Called in periodically
    def update(self):
        # Memory checking
        self.gadget_cycler()
        self.planet_cycler()
        self.weapon_cycler()
        self.vidcomic_cycler()
        self.armor_cycler()
        self.verify_quick_select_and_last_used()
        # Proc Options
        self._write8(RAC3STATUS.MULTIPLIER, self.boltAndXPMultiplierValue)
        if self.weaponLevelLockFlag:
            self.weapon_exp_cycler()
        # Logic Fixes
        self.logic_fixes()
        self.tracker_update()

    @staticmethod
    def get_victory_code():
        victory_name = "Command Center: Biobliterator Defeated!"  # This must can be changed by option
        return Locations.location_table[victory_name].ap_code

    def check_main_menu(self):
        if self._read32(RAC3STATUS.MAIN_MENU):
            return True
        return False

    def proc_option(self, slot_data):
        self.logger.info(f'{slot_data}')
        self.boltAndXPMultiplier = slot_data[RAC3OPTION.BOLT_AND_XP_MULTIPLIER]
        self.weaponLevelLockFlag = slot_data[RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS]
        self.ship = slot_data[RAC3OPTION.SHIP_NOSE] + slot_data[RAC3OPTION.SHIP_WINGS]
        self.ship_skin = slot_data[RAC3OPTION.SHIP_SKIN]
        self.skin = slot_data[RAC3OPTION.SKIN]

    def map_switch(self):
        planet = self._read8(RAC3STATUS.PLANET)
        if planet > 55 or not self._read8(RAC3STATUS.MAP_CHECK):
            planet = 0
        elif planet > 29:
            planet = 3
        return PLANET_NAME_FROM_ID[planet]

    def tyhrranosis_fix(self):
        self._write8(RAC3STATUS.ROBONOIDS, 0)

    def item_received(self, item_code):
        # self.logger.info(f'{item_code}')
        name = ITEM_FROM_AP_CODE[item_code]

        if name in PROGRESSIVE_DICT.keys():
            name = PROGRESSIVE_DICT[name]

        if name in INFOBOT_LIST:
            for slot in SHIP_SLOTS:
                table = RAC3_REGION_DATA_TABLE[slot]
                self.logger.debug(f'{slot}: ID: {table.ID}, Address: {table.SLOT_ADDRESS}')
                if not self._read8(table.SLOT_ADDRESS):
                    self.UnlockItem[name].status = table.ID
        else:
            self.UnlockItem[name].status += 1

        match name:
            case RAC3ITEM.PROGRESSIVE_VIDCOMIC:
                if self.UnlockItem[name].status > 5:
                    self.UnlockItem[name].status = 5
            case RAC3ITEM.PROGRESSIVE_ARMOR:
                if self.UnlockItem[name].status > 4:
                    self.UnlockItem[name].status = 4
            case RAC3ITEM.TITANIUM_BOLT:
                pass
            case RAC3ITEM.BOLTS:
                bolt = self._read32(RAC3STATUS.BOLTS)
                self._write32(RAC3STATUS.BOLTS, bolt + 1000 * random.randint(1, 100))
            case RAC3ITEM.INFERNO_MODE:
                timer = self._read32(RAC3STATUS.INFERNO_TIMER)
                self._write32(RAC3STATUS.INFERNO_TIMER, timer + 1000 + random.randint(1, 100))
            case RAC3ITEM.JACKPOT:
                addr = RAC3STATUS.JACKPOT_TIMER
                timer = self._read32(addr)
                self._write32(addr, timer + 1000 + random.randint(1, 100))
                # Activate Jackpot
                self._write8(RAC3STATUS.JACKPOT, 1)
            case RAC3ITEM.PLAYER_XP:
                exp = self._read32(RAC3STATUS.NANOTECH_EXP)
                self._write32(RAC3STATUS.NANOTECH_EXP, exp + 1000 + random.randint(1, 100))
            case RAC3ITEM.WEAPON_XP:
                valid_weapons = []
                for weapon_name in WEAPON_LIST:
                    if self.UnlockItem[weapon_name].status:
                        level = self._read8(RAC3_ITEM_DATA_TABLE[weapon_name].LEVEL)
                        if level < 5:
                            valid_weapons.append(weapon_name)

                if valid_weapons:
                    weapon_num = random.randint(0, len(valid_weapons) - 1)
                    self.weapon_level_up(valid_weapons[weapon_num])

        if name in EQUIP_LIST:
            if RAC3_ITEM_DATA_TABLE[name].AMMO:
                self._write8(RAC3_ITEM_DATA_TABLE[name].AMMO_ADDRESS, RAC3_ITEM_DATA_TABLE[name].AMMO)
            self.update_equip(name)

    def is_location_checked(self, ap_code):
        # Find the location
        target_location = next((loc for loc in LOCATIONS if loc["Id"] == ap_code), None)  # TODO: Locations
        if not target_location:
            return False  # not found
        # Todo: replace strings with constants
        # --- NEW: if this location has multiple checks ---
        if "Checks" in target_location:
            for check in target_location["Checks"]:
                addr = self.address_convert(check["Address"])

                if check["CheckType"] in (CHECK_TYPE["bit"], CHECK_TYPE["falseBit"]):
                    _value = self._read8(addr)
                    _value = (_value >> check.get("AddressBit", 0)) & 0x01
                elif check["CheckType"] == CHECK_TYPE["byte"]:
                    _value = self._read8(addr)
                elif check["CheckType"] == CHECK_TYPE["short"]:
                    _value = self._read16(addr)
                else:
                    _value = self._read32(addr)

                if check["CheckType"] == CHECK_TYPE["bit"]:
                    _compare_value = 0x01
                elif check["CheckType"] == CHECK_TYPE["falseBit"]:
                    _compare_value = 0x00
                else:
                    _compare_value = check.get("CheckValue", "0")

                _compare_type = check.get("CompareType", COMPARE_TYPE["Match"])

                if _compare_type == COMPARE_TYPE["Match"] and not (_value == _compare_value):
                    return False
                if _compare_type == COMPARE_TYPE["GreaterThan"] and not (_value > _compare_value):
                    return False
                if _compare_type == COMPARE_TYPE["LessThan"] and not (_value < _compare_value):
                    return False
            return True  # <-- RETURN HERE so fallback doesn't run

        # --- OLD: single-check format (only for locations WITHOUT "Checks") ---
        addr = self.address_convert(target_location["Address"])
        if target_location["CheckType"] in (CHECK_TYPE["bit"], CHECK_TYPE["falseBit"]):
            _value = self._read8(addr)
            _value = (_value >> target_location.get("AddressBit", 0)) & 0x01
        elif target_location["CheckType"] == CHECK_TYPE["byte"]:
            _value = self._read8(addr)
        elif target_location["CheckType"] == CHECK_TYPE["short"]:
            _value = self._read16(addr)
        else:
            _value = self._read32(addr)

        if target_location["CheckType"] == CHECK_TYPE["bit"]:
            _compare_value = 0x01
        elif target_location["CheckType"] == CHECK_TYPE["falseBit"]:
            _compare_value = 0x00
        else:
            _compare_value = target_location.get("CheckValue", "0")

        _compare_type = target_location.get("CompareType", COMPARE_TYPE["Match"])

        if _compare_type == COMPARE_TYPE["Match"]:
            return _value == _compare_value
        if _compare_type == COMPARE_TYPE["GreaterThan"]:
            return _value > _compare_value
        if _compare_type == COMPARE_TYPE["LessThan"]:
            return _value < _compare_value
        return False

    ###################################
    # Game dedicated functions        #
    ###################################

    def __init__(self, logger):
        super().__init__(logger)  # GameInterfaceの初期化

    def init_variables(self):
        # Unlock state variables/ArmorUpgrade variable
        self.UnlockItem = {name: UnlockData() for name in ITEM_FROM_AP_CODE.values()}
        self.logger.debug(f'UnlockItem dict:{self.UnlockItem.keys()}')

        # Proc options
        ### Bolt and XPMultiplier
        val = int(self.boltAndXPMultiplier)
        self.boltAndXPMultiplierValue = val - 1  # 0 = x1, 1 = x2, 3 = x4 ...
        ### EnableWeaponLevelAsItem: if enabled, EXP disabler is running.

    # Address conversion from str to int(with US to JP)
    @staticmethod
    def address_convert(address):
        _addr = address
        if isinstance(address, str):
            _addr = int(address, 0)
        if 0x001BBB00 <= _addr <= 0x001BBBFF:  # T-Bolt
            _addr += 0
        elif 0x001D545C <= _addr <= 0x001D5553:  # Current Location + VidComic
            _addr += 0
        elif 0x00100000 <= _addr <= 0x00100050:  # DummyEXP
            _addr += 0
        elif 0x001D4C00 <= _addr <= 0x001D4CFF:  # Equipped garamecha
            _addr += 0
        else:
            pass
        return _addr

    # TO-DO: fixing this syntax KEKW

    # initialization
    def remove_all_items(self):
        for item in self.UnlockItem.keys():
            self.UnlockItem[item].status = 0
        for slot in SHIP_SLOTS:
            self._write8(RAC3_REGION_DATA_TABLE[slot].SLOT_ADDRESS, 0)
        self.UnlockItem[RAC3ITEM.VELDIN].status = 1
        # self.UnlockItem[RAC3ITEM.FLORANA].status = 1
        # self.UnlockItem[RAC3ITEM.STARSHIP_PHOENIX].status = 1
        # self.UnlockItem[RAC3ITEM.MUSEUM].status = 1

        self.weapon_cycler()
        self.gadget_cycler()
        self.planet_cycler()
        self.vidcomic_cycler()
        self.armor_cycler()
        self.verify_quick_select_and_last_used()
        self.weapon_exp_cycler()

    def undo_collections(self):
        pass

    def collect_location(self, ap_code):
        pass

    def add_cosmetics(self):
        self._write8(RAC3STATUS.SHIP_CONFIG, self.ship)
        self._write8(RAC3STATUS.SHIP_SKIN, self.ship_skin)
        self._write8(RAC3STATUS.PLAYER_SKIN, self.skin)
        self._write8(RAC3STATUS.PLAYER_SKIN_2, self.skin)

    # Logic Fixes
    def logic_fixes(self):
        current_planet = self._read8(RAC3STATUS.PLANET)

        # Fix can't play Qwark VidComics in some case which first event is skipped
        if current_planet == RAC3_REGION_DATA_TABLE[RAC3REGION.STARSHIP_PHOENIX].ID:
            self._write8(0x001426E8, 1)  # Todo: Take Qwark to Cage Mission

    # interval update function: Check unlock/lock status of items
    def weapon_cycler(self):
        # self.logger.debug('---------WeaponCycler Start---------')
        for name in WEAPON_LIST:
            # self._write8(RAC3_ITEM_DATA_TABLE[name].UNLOCK_ADDRESS, self.UnlockItem[name].status & 1)

            addr = RAC3_ITEM_DATA_TABLE[name].UNLOCK_ADDRESS
            if self.UnlockItem[name].status:
                if self.UnlockItem[name].unlock_delay:
                    self._write8(addr, 1)
                    self.UnlockItem[name].unlock_delay = 0
                else:
                    self.UnlockItem[name].unlock_delay += 1
            else:
                self._write8(addr, 0)

        replace_equip: int = 0
        equip_data = self._read8(RAC3STATUS.EQUIPPED)
        if equip_data and self.UnlockItem.get(ITEM_NAME_FROM_ID.get(equip_data)).status == 0:  # Not unlocked
            last_0 = self._read8(RAC3STATUS.LAST_USED_0)
            if last_0 and self.UnlockItem.get(ITEM_NAME_FROM_ID.get(last_0)).status:
                replace_equip = last_0
            else:
                last_1 = self._read8(RAC3STATUS.LAST_USED_1)
                if last_1 and self.UnlockItem.get(ITEM_NAME_FROM_ID.get(last_1)).status:
                    replace_equip = last_1
                else:
                    last_2 = self._read8(RAC3STATUS.LAST_USED_2)
                    if last_2 and self.UnlockItem.get(ITEM_NAME_FROM_ID.get(last_2)).status:
                        replace_equip = last_2
                    else:
                        replace_equip = RAC3_ITEM_DATA_TABLE[RAC3ITEM.WRENCH].ID
        if replace_equip:
            self._write8(RAC3STATUS.EQUIPPED, replace_equip)

    def gadget_cycler(self):
        for name in GADGET_LIST:
            addr = RAC3_ITEM_DATA_TABLE[name].UNLOCK_ADDRESS
            if self.UnlockItem[name].status:
                if self.UnlockItem[name].unlock_delay:
                    self._write8(addr, 1)
                    self.UnlockItem[name].unlock_delay = 0
                else:
                    self.UnlockItem[name].unlock_delay += 1
            else:
                self._write8(addr, 0)

    def planet_cycler(self):
        # self.logger.debug('---------PlanetCycler Start---------')
        for name in INFOBOT_LIST:
            planet = RAC3_REGION_DATA_TABLE[PLANET_FROM_INFOBOT[name]]
            addr = 4 * (self.UnlockItem[name].status - 1) + RAC3STATUS.PLANET_SLOT_ADDRESS
            if self.UnlockItem[name].status:
                # Don't allow planets that can softlock
                if ((name != RAC3ITEM.QWARKS_HIDEOUT or self.UnlockItem[RAC3ITEM.REFRACTOR].status == 0) and
                    (name != RAC3ITEM.HOLOSTAR_STUDIOS or
                     (self.UnlockItem[RAC3ITEM.HACKER].status and self.UnlockItem[RAC3ITEM.HYPERSHOT].status))):
                    if self.UnlockItem[name].unlock_delay:
                        self._write8(addr, planet.ID)
                    else:
                        self.UnlockItem[name].unlock_delay += 1
        # self.logger.debug('---------PlanetCycler End---------')

    def vidcomic_cycler(self):
        # self.logger.debug("---------VidComicCycler Start---------")
        comic = self.UnlockItem[RAC3ITEM.PROGRESSIVE_VIDCOMIC]
        for name in range(5):
            addr = RAC3_ITEM_DATA_TABLE[VIDCOMIC_LIST[name]].UNLOCK_ADDRESS
            if name + 1 > comic.status:
                self._write8(addr, 0)  # Disable Vidcomics not unlocked yet
            elif name + 1 <= comic.status:
                unlock_delay_count = 1
                if name == 2:
                    unlock_delay_count = 30  # WA for Annihilation Nation Proceeding
                comic.unlock_delay += 1
                if comic.unlock_delay > unlock_delay_count:
                    self._write8(addr, 1)
                    comic.unlock_delay = 0

    def armor_cycler(self):
        addr = RAC3_ITEM_DATA_TABLE[RAC3ITEM.PROGRESSIVE_ARMOR]
        armor = self.UnlockItem[RAC3ITEM.PROGRESSIVE_ARMOR]
        current_armor_value = self._read8(addr.UNLOCK_ADDRESS)

        if current_armor_value != armor.status:
            armor.unlock_delay += 1
            if armor.unlock_delay > 1:
                self._write8(addr.UNLOCK_ADDRESS, armor.status)
                self._write8(RAC3STATUS.HELMET, armor.status)
                armor.unlock_delay = 0

    def verify_quick_select_and_last_used(self):
        _slots = [RAC3STATUS.LAST_USED_0, RAC3STATUS.LAST_USED_1, RAC3STATUS.LAST_USED_2, RAC3STATUS.EQUIPPED]
        for slot in QUICK_SELECT_LIST:
            _slots.append(RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS)
        for addr in _slots:
            idx = self._read8(self.address_convert(addr))
            if idx:
                name = ITEM_NAME_FROM_ID[idx]
                if not self.UnlockItem[name].status:
                    # Not unlocked, but set
                    self._write8(addr, 0)

    def weapon_exp_cycler(self):
        """Keep weapon level tied to item count"""
        # TODO: Track weapon EXP
        for weapon_name in WEAPON_LIST:
            target_level = self.UnlockItem[weapon_name].status
            self.logger.debug(f'weapon: {weapon_name}, target: {target_level}')
            if target_level:
                target_id = UPGRADE_DICT[weapon_name][target_level]
                target_name = ITEM_NAME_FROM_ID[target_id]
                target_xp = RAC3_ITEM_DATA_TABLE[target_name].XP_THRESHOLD
                self.logger.debug(f'{target_name}, id: {target_id}, xp:{target_xp}')
                self._write8(RAC3_ITEM_DATA_TABLE[weapon_name].XP_ADDRESS, target_xp)

    def weapon_level_up(self, weapon_name):
        """Level up a weapon from xp reward"""
        weapon_data = RAC3_ITEM_DATA_TABLE[weapon_name]
        current_level = self._read8(weapon_data.LEVEL_ADDRESS) - weapon_data.ID
        if current_level < 5:
            target_level = current_level + 1
            target_xp = RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID[UPGRADE_DICT[weapon_name][target_level]]].XP_THRESHOLD
            self._write32(weapon_data.XP_ADDRESS, target_xp)

    # Equip the most recently collected weapon/gadget, update recent uses
    def update_equip(self, name):
        if RAC3_ITEM_DATA_TABLE[name].ID:
            self._write8(RAC3STATUS.LAST_USED_2, self._read8(RAC3STATUS.LAST_USED_1))
            self._write8(RAC3STATUS.LAST_USED_1, self._read8(RAC3STATUS.LAST_USED_0))
            self._write8(RAC3STATUS.LAST_USED_0, RAC3_ITEM_DATA_TABLE[name].ID)
            self._write8(RAC3STATUS.EQUIPPED, RAC3_ITEM_DATA_TABLE[name].ID)
            for slot in QUICK_SELECT_LIST:
                if not self._read8(RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS):
                    self._write8(RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS, RAC3_ITEM_DATA_TABLE[name].ID)
                    break
            self.verify_quick_select_and_last_used()

    def dump_info(self, current_planet, slot_data):
        print(f'Collected Items: {self.UnlockItem}')
        count = 0
        for name in SHIP_SLOTS:
            print(f'Planet{count}: {PLANET_NAME_FROM_ID[self._read8(RAC3_REGION_DATA_TABLE[name].SLOT_ADDRESS)]}')
            count += 1
        print(f'Current planet Tracked: {current_planet}')
        print(f'Slot Data: {slot_data}')

    def tracker_update(self):
        pass

    # Todo: Deathlink
    def alive(self) -> (bool, str):
        if self._read8(RAC3STATUS.HEALTH) > 0:
            return True, "Ratchet is Alive"
        else:
            death = DEATH_FROM_ACTION.get(self._read8(RAC3STATUS.ACTION), "Died")
            return False, f"Ratchet {death}"

    def kill_player(self) -> bool:
        if not self._read8(RAC3STATUS.PAUSE):
            self._write8(RAC3STATUS.HEALTH, 0)
            return True
        else:
            return False
