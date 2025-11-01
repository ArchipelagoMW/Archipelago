if __name__ == "__main__":
    import json

    all_doors: list[str] = []
    all_region_connections: list[str] = []
    all_locations: list[str] = []
    all_regions: list[str] = []
    all_room_connections: list[str] = []
    all_rooms: list[str] = []
    all_levels: list[str] = []


    data_file = open('CelesteLevelData.json')
    level_data = json.load(data_file)
    data_file.close()

    # Levels
    for level in level_data["levels"]:
        level_str = (f"    \"{level['name']}\": Level(\"{level['name']}\", "
                     f"\"{level['display_name']}\", "
                     f"[room for _, room in all_rooms.items() if room.level_name == \"{level['name']}\"], "
                     f"[room_con for _, room_con in all_room_connections.items() if room_con.level_name == \"{level['name']}\"]),"
                    )

        all_levels.append(level_str)

        # Rooms
        for room in level["rooms"]:
            room_full_name = f"{level['name']}_{room['name']}"
            room_full_display_name = f"{level['display_name']} - Room {room['name']}"

            room_str = (f"    \"{room_full_name}\": Room(\"{level['name']}\", "
                         f"\"{room_full_name}\", \"{room_full_display_name}\", "
                         f"[reg for _, reg in all_regions.items() if reg.room_name == \"{room_full_name}\"], "
                         f"[door for _, door in all_doors.items() if door.room_name == \"{room_full_name}\"]"
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
                              f"[reg_con for _, reg_con in all_region_connections.items() if reg_con.source_name == \"{region_full_name}\"], "
                              f"[loc for _, loc in all_locations.items() if loc.region_name == \"{region_full_name}\"]),"
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
                                        f"LocationType.{location['type']}, ["
                                       )

                        if "rule" in location:
                            for possible_access in location['rule']:
                                location_str += f"["
                                for item in possible_access:
                                    if "Key" in item or "Gem" in item:
                                        location_str += f"\"{level['display_name']} - {item}\", "
                                    else:
                                        location_str += f"ItemName.{item}, "
                                location_str += f"], "
                        elif "rules" in location:
                            raise Exception(f"Location {location_full_name} uses 'rules' instead of 'rule")

                        location_str += "]),"

                        all_locations.append(location_str)

                # Region Connections
                for reg_con in region["connections"]:
                    dest_region_full_name = f"{room_full_name}_{reg_con['dest']}"
                    reg_con_full_name = f"{region_full_name}---{dest_region_full_name}"

                    reg_con_str = f"    \"{reg_con_full_name}\": RegionConnection(\"{region_full_name}\", \"{dest_region_full_name}\", ["

                    for possible_access in reg_con['rule']:
                        reg_con_str += f"["
                        for item in possible_access:
                            if "Key" in item or "Gem" in item:
                                reg_con_str += f"\"{level['display_name']} - {item}\", "
                            else:
                                reg_con_str += f"ItemName.{item}, "
                        reg_con_str += f"], "

                    reg_con_str += "]),"

                    all_region_connections.append(reg_con_str)

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
    print("all_rooms: dict[str, Room] = {")
    for line in all_rooms:
        print(line)
    print("}")
    print("")
    print("all_levels: dict[str, Level] = {")
    for line in all_levels:
        print(line)
    print("}")
    print("")

    out_file.close()
