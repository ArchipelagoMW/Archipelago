import json
import string
import timeit

from worlds.factorio_bobs.packDevUtils import get_modpack


def main():
    modpack = get_modpack()
    start = timeit.default_timer()
    
    tech_table = modpack.technology_table
    # progressive technologies
    # auto-progressive
    progressive_rows: dict[str, list[str] | tuple[str, ...]] = {}
    progressive_incs = set()
    for tech_name in tech_table:
        if tech_name.endswith("-1"):
            progressive_rows[tech_name] = []
        elif tech_name[-2] == "-" and tech_name[-1] in string.digits:
            progressive_incs.add(tech_name)

    for root, progressive in progressive_rows.items():
        seeking = root[:-1] + str(int(root[-1]) + 1)
        while seeking in progressive_incs:
            progressive.append(seeking)
            progressive_incs.remove(seeking)
            seeking = seeking[:-1] + str(int(seeking[-1]) + 1)

    # make root entry the progressive name
    for old_name in set(progressive_rows):
        prog_name = "progressive-" + old_name.rsplit("-", 1)[0]
        progressive_rows[prog_name] = tuple([old_name] + progressive_rows[old_name])
        del (progressive_rows[old_name])

    # no -1 start
    base_starts = set()
    for remnant in progressive_incs:
        if remnant[-1] == "2":
            base_starts.add(remnant[:-2])

    for root in base_starts:
        if root not in tech_table:
            root = root.replace("bob-", "")

        if root in tech_table:
            seeking = root + "-2"
            progressive = [root]
            while seeking in progressive_incs:
                progressive.append(seeking)
                progressive_incs.remove(seeking)
                seeking = seeking[:-1] + str(int(seeking[-1]) + 1)
            seeking = "bob-" + seeking
            while seeking in progressive_incs:
                progressive.append(seeking)
                progressive_incs.remove(seeking)
                seeking = seeking[:-1] + str(int(seeking[-1]) + 1)
            progressive_rows["progressive-" + root] = tuple(progressive)


    path = modpack._BaseModpack__root / "Cache/precalc.json"
    json.dump(progressive_rows, open(path, "w"), indent=4, sort_keys=True)
    print(f"Done in {(timeit.default_timer() - start):.2f} seconds")


if __name__ == '__main__':
    main()
