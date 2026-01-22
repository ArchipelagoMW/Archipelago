import json
import timeit

from worlds.factorio_bobs.packDevUtils import get_modpack


def main():
    modpack = get_modpack()

    start = timeit.default_timer()
    output = {}
    for item in modpack.recipe_engine.game_items.values():
        item.raw_calculate()
        if not item.is_valid:
            continue
        output[item.name] = {"score": item.score,
                        "best_recipe": best.name if best else None,
                        "technologies": list(sorted(technology.name for technology in tech)),
                        "category": list(sorted(cat))}
    return
    path = modpack._BaseModpack__root / "Cache/precalc.json"
    json.dump(output, open(path, "w"), indent=4, sort_keys=True)
    print(f"Done in {(timeit.default_timer() - start):.2f} seconds")


if __name__ == '__main__':
    main()
