
import zipfile
from typing import TYPE_CHECKING

from ...ndspy.rom import NintendoDSRom
from ...ndspy.narc import NARC

if TYPE_CHECKING:
    from ...rom import PokemonBWPatch


def write_species(bw_patch_instance: "PokemonBWPatch", opened_zipfile: zipfile.ZipFile) -> None:
    from ...data.pokemon.species import by_name

    slots: list[bytearray] = [
        bytearray(6*3)
        for _ in range(616)
    ]

    for pokemon in bw_patch_instance.world.trainer_teams:
        address = 3 * pokemon.team_number
        species_data = by_name[pokemon.species]
        slots[pokemon.trainer_id][address:address+2] = species_data.dex_number.to_bytes(2, "little")
        slots[pokemon.trainer_id][address+2] = species_data.form

    for file in range(1, 616):
        data = bytes(slots[file])
        while data[-3:] == b'\0\0\0':
            data = data[:-3]
        opened_zipfile.writestr(f"trainer/{file}_pokemon", data)


def patch_species(rom: NintendoDSRom, world_package: str, bw_patch_instance: "PokemonBWPatch",
                  files_dump: zipfile.ZipFile) -> None:

    trainer_narc = NARC(rom.getFileByName("a/0/9/2"))
    pokemon_narc = NARC(rom.getFileByName("a/0/9/3"))

    for file_num in range(1, 616):

        trainer_file = bytearray(trainer_narc.files[file_num])
        pokemon_file = bytearray(pokemon_narc.files[file_num])
        patch_file = bw_patch_instance.get_file(f"trainer/{file_num}_pokemon")
        unique_moves = trainer_file[0] % 2 == 1
        held_items = trainer_file[0] >= 2
        entry_length = 8 + (8 if unique_moves else 0) + (2 if held_items else 0)
        remove_unique_moves = False

        for team_slot in range(len(patch_file)//3):

            patch_address = team_slot * 3
            if patch_file[patch_address:patch_address+2] == b'\0\0':
                continue

            file_address = team_slot * entry_length + 4
            pokemon_file[file_address:file_address+3] = patch_file[patch_address:patch_address+3]
            if unique_moves:
                remove_unique_moves = True

        if remove_unique_moves:
            trainer_file[0] &= 254
            trainer_narc.files[file_num] = bytes(trainer_file)
            files_dump.writestr(f"a092/{file_num}", bytes(trainer_file))
            new_pokemon_file = b''
            for team_slot in range(len(pokemon_file)//entry_length):
                file_address = team_slot * entry_length
                new_pokemon_file += pokemon_file[file_address:file_address+entry_length-8]
            pokemon_narc.files[file_num] = bytes(new_pokemon_file)
        else:
            pokemon_narc.files[file_num] = bytes(pokemon_file)
        files_dump.writestr(f"a093/{file_num}", pokemon_narc.files[file_num])

    rom.setFileByName("a/0/9/2", trainer_narc.save())
    rom.setFileByName("a/0/9/3", pokemon_narc.save())
