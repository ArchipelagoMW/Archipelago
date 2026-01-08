import json

# After testing elevator combos, this can be used to conver the results to a JSON file
# Expects the following format:
# Arboretum -> [Chozo Ruins]: Transport to Tallon Overworld North -> [Tallon Overworld]: Transport to Magmoor Caverns East = 100%
# Arboretum -> [Chozo Ruins]: Transport to Tallon Overworld North -> [Tallon Overworld]: Transport to Chozo Ruins East = 100%
# Arboretum -> [Chozo Ruins]: Transport to Tallon Overworld North -> [Tallon Overworld]: Transport to Chozo Ruins South = 100%

# Define the path to the input file
input_file_path = "./data/elevator_mappings.txt"
# Define the path to the output JSON file
output_file_path = "./data/elevator_access.json"

# Initialize a dictionary to hold the processed data
elevator_access = {}
THRESHOLD_SUCCESS_RATE = 90

# Open and read the input file
with open(input_file_path, "r") as file:
    for line in file:
        # Split the line into components
        parts = line.strip().split(" -> ")
        start_room = parts[0]
        source_elevator = parts[1].split(": ")[1]
        target_elevator = parts[2].split(": ")[1]
        elevator_info = " -> ".join(parts[1:])
        success_rate = int(elevator_info.split("= ")[-1].replace("%", ""))

        # Initialize the start room key in the dictionary if it doesn't exist
        if start_room not in elevator_access:
            elevator_access[start_room] = {"allow": {}, "deny": {}}

        # Group the elevator information based on the success rate
        if success_rate >= THRESHOLD_SUCCESS_RATE:
            if source_elevator not in elevator_access[start_room]["allow"]:
                elevator_access[start_room]["allow"][source_elevator] = []
            elevator_access[start_room]["allow"][source_elevator].append(elevator_info)
        else:
            if source_elevator not in elevator_access[start_room]["deny"]:
                elevator_access[start_room]["deny"][source_elevator] = []
            elevator_access[start_room]["deny"][source_elevator].append(elevator_info)

# Write the processed data to a JSON file
with open(output_file_path, "w") as json_file:
    json.dump(elevator_access, json_file, indent=4)
