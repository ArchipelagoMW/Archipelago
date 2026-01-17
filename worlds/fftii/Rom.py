import json
import os
import pkgutil

from pathlib import Path

import bsdiff4

import Utils
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APPatchExtension
from .enemyrando.EventCodes import EventCode
from .ErrorRecalc import ErrorRecalculator
from .data import memory
from .data.locations import rare_battle_location_names, dd_location_names
from .data.memory import victory_text_offsets, rare_battles_offset, dd_battles_offset
from .data.text import split_text_into_lines
from .data.logic.FFTLocation import LocationNames
from .enemyrando.RandomizedMapping import RandomizedMapping
from .enemyrando.BattleMappings import valid_shuffle_source_units
from .enemyrando.EventIDs import events
from .enemyrando.Job import Job
from .patchersuite.Sector import Sector
from .patchersuite.ENTDEntry import ENTDEntry
from .enemyrando.SourceUnit import SourceUnit
from .enemyrando.SpriteSet import SpriteSet
from .patchersuite.Unit import Unit, UnitTeam


def get_base_rom_as_bytes() -> bytes:
    with open(get_settings().fftii_options.rom_file, "rb") as infile:
        base_rom_bytes = bytes(Utils.read_snes_rom(infile))
    return base_rom_bytes


class FinalFantasyTacticsIIPatchExtension(APPatchExtension):
    game = "Final Fantasy Tactics Ivalice Island"


    @staticmethod
    def write_text_to_location(bytes_to_write, location, rom_data):
        sector_size = 0x930
        data_start = 0x18
        data_size = 0x800
        header_size = 0x18
        ec_size = 0x118
        other_size = header_size + ec_size

        current_sector = location // sector_size
        current_sector_start = current_sector * sector_size
        offset_in_sector = location % sector_size
        data_end = current_sector_start + data_start + data_size

        current_offset = location
        while len(bytes_to_write) > 0:
            rom_data[current_offset] = bytes_to_write.pop(0)
            current_offset += 1
            if current_offset >= data_end:
                current_offset = data_end + other_size
                current_sector = current_offset // sector_size
                current_sector_start = current_sector * sector_size
                data_end = current_sector_start + data_start + data_size
        pass

    @staticmethod
    def apply_enemy_rando(patch_dict, rom_data):
        mapping_dict: dict[EventCode, list[RandomizedMapping]] = {}
        for key, value in patch_dict.items():
            new_list = []
            for entry in value:
                new_list.append(RandomizedMapping.from_json(entry))
            mapping_dict[EventCode(int(key))] = new_list


        entd_size = 80 * 1024
        entd_sector_count = 40
        event_count = 128
        entd_start = 0x0875FD30

        total_entd_length = entd_sector_count * Sector.sector_size
        entd_list: list[bytearray] = list()
        all_entd_sectors: list[Sector] = list()
        for i in range(4):
            start = entd_start + (i * total_entd_length)
            entd = rom_data[start:start + total_entd_length]
            entd_sectors = []
            for j in range(entd_sector_count):
                new_sector = Sector(entd[j * Sector.sector_size:(j + 1) * Sector.sector_size])
                entd_sectors.append(new_sector)
                all_entd_sectors.append(new_sector)
            entd_data = bytearray()
            for sector in entd_sectors:
                entd_data.extend(sector.data)
            entd_list.append(entd_data)
        full_entd = bytearray()
        for entd in entd_list:
            full_entd.extend(entd)
        print(hex(len(full_entd)))
        used_units = []
        entd_entries: list[ENTDEntry] = list()
        for i in range(0x1D5):
            if i in events.keys():
                mapping_list: list[RandomizedMapping] = []
                if EventCode(i) in mapping_dict.keys():
                    mapping_list = mapping_dict[EventCode(i)]
                entd_data = full_entd[i * ENTDEntry.total_length:(i + 1) * ENTDEntry.total_length]
                new_entd_entry = ENTDEntry(entd_data, events[i], i * ENTDEntry.total_length)
                new_entd_entry.index = i
                for unit in new_entd_entry.units:
                    if unit[0] > 0 and unit[1] > 0:
                        new_unit = Unit(unit)
                        if new_unit.job != 0:
                            used_units.append(new_unit.job)
                    else:
                        new_unit = Unit(unit)
                    new_entd_entry.unit_datas.append(new_unit)
                used_sprite_sheets = set()
                used_source_units = set()
                for unit in new_entd_entry.unit_datas:
                    if unit.sprite_set > 0 and unit.team == UnitTeam.RED:
                        source_unit = SourceUnit(SpriteSet(unit.sprite_set), Job(unit.job), unit.gender)
                        if len(mapping_list) > 0:
                            for mapping_entry in mapping_list:
                                if source_unit == mapping_entry.source_unit:
                                    unit.set_new_data(mapping_entry.destination_unit)
                                    unit.apply_unit_data()
                        if source_unit in valid_shuffle_source_units:
                            used_source_units.add(source_unit)
                        if source_unit not in used_sprite_sheets:
                            used_sprite_sheets.add(source_unit)
                for source in used_source_units:
                    pass
                    #print(source)
                new_entd_entry.apply_data()
                entd_entries.append(new_entd_entry)
        new_full_entd: bytearray = full_entd.copy()
        for entd_entry in entd_entries:
            start_location: int = entd_entry.location
            end_location: int = entd_entry.location + ENTDEntry.total_length
            new_full_entd[start_location:end_location] = entd_entry.all_data
        new_all_entd_sectors: list[Sector] = list()
        for sector in all_entd_sectors:
            new_all_entd_sectors.append(Sector(sector.all_data))
        for i in range(len(new_full_entd)):
            # assert new_full_entd[i] == full_entd[i], (i, new_full_entd[i], full_entd[i])
            sector_number: int = i // 2048
            new_all_entd_sectors[sector_number].data[i % 2048] = new_full_entd[i]
        for i in range(len(all_entd_sectors)):
            for j in range(len(all_entd_sectors[i].data)):
                pass
                # assert all_entd_sectors[i].data[j] == new_all_entd_sectors[i].data[j]
            new_all_data: bytearray = bytearray()
            new_all_data.extend(new_all_entd_sectors[i].header)
            new_all_data.extend(new_all_entd_sectors[i].data)
            new_all_data.extend(new_all_entd_sectors[i].error)
            new_all_entd_sectors[i].all_data = new_all_data
        new_iso_data = bytearray(rom_data)
        new_sector_data: bytearray = bytearray()
        for sector in new_all_entd_sectors:
            new_sector_data.extend(sector.all_data)
        new_iso_data[entd_start:entd_start + len(new_sector_data)] = new_sector_data
        return new_iso_data

    @staticmethod
    def patch_bin(caller, iso, placement_file):
        patch_dict = json.loads(caller.get_file(placement_file))
        if patch_dict["APJobs"] == 1:
            base_patch = pkgutil.get_data(__name__, "fftiiapjobs.bsdiff4")
        else:
            base_patch = pkgutil.get_data(__name__, "fftiivanillajobs.bsdiff4")
        rom_data = bsdiff4.patch(iso, base_patch)
        rom_data = bytearray(rom_data)

        if "RareBattles" in patch_dict.keys():
            if patch_dict["RareBattles"] == 1:
                address, bit = memory.yaml_options["RareBattles"]
                rom_data[address] = rom_data[address] | bit
        if patch_dict["Sidequests"] == 1:
            address, bit = memory.yaml_options["Sidequests"]
            rom_data[address] = rom_data[address] | bit
        if patch_dict["FinalBattles"] == 1:
            address, bit = memory.yaml_options["FinalBattles"]
            rom_data[address] = rom_data[address] | bit
        if "EXPMultiplier" in patch_dict.keys():
            exp_mult_values = [0x00, 0x40, 0x80]
            exp_mult_value = exp_mult_values[patch_dict["EXPMultiplier"]]
            address = memory.yaml_options["EXPMultiplier"]
            rom_data[address] = exp_mult_value
        if "JPMultiplier" in patch_dict.keys():
            exp_mult_values = [0x00, 0x40, 0x80]
            exp_mult_value = exp_mult_values[patch_dict["JPMultiplier"]]
            address = memory.yaml_options["JPMultiplier"]
            rom_data[address] = exp_mult_value

        location_dict = patch_dict["LocationDict"]
        for location, text in location_dict.items():
            if location in victory_text_offsets:
                text_lines, byte_lines = split_text_into_lines(text)
                all_bytes = []
                for byte_line in byte_lines:
                    all_bytes.extend(byte_line)
                if isinstance(victory_text_offsets[location], list):
                    for offset in victory_text_offsets[location]:
                        bytes_to_write = all_bytes.copy()
                        FinalFantasyTacticsIIPatchExtension.write_text_to_location(bytes_to_write, offset, rom_data)
                else:
                    offset = victory_text_offsets[location]
                    FinalFantasyTacticsIIPatchExtension.write_text_to_location(all_bytes, offset, rom_data)


                #rom_data[offset:offset + len(all_bytes)] = all_bytes
        if LocationNames.MANDALIA_RARE.value in location_dict.keys():
            all_rare_bytes = []
            for location in rare_battle_location_names:
                text = location_dict[location]
                text_lines, byte_lines = split_text_into_lines(text)
                for byte_line in byte_lines:
                    all_rare_bytes.extend(byte_line)
            FinalFantasyTacticsIIPatchExtension.write_text_to_location(all_rare_bytes, rare_battles_offset, rom_data)
        if LocationNames.NOGIAS_SIDEQUEST.value in location_dict.keys():
            all_dd_bytes = []
            for location in dd_location_names:
                text = location_dict[location]
                text_lines, byte_lines = split_text_into_lines(text)
                for byte_line in byte_lines:
                    all_dd_bytes.extend(byte_line)
            FinalFantasyTacticsIIPatchExtension.write_text_to_location(all_dd_bytes, dd_battles_offset, rom_data)

        if False:
            rom_data = FinalFantasyTacticsIIPatchExtension.apply_enemy_rando(patch_dict["EnemyRandoMapping"], rom_data)
        rom_name_text = patch_dict["RomName"]
        rom_name = bytearray(rom_name_text, 'utf-8')
        rom_name.extend([0] * (20 - len(rom_name)))
        rom_data[memory.rom_name_location:memory.rom_name_location + 20] = bytes(rom_name[:20])
        rom_data[memory.volume_name_location:memory.volume_name_location + 20] = bytes(rom_name[:20])
        seed_hash = int(patch_dict["SeedHash"])
        seed_hash_bytes = seed_hash.to_bytes(2)
        rom_data[memory.seed_hash_location:memory.seed_hash_location + 2] = bytes(seed_hash_bytes)

        return rom_data



class FinalFantasyTacticsIIProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "Final Fantasy Tactics Ivalice Island"
    hash = "b156ba386436d20fd5ed8d37bab6b624"
    patch_file_ending = ".apfftii"
    result_file_ending = ".cue"

    procedure = [
        ("patch_bin", ["patch_file.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_as_bytes()

    def patch(self, target: str) -> None:
        file_name = target[:-4]
        if os.path.exists(file_name + ".cue"):
            os.unlink(file_name + ".cue")
        if os.path.exists(file_name + "patched" + ".bin"):
            os.unlink(file_name + "patched" + ".bin")

        super().patch(target)
        os.rename(target, file_name + "patched" + ".bin")
        error_recalculator = ErrorRecalculator(calculate_form_2_edc=False)
        stats = error_recalculator.recalc(target_file=Path(file_name + "patched" + ".bin"),
                                          base_file=get_settings().fftii_options.rom_file)
        print(
            f"{stats.identical_sectors} identical sectors out of {stats.total_sectors()}, {stats.recalc_sectors} sectors recalculated")
        print(f"{stats.edc_blocks_computed} EDC blocks computed, {stats.ecc_blocks_generated} ECC blocks generated")

        cue_text = f'FILE "{file_name}patched.bin" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00'
        with open(file_name + ".cue", "w") as cue_file:
            cue_file.write(cue_text)