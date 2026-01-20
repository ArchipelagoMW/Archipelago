import json
import timeit

from worlds.factorio_bobs.packDevUtils import get_modpack


def main():
    modpack = get_modpack()

    start = timeit.default_timer()
    output = {}
    for item in modpack.recipe_engine.game_items.values():
        if not item.is_valid_ingredient:
            continue
        print(repr(item))
        if not item.is_valid_ingredient:
            continue
        continue
        output[name] = {"raw_ingredients": {item.name: cost for item, cost in raw.items()},
                        "best_recipe": best.name if best else None,
                        "technologies": list(sorted(technology.name for technology in tech)),
                        "category": list(sorted(cat))}
    return
    path = modpack._BaseModpack__root / "Cache/precalc.json"
    json.dump(output, open(path, "w"), indent=4, sort_keys=True)
    print(f"Done in {(timeit.default_timer() - start):.2f} seconds")


if __name__ == '__main__':
    main()
