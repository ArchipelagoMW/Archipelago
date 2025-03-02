import os
import subprocess
import sys

AP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(AP_DIR))

# pylint: disable=import-error, wrong-import-position
from worlds.tits_the_3rd.util import (
    delete_contents,
    get_tooling_path,
    move_contents_with_file_ending,
    read_dev_config_and_assert_contents
)

def _move_scena_contents(source: str, destination: str):
    """
    Move the ._sn files in the source directory to the destination directory

    :str source: the source directory
    :str destination: the destination directory
    """
    move_contents_with_file_ending(source, destination, "._sn")

def _compile_with_calmare(lb_ark_dir: str):
    """
    Compile .clm files in ED6_DT21_CLM into ._sn files understood by the game.
    Store them in ED6_DT21.

    :str lb_ark_dir: The lbARK directory installation location.
    """
    calmare_path = get_tooling_path("calmare.exe")
    dt21_clm_path = os.path.join(lb_ark_dir, "ED6_DT21_CLM")
    for scena in os.listdir(dt21_clm_path):
        print(f"Running {scena} through calmare...")
        scena_path = os.path.join(dt21_clm_path, scena)
        try:
            subprocess.run([
                calmare_path,
                "--game",
                "tc",
                scena_path,
            ], check=True)
        except subprocess.CalledProcessError as err:
            print(f"Error running calmare: {err}")
            raise err
    dt21_dir = os.path.join(lb_ark_dir, "ED6_DT21")
    if os.listdir(dt21_dir):
        delete_contents(dt21_dir)
    _move_scena_contents(dt21_clm_path, dt21_dir)

def _update_dt21():
    config = read_dev_config_and_assert_contents()
    _compile_with_calmare(config["lbARKDirectory"])

if __name__ == "__main__":
    _update_dt21()
