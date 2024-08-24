import cherrypy
import traceback
import uuid
import io
import zipfile
import os

import rescripter
import util


class RescripterSite:
    def __init__(self, env):
        self._env = env
        self._jobs = {}

    @cherrypy.expose
    def index(self):
        return self._env.get_template('rescripter.html').render()

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    @cherrypy.tools.json_out()
    def setup(self, sourceRom, **kwargs):

        if sourceRom is None or sourceRom.file is None:
            raise cherrypy.HTTPError(400, "No source rom provided")
        
        zSprites = {}
        harpSongs = {}
        PREFIX_COLLECTION_PAIRS = [('zSprite', zSprites), ('harpSong', harpSongs)]

        for prefix, collection in PREFIX_COLLECTION_PAIRS:
            for i in range(4):
                fileParam = kwargs.get(f"{prefix}File{i}", None)
                if fileParam and fileParam.file:
                    label = kwargs.get(f"{prefix}Label{i}", '').strip()
                    if not label and not collection:
                        label = "___default"
                    elif not label or "___default" in collection:
                        raise cherrypy.HTTPError(400, f"Labels are required for all files when using multiple options for a sprite/song")
                    elif label in collection:
                        raise cherrypy.HTTPError(400, f"Duplicate label: {label}")

                    collection[label] = fileParam.file.read().decode('utf-8')

            if not collection:
                collection["___default"] = None

        combinations = []
        for zSpriteLabel in zSprites:
            for harpSongLabel in harpSongs:
                combo = {}
                label_parts = []
                if zSprites[zSpriteLabel] is not None:
                    if zSpriteLabel != '___default':
                        label_parts.append(zSpriteLabel)
                    combo['z'] = zSprites[zSpriteLabel]
                if harpSongs[harpSongLabel] is not None:
                    if harpSongLabel != '___default':
                        label_parts.append(harpSongLabel)
                    combo['harp'] = harpSongs[harpSongLabel]

                if 'z' in combo or 'harp' in combo:
                    combo['label'] = '_'.join(label_parts)
                    combinations.append(combo)

        if not combinations:
            raise cherrypy.HTTPError(400, f"No new scripts provided")

        source_rom_data = sourceRom.file.read()

        job_id = str(uuid.uuid4())
        self._jobs[job_id] = {
            'source_rom_data' : source_rom_data,
            'source_rom_filename' : os.path.basename(sourceRom.filename),
            'combinations' : combinations
            }

        return { "job" : job_id }

    @cherrypy.expose
    def run(self, job):
        if job not in self._jobs:
            raise cherrypy.HTTPError(400, "Job not found")

        cherrypy.response.headers['Content-Type'] = 'text/event-stream'

        job_data = self._jobs[job]
        del self._jobs[job]

        vanilla_rom_data = cherrypy.request.app.config['fetools']['rom']
        def generator():
            LOG_EVENT = "event: log\ndata: {}\n\n"

            try:
                zip_buffer = io.BytesIO()
                output_zip = zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED)

                for combo in job_data['combinations']:
                    yield LOG_EVENT.format(f"Processing {combo['label']}...")
                    
                    rescripted_rom = rescripter.rescript(
                        vanilla_rom_data,
                        job_data['source_rom_data'],
                        zSpriteScript = combo.get('z', None),
                        harpSongScript = combo.get('harp', None)
                        )

                    file_prefix, file_extension = os.path.splitext(job_data['source_rom_filename'])
                    if combo.get('label', ''):
                        file_prefix += '.' + combo['label']
                    else:
                        file_prefix += '.rescript'

                    filename = file_prefix + file_extension
                    output_zip.writestr(filename, rescripted_rom)

                output_zip.close()
                zip_buffer.seek(0)
                encoded_zip = util.btoa(zip_buffer.read())
                yield f"event: download\ndata: {encoded_zip}\n\n"

            except:
                lines = traceback.format_exc().split('\n')
                print('\n'.join(lines))
                lines = [f"data: {line}" for line in lines]
                yield "event: log\n" + "\n".join(lines) + "\n\n"

            yield f"event: done\ndata: \n\n"

        return generator()

    run._cp_config = {'response.stream': True}
