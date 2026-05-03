from __future__ import annotations

import logging
from pathlib import Path

import Utils
from Utils import open_filename

from core import Err, InstallApworld, Ok, ValidateInstall

from launcher.bridge import dispatch


def _validated_apworld(apworld_src: str = "") -> tuple[Path, str, str] | None:
    """Return validated APWorld details, or `None` if the user cancels selection.

    Example::

        result = _validated_apworld("example.apworld")
    """

    if not apworld_src:
        selected_apworld = open_filename("Select APWorld file to install", (("APWorld", (".apworld",)),))
        if not selected_apworld:
            return None
        apworld_src = selected_apworld

    result = dispatch(ValidateInstall(apworld_path=apworld_src))
    match result:
        case Err(error=error):
            raise Exception(error.message)
        case Ok(value=value):
            if not value.valid:
                raise Exception(value.error or f"APWorld is not installable: {apworld_src}")
            if not value.module_name or not value.apworld_name:
                raise Exception("Validated APWorld is missing module metadata.")
            return Path(apworld_src), value.module_name, value.apworld_name


def _install_apworld(apworld_src: str = "") -> tuple[Path, Path] | None:
    """Install an APWorld into the custom worlds directory through core."""

    if not apworld_src:
        validated = _validated_apworld(apworld_src)
        if validated is None:
            return None
        apworld_src = str(validated[0])

    result = dispatch(InstallApworld(apworld_path=apworld_src))
    match result:
        case Err(error=error):
            raise Exception(error.message)
        case Ok(value=value):
            return Path(value.source_path), Path(value.target_path)


def install_apworld(apworld_path: str = "") -> None:
    """Install an APWorld and report the result to the user.

    Example::

        install_apworld("example.apworld")
    """

    try:
        result = _install_apworld(apworld_path)
        if result is None:
            logging.info("Aborting APWorld installation.")
            return
        source, target = result
    except Exception as exc:
        Utils.messagebox("Notice", str(exc), error=True)
        logging.exception(exc)
    else:
        logging.info(f"Installed APWorld successfully, copied {source} to {target}.")
        Utils.messagebox("Install complete.", f"Installed APWorld from {source}.")
