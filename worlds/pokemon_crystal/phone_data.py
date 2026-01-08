from BaseClasses import Location
from .data import PhoneScriptData
from .utils import convert_to_ingame_text


class ScriptLine:
    contents: list[str | int]

    def __init__(self, contents):
        self.contents = contents

    def get_bytes(self):
        out_bytes = []
        for content in self.contents:
            if type(content) is str:
                out_bytes += convert_to_ingame_text(content)
            else:
                out_bytes.append(content)
        return out_bytes


class PhoneScript:
    caller_id: int
    lines: list[ScriptLine]

    def __init__(self, caller_id, lines):
        self.caller_id = caller_id
        self.lines = lines

    def get_script_bytes(self):
        out_bytes = []
        for line in self.lines:
            out_bytes += line.get_bytes()
        return out_bytes


caller_none = 0x00
caller_mom = 0x01
caller_bikeshop = 0x02
caller_bill = 0x03
caller_elm = 0x04

caller_withheld = 38
caller_bank_of_mom = 39
caller_brock = 40
caller_eusine = 41
caller_out_of_area = 42

caller_string_to_id_map = {
    "none": caller_none,
    "mom": caller_mom,
    "bikeshop": caller_bikeshop,
    "bill": caller_bill,
    "elm": caller_elm,
    "withheld": caller_withheld,
    "bank_of_mom": caller_bank_of_mom,
    "brock": caller_brock,
    "eusine": caller_eusine,
    "out_of_area": caller_out_of_area
}

text_cmd = 0x00  # Initiates the text at the beginning of the phone call
para_cmd = 0x51  # Starts a new paragraph, clearing the text box
line_cmd = 0x4f  # Starts a new line (always the 2nd line)
cont_cmd = 0x55  # Scrolls to a third line
# Every "text box" technically contains three lines. cont_cmd can only be after line_cmd. line_cmd can only be after para_cmd. para_cmd can be anywhere.
done_cmd = 0x57  # Exits the phone call

play_g_cmd = 0x14  # Outputs player name
player_cmd = 0x52  # Outputs player name
rival_cmd = 0x53  # Outputs rival name
poke_cmd = 0x54  # Outputs POKÉ

placeholder_map = {
    "<POKE>": poke_cmd,
    "<player>": player_cmd,
    "<rival>": rival_cmd
}

cmd_line_size = {
    poke_cmd: 4,
    player_cmd: 7,
    rival_cmd: 7,
}


def script_line_to_blocks(first_cmd: int, line: str):
    blocks = [first_cmd]
    size = 0
    original_line = line
    while line:
        placeholder_start = line.find("<")
        placeholder_end = line.find(">", placeholder_start)

        if placeholder_start != -1 and placeholder_end != -1:
            # append the string up until the command placeholder
            if placeholder_start > 0:
                blocks.append(line[:placeholder_start])
                size += placeholder_start

            # extract the command
            cmd_string = line[placeholder_start:placeholder_end + 1]
            cmd = placeholder_map.get(cmd_string, None)
            if cmd is None:
                raise ValueError(f"Unknown placeholder: {cmd_string}")
            blocks.append(placeholder_map[cmd_string])
            size += cmd_line_size[cmd]

            # remove the processed command
            line = line[placeholder_end + 1:]
        else:
            # plain text only
            blocks.append(line)
            size += len(line)
            break
    if size > 18:
        raise ValueError(f"Line too long: '{original_line}' measured at {size} characters")

    return blocks


def data_to_script(data: PhoneScriptData):
    script_lines = []

    caller = caller_string_to_id_map.get(data.caller, None)
    if caller is None:
        raise ValueError(f"Invalid caller '{data.caller}' in the phone script '{data.name}'.")

    for paragraph in data.script:
        if not isinstance(paragraph, str):
            raise ValueError(
                f"Invalid script data encountered in phone script '{data.name}': Expected string, got {type(paragraph).__name__}")

        lines = paragraph.rstrip("\n").split("\n")
        if len(lines) > 3:
            raise ValueError(f"A paragraph in phone script '{data.name}' had more than 3 lines:\n{paragraph}")
        cmd = None
        for line in lines:
            if cmd is None:
                cmd = text_cmd if not script_lines else para_cmd
            elif cmd == text_cmd or cmd == para_cmd:
                cmd = line_cmd
            elif cmd == line_cmd:
                cmd = cont_cmd

            try:
                blocks = script_line_to_blocks(cmd, line)
            except ValueError as ex:
                raise ValueError(f"Error in phone script '{data.name}': {ex}") from ex
            script_lines.append(ScriptLine(blocks))

    script_lines.append(ScriptLine([done_cmd]))
    return PhoneScript(caller, script_lines)


