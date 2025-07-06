from worlds.Files import APPatchExtension, APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings, Settings
from Utils import user_path

from os import path as os_path

from gclib import fs_helpers as fs

RANDOMIZER_NAME = "Luigi's Mansion"
LM_USA_MD5 = "6e3d9ae0ed2fbd2f77fa1ca09a60c494"

class LuigisMansionUSAProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Luigi's Mansion"
    hash = [LM_USA_MD5]
    patch_file_ending = ".aplm"
    result_file_ending = ".iso"

    procedure = [
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().luigismansion_options.iso_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())
        return base_rom_bytes


def get_base_rom_bytes(file_name: str = "") -> bytes:
    lm_rom_path = get_base_rom_path(file_name)
    lm_rom_bytes = open(lm_rom_path, "rb").read()
    __verify_supported_version(lm_rom_path)

    basemd5 = hashlib.md5()
    basemd5.update(base_rom_bytes)
    if basemd5.hexdigest() == PROTEUSHASH:
        base_rom_bytes = extract_mm2(base_rom_bytes)
        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
    if basemd5.hexdigest() not in {MM2LCHASH, MM2NESHASH, MM2VCHASH}:
        print(basemd5.hexdigest())
        raise Exception("Supplied Base Rom does not match known MD5 for US, LC, or US VC release. "
                        "Get the correct game and version, then dump it")
    headered_rom = bytearray(base_rom_bytes)
    headered_rom[0:0] = header
    setattr(get_base_rom_bytes, "base_rom_bytes", bytes(headered_rom))
    return bytes(headered_rom)


def get_base_rom_path(file_name: str = "") -> str:
    options: Settings = get_settings()
    if not file_name:
        file_name = options["luigismansion_options"]["iso_file"]
    if not os_path.exists(file_name):
        file_name = user_path(file_name)
    return file_name


# Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
# Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
def __verify_supported_version(rom_bytes: bytes):
    magic = fs.try_read_str(rom_bytes, 0, 4)
    game_id = fs.try_read_str(f, 0, 6)
    if magic == "CISO":
        raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {RANDOMIZER_NAME} randomizer " +
                                   "only supports ISOs in ISO format.")
    if game_id != "GLME01":
        if game_id and game_id.startswith("GLM"):
            raise InvalidCleanISOError(f"Invalid version of {RANDOMIZER_NAME}. " +
                                       "Only the North American version is supported by this randomizer.")
        else:
            raise InvalidCleanISOError("Invalid game given as the vanilla ISO. You must specify a " +
                                       "%s ISO (North American version)." % RANDOMIZER_NAME)
    self.__verify_correct_clean_iso_md5()

# Verify the MD5 hash matches the expectation of a USA-based ISO.
# Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
def __verify_correct_clean_iso_md5(self):
    md5 = hashlib.md5()
    with open(self.clean_iso_path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            md5.update(chunk)

    integer_md5 = int(md5.hexdigest(), 16)
    if integer_md5 != CLEAN_LUIGIS_MANSION_ISO_MD5:
        raise InvalidCleanISOError(
            f"Invalid vanilla {RANDOMIZER_NAME} ISO. Your ISO may be corrupted.\n" +
            f"Correct ISO MD5 hash: {CLEAN_LUIGIS_MANSION_ISO_MD5:x}\nYour ISO's MD5 hash: {integer_md5:x}")