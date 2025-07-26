from .Utils import data_path

# TODO
# Move the tunic to the generalized system

def add_hue(image, color, tiff=False):
    """Function for adding hue to a greyscaled icon"""
    start = 154 if tiff else 0
    for i in range(start, len(image), 4):
        try:
            for x in range(3):
                image[i + x] = int(((image[i + x]/255) * (color[x]/255)) * 255)
        except:
            pass
    return image


def add_belt(tunic, belt, tiff=False):
    """Function for adding belt to tunic"""
    start = 154 if tiff else 0
    for i in range(start, len(tunic), 4):
        try:
            if belt[i + 3] != 0:
                alpha = belt[i + 3] / 255
                for x in range(3):
                    tunic[i + x] = int((belt[i + x] * alpha) + (tunic[i + x] * (1 - alpha)))
        except:
            pass
    return tunic


def generate_tunic_icon(color):
    """Function for putting tunic colors together"""
    with open(data_path('icons/grey.tiff'), 'rb') as grey_fil, open(data_path('icons/belt.tiff'), 'rb') as belt_fil:
        grey = list(grey_fil.read())
        belt = list(belt_fil.read())
        return add_belt(add_hue(grey, color, True), belt, True)[154:]

# END TODO

def add_extra_data(rgbValues, fileName, intensity=0.5):
    """Function to add extra data on top of icon"""
    fileRGB = []
    with open(fileName, "rb") as fil:
        data = fil.read()
        for i in range(0, len(data), 4):
            fileRGB.append(list(data[i:i + 4]))
    for i in range(len(rgbValues)):
        alpha = fileRGB[i][3] / 255
        for x in range(3):
            rgbValues[i][x] = int((fileRGB[i][x] * alpha + intensity) + (rgbValues[i][x] * (1 - alpha - intensity)))


def greyscaleRGB(rgbValues, intensity: int=2):
    """Function for desaturating RGB values"""
    for rgb in rgbValues:
        rgb[0] = rgb[1] = rgb[2] = int((rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722) * intensity)
    return rgbValues


def rgb5a1ToRGB(rgb5a1Bytes):
    """Converts rgb5a1 values to RGBA lists"""
    pixels = []
    for i in range(0, len(rgb5a1Bytes), 2):
        bits = format(rgb5a1Bytes[i], '#010b')[2:] + format(rgb5a1Bytes[i + 1], '#010b')[2:]
        r = int(int(bits[0:5], 2) * (255/31))
        g = int(int(bits[5:10], 2) * (255/31))
        b = int(int(bits[10:15], 2) * (255/31))
        a = int(bits[15], 2) * 255
        pixels.append([r, g, b, a])
    return pixels


def addHueToRGB(rgbValues, color):
    """Adds a hue to RGB values"""
    for rgb in rgbValues:
        for i in range(3):
            rgb[i] = int(((rgb[i]/255) * (color[i]/255)) * 255)
    return rgbValues


def rgbToRGB5a1(rgbValues):
    """Convert RGB to RGB5a1 format"""
    rgb5a1 = []
    for rgb in rgbValues:
        r = int(rgb[0] / (255/31))
        r = r if r <= 31 else 31
        r = r if r >= 0 else 0
        g = int(rgb[1] / (255/31))
        g = g if g <= 31 else 31
        g = g if g >= 0 else 0
        b = int(rgb[2] / (255/31))
        b = b if b <= 31 else 31
        b = b if b >= 0 else 0
        a = int(rgb[3] / 255)
        bits = format(r, '#07b')[2:] + format(g, '#07b')[2:] + format(b, '#07b')[2:] + format(a, '#03b')[2:]
        rgb5a1.append(int(bits[:8], 2))
        rgb5a1.append(int(bits[8:], 2))
    for i in rgb5a1:
        assert i <= 255, i
    return bytes(rgb5a1)


def patch_overworld_icon(rom, color, address, fileName = None):
    original = rom.original.read_bytes(address, 0x800)

    if color is None:
        rom.write_bytes(address, original)
        return

    rgbBytes = rgb5a1ToRGB(original)
    greyscaled = greyscaleRGB(rgbBytes)
    rgbBytes = addHueToRGB(greyscaled, color)
    if fileName != None:
        add_extra_data(rgbBytes, fileName)
    rom.write_bytes(address, rgbToRGB5a1(rgbBytes))
