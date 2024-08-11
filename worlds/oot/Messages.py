# text details: https://wiki.cloudmodding.com/oot/Text_Format

from .HintList import misc_item_hint_table, misc_location_hint_table
from .TextBox import line_wrap
from .Utils import find_last

TEXT_START = 0x92D000
ENG_TEXT_SIZE_LIMIT = 0x39000
JPN_TEXT_SIZE_LIMIT = 0x3A150

JPN_TABLE_START = 0xB808AC
ENG_TABLE_START = 0xB849EC
CREDITS_TABLE_START = 0xB88C0C

JPN_TABLE_SIZE = ENG_TABLE_START - JPN_TABLE_START
ENG_TABLE_SIZE = CREDITS_TABLE_START - ENG_TABLE_START

EXTENDED_TABLE_START = JPN_TABLE_START # start writing entries to the jp table instead of english for more space
EXTENDED_TABLE_SIZE = JPN_TABLE_SIZE + ENG_TABLE_SIZE # 0x8360 bytes, 4204 entries

# name of type, followed by number of additional bytes to read, follwed by a function that prints the code
CONTROL_CODES = {
    0x00: ('pad', 0, lambda _: '<pad>' ),
    0x01: ('line-break', 0, lambda _: '\n' ),
    0x02: ('end', 0, lambda _: '' ),
    0x04: ('box-break', 0, lambda _: '\n▼\n' ),
    0x05: ('color', 1, lambda d: '<color ' + "{:02x}".format(d) + '>' ),
    0x06: ('gap', 1, lambda d: '<' + str(d) + 'px gap>' ),
    0x07: ('goto', 2, lambda d: '<goto ' + "{:04x}".format(d) + '>' ),
    0x08: ('instant', 0, lambda _: '<allow instant text>' ),
    0x09: ('un-instant', 0, lambda _: '<disallow instant text>' ),
    0x0A: ('keep-open', 0, lambda _: '<keep open>' ),
    0x0B: ('event', 0, lambda _: '<event>' ),
    0x0C: ('box-break-delay', 1, lambda d: '\n▼<wait ' + str(d) + ' frames>\n' ),
    0x0E: ('fade-out', 1, lambda d: '<fade after ' + str(d) + ' frames?>' ),
    0x0F: ('name', 0, lambda _: '<name>' ),
    0x10: ('ocarina', 0, lambda _: '<ocarina>' ),
    0x12: ('sound', 2, lambda d: '<play SFX ' + "{:04x}".format(d) + '>' ),
    0x13: ('icon', 1, lambda d: '<icon ' + "{:02x}".format(d) + '>' ),
    0x14: ('speed', 1, lambda d: '<delay each character by ' + str(d) + ' frames>' ),
    0x15: ('background', 3, lambda d: '<set background to ' + "{:06x}".format(d) + '>' ),
    0x16: ('marathon', 0, lambda _: '<marathon time>' ),
    0x17: ('race', 0, lambda _: '<race time>' ),
    0x18: ('points', 0, lambda _: '<points>' ),
    0x19: ('skulltula', 0, lambda _: '<skulltula count>' ),
    0x1A: ('unskippable', 0, lambda _: '<text is unskippable>' ),
    0x1B: ('two-choice', 0, lambda _: '<start two choice>' ),
    0x1C: ('three-choice', 0, lambda _: '<start three choice>' ),
    0x1D: ('fish', 0, lambda _: '<fish weight>' ),
    0x1E: ('high-score', 1, lambda d: '<high-score ' + "{:02x}".format(d) + '>' ),
    0x1F: ('time', 0, lambda _: '<current time>' ),
}

# Maps unicode characters to corresponding bytes in OOTR's character set.
CHARACTER_MAP = {
    'Ⓐ': 0x9F,
    'Ⓑ': 0xA0,
    'Ⓒ': 0xA1,
    'Ⓛ': 0xA2,
    'Ⓡ': 0xA3,
    'Ⓩ': 0xA4,
    '⯅': 0xA5,
    '⯆': 0xA6,
    '⯇': 0xA7,
    '⯈': 0xA8,
    chr(0xA9): 0xA9,  # Down arrow   -- not sure what best supports this
    chr(0xAA): 0xAA,  # Analog stick -- not sure what best supports this
}
# Support other ways of directly specifying controller inputs in OOTR's character set.
# (This is backwards-compatibility support for ShadowShine57's previous patch.)
CHARACTER_MAP.update(tuple((chr(v), v) for v in CHARACTER_MAP.values()))

# Characters 0x20 thru 0x7D map perfectly.  range() excludes the last element.
CHARACTER_MAP.update((chr(c), c) for c in range(0x20, 0x7e))

# Other characters, source: https://wiki.cloudmodding.com/oot/Text_Format
CHARACTER_MAP.update((c, ix) for ix, c in enumerate(
        (
            '\u203e'             # 0x7f
            'ÀîÂÄÇÈÉÊËÏÔÖÙÛÜß'   # 0x80 .. #0x8f
            'àáâäçèéêëïôöùûü'    # 0x90 .. #0x9e
        ),
        start=0x7f
))

SPECIAL_CHARACTERS = {
    0x9F: '[A]',
    0xA0: '[B]',
    0xA1: '[C]',
    0xA2: '[L]',
    0xA3: '[R]',
    0xA4: '[Z]',
    0xA5: '[C Up]',
    0xA6: '[C Down]',
    0xA7: '[C Left]',
    0xA8: '[C Right]',
    0xA9: '[Triangle]',
    0xAA: '[Control Stick]',
}

REVERSE_MAP = list(chr(x) for x in range(256))

for char, byte in CHARACTER_MAP.items():
    SPECIAL_CHARACTERS.setdefault(byte, char)
    REVERSE_MAP[byte] = char

# [0x0500,0x0560] (inclusive) are reserved for plandomakers
GOSSIP_STONE_MESSAGES = list( range(0x0401, 0x04FF) ) # ids of the actual hints
GOSSIP_STONE_MESSAGES += [0x2053, 0x2054] # shared initial stone messages
TEMPLE_HINTS_MESSAGES = [0x7057, 0x707A] # dungeon reward hints from the temple of time pedestal
GS_TOKEN_MESSAGES = [0x00B4, 0x00B5] # Get Gold Skulltula Token messages
ERROR_MESSAGE = 0x0001

