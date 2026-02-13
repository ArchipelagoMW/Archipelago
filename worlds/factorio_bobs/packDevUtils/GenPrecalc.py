import json
import timeit
import datetime
from pathlib import Path

from worlds.factorio_bobs.RecipeEngine import RecipeEngine

RecipeEngine.invalidate_cache = True

from worlds.factorio_bobs.packDevUtils import get_modpack


def main():
    modpack = get_modpack()

    start = timeit.default_timer()
    output = {}
    amount = len(modpack.recipe_engine.game_items)
    done = 0
    mean_time = 0
    for item in modpack.recipe_engine.game_items.values():
        item_timer = timeit.default_timer()
        print(f"Calculating: {item}")
        item.raw_calculate()
        if not item.is_valid:
            output[item.name] = {"invalid": True}
        else:
            output[item.name] = {"score": item.score,
                                 "recipes": [recipe.name for recipe in item.best_recipes]}
        item_done_in = timeit.default_timer() - item_timer
        mean_time = (mean_time * done + item_done_in) / (done+1)
        done += 1
        print(f"{done*100/amount:.2f}%, elapsed time: {datetime.timedelta(seconds=item_done_in)}, estimated time: {datetime.timedelta(seconds=mean_time*(amount-done))}")
        print(f"{item}: {output[item.name]}")

    path: Path = modpack._BaseModpack__root / "Cache/precalc.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(output, open(path, "w"), indent=4, sort_keys=True)
    print(f"Done in {datetime.timedelta(seconds=(timeit.default_timer() - start))} seconds")


if __name__ == '__main__':
    main()
