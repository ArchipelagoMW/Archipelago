'''
Object representing an FF4 rom. Portions of the ROM that
are of interest are exposed as binary data (lists of bytes).
This binary data may then be altered or replaced, and then
saved back to the file, in which case this object handles
the reassignment of space, pointer tables, etc. to match.
'''

import struct
import math
import hashlib
import io
from .datatable import DataTable
from .dataarray import DataArray

NUM_NPCS = 511
NUM_EVENT_SCRIPTS = 256
NUM_MAPS = 383
NUM_TEXT_BANK1 = 512
NUM_TEXT_BANK2 = 768
NUM_TEXT_BANK3 = 256
NUM_TEXT_BATTLE = 0xBA
NUM_TEXT_ALERTS = 0x3B
NUM_TEXT_STATUS = 32
NUM_TEXT_MAP_NAMES = 0x79
NUM_TEXT_DESCRIPTIONS = 60
NUM_TEXT_MAP_NAMES = 0x79
NUM_EVENT_CALLS = 255
NUM_MONSTERS = 0xE0
NUM_COMMANDS = 26
NUM_ITEMS = 256
NUM_SHOPS = 33
NUM_ACTORS = 21
NUM_DROP_TABLES = 64
NUM_MONSTERS = 0xE0
NUM_FORMATIONS = 512
NUM_PLAYER_SPELLS = 0x48
NUM_NAMED_ENEMY_SPELLS = 0xB0 - NUM_PLAYER_SPELLS
NUM_SPELLS = 0xC0
NUM_SPELL_SETS = 13
NUM_AI_CONDITIONS = 0x80

FF2USV10_MD5 = '4fa9e542b954dcb954d5ce38188d9d41'
FF2USV11_MD5 = '27d02a4f03e172e029c9b82ac3db79f7'

class RomError(Exception):
    pass

