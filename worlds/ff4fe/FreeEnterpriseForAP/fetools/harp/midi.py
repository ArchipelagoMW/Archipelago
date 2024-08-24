import io
import struct
import chardet

MIDI_TEXT_EVENTS = {
    0x01 : "Text",
    0x02 : "Copyright",
    0x03 : "Seq/Trk Name",
    0x04 : "Instr Name",
    0x05 : "Lyric",
    0x06 : "Marker",
    0x07 : "Cue",
}
for i in range(0x01, 0x10):
    MIDI_TEXT_EVENTS.setdefault(i, f'Text ({i:02X})')

MIDI_PARAM_COUNTS = {
    0x80 : 2,
    0x90 : 2,
    0xA0 : 2,
    0xB0 : 2,
    0xC0 : 1,
    0xD0 : 1,
    0xE0 : 2,
    0xF1 : 1,
    0xF2 : 2,
    0xF3 : 1
}

def _read_varint(stream):
    val = 0
    while True:
        b = stream.read(1)[0]
        val = (val << 7) | (b & 0x7F)
        if not (b & 0x80):
            return val

class MidiFile:
    def __init__(self, data):
        instream = io.BytesIO(data)

        # read midi chunks
        chunks = []
        while True:
            chunk_type = instream.read(4)
            if len(chunk_type) < 4:
                # eof
                break
            try:
                chunk_type = chunk_type.decode('ascii')
            except UnicodeDecodeError:
                chunk_type = '????'
            chunk_length = struct.unpack('>I', instream.read(4))[0]
            chunk_data = instream.read(chunk_length)

            chunks.append({'type' : chunk_type, 'data' : chunk_data})

        track_chunks = []
        self.unknown_chunks = []
        for chunk in chunks:
            if chunk['type'] == 'MThd':
                self.header_chunk = chunk['data']
            elif chunk['type'] == 'MTrk':
                track_chunks.append(chunk['data'])
            else:
                self.unknown_chunks.append(chunk)

        self.header = MidiHeader(self.header_chunk)
        self.tracks = [MidiTrack(c) for c in track_chunks]

class MidiHeader:
    def __init__(self, data):
        data_stream = io.BytesIO(data)
        self.format = struct.unpack('>H', data_stream.read(2))[0]
        self.num_chunks = struct.unpack('>H', data_stream.read(2))[0]
        self.division = struct.unpack('>H', data_stream.read(2))[0]

class MidiTrack:
    def __init__(self, data):
        data_stream = io.BytesIO(data)
        self.events = []
        self.end_time = 0

        abs_time = 0
        running_status = None
        while data_stream.tell() < len(data):
            # read delta time
            delta_time = _read_varint(data_stream)
            abs_time += delta_time

            # read event
            b = data_stream.read(1)[0]
            if b == 0xF0 or b == 0xF7:
                # sysex event
                length = _read_varint(data_stream)
                d = data_stream.read(length)
                event_data = [b] + list(d)
                running_status = None
            elif b == 0xFF:
                # meta event
                meta_type = data_stream.read(1)[0]
                length = _read_varint(data_stream)
                d = data_stream.read(length)
                event_data = [b, meta_type] + list(d)
                running_status = None

                if meta_type == 0x2F:
                    # end of track message
                    self.end_time = abs_time
            else:
                # midi message
                if (b & 0x80):
                    event_data = [b]
                    param_adjust = 0
                elif running_status is None:
                    raise Exception("Received midi message byte {:02X} without prev running status".format(b))
                else:
                    event_data = [running_status, b]
                    b = running_status
                    param_adjust = -1

                param_count = 0
                if b < 0xF0:
                    if (b & 0xF0) in MIDI_PARAM_COUNTS:
                        param_count = MIDI_PARAM_COUNTS[b & 0xF0]
                else:
                    if b in MIDI_PARAM_COUNTS:
                        param_count = MIDI_PARAM_COUNTS[b]

                param_count += param_adjust

                if param_count > 0:
                    params = data_stream.read(param_count)
                    event_data.extend(params)

                running_status = b

            self.events.append( (abs_time, event_data) )

class MidiChannelTracker:
    def __init__(self):
        self.volume = 100.0
        self.notes = []
        self.notes_on = {}
        self.prog = 0

    # note: this function only works if events are fed to it sequentially
    def add(self, time, event):
        event_type = event[0] & 0xF0
        if event_type == 0x90 and event[2] == 0:
            # note on with velocity 0 is a note off
            event_type = 0x80

        if event_type == 0x90:
            # note on
            note_number = event[1]
            velocity = event[2]
            velocity *= (self.volume / 100.0)
            velocity = int(max(0, min(127, velocity)))

            if note_number in self.notes_on:
                self.notes_on[note_number][3] = time - self.notes_on[note_number][2]
            note = [note_number, velocity, time, 0, self.prog] # last value will be duration
            self.notes.append(note)
            self.notes_on[note_number] = note

        elif event_type == 0x80:
            # note off
            note_number = event[1]
            if note_number in self.notes_on:
                self.notes_on[note_number][3] = time - self.notes_on[note_number][2]
                del self.notes_on[note_number]

        elif event_type == 0xB0 and event[1] == 0x07:
            self.volume = event[2]

        elif event_type == 0xC0:
            # program change message
            self.prog = event[1]

def _decode_midi_text(text_bytes):
    guess = chardet.detect(text_bytes)
    if guess and guess['encoding']:
        try:
            return text_bytes.decode(guess['encoding'])
        except UnicodeDecodeError:
            pass

    try:
        return text_bytes.decode('utf-8')
    except UnicodeDecodeError:
        pass

    try:
        return text_bytes.decode('shift-jis')
    except UnicodeDecodeError:
        pass

    parts = []
    while True:
        try:
            parts.append(text_bytes.decode('utf-8'))
            break
        except UnicodeDecodeError as e:
            m = re.search(r'in position (?P<pos>\d+)', str(e))
            if m:
                position = int(m['pos'])
                parts.append(text_bytes[:position].decode('utf-8'))
                parts.append(f'[{text_bytes[position]:02X}]')
                text_bytes = text_bytes[position+1:]

    return ''.join(parts)

def extract_midi_text(midi_data):
    lines = []
    midi = MidiFile(midi_data)
    for track_index,track in enumerate(midi.tracks):
        shown_track_index = False
        for event in track.events:
            event_data = event[1]
            if event_data[0] == 0xFF: #meta
                if event_data[1] in MIDI_TEXT_EVENTS:
                    if not shown_track_index:
                        lines.append(f"Track {track_index}:")
                        shown_track_index = True
                    text = _decode_midi_text(bytes(event_data[2:]))
                    lines.append(f"    {MIDI_TEXT_EVENTS[event_data[1]]} : {text}")
    return '\n'.join(lines)

def midi_note_name(note_number):
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return '{}{}'.format(NOTE_NAMES[note_number % 12], int(note_number / 12))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('midi_path')
    args = parser.parse_args()

    with open(args.midi_path, 'rb') as infile:
        midi_data = infile.read()

    midifile = MidiFile(midi_data)
    for i,track in enumerate(midifile.tracks):
        print(f"Track {i+1}:")
        for event in track.events:
            print(f"  {event[0]} : " + ' '.join([f'{b:02X}' for b in event[1]]))

    print(extract_midi_text(midi_data))
    