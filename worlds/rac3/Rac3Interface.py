import random
import struct
from enum import IntEnum
from logging import Logger
from typing import Dict, Optional

from . import Items, Locations
from .pcsx2_interface.pine import Pine
from .Rac3Addresses import ADDRESSES, CHECK_TYPE, COMPARE_TYPE, LOCATIONS


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
        return struct.unpack("f", self.pcsx2_interface.read_bytes(address, 4))[0]

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
            self.logger.info("Connected to PCSX2 Emulator")
        try:
            game_id = self.pcsx2_interface.get_game_id()
            # The first read of the address will be null if the client is faster than the emulator
            self.current_game = None
            if game_id in ADDRESSES.keys():
                self.current_game = game_id
                self.addresses = ADDRESSES[game_id]
            if self.current_game is None and self.game_id_error != game_id and game_id != b'\x00\x00\x00\x00\x00\x00':
                self.logger.warning(f"Connected to the wrong game ({game_id})")
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


class Rac3Interface(GameInterface):
    ########################################
    # Mandatory functions                  #
    ########################################

    UnlockWeapons = None
    UnlockGadgets = None
    UnlockVidComics = None
    UnlockPlanets = None
    UnlockArmor = None
    weaponLevelLockFlag = None
    boltAndXPMultiplier = None
    boltAndXPMultiplierValue = None

    # Called at once when client started
    def init(self):
        self.init_variables()

    def file_load(self, locations):
        self.remove_all_weapons()
        self.remove_all_gadgets()
        self.remove_all_planets()

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
        addr = self.addresses["boltXPMultiplier"]
        addr = self.address_convert(addr)
        self._write8(addr, self.boltAndXPMultiplierValue)
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
        if self._read32(self.addresses["MainMenu"]):
            return True
        return False

    def proc_option(self, slot_data):
        self.logger.info(f"{slot_data}")
        self.boltAndXPMultiplier = slot_data["options"]["bolt_and_xp_multiplier"]
        self.weaponLevelLockFlag = slot_data["options"]["enable_progressive_weapons"]

    def map_switch(self):
        planet = self._read8(self.addresses["CurrentPlanet"])
        if planet > 55 or not self._read8(self.addresses["MapCheck"]):
            planet = 0
        elif planet > 29:
            planet = 3
        return list(self.addresses["PlanetValues"])[planet]

    def tyhrranosis_fix(self):
        self._write8(self.addresses["Robonoids active"], 0)

    def item_received(self, item_code, processed_items_count=0):
        # self.logger.info(f"{item_code}")
        if list(Items.weapon_items.values())[0].ap_code <= item_code <= list(Items.weapon_items.values())[-1].ap_code:
            self.received_weapon(item_code)
        elif list(Items.progressive_weapons.values())[0].ap_code <= item_code <= \
            list(Items.progressive_weapons.values())[-1].ap_code:
            self.received_weapon_progressive(item_code)
        elif list(Items.gadget_items.values())[0].ap_code <= item_code <= list(Items.gadget_items.values())[-1].ap_code:
            self.received_gadget(item_code)
        elif list(Items.post_planets.values())[0].ap_code <= item_code <= list(Items.post_planets.values())[-1].ap_code:
            self.received_planet(item_code)
        elif list(Items.progressive_vidcomics.values())[0].ap_code <= item_code <= \
            list(Items.progressive_vidcomics.values())[-1].ap_code:
            self.received_vidcomic()
        elif list(Items.progressive_armor.values())[0].ap_code <= item_code <= \
            list(Items.progressive_armor.values())[-1].ap_code:
            self.received_armor()
        elif processed_items_count >= 0:  # To avoid duplicated items sending when reconnection, First attempt is
            # skipped.
            self.received_others(item_code)

    def is_location_checked(self, ap_code):
        # Find the location
        target_location = next((loc for loc in LOCATIONS if loc["Id"] == ap_code), None)
        if not target_location:
            return False  # not found

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
        self.UnlockWeapons = {name: {"status": 0, "unlockDelay": 0} for name in self.addresses["Weapons"].keys()}
        self.UnlockGadgets = {name: {"status": 0, "unlockDelay": 0} for name in self.addresses["Gadgets"].keys()}
        self.UnlockVidComics = {"status": 0, "unlockDelay": 0}
        self.UnlockPlanets = {name: {"status": 0, "unlockDelay": 0} for name in self.addresses["ShipPlanets"].keys()}
        self.UnlockArmor = {"status": 0, "unlockDelay": 0}

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
    def remove_all_weapons(self):
        for dict_data in self.addresses["Weapons"].values():
            addr = dict_data["unlockAddress"]
            addr = self.address_convert(addr)
            self._write8(addr, 0)
            self._write8(dict_data["ammoAddress"], dict_data["lv1Ammo"])

    def remove_all_gadgets(self):
        for dict_data in self.addresses["Gadgets"].values():
            addr = dict_data["unlockAddress"]
            addr = self.address_convert(addr)
            self._write8(addr, 0)
        for dict_data in self.addresses["VidComics"].values():
            addr = dict_data["unlockAddress"]
            addr = self.address_convert(addr)
            self._write8(addr, 0)

    def remove_all_planets(self):
        for addr in self.addresses["PlanetSlots"]:
            addr = self.address_convert(addr)
            self._write32(addr, 0)
        # Default Unlocked planets
        self.UnlockPlanets["Veldin"]["status"] = 1
        # self.UnlockPlanets["Florana"]["status"] = 1
        # self.UnlockPlanets["Starship Phoenix"]["status"] = 1
        # self.UnlockPlanets["Museum"]["status"] = 1

    # Logic Fixes
    def logic_fixes(self):
        current_planet_addr = self.addresses["CurrentPlanet"]
        current_planet_addr = self.address_convert(current_planet_addr)
        current_planet = self._read8(current_planet_addr)

        # Fix can't play Qwark VidComics in some case which first event is skipped
        addr = self.addresses["Missions"]["Take Qwark to Cage"]
        addr = self.address_convert(addr)
        if current_planet == self.addresses["PlanetValues"]["Starship Phoenix"]:
            self._write8(addr, 1)

    # interval update function: Check unlock/lock status of items
    def weapon_cycler(self):
        # self.logger.debug("---------WeaponCycler Start---------")
        for name, dict_data in self.UnlockWeapons.items():
            unlock_status = dict_data["status"]
            addr = self.addresses["Weapons"][name]["unlockAddress"]
            addr = self.address_convert(addr)

            # self.logger.info(f"[WeaponCycler] {name}: status={unlock_status}, delay={self.UnlockWeapons[name][
            # 'unlockDelay']}, addr={hex(addr)}")
            if unlock_status == 0:
                self.UnlockWeapons[name]["unlockDelay"] += 1
                if dict_data["unlockDelay"] > 1:
                    self._write8(addr, 0)
                    self.UnlockWeapons[name]["unlockDelay"] = 0
                # self.logger.debug(f"{name} locked")
            else:
                self._write8(addr, 1)
        #         self.logger.debug(f"{name} is available")
        # self.logger.debug("---------WeaponCycler End---------")

        addr = self.addresses["CurrentEquipped"]
        addr = self.address_convert(addr)
        current_equipped = self._read8(addr)
        for weapon_name, weapon_data in self.addresses["Weapons"].items():
            if current_equipped == weapon_data["id"] and self.UnlockWeapons[weapon_name][
                "status"] == 0:  # Not unlocked, but set case
                self._write8(addr, 9)  # 9 is omniwrench

    def gadget_cycler(self):
        # self.logger.debug("---------GadgetCycler Start---------")
        for name, dict_data in self.UnlockGadgets.items():
            unlock_status = dict_data["status"]
            addr = self.addresses["Gadgets"][name]["unlockAddress"]
            addr = self.address_convert(addr)

            if unlock_status == 0:
                self.UnlockGadgets[name]["unlockDelay"] += 1
                if dict_data["unlockDelay"] > 1:
                    val = self._read8(addr)
                    self._write8(addr, (val & 0xfe))
                    self.UnlockGadgets[name]["unlockDelay"] = 0
                # self.logger.debug(f"{name} locked")
            else:
                # Get Gadget in event
                if name in ["Hacker", "Hypershot", "Refractor", "Tyhrra-Guise", "Gravity-Boots", "Map-O-Matic",
                            "Warp Pad"]:
                    self._write8(addr, 2)  # 0x2=0b0010
                # Get Gadget in field
                else:
                    self._write8(addr, 1)  # 0x1=0b0001
        #         self.logger.debug(f"{name} is available")
        # self.logger.debug("---------GadgetCycler End---------")

    def planet_cycler(self):
        # self.logger.debug("---------PlanetCycler Start---------")
        address_list: list[int] = self.addresses["PlanetSlots"]
        planet_names: list[str] = list(self.addresses["ShipPlanets"].keys())
        planet_ids: list[int] = list(self.addresses["ShipPlanets"].values())

        for i in range(len(address_list)):
            if self.UnlockPlanets[planet_names[i]]["status"]:
                if self.UnlockPlanets[planet_names[i]]["unlockDelay"]:
                    self._write8(address_list[i], planet_ids[i])
                else:
                    self.UnlockPlanets[planet_names[i]]["unlockDelay"] += 1
            else:
                self._write8(address_list[i], 0)

            # For avoiding Deadlock, Holostar is locked until Hacker and HyperShot is unlocked,
            if planet_names[i] == "Holostar Studios":
                if self.UnlockGadgets["Hacker"]["status"] == 0 or self.UnlockGadgets["Hypershot"]["status"] == 0:
                    self._write8(address_list[i], 0)
            if planet_names[i] == "Qwarks Hideout":
                if self.UnlockGadgets["Refractor"]["status"] == 0:
                    self._write8(address_list[i], 0)

    def vidcomic_cycler(self):
        # self.logger.debug("---------VidComicCycler Start---------")
        unlock_status = self.UnlockVidComics["status"]
        for name in range(5):
            addr = self.addresses["VidComics"][f'Qwark VidComic {name + 1}']["unlockAddress"]
            addr = self.address_convert(addr)
            read_value = self._read8(addr)
            if name + 1 > unlock_status:
                if read_value == 1:
                    self._write8(addr, 0)  # Disable Vidcomics not unlocked yet
                break
            if read_value == 0 and name + 1 <= unlock_status:
                unlock_delay_count = 1
                if name == 2:
                    unlock_delay_count = 30  # WA for Annihilation Nation Proceeding
                self.UnlockVidComics["unlockDelay"] += 1
                if self.UnlockVidComics["unlockDelay"] > unlock_delay_count:
                    self._write8(addr, 1)
                    self.UnlockVidComics["unlockDelay"] = 0
                    # self.logger.debug(f"Qwark VidComic {name + 1} is now available")
                break
        #     else:
        #         is_available = self._read8(addr) == 1
        #         self.logger.debug(f"Qwark VidComic {name + 1} is {'available' if is_available else 'locked'}")
        #
        # self.logger.debug("---------VidComicCycler End---------")

    def armor_cycler(self):
        # self.logger.debug("---------ArmorCycler Start---------")
        addr = self.addresses["ArmorVersion"]
        addr = self.address_convert(addr)
        current_armor_value = self._read8(addr)

        if current_armor_value != self.UnlockArmor["status"]:
            self.UnlockArmor["unlockDelay"] += 1
            if self.UnlockArmor["unlockDelay"] > 1:
                self._write8(addr, self.UnlockArmor["status"])
                self.UnlockArmor["unlockDelay"] = 0
        # self.logger.debug(f"Armor status: {self.UnlockArmor['status']}")
        # self.logger.debug("---------ArmorCycler End---------")

    def verify_quick_select_and_last_used(self):
        _slots = self.addresses["QuickSelectSlots"] + self.addresses["LastUsed"]
        for addr in _slots:
            addr = self.address_convert(addr)
            slot_val = self._read8(addr)
            for weapon_name, weapon_data in self.addresses["Weapons"].items():
                if slot_val == weapon_data["id"] and self.UnlockWeapons[weapon_name]["status"] == 0:
                    # Not unlocked, but set case
                    self._write8(addr, 0)
                    continue
            for gadget_name, gadget_data in self.addresses["Gadgets"].items():
                if slot_val == gadget_data["id"] and self.UnlockGadgets[gadget_name]["status"] == 0:
                    # Not unlocked, but set case
                    self._write8(addr, 0)
                    continue

    def weapon_exp_cycler(self):
        weapon_names = [name for name, data in self.UnlockWeapons.items()]
        for weapon_name in weapon_names:
            # Get weapon information
            # target_weapon_data = [data for data in LOCATIONS if f"{weapon_name}: V" in data["Name"]]
            # exp_list = ["0"] + [data["CheckValue"] for data in target_weapon_data]  # Exp for v1(=0) + Exp for v2~v5
            # addr = target_weapon_data[0]["Address"]
            # addr = self.address_convert(addr)

            # None of the above does anything

            # Check Current Weapon level and set Exp.
            correct_version = self.UnlockWeapons[weapon_name]["status"]  # 1 ~ 5
            if correct_version != 0:
                self.weapon_level_up(weapon_name, version=correct_version)

    # Equip the most recently collected weapon/gadget, update recent uses
    def update_equip(self, type, name):
        if self.addresses[type][name]["id"]:
            self._write8(self.addresses["LastUsed"][2], self._read8(self.addresses["LastUsed"][1]))
            self._write8(self.addresses["LastUsed"][1], self._read8(self.addresses["LastUsed"][0]))
            self._write8(self.addresses["LastUsed"][0], self.addresses[type][name]["id"])
            self._write8(self.addresses["HoldingWeapon"], self.addresses[type][name]["id"])
            for number in range(len(self.addresses["QuickSelectSlots"])):
                if not self._read8(self.addresses["QuickSelectSlots"][number]):
                    self._write8(self.addresses["QuickSelectSlots"][number], self.addresses[type][name]["id"])
                    break
            self.verify_quick_select_and_last_used()

    def received_weapon(self, ap_code):
        for name, item_data in Items.weapon_items.items():
            if item_data.ap_code == ap_code:
                self.UnlockWeapons[name]["status"] = 1
                self._write8(self.addresses["Weapons"][name]["ammoAddress"], self.addresses["Weapons"][name]["lv1Ammo"])
                self.update_equip("Weapons", name)
                return

    def received_weapon_progressive(self, ap_code):
        for name, data in Items.progressive_weapons.items():
            if data.ap_code == ap_code:
                weapon_name = name.replace("Progressive ", "")
                self.UnlockWeapons[weapon_name]["status"] += 1
                if self.UnlockWeapons[weapon_name]["status"] == 1:
                    self._write8(self.addresses["Weapons"][weapon_name]["ammoAddress"],
                                 self.addresses["Weapons"][weapon_name]["lv1Ammo"])
                    self.update_equip("Weapons", weapon_name)
                return

    def weapon_level_up(self, weapon_name, version=0):
        target_weapon_data = [data for data in LOCATIONS if f"{weapon_name}: V" in data["Name"]]
        exp_list = [0] + [data["CheckValue"] for data in target_weapon_data]  # Exp for v1~v5
        addr = target_weapon_data[0]["Address"]
        addr = self.address_convert(addr)
        if version == 0:
            current_exp = self._read32(addr)
            for target_exp in exp_list:
                if current_exp < target_exp:
                    self._write32(addr, target_exp)
                    break
        elif version <= 5:  # version = 1~5:
            self._write32(addr, exp_list[version - 1])

    def received_gadget(self, ap_code):
        for name, item_data in Items.gadget_items.items():
            if item_data.ap_code == ap_code:
                self.UnlockGadgets[name]["status"] = 1
                self.update_equip("Gadgets", name)

    def received_planet(self, ap_code):
        for name, item_data in Items.post_planets.items():
            if item_data.ap_code == ap_code:
                name = name.replace("Infobot: ", "")
                self.UnlockPlanets[name]["status"] = 1

    def received_vidcomic(self):
        self.UnlockVidComics["status"] += 1
        if self.UnlockVidComics["status"] > 5:
            self.UnlockVidComics["status"] = 5

    def received_armor(self):
        self.UnlockArmor["status"] += 1
        if self.UnlockArmor["status"] > 4:
            self.UnlockArmor["status"] = 4

    def received_others(self, ap_code):
        # Get Titanium Bolt
        if ap_code == Items.t_bolts["Titanium Bolt"].ap_code:
            pass  # Nothing to do

        if ap_code == Items.junk_items["Bolts"].ap_code:  # Random get bolts
            addr = self.addresses["Bolt"]
            addr = self.address_convert(addr)
            bolt = self._read32(addr)
            self._write32(addr, bolt + 1000 * random.randint(1, 100))

        if ap_code == Items.junk_items["Inferno Mode"].ap_code:  # Random get Inferno
            addr = self.addresses["InfernoTimer"]
            addr = self.address_convert(addr)
            timer = self._read32(addr)
            self._write32(addr, timer + 1000 + random.randint(1, 100))

        if ap_code == Items.junk_items["Jackpot Mode"].ap_code:  # Random get Jackpot
            addr = self.addresses["JackpotTimer"]
            addr = self.address_convert(addr)
            timer = self._read32(addr)
            self._write32(addr, timer + 1000 + random.randint(1, 100))
            # Activate Jackpot
            addr = self.addresses["JackpotActive"]
            addr = self.address_convert(addr)
            self._write8(addr, 1)

        # Little buggy, but it works in general.
        # ToDo Fix this function
        if ap_code == Items.junk_weapon_exp["Weapon EXP"].ap_code:  # Random Weapon Upgrade
            unlocked_weapon_names = [name for name, data in self.UnlockWeapons.items() if data["status"] == 1]
            # Avoid LevelMax weapon
            for weapon_name in unlocked_weapon_names:
                target_weapon_data = [data for data in LOCATIONS if f"{weapon_name}: V" in data["Name"]]
                # self.logger.info(f"target_weapon_data[{len(target_weapon_data)}]: {target_weapon_data}")
                if len(target_weapon_data) > 0:
                    exp_list = [data["CheckValue"] for data in target_weapon_data]  # Exp for v2~v5
                    addr = target_weapon_data[0]["Address"]
                    addr = self.address_convert(addr)
                    current_exp = self._read32(addr)
                    if current_exp >= exp_list[-1]:
                        unlocked_weapon_names.remove(weapon_name)

            if len(unlocked_weapon_names) > 0:
                weapon_num = random.randint(0, len(unlocked_weapon_names) - 1)
                weapon_name = unlocked_weapon_names[weapon_num]
                self.weapon_level_up(weapon_name)

    def dump_info(self, current_planet, slot_data):
        print(f'Weapons Tracker: {self.UnlockWeapons}')
        print(f'Gadgets Tracker: {self.UnlockGadgets}')
        print(f'VidComics Tracker: {self.UnlockVidComics}')
        print(f'Planets Tracker: {self.UnlockPlanets}')
        print(f'Armor Tracker: {self.UnlockArmor}')
        count = 0
        planet_lookup = list(self.addresses["PlanetValues"].keys())
        for addr in self.addresses["PlanetSlots"]:
            print(f'Planet{count}: {planet_lookup[self._read8(addr)]}')
            count += 1
        print(f'Current planet Tracked: {current_planet}')
        print(f'Slot Data: {slot_data}')

    def tracker_update(self):
        pass

    # Todo: Deathlink
    def alive(self):
        pass

    def kill_player(self):
        pass
