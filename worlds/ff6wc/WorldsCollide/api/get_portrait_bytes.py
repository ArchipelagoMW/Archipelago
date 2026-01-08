
def get_portrait_bytes(portrait_id):
    from ..graphics.portraits.portraits import get_bin_path, get_pal_path

    return get_rgb_bytes(get_bin_path(portrait_id), get_pal_path(portrait_id))

def get_rgb_bytes(portrait_path, palette_path):
    from ..graphics.palette_file import PaletteFile
    from ..graphics.sprite_file import SpriteFile
    from ..graphics.poses import PORTRAIT
    palette = PaletteFile(palette_path)

    sprite = SpriteFile(portrait_path, palette)

    portrait_bytes = [item for sublist in sprite.tile_matrix(PORTRAIT) for item in sublist]
    palette_bytes =  [(color.red, color.green, color.blue) for color in palette.colors]
    return (portrait_bytes, palette_bytes)
