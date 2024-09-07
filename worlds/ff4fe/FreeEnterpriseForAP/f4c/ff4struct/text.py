import re

_RAW_CHAR_MAP = {
    0x01 : "\n",
    #0x09 : "\n",
    0x0A : "`",
    0x42 : "A",
    0x43 : "B",
    0x44 : "C",
    0x45 : "D",
    0x46 : "E",
    0x47 : "F",
    0x48 : "G",
    0x49 : "H",
    0x4A : "I",
    0x4B : "J",
    0x4C : "K",
    0x4D : "L",
    0x4E : "M",
    0x4F : "N",
    0x50 : "O",
    0x51 : "P",
    0x52 : "Q",
    0x53 : "R",
    0x54 : "S",
    0x55 : "T",
    0x56 : "U",
    0x57 : "V",
    0x58 : "W",
    0x59 : "X",
    0x5A : "Y",
    0x5B : "Z",
    0x5C : "a",
    0x5D : "b",
    0x5E : "c",
    0x5F : "d",
    0x60 : "e",
    0x61 : "f",
    0x62 : "g",
    0x63 : "h",
    0x64 : "i",
    0x65 : "j",
    0x66 : "k",
    0x67 : "l",
    0x68 : "m",
    0x69 : "n",
    0x6A : "o",
    0x6B : "p",
    0x6C : "q",
    0x6D : "r",
    0x6E : "s",
    0x6F : "t",
    0x70 : "u",
    0x71 : "v",
    0x72 : "w",
    0x73 : "x",
    0x74 : "y",
    0x75 : "z",
    0x80 : "0",
    0x81 : "1",
    0x82 : "2",
    0x83 : "3",
    0x84 : "4",
    0x85 : "5",
    0x86 : "6",
    0x87 : "7",
    0x88 : "8",
    0x89 : "9",
    0x8A : "e ",
    0x8B : " t",
    0x8C : "th",
    0x8D : "he",
    0x8E : "t ",
    0x8F : "ou",
    0x90 : " a",
    0x91 : "s ",
    0x92 : "er",
    0x93 : "in",
    0x94 : "re",
    0x95 : "d ",
    0x96 : "an",
    0x97 : " o",
    0x98 : "on",
    0x99 : "st",
    0x9A : " w",
    0x9B : "o ",
    0x9C : " m",
    0x9D : "ha",
    0x9E : "to",
    0x9F : "is",
    0xA0 : "yo",
    0xA1 : " y",
    0xA2 : " i",
    0xA3 : "al",
    0xA4 : "ar",
    0xA5 : " h",
    0xA6 : "r ",
    0xA7 : " s",
    0xA8 : "at",
    0xA9 : "n ",
    0xAA : " c",
    0xAB : "ng",
    0xAC : "ve",
    0xAD : "ll",
    0xAE : "y ",
    0xAF : "nd",
    0xB0 : "en",
    0xB1 : "ed",
    0xB2 : "hi",
    0xB3 : "or",
    0xB4 : ", ",
    0xB5 : "I ",
    0xB6 : "u ",
    0xB7 : "me",
    0xB8 : "ta",
    0xB9 : " b",
    0xBA : " I",
    0xBB : "te",
    0xBC : "of",
    0xBD : "ea",
    0xBE : "ur",
    0xBF : "l ",
    0xC0 : "'",
    0xC1 : ".",
    0xC2 : "-",
    0xC3 : "_",
    0xC4 : "!",
    0xC5 : "?",
    0xC6 : "%",
    0xC7 : "/",
    0xC8 : ":",
    0xC9 : ",",
    0xCA : " f",
    0xCB : " d",
    0xCC : "ow",
    0xCD : "se",
    0xCE : "  ",
    0xCF : "it",
    0xD0 : "et",
    0xD1 : "le",
    0xD2 : "f ",
    0xD3 : " g",
    0xD4 : "es",
    0xD5 : "ro",
    0xD6 : "ne",
    0xD7 : "ry",
    0xD8 : " l",
    0xD9 : "us",
    0xDA : "no",
    0xDB : "ut",
    0xDC : "ca",
    0xDD : "as",
    0xDE : "Th",
    0xDF : "ai",
    0xE0 : "ot",
    0xE1 : "be",
    0xE2 : "el",
    0xE3 : "om",
    0xE4 : "'s",
    0xE5 : "il",
    0xE6 : "de",
    0xE7 : "gh",
    0xE8 : "ay",
    0xE9 : "nt",
    0xEA : "Wh",
    0xEB : "Yo",
    0xEC : "wa",
    0xED : "oo",
    0xEE : "We",
    0xEF : "g ",
    0xF0 : "ge",
    0xF1 : " n",
    0xF2 : "ee",
    0xF3 : "wi",
    0xF4 : " M",
    0xF5 : "ke",
    0xF6 : "we",
    0xF7 : " p",
    0xF8 : "ig",
    0xF9 : "ys",
    0xFA : " B",
    0xFB : "am",
    0xFC : "ld",
    0xFD : " W",
    0xFE : "la",
    0xFF : " ",
}

