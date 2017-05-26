text_addresses = {'Altar': (0x180300, 256),
                  'Triforce': (0x180400, 256),
                  'Uncle': (0x180500, 256),
                  'Ganon1': (0x180600, 256),
                  'Ganon2': (0x180700, 256),
                  'Blind': (0x180800, 256),
                  'TavernMan': (0x180C00, 256),
                  'Sahasrahla1': (0x180A00, 256),
                  'Sahasrahla2': (0x180B00, 256),
                  'BombShop1': (0x180E00, 256),
                  'BombShop2': (0x180D00, 256),
                  'PyramidFairy': (0x180900, 256)}

credits_addresses = {'KingsReturn': (0x76928, 22),
                     'Sanctuary': (0x76964, 16),
                     'Kakariko': (0x76997, 23),
                     'DesertPalace': (0x769D4, 24),
                     'MountainTower': (0x76A12, 24),
                     'LinksHouse': (0x76A52, 19),
                     'Zora': (0x76A85, 20),
                     'MagicShop': (0x76AC5, 23),
                     'Lumberjacks': (0x76AFC, 16),
                     'FluteBoy': (0x76B34, 23),
                     'WishingWell': (0x76B71, 23),
                     'Blacksmiths': (0x76BAC, 23),
                     'SickKid': (0x76BDF, 20),
                     'DeathMountain': (0x76C19, 16),
                     'LostWoods': (0x76C51, 16),
                     'Altar': (0x76C81, 20)}

Uncle_texts = ['Good Luck!\nYou will need it.',
               '10\n9\n8\n7\n6\n5\n4\n3\n2\n1\nGo!']
Triforce_texts = ['Product has Hole in center. Bad seller, 0 out of 5.',
                  '\n  Well Done!']
BombShop2_texts = ['Bombs!\nBombs!\nBiggest!\nBestest!\nGreatest!\nBoomest!']
PyramidFairy_texts = ['May I talk to you about our lord and savior, Ganon?']
Sahasrahla2_texts = ['You already got my item, idiot.']
Blind_texts = ['I bet you expected a vision related pun?\n\nNot Today.\n Didn\'t see that coming, did you?']
Ganon1_texts = ['\n\n\n\n\n\n\n\n\nWhy are you reading an empty textbox?',
                'Hi']
TavernMan_texts = ['Did you know that talking to random NPCs wastes time in a race? I hope this information may be of use to you in the future.']

KingsReturn_texts = ['Who is this even']
Sanctuary_texts = ['A Priest\'s love']
Kakariko_texts = ['Shasschahshahsahahrahsashsa']
Blacksmiths_texts = ['frogs for bread']
DeathMountain_texts = ['lost again']
LostWoods_texts = ['thieves\' stump']
WishingWell_texts = ['Bottle for Bottle']
DesertPalace_texts = ['literacy moves']
MountainTower_texts = ['up up and away']
LinksHouse_texts = ['Home Sweet Home']
Lumberjacks_texts = ['agahnim\'s axes']
SickKid_texts = ['Next Time Stay Down']
Zora_texts = ['Splashes For Sale']
MagicShop_texts = ['Drug deal']
FluteBoy_texts = ['Stumped']


def string_to_credits(s, length):
    buf = bytearray()

    if len(s) > length:
        s = s[:length]

    padding = length - len(s)
    leftpadding = padding // 2
    rightpadding = padding - leftpadding
    s = ' '*leftpadding + s + ' '*rightpadding

    for char in s.lower():
        buf.append(char_to_credit_char(char))

    return buf


def string_to_alttp_text(s, maxbytes=256):
    lines = s.upper().split('\n')
    outbuf = bytearray()
    lineindex = 0

    while lines:
        linespace = 14
        line = lines.pop(0)
        words = line.split(' ')
        outbuf.append(0x74 if lineindex == 0 else 0x75 if lineindex == 1 else 0x76)  # line starter
        while words:
            word = words.pop(0)
            # sanity check: if the word we have is more than 14 characters, we take as much as we can still fit and push the rest back for later
            if len(word) > 14:
                if linespace < 14:
                    word = ' ' + word
                word_first = word[:linespace]
                words.insert(0, word[linespace:])
                lines.insert(0, ' '.join(words))

                write_word(outbuf, word_first)
                break

            if len(word) <= (linespace if linespace == 14 else linespace - 1):
                if linespace < 14:
                    word = ' ' + word
                linespace -= len(word)
                write_word(outbuf, word)
            else:
                # ran out of space, push word and lines back and continue with next line
                words.insert(0, word)
                lines.insert(0, ' '.join(words))
                break

        lineindex += 1
        if lineindex % 3 == 0 and lines:
            outbuf.append(0x7E)
        if lineindex >= 3 and lines:
            outbuf.append(0x73)

    # check for max length
    if len(outbuf) > maxbytes - 1:
        outbuf = outbuf[:maxbytes - 1]
        # make sure we interpret the end of box character
        if outbuf[-1] == 0x00:
            outbuf[-1] = 0x73

    outbuf.append(0x7F)
    return outbuf


def write_word(buf, word):
    for char in word:
        buf.extend([0x00, char_to_alttp_char(char)])


