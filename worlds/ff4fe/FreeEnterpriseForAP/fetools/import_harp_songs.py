import glob
import os
import re
import json
import argparse

from harp_tools import HarpSongAsset

parser = argparse.ArgumentParser()
parser.add_argument('path', default='../FreeEnt/assets/harp/src')
args = parser.parse_args()

for path in glob.glob(os.path.join(args.path, '*.mid')):
    print(f'Processing {path}')
    
    metadata_path = path + '.metadata'
    with open(metadata_path, 'r') as infile:
        metadata = json.load(infile)

    asset = HarpSongAsset()
    asset.title = metadata.get('title', '')
    asset.source = metadata.get('from', '')
    asset.composer = metadata.get('composer', '')
    asset.sequencer = metadata.get('sequencer', '')

    reference = ''
    if metadata.get('src_filename', '').startswith('http'):
        reference = metadata.get('src_filename')

    if metadata.get('reference'):
        reference = (metadata.get('reference') + ' / ' + reference) if reference else metadata.get('reference')

    asset.reference = reference

    convert_params = metadata.get('convert_params', {})
    asset.transpose = convert_params.get('transpose', -12)
    asset.octave_range = convert_params.get('octave_range', 5)
    asset.fixed_tempo = convert_params.get('fixed_tempo', 0)

    with open(path, 'rb') as infile:
        asset.midi = infile.read()

    outpath = f'assets/harp/{asset.id}.asset'
    asset.save(outpath)
