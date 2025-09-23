# APContainer

An APContainer is a zip file holding data or code that somehow extends Archipelago.
The main use currently is for patch files to be read by game clients.  
In the future, [apworlds](apworld%20specification.md) may become a type of APContainer as well.

An APContainer is read by a subclass of the APContainer class in [Files.py](../worlds/Files.py).  
This class also has a function to write the APContainer zip file, and this is usually how APContainers are created.

Here's a quick overview of the functions of the APContainer class:

```py
def write(self, file: str | BinaryIO | None = None) -> None:
    """Top level function to write the APContainer to its zip file.
    Should usually not be overwritten, instead overwrite write_contents."""
    ...

def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
    """Can be overwritten, but you must call super().write_contents if you do.
    Subclasses of APContainer such as APProcedurePatch may write other data by default as well,
    such as patch data files created during generation."""
    ...

def read(self, file: str | BinaryIO | None = None) -> None:
    """Top level function to read the APContainer zip file into the APContainer Python class instance.
    Should usually not be overwritten, instead overwrite read_contents."""
    ...

def read_contents(self, opened_zipfile: zipfile.ZipFile) -> dict[str, Any]:
    """Can be overwritten, but you must call super().read_contents() if you do.
    By default, returns the data from the archipelago.json manifest.
    Subclasses of APContainer such as APProcedurePatch may read and return other data by default as well,
    such as byte data of any other files that aren't archipelago.json."""
    ...

def get_manifest(self) -> dict[str, Any]:
    """Return the manifest data for writing archipelago.json when .write is called."""
    return {
        # minimum version of patch system expected for patching to be successful
        "compatible_version": 5,
        "version": container_version,  # Constant defined in Files.py that we update when the Container API changes
    }
```

## Specification

An APContainer must be a zip archive.  
This zip file can (and usually will) have a custom extension linking it to one specific purpose.

An APContainer must contain a manifest file called `archipelago.json`.

## Types of containers

In [Files.py](../worlds/Files.py), there are a lot of predefined subclasses of APContainer for specific purposes.  
Here, you will find a quick description of each one.

For more detailed descriptions of one specific APContainer type, please reference its documentation, if it exists.

### APPlayerContainer

An APPlayerContainer is an APContainer that is linked to one specific player in a multiworld.

The APPlayerContainer class itself has the following fields, both of which can optionally be overridden:
```py
game: ClassVar[Optional[str]] = None
patch_file_ending: str = ""
```

The manifest file of an APPlayerContainer must contain the following fields:

```py
player: int | None  # Can be None, but must be present
player_name: str
server: str  # Can be an empty string, but must be present
```

### APPatch

APPatch is a subclass of APPlayerContainer which represents a patch file for a slot in a multiworld.

It has the following additional field which defines the "procedure" that will be used to execute the patch:

```py
    procedure: Union[Literal["custom"], List[Tuple[str, List[Any]]]] = "custom"
```

You should subclass APPatch directly if your APContainer is a patch file, but it does not get patched automatically.

### APAutoPatchInterface

APAutoPatchInterface is a subclass of APPatch which represents a patch file that can be auto-patched.

APAutoPatchInterface is the first APContainer subclass that *must* define a unique `patch_file_ending`
that is not `.zip`.  
This patch file ending will be used to uniquely associate this container to its patch file type.

APAutoPatchInterface also has a `result_file_ending` field, which is the file ending of the resulting patch**ed** file.

An APAutoPatchInterface subclass must define a `patch` method:

```py
def patch(self, target: str) -> None:
    """ create the output file with the file name `target` """
```

Upon defining an APAutoPatchInterface subclass, there is one immediate effect:  
If Patch.py is launched with a patch file with the specified `patch_file_ending`,
an instance of your APAutoPatchInterface subclass will be created and its `patch` function will be called.

