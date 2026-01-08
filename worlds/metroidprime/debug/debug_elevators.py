import argparse
import json
import os

import yaml
from ..Items import SuitUpgrade
from ..data.AreaNames import MetroidPrimeArea
from ..data.Transports import default_elevator_mappings
from ..data.RoomNames import RoomName
from Generate import main
from ..data.StartRoomData import all_start_rooms

fail = []

# all_rooms = ["Arbor Chamber", "Transport to Chozo Ruins East", "Quarantine Monitor", "Sunchamber Lobby"]
all_rooms = ["Save Station B"]
data = {}
failures = {}
times_to_try = 20

areas_by_room = {
    "Arbor Chamber": MetroidPrimeArea.Tallon_Overworld.value,
    "Transport to Chozo Ruins East": MetroidPrimeArea.Tallon_Overworld.value,
    "Quarantine Monitor": MetroidPrimeArea.Phendrana_Drifts.value,
    "Sunchamber Lobby": MetroidPrimeArea.Chozo_Ruins.value,
}

# for room in all_start_rooms:
for room in all_rooms:
    if room == RoomName.Landing_Site.value or room in all_rooms:
        continue
    source_area = all_start_rooms[room].area.value
    source_elevators = default_elevator_mappings[source_area]
    for source_elevator in source_elevators:
        for target_area, target_elevators in default_elevator_mappings.items():
            if target_area == source_area:
                continue
            for target_elevator in target_elevators.keys():
                if target_elevator == source_elevators[source_elevator]:
                    continue
                config = None
                with open("Players/Hesto2.yaml", "r") as file:
                    config = yaml.safe_load(file)

                config["Metroid Prime"]["elevator_mapping"] = {}
                config["Metroid Prime"]["elevator_mapping"][source_area] = {}
                config["Metroid Prime"]["elevator_mapping"][source_area][
                    source_elevator
                ] = target_elevator

                config["Metroid Prime"]["elevator_mapping"][target_area] = {}
                config["Metroid Prime"]["elevator_mapping"][target_area][
                    target_elevator
                ] = source_elevator
                config["Metroid Prime"]["starting_room"] = room

                with open("Players/Hesto2.yaml", "w") as file:
                    yaml.safe_dump(config, file, default_flow_style=False)

                for time in range(times_to_try):
                    os.environ["skip_output"] = "true"
                    loadouts = all_start_rooms[room].loadouts
                    name = f"{room} -> {source_area}: {source_elevator} -> {target_area}: {target_elevator}"
                    if name not in failures:
                        failures[name] = 0
                    try:
                        main()
                    except Exception as e:
                        failures[name] += 1
                        continue

for room in failures:
    print(f"{room}: {times_to_try - failures[room]}/{times_to_try}")
if len(failures) == 0:
    print(f"No failures detected")