# messages for shorter item messages
# ids are in the space freed up by move_shop_item_messages()
ITEM_MESSAGES = {
    0x0001: "\x08\x06\x30\x05\x41TEXT ID ERROR!\x05\x40",
    0x9001: "\x08\x13\x2DYou borrowed a \x05\x41Pocket Egg\x05\x40!\x01A Pocket Cucco will hatch from\x01it overnight. Be sure to give it\x01back.",
    0x0002: "\x08\x13\x2FYou returned the Pocket Cucco\x01and got \x05\x41Cojiro\x05\x40 in return!\x01Unlike other Cuccos, Cojiro\x01rarely crows.",
    0x0003: "\x08\x13\x30You got an \x05\x41Odd Mushroom\x05\x40!\x01It is sure to spoil quickly! Take\x01it to the Kakariko Potion Shop.",
    0x0004: "\x08\x13\x31You received an \x05\x41Odd Potion\x05\x40!\x01It may be useful for something...\x01Hurry to the Lost Woods!",
    0x0005: "\x08\x13\x32You returned the Odd Potion \x01and got the \x05\x41Poacher's Saw\x05\x40!\x01The young punk guy must have\x01left this.",
    0x0007: "\x08\x13\x48You got a \x01\x05\x41Deku Seeds Bullet Bag\x05\x40.\x01This bag can hold up to \x05\x4640\x05\x40\x01slingshot bullets.",
    0x0008: "\x08\x13\x33You traded the Poacher's Saw \x01for a \x05\x41Broken Goron's Sword\x05\x40!\x01Visit Biggoron to get it repaired!",
    0x0009: "\x08\x13\x34You checked in the Broken \x01Goron's Sword and received a \x01\x05\x41Prescription\x05\x40!\x01Go see King Zora!",
    0x000A: "\x08\x13\x37The Biggoron's Sword...\x01You got a \x05\x41Claim Check \x05\x40for it!\x01You can't wait for the sword!",
    0x000B: "\x08\x13\x2EYou got a \x05\x41Pocket Cucco, \x05\x40one\x01of Anju's prized hens! It fits \x01in your pocket.",
    0x000C: "\x08\x13\x3DYou got the \x05\x41Biggoron's Sword\x05\x40!\x01This blade was forged by a \x01master smith and won't break!",
    0x000D: "\x08\x13\x35You used the Prescription and\x01received an \x05\x41Eyeball Frog\x05\x40!\x01Be quick and deliver it to Lake \x01Hylia!",
    0x000E: "\x08\x13\x36You traded the Eyeball Frog \x01for the \x05\x41World's Finest Eye Drops\x05\x40!\x01Hurry! Take them to Biggoron!",
    0x0010: "\x08\x13\x25You borrowed a \x05\x41Skull Mask\x05\x40.\x01You feel like a monster while you\x01wear this mask!",
    0x0011: "\x08\x13\x26You borrowed a \x05\x41Spooky Mask\x05\x40.\x01You can scare many people\x01with this mask!",
    0x0012: "\x08\x13\x24You borrowed a \x05\x41Keaton Mask\x05\x40.\x01You'll be a popular guy with\x01this mask on!",
    0x0013: "\x08\x13\x27You borrowed a \x05\x41Bunny Hood\x05\x40.\x01The hood's long ears are so\x01cute!",
    0x0014: "\x08\x13\x28You borrowed a \x05\x41Goron Mask\x05\x40.\x01It will make your head look\x01big, though.",
    0x0015: "\x08\x13\x29You borrowed a \x05\x41Zora Mask\x05\x40.\x01With this mask, you can\x01become one of the Zoras!",
    0x0016: "\x08\x13\x2AYou borrowed a \x05\x41Gerudo Mask\x05\x40.\x01This mask will make you look\x01like...a girl?",
    0x0017: "\x08\x13\x2BYou borrowed a \x05\x41Mask of Truth\x05\x40.\x01Show it to many people!",
    0x0030: "\x08\x13\x06You found the \x05\x41Fairy Slingshot\x05\x40!",
    0x0031: "\x08\x13\x03You found the \x05\x41Fairy Bow\x05\x40!",
    0x0032: "\x08\x13\x02You got \x05\x41Bombs\x05\x40!\x01If you see something\x01suspicious, bomb it!",
    0x0033: "\x08\x13\x09You got \x05\x41Bombchus\x05\x40!",
    0x0034: "\x08\x13\x01You got a \x05\x41Deku Nut\x05\x40!",
    0x0035: "\x08\x13\x0EYou found the \x05\x41Boomerang\x05\x40!",
    0x0036: "\x08\x13\x0AYou found the \x05\x41Hookshot\x05\x40!\x01It's a spring-loaded chain that\x01you can cast out to hook things.",
    0x0037: "\x08\x13\x00You got a \x05\x41Deku Stick\x05\x40!",
    0x0038: "\x08\x13\x11You found the \x05\x41Megaton Hammer\x05\x40!\x01It's so heavy, you need to\x01use two hands to swing it!",
    0x0039: "\x08\x13\x0FYou found the \x05\x41Lens of Truth\x05\x40!\x01Mysterious things are hidden\x01everywhere!",
    0x003A: "\x08\x13\x08You found the \x05\x41Ocarina of Time\x05\x40!\x01It glows with a mystical light...",
    0x003C: "\x08\x13\x67You received the \x05\x41Fire\x01Medallion\x05\x40!\x01Darunia awakens as a Sage and\x01adds his power to yours!",
    0x003D: "\x08\x13\x68You received the \x05\x43Water\x01Medallion\x05\x40!\x01Ruto awakens as a Sage and\x01adds her power to yours!",
    0x003E: "\x08\x13\x66You received the \x05\x42Forest\x01Medallion\x05\x40!\x01Saria awakens as a Sage and\x01adds her power to yours!",
    0x003F: "\x08\x13\x69You received the \x05\x46Spirit\x01Medallion\x05\x40!\x01Nabooru awakens as a Sage and\x01adds her power to yours!",
    0x0040: "\x08\x13\x6BYou received the \x05\x44Light\x01Medallion\x05\x40!\x01Rauru the Sage adds his power\x01to yours!",
    0x0041: "\x08\x13\x6AYou received the \x05\x45Shadow\x01Medallion\x05\x40!\x01Impa awakens as a Sage and\x01adds her power to yours!",
    0x0042: "\x08\x13\x14You got an \x05\x41Empty Bottle\x05\x40!\x01You can put something in this\x01bottle.",
    0x0043: "\x08\x13\x15You got a \x05\x41Red Potion\x05\x40!\x01It will restore your health",
    0x0044: "\x08\x13\x16You got a \x05\x42Green Potion\x05\x40!\x01It will restore your magic.",
    0x0045: "\x08\x13\x17You got a \x05\x43Blue Potion\x05\x40!\x01It will recover your health\x01and magic.",
    0x0046: "\x08\x13\x18You caught a \x05\x41Fairy\x05\x40 in a bottle!\x01It will revive you\x01the moment you run out of life \x01energy.",
    0x0047: "\x08\x13\x19You got a \x05\x41Fish\x05\x40!\x01It looks so fresh and\x01delicious!",
    0x0048: "\x08\x13\x10You got a \x05\x41Magic Bean\x05\x40!\x01Find a suitable spot for a garden\x01and plant it.",
    0x9048: "\x08\x13\x10You got a \x05\x41Pack of Magic Beans\x05\x40!\x01Find suitable spots for a garden\x01and plant them.",
    0x004A: "\x08\x13\x07You received the \x05\x41Fairy Ocarina\x05\x40!\x01This is a memento from Saria.",
    0x004B: "\x08\x13\x3DYou got the \x05\x42Giant's Knife\x05\x40!\x01Hold it with both hands to\x01attack! It's so long, you\x01can't use it with a \x05\x44shield\x05\x40.",
    0x004C: "\x08\x13\x3EYou got a \x05\x44Deku Shield\x05\x40!",
    0x004D: "\x08\x13\x3FYou got a \x05\x44Hylian Shield\x05\x40!",
    0x004E: "\x08\x13\x40You found the \x05\x44Mirror Shield\x05\x40!\x01The shield's polished surface can\x01reflect light or energy.",
    0x004F: "\x08\x13\x0BYou found the \x05\x41Longshot\x05\x40!\x01It's an upgraded Hookshot.\x01It extends \x05\x41twice\x05\x40 as far!",
    0x0050: "\x08\x13\x42You got a \x05\x41Goron Tunic\x05\x40!\x01Going to a hot place? No worry!",
    0x0051: "\x08\x13\x43You got a \x05\x43Zora Tunic\x05\x40!\x01Wear it, and you won't drown\x01underwater.",
    0x0052: "\x08You got a \x05\x42Magic Jar\x05\x40!\x01Your Magic Meter is filled!",
    0x0053: "\x08\x13\x45You got the \x05\x41Iron Boots\x05\x40!\x01So heavy, you can't run.\x01So heavy, you can't float.",
    0x0054: "\x08\x13\x46You got the \x05\x41Hover Boots\x05\x40!\x01With these mysterious boots\x01you can hover above the ground.",
    0x0055: "\x08You got a \x05\x45Recovery Heart\x05\x40!\x01Your life energy is recovered!",
    0x0056: "\x08\x13\x4BYou upgraded your quiver to a\x01\x05\x41Big Quiver\x05\x40!\x01Now you can carry more arrows-\x01\x05\x4640 \x05\x40in total!",
    0x0057: "\x08\x13\x4CYou upgraded your quiver to\x01the \x05\x41Biggest Quiver\x05\x40!\x01Now you can carry to a\x01maximum of \x05\x4650\x05\x40 arrows!",
    0x0058: "\x08\x13\x4DYou found a \x05\x41Bomb Bag\x05\x40!\x01You found \x05\x4120 Bombs\x05\x40 inside!",
    0x0059: "\x08\x13\x4EYou got a \x05\x41Big Bomb Bag\x05\x40!\x01Now you can carry more \x01Bombs, up to a maximum of \x05\x4630\x05\x40!",
    0x005A: "\x08\x13\x4FYou got the \x01\x05\x41Biggest Bomb Bag\x05\x40!\x01Now, you can carry up to \x01\x05\x4640\x05\x40 Bombs!",
    0x005B: "\x08\x13\x51You found the \x05\x43Silver Gauntlets\x05\x40!\x01You feel the power to lift\x01big things with it!",
    0x005C: "\x08\x13\x52You found the \x05\x43Golden Gauntlets\x05\x40!\x01You can feel even more power\x01coursing through your arms!",
    0x005D: "\x08\x13\x1CYou put a \x05\x44Blue Fire\x05\x40\x01into the bottle!\x01This is a cool flame you can\x01use on red ice.",
    0x005E: "\x08\x13\x56You got an \x05\x43Adult's Wallet\x05\x40!\x01Now you can hold\x01up to \x05\x46200\x05\x40 \x05\x46Rupees\x05\x40.",
    0x005F: "\x08\x13\x57You got a \x05\x43Giant's Wallet\x05\x40!\x01Now you can hold\x01up to \x05\x46500\x05\x40 \x05\x46Rupees\x05\x40.",
    0x0060: "\x08\x13\x77You found a \x05\x41Small Key\x05\x40!\x01This key will open a locked \x01door. You can use it only\x01in this dungeon.",
    0x0066: "\x08\x13\x76You found the \x05\x41Dungeon Map\x05\x40!\x01It's the map to this dungeon.",
    0x0067: "\x08\x13\x75You found the \x05\x41Compass\x05\x40!\x01Now you can see the locations\x01of many hidden things in the\x01dungeon!",
    0x0068: "\x08\x13\x6FYou obtained the \x05\x41Stone of Agony\x05\x40!\x01If you equip a \x05\x44Rumble Pak\x05\x40, it\x01will react to nearby...secrets.",
    0x0069: "\x08\x13\x23You received \x05\x41Zelda's Letter\x05\x40!\x01Wow! This letter has Princess\x01Zelda's autograph!",
    0x006C: "\x08\x13\x49Your \x05\x41Deku Seeds Bullet Bag \x01\x05\x40has become bigger!\x01This bag can hold \x05\x4650\x05\x41 \x05\x40bullets!",
    0x006F: "\x08You got a \x05\x42Green Rupee\x05\x40!\x01That's \x05\x42one Rupee\x05\x40!",
    0x0070: "\x08\x13\x04You got the \x05\x41Fire Arrow\x05\x40!\x01If you hit your target,\x01it will catch fire.",
    0x0071: "\x08\x13\x0CYou got the \x05\x43Ice Arrow\x05\x40!\x01If you hit your target,\x01it will freeze.",
    0x0072: "\x08\x13\x12You got the \x05\x44Light Arrow\x05\x40!\x01The light of justice\x01will smite evil!",
    0x0073: "\x08\x06\x28You have learned the\x01\x06\x2F\x05\x42Minuet of Forest\x05\x40!",
    0x0074: "\x08\x06\x28You have learned the\x01\x06\x37\x05\x41Bolero of Fire\x05\x40!",
    0x0075: "\x08\x06\x28You have learned the\x01\x06\x29\x05\x43Serenade of Water\x05\x40!",
    0x0076: "\x08\x06\x28You have learned the\x01\x06\x2D\x05\x46Requiem of Spirit\x05\x40!",
    0x0077: "\x08\x06\x28You have learned the\x01\x06\x28\x05\x45Nocturne of Shadow\x05\x40!",
    0x0078: "\x08\x06\x28You have learned the\x01\x06\x32\x05\x44Prelude of Light\x05\x40!",
    0x0079: "\x08\x13\x50You got the \x05\x41Goron's Bracelet\x05\x40!\x01Now you can pull up Bomb\x01Flowers.",
    0x007A: "\x08\x13\x1DYou put a \x05\x41Bug \x05\x40in the bottle!\x01This kind of bug prefers to\x01live in small holes in the ground.",
    0x007B: "\x08\x13\x70You obtained the \x05\x41Gerudo's \x01Membership Card\x05\x40!\x01You can get into the Gerudo's\x01training ground.",
    0x0080: "\x08\x13\x6CYou got the \x05\x42Kokiri's Emerald\x05\x40!\x01This is the Spiritual Stone of \x01Forest passed down by the\x01Great Deku Tree.",
    0x0081: "\x08\x13\x6DYou obtained the \x05\x41Goron's Ruby\x05\x40!\x01This is the Spiritual Stone of \x01Fire passed down by the Gorons!",
    0x0082: "\x08\x13\x6EYou obtained \x05\x43Zora's Sapphire\x05\x40!\x01This is the Spiritual Stone of\x01Water passed down by the\x01Zoras!",
    0x0090: "\x08\x13\x00Now you can pick up \x01many \x05\x41Deku Sticks\x05\x40!\x01You can carry up to \x05\x4620\x05\x40 of them!",
    0x0091: "\x08\x13\x00You can now pick up \x01even more \x05\x41Deku Sticks\x05\x40!\x01You can carry up to \x05\x4630\x05\x40 of them!",
    0x0097: "\x08\x13\x20You caught a \x05\x41Poe \x05\x40in a bottle!\x01Something good might happen!",
    0x0098: "\x08\x13\x1AYou got \x05\x41Lon Lon Milk\x05\x40!\x01This milk is very nutritious!\x01There are two drinks in it.",
    0x0099: "\x08\x13\x1BYou found \x05\x41Ruto's Letter\x05\x40 in a\x01bottle! Show it to King Zora.",
    0x9099: "\x08\x13\x1BYou found \x05\x41a letter in a bottle\x05\x40!\x01You remove the letter from the\x01bottle, freeing it for other uses.",
    0x009A: "\x08\x13\x21You got a \x05\x41Weird Egg\x05\x40!\x01Feels like there's something\x01moving inside!",
    0x00A4: "\x08\x13\x3BYou got the \x05\x42Kokiri Sword\x05\x40!\x01This is a hidden treasure of\x01the Kokiri.",
    0x00A7: "\x08\x13\x01Now you can carry\x01many \x05\x41Deku Nuts\x05\x40!\x01You can hold up to \x05\x4630\x05\x40 nuts!",
    0x00A8: "\x08\x13\x01You can now carry even\x01more \x05\x41Deku Nuts\x05\x40! You can carry\x01up to \x05\x4640\x05\x41 \x05\x40nuts!",
    0x00AD: "\x08\x13\x05You got \x05\x41Din's Fire\x05\x40!\x01Its fireball engulfs everything!",
    0x00AE: "\x08\x13\x0DYou got \x05\x42Farore's Wind\x05\x40!\x01This is warp magic you can use!",
    0x00AF: "\x08\x13\x13You got \x05\x43Nayru's Love\x05\x40!\x01Cast this to create a powerful\x01protective barrier.",
    0x00B4: "\x08You got a \x05\x41Gold Skulltula Token\x05\x40!\x01You've collected \x05\x41\x19\x05\x40 tokens in total.",
    0x00B5: "\x08You destroyed a \x05\x41Gold Skulltula\x05\x40.\x01You got a token proving you \x01destroyed it!", #Unused
    0x00C2: "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01Collect four pieces total to get\x01another Heart Container.",
    0x90C2: "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01You are already at\x01maximum health.",
    0x00C3: "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01So far, you've collected two \x01pieces.",
    0x00C4: "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01Now you've collected three \x01pieces!",
    0x00C5: "\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01You've completed another Heart\x01Container!",
    0x00C6: "\x08\x13\x72You got a \x05\x41Heart Container\x05\x40!\x01Your maximum life energy is \x01increased by one heart.",
    0x90C6: "\x08\x13\x72You got a \x05\x41Heart Container\x05\x40!\x01You are already at\x01maximum health.",
    0x00C7: "\x08\x13\x74You got the \x05\x41Boss Key\x05\x40!\x01Now you can get inside the \x01chamber where the Boss lurks.",
    0x00CC: "\x08You got a \x05\x43Blue Rupee\x05\x40!\x01That's \x05\x43five Rupees\x05\x40!",
    0x00CD: "\x08\x13\x53You got the \x05\x43Silver Scale\x05\x40!\x01You can dive deeper than you\x01could before.",
    0x00CE: "\x08\x13\x54You got the \x05\x43Golden Scale\x05\x40!\x01Now you can dive much\x01deeper than you could before!",
    0x00D1: "\x08\x06\x14You've learned \x05\x42Saria's Song\x05\x40!",
    0x00D2: "\x08\x06\x11You've learned \x05\x41Epona's Song\x05\x40!",
    0x00D3: "\x08\x06\x0BYou've learned the \x05\x46Sun's Song\x05\x40!",
    0x00D4: "\x08\x06\x15You've learned \x05\x43Zelda's Lullaby\x05\x40!",
    0x00D5: "\x08\x06\x05You've learned the \x05\x44Song of Time\x05\x40!",
    0x00D6: "\x08You've learned the \x05\x45Song of Storms\x05\x40!",
    0x00DC: "\x08\x13\x58You got \x05\x41Deku Seeds\x05\x40!\x01Use these as bullets\x01for your Slingshot.",
    0x00DD: "\x08You mastered the secret sword\x01technique of the \x05\x41Spin Attack\x05\x40!",
    0x00E4: "\x08You can now use \x05\x42Magic\x05\x40!",
    0x00E5: "\x08Your \x05\x44defensive power\x05\x40 is enhanced!",
    0x00E6: "\x08You got a \x05\x46bundle of arrows\x05\x40!",
    0x00E8: "\x08Your magic power has been \x01enhanced! Now you have twice\x01as much \x05\x41Magic Power\x05\x40!",
    0x00E9: "\x08Your defensive power has been \x01enhanced! Damage inflicted by \x01enemies will be \x05\x41reduced by half\x05\x40.",
    0x00F0: "\x08You got a \x05\x41Red Rupee\x05\x40!\x01That's \x05\x41twenty Rupees\x05\x40!",
    0x00F1: "\x08You got a \x05\x45Purple Rupee\x05\x40!\x01That's \x05\x45fifty Rupees\x05\x40!",
    0x00F2: "\x08You got a \x05\x46Huge Rupee\x05\x40!\x01This Rupee is worth a whopping\x01\x05\x46two hundred Rupees\x05\x40!",
    0x00F9: "\x08\x13\x1EYou put a \x05\x41Big Poe \x05\x40in a bottle!\x01Let's sell it at the \x05\x41Ghost Shop\x05\x40!\x01Something good might happen!",
    0x00FA: "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01Collect four pieces total to get\x01another Heart Container.",
    0x00FB: "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01So far, you've collected two \x01pieces.",
    0x00FC: "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01Now you've collected three \x01pieces!",
    0x00FD: "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01You've completed another Heart\x01Container!",
    0x90FA: "\x08\x06\x49\x05\x41WINNER\x05\x40!\x04\x08\x13\x73You got a \x05\x41Piece of Heart\x05\x40!\x01You are already at\x01maximum health.",
    0x9002: "\x08You are a \x05\x43FOOL\x05\x40!",
    0x9003: "\x08You found a piece of the \x05\x41Triforce\x05\x40!",
    0x9097: "\x08You got an \x05\x41Archipelago item\x05\x40!\x01It seems \x05\x41important\x05\x40!",
    0x9098: "\x08You got an \x05\x43Archipelago item\x05\x40!\x01Doesn't seem like it's needed.",
}

