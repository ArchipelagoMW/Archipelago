from .tileset import walkable_tiles, entrance_tiles
import random


ENEMIES = {
    "mountains": [
        (0x0B,),
        (0x0E,),
        (0x29,),
        (0x0E, 0x0E),
        (0x0E, 0x0E, 0x23),
        (0x0D,), (0x0D, 0x0D),
    ],
    "egg": [],
    "basic": [
        (), (), (), (), (), (),
        (0x09,), (0x09, 0x09),  # octorock
        (0x9B, 0x9B), (0x9B, 0x9B, 0x1B),  # slimes
        (0xBB, 0x9B),  # bush crawler + slime
        (0xB9,),
        (0x0B, 0x23),  # likelike + moblin
        (0x14, 0x0B, 0x0B),  # moblins + sword
        (0x0B, 0x23, 0x23),  # likelike + moblin
        (0xAE, 0xAE),  # flying octorock
        (0xBA, ),  # Bomber
        (0x0D, 0x0D), (0x0D, ),
    ],
    "town": [
        (), (), (0x6C, 0x6E), (0x6E,), (0x6E, 0x6E),
    ],
    "forest": [
        (0x0B,),  # moblins
        (0x0B, 0x0B),  # moblins
        (0x14, 0x0B, 0x0B),  # moblins + sword
    ],
    "beach": [
        (0xC6, 0xC6),
        (0x0E, 0x0E, 0xC6),
        (0x0E, 0x0E, 0x09),
    ],
    "water": [],
}


def generate_enemies(room):
    options = ENEMIES[room.tileset_id]
    if not options:
        return
    positions = []
    for y in range(1, 7):
        for x in range(1, 9):
            if room.tiles[x + y * 10] in walkable_tiles and room.tiles[x + (y - 1) * 10] not in entrance_tiles:
                positions.append((x, y))
    for type_id in random.choice(options):
        if not positions:
            return
        x, y = random.choice(positions)
        positions.remove((x, y))
        room.entities.append((x, y, type_id))
