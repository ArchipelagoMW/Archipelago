    
from typing import Any, List
import copy
from ..Text.Dialog import Dialog
from ..Text.Texts import openFile
from Utils import unsafe_parse_yaml

class StringTable:

    @staticmethod
    def ParseEntries(resource: str):
        with openFile(resource, 'rb') as f:
            yaml = str(f.read(), "utf-8")
        content = unsafe_parse_yaml(yaml)

        result = []
        for entryValue in content:
            (key, value) = next(iter(entryValue.items()))
            if isinstance(value, List):
                result.append((key, value))
            elif isinstance(value, str):
                result.append((key, Dialog.Compiled(value)))
            else: raise Exception(f"Did not expect an object of type {type(value)}")
        return result

    template = ParseEntries.__func__("smz3/TotalSMZ3/Text/Scripts/StringTable.yaml")

    def __init__(self):
        self.entries = copy.deepcopy(StringTable.template)

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
        self.SetText("ganon_phase_3_no_silvers", text)
        self.SetText("ganon_phase_3_no_silvers_alt", text)

    def SetTriforceRoomText(self, text: str):
        self.SetText("end_triforce", f"{{NOBORDER}}\n{text}")

    def SetPedestalText(self, text: str):
        self.SetText("mastersword_pedestal_translated", text)

    def SetEtherText(self, text: str):
        self.SetText("tablet_ether_book", text)

    def SetBombosText(self, text: str):
        self.SetText("tablet_bombos_book", text)

    def SetTowerRequirementText(self, text: str):
        self.SetText("sign_ganons_tower", text)

    def SetGanonRequirementText(self, text: str):
        self.SetText("sign_ganon", text)

    def SetText(self, name: str, text: str):
        count = 0
        for key, value in self.entries:
            if (key == name):
                index = count
                break
            else:
                count += 1
        self.entries[index] = (name, Dialog.Compiled(text))

    def GetPaddedBytes(self):
        return self.GetBytes(True)

    def GetBytes(self, pad = False):
        maxBytes = 0x7355
        data = []
        for entry in self.entries:
            data += entry[1]

        if (len(data) > maxBytes):
            raise Exception(f"String Table exceeds 0x{maxBytes:X} bytes")

        if (pad and len(data) < maxBytes):
            data += [0xFF] * (maxBytes - len(data))
        return data