KEYSANITY_MESSAGES = {
    0x001C: "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09",
    0x0006: "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09",
    0x001D: "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09",
    0x001E: "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09",
    0x002A: "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09",
    0x0061: "\x13\x74\x08You got the \x05\x41Boss Key\x05\x40\x01for \x05\x41Ganon's Castle\x05\x40!\x09",
    0x0062: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x42Deku Tree\x05\x40!\x09",
    0x0063: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for \x05\x41Dodongo's Cavern\x05\x40!\x09",
    0x0064: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for \x05\x43Jabu Jabu's Belly\x05\x40!\x09",
    0x0065: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09",
    0x007C: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09",
    0x007D: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09",
    0x007E: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09",
    0x007F: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09",
    0x0087: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x44Ice Cavern\x05\x40!\x09",
    0x0088: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x42Deku Tree\x05\x40!\x09",
    0x0089: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for \x05\x41Dodongo's Cavern\x05\x40!\x09",
    0x008A: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for \x05\x43Jabu Jabu's Belly\x05\x40!\x09",
    0x008B: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09",
    0x008C: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09",
    0x008E: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09",
    0x008F: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09",
    0x0092: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x44Ice Cavern\x05\x40!\x09",
    0x0093: "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09",
    0x0094: "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09",
    0x0095: "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09",
    0x009B: "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09",
    0x009F: "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x46Gerudo Training\x01Ground\x05\x40!\x09",
    0x00A0: "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x46Thieves' Hideout\x05\x40!\x09",
    0x00A1: "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for \x05\x41Ganon's Castle\x05\x40!\x09",
    0x00A2: "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09",
    0x00A3: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09",
    0x00A5: "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09",
    0x00A6: "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09",
    0x00A9: "\x13\x77\x08You found a \x05\x41Small Key\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09",
    0x9010: "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for the \x05\x42Forest Temple\x05\x40!\x09",
    0x9011: "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for the \x05\x41Fire Temple\x05\x40!\x09",
    0x9012: "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for the \x05\x43Water Temple\x05\x40!\x09",
    0x9013: "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for the \x05\x46Spirit Temple\x05\x40!\x09",
    0x9014: "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for the \x05\x45Shadow Temple\x05\x40!\x09",
    0x9015: "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for the \x05\x45Bottom of the Well\x05\x40!\x09",
    0x9016: "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for the \x05\x46Gerudo Training\x01Ground\x05\x40!\x09",
    0x9017: "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for the \x05\x46Thieves' Hideout\x05\x40!\x09",
    0x9018: "\x13\x77\x08You found a \x05\x41Small Key Ring\x05\x40\x01for \x05\x41Ganon's Castle\x05\x40!\x09",
}

