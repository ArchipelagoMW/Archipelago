import pathlib
import os
import warnings

import settings

warnings.simplefilter("always")
warnings.filterwarnings(action="ignore", category=DeprecationWarning, module="s2clientprotocol")
settings.no_gui = True
settings.skip_autosave = True
os.environ.setdefault("SKIP_PYTHON_VERSION_CHECK", "1")

import ModuleUpdate

ModuleUpdate.update_ran = True  # don't upgrade

import Utils

file_path = pathlib.Path(__file__).parent.parent
Utils.local_path.cached_path = file_path
Utils.user_path()  # initialize cached_path
