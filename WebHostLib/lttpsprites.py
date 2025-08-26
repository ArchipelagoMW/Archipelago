import os
import threading
import json

from Utils import local_path, user_path
from worlds.alttp.Rom import Sprite


def update_sprites_lttp():
    from tkinter import Tk
    from LttPAdjuster import get_image_for_sprite
    from LttPAdjuster import BackgroundTaskProgress
    from LttPAdjuster import BackgroundTaskProgressNullWindow
    from LttPAdjuster import update_sprites

    # Target directories
    input_dir = user_path("data", "sprites", "alttp", "remote")
    output_dir = local_path("WebHostLib", "static", "generated")  # TODO: move to user_path

    os.makedirs(os.path.join(output_dir, "sprites"), exist_ok=True)
    # update sprites through gui.py's functions
    done = threading.Event()
    try:
        top = Tk()
    except:
        task = BackgroundTaskProgressNullWindow(update_sprites, lambda successful, resultmessage: done.set())
    else:
        top.withdraw()
        task = BackgroundTaskProgress(top, update_sprites, "Updating Sprites", lambda succesful, resultmessage: done.set())
    while not done.isSet():
        task.do_events()

    spriteData = []

    for file in (file for file in os.listdir(input_dir) if not file.startswith(".")):
        sprite = Sprite(os.path.join(input_dir, file))

        if not sprite.name:
            print("Warning:", file, "has no name.")
            sprite.name = file.split(".", 1)[0]
        if sprite.valid:
            with open(os.path.join(output_dir, "sprites", f"{os.path.splitext(file)[0]}.gif"), 'wb') as image:
                image.write(get_image_for_sprite(sprite, True))
            spriteData.append({"file": file, "author": sprite.author_name, "name": sprite.name})
        else:
            print(file, "dropped, as it has no valid sprite data.")
    spriteData.sort(key=lambda entry: entry["name"])
    with open(f'{output_dir}/spriteData.json', 'w') as file:
        json.dump({"sprites": spriteData}, file, indent=1)
    return spriteData