class Rom:
    def __init__(self, rom=None, ignore_checksum=False):
        self._raw_rom_data = None
        self._patches = []
        self._data_structs = []
        if rom is not None:
            self.load_rom(rom, ignore_checksum)

    def load_rom(self, rom, ignore_checksum=False):
        if type(rom) is str:
            close_stream = True
            infile = open(rom, 'rb')
        else:
            close_stream = False
            infile = rom

        self._raw_rom_data = infile.read()

        if not ignore_checksum:
            if len(self._raw_rom_data) != 0x100000:
                if len(self._raw_rom_data) == 0x100200:
                    # strip ROM header
                    self._raw_rom_data = self._raw_rom_data[0x200:]
                    if close_stream:
                        infile.close()
                    infile = io.BytesIO(self._raw_rom_data)
                    close_stream = False
                else:
                    raise RomError("ROM file size is incorrect; expected 0x100000 (or 0x100200 for headered), got 0x{:X}".format(len(self._raw_rom_data)))

            checksum = hashlib.md5()
            checksum.update(self._raw_rom_data)
            if checksum.hexdigest().lower() not in [FF2USV10_MD5, FF2USV11_MD5]:
                raise RomError("ROM MD5 check failed -- data has checksum {}".format(checksum.hexdigest()))

        self.event_scripts = self.create_data_table(infile, pointer_address=0x90000, data_address=0x90200, data_count=NUM_EVENT_SCRIPTS, last_data_size=1, data_overflow_address=0x97000)

        self.npc_sprites = self.create_data_array(infile, 0x97000, NUM_NPCS)
        self.npc_event_calls = self.create_data_table(infile, pointer_address=0x99800, data_address=0x99C00, data_count=NUM_NPCS, use_end_pointer=True, data_overflow_address=0x9A300)

        self.map_infos = self.create_data_table(infile, data_address=0xA9C84, data_count=NUM_MAPS, data_size=13)
        self.placement_groups = self.create_data_table(infile, pointer_address=0x98000, data_address=0x98300, data_count=NUM_MAPS, data_consume_func=_consume_placements, data_overflow_address=0x99700, nonlinear=True)
        self.map_trigger_sets = self.create_data_table(infile, pointer_address=0xA8000, data_address=0xA8300, data_count=NUM_MAPS, use_end_pointer=True, data_overflow_address=0xA961F)
        self.world_trigger_sets = self.create_data_table(infile, pointer_address=0xCFE60, data_address=0xCFE66, data_count=3, data_overflow_address=0xD0000, data_filler=[0x00, 0x00, 0xFF, 0xFF, 0x00])

        self.map_grids = self.create_data_table(infile, pointer_address=0xB8000, data_address=0xB8000, data_count=NUM_MAPS, use_end_pointer=True, pointer_offset_regions={0x100: 0x8000})
        self.tilesets = self.create_data_table(infile, data_address=0xA0E00, data_count=16, data_size=0x100)

        self.event_calls = self.create_data_table(infile, pointer_address=0x97260, data_address=0x97460, data_count=NUM_EVENT_CALLS, use_end_pointer=True, data_overflow_address=0x97660)

        self.text_bank1 = self.create_data_table(infile, pointer_address=0x80000, data_address=0x80400, data_count=NUM_TEXT_BANK1, data_consume_func=_consume_text, data_overflow_address=0x88000) 
        self.text_bank2 = self.create_data_table(infile, pointer_address=0x88000, data_address=0x88300, data_count=NUM_MAPS, use_end_pointer=True, data_overflow_address=0x90000)
        self.text_bank3 = self.create_data_table(infile, pointer_address=0x9A500, data_address=0x9A700, data_count=NUM_TEXT_BANK3, data_consume_func=_consume_text, data_overflow_address=0x9D200)
        self.text_battle = self.create_data_table(infile, pointer_address=0x77200, data_address=0x68000, data_count=NUM_TEXT_BATTLE, data_consume_func=_consume_text, data_overflow_address=0x78000)
        self.text_alerts = self.create_data_table(infile, pointer_address=0x7B000, data_address=0x70000, data_count=NUM_TEXT_ALERTS, data_consume_func=_consume_text, data_overflow_address=0x7B400, nonlinear=True)
        self.text_status = self.create_data_table(infile, pointer_address=0x7B400, data_address=0x70000, data_count=NUM_TEXT_STATUS, data_consume_func=_consume_text, data_overflow_address=0x7B500, nonlinear=True)
        self.text_monster_names = self.create_data_table(infile, data_address=0x71800, data_count=NUM_MONSTERS, data_size=8)
        self.text_command_names = self.create_data_table(infile, data_address=0x7A7C6, data_count=NUM_COMMANDS, data_size=5)
        self.text_map_names = self.create_data_table(infile, data_address=0xA9620, data_count=NUM_TEXT_MAP_NAMES, data_consume_func=_consume_text, data_overflow_address=0xA9C80)
        self.text_item_names = self.create_data_table(infile, data_address=0x78000, data_count=NUM_ITEMS, data_size=9)
        self.text_spell_names = self.create_data_table(infile, data_address=0x78900, data_count=NUM_PLAYER_SPELLS, data_size=6)
        self.text_enemy_spell_names = self.create_data_table(infile, data_address=0x78AB0, data_count=NUM_NAMED_ENEMY_SPELLS, data_size=8)

        self.monster_gp = self.create_data_array(infile, 0x72000, NUM_MONSTERS, data_size=2)
        self.monster_xp = self.create_data_array(infile, 0x721C0, NUM_MONSTERS, data_size=2)
        self.monster_gfx = self.create_data_table(infile, data_address=0x7CA00, data_count=NUM_MONSTERS, data_size=4)
        self.monsters = self.create_data_table(infile, pointer_address=0x726A0, data_address=0x68000, data_count=NUM_MONSTERS, data_consume_func=_consume_monster, data_overflow_address=0x736c0, nonlinear=True)
        self.monster_stats = self.create_data_table(infile, data_address=0x72380, data_count=0xE0, data_size=3)
        self.monster_speeds = self.create_data_table(infile, data_address=0x72620, data_count=0x40, data_size=2)

        self.monster_scripts = self.create_data_table(infile, data_address=0x76900, data_count=0x100, data_consume_func=_consume_until(0xFF))
        self.moon_monster_scripts = self.create_data_table(infile, data_address=0x736C0, data_count=0x5A, data_consume_func=_consume_until(0xFF))
        self.ai_conditions = self.create_data_table(infile, data_address=0x76700, data_count=NUM_AI_CONDITIONS, data_size=4)
        self.ai_condition_sets = self.create_data_table(infile, data_address=0x76600, data_count=0x62, data_consume_func=_consume_until(0xFF), data_overflow_address=0x76700)
        self.ai_groups = self.create_data_table(infile, data_address=0x76030, data_count=0xFE, data_consume_func=_consume_until(0xFF), data_overflow_address=0x76600)
        self.ai_hp_thresholds = self.create_data_array(infile, 0x76000, 24, 2)

        self.spells = self.create_data_table(infile, data_address=0x797A0, data_count=NUM_SPELLS, data_size=6)

        self.formations = self.create_data_table(infile, data_address=0x70000, data_count=NUM_FORMATIONS, data_size=8)

        self.shops = self.create_data_table(infile, data_address=0x9A300, data_count=NUM_SHOPS, data_size=8)

        num_npc_active_flag_bytes = int(math.ceil(NUM_NPCS / 8.0))
        self.npc_active_flags = self.create_data_array(infile, 0x97200, num_npc_active_flag_bytes)

        self.actor_name_ids = self.create_data_array(infile, 0x08457, NUM_ACTORS)
        self.actor_load_info = self.create_data_array(infile, 0x0669A, NUM_ACTORS)
        self.actor_save_info = self.create_data_array(infile, 0x0671D, NUM_ACTORS)
        self.actor_commands = self.create_data_table(infile, data_address=0x9FD55, data_count=NUM_ACTORS, data_size=5)
        self.actor_gear = self.create_data_table(infile, data_address=0x7AB00, data_count=NUM_ACTORS, data_size=7)

        self.spell_sets = self.create_data_table(infile, data_address=0x7C8C0, data_count=NUM_SPELL_SETS, data_consume_func=_consume_until(0xFF, or_length=24), data_overflow_address=0x7CA00)
        self.learned_spells = self.create_data_table(infile, data_address=0x7C700, data_count=NUM_SPELL_SETS, data_consume_func=_consume_until(0xFF), data_overflow_address=0x7C8C0)

        self.drop_tables = self.create_data_table(infile, data_address=0x71F00, data_count=NUM_DROP_TABLES, data_size=4)

        infile.seek(0x9F36D)
        self.text_credits = list(struct.unpack('1130B', infile.read(1130)))
        self._original_text_credits = list(self.text_credits)

        if close_stream:
            infile.close()

    def create_data_table(self, *args, **kwargs):
        dt = DataTable(*args, **kwargs)
        self._data_structs.append(dt)
        return dt

    def create_data_array(self, *args, **kwargs):
        da = DataArray(*args, **kwargs)
        self._data_structs.append(da)
        return da

    def add_patch(self, address, byte_list):
        for patch in self._patches:
            if address < (patch[0] + len(patch[1])) and (address + len(byte_list)) > patch[0]:
                raise RomError("Patch at {:X} conflicts with prior patch at {:X}".format(address, patch[0]))
        self._patches.append( (address, byte_list) )

    def save_rom(self, rom):
        if type(rom) is str:
            outfile = io.BytesIO()
        else:
            outfile = rom

        outfile.write(self._raw_rom_data)

        for dt in self._data_structs:
            dt.save_if_changed(outfile)

        if self.text_credits != self._original_text_credits:
            outfile.seek(0x9F36D)
            outfile.write(struct.pack('{}B'.format(len(self.text_credits)), *self.text_credits))

        # expand rom size to fit patches that apply past the current boundary
        outfile.seek(0, 2)
        rom_size = outfile.tell()

        if self._patches:
            farthest_patch = max(self._patches, key=lambda p:p[0] + len(p[1]))
            minimum_rom_size = farthest_patch[0] + len(farthest_patch[1])

            if rom_size < minimum_rom_size:
                # increase rom size to nearest 8mbit boundary
                if minimum_rom_size & 0xFFFFF:
                    target_rom_size = (minimum_rom_size & 0xFF00000) + 0x100000
                else:
                    target_rom_size = minimum_rom_size

                for i in range(target_rom_size - rom_size):
                    outfile.write(b"\xFF")
                rom_size = target_rom_size

        for patch in self._patches:
            outfile.seek(patch[0])
            if isinstance(patch[1], bytes):
                outfile.write(patch[1])
            else:
                outfile.write(struct.pack('{}B'.format(len(patch[1])), *patch[1]))

        # update checksum
        outfile.seek(0)
        checksum = sum(struct.unpack('{}B'.format(rom_size), outfile.read(rom_size))) & 0xFFFF
        outfile.seek(0x7FDE)
        outfile.write(struct.pack('<H', checksum))
        outfile.seek(0x7FDC)
        outfile.write(struct.pack('<H', (~checksum) & 0xFFFF))

        if type(rom) is str:
            outfile.seek(0)
            with open(rom, 'wb') as actual_outfile:
                actual_outfile.write(outfile.read())

            outfile.close()


