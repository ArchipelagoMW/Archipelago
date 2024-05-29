import os
import shutil
import subprocess
import sys
import tempfile

WORLD_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(WORLD_DIR))

# pylint: disable=import-error, wrong-import-position
from tits_the_3rd.util import (
    get_tooling_path,
    read_dev_config_and_assert_contents
)
from tits_the_3rd.dev_util.items.item import read_new_weapons, Weapon

def _get_base_dt22(source_dir: str, temp_dir: str):
    factoria_path = get_tooling_path("factoria.exe")
    base_file_path = os.path.join(source_dir, "ED6_DT22")
    for extention in [".dir", ".dat"]:
        file_path = f"{base_file_path}{extention}"
        if not os.path.exists(file_path):
            raise ValueError(f"Path {file_path} does not exist.")
    try:
        subprocess.run([
            factoria_path,
            f"{base_file_path}.dir",
            "--output",
            temp_dir
        ], check=True)
    except subprocess.CalledProcessError as err:
        print(f"Error running factoria: {err}")
        raise err
    return os.path.join(temp_dir, "ED6_DT22")

def _read_item_dt_file(path: str) -> list[bytes]:
    offsets = []
    items = []
    with open (path, "rb") as fp:
        first_item_addr = int.from_bytes(fp.read(2), byteorder="little")
        fp.seek(0)
        while fp.tell() < first_item_addr:
            item_offset = int.from_bytes(fp.read(2), byteorder="little")
            offsets.append(item_offset)
        for idx in range(len(offsets)):  # pylint: disable=consider-using-enumerate
            next_offset = offsets[idx + 1] if idx < len(offsets) - 1 else os.path.getsize(path)
            fp.seek(offsets[idx])
            item_bytes = fp.read(next_offset - offsets[idx])
            items.append(item_bytes)
    return items

def _write_item_dt_file(path: str, items: list[bytes]):
    cur_header_offset = 0
    cur_item_offset = len(items) * 2
    with open(path, "wb") as output_file:
        for idx in range(len(items)):  # pylint: disable=consider-using-enumerate
            cur_header_offset = 0x2 * idx
            output_file.seek(cur_header_offset)
            output_file.write(cur_item_offset.to_bytes(2, byteorder="little"))
            output_file.seek(cur_item_offset)
            output_file.write(items[idx])
            cur_item_offset += len(items[idx])

def _write_ittxt_dt_file(path: str, items: list[bytes]):
    cur_header_offset = 0
    cur_item_offset = (len(items)) * 2
    with open(path, "wb") as output_file:
        for idx in range(len(items[:-1])):  # pylint: disable=consider-using-enumerate
            cur_header_offset = 0x2 * idx
            output_file.seek(cur_header_offset)
            output_file.write(cur_item_offset.to_bytes(2, byteorder="little"))
            output_file.seek(cur_item_offset)
            output_file.write(items[idx])
            previous_name_pointer = int.from_bytes(items[idx][4:6], byteorder='little')
            previous_desc_pointer = int.from_bytes(items[idx][6:8], byteorder='little')
            description_offset = previous_desc_pointer - previous_name_pointer
            output_file.seek(cur_item_offset + 0x4)
            output_file.write((cur_item_offset + 0x8).to_bytes(2, byteorder="little"))
            output_file.seek(cur_item_offset + 0x6)
            output_file.write((cur_item_offset + description_offset + 0x8).to_bytes(2, byteorder="little"))
            cur_item_offset += len(items[idx])

def _modify_t_item(t_item2_path: str, output_path: str, new_weapons: list[Weapon]):
    items = _read_item_dt_file(t_item2_path)
    new_items = []
    for item in new_weapons:
        new_items.append(item.convert_to_t_item_bytes())
    items[-1:-1] = new_items
    _write_item_dt_file(output_path, items)

def _modify_t_ittxt(t_ittxt2_path: str, output_path: str, new_weapons: list[Weapon]):
    items = _read_item_dt_file(t_ittxt2_path)
    new_items = []
    for item in new_weapons:
        new_items.append(item.convert_to_t_ittxt_bytes())
    items[-1:-1] = new_items
    _write_ittxt_dt_file(output_path, items)

def inject_custom_items():
    """
    This method adds custom weapons defined in items/new_weapons.json and inserts
    them into the game's t_item / t_ittxt dt files.

    It uses the base t_item / t_ittxt dt files as a base, (the contents of the current patch's files will be overwritten).
    """
    config = read_dev_config_and_assert_contents()
    source_dir = config["gameDirectory"]
    lb_ark_dir = config["lbARKDirectory"]
    script_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir = tempfile.mkdtemp(dir=script_dir)
    try:
        new_weapons = read_new_weapons()
        base_dt22_dir = _get_base_dt22(source_dir, temp_dir)
        _modify_t_item(os.path.join(base_dt22_dir, "t_item2._dt"), os.path.join(lb_ark_dir, "ED6_DT22", "t_item2._dt"), new_weapons)
        _modify_t_ittxt(os.path.join(base_dt22_dir, "t_ittxt2._dt"), os.path.join(lb_ark_dir, "ED6_DT22", "t_ittxt2._dt"), new_weapons)
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    inject_custom_items()
