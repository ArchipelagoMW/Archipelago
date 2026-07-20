from ..assembler import ASM
from ..utils import formatText, setReplacementName
from ..roomEditor import RoomEditor
from .. import entityData
import os
import bsdiff4
import pkgutil

def imageTo2bpp(filename):
    import PIL.Image
    baseimg = PIL.Image.new('P', (1,1))
    baseimg.putpalette((
        128, 0, 128,
        0, 0, 0,
        128, 128, 128,
        255, 255, 255,
    ))
    img = PIL.Image.open(filename)
    img = img.quantize(colors=4, palette=baseimg)
    print (f"Palette: {img.getpalette()}")
    assert (img.size[0] % 8) == 0
    tileheight = 8 if img.size[1] == 8 else 16
    assert (img.size[1] % tileheight) == 0

    cols = img.size[0] // 8
    rows = img.size[1] // tileheight
    result = bytearray(rows * cols * tileheight * 2)
    index = 0
    for ty in range(rows):
        for tx in range(cols):
            for y in range(tileheight):
                a = 0
                b = 0
                for x in range(8):
                    c = img.getpixel((tx * 8 + x, ty * 16 + y))
                    if c & 1:
                        a |= 0x80 >> x
                    if c & 2:
                        b |= 0x80 >> x
                result[index] = a
                result[index+1] = b
                index += 2
    return result


def updateGraphics(rom, bank, offset, data):
    if offset + len(data) > 0x4000:
        updateGraphics(rom, bank, offset, data[:0x4000-offset])
        updateGraphics(rom, bank + 1, 0, data[0x4000 - offset:])
    else:
        rom.banks[bank][offset:offset+len(data)] = data
        if bank < 0x34:
            rom.banks[bank-0x20][offset:offset + len(data)] = data


def gfxMod(rom, filename):
    if os.path.exists(filename + ".names"):
        for line in open(filename + ".names", "rt"):
            if ":" in line:
                k, v = line.strip().split(":", 1)
                setReplacementName(k, v)

    ext = os.path.splitext(filename)[1].lower()
    if ext == ".bin":
        updateGraphics(rom, 0x2C, 0, open(filename, "rb").read())
    elif ext in (".png", ".bmp"):
        updateGraphics(rom, 0x2C, 0, imageTo2bpp(filename))
    elif ext == ".bdiff":
        updateGraphics(rom, 0x2C, 0, prepatch(rom, 0x2C, 0, filename))
    elif ext == ".json":
        import json
        data = json.load(open(filename, "rt"))

        for patch in data:
            if "gfx" in patch:
                updateGraphics(rom, int(patch["bank"], 16), int(patch["offset"], 16), imageTo2bpp(os.path.join(os.path.dirname(filename), patch["gfx"])))
            if "name" in patch:
                setReplacementName(patch["item"], patch["name"])
    else:
        updateGraphics(rom, 0x2C, 0, imageTo2bpp(filename))


def createGfxImage(rom, filename):
    import PIL.Image
    bank_count = 8
    img = PIL.Image.new("P", (32 * 8, 32 * 8 * bank_count))
    img.putpalette((
        128, 0, 128,
        0, 0, 0,
        128, 128, 128,
        255, 255, 255,
    ))
    for bank_nr in range(bank_count):
        bank = rom.banks[0x2C + bank_nr]
        for tx in range(32):
            for ty in range(16):
                for y in range(16):
                    a = bank[tx * 32 + ty * 32 * 32 + y * 2]
                    b = bank[tx * 32 + ty * 32 * 32 + y * 2 + 1]
                    for x in range(8):
                        c = 0
                        if a & (0x80 >> x):
                            c |= 1
                        if b & (0x80 >> x):
                            c |= 2
                        img.putpixel((tx*8+x, bank_nr * 32 * 8 + ty*16+y), c)
    img.save(filename)

def prepatch(rom, bank, offset, filename):
    bank_count = 8
    base_sheet = []
    result = []
    for bank_nr in range(bank_count):
        base_sheet[0x4000 * bank_nr:0x4000 * (bank_nr + 1) - 1] = rom.banks[0x2C + bank_nr]
    with open(filename, "rb") as patch:
        file = patch.read()
        result = bsdiff4.patch(src_bytes=bytes(base_sheet), patch_bytes=file)
    return result

