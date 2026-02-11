"""This module provides an interface for connecting to a pcsx2 game"""

from struct import unpack
from typing import Optional

from CommonClient import logger
from worlds.rac3.constants.version import RAC3VERSION
from worlds.rac3.pcsx2_interface.pine import Pine


class GameInterface:
    """Base class for connecting with a pcsx2 game"""
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
        """Remove connection to PCSX Emulator"""
        self.pcsx2_interface.disconnect()
        self.current_game = None
        logger.info("Disconnected from PCSX2 Emulator")

    def verify_game_version(self) -> bool:
        """Verify that the current game loaded in the PCSX connection has a valid game ID for Ratchet and Clank 3"""
        logger.debug('Start Game Verification')
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
                case RAC3VERSION.US_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: US release')
                case RAC3VERSION.US_GH_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: US Greatest Hits release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case RAC3VERSION.JP_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: Japanese release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case RAC3VERSION.JP_TB_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: Japanese The Best release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case RAC3VERSION.KO_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: Korean release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case RAC3VERSION.CH_ID:
                    self.current_game = game_id
                    logger.info(f'Version Detected: Chinese release')
                    logger.warning('WARNING: Game version untested, please inform apworld devs of any '
                                   'inconsistencies found')
                case RAC3VERSION.EU_ID:
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
        """Safe connection test"""
        try:
            if self.pcsx2_interface.is_connected():
                return self.verify_game_version()
            else:
                return False
        except RuntimeError:
            return False
