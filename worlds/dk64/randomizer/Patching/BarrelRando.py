"""Apply Boss Locations."""

from randomizer.Lists.Minigame import BarrelMetaData, MinigameRequirements
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames


def randomize_barrels(spoiler, ROM_COPY: LocalROM):
    """Randomize barrel locations."""
    barrels = [28, 107, 134]
    if spoiler.settings.bonus_barrel_rando or spoiler.settings.minigames_list_selected:
        barrel_replacements = []
        for location, minigame in spoiler.shuffled_barrel_data.items():
            container_map = int(BarrelMetaData[location].map)
            barrel_data = {
                "instance_id": int(BarrelMetaData[location].barrel_id),
                "new_map": int(MinigameRequirements[minigame].map),
            }
            new_map = True
            if len(barrel_replacements) > 0:
                for x in barrel_replacements:
                    if x["containing_map"] == container_map:
                        x["barrels"].append(barrel_data)
                        new_map = False
            if new_map:
                barrel_replacements.append({"containing_map": container_map, "barrels": [barrel_data]})
        for cont_map in barrel_replacements:
            cont_map_id = int(cont_map["containing_map"])
            cont_map_setup_address = getPointerLocation(TableNames.Setups, cont_map_id)
            ROM_COPY.seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            ROM_COPY.seek(cont_map_setup_address + 4 + (model2_count * 0x30))
            mystery_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            ROM_COPY.seek(cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24))
            actor_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
            start_of_actor_range = cont_map_setup_address + 4 + (model2_count * 0x30) + 4 + (mystery_count * 0x24) + 4
            for x in range(actor_count):
                start_of_actor = start_of_actor_range + (0x38 * x)
                ROM_COPY.seek(start_of_actor)
                ROM_COPY.seek(start_of_actor + 0x32)
                actor_type = int.from_bytes(ROM_COPY.readBytes(2), "big") + 0x10
                if actor_type in barrels:
                    ROM_COPY.seek(start_of_actor + 0x34)
                    actor_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
                    for barrel in cont_map["barrels"]:
                        if int(barrel["instance_id"]) == actor_id:
                            ROM_COPY.seek(start_of_actor + 0x12)
                            ROM_COPY.writeMultipleBytes(barrel["new_map"], 2)
