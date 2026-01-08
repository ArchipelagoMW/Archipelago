class CharacterBattleScript:
    DATA_SIZE = 5
    BATTLE_SCRIPT_OFFSET = 256

    def __init__(self, id, data):
        self.id = id

        self._character     = (data[0] & 0x3f) >> 0
        self.flip           = (data[0] & 0x40) >> 6
        self.hide           = (data[0] & 0x80) >> 7

        self.sprite         = data[1]
        self._battle_script = data[2] # (script index - 256)
        self.x              = data[3]
        self.y              = data[4]

    def data(self):
        data = [0x00] * self.DATA_SIZE

        data[0]  = self._character  << 0
        data[0] |= self.flip        << 6
        data[0] |= self.hide        << 7

        data[1]  = self.sprite
        data[2]  = self._battle_script
        data[3]  = self.x
        data[4]  = self.y

        return data

    @property
    def character(self):
        return self._character

    @character.setter
    def character(self, value):
        self._character = value & 0x3f

    @property
    def battle_script(self):
        return self._battle_script + self.BATTLE_SCRIPT_OFFSET

    @battle_script.setter
    def battle_script(self, value):
        self._battle_script = value - self.BATTLE_SCRIPT_OFFSET

    def delete(self):
        self.character = 0x3f
        self.flip = 1
        self.hide = 1
        self.sprite = 0xff
        self.battle_script = 0x1ff
        self.x = 255
        self.y = 255

    def __str__(self):
        return f"{self.id}: character {self.character}, sprite {self.sprite}, flip {self.flip}, hide {self.hide}, x {self.x}, y {self.y}, battle script {self.battle_script}"

class PartyBattleScript:
    DATA_SIZE = 24

    PARTY_SIZE = 4
    CHARACTER_DATA_START = 4

    def __init__(self, id, data):
        self.id = id

        self.hide_names = (data[0] & 0x7f) >> 0
        self.hide_party = (data[0] & 0x80) >> 7
        self.background = data[1] # 0xff is default battle background
        self.targetable = data[2]
        self.song       = data[3] # 0xff is default song

        self.character_scripts = []
        for script_index in range(self.PARTY_SIZE):
            data_start = self.CHARACTER_DATA_START + CharacterBattleScript.DATA_SIZE * script_index
            script = CharacterBattleScript(script_index, data[data_start : data_start + CharacterBattleScript.DATA_SIZE])
            self.character_scripts.append(script)

    def data(self):
        data = [0x00] * self.DATA_SIZE

        data[0]  = self.hide_names  << 0
        data[0] |= self.hide_party  << 7

        data[1]  = self.background
        data[2]  = self.targetable
        data[3]  = self.song

        for script_index, character_script in enumerate(self.character_scripts):
            data_start = self.CHARACTER_DATA_START + CharacterBattleScript.DATA_SIZE * script_index
            data[data_start : data_start + CharacterBattleScript.DATA_SIZE] = character_script.data()

        return data

    def print(self):
        print(f"{self.id}: hide party {self.hide_party}, hide names {self.hide_names}, background {self.background}, targetable {hex(self.targetable)}, song {self.song}")
        for character_script in self.character_scripts:
            print(f"    {str(character_script)}")