COLOR_MAP = {
    'White':      '\x40',
    'Red':        '\x41',
    'Green':      '\x42',
    'Blue':       '\x43',
    'Light Blue': '\x44',
    'Pink':       '\x45',
    'Yellow':     '\x46',
    'Black':      '\x47',
}

MISC_MESSAGES = {
    0x507B: (bytearray(
            b"\x08I tell you, I saw him!\x04" \
            b"\x08I saw the ghostly figure of Damp\x96\x01" \
            b"the gravekeeper sinking into\x01" \
            b"his grave. It looked like he was\x01" \
            b"holding some kind of \x05\x41treasure\x05\x40!\x02"
            ), None),
    0x0422: ("They say that once \x05\x41Morpha's Curse\x05\x40\x01is lifted, striking \x05\x42this stone\x05\x40 can\x01shift the tides of \x05\x44Lake Hylia\x05\x40.\x02", 0x23),
    0x401C: ("Please find my dear \05\x41Princess Ruto\x05\x40\x01immediately... Zora!\x12\x68\x7A", 0x23),
    0x9100: ("I am out of goods now.\x01Sorry!\x04The mark that will lead you to\x01the Spirit Temple is the \x05\x41flag on\x01the left \x05\x40outside the shop.\x01Be seeing you!\x02", 0x00),
    0x0451: ("\x12\x68\x7AMweep\x07\x04\x52", 0x23),
    0x0452: ("\x12\x68\x7AMweep\x07\x04\x53", 0x23),
    0x0453: ("\x12\x68\x7AMweep\x07\x04\x54", 0x23),
    0x0454: ("\x12\x68\x7AMweep\x07\x04\x55", 0x23),
    0x0455: ("\x12\x68\x7AMweep\x07\x04\x56", 0x23),
    0x0456: ("\x12\x68\x7AMweep\x07\x04\x57", 0x23),
    0x0457: ("\x12\x68\x7AMweep\x07\x04\x58", 0x23),
    0x0458: ("\x12\x68\x7AMweep\x07\x04\x59", 0x23),
    0x0459: ("\x12\x68\x7AMweep\x07\x04\x5A", 0x23),
    0x045A: ("\x12\x68\x7AMweep\x07\x04\x5B", 0x23),
    0x045B: ("\x12\x68\x7AMweep", 0x23)
}


