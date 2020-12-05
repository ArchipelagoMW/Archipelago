from Gui import *
import threading

# Target directories
input_dir = local_path("data", "sprites", "alttpr")
output_dir = local_path("WebHostLib", "static", "static")

#update sprites through gui.py's functions
done = threading.Event()
top = Tk()
top.withdraw()
BackgroundTaskProgress(top, update_sprites, "Updating Sprites", lambda succesful, resultmessage: done.set())
while not done.isSet():
    top.update()

print("Done updating sprites")

spriteData = []

for file in os.listdir(input_dir):
    sprite = Sprite(os.path.join(input_dir, file))

    if not sprite.name:
        print("Warning:",file,"has no name.")
        sprite.name = file.split(".", 1)[0]

    if sprite.valid:
        with open(os.path.join(output_dir, "sprites", f"{sprite.name}.gif"), 'wb') as image:
            image.write(get_image_for_sprite(sprite, True))
        spriteData.append({"file": file, "author": sprite.author_name, "name": sprite.name})
    else:
        print(file, "dropped, as it has no valid sprite data.")
spriteData.sort(key=lambda entry: entry["name"])
with open(f'{output_dir}/spriteData.json', 'w') as file:
    json.dump({"sprites": spriteData}, file)
