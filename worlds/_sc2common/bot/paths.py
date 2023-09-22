import os
import platform
import re
import sys
from contextlib import suppress
from pathlib import Path

from worlds._sc2common.bot import logger

from . import wsl

BASEDIR = {
    "Windows": "C:/Program Files (x86)/StarCraft II",
    "WSL1": "/mnt/c/Program Files (x86)/StarCraft II",
    "WSL2": "/mnt/c/Program Files (x86)/StarCraft II",
    "Darwin": "/Applications/StarCraft II",
    "Linux": "~/StarCraftII",
    "WineLinux": "~/.wine/drive_c/Program Files (x86)/StarCraft II",
}

USERPATH = {
    "Windows": "Documents\\StarCraft II\\ExecuteInfo.txt",
    "WSL1": "Documents/StarCraft II/ExecuteInfo.txt",
    "WSL2": "Documents/StarCraft II/ExecuteInfo.txt",
    "Darwin": "Library/Application Support/Blizzard/StarCraft II/ExecuteInfo.txt",
    "Linux": None,
    "WineLinux": None,
}

BINPATH = {
    "Windows": "SC2_x64.exe",
    "WSL1": "SC2_x64.exe",
    "WSL2": "SC2_x64.exe",
    "Darwin": "SC2.app/Contents/MacOS/SC2",
    "Linux": "SC2_x64",
    "WineLinux": "SC2_x64.exe",
}

CWD = {
    "Windows": "Support64",
    "WSL1": "Support64",
    "WSL2": "Support64",
    "Darwin": None,
    "Linux": None,
    "WineLinux": "Support64",
}


def platform_detect():
    pf = os.environ.get("SC2PF", platform.system())
    if pf == "Linux":
        return wsl.detect() or pf
    return pf


PF = platform_detect()


def get_home():
    """Get home directory of user, using Windows home directory for WSL."""
    if PF in {"WSL1", "WSL2"}:
        return wsl.get_wsl_home() or Path.home().expanduser()
    return Path.home().expanduser()


def get_user_sc2_install():
    """Attempts to find a user's SC2 install if their OS has ExecuteInfo.txt"""
    if USERPATH[PF]:
        einfo = str(get_home() / Path(USERPATH[PF]))
        if os.path.isfile(einfo):
            with open(einfo) as f:
                content = f.read()
            if content:
                base = re.search(r" = (.*)Versions", content).group(1)
                if PF in {"WSL1", "WSL2"}:
                    base = str(wsl.win_path_to_wsl_path(base))

                if os.path.exists(base):
                    return base
    return None


def get_env():
    # TODO: Linux env conf from: https://github.com/deepmind/pysc2/blob/master/pysc2/run_configs/platforms.py
    return None


def get_runner_args(cwd):
    if "WINE" in os.environ:
        runner_file = Path(os.environ.get("WINE"))
        runner_file = runner_file if runner_file.is_file() else runner_file / "wine"
        """
        TODO Is converting linux path really necessary?
        That would convert
        '/home/burny/Games/battlenet/drive_c/Program Files (x86)/StarCraft II/Support64'
        to
        'Z:\\home\\burny\\Games\\battlenet\\drive_c\\Program Files (x86)\\StarCraft II\\Support64'
        """
        return [runner_file, "start", "/d", cwd, "/unix"]
    return []


def latest_executeble(versions_dir, base_build=None):
    latest = None

    if base_build is not None:
        with suppress(ValueError):
            latest = (
                int(base_build[4:]),
                max(p for p in versions_dir.iterdir() if p.is_dir() and p.name.startswith(str(base_build))),
            )

    if base_build is None or latest is None:
        latest = max((int(p.name[4:]), p) for p in versions_dir.iterdir() if p.is_dir() and p.name.startswith("Base"))

    version, path = latest

    if version < 55958:
        logger.critical("Your SC2 binary is too old. Upgrade to 3.16.1 or newer.")
        sys.exit(1)
    return path / BINPATH[PF]


class _MetaPaths(type):
    """"Lazily loads paths to allow importing the library even if SC2 isn't installed."""

    # pylint: disable=C0203
    def __setup(self):
        if PF not in BASEDIR:
            logger.critical(f"Unsupported platform '{PF}'")
            sys.exit(1)

        try:
            base = os.environ.get("SC2PATH") or get_user_sc2_install() or BASEDIR[PF]
            self.BASE = Path(base).expanduser()
            self.EXECUTABLE = latest_executeble(self.BASE / "Versions")
            self.CWD = self.BASE / CWD[PF] if CWD[PF] else None

            self.REPLAYS = self.BASE / "Replays"

            if (self.BASE / "maps").exists():
                self.MAPS = self.BASE / "maps"
            else:
                self.MAPS = self.BASE / "Maps"
        except FileNotFoundError as e:
            logger.critical(f"SC2 installation not found: File '{e.filename}' does not exist.")
            sys.exit(1)

    # pylint: disable=C0203
    def __getattr__(self, attr):
        # pylint: disable=E1120
        self.__setup()
        return getattr(self, attr)


class Paths(metaclass=_MetaPaths):
    """Paths for SC2 folders, lazily loaded using the above metaclass."""
