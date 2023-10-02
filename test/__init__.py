import pathlib
import warnings

import settings

warnings.simplefilter("always")
settings.no_gui = True
settings.skip_autosave = True

import ModuleUpdate

ModuleUpdate.update_ran = True  # don't upgrade

import Utils

Utils.local_path.cached_path = pathlib.Path(__file__).parent.parent
Utils.user_path()  # initialize cached_path
