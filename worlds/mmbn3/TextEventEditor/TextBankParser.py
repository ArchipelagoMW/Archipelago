class TextArchive:
    address: int = 0x000000
    size: int = 0

    scripts = None

    def __init__(self, address):
        self.address = address
        self.scripts = {}

    def __str__(self):
        retstr = f"@archive {hex(self.address)[2:]}\n"
        retstr += f"@size {self.size}"
        for script in self.scripts.values():
            retstr += str(script)
        retstr += '\n'
        return retstr


class Script:
    index: int = 0
    scriptType: str = 0

    commands = None

    def __init__(self, index, script_type):
        self.index = index
        self.scriptType = script_type
        self.commands = []

    def __str__(self):
        retstr = f"script {self.index} {self.scriptType} "+'{\n'
        for command in self.commands:
            retstr += str(command)
        retstr += '}\n'
        return retstr


class Command:
    command: str = ""
    parameters = None

    def __init__(self, command):
        self.command = command
        self.parameters = []

    def __str__(self):
        retstr = '\t'+self.command+'\n'
        for parameter in self.parameters:
            retstr += str(parameter)
        return retstr


class Parameter:
    key: str = ""
    value: str = ""

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"\t\t{self.key} = {self.value}\n"


class TextBlock:
    lines = None

    def __init__(self, lines):
        self.lines = lines

    def __str__(self):
        if len(self.lines) == 1:
            return f"\t\"{self.lines[0]}\"\n"
        retstr = '\t"""\n'
        for line in self.lines:
            retstr += f'\t{line}\n'
        retstr += '\t"""\n'
        return retstr


def parse_text_bank_file(file_path):
    archives = {}
    with open(file_path) as f:
        current_archive = None
        current_script = None
        current_command = None
        current_text_block = None
        lineNo = 0
        for line in f:
            lineNo += 1
            if current_text_block is not None:
                if line.__contains__('"""'):
                    current_script.commands.append(current_text_block)
                    current_text_block = None
                    continue
                else:
                    current_text_block.lines.append(line.strip())
                    continue

            if current_command is not None:
                if line.__contains__('='):
                    split_line = line.split('=')
                    current_command.parameters.append(Parameter(split_line[0].strip(), split_line[1].strip()))
                    continue
                else:
                    current_script.commands.append(current_command)
                    current_command = None

            if line.__contains__('@archive'):
                if current_archive is not None:
                    archives[current_archive.address] = current_archive
                archive_address = int(line.split(' ')[1], 16)
                current_archive = TextArchive(archive_address)
            elif line.__contains__('@size'):
                current_archive.size = int(line.split(' ')[1])
            elif line.__contains__('mmbn3'):
                split_line = line.split(' ')
                current_script = Script(int(split_line[1]), split_line[2])
            elif line.__contains__('}'):
                current_archive.scripts[current_script.index] = current_script
                current_script = None
            elif line.__contains__('"""'):
                if current_text_block is None:
                    current_text_block = TextBlock([])
                else:
                    current_script.commands.append(current_text_block)
                    current_text_block = None
            elif line.strip().startswith('"'):
                current_script.commands.append(TextBlock([line.strip().replace('"', '')]))
            elif len(line.strip()) != 0:
                current_command = Command(line.strip())
        archives[current_archive.address] = current_archive
    return archives