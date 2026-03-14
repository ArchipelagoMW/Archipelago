"""Create archipelago.json manifest file. Run as `python -m worlds.soe.tools.make_manifest`."""

import json
from importlib.metadata import metadata
from pathlib import Path
from typing import Any

from .. import SoEWorld, __version__ as world_version, __author__ as world_author


__all__ = ["make_manifest"]


def make_manifest() -> dict[str, Any]:
    """
    Generate and return manifest dict for the Secret of Evermore APWorld.

    The world version is supposed to be equal to the pyevermizer version, but we may have to break that in the future
    if we ever do a breaking change to the world after we are >= 1.0.0, or we release multiple versions of the APWorld
    for a single pyevermizer version.
    """
    meta = metadata("pyevermizer")
    version = meta["Version"]
    authors = list(dict.fromkeys(map(str.rstrip, (world_author + "," + meta["Author"]).split(","))))
    assert world_version == version, f"Expected world version ({world_version}) == pyevermizer version ({version})."

    return {
        "game": SoEWorld.game,
        "authors": authors,
        "world_version": world_version,
        "minimum_ap_version": "0.4.2",  # introduction of settings API
    }


if __name__ == "__main__":
    assert SoEWorld.__file__, "Could not determine world source."
    module_dir = Path(SoEWorld.__file__).parent
    assert module_dir.is_dir(), f"{module_dir} is not a directory"
    manifest_path = module_dir / "archipelago.json"

    with manifest_path.open("w", encoding="utf-8") as f:
        json.dump(make_manifest(), f, indent=4)
