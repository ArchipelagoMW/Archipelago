# support for AP world
import io
import pathlib
import pkgutil
import sys

is_apworld = ".apworld" in sys.modules[__name__].__file__


def get_zip_file():
    filename = sys.modules[__name__].__file__
    apworld_ext = ".apworld"
    zip_path = pathlib.Path(filename[: filename.index(apworld_ext) + len(apworld_ext)])
    return pkgutil.get_data(__name__, zip_path)


def open_file(resource: str, mode: str = "r", encoding: None = None):
    if is_apworld:
        (zip_file, stem) = get_zip_file()
        with zip_file as zf:
            zip_file_path = resource[resource.index(stem + "/") :]
            if mode == "rb":
                return zf.open(zip_file_path, "r")
            else:
                return io.TextIOWrapper(zf.open(zip_file_path, mode), encoding)
    else:
        return open(resource, mode)
