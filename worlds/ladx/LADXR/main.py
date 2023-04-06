import binascii
from .romTables import ROMWithTables
import json
from . import logic
import argparse
from .settings import Settings
from typing import Optional, List

def get_parser():

    parser = argparse.ArgumentParser(description='Randomize!')
    parser.add_argument('input_filename', metavar='input rom', type=str,
        help="Rom file to use as input.")
    parser.add_argument('-o', '--output', dest="output_filename", metavar='output rom', type=str, required=False,
        help="Output filename to use. If not specified [seed].gbc is used.")
    parser.add_argument('--dump', dest="dump", type=str, nargs="*",
        help="Dump the logic of the given rom (spoilers!)")
    parser.add_argument('--spoilerformat', dest="spoilerformat", choices=["none", "console", "text", "json"], default="none",
       help="Sets the output format for the generated seed's spoiler log")
    parser.add_argument('--spoilerfilename', dest="spoiler_filename", type=str, required=False,
        help="Output filename to use for the spoiler log.  If not specified, LADXR_[seed].txt/json is used.")
    parser.add_argument('--test', dest="test", action="store_true",
        help="Test the logic of the given rom, without showing anything.")
    parser.add_argument('--romdebugmode', dest="romdebugmode", action="store_true",
        help="Patch the rom so that debug mode is enabled, this creates a default save with most items and unlocks some debug features.")
    parser.add_argument('--exportmap', dest="exportmap", action="store_true",
        help="Export the map (many graphical mistakes)")
    parser.add_argument('--emptyplan', dest="emptyplan", type=str, required=False,
        help="Write an unfilled plan file")
    parser.add_argument('--timeout', type=float, required=False,
        help="Timeout generating the seed after the specified number of seconds")
    parser.add_argument('--logdirectory', dest="log_directory", type=str, required=False,
        help="Directory to write the JSON log file. Generated independently from the spoiler log and omitted by default.")

    parser.add_argument('-s', '--setting', dest="settings", action="append", required=False,
        help="Set a configuration setting for rom generation")
    parser.add_argument('--short', dest="shortsettings", type=str, required=False,
        help="Set a configuration setting for rom generation")
    parser.add_argument('--settingjson', dest="settingjson", action="store_true",
        help="Dump a json blob which describes all settings")

    parser.add_argument('--plan', dest="plan", metavar='plandomizer', type=str, required=False,
        help="Read an item placement plan")
    parser.add_argument('--multiworld', dest="multiworld", action="append", required=False,
        help="Set configuration for a multiworld player, supply multiple times for settings per player, requires a short setting string per player.")
    parser.add_argument('--doubletrouble', dest="doubletrouble", action="store_true",
        help="Warning, bugged in various ways")
    parser.add_argument('--pymod', dest="pymod", action='append',
        help="Load python code mods.")

    return parser

