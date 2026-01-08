from ..assembler import ASM
from ..roomEditor import RoomEditor


def fixBowwow(rom):
    ### BowWow patches
    rom.patch(0x03, 0x1E0E, ASM("ld [$DB56], a"), "", fill_nop=True)  # Do not mark BowWow as kidnapped after we complete dungeon 1.
    rom.patch(0x15, 0x06B6, ASM("ld a, [$DB56]\ncp $80"), ASM("xor a"), fill_nop=True)  # always load the moblin boss
    rom.patch(0x03, 0x182D, ASM("ld a, [$DB56]\ncp $80"), ASM("ld a, [$DAE2]\nand $10"))  # load the cave moblins if the chest is not opened
    rom.patch(0x07, 0x3947, ASM("ld a, [$DB56]\ncp $80"), ASM("ld a, [$DAE2]\nand $10"))  # load the cave moblin with sword if the chest is not opened

    # Modify the moblin cave to contain a chest at the end, which contains bowwow
    re = RoomEditor(rom, 0x2E2)
    re.removeEntities(0x6D)
    re.changeObject(8, 3, 0xA0)
    re.store(rom)
    # Place bowwow in the chest table
    rom.banks[0x14][0x560 + 0x2E2] = 0x81

    # Patch bowwow follower sprite to be used from 2nd vram bank
    rom.patch(0x05, 0x001C,
        b"40034023"
        b"42034223"
        b"44034603"
        b"48034A03"
        b"46234423"
        b"4A234823"
        b"4C034C23",
        b"500B502B"
        b"520B522B"
        b"540B560B"
        b"580B5A0B"
        b"562B542B"
        b"5A2B582B"
        b"5C0B5C2B")
    # Patch to use the chain sprite from second vram bank (however, the chain bugs out various things)
    rom.patch(0x05, 0x0282,
        ASM("ld a, $4E\njr nz, $02\nld a, $7E\nld [de], a\ninc de\nld a, $00"),
        ASM("ld a, $5E\nld [de], a\ninc de\nld a, $08"), fill_nop=True)
    # Never load the bowwow tiles in the first VRAM bank, as we do not need them.
    rom.patch(0x00, 0x2EB0, ASM("ld a, [$DB56]\ncp $01\nld a, $A4\njr z, $18"), "", fill_nop=True)

    # Patch the location where bowwow stores chain X/Y positions so it does not conflict with a lot of other things
    rom.patch(0x05, 0x00BE, ASM("ld hl, $D100"), ASM("ld hl, $D180"))
    rom.patch(0x05, 0x0275, ASM("ld hl, $D100"), ASM("ld hl, $D180"))
    rom.patch(0x05, 0x03AD, ASM("ld [$D100], a"), ASM("ld [$D180], a"))
    rom.patch(0x05, 0x03BD, ASM("ld de, $D100"), ASM("ld de, $D180"))
    rom.patch(0x05, 0x049F, ASM("ld hl, $D100"), ASM("ld hl, $D180"))
    rom.patch(0x05, 0x04C2, ASM("ld a, [$D100]"), ASM("ld a, [$D180]"))
    rom.patch(0x05, 0x03C0, ASM("ld hl, $D101"), ASM("ld hl, $D181"))
    rom.patch(0x05, 0x0418, ASM("ld [$D106], a"), ASM("ld [$D186], a"))
    rom.patch(0x05, 0x0423, ASM("ld de, $D106"), ASM("ld de, $D186"))
    rom.patch(0x05, 0x0426, ASM("ld hl, $D105"), ASM("ld hl, $D185"))

    rom.patch(0x19, 0x3A4E, ASM("ld hl, $D100"), ASM("ld hl, $D180"))
    rom.patch(0x19, 0x3A5A, ASM("ld hl, $D110"), ASM("ld hl, $D190"))

    rom.patch(0x05, 0x00D9, ASM("ld hl, $D110"), ASM("ld hl, $D190"))
    rom.patch(0x05, 0x026E, ASM("ld hl, $D110"), ASM("ld hl, $D190"))
    rom.patch(0x05, 0x03BA, ASM("ld [$D110], a"), ASM("ld [$D190], a"))
    rom.patch(0x05, 0x03DD, ASM("ld de, $D110"), ASM("ld de, $D190"))
    rom.patch(0x05, 0x0480, ASM("ld hl, $D110"), ASM("ld hl, $D190"))
    rom.patch(0x05, 0x04B5, ASM("ld a, [$D110]"), ASM("ld a, [$D190]"))
    rom.patch(0x05, 0x03E0, ASM("ld hl, $D111"), ASM("ld hl, $D191"))
    rom.patch(0x05, 0x0420, ASM("ld [$D116], a"), ASM("ld [$D196], a"))
    rom.patch(0x05, 0x044d, ASM("ld de, $D116"), ASM("ld de, $D196"))
    rom.patch(0x05, 0x0450, ASM("ld hl, $D115"), ASM("ld hl, $D195"))

    rom.patch(0x05, 0x0039, ASM("ld [$D154], a"), "", fill_nop=True)  # normally this stores the index to bowwow, for the kiki fight
    rom.patch(0x05, 0x013C, ASM("ld [$D150], a"), ASM("ld [$D197], a"))
    rom.patch(0x05, 0x0144, ASM("ld [$D151], a"), ASM("ld [$D198], a"))
    rom.patch(0x05, 0x02F9, ASM("ld [$D152], a"), ASM("ld [$D199], a"))
    rom.patch(0x05, 0x0335, ASM("ld a, [$D152]"), ASM("ld a, [$D199]"))
    rom.patch(0x05, 0x0485, ASM("ld a, [$D151]"), ASM("ld a, [$D198]"))
    rom.patch(0x05, 0x04A4, ASM("ld a, [$D150]"), ASM("ld a, [$D197]"))

    # Patch bowwow to not stay around when we move from map to map
    rom.patch(0x05, 0x0049, 0x0054, ASM("""
        cp   [hl]
        jr   z, Continue
        ld   hl, $C280
        add  hl, bc
        ld   [hl], b
        ret
Continue:
        """), fill_nop=True)

    # Patch madam meow meow to not take bowwow
    rom.patch(0x06, 0x1BD7, ASM("ld a, [$DB66]\nand $02"), ASM("ld a, $00\nand $02"), fill_nop=True)

    # Patch kiki not to react to bowwow, as bowwow is not with link at this map
    rom.patch(0x07, 0x18A8, ASM("ld a, [$DB56]\ncp $01"), ASM("ld a, $00\ncp $01"), fill_nop=True)

    # Patch the color dungeon entrance not to check for bowwow
    rom.patch(0x02, 0x340D, ASM("ld hl, $DB56\nor [hl]"), "", fill_nop=True)

    # Patch richard to ignore bowwow
    rom.patch(0x06, 0x006C, ASM("ld a, [$DB56]"), ASM("xor a"), fill_nop=True)

    # Patch to modify how bowwow eats enemies, normally it just unloads them, but we call our handler in bank 3E
    rom.patch(0x05, 0x03A0, 0x03A8, ASM("""
        push bc
        ld   b, d
        ld   c, e
        ld   a, $08
        rst  8
        pop  bc
        ret
    """), fill_nop=True)
    rom.patch(0x05, 0x0387, ASM("ld a, $03\nldh [$FFF2], a"), "", fill_nop=True)  # remove the default chomp sfx

    # Various enemies
    rom.banks[0x14][0x1218 + 0xC5] = 0x01  # Urchin
    rom.banks[0x14][0x1218 + 0x93] = 0x01  # MadBomber
    rom.banks[0x14][0x1218 + 0x51] = 0x01  # Swinging ball&chain golden leaf enemy
    rom.banks[0x14][0x1218 + 0xF2] = 0x01  # Color dungeon flying hopper
    rom.banks[0x14][0x1218 + 0xF3] = 0x01  # Color dungeon hopper
    rom.banks[0x14][0x1218 + 0xE9] = 0x01  # Color dungeon shell
    rom.banks[0x14][0x1218 + 0xEA] = 0x01  # Color dungeon shell
    rom.banks[0x14][0x1218 + 0xEB] = 0x01  # Color dungeon shell
    rom.banks[0x14][0x1218 + 0xEC] = 0x01  # Color dungeon thing
    rom.banks[0x14][0x1218 + 0xED] = 0x01  # Color dungeon thing
    rom.banks[0x14][0x1218 + 0xEE] = 0x01  # Color dungeon thing
    rom.banks[0x14][0x1218 + 0x87] = 0x01  # Lanmola (for D4 key)
    rom.banks[0x14][0x1218 + 0x88] = 0x01  # Armos knight (for D6 key)
    rom.banks[0x14][0x1218 + 0x16] = 0x01  # Spark
    rom.banks[0x14][0x1218 + 0x17] = 0x01  # Spark
    rom.banks[0x14][0x1218 + 0x2C] = 0x01  # Spiked beetle
    rom.banks[0x14][0x1218 + 0x90] = 0x01  # Three of a kind (screw these guys)
    rom.banks[0x14][0x1218 + 0x18] = 0x01  # Pols voice
    rom.banks[0x14][0x1218 + 0x50] = 0x01  # Boo buddy
    rom.banks[0x14][0x1218 + 0xA2] = 0x01  # Pirana plant
    rom.banks[0x14][0x1218 + 0x52] = 0x01  # Tractor device
    rom.banks[0x14][0x1218 + 0x53] = 0x01  # Tractor device (D3)
    rom.banks[0x14][0x1218 + 0x55] = 0x01  # Bounding bombite
    rom.banks[0x14][0x1218 + 0x56] = 0x01  # Timer bombite
    rom.banks[0x14][0x1218 + 0x57] = 0x01  # Pairod
    rom.banks[0x14][0x1218 + 0x15] = 0x01  # Antifairy
    rom.banks[0x14][0x1218 + 0xA0] = 0x01  # Peahat
    rom.banks[0x14][0x1218 + 0x9C] = 0x01  # Star
    rom.banks[0x14][0x1218 + 0xA1] = 0x01  # Snake
    rom.banks[0x14][0x1218 + 0xBD] = 0x01  # Vire
    rom.banks[0x14][0x1218 + 0xE4] = 0x01  # Moblin boss

    # Bosses
    rom.banks[0x14][0x1218 + 0x59] = 0x01  # Moldorm
    rom.banks[0x14][0x1218 + 0x5C] = 0x01  # Genie
    rom.banks[0x14][0x1218 + 0x5B] = 0x01  # Slime Eye
    rom.patch(0x04, 0x0AC4, ASM("ld [hl], $28"), ASM("ld [hl], $FF"))  # give more time before slimeeye unsplits
    rom.patch(0x04, 0x0B05, ASM("ld [hl], $50"), ASM("ld [hl], $FF"))  # give more time before slimeeye unsplits
    rom.banks[0x14][0x1218 + 0x65] = 0x01  # Angler fish
    rom.banks[0x14][0x1218 + 0x5D] = 0x01  # Slime eel
    rom.banks[0x14][0x1218 + 0x5A] = 0x01  # Facade
    rom.banks[0x14][0x1218 + 0x63] = 0x01  # Eagle
    rom.banks[0x14][0x1218 + 0x62] = 0x01  # Hot head
    rom.banks[0x14][0x1218 + 0xF9] = 0x01  # Hardhit beetle
    rom.banks[0x14][0x1218 + 0xE6] = 0x01  # Nightmare

    # Minibosses
    rom.banks[0x14][0x1218 + 0x81] = 0x01  # Rolling bones
    rom.banks[0x14][0x1218 + 0x89] = 0x01  # Hinox
    rom.banks[0x14][0x1218 + 0x8E] = 0x01  # Cue ball
    rom.banks[0x14][0x1218 + 0x5E] = 0x01  # Gnoma
    rom.banks[0x14][0x1218 + 0x5F] = 0x01  # Master stalfos
    rom.banks[0x14][0x1218 + 0x92] = 0x01  # Smasher
    rom.banks[0x14][0x1218 + 0xBC] = 0x01  # Grim creeper
    rom.banks[0x14][0x1218 + 0xBE] = 0x01  # Blaino
    rom.banks[0x14][0x1218 + 0xF8] = 0x01  # Giant buzz blob
    rom.banks[0x14][0x1218 + 0xF4] = 0x01  # Avalaunch

    # NPCs
    rom.banks[0x14][0x1218 + 0x6F] = 0x01  # Dog
    rom.banks[0x14][0x1218 + 0x6E] = 0x01  # Butterfly
    rom.banks[0x14][0x1218 + 0x6C] = 0x01  # Cucco
    rom.banks[0x14][0x1218 + 0x70] = 0x01  # Kid
    rom.banks[0x14][0x1218 + 0x71] = 0x01  # Kid
    rom.banks[0x14][0x1218 + 0x72] = 0x01  # Kid
    rom.banks[0x14][0x1218 + 0x73] = 0x01  # Kid
    rom.banks[0x14][0x1218 + 0xD0] = 0x01  # Animal
    rom.banks[0x14][0x1218 + 0xD1] = 0x01  # Animal
    rom.banks[0x14][0x1218 + 0xD2] = 0x01  # Animal
    rom.banks[0x14][0x1218 + 0xD3] = 0x01  # Animal


def bowwowMapPatches(rom):
    # Remove all the cystal things that can only be destroyed with a sword.
    for n in range(0x100, 0x2FF):
        re = RoomEditor(rom, n)
        re.objects = list(filter(lambda obj: obj.type_id != 0xDD, re.objects))
        re.store(rom)
