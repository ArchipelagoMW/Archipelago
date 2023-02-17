import bsdiff4
import json
import os

from Patch import APDeltaPatch

def get_base_rom_as_bytes() -> bytes:
    with open(os.path.join(os.path.dirname(__file__), f"pokeemerald-vanilla.gba"), "rb") as infile:
        base_rom_bytes = bytes(infile.read())
    return base_rom_bytes

# def patch(self):
#     base_rom = get_base_rom_as_bytes()
#     data = read_json("./data.json")
#     item_address = data["ball_items"]["ITEM_ROUTE_104_POTION"]["rom_address"]
#     rom[item_address] = data["constants"]["items"]["ITEM_ARCHIPELAGO_PROGRESSION"]

#     for location in self.multiworld.get_locations():
#         if location.player != self.player:
#             continue

#         if location.item and location.item.player == self.player:
#             rom[location.rom_address] = location.item.id
#         else:
#             rom[location.rom_address] = data["constants"]["items"]["ITEM_ARCHIPELAGO_PROGRESSION"]

#     with open("./patched-emerald.gba", 'wb') as outfile:
#         outfile.write(rom)

def read_json():
    json_string = ""
    with open(os.path.join(os.path.dirname(__file__), f"data.json"), "r") as infile:
        for line in infile.readlines():
            # json_string += line.replace('\n', ' ')
            json_string += line
    return json.loads(json_string)

def generate_output(self, output_directory: str):
    data = read_json() 

    base_rom = get_base_rom_as_bytes()
    with open(os.path.join(os.path.dirname(__file__), f"base_patch.bsdiff4"), "rb") as stream:
        base_patch = bytes(stream.read())
        patched_rom = bytearray(bsdiff4.patch(base_rom, base_patch))

    for location in self.multiworld.get_locations():
        if location.player != self.player:
            continue

        if location.item and location.item.player == self.player:
            patched_rom[location.address] = location.item.code
        else:
            patched_rom[location.address] = data["constants"]["items"]["ITEM_ARCHIPELAGO_PROGRESSION"]

    outfile_player_name = f"_P{self.player}"
    outfile_player_name += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}" \
        if self.multiworld.player_name[self.player] != "Player%d" % self.player else ""

    output_path = os.path.join(output_directory, f"AP_{self.multiworld.seed_name}{outfile_player_name}.gba")
    with open(output_path, "wb") as outfile:
        outfile.write(patched_rom)
    patch = PokemonEmeraldDeltaPatch(os.path.splitext(output_path)[0] + ".apemerald", player=self.player,
                            player_name=self.multiworld.player_name[self.player], patched_path=output_path)

    patch.write()
    os.unlink(output_path)


class PokemonEmeraldDeltaPatch(APDeltaPatch):
    hash = "3d45c1ee9abd5738df46d2bdda8b57dc"
    game = "Pokemon Emerald"
    patch_file_ending = ".apemerald"
    result_file_ending = ".gba"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()
