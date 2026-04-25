"""This module provides an RAC3 interface to control the game"""
import time
from dataclasses import dataclass
from random import choice, randint, uniform
from typing import Any

from BaseClasses import ItemClassification
from CommonClient import logger
from Utils import __version__
from worlds.rac3.client.general_interface import GameInterface
from worlds.rac3.client.notification import RAC3NOTIFICATION
from worlds.rac3.client.texthelper import (
    ITEM_TO_ORIGINAL_STRING_POINTER_OFFSET,
    ITEM_TO_STRING_TABLE_INDEX_OFFSET,
    TEXT_BYTE_TO_EXPECTED_WIDTH,
)
from worlds.rac3.constants.action_type import RAC3ACTIONTYPE
from worlds.rac3.constants.check_type import CHECKTYPE
from worlds.rac3.constants.data.address import RAC3ADDRESSDATA
from worlds.rac3.constants.data.item import (
    ITEM_FROM_AP_CODE,
    ITEM_NAME_FROM_ID,
    PROG_TO_NAME_DICT,
    RAC3_ITEM_DATA_TABLE,
    armor_data,
    cheat_data,
    equipable_data,
    gadget_data,
    infobot_data,
    non_prog_weapon_data,
    timer_to_status,
    vidcomic_data,
)
from worlds.rac3.constants.data.location import (
    LOCATION_FROM_AP_CODE,
    LOCATION_TO_INFOBOT_FLAG,
    RAC3_LOCATION_DATA_TABLE,
    RAC3LOCATIONDATA,
    REGION_TO_INFOBOT_LOCATION,
)
from worlds.rac3.constants.data.position import RAC3POSITIONDATA
from worlds.rac3.constants.data.region import RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.data.status import RAC3_STATUS_DATA_TABLE
from worlds.rac3.constants.data.vendorslot import (
    RAC3ARMORVENDORSLOTDATA,
    RAC3SHIPVENDORSLOTDATA,
    RAC3SKINVENDORSLOTDATA,
    RAC3VENDORSLOTDATA,
    RAC3WEAPONVENDORSLOTDATA,
)
from worlds.rac3.constants.deaths import CLANK_DEATH_FROM_ACTION, DEATH_FROM_ACTION
from worlds.rac3.constants.input import RAC3INPUT
from worlds.rac3.constants.instruction import (
    ORIGINAL_INSTRUCTIONS,
    PATCH_INSTRUCTION_TO_GAME_IDS,
    PATCH_INSTRUCTION_TO_NAME,
    PATCH_INSTRUCTION_TO_PLANET,
    PATCHED_INSTRUCTIONS,
)
from worlds.rac3.constants.item_tags import RAC3ITEMTAG
from worlds.rac3.constants.items import QUICK_SELECT_LIST, RAC3ITEM, UPGRADE_DICT
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.locations.vendors import (
    ARMOR_VENDOR_INVENTORY,
    ARMOR_VENDOR_LOCATION_TO_ITEM,
    ARMOR_VENDOR_LOCATION_TO_UNLOCK_REGION,
    ITEM_TO_ARMOR_VENDOR_LOCATION,
    ITEM_TO_WEAPON_VENDOR_LOCATION,
    MEGACORP_WEAPONS,
    SHIP_VENDOR_INVENTORY,
    WEAPON_VENDOR_LOCATION_TO_ITEM,
    WEAPON_VENDOR_LOCATION_TO_UNLOCK_REGION,
)
from worlds.rac3.constants.messages.box_format import THEME_ID_TO_THEME_COLORS
from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME
from worlds.rac3.constants.messages.messagebox import RAC3MESSAGEBOX
from worlds.rac3.constants.messages.text_format import CLASSIFICATION_TO_COLOR, FORMAT_NAME_TO_BYTE
from worlds.rac3.constants.messages.text_strings import RAC3TEXTFORMATSTRING
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.pause_state import RAC3PAUSESTATE
from worlds.rac3.constants.player_action import RAC3PLAYERACTION
from worlds.rac3.constants.player_type import PLAYER_TYPE_TO_NAME, RAC3PLAYERTYPE
from worlds.rac3.constants.region import (
    PLANET_FROM_INFOBOT,
    PLANET_LOAD_OFFSET,
    PLANET_NAME_FROM_ID,
    PLANET_VENDOR_OFFSET,
    RAC3REGION,
    RESPAWN_COORDS_OFFSET,
    SHIP_SLOTS,
)
from worlds.rac3.constants.status import RAC3STATUS
from worlds.rac3.constants.vendors.type import RAC3VENDORTYPE
from worlds.rac3.constants.vendors.vendor import RAC3SHIPVENDOR, RAC3VENDOR, RAC3WEAPONVENDOR, VENDORTYPE_TO_SLOT_SIZE
from worlds.rac3.constants.version import (
    GAME_ID_TO_OFFSET,
    GAME_ID_TO_VERSION,
    PAL_SHIFTED_PLANETS,
    RAC3VERSION,
    VERSION_TO_BLACK_SCREEN_ORIGINAL_VALUE,
)


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
            return f"{{ status: {self.status}, unlock_delay: {self.unlock_delay} }}"

    @dataclass
    class Options:
        """Data structure for storing options"""
        start_inventory_from_pool: dict[str, int]
        starting_weapons: dict[str, int]
        bolt_and_xp_multiplier: int
        progressive_weapons: int
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
        player_skin: int
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
        ship_vendor: int
        armor_vendor: int
        scout_vendors: dict[str, int]

    UnlockItem: dict[str, UnlockData] = None
    options = Options
    bolt_and_xp_multiplier_value: int = None
    self_respawning: bool = False
    reloading_handled: bool = False
    is_reloading: int = 0
    timers: dict[str, float] = {}
    planet: str = RAC3REGION.GALAXY
    player_type: str = RAC3PLAYERTYPE.RATCHET
    vehicle: int = 0
    action: int = RAC3PLAYERACTION.IDLE
    action_type: int = RAC3ACTIONTYPE.STATIONARY
    prev_action: int = RAC3PLAYERACTION.IDLE
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
    died_from_softlock: bool = False
    inside_hacker_puzzle: bool = False
    notification_queue: list[RAC3NOTIFICATION] = []
    notification_time: float | None = None
    notification_paused_remaining: float = 0
    notification_merge_count: int = 1
    message_display: bool = False
    ship_slot_limit: int = 0
    one_hp_challenge: dict[str, int] = None
    pda_vendor: int = 0
    last_in_vehicle_time: float = 0.0
    last_in_ship_time: float = 0.0
    last_in_vendor_time: float = 0.0
    deathlink_grace_period: float = 0.0
    nanotech_exp: int = 0
    homewarping: bool = False
    checked_locations: set[str] = set()
    clank_disabled: bool = False
    clank_disabled_trap: bool = False
    unfreeze_packs: bool = False
    visited_planets: set[str] = set()
    weapon_vendor_items: list[str] = []
    armor_vendor_items: list[str] = []
    vendor_type: RAC3VENDORTYPE | None = None
    vendor_string_pointers: dict[str, int] = None
    should_restore_vendor_item_names: bool = True
    cycle_times: list[float] = []

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

    def _read_string(self, address, n):
        return super()._read_string(self.address_convert(address), n)

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

    def address_convert(self, address: int):
        """Address conversion from str to int, and for version correction (with US/JP/EU)"""
        _addr = address
        if isinstance(address, str):
            _addr = int(address, 0)
        if (0x001d6a90 <= _addr <= 0x00300000
            and self.planet in PAL_SHIFTED_PLANETS
            and self.current_game == RAC3VERSION.EU_ID):
                _addr += GAME_ID_TO_OFFSET[RAC3VERSION.EU_ID]

        return _addr

    ###############################
    # Called on Server Connection #
    ###############################

    def proc_option(self, slot_data: dict[str, Any]):
        """Process slot option data received when connecting to the server"""
        logger.debug(f"{slot_data}")
        self.one_hp_challenge = slot_data[RAC3OPTION.ONE_HP_CHALLENGE]
        self.options.start_inventory_from_pool = slot_data[RAC3OPTION.START_INVENTORY_FROM_POOL]
        self.options.starting_weapons = slot_data[RAC3OPTION.STARTING_WEAPONS]
        self.options.bolt_and_xp_multiplier = slot_data[RAC3OPTION.BOLT_AND_XP_MULTIPLIER]
        self.options.progressive_weapons = slot_data[RAC3OPTION.PROGRESSIVE_WEAPONS]
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
        self.options.player_skin = slot_data[RAC3OPTION.PLAYER_SKIN]
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
        self.options.ship_vendor = slot_data[RAC3OPTION.SHIP_VENDOR]
        self.options.armor_vendor = slot_data[RAC3OPTION.ARMOR_VENDOR]
        self.options.scout_vendors = slot_data[RAC3OPTION.SCOUT_VENDORS]

    ########################################
    # Called on Game and Server Connection #
    ########################################

    def init(self):
        """Initialise values once the game and server are both connected"""
        # Unlock state variables/ArmorUpgrade variable
        self.UnlockItem = {name: self.UnlockData() for name in ITEM_FROM_AP_CODE.values()}
        self.UnlockItem.update({RAC3REGION.SLOT_0: self.UnlockData()})
        logger.debug(f"UnlockItem dict:{self.UnlockItem.keys()}")

        # Proc options
        # Bolt and XPMultiplier
        self.bolt_and_xp_multiplier_value = int(self.options.bolt_and_xp_multiplier)
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
        self.cheat_cycler()
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
        self._write8(RAC3STATUS.PLAYER_SKIN, self.options.player_skin)
        self._write8(RAC3STATUS.PLAYER_SKIN_2, self.options.player_skin)

    #############################
    # Start of Main Update Loop #
    #############################

    def early_update(self):
        """Ran early in the update cycle, memory reads should happen here before any evaluations begin"""
        self.planet = PLANET_NAME_FROM_ID[self._read8(RAC3STATUS.PLANET)]
        self.player_type = PLAYER_TYPE_TO_NAME[self._read8(RAC3STATUS.PLAYER_TYPE)]
        self.player_pos = RAC3POSITIONDATA(
            self._read_float(RAC3STATUS.POS_X),
            self._read_float(RAC3STATUS.POS_Y),
            self._read_float(RAC3STATUS.POS_Z))
        self.vehicle = self._read32(RAC3STATUS.VEHICLE_POINTER)
        self.action = self._read8(RAC3STATUS.ACTION)
        self.action_type = self._read8(RAC3STATUS.ACTION_TYPE)
        self.prev_action = self._read8(RAC3STATUS.PREV_ACTION)
        self.inputs = RAC3INPUT(self._read16(RAC3STATUS.READ_INPUT))
        self.health = self._read8(RAC3STATUS.HEALTH)
        self.max_health = self._read8(RAC3STATUS.MAX_HEALTH)
        self.is_reloading = self._read8(RAC3STATUS.FORCE_RELOAD)
        self.inside_hacker_puzzle = self._read8(RAC3STATUS.HELD_ITEM) == RAC3_ITEM_DATA_TABLE[RAC3ITEM.HACKER].ID
        self.message_display = bool(self._read_float(self._read32(RAC3MESSAGEBOX.VISIBLE_POINTER)))
        self.nanotech_exp = self._read32(RAC3STATUS.NANOTECH_EXP)
        self.clank_disabled = bool(self._read8(RAC3STATUS.NO_CLANK))
        self.pda_vendor = self.find_pda_vendor()
        self.vendor_type = self.vendor_check()
        self.get_visited_planets()
        self.determine_weapon_vendor_items()
        self.determine_armor_vendor_items()
        self.vehicle_check()
        self.ship_check()
        self.pause_check()
        self.check_latches()

    def get_visited_planets(self):
        """Returns a set of all planets the player has visited"""
        visited_planets: set[str] = set()
        for region in RAC3_REGION_DATA_TABLE.keys():
            if self._read8(RAC3STATUS.VISITED_BASE + RAC3_REGION_DATA_TABLE[region].ID):
                visited_planets.add(region)
        self.visited_planets = visited_planets

    def determine_weapon_vendor_items(self):
        """Determine which items should be sold by the weapon vendor on the current planet."""
        items_to_sell: list[str] = []
        already_sold = set()
        for location, item in WEAPON_VENDOR_LOCATION_TO_ITEM.items():
            if item == RAC3ITEM.HOLO_SHIELD and RAC3LOCATION.TYHRRANOSIS_BOSS not in self.checked_locations:
                continue
            if WEAPON_VENDOR_LOCATION_TO_UNLOCK_REGION[location] in self.visited_planets and item not in already_sold:
                if location in self.checked_locations:
                    already_sold.add(item)
                else:
                    items_to_sell.append(item)
        self.weapon_vendor_items = items_to_sell

    def determine_armor_vendor_items(self):
        """Determine which items should be sold by the armor vendor on the Starship Phoenix."""
        items_to_sell: list[str] = []
        already_sold = set()
        for location, item in ARMOR_VENDOR_LOCATION_TO_ITEM.items():
            if ARMOR_VENDOR_LOCATION_TO_UNLOCK_REGION[location] in self.visited_planets and item not in already_sold:
                if location in self.checked_locations:
                    already_sold.add(item)
                else:
                    items_to_sell.append(item)
        self.armor_vendor_items = items_to_sell

    def ship_check(self):
        """
        Updates the last_in_ship_time to address the short moment where everything is 0 while gadgets spawn
        """
        current_time = time.time()
        if self.pause_state_value == RAC3PAUSESTATE.PLANET_CHANGE:
            self.last_in_ship_time = current_time

    def vehicle_check(self):
        """
        Updates the last_in_vehicle_time when the player is in a vehicle.
        Used to detect if the player died while in a vehicle for deathlink.
        """
        current_time = time.time()
        if self.vehicle or (current_time - self.last_in_vehicle_time < 1 and self.action == RAC3PLAYERACTION.DEATH):
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
            logger.error(f"Aborting homewarp, Unknown Planet: {self.planet}")
            return
        planet_data = RAC3_REGION_DATA_TABLE[self.planet]
        if planet_data.PLANET_TO_LOAD:
            self.homewarping = True
            self._write8(planet_data.PLANET_TO_LOAD, RAC3_REGION_DATA_TABLE[RAC3REGION.STARSHIP_PHOENIX].ID)
            self._write8(planet_data.PLANET_SPECIAL_OFFSET + RAC3STATUS.PLANET_LOAD, 1)
            self._write8(planet_data.PLANET_SPECIAL_OFFSET + RAC3STATUS.PAUSE_STATE, RAC3PAUSESTATE.PLANET_CHANGE)
            logger.debug(f"Player home-warped from {self.planet}")
        else:
            logger.warning(f"Couldn't find warp data to leave planet: {self.planet}")

    #################
    # Receive Items #
    #################

    def item_received(self,
                      item_code: int,
                      our_name: str | None,
                      other_player: str | None,
                      location: int | None):
        """Handle receiving items from the multiworld"""
        name = PROG_TO_NAME_DICT.get(ITEM_FROM_AP_CODE[item_code], ITEM_FROM_AP_CODE[item_code])
        if other_player is not None:
            classification = RAC3_ITEM_DATA_TABLE[name].AP_CLASSIFICATION
            if other_player == our_name:
                if location == 0:
                    pass
                elif location > 0:
                    if classification == ItemClassification.trap:
                        self.enqueue_notification(
                            f"{RAC3TEXTFORMATSTRING.WHITE}Activated "
                            f"{RAC3TEXTFORMATSTRING.NORMAL}{ITEM_FROM_AP_CODE[item_code]} "
                            f"{RAC3TEXTFORMATSTRING.WHITE}at\n"
                            f"{RAC3TEXTFORMATSTRING.WHITE}{LOCATION_FROM_AP_CODE[location]}",
                            RAC3BOXTHEME.WARNING)
                    else:
                        self.enqueue_notification(
                            f"Found "
                            f"{CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]} "
                            f"{RAC3TEXTFORMATSTRING.NORMAL}at\n{LOCATION_FROM_AP_CODE[location]}")
                else:
                    if classification == ItemClassification.trap:
                        self.enqueue_notification(
                            f"{RAC3TEXTFORMATSTRING.WHITE}Activated "
                            f"{RAC3TEXTFORMATSTRING.NORMAL}{ITEM_FROM_AP_CODE[item_code]}",
                            RAC3BOXTHEME.WARNING)
                    else:
                        self.enqueue_notification(
                            f"Collected {CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]}")
            else:
                if classification == ItemClassification.trap:
                    self.enqueue_notification(
                        f"{RAC3TEXTFORMATSTRING.GREEN}{other_player}"
                        f"{RAC3TEXTFORMATSTRING.WHITE} activated your "
                        f"{RAC3TEXTFORMATSTRING.NORMAL}{ITEM_FROM_AP_CODE[item_code]}",
                        RAC3BOXTHEME.WARNING)
                else:
                    self.enqueue_notification(
                        f"Received {CLASSIFICATION_TO_COLOR[classification]}{ITEM_FROM_AP_CODE[item_code]} "
                        f"{RAC3TEXTFORMATSTRING.NORMAL}from "
                        f"{RAC3TEXTFORMATSTRING.GREEN}{other_player}")
        logger.debug(f"Item received: {ITEM_FROM_AP_CODE[item_code]}, AP code: {item_code}")
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
                bolt_pack = min(200000, max(30000, int(bolt * 0.2)))
                new_bolts = bolt + bolt_pack
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
                if self.bolt_and_xp_multiplier_value <= 6:
                    _time = round(time.time() + uniform(10, 30), 4)
                    self.timers[name + str(_time)] = _time
                    self.bolt_and_xp_multiplier_value += 1
            case RAC3ITEM.NANOTECH_XP:
                nanotech_gain = min(200000, max(20000, int(self.nanotech_exp * 0.15)))
                self.nanotech_exp += nanotech_gain
                if self.nanotech_exp > 0x7FFFFFFF:
                    self.nanotech_exp = 0x7FFFFFFF
                self._write32(RAC3STATUS.NANOTECH_EXP, self.nanotech_exp)
            case RAC3ITEM.WEAPON_XP:
                valid_weapons = []
                for weapon_name, weapon_data in non_prog_weapon_data.items():
                    if self.UnlockItem[weapon_name].status:
                        level = max(RAC3_ITEM_DATA_TABLE[ITEM_NAME_FROM_ID[self._read8(weapon_data.LEVEL_ADDRESS)]].LEVEL,
                                    self.weapon_level_from_xp(weapon_name))
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
                if self.vehicle:
                    health_addr = self._read32(self._read32(self.vehicle + 0x68))
                    self._write_float(health_addr, 1)
            case RAC3ITEM.NO_AMMO_TRAP:
                for weapon_name in non_prog_weapon_data.keys():
                    if self.UnlockItem[weapon_name].status:
                        self._write32(non_prog_weapon_data[weapon_name].AMMO_ADDRESS, 0)
                self._write8(RAC3STATUS.QWARK_AMMO, 0)
            case RAC3ITEM.LOCK_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(10, 20)
                else:
                    self.timers[name] = int(time.time() + uniform(10, 15))
            case RAC3ITEM.MIRROR_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(10, 20)
                else:
                    self.timers[name] = int(time.time() + uniform(10, 20))
            case RAC3ITEM.BLACK_SCREEN_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(6, 12)
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
                    self.timers[name] += randint(10, 20)
                else:
                    self.timers[name] = int(time.time() + uniform(10, 20))
            case RAC3ITEM.DISARM_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(6, 15)
                else:
                    self.timers[name] = int(time.time() + uniform(6, 15))
            case RAC3ITEM.WRENCH_ONLY_TRAP:
                if self.timers.get(name, False):
                    self.timers[name] += randint(10, 15)
                else:
                    self.timers[name] = int(time.time() + uniform(10, 20))
            case RAC3ITEM.LIGHTSABER_WRENCH:
                self._write8(RAC3STATUS.WRENCH_REPLACEMENT_CHEAT, 1)
        if name in non_prog_weapon_data.keys():
            if non_prog_weapon_data[name].AMMO:
                self._write32(non_prog_weapon_data[name].AMMO_ADDRESS, non_prog_weapon_data[name].AMMO)
        if name in equipable_data.keys() and self.UnlockItem[name].status == 1:
            self.update_equip(name)

    def weapon_level_up(self, weapon_name: str):
        """Level up a weapon from xp reward"""
        weapon_data = non_prog_weapon_data[weapon_name]
        current_id = self._read8(weapon_data.LEVEL_ADDRESS)
        current_name = ITEM_NAME_FROM_ID[current_id]
        current_level = max(RAC3_ITEM_DATA_TABLE[current_name].LEVEL, self.weapon_level_from_xp(weapon_name))
        if current_level < 5:
            target_level = current_level + 1
            target_id = UPGRADE_DICT[weapon_name][target_level - 1]
            target_name = ITEM_NAME_FROM_ID[target_id]
            target_xp = RAC3_ITEM_DATA_TABLE[target_name].XP_THRESHOLD
            target_ammo = RAC3_ITEM_DATA_TABLE[target_name].AMMO
            logger.debug(f"level up {weapon_name} to {target_name}, target level: {current_level}, "
                         f"target id: {target_id}, target xp:{target_xp}")
            self._write32(weapon_data.XP_ADDRESS, target_xp)
            self._write8(weapon_data.LEVEL_ADDRESS, target_id)
            if target_ammo:
                self._write32(weapon_data.AMMO_ADDRESS, target_ammo)

    def weapon_level_from_xp(self, weapon_name: str) -> int:
        """Returns the weapon level based on the current xp"""
        current_xp = self._read32(non_prog_weapon_data[weapon_name].XP_ADDRESS)
        level_from_xp = 1
        for lvl in range(5):
            target_id = UPGRADE_DICT[weapon_name][lvl]
            target_name = ITEM_NAME_FROM_ID[target_id]
            xp_threshold = RAC3_ITEM_DATA_TABLE[target_name].XP_THRESHOLD
            if current_xp >= xp_threshold:
                level_from_xp = lvl + 1
        return level_from_xp

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
        #TODO: Implement a distance based checktype
        if location == RAC3LOCATION.OBANI_GEMINI_SKIDD and self.planet == RAC3REGION.OBANI_GEMINI:
            current_pos = self.player_pos
            skidd_pos = RAC3POSITIONDATA(201.2, 364, 296.8)
            return (
                abs(current_pos.X - skidd_pos.X) < 8
                and abs(current_pos.Y - skidd_pos.Y) < 8
                and abs(current_pos.Z - skidd_pos.Z) < 8
            )
        if location == RAC3LOCATION.PHOENIX_MEET_SASHA and self.planet == RAC3REGION.STARSHIP_PHOENIX:
            current_pos = self.player_pos
            sasha_pos = RAC3POSITIONDATA(157, 362, 118)
            return (
                abs(current_pos.X - sasha_pos.X) < 8
                and abs(current_pos.Y - sasha_pos.Y) < 8
                and abs(current_pos.Z - sasha_pos.Z) < 8
            )
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
            self.died_from_softlock = self._read16(RAC3STATUS.SOFTLOCK_TIMER) >= 0xF0
            self.reloading_handled = True
            logger.debug(f"{self.player_type} is Respawning, death state: {self.last_death_state},"
                         f" death count: {self.last_death_count}, in vehicle? {self.died_in_vehicle}")
        if not self.is_reloading and self.reloading_handled:
            self.death_count = self._read32(RAC3STATUS.DEATH_COUNT)
            self.has_died = self.death_count > self.last_death_count
            self.last_death_count = self.death_count
            self.reloading_handled = False
            logger.debug(f"{self.player_type} has Respawned, death count: {self.death_count}, has died?"
                         f" {self.has_died}")
        else:
            self.has_died = False

    def alive(self) -> tuple[bool, str]:
        """Checks the current game state to determine if the player is still alive, and if not then how they died"""
        if self.has_died:
            self.last_death_count = self.death_count
            logger.debug("Death Detected! (death count increased)")
            is_clank = self.player_type == RAC3PLAYERTYPE.CLANK
            death = DEATH_FROM_ACTION.get(self.last_death_state, "ran out of nanotech.") if not is_clank else (
                CLANK_DEATH_FROM_ACTION.get(self.last_death_state, "ran out of nanotech."))

            # Vehicle pointer becomes 0 during reload, but the address next to it gets a value during reload after
            # vehicle death
            if self.died_in_vehicle:
                # Vehicle death uses state 34 which is the same as getting eaten by a shark
                death = "didn't leave the vehicle in time."
            elif self.died_from_softlock:
                death = "softlocked."
            return False, f"{self.player_type} {death}"

        #logger.debug(f"{self.player_type} is Alive")
        return True, f"{self.player_type} is Alive"

    def can_be_killed(self) -> bool:
        """Checks if the player can be killed based on the current game state."""
        current_time = time.time()
        if (self.pause_state
                or self.inside_hacker_puzzle
                or (self.action_type == RAC3ACTIONTYPE.PLAYER_MOVEMENT_LOCKED and not self.vehicle)
                or self.action_type == RAC3ACTIONTYPE.IN_CUTSCENE):
            self.deathlink_grace_period = current_time
        if current_time - self.deathlink_grace_period < 1:
            return False
        return True

    def kill_player(self) -> bool:
        """Checks the current game state to determine if and how to kill the player, returns success/failure"""
        if not self.can_be_killed():
            logger.debug("player unable to be killed")
            return False
        self._write8(RAC3STATUS.HEALTH, 0)
        self._write8(RAC3STATUS.NANOPAK_HEALTH, 0)
        # death = choice(list(DEATH_FROM_ACTION.keys()))
        if self.vehicle:
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
            logger.debug("player in vehicle, killing vehicle too")
            # logger.debug(f'player died of {DEATH_FROM_ACTION[death]}')
        else:
            match self.player_type:
                case RAC3PLAYERTYPE.RATCHET:
                    if self.action not in DEATH_FROM_ACTION.keys() and self.vehicle == 0:
                        self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.HURT)
                        # update ratchet state to cancel free fall and other problematic states

                    # self._write8(RAC3STATUS.ACTION, death)
                    # logger.debug(f'player died of {DEATH_FROM_ACTION[death]}')
                case RAC3PLAYERTYPE.CLANK:
                    # Clank taking damage state (updates state to trigger death animation once at 0 health)
                    self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.CLANK_HURT)
                    self._write8(RAC3STATUS.PREV_ACTION, RAC3PLAYERACTION.CLANK_HURT)  # Past state
                    self._write8(RAC3STATUS.SECOND_PREV_ACTION, RAC3PLAYERACTION.CLANK_HURT)  # This helps the death animation trigger
                    logger.debug("player is clank, clank must die dramatically")
                case RAC3PLAYERTYPE.GIANT:
                    # Giant Clank punched state (updates state to trigger death animation once at 0 health)
                    self._write32(RAC3STATUS.GIANT_CLANK_HEALTH, 0)
                    self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.GIANT_CLANK_HURT)
                    self._write8(RAC3STATUS.PREV_ACTION, RAC3PLAYERACTION.GIANT_CLANK_HURT)  # Past state
                    self._write8(RAC3STATUS.SECOND_PREV_ACTION, RAC3PLAYERACTION.GIANT_CLANK_HURT)  # This helps the death animation trigger
                    logger.debug("player is giant clank, giant clank must die dramatically")
                case RAC3PLAYERTYPE.TYHRRANOID:
                    # Tyhrranoid taking damage state (updates state to trigger death animation once at 0 health)
                    self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.TYHRRANOID_HURT)
                    self._write8(RAC3STATUS.PREV_ACTION, RAC3PLAYERACTION.TYHRRANOID_HURT)  # Past state
                    self._write8(RAC3STATUS.SECOND_PREV_ACTION, RAC3PLAYERACTION.TYHRRANOID_HURT)  # This helps the death animation trigger
                    logger.debug("player is tyhrranoid, tyhrranoid must be squished")
                case RAC3PLAYERTYPE.QWARK:
                    # Qwark taking damage state (updates state to trigger death animation once at 0 health)
                    self._write8(RAC3STATUS.ACTION, RAC3PLAYERACTION.QWARK_HURT)
                    self._write8(RAC3STATUS.PREV_ACTION, RAC3PLAYERACTION.QWARK_HURT)  # Past state
                    self._write8(RAC3STATUS.SECOND_PREV_ACTION, RAC3PLAYERACTION.QWARK_HURT)  # This helps the death animation trigger
                    logger.debug("player is qwark, qwark must die dramatically")
        logger.debug("player successfully killed")
        return True

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
                    self.enqueue_notification(
                        f"You do not have the items required\nto leave this planet through your ship.\n\n"
                        f"Hold:{RAC3TEXTFORMATSTRING.WHITE}{RAC3TEXTFORMATSTRING.L2}+{RAC3TEXTFORMATSTRING.R2}+{RAC3TEXTFORMATSTRING.L1}+{RAC3TEXTFORMATSTRING.R1}+ SELECT{RAC3TEXTFORMATSTRING.NORMAL}\nto warp back to the {RAC3TEXTFORMATSTRING.GREEN}Starship Phoenix{RAC3TEXTFORMATSTRING.NORMAL}.",
                        RAC3BOXTHEME.WARNING,
                        8.0)
            case RAC3REGION.PHOENIX_ASSAULT:
                logger.info("If you want to travel to the regular phoenix, hold L2 + R2 + L1 + R1 + SELECT")
                self.enqueue_notification(
                    f"If you want to travel to the regular phoenix\nHold:{RAC3TEXTFORMATSTRING.WHITE}{RAC3TEXTFORMATSTRING.L2}+{RAC3TEXTFORMATSTRING.R2}+{RAC3TEXTFORMATSTRING.L1}+{RAC3TEXTFORMATSTRING.R1}+ SELECT",
                    RAC3BOXTHEME.WARNING,
                    5.0)

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
            logger.debug(f"Player respawned on: {self.planet}")
        else:
            logger.debug(f"Player respawned at last checkpoint on: {self.planet}")
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

    ###################
    # Vendor Handling #
    ###################

    def vendor_check(self):
        """Returns the current vendor type if the vendor is open, else None"""
        if self.pause_state_value == RAC3PAUSESTATE.VENDOR and self.planet in PLANET_VENDOR_OFFSET.keys():
            self.last_in_vendor_time = time.time()
            try:
                return RAC3VENDORTYPE(self._read8(
                    RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.VENDOR_TYPE_OFFSET)))
            except ValueError:
                return None
        self.restore_vendor_item_names()
        return None

    def vendor_update(self):
        """Read current vendor inventory and replace all items after the all ammo item with all items in the game"""
        # Only update vendor if on a known planet with a vendor
        if self.planet not in PLANET_VENDOR_OFFSET.keys() or self.vendor_type is None:
            return

        is_pda_vendor = self._read8(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.IS_PDA_OFFSET))
        if is_pda_vendor:
            return

        vendor_size = self._read32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.SLOT_COUNT_OFFSET))
        current_inventory = [self.read_vendor_slot_data(self.vendor_type, slot) for slot in range(vendor_size)]
        new_inventory = []
        match self.vendor_type:
            case RAC3VENDORTYPE.WEAPON:
                if not self.options.weapon_vendors:
                    return
                is_slimcognito = (self.planet == RAC3REGION.AQUATOS
                                  and bool(self._read8(RAC3WEAPONVENDOR.get_vendor_property_address(
                            self.planet, RAC3WEAPONVENDOR.VENDOR_WEAPON_TYPE_OFFSET))))
                # Slim Cognito does not have a max ammo item, so we just replace the entire inventory
                if is_slimcognito:
                    # Only show megacorp weapons
                    megacorp_weapons = [item for item in self.weapon_vendor_items if item in MEGACORP_WEAPONS]
                    new_inventory.extend(
                        [RAC3WEAPONVENDORSLOTDATA([RAC3_ITEM_DATA_TABLE[item].ID, 0, 0x0CDB, 0, 0, 0, 0]) for item in megacorp_weapons])
                    # Add the memory card item
                    new_inventory.append(RAC3WEAPONVENDORSLOTDATA([0, 0, 0x0CDB, 0, 0, 0, 1]))
                else:
                    # Only show gadgetron weapons, keep current inventory up to all_ammo
                    for slot_data in current_inventory:
                        new_inventory.append(slot_data)
                        if slot_data.all_ammo.value:
                            break
                    gadgetron_weapons = [item for item in self.weapon_vendor_items if item not in MEGACORP_WEAPONS]
                    new_inventory.extend(
                        [RAC3WEAPONVENDORSLOTDATA([RAC3_ITEM_DATA_TABLE[item].ID, 0, 0x0CDB, 0, 0, 0, 0]) for item in gadgetron_weapons])
                    if self.planet == RAC3REGION.STARSHIP_PHOENIX:
                        # add memory card item
                        new_inventory.append(RAC3WEAPONVENDORSLOTDATA([0, 0, 0x0CDB, 0, 0, 0, 1]))
                self.overwrite_vendor_item_names()
            case RAC3VENDORTYPE.ARMOR:
                if not self.options.armor_vendor:
                    return
                new_inventory = [ARMOR_VENDOR_INVENTORY[ITEM_TO_ARMOR_VENDOR_LOCATION[item]] for item in self.armor_vendor_items]
                self.overwrite_vendor_item_names()
            case RAC3VENDORTYPE.SHIP:
                if not self.options.ship_vendor:
                    return
                ship_keys = list(SHIP_VENDOR_INVENTORY.keys())[:self.UnlockItem[RAC3REGION.SLOT_0].status*3]
                # Set item_name_ptr for each ship item using the string pointer
                for key in ship_keys:
                    addr = self.vendor_string_pointers.get(key, 0)
                    SHIP_VENDOR_INVENTORY[key].item_name_ptr.value = addr
                filtered_ship_items = [SHIP_VENDOR_INVENTORY[key] for key in ship_keys if key not in self.checked_locations]
                new_inventory = filtered_ship_items
                # Undo the cosmetic overwrite from buying ship vendor items
                self.add_cosmetics()
            case _:
                logger.debug(f"Vendor cycler does not support vendor type {self.vendor_type} yet")
                return
        self.write_vendor_inventory(new_inventory, self.vendor_type)
        cursor_pos = self._read32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.CURSOR_OFFSET))
        if len(new_inventory) == 0:
            self._write32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.CURSOR_OFFSET), 0)
        elif cursor_pos >= len(new_inventory):
            self._write32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.CURSOR_OFFSET),
                          len(new_inventory) - 1)

    def read_vendor_slot_data(self, vendor_type: RAC3VENDORTYPE,
                              slot: int) -> RAC3WEAPONVENDORSLOTDATA | RAC3ARMORVENDORSLOTDATA | RAC3SHIPVENDORSLOTDATA:
        """Returns the data for a given slot in the vendor inventory"""
        self._read32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.VENDOR_TYPE_OFFSET))
        match vendor_type:
            case RAC3VENDORTYPE.WEAPON:
                data = RAC3WEAPONVENDORSLOTDATA(
                    [self.read_vendor_prop(prop, slot, vendor_type) for prop in RAC3WEAPONVENDORSLOTDATA().get_data()])
            case RAC3VENDORTYPE.ARMOR:
                data = RAC3ARMORVENDORSLOTDATA(
                    [self.read_vendor_prop(prop, slot, vendor_type) for prop in RAC3ARMORVENDORSLOTDATA().get_data()])
            case RAC3VENDORTYPE.SHIP:
                data = RAC3SHIPVENDORSLOTDATA(
                    [self.read_vendor_prop(prop, slot, vendor_type) for prop in RAC3SHIPVENDORSLOTDATA().get_data()])
            case RAC3VENDORTYPE.SKIN:
                data = RAC3SKINVENDORSLOTDATA(
                    [self.read_vendor_prop(prop, slot, vendor_type) for prop in RAC3SKINVENDORSLOTDATA().get_data()])
            case _:
                raise NotImplementedError(f"Reading vendor type {vendor_type.name} has not been implemented yet")
        return data

    def read_vendor_prop(self, prop: RAC3VENDORSLOTDATA.Property, slot: int, vendor_type: RAC3VENDORTYPE) -> int:
        """Reads the value of a vendor slot property"""
        match prop.size:
            case 1:
                return self._read8(RAC3VENDOR.get_vendor_item_property_address(self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type]))
            case 2:
                return self._read16(RAC3VENDOR.get_vendor_item_property_address(self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type]))
            case 4:
                return self._read32(RAC3VENDOR.get_vendor_item_property_address(self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type]))
            case _:
                raise ValueError(f"Invalid property size: {prop.size} Bytes")

    def write_vendor_inventory(self, inventory: list[RAC3VENDORSLOTDATA], vendor_type: RAC3VENDORTYPE):
        """Write a list of vendor slot data objects to the current planet's vendor inventory"""
        self._write32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.SLOT_COUNT_OFFSET), len(inventory))
        if len(inventory) == 0:
            start_address = RAC3STATUS.VENDOR_BASE + PLANET_VENDOR_OFFSET[self.planet]
            match vendor_type:
                case RAC3VENDORTYPE.SHIP:
                    # change the string pointer to no items available message in code cave
                    item_name_addr = start_address + RAC3SHIPVENDOR.ITEM_NAME_PTR_OFFSET
                    already_equipped_addr = start_address + RAC3SHIPVENDOR.ITEM_IS_EQUIPPED_OFFSET
                    string_key = (RAC3VENDOR.ALL_ITEMS_SOLD_OUT_LOC_KEY
                                  if self.has_checked_all_locations_with_tag(RAC3TAG.SHIP)
                                  else RAC3VENDOR.NO_ITEMS_AVAILABLE_LOC_KEY)
                    self._write32(item_name_addr, self.vendor_string_pointers[string_key])
                    self._write32(already_equipped_addr, 1)
                case _:
                    # clear out vendor slot memory
                    slot_size = VENDORTYPE_TO_SLOT_SIZE[vendor_type]
                    self._write_bytes(start_address, bytes(slot_size*5))

        for slot, slot_data in enumerate(inventory):
            for prop in slot_data.get_data():
                match prop.size:
                    case 1:
                        self._write8(RAC3VENDOR.get_vendor_item_property_address(self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type]),
                                    prop.value)
                    case 2:
                        self._write16(RAC3VENDOR.get_vendor_item_property_address(self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type]),
                                    prop.value)
                    case 4:
                        self._write32(RAC3VENDOR.get_vendor_item_property_address(self.planet, slot, prop.offset, VENDORTYPE_TO_SLOT_SIZE[vendor_type]),
                                    prop.value)
        logger.debug(f"Wrote {len(inventory)} items to {vendor_type.name} vendor on planet {self.planet}")

    def hovering_over_ammo(self) -> bool:
        """Check if the player is currently hovering over the max ammo item in a weapon vendor"""
        if self.vendor_type != RAC3VENDORTYPE.WEAPON:
            return False
        cursor_pos = self._read32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.CURSOR_OFFSET))
        slot_data = self.read_vendor_slot_data(RAC3VENDORTYPE.WEAPON, cursor_pos)
        if slot_data.ammo_text.value:
            return True
        return False

    def overwrite_vendor_item_names(self):
        """Overwrite the names of the weapons in the weapon vendor with the provided list of weapon names"""
        if self.planet not in PLANET_VENDOR_OFFSET.keys():
            return
        string_id_table_start = self._read32(PLANET_LOAD_OFFSET[self.planet] + RAC3STATUS.PLANET_STRING_TABLE_BASE)
        combined_locations = ITEM_TO_WEAPON_VENDOR_LOCATION | ITEM_TO_ARMOR_VENDOR_LOCATION
        for item in self.weapon_vendor_items + self.armor_vendor_items:
            item_string_offset = ITEM_TO_STRING_TABLE_INDEX_OFFSET.get(item, None)
            if item_string_offset is not None:
                item_string_address = string_id_table_start + item_string_offset
                location = combined_locations[item]
                ap_item_ptr = self.vendor_string_pointers[location]
                self._write32(item_string_address, ap_item_ptr)
        self.should_restore_vendor_item_names = True

    def restore_vendor_item_names(self):
        """Restore the names of the weapons in the weapon vendor to their original values"""
        if not self.should_restore_vendor_item_names or self.planet not in PLANET_VENDOR_OFFSET.keys():
            return
        string_id_table_start = self._read32(PLANET_LOAD_OFFSET[self.planet] + RAC3STATUS.PLANET_STRING_TABLE_BASE)
        all_strings_start = self._read32(string_id_table_start)
        for item in non_prog_weapon_data.keys() | armor_data.keys():
            item_string_offset = ITEM_TO_STRING_TABLE_INDEX_OFFSET.get(item, None)
            if item_string_offset is not None:
                item_string_address = string_id_table_start + item_string_offset
                if self._read32(item_string_address) not in self.vendor_string_pointers.values():
                     continue
                original_string_ptr = all_strings_start + ITEM_TO_ORIGINAL_STRING_POINTER_OFFSET[item]
                if self.current_game == RAC3VERSION.EU_ID:
                    original_string_ptr += 0x11
                self._write32(item_string_address, original_string_ptr)
        self.should_restore_vendor_item_names = False

    ##################
    # Sequence Break #
    ##################

    def sequence_break(self) -> None:
        """Checks the current planet and unsets any planet access flags that would interfere with location collecting"""
        infobot_location = REGION_TO_INFOBOT_LOCATION.get(self.planet, None)
        if infobot_location is not None and infobot_location in RAC3_LOCATION_DATA_TABLE:
            infobot_flag = LOCATION_TO_INFOBOT_FLAG.get(infobot_location, None)
            if (infobot_flag is not None
                    and infobot_location not in self.checked_locations
                    and infobot_flag != RAC3STATUS.ALLOW_SHIP):
                self._write8(infobot_flag, 0)

        if self.planet == RAC3REGION.STARSHIP_PHOENIX:
            # Fix can't play Qwark VidComics in some case which first event is skipped
            self._write8(0x001426E8, 1)  # Todo: Take Qwark to Cage Mission
            # Bring qwark back to life until Ratchet has met Sasha on the bridge
            if RAC3LOCATION.PHOENIX_MEET_SASHA not in self.checked_locations:
                self._write8(RAC3STATUS.ESCAPED_LEVIATHAN, 0)
        if self.planet != RAC3REGION.ZELDRIN_STARPORT and not self._read8(RAC3STATUS.ZELDRIN_END_LEVIATHAN):
            self._write8(RAC3STATUS.ZELDRIN_START_LEVIATHAN, 0)

        if self.options.holostar_skip:
            self._write8(RAC3STATUS.VISITED_BASE + RAC3_REGION_DATA_TABLE[RAC3REGION.HOLOSTAR_STUDIOS_CLANK].ID, 1)

    ##################
    # End of Main Loop #
    ##################

    def late_update(self):
        """Ran at the end of the main loop to update any memory values based on collection state"""
        self.gadget_cycler()
        self.planet_cycler()
        self.weapon_cycler()
        self.vidcomic_cycler()
        self.armor_cycler()
        self.timer_cycler()
        self.cheat_cycler()
        self.weapon_exp_cycler()
        self.verify_quick_select_and_last_used()
        self.clank_cycler()
        self.multiplier_cycler()
        self.patch_cycler()
        self.overflow_fix()
        self.health_cycler()
        self.pda_vendor_cycler()
        self.notification_cycler()

    def gadget_cycler(self):
        """Cycles through each gadget and updates their state"""
        if not self.should_cycle_gadgets() or self.near_pda_vendor():
            self.respawn_gadgets()
            return

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

    def should_cycle_gadgets(self) -> bool:
        """Check if it's safe to cycle gadgets
        used to ensure gadgets can respawn without the cycler interfering"""
        if ((time.time() - self.last_in_ship_time) < 1.5
                or self.is_reloading
                or self.self_respawning
                or self.action_type == RAC3ACTIONTYPE.PLAYER_MOVEMENT_LOCKED):
            return False
        return True

    def near_pda_vendor(self) -> bool:
        """Check if we are near the PDA Vendor"""
        if self.planet == RAC3REGION.QWARKS_HIDEOUT and self.distance_to_moby(self.pda_vendor) < 15.0:
            # In case the PDA vendor bugs out and doesn't play the cutscene
            if (self._read32(PLANET_LOAD_OFFSET[self.planet] + RAC3STATUS.PLANET_BOLT_DIFFERENCE_BASE) & 0x80000000 # If bolt difference is negative
                and self.action_type != RAC3ACTIONTYPE.PLAYER_MOVEMENT_LOCKED):
                 self._write8(gadget_data[RAC3ITEM.PDA].UNLOCK_ADDRESS_2, 1)
            return True
        return False

    def distance_to_moby(self, moby) -> float:
        """Calculate the distance from the player to the moby"""
        if not moby:
            return float("inf")
        assert RAC3STATUS.HIDEOUT_MOBY_TABLE_START < moby < RAC3STATUS.HIDEOUT_MOBY_TABLE_START + 0x00100000, \
            "Moby not in the typical moby range"
        player_pos = self.player_pos
        moby_pos = RAC3POSITIONDATA(
            self._read_float(moby + 0x10),
            self._read_float(moby + 0x14),
            self._read_float(moby + 0x18))
        distance = ((player_pos.X - moby_pos.X) ** 2 +
                    (player_pos.Y - moby_pos.Y) ** 2 +
                    (player_pos.Z - moby_pos.Z) ** 2) ** 0.5
        return distance

    def get_checked_locations_by_tag(self, tag: str) -> list[int]:
        """Get a list of checked locations that match the given tag"""
        return [loc for loc in self.checked_locations if tag in RAC3_LOCATION_DATA_TABLE[loc].TAGS]

    def has_checked_all_locations_with_tag(self, tag: str) -> bool:
        """Check if all locations with the given tag have been checked"""
        for loc in RAC3_LOCATION_DATA_TABLE.keys():
            if tag in RAC3_LOCATION_DATA_TABLE[loc].TAGS and loc not in self.checked_locations:
                return False
        return True

    def respawn_gadgets(self):
        """Respawn gadget if the associated location isn't checked but the gadget is unlocked through AP"""
        if (self.UnlockItem[RAC3ITEM.REFRACTOR].status
                and RAC3LOCATION.MARCADIA_REFRACTOR not in self.checked_locations
                and self.planet == RAC3REGION.MARCADIA):
            self._write8(gadget_data[RAC3ITEM.REFRACTOR].UNLOCK_ADDRESS, 0)

        if (self.UnlockItem[RAC3ITEM.CHARGE_BOOTS].status
                and RAC3LOCATION.DAXX_CHARGE_BOOTS not in self.checked_locations
                and self.planet == RAC3REGION.DAXX):
            self._write8(gadget_data[RAC3ITEM.CHARGE_BOOTS].UNLOCK_ADDRESS, 0)

        if (self.UnlockItem[RAC3ITEM.NANO_PAK].status
                and RAC3LOCATION.CRASH_SITE_NANO_PAK not in self.checked_locations
                and self.planet == RAC3REGION.CRASH_SITE):
            self._write8(gadget_data[RAC3ITEM.NANO_PAK].UNLOCK_ADDRESS, 0)

        if ((self.UnlockItem[RAC3ITEM.BOLT_GRABBER].status or self.UnlockItem[RAC3ITEM.BOX_BREAKER].status)
                and RAC3LOCATION.ZELDRIN_STARPORT_BOLT_GRABBER not in self.checked_locations
                and self.planet == RAC3REGION.ZELDRIN_STARPORT):
            self._write8(gadget_data[RAC3ITEM.BOLT_GRABBER].UNLOCK_ADDRESS, 0)
            self._write8(gadget_data[RAC3ITEM.BOX_BREAKER].UNLOCK_ADDRESS, 0)
        if (self.UnlockItem[RAC3ITEM.PDA].status
                and RAC3LOCATION.HIDEOUT_PDA not in self.checked_locations
                and self.planet == RAC3REGION.QWARKS_HIDEOUT):
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
        # If in vendor, lock all non-progressive weapons to allow second unlock address to work properly
        if self.vendor_type == RAC3VENDORTYPE.WEAPON and not self.hovering_over_ammo():
            weapons_to_remove = self.weapon_vendor_items
            for name in non_prog_weapon_data.keys():
                if name in weapons_to_remove:
                    addr = non_prog_weapon_data[name].UNLOCK_ADDRESS
                    self._write8(addr, 0)
            return

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

    def update_weapon_equip(self, equip: int | None, last_0: int | None,
                            last_1: int | None, last_2: int | None):
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

            # Prevent Vidcomic 2 from reappearing after being collected the first time on Heat Street
            if (index == 2
                and self.planet == RAC3REGION.ANNIHILATION_NATION
                and self.is_location_checked(RAC3_LOCATION_DATA_TABLE[RAC3LOCATION.NATION_HEAT_STREET].AP_CODE)
                and self.pause_state_value != RAC3PAUSESTATE.PAUSED
                and comic.status == 0):
                 self._write8(addr, 1)
                 continue

            unlock_delay_count = 1
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
                            self._write8(status + 4, 0)
                            self._write16(RAC3STATUS.BLACK_SCREEN_2, 0)
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
                if "Jackpot" in name:
                    self.enqueue_notification(
                        f"{RAC3TEXTFORMATSTRING.WHITE}Jackpot x{2 ** self.bolt_and_xp_multiplier_value} "
                        f"{RAC3TEXTFORMATSTRING.NORMAL}effect has worn off.")
                else:
                    self.enqueue_notification(
                        f"{name}{RAC3TEXTFORMATSTRING.WHITE} effect has worn off.",
                        RAC3BOXTHEME.WARNING)
                match _name:
                    case RAC3ITEM.LOCK_TRAP:  # Special case for lock trap
                        # Clear when timer ends directly rather than from the trap cleanup loop below
                        # Todo: Check for arena mission
                        self._write8(RAC3STATUS.WEAPON_LOCK, 0)
                    case RAC3ITEM.JACKPOT:
                        self.bolt_and_xp_multiplier_value -= 1
                    case RAC3ITEM.MIRROR_TRAP:
                        self._write8(RAC3STATUS.MIRROR_UNIVERSE, 0)
                    case RAC3ITEM.BLACK_SCREEN_TRAP:
                        blackscreen_orig_value = VERSION_TO_BLACK_SCREEN_ORIGINAL_VALUE.get(self.current_game, 0x8C)
                        self._write16(RAC3STATUS.BLACK_SCREEN, blackscreen_orig_value)
                        self._write16(RAC3STATUS.BLACK_SCREEN_2, blackscreen_orig_value)
                        self._write8(RAC3STATUS.BLACK_SCREEN + 4, 1)
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
        """
        Synchronize weapon experience and level with the player's item collection and vendor state.

        - If progressive weapons are enabled, set each weapon's level and XP threshold based on the number of collected upgrades.
        - If the player is in a weapon vendor and not hovering over ammo, force the vendor slot weapon to level 1.
        - For the RY3N0 weapon, cap the level at 4 if the ryno flag is set.
        - If progressive weapons are not enabled, restore weapon level based on XP, unless in a vendor and not hovering over ammo, in which case set to base level.
        - Handles both progressive and non-progressive weapon logic, including syncing XP and level addresses in memory.
        """
        # TODO: Track weapon EXP
        if self.options.progressive_weapons:
            for weapon_name in non_prog_weapon_data.keys():
                target_level = self.UnlockItem[weapon_name].status
                if not target_level:
                    continue
                if target_level > 5: # TODO: change limit to 8 if NG+ weapons are added
                    target_level = 5
                if self.vendor_type == RAC3VENDORTYPE.WEAPON:
                    cursor_pos = self._read32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.CURSOR_OFFSET))
                    slot_data = self.read_vendor_slot_data(RAC3VENDORTYPE.WEAPON, cursor_pos)
                    if slot_data.item_id.value == RAC3_ITEM_DATA_TABLE[weapon_name].ID and not self.hovering_over_ammo():
                        target_level = 1
                if self.ryno and weapon_name == RAC3ITEM.RY3N0 and target_level > 4:
                    target_level = 4
                #logger.debug(f"weapon: {weapon_name}, target: {target_level}")
                target_id = UPGRADE_DICT[weapon_name][target_level - 1]
                target_name = ITEM_NAME_FROM_ID[target_id]
                target_xp = RAC3_ITEM_DATA_TABLE[target_name].XP_THRESHOLD
                #logger.debug(f"{target_name}, id: {target_id}, xp:{target_xp}")
                self._write32(non_prog_weapon_data[weapon_name].XP_ADDRESS, target_xp)
                self._write8(non_prog_weapon_data[weapon_name].LEVEL_ADDRESS, target_id)
        else:
            for weapon_name in non_prog_weapon_data.keys():
                if not self.UnlockItem[weapon_name].status:
                    continue
                if self.vendor_type == RAC3VENDORTYPE.WEAPON:
                    cursor_pos = self._read32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.CURSOR_OFFSET))
                    slot_data = self.read_vendor_slot_data(RAC3VENDORTYPE.WEAPON, cursor_pos)
                    if slot_data.item_id.value == RAC3_ITEM_DATA_TABLE[weapon_name].ID and not self.hovering_over_ammo():
                        self._write8(non_prog_weapon_data[weapon_name].LEVEL_ADDRESS, RAC3_ITEM_DATA_TABLE[weapon_name].ID)
                    else:
                        restore_id = UPGRADE_DICT[weapon_name][self.weapon_level_from_xp(weapon_name) - 1]
                        self._write8(non_prog_weapon_data[weapon_name].LEVEL_ADDRESS, restore_id)

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
        self._write8(RAC3STATUS.JACKPOT, self.bolt_and_xp_multiplier_value)

    def cheat_cycler(self):
        """Handles unlocking cheats such as the lightsaber wrench cheat"""
        for name in cheat_data.keys():
            addr = cheat_data[name].UNLOCK_ADDRESS
            if self.UnlockItem[name].status:
                if self.UnlockItem[name].unlock_delay:
                    self._write8(addr, 1)
                    self.UnlockItem[name].unlock_delay = 0
                else:
                    self.UnlockItem[name].unlock_delay += 1

    def safe_patch_instruction(self, instruction_address: int, restore: bool = False):
        """Safely apply or restore an instruction patch if current opcode matches the expected source opcode."""
        original = ORIGINAL_INSTRUCTIONS.get(instruction_address)
        patched = PATCHED_INSTRUCTIONS.get(instruction_address)
        if original is None or patched is None:
            return

        # Determine source and target opcodes based on whether we are restoring or patching
        source = patched if restore else original
        target = original if restore else patched
        current = self._read32(instruction_address)
        if current == source:
            self._write32(instruction_address, target)

    def get_planet_patch_instructions(self) -> list[int]:
        """Return all patch instructions associated with the current planet and game version."""
        game_version = self.current_game
        if game_version == RAC3VERSION.US_GH_ID:
            game_version = RAC3VERSION.US_ID  # US and US GH versions have the same instruction offsets
        return [
            instruction for instruction, planet in PATCH_INSTRUCTION_TO_PLANET.items()
            if planet == self.planet
            and (PATCH_INSTRUCTION_TO_GAME_IDS[instruction] is None
                 or game_version == PATCH_INSTRUCTION_TO_GAME_IDS[instruction])]

    def patch_cycler(self):
        """Apply runtime instruction patches based on current planet."""
        planet_patches = self.get_planet_patch_instructions()
        if not planet_patches:
            return

        if self.planet == RAC3REGION.ANNIHILATION_NATION:
            # One HP challenge patches for Ratchet to prevent automatically losing One Hit Wonder type challenges.
            # Sadly doesnt fix Flee Flawlessly skill point.
            character = self.player_type
            if character == RAC3PLAYERTYPE.TYHRRANOID:
                character = RAC3PLAYERTYPE.RATCHET

            # Apply patches if one HP challenge is enabled for Ratchet.
            if self.one_hp_challenge.get(character, False) and character == RAC3PLAYERTYPE.RATCHET:
                for instruction in planet_patches:
                    self.safe_patch_instruction(instruction)
            # Restore original instructions if one HP challenge is not enabled for Ratchet.
            elif not self.one_hp_challenge.get(character, False):
                for instruction in planet_patches:
                    self.safe_patch_instruction(instruction, restore=True)
            return

        # Apply all non-conditional patches for the current planet.
        for instruction in planet_patches:
            self.safe_patch_instruction(instruction)

    def get_active_patches(self) -> list[int]:
        """Return a list of currently active patch addresses based on the current planet."""
        return [
            instruction for instruction in self.get_planet_patch_instructions()
            if self._read32(instruction) == PATCHED_INSTRUCTIONS[instruction]]

    def get_failed_patches(self) -> list[int]:
        """Return patch addresses whose opcode is neither the original nor patched value."""
        return [
            instruction for instruction in self.get_planet_patch_instructions()
            if self._read32(instruction) not in {
                ORIGINAL_INSTRUCTIONS[instruction],
                PATCHED_INSTRUCTIONS[instruction],
            }]

    def overflow_fix(self):
        """Detect any integer overflows and reset the value"""
        if self.nanotech_exp > 0x7FFFFFFF:
            self._write32(RAC3STATUS.NANOTECH_EXP, 0)
            self.enqueue_notification("Negative Nanotech EXP detected! Resetting EXP to 0", RAC3BOXTHEME.WARNING)
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
        if self.current_game == RAC3VERSION.EU_ID:
            table_start = 0x01D2AAC0
        moby_offset = 0
        current_id = 0
        for traversal in range(1, 10001):
            if current_id == target_moby_id:
                # once vendor has been found, save address
                pda_vendor_addr = table_start + moby_offset
                logger.debug(f"PDA Vendor found at address: {hex(pda_vendor_addr)} after {traversal} traversals")
                return pda_vendor_addr
            next_ptr = self._read32(table_start + 0x28 + moby_offset)
            if next_ptr == 0:  # Null pointer found
                logger.debug(f"PDA Vendor not found after {traversal} traversals, reached null pointer")
                return 0
            moby_offset = next_ptr - table_start
            if moby_offset < 0:
                logger.debug(f"PDA Vendor not found after {traversal} traversals, invalid offset detected")
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
            logger.debug(f"Ratchet has PDA and PDA location unchecked, distance to PDA Vendor: {distance:.2f}")
            if distance < 12.0:
                logger.debug(f"Ratchet is close to PDA Vendor (Distance: {distance:.2f}), resetting vendor")
                self.reset_pda_vendor()

    def reset_pda_vendor(self):
        """Reset PDA Vendor to initial state to allow repurchasing the PDA"""
        if self.pda_vendor == 0:
            logger.error("PDA Vendor not found, cannot reset")
            return
        self._write8(self.pda_vendor + 0x7C, 1)  # Put PDA back in vendor
        self._write8(self.pda_vendor + 0x94, 0)  # Set bought flag to 0
        self._write8(self.pda_vendor + 0x20, 1)  # Reset interaction state

    def enqueue_notification(self,
                             message_or_notification: str | RAC3NOTIFICATION,
                             theme: int = RAC3BOXTHEME.DEFAULT,
                             duration: float = 3.0) -> None:
        """Append a notification to the queue from a message or pre-built RAC3NOTIFICATION."""
        if isinstance(message_or_notification, RAC3NOTIFICATION):
            notification = message_or_notification
        else:
            notification = RAC3NOTIFICATION(message_or_notification, theme, duration)
        self.notification_queue.append(notification)

    def dequeue_notifications(self, count: int = 1) -> None:
        """Pop up to `count` notifications from the front of the queue."""
        for _ in range(max(0, count)):
            if not self.notification_queue:
                break
            self.notification_queue.pop(0)

    def notification_cycler(self):
        """Handle the current displayed pop-up message notification, and message queue"""
        current_time = time.time()
        tyhrranoid_game = self.player_type == RAC3PLAYERTYPE.TYHRRANOID and self.action == RAC3PLAYERACTION.TYHRRANOID_MINIGAME
        paused = ((self.pause_state 
                   and self.pause_state_value != RAC3PAUSESTATE.QUICK_SELECT) 
                   or (current_time - self.last_in_ship_time) < 1.25 
                   or (current_time - self.last_in_vendor_time) < 0.25)
        self._write32(RAC3MESSAGEBOX.HIDDEN_AND_PAUSED,
                      int(self.inside_hacker_puzzle or paused))
        if self.notification_queue:
            if not self.notification_time:
                self.notification_time = current_time + self.notification_queue[0].duration
            if tyhrranoid_game or paused:
                if self.notification_paused_remaining:
                    # Pause the notification timer
                    self.notification_time = current_time + self.notification_paused_remaining
                else:
                    self.notification_time = current_time + self.notification_queue[0].duration
                return
            if self.notification_time < current_time and not self.message_display:
                # Pop the number of messages that were displayed last cycle
                next_duration = self.notification_queue[0].duration
                self.dequeue_notifications(self.notification_merge_count)
                self.write_messagebox_theme()
                logger.debug(f"notification queue: {len(self.notification_queue)}")
                if self.notification_queue:
                    next_duration = self.notification_queue[0].duration
                self.notification_time = current_time + next_duration
            if self.notification_queue:
                # Merge up to 3 notifications of the same theme, but do not exceed 235 chars
                merged_notification = self.notification_queue[0]
                merged_message = merged_notification.message
                theme = merged_notification.theme
                merge_count = 1
                total_length = len(merged_message)
                for i in range(1, min(3, len(self.notification_queue))):
                    next_notification = self.notification_queue[i]
                    next_message = next_notification.message
                    next_theme = next_notification.theme
                    # +2 for the '\n' separator
                    add_length = 2 + len(next_message)
                    if next_theme == theme and (total_length + add_length) <= 235:
                        merged_message += "\n" + next_message
                        total_length += add_length
                        merge_count += 1
                    else:
                        break
                self.notification_merge_count = merge_count
                msg_list, longest_line_length = self.format_textbox_string(merged_message)
                if not self.message_display:
                    if self.notification_time < current_time:
                        self.notification_time = current_time + merged_notification.duration
                    display_time = int((self.notification_time - current_time) * 120)
                    self.messagebox(msg_list, longest_line_length, theme, display_time)
                else:
                    write_message = b""
                    for line in msg_list:
                        write_message += line
                    read_message = self._read_bytes(RAC3MESSAGEBOX.MESSAGE, len(write_message))
                    if read_message != write_message:
                        # Give the player a bit more time to read the new appended line in case it was about to
                        # expire
                        if self.notification_time - current_time < 1.5:
                            self.notification_time = current_time + 1.5
                        display_time = int((self.notification_time - current_time) * 120)
                        # A lot of messages can cause this value to go negative and if so, set a minimum display
                        # time
                        if display_time < 0:
                            self.notification_time = current_time + 1
                            display_time = int((self.notification_time - current_time) * 120)
                        self.messagebox(msg_list, longest_line_length, theme, display_time)
                        logger.debug("Warning: Incorrect Display message detected")
                        logger.debug(f"Message: {merged_message}")
                        logger.debug(f"{read_message}")
                        logger.debug(f"{write_message}")
                    self.notification_paused_remaining = max(0, self.notification_time - current_time)
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

    def format_textbox_string(self, msg: str) -> tuple[list[bytes], int]:
        """Process a full message into game insertable bytes, for use with in game pop-ups"""
        # Split message on \n to handle newlines
        lines = msg.split("\n")
        # Write each line to memory, update string pointers
        longest_line_length = 0
        message_list: list[bytes] = []
        for _idx, line in enumerate(lines):
            # Convert to bytes, add null terminator
            line_bytes, line_expected_length = self.format_color_string(line)
            line_bytes += b"\x00"
            message_list.append(line_bytes)
            if line_expected_length > longest_line_length:
                longest_line_length = line_expected_length
        return message_list, longest_line_length

    @staticmethod
    def format_color_string(msg: str) -> tuple[bytes, int]:
        """Converts a message string with color formatting to game insertable bytes with color formatting"""
        result = bytearray()
        i = 0
        expected_length = 0
        while i < len(msg):
            matched = False
            for code, byte in FORMAT_NAME_TO_BYTE.items():
                if msg.startswith(code, i):
                    # Insert the color code byte (as a single byte)
                    if isinstance(byte, str):
                        byte = ord(byte)
                    expected_length += TEXT_BYTE_TO_EXPECTED_WIDTH.get(byte, 7)
                    result.append(byte)
                    i += len(code)
                    matched = True
                    break
            if not matched:
                # Insert the ASCII value of the character
                msg_ordinal = ord(msg[i])
                if msg_ordinal < 0 or msg_ordinal > 256:
                    # Replace unsupported characters with a question mark
                    msg_ordinal = ord("?")
                result.append(msg_ordinal)
                expected_length += TEXT_BYTE_TO_EXPECTED_WIDTH.get(msg_ordinal, 7)
                i += 1
        return bytes(result), expected_length

    def messagebox(self,
                   msg_list: list[bytes],
                   longest_line_length: int,
                   box_theme: int = RAC3BOXTHEME.DEFAULT,
                   _time: int = 0x168) -> None:
        """Update the contents of the current pop-up message"""
        if _time < 0:
            _time = 0
        # real overflow cap is actually about 248, but we don't need that long messages
        curr_addr = RAC3MESSAGEBOX.MESSAGE
        msg_bytes = b""
        for idx, line in enumerate(msg_list):
            msg_bytes += line
            # self._write_bytes(curr_addr, line)
            # Write pointer to this line at pointer_addr + 4*idx
            self._write32(RAC3MESSAGEBOX.TEXT_POINTER + 4 * idx, curr_addr)
            # Move to next address after this string
            curr_addr += len(line)
        self._write32(RAC3MESSAGEBOX.NUM_LINES, len(msg_list))
        width = longest_line_length
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

    def print_all_vendor_items(self):
        """Print all items sold by the current planet's vendor to the log, including all relevant properties"""
        vendor_type = self.vendor_type
        if vendor_type is None:
            logger.error("Vendor type is None, cannot print vendor items. This command should only be used when in a vendor menu.")
            return
        num_slots = self._read32(RAC3VENDOR.get_vendor_property_address(self.planet, RAC3VENDOR.SLOT_COUNT_OFFSET))
        logger.info(f"{vendor_type} has {num_slots} slots")
        inventory = [self.read_vendor_slot_data(vendor_type, slot) for slot in range(num_slots)]
        for slot, slot_data in enumerate(inventory):
            match vendor_type:
                case RAC3VENDORTYPE.WEAPON:
                    item_name = ITEM_NAME_FROM_ID.get(
                        slot_data.item_id.value,
                        f"Unknown Item ID {slot_data.item_id.value}"
                    )
                case RAC3VENDORTYPE.ARMOR:
                    item_name = ITEM_NAME_FROM_ID.get(
                        slot_data.armor_level.value + 0xF5,
                        f"Unknown Armor Level {slot_data.armor_level.value}"
                    )
                case RAC3VENDORTYPE.SHIP:
                    item_name = self._read_string(slot_data.item_name_ptr.value, 64)
                case _:
                    item_name = "???"
            logger.info(
                f"Vendor Slot {slot}: "
                f"Item Name: {item_name}, "
                "\n" + "\n".join(f"{prop.name}: {prop.read_property()}" for prop in slot_data.get_data()) + "\n"
            )

    def dump_info(self, slot_data: dict[str, Any]):
        """Dumps info about the current state of the client"""
        logger.info(f"Collected Items: {self.UnlockItem}")
        count = 0
        for name in SHIP_SLOTS:
            logger.info(f"Planet{count}: {PLANET_NAME_FROM_ID[self._read8(RAC3_REGION_DATA_TABLE[name].SLOT_ADDRESS)]}")
            count += 1
        logger.info(f"Slot Data: {slot_data}")
        logger.info(f"Archipelago Version: {__version__}")
        logger.info(f"AP World Version: {RAC3OPTION.VERSION_NUMBER}")
        logger.info(f'Game Version: {GAME_ID_TO_VERSION.get(self.current_game, "Unknown")} ({self.current_game})')
        logger.info(f"Current planet Tracked: {self.planet}")
        if self.cycle_times:
            cycle_min = min(self.cycle_times)
            cycle_avg = sum(self.cycle_times) / len(self.cycle_times)
            cycle_max = max(self.cycle_times)
            logger.info(
                f"Update cycle execution time last {len(self.cycle_times)} cycles: "
                f"min {cycle_min:.4f}s / avg {cycle_avg:.4f}s / max {cycle_max:.4f}s"
            )
        else:
            logger.info("Update cycle execution time: no samples collected yet")
        logger.info(f"Sewer Crystals Inventory: {self._read8(RAC3STATUS.CRYSTALS_CURRENT)}")
        logger.info(f"Sewer Crystals Traded: {self._read8(RAC3STATUS.CRYSTALS_TRADED)}")
        logger.info(f"Ship Slot Limit: {self.ship_slot_limit}")
        if self.planet != RAC3REGION.QWARKS_HIDEOUT:
            pda_vendor_str = "N/A"
        else:
            pda_vendor_str = hex(self.pda_vendor) if self.pda_vendor else "Not Found"
        logger.info(f"PDA Vendor Address: {pda_vendor_str}")
        logger.info(f"Meet Sasha Bridge: {RAC3LOCATION.PHOENIX_MEET_SASHA in self.checked_locations}")
        logger.info(f"Visited Planets: {[planet for planet in PLANET_NAME_FROM_ID.values() if planet in self.visited_planets and not (planet == RAC3REGION.HOLOSTAR_STUDIOS_CLANK and self.options.holostar_skip)]}")
        logger.info(f"Active Patches: {[PATCH_INSTRUCTION_TO_NAME[patch] for patch in self.get_active_patches()]}")
        failed_patches = self.get_failed_patches()
        logger.info(f"Failed Patches: {[PATCH_INSTRUCTION_TO_NAME[patch] for patch in failed_patches]}")
        if len(failed_patches) > 0:
            logger.warning("Failed patches detected: instruction opcodes were neither source nor patched values. "
                           "This may indicate a corrupted ISO or an unsupported game version. "
                           "Please report this to the developers with the above information.")
