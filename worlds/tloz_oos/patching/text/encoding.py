import re
from collections import defaultdict
from functools import lru_cache
from typing import List, Union, Optional
from . import char_table, kanji_table, text_offset_split_index_seasons, text_offset_1_table_address_seasons, text_offset_2_table_address_seasons, \
    text_table_eng_address_seasons, \
    text_addresses_limit_seasons, text_offset_split_index_ages, text_offset_1_table_address_ages, text_offset_2_table_address_ages, text_table_eng_address_ages, \
    text_addresses_limit_ages
from ..RomData import RomData
from ..Util import simple_hex
from ..z80asm.Assembler import GameboyAddress

control_sequence_pattern = re.compile(r"""
    \\
    (jump|cmd|col|charsfx|speed|pos|wait|sfx|call)
    \(([^)]+)\) |
    \\(link_name|child_name|w7SecretBuffer1|w7SecretBuffer2|
    num1|opt|stop|heartpiece|num2|slow)
""", re.VERBOSE)
dict_pattern = re.compile(r"DICT(\d+)_([0-9a-f]+)")


def add_to_tree(tree: dict[str, list[int]], char: str, keys: [int]):
    tree[char] = keys


def build_encoding_dict() -> dict[str, list[int]]:
    tree = {}
    for i in range(len(char_table)):
        char = char_table[i]
        if char != "🚫" and char != "∅":
            add_to_tree(tree, char, [i])

    for i in range(len(kanji_table)):
        char = kanji_table[i]
        if char != "∅":
            add_to_tree(tree, char, [0x06, i])

    add_to_tree(tree, "jump", [0x07, 0x00])
    add_to_tree(tree, "cmd", [0x08, 0x00])

    add_to_tree(tree, "⬜", [0x09, 0x00])
    add_to_tree(tree, "🟥", [0x09, 0x01])
    add_to_tree(tree, "🟧", [0x09, 0x02])
    add_to_tree(tree, "🟦", [0x09, 0x03])
    add_to_tree(tree, "🟩", [0x09, 0x04])
    add_to_tree(tree, "col", [0x09, 0x00])

    add_to_tree(tree, "link_name", [0x0a, 0x00])
    add_to_tree(tree, "child_name", [0x0a, 0x01])
    add_to_tree(tree, "w7SecretBuffer1", [0x0a, 0x02])
    add_to_tree(tree, "w7SecretBuffer2", [0x0a, 0x03])

    add_to_tree(tree, "speed", [0x0c, 0x00])
    add_to_tree(tree, "num1", [0x0c, 0x08])
    add_to_tree(tree, "opt", [0x0c, 0x10])
    add_to_tree(tree, "stop", [0x0c, 0x18])
    add_to_tree(tree, "pos", [0x0c, 0x20])
    add_to_tree(tree, "heartpiece", [0x0c, 0x28])
    add_to_tree(tree, "num2", [0x0c, 0x30])
    add_to_tree(tree, "slow", [0x0c, 0x38])

    add_to_tree(tree, "wait", [0x0d, 0x00])
    add_to_tree(tree, "sfx", [0x0e, 0x00])
    add_to_tree(tree, "call", [0x0f, 0x00])

    add_to_tree(tree, "Ⓐ", [0xb8, 0xb9])
    add_to_tree(tree, "Ⓑ", [0xba, 0xbb])

    return tree


# --- Trie Data Structure ---
class TrieNode:
    def __init__(self):
        self.children = defaultdict(lambda: TrieNode())
        self.code = None


# --- Global Caches ---
encode_current_trie: Optional[TrieNode] = None
encode_current_encoding: Optional[dict[str, list[int]]] = None
encode_last_ids = (None, None)

control_keywords = {
    "link_name", "child_name", "w7SecretBuffer1", "w7SecretBuffer2",
    "num1", "opt", "stop", "heartpiece", "num2", "slow"
}

control_functions = {
    "jump", "cmd", "col", "charsfx", "speed", "pos", "wait", "sfx", "call"
}


