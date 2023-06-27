import re

class Dialog:

    command = re.compile(r"^\{[^}]*\}")
    invalid = re.compile(r"(?<!^)\{[^}]*\}(?!$)", re.MULTILINE)
    character = re.compile(r"(?P<digit>[0-9])|(?P<upper>[A-Z])|(?P<lower>[a-z])")

    @staticmethod
    def Simple(text: str):
        maxBytes = 256
        wrap = 19

        bytes = []
        lines = text.split('\n')
        lineIndex = 0
        for line in lines:
            bytes.append(0x74 if 0 else 0x75 if 1 else 0x76)
            letters = line[:wrap] if len(line) > wrap else line
            for letter in letters:
                write = Dialog.LetterToBytes(letter)
                if (write[0] == 0xFD):
                    bytes += write
                else:
                    for b in write:
                        bytes += [ 0x00, b ]

            lineIndex += 1

            if (lineIndex < len(lines)):
                if (lineIndex % 3 == 0):
                    bytes.append(0x7E) # pause for input
                if (lineIndex >= 3):
                    bytes.append(0x73) # scroll

        return bytes[:maxBytes - 1].append(0x7F)

    @staticmethod
    def Compiled(text: str):
        maxBytes = 2046
        wrap = 19

        if (Dialog.invalid.match(text)):
            raise Exception("Dialog commands must be placed on separate lines", text)

        padOut = False
        pause = True

        bytes = [ 0xFB ]
        lines = Dialog.Wordwrap(text, wrap)
        lineCount = len([l for l in lines if not Dialog.command.match(l)])
        lineIndex = 0
        for line in lines:
            match = Dialog.command.match(line)
            if (match is not None):
                if (match.string == "{NOTEXT}"):
                    return [ 0xFB, 0xFE, 0x6E, 0x00, 0xFE, 0x6B, 0x04 ]
                if (match.string == "{INTRO}"):
                    padOut = True
                if (match.string == "{NOPAUSE}"):
                    pause = False
                    continue

                result = Dialog.CommandBytesFor(match.string)
                if (result is None):
                    raise Exception(f"Dialog text contained unknown command {match.string}", text)
                else:
                    bytes += result

                if (len(bytes) > maxBytes):
                    raise Exception("Command overflowed maximum byte length", text)

                continue

            if (lineIndex > 0):
                bytes.append(0xF8 if lineIndex == 1 else    #// row 2
                             0xF9 if lineIndex == 2 else    #// row 3
                             0xF6)                          #// scroll

            #// The first box needs to fill the full width with spaces as the palette is loaded weird.
            letters = line + (" " * wrap) if padOut and lineIndex < 3 else line
            for letter in letters:
                bytes += Dialog.LetterToBytes(letter)

            lineIndex += 1

            if (pause and lineIndex % 3 == 0 and lineIndex < lineCount):
                bytes.append(0xFA) #// pause for input

        return bytes[:maxBytes]

    @staticmethod
    def CommandBytesFor(text: str):
        bytesMap = {
                        "{SPEED0}" : [ 0xFC, 0x00 ],
                        "{SPEED2}" : [ 0xFC, 0x02 ],
                        "{SPEED6}" : [ 0xFC, 0x06 ],
                        "{PAUSE1}" : [ 0xFE, 0x78, 0x01 ],
                        "{PAUSE3}" : [ 0xFE, 0x78, 0x03 ],
                        "{PAUSE5}" : [ 0xFE, 0x78, 0x05 ],
                        "{PAUSE7}" : [ 0xFE, 0x78, 0x07 ],
                        "{PAUSE9}" : [ 0xFE, 0x78, 0x09 ],
                        "{INPUT}" : [ 0xFA ],
                        "{CHOICE}" : [ 0xFE, 0x68 ],
                        "{ITEMSELECT}" : [ 0xFE, 0x69 ],
                        "{CHOICE2}" : [ 0xFE, 0x71 ],
                        "{CHOICE3}" : [ 0xFE, 0x72 ],
                        "{C:GREEN}" : [ 0xFE, 0x77, 0x07 ],
                        "{C:YELLOW}" : [ 0xFE, 0x77, 0x02 ],
                        "{HARP}" : [ 0xFE, 0x79, 0x2D ],
                        "{MENU}" : [ 0xFE, 0x6D, 0x00 ],
                        "{BOTTOM}" : [ 0xFE, 0x6D, 0x01 ],
                        "{NOBORDER}" : [ 0xFE, 0x6B, 0x02 ],
                        "{CHANGEPIC}" : [ 0xFE, 0x67, 0xFE, 0x67 ],
                        "{CHANGEMUSIC}" : [ 0xFE, 0x67 ],
                        "{INTRO}" : [ 0xFE, 0x6E, 0x00, 0xFE, 0x77, 0x07, 0xFC, 0x03, 0xFE, 0x6B, 0x02, 0xFE, 0x67 ],
                        "{IBOX}" : [ 0xFE, 0x6B, 0x02, 0xFE, 0x77, 0x07, 0xFC, 0x03, 0xF7 ],
                    }
        return bytesMap.get(text, None)

    @staticmethod
    def Wordwrap(text: str, width: int):
        result = []
        for line in text.split('\n'):
            line = line.rstrip()
            if (len(line) <= width):
                result.append(line)
            else:
                words = line.split(' ')
                lines = [ "" ]
                for word in words:
                    line = lines.pop()
                    if (len(line) + len(word) <= width):
                        line = f"{line}{word} "
                    else:
                        if (len(line) > 0):
                            lines.append(line)
                        line = word
                        while (len(line) > width):
                            lines.append(line[:width])
                            line = line[width:]
                        line = f"{line} "
                    lines.append(line)
                #lines.reverse()
                result += [l.strip() for l in lines]
        return result

    @staticmethod
    def LetterToBytes(c: str):
        match = Dialog.character.match(c)
        if match is None: 
            value = Dialog.letters.get(c, None)
            return value if value else [ 0xFF ]
        elif match.group("digit") != None: return [(ord(c) - ord('0') + 0xA0) ]
        elif match.group("upper") != None: return [ (ord(c) - ord('A') + 0xAA) ]
        elif match.group("lower") != None: return [ (ord(c) - ord('a') + 0x30) ]
        else:
            value = Dialog.letters.get(c, None)
            return value if value else [ 0xFF ]

        #regions letter bytes lookup

    letters = {
        ' ' : [ 0x4F ],
        '?' : [ 0xC6 ],
        '!' : [ 0xC7 ],
        ',' : [ 0xC8 ],
        '-' : [ 0xC9 ],
        '…' : [ 0xCC ],
        '.' : [ 0xCD ],
        '~' : [ 0xCE ],
        '～' : [ 0xCE ],
        '\'' : [ 0xD8 ],
        '’' : [ 0xD8 ],
        '"' : [ 0xD8 ],
        ':' : [ 0x4A ],
        '@' : [ 0x4B ],
        '#' : [ 0x4C ],
        '¤' : [ 0x4D, 0x4E ], #// Morphing ball
        '_' : [ 0xFF ], #// Full width space
        '£' : [ 0xFE, 0x6A ], #// link's name compressed
        '>' : [ 0xD2, 0xD3 ], #// link face
        '%' : [ 0xDD ], #// Hylian Bird
        '^' : [ 0xDE ], #// Hylian Ankh
        '=' : [ 0xDF ], #// Hylian Wavy lines
        '↑' : [ 0xE0 ],
        '↓' : [ 0xE1 ],
        '→' : [ 0xE2 ],
        '←' : [ 0xE3 ],
        '≥' : [ 0xE4 ], #// cursor
        '¼' : [ 0xE5, 0xE7 ], #// 1/4 heart
        '½' : [ 0xE6, 0xE7 ], #// 1/2 heart
        '¾' : [ 0xE8, 0xE9 ], #// 3/4 heart
        '♥' : [ 0xEA, 0xEB ], #// full heart
        'ᚋ' : [ 0xFE, 0x6C, 0x00 ], #// var 0
        'ᚌ' : [ 0xFE, 0x6C, 0x01 ], #// var 1
        'ᚍ' : [ 0xFE, 0x6C, 0x02 ], #// var 2
        'ᚎ' : [ 0xFE, 0x6C, 0x03 ], #// var 3

        'あ' : [ 0x00 ],
        'い' : [ 0x01 ],
        'う' : [ 0x02 ],
        'え' : [ 0x03 ],
        'お' : [ 0x04 ],
        'や' : [ 0x05 ],
        'ゆ' : [ 0x06 ],
        'よ' : [ 0x07 ],
        'か' : [ 0x08 ],
        'き' : [ 0x09 ],
        'く' : [ 0x0A ],
        'け' : [ 0x0B ],
        'こ' : [ 0x0C ],
        'わ' : [ 0x0D ],
        'を' : [ 0x0E ],
        'ん' : [ 0x0F ],
        'さ' : [ 0x10 ],
        'し' : [ 0x11 ],
        'す' : [ 0x12 ],
        'せ' : [ 0x13 ],
        'そ' : [ 0x14 ],
        'が' : [ 0x15 ],
        'ぎ' : [ 0x16 ],
        'ぐ' : [ 0x17 ],
        'た' : [ 0x18 ],
        'ち' : [ 0x19 ],
        'つ' : [ 0x1A ],
        'て' : [ 0x1B ],
        'と' : [ 0x1C ],
        'げ' : [ 0x1D ],
        'ご' : [ 0x1E ],
        'ざ' : [ 0x1F ],
        'な' : [ 0x20 ],
        'に' : [ 0x21 ],
        'ぬ' : [ 0x22 ],
        'ね' : [ 0x23 ],
        'の' : [ 0x24 ],
        'じ' : [ 0x25 ],
        'ず' : [ 0x26 ],
        'ぜ' : [ 0x27 ],
        'は' : [ 0x28 ],
        'ひ' : [ 0x29 ],
        'ふ' : [ 0x2A ],
        'へ' : [ 0x2B ],
        'ほ' : [ 0x2C ],
        'ぞ' : [ 0x2D ],
        'だ' : [ 0x2E ],
        'ぢ' : [ 0x2F ],

        'ア' : [ 0x50 ],
        'イ' : [ 0x51 ],
        'ウ' : [ 0x52 ],
        'エ' : [ 0x53 ],
        'オ' : [ 0x54 ],
        'ヤ' : [ 0x55 ],
        'ユ' : [ 0x56 ],
        'ヨ' : [ 0x57 ],
        'カ' : [ 0x58 ],
        'キ' : [ 0x59 ],
        'ク' : [ 0x5A ],
        'ケ' : [ 0x5B ],
        'コ' : [ 0x5C ],
        'ワ' : [ 0x5D ],
        'ヲ' : [ 0x5E ],
        'ン' : [ 0x5F ],
        'サ' : [ 0x60 ],
        'シ' : [ 0x61 ],
        'ス' : [ 0x62 ],
        'セ' : [ 0x63 ],
        'ソ' : [ 0x64 ],
        'ガ' : [ 0x65 ],
        'ギ' : [ 0x66 ],
        'グ' : [ 0x67 ],
        'タ' : [ 0x68 ],
        'チ' : [ 0x69 ],
        'ツ' : [ 0x6A ],
        'テ' : [ 0x6B ],
        'ト' : [ 0x6C ],
        'ゲ' : [ 0x6D ],
        'ゴ' : [ 0x6E ],
        'ザ' : [ 0x6F ],
        'ナ' : [ 0x70 ],
        'ニ' : [ 0x71 ],
        'ヌ' : [ 0x72 ],
        'ネ' : [ 0x73 ],
        'ノ' : [ 0x74 ],
        'ジ' : [ 0x75 ],
        'ズ' : [ 0x76 ],
        'ゼ' : [ 0x77 ],
        'ハ' : [ 0x78 ],
        'ヒ' : [ 0x79 ],
        'フ' : [ 0x7A ],
        'ヘ' : [ 0x7B ],
        'ホ' : [ 0x7C ],
        'ゾ' : [ 0x7D ],
        'ダ' : [ 0x7E ],
        'マ' : [ 0x80 ],
        'ミ' : [ 0x81 ],
        'ム' : [ 0x82 ],
        'メ' : [ 0x83 ],
        'モ' : [ 0x84 ],
        'ヅ' : [ 0x85 ],
        'デ' : [ 0x86 ],
        'ド' : [ 0x87 ],
        'ラ' : [ 0x88 ],
        'リ' : [ 0x89 ],
        'ル' : [ 0x8A ],
        'レ' : [ 0x8B ],
        'ロ' : [ 0x8C ],
        'バ' : [ 0x8D ],
        'ビ' : [ 0x8E ],
        'ブ' : [ 0x8F ],
        'ベ' : [ 0x90 ],
        'ボ' : [ 0x91 ],
        'パ' : [ 0x92 ],
        'ピ' : [ 0x93 ],
        'プ' : [ 0x94 ],
        'ペ' : [ 0x95 ],
        'ポ' : [ 0x96 ],
        'ャ' : [ 0x97 ],
        'ュ' : [ 0x98 ],
        'ョ' : [ 0x99 ],
        'ッ' : [ 0x9A ],
        'ァ' : [ 0x9B ],
        'ィ' : [ 0x9C ],
        'ゥ' : [ 0x9D ],
        'ェ' : [ 0x9E ],
        'ォ' : [ 0x9F ],
    }
