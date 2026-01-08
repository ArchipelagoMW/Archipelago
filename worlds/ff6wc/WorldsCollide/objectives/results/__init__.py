results = {}
def __init__():
    import os
    import pkgutil
    import importlib
    for module_file in pkgutil.iter_modules([os.path.dirname(__file__)]):
        if module_file.name[0] == '_':
            continue
        module_name = module_file.name
        module = importlib.import_module("." + module_name, "worlds.ff6wc.WorldsCollide.objectives.results")
        results[module.Result.NAME] = module.Result
__init__()