_SYMBOLS = {
    0x02 : "space",
    0x06 : "next",
    0x07 : "item",
    0x08 : "amount",
    #0x0A : "dot",
    0x21 : "stone",
    0x22 : "frog",
    0x23 : "tiny",
    0x24 : "pig",
    0x25 : "mute",
    0x26 : "blind",
    0x27 : "poison",
    0x28 : "floating",
    0x29 : "claw",
    0x2A : "rod",
    0x2B : "staff",
    0x2C : "darksword",
    0x2D : "sword",
    0x2E : "lightsword",
    0x2F : "spear",
    0x30 : "knife",
    0x31 : "katana",
    0x32 : "shuriken",
    0x33 : "boomerang",
    0x34 : "axe",
    0x35 : "wrench",
    0x36 : "harp",
    0x37 : "bow",
    0x38 : "arrow",
    0x39 : "hammer",
    0x3A : "whip",
    0x3B : "shield",
    0x3C : "helmet",
    0x3D : "armor",
    0x3E : "gauntlet",
    0x3F : "blackmagic",
    0x40 : "whitemagic",
    0x41 : "callmagic",
    0x76 : "flatm",
    0x77 : "flath",
    0x78 : "flatp",
    0x79 : "tent",
    0x7A : "potion",
    0x7B : "shirt",
    0x7C : "ring",
    0x7D : "crystal",
    0x7E : "key",
    0x7F : "tail",
}

_NAMES = {
    0x00 : "Cecil",
    0x01 : "Kain",
    0x02 : "Rydia",
    0x03 : "Tellah",
    0x04 : "Edward",
    0x05 : "Rosa",
    0x06 : "Yang",
    0x07 : "Palom",
    0x08 : "Porom",
    0x09 : "Cid",
    0x0A : "Edge",
    0x0B : "Fusoya",
    0x0C : "Golbez",
    0x0D : "Anna"
}

_ENCODE_TREE = {}
_SYMBOL_CODE_LOOKUP = {}

'''
Given a list of bytes representing a text string in the FF4 ROM, return a decoded
string containing the text contents. If the data contains multiple strings, then
return a list of decoded strings instead.
'''
def decode(byte_list, consts=None):
    results = []
    chars = []

    i = 0
    while i < len(byte_list):
        b = byte_list[i]
        if b == 0:
            results.append(''.join(chars))
            chars = []
        elif b == 0x02:
            i += 1
            param = byte_list[i]
            #chars.append("[space {}]".format(param))
            chars.append("~" * param)
        elif b == 0x03:
            i += 1
            param = byte_list[i]
            music_name = '${:02X}'.format(param)
            if consts and consts.get_name(param, 'music'):
                music_name = '#{}'.format(consts.get_name(param, 'music'))
            chars.append("[music {}]".format(music_name))
        elif b == 0x04:
            i += 1
            param = byte_list[i]
            if param in _NAMES:
                chars.append('[{}]'.format(_NAMES[param]))
            else:
                chars.append("[name ${:02X}]".format(param))
        elif b == 0x05:
            i += 1
            param = byte_list[i]
            chars.append("[pause {}]".format(param))
        elif b == 0x09:
            chars.append("\n")
        elif b in _RAW_CHAR_MAP:
            chars.append(_RAW_CHAR_MAP[b])
        elif b in _SYMBOLS:
            chars.append('[{}]'.format(_SYMBOLS[b]))
        else:
            chars.append('[${:02X}]'.format(b))

        i += 1

    if chars:
        results.append(''.join(chars))

    if len(results) > 1:
        return results
    else:
        return results[0]

'''
Given an ASCII string (with symbol annotations), return an FF4-encoded list of
bytes representing that string. If a list of input strings is provided, then instead
return the concatenation of all those encoded strings.
'''
def encode(text, optimize=False, allow_dual_char=True, fixed_length=None):
    _build_encode_maps()

    encoding = []
    
    if type(text) in [list, tuple]:
        for t in text:
            encoding.extend(encode(t, optimize=optimize, allow_dual_char=allow_dual_char, fixed_length=fixed_length))
    else:
        for line in text.splitlines(True):
            if allow_dual_char and line == "\n":
                encoding.append(0x09)
            else:
                parts = re.split(r'(\[[A-Za-z0-9 \$]+\])', line)
                for part in parts:
                    if part.startswith('[') and part.endswith(']'):
                        encoding.extend(_encode_symbol(part[1:-1]))
                    else:
                        encoding.extend(_encode_raw(part, optimize=optimize, allow_dual_char=allow_dual_char))

        if fixed_length:
            if len(encoding) < fixed_length:
                encoding.extend([0xFF] * (fixed_length - len(encoding)))
        else:
            encoding.append(0x00)
    
    return encoding

