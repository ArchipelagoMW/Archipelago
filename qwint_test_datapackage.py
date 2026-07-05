import json

from Generate import main as G
from Main import main as M
from worlds import AutoWorld, network_data_package

args, seed = G()

# check player 1's checksums
world = AutoWorld.AutoWorldRegister.world_types[args.game[1]]
first_datapackage = world.get_data_package_data()

multiworld = M(args, seed)

final_datapackage = world.get_data_package_data()

core_datapackage = network_data_package["games"][world.game]
assert core_datapackage["checksum"] == first_datapackage["checksum"], json.dump({"lookup": core_datapackage, "method": first_datapackage}, indent=2)
assert first_datapackage["checksum"] == final_datapackage["checksum"], json.dump({"before": first_datapackage, "after": final_datapackage}, indent=2)
