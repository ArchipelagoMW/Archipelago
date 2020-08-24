import os
import shutil
import sys
import sysconfig
from pathlib import Path
import cx_Freeze

is_64bits = sys.maxsize > 2 ** 32

folder = "exe.{platform}-{version}".format(platform=sysconfig.get_platform(),
                                           version=sysconfig.get_python_version())
buildfolder = Path("build", folder)
sbuildfolder = str(buildfolder)
libfolder = Path(buildfolder, "lib")
library = Path(libfolder, "library.zip")
print("Outputting to: " + str(buildfolder))
compress = False
icon="icon.ico"

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

def manifest_creation():
    hashes = {}
    manifestpath = os.path.join(buildfolder, "manifest.json")
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor()
    for dirpath, dirnames, filenames in os.walk(buildfolder):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            hashes[os.path.relpath(path, start=buildfolder)] = pool.submit(_threaded_hash, path)
    import json
    manifest = {"buildtime": buildtime.isoformat(sep=" ", timespec="seconds")}
    manifest["hashes"] = {path: hash.result() for path, hash in hashes.items()}
    json.dump(manifest, open(manifestpath, "wt"), indent=4)
    print("Created Manifest")


scripts = {"MultiClient.py" : "BerserkerMultiClient",
           "MultiMystery.py" : "BerserkerMultiMystery",
           "MultiServer.py" : "BerserkerMultiServer",
           "gui.py" : "BerserkerMultiCreator",
           "Mystery.py" : "BerserkerMystery"}

exes = []

for script, scriptname in scripts.items():
    exes.append(cx_Freeze.Executable(
        script=script,
        targetName=scriptname + ("" if sys.platform == "linux" else ".exe"),
        icon=icon,
    ))


import datetime

buildtime = datetime.datetime.utcnow()

cx_Freeze.setup(
    name="BerserkerMultiWorld",
    version=f"{buildtime.year}.{buildtime.month}.{buildtime.day}.{buildtime.hour}",
    description="BerserkerMultiWorld",
    executables=exes,
    options={
        "build_exe": {
            "includes": [],
            "zip_include_packages": ["*"],
            "zip_exclude_packages": ["maseya"],
            "include_files": [],
            "include_msvcr": True,
            "replace_paths": [("*", "")],
            "optimize": 2,
            "build_exe": buildfolder
        },
    },
)



def installfile(path):
    lbuildfolder = buildfolder
    print('copying', path, '->', lbuildfolder)
    if path.is_dir():
        lbuildfolder /= path.name
        if lbuildfolder.is_dir():
            shutil.rmtree(lbuildfolder)
        shutil.copytree(path, lbuildfolder)
    elif path.is_file():
        shutil.copy(path, lbuildfolder)
    else:
        print('Warning,', path, 'not found')


extra_data = ["LICENSE", "data", "EnemizerCLI", "host.yaml", "QUsb2Snes", "meta.yaml"]

for data in extra_data:
    installfile(Path(data))

os.makedirs(buildfolder / "Players", exist_ok=True)
shutil.copyfile("playerSettings.yaml", buildfolder / "Players" / "playerSettings.yaml")

qusb2sneslog = buildfolder / "QUsb2Snes" / "log.txt"
if os.path.exists(qusb2sneslog):
    os.remove(qusb2sneslog)

if signtool:
    for exe in exes:
        print(f"Signing {exe.targetName}")
        os.system(signtool+exe.targetName)


manifest_creation()
