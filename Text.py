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
                  'PyramidFairy': (0x180900, 256),
                  }


altar_text = {'Fighter Sword': 'A pathetic\nsword rests\nhere!',
              'Master Sword': 'I thought this\nwas meant to\nbe randomized?',
              'Tempered Sword': 'I stole the\nblacksmith\'s\njob!',
              'Golden Sword': 'The butter\nsword rests\nhere!',
              'Blue Shield': 'Now you can\ndefend against\npebbles!',
              'Red Shield': 'Now you can\ndefend against\nfireballs!',
              'Mirror Shield': 'Now you can\ndefend against\nlasers!',
              'Fir eRod': 'I\'m the hot\nrod. I make\nthings burn!',
              'Ice Rod': 'I\'m the cold\nrod. I make\nthings freeze!',
              'Hammer': 'stop\nhammer time!',
              'Hookshot': 'BOING!!!\nBOING!!!\nBOING!!!',
              'Bow': 'You have\nchosen the\narcher class.',
              'Blue Boomerang': 'No matter what\nyou do, blue\nreturns to you',
              'Red Boomerang': 'No matter what\nyou do, red\nreturns to you',
              'Magic Powder': 'you can turn\nanti-faeries\ninto fairies',
              'Bombos': 'Burn, baby,\nburn! Fear my\nring of fire!',
              'Ether': 'Zero Kelvin!\nAbsolute zero!\nFear the cold!',
              'Quake': 'Maxing out the\nRichter scale\nis what I do!',
              'Lamp': 'Baby, baby,\nbaby.\nLight my way!',
              'Shovel': 'Can\n   You\n      Dig it?',
              'Cane of Somaria': 'I make blocks\nto hold down\nswitches!',
              'Cane of Byrna': 'Use this to\nbecome\ninvincible!',
              'Cape': 'Wear this to\nbecome\ninvisible!',
              'Magic Mirror': 'Isn\'t your\nreflection so\npretty?',
              'Power Glove': 'Now you can\nlift weak\nstuff!',
              'Titans Mitt': 'Now you can\nlift heavy\nstuff!',
              'Book of Mudora': 'This is a\nparadox?!',
              'Flippers': 'fancy a swim?',
              'Moon Pearl': '  Bunny Link\n      be\n     gone!',
              'Bug Catching Net': 'Let\'s catch\nsome bees and\nfaeries!',
              'Blue Mail': 'Now you\'re a\nblue elf!',
              'Red Mail': 'Now you\'re a\nred elf!',
              'Piece of Heart': 'Just a little\npiece of love!',
              'Boss Heart Container': 'Maximum health\nincreased!\nYeah!',
              'Single Bomb': 'I make things\ngo BOOM! But\njust once.',
              'Bombs (3)': 'I make things\ngo triple\nBOOM!!!',
              'Mushroom': 'I\'m a fun guy!\n\nI\'m a funghi!',
              'Bottle': 'Now you can\nstore potions\nand stuff!',
              'Single Arrow': 'a lonely arrow\nsits here.',
              'Arrows (10)': 'This will give\nyou ten shots\nwith your bow!',
              'Rupee (1)': 'Just pocket\nchange. Move\nright along.',
              'Rupees (5)': 'Just pocket\nchange. Move\nright along.',
              'Rupees (20)': 'Just couch\ncash. Move\nright along.',
              'Rupees (50)': 'Just couch\ncash. Move\nright along.',
              'Rupees (100)': 'A rupee stash!\nHell yeah!',
              'Rupees (300)': 'A rupee hoard!\nHell yeah!',
              'Ocarina': 'Save the duck\nand fly to\nfreedom!',
              'Pegasus Boots': 'Gotta go fast!',
              'Bomb Upgrade (+5)': 'increase bomb\nstorage, low\nlow price',
              'Bomb Upgrade (+10)': 'increase bomb\nstorage, low\nlow price',
              'Arrow Upgrade (+5)': 'increase arrow\nstorage, low\nlow price',
              'Arrow Upgrade (+10)': 'increase arrow\nstorage, low\nlow price',
              'Silver Arrows': 'Do you fancy\nsilver tipped\narrows?',
              'Magic Upgrade (1/2)': 'Your magic\npower has been\ndoubled!',
              'Magic Upgrade (1/4)': 'Your magic\npower has been\nquadrupled!',
              'Progressive Sword': 'a better copy\nof your sword\nfor your time',
              'Progressive Shield': 'have a better\nblocker in\nfront of you',
              'Progressive Armor': 'time for a\nchange of\nclothes?',
              'Progressive Glove': 'a way to lift\nheavier things',
              'Triforce': '\n   YOU WIN!',
              'Nothing': 'Some Hot Air'}


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
            '\'': 0xD8,
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


def char_to_alttp_char(char):
    if 0x30 <= ord(char) <= 0x39:
        return ord(char) + 0x80

    if 0x41 <= ord(char) <= 0x5A:
        return ord(char) + 0x69

    return char_map.get(char, 0xFF)

