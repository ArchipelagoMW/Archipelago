import shutil

from worlds.Files import APPatch, APPlayerContainer, AutoPatchRegister
from settings import get_settings, Settings
import Utils

from hashlib import md5
from typing import Any
import yaml, json, logging, sys, os, zipfile, tempfile
import urllib.request

logger = logging.getLogger()
MAIN_PKG_NAME = "worlds.luigismansion.LMGenerator"

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

    def __init__(self, player_choices: dict, patch_path: str, base_path:str, player_name: str, player: int,
        server: str = ""):
        self.output_data = player_choices
        self.file_path = base_path
        super().__init__(patch_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.aplm",
            yaml.dump(self.output_data,sort_keys=False,Dumper=yaml.CDumper))
        super().write_contents(opened_zipfile)


class LMUSAAPPatch(APPatch, metaclass=AutoPatchRegister):
    game = RANDOMIZER_NAME
    hash = LM_USA_MD5
    patch_file_ending = ".aplm"
    result_file_ending = ".iso"

    procedure = ["custom"]

    def __init__(self, *args: Any, **kwargs: Any):
        super(LMUSAAPPatch, self).__init__(*args, **kwargs)

    def __get_archive_name(self) -> str:
        if not (Utils.is_linux or Utils.is_windows):
            message = f"Your OS is not supported with this randomizer {sys.platform}."
            logger.error(message)
            raise RuntimeError(message)

        lib_path = ""
        if Utils.is_windows:
            lib_path = "lib-windows"
        elif Utils.is_linux:
            lib_path = "lib-linux"

        logger.info(f"Dependency archive name to use: {lib_path}")
        return lib_path

    def __get_temp_folder_name(self) -> str:
        from ..LMClient import CLIENT_VERSION
        temp_path = os.path.join(tempfile.gettempdir(), "luigis_mansion", CLIENT_VERSION, "libs")
        return temp_path

    def patch(self, aplm_patch: str) -> None:
        # Get the AP Path for the base ROM
        lm_clean_iso = self.get_base_rom_path()
        logger.info("Provided Luigi's Mansion ISO Path was: " + lm_clean_iso)

        base_path = os.path.splitext(aplm_patch)[0]
        output_file = base_path + self.result_file_ending

        try:
            # Verify we have a clean rom of the game first
            self.verify_base_rom(lm_clean_iso)

            # Use our randomize function to patch the file into an ISO.
            from ..LMGenerator import LuigisMansionRandomizer
            with zipfile.ZipFile(aplm_patch, "r") as zf:
                aplm_bytes = zf.read("patch.aplm")
            LuigisMansionRandomizer(lm_clean_iso, output_file, aplm_bytes)
        except ImportError:
            self.__get_remote_dependencies_and_create_iso(aplm_patch, output_file, lm_clean_iso)

    def read_contents(self, aplm_patch: str) -> dict[str, Any]:
        with zipfile.ZipFile(aplm_patch, "r") as zf:
            with zf.open("archipelago.json", "r") as f:
                manifest = json.load(f)
        if manifest["compatible_version"] > self.version:
            raise Exception(f"File (version: {manifest['compatible_version']}) too new "
                            f"for this handler (version: {self.version})")
        return manifest

    @classmethod
    def get_base_rom_path(cls) -> str:
        options: Settings = get_settings()
        file_name = options["luigismansion_options"]["iso_file"]
        if not os.path.exists(file_name):
            file_name = Utils.user_path(file_name)
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
            raise InvalidCleanISOError(f"Invalid vanilla {RANDOMIZER_NAME} ISO.\nYour ISO may be corrupted or your " +
                f"MD5 hashes do not match.\nCorrect ISO MD5 hash: {LM_USA_MD5:x}\nYour ISO's MD5 hash: {md5_conv}")

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


    def download_lib_zip(self, tmp_dir_path: str) -> None:
        logger.info("Getting missing dependencies for Luigi's Mansion from remote source.")

        from ..LMClient import CLIENT_VERSION
        lib_path = self.__get_archive_name()
        lib_path_base = f"https://github.com/BootsinSoots/Archipelago/releases/download/{CLIENT_VERSION}"
        download_path = f"{lib_path_base}/{lib_path}.zip"

        temp_zip_path = os.path.join(tmp_dir_path, "temp.zip")
        with urllib.request.urlopen(download_path) as response, open(temp_zip_path, 'wb') as created_zip:
            created_zip.write(response.read())

        with zipfile.ZipFile(temp_zip_path) as z:
            z.extractall(tmp_dir_path)

        return

    def create_iso(self, temp_dir_path: str, patch_file_path: str, output_iso_path: str, vanilla_iso_path: str):
        logger.info(f"Appending the following to sys path to get dependencies correctly: {temp_dir_path}")
        sys.path.append(temp_dir_path)

        # Verify we have a clean rom of the game first
        self.verify_base_rom(vanilla_iso_path)

        # Use our randomize function to patch the file into an ISO.
        from ..LMGenerator import LuigisMansionRandomizer
        with zipfile.ZipFile(patch_file_path, "r") as zf:
            aplm_bytes = zf.read("patch.aplm")
        LuigisMansionRandomizer(vanilla_iso_path, output_iso_path, aplm_bytes)

    def __get_remote_dependencies_and_create_iso(self, aplm_patch: str, output_file: str, lm_clean_iso: str):
        try:
            local_dir_path = self.__get_temp_folder_name()
            # if temp directory exists and we failed to patch the ISO we want to remove the directory
            # and get a fresh install.
            if os.path.isdir(local_dir_path):
                logger.info("Found temporary directory after unsuccessful attempt of generating seed, deleting %s.", local_dir_path)
                shutil.rmtree(local_dir_path)
            os.makedirs(local_dir_path, exist_ok=True)
            # Load the external dependencies based on OS
            logger.info("Temporary Directory created as: %s", local_dir_path)
            self.download_lib_zip(local_dir_path)
            self.create_iso(local_dir_path, aplm_patch, output_file, lm_clean_iso)
        except PermissionError:
            logger.warning("Failed to cleanup temp folder, %s ignoring delete.", local_dir_path)
