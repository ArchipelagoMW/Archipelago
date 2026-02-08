import logging

import yaml
import os
import Utils
import zipfile

from datetime import datetime, UTC

from worlds.Files import APPlayerContainer

# This is used to create the data file that will be downloaded for the player. Check out \world\file.py for more information on APPlayerContainer.
class EVNContainer(APPlayerContainer):
    game: str = 'EV Nova'
    patch_file_ending = ".zip"

    def __init__(self, patch_data: dict, base_path: str, output_directory: str, player=None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.file_path = base_path
        container_path = os.path.join(output_directory, base_path + ".zip")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        for filename, yml in self.patch_data.items():
           opened_zipfile.writestr(filename, yml)
        #opened_zipfile.writestr("hello world.txt", "This is a test file.")
        super().write_contents(opened_zipfile)


# def patch_evn(self, output_directory):
    
#     curr_timestamp = datetime.strftime(datetime.now(UTC), "%d%b%Y-%H%M%S")
#     mod_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}-{curr_timestamp}"