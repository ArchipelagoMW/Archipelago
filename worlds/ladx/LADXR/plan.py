

# Helper class to read and store planomizer data
class Plan:
    def __init__(self, filename):
        self.forced_items = {}
        self.item_pool = {}
        item_group = {}

        for line in open(filename, "rt"):
            line = line.strip()
            if ";" in line:
                line = line[:line.find(";")]
            if "#" in line:
                line = line[:line.find("#")]
            if ":" not in line:
                continue
            entry_type, params = map(str.strip, line.upper().split(":", 1))

            if entry_type == "LOCATION" and ":" in params:
                location, item = map(str.strip, params.split(":", 1))
                if item == "":
                    continue
                if item.startswith("[") and item.endswith("]"):
                    item = item_group[item[1:-1]]
                if "," in item:
                    item = list(map(str.strip, item.split(",")))
                self.forced_items[location] = item
            elif entry_type == "POOL" and ":" in params:
                item, count = map(str.strip, params.split(":", 1))
                self.item_pool[item] = self.item_pool.get(item, 0) + int(count)
            elif entry_type == "GROUP" and ":" in params:
                name, item = map(str.strip, params.split(":", 1))
                if item == "":
                    continue
                if "," in item:
                    item = list(map(str.strip, item.split(",")))
                item_group[name] = item
