"""This module provides an RAC3 interface to control the game"""
import time
from dataclasses import dataclass
from random import choice, randint, uniform
from typing import Any, Optional

from BaseClasses import ItemClassification
from CommonClient import logger
from worlds.rac3.client.general_interface import GameInterface
from worlds.rac3.constants.check_type import CHECKTYPE
from worlds.rac3.constants.data.address import RAC3ADDRESSDATA
from worlds.rac3.constants.data.item import (armor_data, equipable_data, gadget_data, infobot_data, ITEM_FROM_AP_CODE,
                                             ITEM_NAME_FROM_ID, non_prog_weapon_data, PROG_TO_NAME_DICT,
                                             RAC3_ITEM_DATA_TABLE, timer_to_status, vidcomic_data)
from worlds.rac3.constants.data.location import (LOCATION_FROM_AP_CODE, LOCATION_TO_INFOBOT_FLAG,
                                                 RAC3_LOCATION_DATA_TABLE, RAC3LOCATIONDATA,
                                                 REGION_TO_INFOBOT_LOCATION)
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
from worlds.rac3.constants.messages.text_format import CLASSIFICATION_TO_COLOR, FORMAT_NAME_TO_BYTE
from worlds.rac3.constants.messages.text_strings import RAC3TEXTFORMATSTRING
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.pause_state import RAC3PAUSESTATE
from worlds.rac3.constants.player_type import PLAYER_TYPE_TO_NAME, RAC3PLAYERTYPE
from worlds.rac3.constants.region import (PLANET_FROM_INFOBOT, PLANET_NAME_FROM_ID, RAC3REGION, RESPAWN_COORDS_OFFSET,
                                          SHIP_SLOTS)
from worlds.rac3.constants.status import RAC3STATUS