def split_location(location_name):
    if len(location_name) < 17:
        return [line_cmd, location_name]
    if len(location_name) < 33:
        return [line_cmd, location_name[:15] + "-", cont_cmd, location_name[15:]]
    return [line_cmd, location_name[:15] + "-", cont_cmd, location_name[15:30] + "…"]


def template_call_remote(location: Location, world):
    player = location.item.player
    # split into lines with cont
    location_cmd = split_location(location.name.upper())

    POKEMON_REGIONS = {
        "POKEMON RED AND BLUE": "KANTO",
        "POKEMON CRYSTAL": "JOHTO",
        "POKEMON EMERALD": "HOENN",
        "POKEMON FIRERED AND LEAFGREEN": "KANTO",
        "POKEMON PLATINUM": "SINNOH",
        "POKEMON BLACK AND WHITE": "UNOVA",
        "VOLTORB FLIP": "the GAME CORNER",
        "POKEMON PINBALL": "KANTO GAME CORNER",
        "POKEMON MYSTERY DUNGEON EXPLORERS OF SKY": "GRASS CONTINENT"
    }

    raw_game_name = location.item.game.upper()
    game_name = POKEMON_REGIONS.get(raw_game_name, raw_game_name)
    game_name = (game_name[:15] + "…") if len(game_name) > 16 else game_name

    player_name = world.multiworld.player_name[player].upper()

    item_name = location.item.name.upper()
    item_name = (item_name[:15] + "…") if len(item_name) > 16 else item_name

    return PhoneScript(caller_out_of_area, [
        ScriptLine([text_cmd, "Hi, ", play_g_cmd, "! It's"]),
        ScriptLine([line_cmd, player_name]),
        ScriptLine([para_cmd, "I'm calling from"]),
        ScriptLine([line_cmd, game_name]),
        ScriptLine([para_cmd, "I'm looking for my"]),
        ScriptLine([line_cmd, item_name]),
        ScriptLine([para_cmd, "that's at your"]),
        ScriptLine(location_cmd),
        ScriptLine([para_cmd, "Have you found it"]),
        ScriptLine([line_cmd, "yet?"]),
        ScriptLine([done_cmd])
    ])


def template_call_bike_shop(location):
    item_name = location.item.name.upper()
    item_name = (item_name[:15] + "…") if len(item_name) > 16 else item_name
    return PhoneScript(caller_mom, [
        ScriptLine([text_cmd, "Hello?"]),
        ScriptLine([para_cmd, "Hi ", play_g_cmd, "!"]),
        ScriptLine([para_cmd, "I got a call from"]),
        ScriptLine([line_cmd, "a man in GOLDENROD"]),
        ScriptLine([para_cmd, "He said he has a"]),
        ScriptLine([line_cmd, item_name]),
        ScriptLine([cont_cmd, "for you."]),
        ScriptLine([para_cmd, "Make sure you head"]),
        ScriptLine([line_cmd, "to the BIKE SHOP"]),
        ScriptLine([para_cmd, "to pick that up,"]),
        ScriptLine([line_cmd, "okay?"]),
        ScriptLine([done_cmd])
    ])


def template_call_psychic():
    return PhoneScript(caller_withheld, [
        ScriptLine([text_cmd, "…"]),
        ScriptLine([para_cmd, "…"]),
        ScriptLine([para_cmd, "…"]),
        ScriptLine([para_cmd, "…I got it!"]),
        ScriptLine([para_cmd, "You're looking"]),
        ScriptLine([line_cmd, "for this!"]),
        ScriptLine([done_cmd])
    ])


def template_call_filler_hint(location, world):
    player_name = world.multiworld.player_name[location.item.player].upper()

    item_name = location.item.name.upper()
    item_name = (item_name[:15] + "…") if len(item_name) > 16 else item_name
    return PhoneScript(caller_withheld, [
        ScriptLine([text_cmd, "Hiii, ", play_g_cmd, "!"]),
        ScriptLine([para_cmd, "I've heard that"]),
        ScriptLine([line_cmd, player_name]),
        ScriptLine([cont_cmd, "is currently BK"]),
        ScriptLine([para_cmd, "To progress"]),
        ScriptLine([line_cmd, "further, they"]),
        ScriptLine([cont_cmd, "require"]),
        ScriptLine([para_cmd, item_name]),
        ScriptLine([line_cmd, "Please get it as"]),
        ScriptLine([cont_cmd, "soon as possible"]),
        ScriptLine([para_cmd, "It's very"]),
        ScriptLine([line_cmd, "important!"]),
        ScriptLine([done_cmd])
    ])


def get_shuffled_basic_calls(random, phone_scripts) -> list[PhoneScript]:
    basic_calls = []
    for phone_data in phone_scripts:
        basic_calls.append(data_to_script(phone_data))
    random.shuffle(basic_calls)
    return basic_calls

# Phone scripts now defined in ./data/phone_data.yaml
