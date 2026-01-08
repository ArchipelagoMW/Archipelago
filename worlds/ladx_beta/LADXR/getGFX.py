import requests
import PIL.Image
import re

url = "https://raw.githubusercontent.com/CrystalSaver/Z4RandomizerBeta2/master/"

for k, v in requests.get(url + "asset-manifest.json").json()['files'].items():
    m = re.match("static/media/Graphics(.+)\\.bin", k)
    assert m is not None
    if not k.startswith("static/media/Graphics") or not k.endswith(".bin"):
        continue
    name = m.group(1)
    
    data = requests.get(url + v).content
    
    icon = PIL.Image.new("P", (16, 16))
    buffer = bytearray(b'\x00' * 16 * 8)
    for idx in range(0x0C0, 0x0C2):
        for y in range(16):
            a = data[idx * 32 + y * 2]
            b = data[idx * 32 + y * 2 + 1]
            for x in range(8):
                v = 0
                if a & (0x80 >> x):
                    v |= 1
                if b & (0x80 >> x):
                    v |= 2
                buffer[x+y*8] = v
        tile = PIL.Image.frombytes('P', (8, 16), bytes(buffer))
        x = (idx % 16) * 8
        icon.paste(tile, (x, 0))
    pal = icon.getpalette()
    assert pal is not None
    pal[0:3] = [150, 150, 255]
    pal[3:6] = [0, 0, 0]
    pal[6:9] = [59, 180, 112]
    pal[9:12] = [251, 221, 197]
    icon.putpalette(pal)
    icon = icon.resize((32, 32))
    icon.save("gfx/%s.bin.png" % (name))
    open("gfx/%s.bin" % (name), "wb").write(data)
