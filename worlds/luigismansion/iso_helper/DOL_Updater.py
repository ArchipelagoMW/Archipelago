import struct

from gclib.dol import DOL, DOLSection
from gclib.gcm import GCM

MAIN_PKG_NAME = "worlds.luigismansion.LMGenerator"

# Updates the main DOL file, which is the main file used for GC and Wii games. This section includes some custom code
# inside the DOL file itself.
def update_dol_offsets(gcm: GCM, dol: DOL, start_inv: list[str], walk_speed: int, slot_name: str,
    king_boo_health: int, fear_anim_disabled: bool, pickup_anim_enabled: bool, boo_rand_on: bool):
    # Find the main 
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
        boo_custom_code_one = "93C1FFF0"
        dol.data.write(bytes.fromhex(boo_custom_code_one))

        dol.data.seek(0x04DBB0)
        boo_custom_code_two = "4848CDE5"
        dol.data.write(bytes.fromhex(boo_custom_code_two))

        dol.data.seek(0x04DC10)
        boo_custom_code_three = "4848CD85"
        dol.data.write(bytes.fromhex(boo_custom_code_three))

    # Turn off pickup animations
    if pickup_anim_enabled == 1:
        pickup_val = [0x01]
        gem_val = [0x05]

        # Write additional code to enable Custom Pickup animations when animations are turned off.
        dol.data.seek(0xAD625)
        dol.data.write(bytes.fromhex("42D0F5"))
    else:
        pickup_val = [0x02]
        gem_val = [0x06]

    # Keys and important animations
    dol.data.seek(0xCD39B)
    dol.data.write(struct.pack(">B", *pickup_val))

    # Diamonds and other treasure animations
    dol.data.seek(0xCE8D3)
    dol.data.write(struct.pack(">B", *gem_val))

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
    new_dol_sect = DOLSection(0x39FA20, 0x804DD940, new_dol_size)
    dol.sections[2] = new_dol_sect

    # Append the extra bytes we expect, to ensure we can write to them in memory.
    dol.data.seek(len(dol.data.getvalue()))
    blank_data = b"\x00" * new_dol_size
    dol.data.write(blank_data)

    # Read in all the other custom DOL changes and update their values to the new value as expected.
    # TODO update reading the DOL offsets here and then add 39AF20 to them to write them back
    #   Alternatively read the entire bin file and write teh contents to 39AF20.
    #   From there, dol_diff can still be used for minor hooks we need to update.
    custom_DOL_offsets = gcm.read_file_data()
    from importlib.resources import files
    with files(data).joinpath("dol_diff.csv").open() as file:
        hex_reader = csv.DictReader(file)
        for line in hex_reader:
            new_dol_offset, hex_val = int(line["addr"], 16), bytes.fromhex(line["val"])
            dol.data.seek(new_dol_offset)
            dol.data.write(hex_val)

    # Save all changes to the DOL itself.
    dol.save_changes()
    gcm.changed_files["sys/main.dol"] = dol.data