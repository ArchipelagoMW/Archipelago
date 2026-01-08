from ..memory.space import Bank, Reserve, Allocate, Write
from ..instruction import asm as asm

def mastered_mod(espers):
    # Ported with mods from https://www.ff6hacking.com/forums/thread-4181.html
    # Mods from Madsuir's original:
    #   1. Rather than using the space at the right, I replace the ... before the MP
    #   2. Using F0 freespace
    #   3. Displaced code is different to deconflict with equipable_mod
    from ..data.text.text2 import text_value
    space = Reserve(0x487b0, 0x487be, "add star icon for text2 to unused space")
    space.write(
        0x18,0x00,0x3C,0x18,0xFF,0x18,0xFF,0x7E,0x7E,0x3C,0xFF,0x7E,0xFF,0x66 # raw hex for star icon
    )

    MASTERED_ICON = 0x7f # points to the star icon created above
    SPELL_OFFSET_STORAGE_RAM = 0x0203 # free Menu RAM location used to calculate character spell offset once per Skills menu
    src = [
        asm.PHX(), # save X
        asm.TDC(), # clear A
        asm.LDA(0x28, asm.DIR), # load slot ID (0-3)
        asm.TAX(),
        asm.LDA(0x69, asm.DIR_X), # load actor ID in slot
        asm.XBA(),
        asm.LDA(0x36, asm.IMM8), # 54 spells
        asm.A16(),
        asm.STA(0x004202, asm.LNG), #prepare multiplication (actor ID * 54)
        asm.NOP(),
        asm.NOP(),
        asm.NOP(),
        asm.NOP(),
        asm.LDA(0x004216, asm.LNG), #load multiplication result
        asm.STA(SPELL_OFFSET_STORAGE_RAM, asm.ABS), #store it
        asm.A8(),
        asm.PLX(), # restore X
        asm.JSL(0xc20006), # get actor stats -- displaced code
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "set spell offset")
    set_spell_offset = space.start_address_snes

    space = Reserve(0x31b64, 0x31b67, "calculate actor's spells starting RAM offset")
    space.write(
        asm.JSL(set_spell_offset),
    )

    src = [
        asm.PHX(),
        asm.PHY(),
        asm.TDC(), # clear A
        asm.STA(0xfb, asm.DIR),
        asm.LDA(0x7e9d89, asm.LNG_X), # load esper ID
        asm.A16(),
        asm.STA(0xfc, asm.DIR), # save it
        asm.ASL(), # x2
        asm.STA(0xfe, asm.DIR), # save it
        asm.ASL(), # x4
        asm.ASL(), # x8
        asm.CLC(),
        asm.ADC(0xfe, asm.DIR), # x10
        asm.CLC(),
        asm.ADC(0xfc, asm.DIR), # x11
        asm.TAX(),
        asm.STZ(0xfc, asm.DIR),
        asm.LDY(0x0005, asm.IMM16), # 5 spells max per esper
        asm.A8(),
        "LOOP",
        asm.TDC(), # clear A
        asm.LDA(0xd86e01, asm.LNG_X), # esper spell
        asm.CMP(0xff, asm.IMM8), # no spell?
        asm.BEQ("NO_ESPER"), # exit if no esper
        asm.STA(0xfc, asm.DIR), # save spell ID
        asm.A16(),
        asm.LDA(SPELL_OFFSET_STORAGE_RAM, asm.ABS), # load current character spell offset
        asm.CLC(),
        asm.ADC(0xfc, asm.DIR), # spell offset + spell ID
        asm.PHX(),
        asm.TAX(), # set X as spell learnt percentage
        asm.A8(),
        asm.LDA(0x1a6e, asm.ABS_X), # load spell learnt percentage
        asm.PLX(),
        asm.CMP(0xff, asm.IMM8), # compare learnt rate to 100%
        asm.BNE("NOT_MASTERED"), # branch if not 100%
        asm.INX(),
        asm.INX(),
        asm.DEY(),
        asm.BNE("LOOP"),
        "NO_ESPER",
        asm.INC(0xfb, asm.DIR), # set esper as mastered
        "NOT_MASTERED",
        asm.PLY(),
        asm.PLX(),
        asm.LDA(0x7e9d89, asm.LNG_X), # load esper ID -- displaced code
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "check mastered")
    check_mastered = space.start_address_snes

    space = Reserve(0x3552e, 0x35531, "check if current esper is mastered")
    space.write(
        asm.JSL(check_mastered),
    )

    src = [
        asm.LDA(0xfb, asm.DIR), # load mastered esper byte
        asm.BEQ("NOT_MASTERED"), # branch if not mastered
        asm.LDA(MASTERED_ICON, asm.IMM8), #load our mastered icon
        asm.BRA("RETURN"),
        "NOT_MASTERED",
        asm.LDA(text_value['…'], asm.IMM8), # load the normal icon
        "RETURN",
        asm.STA(0x2180, asm.ABS), # add to string -- displaced code
        asm.RTL(),
    ]

    space = Write(Bank.F0, src, "add esper learned icon")
    add_icon = space.start_address_snes

    space = Reserve(0x3553f, 0x35543, "set icon for mastered espers", asm.NOP())
    space.write(
        asm.JSL(add_icon),
    )