char_map = {' ': 0xFF,
            '?': 0xC6,
            '!': 0xC7,
            ',': 0xC8,
            '-': 0xC9,
            '…': 0xCC,
            '.': 0xCD,
            '~': 0xCE,
            '～': 0xCE,
            "'": 0xD8,
            '’': 0xD8,
            '↑': 0xE0,
            '↓': 0xE1,
            '→': 0xE2,
            '←': 0xE3,
            'あ': 0x00,
            'い': 0x01,
            'う': 0x02,
            'え': 0x03,
            'お': 0x04,
            'や': 0x05,
            'ゆ': 0x06,
            'よ': 0x07,
            'か': 0x08,
            'き': 0x09,
            'く': 0x0A,
            'け': 0x0B,
            'こ': 0x0C,
            'わ': 0x0D,
            'を': 0x0E,
            'ん': 0x0F,
            'さ': 0x10,
            'し': 0x11,
            'す': 0x12,
            'せ': 0x13,
            'そ': 0x14,
            'が': 0x15,
            'ぎ': 0x16,
            'ぐ': 0x17,
            'た': 0x18,
            'ち': 0x19,
            'つ': 0x1A,
            'て': 0x1B,
            'と': 0x1C,
            'げ': 0x1D,
            'ご': 0x1E,
            'ざ': 0x1F,
            'な': 0x20,
            'に': 0x21,
            'ぬ': 0x22,
            'ね': 0x23,
            'の': 0x24,
            'じ': 0x25,
            'ず': 0x26,
            'ぜ': 0x27,
            'は': 0x28,
            'ひ': 0x29,
            'ふ': 0x2A,
            'へ': 0x2B,
            'ほ': 0x2C,
            'ぞ': 0x2D,
            'だ': 0x2E,
            'ぢ': 0x2F,
            'ま': 0x30,
            'み': 0x31,
            'む': 0x32,
            'め': 0x33,
            'も': 0x34,
            'づ': 0x35,
            'で': 0x36,
            'ど': 0x37,
            'ら': 0x38,
            'り': 0x39,
            'る': 0x3A,
            'れ': 0x3B,
            'ろ': 0x3C,
            'ば': 0x3D,
            'び': 0x3E,
            'ぶ': 0x3F,
            'べ': 0x40,
            'ぼ': 0x41,
            'ぱ': 0x42,
            'ぴ': 0x43,
            'ぷ': 0x44,
            'ぺ': 0x45,
            'ぽ': 0x46,
            'ゃ': 0x47,
            'ゅ': 0x48,
            'ょ': 0x49,
            'っ': 0x4A,
            'ぁ': 0x4B,
            'ぃ': 0x4C,
            'ぅ': 0x4D,
            'ぇ': 0x4E,
            'ぉ': 0x4F,
            'ア': 0x50,
            'イ': 0x51,
            'ウ': 0x52,
            'エ': 0x53,
            'オ': 0x54,
            'ヤ': 0x55,
            'ユ': 0x56,
            'ヨ': 0x57,
            'カ': 0x58,
            'キ': 0x59,
            'ク': 0x5A,
            'ケ': 0x5B,
            'コ': 0x5C,
            'ワ': 0x5D,
            'ヲ': 0x5E,
            'ン': 0x5F,
            'サ': 0x60,
            'シ': 0x61,
            'ス': 0x62,
            'セ': 0x63,
            'ソ': 0x64,
            'ガ': 0x65,
            'ギ': 0x66,
            'グ': 0x67,
            'タ': 0x68,
            'チ': 0x69,
            'ツ': 0x6A,
            'テ': 0x6B,
            'ト': 0x6C,
            'ゲ': 0x6D,
            'ゴ': 0x6E,
            'ザ': 0x6F,
            'ナ': 0x70,
            'ニ': 0x71,
            'ヌ': 0x72,
            'ネ': 0x73,
            'ノ': 0x74,
            'ジ': 0x75,
            'ズ': 0x76,
            'ゼ': 0x77,
            'ハ': 0x78,
            'ヒ': 0x79,
            'フ': 0x7A,
            'ヘ': 0x7B,
            'ホ': 0x7C,
            'ゾ': 0x7D,
            'ダ': 0x7E,
            'マ': 0x80,
            'ミ': 0x81,
            'ム': 0x82,
            'メ': 0x83,
            'モ': 0x84,
            'ヅ': 0x85,
            'デ': 0x86,
            'ド': 0x87,
            'ラ': 0x88,
            'リ': 0x89,
            'ル': 0x8A,
            'レ': 0x8B,
            'ロ': 0x8C,
            'バ': 0x8D,
            'ビ': 0x8E,
            'ブ': 0x8F,
            'ベ': 0x90,
            'ボ': 0x91,
            'パ': 0x92,
            'ピ': 0x93,
            'プ': 0x94,
            'ペ': 0x95,
            'ポ': 0x96,
            'ャ': 0x97,
            'ュ': 0x98,
            'ョ': 0x99,
            'ッ': 0x9A,
            'ァ': 0x9B,
            'ィ': 0x9C,
            'ゥ': 0x9D,
            'ェ': 0x9E,
            'ォ': 0x9F}

credit_char_map = {' ': 0x9F,
                   ',': 0x37,
                   '.': 0x37,
                   '-': 0x36,
                   "'": 0x35}


def char_to_alttp_char(char):
    if 0x30 <= ord(char) <= 0x39:
        return ord(char) + 0x70

    if 0x41 <= ord(char) <= 0x5A:
        return ord(char) + 0x69

    return char_map.get(char, 0xFF)


def char_to_credit_char(char):
    if 0x61 <= ord(char) <= 0x7A:
        return ord(char) - 0x47

    return credit_char_map.get(char, 0x9F)

