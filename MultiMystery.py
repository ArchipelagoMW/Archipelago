__author__ = "Berserker55" # you can find me on the ALTTP Randomizer Discord
__version__ = 1.6

"""
This script launches a Multiplayer "Multiworld" Mystery Game

.yaml files for all participating players should be placed in a /Players folder.
For every player a mystery game is rolled and a ROM created.
After generation the server is automatically launched.
It is still up to the host to forward the correct port (38281 by default) and distribute the roms to the players.
Regular Mystery has to work for this first, such as a ALTTP Base ROM and Enemizer Setup.
A guide can be found here: https://docs.google.com/document/d/19FoqUkuyStMqhOq8uGiocskMo1KMjOW4nEeG81xrKoI/edit
Configuration can be found in host.yaml
"""

import os
import subprocess
import sys

def feedback(text:str):
    print(text)
    input("Press Enter to ignore and probably crash.")


if __name__ == "__main__":
    try:
        print(f"{__author__}'s MultiMystery Launcher V{__version__}")
        import ModuleUpdate
        ModuleUpdate.update()

        from Utils import parse_yaml

        multi_mystery_options = parse_yaml(open("host.yaml").read())["multi_mystery_options"]
        output_path = multi_mystery_options["output_path"]
        enemizer_path = multi_mystery_options["enemizer_path"]
        player_files_path = multi_mystery_options["player_files_path"]
        race = multi_mystery_options["race"]
        create_spoiler = multi_mystery_options["create_spoiler"]
        zip_roms = multi_mystery_options["zip_roms"]
        zip_spoiler = multi_mystery_options["zip_spoiler"]
        zip_multidata = multi_mystery_options["zip_multidata"]
        player_name = multi_mystery_options["player_name"]


        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"

        if not os.path.exists(enemizer_path):
            feedback(f"Enemizer not found at {enemizer_path}, please adjust the path in MultiMystery.py's config or put Enemizer in the default location.")
        if not os.path.exists("Zelda no Densetsu - Kamigami no Triforce (Japan).sfc"):
            feedback("Base rom is expected as Zelda no Densetsu - Kamigami no Triforce (Japan).sfc in the Multiworld root folder please place/rename it there.")
        player_files = []
        os.makedirs(player_files_path, exist_ok=True)
        for file in os.listdir(player_files_path):
            if file.lower().endswith(".yaml"):
                player_files.append(file)
                print(f"Player {file[:-5]} found.")
        player_count = len(player_files)
        if player_count == 0:
            feedback(f"No player files found. Please put them in a {player_files_path} folder.")
        else:
            print(player_count, "Players found.")

        player_string = ""
        for i,file in enumerate(player_files):
            player_string += f"--p{i+1} {os.path.join(player_files_path, file)} "

        player_names = list(file[:-5] for file in player_files)

        if os.path.exists("BerserkerMultiServer.exe"):
            basemysterycommand = "BerserkerMystery.exe" #compiled windows
        elif os.path.exists("BerserkerMultiServer"):
            basemysterycommand = "BerserkerMystery" # compiled linux
        else:
            basemysterycommand = f"py -{py_version} Mystery.py" #source

        command = f"{basemysterycommand} --multi {len(player_files)} {player_string} " \
                  f"--names {','.join(player_names)} --enemizercli {enemizer_path} " \
                  f"--outputpath {output_path}" + " --create_spoiler" if create_spoiler else "" + " --race" if race else ""
        print(command)
        import time
        start = time.perf_counter()
        text = subprocess.check_output(command, shell=True).decode()
        print(f"Took {time.perf_counter()-start:.3f} seconds to generate rom(s).")
        seedname = ""

        for segment in text.split():
            if segment.startswith("M"):
                seedname = segment
                break

        multidataname = f"ER_{seedname}_multidata"
        spoilername = f"ER_{seedname}_Spoiler.txt"
        romfilename = ""

        if player_name:
            for file in os.listdir(output_path):
                if player_name in file:
                    import webbrowser

                    romfilename = os.path.join(output_path, file)
                    print(f"Launching ROM file {romfilename}")
                    webbrowser.open(romfilename)
                    break

        if any((zip_roms, zip_multidata, zip_spoiler)):
            import zipfile

            def pack_file(file: str):
                zf.write(os.path.join(output_path, file), file)
                print(f"Packed {file} into zipfile {zipname}")

            def remove_zipped_file(file: str):
                os.remove(os.path.join(output_path, file))
                print(f"Removed {file} which is now present in the zipfile")

            zipname = os.path.join(output_path, f"ER_{seedname}.zip")
            print(f"Creating zipfile {zipname}")

            with zipfile.ZipFile(zipname, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                for file in os.listdir(output_path):
                    if zip_roms and file.endswith(".sfc") and seedname in file:
                        pack_file(file)
                        if zip_roms == 2 and player_name.lower() not in file.lower():
                            remove_zipped_file(file)
                if zip_multidata and os.path.exists(os.path.join(output_path, multidataname)):
                    pack_file(multidataname)
                    if zip_multidata == 2:
                        remove_zipped_file(multidataname)
                if zip_spoiler and create_spoiler:
                    pack_file(spoilername)
                    if zip_spoiler == 2:
                        remove_zipped_file(spoilername)

        if os.path.exists(os.path.join(output_path, multidataname)):
            if os.path.exists("BerserkerMultiServer.exe"):
                baseservercommand = "BerserkerMultiServer.exe"  # compiled windows
            elif os.path.exists("BerserkerMultiServer"):
                baseservercommand = "BerserkerMultiServer"  # compiled linux
            else:
                baseservercommand = f"py -{py_version} MultiServer.py"  # source
            #don't have a mac to test that. If you try to run compiled on mac, good luck.

            subprocess.call(f"{baseservercommand} --multidata {os.path.join(output_path, multidataname)}")
    except:
        import traceback
        traceback.print_exc()
        input("Press enter to close")
