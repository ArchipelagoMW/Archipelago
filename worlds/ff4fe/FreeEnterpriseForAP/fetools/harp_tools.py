import dataclasses
import io
import zipfile

import util
import cherrypy

from asset_tools import AssetToolSite, asset_action, make_save_result, make_text_result
from asset import assetclass

import harp.common
import harp.midi

@assetclass
class HarpSongAsset:
    midi : bytes = dataclasses.field(default=bytes(), metadata={'mimetype' : 'audio/midi'})
    title : str = '-untitled-'
    source : str = ''
    composer : str = ''
    sequencer : str = ''
    reference : str = ''

    converter : str = dataclasses.field(default='general', metadata={'options' : ['general', 'permissive']})
    transpose : int = -12
    octave_range : int = 5
    fixed_tempo : int = 0

@asset_action('Download MIDI')
def download_midi(asset):
    return make_save_result(asset.midi, util.filesafe(f"{asset.source}_{asset.title}") + '.mid', 'audio/midi')

@asset_action('Test ROM')
def test_rom(asset):
    test_rom = util.compile_test_rom(harp.common.generate_test_rom_script(asset))
    return make_save_result(test_rom, 'testharp_' + util.filesafe(f"{asset.source}_{asset.title}") + '.sfc')

@asset_action('Compile F4C')
def compile_f4c(asset):
    script = harp.common.generate_script(asset)
    return make_save_result(script.encode('utf-8'), f'harp_{asset.id}.f4c')

@asset_action("View embedded MIDI text")
def view_text(asset):
    return make_text_result(harp.midi.extract_midi_text(asset.midi))

@asset_action("Generate full catalog")
def catalog(assets):
    zip_stream = io.BytesIO()
    catalog_zip = zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED)
    ids = []
    for asset in assets:
        print(f'Cataloguing {asset.id} - {asset.title} / {asset.source}')
        ids.append(asset.id)

        filename = f'{asset.id}.asset'
        script = harp.common.generate_script(asset)
        catalog_zip.writestr(filename, script.encode('utf-8'))

    catalog_zip.writestr('catalog', ('\n'.join(ids) + '\n').encode('utf-8'))

    catalog_zip.close()
    zip_stream.seek(0)

    return make_save_result(zip_stream.read(), 'harp_catalog.zip', 'application/zip')


class HarpToolSite(AssetToolSite):
    def __init__(self, env, title, asset_path):
        super().__init__(
            env = env, 
            title = title, 
            asset_path = asset_path,
            asset_class = HarpSongAsset,
            table_columns = ['title', 'source'],
            table_actions = [test_rom, compile_f4c],
            detail_actions = [download_midi, view_text, test_rom, compile_f4c],
            global_actions = [catalog],
            detail_scripts = ['harpEditHelpers.js']
            )

