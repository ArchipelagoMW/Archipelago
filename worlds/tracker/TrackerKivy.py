from kvui import ImageLoaderPkgutil
from kivy.core.image import ImageData


def load(self, filename: str) -> list[ImageData]:
    import re

    filename = filename[7:]
    print(filename)
    parentPath, childPath = filename.split("zip/", 1)
    childPath = re.sub(r"^\/*", "", childPath)
    import zipfile
    with zipfile.ZipFile(parentPath+"zip") as parentSource:
        with parentSource.open(childPath) as childSource:
            return self._bytes_to_data(childSource.read())


# grab the default loader method so we can override it but use it as a fallback
_original_image_loader_load = ImageLoaderPkgutil.load


def load_override(self, filename: str, default_load=_original_image_loader_load, **kwargs):
    if filename.startswith("ap:zip:"):
        return load(self, filename)
    else:
        return default_load(self, filename, **kwargs)


ImageLoaderPkgutil.load = load_override


def SomethingNeatJustToMakePythonHappy():
    pass
