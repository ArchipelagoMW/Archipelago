import bsdiff4
import yaml
from typing import Optional
import Utils


USHASH = '6e9c94511d04fac6e0a1e582c170be3a'
current_patch_version = 2


def read_rom(stream, strip_header=True) -> bytes:
    """Reads rom into bytearray and optionally strips off any smc header"""
    data = stream.read()
    if strip_header and len(data) % 0x400 == 0x200:
        return data[0x200:]
    return data


def generate_yaml(patch: bytes, metadata: Optional[dict] = None) -> bytes:
    patch = yaml.dump({"meta": metadata,
                       "patch": patch,
                       "game": "Secret of Evermore",
                       # minimum version of patch system expected for patching to be successful
                       "compatible_version": 1,
                       "version": current_patch_version,
                       "base_checksum": USHASH})
    return patch.encode(encoding="utf-8-sig")


def generate_patch(vanilla_file, randomized_file, metadata: Optional[dict] = None) -> bytes:
    with open(vanilla_file, "rb") as f:
        vanilla = read_rom(f)
    with open(randomized_file, "rb") as f:
        randomized = read_rom(f)
    if metadata is None:
        metadata = {}
    patch = bsdiff4.diff(vanilla, randomized)
    return generate_yaml(patch, metadata)


if __name__ == '__main__':
    import argparse
    import pathlib
    import lzma
    parser = argparse.ArgumentParser(description='Apply patch to Secret of Evermore.')
    parser.add_argument('patch', type=pathlib.Path, help='path to .absoe file')
    args = parser.parse_args()
    with open(args.patch, "rb") as f:
        data = Utils.parse_yaml(lzma.decompress(f.read()).decode("utf-8-sig"))
    if data['game'] != 'Secret of Evermore':
        raise RuntimeError('Patch is not for Secret of Evermore')
    with open(Utils.get_options()['soe_options']['rom_file'], 'rb') as f:
        vanilla_data = read_rom(f)
    patched_data = bsdiff4.patch(vanilla_data, data["patch"])
    with open(args.patch.parent / (args.patch.stem + '.sfc'), 'wb') as f:
        f.write(patched_data)

