import time
from dataclasses import dataclass
from enum import IntEnum
from random import randint, uniform
from struct import unpack
from typing import Any, Optional

from BaseClasses import ItemClassification
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
from worlds.rac3.constants.instruction import RAC3INSTRUCTION
from worlds.rac3.constants.item_tags import RAC3ITEMTAG
from worlds.rac3.constants.items import QUICK_SELECT_LIST, RAC3ITEM, UPGRADE_DICT
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.messages.box_format import THEME_ID_TO_THEME_COLORS
from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME
from worlds.rac3.constants.messages.messagebox import RAC3MESSAGEBOX
from worlds.rac3.constants.messages.text_color import RAC3TEXTCOLOR
from worlds.rac3.constants.messages.text_format import CLASSIFICATION_TO_COLOR, COLOR_NAME_TO_BYTE
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.player_type import PLAYER_TYPE_TO_NAME, RAC3PLAYERTYPE
from worlds.rac3.constants.region import (PLANET_FROM_INFOBOT, PLANET_NAME_FROM_ID, RAC3REGION, RESPAWN_COORDS_OFFSET,
                                          SHIP_SLOTS)
from worlds.rac3.constants.status import RAC3STATUS
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

    def _write_string(self, address: int, value: str):
        self.pcsx2_interface.write_string(address, value)

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
            match game_id:
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
                case RAC3STATUS.JP_TB_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: Japanese The Best release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case RAC3STATUS.KO_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: Korean release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case RAC3STATUS.CH_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: Chinese release')
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
    self_respawning: bool = False
    reloading_handled: bool = False
    is_reloading: int = 0
    ship: int = 0
    ship_skin: int = 0
    skin: int = 0
    timers: dict[str, int] = {}
    weaponLevelLockFlag: bool = None
    planet: str = RAC3REGION.GALAXY
    player_type: str = RAC3PLAYERTYPE.RATCHET
    vehicle: int = 0
    action: int = 0  # Todo: Player Action
    prev_action: int = 0
    pause_menu: bool = False
    pause_state: bool = False
    inputs: int = RAC3INPUT.NOTHING
    health: int = 100
    max_health: int = 10
    main_menu: bool = False
    ryno: bool = False
    death_count: int = 0
    last_death_count: int = 0
    last_death_state: int = 0
    has_died: bool = False
    inside_hacker_puzzle: bool = False
    notification_queue: list[tuple] = []
    notification_time: float | None = None
    notification_merge_count: int = 1
    message_display: bool = False
    ship_slot_limit: int = 0
    one_hp_challenge: dict[str, bool] = None

    # Called at once when client started
    def init(self):
        self.init_variables()

    def reset_file(self):
        self.remove_all_items()
        self.undo_collections()

    def important_items(self, item: int, us: str, them: str, location: int):
        """Runs when loading into game from the main menu to update the player with important items from the server,
        skips filler and trap items to not flood the player with bolts/xp"""
        if (RAC3ITEMTAG.FILLER in RAC3_ITEM_DATA_TABLE[ITEM_FROM_AP_CODE[item]].TAGS or RAC3ITEMTAG.TRAP in
                RAC3_ITEM_DATA_TABLE[ITEM_FROM_AP_CODE[item]].TAGS):
            return
        self.item_received(item, us, None, location)

    def early_update(self):
        self.planet = PLANET_NAME_FROM_ID[self._read8(RAC3STATUS.PLANET)]
        self.player_type = PLAYER_TYPE_TO_NAME[self._read8(RAC3STATUS.PLAYER_TYPE)]
        self.vehicle = self._read32(RAC3STATUS.VEHICLE_POINTER)
        self.action = self._read8(RAC3STATUS.ACTION)
        self.prev_action = self._read8(RAC3STATUS.PREV_ACTION)
        self.inputs = self._read16(RAC3STATUS.READ_INPUT)
        self.health = self._read8(RAC3STATUS.HEALTH)
        self.max_health = self._read8(RAC3STATUS.MAX_HEALTH)
        self.is_reloading = self._read8(RAC3STATUS.FORCE_RELOAD)
        self.inside_hacker_puzzle = self._read8(RAC3STATUS.HELD_ITEM) == RAC3_ITEM_DATA_TABLE[RAC3ITEM.HACKER].ID
        self.message_display = bool(self._read_float(self._read32(RAC3MESSAGEBOX.VISIBLE_POINTER)))

        self.pause_check()
        if self.self_respawning:
            if not self.is_reloading:
                self.self_respawning = False

    # Called in periodically
    def late_update(self):
        # Memory checking
        self.gadget_cycler()
        self.planet_cycler()
        self.weapon_cycler()
        self.vidcomic_cycler()
        self.armor_cycler()
        self.timer_cycler()
        self.verify_quick_select_and_last_used()
        self.notification_cycler()
        # Proc Options
        self.multiplier_cycler()
        self.overflow_fix()
        self.health_cycler()
        if self.weaponLevelLockFlag:
            self.weapon_exp_cycler()
        # Logic Fixes
        self.logic_fixes()
        # If loading from the main menu we delay fixing the current health until the load is complete
        if self.main_menu:
            if self.max_health > 10:
                self._write8(RAC3STATUS.HEALTH, self.max_health)
                self.main_menu = False

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
        self.one_hp_challenge = slot_data[RAC3OPTION.ONE_HP_CHALLENGE]

    def map_switch(self) -> tuple[str, str]:
        planet = RAC3_REGION_DATA_TABLE[self.planet].ID
        _planet = planet
        if planet > 55 or not self._read8(RAC3STATUS.MAP_CHECK):
            _planet = 0
        elif planet > 29:
            _planet = 3
        return PLANET_NAME_FROM_ID[planet], PLANET_NAME_FROM_ID[_planet]

    def tyhrranosis_fix(self):
        self._write8(RAC3STATUS.ROBONOIDS, 0)

    def item_received(self, item_code: int, our_name: Optional[str], other_player: Optional[str], location: Optional[
        int]):
        name = PROG_TO_NAME_DICT.get(ITEM_FROM_AP_CODE[item_code], ITEM_FROM_AP_CODE[item_code])
        if other_player is not None:
            classification = RAC3_ITEM_DATA_TABLE[name].AP_CLASSIFICATION
            if other_player == our_name:
                if location == 0:
                    pass
                elif location > 0:
                    if classification == ItemClassification.trap:
                        self.notification_queue.append(
                            (f'{RAC3TEXTCOLOR.WHITE}Activated {RAC3TEXTCOLOR.NORMAL}{ITEM_FROM_AP_CODE[item_code]} '
                             f'{RAC3TEXTCOLOR.WHITE}at\\n{RAC3TEXTCOLOR.WHITE}{LOCATION_FROM_AP_CODE[location]}', 
                             RAC3BOXTHEME.WARNING))
                    else:
                        self.notification_queue.append(
                            (f'Found {CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]} '
                            f'{RAC3TEXTCOLOR.NORMAL}at\\n{LOCATION_FROM_AP_CODE[location]}', RAC3BOXTHEME.DEFAULT))
                else:
                    if classification == ItemClassification.trap:
                        self.notification_queue.append(
                            (f'{RAC3TEXTCOLOR.WHITE}Activated {RAC3TEXTCOLOR.NORMAL}{ITEM_FROM_AP_CODE[item_code]}',
                             RAC3BOXTHEME.WARNING))
                    else:
                        self.notification_queue.append(
                            (f'Collected {CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]}',
                            RAC3BOXTHEME.DEFAULT))
            else:
                if classification == ItemClassification.trap:
                    self.notification_queue.append((
                        f'{RAC3TEXTCOLOR.GREEN}{other_player}{RAC3TEXTCOLOR.WHITE} activated your '
                        f'{RAC3TEXTCOLOR.NORMAL}{ITEM_FROM_AP_CODE[item_code]}', RAC3BOXTHEME.WARNING))
                else:
                    self.notification_queue.append((
                        f"Received {CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]} "
                        f"{RAC3TEXTCOLOR.NORMAL}from "
                        f"{RAC3TEXTCOLOR.GREEN}{other_player}", RAC3BOXTHEME.DEFAULT))
        logger.debug(f'Item received: {ITEM_FROM_AP_CODE[item_code]}, AP code: {item_code}')
        if name in infobot_data.keys():
            if self.UnlockItem[name].status:
                return
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
                new_bolts = bolt + 1000 * randint(1, 100)
                if new_bolts > 0x7FFFFFFF:
                    new_bolts = 0x7FFFFFFF
                self._write32(RAC3STATUS.BOLTS, new_bolts)
            case RAC3ITEM.INFERNO_MODE:
                timer = self._read32(RAC3STATUS.INFERNO_TIMER)
                new_timer = timer + 1000 + randint(1, 100)
                if new_timer > 0x7FFFFFFF:
                    new_timer = 0x7FFFFFFF
                self._write32(RAC3STATUS.INFERNO_TIMER, new_timer)
            case RAC3ITEM.JACKPOT:
                # TODO rework jackpot filler item to extend time instead of increasing multiplier
                # Limit multiplier to 128x
                if self.boltAndXPMultiplierValue <= 6: 
                    _time = round(time.time() + uniform(10, 30), 4)
                    self.timers[name + str(_time)] = _time
                    self.boltAndXPMultiplierValue += 1
            case RAC3ITEM.PLAYER_XP:
                exp = self._read32(RAC3STATUS.NANOTECH_EXP)
                level = self._read8(RAC3STATUS.MAX_HEALTH)
                new_exp = exp + 10000 + randint(1, 300 * level)
                if new_exp > 0x7FFFFFFF:
                    new_exp = 0x7FFFFFFF
                self._write32(RAC3STATUS.NANOTECH_EXP, new_exp)
            case RAC3ITEM.WEAPON_XP:
                valid_weapons = []
                for weapon_name in non_prog_weapon_data.keys():
                    if self.UnlockItem[weapon_name].status:
                        level = self._read8(non_prog_weapon_data[weapon_name].LEVEL)
                        if ((weapon_name != RAC3ITEM.RY3N0 and level < 5) or
                                (weapon_name == RAC3ITEM.RY3N0 and level < 4) or
                                (weapon_name == RAC3ITEM.RY3N0 and level < 5 and not self.ryno)):
                            valid_weapons.append(weapon_name)

                if valid_weapons:
                    weapon_num = randint(0, len(valid_weapons) - 1)
                    self.weapon_level_up(valid_weapons[weapon_num])
            case RAC3ITEM.OHKO_TRAP:
                self._write8(RAC3STATUS.NANOPAK_HEALTH, 0)
                self._write8(RAC3STATUS.HEALTH, 1)
                if self.player_type == RAC3PLAYERTYPE.GIANT:
                    self._write32(RAC3STATUS.GIANT_CLANK_HEALTH, 1)
            case RAC3ITEM.NO_AMMO_TRAP:
                for weapon_name in non_prog_weapon_data.keys():
                    if self.UnlockItem[weapon_name].status:
                        self._write8(non_prog_weapon_data[weapon_name].AMMO_ADDRESS, 0)
                self._write8(RAC3STATUS.QWARK_AMMO, 0)
            case RAC3ITEM.LOCK_TRAP:
                    if self.timers.get(name, False):
                        self.timers[name] += randint(5, 15)
                    else:
                        self.timers[name] = int(time.time() + uniform(5, 15))
            case RAC3ITEM.MIRROR_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(5, 20)
                else:
                    self.timers[name] = int(time.time() + uniform(5, 20))
            case RAC3ITEM.BLACK_SCREEN_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(3, 5)
                else:
                    self.timers[name] = int(time.time() + uniform(3, 5))
            case RAC3ITEM.NO_CLANK_TRAP:
                    if self.timers.get(name, False):
                        self.timers[name] += randint(5, 20)
                    else:
                        # Special case for holostar, nefarious base and klunk fight
                        already_no_clank = self._read8(RAC3STATUS.NO_CLANK)
                        if already_no_clank == 0:
                            self.timers[name] = int(time.time() + uniform(5, 20))
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
        self.notification_cycler()

    def undo_collections(self):
        self.health = self._read8(RAC3STATUS.HEALTH)
        sewer, nano = 0, 0
        for location in RAC3_LOCATION_DATA_TABLE.values():
            if RAC3TAG.SEWER in location.TAGS:
                if not sewer:
                    self._write8(location.CHECK_ADDRESS[0].ADDRESS, 0)  # Reset to 0 Crystals
                    sewer += 1
                continue
            if RAC3TAG.NANOTECH in location.TAGS:
                if not nano:
                    self._write8(location.CHECK_ADDRESS[0].ADDRESS, 10)  # Reset to 10 Health
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

    def fix_health(self):
        self._write8(RAC3STATUS.HEALTH, self.health)

    def reset_death_count(self):
        self.death_count = self._read32(RAC3STATUS.DEATH_COUNT)
        self.last_death_count = self.death_count

    def add_cosmetics(self):
        self._write8(RAC3STATUS.SHIP_CONFIG, self.ship)
        self._write8(RAC3STATUS.SHIP_SKIN, self.ship_skin)
        self._write8(RAC3STATUS.PLAYER_SKIN, self.skin)
        self._write8(RAC3STATUS.PLAYER_SKIN_2, self.skin)

    # Logic Fixes
    def logic_fixes(self):
        # Fix can't play Qwark VidComics in some case which first event is skipped
        if self.planet == RAC3REGION.STARSHIP_PHOENIX:
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
                if name == RAC3ITEM.RY3N0 and self.ryno:
                    _xp = self._read32(RAC3_ITEM_DATA_TABLE[name].XP_ADDRESS)
                    threshold_id = UPGRADE_DICT[name][3]
                    threshold_xp = RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID[threshold_id]].XP_THRESHOLD
                    if _xp > threshold_xp:
                        self._write32(RAC3_ITEM_DATA_TABLE[name].XP_ADDRESS, threshold_xp)
                        self._write8(RAC3_ITEM_DATA_TABLE[name].LEVEL_ADDRESS, threshold_id)
            else:
                self._write8(addr, 0)

        equip_data = self._read8(RAC3STATUS.EQUIPPED)
        if equip_data > 1 and self.UnlockItem.get(ITEM_NAME_FROM_ID.get(equip_data)).status == 0:  # Not unlocked
            last_1 = self._read8(RAC3STATUS.LAST_USED_1)
            if last_1 == 0:
                self._write8(RAC3STATUS.EQUIPPED, equipable_data[RAC3ITEM.WRENCH].ID)
                self._write8(RAC3STATUS.LAST_USED_0, 0)
                return
            last_2 = self._read8(RAC3STATUS.LAST_USED_2)
            last_3 = self._read8(RAC3STATUS.LAST_USED_3)
            if self.UnlockItem.get(ITEM_NAME_FROM_ID.get(last_1)).status:
                self._write8(RAC3STATUS.EQUIPPED, last_1)
                self._write8(RAC3STATUS.LAST_USED_0, last_1)
                self._write8(RAC3STATUS.LAST_USED_1, last_2)
                self._write8(RAC3STATUS.LAST_USED_2, last_3)
                return
            if last_2 == 0:
                self._write8(RAC3STATUS.EQUIPPED, equipable_data[RAC3ITEM.WRENCH].ID)
                self._write8(RAC3STATUS.LAST_USED_0, 0)
                self._write8(RAC3STATUS.LAST_USED_1, 0)
                return
            last_4 = self._read8(RAC3STATUS.LAST_USED_4)
            if self.UnlockItem.get(ITEM_NAME_FROM_ID.get(last_2)).status:
                self._write8(RAC3STATUS.EQUIPPED, last_2)
                self._write8(RAC3STATUS.LAST_USED_0, last_2)
                self._write8(RAC3STATUS.LAST_USED_1, last_3)
                self._write8(RAC3STATUS.LAST_USED_2, last_4)
                return
            last_5 = self._read8(RAC3STATUS.LAST_USED_5)
            self._write8(RAC3STATUS.LAST_USED_0, last_3)
            self._write8(RAC3STATUS.LAST_USED_1, last_4)
            self._write8(RAC3STATUS.LAST_USED_2, last_5)
            if last_3 == 0 or self.UnlockItem.get(ITEM_NAME_FROM_ID.get(last_3)).status:
                self._write8(RAC3STATUS.EQUIPPED, equipable_data[RAC3ITEM.WRENCH].ID)
            else:
                self._write8(RAC3STATUS.EQUIPPED, last_3)

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
                if name == RAC3ITEM.QWARKS_HIDEOUT and not self.UnlockItem[RAC3ITEM.REFRACTOR].status:
                    # Write 0 if Qwarks Hideout is missing Refractor
                    self._write8(addr, 0)
                elif name == RAC3ITEM.HOLOSTAR_STUDIOS and (
                        self.UnlockItem[RAC3ITEM.HACKER].status == 0 or self.UnlockItem[RAC3ITEM.HYPERSHOT].status == 0):
                    # Write 0 if Holostar Studios is missing Hacker or Hypershot
                    self._write8(addr, 0)
                else:
                    if self.UnlockItem[name].unlock_delay:
                        # logger.debug(f'Write access to: {name} at {hex(addr)} value: {hex(planet.ID)}')
                        self._write8(addr, planet.ID)
                    else:
                        self.UnlockItem[name].unlock_delay += 1
        for number, slot in enumerate(SHIP_SLOTS):
            self.ship_slot_limit = self.UnlockItem[RAC3REGION.SLOT_0].status
            if number >= self.ship_slot_limit:
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
            if self.ryno and weapon_name == RAC3ITEM.RY3N0 and target_level > 4:
                target_level = 4
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
            self._write8(weapon_data.LEVEL_ADDRESS, target_id)

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

    def notification_cycler(self):
        current_time = time.time()
        tyhrranoid_game = self.player_type == RAC3PLAYERTYPE.TYHRRANOID and self.action == 0x58
        self._write32(RAC3MESSAGEBOX.HIDDEN_AND_PAUSED, int(self.inside_hacker_puzzle)) # Hide message box during hacker puzzle
        if self.notification_queue:
            if not self.notification_time:
                self.notification_time = current_time + 3
            if not tyhrranoid_game:
                if self.notification_time < current_time and not self.message_display:
                    # Pop the number of messages that were displayed last cycle
                    for _ in range(self.notification_merge_count):
                        if self.notification_queue:
                            self.notification_queue.pop(0)
                    self.reset_messagebox_theme()
                    logger.debug(f'notification queue: {len(self.notification_queue)}')
                    self.notification_time = current_time + 3
                if self.notification_queue:
                    # Merge up to 3 notifications of the same theme, but do not exceed 225 chars
                    merged_message, theme = self.notification_queue[0]
                    merge_count = 1
                    total_length = len(merged_message)
                    for i in range(1, min(3, len(self.notification_queue))):
                        next_message, next_theme = self.notification_queue[i]
                        # +2 for the '\n' separator
                        add_length = 2 + len(next_message)
                        if next_theme == theme and (total_length + add_length) <= 225:
                            merged_message += "\\n" + next_message
                            total_length += add_length
                            merge_count += 1
                        else:
                            break
                    self.notification_merge_count = merge_count
                    msg_list, color_bytes_count, longest_line_length = self.format_textbox_string(merged_message)
                    if not self.message_display:
                        self.notification_time = current_time + 3
                        display_time = int((self.notification_time - current_time)*120)
                        self.messagebox(msg_list, color_bytes_count, longest_line_length, theme, display_time)
                    else:
                        write_message = b''
                        for line in msg_list:
                            write_message += line
                        read_message = self._read_bytes(RAC3MESSAGEBOX.MESSAGE, len(write_message))
                        if read_message != write_message:
                            # Give the player a bit more time to read the new appended line in case it was about to expire
                            self.notification_time += 0.33
                            display_time = int((self.notification_time - current_time)*120)
                            # A lot of messages can cause this value to go negative and if so, set a minimum display time
                            if display_time < 0:
                                self.notification_time = current_time + 0.33
                                display_time = int((self.notification_time - current_time)*120)
                            self.messagebox(msg_list, color_bytes_count, longest_line_length, theme, display_time)
                            logger.debug(f'Warning: Incorrect Display message detected')
                            logger.debug(f'Message: {merged_message}')
                            logger.debug(f'{read_message}')
                            logger.debug(f'{write_message}')
        else:
            self.notification_time = None
            self.notification_merge_count = 1

    def dump_info(self, slot_data: dict[str, Any]):
        logger.info(f'Collected Items: {self.UnlockItem}')
        count = 0
        for name in SHIP_SLOTS:
            logger.info(
                f'Planet{count}: {PLANET_NAME_FROM_ID[self._read8(RAC3_REGION_DATA_TABLE[name].SLOT_ADDRESS)]}')
            count += 1
        logger.info(f'Current planet Tracked: {self.planet}')
        logger.info(f'Ship Slot Limit: {self.ship_slot_limit}')
        logger.info(f'Softlock Prevention:\nHolostar Studios - {self.softlock_prevention_check(RAC3REGION.HOLOSTAR_STUDIOS)}\nQwarks Hideout - {self.softlock_prevention_check(RAC3REGION.QWARKS_HIDEOUT)}')
        logger.info(f'Slot Data: {slot_data}')

    def multiplier_cycler(self):
        self._write32(RAC3STATUS.JACKPOT_TIMER, 0x7FFFFFFF)
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
                    status = timer_to_status[name]
                    match status:
                        case RAC3STATUS.BLACK_SCREEN:
                            self._write16(status, 0)
                        case _:
                            self._write8(status, 1)
            else:
                self.timers.pop(name)
                if 'Jackpot' in name:
                    self.notification_queue.append((f'{RAC3TEXTCOLOR.WHITE}Jackpot x{2 ** self.boltAndXPMultiplierValue} '
                                                    f'{RAC3TEXTCOLOR.NORMAL}effect has worn off.', RAC3BOXTHEME.DEFAULT))
                else:
                    self.notification_queue.append((f'{name}{RAC3TEXTCOLOR.WHITE} effect has worn off.', RAC3BOXTHEME.WARNING))
                match _name:
                    case RAC3ITEM.LOCK_TRAP:  # Special case for lock trap
                        # Clear when timer ends directly rather than from the trap cleanup loop below
                        # Todo: Check for arena mission
                        self._write8(RAC3STATUS.WEAPON_LOCK, 0)
                    case RAC3ITEM.JACKPOT:
                        self.boltAndXPMultiplierValue -= 1
                    case RAC3ITEM.MIRROR_TRAP:
                        self._write8(RAC3STATUS.MIRROR_UNIVERSE, 0)
                    case RAC3ITEM.BLACK_SCREEN_TRAP:
                        self._write16(RAC3STATUS.BLACK_SCREEN, 0x8C)
                    case RAC3ITEM.NO_CLANK_TRAP:
                        self._write8(RAC3STATUS.NO_CLANK, 0)

        # Remove trap effects for traps not in the timer dictionary to prevent any stuck effects
        # Prevent not having lock trap from unlocking weapon during arena weapon specific challenges every cycle
        # for trap_name, status_address in trap_to_status.items():
        #     if trap_name not in self.trap_timers and trap_name != RAC3ITEM.LOCK_TRAP:
        #         self._write8(status_address, 0)

    def health_cycler(self):
        """
        Enforces one HP challenge for player and vehicle if enabled in settings
        Sets health to 1 if above 1 for the current character
        """
        character = self.player_type
        if character == RAC3PLAYERTYPE.TYHRRANOID:
            character = RAC3PLAYERTYPE.RATCHET # Treat Tyhrranoid as Ratchet for one HP challenge
        # Check for one HP challenge for current character
        if self.one_hp_challenge.get(character, False):
            if character == RAC3PLAYERTYPE.GIANT:
                if self._read32(RAC3STATUS.GIANT_CLANK_HEALTH) > 1:
                    self._write32(RAC3STATUS.GIANT_CLANK_HEALTH, 1)
            else:
                # Applies to Ratchet, Clank, Qwark
                # Ban shield charger usage if one HP challenge is active for Ratchet
                if character == RAC3PLAYERTYPE.RATCHET:
                    self._write8(non_prog_weapon_data[RAC3ITEM.SHIELD_CHARGER].AMMO_ADDRESS, 0)
                if self._read8(RAC3STATUS.HEALTH) > 1:
                    self._write8(RAC3STATUS.HEALTH, 1)
                    self._write8(RAC3STATUS.NANOPAK_HEALTH, 0)
                if character == RAC3PLAYERTYPE.RATCHET and self.planet == RAC3REGION.ANNIHILATION_NATION and not self.pause_state:
                    # Patch out sleeping gas health reduction to prevent death
                    self._write32(RAC3INSTRUCTION.NATION_SLEEP_GAS_HEALTH_UPDATE, 0x24420000) # addiu v0,v0,0x0
                    # Patch out health refill to prevent auto losing One Hit Wonder challenge
                    self._write32(RAC3INSTRUCTION.NATION_HEALTH_REFILL, 0x00000000) # nop

        # Vehicle one HP challenge is independent of player_type
        if self.vehicle and self.one_hp_challenge.get(RAC3PLAYERTYPE.VEHICLE, False):
            health_addr = self._read32(self._read32(self.vehicle + 0x68))
            if self._read_float(health_addr) > 5.0:
                # This displays as 1 HP in-game for vehicles
                self._write_float(health_addr, 5)
        
        if not self.one_hp_challenge.get(character, False) and self.planet == RAC3REGION.ANNIHILATION_NATION and not self.pause_state:
            # Restore sleeping gas health reduction if one HP challenge is not active for Ratchet
            self._write32(RAC3INSTRUCTION.NATION_SLEEP_GAS_HEALTH_UPDATE, 0x2442FFFF) # addiu v0,v0,-0x1
            self._write32(RAC3INSTRUCTION.NATION_HEALTH_REFILL, 0xAC652850) # sw a1,0x2850(v1)

    def overflow_fix(self):
        nanotech_exp = self._read32(RAC3STATUS.NANOTECH_EXP)
        if nanotech_exp > 0x7FFFFFFF:
            self._write32(RAC3STATUS.NANOTECH_EXP, 0)
            self.notification_queue.append((f'Negative Nanotech EXP detected! Resetting EXP to 0', RAC3BOXTHEME.WARNING))
        # If other stuff needs overflow fixing, add here

    def reload_check(self):
        """Detects if the game is currently being reloaded, and updates death data"""
        if self.is_reloading and not self.reloading_handled and not self.self_respawning:
            self.last_death_state = self.action
            self.reloading_handled = True
            logger.debug(f'{self.player_type} is Respawning, death state: {self.last_death_state},'
                         f' death count: {self.last_death_count}')
        if not self.is_reloading and self.reloading_handled:
            self.death_count = self._read32(RAC3STATUS.DEATH_COUNT)
            self.has_died = self.death_count > self.last_death_count
            self.last_death_count = self.death_count
            self.reloading_handled = False
            logger.debug(f'{self.player_type} has Respawned, death count: {self.death_count}, has died?'
                         f' {self.has_died}')
        else:
            self.has_died = False

    def pause_check(self):
        if self.planet not in RAC3_REGION_DATA_TABLE.keys():
            # Unknown planet, assume paused to be safe
            self.pause_menu = True
            self.pause_state = True
            return

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
        self.self_respawning = True
        self._write8(RAC3STATUS.FORCE_RELOAD, 1)

    def teleport_to_coords(self):
        self._write_bytes(RAC3STATUS.RATCHET_X, self._read_bytes(RAC3STATUS.ENTRANCE_X, 28))

    def alive(self) -> tuple[bool, str]:
        if self.has_died:
            self.last_death_count = self.death_count
            logger.debug(f'Death Detected! (death count increased)')
            is_clank = self.player_type == RAC3PLAYERTYPE.CLANK
            death = DEATH_FROM_ACTION.get(self.last_death_state, 'Died') if not is_clank else (
                CLANK_DEATH_FROM_ACTION.get(self.last_death_state, 'Died'))
            return False, f"{self.player_type} {death}"

        logger.debug(f'{self.player_type} is Alive')
        return True, f"{self.player_type} is Alive"

    def kill_player(self) -> bool:
        if not self.pause_state and not self.inside_hacker_puzzle:
            self._write8(RAC3STATUS.HEALTH, 0)
            self._write8(RAC3STATUS.NANOPAK_HEALTH, 0)
            # death = choice(list(DEATH_FROM_ACTION.keys()))
            if self.vehicle != 0:
                health_addr = self._read32(self._read32(self.vehicle + 0x68))
                self._write32(health_addr, 0)  # health is a float, but we can write 0 as int32
                if self.planet == RAC3REGION.MARCADIA:
                    # special case for the marcadia turret mission that cant blow up
                    # this will force mission failure and increase death count by 1
                    vehicle_reload_addr = self.vehicle + 0xCB
                    self._write8(vehicle_reload_addr, 0xD0)  # 0xD0: force reload from vehicle death
                else:
                    vehicle_blow_up_addr = self.vehicle + 0xBC
                    self._write8(vehicle_blow_up_addr, 0x9)  # 0x9: blow up vehicle immediately 0xA: force respawn
                # self._write8(RAC3STATUS.ACTION, death)
                logger.debug(f'player in vehicle, killing vehicle too')
                # logger.debug(f'player died of {DEATH_FROM_ACTION[death]}')
            else:
                match self.player_type:
                    case RAC3PLAYERTYPE.RATCHET:
                        if self.action not in DEATH_FROM_ACTION.keys() and self.vehicle == 0:
                            self._write8(RAC3STATUS.ACTION, 0x16)
                            # update ratchet state to cancel free fall and other problematic states

                        # self._write8(RAC3STATUS.ACTION, death)
                        # logger.debug(f'player died of {DEATH_FROM_ACTION[death]}')
                    case RAC3PLAYERTYPE.CLANK:
                        # Clank taking damage state (updates state to trigger death animation once at 0 health)
                        self._write8(RAC3STATUS.ACTION, 0x42)
                        self._write8(RAC3STATUS.PREV_ACTION, 0x42)  # Past state
                        self._write8(RAC3STATUS.SECOND_PREV_ACTION, 0x42)  # This helps the death animation trigger
                        logger.debug(f'player is clank, clank must die dramatically')
                    case RAC3PLAYERTYPE.GIANT:
                        # Giant Clank punched state (updates state to trigger death animation once at 0 health)
                        self._write32(RAC3STATUS.GIANT_CLANK_HEALTH, 0)
                        self._write8(RAC3STATUS.ACTION, 0x5D)
                        self._write8(RAC3STATUS.PREV_ACTION, 0x5D)  # Past state
                        self._write8(RAC3STATUS.SECOND_PREV_ACTION, 0x5D)  # This helps the death animation trigger
                        logger.debug(f'player is giant clank, giant clank must die dramatically')
                    case RAC3PLAYERTYPE.TYHRRANOID:
                        # Tyhrranoid taking damage state (updates state to trigger death animation once at 0 health)
                        self._write8(RAC3STATUS.ACTION, 0x55)
                        self._write8(RAC3STATUS.PREV_ACTION, 0x55)  # Past state
                        self._write8(RAC3STATUS.SECOND_PREV_ACTION, 0x55)  # This helps the death animation trigger
                        logger.debug(f'player is tyhrranoid, tyhrranoid must be squished')
                    case RAC3PLAYERTYPE.QWARK:
                        # Qwark taking damage state (updates state to trigger death animation once at 0 health)
                        self._write8(RAC3STATUS.ACTION, 0x9E)
                        self._write8(RAC3STATUS.PREV_ACTION, 0x9E)  # Past state
                        self._write8(RAC3STATUS.SECOND_PREV_ACTION, 0x9E)  # This helps the death animation trigger
                        logger.debug(f'player is qwark, qwark must die dramatically')
            logger.debug(f'player successfully killed')
            return True
        else:
            logger.debug(f'player unable to be killed')
            return False

    def respawn_inputs(self) -> bool:
        pressed_square = bool(self.inputs & RAC3INPUT.SQUARE)
        return self.pause_menu and pressed_square

    def messagebox(self, msg_list: list[bytes], color_bytes_count: int, longest_line_length: int, box_theme: int =
    RAC3BOXTHEME.DEFAULT, time: int = 0x168) -> None:
        if time < 0:
            time = 0
        # real overflow cap is actually about 248, but we don't need that long messages
        curr_addr = RAC3MESSAGEBOX.MESSAGE
        msg_bytes = b''
        for idx, line in enumerate(msg_list):
            msg_bytes += line
            # self._write_bytes(curr_addr, line)
            # Write pointer to this line at pointer_addr + 4*idx
            self._write32(RAC3MESSAGEBOX.TEXT_POINTER + 4 * idx, curr_addr)
            # Move to next address after this string
            curr_addr += len(line)
        self._write32(RAC3MESSAGEBOX.NUM_LINES, len(msg_list))
        msg_length = int(longest_line_length - color_bytes_count)
        width = msg_length * 7 + 12
        if width % 2 != 0:
            # Odd numbered width values display as if it was the even number below it
            # Ex: 101 width displays as 100 width
            width += 1

        theme_format = THEME_ID_TO_THEME_COLORS[box_theme]
        box_color = theme_format.BOX
        text_color = theme_format.TEXT
        background_color = theme_format.BACKGROUND
        self._write32(self._read32(RAC3MESSAGEBOX.BACKGROUND_COLOR_POINTER), background_color)
        self._write32(self._read32(RAC3MESSAGEBOX.EDGE_COLOR_POINTER), box_color)
        self._write32(self._read32(RAC3MESSAGEBOX.CENTER_COLOR_POINTER), box_color)
        self._write32(self._read32(RAC3MESSAGEBOX.TEXT_COLOR_POINTER), text_color)

        self._write32(RAC3MESSAGEBOX.TIMER, time)
        self._write32(RAC3MESSAGEBOX.TEXT_POINTER, RAC3MESSAGEBOX.MESSAGE)
        self._write32(RAC3MESSAGEBOX.BOX_WIDTH, width)
        self._write_bytes(RAC3MESSAGEBOX.MESSAGE, msg_bytes)
        self._write_float(self._read32(RAC3MESSAGEBOX.VISIBLE_POINTER), 1.0)

    def format_textbox_string(self, msg: str) -> tuple[list[bytes], int, int]:
        # Split message on \n to handle newlines
        lines = msg.split('\\n')
        color_byte_count = 0
        # Write each line to memory, update string pointers
        longest_line_length = 0
        message_list: list[bytes] = []
        for idx, line in enumerate(lines):
            # Convert to bytes, add null terminator
            line_bytes, line_color_byte_count = self.format_color_string(line)
            line_bytes += b'\x00'
            message_list.append(line_bytes)
            if len(line_bytes) > longest_line_length:
                longest_line_length = len(line_bytes)
                color_byte_count = line_color_byte_count
        return message_list, color_byte_count, longest_line_length

    @staticmethod
    def format_color_string(msg: str) -> tuple[bytes, int]:
        result = bytearray()
        color_byte_count = 0
        i = 0
        while i < len(msg):
            matched = False
            for code, byte in COLOR_NAME_TO_BYTE.items():
                if msg.startswith(code, i):
                    # Insert the color code byte (as a single byte)
                    if isinstance(byte, str):
                        byte = ord(byte)
                    result.append(byte)
                    color_byte_count += 1
                    i += len(code)
                    matched = True
                    break
            if not matched:
                # Insert the ASCII value of the character
                result.append(ord(msg[i]))
                i += 1
        color_byte_count += 1  # Count the null terminator
        return bytes(result), color_byte_count

    def reset_messagebox_theme(self) -> None:
        default_theme = THEME_ID_TO_THEME_COLORS[RAC3BOXTHEME.DEFAULT]
        self._write32(self._read32(RAC3MESSAGEBOX.BACKGROUND_COLOR_POINTER), default_theme.BACKGROUND)
        self._write32(self._read32(RAC3MESSAGEBOX.EDGE_COLOR_POINTER), default_theme.BOX)
        self._write32(self._read32(RAC3MESSAGEBOX.CENTER_COLOR_POINTER), default_theme.BOX)
        self._write32(self._read32(RAC3MESSAGEBOX.TEXT_COLOR_POINTER), default_theme.TEXT)
    
    def softlock_prevention_check(self, planet: str) -> bool:
        match planet:
            case RAC3REGION.QWARKS_HIDEOUT:
                return (self.UnlockItem[RAC3ITEM.QWARKS_HIDEOUT].status > 0 and 
                        (self.UnlockItem[RAC3ITEM.REFRACTOR].status == 0))
            case RAC3REGION.HOLOSTAR_STUDIOS:
                return (self.UnlockItem[RAC3ITEM.HOLOSTAR_STUDIOS].status > 0 and
                        (self.UnlockItem[RAC3ITEM.HACKER].status == 0 or
                        self.UnlockItem[RAC3ITEM.HYPERSHOT].status == 0))
        return False
