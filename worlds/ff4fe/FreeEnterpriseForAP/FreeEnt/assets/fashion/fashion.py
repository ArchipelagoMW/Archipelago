from PIL import Image, ImageDraw
import argparse
import sys
import glob
import os
import io
import math

JOBS = [
    'DKCecil', 'Kain', 'CRydia', 'Tellah', 'Edward', 'Rosa', 'Yang', 'Palom', 'Porom', 'PCecil', 'Cid', 'ARydia', 'Edge', 'Fusoya'
    ]

TILES_PER_SET = 64

COMBINATIONS = {
    'stand' : [[0x00,0x01], [0x02,0x03], [0x04,0x05]],
    'walk' : [[0x00,0x01], [0x02,0x03], [0x0C,0x0D]],  
    'ready' : [[0x06,0x07], [0x08,0x09], [0x0A,0x0B]],  
    'rh swing up' : [[0x00,0x01], [0x14,0x03], [0x15,0x0D]],  
    'lh swing up' : [[0x00,0x1A], [0x02,0x1B], [0x1C,0x1D]],  
    'lh swing down' : [[0x00,0x01], [0x16,0x17], [0x18,0x19]],  
    'casting 1' : [[0x39,0x3A], [0x3B,0x3C], [0x3D,0x3E]],  
    'casting 2' : [[0x39,0x3A], [0x3F,0x3C], [0x3D,0x3E]],  
    'special' : [[0x30,0x31,0x32], [0x33,0x34,0x35], [0x36,0x37,0x38]],  
    'cheer' : [[0x24,0x25], [0x26,0x27], [0x28,0x29]],  
    'hit' : [[0x1E,0x1F], [0x20,0x21], [0x22,0x23]],  
    'weak' : [[0x0E,0x0F], [0x10,0x11], [0x12,0x13]],  
    'dead' : [[0x2A,0x2B,0x2C], [0x2D,0x2E,0x2F]],     
    }

TEMPLATE = {
    'filename' : 'battle_sprite_template.png',
    'combinations': {
        'stand' : (8, 18),
        'walk' : (28, 18),
        'ready' : (48, 18),
        'rh swing up' : (68, 18),
        'lh swing up' : (88, 18),
        'lh swing down' : (108, 18),
        'casting 1' : (128, 18),
        'casting 2' : (148, 18),

        'special' : (20, 46),
        'cheer' : (48, 46),
        'hit' : (68, 46),
        'weak' : (88, 46),
        'dead' : (108, 54),
        },
    'palette' : (8, 76),
    'palette_stride' : 4,
    }

def get_template_coordinate(tileset_index, pos):
    for combination in COMBINATIONS:
        for row_index,row in enumerate(COMBINATIONS[combination]):
            if tileset_index in row:
                col_index = row.index(tileset_index)

                template_pos = TEMPLATE['combinations'][combination]
                return (
                    template_pos[0] + col_index * 8 + pos[0],
                    template_pos[1] + row_index * 8 + pos[1]
                    )
    return None

characters = []

