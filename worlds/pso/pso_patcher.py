import os
import json
import struct, zipfile

from gclib.gcm import GCM
from gclib.dol import DOL

import Utils

from .items import ALL_ITEMS_TABLE, MMXCMItemData
from .locations import LOCATION_TABLE, MMXCMLocationData
from .helpers import CLIENT_VERSION, AP_WORLD_VERSION_NAME, StringByteFunction as sbf
from .files.MMXCMDolChanges import CODE_PATCHES

MMXCM_PLAYER_NAME_BYTE_LENGTH = 64

class PSOPatcher:
    def __init__(self, patch_file_path: str):

class MMXCMPatcher:
    def __init__(self, patch_file_path: str):
        from .files.mmxcm_rom import get_base_rom_path, MMXCMPALPatch
        self.clean_iso_path = get_base_rom_path()

        base_path = os.path.splitext(patch_file_path)[0]
        self.randomized_output_file_path = base_path + MMXCMPALPatch.result_file_ending
        self.gcm = None
        self.dol = None

        try:
            if os.path.isfile(patch_file_path):
                temp_file = open(patch_file_path, "r+")
                temp_file.close()
        except IOError:
            raise Exception("'" + patch_file_path + "' is currently used in another program.")

        with zipfile.ZipFile(patch_file_path, "r") as zf:
            apmmxcm_bytes = zf.read("patch.apmmxcm")
        self.output_data = json.loads(apmmxcm_bytes.decode('utf-8'))

        # This will make sure the client and server versions match
        self._check_apworld_version(self.output_data)

        # This will read the options based on the player's choices in YAML.
        self.options = self.output_data.get("Options", {})
        self.encounter_rate = self.options.get("encounter_rate", 1)  # 1 is our default: Vanilla

        # This will read the entire iso, system files, etc after checking server version.
        self.gcm = GCM(self.clean_iso_path)
        self.gcm.read_entire_disc()
        self.dol = DOL()
        self.dol.read(self.gcm.read_file_data("sys/main.dol"))

        # Change game ID so save files are different
        from CommonClient import logger  # We have to lazy import to avoid error.

        logger.info("Updating the ISO game id with the AP generated seed.")
        self.seed = self.output_data["Seed"]
        magic_seed = str(self.seed)
        bin_data = self.gcm.read_file_data("sys/boot.bin")
        bin_data.seek(0x01)
        bin_data.write(sbf.string_to_bytes(magic_seed, len(magic_seed)))
        self.gcm.changed_files["sys/boot.bin"] = bin_data

    def _check_apworld_version(self, output_data):
        """
        Compares the AP version in the patch to the client version.
        """

        ap_world_version = output_data[AP_WORLD_VERSION_NAME]
        if ap_world_version != CLIENT_VERSION:
            raise Utils.VersionException("Error! Server was generated with a different MMXCM Seed!")

    def write_item_to_location(self, location_name: str, item_name: str):
        """
        This function to look up the correct addresses and IDs and write the new item into the ROM.
        """
        try:
            # 1 - We will look up the locations address from Location table
            if location_name not in LOCATION_TABLE:
                print(f"Warning: Skipping unknown '{location_name}'.")
                return

            # 2 - Look up the Item's ID from ALL_ITEMS_TABLE
            if item_name not in ALL_ITEMS_TABLE:
                print(f"Warning: Skipping Unknown Item '{item_name}'.")
                return

            location_data: MMXCMLocationData = LOCATION_TABLE[location_name]
            dol_address = location_data.ram_data

            item_data: MMXCMItemData = ALL_ITEMS_TABLE[item_name]
            # This access our item ID from our Data class to tell this randomizer WHICH item it is.
            # I.e. X Buster = 25
            item_rom_id = item_data.item_id

            # Writes the New Item ID to the DOL - - - - -
            # This coverts the Item ID into the byte sequence.
            item_id_bytes = struct.pack(">I", item_rom_id)
            self.dol.data.seek(dol_address)
            self.dol.data.write(item_id_bytes)

        except Exception as e:
            print(f"An error occured while writing data for location '{location_name}' and item '{item_name}': {e}")
            return

    def create_patch(self):
        """
        This function will take the base ROM, apply our changes and randomization data, and save the patched ROM.
        """

        if self.encounter_rate == 0:
            print("Applying Encounter Rate OFF Patch...")

            # First Address - Dash = remove adding the encounter rate. (fadds f1,f2,f3 -> fsubs f1,f2,f2)
            set_address = 0x074FC
            set_value = bytes([0xEC, 0x22, 0x10, 0x28])
            self.dol.data.seek(set_address)
            self.dol.data.write(set_value)
            print(f"Wrote {len(set_value)} bytes at address {hex(set_address)}.")

            # NOP The 1st Addition Command (For Dash 1)
            set_address = 0x07500
            set_value = bytes([0x60, 0x00, 0x00, 0x00])
            self.dol.data.seek(set_address)
            self.dol.data.write(set_value)
            print(f"Wrote {len(set_value)} bytes at address {hex(set_address)}.")

            # Second Address - Walk = Remove adding the encounter rate. (fadds f1,f1,f2 -> fsubs f1,f2,f2)
            reset_address = 0x0718C
            reset_value = bytes([0xEC, 0x22, 0x10, 0x28])
            self.dol.data.seek(reset_address)
            self.dol.data.write(reset_value)
            print(f"Wrote {len(reset_value)} bytes at address {hex(reset_address)}.")

            # NOP The 2nd Addition Command (For WALK 1)
            set_address = 0x07190
            set_value = bytes([0x60, 0x00, 0x00, 0x00])
            self.dol.data.seek(set_address)
            self.dol.data.write(set_value)
            print(f"Wrote {len(set_value)} bytes at address {hex(set_address)}.")

            # Third Address - Walk 2: + NOP to Remove adding the encounter rate. (fadds f1,f1,f2 -> fsubs f1,f2,f2)
            reset_address = 0x07118
            reset_value = bytes([0xEC, 0x22, 0x10, 0x28])
            self.dol.data.seek(reset_address)
            self.dol.data.write(reset_value)
            print(f"Wrote {len(reset_value)} bytes at address {hex(reset_address)}.")

            # NOP The 3rd Addition Command (For WALK 2)
            set_address = 0x0711C
            set_value = bytes([0x60, 0x00, 0x00, 0x00])
            self.dol.data.seek(set_address)
            self.dol.data.write(set_value)
            print(f"Wrote {len(set_value)} bytes at address {hex(set_address)}.")

            print("Encounter Rate OFF Patch Complete.")

        print("Applying Internal Code Patches...")

        for patch in CODE_PATCHES:
            try:
                address = patch["address"]
                data_to_write = bytes(patch["data"])

                # Seeks the specific DOL Offset.
                self.dol.data.seek(address)

                # Write the new bytes, overwriting old PowerPc command.
                self.dol.data.write(data_to_write)

                # We want to have GClib just do this to target the DOL!

                print(f"Wrote {len(data_to_write)} bytes at address {hex(address)}.")
            except KeyError as e:
                print(f"Skipping malformed patch data: missing key {e}")
            except Exception as e:
                print(f"An error occured while applying a code patch: {e}")
        print("Internal code patching complete.")

        # This is the loop for calling the REFACTORED item to location information above.
        print("Applying Randomized Item Patches...")
        for location_name, item_name in self.output_data["Locations"].items():
            self.write_item_to_location(location_name, item_name)
        print("Randomized item patching complete!")

        # Put the player name into the DOL Bytes.
        self.dol.data.seek(0x2E0D00)
        self.dol.data.write(sbf.string_to_bytes(self.output_data["Name"], MMXCM_PLAYER_NAME_BYTE_LENGTH))

        # Save all changes to the DOL itself.
        self.dol.save_changes()
        self.gcm.changed_files["sys/main.dol"] = self.dol.data

        # Generator function to combine all necessary files into an ISO file.
        # Returned information is ignored.
        for _, _ in self.export_files_from_memory():
            continue

            # If Export to disc is true, Exports the entire file/directory contents of the ISO to specified folder

    # Otherwise, creates a direct ISO file.
    def export_files_from_memory(self):
        yield from self.gcm.export_disc_to_iso_with_changed_files(self.randomized_output_file_path)