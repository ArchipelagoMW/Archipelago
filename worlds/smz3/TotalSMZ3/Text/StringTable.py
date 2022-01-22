    
from typing import Any, List
import copy
from worlds.smz3.TotalSMZ3.Text.Dialog import Dialog
from yaml import load, Loader
import Utils

class StringTable:

    @staticmethod
    def ParseEntries(resource: str):
        with open(resource, 'rb') as f:
            yaml = str(f.read(), "utf-8")
        content = load(yaml, Loader)

        result = []
        for entryValue in content:
            (key, value) = next(iter(entryValue.items()))
            if isinstance(value, List):
                result.append((key, value))
            elif isinstance(value, str):
                result.append((key, Dialog.Compiled(value)))
            elif isinstance(value, dict):
                result.append((key, Dialog.Compiled(value["NoPause"], False)))
            else: raise Exception(f"Did not expect an object of type {type(value)}")
        return result

    template = ParseEntries.__func__(("lib/" if Utils.is_frozen() else "") + "worlds/smz3/TotalSMZ3/Text/Scripts/StringTable.yaml")
    entries = copy.deepcopy(template)

    def SetSahasrahlaRevealText(self, text: str):
        self.SetText("sahasrahla_quest_information", text)

    def SetBombShopRevealText(self, text: str):
        self.SetText("bomb_shop", text)

    def SetBlindText(self, text: str):
        self.SetText("blind_by_the_light", text)

    def SetTavernManText(self, text: str):
        self.SetText("kakariko_tavern_fisherman", text)

    def SetGanonFirstPhaseText(self, text: str):
        self.SetText("ganon_fall_in", text)

    def SetGanonThirdPhaseText(self, text: str):
        self.SetText("ganon_phase_3", text)

    def SetTriforceRoomText(self, text: str):
        self.SetText("end_triforce", "{NOBORDER}\n" + text)

    def SetPedestalText(self, text: str):
        self.SetText("mastersword_pedestal_translated", text)

    def SetEtherText(self, text: str):
        self.SetText("tablet_ether_book", text)

    def SetBombosText(self, text: str):
        self.SetText("tablet_bombos_book", text)

    def SetText(self, name: str, text: str):
        count = 0
        for key, value in StringTable.entries:
            if (key == name):
                index = count
                break
            else:
                count += 1
        StringTable.entries[index] = (name, Dialog.Compiled(text))

    def GetPaddedBytes(self):
        return self.GetBytes(True)

    def GetBytes(self, pad = False):
        maxBytes = 0x7355
        data = []
        for entry in StringTable.entries:
            data += entry[1]

        if (len(data) > maxBytes):
            raise Exception(f"String Table exceeds 0x{maxBytes:X} bytes")

        if (pad and len(data) < maxBytes):
            data += [0xFF] * (maxBytes - len(data))
        return data