def next_character(text: str, index: int) -> tuple[Union[str, tuple[str, int]], int]:
    if index >= len(text):
        return "\0", 1

    if text[index] != "\\":
        return text[index], 1

    # Try parsing a function-style command: \name(hex)
    for name in control_functions:
        if text.startswith(f"\\{name}(", index):
            start = index + len(name) + 2  # skip past '\name('
            end = start + 2
            value = text[start:end]
            return (name, int(value, 16)), end + 1 - index

    # Try keyword match (e.g. \opt)
    for name in control_keywords:
        if text.startswith(f"\\{name}", index):
            return name, 1 + len(name)

    raise Exception()


def build_trie(dictionary: dict[str, str]) -> TrieNode:
    root = TrieNode()
    for key, value in dictionary.items():
        node = root
        i = 0
        while i < len(value):
            token, length = next_character(value, i)
            node = node.children[token]
            i += length
        node.code = [2 + int(key[4]), int(key[6:8], 16)]
    return root


@lru_cache
def recursive_encode(text: str, index: int) -> tuple[int]:
    if index >= len(text):
        return (0,)

    token, length = next_character(text, index)
    if isinstance(token, tuple):
        encoded = list(encode_current_encoding[token[0]])
        encoded[-1] += token[1]
        if token[0] == "jump":
            return tuple(encoded)
    else:
        if token not in encode_current_encoding:
            token = "口"  # Use a white square to denote unknown characters
        encoded = encode_current_encoding[token]

    best = list(encoded) + list(recursive_encode(text, index + length))

    if token not in encode_current_trie.children:
        # No dict entry
        return tuple(best)

    node = encode_current_trie.children[token]
    i = index + length
    depth = 1

    while i < len(text):
        token2, tlen = next_character(text, i)
        if token2 not in node.children:
            break
        node = node.children[token2]
        i += tlen
        depth += 1
        if node.code:
            candidate = node.code + list(recursive_encode(text, i))
            if len(candidate) < len(best):
                best = candidate

    return tuple(best)


# --- Main Function ---
def encode_text(text: str, encoding: dict[str, List[int]], dictionary: dict[str, str]) -> List[int]:
    global encode_current_trie, encode_current_encoding, encode_last_ids
    id_dict = id(dictionary)
    id_enc = id(encoding)

    # Rebuild trie/cache if dictionary/encoding changed
    if encode_last_ids != (id_dict, id_enc):
        encode_current_trie = build_trie(dictionary)
        encode_current_encoding = encoding
        encode_last_ids = (id_dict, id_enc)

    result = list(recursive_encode(text, 0))
    return result


def encode_dict(text_data: dict[str, str], dictionary: Optional[dict[str, str]] = None) -> dict[str, list[int]]:
    if dictionary is None:
        dictionary = {}
    encoding_dict = build_encoding_dict()
    encoded_dict = {}
    for key in text_data:
        encoded_text = encode_text(text_data[key], encoding_dict, dictionary)
        encoded_dict[key] = encoded_text
    recursive_encode.cache_clear()
    return encoded_dict


def build_compact_table(data: dict[str, list[int]]) -> tuple[list[int], dict[str, int]]:
    sorted_items = sorted(data.items(), key=lambda kv: -len(kv[1]))
    compact = []
    offsets = {}

    for key, seq in sorted_items:
        for key2 in offsets:
            string_end = offsets[key2] + len(data[key2])
            if compact[string_end - len(seq):string_end] == seq:
                offset = string_end - len(seq)
                break
        else:
            offset = len(compact)
            compact.extend(seq)
        offsets[key] = offset
    assert len(compact) <= 0xffff

    return compact, offsets


