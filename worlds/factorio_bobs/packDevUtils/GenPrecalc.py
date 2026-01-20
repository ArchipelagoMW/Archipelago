import json
import timeit

from worlds.factorio_bobs.packDevUtils import get_modpack


def main():
    modpack = get_modpack()

    start = timeit.default_timer()
    output = {}
    all_ingredients = set(modpack.recipe_engine.valid_ingredients.keys()) - modpack.recipe_engine.invalid_ingredients
    for name in all_ingredients:
        item = modpack.recipe_engine.all_ingredients[name]
        raw, best, tech, cat = item.eval()
        if not cat:
            print(f"{name}: {raw[item]}")
        output[name] = {"raw_ingredients": {item.name: cost for item, cost in raw.items()},
                        "best_recipe": best.name if best else None,
                        "technologies": list(sorted(technology.name for technology in tech)),
                        "category": list(sorted(cat))}
    path = modpack._BaseModpack__root / "Cache/precalc.json"
    json.dump(output, open(path, "w"), indent=4, sort_keys=True)
    print(f"Done in {(timeit.default_timer() - start):.2f} seconds")


if __name__ == '__main__':
    main()