#-----------------------------------------------------------------------------------------------------

def _translate_number(number_string):
    if re.search(r'^\$[A-Fa-f0-9]+$', number_string):
        return int(number_string[1:], 16)
    elif re.search(r'^[0-9]+$', number_string):
        return int(number_string)
    else:
        return None

def _encode_symbol(symbol_name):
    symbol_slug = symbol_name.lower().replace(' ', '')

    if symbol_slug in _SYMBOL_CODE_LOOKUP:
        return _SYMBOL_CODE_LOOKUP[symbol_slug]
    elif _translate_number(symbol_slug) is not None:
        val = _translate_number(symbol_slug)
        if val < 0 or val > 255:
            raise ValueError("Cannot encode raw byte value {0} / ${0:02X} (out of range)".format(val))
        return [val]
    else:
        parameterized_symbols = {
            'space' : 0x02,
            'music' : 0x03,
            'name'  : 0x04,
            'pause' : 0x05,
        }
        for s in parameterized_symbols:
            if symbol_slug.startswith(s):
                val = _translate_number(symbol_slug[len(s):])
                if val is None or val < 0 or val > 255:
                    raise ValueError("Cannot encode symbol parameter value '{}'".format(symbol_slug[len(s):]))
                return [parameterized_symbols[s], val]
    
    raise ValueError("Cannot encode unrecognized symbol '{}'".format(symbol_name))


def _encode_raw(text, optimize=False, allow_dual_char=True):
    if text == '':
        return []

    m = re.search(r'^\~+', text)
    if m:
        return [0x02, len(m.group(0))] + _encode_raw(text[len(m.group(0)):], optimize=optimize, allow_dual_char=allow_dual_char)

    if text[0] not in _ENCODE_TREE:
        raise ValueError("Cannot encode text character {} (ordinal {}) in snippet '{}'".format(text[0], ord(text[0]), text))

    options = []
    snippets = _ENCODE_TREE[text[0]]
    for snippet in snippets:
        if not allow_dual_char and len(snippet[0]) > 1:
            continue

        if text.startswith(snippet[0]):
            code = snippet[1]
            encoding = [code] + _encode_raw(text[len(snippet[0]):], optimize=optimize, allow_dual_char=allow_dual_char)
            if optimize:
                options.append(encoding)
            else:
                return encoding

    options.sort(key=len)
    return options[0]

def _build_encode_maps():
    if _ENCODE_TREE:
        return

    for code in _RAW_CHAR_MAP:
        t = _RAW_CHAR_MAP[code]
        _ENCODE_TREE.setdefault(t[0], []).append( (t, code) )

    for startchar in _ENCODE_TREE:
        _ENCODE_TREE[startchar].sort(key=lambda p: (len(p[0]), p[1]), reverse=True)

    for code in _SYMBOLS:
        _SYMBOL_CODE_LOOKUP[_SYMBOLS[code]] = [code]

    for code in _NAMES:
        _SYMBOL_CODE_LOOKUP[_NAMES[code].lower()] = [0x04, code]

#-----------------------------------------------------------------------------------------------------

def _hex_string_to_byte_list(hex_string):
    hex_string = re.sub(r'\s', '', hex_string)
    result = []
    for i in range(0, len(hex_string), 2):
        result.append(int(hex_string[i:i+2], 16))
    return result

def _print_hex(byte_list):
    print(' '.join('{:02X}'.format(x) for x in byte_list))

