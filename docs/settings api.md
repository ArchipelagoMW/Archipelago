# Archipelago Settings API

The settings API describes how to use installation-wide config and let the user configure them, like paths, etc. using
host.yaml. For the player options / player yamls see [options api.md](options api.md).

The settings API replaces `Utils.get_options()` and `Utils.get_default_options()`
as well as the predefined `host.yaml` in the repository.

For backwards compatibility with APWorlds, some interfaces are kept for now and will produce a warning when being used.


## Config File

Settings use options.yaml (manual override), if that exists, or host.yaml (the default) otherwise.
The files are searched for in the current working directory, if different from install directory, and in `user_path`,
which either points to the installation directory, if writable, or to %home%/Archipelago otherwise.

**Examples:**
* C:\Program Data\Archipelago\options.yaml
* C:\Program Data\Archipelago\host.yaml
* path\to\code\repository\host.yaml
* ~/Archipelago/host.yaml

Using the settings API, AP can update the config file or create a new one with default values and comments, 
if it does not exist.


## Global Settings

All non-world-specific settings are defined directly in settings.py.
Each value needs to have a default. If the default should be `None`, annotate it using `T | None = None`.

To access a "global" config value, with correct typing, use one of
```python
from settings import get_settings, GeneralOptions, FolderPath
from typing import cast

x = get_settings().general_options.output_path
y = cast(GeneralOptions, get_settings()["general_options"]).output_path
z = cast(FolderPath, get_settings()["general_options"]["output_path"])
```


## World Settings

Worlds can define the top level key to use by defining `settings_key: ClassVar[str]` in their World class.
It defaults to `{folder_name}_options` if undefined, i.e. `worlds/factorio/...` defaults to `factorio_options`.

Worlds define the layout of their config section using type annotation of the variable `settings` in the class.
The type has to inherit from `settings.Group`. Each value in the config can have a comment by subclassing a built-in
type. Some helper types are defined in `settings.py`, see [Types](#Types) for a list.```

Inside the class code, you can then simply use `self.settings.rom_file` to get the value.
In case of paths they will automatically be read as absolute file paths. No need to use user_path or local_path.

```python
import settings
from worlds.AutoWorld import World


class MyGameSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """Description that is put into host.yaml"""
        description = "My Game US v1.0 ROM File"  # displayed in the file browser
        copy_to = "MyGame.sfc"  # instead of storing the path, copy to AP dir
        md5s = ["..."]

    rom_file: RomFile = RomFile("MyGame.sfc")  # definition and default value


class MyGameWorld(World):
    ...
    settings: MyGameSettings
    ...

    def something(self):
        pass  # use self.settings.rom_file here
```


## Types

When writing the host.yaml, the code will down cast the values to builtins.
When reading the host.yaml, the code will upcast the values to what is defined in the type annotations.
E.g. an IntEnum becomes int when saving and will construct the IntEnum when loading.

Types that can not be down cast to / up cast from a builtin can not be used except for Group, which will be converted
to/from a dict.
`bool` is a special case, see settings.py: ServerOptions.disable_item_cheat for an example.

Below are some predefined types that can be used if they match your requirements:


### Group

A section / dict in the config file. Behaves similar to a dataclass.
Type annotation and default assignment define how loading, saving and default values behave.
It can be accessed using attributes or as a dict: `group["a"]` is equivalent to `group.a`.

In worlds, this should only be used for the top level to avoid issues when upgrading/migrating.


### Bool

Since `bool` can not be subclassed, use the `settings.Bool` helper in a union to get a comment in host.yaml.

```python
import settings

class MySettings(settings.Group):
    class MyBool(settings.Bool):
        """Doc string"""

    my_value: MyBool | bool = True
```

### UserFilePath

Path to a single file. Automatically resolves as user_path:
Source folder or AP install path on Windows. ~/Archipelago for the AppImage.
Will open a file browser if the file is missing when in GUI mode.

If the file is used in the world's `generate_output`, make sure to add a `stage_assert_generate` that checks if the
file is available, otherwise generation may fail at the very end.
See also [world api.md](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#generation).

#### class method validate(cls, path: str)

Override this and raise ValueError if validation fails.
Checks the file against [md5s](#md5s) by default.

#### is_exe: bool

Resolves to an executable (varying file extension based on platform)

#### description: str | None

Human-readable name to use in file browser

#### copy_to: str | None

Instead of storing the path, copy the file.

#### md5s: list[str | bytes]

Provide md5 hashes as hex digests or raw bytes for automatic validation.


### UserFolderPath

Same as [UserFilePath](#UserFilePath), but for a folder instead of a file.


### LocalFilePath

Same as [UserFilePath](#UserFilePath), but resolves as local_path:
path inside the AP dir or Appimage even if read-only.


### LocalFolderPath

Same as [LocalFilePath](#LocalFilePath), but for a folder instead of a file.


### OptionalUserFilePath, OptionalUserFolderPath, OptionalLocalFilePath, OptionalLocalFolderPath

Same as UserFilePath, UserFolderPath, LocalFilePath, LocalFolderPath but does not open a file browser if missing.


### SNESRomPath

Specialized [UserFilePath](#UserFilePath) that ignores an optional 512 byte header when validating.


## Caveats

### Circular Imports

Because the settings are defined on import, code that runs on import can not use settings since that would result in
circular / partial imports. Instead, the code should fetch from settings on demand during generation.

"Global" settings are populated immediately, while worlds settings are lazy loaded, so if really necessary,
"global" settings could be used in global scope of worlds.
