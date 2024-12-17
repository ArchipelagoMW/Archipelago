# create sprites for standing

SPRITE_START_X = 0x10 - 2
SPRITE_START_Y = 0x38 - 2
SPRITE_STRIDE_X = 0x50
SPRITE_STRIDE_Y = 0x20

sprite_obj = []
sprite_ext = []
name_addrs = []

for char_id in range(12):
    char_row = char_id % 4
    char_col = char_id // 4

    start_x = SPRITE_START_X + char_col * SPRITE_STRIDE_X
    start_y = SPRITE_START_Y + char_row * SPRITE_STRIDE_Y

    name_addrs.append(0x208 + (char_col * 2 * 10) + (char_row * 0x40 * 4))

    for row in range(3):
        for col in range(2):
            x = start_x + col * 8
            y = start_y + row * 8
            tile = 0xB0 + (char_id * 6) + (row * 2) + col
            palette = 4
            sprite_obj.extend([
                x & 0xFF,
                y,
                tile & 0xFF,
                0b00110000 | (palette << 1) | ((tile >> 8) & 0x01)
                ])
            sprite_ext.append((x >> 8) & 0x01)

while len(sprite_ext) % 4:
    sprite_ext.append(0)

packed_sprite_ext = []
for i in range(0, len(sprite_ext), 4):
    b = 0
    for j in range(4):
        b |= (sprite_ext[i+j] << j)
    packed_sprite_ext.append(b)

print(' '.join([f'{b:02X}' for b in sprite_obj]))
print()
print(f'{len(sprite_obj):X}')
print()
print(' '.join([f'{b:02X}' for b in packed_sprite_ext]))
print()
print(f'{len(packed_sprite_ext):X}')
print()
print(' '.join([f'{(v & 0xFF):02X} {((v >> 8) & 0xFF):02X}' for v in name_addrs]))
