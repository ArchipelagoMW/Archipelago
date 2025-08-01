#Much of this is heavily inspired from and/or based on az64's / Deathbasket's MM randomizer

import os
from .Utils import compare_version, data_path


# Format: (Title, Sequence ID)
bgm_sequence_ids = [
    ("Hyrule Field", 0x02),
    ("Dodongos Cavern", 0x18),
    ("Kakariko Adult", 0x19),
    ("Battle", 0x1A),
    ("Boss Battle", 0x1B),
    ("Inside Deku Tree", 0x1C),
    ("Market", 0x1D),
    ("Title Theme", 0x1E),
    ("House", 0x1F),
    ("Jabu Jabu", 0x26),
    ("Kakariko Child", 0x27),
    ("Fairy Fountain", 0x28),
    ("Zelda Theme", 0x29),
    ("Fire Temple", 0x2A),
    ("Forest Temple", 0x2C),
    ("Castle Courtyard", 0x2D),
    ("Ganondorf Theme", 0x2E),
    ("Lon Lon Ranch", 0x2F),
    ("Goron City", 0x30),
    ("Miniboss Battle", 0x38),
    ("Temple of Time", 0x3A),
    ("Kokiri Forest", 0x3C),
    ("Lost Woods", 0x3E),
    ("Spirit Temple", 0x3F),
    ("Horse Race", 0x40),
    ("Ingo Theme", 0x42),
    ("Fairy Flying", 0x4A),
    ("Deku Tree", 0x4B),
    ("Windmill Hut", 0x4C),
    ("Shooting Gallery", 0x4E),
    ("Sheik Theme", 0x4F),
    ("Zoras Domain", 0x50),
    ("Shop", 0x55),
    ("Chamber of the Sages", 0x56),
    ("Ice Cavern", 0x58),
    ("Kaepora Gaebora", 0x5A),
    ("Shadow Temple", 0x5B),
    ("Water Temple", 0x5C),
    ("Gerudo Valley", 0x5F),
    ("Potion Shop", 0x60),
    ("Kotake and Koume", 0x61),
    ("Castle Escape", 0x62),
    ("Castle Underground", 0x63),
    ("Ganondorf Battle", 0x64),
    ("Ganon Battle", 0x65),
    ("Fire Boss", 0x6B),
    ("Mini-game", 0x6C)
]

fanfare_sequence_ids = [
    ("Game Over", 0x20),
    ("Boss Defeated", 0x21),
    ("Item Get", 0x22),
    ("Ganondorf Appears", 0x23),
    ("Heart Container Get", 0x24),
    ("Treasure Chest", 0x2B),
    ("Spirit Stone Get", 0x32),
    ("Heart Piece Get", 0x39),
    ("Escape from Ranch", 0x3B),
    ("Learn Song", 0x3D),
    ("Epona Race Goal", 0x41),
    ("Medallion Get", 0x43),
    ("Zelda Turns Around", 0x51),
    ("Master Sword", 0x53),
    ("Door of Time", 0x59)
]

ocarina_sequence_ids = [
    ("Prelude of Light", 0x25),
    ("Bolero of Fire", 0x33),
    ("Minuet of Forest", 0x34),
    ("Serenade of Water", 0x35),
    ("Requiem of Spirit", 0x36),
    ("Nocturne of Shadow", 0x37),
    ("Saria's Song", 0x44),
    ("Epona's Song", 0x45),
    ("Zelda's Lullaby", 0x46),
    ("Sun's Song", 0x47),
    ("Song of Time", 0x48),
    ("Song of Storms", 0x49)
]

# Represents the information associated with a sequence, aside from the sequence data itself
class TableEntry(object):
    def __init__(self, name, cosmetic_name, type = 0x0202, instrument_set = 0x03, replaces = -1, vanilla_id = -1):
        self.name = name
        self.cosmetic_name = cosmetic_name
        self.replaces = replaces
        self.vanilla_id = vanilla_id
        self.type = type
        self.instrument_set = instrument_set


    def copy(self):
        copy = TableEntry(self.name, self.cosmetic_name, self.type, self.instrument_set, self.replaces, self.vanilla_id)
        return copy


# Represents actual sequence data, along with metadata for the sequence data block
class Sequence(object):
    def __init__(self):
        self.address = -1
        self.size = -1
        self.data = []


