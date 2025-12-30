import pkgutil

from Utils import parse_yaml

from .definitions_types import AutopelagoDefinitions

GAME_NAME = "Autopelago"
defs: AutopelagoDefinitions = parse_yaml(pkgutil.get_data(__name__, "AutopelagoDefinitions.yml"))


def gen_ids():
    next_id = 1
    while True:
        yield next_id
        next_id += 1
