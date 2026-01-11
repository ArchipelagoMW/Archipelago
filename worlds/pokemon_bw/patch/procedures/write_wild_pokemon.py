
import zipfile
from typing import TYPE_CHECKING

from ...ndspy.rom import NintendoDSRom
from ...ndspy.narc import NARC

if TYPE_CHECKING:
    from ...rom import PokemonBWPatch


def write_patch(bw_patch_instance: "PokemonBWPatch", opened_zipfile: zipfile.ZipFile) -> None:

    slots: list[list[bytearray]] = [
        [bytearray(56*2), bytearray(56*2), bytearray(56*2), bytearray(56*2)]
        for _ in range(112)
    ]

    for slot in bw_patch_instance.world.wild_encounter.values():
        if slot.write:
            file = slot.file_index
            species = slot.species_id
            value = (species[0] + (species[1] * 2048)).to_bytes(2, "little")
            slots[file[0]][file[1]][file[2]*2:file[2]*2+2] = value

    empty = bytes(56*2)
    for file_num in range(112):
        if slots[file_num][3] != empty:
            data = slots[file_num][0] + slots[file_num][1] + slots[file_num][2] + slots[file_num][3]
        elif slots[file_num][2] != empty:
            data = slots[file_num][0] + slots[file_num][1] + slots[file_num][2]
        elif slots[file_num][1] != empty:
            data = slots[file_num][0] + slots[file_num][1]
        elif slots[file_num][0] != empty:
            data = slots[file_num][0]
        else:
            data = bytearray(0)
        opened_zipfile.writestr(f"wild/{file_num}", bytes(data))


def patch(rom: NintendoDSRom, world_package: str, bw_patch_instance: "PokemonBWPatch",
          files_dump: zipfile.ZipFile) -> None:

    narc = NARC(rom.getFileByName("a/1/2/6"))

    for file_num in range(112):

        game_file = bytearray(narc.files[file_num])
        patch_file = bw_patch_instance.get_file(f"wild/{file_num}")
        season_count_game = len(game_file) // (56 * 4 + 8)
        season_count_patch = len(patch_file) // (56 * 2)
        if season_count_patch > season_count_game:
            raise Exception(f"Patch file has more seasons than game file: file {file_num}, "
                            f"{season_count_game} game season, {season_count_patch} patch seasons")

        for season in range(season_count_patch):
            for slot in range(56):
                game_address = (season * (56 * 4 + 8) + 8) + (slot * 4)
                patch_address = (season * 56 * 2) + (slot * 2)
                species: bytes = patch_file[patch_address:patch_address+2]
                if species != b'\0\0':
                    game_file[game_address:game_address+2] = species

        narc.files[file_num] = bytes(game_file)
        files_dump.writestr(f"a126/{file_num}", bytes(game_file))

    rom.setFileByName("a/1/2/6", narc.save())
