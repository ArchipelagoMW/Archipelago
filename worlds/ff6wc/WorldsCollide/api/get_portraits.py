
def get_portraits():
    from ..graphics.portraits.portraits import id_portrait
    
    sprites = [{
        'id': portrait_id,
        'key': key,
    } for ((portrait_id, key)) in id_portrait.items()]
    
    return sprites

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

    import json
    print(json.dumps(get_portraits()))
