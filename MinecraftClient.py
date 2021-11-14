import argparse
import os, sys
import re
import atexit
from subprocess import Popen
from shutil import copyfile
from time import strftime
import logging

import requests

import Utils

atexit.register(input, "Press enter to exit.")

# 1 or more digits followed by m or g, then optional b
max_heap_re = re.compile(r"^\d+[mMgG][bB]?$")


def prompt_yes_no(prompt):
    yes_inputs = {'yes', 'ye', 'y'}
    no_inputs = {'no', 'n'}
    while True:
        choice = input(prompt + " [y/n] ").lower()
        if choice in yes_inputs: 
            return True
        elif choice in no_inputs: 
            return False
        else:
            print('Please respond with "y" or "n".')


# Find Forge jar file; raise error if not found 
def find_forge_jar(forge_dir):
    for entry in os.scandir(forge_dir):
        if ".jar" in entry.name and "forge" in entry.name:
            logging.info(f"Found forge .jar: {entry.name}")
            return entry.name
    raise FileNotFoundError(f"Could not find forge .jar in {forge_dir}.")


# Create mods folder if needed; find AP randomizer jar; return None if not found.
def find_ap_randomizer_jar(forge_dir):
    mods_dir = os.path.join(forge_dir, 'mods')
    if os.path.isdir(mods_dir):
        ap_mod_re = re.compile(r"^aprandomizer-[\d\.]+\.jar$")
        for entry in os.scandir(mods_dir):
            match = ap_mod_re.match(entry.name)
            if match:
                logging.info(f"Found AP randomizer mod: {match.group()}")
                return match.group()
        return None
    else:
        os.mkdir(mods_dir)
        logging.info(f"Created mods folder in {forge_dir}")
        return None


# Create APData folder if needed; clean .apmc files from APData; copy given .apmc into directory.
def replace_apmc_files(forge_dir, apmc_file):
    if apmc_file is None:
        return
    apdata_dir = os.path.join(forge_dir, 'APData')
    copy_apmc = True
    if not os.path.isdir(apdata_dir):
        os.mkdir(apdata_dir)
        logging.info(f"Created APData folder in {forge_dir}")
    for entry in os.scandir(apdata_dir):
        if entry.name.endswith(".apmc") and entry.is_file():
            if not os.path.samefile(apmc_file, entry.path):
                os.remove(entry.path)
                logging.info(f"Removed {entry.name} in {apdata_dir}")
            else: # apmc already in apdata
                copy_apmc = False
    if copy_apmc:
        copyfile(apmc_file, os.path.join(apdata_dir, os.path.basename(apmc_file)))
        logging.info(f"Copied {os.path.basename(apmc_file)} to {apdata_dir}")


# Check mod version, download new mod from GitHub releases page if needed. 
def update_mod(forge_dir):
    ap_randomizer = find_ap_randomizer_jar(forge_dir)

    client_releases_endpoint = "https://api.github.com/repos/KonoTyran/Minecraft_AP_Randomizer/releases"
    resp = requests.get(client_releases_endpoint)
    if resp.status_code == 200:  # OK
        latest_release = resp.json()[0]
        if ap_randomizer != latest_release['assets'][0]['name']:
            logging.info(f"A new release of the Minecraft AP randomizer mod was found: "
                         f"{latest_release['assets'][0]['name']}")
            if ap_randomizer is not None:
                logging.info(f"Your current mod is {ap_randomizer}.")
            else:
                logging.info(f"You do not have the AP randomizer mod installed.")
            if prompt_yes_no("Would you like to update?"):
                old_ap_mod = os.path.join(forge_dir, 'mods', ap_randomizer) if ap_randomizer is not None else None
                new_ap_mod = os.path.join(forge_dir, 'mods', latest_release['assets'][0]['name'])
                logging.info("Downloading AP randomizer mod. This may take a moment...")
                apmod_resp = requests.get(latest_release['assets'][0]['browser_download_url'])
                if apmod_resp.status_code == 200: 
                    with open(new_ap_mod, 'wb') as f:
                        f.write(apmod_resp.content)
                        logging.info(f"Wrote new mod file to {new_ap_mod}")
                    if old_ap_mod is not None:
                        os.remove(old_ap_mod)
                        logging.info(f"Removed old mod file from {old_ap_mod}")
                else:
                    logging.error(f"Error retrieving the randomizer mod (status code {apmod_resp.status_code}).")
                    logging.error(f"Please report this issue on the Archipelago Discord server.")
                    sys.exit(1)
    else:
        logging.error(f"Error checking for randomizer mod updates (status code {resp.status_code}).")
        logging.error(f"If this was not expected, please report this issue on the Archipelago Discord server.")
        if not prompt_yes_no("Continue anyways?"):
            sys.exit(0)


