from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings, Settings
from Utils import user_path
from CommonClient import logger

from hashlib import md5
from os import path as os_path

from gclib import fs_helpers as fs

RANDOMIZER_NAME = "Luigi's Mansion"
LM_USA_MD5 = "6e3d9ae0ed2fbd2f77fa1ca09a60c494"

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

class LuigisMansionUSAProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Luigi's Mansion"
    hash = [LM_USA_MD5]
    patch_file_ending = ".aplm"
    result_file_ending = ".iso"

    procedure = [
        ("apply_aplm", ["patch.aplm"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_settings().luigismansion_options.iso_file.encode()

    @classmethod
    def patch(cls, target: str) -> None:
        pass
        # TODO Potentially pass the GCM here and allow it to create the ISO output, where target is output file path


class LuigisMansionAPPatchExtension(APPatchExtension):
    game = "Luigi's Mansion"

    @staticmethod
    def apply_yaml(caller: LuigisMansionUSAProcedurePatch, rom_path_bytes: bytes, patch_yaml_path: str):
      rom_path = rom_path_bytes.decode()
      caller.patch(rom_path, patch_yaml_path)

def verify_base_rom():
    base_md5 = md5()
    lm_rom_path = get_base_rom_path()

    with open(lm_rom_path, "rb") as f:
        magic = fs.try_read_str(f, 0, 4)
        game_id = fs.try_read_str(f, 0, 6)
        logger.info(f"Magic Code: {magic}")
        logger.info(f"LM Game ID: {game_id}")
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            base_md5.update(chunk)

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

    if base_md5.hexdigest() != LM_USA_MD5:
        raise InvalidCleanISOError(f"Invalid vanilla {RANDOMIZER_NAME} ISO.\nYour ISO may be corrupted or your MD5 " +
            f"hashes do not match.\nCorrect ISO MD5 hash: {LM_USA_MD5}\nYour ISO's MD5 hash: {base_md5.hexdigest()}")
    return


def get_base_rom_path() -> str:
    options: Settings = get_settings()
    file_name = options["luigismansion_options"]["iso_file"]
    if not os_path.exists(file_name):
        file_name = user_path(file_name)
    return file_name