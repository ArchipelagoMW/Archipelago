from . import ff4struct

TILESET_DESCRIPTIONS = [
    "Airship",
    "Lunar Core",
    "Sealed Cave",
    "Castle Exterior",
    "Town",
    "House",
    "Castle Interior",
    "Crystal Room",
    "Lunar Whale",
    "Feymarch",
    "Tower",
    "Giant",
    "Lunar Subterrane",
    "Mountain",
    "Cave",
    "Ship",
]

TILE_PROPERTIES = {
    'layer1'        : 'is layer 1',
    'layer2'        : 'is layer 2',
    'bridge_layer'  : 'is bridge layer',
    'save_point'    : 'is save point',
    'closed_door'   : 'is closed door',
    'walk_behind'   : 'is walk behind',
    'bottom_half'   : 'is bottom half',
    'warp'          : 'is warp',
    'talkover'      : 'is talkover',
    'encounters'    : 'has encounters',
    'trigger'       : 'is trigger'
}

def decompile_tilesets(rom):
    lines = []
    for i,byte_list in enumerate(rom.tilesets):
        lines.append('tileset(${:02X}) // {}'.format(i, TILESET_DESCRIPTIONS[i]))
        lines.append('{')
        tileset = ff4struct.tileset.decode(byte_list)
        for tile_id,tile in enumerate(tileset):
            relevant_properties = []
            for p in TILE_PROPERTIES:
                if getattr(tile, p):
                    relevant_properties.append(TILE_PROPERTIES[p])

            lines.append('    ${:02X} {{ {} }}'.format(
                tile_id,
                ', '.join(relevant_properties)
                ))
        lines.append('}')
        lines.append('')

    return '\n'.join(lines)
