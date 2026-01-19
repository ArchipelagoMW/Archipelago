import sys
import timeit
from pathlib import Path

from worlds.factorio_bobs.packDevUtils import get_modpack

import json

def main():
    modpack = get_modpack()

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