# convert byte array to an integer
def bytes_to_int(bytes, signed=False):
    return int.from_bytes(bytes, byteorder='big', signed=signed)


# convert int to an array of bytes of the given width
def int_to_bytes(num, width, signed=False):
    return int.to_bytes(num, width, byteorder='big', signed=signed)


def display_code_list(codes):
    message = ""
    for code in codes:
        message += str(code)
    return message


def encode_text_string(text):
    result = []
    it = iter(text)
    for ch in it:
        n = ord(ch)
        mapped = CHARACTER_MAP.get(ch)
        if mapped:
            result.append(mapped)
            continue
        if n in CONTROL_CODES:
            result.append(n)
            for _ in range(CONTROL_CODES[n][1]):
                result.append(ord(next(it)))
            continue
        if n in CHARACTER_MAP.values(): # Character has already been translated
            result.append(n)
            continue
        raise ValueError(f"While encoding {text!r}: Unable to translate unicode character {ch!r} ({n}).  (Already decoded: {result!r})")
    return result


def parse_control_codes(text):
    if isinstance(text, list):
        bytes = text
    elif isinstance(text, bytearray):
        bytes = list(text)
    else:
        bytes = encode_text_string(text)

    text_codes = []
    index = 0
    while index < len(bytes):
        next_char = bytes[index]
        data = 0
        index += 1
        if next_char in CONTROL_CODES:
            extra_bytes = CONTROL_CODES[next_char][1]
            if extra_bytes > 0:
                data = bytes_to_int(bytes[index : index + extra_bytes])
                index += extra_bytes
        text_code = Text_Code(next_char, data)
        text_codes.append(text_code)
        if text_code.code == 0x02:  # message end code
            break

    return text_codes


# holds a single character or control code of a string
class Text_Code:
    def display(self):
        if self.code in CONTROL_CODES:
            return CONTROL_CODES[self.code][2](self.data)
        elif self.code in SPECIAL_CHARACTERS:
            return SPECIAL_CHARACTERS[self.code]
        elif self.code >= 0x7F:
            return '?'
        else:
            return chr(self.code)

    def get_python_string(self):
        if self.code in CONTROL_CODES:
            ret = ''
            subdata = self.data
            for _ in range(0, CONTROL_CODES[self.code][1]):
                ret = ('\\x%02X' % (subdata & 0xFF)) + ret
                subdata = subdata >> 8
            ret = '\\x%02X' % self.code + ret
            return ret
        elif self.code in SPECIAL_CHARACTERS:
            return '\\x%02X' % self.code
        elif self.code >= 0x7F:
            return '?'
        else:
            return chr(self.code)

    def get_string(self):
        if self.code in CONTROL_CODES:
            ret = ''
            subdata = self.data
            for _ in range(0, CONTROL_CODES[self.code][1]):
                ret = chr(subdata & 0xFF) + ret
                subdata = subdata >> 8
            ret = chr(self.code) + ret
            return ret
        else:
            # raise ValueError(repr(REVERSE_MAP))
            return REVERSE_MAP[self.code]

    # writes the code to the given offset, and returns the offset of the next byte
    def size(self):
        size = 1
        if self.code in CONTROL_CODES:
            size += CONTROL_CODES[self.code][1]
        return size

    # writes the code to the given offset, and returns the offset of the next byte
    def write(self, rom, offset):
        rom.write_byte(TEXT_START + offset, self.code)

        extra_bytes = 0
        if self.code in CONTROL_CODES:
            extra_bytes = CONTROL_CODES[self.code][1]
            bytes_to_write = int_to_bytes(self.data, extra_bytes)
            rom.write_bytes(TEXT_START + offset + 1, bytes_to_write)

        return offset + 1 + extra_bytes

    def __init__(self, code, data):
        self.code = code
        if code in CONTROL_CODES:
            self.type = CONTROL_CODES[code][0]
        else:
            self.type = 'character'
        self.data = data

    __str__ = __repr__ = display


