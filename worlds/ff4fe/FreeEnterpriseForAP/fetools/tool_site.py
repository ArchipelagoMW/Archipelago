import os
import argparse

import cherrypy
import jinja2
import dotenv

from z_tools import ZToolSite
from harp_tools import HarpToolSite
from rescript_tools import RescripterSite

class ToolSite:
    def __init__(self):
        self._env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'template')),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            )
        self.z = ZToolSite(self._env,
            title = 'Z Sprites',
            asset_path = os.path.join(os.path.dirname(__file__), 'assets', 'z')
            )
        self.harp = HarpToolSite(self._env,
            title = 'Harp Songs',
            asset_path = os.path.join(os.path.dirname(__file__), 'assets', 'harp')
            )
        self.rescript = RescripterSite(self._env)

    @cherrypy.expose
    def index(self):
        return self._env.get_template('home.html').render()

if __name__ == '__main__':
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('rom')
    args = parser.parse_args()

    with open(args.rom, 'rb') as infile:
        rom_data = infile.read()

    conf = {
        '/static' : {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
        },
        'fetools' : {
            'rom' : rom_data
        }
    }

    cherrypy.config.update({'server.socket_port' : 8082})

    website = ToolSite()
    cherrypy.quickstart(website, '', conf)