class Character:
    def __init__(self):
        self.palette = [(0,0,0)] * 16
        self.tiles = [None] * TILES_PER_SET

    def decode_palette(self, palette_bytes):
        for i in range(16):
            col = palette_bytes[i * 2] | (palette_bytes[i * 2 + 1] << 8)
            r = col & 0x1F
            g = (col >> 5) & 0x1F
            b = (col >> 10) & 0x1F
            self.palette[i] = tuple([int(v * 255.0 / 0x1F) for v in [r, g, b]])

    def decode_tileset(self, tileset_bytes):
        for i in range(TILES_PER_SET):
            tile_bytes = tileset_bytes[i * 0x20 : (i + 1) * 0x20]
            tile = Image.new('RGB', (8, 8), self.palette[0])
            for x in range(8):
                for y in range(8):
                    c = (
                        ((tile_bytes[0x00 + y * 2] & (0x80 >> x)) << 0) |
                        ((tile_bytes[0x01 + y * 2] & (0x80 >> x)) << 1) |
                        ((tile_bytes[0x10 + y * 2] & (0x80 >> x)) << 2) |
                        ((tile_bytes[0x11 + y * 2] & (0x80 >> x)) << 3)
                        ) >> (7 - x)
                    tile.putpixel((x,y), self.palette[c])
            self.tiles[i] = tile

    def test_export_raw(self, filename):
        composite = Image.new('RGB', (128, 32), self.palette[0])
        for i,tile in enumerate(self.tiles):
            composite.paste(tile, ((i % 16) * 8, (int(i / 16)) * 8))
        composite.save(filename)

    def build_combinations(self):
        combinations = {}
        used_tiles = set()
        red_tile = Image.new('RGBA', (8,8), (255, 0, 0, 160))

        for spec_name in COMBINATIONS:
            spec = COMBINATIONS[spec_name]
            width = len(spec[0]) * 8
            height = len(spec) * 8
            combo = Image.new('RGBA', (width, height), (0,0,0,0))

            for y,row in enumerate(spec):
                for x,index in enumerate(row):
                    if index != 0x36:   # hardcode to exclude unused "special" tile
                        combo.paste(self.tiles[index], (x * 8, y * 8))
                    if index in used_tiles:
                        combo.alpha_composite(red_tile, (x * 8, y * 8))
                    used_tiles.add(index)

            combinations[spec_name] = combo
            
        return combinations


    def test_export_combinations(self, filename):
        combinations = self.build_combinations()
        total_width = 0
        PADDING = 4

        for combo in combinations:
            total_width += combo.width + PADDING

        total_width -= PADDING

        composite = Image.new('RGB', (total_width, 24), self.palette[0])
        x = 0
        for combo in combinations:
            composite.paste(combo, (x, 24 - combo.height))
            x += combo.width + PADDING

        composite.save(filename)

    def export_template(self, filename):
        img = Image.open(TEMPLATE['filename']).convert('RGBA')

        combinations = self.build_combinations()
        for name in TEMPLATE['combinations']:
            img.alpha_composite(combinations[name], TEMPLATE['combinations'][name])

        draw = ImageDraw.Draw(img)
        x,y = TEMPLATE['palette']
        corner_offset = TEMPLATE['palette_stride'] - 1
        for color in self.palette:
            draw.rectangle([(x,y),(x+corner_offset,y+corner_offset)], color)
            x += TEMPLATE['palette_stride']

        img.save(filename)

    def import_template(self, filename):
        img = Image.open(filename)

        # load palette
        for i in range(16):
            x,y = TEMPLATE['palette']
            x += i * TEMPLATE['palette_stride']
            self.palette[i] = img.getpixel( (x, y) )

        # load tiles
        new_tiles = [None] * TILES_PER_SET
        for combination in TEMPLATE['combinations']:
            src_x, src_y = TEMPLATE['combinations'][combination]
            for row_index,row in enumerate(COMBINATIONS[combination]):
                for col_index,tileset_index in enumerate(row):
                    if new_tiles[tileset_index] is not None:
                        continue

                    if tileset_index == 0x36:
                        # don't import unused tile 0x36
                        continue

                    x = src_x + col_index * 8
                    y = src_y + row_index * 8
                    box = (x, y, x + 8, y + 8)
                    new_tiles[tileset_index] = img.crop(box)

        self.tiles = new_tiles

    def encode_palette(self, vintage=False):
        palette_bytes = []

        if vintage:
            palette = crush(self.palette, transparent=True, keep_indices=[1], use_kept_colors=False, keep_count=3)
        else:
            palette = self.palette

        for palette_index,color in enumerate(palette):
            val = 0
            for i in range(3):
                component = color[i] / 255.0

                # Apply color transform to tweak brightness in darker colors
                component = math.pow(component, 0.85)

                converted_component = int(round(component * 31.0))
                val |= (converted_component << (i * 5))

            palette_bytes.append(val & 0xFF)
            palette_bytes.append((val >> 8) & 0xFF)

        return bytes(palette_bytes)

    def encode_tileset(self):
        tileset_bytes = []
        for tileset_index,tile in enumerate(self.tiles):
            if tileset_index == 0x36:
                # dummy data for unused special tile
                tileset_bytes.extend([int(b, 16) for b in 'ff 00 ff 00 ff 00 ff 00 ff 00 ff 00 ff 00 ff 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'.split()])
                continue

            bitplanes = [[], [], [], []]
            for y in range(8):
                row = []
                for x in range(8):
                    pixel = tile.getpixel( (x,y) )
                    if pixel not in self.palette:
                        template_coordinate = get_template_coordinate(tileset_index, (x, y))
                        sys.stderr.write(f'Error: tile {tileset_index:02X} contains color not in palette @ template position {template_coordinate}\n')
                        row.append(0)
                    else:
                        row.append(self.palette.index(pixel))

                # convert row to bitplanes
                for bitplane_index in range(len(bitplanes)):
                    bitrow = 0
                    for i,val in enumerate(row):
                        if val & (0x01 << bitplane_index):
                            bitrow |= (0x80 >> i)
                    bitplanes[bitplane_index].append(bitrow)

            interleaved_bitplanes = []
            for i in range(8):
                interleaved_bitplanes.append(bitplanes[0][i])
                interleaved_bitplanes.append(bitplanes[1][i])
            for i in range(8):
                interleaved_bitplanes.append(bitplanes[2][i])
                interleaved_bitplanes.append(bitplanes[3][i])

            tileset_bytes.extend(interleaved_bitplanes)

        return bytes(tileset_bytes)

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


