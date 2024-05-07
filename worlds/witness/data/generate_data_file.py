from collections import defaultdict

if __name__ == "__main__":
    with open("APWitnessData.h", "w") as datafile:
        datafile.write("""# pragma once

# include <map>
# include <set>
# include <string>

""")
        area_to_location_ids = defaultdict(list)
        area_to_entity_ids = defaultdict(list)

        with open("WitnessLogic.txt") as w:
            current_area = ""

            for line in w.readlines():
                line = line.strip()
                if not line:
                    continue

                if line.startswith("=="):
                    current_area = line[2:-2]
                    continue

                if line.endswith(":"):
                    continue

                line_split = line.split(" - ")
                location_id = line_split[0]
                if location_id.isnumeric():
                    area_to_location_ids[current_area].append(location_id)

                entity_id = line_split[1].split(" ", 1)[0]

                area_to_entity_ids[current_area].append(entity_id)

        datafile.write("inline std::map<std::string, std::set<int64_t>> areaNameToLocationIDs = {\n")
        datafile.write(
            "\n".join(
                '\t{"' + area + '", { ' + ", ".join(location_ids) + " }},"
                for area, location_ids in area_to_location_ids.items()
            )
        )
        datafile.write("\n};\n\n")

        datafile.write("inline std::map<std::string, std::set<int64_t>> areaNameToEntityIDs = {\n")
        datafile.write(
            "\n".join(
                '\t{"' + area + '", { ' + ", ".join(entity_ids) + " }},"
                for area, entity_ids in area_to_entity_ids.items()
            )
        )
        datafile.write("\n};\n")
