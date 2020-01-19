__author__ = "Berserker55" # you can find me on the ALTTP Randomizer Discord
__version__ = 1.5

"""
This script launches a Multiplayer "Multiworld" Mystery Game

.yaml files for all participating players should be placed in a /Players folder.
For every player a mystery game is rolled and a ROM created.
After generation the server is automatically launched.
It is still up to the host to forward the correct port (38281 by default) and distribute the roms to the players.
Regular Mystery has to work for this first, such as a ALTTP Base ROM and Enemizer Setup.
A guide can be found here: https://docs.google.com/document/d/19FoqUkuyStMqhOq8uGiocskMo1KMjOW4nEeG81xrKoI/edit
This script itself should be placed within the Bonta Multiworld folder, that you download in step 1
"""

####config####
#location of your Enemizer CLI, available here: https://github.com/Bonta0/Enemizer/releases
enemizer_location:str = "EnemizerCLI/EnemizerCLI.Core.exe"

#Where to place the resulting files
outputpath:str = "MultiMystery"

#automatically launches {player_name}.yaml's ROM file using the OS's default program once generation completes. (likely your emulator)
#does nothing if the name is not found
#example: player_name = "Berserker"
player_name:str = ""

#Zip the resulting roms
#0 -> Don't
#1 -> Create a zip
#2 -> Create a zip and delete the ROMs that will be in it, except the hosts (requires player_name to be set correctly)
zip_roms:int = 1

#create a spoiler file
create_spoiler:bool = True

#create roms as race coms
race:bool= False

#folder from which the player yaml files are pulled from
player_files_folder:str = "Players"

#Version of python to use for Bonta Multiworld. Probably leave this as is, if you don't know what this does.
#can be tagged for bitness, for example "3.8-32" would be latest installed 3.8 on 32 bits
#special case: None -> use the python which was used to launch this file.
py_version:str = None
####end of config####

import os
import subprocess
import sys

def feedback(text:str):
    print(text)
    input("Press Enter to ignore and probably crash.")


if __name__ == "__main__":
    try:
        if not py_version:
            py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        import ModuleUpdate
        ModuleUpdate.update()

        print(f"{__author__}'s MultiMystery Launcher V{__version__}")
        if not os.path.exists(enemizer_location):
            feedback(f"Enemizer not found at {enemizer_location}, please adjust the path in MultiMystery.py's config or put Enemizer in the default location.")
        if not os.path.exists("Zelda no Densetsu - Kamigami no Triforce (Japan).sfc"):
            feedback("Base rom is expected as Zelda no Densetsu - Kamigami no Triforce (Japan).sfc in the Multiworld root folder please place/rename it there.")
        player_files = []
        os.makedirs(player_files_folder, exist_ok=True)
        for file in os.listdir(player_files_folder):
            if file.lower().endswith(".yaml"):
                player_files.append(file)
                print(f"Player {file[:-5]} found.")
        player_count = len(player_files)
        if player_count == 0:
            feedback(f"No player files found. Please put them in a {player_files_folder} folder.")
        else:
            print(player_count, "Players found.")

        player_string = ""
        for i,file in enumerate(player_files):
            player_string += f"--p{i+1} {os.path.join(player_files_folder, file)} "

        player_names = list(file[:-5] for file in player_files)

        command = f"py -{py_version} Mystery.py --multi {len(player_files)} {player_string} " \
                  f"--names {','.join(player_names)} --enemizercli {enemizer_location} " \
                  f"--outputpath {outputpath}" + " --create_spoiler" if create_spoiler else "" + " --race" if race else ""
        print(command)
        import time
        start = time.perf_counter()
        text = subprocess.check_output(command, shell=True).decode()
        print(f"Took {time.perf_counter()-start:.3f} seconds to generate seed.")
        seedname = ""

        for segment in text.split():
            if segment.startswith("M"):
                seedname = segment
                break

        multidataname = f"ER_{seedname}_multidata"

        romfilename = ""
        if player_name:
            try:
                index = player_names.index(player_name)
            except IndexError:
                print(f"Could not find Player {player_name}")
            else:
                romfilename = os.path.join(outputpath, f"ER_{seedname}_P{index+1}_{player_name}.sfc")
                import webbrowser
                if os.path.exists(romfilename):
                    print(f"Launching ROM file {romfilename}")
                    webbrowser.open(romfilename)

        if zip_roms:
            zipname = os.path.join(outputpath, f"ER_{seedname}.zip")
            print(f"Creating zipfile {zipname}")
            import zipfile
            with zipfile.ZipFile(zipname, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
                for file in os.listdir(outputpath):
                    if file.endswith(".sfc") and seedname in file:
                        zf.write(os.path.join(outputpath, file), file)
                        print(f"Packed {file} into zipfile {zipname}")
                        if zip_roms == 2 and player_name.lower() not in file.lower():
                            os.remove(file)
                            print(f"Removed file {file} that is now present in the zipfile")

        subprocess.call(f"py -{py_version} MultiServer.py --multidata {os.path.join(outputpath, multidataname)}")
    except:
        import traceback
        traceback.print_exc()
        input("Press enter to close")
