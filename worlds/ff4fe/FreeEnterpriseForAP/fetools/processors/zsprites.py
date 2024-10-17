import math
import itertools
import os
import io
import re
from PIL import Image

class ConvertError(Exception):
    pass

def generate_sprite_script(image_bytes, name, vintage=False):
    im = Image.open(io.BytesIO(image_bytes))
    im = im.quantize(colors=16)
    #im.save('testquant-{}.png'.format(os.path.splitext(os.path.basename(filename))[0]))
    lookup_im = im.convert(mode="RGB")
    transparent_color = im.getpixel( (im.size[0] - 1, 0) )

    tile_size = ( int(math.ceil(im.size[0] / 8.0)), int(math.ceil(im.size[1] / 8.0)) )
    offset = ( 
        max(0, int((0x13 - tile_size[0]) / 2)), 
        max(0, int((0x12 - tile_size[1]) / 2)) 
        )
    palette = [None] * 16
    chr_data = []
    chr_data_pages = [chr_data]
    tilemap_data = []
    chr_count = 0
    page_turn = None

    left_edge_transparent = 0
    left_edge_opaque = 0

    for ty in range(tile_size[1]):
        tilemap_data.append([])
        for tx in range(tile_size[0]):
            bitplanes = [[0x00] * 8, [0x00] * 8, [0x00] * 8, [0x00] * 8]
            for y in range(8):
                for x in range(8):
                    px = tx * 8 + x
                    py = ty * 8 + y
                    if px >= im.size[0] or py >= im.size[1]:
                        c = transparent_color
                    else:
                        c = im.getpixel( (px, py) )

                    if transparent_color != 0:
                        if c == transparent_color:
                            c = 0
                        elif c == 0:
                            c = transparent_color

                    if px == 0:
                        if c == 0:
                            left_edge_transparent += 1
                        else:
                            left_edge_opaque += 1

                    if palette[c] is None:
                        palette[c] = lookup_im.getpixel( (px, py) )

                    for b,bitplane in enumerate(bitplanes):
                        if c & (1 << b):
                            bitplane[y] |= (0x80 >> x)

            interleaved_bitplanes = []
            for i in range(8):
                interleaved_bitplanes.append(bitplanes[0][i])
                interleaved_bitplanes.append(bitplanes[1][i])
            for i in range(8):
                interleaved_bitplanes.append(bitplanes[2][i])
                interleaved_bitplanes.append(bitplanes[3][i])

            if sum(interleaved_bitplanes) == 0:
                tilemap_data[-1].append(0xFF)
            elif interleaved_bitplanes in chr_data:
                tilemap_data[-1].append(chr_data.index(interleaved_bitplanes))
            else:
                if chr_count == 0xFE:
                    # pad out current page
                    chr_data.append([0] * 32)
                    chr_data.append([0] * 32)
                    # start new page
                    chr_data = []
                    chr_data_pages.append(chr_data)
                    # remember where we turned the page
                    page_turn = (tx, ty)

                tilemap_data[-1].append(len(chr_data))
                chr_data.append(interleaved_bitplanes)
                chr_count += 1

    flat_chr_data_pages = list(itertools.chain(*chr_data_pages))
    flat_chr_data = list(itertools.chain(*flat_chr_data_pages))

    MAX_TILE_COUNT = 0x17E
    if chr_count > (MAX_TILE_COUNT):
        raise ConvertError("Too many distinct tiles ({}) required for graphic (maximum {})".format(chr_count, MAX_TILE_COUNT))

    packed_tilemap_data = []
    for row in tilemap_data:
        while row:
            t = row.pop(0)
            if t == 0xFF:
                blank_count = 1
                while row and row[0] == 0xFF:
                    row.pop(0)
                    blank_count += 1
                if blank_count > 1:
                    packed_tilemap_data.append(0xFE)
                    packed_tilemap_data.append(blank_count)
                else:
                    packed_tilemap_data.append(0xFF)
            else:
                packed_tilemap_data.append(t)

    max_length = 0x76000 - 0x75e56
    if len(packed_tilemap_data) > max_length:
        raise ConvertError(f"Tilemap too large ({len(packed_tilemap_data)}) to fit in available space ({max_length})")

    if vintage:
        palette = list(map(lambda c : (0,0,0) if c is None else c, palette))
        palette = crush(palette, transparent=True, keep_colors=[(0,0,0)], keep_count=4, use_kept_colors=False)

    snes_palette = []
    for c in palette:
        if c is None:
            snes_palette.append(0x00)
            snes_palette.append(0x00)
        else:
            def color_scale(val):
                sin_val = math.sin(val * math.pi / 512) * 32
                lin_val = val / 8.0
                return int((sin_val + lin_val) * 0.5)

            snes_color = color_scale(c[0]) | (color_scale(c[1]) << 5) | (color_scale(c[2]) << 10)
            snes_palette.append(snes_color & 0xFF)
            snes_palette.append((snes_color >> 8) & 0xFF)

    script_lines = []

    # name
    enemy_name = name
    script_lines.append('text(monster name $C9) {{{}}}\n'.format(enemy_name[:8]))
    if len(enemy_name) > 8:
        script_lines.append('text(monster name $CA) {{{}}}\n'.format(enemy_name[8:10]))
        script_lines.append(EXTENDED_NAME_SCRIPT)

    # tile size
    script_lines.append('patch($6ffb0) {{ {:02X} {:02X} }}'.format(*tile_size))

    # position offset
    offset_byte = ((offset[0] & 0xF) << 4) | (offset[1] & 0xF)
    script_lines.append('patch($7cf1d) {{ {:02X} }}'.format(offset_byte))

    # palette
    script_lines.append('patch($e7a90) {')
    script_lines.append(' '.join(['{:02X}'.format(b) for b in snes_palette]))
    script_lines.append('}')

    # CHR data
    if page_turn:
        script_lines.append('patch($228000 bus) {')
    else:
        script_lines.append('patch($616f8) {')
    script_lines.append(' '.join(['{:02X}'.format(b) for b in flat_chr_data]))
    script_lines.append('}')

    # packed tilemap
    script_lines.append('patch($75e56) {')
    script_lines.append(' '.join(['{:02X}'.format(b) for b in packed_tilemap_data]))
    script_lines.append('}')

    # offset if necessary
    if left_edge_opaque >= left_edge_transparent:
        script_lines.append(SHIFT_LEFT_SCRIPT)

    # page turn stuff if necessary
    if page_turn:
        extended_chr_script = EXTENDED_CHR_SCRIPT.replace(
            '[[ROW]]', '{:04X}'.format(page_turn[0] * 2)
            ).replace(
            '[[COL]]', '{:02X}'.format(tile_size[1] - page_turn[1])
            )
        script_lines.append(extended_chr_script)

    return '\n'.join(script_lines)

