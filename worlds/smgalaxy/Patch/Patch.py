import hashlib
from pathlib import Path
import os, time

from disc_riider_py import WiiIsoExtractor, rebuild_from_directory
from ooga_booga import create_new_files
from gclib.rarc import RARC

class InvalidCleanISOError(Exception): pass

# Name of the game, which is used in various error messaging.
RANDOMIZER_NAME: str = "Super Mario Galaxy"

# Can pull this from dolphin or a cmd command / bash command
CLEAN_MD5: int = 0xf99a97f9ae4dccd1db45e9aaab9cebd8

# Expected Game ID of the GC/Wii game we expect here.
EXPECTED_GAME_ID: str = "RMGE01"


iso_path = r"Super Mario Galaxy (USA) (En,Fr,Es).iso"

class WiiISO:
    
    def __init__(self, clean_iso_path: str, iso_name: str = RANDOMIZER_NAME + r" Patched", dest_path: str = r"", temp_dir: str = r"temp"):
        # Path of the unmodified iso
        self.clean_iso_path = clean_iso_path
        
        # Where it should place the repacked ISO
        self.dest_path = dest_path
        
        # Temporary path that can be used for the extracted ISO (to be removed later)
        self.temp_dir = temp_dir
        
        # Name of the new ISO
        self.iso_name = iso_name

        self.progress = -1
        self.calling_function = ''

    def verify_base_rom(self):
        """Verifies that the base Vanilla ROM against a few rules. First, the file is of type ISO, second, the MD5
        of the file matches against the one we expect, and third, we had a game id in the file that matches the games
        official one"""
        # Verifies we have a valid installation of Luigi's Mansion USA. There are some regional file differences.
        print(f"Verifying if the provided ISO is a valid copy of {RANDOMIZER_NAME}...")
        
        # Reads the file in chunks, as its too big as a file on its own and could lead to the python process slowing
        # down to process and read each byte. After reading each chunk, it updates and calculates the MD5
        base_md5 = hashlib.md5()
        with open(self.clean_iso_path, "rb") as f:
            while chunk := f.read(1024 * 1024):  # Read the file in chunks.
                base_md5.update(chunk)

            # Grab the Magic Code and Game_ID with the file still open
            f.seek(0)
            game_id = f.read(6).decode("shift_jis")
            magic = game_id[:4]
            print(f"Magic Code: {magic}; Game ID: {game_id}")

        # Verify that the file has the right has format first, as the wrong file could have been loaded.
        md5_conv = int(base_md5.hexdigest(), 16)
        if md5_conv != CLEAN_MD5:
            raise InvalidCleanISOError(f"Invalid vanilla {RANDOMIZER_NAME} ISO.\nYour ISO may be corrupted or your " +
                f"MD5 hashes do not match.\nCorrect ISO MD5 hash: {CLEAN_MD5:x}\nYour ISO's MD5 hash: {md5_conv}")

        # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
        # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
        if magic == "CISO":
            raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {RANDOMIZER_NAME} randomizer " +
                "only supports ISOs in ISO format.")
        if game_id != EXPECTED_GAME_ID:
            # Checks this starts with "RMG" at least, otherwise user provided an entirely different game.
            if game_id and game_id.startswith(EXPECTED_GAME_ID[:3]):
                raise InvalidCleanISOError(f"Invalid version of {RANDOMIZER_NAME}. " +
                    "Currently, only the North American / English version is supported by this randomizer.")
            else:
                raise InvalidCleanISOError(f"Non-{RANDOMIZER_NAME} game detected. Please re-select the vanilla " +
                    f"{RANDOMIZER_NAME}'s ISO (North American version).")
        return

    def extract_iso(self):
        """Extracts the ISO into the output directory, preserving the orignal file/folder structure within the ISO.
        Once extracted, you can then read these files individually to change/edit, create new folders/files in the
        structure or delete old ones."""

        try:
            # Makes sure the file exists
            if not Path(self.clean_iso_path).exists():
                raise Exception(f"ISO file not found: {self.iso_path}")
                
            # Extract the Wii file into memory and load all the disc partitions/disc structure.
            extractor: WiiIsoExtractor = WiiIsoExtractor(self.clean_iso_path)

            # Prepare the Data section of the disc by reading its file metadata into memory.
            extractor.prepare_extract_section("DATA")

            # Once prepared, we can export it to a directory of our choice.
            print("Initiating extracting ISO")
            self.calling_function = 'extract_iso'
            extractor.extract_to(self.temp_dir, self.progress_callback)

        except Exception as e:
            raise Exception(f"ISO extraction failed: {e}")

    def repack_iso(self):
        """Takes an extracted ISO directory and re-compiles it into a playable Wii ISO."""
        output_path = Path(self.dest_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print("Initiating repacking ISO")
        self.calling_function = 'repack_iso'
        rebuild_from_directory(self.temp_dir, self.dest_path + self.iso_name + '.iso', callback=self.progress_callback)
        
        # Delete the extracted ISO after its done repacking
        time.sleep(3)
        self._delete_temp_dir(self.temp_dir)
        
    def _delete_temp_dir(self, temp_dir):
        """Remove the temporarily created directory for the extracted ISO"""
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            
            # Remove it if its a file otherwise recurse
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleting temp file: {file_path}")
            else:
                self._delete_temp_dir(file_path)
        
        print(f"Deleting empty directory: {temp_dir}")
        os.rmdir(temp_dir)

    def progress_callback(self, progress):
        """Prints the progress as the callback is completing its steps."""
        out = ''
        
        if self.calling_function == 'repack_iso':
            out = "repacking ISO"
        elif self.calling_function == 'extract_iso':
            out = "extracting ISO"
        
        if progress % 10 == 0:
            if self.progress != progress:
                self.progress = progress
                print(f"Progress {out}: {self.progress}%")

if __name__ == '__main__':
    iso = WiiISO(iso_path)
    
    iso.verify_base_rom()
    iso.extract_iso()
    
    astrodome_file = iso.temp_dir + r"/DATA/files/StageData/AstroDome.arc"
    
    astrodome = RARC(astrodome_file)
    
    files = create_new_files()
    
    for i, file in enumerate(files):
        objinfo_entry = astrodome.get_node_by_path('').files[1].node.files[6].node.files[i+1].node.files[3]
        new_data = open(file,'rb').read()
        objinfo_entry.data.write(new_data)
        astrodome.get_node_by_path('').files[1].node.files[6].node.files[i+1].node.files[3] = objinfo_entry
        
    astrodome.save_changes()
    
    with open(astrodome_file, 'wb') as f:
        astrodome.data.seek(0)
        f.write(astrodome.data.read())
    
    iso.repack_iso()