def process_sequences(rom, sequences, target_sequences, disabled_source_sequences, disabled_target_sequences, ids, seq_type = 'bgm'):
    # Process vanilla music data
    for bgm in ids:
        # Get sequence metadata
        name = bgm[0]
        cosmetic_name = name
        type = rom.read_int16(0xB89AE8 + (bgm[1] * 0x10))
        instrument_set = rom.read_byte(0xB89911 + 0xDD + (bgm[1] * 2))
        id = bgm[1]

        # Create new sequences
        seq = TableEntry(name, cosmetic_name, type, instrument_set, vanilla_id = id)
        target = TableEntry(name, cosmetic_name, type, instrument_set, replaces = id)

        # Special handling for file select/fairy fountain
        if seq.vanilla_id != 0x57 and cosmetic_name not in disabled_source_sequences:
            sequences.append(seq)
        if cosmetic_name not in disabled_target_sequences:
            target_sequences.append(target)

    # If present, load the file containing custom music to exclude
    try:
        with open(os.path.join(data_path(), u'custom_music_exclusion.txt')) as excl_in:
            seq_exclusion_list = excl_in.readlines()
        seq_exclusion_list = [seq.rstrip() for seq in seq_exclusion_list if seq[0] != '#']
        seq_exclusion_list = [seq for seq in seq_exclusion_list if seq.endswith('.meta')]
    except FileNotFoundError:
        seq_exclusion_list = []

    # Process music data in data/Music/
    # Each sequence requires a valid .seq sequence file and a .meta metadata file
    # Current .meta format: Cosmetic Name\nInstrument Set\nPool
    for dirpath, _, filenames in os.walk(u'./data/Music', followlinks=True):
        for fname in filenames:
            # Skip if included in exclusion file
            if fname in seq_exclusion_list:
                continue

            # Find meta file and check if corresponding seq file exists
            if fname.endswith('.meta') and os.path.isfile(os.path.join(dirpath, fname.split('.')[0] + '.seq')):
                # Read meta info
                try:
                    with open(os.path.join(dirpath, fname), 'r') as stream:
                        lines = stream.readlines()
                    # Strip newline(s)
                    lines = [line.rstrip() for line in lines]
                except FileNotFoundError as ex:
                    raise FileNotFoundError('No meta file for: "' + fname + '". This should never happen')

                # Create new sequence, checking third line for correct type
                if (len(lines) > 2 and (lines[2].lower() == seq_type.lower() or lines[2] == '')) or (len(lines) <= 2 and seq_type == 'bgm'):
                    seq = TableEntry(os.path.join(dirpath, fname.split('.')[0]), lines[0], instrument_set = int(lines[1], 16))

                    if seq.instrument_set < 0x00 or seq.instrument_set > 0x25:
                        raise Exception('Sequence instrument must be in range [0x00, 0x25]')

                    if seq.cosmetic_name not in disabled_source_sequences:
                        sequences.append(seq)

    return sequences, target_sequences


def shuffle_music(sequences, target_sequences, music_mapping, log, rand):
    sequence_dict = {}
    sequence_ids = []

    for sequence in sequences:
        if sequence.cosmetic_name == "None":
            raise Exception('Sequences should not be named "None" as that is used for disabled music. Sequence with improper name: %s' % sequence.name)
        if sequence.cosmetic_name in sequence_dict:
            raise Exception('Sequence names should be unique. Duplicate sequence name: %s' % sequence.cosmetic_name)
        sequence_dict[sequence.cosmetic_name] = sequence
        if sequence.cosmetic_name not in music_mapping.values():
            sequence_ids.append(sequence.cosmetic_name)

    # Shuffle the sequences
    if len(sequences) < len(target_sequences):
        raise Exception(f"Not enough custom music/fanfares ({len(sequences)}) to omit base Ocarina of Time sequences ({len(target_sequences)}).")
    rand.shuffle(sequence_ids)

    sequences = []
    for target_sequence in target_sequences:
        sequence = sequence_dict[sequence_ids.pop()].copy() if target_sequence.cosmetic_name not in music_mapping \
            else ("None", 0x0) if music_mapping[target_sequence.cosmetic_name] == "None" \
            else sequence_dict[music_mapping[target_sequence.cosmetic_name]].copy()
        sequences.append(sequence)
        sequence.replaces = target_sequence.replaces
        log[target_sequence.cosmetic_name] = sequence.cosmetic_name

    return sequences, log


