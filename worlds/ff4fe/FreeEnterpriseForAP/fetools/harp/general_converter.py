import math

from .midi import MidiFile, MidiChannelTracker
from . import common

SNES_NOTE_DURATIONS = [
      0xc0, 0x90, 0x60, 0x48, 0x40, 0x30, 0x24, 0x20, 0x18, 0x10,
      0x0c, 0x08, 0x06, 0x04, 0x03,
    ]

SNES_TEMPO_BPM_MULTIPLIER = 170.0 / 160.0

class HarpChannelTracker:
    def __init__(self):
        self.script = []
        self._pending_note = None
        self._pending_note_time = 0
        self._current_octave = None
        self.loop_offset = 0

    def add_note(self, time, note_number, velocity):
        if self._pending_note is not None and (time - self._pending_note_time) < SNES_NOTE_DURATIONS[-1]:
            # ignore note if it comes too fast on heels of prev note
            return

        self.finalize_pending(time)

        self._pending_note = [note_number, velocity]
        self._pending_note_time = time

    def set_loop_point(self, time):
        self.finalize_pending(time)
        self._pending_note_time = time
        self.loop_offset = len(self.script)

    def add_tempo(self, time, tempo):
        self.finalize_pending(time)
        self._pending_note_time = time
        self.script.extend([0xD2, 0x00, 0x00, tempo])

    def finalize_pending(self, time):
        duration = time - self._pending_note_time
        if duration > 0:
            sub_durations = _decompose_duration(duration)
            #print('{:X} <- {}'.format(duration, ' '.join(['{:2X}'.format(SNES_NOTE_DURATIONS[i]) for i in sub_durations])))
        else:
            sub_durations = []

        if sub_durations is False:
            raise Exception('Could not decompose duration 0x{:X}'.format(duration))

        if self._pending_note is None:
            self.script.extend([(0xB4 + i) for i in sub_durations])
        else:
            note_name = self._pending_note[0] % 12
            note_octave = int(self._pending_note[0] / 12)
            if self._current_octave is None or abs(self._current_octave - note_octave) >= 2:
                self.script.extend([0xDA, note_octave])
                self._current_octave = note_octave
            else:
                while self._current_octave < note_octave:
                    self.script.append(0xE1)
                    self._current_octave += 1
                while self._current_octave > note_octave:
                    self.script.append(0xE2)
                    self._current_octave -= 1
            
            #self.script.extend([0xF2, 0x00, 0x00, self._pending_note[1]])

            if sub_durations:
                self.script.append(note_name * len(SNES_NOTE_DURATIONS) + sub_durations[0])
                self.script.extend([(0xC3 + i) for i in sub_durations[1:]])

            self._pending_note = None


def _decompose_duration(duration, start_index=0):
    for i in range(start_index, len(SNES_NOTE_DURATIONS)):
        d = SNES_NOTE_DURATIONS[i]
        if d == duration:
            return [i]
        elif d < duration:
            sub_durations = _decompose_duration(duration - d, start_index=i)
            if sub_durations is not False:
                return [i] + sub_durations
    return False