def write_text_data(rom: RomData, dictionary: dict[str, str], texts: dict[str, str], seasons: bool):
    if seasons:
        text_offset_split_index = text_offset_split_index_seasons
        text_offset_1 = GameboyAddress(rom.read_byte(text_offset_1_table_address_seasons), rom.read_word(text_offset_1_table_address_seasons + 1))
        text_offset_2 = GameboyAddress(rom.read_byte(text_offset_2_table_address_seasons), rom.read_word(text_offset_2_table_address_seasons + 1))
        text_table_eng_address = text_table_eng_address_seasons
        text_addresses_limit = text_addresses_limit_seasons
    else:
        text_offset_split_index = text_offset_split_index_ages
        text_offset_1 = GameboyAddress(rom.read_byte(text_offset_1_table_address_ages), rom.read_word(text_offset_1_table_address_ages + 1))
        text_offset_2 = GameboyAddress(rom.read_byte(text_offset_2_table_address_ages), rom.read_word(text_offset_2_table_address_ages + 1))
        text_table_eng_address = text_table_eng_address_ages
        text_addresses_limit = text_addresses_limit_ages

    dict1 = {}
    dict2 = {}
    for key in texts:
        if int(key[3:5], 16) < text_offset_split_index - 4:
            dict1[key] = texts[key]
        else:
            dict2[key] = texts[key]

    encoded_dict1 = encode_dict(dict1, dictionary)
    encoded_dict1.update(encode_dict(dictionary))
    encoded_dict2 = encode_dict(dict2, dictionary)

    offset_table_length = (len(encoded_dict1) + len(encoded_dict2)) * 2
    text_offset_1_address = text_offset_1.address_in_rom()
    text_offset_2_address = text_offset_2.address_in_rom()
    text_table_current_address = text_table_eng_address
    tx_table_current_address = text_table_eng_address + 0x64 * 2
    text_offset_1_offset = text_table_eng_address + 0x64 * 2 + offset_table_length - text_offset_1_address
    assert text_offset_1_offset >= 0

    compact_table1, compact_offsets1 = build_compact_table(encoded_dict1)
    rom.write_bytes(text_offset_1_address + text_offset_1_offset, compact_table1)

    for i in range(4):
        rom.write_word(text_table_current_address, tx_table_current_address - text_table_eng_address)
        text_table_current_address += 2
        for j in range(0, 0x100):
            entry_name = f"DICT{i}_{simple_hex(j)}"
            rom.write_word(tx_table_current_address, compact_offsets1[entry_name] + text_offset_1_offset)
            tx_table_current_address += 2

    for i in range(text_offset_split_index - 4):
        start_address = tx_table_current_address
        subid = 0
        while True:
            tx = f"TX_{simple_hex(i)}{simple_hex(subid)}"
            if tx not in dict1:
                break
            subid += 1

            rom.write_word(tx_table_current_address, compact_offsets1[tx] + text_offset_1_offset)
            tx_table_current_address += 2
        if subid > 0:
            rom.write_word(text_table_current_address, start_address - text_table_eng_address)
        else:
            rom.write_word(text_table_current_address, 0)
        text_table_current_address += 2

    text_offset_2_offset = max(0, text_offset_1_address + text_offset_1_offset + len(compact_table1) - text_offset_2_address)
    compact_table2, compact_offsets2 = build_compact_table(encoded_dict2)
    assert text_offset_2_address + text_offset_2_offset + len(compact_table2) < text_addresses_limit, \
        f"Text is too long ({text_offset_2_address + text_offset_2_offset + len(compact_table2) - text_addresses_limit} too many bytes)"
    print(f"Free text bytes: {text_addresses_limit - text_offset_2_address - text_offset_2_offset - len(compact_table2)}")
    rom.write_bytes(text_offset_2_address + text_offset_2_offset, compact_table2)

    for i in range(text_offset_split_index - 4, 0x60):
        start_address = tx_table_current_address
        subid = 0
        while True:
            tx = f"TX_{simple_hex(i)}{simple_hex(subid)}"
            if tx not in dict2:
                break
            subid += 1

            rom.write_word(tx_table_current_address, compact_offsets2[tx] + text_offset_2_offset)
            tx_table_current_address += 2
        if subid > 0:
            rom.write_word(text_table_current_address, start_address - text_table_eng_address)
        else:
            rom.write_word(text_table_current_address, 0)
        text_table_current_address += 2
