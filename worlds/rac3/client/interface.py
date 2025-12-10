import time
from dataclasses import dataclass
from enum import IntEnum
from random import randint, uniform
from struct import unpack
from typing import Any, Optional

from CommonClient import logger
from worlds.rac3.constants.check_type import CHECKTYPE
from worlds.rac3.constants.data.address import RAC3ADDRESSDATA
from worlds.rac3.constants.data.item import (armor_data, equipable_data, gadget_data, infobot_data, ITEM_FROM_AP_CODE,
                                             ITEM_NAME_FROM_ID, non_prog_weapon_data, PROG_TO_NAME_DICT,
                                             RAC3_ITEM_DATA_TABLE, timer_to_status, vidcomic_data, weapon_upgrade_data)
from worlds.rac3.constants.data.location import LOCATION_FROM_AP_CODE, RAC3_LOCATION_DATA_TABLE, RAC3LOCATIONDATA
from worlds.rac3.constants.data.region import RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.data.status import RAC3_STATUS_DATA_TABLE
from worlds.rac3.constants.deaths import CLANK_DEATH_FROM_ACTION, DEATH_FROM_ACTION
from worlds.rac3.constants.input import RAC3INPUT
from worlds.rac3.constants.item_tags import RAC3ITEMTAG
from worlds.rac3.constants.items import QUICK_SELECT_LIST, RAC3ITEM, UPGRADE_DICT
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.region import (PLANET_FROM_INFOBOT, PLANET_NAME_FROM_ID, RAC3REGION, RESPAWN_COORDS_OFFSET,
                                          SHIP_SLOTS, VIDCOMIC_REGIONS)
from worlds.rac3.constants.status import PLAYER_TYPE_TO_NAME, RAC3STATUS
from worlds.rac3.pcsx2_interface.pine import Pine


class Dummy(IntEnum):
    test = 0


class GameInterface:
    """
    Base class for connecting with a pcsx2 game
    """
    current_game: Optional[str] = None
    game_id_error: Optional[str] = None
    is_connecting: bool = False
    pcsx2_interface: Pine = Pine()

    def __init__(self) -> None:
        pass

    def _read8(self, address: int):
        return self.pcsx2_interface.read_int8(address)

    def _read16(self, address: int):
        return self.pcsx2_interface.read_int16(address)

    def _read32(self, address: int):
        return self.pcsx2_interface.read_int32(address)

    def _read_bytes(self, address: int, n: int):
        return self.pcsx2_interface.read_bytes(address, n)

    def _read_float(self, address: int):
        return unpack('f', self.pcsx2_interface.read_bytes(address, 4))[0]

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

    def connect_to_game(self):
        """
        Initializes the connection to PCSX2 and verifies it is connected to the
        right game
        """
        if not self.pcsx2_interface.is_connected():
            self.is_connecting = True
            logger.debug('Begin attempting emulator connection...')
            self.pcsx2_interface.connect()
            self.is_connecting = False
            if not self.pcsx2_interface.is_connected():
                logger.debug('No Connection to PCSX2 Emulator')
                return
            logger.info('Connected to PCSX2 Emulator')
        self.current_game = None
        try:
            self.verify_game_version()
        except RuntimeError:
            logger.warning('PCSX2 Emulator is unreachable')
        except ConnectionError as error:
            logger.warning(f'Connection to PCSX2 Emulator lost: {error}')

    def disconnect_from_game(self):
        self.pcsx2_interface.disconnect()
        self.current_game = None
        logger.info("Disconnected from PCSX2 Emulator")

    def verify_game_version(self) -> bool:
        logger.debug('Start Game Verfication')
        try:
            game_id = self.pcsx2_interface.get_game_id()
        except ConnectionError as error:
            logger.debug(f'Game Verify Connection Error: {error}')
            return False
        # The first read of the address will be null if the client is faster than the emulator
        if game_id is None:
            logger.info('No Game Loaded')
            return False
        if game_id != self.current_game:
            logger.info(f'Detecting new game version...')
            match game_id:  # Todo: Add other game versions
                case RAC3STATUS.US_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: US release')
                case RAC3STATUS.US_GH_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: US Greatest Hits release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case RAC3STATUS.JP_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: Japanese release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case RAC3STATUS.EU_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: EU release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case _:
                    self.current_game = None
                    logger.info('Unknown game version detected')
        if self.current_game is None and self.game_id_error != game_id and game_id != b'\x00\x00\x00\x00\x00\x00':
            logger.warning(f'Connected to the wrong game ({game_id})')
            self.game_id_error = game_id
            return False
        else:
            logger.debug('Valid Game detected')
            return True

    def get_connection_state(self) -> bool:
        try:
            if self.pcsx2_interface.is_connected():
                return self.verify_game_version()
            else:
                return False
        except RuntimeError:
            return False


