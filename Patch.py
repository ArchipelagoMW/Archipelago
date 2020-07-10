import bsdiff4
import yaml
import os
import lzma
import hashlib
import threading
import concurrent.futures
import zipfile
import sys
from typing import Tuple, Optional

import Utils
from Rom import JAP10HASH


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["general_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


def get_base_rom_bytes(file_name: str = "") -> bytes:
    from Rom import read_rom
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if JAP10HASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for JAP(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def generate_yaml(patch: bytes, metadata: Optional[dict] = None) -> bytes:
    patch = yaml.dump({"meta": metadata,
                       "patch": patch,
                       "game": "alttp",
                       "base_checksum": JAP10HASH})
    return patch.encode(encoding="utf-8-sig")


def generate_patch(rom: bytes, metadata: Optional[dict] = None) -> bytes:
    if metadata is None:
        metadata = {}
    patch = bsdiff4.diff(get_base_rom_bytes(), rom)
    return generate_yaml(patch, metadata)


def create_patch_file(rom_file_to_patch: str, server: str = "", destination: str = None) -> str:
    bytes = generate_patch(load_bytes(rom_file_to_patch),
                           {
                               "server": server})  # allow immediate connection to server in multiworld. Empty string otherwise
    target = destination if destination else os.path.splitext(rom_file_to_patch)[0] + ".bmbp"
    write_lzma(bytes, target)
    return target

def create_rom_bytes(patch_file: str) -> Tuple[dict, str, bytearray]:
    data = Utils.parse_yaml(lzma.decompress(load_bytes(patch_file)).decode("utf-8-sig"))
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

                elif rom.endswith(".bmbp"):
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

                elif rom.endswith("_multidata"):
                    import json
                    import zlib
                    with open(rom, 'rb') as fr:
                        multidata = zlib.decompress(fr.read()).decode("utf-8")
                        with open(rom + '.txt', 'w') as fw:
                            fw.write(multidata)
                        multidata = json.loads(multidata)
                        for rom in multidata['roms']:
                            Utils.persistent_store("servers", "".join(chr(byte) for byte in rom[2]), address)

                elif rom.endswith(".zip"):
                    print(f"Updating host in patch files contained in {rom}")

                    def _handle_zip_file_entry(zfinfo : zipfile.ZipInfo, server: str):
                        data = zfr.read(zfinfo)
                        if zfinfo.filename.endswith(".bmbp"):
                            data = update_patch_data(data, server)
                        with ziplock:
                            zfw.writestr(zfinfo, data)
                        return zfinfo.filename


                    futures = []
                    with zipfile.ZipFile(rom, "r") as zfr:
                        updated_zip = os.path.splitext(rom)[0] + "_updated.zip"
                        with zipfile.ZipFile(updated_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zfw:
                            for zfname in zfr.namelist():
                                futures.append(pool.submit(_handle_zip_file_entry, zfr.getinfo(zfname), address))
                            for future in futures:
                                print(f"File {future.result()} added to {os.path.split(updated_zip)[1]}")

            except:
                import traceback
                traceback.print_exc()
                input("Press enter to close.")

