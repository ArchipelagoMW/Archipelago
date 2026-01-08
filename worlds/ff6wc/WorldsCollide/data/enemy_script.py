from ..data import enemy_script_parser as parser

class EnemyScript():
    def __init__(self, id, data):
        self.id = id
        self.instructions = parser.parse_script(data)

    def append(self, instruction):
        self.instructions.append(instruction)

    def extend(self, instructions):
        self.instructions.extend(instructions)

    def insert(self, index, instructions):
        if type(instructions) is list:
            self.instructions[index : index] = instructions
        else:
            self.instructions.insert(index, instructions)

    def index(self, instruction, start = 0, end = None):
        if end is None:
            end = len(self.instructions)

        if type(instruction) is list:
            haystack = self.instructions[start : end]
            needle = instruction

            for haystack_index in range(len(haystack) - len(needle) + 1):
                for needle_index in range(len(needle)):
                    if haystack[haystack_index + needle_index] != needle[needle_index]:
                        break
                else:
                    return start + haystack_index

            raise ValueError(f"\n{self.format_instructions(needle)}\nNot found in script {self.id}")
        else:
            try:
                return self.instructions.index(instruction, start, end)
            except ValueError:
                raise ValueError(f"{str(instruction)} not found in script {self.id}")

    def remove(self, instructions, count = 1):
        if type(instructions) is list:
            start = 0
            for _ in range(count):
                start = self.index(instructions, start)
                del self.instructions[start : start + len(instructions)]
        else:
            try:
                for _ in range(count):
                    self.instructions.remove(instructions)
            except ValueError:
                raise ValueError(f"{str(instructions)} not found in script {self.id}")

    def replace(self, old_instructions, new_instructions, count = 1):
        old_instructions_len = 1
        if type(old_instructions) is list:
            old_instructions_len = len(old_instructions)

        start = 0
        for _ in range(count):
            start = self.index(old_instructions, start)
            del self.instructions[start : start + old_instructions_len]
            self.insert(start, new_instructions)

    def delete(self):
        self.instructions = []

    def data(self):
        data = []
        for instruction in self.instructions:
            data.extend(instruction())
        return data

    def format_instructions(self, instructions, include_addresses = False):
        from ..data import enemy_script_commands as ai_instr

        result = ""
        indentation = 0
        for instruction in instructions:
            if type(instruction) is ai_instr.EndIf or \
               type(instruction) is ai_instr.EndMainLoop or \
               type(instruction) is ai_instr.EndScript:
                indentation = 0

            if include_addresses:
                result += f"{repr(instruction):<19} | "
            result += f"{indentation * 4 * ' '}{str(instruction)}\n"

            if type(instruction) is ai_instr.If:
                indentation += 1
        return result[:-1]

    def __str__(self):
        result = f"{self.id}:\n"
        return result + self.format_instructions(self.instructions, include_addresses = False)

    def __repr__(self):
        result = f"{self.id}:\n"
        return result + self.format_instructions(self.instructions, include_addresses = True)