def _consume_text(stream):
    data = []
    while True:
        val = struct.unpack('B', stream.read(1))[0]
        data.append(val)
        if val == 0:
            break
        if val == 4 or val == 3 or val == 5:
            val = struct.unpack('B', stream.read(1))[0]
            data.append(val)
    return data

def _consume_placements(stream):
    data = []
    for i in range(13):
        b = struct.unpack('B', stream.read(1))[0]
        data.append(b)
        if b == 0:
            break
        if i == 12:
            raise ValueError("Expected $00 after list of 12 placements")
        data.extend(struct.unpack('BBB', stream.read(3)))

    return data

def _consume_until(byte_value, or_length=None):
    def func(stream):
        data = []
        while(True):
            b = struct.unpack('B', stream.read(1))[0]
            data.append(b)
            if b == byte_value or (or_length is not None and len(data) == or_length):
                break
        return data
    return func

def _consume_monster(stream):
    data = []
    data.extend(struct.unpack('10B', stream.read(10)))
    flags = data[9]
    if flags & 0x80:
        data.extend(struct.unpack('3B', stream.read(3)))
    if flags & 0x40:
        data.extend(struct.unpack('3B', stream.read(3)))
    if flags & 0x20:
        data.extend(struct.unpack('B', stream.read(1)))
    if flags & 0x10:
        data.extend(struct.unpack('B', stream.read(1)))
    if flags & 0x08:
        data.extend(struct.unpack('B', stream.read(1)))
    if flags & 0x04:
        data.extend(struct.unpack('B', stream.read(1)))
    return data


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('romfile')
    args = parser.parse_args()

    test_rom = Rom(args.romfile)