def generate_test_rom_script(*args, **kwargs):
    sprite_script = generate_sprite_script(*args, **kwargs)
    return sprite_script + '\n' + (VINTAGE_TESTROM_SCRIPT if kwargs.get('vintage', False) else TESTROM_SCRIPT)


#-----------------------------------------------------------------------------------

SHIFT_LEFT_SCRIPT = '''
msfpatch {
    ZeromusPicLeftEdge:
        lda $efa4
        cmp #$29  // magic number only used by Zeromus
        beq $+ZeromusPicLeftEdge_Do

        // original behavior
        lda $efa3
        and #$f0
        lsr a
        lsr a
        lsr a
        lsr a
        inc a
        inc a
        jml $028c45

    ZeromusPicLeftEdge_Do:
        // similar but without shift to right
        lda $efa3
        and #$f0
        lsr a
        lsr a
        lsr a
        lsr a
        jml $028c45


    .addr $028c3a
        jml $=ZeromusPicLeftEdge
}
'''

EXTENDED_CHR_SCRIPT = '''
msfpatch {
    .addr $02903d
        jml $=ZeromusCHRExpansion_Load
}

msfpatch {
    ZeromusCHRExpansion_Load:
        // copy 384 tiles instead of just 255 :>
        ldx #$3000
        stx $00

        // replace source address
        ldx #$8000

        // A on stack contains bank source of transfer, replace that
        pla
        lda #$22

        // return to original code
        jml $029044
}

msfpatch {
    .addr $028c9c
        jml $=ZeromusCHRExpansion_TileDraw
}

msfpatch {
    ZeromusCHRExpansion_TileDraw:
        lda $efa4
        cmp #$29
        beq $+ZeromusCHRExpansion_TileDraw_Do
        // not Zeromus = perform displaced instructions and return
        lda $00
        sta $02
        jml $028ca0

    ZeromusCHRExpansion_TileDraw_Do:
        // recreate the loop from $028c9c with additional checks for our "rollover" value
        lda $00
        sta $02
        ldy #$0000

    ZeromusCHRExpansion_TileDraw_LoopStart:
        cpy #$[[ROW]]  // to be replaced by tile X * 2
        bne $+ZeromusCHRExpansion_TileDraw_BypassPageTurn
        lda $01
        cmp #$[[COL]]
        bne $+ZeromusCHRExpansion_TileDraw_BypassPageTurn

        // do page turn
        inc $07
        
    ZeromusCHRExpansion_TileDraw_BypassPageTurn:
        // literally just a copy of $028ca3
        jsr $_ZeromusCHRExpansion_TileDraw_Draw
        sta ($04),y
        iny
        lda $07
        and $0c
        ora $08
        ora $2a
        sta ($04),y
        iny
        dec $02
        bne $-ZeromusCHRExpansion_TileDraw_LoopStart

        // return to original code after replaced loop
        jml $028cb8


    ZeromusCHRExpansion_TileDraw_Draw:
        // literally just a copy of $028ce1
        stz $2a
        lda $09
        beq $0f
        dec $09
        lda #$fe
        sta $0c
        lda #$02
        ora $f49d
        sta $08
        tdc
        rts
        phy
        phx
        ply
        lda [$26],y
        cmp #$ff
        beq $0b
        cmp #$fe
        bne $15
        iny
        lda [$26],y
        dec a
        sta $09
        inx
        lda #$fe
        sta $0c
        lda #$02
        ora $f49d
        sta $08
        tdc
        bra $10
        pha
        lda #$ff
        sta $0c
        lda $f49d
        sta $08
        pla
        clc
        adc $06
        rol $2a
        inx
        ply
        rts
}
'''

