
import argparse
import pathlib

import py_randomprime


def print_report(percent: float, message: str):
    print("[{:3d}%] {}".format(int(percent * 100), message))


parser = argparse.ArgumentParser()
parser.add_argument("json_file", type=pathlib.Path, help="Path to the JSON file to pass to the config file.")
args = parser.parse_args()

py_randomprime.patch_iso_raw(args.json_file.read_text("utf-8"), py_randomprime.ProgressNotifier(print_report))
