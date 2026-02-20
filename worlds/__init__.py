from __future__ import annotations

import os

from Utils import local_path, user_path

from . import AutoWorld
from .AutoWorld import AutoWorldRegister
from .registry import get_registry

local_folder = os.path.dirname(__file__)
user_folder = user_path("worlds") if user_path() != local_path() else user_path("custom_worlds")
try:
    os.makedirs(user_folder, exist_ok=True)
except OSError:
    user_folder = None

_registry = get_registry()

__all__ = [
    "AutoWorld",
    "AutoWorldRegister",
    "local_folder",
    "network_data_package",
    "user_folder",
]

# Backwards compatibility, uses registry
network_data_package = _registry.network_data_package
