import importlib
from ..logic.logic import Logic
from ..patches.common.patches import patches, additional_PLMs
from ..utils.parameters import appDir
from ..utils.utils import listDir, exists

class PatchAccess(object):
    def __init__(self):
        # load all ips patches
        self.patchesPath = {}
        commonDir = "/".join((appDir, 'worlds/sm/variaRandomizer/patches/common/ips'))
        for patch in listDir(commonDir):
            self.patchesPath[patch] = commonDir
        logicDir = "/".join((appDir, 'worlds/sm/variaRandomizer/patches/{}/ips'.format(Logic.patches)))
        for patch in listDir(logicDir):
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
            if exists(patch):
                return patch
            else:
                raise Exception("unknown patch: {}".format(patch))

    def getDictPatches(self):
        return self.dictPatches

    def getAdditionalPLMs(self):
        return self.additionalPLMs
