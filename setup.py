import os
import shutil
import sys
import sysconfig
from pathlib import Path

import ModuleUpdate
# I don't really want to have another root directory file for a single requirement, but this special case is also jank.
# Might move this into a cleaner solution when I think of one.
with open("freeze_requirements.txt", "w") as f:
    f.write("cx-Freeze>=6.9\n")
ModuleUpdate.requirements_files.add("freeze_requirements.txt")
ModuleUpdate.requirements_files.add(os.path.join("WebHostLib", "requirements.txt"))
ModuleUpdate.update()

import cx_Freeze
from kivy_deps import sdl2, glew
from Utils import version_tuple

arch_folder = "exe.{platform}-{version}".format(platform=sysconfig.get_platform(),
                                                version=sysconfig.get_python_version())
buildfolder = Path("build", arch_folder)
sbuildfolder = str(buildfolder)
libfolder = Path(buildfolder, "lib")
library = Path(libfolder, "library.zip")
print("Outputting to: " + sbuildfolder)

icon = os.path.join("data", "icon.ico")
mcicon = os.path.join("data", "mcicon.ico")

if os.path.exists("X:/pw.txt"):
    print("Using signtool")
    with open("X:/pw.txt") as f:
        pw = f.read()
    signtool = r'signtool sign /f X:/_SITS_Zertifikat_.pfx /p ' + pw + r' /fd sha256 /tr http://timestamp.digicert.com/ '
else:
    signtool = None

from hashlib import sha3_512
import base64


def _threaded_hash(filepath):
    hasher = sha3_512()
    hasher.update(open(filepath, "rb").read())
    return base64.b85encode(hasher.digest()).decode()


os.makedirs(buildfolder, exist_ok=True)


def manifest_creation(folder, create_hashes=False):
    # Since the setup is now split into components and the manifest is not,
    # it makes most sense to just remove the hashes for now. Not aware of anyone using them.
    hashes = {}
    manifestpath = os.path.join(folder, "manifest.json")
    if create_hashes:
        from concurrent.futures import ThreadPoolExecutor
        pool = ThreadPoolExecutor()
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                hashes[os.path.relpath(path, start=folder)] = pool.submit(_threaded_hash, path)

    import json
    manifest = {
        "buildtime": buildtime.isoformat(sep=" ", timespec="seconds"),
        "hashes": {path: hash.result() for path, hash in hashes.items()},
        "version": version_tuple}

    json.dump(manifest, open(manifestpath, "wt"), indent=4)
    print("Created Manifest")


def remove_sprites_from_folder(folder):
    for file in os.listdir(folder):
        if file != ".gitignore":
            os.remove(folder / file)


scripts = {
    # Core
    "MultiServer.py": ("ArchipelagoServer", False, icon),
    "Generate.py": ("ArchipelagoGenerate", False, icon),
    "CommonClient.py": ("ArchipelagoTextClient", True, icon),
    # SNI
    "SNIClient.py": ("ArchipelagoSNIClient", True, icon),
    "LttPAdjuster.py": ("ArchipelagoLttPAdjuster", True, icon),
    # Factorio
    "FactorioClient.py": ("ArchipelagoFactorioClient", True, icon),
    # Minecraft
    "MinecraftClient.py": ("ArchipelagoMinecraftClient", False, mcicon),
    # Ocarina of Time
    "OoTClient.py": ("ArchipelagoOoTClient", True, icon),
    "OoTAdjuster.py": ("ArchipelagoOoTAdjuster", True, icon),
    # FF1
    "FF1Client.py": ("ArchipelagoFF1Client", True, icon),
}

exes = []

for script, (scriptname, gui, icon) in scripts.items():
    exes.append(cx_Freeze.Executable(
        script=script,
        target_name=scriptname + ("" if sys.platform == "linux" else ".exe"),
        icon=icon,
        base="Win32GUI" if sys.platform == "win32" and gui else None
    ))

import datetime

buildtime = datetime.datetime.utcnow()

cx_Freeze.setup(
    name="Archipelago",
    version=f"{version_tuple.major}.{version_tuple.minor}.{version_tuple.build}",
    description="Archipelago",
    executables=exes,
    options={
        "build_exe": {
            "packages": ["websockets", "worlds", "kivy"],
            "includes": [],
            "excludes": ["numpy", "Cython", "PySide2", "PIL",
                         "pandas"],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": ["worlds", "kivy"],
            "include_files": [],
            "include_msvcr": False,
            "replace_paths": [("*", "")],
            "optimize": 1,
            "build_exe": buildfolder
        },
    },
)


def installfile(path, keep_content=False):
    lbuildfolder = buildfolder
    print('copying', path, '->', lbuildfolder)
    if path.is_dir():
        lbuildfolder /= path.name
        if lbuildfolder.is_dir() and not keep_content:
            shutil.rmtree(lbuildfolder)
        shutil.copytree(path, lbuildfolder, dirs_exist_ok=True)
    elif path.is_file():
        shutil.copy(path, lbuildfolder)
    else:
        print('Warning,', path, 'not found')


for folder in sdl2.dep_bins + glew.dep_bins:
    shutil.copytree(folder, libfolder, dirs_exist_ok=True)
    print('copying', folder, '->', libfolder)

extra_data = ["LICENSE", "data", "EnemizerCLI", "host.yaml", "SNI"]

for data in extra_data:
    installfile(Path(data))

os.makedirs(buildfolder / "Players" / "Templates", exist_ok=True)
from WebHostLib.options import create
create()
from worlds.AutoWorld import AutoWorldRegister
for worldname, worldtype in AutoWorldRegister.world_types.items():
    if not worldtype.hidden:
        file_name = worldname+".yaml"
        shutil.copyfile(os.path.join("WebHostLib", "static", "generated", "configs", file_name),
                        buildfolder / "Players" / "Templates" / file_name)
shutil.copyfile("meta.yaml", buildfolder / "Players" / "Templates" / "meta.yaml")

try:
    from maseya import z3pr
except ImportError:
    print("Maseya Palette Shuffle not found, skipping data files.")
else:
    # maseya Palette Shuffle exists and needs its data files
    print("Maseya Palette Shuffle found, including data files...")
    file = z3pr.__file__
    installfile(Path(os.path.dirname(file)) / "data", keep_content=True)

if signtool:
    for exe in exes:
        print(f"Signing {exe.target_name}")
        os.system(signtool + os.path.join(buildfolder, exe.target_name))
    print(f"Signing SNI")
    os.system(signtool + os.path.join(buildfolder, "SNI", "SNI.exe"))
    print(f"Signing OoT Utils")
    for exe_path in (("Compress", "Compress.exe"), ("Decompress", "Decompress.exe")):
        os.system(signtool + os.path.join(buildfolder, "lib", "worlds", "oot", "data", *exe_path))

remove_sprites_from_folder(buildfolder / "data" / "sprites" / "alttpr")

manifest_creation(buildfolder)

if sys.platform == "win32":
    with open("setup.ini", "w") as f:
        min_supported_windows = "6.2.9200" if sys.version_info > (3, 9) else "6.0.6000"
        f.write(f"[Data]\nsource_path={buildfolder}\nmin_windows={min_supported_windows}\n")
