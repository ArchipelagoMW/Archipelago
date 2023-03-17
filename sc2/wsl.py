# pylint: disable=R0911,W1510
import os
import re
import subprocess
from pathlib import Path, PureWindowsPath

from loguru import logger

## This file is used for compatibility with WSL and shouldn't need to be
## accessed directly by any bot clients


def win_path_to_wsl_path(path):
    """Convert a path like C:\\foo to /mnt/c/foo"""
    return Path("/mnt") / PureWindowsPath(re.sub("^([A-Z]):", lambda m: m.group(1).lower(), path))


def wsl_path_to_win_path(path):
    """Convert a path like /mnt/c/foo to C:\\foo"""
    return PureWindowsPath(re.sub("^/mnt/([a-z])", lambda m: m.group(1).upper() + ":", path))


def get_wsl_home():
    """Get home directory of from Windows, even if run in WSL"""
    proc = subprocess.run(["powershell.exe", "-Command", "Write-Host -NoNewLine $HOME"], capture_output=True)

    if proc.returncode != 0:
        return None

    return win_path_to_wsl_path(proc.stdout.decode("utf-8"))


RUN_SCRIPT = """$proc = Start-Process -NoNewWindow -PassThru "%s" "%s"
if ($proc) {
    Write-Host $proc.id
    exit $proc.ExitCode
} else {
    exit 1
}"""


def run(popen_args, sc2_cwd):
    """Run SC2 in Windows and get the pid so that it can be killed later."""
    path = wsl_path_to_win_path(popen_args[0])
    args = " ".join(popen_args[1:])

    return subprocess.Popen(
        ["powershell.exe", "-Command", RUN_SCRIPT % (path, args)],
        cwd=sc2_cwd,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,
    )


def kill(wsl_process):
    """Needed to kill a process started with WSL. Returns true if killed successfully."""
    # HACK: subprocess and WSL1 appear to have a nasty interaction where
    # any streams are never closed and the process is never considered killed,
    # despite having an exit code (this works on WSL2 as well, but isn't
    # necessary). As a result,
    # 1: We need to read using readline (to make sure we block long enough to
    #    get the exit code in the rare case where the user immediately hits ^C)
    out = wsl_process.stdout.readline().rstrip()
    # 2: We need to use __exit__, since kill() calls send_signal(), which thinks
    #    the process has already exited!
    wsl_process.__exit__(None, None, None)
    proc = subprocess.run(["taskkill.exe", "-f", "-pid", out], capture_output=True)
    return proc.returncode == 0  # Returns 128 on failure


def detect():
    """Detect the current running version of WSL, and bail out if it doesn't exist"""
    # Allow disabling WSL detection with an environment variable
    if os.getenv("SC2_WSL_DETECT", "1") == "0":
        return None

    wsl_name = os.environ.get("WSL_DISTRO_NAME")
    if not wsl_name:
        return None

    try:
        wsl_proc = subprocess.run(["wsl.exe", "--list", "--running", "--verbose"], capture_output=True)
    except (OSError, ValueError):
        return None
    if wsl_proc.returncode != 0:
        return None

    # WSL.exe returns a bunch of null characters for some reason, as well as
    # windows-style linebreaks. It's inconsistent about how many \rs it uses
    # and this could change in the future, so strip out all junk and split by
    # Unix-style newlines for safety's sake.
    lines = re.sub(r"\000|\r", "", wsl_proc.stdout.decode("utf-8")).split("\n")

    def line_has_proc(ln):
        return re.search("^\\s*[*]?\\s+" + wsl_name, ln)

    def line_version(ln):
        return re.sub("^.*\\s+(\\d+)\\s*$", "\\1", ln)

    versions = [line_version(ln) for ln in lines if line_has_proc(ln)]

    try:
        version = versions[0]
        if int(version) not in [1, 2]:
            return None
    except (ValueError, IndexError):
        return None

    logger.info(f"WSL version {version} detected")

    if version == "2" and not (os.environ.get("SC2CLIENTHOST") and os.environ.get("SC2SERVERHOST")):
        logger.warning("You appear to be running WSL2 without your hosts configured correctly.")
        logger.warning("This may result in SC2 staying on a black screen and not connecting to your bot.")
        logger.warning("Please see the python-sc2 README for WSL2 configuration instructions.")

    return "WSL" + version