def rebuild_sequences(rom, sequences):
    # List of sequences (actual sequence data objects) containing the vanilla sequence data
    old_sequences = []

    for i in range(0x6E):
        # Create new sequence object, an entry for the audio sequence
        entry = Sequence()
        # Get the address for the entry's pointer table entry
        entry_address = 0xB89AE0 + (i * 0x10)
        # Extract the info from the pointer table entry
        entry.address = rom.read_int32(entry_address)
        entry.size = rom.read_int32(entry_address + 0x04)

        # If size > 0, read the sequence data from the rom into the sequence object
        if entry.size > 0:
            entry.data = rom.read_bytes(entry.address + 0x029DE0, entry.size)
        else:
            s = [seq for seq in sequences if seq.replaces == i]
            if s != [] and entry.address > 0 and entry.address < 128:
                s = s.pop()
                if s.replaces != 0x28:
                    s.replaces = entry.address
                else:
                    # Special handling for file select/fairy fountain
                    entry.data = old_sequences[0x57].data
                    entry.size = old_sequences[0x57].size

        old_sequences.append(entry)

    # List of sequences containing the new sequence data
    new_sequences = []
    address = 0
    # Byte array to hold the data for the whole audio sequence
    new_audio_sequence = []

    for i in range(0x6E):
        new_entry = Sequence()
        # If sequence size is 0, the address doesn't matter and it doesn't effect the current address
        if old_sequences[i].size == 0:
            new_entry.address = old_sequences[i].address
        # Continue from the end of the new sequence table
        else:
            new_entry.address = address

        s = [seq for seq in sequences if seq.replaces == i]
        if s != []:
            assert len(s) == 1
            s = s.pop()
            # If we are using a vanilla sequence, get its data from old_sequences
            if s.vanilla_id != -1:
                new_entry.size = old_sequences[s.vanilla_id].size
                new_entry.data = old_sequences[s.vanilla_id].data
            else:
                # Read sequence info
                try:
                    with open(s.name + '.seq', 'rb') as stream:
                        new_entry.data = bytearray(stream.read())
                    new_entry.size = len(new_entry.data)
                    if new_entry.size <= 0x10:
                        raise Exception('Invalid sequence file "' + s.name + '.seq"')
                    new_entry.data[1] = 0x20
                except FileNotFoundError as ex:
                    raise FileNotFoundError('No sequence file for: "' + s.name + '"')
        else:
            new_entry.size = old_sequences[i].size
            new_entry.data = old_sequences[i].data

        new_sequences.append(new_entry)

        # Concatenate the full audio sequence and the new sequence data
        if new_entry.data != [] and new_entry.size > 0:
            # Align sequences to 0x10
            if new_entry.size % 0x10 != 0:
                new_entry.data.extend(bytearray(0x10 - (new_entry.size % 0x10)))
                new_entry.size += 0x10 - (new_entry.size % 0x10)
            new_audio_sequence.extend(new_entry.data)
            # Increment the current address by the size of the new sequence
            address += new_entry.size

    # Check if the new audio sequence is larger than the vanilla one
    if address > 0x04F690:
        # Zero out the old audio sequence
        rom.buffer[0x029DE0 : 0x029DE0 + 0x04F690] = [0] * 0x04F690

        # Append new audio sequence
        new_address = rom.free_space()
        rom.write_bytes(new_address, new_audio_sequence)

        #Update dmatable
        rom.update_dmadata_record(0x029DE0, new_address, new_address + address)

    else:
        # Write new audio sequence file
        rom.write_bytes(0x029DE0, new_audio_sequence)

    # Update pointer table
    for i in range(0x6E):
        rom.write_int32(0xB89AE0 + (i * 0x10), new_sequences[i].address)
        rom.write_int32(0xB89AE0 + (i * 0x10) + 0x04, new_sequences[i].size)
        s = [seq for seq in sequences if seq.replaces == i]
        if s != []:
            assert len(s) == 1
            s = s.pop()
            rom.write_int16(0xB89AE0 + (i * 0x10) + 0x08, s.type)

    # Update instrument sets
    for i in range(0x6E):
        base = 0xB89911 + 0xDD + (i * 2)
        j = -1
        if new_sequences[i].size == 0:
            try:
                j = [seq for seq in sequences if seq.replaces == new_sequences[i].address].pop()
            except:
                j = -1
        else:
            try:
                j = [seq for seq in sequences if seq.replaces == i].pop()
            except:
                j = -1
        if j != -1:
            rom.write_byte(base, j.instrument_set)