# Check if the EULA is agreed to, and prompt the user to read and agree if necessary.
def check_eula(forge_dir):
    eula_path = os.path.join(forge_dir, "eula.txt")
    if not os.path.isfile(eula_path):
        # Create eula.txt
        with open(eula_path, 'w') as f:
            f.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n")
            f.write(f"#{strftime('%a %b %d %X %Z %Y')}\n")
            f.write("eula=false\n")
    with open(eula_path, 'r+') as f:
        text = f.read()
        if 'false' in text:
            # Prompt user to agree to the EULA
            logging.info("You need to agree to the Minecraft EULA in order to run the server.")
            logging.info("The EULA can be found at https://account.mojang.com/documents/minecraft_eula")
            if prompt_yes_no("Do you agree to the EULA?"):
                f.seek(0)
                f.write(text.replace('false', 'true'))
                f.truncate()
                logging.info(f"Set {eula_path} to true")
            else:
                sys.exit(0)


# Run the Forge server. Return process object
def run_forge_server(forge_dir, heap_arg):
    forge_server = find_forge_jar(forge_dir)

    java_exe = os.path.abspath(os.path.join('jre8', 'bin', 'java.exe'))
    if not os.path.isfile(java_exe):
        java_exe = "java"  # try to fall back on java in the PATH

    heap_arg = max_heap_re.match(max_heap).group()
    if heap_arg[-1] in ['b', 'B']:
        heap_arg = heap_arg[:-1]
    heap_arg = "-Xmx" + heap_arg

    argstring = ' '.join([java_exe, heap_arg, "-jar", forge_server, "-nogui"])
    logging.info(f"Running Forge server: {argstring}")
    os.chdir(forge_dir)
    return Popen(argstring)


if __name__ == '__main__':
    Utils.init_logging("MinecraftClient")
    parser = argparse.ArgumentParser()
    parser.add_argument("apmc_file", default=None, nargs='?', help="Path to an Archipelago Minecraft data file (.apmc)")

    args = parser.parse_args()
    apmc_file = os.path.abspath(args.apmc_file) if args.apmc_file else None

    # Change to executable's working directory
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
    
    options = Utils.get_options()
    forge_dir = options["minecraft_options"]["forge_directory"]
    max_heap = options["minecraft_options"]["max_heap_size"]

    if apmc_file is not None and not os.path.isfile(apmc_file):
        raise FileNotFoundError(f"Path {apmc_file} does not exist or could not be accessed.")
    if not os.path.isdir(forge_dir):
        raise NotADirectoryError(f"Path {forge_dir} does not exist or could not be accessed.")
    if not max_heap_re.match(max_heap):
        raise Exception(f"Max heap size {max_heap} in incorrect format. Use a number followed by M or G, e.g. 512M or 2G.")

    update_mod(forge_dir)
    replace_apmc_files(forge_dir, apmc_file)
    check_eula(forge_dir)
    server_process = run_forge_server(forge_dir, max_heap)
    server_process.wait()