Furthermore, defining and APAutoPatchInterface subclass will allow the usage of `Patch.create_rom_file`.  
If you call this function with the patch file as the input, it will do the following:
1. Find your APAutoPatchInterface class automatically and create an instance of it (via its `__init__`)
2. Call this instance's `patch`
3. Grab the APPlayerContainer metadata (player, server, and player_name), **as long as** at any point during the
first two steps, `.read_contents()` was called
(if you have overridden `read_contents`, it has to call `super().read_contents()` for this to work).
4. Return the metadata, followed by the output file you created in `patch`.

With all of this in place, a client Component that was launched with a patch file can just call
`Patch.create_rom_file` with this patch file.  
This will retrieve the metadata to allow you to automatically connect the client to the Archipelago server,
and it will execute the patch, returning the location of the resulting patched file.

### APProcedurePatch

APProcedurePatch is a subclass of APAutoPatchInterface that implements the patching procedure protocol for roms.  
(Note: You can patch things that aren't roms, it's just become convention to call the patch infile a "rom")  
It must define at least one `procedure`, where `procedure` is a list of patching procedures to be applied to the rom.

Example:

```py
procedure = [
    ("apply_bsdiff4", ["mygame_basepatch.bsdiff4"]),
    ("apply_tokens", ["mygame_token_patch.bin"]),
    ("calc_snes_crc", [])
]
```

An APProcedurePatch also must implement a function `get_source_data` which gets the bytes of the base rom,
usually from the user's file system.

```py
@classmethod
def get_source_data(cls) -> bytes:
    """Get Base data"""
    ...
```

Finally, APProcedurePatch has a `hash` field that automatically gets written and read to the manifest of the
APProcedurePatch zip file.

#### Patching procedure

A patching procedure is a function on a subclass of `APPatchExtension` which performs a patch.
Aside from being passed the instance of APProcedurePatch that this procedure was called from,
a procedure function takes bytes as an input, and outputs bytes. Usually: Unpatched rom -> Patched rom.  
Many procedures also take a third arg, which points to a file in the APContainer zip file containing the "patch data",
usually written during [World.generate-output](world%20api.md#generate-output)
using the `write()` function of the APContainer/APProcedurePatch subclass.

This is what an AutoPatchExtension might look like:

```py
class MyGamePatchExtension(APPatchExtension):
    game: str = "My Game"

    @staticmethod
    def apply_mygame_patches(caller: APProcedurePatch, rom: bytes, patch_file_path: str) -> bytes:
        ...
```

If this class exists somewhere in your code, it will be registered in the `AutoPatchExtensionRegister`.  
Now, your subclass of APProcedurePatch can add this procedure to the list of procedures:

```py
class MyGameAPProcedurePatch(APProcedurePatch):
    game: str = "My Game"

    procedure = [
        ("apply_mygame_patches", ["mygamepatch.json"])
    ]
```

There are a few predefined procedures that you can make use of.  
Each of these warrants their own documentation, but a short description of each is:
1. "apply_bsdiff4" - For patching a rom file using a bsdiff4 delta patch.
2. "apply_tokens" - For patching a rom using a list of tokens. Crucially, this allows generation without a rom.
See [APTokenMixin](#APTokenMixin).
3. "calc_snes_crc" - Calculates and applies a valid CRC for an SNES rom header.

### APDeltaPatch

APDeltaPatch is a subclass of APProcedurePatch that simplifies the process of writing an APProcedurePatch based on a
bsdiff4 delta patch file:

```py
class MyGameDeltaPatch(APDeltaPatch):
    hash = MYGAME_HASH
    game: str = "My Game"
    patch_file_ending = ".apmygame"

    @classmethod
    def get_source_data(cls) -> bytes:
        ...
```

### APTokenMixin

APTokenMixin is a Mixin class for APProcedurePatch that simplifies the process of writing an APProcedurePatch using the
`apply_tokens` procedure.  
Mainly, it supplies the class with a few functions for writing the tokens in its `.write`.
(Further documentation needed)