class Rac3Interface(GameInterface):
    """Handles reading and modifying the game memory"""

    @dataclass
    class UnlockData:
        """Data structure for tracking if items should be unlocked and if they are now being unlocked"""
        status: int
        unlock_delay: int

        def __init__(self,
                     status: int = 0,
                     unlock_delay: int = 0):
            self.status = status
            self.unlock_delay = unlock_delay

        def __repr__(self):
            return f'{{ status: {self.status}, unlock_delay: {self.unlock_delay} }}'

    @dataclass
    class Options:
        """Data structure for storing options"""
        start_inventory_from_pool: dict[str, int]
        starting_weapons: dict[str, int]
        bolt_and_xp_multiplier: int
        enable_progressive_weapons: int
        armor_upgrade: int
        skill_points: int
        trophies: int
        titanium_bolts: int
        nanotech_milestones: int
        exclude_locations: set[str]
        deathlink: int
        ship_nose: int
        ship_wings: int
        ship_skin: int
        skin: int
        traps_enabled: int
        trap_weight: dict[str, int]
        rangers: int
        arena: int
        vidcomics: int
        vr_challenges: int
        sewer_crystals: int
        sewer_limitation: int
        nanotech_limitation: int
        weapon_vendors: int
        filler_weight: dict[str, int]
        one_hp_challenge: int
        intro_skip: int
        holostar_skip: int
        clank_options: int

    UnlockItem: dict[str, UnlockData] = None
    options = Options
    boltAndXPMultiplierValue: int = None
    self_respawning: bool = False
    reloading_handled: bool = False
    is_reloading: int = 0
    timers: dict[str, float] = {}
    planet: str = RAC3REGION.GALAXY
    player_type: str = RAC3PLAYERTYPE.RATCHET
    vehicle: int = 0
    action: int = 0  # Todo: Player Action
    action_2: int = 0
    prev_action: int = 0
    pause_menu: bool = False
    pause_state: bool = False
    pause_state_value: int = 0
    inputs: int = RAC3INPUT.NOTHING
    health: int = 100
    max_health: int = 10
    main_menu: bool = False
    ryno: bool = False
    death_count: int = 0
    last_death_count: int = 0
    last_death_state: int = 0
    has_died: bool = False
    died_in_vehicle: bool = False
    inside_hacker_puzzle: bool = False
    notification_queue: list[tuple] = []
    notification_time: float | None = None
    notification_merge_count: int = 1
    message_display: bool = False
    ship_slot_limit: int = 0
    one_hp_challenge: dict[str, int] = None
    pda_vendor: int = 0
    last_in_vehicle_time: float = 0.0
    nanotech_exp: int = 0
    homewarping: bool = False
    checked_locations: set[str] = set()
    clank_disabled: bool = False
    clank_disabled_trap: bool = False
    unfreeze_packs: bool = False
    vidcomic_2_fix: int = 0
    player_actionable: int = 0x8000

    def __init__(self):
        super().__init__()  # GameInterfaceの初期化

    #####################
    # Inherit functions #
    #####################

    def _read8(self, address: int):
        return super()._read8(self.address_convert(address))

    def _read16(self, address: int):
        return super()._read16(self.address_convert(address))

    def _read32(self, address: int):
        return super()._read32(self.address_convert(address))

    def _read_bytes(self, address: int, n: int):
        return super()._read_bytes(self.address_convert(address), n)

    def _read_float(self, address: int):
        return super()._read_float(self.address_convert(address))

    def _write8(self, address: int, value: int):
        return super()._write8(self.address_convert(address), value)

    def _write16(self, address: int, value: int):
        return super()._write16(self.address_convert(address), value)

    def _write32(self, address: int, value: int):
        return super()._write32(self.address_convert(address), value)

    def _write_bytes(self, address: int, value: bytes):
        return super()._write_bytes(self.address_convert(address), value)

    def _write_float(self, address: int, value: float):
        return super()._write_float(self.address_convert(address), value)

    def _write_string(self, address: int, value: str):
        return super()._write_string(self.address_convert(address), value)

    @staticmethod
    def address_convert(address: int):
        """Address conversion from str to int, and for version correction (with US/JP/EU)"""
        _addr = address
        if isinstance(address, str):
            _addr = int(address, 0)
        if 0x001BBB00 <= _addr <= 0x001BBBFF:  # T-Bolt
            _addr += 0
        elif 0x001D545C <= _addr <= 0x001D5553:  # Current Location + VidComic
            _addr += 0
        elif 0x00100000 <= _addr <= 0x00100050:  # DummyEXP
            _addr += 0
        elif 0x001D4C00 <= _addr <= 0x001D4CFF:  # Equipped Items
            _addr += 0
        else:
            pass
        return _addr

    ###############################
    # Called on Server Connection #
    ###############################

    def proc_option(self, slot_data: dict[str, Any]):
        """Process slot option data received when connecting to the server"""
        logger.debug(f'{slot_data}')
        self.one_hp_challenge = slot_data[RAC3OPTION.ONE_HP_CHALLENGE]
        self.options.start_inventory_from_pool = slot_data[RAC3OPTION.START_INVENTORY_FROM_POOL]
        self.options.starting_weapons = slot_data[RAC3OPTION.STARTING_WEAPONS]
        self.options.bolt_and_xp_multiplier = slot_data[RAC3OPTION.BOLT_AND_XP_MULTIPLIER]
        self.options.enable_progressive_weapons = slot_data[RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS]
        self.options.armor_upgrade = slot_data[RAC3OPTION.ARMOR_UPGRADE]
        self.options.skill_points = slot_data[RAC3OPTION.SKILL_POINTS]
        self.options.trophies = slot_data[RAC3OPTION.TROPHIES]
        self.options.titanium_bolts = slot_data[RAC3OPTION.TITANIUM_BOLTS]
        self.options.nanotech_milestones = slot_data[RAC3OPTION.NANOTECH_MILESTONES]
        self.options.exclude_locations = slot_data[RAC3OPTION.EXCLUDE]
        self.options.deathlink = slot_data[RAC3OPTION.DEATHLINK]
        self.options.ship_nose = slot_data[RAC3OPTION.SHIP_NOSE]
        self.options.ship_wings = slot_data[RAC3OPTION.SHIP_WINGS]
        self.options.ship_skin = slot_data[RAC3OPTION.SHIP_SKIN]
        self.options.skin = slot_data[RAC3OPTION.SKIN]
        self.options.traps_enabled = slot_data[RAC3OPTION.ENABLE_TRAPS]
        self.options.trap_weight = slot_data[RAC3OPTION.TRAP_WEIGHT]
        self.options.rangers = slot_data[RAC3OPTION.RANGERS]
        self.options.arena = slot_data[RAC3OPTION.ARENA]
        self.options.vidcomics = slot_data[RAC3OPTION.VIDCOMICS]
        self.options.vr_challenges = slot_data[RAC3OPTION.VR_CHALLENGES]
        self.options.sewer_crystals = slot_data[RAC3OPTION.SEWER_CRYSTALS]
        self.options.sewer_limitation = slot_data[RAC3OPTION.SEWER_LIMITATION]
        self.options.nanotech_limitation = slot_data[RAC3OPTION.NANOTECH_LIMITATION]
        self.options.weapon_vendors = slot_data[RAC3OPTION.WEAPON_VENDORS]
        self.options.filler_weight = slot_data[RAC3OPTION.FILLER_WEIGHT]
        self.options.one_hp_challenge = slot_data[RAC3OPTION.ONE_HP_CHALLENGE]
        self.options.intro_skip = slot_data[RAC3OPTION.INTRO_SKIP]
        self.options.holostar_skip = slot_data[RAC3OPTION.HOLOSTAR_SKIP]
        self.options.clank_options = slot_data[RAC3OPTION.CLANK_OPTIONS]

    ########################################
    # Called on Game and Server Connection #
    ########################################

    def init(self):
        """Initialise values once the game and server are both connected"""
        # Unlock state variables/ArmorUpgrade variable
        self.UnlockItem = {name: self.UnlockData() for name in ITEM_FROM_AP_CODE.values()}
        self.UnlockItem.update({RAC3REGION.SLOT_0: self.UnlockData()})
        logger.debug(f'UnlockItem dict:{self.UnlockItem.keys()}')

        # Proc options
        # Bolt and XPMultiplier
        self.boltAndXPMultiplierValue = int(self.options.bolt_and_xp_multiplier)
        # EnableWeaponLevelAsItem: if enabled, EXP disabler is running.

    def check_main_menu(self):
        """Check if the player is on the main menu, before starting the game"""
        if self._read32(RAC3STATUS.MAIN_MENU) == 0xFFFFFFFF:
            return True
        return False

    ##########################
    # Called on Loading File #
    ##########################

    def reset_file(self):
        """Remove all items and progress on the current file, ready to be set based on current slot progress"""
        self.remove_all_items()
        self.undo_collections()

    def remove_all_items(self):
        """Remove all items from the player's inventory"""
        for item in self.UnlockItem.keys():
            self.UnlockItem[item].status = 0
        for slot in SHIP_SLOTS:
            self._write8(RAC3_REGION_DATA_TABLE[slot].SLOT_ADDRESS, 0)
        self.UnlockItem[RAC3ITEM.VELDIN].status = 1
        # self.UnlockItem[RAC3ITEM.FLORANA].status = 1
        # self.UnlockItem[RAC3ITEM.STARSHIP_PHOENIX].status = 1
        # self.UnlockItem[RAC3ITEM.MUSEUM].status = 1
        self.timers.clear()
        self.checked_locations.clear()
        self.gadget_cycler()
        self.planet_cycler()
        self.weapon_cycler()
        self.vidcomic_cycler()
        self.armor_cycler()
        self.timer_cycler()
        self.weapon_exp_cycler()
        self.verify_quick_select_and_last_used()
        self.clank_cycler()
        self.notification_cycler()

    def undo_collections(self):
        """Unset flags in the game associated to randomizer locations"""
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

    def important_items(self, item: int, us: str, location: int):
        """Runs when loading into game from the main menu to update the player with important items from the server,
        skips filler and trap items to not flood the player with bolts/xp"""
        if (RAC3ITEMTAG.FILLER in RAC3_ITEM_DATA_TABLE[ITEM_FROM_AP_CODE[item]].TAGS or RAC3ITEMTAG.TRAP in
                RAC3_ITEM_DATA_TABLE[ITEM_FROM_AP_CODE[item]].TAGS):
            return
        self.item_received(item, us, None, location)

    def collect_location(self, location: str):
        """Set the in game flags for this location for it to act as if the player has already collected the item here"""
        self.checked_locations.add(location)
        loc_data: RAC3LOCATIONDATA = RAC3_LOCATION_DATA_TABLE[location]
        if RAC3TAG.NANOTECH in loc_data.TAGS or RAC3TAG.SEWER in loc_data.TAGS:
            return
        for check in loc_data.CHECK_ADDRESS:
            if check.TYPE & CHECKTYPE.SIZE == CHECKTYPE.BIT:
                self._write8(check.ADDRESS, self._read8(check.ADDRESS) | (0x01 << check.VALUE))

    def fix_health(self):
        """Set the player health back to the value before we reset"""
        self._write8(RAC3STATUS.HEALTH, self.health)

    def reset_death_count(self):
        """Update the tracked death count to the value in game"""
        self.death_count = self._read32(RAC3STATUS.DEATH_COUNT)
        self.last_death_count = self.death_count

    def add_cosmetics(self):
        """Apply the generated cosmetics to the current game"""
        self._write8(RAC3STATUS.SHIP_CONFIG, self.options.ship_nose + self.options.ship_wings)
        self._write8(RAC3STATUS.SHIP_SKIN, self.options.ship_skin)
        self._write8(RAC3STATUS.PLAYER_SKIN, self.options.skin)
        self._write8(RAC3STATUS.PLAYER_SKIN_2, self.options.skin)

    #############################
    # Start of Main Update Loop #
    #############################

    def early_update(self):
        """Ran early in the update cycle, memory reads should happen here before any evaluations begin"""
        self.planet = PLANET_NAME_FROM_ID[self._read8(RAC3STATUS.PLANET)]
        self.player_type = PLAYER_TYPE_TO_NAME[self._read8(RAC3STATUS.PLAYER_TYPE)]
        self.vehicle = self._read32(RAC3STATUS.VEHICLE_POINTER)
        self.action = self._read8(RAC3STATUS.ACTION)
        self.action_2 = self._read8(RAC3STATUS.ACTION_2)
        self.prev_action = self._read8(RAC3STATUS.PREV_ACTION)
        self.inputs = RAC3INPUT(self._read16(RAC3STATUS.READ_INPUT))
        self.health = self._read8(RAC3STATUS.HEALTH)
        self.max_health = self._read8(RAC3STATUS.MAX_HEALTH)
        self.is_reloading = self._read8(RAC3STATUS.FORCE_RELOAD)
        self.inside_hacker_puzzle = self._read8(RAC3STATUS.HELD_ITEM) == RAC3_ITEM_DATA_TABLE[RAC3ITEM.HACKER].ID
        self.message_display = bool(self._read_float(self._read32(RAC3MESSAGEBOX.VISIBLE_POINTER)))
        self.nanotech_exp = self._read32(RAC3STATUS.NANOTECH_EXP)
        self.clank_disabled = bool(self._read8(RAC3STATUS.NO_CLANK))
        self.player_actionable = self._read16(RAC3STATUS.PLAYER_ACTIONABLE)
        self.pda_vendor = self.find_pda_vendor()
        self.vehicle_check()
        self.pause_check()
        self.check_latches()

    def vehicle_check(self):
        """
        Updates the last_in_vehicle_time when the player is in a vehicle.
        Used to detect if the player died while in a vehicle for deathlink.
        """
        current_time = time.time()
        if self.vehicle or (current_time - self.last_in_vehicle_time < 1 and self.action == 0x39):
            self.last_in_vehicle_time = current_time

    def pause_check(self):
        """Update the current pause data, depending on the current planet"""
        planet_data = RAC3_REGION_DATA_TABLE.get(self.planet, None)
        if planet_data:
            self.pause_menu = bool(self._read8(planet_data.PAUSE_ADDRESS)) if planet_data.PAUSE_ADDRESS else False
            self.pause_state_value = self._read8(RAC3STATUS.PAUSE_STATE
                                                 + planet_data.PLANET_SPECIAL_OFFSET
                                                 ) if planet_data.PLANET_SPECIAL_OFFSET is not None else None
            self.pause_state = bool(self.pause_state_value)
        else:
            # Unknown planet, assume paused to be safe
            self.pause_menu = True
            self.pause_state_value = RAC3PAUSESTATE.PAUSED
            self.pause_state = True

    def check_latches(self):
        """Check specific latched states need to be reset"""
        if self.homewarping:
            if self.pause_state_value != RAC3PAUSESTATE.PLANET_CHANGE:
                self.homewarping = False
        if self.self_respawning:
            if not self.is_reloading:
                self.self_respawning = False

    ##############
    # Intro Skip #
    ##############

    def homewarp(self):
        """Triggers a planet load to the starship phoenix"""
        if self.planet not in RAC3_REGION_DATA_TABLE.keys():
            # Unknown planet, abort homewarp
            logger.error(f'Aborting homewarp, Unknown Planet: {self.planet}')
            return
        planet_data = RAC3_REGION_DATA_TABLE[self.planet]
        if planet_data.PLANET_TO_LOAD:
            self.homewarping = True
            self._write8(planet_data.PLANET_TO_LOAD, RAC3_REGION_DATA_TABLE[RAC3REGION.STARSHIP_PHOENIX].ID)
            self._write8(planet_data.PLANET_SPECIAL_OFFSET + RAC3STATUS.PLANET_LOAD, 1)
            self._write8(planet_data.PLANET_SPECIAL_OFFSET + RAC3STATUS.PAUSE_STATE, 6)
            logger.debug(f"Player home-warped from {self.planet}")
        else:
            logger.warning(f"Couldn't find warp data to leave planet: {self.planet}")

    #################
    # Receive Items #
    #################

    def item_received(self,
                      item_code: int,
                      our_name: Optional[str],
                      other_player: Optional[str],
                      location: Optional[int]):
        """Handle receiving items from the multiworld"""
        name = PROG_TO_NAME_DICT.get(ITEM_FROM_AP_CODE[item_code], ITEM_FROM_AP_CODE[item_code])
        if other_player is not None:
            classification = RAC3_ITEM_DATA_TABLE[name].AP_CLASSIFICATION
            if other_player == our_name:
                if location == 0:
                    pass
                elif location > 0:
                    if classification == ItemClassification.trap:
                        self.notification_queue.append(
                            (f'{RAC3TEXTFORMATSTRING.WHITE}Activated '
                             f'{RAC3TEXTFORMATSTRING.NORMAL}{ITEM_FROM_AP_CODE[item_code]} '
                             f'{RAC3TEXTFORMATSTRING.WHITE}at\\n'
                             f'{RAC3TEXTFORMATSTRING.WHITE}{LOCATION_FROM_AP_CODE[location]}', RAC3BOXTHEME.WARNING))
                    else:
                        self.notification_queue.append(
                            (f'Found '
                             f'{CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]} '
                             f'{RAC3TEXTFORMATSTRING.NORMAL}at\\n{LOCATION_FROM_AP_CODE[location]}',
                             RAC3BOXTHEME.DEFAULT))
                else:
                    if classification == ItemClassification.trap:
                        self.notification_queue.append(
                            (f'{RAC3TEXTFORMATSTRING.WHITE}Activated '
                             f'{RAC3TEXTFORMATSTRING.NORMAL}{ITEM_FROM_AP_CODE[item_code]}', RAC3BOXTHEME.WARNING))
                    else:
                        self.notification_queue.append(
                            (f'Collected {CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]}',
                             RAC3BOXTHEME.DEFAULT))
            else:
                if classification == ItemClassification.trap:
                    self.notification_queue.append((
                        f'{RAC3TEXTFORMATSTRING.GREEN}{other_player}'
                        f'{RAC3TEXTFORMATSTRING.WHITE} activated your '
                        f'{RAC3TEXTFORMATSTRING.NORMAL}{ITEM_FROM_AP_CODE[item_code]}', RAC3BOXTHEME.WARNING))
                else:
                    self.notification_queue.append((
                        f"Received {CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]} "
                        f"{RAC3TEXTFORMATSTRING.NORMAL}from "
                        f"{RAC3TEXTFORMATSTRING.GREEN}{other_player}", RAC3BOXTHEME.DEFAULT))
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
            case RAC3ITEM.PROGRESSIVE_PACK:
                self.UnlockItem[RAC3ITEM.CLANK].status = 1
                self.UnlockItem[RAC3ITEM.HELI_PACK].status = 1
                if self.UnlockItem[name].status > 1:
                    self.UnlockItem[RAC3ITEM.THRUSTER_PACK].status = 1
                    self.UnlockItem[name].status = 2
            case RAC3ITEM.HELI_PACK:
                self.UnlockItem[RAC3ITEM.CLANK].status = 1
            case RAC3ITEM.THRUSTER_PACK:
                self.UnlockItem[RAC3ITEM.CLANK].status = 1
            case RAC3ITEM.CLANK:
                self.UnlockItem[RAC3ITEM.HELI_PACK].status = 1
                self.UnlockItem[RAC3ITEM.THRUSTER_PACK].status = 1
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
                self.nanotech_exp += 10000 + randint(1, 300 * self.max_health)
                if self.nanotech_exp > 0x7FFFFFFF:
                    self.nanotech_exp = 0x7FFFFFFF
                self._write32(RAC3STATUS.NANOTECH_EXP, self.nanotech_exp)
            case RAC3ITEM.WEAPON_XP:
                valid_weapons = []
                for weapon_name, weapon_data in non_prog_weapon_data.items():
                    if self.UnlockItem[weapon_name].status:
                        level = RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID[self._read8(weapon_data.LEVEL_ADDRESS)]].LEVEL
                        if ((weapon_name != RAC3ITEM.RY3N0 and level < 5) or
                                (weapon_name == RAC3ITEM.RY3N0 and level < 4) or
                                (weapon_name == RAC3ITEM.RY3N0 and level < 5 and not self.ryno)):
                            valid_weapons.append(weapon_name)

                if valid_weapons:
                    self.weapon_level_up(choice(valid_weapons))
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
                    self.timers[name] += randint(10, 15)
                else:
                    self.timers[name] = int(time.time() + uniform(10, 15))
            case RAC3ITEM.MIRROR_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(10, 20)
                else:
                    self.timers[name] = int(time.time() + uniform(10, 20))
            case RAC3ITEM.BLACK_SCREEN_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(6, 10)
                else:
                    self.timers[name] = int(time.time() + uniform(6, 10))
            case RAC3ITEM.NO_CLANK_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(10, 20)
                else:
                    # Special case for holostar, nefarious base and klunk fight
                    if not self.clank_disabled:
                        self.timers[name] = int(time.time() + uniform(10, 20))
            case RAC3ITEM.INVISIBLE_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(6, 15)
                else:
                    self.timers[name] = int(time.time() + uniform(6, 15))
            case RAC3ITEM.DISARM_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(6, 15)
                else:
                    self.timers[name] = int(time.time() + uniform(6, 15))
            case RAC3ITEM.WRENCH_ONLY_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(6, 15)
                else:
                    self.timers[name] = int(time.time() + uniform(6, 15))
        if name in non_prog_weapon_data.keys():
            if non_prog_weapon_data[name].AMMO:
                self._write8(non_prog_weapon_data[name].AMMO_ADDRESS, non_prog_weapon_data[name].AMMO)
        if name in equipable_data.keys() and self.UnlockItem[name].status == 1:
            self.update_equip(name)

    def weapon_level_up(self, weapon_name: str):
        """Level up a weapon from xp reward"""
        weapon_data = non_prog_weapon_data[weapon_name]
        current_id = self._read8(weapon_data.LEVEL_ADDRESS)
        current_name = ITEM_NAME_FROM_ID[current_id]
        current_level = RAC3_ITEM_DATA_TABLE[current_name].LEVEL
        if current_level < 5:
            target_level = current_level + 1
            target_id = UPGRADE_DICT[weapon_name][target_level - 1]
            target_name = ITEM_NAME_FROM_ID[target_id]
            target_xp = RAC3_ITEM_DATA_TABLE[target_name].XP_THRESHOLD
            target_ammo = RAC3_ITEM_DATA_TABLE[target_name].AMMO
            logger.debug(f'level up {weapon_name} to {target_name}, target level: {current_level}, '
                         f'target id: {target_id}, target xp:{target_xp}')
            self._write32(weapon_data.XP_ADDRESS, target_xp)
            self._write8(weapon_data.LEVEL_ADDRESS, target_id)
            if target_ammo:
                self._write32(weapon_data.AMMO_ADDRESS, target_ammo)

    def update_equip(self, name: str):
        """Equip the most recently collected weapon/gadget, update recent uses"""
        if equipable_data[name].ID:
            self._write8(RAC3STATUS.LAST_USED_2, self._read8(RAC3STATUS.LAST_USED_1))
            self._write8(RAC3STATUS.LAST_USED_1, self._read8(RAC3STATUS.LAST_USED_0))
            self._write8(RAC3STATUS.LAST_USED_0, equipable_data[name].ID)
            self._write8(RAC3STATUS.EQUIPPED, equipable_data[name].ID)
            for slot in QUICK_SELECT_LIST:
                if not self._read8(RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS):
                    self._write8(RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS, equipable_data[name].ID)
                    break

    ###################
    # Check Locations #
    ###################

    def is_location_checked(self, ap_code: int) -> bool:
        """Reads location data to find what memory check should be done, returns the collection state of the location"""
        location = LOCATION_FROM_AP_CODE[ap_code]
        if location in self.checked_locations:
            return True
        loc_data: RAC3LOCATIONDATA = RAC3_LOCATION_DATA_TABLE[location]
        if not loc_data:
            return False
        if location == RAC3LOCATION.OBANI_GEMINI_SKIDD and self.planet == RAC3REGION.OBANI_GEMINI:
            _x = abs(self._read_float(RAC3STATUS.POS_X) - 201.2) < 10
            _y = abs(self._read_float(RAC3STATUS.POS_Y) - 364) < 10
            _z = abs(self._read_float(RAC3STATUS.POS_Z) - 296.8) < 10
            return _x & _y & _z
        check_all: bool = True
        for check in loc_data.CHECK_ADDRESS:
            match check.TYPE & CHECKTYPE.SIZE:
                case CHECKTYPE.BIT:
                    check_all &= (self._read8(check.ADDRESS) >> check.VALUE) & 0x01
                case CHECKTYPE.BYTE:
                    check_all &= self.compare(self._read8(check.ADDRESS), check)
                case CHECKTYPE.SHORT:
                    check_all &= self.compare(self._read16(check.ADDRESS), check)
                case CHECKTYPE.INT:
                    check_all &= self.compare(self._read32(check.ADDRESS), check)
        if check_all:
            self.checked_locations.add(location)
        return check_all

    @staticmethod
    def compare(value: int, check: RAC3ADDRESSDATA) -> bool:
        """Compares a value using the checktype provided in data"""
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

    #############
    # Deathlink #
    #############

    def reload_check(self):
        """Detects if the game is being reloaded, and updates death data"""
        if self.is_reloading and not self.reloading_handled and not self.self_respawning:
            self.last_death_state = self.action
            self.died_in_vehicle = time.time() - self.last_in_vehicle_time < 1.5
            self.reloading_handled = True
            logger.debug(f'{self.player_type} is Respawning, death state: {self.last_death_state},'
                         f' death count: {self.last_death_count}, in vehicle? {self.died_in_vehicle}')
        if not self.is_reloading and self.reloading_handled:
            self.death_count = self._read32(RAC3STATUS.DEATH_COUNT)
            self.has_died = self.death_count > self.last_death_count
            self.last_death_count = self.death_count
            self.reloading_handled = False
            logger.debug(f'{self.player_type} has Respawned, death count: {self.death_count}, has died?'
                         f' {self.has_died}')
        else:
            self.has_died = False

    def alive(self) -> tuple[bool, str]:
        """Checks the current game state to determine if the player is still alive, and if not then how they died"""
        if self.has_died:
            self.last_death_count = self.death_count
            logger.debug(f'Death Detected! (death count increased)')
            is_clank = self.player_type == RAC3PLAYERTYPE.CLANK
            death = DEATH_FROM_ACTION.get(self.last_death_state, 'ran out of nanotech.') if not is_clank else (
                CLANK_DEATH_FROM_ACTION.get(self.last_death_state, 'ran out of nanotech.'))

            # Vehicle pointer becomes 0 during reload, but the address next to it gets a value during reload after
            # vehicle death
            if self.died_in_vehicle:
                # Vehicle death uses state 34 which is the same as getting eaten by a shark
                death = "Didn't leave the vehicle in time."
            return False, f"{self.player_type} {death}"

        logger.debug(f'{self.player_type} is Alive')
        return True, f"{self.player_type} is Alive"

    def kill_player(self) -> bool:
        """Checks the current game state to determine if and how to kill the player, returns success/failure"""
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

    ##############
    # Check Goal #
    ##############

    @staticmethod
    def get_victory_code():
        """Returns the apcode value of the goal location"""
        return RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.COMMAND_CENTER_BIOBLITERATOR].AP_CODE
        # let this be changed by an option

    ###################
    # Changing Planet #
    ###################

    def map_switch(self) -> tuple[str, str]:
        """Update and validate the current planet for the UT map"""
        _raw_planet = RAC3_REGION_DATA_TABLE[self.planet].ID
        _safe_planet = _raw_planet
        if _raw_planet > 55 or not self._read8(RAC3STATUS.MAP_CHECK):
            _safe_planet = 0
        elif _raw_planet > 29:
            _safe_planet = 3
        return PLANET_NAME_FROM_ID[_raw_planet], PLANET_NAME_FROM_ID[_safe_planet]

    def tyhrranosis_fix(self):
        """Prevent a Crash on Tyhrranosis by disabling the robot tyhrranoids"""
        self._write8(RAC3STATUS.ROBONOIDS, 0)

    def softlock_warning(self):
        """Checks if the player is on a planet with a potential softlock and informs them on how to escape"""
        match self.planet:
            case RAC3REGION.HOLOSTAR_STUDIOS | RAC3REGION.HOLOSTAR_STUDIOS_CLANK:
                if not (self.UnlockItem[RAC3ITEM.HACKER].status and self.UnlockItem[RAC3ITEM.HYPERSHOT].status):
                    logger.info("You do not have the items required to leave this planet through your ship. If you are"
                                " stuck, hold L2 + R2 + L1 + R1 + SELECT to warp back to the phoenix")
            case RAC3REGION.PHOENIX_ASSAULT:
                logger.info("If you want to travel to the regular phoenix, hold L2 + R2 + L1 + R1 + SELECT")

    ##################
    # Player Respawn #
    ##################

    def check_inputs(self, check: RAC3INPUT, pause_required: bool = False) -> bool:
        """Checks if the game is receiving a button combination, with optional pause check"""
        pause_check = self.pause_menu and not self.inputs & RAC3INPUT.START
        return (pause_check or not pause_required) and (self.inputs & check) == check

    def unpause_game(self):
        """Unpause the game if it is on the pause menu"""
        if self.pause_menu:
            self.write_input(RAC3INPUT.START)

    def write_input(self, button: RAC3INPUT):
        """Send the game button inputs"""
        left_shifted = (button & 0x00FF) << 8
        right_shifted = button >> 8
        bitmasked = RAC3INPUT.MASK ^ (left_shifted | right_shifted)
        self._write16(RAC3STATUS.WRITE_INPUT_1, bitmasked)
        self._write16(RAC3STATUS.WRITE_INPUT_2, bitmasked)

    def teleport_to_ship(self):
        """Handle respawning the player, to their ship if available, otherwise to the most recent checkpoint"""
        if self.should_overwrite_respawn() and self.planet in RESPAWN_COORDS_OFFSET.keys():
            self._write_bytes(
                RESPAWN_COORDS_OFFSET[self.planet] + RAC3STATUS.RESPAWN_BASE,
                self._read_bytes(RAC3STATUS.ENTRANCE_X, 28))
            logger.debug(f'Player respawned on: {self.planet}')
        else:
            logger.debug(f'Player respawned at last checkpoint on: {self.planet}')
        self.force_respawn()

    def should_overwrite_respawn(self):
        """Determine if the current respawn coordinates should be overwritten to the ship coordinates"""
        if self.player_type in {RAC3PLAYERTYPE.CLANK, RAC3PLAYERTYPE.GIANT, RAC3PLAYERTYPE.QWARK}:
            return False
        match self.planet:
            case RAC3REGION.VELDIN | RAC3REGION.TYHRRANOSIS | RAC3REGION.ZELDRIN_STARPORT:
                # Veldin: Problems with F-sector
                # Tyhrranosis: Entrance coordinates in the first section that gets unloaded after leaving
                # Zeldrin: only one respawn point, that is right next to the ship, and we don't want anything to happen
                #          while aboard the leviathan
                return False
            case RAC3REGION.MARCADIA:
                return self._read32(RAC3STATUS.MARCADIA_SECTION) < 3  # 1: Main, 2: Rangers, 3: LDF
            case _:
                return True

    def force_respawn(self):
        """Force the game to reload the current planet, respawning the player"""
        self.self_respawning = True
        self._write8(RAC3STATUS.FORCE_RELOAD, 1)

    def check_intro(self) -> bool:
        """Checks if the player has reached the end of the intro by collecting the phoenix coordinates"""
        if not self._read8(RAC3STATUS.VISITED_BASE + RAC3_REGION_DATA_TABLE[RAC3REGION.STARSHIP_PHOENIX].ID):
            return True
        return False

    ##################
    # Sequence Break #
    ##################

    def sequence_break(self) -> None:
        """Checks the current planet and unsets any planet access flags that would interfere with location collecting"""
        infobot_location = REGION_TO_INFOBOT_LOCATION.get(self.planet, None)
        if infobot_location is not None and infobot_location in RAC3_LOCATION_DATA_TABLE:
            infobot_flag = LOCATION_TO_INFOBOT_FLAG.get(infobot_location, None)
            if (infobot_flag is not None
                    and not infobot_location in self.checked_locations
                    and infobot_flag != RAC3STATUS.ALLOW_SHIP):
                self._write8(infobot_flag, 0)

        if self.planet == RAC3REGION.STARSHIP_PHOENIX:
            # Fix can't play Qwark VidComics in some case which first event is skipped
            self._write8(0x001426E8, 1)  # Todo: Take Qwark to Cage Mission
            # Bring qwark back to life until Ratchet has met Sasha on the bridge
            if RAC3LOCATION.PHOENIX_MEET_SASHA not in self.checked_locations:
                self._write8(RAC3STATUS.ESCAPED_LEVIATHAN, 0)
        if self.planet == RAC3REGION.ANNIHILATION_NATION and self.vidcomic_2_fix < 30:
            if self.is_location_checked(RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.NATION_HEAT_STREET].AP_CODE):
                self.vidcomic_2_fix += 1
                self._write8(RAC3STATUS.HEAT_STREET_FIX, 1)
        if self.planet != RAC3REGION.ZELDRIN_STARPORT and not self._read8(RAC3STATUS.ZELDRIN_END_LEVIATHAN):
            self._write8(RAC3STATUS.ZELDRIN_START_LEVIATHAN, 0)

        if self.options.holostar_skip:
            self._write8(RAC3STATUS.VISITED_BASE + RAC3_REGION_DATA_TABLE[RAC3REGION.HOLOSTAR_STUDIOS_CLANK].ID, 1)

    ##################
    # End of Main Loop #
    ##################

    def late_update(self):
        """Ran at the end of the main loop to update any memory values based on collection state"""
        self.cutscene_gadget_fix()
        self.gadget_cycler()
        self.planet_cycler()
        self.weapon_cycler()
        self.vidcomic_cycler()
        self.armor_cycler()
        self.timer_cycler()
        if self.options.enable_progressive_weapons:
            self.weapon_exp_cycler()
        self.verify_quick_select_and_last_used()
        self.clank_cycler()
        self.multiplier_cycler()
        self.overflow_fix()
        self.health_cycler()
        self.pda_vendor_cycler()
        self.notification_cycler()

    def cutscene_gadget_fix(self):
        """Temporarily removing a gadget when grabbing it during a cutscene to make sure the location check address
        gets checked"""
        if bool(self._read8(RAC3STATUS.HIDE_WEAPON)):
            match self.planet:
                case RAC3REGION.MARCADIA:
                    self._write8(gadget_data[RAC3ITEM.REFRACTOR].UNLOCK_ADDRESS, 0)
                case RAC3REGION.DAXX:
                    self._write8(gadget_data[RAC3ITEM.CHARGE_BOOTS].UNLOCK_ADDRESS, 0)
                case RAC3REGION.ZELDRIN_STARPORT:
                    self._write8(gadget_data[RAC3ITEM.BOLT_GRABBER].UNLOCK_ADDRESS, 0)
                    self._write8(gadget_data[RAC3ITEM.BOX_BREAKER].UNLOCK_ADDRESS, 0)
                case RAC3REGION.CRASH_SITE:
                    self._write8(gadget_data[RAC3ITEM.NANO_PAK].UNLOCK_ADDRESS, 0)
                case RAC3REGION.QWARKS_HIDEOUT:
                    self._write8(gadget_data[RAC3ITEM.PDA].UNLOCK_ADDRESS, 0)

    def gadget_cycler(self):
        """Cycles through each gadget and updates their state"""
        if not self.should_cycle_gadgets() or self.near_pda_vendor():
            self.respawn_gadgets()
            return

        for name in gadget_data.keys():
            addr = gadget_data[name].UNLOCK_ADDRESS
            if self.UnlockItem[name].status:
                if (name == RAC3ITEM.TYHRRA_GUISE and self.planet == RAC3REGION.STARSHIP_PHOENIX and not
                RAC3LOCATION.PHOENIX_MEET_SASHA in self.checked_locations):
                    self._write8(addr, 0)
                    continue
                if self.UnlockItem[name].unlock_delay:
                    self._write8(addr, 1)
                    self.UnlockItem[name].unlock_delay = 0
                else:
                    self.UnlockItem[name].unlock_delay += 1
            else:
                self._write8(addr, 0)

    def should_cycle_gadgets(self) -> bool:
        """Check if it's safe to cycle gadgets
        used to ensure gadgets can respawn without the cycler interfering"""
        if ((self.player_actionable == 0x8000 and self.pause_state_value in [RAC3PAUSESTATE.PLANET_CHANGE,
                                                                             RAC3PAUSESTATE.UNPAUSED])
                or self.is_reloading
                or self.self_respawning
                or self.action_2 == 0x09):
            return False
        return True

    def near_pda_vendor(self) -> bool:
        """Check if we are near the PDA Vendor"""
        if self.planet == RAC3REGION.QWARKS_HIDEOUT and self.distance_to_moby(self.pda_vendor) < 12.0:
            return True
        return False

    def distance_to_moby(self, moby) -> float:
        """Calculate the distance from the player to the moby"""
        if not moby:
            return float('inf')
        assert RAC3STATUS.HIDEOUT_MOBY_TABLE_START < moby < RAC3STATUS.HIDEOUT_MOBY_TABLE_START + 0x00100000, \
            "Moby not in the typical moby range"
        player_pos = (self._read_float(RAC3STATUS.POS_X),
                      self._read_float(RAC3STATUS.POS_Y),
                      self._read_float(RAC3STATUS.POS_Z))
        moby_pos = (self._read_float(moby + 0x10),
                    self._read_float(moby + 0x14),
                    self._read_float(moby + 0x18))
        distance = ((player_pos[0] - moby_pos[0]) ** 2 +
                    (player_pos[1] - moby_pos[1]) ** 2 +
                    (player_pos[2] - moby_pos[2]) ** 2) ** 0.5
        return distance

    def respawn_gadgets(self):
        """Respawn gadget if the associated location isn't checked but the gadget is unlocked through AP"""
        if (self.UnlockItem[RAC3ITEM.REFRACTOR].status and
                not self.is_location_checked(RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.MARCADIA_REFRACTOR].AP_CODE)):
            self._write8(gadget_data[RAC3ITEM.REFRACTOR].UNLOCK_ADDRESS, 0)

        if (self.UnlockItem[RAC3ITEM.CHARGE_BOOTS].status and
                not self.is_location_checked(RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.DAXX_CHARGE_BOOTS].AP_CODE)):
            self._write8(gadget_data[RAC3ITEM.CHARGE_BOOTS].UNLOCK_ADDRESS, 0)

        if (self.UnlockItem[RAC3ITEM.NANO_PAK].status and
                not self.is_location_checked(RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.CRASH_SITE_NANO_PAK].AP_CODE)):
            self._write8(gadget_data[RAC3ITEM.NANO_PAK].UNLOCK_ADDRESS, 0)

        if ((self.UnlockItem[RAC3ITEM.BOLT_GRABBER].status or self.UnlockItem[RAC3ITEM.BOX_BREAKER].status) and
                not self.is_location_checked(
                    RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.ZELDRIN_STARPORT_BOLT_GRABBER].AP_CODE)):
            self._write8(gadget_data[RAC3ITEM.BOLT_GRABBER].UNLOCK_ADDRESS, 0)
            self._write8(gadget_data[RAC3ITEM.BOX_BREAKER].UNLOCK_ADDRESS, 0)
        if (self.UnlockItem[RAC3ITEM.PDA].status and
                not self.is_location_checked(RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.HIDEOUT_PDA].AP_CODE)):
            self._write8(gadget_data[RAC3ITEM.PDA].UNLOCK_ADDRESS, 0)

    def planet_cycler(self):
        """Handles unlocking planets if their "infobot" has been collected"""
        for name in infobot_data.keys():
            planet = RAC3_REGION_DATA_TABLE[PLANET_FROM_INFOBOT[name]]
            if self.UnlockItem[name].status:
                addr = RAC3_REGION_DATA_TABLE[SHIP_SLOTS[self.UnlockItem[name].status - 1]].SLOT_ADDRESS
                if self.UnlockItem[name].unlock_delay:
                    self._write8(addr, planet.ID)
                else:
                    self.UnlockItem[name].unlock_delay += 1
        for number, slot in enumerate(SHIP_SLOTS):
            self.ship_slot_limit = self.UnlockItem[RAC3REGION.SLOT_0].status
            if number >= self.ship_slot_limit:
                self._write8(RAC3_REGION_DATA_TABLE[slot].SLOT_ADDRESS, 0)

    def weapon_cycler(self):
        """Interval update function: Check unlock/lock status of weapons"""
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
                self.update_weapon_equip(equipable_data[RAC3ITEM.WRENCH].ID, 0, None, None)
                return
            last_2 = self._read8(RAC3STATUS.LAST_USED_2)
            last_3 = self._read8(RAC3STATUS.LAST_USED_3)
            if self.UnlockItem.get(ITEM_NAME_FROM_ID.get(last_1)).status:
                self.update_weapon_equip(last_1, last_1, last_2, last_3)
                return
            if last_2 == 0:
                self.update_weapon_equip(equipable_data[RAC3ITEM.WRENCH].ID, 0, 0, None)
                return
            last_4 = self._read8(RAC3STATUS.LAST_USED_4)
            if self.UnlockItem.get(ITEM_NAME_FROM_ID.get(last_2)).status:
                self.update_weapon_equip(last_2, last_2, last_3, last_4)
                return
            last_5 = self._read8(RAC3STATUS.LAST_USED_5)
            if last_3 == 0 or self.UnlockItem.get(ITEM_NAME_FROM_ID.get(last_3)).status:
                self.update_weapon_equip(equipable_data[RAC3ITEM.WRENCH].ID, last_3, last_4, last_5)
            else:
                self.update_weapon_equip(last_3, last_3, last_4, last_5)

    def update_weapon_equip(self, equip: Optional[int], last_0: Optional[int],
                            last_1: Optional[int], last_2: Optional[int]):
        """Writes new values to the player's last used item history"""
        if equip is not None:
            self._write8(RAC3STATUS.EQUIPPED, equip)
        if last_0 is not None:
            self._write8(RAC3STATUS.LAST_USED_0, last_0)
        if last_1 is not None:
            self._write8(RAC3STATUS.LAST_USED_1, last_1)
        if last_2 is not None:
            self._write8(RAC3STATUS.LAST_USED_2, last_2)

    def vidcomic_cycler(self):
        """Cycle through all vidcomics and update their state"""
        prog_comic = self.UnlockItem[RAC3ITEM.PROGRESSIVE_VIDCOMIC]
        for index, name in enumerate(vidcomic_data.keys()):
            comic = self.UnlockItem[name]
            addr = vidcomic_data[name].UNLOCK_ADDRESS
            if index == 0:
                continue

            unlock_delay_count = 30 if index == 2 else 1  # extra delay for Annihilation Nation Proceeding
            if comic.unlock_delay < unlock_delay_count:
                comic.unlock_delay += 1
                continue
            comic.unlock_delay = 0

            value = 0 if index > prog_comic.status else 1
            self._write8(addr, value)

    def armor_cycler(self):
        """Cycle through all armors and update their state"""
        addr = armor_data[RAC3ITEM.PROGRESSIVE_ARMOR]
        armor = self.UnlockItem[RAC3ITEM.PROGRESSIVE_ARMOR]
        current_armor_value = self._read8(addr.UNLOCK_ADDRESS)

        if current_armor_value != armor.status:
            armor.unlock_delay += 1
            if armor.unlock_delay > 1:
                self._write8(addr.UNLOCK_ADDRESS, armor.status)
                self._write8(RAC3STATUS.HELMET, armor.status)
                armor.unlock_delay = 0

    def timer_cycler(self):
        """Cycle through the timer dictionary, check their duration, and handle their effects"""
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
                        case RAC3STATUS.INVISIBLE:
                            self._write8(status, 2)
                        case RAC3STATUS.WRENCH_ONLY:
                            self._write8(status, 2)
                        case RAC3STATUS.DISARM:
                            if self.vehicle == 0:
                                self._write8(status, 1)
                        case RAC3STATUS.NO_CLANK:
                            self.clank_disabled_trap = True
                        case _:
                            self._write8(status, 1)
            else:
                self.timers.pop(name)
                if 'Jackpot' in name:
                    self.notification_queue.append(
                        (f'{RAC3TEXTFORMATSTRING.WHITE}Jackpot x{2 ** self.boltAndXPMultiplierValue} '
                         f'{RAC3TEXTFORMATSTRING.NORMAL}effect has worn off.', RAC3BOXTHEME.DEFAULT))
                else:
                    self.notification_queue.append(
                        (f'{name}{RAC3TEXTFORMATSTRING.WHITE} effect has worn off.', RAC3BOXTHEME.WARNING))
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
                        self.clank_disabled_trap = False
                    case RAC3ITEM.INVISIBLE_TRAP:
                        self._write8(RAC3STATUS.INVISIBLE, 0)
                    case RAC3ITEM.DISARM_TRAP:
                        self._write8(RAC3STATUS.DISARM, 0)
                    case RAC3ITEM.WRENCH_ONLY_TRAP:
                        self._write8(RAC3STATUS.WRENCH_ONLY, 0)

        # Remove trap effects for traps not in the timer dictionary to prevent any stuck effects
        # Prevent not having lock trap from unlocking weapon during arena weapon specific challenges every cycle
        # for trap_name, status_address in trap_to_status.items():
        #     if trap_name not in self.trap_timers and trap_name != RAC3ITEM.LOCK_TRAP:
        #         self._write8(status_address, 0)

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

    def verify_quick_select_and_last_used(self):
        """Check each slot in quick select and held item history, reset if that item has not been collected yet."""
        _slots = [RAC3STATUS.LAST_USED_0, RAC3STATUS.LAST_USED_1, RAC3STATUS.LAST_USED_2, RAC3STATUS.EQUIPPED]
        for slot in QUICK_SELECT_LIST:
            _slots.append(RAC3_STATUS_DATA_TABLE[slot].SLOT_ADDRESS)
        for addr in _slots:
            idx = self._read8(addr)
            if idx > 1:
                name = ITEM_NAME_FROM_ID[idx]
                if not self.UnlockItem[name].status:
                    # Not unlocked, but set
                    self._write8(addr, 0)

    def clank_cycler(self):
        """Checks the current state to see if clank needs to be disabled"""
        # Special cases where Clank is already removed
        if ((self.planet == RAC3REGION.HOLOSTAR_STUDIOS and not self._read8(RAC3STATUS.HOLOSTAR_CLANK_FIX))
                or self.planet == RAC3REGION.AQUATOS_BASE
                or not self.UnlockItem[RAC3ITEM.CLANK].status
                or self.clank_disabled_trap):
            self._write8(RAC3STATUS.NO_CLANK, 1)
        # No special case:
        else:
            if self.UnlockItem[RAC3ITEM.CLANK].unlock_delay:
                self._write8(RAC3STATUS.NO_CLANK, 0)
                self.UnlockItem[RAC3ITEM.CLANK].unlock_delay = 0
            else:
                self.UnlockItem[RAC3ITEM.CLANK].unlock_delay += 1
        if self.UnlockItem[RAC3ITEM.HELI_PACK].status:
            if self.UnlockItem[RAC3ITEM.THRUSTER_PACK].status:
                if not self.unfreeze_packs:
                    self._write8(RAC3STATUS.PACK_EQUIP, 2)  # Unset pack freeze
                self.unfreeze_packs = True
            else:
                if self.pause_state_value == RAC3PAUSESTATE.PAUSED:
                    self._write8(RAC3STATUS.PACK_EQUIP, 3)  # Set pack freeze
                else:
                    self._write8(RAC3STATUS.PACK_EQUIP, 2)  # Unset pack freeze
        elif self.UnlockItem[RAC3ITEM.THRUSTER_PACK].status:
            self.unfreeze_packs = True

    def multiplier_cycler(self):
        """Update the Bolt+EXP multiplier based on settings"""
        self._write32(RAC3STATUS.JACKPOT_TIMER, 0x7FFFFFFF)
        self._write8(RAC3STATUS.JACKPOT, self.boltAndXPMultiplierValue)

    def overflow_fix(self):
        """Detect any integer overflows and reset the value"""
        if self.nanotech_exp > 0x7FFFFFFF:
            self._write32(RAC3STATUS.NANOTECH_EXP, 0)
            self.notification_queue.append(
                (f'Negative Nanotech EXP detected! Resetting EXP to 0', RAC3BOXTHEME.WARNING))
        # If other stuff needs overflow fixing, add here

    def health_cycler(self):
        """
        Enforces one HP challenge for player and vehicle if enabled in settings
        Sets health to 1 if above 1 for the current character
        """
        character = self.player_type
        if character == RAC3PLAYERTYPE.TYHRRANOID:
            character = RAC3PLAYERTYPE.RATCHET  # Treat Tyhrranoid as Ratchet for one HP challenge
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
                if (character == RAC3PLAYERTYPE.RATCHET
                        and self.planet == RAC3REGION.ANNIHILATION_NATION):
                    # Patch out sleeping gas health reduction to prevent death
                    if self._read32(RAC3INSTRUCTION.NATION_SLEEP_GAS_HEALTH_UPDATE) == 0x2442FFFF:
                        self._write32(RAC3INSTRUCTION.NATION_SLEEP_GAS_HEALTH_UPDATE, 0x24420000)  # addiu v0,v0,0x0
                    # Patch out health refill to prevent auto losing One Hit Wonder challenge
                    if self._read32(RAC3INSTRUCTION.NATION_HEALTH_REFILL) == 0xAC652850:
                        self._write32(RAC3INSTRUCTION.NATION_HEALTH_REFILL, 0x00000000)  # nop
                    # Patch out nanotech level up healing to prevent losing One Hit Wonder challenge
                    if self._read32(RAC3INSTRUCTION.NATION_LEVELUP_HEALING) == 0x00621821:
                        self._write32(RAC3INSTRUCTION.NATION_LEVELUP_HEALING, 0x00000000)  # nop
                    if self._read32(RAC3INSTRUCTION.NATION_LEVELUP_MILESTONE_HEALING) == 0xACA22850:
                        self._write32(RAC3INSTRUCTION.NATION_LEVELUP_MILESTONE_HEALING, 0x00000000)  # nop

        # Vehicle one HP challenge is independent of player_type
        if self.vehicle and self.one_hp_challenge.get(RAC3PLAYERTYPE.VEHICLE, False):
            health_addr = self._read32(self._read32(self.vehicle + 0x68))
            target_health = 5.0
            if self.planet in [RAC3REGION.TYHRRANOSIS_RANGERS, RAC3REGION.MARCADIA]:
                target_health = 1.0  # For some reason these vehicles have 100 max health instead of 500
            elif self.planet == RAC3REGION.TYHRRANOSIS:
                target_health = 0.6  # For some reason the turboslider on Tyhrranosis has 60 max health
            if self._read_float(health_addr) > target_health:
                # This displays as 1 HP in-game for vehicles with 500 max health
                self._write_float(health_addr, target_health)

        if (not self.one_hp_challenge.get(character, False)
                and self.planet == RAC3REGION.ANNIHILATION_NATION):
            # Restore patched instructions to their original state when not doing one HP challenge
            if self._read32(RAC3INSTRUCTION.NATION_SLEEP_GAS_HEALTH_UPDATE) == 0x24420000:
                self._write32(RAC3INSTRUCTION.NATION_SLEEP_GAS_HEALTH_UPDATE, 0x2442FFFF)  # addiu v0,v0,-0x1
            if self._read32(RAC3INSTRUCTION.NATION_HEALTH_REFILL) == 0x00000000:
                self._write32(RAC3INSTRUCTION.NATION_HEALTH_REFILL, 0xAC652850)  # sw a1,0x2850(v1)
            if self._read32(RAC3INSTRUCTION.NATION_LEVELUP_HEALING) == 0x00000000:
                self._write32(RAC3INSTRUCTION.NATION_LEVELUP_HEALING, 0x00621821)  # addu v1,v1,v0
            if self._read32(RAC3INSTRUCTION.NATION_LEVELUP_MILESTONE_HEALING) == 0x00000000:
                self._write32(RAC3INSTRUCTION.NATION_LEVELUP_MILESTONE_HEALING, 0xACA22850)  # sw a2,0x2850(v1)

        # If loading from the main menu we delay fixing the current health until the load is complete
        if self.main_menu:
            if self.max_health > 10:
                self._write8(RAC3STATUS.HEALTH, self.max_health)
                self.main_menu = False

    def find_pda_vendor(self) -> int | str:
        """Traverse the moby linked list on Qwarks Hideout to find the PDA vendor moby and return its address"""
        if self.planet != RAC3REGION.QWARKS_HIDEOUT:
            # reset PDA vendor when leaving Qwarks Hideout
            return 0
        target_moby_id = RAC3STATUS.PDA_VENDOR_MOBY_ID
        if self.pda_vendor and self._read16(self.pda_vendor + 0xB2) == target_moby_id:
            return self.pda_vendor
        table_start = RAC3STATUS.HIDEOUT_MOBY_TABLE_START
        moby_offset = 0
        current_id = 0
        for traversal in range(1, 10001):
            if current_id == target_moby_id:
                # once vendor has been found, save address
                pda_vendor_addr = table_start + moby_offset
                logger.debug(f'PDA Vendor found at address: {hex(pda_vendor_addr)} after {traversal} traversals')
                return pda_vendor_addr
            next_ptr = self._read32(table_start + 0x28 + moby_offset)
            if next_ptr == 0:  # Null pointer found
                logger.debug(f'PDA Vendor not found after {traversal} traversals, reached null pointer')
                return 0
            moby_offset = next_ptr - table_start
            if moby_offset < 0:
                logger.debug(f'PDA Vendor not found after {traversal} traversals, invalid offset detected')
                return 0
            current_id = self._read16(table_start + 0xB2 + moby_offset)
        return 0

    def pda_vendor_cycler(self):
        """Handles PDA vendor logic: finding, resetting, and repurchasing on Qwark's Hideout."""

        # If PDA vendor not found, don't continue
        if self.pda_vendor == 0:
            return

        # Wait until Qwarks Hideout is fully loaded and PDA is unlocked
        if not self.should_cycle_gadgets() or self.UnlockItem[RAC3ITEM.PDA].status == 0:
            return

        # If Ratchet has the PDA but has not checked the PDA location, reset the vendor if close
        if (self.UnlockItem[RAC3ITEM.PDA].status == 1 and
                not self.is_location_checked(RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.HIDEOUT_PDA].AP_CODE)):
            distance = self.distance_to_moby(self.pda_vendor)
            logger.debug(f'Ratchet has PDA and PDA location unchecked, distance to PDA Vendor: {distance:.2f}')
            if distance < 12.0:
                logger.debug(f'Ratchet is close to PDA Vendor (Distance: {distance:.2f}), resetting vendor')
                self.reset_pda_vendor()

    def reset_pda_vendor(self):
        """Reset PDA Vendor to initial state to allow repurchasing the PDA"""
        if self.pda_vendor == 0:
            logger.error('PDA Vendor not found, cannot reset')
            return
        self._write8(self.pda_vendor + 0x7C, 1)  # Put PDA back in vendor
        self._write8(self.pda_vendor + 0x94, 0)  # Set bought flag to 0
        self._write8(self.pda_vendor + 0x20, 1)  # Reset interaction state

    def notification_cycler(self):
        """Handle the current displayed pop-up message notification, and message queue"""
        current_time = time.time()
        tyhrranoid_game = self.player_type == RAC3PLAYERTYPE.TYHRRANOID and self.action == 0x58
        self._write32(RAC3MESSAGEBOX.HIDDEN_AND_PAUSED,
                      int(self.inside_hacker_puzzle))  # Hide message box during hacker puzzle
        if self.notification_queue:
            if not self.notification_time:
                self.notification_time = current_time + 3
            if not tyhrranoid_game:
                if self.notification_time < current_time and not self.message_display:
                    # Pop the number of messages that were displayed last cycle
                    for _ in range(self.notification_merge_count):
                        if self.notification_queue:
                            self.notification_queue.pop(0)
                    self.write_messagebox_theme()
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
                        display_time = int((self.notification_time - current_time) * 120)
                        self.messagebox(msg_list, color_bytes_count, longest_line_length, theme, display_time)
                    else:
                        write_message = b''
                        for line in msg_list:
                            write_message += line
                        read_message = self._read_bytes(RAC3MESSAGEBOX.MESSAGE, len(write_message))
                        if read_message != write_message:
                            # Give the player a bit more time to read the new appended line in case it was about to
                            # expire
                            self.notification_time += 0.33
                            display_time = int((self.notification_time - current_time) * 120)
                            # A lot of messages can cause this value to go negative and if so, set a minimum display
                            # time
                            if display_time < 0:
                                self.notification_time = current_time + 0.33
                                display_time = int((self.notification_time - current_time) * 120)
                            self.messagebox(msg_list, color_bytes_count, longest_line_length, theme, display_time)
                            logger.debug(f'Warning: Incorrect Display message detected')
                            logger.debug(f'Message: {merged_message}')
                            logger.debug(f'{read_message}')
                            logger.debug(f'{write_message}')
        else:
            self.notification_time = None
            self.notification_merge_count = 1

    def write_messagebox_theme(self, theme_name: int = RAC3BOXTHEME.DEFAULT) -> None:
        """Update the current messagebox theme, either to the default or a specific theme"""
        theme = THEME_ID_TO_THEME_COLORS[theme_name]
        self._write32(self._read32(RAC3MESSAGEBOX.BACKGROUND_COLOR_POINTER), theme.BACKGROUND)
        self._write32(self._read32(RAC3MESSAGEBOX.EDGE_COLOR_POINTER), theme.BOX)
        self._write32(self._read32(RAC3MESSAGEBOX.CENTER_COLOR_POINTER), theme.BOX)
        self._write32(self._read32(RAC3MESSAGEBOX.TEXT_COLOR_POINTER), theme.TEXT)

    def format_textbox_string(self, msg: str) -> tuple[list[bytes], int, int]:
        """Process a full message into game insertable bytes, for use with in game pop-ups"""
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
        """Converts a message string with color formatting to game insertable bytes with color formatting"""
        result = bytearray()
        color_byte_count = 0
        i = 0
        while i < len(msg):
            matched = False
            for code, byte in FORMAT_NAME_TO_BYTE.items():
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

    def messagebox(self,
                   msg_list: list[bytes],
                   color_bytes_count: int,
                   longest_line_length: int,
                   box_theme: int = RAC3BOXTHEME.DEFAULT,
                   _time: int = 0x168) -> None:
        """Update the contents of the current pop-up message"""
        if _time < 0:
            _time = 0
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
        self.write_messagebox_theme(box_theme)

        self._write32(RAC3MESSAGEBOX.TIMER, _time)
        self._write32(RAC3MESSAGEBOX.TEXT_POINTER, RAC3MESSAGEBOX.MESSAGE)
        self._write32(RAC3MESSAGEBOX.BOX_WIDTH, width)
        self._write_bytes(RAC3MESSAGEBOX.MESSAGE, msg_bytes)
        self._write_float(self._read32(RAC3MESSAGEBOX.VISIBLE_POINTER), 1.0)

    #######################
    # Command Only        #
    #######################

    def dump_info(self, slot_data: dict[str, Any]):
        """Dumps info about the current state of the client"""
        logger.info(f'Collected Items: {self.UnlockItem}')
        count = 0
        for name in SHIP_SLOTS:
            logger.info(f'Planet{count}: {PLANET_NAME_FROM_ID[self._read8(RAC3_REGION_DATA_TABLE[name].SLOT_ADDRESS)]}')
            count += 1
        logger.info(f'Current planet Tracked: {self.planet}')
        logger.info(f'Ship Slot Limit: {self.ship_slot_limit}')
        logger.info(f'Slot Data: {slot_data}')