def shuffle_pointers_table(rom, ids, music_mapping, log, rand):
    # Read in all the Music data
    bgm_data = {}
    bgm_ids = []

    for bgm in ids:
        bgm_sequence = rom.read_bytes(0xB89AE0 + (bgm[1] * 0x10), 0x10)
        bgm_instrument = rom.read_int16(0xB89910 + 0xDD + (bgm[1] * 2))
        bgm_data[bgm[0]] = (bgm[0], bgm_sequence, bgm_instrument)
        if bgm[0] not in music_mapping.values():
            bgm_ids.append(bgm[0])

    # shuffle data
    rand.shuffle(bgm_ids)

    # Write Music data back in random ordering
    for bgm in ids:
        if bgm[0] in music_mapping and music_mapping[bgm[0]] in bgm_data:
            bgm_name = music_mapping[bgm[0]]
        else:
            bgm_name = bgm_ids.pop()
        bgm_name, bgm_sequence, bgm_instrument = bgm_data[bgm_name]
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), bgm_sequence)
        rom.write_int16(0xB89910 + 0xDD + (bgm[1] * 2), bgm_instrument)
        log[bgm[0]] = bgm_name

    # Write Fairy Fountain instrument to File Select (uses same track but different instrument set pointer for some reason)
    rom.write_int16(0xB89910 + 0xDD + (0x57 * 2), rom.read_int16(0xB89910 + 0xDD + (0x28 * 2)))
    return log


