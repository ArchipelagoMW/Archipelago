from ..data.party_battle_script import PartyBattleScript
from ..data.structures import DataArray

class PartyBattleScripts:
    DATA_START = 0x10fd00
    DATA_END = 0x10ffff

    def __init__(self, rom, args, characters):
        self.rom = rom
        self.args = args
        self.characters = characters

        self.party_script_data = DataArray(self.rom, self.DATA_START, self.DATA_END, PartyBattleScript.DATA_SIZE)

        self.scripts = []
        for script_index in range(len(self.party_script_data)):
            script = PartyBattleScript(script_index, self.party_script_data[script_index])
            self.scripts.append(script)

    def __len__(self):
        return len(self.scripts)

    def imperial_camp_cyan_mod(self):
        # remove uncontrollable cyan from imperial camp battles
        # his character slot is unavailable with 4 party members

        battle_indices = [5, 6] # 3 battles, 2 unique
        for index in battle_indices:
            self.scripts[index].character_scripts[0].delete()

    def leap_char_mod(self):
        self.leap_char = self.characters.get_characters_with_command("Leap")
        if not self.leap_char:
            self.leap_char = self.characters.GAU
        else:
            self.leap_char = self.leap_char[0]

        gau_veldt_appear_index = 10
        self.scripts[gau_veldt_appear_index].character_scripts[0].character = self.leap_char
        self.scripts[gau_veldt_appear_index].character_scripts[0].sprite = self.leap_char

    def mod(self):
        self.imperial_camp_cyan_mod()
        self.leap_char_mod()

    def print(self):
        for script in self.scripts:
            script.print()

    def write(self):
        for script_index in range(len(self.scripts)):
            self.party_script_data[script_index] = self.scripts[script_index].data()

        self.party_script_data.write()
