import os
import shutil
import unittest
import zipfile
import zipimport
from pathlib import Path

from worlds.AutoWorld import AutoWorldRegister
from worlds import WorldSource


class TestAPWorld(unittest.TestCase):
    def test_packing(self):
        # setup.py is written assumed it's __main__ so redefine this here.
        non_apworlds = ["A Link to the Past", "Adventure", "ArchipIDLE", "Archipelago", "Blasphemous", "ChecksFinder",
                        "Clique", "DLCQuest", "Dark Souls III", "Final Fantasy", "Hollow Knight", "Hylics 2",
                        "Kingdom Hearts 2", "Lufia II Ancient Cave", "Meritous", "Ocarina of Time", "Overcooked! 2",
                        "Pokemon Red and Blue", "Raft", "Secret of Evermore", "Slay the Spire",
                        "Starcraft 2 Wings of Liberty", "Sudoku", "Super Mario 64", "VVVVVV", "Wargroove", "Zillion"]
        test_worlds = {game: world for game, world in AutoWorldRegister.world_types.items() if game not in non_apworlds}
        # clear world_types so the apworlds are registerable
        AutoWorldRegister.world_types = {}
        for game_name, world_type in test_worlds.items():
            with self.subTest("Game", game=game_name):
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
                # the actual test
                world_source = WorldSource(apworld_path, is_zip=True)
                world_source.load()
            # cleanup which we want to do even if the test fails
            shutil.copytree(copy_path, directory)
            shutil.rmtree(copy_path)
            os.remove(apworld_path)
