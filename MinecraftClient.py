import argparse
import json
import os
import sys
import re
import atexit
import shutil
from subprocess import Popen
from shutil import copyfile
from time import strftime
import logging

import requests

import Utils
from Utils import is_windows

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


def find_ap_randomizer_jar(forge_dir):
    """Create mods folder if needed; find AP randomizer jar; return None if not found."""
    mods_dir = os.path.join(forge_dir, 'mods')
    if os.path.isdir(mods_dir):
        for entry in os.scandir(mods_dir):
            if entry.name.startswith("aprandomizer") and entry.name.endswith(".jar"):
                logging.info(f"Found AP randomizer mod: {entry.name}")
                return entry.name
        return None
    else:
        os.mkdir(mods_dir)
        logging.info(f"Created mods folder in {forge_dir}")
        return None


def replace_apmc_files(forge_dir, apmc_file):
    """Create APData folder if needed; clean .apmc files from APData; copy given .apmc into directory."""
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


def read_apmc_file(apmc_file):
    from base64 import b64decode

    with open(apmc_file, 'r') as f:
        return json.loads(b64decode(f.read()))


def update_mod(forge_dir, url: str):
    """Check mod version, download new mod from GitHub releases page if needed. """
    ap_randomizer = find_ap_randomizer_jar(forge_dir)
    os.path.basename(url)
    if ap_randomizer is not None:
        logging.info(f"Your current mod is {ap_randomizer}.")
    else:
        logging.info(f"You do not have the AP randomizer mod installed.")

    if ap_randomizer != os.path.basename(url):
        logging.info(f"A new release of the Minecraft AP randomizer mod was found: "
                     f"{os.path.basename(url)}")
        if prompt_yes_no("Would you like to update?"):
            old_ap_mod = os.path.join(forge_dir, 'mods', ap_randomizer) if ap_randomizer is not None else None
            new_ap_mod = os.path.join(forge_dir, 'mods', os.path.basename(url))
            logging.info("Downloading AP randomizer mod. This may take a moment...")
            apmod_resp = requests.get(url)
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


def check_eula(forge_dir):
    """Check if the EULA is agreed to, and prompt the user to read and agree if necessary."""
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


def find_jdk_dir(version: str) -> str:
    """get the specified versions jdk directory"""
    for entry in os.listdir():
        if os.path.isdir(entry) and entry.startswith(f"jdk{version}"):
            return os.path.abspath(entry)


def find_jdk(version: str) -> str:
    """get the java exe location"""

    if is_windows:
        jdk = find_jdk_dir(version)
        jdk_exe = os.path.join(jdk, "bin", "java.exe")
        if os.path.isfile(jdk_exe):
            return jdk_exe
    else:
        jdk_exe = shutil.which(options["minecraft_options"].get("java", "java"))
        if not jdk_exe:
            raise Exception("Could not find Java. Is Java installed on the system?")
        return jdk_exe


def download_java(java: str):
    """Download Corretto (Amazon JDK)"""

    jdk = find_jdk_dir(java)
    if jdk is not None:
        print(f"Removing old JDK...")
        from shutil import rmtree
        rmtree(jdk)

    print(f"Downloading Java...")
    jdk_url = f"https://corretto.aws/downloads/latest/amazon-corretto-{java}-x64-windows-jdk.zip"
    resp = requests.get(jdk_url)
    if resp.status_code == 200:  # OK
        print(f"Extracting...")
        import zipfile
        from io import BytesIO
        with zipfile.ZipFile(BytesIO(resp.content)) as zf:
            zf.extractall()
    else:
        print(f"Error downloading Java (status code {resp.status_code}).")
        print(f"If this was not expected, please report this issue on the Archipelago Discord server.")
        if not prompt_yes_no("Continue anyways?"):
            sys.exit(0)


def install_forge(directory: str, forge_version: str, java_version: str):
    """download and install forge"""

    java_exe = find_jdk(java_version)
    if java_exe is not None:
        print(f"Downloading Forge {forge_version}...")
        forge_url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{forge_version}/forge-{forge_version}-installer.jar"
        resp = requests.get(forge_url)
        if resp.status_code == 200:  # OK
            forge_install_jar = os.path.join(directory, "forge_install.jar")
            if not os.path.exists(directory):
                os.mkdir(directory)
            with open(forge_install_jar, 'wb') as f:
                f.write(resp.content)
            print(f"Installing Forge...")
            install_process = Popen([java_exe, "-jar", forge_install_jar, "--installServer", directory])
            install_process.wait()
            os.remove(forge_install_jar)


def run_forge_server(forge_dir: str, java_version: str, heap_arg: str) -> Popen:
    """Run the Forge server."""

    java_exe = find_jdk(java_version)
    if not os.path.isfile(java_exe):
        java_exe = "java"  # try to fall back on java in the PATH

    heap_arg = max_heap_re.match(heap_arg).group()
    if heap_arg[-1] in ['b', 'B']:
        heap_arg = heap_arg[:-1]
    heap_arg = "-Xmx" + heap_arg

    os_args = "win_args.txt" if is_windows else "unix_args.txt"
    args_file = os.path.join(forge_dir, "libraries", "net", "minecraftforge", "forge", forge_version, os_args)
    forge_args = []
    with open(args_file) as argfile:
        for line in argfile:
            forge_args.extend(line.strip().split(" "))

    args = [java_exe, heap_arg, *forge_args, "-nogui"]
    logging.info(f"Running Forge server: {args}")
    os.chdir(forge_dir)
    return Popen(args)


