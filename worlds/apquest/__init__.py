# The first thing you should make for your world is an archipelago.json manifest file.
# You can reference APQuest's, but you should change the "game" field (obviously),
# and you should also change the "minimum_ap_version" - probably to the current value of Utils.__version__.

# Apart from the regular apworld code that allows generating multiworld seeds with your game,
# your apworld might have other "components" that should be launchable from the Archipelago Launcher.
# You can ignore this for now. If you are specifically interested in components, you can read components.py.
from . import components as components

# The main thing we do in our __init__.py is importing our World and WebWorld classes
# from our world.py and web_world.py to initialize them.
# Obviously,these classes needs to exist first. For this, read world.py and web_world.py.
from .world import APQuestWorld as APQuestWorld
from .web_world import APQuestWebWorld as APQuestWebWorld