# holds a single message, and all its data
class Message:
    def display(self):
        meta_data = [
            "#" + str(self.index),
            "ID: 0x" + "{:04x}".format(self.id),
            "Offset: 0x" + "{:06x}".format(self.offset),
            "Length: 0x" + "{:04x}".format(self.unpadded_length) + "/0x" + "{:04x}".format(self.length),
            "Box Type: " + str(self.box_type),
            "Postion: " + str(self.position)
        ]
        return ', '.join(meta_data) + '\n' + self.text

    def get_python_string(self):
        ret = ''
        for code in self.text_codes:
            ret = ret + code.get_python_string()
        return ret

    # check if this is an unused message that just contains it's own id as text
    def is_id_message(self):
        if self.unpadded_length != 5:
            return False
        for i in range(4):
            code = self.text_codes[i].code
            if not (
                    code in range(ord('0'), ord('9')+1)
                    or code in range(ord('A'), ord('F')+1)
                    or code in range(ord('a'), ord('f')+1)
            ):
                return False
        return True

    def parse_text(self):
        self.text_codes = parse_control_codes(self.raw_text)

        index = 0
        for text_code in self.text_codes:
            index += text_code.size()
            if text_code.code == 0x02:  # message end code
                break
            if text_code.code == 0x07:  # goto
                self.has_goto = True
                self.ending = text_code
            if text_code.code == 0x0A:  # keep-open
                self.has_keep_open = True
                self.ending = text_code
            if text_code.code == 0x0B:  # event
                self.has_event = True
                self.ending = text_code
            if text_code.code == 0x0E:  # fade out
                self.has_fade = True
                self.ending = text_code
            if text_code.code == 0x10:  # ocarina
                self.has_ocarina = True
                self.ending = text_code
            if text_code.code == 0x1B:  # two choice
                self.has_two_choice = True
            if text_code.code == 0x1C:  # three choice
                self.has_three_choice = True
        self.text = display_code_list(self.text_codes)
        self.unpadded_length = index

    def is_basic(self):
        return not (self.has_goto or self.has_keep_open or self.has_event or self.has_fade or self.has_ocarina or self.has_two_choice or self.has_three_choice)

    # computes the size of a message, including padding
    def size(self):
        size = 0

        for code in self.text_codes:
            size += code.size()

        size = (size + 3) & -4 # align to nearest 4 bytes

        return size
    
    # applies whatever transformations we want to the dialogs
    def transform(self, replace_ending=False, ending=None, always_allow_skip=True, speed_up_text=True):
        ending_codes = [0x02, 0x07, 0x0A, 0x0B, 0x0E, 0x10]
        box_breaks = [0x04, 0x0C]
        slows_text = [0x08, 0x09, 0x14]
        slow_icons = [0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x04, 0x02]

        text_codes = []
        instant_text_code = Text_Code(0x08, 0)

        # # speed the text
        if speed_up_text:
            text_codes.append(instant_text_code) # allow instant

        # write the message
        for code in self.text_codes:
            # ignore ending codes if it's going to be replaced
            if replace_ending and code.code in ending_codes:
                pass
            # ignore the "make unskippable flag"
            elif always_allow_skip and code.code == 0x1A:
                pass
            # ignore anything that slows down text
            elif speed_up_text and code.code in slows_text:
                pass
            elif speed_up_text and code.code in box_breaks:
                # some special cases for text that needs to be on a timer
                if (self.id == 0x605A or  # twinrova transformation
                    self.id == 0x706C or  # rauru ending text
                    self.id == 0x70DD or  # ganondorf ending text
                    self.id in (0x706F, 0x7091, 0x7092, 0x7093, 0x7094, 0x7095, 0x7070)  # zelda ending text
                ):
                    text_codes.append(code)
                    text_codes.append(instant_text_code)  # allow instant
                else:
                    text_codes.append(Text_Code(0x04, 0))  # un-delayed break
                    text_codes.append(instant_text_code)  # allow instant
            elif speed_up_text and code.code == 0x13 and code.data in slow_icons:
                text_codes.append(code)
                text_codes.pop(find_last(text_codes, instant_text_code))  # remove last instance of instant text
                text_codes.append(instant_text_code)  # allow instant
            else:
                text_codes.append(code)

        if replace_ending:
            if ending:
                if speed_up_text and ending.code == 0x10:  # ocarina
                    text_codes.append(Text_Code(0x09, 0))  # disallow instant text
                text_codes.append(ending)  # write special ending
            text_codes.append(Text_Code(0x02, 0))  # write end code

        self.text_codes = text_codes

    # writes a Message back into the rom, using the given index and offset to update the table
    # returns the offset of the next message
    def write(self, rom, index, offset):
        # construct the table entry
        id_bytes = int_to_bytes(self.id, 2)
        offset_bytes = int_to_bytes(offset, 3)
        entry = id_bytes + bytes([self.opts, 0x00, 0x07]) + offset_bytes
        # write it back
        entry_offset = EXTENDED_TABLE_START + 8 * index
        rom.write_bytes(entry_offset, entry)

        for code in self.text_codes:
            offset = code.write(rom, offset)

        while offset % 4 > 0:
            offset = Text_Code(0x00, 0).write(rom, offset) # pad to 4 byte align

        return offset


    def __init__(self, raw_text, index, id, opts, offset, length):
        self.raw_text = raw_text

        self.index = index
        self.id = id
        self.opts = opts  # Textbox type and y position
        self.box_type = (self.opts & 0xF0) >> 4
        self.position = (self.opts & 0x0F)
        self.offset = offset
        self.length = length

        self.has_goto = False
        self.has_keep_open = False
        self.has_event = False
        self.has_fade = False
        self.has_ocarina = False
        self.has_two_choice = False
        self.has_three_choice = False
        self.ending = None

        self.parse_text()

    # read a single message from rom
    @classmethod
    def from_rom(cls, rom, index):
        entry_offset = ENG_TABLE_START + 8 * index
        entry = rom.read_bytes(entry_offset, 8)
        next = rom.read_bytes(entry_offset + 8, 8)

        id = bytes_to_int(entry[0:2])
        opts = entry[2]
        offset = bytes_to_int(entry[5:8])
        length = bytes_to_int(next[5:8]) - offset

        raw_text = rom.read_bytes(TEXT_START + offset, length)

        return cls(raw_text, index, id, opts, offset, length)

    @classmethod
    def from_string(cls, text, id=0, opts=0x00):
        bytes = text + "\x02"
        return cls(bytes, 0, id, opts, 0, len(bytes) + 1)

    @classmethod
    def from_bytearray(cls, bytearray, id=0, opts=0x00):
        bytes = list(bytearray) + [0x02]

        return cls(bytes, 0, id, opts, 0, len(bytes) + 1)

    __str__ = __repr__ = display

