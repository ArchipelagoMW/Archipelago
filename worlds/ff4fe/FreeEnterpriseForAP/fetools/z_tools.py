import dataclasses
import io
import zipfile

import cherrypy

import util
from asset_tools import AssetToolSite, asset_action, make_save_result
from asset import assetclass

from processors import zsprites
import f4c

@assetclass
class ZSpriteAsset:
    name : str = '-unnamed-'
    png : bytes = dataclasses.field(default=bytes(), metadata={'mimetype' : 'image/png'})
    description : str = ''

def _filesafe(name):
    return name.replace('?', '_').replace('/', '_')

@asset_action('Download PNG')
def download_png(asset):
    return make_save_result(asset.png, _filesafe(asset.name) + '.png', 'image/png')

def _generate_test_rom(asset, vintage=False):
    script = zsprites.generate_test_rom_script(asset.png, asset.name, vintage)
    return util.compile_test_rom(script)

@asset_action('Test ROM')
def test_rom(asset):
    test_rom = _generate_test_rom(asset, vintage=False)
    return make_save_result(test_rom, 'testzsprite_' + _filesafe(asset.name) + '.test.sfc')

@asset_action('Test ROM (-vintage)')
def test_rom_vintage(asset):
    test_rom = _generate_test_rom(asset, vintage=True)
    return make_save_result(test_rom, 'testzsprite_' + _filesafe(asset.name) + '.vintage.test.sfc')

@asset_action('Compile F4C')
def compile_f4c(asset):
    script = zsprites.generate_sprite_script(asset.png, asset.name)
    return make_save_result(script.encode('utf-8'), f'zsprite_{asset.id}.f4c')

@asset_action('Compile F4C (vintage)')
def compile_f4c_vintage(asset):
    script = zsprites.generate_sprite_script(asset.png, asset.name, True)
    return make_save_result(script.encode('utf-8'), f'zsprite_{asset.id}.vintage.f4c')

@asset_action('Generate full catalog')
def catalog(assets):
    zip_stream = io.BytesIO()
    catalog_zip = zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED)
    ids = []
    for asset in assets:
        print(f'Cataloguing {asset.id} - {asset.name}')
        ids.append(asset.id)

        filename = f'{asset.id}.asset'
        script = zsprites.generate_sprite_script(asset.png, asset.name, vintage=False)
        catalog_zip.writestr(filename, script.encode('utf-8'))

        vintage_filename = f'{asset.id}.vintage.asset'
        vintage_script = zsprites.generate_sprite_script(asset.png, asset.name, vintage=True)
        catalog_zip.writestr(vintage_filename, vintage_script.encode('utf-8'))

    catalog_zip.writestr('catalog', ('\n'.join(ids) + '\n').encode('utf-8'))

    catalog_zip.close()
    zip_stream.seek(0)

    return make_save_result(zip_stream.read(), 'zsprites_catalog.zip', 'application/zip')


class ZToolSite(AssetToolSite):
    def __init__(self, env, title, asset_path):
        super().__init__(
            env = env, 
            title = title, 
            asset_path = asset_path,
            asset_class = ZSpriteAsset,
            table_columns = ['name'],
            table_actions = [test_rom, compile_f4c],
            detail_actions = [download_png, test_rom, test_rom_vintage, compile_f4c, compile_f4c_vintage],
            global_actions = [catalog],
            index_scripts = ['zHelpers.js'],
            detail_scripts = ['zEditHelpers.js']
            )

    @cherrypy.expose
    def preview(self, asset):
        asset = self._load_asset(asset)
        return util.btoa(asset.png)
