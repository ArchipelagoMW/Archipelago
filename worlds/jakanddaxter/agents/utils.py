import os
from functools import cache

from Utils import user_path


@cache
def user_data_path(filename: str) -> str:
    """
    Wrapper for Utils.user_path for jak1 related user data.

    This avoids permission issues when Archipelago is installed in
    system-owned locations (e.g. /opt).
    """
    _user_path = user_path()  # Uses Utils user path for consistency across worlds
    data_path = os.path.join(_user_path, "data", "jak1")  # Custom folder structure for jak1
    os.makedirs(data_path, exist_ok=True)  # Makes sure it exists
    return os.path.join(data_path, filename)
