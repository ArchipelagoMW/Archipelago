if __name__ == "__main__":
    import itertools
    import json


    def get_full_access_string(possible_access_str: str, multi_dashes: list[list[str]]) -> str:
        output: str = ""

        if len(multi_dashes) == 0:
            output += f"[{possible_access_str}], "
        else:
            combinations = itertools.product(*multi_dashes)

            filtered_combinations: list[list[str]] = list()
            for comb in combinations:
                comb_set = sorted(list(set(comb)))
                if comb_set not in filtered_combinations:
                    filtered_combinations.append(comb_set)

            for filtered_comb in sorted(filtered_combinations):
                output += f"["
                if len(possible_access_str) > 0:
                    output += possible_access_str
                for dash_str in filtered_comb:
                    output += f"ItemName.{dash_str}_dash, "
                output += f"], "

        return output


    all_doors: list[str] = []
    all_region_connections: list[str] = []
    all_locations: list[str] = []
    all_regions: list[str] = []
    all_room_connections: list[str] = []
    all_rooms: list[str] = []
    all_levels: list[str] = []
    all_level_items: list[str] = []


    data_file = open('CelesteLevelData.json')
    level_data = json.load(data_file)
    data_file.close()

    # Levels
    for level in level_data["levels"]:
        level_str = (f"    \"{level['name']}\": Level(\"{level['name']}\", "
                     f"\"{level['display_name']}\", "
                     f"rooms_by_level[\"{level['name']}\"], "
                     f"room_cons_by_level[\"{level['name']}\"], "
                     f"set(["
                    )

        for item in level["items"]:
            level_str += f"ItemName.{item}, "

        level_str += f"])),"

        all_levels.append(level_str)

        # Rooms
        for room in level["rooms"]:
            room_full_name = f"{level['name']}_{room['name']}"
            room_full_display_name = f"{level['display_name']} - Room {room['name']}"

            room_str = (f"    \"{room_full_name}\": Room(\"{level['name']}\", "
                         f"\"{room_full_name}\", \"{room_full_display_name}\", "
                         f"regions_by_room[\"{room_full_name}\"], "
                         f"doors_by_room[\"{room_full_name}\"]"
                        )

            if "checkpoint" in room and room["checkpoint"] != "":
                room_str += f", \"{room['checkpoint']}\", \"{room_full_name}_{room['checkpoint_region']}\""
            room_str += "),"

            all_rooms.append(room_str)

            # Regions
            for region in room["regions"]:
                region_full_name = f"{room_full_name}_{region['name']}"

                region_str = (f"    \"{region_full_name}\": PreRegion(\"{region_full_name}\", "
                              f"\"{room_full_name}\", "
                              f"connections_by_region[\"{region_full_name}\"], "
                              f"locations_by_region[\"{region_full_name}\"]),"
                             )

                all_regions.append(region_str)

                # Locations
                if "locations" in region:
                    for location in region["locations"]:
                        location_full_name = f"{room_full_name}_{location['name']}"

                        location_display_name = location['display_name']
                        if (location['type'] == "strawberry" and location_display_name != "Moon Berry") or location['type'] == "binoculars" :
                            location_display_name = f"Room {room['name']} {location_display_name}"
                        location_full_display_name = f"{level['display_name']} - {location_display_name}"

                        location_str = (f"    \"{location_full_name}\": LevelLocation(\"{location_full_name}\", "
                                        f"\"{location_full_display_name}\", \"{region_full_name}\", "
                                        f"LocationType.{location['type']}"
                                       )

                        for rule_key in ['rule', 'vm_rule', 'assist_rule']:
                            location_str += ", "
                            if rule_key in location:
                                location_str += "["
                                for possible_access in location[rule_key]:
                                    multi_dashes: list[list[str]] = []
                                    possible_access_str = ""
                                    for item in possible_access:
                                        if "any_dash_" in item:
                                            multi_dashes.append(list(item[9:].split("_")))
                                        elif "Key" in item or "Gem" in item:
                                            possible_access_str += f"\"{level['display_name']} - {item}\", "
                                        else:
                                            possible_access_str += f"ItemName.{item}, "
                                    location_str += get_full_access_string(possible_access_str, multi_dashes)
                                location_str += "]"
                            else:
                                location_str += "[]"

                        location_str += "),"

                        all_locations.append(location_str)

                        if location.keys() - { "name", "display_name", "type", "rule", "assist_rule", "vm_rule" }:
                            print(location_full_name + "   |   " + str(location.keys() - { "name", "display_name", "type", "rule", "assist_rule", "vm_rule" }))

                # Region Connections
                for reg_con in region["connections"]:
                    dest_region_full_name = f"{room_full_name}_{reg_con['dest']}"
                    reg_con_full_name = f"{region_full_name}---{dest_region_full_name}"

                    reg_con_str = f"    \"{reg_con_full_name}\": RegionConnection(\"{region_full_name}\", \"{dest_region_full_name}\""

                    for rule_key in ['rule', 'vm_rule', 'assist_rule']:
                        reg_con_str += ", "
                        if rule_key in reg_con:
                            reg_con_str += "["
                            for possible_access in reg_con[rule_key]:
                                multi_dashes: list[list[str]] = []
                                possible_access_str = ""
                                for item in possible_access:
                                    if "any_dash_" in item:
                                        multi_dashes.append(list(item[9:].split("_")))
                                    elif "Key" in item or "Gem" in item:
                                        possible_access_str += f"\"{level['display_name']} - {item}\", "
                                    else:
                                        possible_access_str += f"ItemName.{item}, "
                                reg_con_str += get_full_access_string(possible_access_str, multi_dashes)
                            reg_con_str += "]"
                        else:
                            reg_con_str += "[]"

                    reg_con_str += "),"

                    all_region_connections.append(reg_con_str)

                    if reg_con.keys() - { "dest", "rule", "assist_rule", "vm_rule" }:
                        print(f"{region_full_name} -> {reg_con['dest']}    |    " + str(reg_con.keys() - { "dest", "rule", "assist_rule", "vm_rule" }))

            for door in room["doors"]:
                door_full_name = f"{room_full_name}_{door['name']}"

                door_str = (f"    \"{door_full_name}\": Door(\"{door_full_name}\", "
                            f"\"{room_full_name}\", "
                            f"DoorDirection.{door['direction']}, "
                            )

                door_str += "True, " if door["blocked"] else "False, "
                door_str += "True)," if door["closes_behind"] else "False),"

                all_doors.append(door_str)

            all_regions.append("")
            all_region_connections.append("")
            all_doors.append("")

        all_locations.append("")
        all_rooms.append("")

        # Room Connections
        for room_con in level["room_connections"]:
            source_door_full_name = f"{level['name']}_{room_con['source_room']}_{room_con['source_door']}"
            dest_door_full_name = f"{level['name']}_{room_con['dest_room']}_{room_con['dest_door']}"

            room_con_str = (f"    \"{source_door_full_name}---{dest_door_full_name}\": RoomConnection(\"{level['name']}\", "
                            f"all_doors[\"{source_door_full_name}\"], "
                            f"all_doors[\"{dest_door_full_name}\"]),"
                           )

            all_room_connections.append(room_con_str)

        all_room_connections.append("")


    all_levels.append("")


    import sys
    out_file = open("CelesteLevelData.py", "w")
    sys.stdout = out_file

    print("# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT MANUALLY EDIT.")
    print("")
    print("from ..Levels import Level, Room, PreRegion, LevelLocation, RegionConnection, RoomConnection, Door, DoorDirection, LocationType")
    print("from ..Names import ItemName")
    print(f"from collections import defaultdict")
    print("")
    print("all_doors: dict[str, Door] = {")
    for line in all_doors:
        print(line)
    print("}")
    print("")
    print("all_region_connections: dict[str, RegionConnection] = {")
    for line in all_region_connections:
        print(line)
    print("}")
    print("")
    print("all_locations: dict[str, LevelLocation] = {")
    for line in all_locations:
        print(line)
    print("}")
    print("")
    print("connections_by_region: defaultdict[str, list[RegionConnection]] = defaultdict(lambda: [])")
    print("locations_by_region: defaultdict[str, list[LevelLocation]] = defaultdict(lambda: [])")
    print("")
    print("for _, connection in all_region_connections.items():")
    print("    connections_by_region[connection.source_name].append(connection)")
    print("")
    print("for _, location in all_locations.items():")
    print("    locations_by_region[location.region_name].append(location)")
    print("")
    print("all_regions: dict[str, PreRegion] = {")
    for line in all_regions:
        print(line)
    print("}")
    print("")
    print("all_room_connections: dict[str, RoomConnection] = {")
    for line in all_room_connections:
        print(line)
    print("}")
    print("")
    print("regions_by_room: defaultdict[str, list[PreRegion]] = defaultdict(lambda: [])")
    print("doors_by_room: defaultdict[str, list[Door]] = defaultdict(lambda: [])")
    print("")
    print("for _, region in all_regions.items():")
    print("    regions_by_room[region.room_name].append(region)")
    print("")
    print("for _, door in all_doors.items():")
    print("    doors_by_room[door.room_name].append(door)")
    print("")
    print("all_rooms: dict[str, Room] = {")
    for line in all_rooms:
        print(line)
    print("}")
    print("")
    print("rooms_by_level: defaultdict[str, list[Room]] = defaultdict(lambda: [])")
    print("room_cons_by_level: defaultdict[str, list[RoomConnection]] = defaultdict(lambda: [])")
    print("")
    print("for _, room in all_rooms.items():")
    print("    rooms_by_level[room.level_name].append(room)")
    print("")
    print("for _, room_con in all_room_connections.items():")
    print("    room_cons_by_level[room_con.level_name].append(room_con)")
    print("")
    print("all_levels: dict[str, Level] = {")
    for line in all_levels:
        print(line)
    print("}")
    print("")

    out_file.close()
