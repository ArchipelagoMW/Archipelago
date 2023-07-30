import os
import shutil
import unittest
import zipfile
from pathlib import Path
from typing import List

from worlds import WorldSource
from worlds.AutoWorld import AutoWorldRegister


class TestAPWorld(unittest.TestCase):
    def test_packing(self):
        # setup.py is written assumed it's __main__ so redefine this here.
        non_apworlds = ["A Link to the Past", "Adventure", "ArchipIDLE", "Archipelago", "Blasphemous", "ChecksFinder",
                        "Clique", "DLCQuest", "Dark Souls III", "Final Fantasy", "Hollow Knight", "Hylics 2",
                        "Kingdom Hearts 2", "Lufia II Ancient Cave", "Meritous", "Ocarina of Time", "Overcooked! 2",
                        "Pokemon Red and Blue", "Raft", "Secret of Evermore", "Slay the Spire",
                        "Starcraft 2 Wings of Liberty", "Sudoku", "Super Mario 64", "VVVVVV", "Wargroove", "Zillion"]
        non_apworld_dirs = [os.path.dirname(world.__file__)
                            for game, world in AutoWorldRegister.world_types.items() if game in non_apworlds]
        test_worlds = {game: world for game, world in AutoWorldRegister.world_types.items() if game not in non_apworlds}
        # clear world_types so the apworlds are registerable
        AutoWorldRegister.world_types = {}
        for game_name, world_type in test_worlds.items():
            directory = Path(os.path.dirname(world_type.__file__))
            apworld_path = f"{directory}.apworld"
            # create the apworld
            with zipfile.ZipFile(apworld_path, "x", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
                for path in directory.rglob("*.*"):
                    relative_path = os.path.join(*path.parts[path.parts.index("worlds")+1:])
                    z.write(path, relative_path)
            # temporarily move the world folder to worlds_disabled
            copy_path = Path(os.path.dirname(world_type.__file__).replace("worlds", "worlds_disabled"))
            shutil.copytree(directory, copy_path)
            shutil.rmtree(directory)
        
        world_sources: List[WorldSource] = []
        with self.subTest("apworld created"):
            for file in os.scandir(Path(non_apworld_dirs[0]).parent):
                if not file.name.startswith(("_", ".")) and file.name in non_apworld_dirs:
                    self.assertTrue(file.is_file() and file.name.endswith(".apworld"))
                    world_sources.append(WorldSource(file.name, is_zip=True))
        
        # the actual test
        world_sources.sort()
        for source in world_sources:
            with self.subTest("APWorld", file_path=source.path):
                source.load()

        # cleanup which we want to do even if the test fails
        for game_name, world_type in test_worlds.items():
            directory = Path(os.path.dirname(world_type.__file__))
            apworld_path = f"{directory}.apworld"
            copy_path = Path(os.path.dirname(world_type.__file__).replace("worlds", "worlds_disabled"))
            shutil.copytree(copy_path, directory)
            shutil.rmtree(copy_path)
            os.remove(apworld_path)