# wrapper for updating the text of a message, given its message id
# if the id does not exist in the list, then it will add it
def update_message_by_id(messages, id, text, opts=None):
    # get the message index
    index = next( (m.index for m in messages if m.id == id), -1)
    # update if it was found
    if index >= 0:
        update_message_by_index(messages, index, text, opts)
    else:
        add_message(messages, text, id, opts)

# Gets the message by its ID. Returns None if the index does not exist
def get_message_by_id(messages, id):
    # get the message index
    index = next( (m.index for m in messages if m.id == id), -1)
    if index >= 0:
        return messages[index]
    else:
        return None

# wrapper for updating the text of a message, given its index in the list
def update_message_by_index(messages, index, text, opts=None):
    if opts is None:
        opts = messages[index].opts

    if isinstance(text, bytearray):
        messages[index] = Message.from_bytearray(text, messages[index].id, opts)
    else:
        messages[index] = Message.from_string(text, messages[index].id, opts)
    messages[index].index = index

# wrapper for adding a string message to a list of messages
def add_message(messages, text, id=0, opts=0x00):
    if isinstance(text, bytearray):
        messages.append( Message.from_bytearray(text, id, opts) )
    else:
        messages.append( Message.from_string(text, id, opts) )
    messages[-1].index = len(messages) - 1

# holds a row in the shop item table (which contains pointers to the description and purchase messages)
class Shop_Item():

    def display(self):
        meta_data = ["#" + str(self.index),
         "Item: 0x" + "{:04x}".format(self.get_item_id),
         "Price: " + str(self.price),
         "Amount: " + str(self.pieces),
         "Object: 0x" + "{:04x}".format(self.object),
         "Model: 0x" + "{:04x}".format(self.model),
         "Description: 0x" + "{:04x}".format(self.description_message),
         "Purchase: 0x" + "{:04x}".format(self.purchase_message),]
        func_data = [
         "func1: 0x" + "{:08x}".format(self.func1),
         "func2: 0x" + "{:08x}".format(self.func2),
         "func3: 0x" + "{:08x}".format(self.func3),
         "func4: 0x" + "{:08x}".format(self.func4),]
        return ', '.join(meta_data) + '\n' + ', '.join(func_data)

    # write the shop item back
    def write(self, rom, shop_table_address, index):

        entry_offset = shop_table_address + 0x20 * index

        bytes = []
        bytes += int_to_bytes(self.object, 2)
        bytes += int_to_bytes(self.model, 2)
        bytes += int_to_bytes(self.func1, 4)
        bytes += int_to_bytes(self.price, 2, signed=True)
        bytes += int_to_bytes(self.pieces, 2)
        bytes += int_to_bytes(self.description_message, 2)
        bytes += int_to_bytes(self.purchase_message, 2)
        bytes += [0x00, 0x00]
        bytes += int_to_bytes(self.get_item_id, 2)
        bytes += int_to_bytes(self.func2, 4)
        bytes += int_to_bytes(self.func3, 4)
        bytes += int_to_bytes(self.func4, 4)

        rom.write_bytes(entry_offset, bytes)

    # read a single message
    def __init__(self, rom, shop_table_address, index):

        entry_offset = shop_table_address + 0x20 * index
        entry = rom.read_bytes(entry_offset, 0x20)

        self.index = index
        self.object = bytes_to_int(entry[0x00:0x02])
        self.model = bytes_to_int(entry[0x02:0x04])
        self.func1 = bytes_to_int(entry[0x04:0x08])
        self.price = bytes_to_int(entry[0x08:0x0A])
        self.pieces = bytes_to_int(entry[0x0A:0x0C])
        self.description_message = bytes_to_int(entry[0x0C:0x0E])
        self.purchase_message = bytes_to_int(entry[0x0E:0x10])
        # 0x10-0x11 is always 0000 padded apparently
        self.get_item_id = bytes_to_int(entry[0x12:0x14])
        self.func2 = bytes_to_int(entry[0x14:0x18])
        self.func3 = bytes_to_int(entry[0x18:0x1C])
        self.func4 = bytes_to_int(entry[0x1C:0x20])

    __str__ = __repr__ = display

# reads each of the shop items
def read_shop_items(rom, shop_table_address):
    shop_items = []

    for index in range(0, 100):
        shop_items.append( Shop_Item(rom, shop_table_address, index) )

    return shop_items

# writes each of the shop item back into rom
def write_shop_items(rom, shop_table_address, shop_items):
    for s in shop_items:
        s.write(rom, shop_table_address, s.index)

# these are unused shop items, and contain text ids that are used elsewhere, and should not be moved
SHOP_ITEM_EXCEPTIONS = [0x0A, 0x0B, 0x11, 0x12, 0x13, 0x14, 0x29]

# returns a set of all message ids used for shop items
def get_shop_message_id_set(shop_items):
    ids = set()
    for shop in shop_items:
        if shop.index not in SHOP_ITEM_EXCEPTIONS:
            ids.add(shop.description_message)
            ids.add(shop.purchase_message)
    return ids

# remove all messages that easy to tell are unused to create space in the message index table
def remove_unused_messages(messages):
    messages[:] = [m for m in messages if not m.is_id_message()]
    for index, m in enumerate(messages):
        m.index = index

# takes all messages used for shop items, and moves messages from the 00xx range into the unused 80xx range
def move_shop_item_messages(messages, shop_items):
    # checks if a message id is in the item message range
    def is_in_item_range(id):
        bytes = int_to_bytes(id, 2)
        return bytes[0] == 0x00
    # get the ids we want to move
    ids = set( id for id in get_shop_message_id_set(shop_items) if is_in_item_range(id) )
    # update them in the message list
    for id in ids:
        # should be a singleton list, but in case something funky is going on, handle it as a list regardless
        relevant_messages = [message for message in messages if message.id == id]
        if len(relevant_messages) >= 2:
            raise(TypeError("duplicate id in move_shop_item_messages"))

        for message in relevant_messages:
            message.id |= 0x8000
    # update them in the shop item list
    for shop in shop_items:
        if is_in_item_range(shop.description_message):
            shop.description_message |= 0x8000
        if is_in_item_range(shop.purchase_message):
            shop.purchase_message |= 0x8000

def make_player_message(text):
    player_text = '\x05\x42\x0F\x05\x40'
    pronoun_mapping = {
        "You have ": player_text + " ",
        "You are ":  player_text + " is ",
        "You've ":   player_text + " ",
        "Your ":     player_text + "'s ",
        "You ":      player_text + " ",

        "you have ": player_text + " ",
        "you are ":  player_text + " is ",
        "you've ":   player_text + " ",
        "your ":     player_text + "'s ",
        "you ":      player_text + " ",
    }

    verb_mapping = {
        'obtained ': 'got ',
        'received ': 'got ',
        'learned ':  'got ',
        'borrowed ': 'got ',
        'found ':    'got ',
    }

    new_text = text

    # Replace the first instance of a 'You' with the player name
    lower_text = text.lower()
    you_index = lower_text.find('you')
    if you_index != -1:
        for find_text, replace_text in pronoun_mapping.items():
            # if the index do not match, then it is not the first 'You'
            if text.find(find_text) == you_index:
                new_text = new_text.replace(find_text, replace_text, 1)
                break

    # because names are longer, we shorten the verbs to they fit in the textboxes better
    for find_text, replace_text in verb_mapping.items():
        new_text = new_text.replace(find_text, replace_text)

    wrapped_text = line_wrap(new_text, False, False, False)
    if wrapped_text != new_text:
        new_text = line_wrap(new_text, True, False, False)

    return new_text


