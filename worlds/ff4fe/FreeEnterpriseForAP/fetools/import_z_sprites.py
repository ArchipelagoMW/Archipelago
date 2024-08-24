import glob
import os
import re
import argparse

from z_tools import ZSpriteAsset

parser = argparse.ArgumentParser()
parser.add_argument('path', default='../FreeEnt/assets/zeromus_pics')
args = parser.parse_args()

def filename_to_enemy_name(filename):
    enemy_name = os.path.splitext(os.path.basename(filename))[0]
    enemy_name = re.sub(r'^__', '', enemy_name)
    enemy_name = enemy_name.replace('[Q]', '?')
    enemy_name = enemy_name.replace('[S]', '/')
    enemy_name = re.sub(r'\s*\(\d+\)\s*$', '', enemy_name)
    return enemy_name

for path in glob.glob(os.path.join(args.path, '*.png')):
    print(f'Processing {path}')
    with open(path, 'rb') as infile:
        png_bytes = infile.read()

    asset = ZSpriteAsset()
    asset.name = filename_to_enemy_name(path)
    asset.png = png_bytes
    asset.source = ''

    outpath = f'assets/z/{asset.id}.asset'
    asset.save(outpath)
