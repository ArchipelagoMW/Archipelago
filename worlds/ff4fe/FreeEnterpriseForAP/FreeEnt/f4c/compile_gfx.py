from . import compile_common
import re

def process_chr_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'gfx', 'chr_block_params')
    patch_address = params_tree.children[0]
    if len(params_tree.children) > 1:
        bitdepth = int(str(params_tree.children[1].children[0])[0])
    else:
        bitdepth = 4

    pixels = [int(c, 16) for c in re.sub(r'[^A-Fa-f0-9]', '', block['body'])]
    if len(pixels) != 64 and len(pixels) != 256:
        raise compile_common.CompileError("CHR block does not contain exactly 64 or 256 pixels: {}".format(block['body']))

    interleaved = []
    num_chrs = (len(pixels) >> 6)

    for chr_id in range(num_chrs):
        if num_chrs == 1:
            chr_pixels = pixels
        else:
            chr_pixels = []
            for y in range(8):
                index = (128 * (chr_id >> 1)) + (8 * (chr_id & 1)) + (16 * y)
                chr_pixels.extend(pixels[index:index+8])

        bitplanes = []
        for layer in range(bitdepth):
            bitplanes.append([0x00] * 8)
            bitmask = (1 << layer)
            for y in range(8):
                bitrow = 0x00
                for x in range(8):
                    if (chr_pixels[y * 8 + x] & bitmask):
                        bitrow |= (0x80 >> x)

                bitplanes[layer][y] = bitrow

        for i in range(0, bitdepth, 2):
            if i + 1 < bitdepth:
                for j in range(8):
                    interleaved.append(bitplanes[i][j])
                    interleaved.append(bitplanes[i + 1][j])
            else:
                interleaved.extend(bitplanes[i])

    rom.add_patch(patch_address, interleaved)

def process_pal_block(block, rom, env):
    params_tree = compile_common.parse(block['parameters'], 'gfx', 'pal_block_params')
    patch_address = params_tree.children[0]

    tree = compile_common.parse(block['parameters'], 'gfx', 'pal_block_body')
    data = []
    for rgb in tree.children:
        r, g, b = rgb.children
        if min([r, g, b]) < 0 or max([r, g, b]) >= 32:
            raise compile_common.CompileError("PAL block contains RGB values outside accepted range 0-31: {}".format(block['body']))
        color = (b << 10) | (g << 5) | r
        data.append(color & 0xff)
        data.append((color >> 8) & 0xff)

    rom.add_patch(patch_address, data)
