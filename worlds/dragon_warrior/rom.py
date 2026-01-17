import hashlib
import os
import sys
import logging
import platform
from typing_extensions import override
import zipfile
from worlds.AutoWorld import World
import Utils
import settings
from worlds.Files import APAutoPatchInterface
from .client import EXPECTED_VERSION

DRAGON_WARRIOR_PRG0_HASH = "1cfeeac7a20b405780eea318d3d1af2a"
DRAGON_WARRIOR_PRG1_HASH = "25cf03eb7ac2dec4ef332425c151f373"

class DWPatch(APAutoPatchInterface):
    # Add flags to the APAutoPatchInterface to pass to DWR during patch time
    hash = [DRAGON_WARRIOR_PRG0_HASH, DRAGON_WARRIOR_PRG1_HASH]
    game = "Dragon Warrior"
    patch_file_ending = ".apdw"
    result_file_ending = ".nes"

    flags: str
    searchsanity: bool
    shopsanity: bool
    deathlink: bool

    def __init__(self,
                path: str | None = None,
                player: int | None = None,
                player_name: str = "",
                server: str = "",
                *,
                flags: str = "",
                searchsanity: bool = False,
                shopsanity: bool = False,
                deathlink: bool = False) -> None:
        super().__init__(path=path, player=player, player_name=player_name, server=server)
        self.flags = flags
        self.searchsanity = searchsanity
        self.shopsanity = shopsanity
        self.deathlink = deathlink > 0

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()
    
    @override
    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().write_contents(opened_zipfile)
        opened_zipfile.writestr("flags.txt",
                                self.flags,
                                compress_type=zipfile.ZIP_DEFLATED)
        opened_zipfile.writestr("search.txt",
                                str(self.searchsanity),
                                compress_type=zipfile.ZIP_DEFLATED)
        opened_zipfile.writestr("shopsanity.txt",
                                str(self.shopsanity),
                                compress_type=zipfile.ZIP_DEFLATED)
        opened_zipfile.writestr("deathlink.txt",
                                str(self.deathlink),
                                compress_type=zipfile.ZIP_DEFLATED)

    @override
    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super().read_contents(opened_zipfile)
        self.flags = opened_zipfile.read("flags.txt").decode()
        self.searchsanity = opened_zipfile.read("search.txt").decode()
        self.shopsanity = opened_zipfile.read("shopsanity.txt").decode()
        self.deathlink = opened_zipfile.read("deathlink.txt").decode()
    
    @override
    def patch(self, target: str) -> None:
        # Extract the dwr module from the .apworld depending on OS into a temp directory
        current_directory = Utils.user_path()
        new_dir = os.path.join(current_directory, "dragon_warrior_randomizer")

        # Load the appropriate module file depending on OS and which Python version is running
        python_version = str(sys.version_info.major) + str(sys.version_info.minor)

        if platform.system() == "Windows":
            file = "dwr.cp" + python_version + "-win_amd64.pyd"
        else:
            file = "dwr.cpython-" + python_version +"-x86_64-linux-gnu.so"

        try:
            os.mkdir(new_dir)
        except FileExistsError:
            pass

        with zipfile.ZipFile(os.path.join(current_directory, "custom_worlds", "dragon_warrior.apworld")) as zf:
            zf.extract("dragon_warrior/" + file, path=new_dir)

        # Clean up format from zip file
        os.replace(os.path.join(new_dir, "dragon_warrior", file), os.path.join(new_dir, file))
        os.rmdir(os.path.join(new_dir, "dragon_warrior"))
        open(os.path.join(new_dir, "__init__.py"), "a")

        sys.path.append(new_dir)

        self.read()
        # Create seed using target path hash
        temp = hash(target)
        if temp < 0:
            temp *= -1
        temp = str(temp)
        while len(temp) < 15:
            temp = temp + "0"
        seed = int(temp[:15])
        write_rom(seed, self.flags, target, self.searchsanity, self.shopsanity, self.player_name, self.deathlink)


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = open(file_name, "rb").read()

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in [DRAGON_WARRIOR_PRG0_HASH, DRAGON_WARRIOR_PRG1_HASH]:
            raise Exception('Supplied Base Rom does not match known MD5 for US(PRG0) or US(PRG1) release.'
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes

def get_base_rom_path(file_name: str = "") -> str:
    options = settings.get_settings()
    if not file_name:
        file_name = options.dw_options["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

def write_rom(
        seed: int, 
        flags: str, 
        target: str, 
        search: bool, 
        shopsanity: bool, 
        player_name: str, 
        deathlink: bool
    ) -> None:
    # Patch using DWRandomizer
    if os.path.isfile(target):
        return
    import dwr # type: ignore
    dwr.py_dwr_randomize(bytes(get_base_rom_path(), encoding="ascii"), 
                               seed, 
                               bytes(flags, encoding="ascii"), 
                               bytes(target, encoding="ascii"), 
                               bytes(EXPECTED_VERSION, encoding="ascii"),
                               search == 'SearchSanity(Yes)',
                               shopsanity == 'ShopSanity(Yes)')
    
    # Write Slot Name and Deathlink status to ROM
    with open(target, "r+b", buffering=0) as f:
        f.seek(0xBFF0)
        f.write(player_name.encode() + 0x00.to_bytes() * (16 - len(player_name)))  # Pad to 16 chars
        f.flush()
        if deathlink == "True":
            f.seek(0x7FFF)
            f.write(0xDE.to_bytes())
            f.flush()
        os.fsync(f.fileno())