import random
import struct
import itertools

from .game import CypherItems, GameOptions
from .goals import Event, Goals
from .romWriter import RomWriter

base_event_id = 0xF2
base_hint_id = 0x01C0
base_hint_solve_id = 0x01E1
base_message_id = 0x60

max_goal_count = 12

event_address = 0x10C000
final_room_init_address = 0x07BE9E
messages_boxes_address = 0x0296ED-6
log_mission_address = 0x1E05D6
check_event_func = 0xF600

message_box_map = {
    'A': 0x28C0,
    'B': 0x28C1,
    'C': 0x28C2,
    'D': 0x28C3,
    'E': 0x28C4,
    'F': 0x28C5,
    'G': 0x28C6,
    'H': 0x28C7,
    'I': 0x28C8,
    'J': 0x28C9,
    'K': 0x28CA,
    'L': 0x28CB,
    'M': 0x28CC,
    'N': 0x28CD,
    'O': 0x28CE,
    'P': 0x28CF,
    'Q': 0x28D0,
    'R': 0x28D1,
    'S': 0x28D2,
    'T': 0x28D3,
    'U': 0x28D4,
    'V': 0x28D5,
    'W': 0x28D6,
    'X': 0x28D7,
    'Y': 0x28D8,
    'Z': 0x28D9,
    ' ': 0x280F,
    '!': 0x28DF,
    '?': 0x28DE,
    '\'': 0x28DC,
    ',': 0xA8DC,
    '.': 0x28DA,
    '-': 0x28DD,
    '_': 0x280E,
    '1': 0x2801,
    '2': 0x2802,
    '3': 0x2803,
    '4': 0x2804,
    '5': 0x2805,
    '6': 0x2806,
    '7': 0x2807,
    '8': 0x2808,
    '9': 0x2809,
    '0': 0x2800,
    '%': 0x280A,
    '/': 0x281A,
    '\\': 0x681A,
}

events: list[list[Event]] = [
    [(0x40, "KRAID",        "DEFEAT KRAID IN THE SUBMARINE LAIR.")],
    [(0x49, "SPORE SPAWN",  "DEFEAT SPORE SPAWN IN THE SPORE FIELD GENERATOR.")],
    [(0x4A, "BOMB TORIZO",  "DEFEAT THE TORIZO TRIO IN THE ARENA.")],
    [(0x50, "DRAYGON",      "DEFEAT DRAYGON IN THEIR MOLTEN NURSERY.")],
    [(0x51, "DUST TORIZO",  "ANNIHILATE THE DEAD TORIZO IN THE HIVE.")],
    [(0x52, "GOLD TORIZO",  "DEFEAT THE GOLD TORIZO GUARDING THE MAGMA LAKE.")],
    [(0x58, "CROCOMIRE",    "DEFEAT CROCOMIRE IN THE JUNGLE LAIR.")],
    [(0x60, "RIDLEY",       "DEFEAT RIDLEY IN THE SKY TEMPLE BOODING CHAMBER."),
     (0x61, "PHANTOON",     "DEFEAT PHANTOON IN THE SKY TEMPLE RELIQUARY.")],
    [(0x6A, "HYPER TORIZO", "DEFEAT HYPER TORIZO IN THE THUNDER LABS.")],
    [(0x1D, "SPACE PORT",   "DESTROY THE SPACE PORT AND CRASH THE DOCKED SHIPS."),
     (0x79, "BOTWOON",      "DEFEAT BOTWOON IN THE CRASHED CARGO SHIP.")],
    [(0x1F, "POWER OFF",    "TURN THE GEOTHERMAL ENERGY PLANT OFF.")],
]


map_stations = {
    0x3FFDFE: "OCEANIA MAP STATION",          # [Area 0 (0F, 0F):
    0x3FF9A0: "VULNAR CAVES MAP STATION",     # [Area 1 (13, 10):
    0x3FE68E: "MINES MAP STATION",            # [Area 2 (12, 07):
    0x3FECA8: "HIVE MAP STATION",             # [Area 2 (20, 07):
    0x3FE594: "LABORATORY MAP STATION",       # [Area 3 (0D, 0F):
    0x3FE0D8: "JUNGLE RUINS MAP STATION",     # [Area 3 (2B, 14):
    0x3FDF4A: "VULNAR PEAK MAP STATION",      # [Area 4 (19, 05):
    0x3FDF8C: "HYDRAULIC WORKS MAP STATION",  # [Area 4 (24, 10):
    0x3FDB9C: "SUZI RUINS MAP STATION",       # [Area 5 (14, 18):
    0x3FD894: "REEF MAP STATION",             # [Area 5 (28, 0E):
    0x3FD402: "ORBITAL MAP STATION",          # [Area 6 (1B, 15):
    0x3FD4C0: "GFS DAPHNE MAP STATION",       # [Area 6 (29, 10):
}


def ConvertToLabel(text: str) -> bytes:
    text = f'{text:12}'.replace(' ', '@')
    text += chr(0x00)
    return text.encode('LATIN-1')


def ConvertToText(text: str, event: int) -> bytes:
    line = ''
    new_text = ''
    for word in text.split(' '):
        if len(line) + len(word) + 1 > 17:
            new_text += f'{line:@<17} '
            line = ''

        if line:
            line += '@'
        line += word

    if line:
        new_text += f'{line:@<17} '
    while len(new_text) < (17 * 4):
        new_text += ('@' * 17) + ' '
    text = new_text + '\n'

    # event set text
    text += chr(0x01)
    text += chr((event >> 0) & 0xFF)
    text += chr((event >> 8) & 0xFF)
    text += chr(0x83)  # color blue
    text += "MISSION@COMPLETED"

    # event not set text
    text += chr(0x02)
    text += chr((event >> 0) & 0xFF)
    text += chr((event >> 8) & 0xFF)
    text += chr(0x82)  # color red
    text += "[INCOMPLETE]@@@@@"

    text += chr(0x00)  # terminator
    return text.encode('LATIN-1')


