import glob
import os
import json
import dataclasses
import io
import zipfile
import traceback

import cherrypy

import util

class AssetAction:
    def __init__(self, fn, slug, title):
        self._fn = fn
        self._slug = slug
        self._title = title

    @property
    def fn(self):
        return self._fn

    @property
    def slug(self):
        return self._slug

    @property
    def title(self):
        return self._title

def asset_action(title):
    def wrapper(fn):
        return AssetAction(fn, fn.__name__, title)
    return wrapper

def make_save_result(data, filename, mimetype='application/octet-stream'):
    return {
        'action' : 'save',
        'filename' : filename,
        'mimetype' : mimetype,
        'data' : util.btoa(data)
        }

def make_text_result(text):
    return {
        'action' : 'text',
        'text' : text
    }

class AssetToolSite:
    def __init__(self, env,
        title,
        asset_class,
        asset_path,
        table_columns = [],
        table_actions = [],
        detail_actions = [],
        global_actions = [],
        index_scripts = [],
        detail_scripts = [],
    ):
        self._env = env
        self._title = title
        self._asset_class = asset_class
        self._asset_path = asset_path
        self._table_columns = table_columns
        self._table_actions = table_actions
        self._detail_actions = detail_actions
        self._global_actions = global_actions
        self._index_scripts = index_scripts
        self._detail_scripts = detail_scripts

        self._action_map = { action.slug : action for action in (table_actions + detail_actions + global_actions) }

    def _get_asset_path(self, assetId):
        return os.path.join(self._asset_path, f'{assetId}.asset')

    def _load_asset(self, assetId):
        return self._asset_class.fromfile(self._get_asset_path(assetId))

    def _load_all_assets(self):
        assets = []
        for path in glob.glob(os.path.join(self._asset_path, '*.asset')):
            asset = self._asset_class.fromfile(path)
            assets.append(asset)

        return assets

    @cherrypy.expose
    def index(self):
        assets = self._load_all_assets()
        assets_data = []
        for asset in assets:
            data = {'id' : asset.id, 'created' : asset.ctime, 'modified' : asset.mtime}
            for column in self._table_columns:
                data[column] = getattr(asset, column)
            assets_data.append(data)

        assets_json = json.dumps(assets_data)

        return self._env.get_template('asset_index.html').render(
            title = self._title,
            asset_count = len(assets),
            assets_json = assets_json,
            columns = self._table_columns,
            table_actions = self._table_actions,
            global_actions = self._global_actions,
            scripts = self._index_scripts
            )

    def _render_edit_page(self, asset):
        fields = []
        for f in asset.fields:
            field_info = { 
                'name' : f.name, 
                'type' : f.type.__name__, 
                'default' : (util.btoa(getattr(asset, f.name)) if f.type is bytes else str(getattr(asset, f.name))).replace('"', '\\"'),
                'mimetype' : f.metadata.get('mimetype', ''),
                'options' : f.metadata.get('options', None)
            }
            fields.append(field_info)

        return self._env.get_template('asset_edit.html').render(
            asset = asset,
            fields = fields,
            detail_actions = self._detail_actions,
            scripts = self._detail_scripts
            )

    @cherrypy.expose
    def new(self):
        asset = self._asset_class()
        while (os.path.exists(self._get_asset_path(asset.id))):
            asset = self._asset_class()
        return self._render_edit_page(asset)

    @cherrypy.expose
    def edit(self, assetId):
        asset = self._load_asset(assetId)
        return self._render_edit_page(asset)

    def _build_asset_from_post_params(self):
        asset = self._asset_class()
        fields = { f.name : f.type for f in asset.fields }
        found_field = False
        for q in cherrypy.request.params:
            if not q.startswith('assetfield__'):
                continue
            field = q[len('assetfield__'):]
            if field in fields:
                found_field = True
                field_type = fields[field]
                field_value = cherrypy.request.params[q]
                if field_type is str:
                    setattr(asset, field, field_value)
                elif field_type is bytes:
                    setattr(asset, field, field_value.file.read())
                else:
                    setattr(asset, field, field_type(field_value))

        return (asset if found_field else None)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def action(self, action, assetId=None, **kwargs):
        asset = None
        if assetId is None and cherrypy.request.method == 'POST':
            asset = self._build_asset_from_post_params()
        elif assetId:
            asset = self._load_asset(assetId)

        try:
            if asset:
                return self._action_map[action].fn(asset)
            else:
                return self._action_map[action].fn(self._load_all_assets())
        except:
            return { 'error' : traceback.format_exc() }

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def save(self, **kwargs):
        asset = self._build_asset_from_post_params()
        if asset is None:
            raise cherrypy.HTTPError(400, "No asset provided");

        asset.save(self._get_asset_path(asset.id))

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def delete(self, assetId):
        if os.path.isfile(self._get_asset_path(assetId)):
            os.unlink(self._get_asset_path(assetId))

    @cherrypy.expose
    def download_raw_asset(self, assetId):
        with open(self._get_asset_path(assetId), 'rb') as infile:
            return infile.read()

    @cherrypy.expose
    def download_all_assets(self):
        zip_stream = io.BytesIO()
        assets_zip = zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED)
        for path in glob.glob(os.path.join(self._asset_path, '*.asset')):
            with open(path, 'rb') as infile:
                assets_zip.writestr(os.path.basename(path), infile.read())
        assets_zip.close()
        zip_stream.seek(0)
        return zip_stream.read()

