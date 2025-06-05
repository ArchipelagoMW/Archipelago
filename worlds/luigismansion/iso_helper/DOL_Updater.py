import random
import struct
from pkgutil import get_data

from gclib.dol import DOL, DOLSection
from gclib.gcm import GCM

from ..Regions import spawn_locations

MAIN_PKG_NAME = "worlds.luigismansion.LMGenerator"
CUSTOM_CODE_OFFSET_START = 0x39FA20

# Updates the main DOL file, which is the main file used for GC and Wii games. This section includes some custom code
# inside the DOL file itself.
def update_dol_offsets(gcm: GCM, dol: DOL, seed: str, start_inv: list[str], walk_speed: int, slot_name: str,
    random_spawn: str, king_boo_health: int, fear_anim_disabled: bool, pickup_anim_enabled: bool,
    boo_rand_on: bool, dool_model_rando_on: bool) -> (GCM, DOL):

    random.seed(seed)

    # Find the main DOL file and read it.
    dol_data = gcm.read_file_data("sys/main.dol")
    dol.read(dol_data)

    # Walk Speed
    if walk_speed == 0:
        speed_to_use = 16784
    elif walk_speed == 1:
        speed_to_use = 16850
    else:
        speed_to_use = 16950
    dol.data.seek(0x396538)
    dol.data.write(struct.pack(">H", speed_to_use))

    # Vacuum Speed
    if any("Poltergust 4000" in key for key in start_inv):
        vac_speed = "3800000F"
    else:
        vac_speed = "800D0160"
    dol.data.seek(0x7EA28)
    dol.data.write(bytes.fromhex(vac_speed))

    # Fix Boos to properly spawn
    dol.data.seek(0x12DCC9)
    boo_data = "000005"
    dol.data.write(bytes.fromhex(boo_data))

    # Turn on custom code handler for boo display counter only if Boo Rando is on.
    if boo_rand_on:
        dol.data.seek(0x04DB50)
        dol.data.write(bytes.fromhex("93C1FFF0"))

        dol.data.seek(0x04DBB0)
        dol.data.write(bytes.fromhex("4848D0C1"))

        dol.data.seek(0x04DC10)
        dol.data.write(bytes.fromhex("4848D061"))

    # Turn off pickup animations
    if pickup_anim_enabled == 1:
        keys_and_others_val = "01"
        gem_val = "05"
        hat_val = "05"
        elem_val = "15"

        # Write additional code to enable Custom Pickup animations when animations are turned off for King Boo
        dol.data.seek(0x0AD624)
        dol.data.write(bytes.fromhex("4842D769"))
    else:
        keys_and_others_val = "02"
        gem_val = "06"
        hat_val = "06"
        elem_val = "16"

    # Keys and important animations
    dol.data.seek(0xCD39B)
    dol.data.write(bytes.fromhex(keys_and_others_val))

    # Diamonds and other treasure animations
    dol.data.seek(0xCE8D3)
    dol.data.write(bytes.fromhex(gem_val))

    # Disable Mario Item pickup animations
    dol.data.seek(0x0CD707)
    dol.data.write(bytes.fromhex(hat_val))

    # Disable Elemental Medal pickup animations
    dol.data.seek(0x0CF4A3)
    dol.data.write(bytes.fromhex(elem_val))

    # Turn off luigi scare animations
    if fear_anim_disabled == 1:
        scare_val = [0x00]
    else:
        scare_val = [0x44]
    dol.data.seek(0x396578)
    dol.data.write(struct.pack(">B", *scare_val))

    # Store Player name
    lm_player_name = str(slot_name).strip()
    dol.data.seek(0x311660)
    dol.data.write(struct.pack(str(len(lm_player_name)) + "s", lm_player_name.encode()))

    # Change King Boo's Health
    dol.data.seek(0x399228)
    dol.data.write(struct.pack(">H", king_boo_health))

    # Replace section two with our own custom section, which is about 1000 hex bytes long.
    new_dol_size = 0x1000
    new_dol_sect = DOLSection(CUSTOM_CODE_OFFSET_START, 0x804DD940, new_dol_size)
    dol.sections[2] = new_dol_sect

    # Append the extra bytes we expect, to ensure we can write to them in memory.
    dol.data.seek(len(dol.data.getvalue()))
    blank_data = b"\x00" * new_dol_size
    dol.data.write(blank_data)

    # Read in all the other custom DOL changes and update their values to the new value as expected.
    custom_dol_code = get_data(MAIN_PKG_NAME, "data/lm_custom_code.lmco")
    dol.data.seek(CUSTOM_CODE_OFFSET_START)
    dol.data.write(custom_dol_code)

    dol_csv_offsets = get_data(MAIN_PKG_NAME, "data/dol_diff.csv").decode("utf-8").splitlines()
    for csv_line in dol_csv_offsets:
        dol_addr, dol_val = csv_line.split(",")
        dol.data.seek(int(dol_addr, 16))
        dol.data.write(bytes.fromhex(dol_val))

    if not random_spawn == "Foyer":
        spawn_info: dict = spawn_locations[random_spawn]
        dol.data.seek(0x3A02B0)
        dol.data.write(struct.pack(">f", spawn_info["pos_x"]))
        dol.data.seek(0x3A02B4)
        dol.data.write(struct.pack(">f", spawn_info["pos_y"]))
        dol.data.seek(0x3A02B8)
        dol.data.write(struct.pack(">f", spawn_info["pos_z"]))

    if dool_model_rando_on:
        door_model_offsets: list[int] = [0x2FFFBE, 0x2FFFDA, 0x2FFFF6, 0x300012, 0x30004A, 0x300066, 0x300082,
            0x30009E, 0x3000BA, 0x3000D6, 0x300146, 0x300162, 0x30017E, 0x30019A, 0x3001B6, 0x3001D2, 0x3001EE,
            0x30020A, 0x300242, 0x30025E, 0x30027A, 0x3002B2, 0x3002CE, 0x3002EA, 0x300306, 0x30035A, 0x3003AE,
            0x3003CA, 0x3003E6, 0x300402, 0x30043A, 0x300456, 0x300472, 0x30048E, 0x3004C6, 0x3004E2, 0x3004FE,
            0x30051A, 0x30056E, 0x30058A, 0x3005A6, 0x3005DE, 0x3005FA, 0x300616, 0x300632, 0x30064E, 0x300686,
            0x3006A2, 0x3006BE, 0x3006DA, 0x3006F6, 0x300712, 0x30072E, 0x30074A]
        for map_two_doors in door_model_offsets:
            dol.data.seek(map_two_doors)
            door_model_id = random.randint(1,14)
            dol.data.write(door_model_id.to_bytes())

    # Save all changes to the DOL itself.
    dol.save_changes()
    gcm.changed_files["sys/main.dol"] = dol.data

    return gcm, dol