import shutil

from worlds.Files import APPatch, APPlayerContainer, AutoPatchRegister
from settings import get_settings, Settings
from NetUtils import convert_to_base_types
import Utils

from hashlib import md5
from typing import Any
import json, logging, sys, os, zipfile, tempfile

GAME_NAME = "Phantasy Star Online Episode I&II Plus"

PSO_MD5 = 0x36a7f90ad904975b745df9294a06baea

class InvalidCleanISOError(Exception):
    """
    This exception will be raised when the user has an issue with their PSO Rom.
    :param message: the explanation of the error
    """

    def __init__(self, message="Invalid Clean ISO provided"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidCleanISOError: {self.message}"

class PSOPlayerContainer(APPlayerContainer):
    game = GAME_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".appso"

    # Player options is the RANDOMIZED data based on the players options... not the options themselves.
    def __init__(self, player_options: dict, patch_path: str, player_name: str, player: int):
        self.output_data = player_options
        super().__init__(patch_path, player, player_name)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.appso", json.dumps(self.output_data, indent=4, default=convert_to_base_types))
        super().write_contents(opened_zipfile)

class PSOPatch(APPatch, metaclass=AutoPatchRegister):
    game = GAME_NAME
    hash = PSO_MD5
    patch_file_ending = ".appso"
    result_file_ending = ".iso"

    def __init__(self, *args: Any, **kwargs: Any):
        super(PSOPatch, self).__init__(*args, **kwargs)

    def __get_archive_name(self) -> str:
        if not (Utils.is_linux or Utils.is_windows):
            message = f"Your OS is not support with this Randomizer."
            logging.error(message)

            raise RuntimeError

        lib_path = ""
        if Utils.is_windows:
            lib_path = "lib-windows"
        elif Utils.is_linux:
            lib_path = "lib-linux"

        logging.info(f"Dependency archive name to use {lib_path}")
        return lib_path

    def __get_temp_folder_name(self) -> str:
        from helpers import CLIENT_VERSION
        temp_path = os.path.join(tempfile.gettempdir(), "phantasystar", CLIENT_VERSION, "libs")
        return temp_path

    def patch(self, appso_patch:str):
        #Gets the AP path for base ROM.
        pso_clean_iso = get_base_rom_path()
        logging.info("Provided PSO iso path: " + pso_clean_iso)

        base_path = os.path.splitext(appso_patch)[0]
        output_file = base_path + self.result_file_ending

        try:
            # Make sure we have the clean rom first
            self.verify_base_rom(pso_clean_iso, throw_on_missing_speedups=True)

            # Calls the PSOPatcher to patch the file into ISO
            from pso_patcher import PSOPatcher
            PSOPatcher(appso_patch)
        except ImportError:
            self.__get_remote_dependencies_and_create_iso(appso_patch, pso_clean_iso)
        return output_file

    def read_contents(self, appso_patch: str) -> dict[str, Any]:
        with zipfile.ZipFile(appso_patch, "r") as zf:
            with zf.open("archipelago.json", "r") as f:
                manifest = json.load(f)

        if manifest["compatible_version"] > self.version:
            raise Exception(f"File (version: {manifest['compatible_version']}) too new"
                            f"for this handler (version: {self.version}")
        return manifest

    @classmethod
    def verify_base_rom(cls, pso_rom_path: str, throw_on_missing_speedups: bool = False):
        # Double checks that we have a valid installation of Phantasy Star Online
        logging.info("Verifying if ISO is Phantasy Star Online Episode I & II Plus (USA).")
        logging.info("Checking gclib and speedups.")
        # Making sure speedups is available
        import pyfastyaz0yay0
        from gclib import fs_helpers as fs, yaz0_yay0
        logging.info("Using GClib from path: %s.", fs.__file__)
        logging.info("Using speedups from path: %s.", pyfastyaz0yay0.__file__)
        logging.info(sys.modules["gclib.yaz0_yay0"])

        if yaz0_yay0.PY_FAST_YAZ0_YAY0_INSTALLED:
            logging.info("Speedups detected.")
        else:
            logging.info("Python module paths: %s", sys.path)
            if throw_on_missing_speedups:
                logging.info("Speedups not detected, attempting to pull remote release.")
                raise ImportError("Cannot continue patching PSO due to missing libraries")
            logging.info("Continuing patching without speedups.")

        base_md5 = md5()
        with open(pso_rom_path, "rb") as f:
            while chunk := f.read(1024 * 1024): # - - -This reads the file in 1 MB chunks.
                base_md5.update(chunk)

            # This grabs the Game ID and the Code while the file is open.
            code = fs.try_read_str(f,0,4)
            game_id = fs.try_read_str(f,0,6)
            logging.info(f"Code: {code}")
            logging.info(f"PSO Game ID: {game_id}")

        # Double-checks the file is correct first.
        md5_conv = int(base_md5.hexdigest(), 16)
        if md5_conv != PSO_MD5:
            raise InvalidCleanISOError(f"Invalid vanilla {GAME_NAME} iso file – Verify your file is not corrupted")

        #Double-check the file has a correct iso format file extension
        if code in ("CISO", "RVZ"):
            raise InvalidCleanISOError(f"Invalid vanilla {GAME_NAME} iso file – Make sure your file is a .iso")

        else:
            raise InvalidCleanISOError("Invalid game given as vanilla PSO iso – verify you have the correct Phantasy Star Online Episode I & II Plus (USA) iso")

    def create_iso(self, temp_dir_path: str, patch_file_path: str, vanilla_iso_path: str):
        logging.info(f"Appending the following to sys path to get dependencies: {temp_dir_path}")
        sys.path.insert(0, temp_dir_path)

        # Verify it's the clean rom.
        self.verify_base_rom(vanilla_iso_path)

        #Use the Patcher to patch it into an iso.
        from pso_patcher import PSOPatcher
        PSOPatcher(patch_file_path)

    def __get_remote_dependencies_and_create_iso(self, appso_patch: str, pso_clean_iso: str):
        local_dir_path = self.__get_temp_folder_name()
        try:
            # Remove the temporary directory if we failed to patch the ISO correctly.
            if os.path.isdir(local_dir_path):
                logging.info("Found temp directory after failing seed generation, deleting %s.", local_dir_path)
                shutil.rmtree(local_dir_path)
                os.makedirs(local_dir_path, exist_ok=True)

                #Load external dependencies based on which OS
                logging.info("Temporary Directory created as: %s", local_dir_path)
                self.create_iso(local_dir_path, appso_patch, pso_clean_iso)
        except PermissionError:
            logging.warning("Failed to cleanup temp folder, %s ignoring delete.", local_dir_path)

def get_base_rom_path() -> str:
    options: Settings = get_settings()
    file_name = (options.get("phantasystar_options", "")).get("iso_file", "")
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name