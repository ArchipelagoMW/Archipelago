import base64
import re
import io
import os

import cherrypy

import f4c

'''
Base 64 encoding method that is compatible with browser JavaScript's atob for decoding
'''
def btoa(binary_data):
    encoded = base64.b64encode(binary_data, b'+/').decode('utf-8')
    encoded = re.sub(r'=*$', '', encoded)
    return encoded

def filesafe(name):
    return name.replace('?', '_').replace('/', '_')

def compile_test_rom(*scripts):
    rom = cherrypy.request.app.config['fetools']['rom']
    input_rom_stream = io.BytesIO(rom)
    output_rom_stream = io.BytesIO()
    build_report = f4c.compile(
        input_rom_stream, 
        output_rom_stream, 
        os.path.join(os.path.dirname(__file__), 'processors', 'default.consts.f4c'),
        *scripts)
    output_rom_stream.seek(0)
    return output_rom_stream.read()
