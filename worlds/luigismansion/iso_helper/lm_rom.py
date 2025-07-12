from worlds.Files import APPatchExtension, AutoPatchExtensionRegister, APAutoPatchInterface, APPlayerContainer, \
    APProcedurePatch
from settings import get_settings, Settings
from Utils import user_path

from hashlib import md5
from os import path as os_path
import yaml
from yaml import CDumper as Dumper
import logging
from sys import platform, path
from importlib import resources
import zipfile

logger = logging.getLogger()

RANDOMIZER_NAME = "Luigi's Mansion"
LM_USA_MD5 = 0x6e3d9ae0ed2fbd2f77fa1ca09a60c494

class InvalidCleanISOError(Exception):
    """
    Exception raised for when user has an issue with their provided Luigi's Mansion ISO.

    Attributes:
        message -- Explanation of the error
    """

    def __init__(self, message="Invalid Clean ISO provided"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidCleanISOError: {self.message}"

class LMPlayerContainer(APPlayerContainer):
    game = RANDOMIZER_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".aplm"

    def __init__(self, player_choices: dict, patch_path: str, base_path:str, player_name: str, server: str,
            player: int):
        self.output_data = player_choices
        self.file_path = base_path
        super().__init__(patch_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.aplm", yaml.dump(self.output_data, sort_keys=False, Dumper=Dumper))
        super().write_contents(opened_zipfile)

class LMUSAAPPatchInterface(APAutoPatchInterface):
    game = RANDOMIZER_NAME
    hash = LM_USA_MD5
    files: dict[str, bytes]
    patch_file_ending = ".aplm"
    result_file_ending = ".iso"
    patch_file = "patch.aplm"

    @classmethod
    def get_source_data(cls) -> bytes:
        return cls.get_base_rom_path().encode()

    @classmethod
    def get_file(cls, file: str) -> bytes:
        """ Retrieves a file from the patch container."""
        if file not in cls.files:
            cls.read(cls())
        return cls.files[file]

    @classmethod
    def patch(cls, target: str) -> None:
        cls.files = {}
        # Get the AP Path for the base ROM
        lm_clean_iso = cls.get_base_rom_path()
        logger.info("Provided Luigi's Mansion ISO Path was: " + lm_clean_iso)

        # Load the external dependencies based on OS
        logger.info("Loading required dependencies for Luigi's Mansion, including GClib...")
        is_linux = platform.startswith("linux")
        is_windows = platform in ("win32", "cygwin", "msys")
        lib_path = ""
        if not (is_linux or is_windows):
            raise RuntimeError(f"Your OS is not supported with this randomizer {platform}")
        if is_windows:
            lib_path = "lib-windows"
        elif is_linux:
            lib_path = "lib-linux"

        # Use importlib.resources to automatically make a temp directory that will get auto cleaned up after
        # the with block ends.
        with resources.as_file(resources.files(__name__).joinpath(lib_path)) as resource_lib_path:
            logger.info("Temp Resource Path: " + str(resource_lib_path))
            path.append(str(resource_lib_path))

            # Verify we have a clean rom of the game first
            cls.verify_base_rom(lm_clean_iso)

            # Use our randomize function to patch the file into an ISO.
            from ..LMGenerator import LuigisMansionRandomizer
            print(cls.patch_file)
            lm_out_data = cls.get_file(cls.patch_file)
            LuigisMansionRandomizer(lm_clean_iso, target, lm_out_data)


    @classmethod
    def get_base_rom_path(cls) -> str:
        options: Settings = get_settings()
        file_name = options["luigismansion_options"]["iso_file"]
        if not os_path.exists(file_name):
            file_name = user_path(file_name)
        return file_name

    @classmethod
    def verify_base_rom(cls, lm_rom_path: str):
        # Verifies we have a valid installation of Luigi's Mansion USA. There are some regional file differences.
        logger.info("Verifying if the provided ISO is a valid copy of Luigi's Mansion USA edition.")
        from gclib import fs_helpers as fs

        base_md5 = md5()
        with open(lm_rom_path, "rb") as f:
            while chunk := f.read(1024 * 1024):  # Read the file in chunks.
                base_md5.update(chunk)

            # Grab the Magic Code and Game_ID with the file still open
            magic = fs.try_read_str(f, 0, 4)
            game_id = fs.try_read_str(f, 0, 6)
            logger.info(f"Magic Code: {magic}")
            logger.info(f"LM Game ID: {game_id}")

        # Verify that the file has the right has first, as the wrong file could have been loaded.
        md5_conv = int(base_md5.hexdigest(), 16)
        if md5_conv != LM_USA_MD5:
            raise InvalidCleanISOError(f"Invalid vanilla {RANDOMIZER_NAME} ISO.\nYour ISO may be corrupted or your MD5 " +
                                       f"hashes do not match.\nCorrect ISO MD5 hash: {LM_USA_MD5:x}\nYour ISO's MD5 hash: {md5_conv}")

        # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
        # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
        if magic == "CISO":
            raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {RANDOMIZER_NAME} randomizer " +
                                       "only supports ISOs in ISO format.")
        if game_id != "GLME01":
            if game_id and game_id.startswith("GLM"):
                raise InvalidCleanISOError(f"Invalid version of {RANDOMIZER_NAME}. " +
                                           "Currently, only the North American version is supported by this randomizer.")
            else:
                raise InvalidCleanISOError("Invalid game given as the vanilla ISO. You must specify a " +
                                           f"{RANDOMIZER_NAME}'s ISO (North American version).")
        return