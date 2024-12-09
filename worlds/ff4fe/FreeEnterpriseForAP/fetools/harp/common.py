from . import general_converter

MAX_LINE_LENGTH = 26

HARP_TEST_SCRIPT = '''
    patch($008609 bus) { 00 }

    // skip title screen
    patch($00803d bus) { ea ea ea }

    event($10)
    {
        player invisible
        load map $7C at 1 1 facing up // BlackBG map
        music $12 // harp song
        message $11c
    }

    event($11)
    {
        message $11c
    }

    map($7C)
    {
        placement group $00
    }

    npc($01)
    {
        default active
        sprite $65 // transparent
        eventcall {
            $11
        }
    }

    placement($00 0) {
        position 0 1
        tangible
        npc $01
    }
    placement($00 1) {
        position 1 0
        tangible
        npc $01
    }
    placement($00 2) {
        position 2 1
        tangible
        npc $01
    }
    placement($00 3) {
        position 1 2
        tangible
        npc $01
    }

    // clear some text so it doesn't overflow
    text (map 0 message $00) {X}
    text (map 0 message $01) {X}
    text (map 0 message $02) {X}
    text (map 0 message $03) {X}
    text (map 0 message $04) {X}
    text (map 0 message $05) {X}
    text (map 0 message $06) {X}
    text (map 0 message $07) {X}
    text (map 0 message $08) {X}
    text (map 0 message $09) {X}
    text (map 0 message $0A) {X}
    text (map 0 message $0B) {X}
    text (map 0 message $0C) {X}
    text (map 0 message $0D) {X}
    text (map 0 message $0E) {X}
    text (map 0 message $0F) {X}
    text (map 0 message $10) {X}
    text (map 0 message $11) {X}
    '''

MIDIHARP_SCRIPT = '''
    // hook into music loading code and hijack Edward's song score loading
    msfpatch {
        MidiHarp__Start:
            cmp #$12  // Edward's theme
            beq $+MidiHarp__LoadScore

            // resume normal operation
            sta $4202   // displaced instruction
            lda #$03    // displaced instruction
            jml $048188

        MidiHarp__LoadScore:
            // hardcode midiharp score address
            lda #$00
            sta $10
            lda #$C0
            sta $11
            lda #$21
            sta $12
            // jump back to code, bypassing normal
            // score address lookup
            jml $0481f3

        .addr 0x048183
            jml $=MidiHarp__Start
    }


    // target score needs to go to $21c000
    '''

def tempo_event_to_bpm(tempo_event):
    microseconds_per_quarter = (tempo_event[2] << 16) | (tempo_event[3] << 8) | tempo_event[4]
    return 60000000.0 / microseconds_per_quarter

def generate_metadata_script(asset):
    text_lines = []

    if not asset.source.strip():
        PAGE1_LAYOUTS = [
            ['Now Playing', '{title}'],
            ['Now Playing {title}']
        ]
    else:
        PAGE1_LAYOUTS = [
            ['Now Playing', '{title}', 'from', '{fr}'],
            ['Now Playing', '{title}', 'from {fr}'],
            ['{title}', 'from', '{fr}'],
            ['{title}', 'from {fr}'],
        ]

    for layout in PAGE1_LAYOUTS:
        lines = []
        for s in layout:
            lines.extend(_word_wrap(s.format(
                title = asset.title.upper(),
                fr = asset.source)
                ))

        if len(lines) <= 4 or layout == PAGE1_LAYOUTS[-1]:
            if len(lines) > 4:
                print("WARNING: page 1 metadata overflow")
            text_lines.extend(lines)
            text_lines.extend([''] * (4 - len(lines)))
            break

    if not asset.sequencer.strip():
        PAGE2_LAYOUTS = [
            ['Composed by', '{composer}'],
        ]
    else:
        PAGE2_LAYOUTS = [
            ['Composed by', '{composer}', 'MIDI sequenced by', '{sequencer}'],
            ['Composed by', '{composer}', 'Sequenced by {sequencer}'],
            ['Composed by {composer}', 'Sequenced by {sequencer}'],
        ]

    for layout in PAGE2_LAYOUTS:
        lines = []
        for s in layout:
            lines.extend(_word_wrap(s.format(
                composer = asset.composer,
                sequencer = asset.sequencer)
                ))

        if len(lines) <= 4 or layout == PAGE2_LAYOUTS[-1]:
            if len(lines) > 4:
                print("WARNING: page 2 metadata overflow")
            text_lines.extend(lines)
            #text_lines.extend([''] * (4 - len(lines)))
            break

    for i,line in enumerate(text_lines):
        line = (' ' * ((MAX_LINE_LENGTH - len(line)) // 2)) + line
        line = line.replace('&', '[name $f4]')
        #try:
        #    f4c.encode_text(line)
        #except Exception as e:
        #    print(f'WARNING: line {line} cannot be encoded: {e}')
        text_lines[i] = line

    text_lines[0] = '[music $12]' + text_lines[0]

    return (
        'text(map $94 message 1) // #CaveMagnesCrystalRoom\n{\n' + '\n'.join(text_lines) + '\n}' 
        + '\n\n'
        + 'text(bank 1 message $11C) {\n' + '\n'.join(text_lines) + '\n}' 
        )

def _word_wrap(text):
    parts = text.split()
    lines = []
    for part in parts:
        if len(part) > MAX_LINE_LENGTH:
            while len(part) > MAX_LINE_LENGTH:
                lines.append(part[:MAX_LINE_LENGTH])
                part = part[MAX_LINE_LENGTH:]
            lines.append(part)
        elif lines and len(lines[-1]) + len(part) + 1 <= MAX_LINE_LENGTH:
            lines[-1] += ' ' + part
        else:
            lines.append(part)
    return lines

def generate_script(asset):
    song_data = general_converter.generate_song_data(asset, permissive=(asset.converter == 'permissive'))
    
    script_lines = []
    if len(song_data) > 0x0F00:
        script_lines.append(f'// WARNING: {asset.id} length truncated')

    script_lines.append('patch($21c000 bus) {')
    script_lines.append(' '.join([f'{b:02X}' for b in song_data]))
    script_lines.append('}')

    song_script = '\n'.join(script_lines)
    return song_script + '\n\n' + generate_metadata_script(asset)

def generate_test_rom_script(asset):
    song_script = generate_script(asset)
    return f"{song_script}\n\n{HARP_TEST_SCRIPT}\n\n{MIDIHARP_SCRIPT}"

