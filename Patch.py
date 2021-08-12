import bsdiff4
import yaml
import os
import lzma
import threading
import concurrent.futures
import zipfile
import sys
from typing import Tuple, Optional

import Utils


current_patch_version = 2


def generate_yaml(patch: bytes, metadata: Optional[dict] = None) -> bytes:
    from worlds.alttp.Rom import JAP10HASH
    patch = yaml.dump({"meta": metadata,
                       "patch": patch,
                       "game": "A Link to the Past",
                       # minimum version of patch system expected for patching to be successful
                       "compatible_version": 1,
                       "version": current_patch_version,
                       "base_checksum": JAP10HASH})
    return patch.encode(encoding="utf-8-sig")


def generate_patch(rom: bytes, metadata: Optional[dict] = None) -> bytes:
    from worlds.alttp.Rom import get_base_rom_bytes
    if metadata is None:
        metadata = {}
    patch = bsdiff4.diff(get_base_rom_bytes(), rom)
    return generate_yaml(patch, metadata)


def create_patch_file(rom_file_to_patch: str, server: str = "", destination: str = None,
                      player: int = 0, player_name: str = "") -> str:
    meta = {"server": server, # allow immediate connection to server in multiworld. Empty string otherwise
            "player_id": player,
            "player_name": player_name}
    bytes = generate_patch(load_bytes(rom_file_to_patch),
                           meta)
    target = destination if destination else os.path.splitext(rom_file_to_patch)[0] + ".apbp"
    write_lzma(bytes, target)
    return target


def create_rom_bytes(patch_file: str, ignore_version: bool = False) -> Tuple[dict, str, bytearray]:
    from worlds.alttp.Rom import get_base_rom_bytes
    data = Utils.parse_yaml(lzma.decompress(load_bytes(patch_file)).decode("utf-8-sig"))
    if not ignore_version and data["compatible_version"] > current_patch_version:
        raise RuntimeError("Patch file is incompatible with this patcher, likely an update is required.")
    patched_data = bsdiff4.patch(get_base_rom_bytes(), data["patch"])
    rom_hash = patched_data[int(0x7FC0):int(0x7FD5)]
    data["meta"]["hash"] = "".join(chr(x) for x in rom_hash)
    target = os.path.splitext(patch_file)[0] + ".sfc"
    return data["meta"], target, patched_data


def create_rom_file(patch_file: str) -> Tuple[dict, str]:
    data, target, patched_data = create_rom_bytes(patch_file)
    with open(target, "wb") as f:
        f.write(patched_data)
    return data, target


def update_patch_data(patch_data: bytes, server: str = "") -> bytes:
    data = Utils.parse_yaml(lzma.decompress(patch_data).decode("utf-8-sig"))
    data["meta"]["server"] = server
    bytes = generate_yaml(data["patch"], data["meta"])
    return lzma.compress(bytes)


def load_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def write_lzma(data: bytes, path: str):
    with lzma.LZMAFile(path, 'wb') as f:
        f.write(data)


if __name__ == "__main__":
    host = Utils.get_public_ipv4()
    options = Utils.get_options()['server_options']
    if options['host']:
        host = options['host']

    address = f"{host}:{options['port']}"
    ziplock = threading.Lock()
    print(f"Host for patches to be created is {address}")
    with concurrent.futures.ThreadPoolExecutor() as pool:
        for rom in sys.argv:
            try:
                if rom.endswith(".sfc"):
                    print(f"Creating patch for {rom}")
                    result = pool.submit(create_patch_file, rom, address)
                    result.add_done_callback(lambda task: print(f"Created patch {task.result()}"))

                elif rom.endswith(".apbp"):
                    print(f"Applying patch {rom}")
                    data, target = create_rom_file(rom)
                    romfile, adjusted = Utils.get_adjuster_settings(target)
                    if adjusted:
                        try:
                            os.replace(romfile, target)
                            romfile = target
                        except Exception as e:
                            print(e)
                    print(f"Created rom {romfile if adjusted else target}.")
                    if 'server' in data:
                        Utils.persistent_store("servers", data['hash'], data['server'])
                        print(f"Host is {data['server']}")

                elif rom.endswith(".archipelago"):
                    import json
                    import zlib

                    with open(rom, 'rb') as fr:

                        multidata = zlib.decompress(fr.read()).decode("utf-8")
                        with open(rom + '.txt', 'w') as fw:
                            fw.write(multidata)
                        multidata = json.loads(multidata)
                        for romname in multidata['roms']:
                            Utils.persistent_store("servers", "".join(chr(byte) for byte in romname[2]), address)
                        from Utils import get_options

                        multidata["server_options"] = get_options()["server_options"]
                        multidata = zlib.compress(json.dumps(multidata).encode("utf-8"), 9)
                        with open(rom + "_updated.archipelago", 'wb') as f:
                            f.write(multidata)

                elif rom.endswith(".zip"):
                    print(f"Updating host in patch files contained in {rom}")


                    def _handle_zip_file_entry(zfinfo: zipfile.ZipInfo, server: str):
                        data = zfr.read(zfinfo)
                        if zfinfo.filename.endswith(".apbp"):
                            data = update_patch_data(data, server)
                        with ziplock:
                            zfw.writestr(zfinfo, data)
                        return zfinfo.filename


                    futures = []
                    with zipfile.ZipFile(rom, "r") as zfr:
                        updated_zip = os.path.splitext(rom)[0] + "_updated.zip"
                        with zipfile.ZipFile(updated_zip, "w", compression=zipfile.ZIP_DEFLATED,
                                             compresslevel=9) as zfw:
                            for zfname in zfr.namelist():
                                futures.append(pool.submit(_handle_zip_file_entry, zfr.getinfo(zfname), address))
                            for future in futures:
                                print(f"File {future.result()} added to {os.path.split(updated_zip)[1]}")

            except:
                import traceback

                traceback.print_exc()
                input("Press enter to close.")


def read_rom(stream, strip_header=True) -> bytearray:
    """Reads rom into bytearray and optionally strips off any smc header"""
    buffer = bytearray(stream.read())
    if strip_header and len(buffer) % 0x400 == 0x200:
        return buffer[0x200:]
    return buffer
