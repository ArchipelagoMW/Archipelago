class Instruction:
    def __init__(self, values):
        if len(values) != len(self):
            raise ValueError(f"{self.__class__.__name__} invalid number arguments: {len(values)} != {len(self)}")
        if values[0] != self.OPCODE and self.OPCODE >= 0xf0:
            raise ValueError(f"{self.__class__.__name__} invalid opcode: {values[0]} != {self.OPCODE}")
        self.values = values

    def __len__(self):
        return self.SIZE

    def __call__(self):
        return self.values

    def __eq__(self, other):
        return type(self) is type(other) and self() == other()

    def __repr__(self):
        result = ""
        for value in self():
            result += f"0x{value:02x} "
        return result[:-1]

class RandomAttack(Instruction):
    OPCODE = 0xf0
    SIZE = 4

    def __init__(self, attack1, attack2, attack3):
        self._attack1 = attack1
        self._attack2 = attack2
        self._attack3 = attack3

    @property
    def attack1(self):
        return self._attack1

    @attack1.setter
    def attack1(self, value):
        self._attack1 = value

    @property
    def attack2(self):
        return self._attack2

    @attack2.setter
    def attack2(self, value):
        self._attack2 = value

    @property
    def attack3(self):
        return self._attack3

    @attack3.setter
    def attack3(self, value):
        self._attack3 = value

    def __call__(self):
        return [self.OPCODE, self._attack1, self._attack2, self._attack3]

    def __str__(self):
        from ..data.spell_names import id_name
        return f"RandomAttack: {id_name[self._attack1]}, {id_name[self._attack2]}, {id_name[self._attack3]}"

class SetTarget(Instruction):
    OPCODE = 0xf1
    SIZE = 2

    def __init__(self, value):
        super().__init__([self.OPCODE, value])

    def __str__(self):
        return f"SetTarget: {self.values[1]}"

class SetFormation(Instruction):
    OPCODE = 0xf2
    SIZE = 4

    def __init__(self, value1, value2, value3):
        super().__init__([self.OPCODE, value1, value2, value3])

    def __str__(self):
        return "SetFormation"

class Message(Instruction):
    OPCODE = 0xf3
    SIZE = 3

    def __init__(self, value1, value2 = None):
        if value2 is None:
            self.value1 = value1 & 0xff
            self.value2 = (value1 >> 8) & 0xff
            self.message_id = value1
        else:
            self.value1 = value1
            self.value2 = value2
            self.message_id = (value2 << 8) | value1
        super().__init__([self.OPCODE, self.value1, self.value2])

    def __str__(self):
        return f"Display Message: 0x{self.message_id:04x}"

class RandomCommand(Instruction):
    OPCODE = 0xf4
    SIZE = 4

    def __init__(self, value1, value2, value3):
        super().__init__([self.OPCODE, value1, value2, value3])

    def __str__(self):
        return "RandomCommand"

class ChangeEnemies(Instruction):
    OPCODE = 0xf5
    SIZE = 4

    def __init__(self, value1, value2, value3):
        super().__init__([self.OPCODE, value1, value2, value3])

    def __str__(self):
        return "ChangeEnemies"

class RandomItem(Instruction):
    OPCODE = 0xf6
    SIZE = 4

    def __init__(self, value1, value2, value3):
        super().__init__([self.OPCODE, value1, value2, value3])

    def __str__(self):
        return "RandomItem"

class Event(Instruction):
    OPCODE = 0xf7
    SIZE = 2

    def __init__(self, value):
        super().__init__([self.OPCODE, value])

    def __str__(self):
        return "Event"

class Arithmetic(Instruction):
    OPCODE = 0xf8
    SIZE = 3

    ADD = 0x80
    SUBTRACT = 0xc0

    def __init__(self, value1, value2):
        super().__init__([self.OPCODE, value1, value2])

        self.variable = value1
        self.operation = value2 & 0xc0
        self.value = value2 & 0xfc

    def __str__(self):
        if self.operation == self.ADD:
            return f"VAR_{self.variable} += {self.value}"
        elif self.operation == self.SUBTRACT:
            return f"VAR_{self.variable} -= {self.value}"
        return f"VAR_{self.variable} = {self.value}"

class Bits(Instruction):
    OPCODE = 0xf9
    SIZE = 4

    def __init__(self, value1, value2, value3):
        super().__init__([self.OPCODE, value1, value2, value3])

    def __str__(self):
        return "Bits"

class Animate(Instruction):
    OPCODE = 0xfa
    SIZE = 4

    def __init__(self, value1, value2, value3):
        super().__init__([self.OPCODE, value1, value2, value3])

    def __str__(self):
        return f"Animate {self.values[1]} {self.values[2]} {self.values[3]}"

class Misc(Instruction):
    OPCODE = 0xfb
    SIZE = 3

    def __init__(self, value1, value2):
        super().__init__([self.OPCODE, value1, value2])

    def __str__(self):
        return "Misc"

class If(Instruction):
    OPCODE = 0xfc
    SIZE = 4

    def __init__(self, value1, value2, value3):
        super().__init__([self.OPCODE, value1, value2, value3])

    def __str__(self):
        return f"If {self.values[1]} {self.values[2]} {self.values[3]}"

class EndTurn(Instruction): # resets targeting
    OPCODE = 0xfd
    SIZE = 1

    def __init__(self):
        super().__init__([self.OPCODE])

    def __str__(self):
        return "EndTurn"

class EndIf(Instruction):
    OPCODE = 0xfe
    SIZE = 1

    def __init__(self):
        super().__init__([self.OPCODE])

    def __str__(self):
        return "EndIf"

class EndMainLoop(Instruction):
    OPCODE = 0xff
    SIZE = 1

    def __init__(self):
        super().__init__([self.OPCODE])

    def __str__(self):
        return "EndMainLoop"

class EndScript(Instruction):
    OPCODE = 0xff
    SIZE = 1

    def __init__(self):
        super().__init__([self.OPCODE])

    def __str__(self):
        return "EndScript"

class Spell(Instruction):
    OPCODE = 0x00 # any spell id
    SIZE = 1

    def __init__(self, spell_id):
        self._spell_id = spell_id

        from ..data.spell_names import id_name
        self.name = id_name[self._spell_id]

    @property
    def spell_id(self):
        return self._spell_id

    @spell_id.setter
    def spell_id(self, spell_id):
        self._spell_id = spell_id

    def __call__(self):
        return [self._spell_id]

    def __str__(self):
        return self.name
