import os


def pytest_configure(config):
    # AP_TEST_WORLDS implies `-m world` unless an explicit -m was given; the scoping itself lives in
    # worlds/__init__
    if os.environ.get("AP_TEST_WORLDS") and not config.option.markexpr:
        config.option.markexpr = "world"


def pytest_ignore_collect(collection_path, config):
    # skip worlds/<world>/... for any world not named, so other worlds are never imported
    env = os.environ.get("AP_TEST_WORLDS")
    if not env:
        return None
    selected = {name.strip() for name in env.split(",") if name.strip()}
    parts = collection_path.parts
    if "worlds" in parts:
        i = parts.index("worlds")
        if i + 1 < len(parts) and parts[i + 1] not in selected:
            return True
    return None


def pytest_collection_modifyitems(items):
    # mark for `-m world`: classes with `world_relevant = True`, plus anything under worlds/ (nodeid is
    # always "/"-separated and relative to rootdir)
    for item in items:
        if getattr(getattr(item, "cls", None), "world_relevant", False) or \
                item.nodeid.split("/", 1)[0] == "worlds":
            item.add_marker("world")
