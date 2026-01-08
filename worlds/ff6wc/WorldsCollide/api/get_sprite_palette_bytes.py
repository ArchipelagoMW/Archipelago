def get_sprite_palette_bytes(sprite_id, palette_id, pose_id):
    from ..graphics.sprites.sprites import get_path as get_sprite_path
    from ..graphics.palettes.palettes import get_path as get_palette_path
    from ..graphics.palette_file import PaletteFile
    from ..graphics.sprite_file import SpriteFile
    from ..graphics.poses import CHARACTER
    
    palette = PaletteFile(get_palette_path(palette_id))
    sprite = SpriteFile(get_sprite_path(sprite_id), palette)
    
    palette_bytes = [(color.red, color.green, color.blue) for color in palette.colors]
    sprite_bytes = [item for sublist in sprite.tile_matrix(CHARACTER[pose_id]) for item in sublist]
    
    return (sprite_bytes, palette_bytes)

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("sprite_id", type=int,
                        help="Id of the sprite to print")
    parser.add_argument("palette_id", type=int,
                        help="Id of the palette for the sprite")
    parser.add_argument("pose_id", type=int,
                        help="Id of the pose for the sprite", default=1)

    args = parser.parse_args()

    (sprite, palette) = get_sprite_palette_bytes(args.sprite_id, args.palette_id, args.pose_id)

    import json
    print(json.dumps({
        'sprite': sprite,
        'palette': palette,
    }))
