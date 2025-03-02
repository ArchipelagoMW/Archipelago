from collections import defaultdict

from data import static_logic as static_witness_logic

if __name__ == "__main__":
    with open("data/APWitnessData.h", "w") as datafile:
        datafile.write("""# pragma once

# include <map>
# include <set>
# include <string>

""")

        area_to_location_ids = defaultdict(list)
        area_to_entity_ids = defaultdict(list)

        for entity_id, entity_object in static_witness_logic.ENTITIES_BY_HEX.items():
            location_id = entity_object["id"]

            area = entity_object["area"]["name"]
            area_to_entity_ids[area].append(entity_id)

            if location_id is None:
                continue

            area_to_location_ids[area].append(str(location_id))

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
        datafile.write("\n};\n\n")