@dataclass
class UnlockData:
    status: int
    unlock_delay: int

    def __init__(self,
                 status: int = 0,
                 unlock_delay: int = 0):
        self.status = status
        self.unlock_delay = unlock_delay

    def __repr__(self):
        return f'{{ status: {self.status}, unlock_delay: {self.unlock_delay} }}'


def compare(value: int, check: RAC3ADDRESSDATA) -> bool:
    match check.TYPE & CHECKTYPE.SIGN:
        case CHECKTYPE.EQ:
            return value == check.VALUE
        case CHECKTYPE.NEQ:
            return value != check.VALUE
        case CHECKTYPE.GT:
            return value > check.VALUE
        case CHECKTYPE.LT:
            return value < check.VALUE
        case CHECKTYPE.GE:
            return value >= check.VALUE
        case CHECKTYPE.LE:
            return value <= check.VALUE
    return False


class Rac3Interface(GameInterface):
    ########################################
    # Mandatory functions                  #
    ########################################

    UnlockItem: dict[str, UnlockData] = None
    boltAndXPMultiplier: int = None
    boltAndXPMultiplierValue: int = None
    respawning: bool = False
    ship: int = 0
    ship_skin: int = 0
    skin: int = 0
    timers: dict[str, int] = {}
    weaponLevelLockFlag: bool = None

    # Called at once when client started
    def init(self):
        self.init_variables()

    def reset_file(self):
        self.remove_all_items()
        self.undo_collections()

    def important_items(self, item: int):
        """Runs when loading into game from the main menu to update the player with important items from the server,
        skips filler and trap items to not flood the player with bolts/xp"""
        if (RAC3ITEMTAG.FILLER in RAC3_ITEM_DATA_TABLE[ITEM_FROM_AP_CODE[item]].TAGS or RAC3ITEMTAG.TRAP in
                RAC3_ITEM_DATA_TABLE[ITEM_FROM_AP_CODE[item]].TAGS):
            return
        self.item_received(item)

    # Called in periodically
    def update(self):
        # Memory checking
        self.gadget_cycler()
        self.planet_cycler()
        self.weapon_cycler()
        self.vidcomic_cycler()
        self.armor_cycler()
        self.timer_cycler()
        self.input_cycler()
        self.verify_quick_select_and_last_used()
        # Proc Options
        self.multiplier_cycler()
        if self.weaponLevelLockFlag:
            self.weapon_exp_cycler()
        # Logic Fixes
        self.logic_fixes()
        if self.respawning:
            if self._read8(RAC3STATUS.FORCE_RELOAD) == 0:
                self.respawning = False

    @staticmethod
    def get_victory_code():
        return RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR].AP_CODE
        # let this be changed by an option

    def check_main_menu(self):
        if self._read32(RAC3STATUS.MAIN_MENU) == 0xFFFFFFFF:
            return True
        return False

    def proc_option(self, slot_data: dict[str, Any]):
        logger.debug(f'{slot_data}')
        self.boltAndXPMultiplier = slot_data[RAC3OPTION.BOLT_AND_XP_MULTIPLIER]
        self.weaponLevelLockFlag = slot_data[RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS]
        self.ship = slot_data[RAC3OPTION.SHIP_NOSE] + slot_data[RAC3OPTION.SHIP_WINGS]
        self.ship_skin = slot_data[RAC3OPTION.SHIP_SKIN]
        self.skin = slot_data[RAC3OPTION.SKIN]

    def map_switch(self) -> tuple[str, str]:
        planet = self._read8(RAC3STATUS.PLANET)
        _planet = planet
        if planet > 55 or not self._read8(RAC3STATUS.MAP_CHECK):
            _planet = 0
        elif planet > 29:
            _planet = 3
        return PLANET_NAME_FROM_ID[planet], PLANET_NAME_FROM_ID[_planet]

    def tyhrranosis_fix(self):
        self._write8(RAC3STATUS.ROBONOIDS, 0)

    def item_received(self, item_code: int):
        name = PROG_TO_NAME_DICT.get(ITEM_FROM_AP_CODE[item_code], ITEM_FROM_AP_CODE[item_code])
        logger.debug(f'Item received: {name}, AP code: {item_code}')
        if name in infobot_data.keys():
            self.UnlockItem[RAC3REGION.SLOT_0].status += 1
            self.UnlockItem[name].status = self.UnlockItem[RAC3REGION.SLOT_0].status
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
                self._write32(RAC3STATUS.BOLTS, bolt + 1000 * randint(1, 100))
            case RAC3ITEM.INFERNO_MODE:
                timer = self._read32(RAC3STATUS.INFERNO_TIMER)
                self._write32(RAC3STATUS.INFERNO_TIMER, timer + 1000 + randint(1, 100))
            case RAC3ITEM.JACKPOT:
                _time = int(time.time() + uniform(10, 30))
                self.timers[name + str(_time)] = _time
                self.boltAndXPMultiplierValue += 1
            case RAC3ITEM.PLAYER_XP:
                exp = self._read32(RAC3STATUS.NANOTECH_EXP)
                level = self._read8(RAC3STATUS.MAX_HEALTH)
                self._write32(RAC3STATUS.NANOTECH_EXP, exp + 10000 + randint(1, 300 * level))
            case RAC3ITEM.WEAPON_XP:
                valid_weapons = []
                for weapon_name in non_prog_weapon_data.keys():
                    if self.UnlockItem[weapon_name].status:
                        level = self._read8(non_prog_weapon_data[weapon_name].LEVEL)
                        if level < 5:
                            valid_weapons.append(weapon_name)

                if valid_weapons:
                    weapon_num = randint(0, len(valid_weapons) - 1)
                    self.weapon_level_up(valid_weapons[weapon_num])
            case RAC3ITEM.OHKO_TRAP:
                self._write8(RAC3STATUS.HEALTH, 1)
            case RAC3ITEM.NO_AMMO_TRAP:
                for weapon_name in non_prog_weapon_data.keys():
                    if self.UnlockItem[weapon_name].status:
                        self._write8(non_prog_weapon_data[weapon_name].AMMO_ADDRESS, 0)
                self._write8(RAC3STATUS.QWARK_AMMO, 0)
            case RAC3ITEM.LOCK_TRAP:
                already_locked = self._read8(RAC3STATUS.WEAPON_LOCK)

                # skip if already locked like in weapon challenges or weapon cycle challenges
                if already_locked == 0:
                    if self.timers.get(name, False):
                        self.timers[name] += randint(5, 15)
                    else:
                        self.timers[name] = int(time.time() + uniform(5, 15))
        if name in non_prog_weapon_data.keys():
            if non_prog_weapon_data[name].AMMO:
                self._write8(non_prog_weapon_data[name].AMMO_ADDRESS, non_prog_weapon_data[name].AMMO)
        if name in equipable_data.keys() and self.UnlockItem[name].status == 1:
            self.update_equip(name)

    def is_location_checked(self, ap_code: int) -> bool:
        loc_data: RAC3LOCATIONDATA = RAC3_LOCATION_DATA_TABLE[LOCATION_FROM_AP_CODE[ap_code]]
        if not loc_data:
            return False
        check_all: bool = True
        for check in loc_data.CHECK_ADDRESS:
            match check.TYPE & CHECKTYPE.SIZE:
                case CHECKTYPE.BIT:
                    check_all &= (self._read8(check.ADDRESS) >> check.VALUE) & 0x01
                case CHECKTYPE.BYTE:
                    check_all &= compare(self._read8(check.ADDRESS), check)
                case CHECKTYPE.SHORT:
                    check_all &= compare(self._read16(check.ADDRESS), check)
                case CHECKTYPE.INT:
                    check_all &= compare(self._read32(check.ADDRESS), check)
        return check_all

    ###################################
    # Game dedicated functions        #
    ###################################

    def __init__(self):
        super().__init__()  # GameInterfaceの初期化

    def init_variables(self):
        # Unlock state variables/ArmorUpgrade variable
        self.UnlockItem = {name: UnlockData() for name in ITEM_FROM_AP_CODE.values()}
        self.UnlockItem.update({RAC3REGION.SLOT_0: UnlockData()})
        logger.debug(f'UnlockItem dict:{self.UnlockItem.keys()}')

        # Proc options
        ### Bolt and XPMultiplier
        self.boltAndXPMultiplierValue = int(self.boltAndXPMultiplier)
        ### EnableWeaponLevelAsItem: if enabled, EXP disabler is running.

    # Address conversion from str to int(with US to JP)
    @staticmethod
    def address_convert(address: int):
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
        self.timers.clear()

        self.weapon_cycler()
        self.gadget_cycler()
        self.planet_cycler()
        self.vidcomic_cycler()
        self.armor_cycler()
        self.verify_quick_select_and_last_used()
        self.weapon_exp_cycler()
        self.timer_cycler()

    def undo_collections(self):
        sewer, nano = 0, 0
        for location in RAC3_LOCATION_DATA_TABLE.values():
            if RAC3TAG.SEWER in location.TAGS:
                if not sewer:
                    self._write8(location.CHECK_ADDRESS[0].ADDRESS, 0)
                    sewer += 1
                continue
            if RAC3TAG.NANOTECH in location.TAGS:
                if not nano:
                    self._write8(location.CHECK_ADDRESS[0].ADDRESS, 0)
                    nano += 1
                continue
            for check in location.CHECK_ADDRESS:
                if check.TYPE & CHECKTYPE.SIZE == CHECKTYPE.BIT:
                    self._write8(check.ADDRESS, self._read8(check.ADDRESS) & (0xFF ^ (0x01 << check.VALUE)))

    def collect_location(self, ap_code: int):
        loc_data: RAC3LOCATIONDATA = RAC3_LOCATION_DATA_TABLE[LOCATION_FROM_AP_CODE[ap_code]]
        if RAC3TAG.NANOTECH in loc_data.TAGS or RAC3TAG.SEWER in loc_data.TAGS:
            return
        for check in loc_data.CHECK_ADDRESS:
            if check.TYPE & CHECKTYPE.SIZE == CHECKTYPE.BIT:
                self._write8(check.ADDRESS, self._read8(check.ADDRESS) | (0x01 << check.VALUE))

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
        # logger.debug('---------WeaponCycler Start---------')
        for name in non_prog_weapon_data.keys():
            addr = non_prog_weapon_data[name].UNLOCK_ADDRESS
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
        if equip_data > 1 and self.UnlockItem.get(ITEM_NAME_FROM_ID.get(equip_data)).status == 0:  # Not unlocked
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
                        replace_equip = equipable_data[RAC3ITEM.WRENCH].ID
        if replace_equip:
            self._write8(RAC3STATUS.EQUIPPED, replace_equip)

    def gadget_cycler(self):
        for name in gadget_data.keys():
            addr = gadget_data[name].UNLOCK_ADDRESS
            if self.UnlockItem[name].status:
                if self.UnlockItem[name].unlock_delay:
                    self._write8(addr, 1)
                    self.UnlockItem[name].unlock_delay = 0
                else:
                    self.UnlockItem[name].unlock_delay += 1
            else:
                self._write8(addr, 0)

    def planet_cycler(self):
        # logger.debug('---------PlanetCycler Start---------')
        for name in infobot_data.keys():
            planet = RAC3_REGION_DATA_TABLE[PLANET_FROM_INFOBOT[name]]
            if self.UnlockItem[name].status:
                addr = RAC3_REGION_DATA_TABLE[SHIP_SLOTS[self.UnlockItem[name].status - 1]].SLOT_ADDRESS
                # Don't allow planets that can softlock
                if ((name != RAC3ITEM.QWARKS_HIDEOUT or self.UnlockItem[RAC3ITEM.REFRACTOR].status) and
                        (name != RAC3ITEM.HOLOSTAR_STUDIOS or
                         (self.UnlockItem[RAC3ITEM.HACKER].status and self.UnlockItem[RAC3ITEM.HYPERSHOT].status))):
                    if self.UnlockItem[name].unlock_delay:
                        # logger.debug(f'Write access to: {name} at {hex(addr)} value: {hex(planet.ID)}')
                        self._write8(addr, planet.ID)
                    else:
                        self.UnlockItem[name].unlock_delay += 1
        for number, slot in enumerate(SHIP_SLOTS):
            if number >= self.UnlockItem[RAC3REGION.SLOT_0].status:
                # logger.debug(f'Remove planet at {slot}')
                self._write8(RAC3_REGION_DATA_TABLE[slot].SLOT_ADDRESS, 0)
        # logger.debug('---------PlanetCycler End---------')

    def vidcomic_cycler(self):
        # logger.debug("---------VidComicCycler Start---------")
        prog_comic = self.UnlockItem[RAC3ITEM.PROGRESSIVE_VIDCOMIC]
        for index, name in enumerate(vidcomic_data.keys()):
            comic = self.UnlockItem[name]
            addr = vidcomic_data[name].UNLOCK_ADDRESS
            if index == 0:
                continue
            if index > prog_comic.status:
                self._write8(addr, 0)  # Disable Vidcomics not unlocked yet
            elif index <= prog_comic.status:
                unlock_delay_count = 1
                if index == 2:
                    unlock_delay_count = 30  # WA for Annihilation Nation Proceeding
                comic.unlock_delay += 1
                if comic.unlock_delay > unlock_delay_count:
                    self._write8(addr, 1)
                    comic.unlock_delay = 0

    def armor_cycler(self):
        addr = armor_data[RAC3ITEM.PROGRESSIVE_ARMOR]
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
            if idx > 1:
                name = ITEM_NAME_FROM_ID[idx]
                if not self.UnlockItem[name].status:
                    # Not unlocked, but set
                    self._write8(addr, 0)

    def weapon_exp_cycler(self):
        """Keep weapon level tied to item count"""
        # TODO: Track weapon EXP
        for weapon_name in non_prog_weapon_data.keys():
            target_level = self.UnlockItem[weapon_name].status
            logger.debug(f'weapon: {weapon_name}, target: {target_level}')
            if target_level:
                target_id = UPGRADE_DICT[weapon_name][target_level - 1]
                target_name = ITEM_NAME_FROM_ID[target_id]
                target_xp = RAC3_ITEM_DATA_TABLE[target_name].XP_THRESHOLD
                logger.debug(f'{target_name}, id: {target_id}, xp:{target_xp}')
                self._write32(non_prog_weapon_data[weapon_name].XP_ADDRESS, target_xp)
                self._write8(non_prog_weapon_data[weapon_name].LEVEL_ADDRESS, target_id)

    def weapon_level_up(self, weapon_name: str):
        """Level up a weapon from xp reward"""
        weapon_data = non_prog_weapon_data[weapon_name]
        current_level = self._read8(weapon_data.LEVEL_ADDRESS) - weapon_data.ID + 1
        if current_level < 5:
            target_level = current_level + 1
            target_id = UPGRADE_DICT[weapon_name][target_level - 1]
            target_name = ITEM_NAME_FROM_ID[target_id]
            target_xp = weapon_upgrade_data[target_name].XP_THRESHOLD
            logger.debug(f'level up {weapon_name} to {target_name}, target level: {current_level}, '
                         f'target id: {target_id}, target xp:{target_xp}')
            self._write32(weapon_data.XP_ADDRESS, target_xp)
            self._write8(weapon_data.LEVEL_ADDRESS, target_level)

    # Equip the most recently collected weapon/gadget, update recent uses
    def update_equip(self, name: str):
        if equipable_data[name].ID:
            self._write8(RAC3STATUS.LAST_USED_2, self._read8(RAC3STATUS.LAST_USED_1))
            self._write8(RAC3STATUS.LAST_USED_1, self._read8(RAC3STATUS.LAST_USED_0))
            self._write8(RAC3STATUS.LAST_USED_0, equipable_data[name].ID)
            self._write8(RAC3STATUS.EQUIPPED, equipable_data[name].ID)
            for slot in QUICK_SELECT_LIST:
                if not self._read8(RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS):
                    self._write8(RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS, equipable_data[name].ID)
                    break
            self.verify_quick_select_and_last_used()

    def dump_info(self, current_planet: str, slot_data: dict[str, Any]):
        logger.info(f'Collected Items: {self.UnlockItem}')
        count = 0
        for name in SHIP_SLOTS:
            logger.info(
                f'Planet{count}: {PLANET_NAME_FROM_ID[self._read8(RAC3_REGION_DATA_TABLE[name].SLOT_ADDRESS)]}')
            count += 1
        logger.info(f'Current planet Tracked: {current_planet}')
        logger.info(f'Slot Data: {slot_data}')

    def multiplier_cycler(self):
        self._write32(RAC3STATUS.JACKPOT_TIMER, 0xFFFFFFFF)
        self._write8(RAC3STATUS.JACKPOT, self.boltAndXPMultiplierValue)

    def timer_cycler(self):
        timers = list(self.timers.items())
        for name, _time in timers:
            if name.endswith(str(_time)):
                _name = name[:-len(str(_time))]
            else:
                _name = name
            if time.time() < _time:
                if _name == name:
                    self._write8(timer_to_status[name], 1)
            else:
                self.timers.pop(name)
                match _name:
                    case RAC3ITEM.LOCK_TRAP:  # Special case for lock trap
                        # Clear when timer ends directly rather than from the trap cleanup loop below
                        # Todo: Check for arena mission
                        self._write8(RAC3STATUS.WEAPON_LOCK, 0)
                    case RAC3ITEM.JACKPOT:
                        self.boltAndXPMultiplierValue -= 1

        # Remove trap effects for traps not in the timer dictionary to prevent any stuck effects
        # Prevent not having lock trap from unlocking weapon during arena weapon specific challenges every cycle
        # for trap_name, status_address in trap_to_status.items():
        #     if trap_name not in self.trap_timers and trap_name != RAC3ITEM.LOCK_TRAP:
        #         self._write8(status_address, 0)

    def pause_check(self):
        pause_address = RAC3_REGION_DATA_TABLE[self.planet].PAUSE_ADDRESS
        self.pause_menu = bool(self._read8(pause_address)) if pause_address else False
        self.pause_state = bool(self._read8(RAC3STATUS.PAUSE_STATE))
        match self.planet:
            case RAC3REGION.QWARKS_HIDEOUT:
                self.pause_state = bool(self._read8(RAC3STATUS.PAUSE_STATE + 0x40))
            case (RAC3REGION.BLACKWATER_CITY | RAC3REGION.ARIDIA |
                  RAC3REGION.METROPOLIS_RANGERS | RAC3REGION.TYHRRANOSIS_RANGERS):
                self.pause_state = bool(self._read8(RAC3STATUS.PAUSE_STATE + 0x50))

    def unpause_game(self):
        if self.pause_menu:
            self.write_input(RAC3INPUT.START)

    def write_input(self, button: RAC3INPUT):
        left_shifted = (button & 0x00FF) << 8
        right_shifted = button >> 8
        bitmasked = RAC3INPUT.MASK ^ (left_shifted | right_shifted)
        self._write16(RAC3STATUS.WRITE_INPUT_1, bitmasked)
        self._write16(RAC3STATUS.WRITE_INPUT_2, bitmasked)

    def teleport_to_ship(self):
        if self.should_overwrite_respawn() and self.planet in RESPAWN_COORDS_OFFSET.keys():
            self._write_bytes(
                RESPAWN_COORDS_OFFSET[self.planet] + RAC3STATUS.RESPAWN_BASE,
                self._read_bytes(RAC3STATUS.ENTRANCE_X, 28))
            logger.debug(f'Teleporting to ship on: {self.planet}')
        else:
            logger.debug(f'Teleporting to last checkpoint on: {self.planet}')
        self.force_respawn()

    def should_overwrite_respawn(self):
        if self.player_type in {RAC3PLAYERTYPE.CLANK, RAC3PLAYERTYPE.GIANT, RAC3PLAYERTYPE.QWARK}:
            return False
        match self.planet:
            # Todo: add more special cases
            case RAC3REGION.VELDIN:
                return False  # Problems with F-sector
            case RAC3REGION.MARCADIA:
                return self._read_float(RAC3STATUS.MARCADIA_SECTION) < 3  # 1: Main, 2: Rangers, 3: LDF
            case RAC3REGION.TYHRRANOSIS:
                return False  # Entrance coordinates in the first section that gets unloaded after leaving
            case RAC3REGION.ZELDRIN_STARPORT:
                return False  # Zeldrin has only one respawn point that is right next to the ship and we don't want
                # anything to happen while aboard the leviathan
            case _:
                return True

    def force_respawn(self):
        self.respawning = True
        self._write8(RAC3STATUS.FORCE_RELOAD, 1)

    def teleport_to_coords(self):
        self._write_bytes(RAC3STATUS.RATCHET_X, self._read_bytes(RAC3STATUS.ENTRANCE_X, 28))

    # Todo: Deathlink
    def alive(self) -> tuple[bool, str]:
        action_state = self._read8(RAC3STATUS.ACTION)
        player_type = self._read8(RAC3STATUS.PLAYER_TYPE)
        is_dead = (self._read8(RAC3STATUS.HEALTH) == 0
                   or (player_type == 2 and self._read32(RAC3STATUS.GIANT_CLANK_HEALTH) == 0))
        is_clank = player_type == 1
        death = DEATH_FROM_ACTION.get(action_state, False) if not is_clank else CLANK_DEATH_FROM_ACTION.get(
            action_state, False)
        character = PLAYER_TYPE_TO_NAME[player_type]
        in_nefarious_base = PLANET_NAME_FROM_ID[self._read8(RAC3STATUS.PLANET)] == RAC3REGION.AQUATOS_BASE

        if is_dead:
            logger.debug(f'Death Detected! (0 health)')
            return False, f"{character} {'Ran out of nanotech' if not death else death}"

        if action_state == 0x31:  # Eaten or in vehicle
            in_vehicle = self._read32(RAC3STATUS.VEHICLE_POINTER) != 0
            if in_vehicle:
                death = False

        # Special case for Nefarious's Base pitfall which doesn't set action state to death
        if in_nefarious_base and is_clank:
            if not self.respawning and self._read8(RAC3STATUS.FORCE_RELOAD):
                death = 'Fell to their doom in Nefarious\'s Base'

        if death:
            logger.debug(f'Death Detected! ({death})')
            return False, f"{character} {death}"

        logger.debug(f'{character} is Alive')
        return True, f"{character} is Alive"

    def kill_player(self) -> bool:
        pause_state_addr = RAC3STATUS.PAUSE_STATE
        current_planet = PLANET_NAME_FROM_ID[self._read8(RAC3STATUS.PLANET)]

        # Ranger missions and Qwark's Hideout have different pause state addresses than the rest
        match current_planet:
            case RAC3REGION.QWARKS_HIDEOUT:
                pause_state_addr += 0x40
            case (RAC3REGION.BLACKWATER_CITY | RAC3REGION.ARIDIA |
                  RAC3REGION.METROPOLIS_RANGERS | RAC3REGION.TYHRRANOSIS_RANGERS):
                pause_state_addr += 0x50

        pause_state = self._read8(pause_state_addr)  # 0x0 = unpaused
        if not pause_state:
            self._write8(RAC3STATUS.HEALTH, 0)
            in_vehicle = self._read32(RAC3STATUS.VEHICLE_POINTER) != 0
            in_vidcomic = current_planet in VIDCOMIC_REGIONS
            player_type = self._read8(RAC3STATUS.PLAYER_TYPE)
            if in_vehicle:
                health_addr = self._read32(self._read32(self._read32(RAC3STATUS.VEHICLE_POINTER) + 0x68))
                vehicle_blow_up_addr = self._read32(RAC3STATUS.VEHICLE_POINTER) + 0xBC
                self._write32(health_addr, 0)  # health is a float, but we can write 0 as int32
                self._write8(vehicle_blow_up_addr, 0x9)  # 0x9: blow up vehicle immediately 0xA: force respawn
                logger.debug(f'player in vehicle, killing vehicle too')
            elif in_vidcomic:
                # Qwark taking damage state (updates state to trigger death animation once at 0 health)
                self._write8(RAC3STATUS.ACTION, 0x9E)
                self._write8(RAC3STATUS.ACTION + 0xC, 0x9E)  # Past state
                self._write8(RAC3STATUS.ACTION + 0x18, 0x9E)  # This address helps the death animation trigger
                logger.debug(f'player in vidcomic, qwark must die dramatically')
            elif player_type == 1:  # Clank
                # Clank taking damage state (updates state to trigger death animation once at 0 health)
                self._write8(RAC3STATUS.ACTION, 0x42)
                self._write8(RAC3STATUS.ACTION + 0xC, 0x42)  # Past state
                self._write8(RAC3STATUS.ACTION + 0x18, 0x42)  # This address helps the death animation trigger
                logger.debug(f'player is clank, clank must die dramatically')
            elif player_type == 2:  # Giant Clank
                # Giant Clank punched state (updates state to trigger death animation once at 0 health)
                self._write32(RAC3STATUS.GIANT_CLANK_HEALTH, 0)
                self._write8(RAC3STATUS.ACTION, 0x5D)
                self._write8(RAC3STATUS.ACTION + 0xC, 0x5D)  # Past state
                self._write8(RAC3STATUS.ACTION + 0x18, 0x5D)  # This address helps the death animation trigger
                logger.debug(f'player is giant clank, giant clank must die dramatically')
            elif player_type == 3:  # Tyhrranoid
                # Tyhrranoid taking damage state (updates state to trigger death animation once at 0 health)
                self._write8(RAC3STATUS.ACTION, 0x55)
                self._write8(RAC3STATUS.ACTION + 0xC, 0x55)  # Past state
                self._write8(RAC3STATUS.ACTION + 0x18, 0x55)  # This address helps the death animation trigger
                logger.debug(f'player is tyhrranoid, tyhrranoid must be squished')
            logger.debug(f'player successfully killed')
            return True
        else:
            logger.debug(f'player unable to be killed')
            return False

    def respawn_inputs(self) -> bool:
        pressed_square = bool(self.inputs & RAC3INPUT.SQUARE)
        return self.pause_menu and pressed_square