def noSwordMusic(rom):
    # Skip no-sword music override
    # Instead of loading the sword level, we put the value 1 in the A register, indicating we have a sword.
    rom.patch(2, 0x0151, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(2, 0x3AEF, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(3, 0x0996, ASM("ld a, [$DB4E]"), ASM("ld a, $01"), fill_nop=True)
    rom.patch(3, 0x0B35, ASM("ld a, [$DB44]"), ASM("ld a, $01"), fill_nop=True)


def removeNagMessages(rom):
    # Remove "this object is heavy, bla bla", and other nag messages when touching an object
    rom.patch(0x02, 0x32BB, ASM("ld a, [$C14A]"), ASM("ld a, $01"), fill_nop=True)  # crystal blocks
    rom.patch(0x02, 0x32EC, ASM("ld a, [$C5A6]"), ASM("ld a, $01"), fill_nop=True) # cracked blocks
    rom.patch(0x02, 0x32D3, ASM("jr nz, $25"), ASM("jr $25"), fill_nop=True)  # stones/pots
    rom.patch(0x02, 0x2B88, ASM("jr nz, $0F"), ASM("jr $0F"), fill_nop=True)  # ice blocks


def removeLowHPBeep(rom):
    rom.patch(2,  0x233A, ASM("ld hl, $FFF3\nld [hl], $04"), b"", fill_nop=True) # Remove health beep


def slowLowHPBeep(rom):
    rom.patch(2, 0x2338, ASM("ld a, $30"), ASM("ld a, $60"))  # slow slow hp beep


def removeFlashingLights(rom):
    # Remove the switching between two backgrounds at mamu, always show the spotlights.
    rom.patch(0x00, 0x01EB, ASM("ldh a, [$E7]\nrrca\nand $80"), ASM("ld a, $80"), fill_nop=True)
    # Remove flashing colors from shopkeeper killing you after stealing and the mad batter giving items.
    rom.patch(0x24, 0x3B77, ASM("push bc"), ASM("ret"))


def forceLinksPalette(rom, index):
    # This forces the link sprite into a specific palette index ignoring the tunic options.
    rom.patch(0, 0x1D8C,
            ASM("ld a, [$DC0F]\nand a\njr z, $03\ninc a"),
            ASM("ld a, $%02X" % (index)), fill_nop=True)
    rom.patch(0, 0x1DD2,
            ASM("ld a, [$DC0F]\nand a\njr z, $03\ninc a"),
            ASM("ld a, $%02X" % (index)), fill_nop=True)
    # Fix the waking up from bed palette
    if index == 1:
        rom.patch(0x21, 0x33FC, "A222", "FF05")
    elif index == 2:
        rom.patch(0x21, 0x33FC, "A222", "3F14")
    elif index == 3:
        rom.patch(0x21, 0x33FC, "A222", "037E")
    for n in range(6):
        rom.patch(0x05, 0x1261 + n * 2, "00", f"{index:02x}")


def fastText(rom):
    rom.patch(0x00, 0x24CA, ASM("jp $2485"), ASM("call $2485"))


def noText(rom):
    for idx in range(len(rom.texts)):
        if not isinstance(rom.texts[idx], int) and (idx < 0x217 or idx > 0x21A):
            rom.texts[idx] = rom.texts[idx][-1:]


def reduceMessageLengths(rom, rnd):
    # Into text from Marin. Got to go fast, so less text. (This intro text is very long)
    lines = pkgutil.get_data(__name__, "marin.txt").splitlines(keepends=True)
    while lines and lines[-1].strip() == b'':
        lines.pop(-1)
    rom.texts[0x01] = formatText(rnd.choice(lines).strip().decode("unicode_escape"))

    # Reduce length of a bunch of common texts
    rom.texts[0xEA] = formatText("You've got a Guardian Acorn!")
    rom.texts[0xEB] = rom.texts[0xEA]
    rom.texts[0xEC] = rom.texts[0xEA]
    rom.texts[0x08] = formatText("You got a Piece of Power!")
    rom.texts[0xEF] = formatText("You found a {SEASHELL}!")
    rom.texts[0xA7] = formatText("You've got the {COMPASS}!")

    rom.texts[0x07] = formatText("You need the {NIGHTMARE_KEY}!")
    rom.texts[0x8C] = formatText("You need a {KEY}!")  # keyhole block

    rom.texts[0x09] = formatText("Ahhh... It has  the Sleepy {TOADSTOOL}, it does! We'll mix it up something in a jiffy, we will!")
    rom.texts[0x0A] = formatText("The last thing I kin remember was bitin' into a big juicy {TOADSTOOL}... Then, I had the darndest dream... I was a raccoon! Yeah, sounds strange, but it sure was fun!")
    rom.texts[0x0F] = formatText("You pick the {TOADSTOOL}... As you hold it over your head, a mellow aroma flows into your nostrils.")
    rom.texts[0x13] = formatText("You've learned the ^{SONG1}!^ This song will always remain in your heart!")
    rom.texts[0x18] = formatText("Will you give me 28 {RUPEES} for my secret?", ask="Give Don't")
    rom.texts[0x19] = formatText("How about it? 42 {RUPEES} for my little secret...", ask="Give Don't")
    rom.texts[0x1e] = formatText("...You're so cute! I'll give you a 7 {RUPEE} discount!")
    rom.texts[0x2d] = formatText("{ARROWS_10}\n10 {RUPEES}!", ask="Buy  Don't")
    rom.texts[0x32] = formatText("{SHIELD}\n20 {RUPEES}!", ask="Buy  Don't")
    rom.texts[0x33] = formatText("Ten {BOMB}\n10 {RUPEES}", ask="Buy  Don't")
    rom.texts[0x3d] = formatText("It's a {SHIELD}! There is space for your name!")
    rom.texts[0x42] = formatText("It's 30 {RUPEES}! You can play the game three more times with this!")
    rom.texts[0x45] = formatText("How about some fishing, little buddy? I'll only charge you 10 {RUPEES}...", ask="Fish Not Now")
    rom.texts[0x4b] = formatText("Wow! Nice Fish! It's a lunker!! I'll give you a 20 {RUPEE} prize! Try again?", ask="Cast Not Now")
    rom.texts[0x4e] = formatText("You're short of {RUPEES}? Don't worry about it. You just come back when you have more money, little buddy.")
    rom.texts[0x4f] = formatText("You've got a {HEART_PIECE}! Press SELECT on the Subscreen to see.")
    rom.texts[0x8e] = formatText("Well, it's an {OCARINA}, but you don't know how  to play it...")
    rom.texts[0x90] = formatText("You found the {POWER_BRACELET}! At last, you can pick up pots and stones!")
    rom.texts[0x91] = formatText("You got your {SHIELD} back! Press the button and repel enemies with it!")
    rom.texts[0x93] = formatText("You've got the {HOOKSHOT}! Its chain stretches long when you use it!")
    rom.texts[0x94] = formatText("You've got the {MAGIC_ROD}! Now you can burn things! Burn it! Burn, baby burn!")
    rom.texts[0x95] = formatText("You've got the {PEGASUS_BOOTS}! If you hold down the Button, you can dash!")
    rom.texts[0x96] = formatText("You've got the {OCARINA}! You should learn to play many songs!")
    rom.texts[0x97] = formatText("You've got the {FEATHER}! It feels like your body is a  lot lighter!")
    rom.texts[0x98] = formatText("You've got a {SHOVEL}! Now you can feel the joy of digging!")
    rom.texts[0x99] = formatText("You've got some {MAGIC_POWDER}! Try sprinkling it on a variety of things!")
    rom.texts[0x9b] = formatText("You found your {SWORD}!  It must be yours because it has your name engraved on it!")
    rom.texts[0x9c] = formatText("You've got the {FLIPPERS}! If you press the B Button while you swim, you can dive underwater!")
    rom.texts[0x9e] = formatText("You've got a new {SWORD}! You should put your name on it right away!")
    rom.texts[0x9f] = formatText("You've got a new {SWORD}! You should put your name on it right away!")
    rom.texts[0xa0] = formatText("You found the {MEDICINE}! You should apply this and see what happens!")
    rom.texts[0xa1] = formatText("You've got the {TAIL_KEY}! Now you can open the Tail Cave gate!")
    rom.texts[0xa2] = formatText("You've got the {SLIME_KEY}! Now you can open the gate in Ukuku Prairie!")
    rom.texts[0xa3] = formatText("You've got the {ANGLER_KEY}!")
    rom.texts[0xa4] = formatText("You've got the {FACE_KEY}!")
    rom.texts[0xa5] = formatText("You've got the {BIRD_KEY}!")
    rom.texts[0xa6] = formatText("At last, you got a {MAP}! Press the START Button to look at it!")
    rom.texts[0xa8] = formatText("You found a {STONE_BEAK}! Let's find the owl statue that belongs to it.")
    rom.texts[0xa9] = formatText("You've got the {NIGHTMARE_KEY}! Now you can open the door to the Nightmare's Lair!")
    rom.texts[0xaa] = formatText("You got a {KEY}! You can open a locked door.")
    rom.texts[0xab] = formatText("You got 20 {RUPEES}! JOY!", center=True)
    rom.texts[0xac] = formatText("You got 50 {RUPEES}! Very Nice!", center=True)
    rom.texts[0xad] = formatText("You got 100 {RUPEES}! You're Happy!", center=True)
    rom.texts[0xae] = formatText("You got 200 {RUPEES}! You're Ecstatic!", center=True)
    rom.texts[0xdc] = formatText("Ribbit! Ribbit! I'm Mamu, on vocals! But I don't need to tell you that, do I? Everybody knows me! Want to hang out and listen to us jam? For 300 Rupees, we'll let you listen to a previously unreleased cut! What do you do?", ask="Pay Leave")
    rom.texts[0xe8] = formatText("You've found a {GOLD_LEAF}! Press START to see how many you've collected!")
    rom.texts[0xed] = formatText("You've got the Mirror Shield! You can now turnback the beams you couldn't block before!")
    rom.texts[0xee] = formatText("You've got a more Powerful {POWER_BRACELET}! Now you can almost lift a whale!")
    rom.texts[0xf0] = formatText("Want to go on a raft ride for a hundred {RUPEES}?", ask="Yes No Way")


def allowColorDungeonSpritesEverywhere(rom):
    # Set sprite set numbers $01-$40 to map to the color dungeon sprites
    rom.patch(0x00, 0x2E6F, "00", "15")
    # Patch the spriteset loading code to load the 4 entries from the normal table instead of skipping this for color dungeon specific exception weirdness
    rom.patch(0x00, 0x0DA4, ASM("jr nc, $05"), ASM("jr nc, $41"))
    rom.patch(0x00, 0x0DE5, ASM("""
        ldh  a, [$F7]
        cp   $FF
        jr   nz, $06
        ld a, $01
        ldh [$91], a
        jr $40
    """), ASM("""
        jr $0A ; skip over the rest of the code
        cp $FF ; check if color dungeon
        jp nz, $0DAB
        inc d
        jp $0DAA
    """), fill_nop=True)
    # Disable color dungeon specific tile load hacks
    rom.patch(0x00, 0x06A7, ASM("jr nz, $22"), ASM("jr $22"))
    rom.patch(0x00, 0x2E77, ASM("jr nz, $0B"), ASM("jr $0B"))
    
    # Finally fill in the sprite data for the color dungeon
    for n in range(22):
        data = bytearray()
        for m in range(4):
            idx = rom.banks[0x20][0x06AA + 44 * m + n * 2]
            bank = rom.banks[0x20][0x06AA + 44 * m + n * 2 + 1]
            if idx == 0 and bank == 0:
                v = 0xFF
            elif bank == 0x35:
                v = idx - 0x40
            elif bank == 0x31:
                v = idx
            elif bank == 0x2E:
                v = idx + 0x40
            else:
                assert False, "%02x %02x" % (idx, bank)
            data += bytes([v])
        rom.room_sprite_data_indoor[0x200 + n] = data

    # Patch the graphics loading code to use DMA and load all sets that need to be reloaded, not just the first and last
    rom.patch(0x00, 0x06FA, 0x07AF, ASM("""
        ;We enter this code with the right bank selected for tile data copy,
        ;d = tile row (source addr = (d*$100+$4000))
        ;e = $00
        ;$C197 = index of sprite set to update (target addr = ($8400 + $100 * [$C197]))
        ld  a, d
        add a, $40
        ldh [$51], a
        xor a
        ldh [$52], a
        ldh [$54], a
        ld  a, [$C197]
        add a, $84
        ldh [$53], a
        ld  a, $0F
        ldh [$55], a

        ; See if we need to do anything next
        ld  a, [$C10E] ; check the 2nd update flag
        and a
        jr  nz, getNext
        ldh [$91], a ; no 2nd update flag, so clear primary update flag
        ret
    getNext:
        ld  hl, $C197
        inc [hl]
        res 2, [hl]
        ld  a, [$C10D]
        cp  [hl]
        ret nz
        xor a ; clear the 2nd update flag when we prepare to update the last spriteset
        ld  [$C10E], a
        ret
    """), fill_nop=True)
    rom.patch(0x00, 0x0738, "00" * (0x073E - 0x0738), ASM("""
        ; we get here by some color dungeon specific code jumping to this position
        ; We still need that color dungeon specific code as it loads background tiles
        xor a
        ldh [$91], a
        ldh [$93], a
        ret
    """))
    rom.patch(0x00, 0x073E, "00" * (0x07AF - 0x073E), ASM("""
        ;If we get here, only the 2nd flag is filled and the primary is not. So swap those around.
        ld  a, [$C10D] ;copy the index number
        ld  [$C197], a
        xor a
        ld  [$C10E], a ; clear the 2nd update flag
        inc a
        ldh [$91], a ; set the primary update flag
        ret
    """), fill_nop=True)


def updateSpriteData(rom):
    # Change the special sprite change exceptions
    rom.patch(0x00, 0x0DAD, 0x0DDB, ASM("""
    ; Check for indoor
    ld   a, d
    and  a
    jr   nz, noChange
    ldh  a, [$F6] ; hMapRoom
    cp   $C9
    jr   nz, sirenRoomEnd
    ld   a, [$D8C9] ; wOverworldRoomStatus + ROOM_OW_SIREN
    and  $20
    jr   z, noChange
    ld   hl, $7837
    jp   $0DFE
sirenRoomEnd:
    ldh  a, [$F6] ; hMapRoom
    cp   $D8
    jr   nz, noChange
    ld   a, [$D8FD] ; wOverworldRoomStatus + ROOM_OW_WALRUS 
    and  $20
    jr   z, noChange
    ld   hl, $783B
    jp   $0DFE
noChange:
    """), fill_nop=True)
    rom.patch(0x20, 0x3837, "A4FF8BFF", "A461FF72")
    rom.patch(0x20, 0x383B, "A44DFFFF", "A4C5FF70")

    # For each room update the sprite load data based on which entities are in there.
    for room_nr in range(0x316):
        if room_nr == 0x2FF:
            continue
        values = [None, None, None, None]
        if room_nr == 0x00E:  # D7 entrance opening
            values[2] = 0xD6
            values[3] = 0xD7
        if 0x211 <= room_nr <= 0x21E:  # D7 throwing ball thing.
            values[0] = 0x66
        r = RoomEditor(rom, room_nr)
        for obj in r.objects:
            if obj.type_id == 0xC5 and room_nr < 0x100: # Pushable Gravestone
                values[3] = 0x82
        for x, y, entity in r.entities:
            sprite_data = entityData.SPRITE_DATA[entity]
            if callable(sprite_data):
                sprite_data = sprite_data(r)
            if sprite_data is None:
                continue
            for m in range(0, len(sprite_data), 2):
                idx, value = sprite_data[m:m+2]
                if values[idx] is None:
                    values[idx] = value
                elif isinstance(values[idx], set) and isinstance(value, set):
                    values[idx] = values[idx].intersection(value)
                    assert len(values[idx]) > 0
                elif isinstance(values[idx], set) and value in values[idx]:
                    values[idx] = value
                elif isinstance(value, set) and values[idx] in value:
                    pass
                elif values[idx] == value:
                    pass
                else:
                    assert False, "Room: %03x cannot load graphics for entity: %02x (Index: %d Failed: %s, Active: %s)" % (room_nr, entity, idx, value, values[idx])

        data = bytearray()
        for v in values:
            if isinstance(v, set):
                v = next(iter(v))
            elif v is None:
                v = 0xff
            data.append(v)

        if room_nr < 0x100:
            rom.room_sprite_data_overworld[room_nr] = data
        else:
            rom.room_sprite_data_indoor[room_nr - 0x100] = data


def bin_to_rgb(word):
    red   = word & 0b11111
    word >>= 5
    green = word & 0b11111
    word >>= 5
    blue  = word & 0b11111
    return (red, green, blue)

def rgb_to_bin(r, g, b):
    return (b << 10) | (g << 5) | r
