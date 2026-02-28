"""This is a dummy module that only exists to override the built in pyodide module."""

from __future__ import annotations
import pkgutil
import json
from typing import TYPE_CHECKING


def postMessage(message: str) -> None:
    """Fake function for printing messages with JS."""
    print(message)


def getFile(filename):
    """Fake function for loading files with Javascript."""
    try:
        with open(filename, "rb") as file:
            return file.read()
    except Exception:
        try:
            return pkgutil.get_data("worlds.dk64", filename)
        except Exception:
            with open(f"worlds/dk64/{filename}", "rb") as file:
                return file.read()


def getStringFile(filename):
    """Fake function for loading files with Javascript."""
    try:
        with open(filename, "r") as file:
            return file.read()
    except Exception:
        try:
            return pkgutil.get_data("worlds.dk64", filename).decode()
        except Exception:
            with open(f"worlds/dk64/{filename}", "r") as file:
                return file.read()


pointer_addresses = None
rom_symbols = None
try:
    with open("./static/patches/pointer_addresses.json", "rb") as file:
        pointer_addresses = json.loads(file.read())

    with open("./static/patches/symbols.json", "rb") as file:
        rom_symbols = json.loads(file.read())
except Exception:
    try:
        pointer_addresses = json.loads(pkgutil.get_data("worlds.dk64", "static/patches/pointer_addresses.json").decode())
        rom_symbols = json.loads(pkgutil.get_data("worlds.dk64", "static/patches/symbols.json").decode())
    except Exception:
        with open(f"worlds/dk64/static/patches/pointer_addresses.json", "rb") as file:
            pointer_addresses = json.loads(file.read())

        with open(f"worlds/dk64/static/patches/symbols.json", "rb") as file:
            rom_symbols = json.loads(file.read())