def action_export(args):
    with open('PATH-TO-ROM', 'rb') as infile:
        palette_data = []
        tileset_data = []

        infile.seek(0xE7D00)
        for i in range(14):
            palette_data.append(infile.read(0x20))

        infile.seek(0xD0000)
        for i in range(14):
            tileset_data.append(infile.read(TILES_PER_SET * 0x20))


    for i in range(14):
        character = Character()
        character.decode_palette(palette_data[i])
        character.decode_tileset(tileset_data[i])
        character.export_template(f'template_{JOBS[i]}.png')

def action_import(args):
    character = Character()
    character.import_template(args.filename)
    print(character.encode_palette())
    print(character.encode_tileset())

def action_build(args):
    print('Scanning src directory...')
    bank_srcs = []
    for job_index,job in enumerate(JOBS):
        filenames = sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'src', job, '*.png')))
        for i,filename in enumerate(filenames):
            while i >= len(bank_srcs):
                bank_srcs.append([None] * len(JOBS))
            bank_srcs[i][job_index] = filename

    with open(os.path.join(os.path.dirname(__file__), 'piggy.bin'), 'rb') as infile:
        piggy_data = infile.read()

    combined_bank_stream = io.BytesIO()
    combined_vintage_bank_stream = io.BytesIO()

    for bank_index,bank_src in enumerate(bank_srcs):
        if None in bank_srcs:
            sys.stderr.write(f'Fashion bank {bank_index} does not contain images for all jobs; aborting\n')
            break

        print(f'Building fashion bank {bank_index}')

        chr_bytestream = io.BytesIO()
        pal_bytestream = io.BytesIO()
        vintage_pal_bytestream = io.BytesIO()

        for filename in bank_src:
            print(f'  Importing {filename}')
            character = Character()
            character.import_template(filename)
            chr_bytestream.write(character.encode_tileset())
            pal_bytestream.write(character.encode_palette())
            vintage_pal_bytestream.write(character.encode_palette(vintage=True))

        chr_bytestream.seek(0)
        pal_bytestream.seek(0)

        combined_bank_stream.write(chr_bytestream.read())
        combined_bank_stream.write(bytes([0,]) * (0x7000 - chr_bytestream.tell()))
        combined_bank_stream.write(piggy_data)
        combined_bank_stream.write(bytes([0,]) * (0x0D00 - len(piggy_data)))
        combined_bank_stream.write(pal_bytestream.read())
        combined_bank_stream.write(bytes([0,]) * (0x0300 - pal_bytestream.tell()))

        chr_bytestream.seek(0)
        vintage_pal_bytestream.seek(0)

        combined_vintage_bank_stream.write(chr_bytestream.read())
        combined_vintage_bank_stream.write(bytes([0,]) * (0x7000 - chr_bytestream.tell()))
        combined_vintage_bank_stream.write(piggy_data)
        combined_vintage_bank_stream.write(bytes([0,]) * (0x0D00 - len(piggy_data)))
        combined_vintage_bank_stream.write(vintage_pal_bytestream.read())
        combined_vintage_bank_stream.write(bytes([0,]) * (0x0300 - vintage_pal_bytestream.tell()))

    print('Writing combined banks')
    combined_bank_stream.seek(0)
    with open(os.path.join(os.path.dirname(__file__), 'fashion.bin'), 'wb') as outfile:
        outfile.write(combined_bank_stream.read())

    combined_vintage_bank_stream.seek(0)
    with open(os.path.join(os.path.dirname(__file__), 'fashion_vintage.bin'), 'wb') as outfile:
        outfile.write(combined_vintage_bank_stream.read())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    export_parser = subparsers.add_parser('export')
    export_parser.set_defaults(func=action_export)

    import_parser = subparsers.add_parser('import')
    import_parser.set_defaults(func=action_import)
    import_parser.add_argument('filename')

    build_parser = subparsers.add_parser('build')
    build_parser.set_defaults(func=action_build)

    args = parser.parse_args()
    args.func(args)