EXTENDED_NAME_SCRIPT = '''
msfpatch {
    // hack code that draws enemy quantity to instead draw
    // extra chars for Z
    .addr $02a78e
        jml $=Zeromus__NameExtension

    .new
    Zeromus__NameExtension:
        // A = monster type at this point

        // replicate original check
        cmp #$ff
        beq $+NoEnemy

        // check for Z
        cmp #$c9
        beq $+IsZeromus

        // otherwise return
        jml $02a792

    %NoEnemy:
        jml $02a7a4

    %IsZeromus:
        // write last two characters of name instead of other behavior        
        lda $0e9e50
        dey
        dey
        sta ($34),y
        iny
        lda $36
        sta ($34),y
        iny
        lda $0e9e51
        jml $02a49f
}
'''


#-------------------------------------------------------------------
# copy/pasted code from palette_crusher.py; refactor later if possible

def dist(col1, col2):
    return math.sqrt(sum([(col1[i] - col2[i]) ** 2 for i in range(len(col1))]))

def generate_subsets(item_list, count):
    mask = ([True] * count) + ([False] * (len(item_list) - count))

    while True:
        subset = [item_list[i] for i in range(len(item_list)) if mask[i]]
        yield subset

        # next permutation algorithm:
        #   find leftmost True value that is before a False value
        #   swap them
        #   push all Trues left of that True value back to the leftmost positions
        seen_true_count = 0
        advanced = False
        for i in range(len(mask) - 1):
            if mask[i] and not mask[i + 1]:
                mask[i] = False
                mask[i + 1] = True
                mask[:i] = ([True] * seen_true_count) + ([False] * (i - seen_true_count))
                advanced = True
                break
            elif mask[i]:
                seen_true_count += 1

        if not advanced:
            break


def crush(palette, transparent=False, keep_indices=[], keep_colors=[], use_kept_colors=False, keep_count=3):
    candidates = []

    select_count = keep_count

    # copy input lists so we don't change the sources
    keep_indices = list(keep_indices)
    keep_colors = list(keep_colors)

    if transparent:
        transparent_color = palette[0]
        palette = palette[1:]
        keep_indices = [i - 1 for i in keep_indices]

    for color in keep_colors:
        if type(color) is int:
            color = decode_snes_palette([color & 0xFF, (color >> 8) & 0xFF])[0]

        if color in palette:
            idx = palette.index(color)
            if idx not in keep_indices:
                keep_indices.append(idx)
                select_count -= 1

    forced_set = [c for i,c in enumerate(palette) if i in keep_indices]
    unforced_set = [c for i,c in enumerate(palette) if i not in keep_indices]

    for subset in generate_subsets(unforced_set, select_count):
        if use_kept_colors:
            mini_palette = forced_set + subset
        else:
            mini_palette = subset

        candidate = {
            'mini_palette' : mini_palette,
            'score' : 0,
            'crushed_palette' : []
            }
        if transparent:
            candidate['crushed_palette'].append(transparent_color)

        for color in palette:
            if color in forced_set:
                candidate['crushed_palette'].append(color)
            else:
                distances = []
                for root_color in mini_palette:
                    distances.append({'distance' : dist(color, root_color), 'color' : root_color})
                best_distance = min(distances, key = lambda d : d['distance'])
                candidate['score'] += best_distance['distance']
                candidate['crushed_palette'].append(best_distance['color'])
        candidates.append(candidate)

    best_candidate = min(candidates, key = lambda c : c['score'])
    return best_candidate['crushed_palette']