def randomize_music(rom, ootworld, music_mapping):
    log = {}
    errors = []
    sequences = []
    target_sequences = []
    fanfare_sequences = []
    fanfare_target_sequences = []
    disabled_source_sequences = {}
    disabled_target_sequences = {}

    # Make sure we aren't operating directly on these.
    music_mapping = music_mapping.copy()
    bgm_ids = bgm_sequence_ids.copy()
    ff_ids = fanfare_sequence_ids.copy()

    # Check if we have mapped music for BGM, Fanfares, or Ocarina Fanfares
    bgm_mapped = any(bgm[0] in music_mapping for bgm in bgm_ids)
    ff_mapped = any(ff[0] in music_mapping for ff in ff_ids)
    ocarina_mapped = any(ocarina[0] in music_mapping for ocarina in ocarina_sequence_ids)

    # Include ocarina songs in fanfare pool if checked
    if ootworld.ocarina_fanfares or ocarina_mapped:
        ff_ids.extend(ocarina_sequence_ids)

    # Flag sequence locations that are set to off for disabling.
    disabled_ids = []
    if ootworld.background_music == 'off':
        disabled_ids += [music_id for music_id in bgm_ids]
    if ootworld.fanfares == 'off':
        disabled_ids += [music_id for music_id in ff_ids]
        disabled_ids += [music_id for music_id in ocarina_sequence_ids]
    for bgm in [music_id for music_id in bgm_ids + ff_ids + ocarina_sequence_ids]:
        if music_mapping.get(bgm[0], '') == "None":
            disabled_target_sequences[bgm[0]] = bgm
    for bgm in disabled_ids:
        if bgm[0] not in music_mapping:
            music_mapping[bgm[0]] = "None"
            disabled_target_sequences[bgm[0]] = bgm

    # Map music to itself if music is set to normal.
    normal_ids = []
    if ootworld.background_music == 'normal' and bgm_mapped:
        normal_ids += [music_id for music_id in bgm_ids]
    if ootworld.fanfares == 'normal' and (ff_mapped or ocarina_mapped):
        normal_ids += [music_id for music_id in ff_ids]
    if not ootworld.ocarina_fanfares and ootworld.fanfares == 'normal' and ocarina_mapped:
        normal_ids += [music_id for music_id in ocarina_sequence_ids]
    for bgm in normal_ids:
        if bgm[0] not in music_mapping:
            music_mapping[bgm[0]] = bgm[0]

    # If not creating patch file, shuffle audio sequences. Otherwise, shuffle pointer table
    # If generating from patch, also do a version check to make sure custom sequences are supported.
    # custom_sequences_enabled = ootworld.compress_rom != 'Patch'
    # if ootworld.patch_file != '':
    #     rom_version_bytes = rom.read_bytes(0x35, 3)
    #     rom_version = f'{rom_version_bytes[0]}.{rom_version_bytes[1]}.{rom_version_bytes[2]}'
    #     if compare_version(rom_version, '4.11.13') < 0:
    #         errors.append("Custom music is not supported by this patch version. Only randomizing vanilla music.")
    #         custom_sequences_enabled = False
    # if custom_sequences_enabled:
    #     if ootworld.background_music in ['random', 'random_custom_only'] or bgm_mapped:
    #         process_sequences(rom, sequences, target_sequences, disabled_source_sequences, disabled_target_sequences, bgm_ids)
    #         if ootworld.background_music == 'random_custom_only':
    #             sequences = [seq for seq in sequences if seq.cosmetic_name not in [x[0] for x in bgm_ids] or seq.cosmetic_name in music_mapping.values()]
    #         sequences, log = shuffle_music(sequences, target_sequences, music_mapping, log, ootworld.random)

    #     if ootworld.fanfares in ['random', 'random_custom_only'] or ff_mapped or ocarina_mapped:
    #         process_sequences(rom, fanfare_sequences, fanfare_target_sequences, disabled_source_sequences, disabled_target_sequences, ff_ids, 'fanfare')
    #         if ootworld.fanfares == 'random_custom_only':
    #             fanfare_sequences = [seq for seq in fanfare_sequences if seq.cosmetic_name not in [x[0] for x in fanfare_sequence_ids] or seq.cosmetic_name in music_mapping.values()]
    #         fanfare_sequences, log = shuffle_music(fanfare_sequences, fanfare_target_sequences, music_mapping, log, ootworld.random)

    #     if disabled_source_sequences:
    #         log = disable_music(rom, disabled_source_sequences.values(), log)

    #     rebuild_sequences(rom, sequences + fanfare_sequences)
    # else:
    if ootworld.background_music == 'randomized' or bgm_mapped:
        log = shuffle_pointers_table(rom, bgm_ids, music_mapping, log, ootworld.random)

    if ootworld.fanfares == 'randomized' or ff_mapped or ocarina_mapped:
        log = shuffle_pointers_table(rom, ff_ids, music_mapping, log, ootworld.random)
    # end_else
    if disabled_target_sequences:
        log = disable_music(rom, disabled_target_sequences.values(), log)

    return log, errors


def disable_music(rom, ids, log):
    # First track is no music
    blank_track = rom.read_bytes(0xB89AE0 + (0 * 0x10), 0x10)
    for bgm in ids:
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), blank_track)
        log[bgm[0]] = "None"

    return log


def restore_music(rom):
    # Restore all music from original
    for bgm in bgm_sequence_ids + fanfare_sequence_ids + ocarina_sequence_ids:
        bgm_sequence = rom.original.read_bytes(0xB89AE0 + (bgm[1] * 0x10), 0x10)
        rom.write_bytes(0xB89AE0 + (bgm[1] * 0x10), bgm_sequence)
        bgm_instrument = rom.original.read_int16(0xB89910 + 0xDD + (bgm[1] * 2))
        rom.write_int16(0xB89910 + 0xDD + (bgm[1] * 2), bgm_instrument)

    # restore file select instrument
    bgm_instrument = rom.original.read_int16(0xB89910 + 0xDD + (0x57 * 2))
    rom.write_int16(0xB89910 + 0xDD + (0x57 * 2), bgm_instrument)

    # Rebuild audioseq
    orig_start, orig_end, orig_size = rom.original._get_dmadata_record(0x7470)
    rom.write_bytes(orig_start, rom.original.read_bytes(orig_start, orig_size))

    # If Audioseq was relocated
    start, end, size = rom._get_dmadata_record(0x7470)
    if start != 0x029DE0:
        # Zero out old audioseq
        rom.write_bytes(start, [0] * size)
        rom.update_dmadata_record(start, orig_start, orig_end)

