    
from typing import Any, List
import copy
import Dialog
from yaml import load

class StringTable:

    @staticmethod
    def ParseEntries(resource: str):
        with open(resource, 'rb') as f:
            yaml = str(f.read(), "utf-8")
        content = load(yaml)

        result = []
        for entryKey, entryValue in content.items():
            if isinstance(entryValue, List):
                for b in entryValue:
                    result += bytearray(b)
            elif isinstance(entryValue, str):
                result.append(Dialog.Compiled(entryValue))
            elif isinstance(entryValue, dict):
                result.append(Dialog.Compiled(entryValue["NoPause"], False))
            else: raise Exception(f"Did not expect an object of type {type(entryValue)}")

    template: List[str, List[Any]] = ParseEntries.__func__("Text/Scripts/StringTable.yaml")
    entries: List[str, List[Any]] = copy.deepcopy(template)

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
        index = StringTable.entries.index(name)
        StringTable.entries[index] = (name, Dialog.Compiled(text))

    def GetPaddedBytes(self):
        return self.GetBytes(True)

    def GetBytes(pad = False):
        maxBytes = 0x7355
        data = []
        for entry in StringTable.entries:
            data += entry.bytes

        if (len(data) > maxBytes):
            raise Exception(f"String Table exceeds 0x{maxBytes:X} bytes")

        if (pad and len(data) < maxBytes):
            data += [0xFF] * (maxBytes - len(data))
        return data
