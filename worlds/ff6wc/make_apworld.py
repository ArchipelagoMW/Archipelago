# a script for creating the apworld
# (This is not a module for Archipelago. This is a stand-alone script.)

import os
from shutil import copytree, make_archive, rmtree

ORIG = "ff6wc"
TEMP = "ff6wc_temp"
MOVE = "ff6wc_move"


def delete_pycache(directory: str) -> None:
    for root, dirs, _files in os.walk(directory):
        if "__pycache__" in dirs:
            pycache_dir = os.path.join(root, "__pycache__")
            rmtree(pycache_dir)
            # print(f"deleted: {pycache_dir}")


def old_main() -> None:
    # working directory near worlds will be changed to worlds
    if os.getcwd().endswith("Archipelago"):
        os.chdir("worlds")
    else:
        os.chdir("..")
    assert os.getcwd().endswith("worlds"), f"incorrect directory: {os.getcwd()=}"

    assert os.path.exists(ORIG), f"{ORIG} doesn't exist"
    assert not os.path.exists(TEMP), f"{TEMP} exists"
    assert not os.path.exists(MOVE), f"{MOVE} exists"

    destination = os.path.join("ff6wc.apworld")
    if os.path.exists(destination):
        os.unlink(destination)
    assert not os.path.exists(destination)

    copytree(ORIG, TEMP)

    delete_pycache(TEMP)

    os.rename(ORIG, MOVE)
    os.rename(TEMP, ORIG)

    zip_file_name = make_archive("ff6wc", "zip", ".", ORIG)
    print(f"{zip_file_name} -> {destination}")
    os.rename(zip_file_name, destination)

    rmtree(ORIG)
    os.rename(MOVE, ORIG)

    assert os.path.exists(ORIG), f"{ORIG} doesn't exist at end"
    assert not os.path.exists(TEMP), f"{TEMP} exists at end"
    assert not os.path.exists(MOVE), f"{MOVE} exists at end"


def new_apworld_builder() -> None:
    from subprocess import run

    proc = run(["python", "Launcher.py", "Build APWorlds", "Final Fantasy 6 Worlds Collide"], check=True)
    assert proc.returncode == 0


if __name__ == "__main__":
    new_apworld_builder()
