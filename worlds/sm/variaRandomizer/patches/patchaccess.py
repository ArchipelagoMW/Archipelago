import os, importlib
import pathlib
import sys
import zipfile
from ..logic.logic import Logic
from ..patches.common.patches import patches, additional_PLMs
from ..utils.parameters import appDir

def ListDir(resource: str):
    filename = sys.modules[PatchAccess.__module__].__file__
    apworldExt = ".apworld"
    game = "sm/"
    if apworldExt in filename:
        zipPath = pathlib.Path(filename[:filename.index(apworldExt) + len(apworldExt)])
        with zipfile.ZipFile(zipPath) as zf:
            zipFilePath = resource[resource.index(game):]
            path = zipfile.Path(zf, zipFilePath + "/")
            files = [f.at[len(zipFilePath)+1:] for f in path.iterdir()]
            print(zipFilePath)
            #files = list(set(f for f in zf.namelist() if f.startswith(zipFilePath) and f.count("/") == zipFilePath.count("/")))
            print(files)
            return files
    else:
        return os.listdir(resource)    
    
def Exists(resource: str):
    filename = sys.modules[PatchAccess.__module__].__file__
    apworldExt = ".apworld"
    game = "sm/"
    if apworldExt in filename:
        zipPath = pathlib.Path(filename[:filename.index(apworldExt) + len(apworldExt)])
        with zipfile.ZipFile(zipPath) as zf:
            print(resource)
            if (game in resource):
                zipFilePath = resource[resource.index(game):]
                path = zipfile.Path(zf, zipFilePath)
                return path.exists()
            else:
                return False
    else:
        return os.path.exists(resource)   

class PatchAccess(object):
    def __init__(self):
        # load all ips patches
        self.patchesPath = {}
        commonDir = "/".join((str(appDir), 'worlds/sm/variaRandomizer/patches/common/ips'))
        for patch in ListDir(commonDir):
            self.patchesPath[patch] = commonDir
        logicDir = "/".join((str(appDir), 'worlds/sm/variaRandomizer/patches/{}/ips'.format(Logic.patches)))
        for patch in ListDir(logicDir):
            self.patchesPath[patch] = logicDir

        # load dict patches
        self.dictPatches = patches
        logicPatches = importlib.import_module("worlds.sm.variaRandomizer.patches.{}.patches".format(Logic.patches)).patches
        self.dictPatches.update(logicPatches)

        # load additional PLMs
        self.additionalPLMs = additional_PLMs
        logicPLMs = importlib.import_module("worlds.sm.variaRandomizer.patches.{}.patches".format(Logic.patches)).additional_PLMs
        self.additionalPLMs.update(logicPLMs)

    def getPatchPath(self, patch):
        # is patch preloaded
        if patch in self.patchesPath:
            return "/".join((self.patchesPath[patch], patch))
        else:
            # patchs from varia_repository used by the customizer for permalinks
            if Exists(patch):
                return patch
            else:
                raise Exception("unknown patch: {}".format(patch))

    def getDictPatches(self):
        return self.dictPatches

    def getAdditionalPLMs(self):
        return self.additionalPLMs
