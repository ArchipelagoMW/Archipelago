import argparse
import json
from os import listdir
from os.path import isfile, join
from Rom import Sprite
from Gui import get_image_for_sprite

parser = argparse.ArgumentParser(description='Dump sprite data and .png files to a directory.')
parser.add_argument('-i')
parser.add_argument('-o')
args = parser.parse_args()

if not args.i or not args.o:
    print('Invalid arguments provided. -i and -o are required.')
    exit()

# Target directories
input_dir = args.i
output_dir = args.o

# Get a list of all files in the input directory
targetFiles = [file for file in listdir(input_dir) if isfile(join(input_dir, file))]

spriteData = {}

for file in targetFiles:
    if file[-5:] != '.zspr':
        continue

    sprite = Sprite(join(input_dir, file))
    spriteData[sprite.name] = file

    image = open(f'{output_dir}/{sprite.name}.gif', 'wb')
    image.write(get_image_for_sprite(sprite, True))
    image.close()

jsonFile = open(f'{output_dir}/spriteData.json', 'w')
jsonFile.write(json.dumps(spriteData))
jsonFile.close()
