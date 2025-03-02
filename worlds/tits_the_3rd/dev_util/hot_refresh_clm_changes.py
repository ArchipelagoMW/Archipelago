import os
import shutil
import subprocess
import sys
import time

AP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(AP_DIR))

# pylint: disable=import-error, wrong-import-position
from worlds.tits_the_3rd.util import (
    assert_path_exists,
    get_tooling_path,
    read_dev_config_and_assert_contents
)

def _update_file(dt21_clm_dir: str, dt21_dir: str, calmare_path: str, file: str):
    """
    Update a specified file in the lbARK ED6_DT21_CLM directory.
    Run it through calmare and move them to the lbARK ED6_DT21 directory.

    :str dt21_clm_dir: The path to the lbARK ED6_DT21_CLM directory.
    :str dt21_dir: The path to the lbARK ED6_DT21 directory.
    :str calmare_path: The path to calmare.
    :str file: the filename to update in the ED6_DT21_CLM directory.
    """
    print(f"Updating {file}")
    src_path = os.path.join(dt21_clm_dir, file)
    subprocess.run([
        calmare_path,
        "--game",
        "tc",
        src_path,
    ], check=True)
    scena_filename = file.replace(".clm", "._sn")
    calmare_out_path = os.path.join(dt21_clm_dir, scena_filename)
    shutil.move(calmare_out_path, os.path.join(dt21_dir, scena_filename))

def _watch_for_changes(dt21_clm_dir: str, dt21_dir: str, calmare: str, newer_than: float):
    """
    Check if any files in the ED6_DT21_CLM dir have been updated. If they have put them
    through calmare and copy to the ED6_DT21 directory

    :str dt21_clm_dir: The path to the lbARK ED6_DT21_CLM directory.
    :str dt21_dir: The path to the lbARK ED6_DT21 directory.
    :str calmare_path: The path to calmare.
    :float newer_than: Act on files newer than this time.
    """
    for root, _, files in os.walk(dt21_clm_dir):
        for file in files:
            if os.path.getmtime(os.path.join(root, file)) > newer_than:
                if (file.endswith(".clm")):
                    _update_file(dt21_clm_dir, dt21_dir, calmare, file)

def watch_for_changes():
    """
    Watch for changes to calmare files in the lbARK ED6_DT21_CLM directory.
    When they occur, run them through calmare and move them to the lbARK ED6_DT21 directory.
    """
    config = read_dev_config_and_assert_contents()

    # Extract directory paths from command line arguments
    dt21_clm = os.path.join(config["lbARKDirectory"], "ED6_DT21_CLM")
    dt21_sn = os.path.join(config["lbARKDirectory"], "ED6_DT21")

    assert_path_exists(dt21_clm)
    assert_path_exists(dt21_sn)
    calmare = get_tooling_path("calmare.exe")

    last_checked = time.time()
    try:
        while True:
            _watch_for_changes(dt21_clm, dt21_sn, calmare, last_checked)
            last_checked = time.time()
            time.sleep(2)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as err:
        print(err)
        sys.exit(1)

if __name__ == "__main__":
    watch_for_changes()
