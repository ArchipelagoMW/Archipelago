def get_palette_bytes(palette_id):
    from ..graphics.palettes.palettes import get_path as get_palette_path

    return get_rgb_bytes(get_palette_path(palette_id))

def get_rgb_bytes(palette_path):
    from ..graphics.palette_file import PaletteFile
    palette = PaletteFile(palette_path)

    return [(color.red, color.green, color.blue) for color in palette.colors]