def ConvertToMessagebox(text: str) -> bytes:
    text = f'___{text:^26}___'
    text_codes = [message_box_map.get(c, 0x280F) for c in text]
    text_words = [struct.pack('<H', c) for c in text_codes]
    text_bytes = bytes(itertools.chain.from_iterable(text_words))
    return text_bytes


def GetShortAddress(address: int) -> int:
    return (address & 0x007FFF) | 0x8000


def WriteLogEntry(romWriter: RomWriter, address: int, index: int, event: int, name: str, description: str) -> int:
    label = ConvertToLabel(name)
    text = ConvertToText(description, base_hint_solve_id + index)

    label_start = address + 8
    text_start = label_start + len(label)
    end = text_start + len(text)

    header = struct.pack(
        '<HHHH', GetShortAddress(label_start), GetShortAddress(text_start), 0, base_hint_solve_id + index
    )

    romWriter.writeBytes(address, header)
    romWriter.writeBytes(label_start, label)
    romWriter.writeBytes(text_start, text)

    return end


def WriteLogs(romWriter: RomWriter, address: int, goals: list[Event]) -> None:
    hint_address = address + 2 + (2 * len(goals))

    for i, goal in enumerate(goals):
        romWriter.writeBytes(address, struct.pack('<H', GetShortAddress(hint_address)))
        hint_address = WriteLogEntry(romWriter, hint_address, i, *goal)
        address += 2
    romWriter.writeBytes(address, struct.pack('<H', 0))


def WriteMessageBoxes(romWriter: RomWriter, address: int, goals: list[Event]) -> None:
    message_address = address + (6 * (len(goals) + 2))

    message = ConvertToMessagebox('OBJECTIVES NOT COMPLETE')
    romWriter.writeBytes(address, struct.pack('<HHH', 0x8436, 0x825A, GetShortAddress(message_address)))
    romWriter.writeBytes(message_address, message)
    address += 6
    message_address += len(message)
    for i, goal in enumerate(goals):
        message = ConvertToMessagebox(f'GOAL {chr(ord("A") + i)}: {goal[1]}')
        romWriter.writeBytes(address, struct.pack('<HHH', 0x8436, 0x825A, GetShortAddress(message_address)))
        romWriter.writeBytes(message_address, message)
        address += 6
        message_address += len(message)
    romWriter.writeBytes(address, struct.pack('<HHH', 0x8436, 0x825A, GetShortAddress(message_address)))


def generate_goals(options: GameOptions) -> Goals:
    count = options.objective_rando

    bad_events: set[str] = set()
    if options.area_rando:
        bad_events.add("POWER OFF")
    if options.cypher_items != CypherItems.Anything:
        bad_events.add("HYPER TORIZO")

    valid_events = [
        [sub_event for sub_event in event if sub_event[1] not in bad_events]
        for event in events
    ]
    valid_events = [event for event in valid_events if event]

    bad_maps: list[int] = []  # list instead of set because we will still use this in the final order
    if options.cypher_items == CypherItems.SmallAmmo:
        bad_maps.extend(addr
                        for addr, name in map_stations.items()
                        if name in ("SUZI RUINS MAP STATION", "REEF MAP STATION"))
    valid_maps = [addr for addr in map_stations.keys() if addr not in bad_maps]

    max_with_options = min(max_goal_count, len(valid_events), len(valid_maps))

    if count > max_with_options:
        count = max_with_options

    # select goals
    goals = [random.sample(subgoals, 1)[0] for subgoals in random.sample(valid_events, count)]

    # select map station order
    random.shuffle(valid_maps)
    random.shuffle(bad_maps)
    # putting bad maps at the end means they won't be required to find all the objectives
    map_station_order = valid_maps + bad_maps
    assert len(map_station_order) == len(map_stations), f"{map_station_order=}"

    return Goals(goals, map_station_order)


def write_goals(goals: Goals, romWriter: RomWriter) -> None:
    # write room init function to check state conditions
    romWriter.writeBytes(final_room_init_address, struct.pack('<H', check_event_func))

    # write event list
    data = bytes([goal[0] for goal in goals.objectives])
    romWriter.writeBytes(event_address, data)

    WriteLogs(romWriter, log_mission_address, goals.objectives)
    WriteMessageBoxes(romWriter, messages_boxes_address + (base_message_id * 6), goals.objectives)

    # write out map station plm data
    for i, map_station in enumerate(goals.map_station_order):
        i = i % len(goals.objectives)

        # change map station into message station
        romWriter.writeBytes(map_station + 0, struct.pack('<H', 0xF2C0))
        # skip over the 2 bytes for the plm position
        # write message and event into plm arg
        romWriter.writeBytes(map_station + 4, struct.pack('BB', base_event_id + i, base_message_id + i + 1))


def goal_spoiler(goals: Goals) -> str:
    map_station_mapping: dict[Event, list[str]] = {
        obj: []
        for obj in goals.objectives
    }
    for i, map_station_addr in enumerate(goals.map_station_order):
        i = i % len(goals.objectives)
        # [:-12] removes " Map Station" to make them shorter
        map_station_mapping[goals.objectives[i]].append(map_stations[map_station_addr][:-12].title())
    out = "Objectives:\n"
    for obj in goals.objectives:
        station_list = ", ".join(map_station_mapping[obj])
        out += f"{obj[1].title().rjust(19)}  hinted at  {station_list}\n"
    return out
