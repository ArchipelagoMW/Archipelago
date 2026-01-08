def get_sprites():
    from ..graphics.sprites.sprites import id_sprite
    
    sprites = [{
        'id': sprite_id,
        'key': key,
    } for ((sprite_id, key)) in id_sprite.items()]
    
    return sprites

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

    import json
    print(json.dumps(get_sprites()))
