import argparse
from pathlib import Path
from Utils import local_path
from worlds.Export import export_world
from worlds.AutoWorld import AutoWorldRegister

if __name__ == "__main__":
    ap_root_path = local_path("worlds")

    parser = argparse.ArgumentParser("simple_example")
    parser.add_argument("world_name", help="World to be exported.", type=str)
    parser.add_argument("output_dir", help="Export directory.", type=Path, default=ap_root_path, nargs='?')
    args = parser.parse_args()

    output = export_world(ap_root_path, AutoWorldRegister.world_types[args.world_name], args.output_dir,
                          is_frozen=False)
    print(f"Output to {output}")
