import re

from . import compile_common
from . import lark

_hints = {}

class HintsProcessor(lark.Transformer):
    def event_map_hint(self, pair):
        event_id,map_id = pair
        _hints.setdefault('event map', {})[event_id] = map_id
        return None

def load_file(filename):
    with open(filename, 'r') as infile:
        lines = infile.read().split('\n')
    
    lines = [re.sub(r'//.*$', '', l) for l in lines]
    tree = compile_common.parse('\n'.join(lines), 'hints', 'start')

    HintsProcessor().transform(tree)

def get_event_map(event_id):
    try:
        return _hints['event map'][event_id]
    except KeyError:
        return None

