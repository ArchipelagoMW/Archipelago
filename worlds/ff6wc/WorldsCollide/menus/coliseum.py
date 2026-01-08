from ..memory.space import Bank, Reserve, Allocate
from ..instruction import asm as asm
from .. import args as args

class ColiseumMenu:
    def __init__(self):
        self.free_space = Allocate(Bank.C3, 201, "coliseum menu")
        self.args = args

        self.mod()

    def item_count_mod(self):
        # update the description and item quantity after handling d-pad
        draw_item_quantity = self.free_space.next_address

        # if the first character in the description is <end> then clear the description
        # have to write <space><end> to clear it instead of just <end>
        # not entirely sure why I need to do this myself, how does item menu handle it?
        # there is already similar code at c3576d, but c3573a checks for blank slot, not blank description
        self.free_space.copy_from(0x382f1, 0x382fa) # load description pointers and item in cursor slot
        self.free_space.copy_from(0x3573c, 0x35746) # load first character of description
        self.free_space.write(
            asm.BEQ("NO_DESCRIPTION"),  # branch if first character is 0x00 (i.e. <end>)

            asm.JSR(0x5747, asm.ABS),   # load the description
            asm.BRA("DRAW_QUANTITY"),

            "NO_DESCRIPTION",
            asm.JSR(0x576d, asm.ABS),   # overwrite current description text with <space><end>

            "DRAW_QUANTITY",
            asm.LDX(0x4b, asm.DIR),     # x = cursor slot
            asm.LDA(0x1969, asm.ABS_X), # a = item quantity
            asm.JSR(0x04e0, asm.ABS),   # convert to text
            asm.LDX(0x7ac1, asm.IMM16), # position to draw text
            asm.JSR(0x04b6, asm.ABS),   # draw 2 digits
            asm.JSR(0x0f61, asm.ABS),   # upload bg3 a version 2
            asm.RTS(),
        )

        space = Reserve(0x3aced, 0x3acef, "coliseum sustain item menu load item description")
        space.write(
            asm.JSR(draw_item_quantity, asm.ABS),
        )

        space = Reserve(0x3ad65, 0x3ad67, "coliseum initialize item menu load item description")
        space.write(
            asm.JSR(draw_item_quantity, asm.ABS),
        )

        # when initializing coliseum item menu, an empty item is added to inventory
        # this seems useless and causes a bug when displaying item quantity
        # if the first inventory slot is empty its quantity will increment each time the menu is initialized
        # because the add item to inventory (c39d5e) function checks the slot before checking for empty item
        # c39d63 will find a match to the empty item in slot zero and skip the empty item check at c39d68
        space = Reserve(0x3acad, 0x3acb2, "coliseum item menu remove add empty item to inventory?", asm.NOP())

    def display_rewards_mod(self):
        # draw reward icon/name in right column
        draw_reward_item = self.free_space.next_address
        self.free_space.write(
            asm.LDA(0xe6, asm.DIR),         # bg1 write row
            asm.INC(),                      # down a row
            asm.LDX(0x0010, asm.IMM16),     # x position to write at
            asm.JSR(0x809f, asm.ABS),       # calculate position on screen
            asm.A16(),
            asm.STA(0x7e9e89, asm.LNG),     # write position to draw reward at
            asm.A8(),
            asm.TDC(),

            asm.LDX(0x9e8b, asm.IMM16),     # wram LBs
            asm.STX(0x2181, asm.ABS),       # store wram LBs

            "H_BLANK_CHECK",
            asm.LDA(0x4212, asm.ABS),       # PPU status
            asm.AND(0x40, asm.IMM8),        # h-blank?
            asm.BEQ("H_BLANK_CHECK"),

            asm.LDA(0xe5, asm.DIR),         # a = item slot
            asm.TAY(),                      # y = item slot
            asm.LDA(0x1869, asm.ABS_Y),     # a = item in slot
            asm.CMP(0xff, asm.IMM8),        # no item?
            asm.BEQ("LOAD_EMPTY_REWARD"),

            asm.A16(),
            asm.ASL(),
            asm.ASL(),                      # a = item id * 4 (match data 4 bytes each)
            asm.TAX(),                      # x = item id * 4
            asm.TDC(),
            asm.A8(),
            asm.LDA(0xdfb603, asm.LNG_X),   # a = hide reward flag
            asm.BNE("LOAD_UNKNOWN_REWARD"), # branch if reward hidden

            asm.LDA(0xdfb602, asm.LNG_X),   # a = reward id
            asm.JSR(0x80ce, asm.ABS),       # load <icon><name>:

            # above call added a ':' character at the end, remove it
            asm.LDX(0x9e98, asm.IMM16),
            asm.STX(0x2181, asm.ABS),
            asm.STZ(0x2180, asm.ABS),
            asm.BRA("DRAW_REWARD_STRING"),

            "LOAD_UNKNOWN_REWARD",
            asm.LDY(0x000d, asm.IMM16),     # y = 13 (length of ? string)

            "QUESTION_MARK_LOOP",
            asm.LDA(0xbf, asm.IMM8),        # a = '?' character
            asm.STA(0x2180, asm.ABS),       # store '?' character
            asm.DEY(),                      # decrement character index
            asm.BNE("QUESTION_MARK_LOOP"),  # branch if not written all characters yet
            asm.STZ(0x2180, asm.ABS),       # store end of string
            asm.BRA("DRAW_REWARD_STRING"),

            "LOAD_EMPTY_REWARD",
            asm.JSR(0x80f6, asm.ABS),       # load empty string

            "DRAW_REWARD_STRING",
            asm.JSR(0x7fd9, asm.ABS),       # draw loaded reward string
            asm.RTS(),
        )

        # replace draw item quantity with draw reward icon/name
        draw_item_quantity = self.free_space.next_address
        self.free_space.write(
            asm.LDA(0x0200, asm.ABS),       # a = root menu id
            asm.CMP(0x07, asm.IMM8),        # is this the coliseum menu?
            asm.BEQ("DRAW_REWARD"),         # if so, draw reward instead of item quantity
        )
        self.free_space.copy_from(0x37fa8, 0x37fb9) # draw item quantity
        self.free_space.write(
            asm.RTS(),

            "DRAW_REWARD",
            asm.JSR(draw_reward_item, asm.ABS),
            asm.RTS(),
        )

        space = Reserve(0x37fa8, 0x37fb9, "coliseum item menu draw item quantity", asm.NOP())
        space.write(
            asm.JSR(draw_item_quantity, asm.ABS),
        )

        # do not draw item type in coliseum item list
        draw_item_type = self.free_space.next_address
        self.free_space.write(
            asm.LDA(0x0200, asm.ABS),           # a = root menu id
            asm.CMP(0x07, asm.IMM8),            # is this the coliseum menu?
            asm.BEQ("DRAW_ITEM_TYPE_RETURN"),   # skip drawing item type
        )
        self.free_space.copy_from(0x37fd6, 0x37fd8) # call draw item type
        self.free_space.write(
            "DRAW_ITEM_TYPE_RETURN",
            asm.RTS(),
        )

        space = Reserve(0x37fd6, 0x37fd8, "coliseum item menu draw item type")
        space.write(
            asm.JSR(draw_item_type, asm.ABS),
        )

        # <icon><name>:<icon><name> takes up more space than available
        # either the left icon is covered by cursor or last character of right name is covered by scroll bar
        # it looks cleaner to me to have the cursor cover the icon so shift the name left 1 for coliseum item list
        shift_name = self.free_space.next_address
        self.free_space.write(
            asm.LDA(0x0200, asm.ABS),           # a = root menu id
            asm.CMP(0x07, asm.IMM8),            # is this the coliseum menu?
            asm.BEQ("ITEM_NAME_SHIFTED_LEFT"),  # shift item name left by one
            asm.LDX(0x0003, asm.IMM16),         # load original item name position
            asm.RTS(),

            "ITEM_NAME_SHIFTED_LEFT",
            asm.LDX(0x0002, asm.IMM16),         # shift item name position left one
            asm.RTS(),
        )

        space = Reserve(0x37fba, 0x37fbf, "item name position", asm.NOP())
        space.write(
            asm.JSR(shift_name, asm.ABS),
            asm.LDA(0xe6, asm.DIR),             # bg1 write rwo
            asm.INC(),                          # down 1 row
        )

    def mod(self):
        if args.coliseum_rewards_menu:
            self.item_count_mod()
            self.display_rewards_mod()
