import sys
import timeit
from pathlib import Path


if __name__ == '__main__' and (__package__ is None or __package__ == ''):
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[2]

    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError: # Already removed
        pass

    import worlds.factorio_bobs
    __package__ = 'worlds.factorio_bobs'

import json

from .FactorioModpack import FactorioModpack
from .APModpackManager import modpacks

def main():
    modpack: FactorioModpack = modpacks["bob's"]
    modpack.init_items()
    modpack.init_locations()
    modpack.init_pack_check()

    start = timeit.default_timer()
    output = {}
    all_ingredients = modpack.recipe_engine.all_ingredients
    for name, item in all_ingredients.items():
        raw, best, tech, cat = item.eval()
        output[name] = {"raw_ingredients": {item.name: cost for item, cost in raw.items()},
                        "best_recipe": best.name if best else None,
                        "technologies": list(sorted(technology.name for technology in tech)),
                        "category": list(sorted(cat))}
    path = modpack._BaseModpack__root / "Cache/precalc.json"
    json.dump(output, open(path, "w"), indent=4, sort_keys=True)
    print(f"Done in {(timeit.default_timer() - start):.2f} seconds")


if __name__ == '__main__':
    main()
