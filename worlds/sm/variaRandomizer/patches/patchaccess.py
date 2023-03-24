import os, importlib
from logic.logic import Logic
from patches.common.patches import patches, additional_PLMs
from utils.parameters import appDir
from patches.vanilla.patches import patches as logicPatches
from patches.vanilla.patches import additional_PLMs as logicPLMs

class PatchAccess(object):
    def __init__(self):
        # load all ips patches
        self.patchesPath = {}
        commonDir = os.path.join(appDir, 'worlds/sm/variaRandomizer/patches/common/ips/')
        for patch in os.listdir(commonDir):
            self.patchesPath[patch] = commonDir
        logicDir = os.path.join(appDir, 'worlds/sm/variaRandomizer/patches/{}/ips/'.format(Logic.patches))
        for patch in os.listdir(logicDir):
            self.patchesPath[patch] = logicDir

        # load dict patches
        self.dictPatches = patches
        # seems broken with cx_freeze
        # not required until Rotation hack is added
        #logicPatches = importlib.import_module("patches.{}.patches".format(Logic.patches)).patches
        self.dictPatches.update(logicPatches)

        # load additional PLMs
        self.additionalPLMs = additional_PLMs
        # seems broken with cx_freeze
        # not required until Rotation hack is added
        # logicPLMs = importlib.import_module("patches.{}.patches".format(Logic.patches)).additional_PLMs
        self.additionalPLMs.update(logicPLMs)

    def getPatchPath(self, patch):
        # is patch preloaded
        if patch in self.patchesPath:
            return os.path.join(self.patchesPath[patch], patch)
        else:
            # patchs from varia_repository used by the customizer for permalinks
            if os.path.exists(patch):
                return patch
            else:
                raise Exception("unknown patch: {}".format(patch))

    def getDictPatches(self):
        return self.dictPatches

    def getAdditionalPLMs(self):
        return self.additionalPLMs