def equipable_mod(espers):
    from ..data.characters import Characters

    character_id_address = 0x1cf8
    gray_out_if_equipped = 0xc35576
    set_text_color = 0xc35595

    space = Allocate(Bank.C3, 145, "equipable espers", asm.NOP())

    equip_table = space.next_address
    for esper in espers.espers:
        space.write(
            esper.equipable_characters.to_bytes(2, "little"),
        )

    store_character_id = space.next_address
    space.copy_from(0x31b61, 0x31b63)   # x = character slot, a = character id
    space.write(
        asm.STA(character_id_address, asm.ABS),
        asm.RTS(),
    )

    check_equipable = space.next_address
    space.write(
        asm.PHX(),
        asm.PHP(),
        asm.STA(0xe0, asm.DIR),         # save esper (for use by callers)
        asm.XY8(),
        asm.A16(),
        asm.ASL(),                      # a = esper id * 2 (2 bytes for character bits)
        asm.TAX(),                      # x = esper id * 2
        asm.PHX(),
        asm.LDA(character_id_address, asm.ABS), # a = character id
        asm.ASL(),                      # a = character id * 2 (2 bytes for character bits)
        asm.TAX(),                      # x = character id * 2
        asm.LDA(0xc39c67, asm.LNG_X),   # a = character bit mask
        asm.PLX(),
        asm.AND(equip_table, asm.LNG_X),# and character bit mask with esper equipable bit mask
        asm.BEQ("NOT_EQUIPABLE"),       # branch if result is zero
        asm.PLP(),
        asm.PLX(),
        asm.JMP(gray_out_if_equipped, asm.ABS),

        "NOT_EQUIPABLE",
        asm.PLP(),
        asm.PLX(),
        asm.LDA(0x28, asm.IMM8),        # load text color (gray)
        asm.JMP(set_text_color, asm.ABS),
    )

    # TODO add new text type for this
    cant_equip_len = len("Can't equip!")
    cant_equip_error_text = space.next_address
    space.write(
        0x82, # C
        0x9a, # a
        0xa7, # n
        0xc3, # '
        0xad, # t
        0xff, #
        0x9e, # e
        0xaa, # q
        0xae, # u
        0xa2, # i
        0xa9, # p
        0xbe, # !
    )

    # change error message from "<character> has it!" to "Can't equip!"
    unequipable_error = space.next_address
    space.write(
        asm.LDA(0x1602, asm.ABS_X),     # a = first letter of name of character with esper equipped
        asm.CMP(0x80, asm.IMM8),        # compare against empty character (no character has esper equipped)
        asm.BCC("UNEQUIPABLE"),         # branch if not already equipped by another character

        "ALREADY_EQIPPED",
        asm.LDY(Characters.NAME_SIZE, asm.IMM8),    # y = name length
        asm.RTS(),

        "UNEQUIPABLE",
        asm.PLX(),                      # pull return address (do not return to vanilla already equipped)
        asm.LDX(0x0000, asm.IMM16),     # start at character zero in error message

        "PRINT_ERROR_LOOP",
        asm.LDA(cant_equip_error_text, asm.LNG_X),  # a = error_message[x]
        asm.STA(0x2180, asm.ABS),                   # print error_message[x]
        asm.INX(),
        asm.CPX(cant_equip_len, asm.IMM16),
        asm.BCC("PRINT_ERROR_LOOP"),
        asm.STZ(0x2180, asm.ABS),                   # print NULL
        asm.JMP(0x7fd9, asm.ABS),                   # print error_message
    )

    space = Reserve(0x31b61, 0x31b63, "skill menu store character id")
    space.write(
        asm.JSR(store_character_id, asm.ABS),
    )

    space = Reserve(0x35594, 0x35594, "already equipped esper name color")
    space.write(
        0x2c, # gray, blue shadow
    )

    space = Reserve(0x355af, 0x355b1, "load name length for esper already equipped error message", asm.NOP())
    space.write(
        asm.JSR(unequipable_error, asm.ABS),
    )

    space = Reserve(0x35524, 0x35526, "load esper palette", asm.NOP())
    space.write(
        asm.JSR(check_equipable, asm.ABS),
    )

    space = Reserve(0x358e1, 0x358e5, "load esper palette", asm.NOP())
    space.write(
        asm.JSR(check_equipable, asm.ABS),
    )

    space = Reserve(0x359b1, 0x359b3, "load esper palette", asm.NOP())
    space.write(
        asm.JSR(check_equipable, asm.ABS),
    )

    space = Reserve(0x358e8, 0x358eb, "equip esper if name not grayed out", asm.NOP())
    space.add_label("EQUIP_ESPER", 0x35902)
    space.write(
        asm.CMP(0x20, asm.IMM8),
        asm.BEQ("EQUIP_ESPER"),
    )
