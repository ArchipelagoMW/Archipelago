# support for AP world
import pathlib
import sys
import zipfile
import io

isAPWorld = ".apworld" in sys.modules[__name__].__file__


def getZipFile():
    filename = sys.modules[__name__].__file__
    apworldExt = ".apworld"
    zipPath = pathlib.Path(filename[:filename.index(apworldExt) + len(apworldExt)])
    return (zipfile.ZipFile(zipPath), zipPath.stem)


def openFile(resource: str, mode: str = "r", encoding: None = None):
    if isAPWorld:
        (zipFile, stem) = getZipFile()
        with zipFile as zf:
            zipFilePath = resource[resource.index(stem + "/"):]
            if mode == 'rb':
                return zf.open(zipFilePath, 'r')
            else:
                return io.TextIOWrapper(zf.open(zipFilePath, mode), encoding)
    else:
        return open(resource, mode)