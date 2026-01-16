import os
import json
import struct, zipfile

from gclib.gcm import GCM
from gclib.dol import DOL

import Utils

from ..items import ITEM_TABLE, PSOItemData
from ..locations import LOCATION_TABLE, PSOLocationData
from ..helpers import CLIENT_VERSION, SLOT_NAME_ADDR, string_to_bytes
from .dol_changes import CODE_PATCHES

PSO_PLAYER_NAME_BYTE_LENGTH = 0x40

AP_WORLD_VERSION_NAME = "APWorldVersion"

class PSOPatcher:
    def __init__(self, patch_file_path: str):
        from .rom_patch import get_base_rom_path, PSOPatch
        self.clean_iso_path = get_base_rom_path()

        base_path = os.path.splitext(patch_file_path)[0]
        self.randomized_output_file_path = base_path + PSOPatch.result_file_ending
        self.gcm = None
        self.dol = None

        try:
            if os.path.isfile(patch_file_path):
                temp_file = open(patch_file_path, "r+")
                temp_file.close()
        except IOError:
            raise Exception("'" + patch_file_path + "' is currently used in another program.")

        with zipfile.ZipFile(patch_file_path, "r") as zf:
            appso_bytes = zf.read("patch.appso")
        self.output_data = json.loads(appso_bytes.decode('utf-8'))

        # Check to make sure the client and server versions match
        self._check_apworld_version(self.output_data)

        # Grab the player's options from the YAML
        self.options = self.output_data.get("Options", {})

        # Read the entire iso, system files, to... TODO: Why do we do this?
        self.gcm = GCM(self.clean_iso_path)
        self.gcm.read_entire_disc()
        self.dol = DOL()
        self.dol.read(self.gcm.read_file_data("sys/main.dol"))

        from CommonClient import logger
        logger.info("Updating the ISO game id with the AP generated seed.")

        self.seed = self.output_data["Seed"]
        magic_seed = str(self.seed)
        bin_data = self.gcm.read_file_data("sys/boot.bin")
        bin_data.seek(0x01)
        bin_data.write(string_to_bytes(magic_seed, len(magic_seed)))
        self.gcm.changed_files["sys/boot.bin"] = bin_data


    def _check_apworld_version(self, output_data):
        """
        Compare the AP version in the patch to the client version.

        :param output_data: json-formatted data from reading the patch file
        """

        ap_world_version = output_data[AP_WORLD_VERSION_NAME]
        if ap_world_version != CLIENT_VERSION:
            raise Utils.VersionException("Error! Server was generated with a different MMXCM Seed!")


    def write_item_to_location(self, location_name: str, item_name: str):
        """
        Look up the correct addresses and IDs for items and write them into the ROM
        """
        try:
            # Verify we have data for the location being read
            if location_name not in LOCATION_TABLE:
                print(f"Warning: Skipping unknown '{location_name}'.")
                return

            # Verify we have data for the item being read
            if item_name not in ITEM_TABLE:
                print(f"Warning: Skipping Unknown Item '{item_name}'.")
                return

            location_data: PSOLocationData = LOCATION_TABLE[location_name]
            dol_address = location_data.ram_data.ram_addr

            item_data: PSOItemData = ITEM_TABLE[item_name]
            # Access our unique item ID/code from our Data class to tell this randomizer WHICH item it is
            # e.g. Lavis Blade = 18

            # Write the New Item ID to the DOL
            # Covert the Item ID into the byte sequence
            item_id_bytes = struct.pack(">I", item_data.code)
            self.dol.data.seek(dol_address)
            self.dol.data.write(item_id_bytes)

        except Exception as error:
            print(f"An error occurred while writing data for location '{location_name}' and item '{item_name}': {error}")
            return


    def create_patch(self):
        """
        Take the base ROM, apply our changes and randomization data, and save the patched ROM
        """

        print("Applying Internal Code Patches...")

        for patch in CODE_PATCHES:
            address = patch.address

            try:
                data_to_write = bytes(patch.data)

                # Seeks the specific DOL Offset.
                self.dol.data.seek(address)

                # Write the new bytes, overwriting old PowerPc command.
                self.dol.data.write(data_to_write)

                # We want to have GClib just do this to target the DOL!
                # TODO: Is this always 4 bytes?
                print(f"Wrote {len(data_to_write)} bytes at address {hex(address)}.")
            except KeyError as error:
                print(f"Skipping malformed patch data: missing key {error}")
            except Exception as error:
                print(f"An error occurred while applying a code patch at address {hex(address)}: {error}")
        print("Internal code patching complete.")

        # This is the loop for calling the REFACTORED item to location information above.
        print("Applying Randomized Item Patches...")
        for location_name, item_name in self.output_data["Locations"].items():
            self.write_item_to_location(location_name, item_name)
        print("Randomized item patching complete!")

        # Put the player name into the DOL Bytes.
        self.dol.data.seek(SLOT_NAME_ADDR)
        self.dol.data.write(string_to_bytes(self.output_data["Name"], PSO_PLAYER_NAME_BYTE_LENGTH))

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