
from typing import NamedTuple


class VersionCompatibility(NamedTuple):
    ut_accuracy: tuple[int, int, int]
    ut_compatibility: tuple[int, int, int]
    ap_minimum: tuple[int, int, int]


version: tuple[int, int, int] = (0, 99, 4)

compatibility: dict[tuple[int, int, int], VersionCompatibility] = {
    (0, 99, 4): VersionCompatibility((0, 99, 4), (0, 99, 0), (0, 6, 5)),
    (0, 99, 3): VersionCompatibility((0, 99, 3), (0, 99, 0), (0, 6, 5)),
    (0, 99, 2): VersionCompatibility((0, 99, 2), (0, 99, 0), (0, 6, 5)),
    (0, 99, 1): VersionCompatibility((0, 99, 1), (0, 99, 0), (0, 6, 5)),
    (0, 99, 0): VersionCompatibility((0, 99, 0), (0, 99, 0), (0, 6, 5)),
}


def ut_accuracy() -> tuple[int, int, int]:
    return compatibility[version].ut_accuracy


def ut_compatibility() -> tuple[int, int, int]:
    return compatibility[version].ut_compatibility


def ap_minimum() -> tuple[int, int, int]:
    return compatibility[version].ap_minimum


if __name__ == "__main__":
    import orjson
    import os
    import zipfile
    from worlds.Files import container_version

    apworld = "shapez_2"
    dev_dir = "D:/Games/Archipelago/custom_worlds/dev/"

    with zipfile.ZipFile(dev_dir + apworld + ".apworld", 'w', zipfile.ZIP_DEFLATED, True, 9) as zipf2:
        metadata = {
            "game": "shapez 2",
            "minimum_ap_version": ".".join(str(i) for i in ap_minimum()),
            "authors": ["BlastSlimey"],
            "world_version": ".".join(str(i) for i in version),
            "version": container_version,
            "compatible_version": 7,
        }
        zipf2.writestr(os.path.join(apworld, "archipelago.json"), orjson.dumps(metadata))
        for root, dirs, files in os.walk("../"):
            if "__pycache__" in root:
                continue
            if "_temp" in root:
                continue
            for file in files:
                zipf2.write(os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file),
                                            "../../"))