#-------------------------------------------------------------------
TESTROM_SCRIPT = '''
    event($10) {
        load map #LunarCoreZemusRoom at 15 22 facing up
        //give actor #Kain1
        //give actor #CRydia
        //give actor #Tellah1
        //give actor #Edward
        fight $B7
    }

    ai_script(moon $47)
    {
        use #Transform3
    }

    ai_script(moon $4B)
    {
        use #InvincibleOff
        
        use #ZeromusShake2

        use #Enemy_BigBang

        target self
        use #Nuke

        target self
        use #Enemy_Vanish
    }

    patch($00803d bus) { ea ea ea }

    patch($0fa907 bus) { 0f 27 0f 27 }
    //patch($0fa927 bus) { 0f 27 0f 27 }
    //patch($0fa947 bus) { 0f 27 0f 27 }
    //patch($0fa967 bus) { 0f 27 0f 27 }
    //patch($0fa987 bus) { 0f 27 0f 27 }
    '''

VINTAGE_TESTROM_SCRIPT = TESTROM_SCRIPT + '''
// load special CHR data we need
msfpatch {
    VintageBattlefield__LoadCHR:
        phb
        pha 
        plb 
        sty $2116
        stx $02
        ldy #$0000
    VintageBattlefield__LoadCHR_LoopStart:
        rep #$20
        .mx 0x00
        pha 
        ldx #$0010
    VintageBattlefield__LoadCHR_InnerLoopStart:
        lda ($02),y
        sta $2118
        iny 
        iny 
        dex 
        bne $-VintageBattlefield__LoadCHR_InnerLoopStart
        pla 
        sep #$20
        .mx 0x20

        dec $00
        bne $-VintageBattlefield__LoadCHR_LoopStart
        plb 
        rts 
}

msfpatch {
    VintageBattlefield__LoadBorderCHR:
        ldx #$0006
        stx $00
        ldx #$_VintageBattlefield__CHRData
        lda #$20
        ldy #$4530
        jsr $_VintageBattlefield__LoadCHR

        // perform displaced instructions and return
        ldx #$0002
        stx $00
        jml $028b59

    .addr $028b54
        jml $=VintageBattlefield__LoadBorderCHR
}

msfpatch {
    VintageBattlefield__CHRData:
        [[
        00 00 00 00 00 00 3f 00 60 1f 4f 30 58 20 50 20
        00 00 00 00 00 00 00 3f 00 7f 00 7f 00 78 00 70
        00 00 00 00 00 00 ff 00 00 ff ff 00 00 00 00 00
        00 00 00 00 00 00 00 ff 00 ff 00 ff 00 00 00 00
        00 00 00 00 00 00 fe 00 03 fc f9 06 0d 02 05 02
        00 00 00 00 00 00 00 fe 00 ff 00 ff 00 0f 00 07
        50 20 50 20 50 20 50 20 50 20 50 20 50 20 50 20
        00 70 00 70 00 70 00 70 00 70 00 70 00 70 00 70
        05 02 05 02 05 02 05 02 05 02 05 02 05 02 05 02
        00 07 00 07 00 07 00 07 00 07 00 07 00 07 00 07
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        ]]
}

// patch battle BG background loader to render FF1
// battle frames
msfpatch {
    .addr $01e95c
        jml $=VintageBattlefield__BorderTiles_TopHalf

    .new
    VintageBattlefield__BorderTiles_TopHalf:
        // if Zeromus, keep top 4 rows
        cpy #$0100
        bcc $+Normal
        jmp $_Blank

    %Normal:
        // use normal graphic
        lda $16ed80,x
        jml $01e960

    %Blank:
        lda #$58
        jmp $_Draw

    %Draw:
        sta $6cfd,y
        iny
        lda #$06 // palette 1, tile page 2
        sta $6cfd,y
        iny
        jml $01e982
}

msfpatch {
    .addr $01e925
        jml $=VintageBattlefield__BorderTiles_BottomHalf

    .new
    VintageBattlefield__BorderTiles_BottomHalf:

    %Blank:
        lda #$58
        jmp $_Draw

    %Draw:
        sta $6efd,x
        inx
        lda #$06  // palette 1, tile page 2
        sta $6efd,x
        inx
        jml $01e94c     
}
'''
