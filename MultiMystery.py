__author__ = "Berserker55"  # you can find me on discord.gg/8Z65BR2

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
import threading
import concurrent.futures
import argparse
import logging


def feedback(text: str):
    logging.info(text)
    input("Press Enter to ignore and probably crash.")


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    try:
        logging.info(f"{__author__}'s MultiMystery Launcher")
        import ModuleUpdate

        ModuleUpdate.update()

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('--disable_autohost', action='store_true')
        args = parser.parse_args()

        from Utils import get_public_ipv4, get_options

        from Patch import create_patch_file

        options = get_options()

        multi_mystery_options = options["multi_mystery_options"]
        output_path = options["general_options"]["output_path"]
        enemizer_path = multi_mystery_options["enemizer_path"]
        player_files_path = multi_mystery_options["player_files_path"]
        target_player_count = multi_mystery_options["players"]
        race = multi_mystery_options["race"]
        plando_options = multi_mystery_options["plando_options"]
        create_spoiler = multi_mystery_options["create_spoiler"]
        zip_roms = multi_mystery_options["zip_roms"]
        zip_diffs = multi_mystery_options["zip_diffs"]
        zip_spoiler = multi_mystery_options["zip_spoiler"]
        zip_multidata = multi_mystery_options["zip_multidata"]
        zip_format = multi_mystery_options["zip_format"]
        # zip_password = multi_mystery_options["zip_password"] not at this time
        player_name = multi_mystery_options["player_name"]
        meta_file_path = multi_mystery_options["meta_file_path"]
        weights_file_path = multi_mystery_options["weights_file_path"]
        pre_roll = multi_mystery_options["pre_roll"]
        teams = multi_mystery_options["teams"]
        rom_file = options["general_options"]["rom_file"]
        host = options["server_options"]["host"]
        port = options["server_options"]["port"]

        py_version = f"{sys.version_info.major}.{sys.version_info.minor}"

        if not os.path.exists(enemizer_path):
            feedback(
                f"Enemizer not found at {enemizer_path}, please adjust the path in MultiMystery.py's config or put Enemizer in the default location.")
        if not os.path.exists(rom_file):
            feedback(f"Base rom is expected as {rom_file} in the Multiworld root folder please place/rename it there.")
        player_files = []
        os.makedirs(player_files_path, exist_ok=True)
        for file in os.listdir(player_files_path):
            lfile = file.lower()
            if lfile.endswith(".yaml") and lfile != meta_file_path.lower() and lfile != weights_file_path.lower():
                player_files.append(file)
                logging.info(f"Found player's file {file}.")

        player_string = ""
        for i, file in enumerate(player_files, 1):
            player_string += f"--p{i} \"{os.path.join(player_files_path, file)}\" "

        if os.path.exists("BerserkerMultiServer.exe"):
            basemysterycommand = "BerserkerMystery.exe"  # compiled windows
        elif os.path.exists("BerserkerMultiServer"):
            basemysterycommand = "BerserkerMystery"  # compiled linux
        else:
            basemysterycommand = f"py -{py_version} Mystery.py"  # source

        weights_file_path = os.path.join(player_files_path, weights_file_path)
        if os.path.exists(weights_file_path):
            target_player_count = max(len(player_files), target_player_count)
        else:
            target_player_count = len(player_files)

        if target_player_count == 0:
            feedback(f"No player files found. Please put them in a {player_files_path} folder.")
        else:
            logging.info(f"{target_player_count} Players found.")

        command = f"{basemysterycommand} --multi {target_player_count} {player_string} " \
                  f"--rom \"{rom_file}\" --enemizercli \"{enemizer_path}\" " \
                  f"--outputpath \"{output_path}\" --teams {teams} --plando \"{plando_options}\""

        if create_spoiler:
            command += " --create_spoiler"
            if create_spoiler == 2:
                command += " --skip_playthrough"
        if zip_diffs:
            command += " --create_diff"
        if race:
            command += " --race"
        if os.path.exists(os.path.join(player_files_path, meta_file_path)):
            command += f" --meta {os.path.join(player_files_path, meta_file_path)}"
        if os.path.exists(weights_file_path):
            command += f" --weights {weights_file_path}"
        if pre_roll:
            command += " --pre_roll"

        logging.info(command)
        import time

        start = time.perf_counter()
        text = subprocess.check_output(command, shell=True).decode()
        logging.info(f"Took {time.perf_counter() - start:.3f} seconds to generate multiworld.")
        seedname = ""

        for segment in text.split():
            if segment.startswith("M"):
                seedname = segment
                break

        multidataname = f"BM_{seedname}.multidata"
        spoilername = f"BM_{seedname}_Spoiler.txt"
        romfilename = ""

        if player_name:
            for file in os.listdir(output_path):
                if player_name in file:
                    import MultiClient
                    import asyncio

                    asyncio.run(MultiClient.run_game(os.path.join(output_path, file)))
                    break

        if any((zip_roms, zip_multidata, zip_spoiler, zip_diffs)):
            import zipfile

            compression = {1: zipfile.ZIP_DEFLATED,
                           2: zipfile.ZIP_LZMA,
                           3: zipfile.ZIP_BZIP2}[zip_format]

            typical_zip_ending = {1: "zip",
                                  2: "7z",
                                  3: "bz2"}[zip_format]

            ziplock = threading.Lock()


            def pack_file(file: str):
                with ziplock:
                    zf.write(os.path.join(output_path, file), file)
                    logging.info(f"Packed {file} into zipfile {zipname}")


            def remove_zipped_file(file: str):
                os.remove(os.path.join(output_path, file))
                logging.info(f"Removed {file} which is now present in the zipfile")


            zipname = os.path.join(output_path, f"BM_{seedname}.{typical_zip_ending}")

            logging.info(f"Creating zipfile {zipname}")
            ipv4 = (host if host else get_public_ipv4()) + ":" + str(port)


            def _handle_sfc_file(file: str):
                if zip_roms:
                    pack_file(file)
                    if zip_roms == 2 and player_name.lower() not in file.lower():
                        remove_zipped_file(file)


            def _handle_diff_file(file: str):
                if zip_diffs > 0:
                    pack_file(file)
                    if zip_diffs == 2:
                        remove_zipped_file(file)


            with concurrent.futures.ThreadPoolExecutor() as pool:
                futures = []
                with zipfile.ZipFile(zipname, "w", compression=compression, compresslevel=9) as zf:
                    for file in os.listdir(output_path):
                        if seedname in file:
                            if file.endswith(".sfc"):
                                futures.append(pool.submit(_handle_sfc_file, file))
                            elif file.endswith(".bmbp"):
                                futures.append(pool.submit(_handle_diff_file, file))

                    if zip_multidata and os.path.exists(os.path.join(output_path, multidataname)):
                        pack_file(multidataname)
                        if zip_multidata == 2:
                            remove_zipped_file(multidataname)

                    if zip_spoiler and create_spoiler:
                        pack_file(spoilername)
                        if zip_spoiler == 2:
                            remove_zipped_file(spoilername)

                    for future in futures:
                        future.result()  # make sure we close the zip AFTER any packing is done

        if not args.disable_autohost:
            if os.path.exists(os.path.join(output_path, multidataname)):
                if os.path.exists("BerserkerMultiServer.exe"):
                    baseservercommand = "BerserkerMultiServer.exe"  # compiled windows
                elif os.path.exists("BerserkerMultiServer"):
                    baseservercommand = "BerserkerMultiServer"  # compiled linux
                else:
                    baseservercommand = f"py -{py_version} MultiServer.py"  # source
                # don't have a mac to test that. If you try to run compiled on mac, good luck.

                subprocess.call(f"{baseservercommand} --multidata {os.path.join(output_path, multidataname)}")
    except:
        import traceback

        traceback.print_exc()
        input("Press enter to close")