# reduce item message sizes and add new item messages
# make sure to call this AFTER move_shop_item_messages()
def update_item_messages(messages, world):
    new_item_messages = {**ITEM_MESSAGES, **KEYSANITY_MESSAGES}
    for id, text in new_item_messages.items():
        if world.multiworld.players > 1:
            update_message_by_id(messages, id, make_player_message(text), 0x23)
        else:
            update_message_by_id(messages, id, text, 0x23)

    for id, (text, opt) in MISC_MESSAGES.items():
        update_message_by_id(messages, id, text, opt)


# run all keysanity related patching to add messages for dungeon specific items
def add_item_messages(messages, shop_items, world):
    move_shop_item_messages(messages, shop_items)
    update_item_messages(messages, world)


# reads each of the game's messages into a list of Message objects
def read_messages(rom):
    table_offset = ENG_TABLE_START
    index = 0
    messages = []
    while True:
        entry = rom.read_bytes(table_offset, 8)
        id = bytes_to_int(entry[0:2])

        if id == 0xFFFD:
            table_offset += 8
            continue # this is only here to give an ending offset
        if id == 0xFFFF:
            break # this marks the end of the table

        messages.append( Message.from_rom(rom, index) )

        index += 1
        table_offset += 8

    return messages

# write the messages back
def repack_messages(rom, messages, permutation=None, always_allow_skip=True, speed_up_text=True):

    rom.update_dmadata_record(TEXT_START, TEXT_START, TEXT_START + ENG_TEXT_SIZE_LIMIT)

    if permutation is None:
        permutation = range(len(messages))

    # repack messages
    offset = 0
    text_size_limit = ENG_TEXT_SIZE_LIMIT

    for old_index, new_index in enumerate(permutation):
        old_message = messages[old_index]
        new_message = messages[new_index]
        remember_id = new_message.id
        new_message.id = old_message.id

        # modify message, making it represent how we want it to be written
        new_message.transform(True, old_message.ending, always_allow_skip, speed_up_text)

        # actually write the message
        offset = new_message.write(rom, old_index, offset)

        new_message.id = remember_id

    # raise an exception if too much is written
    # we raise it at the end so that we know how much overflow there is
    if offset > text_size_limit:
        raise(TypeError("Message Text table is too large: 0x" + "{:x}".format(offset) + " written / 0x" + "{:x}".format(ENG_TEXT_SIZE_LIMIT) + " allowed."))

    # end the table
    table_index = len(messages)
    entry = bytes([0xFF, 0xFD, 0x00, 0x00, 0x07]) + int_to_bytes(offset, 3)
    entry_offset = EXTENDED_TABLE_START + 8 * table_index
    rom.write_bytes(entry_offset, entry)
    table_index += 1
    entry_offset = EXTENDED_TABLE_START + 8 * table_index
    if 8 * (table_index + 1) > EXTENDED_TABLE_SIZE:
        raise(TypeError("Message ID table is too large: 0x" + "{:x}".format(8 * (table_index + 1)) + " written / 0x" + "{:x}".format(EXTENDED_TABLE_SIZE) + " allowed."))
    rom.write_bytes(entry_offset, [0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

# shuffles the messages in the game, making sure to keep various message types in their own group
def shuffle_messages(messages, rand, except_hints=True, always_allow_skip=True):

    permutation = [i for i, _ in enumerate(messages)]

    def is_exempt(m):
        hint_ids = (
            GOSSIP_STONE_MESSAGES + TEMPLE_HINTS_MESSAGES +
            [data['id'] for data in misc_item_hint_table.values()] +
            [data['id'] for data in misc_location_hint_table.values()] +
            list(KEYSANITY_MESSAGES.keys()) + shuffle_messages.shop_item_messages +
            shuffle_messages.scrubs_message_ids +
            [0x5036, 0x70F5] # Chicken count and poe count respectively
        )
        shuffle_exempt = [
            0x208D,         # "One more lap!" for Cow in House race.
        ]
        is_hint = (except_hints and m.id in hint_ids)
        is_error_message = (m.id == ERROR_MESSAGE)
        is_shuffle_exempt = (m.id in shuffle_exempt)
        return (is_hint or is_error_message or m.is_id_message() or is_shuffle_exempt)

    have_goto         = list( filter(lambda m: not is_exempt(m) and m.has_goto,         messages) )
    have_keep_open    = list( filter(lambda m: not is_exempt(m) and m.has_keep_open,    messages) )
    have_event        = list( filter(lambda m: not is_exempt(m) and m.has_event,        messages) )
    have_fade         = list( filter(lambda m: not is_exempt(m) and m.has_fade,         messages) )
    have_ocarina      = list( filter(lambda m: not is_exempt(m) and m.has_ocarina,      messages) )
    have_two_choice   = list( filter(lambda m: not is_exempt(m) and m.has_two_choice,   messages) )
    have_three_choice = list( filter(lambda m: not is_exempt(m) and m.has_three_choice, messages) )
    basic_messages    = list( filter(lambda m: not is_exempt(m) and m.is_basic(),       messages) )


    def shuffle_group(group):
        group_permutation = [i for i, _ in enumerate(group)]
        rand.shuffle(group_permutation)

        for index_from, index_to in enumerate(group_permutation):
            permutation[group[index_to].index] = group[index_from].index

    # need to use 'list' to force 'map' to actually run through
    list( map( shuffle_group, [
        have_goto + have_keep_open + have_event + have_fade + basic_messages,
        have_ocarina,
        have_two_choice,
        have_three_choice,
    ]))

    return permutation

# Update warp song text boxes for ER
def update_warp_song_text(messages, world):
    from .Hints import HintArea

    msg_list = {
        0x088D: 'Minuet of Forest Warp -> Sacred Forest Meadow',
        0x088E: 'Bolero of Fire Warp -> DMC Central Local',
        0x088F: 'Serenade of Water Warp -> Lake Hylia',
        0x0890: 'Requiem of Spirit Warp -> Desert Colossus',
        0x0891: 'Nocturne of Shadow Warp -> Graveyard Warp Pad Region',
        0x0892: 'Prelude of Light Warp -> Temple of Time',
    }

    if world.logic_rules != "glitched": # Entrances not set on glitched logic so following code will error
        for id, entr in msg_list.items():
            if 'warp_songs' in world.misc_hints or not world.warp_songs:
                destination = world.get_entrance(entr).connected_region
                destination_name = HintArea.at(destination)
                color = COLOR_MAP[destination_name.color]
                if destination_name.preposition(True) is not None:
                    destination_name = f'to {destination_name}'
            else:
                destination_name = 'to a mysterious place'
                color = COLOR_MAP['White']

            new_msg = f"\x08\x05{color}Warp {destination_name}?\x05\40\x09\x01\x01\x1b\x05\x42OK\x01No\x05\40"
            update_message_by_id(messages, id, new_msg)
