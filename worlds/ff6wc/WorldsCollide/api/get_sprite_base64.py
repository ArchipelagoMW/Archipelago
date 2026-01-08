def get_sprite_base64(sprite_id, palette_id, pose_id):
    from ..graphics.sprites.sprites import get_path as get_sprite_path
    from ..graphics.palettes.palettes import get_path as get_palette_path

    return get_base64(get_sprite_path(sprite_id), get_palette_path(palette_id), pose_id)

def get_base64(sprite_path, palette_path, pose_id):
    from ..graphics.palette_file import PaletteFile
    from ..graphics.sprite_file import SpriteFile
    from ..graphics.poses import CHARACTER
    palette = PaletteFile(palette_path)
    sprite = SpriteFile(sprite_path, palette)
    (r, g, b) = palette.alpha_rgb_data

    image = sprite.get_ppm(CHARACTER[pose_id])
    from PIL import Image 
    from io import BytesIO
    import base64
    
    png = Image.open(BytesIO(bytes(image))).convert('RGBA')
    no_bg = Image.new('RGBA', png.size, (r, g, b, 0))

    new_image = []
    for item in png.getdata():
        if item[:3] == (r, g, b):
            new_image.append((255, 255, 255, 0))
        else:
            new_image.append(item)

    no_bg.putdata(new_image)
    
    io = BytesIO()
    no_bg.save(io, format="PNG")
    img_str = base64.b64encode(io.getvalue())
    print(img_str.decode('utf-8'))
    return img_str.decode('utf-8')
    