def get_minecraft_versions(version, release_channel="release"):
    version_file_endpoint = "https://raw.githubusercontent.com/KonoTyran/Minecraft_AP_Randomizer/master/versions/minecraft_versions.json"
    resp = requests.get(version_file_endpoint)
    local = False
    if resp.status_code == 200:  # OK
        try:
            data = resp.json()
        except requests.exceptions.JSONDecodeError:
            logging.warning(f"Unable to fetch version update file, using local version. (status code {resp.status_code}).")
            local = True
    else:
        logging.warning(f"Unable to fetch version update file, using local version. (status code {resp.status_code}).")
        local = True

    if local:
        with open(Utils.user_path("minecraft_versions.json"), 'r') as f:
            data = json.load(f)
    else:
        with open(Utils.user_path("minecraft_versions.json"), 'w') as f:
            json.dump(data, f)

    try:
        if version:
            return next(filter(lambda entry: entry["version"] == version, data[release_channel]))
        else:
            return resp.json()[release_channel][0]
    except (StopIteration, KeyError):
        logging.error(f"No compatible mod version found for client version {version} on \"{release_channel}\" channel.")
        if release_channel != "release":
            logging.error("Consider switching \"release_channel\" to \"release\" in your Host.yaml file")
        else:
            logging.error("No suitable mod found on the \"release\" channel. Please Contact us on discord to report this error.")
        sys.exit(0)


def is_correct_forge(forge_dir) -> bool:
    if os.path.isdir(os.path.join(forge_dir, "libraries", "net", "minecraftforge", "forge", forge_version)):
        return True
    return False


if __name__ == '__main__':
    Utils.init_logging("MinecraftClient")
    parser = argparse.ArgumentParser()
    parser.add_argument("apmc_file", default=None, nargs='?', help="Path to an Archipelago Minecraft data file (.apmc)")
    parser.add_argument('--install', '-i', dest='install', default=False, action='store_true',
                        help="Download and install Java and the Forge server. Does not launch the client afterwards.")
    parser.add_argument('--release_channel', '-r', dest="channel", type=str, action='store',
                        help="Specify release channel to use.")
    parser.add_argument('--java', '-j', metavar='17', dest='java', type=str, default=False, action='store',
                        help="specify java version.")
    parser.add_argument('--forge', '-f', metavar='1.18.2-40.1.0', dest='forge', type=str, default=False, action='store',
                        help="specify forge version. (Minecraft Version-Forge Version)")
    parser.add_argument('--version', '-v', metavar='9', dest='data_version', type=int, action='store',
                        help="specify Mod data version to download.")

    args = parser.parse_args()
    apmc_file = os.path.abspath(args.apmc_file) if args.apmc_file else None

    # Change to executable's working directory
    os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))

    options = Utils.get_options()
    channel = args.channel or options["minecraft_options"]["release_channel"]
    apmc_data = None
    data_version = args.data_version or None

    if apmc_file is None and not args.install:
        apmc_file = Utils.open_filename('Select APMC file', (('APMC File', ('.apmc',)),))

    if apmc_file is not None and data_version is None:
        apmc_data = read_apmc_file(apmc_file)
        data_version = apmc_data.get('client_version', '')

    versions = get_minecraft_versions(data_version, channel)

    forge_dir = options["minecraft_options"]["forge_directory"]
    max_heap = options["minecraft_options"]["max_heap_size"]
    forge_version = args.forge or versions["forge"]
    java_version = args.java or versions["java"]
    mod_url = versions["url"]
    java_dir = find_jdk_dir(java_version)

    if args.install:
        if is_windows:
            print("Installing Java")
            download_java(java_version)
        if not is_correct_forge(forge_dir):
            print("Installing Minecraft Forge")
            install_forge(forge_dir, forge_version, java_version)
        else:
            print("Correct Forge version already found, skipping install.")
        sys.exit(0)

    if apmc_data is None:
        raise FileNotFoundError(f"APMC file does not exist or is inaccessible at the given location ({apmc_file})")

    if is_windows:
        if java_dir is None or not os.path.isdir(java_dir):
            if prompt_yes_no("Did not find java directory. Download and install java now?"):
                download_java(java_version)
                java_dir = find_jdk_dir(java_version)
            if java_dir is None or not os.path.isdir(java_dir):
                raise NotADirectoryError(f"Path {java_dir} does not exist or could not be accessed.")

    if not is_correct_forge(forge_dir):
        if prompt_yes_no(f"Did not find forge version {forge_version} download and install it now?"):
            install_forge(forge_dir, forge_version, java_version)
        if not os.path.isdir(forge_dir):
            raise NotADirectoryError(f"Path {forge_dir} does not exist or could not be accessed.")

    if not max_heap_re.match(max_heap):
        raise Exception(f"Max heap size {max_heap} in incorrect format. Use a number followed by M or G, e.g. 512M or 2G.")

    update_mod(forge_dir, mod_url)
    replace_apmc_files(forge_dir, apmc_file)
    check_eula(forge_dir)
    server_process = run_forge_server(forge_dir, java_version, max_heap)
    server_process.wait()