if __name__ == '__main__':
    #print('\n'.join(decode(_hex_string_to_byte_list('''
    #    04 01 C8 55 8D A9 4A 9C D9 8E 6B E8 01 B9 5C 5E 66 9C AE E6 5D 6F 6E 8B 9B 5B 60 68 D9 C4 00 04 01 C8 04 05 C3 01 09 09 09 04 05 C8 04 0C 9A DD 90 67 6E 6A 01 FF 70 AF 92 8B 63 8A 5E 98 6F D5 67 C4 01 BA 6F C0 91 DA 8E 04 01 C0 91 61 5C 70 67 6F C4 01 09 04 01 C8 04 0C C3 8B ED C5 00 04 0A C8 5A BD 63 C4 FF EA 9B 5F 6A 01 A1 8F 8B 63 93 66 FF 94 5C 5E 6F 64 71 A8 B1 01 8B 63 8A 48 64 96 8E BC FA 5C 5D C2 E5 C5 00 04 01 C8 55 A3 66 D8 A8 92 C4 01 FD 8A 68 D9 8E 63 BE D7 C4 00 04 05 C8 49 BE 6D AE 70 6B C4 00 5A 8F 9A 94 6F 5E 63 C4 C4 00 04 0B C8 4A 6F E4 8B 63 8A 5E B3 8A BC 01 8B B2 91 48 64 96 6F C9 8B 63 8A 44 51 56 C4 01 04 0A C8 4E 96 C4 BA 6F C0 91 63 70 F0 C4 01 09 04 0B C8 58 8A 68 D9 8E E6 99 D5 74 8B 8D 01 FF 45 60 61 B0 6E 64 71 8A 54 74 99 60 68 CA 64 6D 99 C4 01 FF 50 8C 92 72 9F 8A A3 67 8B 63 8A 5F FB 5C F0 01 9A 64 AD B9 8A 94 6B DF 94 5F C4 00 04 01 C8 58 8A 5F 64 95 CF C4 01 04 0A C8 4A 8E 99 6A 6B 6B B1 C4 00 04 0C C8 5A 8F FF 6D 70 93 60 95 68 AE 6B 67 96 C4 01 FF 5A 8F A7 9D AD F7 5C AE 61 B3 8B 63 9F C4 01 09 09 04 0B C8 5A 8F C4 00 04 0C C8 48 60 8E 5C 72 E8 C4 01 04 0B C8 45 98 C0 8E 74 8F FF 94 A3 64 75 60 01 9A 63 9B 74 8F 90 94 C5 01 04 0C C8 54 9E 6B A2 6F C4 01 04 0B C8 58 5C 66 8A 70 6B C4 00 04 0C C8 EA AE 5F 64 95 B5 9D 71 8A A3 67 01 8B 9D 8E 9D 6F 94 5F C5 01 09 09 04 0B C8 44 E3 8A 6F 9B 74 8F 6D 01 A7 B0 CD 6E C4 01 FF 45 9B 74 8F FF 94 B7 68 5D 92 A1 8F 6D 01 CA 5C 8C 92 C0 91 69 5C B7 C5 01 04 0C C8 4E AE 61 5C 8C 92 C5 01 FF 49 64 91 69 FB 8A 9F C3 FF 4C 67 70 5A 5C C3 C5 01 09 09 04 00 C8 58 9D 6F C4 C5 01 09 09 09 04 05 C8 55 9D 8E B7 96 6E C3 01 04 0A C8 04 00 E4 C3 B9 D5 8C 92 C4 C5 01 09 09 04 00 C8 04 0C C3 FF 9F C3 9C 74 C3 01 09 09 09 04 0B C8 5A 8F 9A 92 8A 5E 98 6F D5 AD B1 01 B9 AE 5B 60 68 D9 C0 8B 60 D1 6B 5C 8C 74 C1 01 FF 5A 8F A6 5D 67 ED 95 68 5C 5F 8A 64 8E BD 6E 64 92 01 CA B3 A5 64 68 8B 9B D9 8A 74 8F C1 00 04 0A C8 4E 96 C4 01 09 09 09 04 00 C8 B5 9D 71 8A E1 B0 01 CA 64 E7 6F 93 62 9C 74 97 72 A9 5D D5 8C 92 C3 01 09 09 04 0C C8 5A 8F 90 6D 8A 68 AE 5D D5 8C 92 C5 01 09 09 09 04 00 C8 43 DB C3 A2 8E 5E 8F 67 95 9D AC 01 B9 60 B0 9C 60 C3 9A 63 6A 9A DD 01 AA 98 6F D5 AD 60 95 5D AE 5B 60 68 D9 C0 01 8B 60 D1 6B 5C 8C 74 C1 01 04 0C C8 43 70 8E 4A 8E EC 91 B7 C3 01 BA 8E B7 96 91 68 74 A7 8F 67 9A DD 01 FF 99 5C 93 60 95 F3 8C FF 60 71 64 BF 61 B3 01 FF 5B 60 68 D9 8B 9B 70 CD C3 C3
    #    '''))))

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('data', nargs="+")
    parser.add_argument('-d', '--dual_char', action='store_true')
    args = parser.parse_args()
    input_data = ' '.join(args.data)

    if re.match(r'^\s*([A-Fa-f0-9]{2}\s*)*$', input_data):
        # decode text from hex
        byte_list = []
        input_data = re.sub(r'[^A-Fa-f0-9]', '', input_data)
        for i in range(0, len(input_data), 2):
            byte_list.append(int(input_data[i:i+2], 16))
        print(decode(byte_list))
    else:
        # encode hex from text
        data = encode(input_data, allow_dual_char=args.dual_char)
        print(' '.join(["{:02X}".format(b) for b in data]))


