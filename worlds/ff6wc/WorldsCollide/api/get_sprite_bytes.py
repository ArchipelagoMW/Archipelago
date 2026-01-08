def get_sprite_bytes(sprite_id, palette_id, pose_id):
    from ..graphics.sprites.sprites import get_path as get_sprite_path
    from ..graphics.palettes.palettes import get_path as get_palette_path

    return get_rgb_bytes(get_sprite_path(sprite_id), get_palette_path(palette_id), pose_id)

def get_rgb_bytes(sprite_path, palette_path, pose_id):
    from ..graphics.palette_file import PaletteFile
    from ..graphics.sprite_file import SpriteFile
    from ..graphics.poses import CHARACTER
    palette = PaletteFile(palette_path)

    sprite = SpriteFile(sprite_path, palette)

    rgb_bytes = sprite.rgb_data(CHARACTER[pose_id])
    alpha_bytes = palette.alpha_rgb_data
    return (rgb_bytes, alpha_bytes)
