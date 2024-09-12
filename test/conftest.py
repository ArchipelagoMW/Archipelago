# Handle disabled worlds for pytest
from worlds.AutoWorld import AutoWorldRegister, Visibility, disabled_worlds
from worlds import failed_world_loads, world_sources
from Utils import local_path
from os.path import dirname, basename, join
from pytest import hookimpl
disabled_tests = []

for name, world in AutoWorldRegister.world_types.items():
    if world.visibility not in (Visibility.visible, Visibility.hidden):
        disabled_tests.append(dirname(world.__file__))

for world in disabled_worlds:
    disabled = dirname(world.replace(local_path(), ""))
    disabled_tests.append(disabled)

for source in world_sources:
    world_name = basename(source.path).rsplit(".", 1)[0]
    if world_name in failed_world_loads:
        disabled_tests.append(source.resolved_path)

print(disabled_tests)

@hookimpl
def pytest_collection_modifyitems(session, config, items):
    copy = items.copy()
    deselected = []
    for item in copy:
        if any(disabled in str(item.path) for disabled in disabled_tests):
            items.remove(item)
            deselected.append(item)
    config.hook.pytest_deselected(items=deselected)
