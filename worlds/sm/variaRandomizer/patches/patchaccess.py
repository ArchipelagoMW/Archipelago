import importlib

from ..logic.logic import Logic
from ..patches.common.patches import additional_PLMs, patches
from ..utils.parameters import appDir
from ..utils.utils import exists, listDir


class PatchAccess:
    def __init__(self):
        # load all ips patches
        self.patchesPath = {}
        commonDir = "/".join((appDir, "worlds/sm/variaRandomizer/patches/common/ips"))
        for patch in listDir(commonDir):
            self.patchesPath[patch] = commonDir
        logicDir = "/".join((appDir, f"worlds/sm/variaRandomizer/patches/{Logic.patches}/ips"))
        for patch in listDir(logicDir):
            self.patchesPath[patch] = logicDir

        # load dict patches
        self.dictPatches = patches
        logicPatches = importlib.import_module(f"worlds.sm.variaRandomizer.patches.{Logic.patches}.patches").patches
        self.dictPatches.update(logicPatches)

        # load additional PLMs
        self.additionalPLMs = additional_PLMs
        logicPLMs = importlib.import_module(f"worlds.sm.variaRandomizer.patches.{Logic.patches}.patches").additional_PLMs
        self.additionalPLMs.update(logicPLMs)

    def getPatchPath(self, patch):
        # is patch preloaded
        if patch in self.patchesPath:
            return "/".join((self.patchesPath[patch], patch))
        else:
            # patchs from varia_repository used by the customizer for permalinks
            if exists(patch):
                return patch
            else:
                raise Exception(f"unknown patch: {patch}")

    def getDictPatches(self):
        return self.dictPatches

    def getAdditionalPLMs(self):
        return self.additionalPLMs
