
from typing import TYPE_CHECKING
from zipfile import ZipFile

from ...ndspy.rom import NintendoDSRom
from ...ndspy.narc import NARC

if TYPE_CHECKING:
    from ...rom import PokemonBWPatch


def patch_wild(rom: NintendoDSRom, world_package: str, bw_patch_instance: "PokemonBWPatch",
               files_dump: ZipFile) -> None:
    from ...data.adjustments import wild_levels

    file_wild = NARC(rom.getFileByName("a/1/2/6"))
    files = [bytearray(file) for file in file_wild.files]
    methods: dict[str, tuple[int, int]] = {  # starting slot (inclusive), ending slot (exclusive)
        "grass": (0, 12),
        "dark grass": (12, 24),
        "rustling grass": (24, 36),
        "surfing": (36, 41),
        "surfing rippling": (41, 46),
        "fishing": (46, 51),
        "fishing rippling": (51, 56),
    }

    for adjustment in wild_levels.adjustments:
        start, end = methods[adjustment.method]
        for slot in range(start, end):
            slot_pos = 8 + (adjustment.season * (56 * 4 + 8)) + (4 * slot)
            files[adjustment.file][slot_pos+2] = adjustment.calculation(files[adjustment.file][slot_pos+2])
            files[adjustment.file][slot_pos+3] = adjustment.calculation(files[adjustment.file][slot_pos+3])

    for i in range(len(files)):
        file_wild.files[i] = bytes(files[i])
        files_dump.writestr(f"a126/{i}", bytes(files[i]))
    rom.setFileByName("a/1/2/6", file_wild.save())


def patch_trainer(rom: NintendoDSRom, world_package: str, bw_patch_instance: "PokemonBWPatch",
                  files_dump: ZipFile) -> None:
    from ...data.adjustments import trainer_levels

    file_data = NARC(rom.getFileByName("a/0/9/2"))
    file_pokemon = NARC(rom.getFileByName("a/0/9/3"))

    for adjustment in trainer_levels.adjustments:
        trainer_data = file_data.files[adjustment.trainer_id]
        trainer_pokemon = bytearray(file_pokemon.files[adjustment.trainer_id])
        trainer_format = trainer_data[0]
        pkmn_count = trainer_data[3]
        has_held_items = trainer_format >= 2
        has_unique_moves = trainer_format % 2 == 1
        pkmn_entry_length = 8 + (8 if has_unique_moves else 0) + (2 if has_held_items else 0)
        for i in range(pkmn_count):
            pos = i * pkmn_entry_length + 2
            trainer_pokemon[pos] = adjustment.calculation(trainer_pokemon[pos])
        file_pokemon.files[adjustment.trainer_id] = bytes(trainer_pokemon)
        files_dump.writestr(f"a093/{adjustment.trainer_id}", bytes(trainer_pokemon))

    rom.setFileByName("a/0/9/3", file_pokemon.save())