def _midi_to_harp(asset, permissive=False, **param_overrides): #polyphony=5, octave_range=5, strumming=True, transpose=None, fixed_tempo=None, auto_truncate=True):
    transpose = param_overrides.get('transpose', asset.transpose)
    fixed_tempo = param_overrides.get('fixed_tempo', asset.fixed_tempo)
    if permissive:
        polyphony = 6
        octave_range = None
        strumming = False
        auto_truncate = True
    else:
        polyphony = param_overrides.get('polyphony', 5)
        octave_range = param_overrides.get('octave_range', asset.octave_range)
        strumming = param_overrides.get('strumming', True)
        auto_truncate = param_overrides.get('auto_truncate', True)

    if fixed_tempo <= 0:
        fixed_tempo = None

    midi_file = MidiFile(asset.midi)
    header = midi_file.header

    if header.format == 2 and len(tracks) > 1:
        raise Exception("MIDI file is format 2 with multiple tracks, this is not supported")

    if header.division & 0x8000:
        raise Exception("MIDI file uses SMTPE frame timing, this is unsupported")

    ticks_per_quarter = header.division

    tracks = midi_file.tracks

    mega_track = []
    for track in tracks:
        mega_track.extend(track.events)
    mega_track.sort()

    if fixed_tempo is not None:
        tempo_track = [(0, float(fixed_tempo))]
    else:
        tempo_track = [(e[0], common.tempo_event_to_bpm(e[1])) for e in mega_track if e[1][0] == 0xFF and e[1][1] == 0x51]
        if len(tempo_track) == 0:
            tempo_track.insert(0, (0, 120.0))

    max_tempo = max(tempo_track, key=lambda p: p[1])[1]
    snes_ticks_per_quarter = 0x30
    while max_tempo > 0xFF * SNES_TEMPO_BPM_MULTIPLIER:
        max_tempo /= 2
        snes_ticks_per_quarter /= 2

    snes_ticks_per_quarter = int(round(snes_ticks_per_quarter))

    channels = []
    for i in range(16):
        channels.append(MidiChannelTracker())

    loop_time = None
    loop_time_check_channel = None
    for time,event in mega_track:
        if event[0] < 0xF0:
            # channel message
            ch = event[0] & 0x0F
            channels[ch].add(time, event)

            if permissive:
                if ch == loop_time_check_channel and event[0] & 0xF0 == 0x90 and event[2] > 0:
                    # first note on event after CC 16 event sets loop time
                    loop_time = time
                    loop_time_check_channel = None
                elif event[0] & 0xF0 == 0b10110000 and event[1] == 0x10 and event[2] > 0:
                    loop_time_check_channel = ch

    if loop_time is not None:
        tempo_track.append( (loop_time, 'LOOP') )
        tempo_track.sort()

    # get all notes except drum channel notes
    all_notes = []
    for i,channel in enumerate(channels):
        if i != 9:
            all_notes.extend(channel.notes)

    if permissive:
        # alternate sort: at any given time, lowest note first, then top notes descending
        grouped_notes = {}
        for note in sorted(all_notes, key=lambda n: n[2]):
            grouped_notes.setdefault(note[2], []).append(note)
        all_notes = []
        for group_time in grouped_notes:
            group = grouped_notes[group_time]
            group.sort(key=lambda n: n[0], reverse=True)
            group = [group[-1]] + group[:-1]
            all_notes.extend(group)
    else:
        all_notes.sort(key = lambda n: (n[2], 128-n[0])) # sort by start time, then highest pitch

    '''
    Scratch pad for tempo math.

    In the SNES, there are 0x30 ticks to a quarter note.
    Our range of usable tempos goes up to 272 bpm.
    If we need a faster tempo, then we have to scale the times:
        - half as many SNES ticks per quarter note
        - repeat as necessary until desired tempo is in range

    In the MIDI file, we know the number of ticks per quarter
    note, as well as the number of microseconds per quarter
    (from which we can derive BPM).    
    '''

    harp_channels = []
    setup_scripts = []
    for i in range(polyphony):
        harp_channels.append(HarpChannelTracker())
        setup_scripts.append([])

    #snes_tempo = round(tempo_track[0][1] / SNES_TEMPO_BPM_MULTIPLIER)
    #setup_scripts[0].extend([0xD2, 0x00, 0x00, snes_tempo])

    for setup_script in setup_scripts:
        setup_script.extend([
            0xD4, 0x46,             # echo
            0xD5, 0x46, 0x00,       # reverb
            0xF2, 0x00, 0x00, 0xFF, # volume
            0xF3, 0x00, 0x00, 0x80, # pan
            0xDB, 0x40,             # instrument
            0xDC, 0x0B,             # envelope
            0xDD, 0x00,             # release
            0xDE, 0x5F,             # legato
            0xEA,                   # effects on
            ])

    # estimate transpose based on range
    if transpose is None:
        octave_counts = {}
        for note in all_notes:
            octave = int(note[0] / 12)
            octave_counts.setdefault(octave, 0)
            octave_counts[octave] += 1
        total_count = len(all_notes)
        avg_octave = sum([o * octave_counts[o] / total_count for o in octave_counts])
        transpose = -12 * int(avg_octave - 4)

    next_ch = 0
    last_note_time = None
    notes_used = set()
    strum_time = 0
    first_note_time = None
    end_time = None
    additional_length = (2 * polyphony) + sum([len(s) for s in setup_scripts]) + (3 * polyphony)

    for note in all_notes:
        note_number, velocity, start_time, duration, prog = note
        if note_number == 0:
            continue

        # discard notes from non-pitched instruments
        if prog >= 0xF0:
            continue

        if velocity < 32 and not permissive:
            # discard quiet notes?
            continue

        if first_note_time is None:
            first_note_time = start_time
            start_time = 0
        else:
            start_time -= first_note_time

        note_number += transpose
        if not permissive:
            # compress notes into "harp range" :>
            top_octave = 5 + math.ceil(octave_range / 2.0)
            bottom_octave = top_octave - octave_range
            while note_number < (12 * bottom_octave - 6):
                note_number += 12
            #while note_number > (12 * top_octave):
            #    note_number -= 12

        # convert start time to SNES time
        #   t / ticks_per_quarter * SNES_ticks_per_quarter
        snes_start_time = int(round(start_time * snes_ticks_per_quarter / ticks_per_quarter))

        # quantize to 32nd note resolution
        snes_start_time = int(round(snes_start_time / 6) * 6)

        #print('{} {}'.format(_midi_note_name(note_number), note[1:]))

        if last_note_time is None or snes_start_time > last_note_time:
            last_note_time = snes_start_time
            notes_used = set()
            strum_time = 0
        elif note_number in notes_used or len(notes_used) >= len(harp_channels):
            continue

        if notes_used and strumming:
            strum_time ^= 3

        notes_used.add(note_number)

        while tempo_track and (tempo_track[0][0] - first_note_time) <= start_time:
            tempo_event = tempo_track.pop(0)
            tempo_time = max(0, tempo_event[0] - first_note_time)

            snes_tempo_time = int(round(tempo_time * snes_ticks_per_quarter / ticks_per_quarter))
            # quantize to 32nd note resolution
            snes_tempo_time = int(round(snes_tempo_time / 6) * 6)
            if tempo_event[1] == 'LOOP':
                for harp_channel in harp_channels:
                    harp_channel.set_loop_point(snes_tempo_time)
            else:
                snes_tempo = int(round(tempo_event[1] / SNES_TEMPO_BPM_MULTIPLIER))
                harp_channels[0].add_tempo(snes_tempo_time, snes_tempo)

        harp_channels[next_ch].add_note(snes_start_time + strum_time, note_number, velocity)
        next_ch = (next_ch + 1) % len(harp_channels)

        if auto_truncate:
            running_total_length = sum([len(ch.script) for ch in harp_channels]) + additional_length
            if running_total_length > 0x0FC0:
                # too long, abort
                end_time = start_time + duration
                break

    if end_time is None:
        end_time = max([track.end_time for track in tracks]) - first_note_time

    snes_end_time = int(round(end_time * snes_ticks_per_quarter / ticks_per_quarter))
    snes_end_time = int(round(snes_end_time / 6) * 6)

    for harp_channel in harp_channels:
        harp_channel.finalize_pending(snes_end_time)

    full_script = [0x00] * 0x10
    for i,harp_channel in enumerate(harp_channels):
        channel_pointer = 0x2000 + len(full_script)
        full_script[i << 1] = (channel_pointer & 0xff)
        full_script[(i << 1) + 1] = (channel_pointer >> 8) & 0xff
        full_script.extend(setup_scripts[i])
        loop_pointer = 0x2000 + len(full_script) + harp_channel.loop_offset
        full_script.extend(harp_channel.script)
        full_script.extend([0xF4, (loop_pointer & 0xff), ((loop_pointer >> 8) & 0xff)])

    full_script_length = len(full_script)
    return [full_script_length & 0xff, (full_script_length >> 8) & 0xff] + full_script


def generate_song_data(asset, permissive=False):
    if permissive:
        data = _midi_to_harp(asset, permissive=True)
    else:
        data = _midi_to_harp(asset)
        if len(data) > 0x0F00:
            # try again without strumming
            data = _midi_to_harp(asset, strumming = False, polyphony = 4)

    return data
