from ..memory.space import Allocate, Bank, Reserve, Write
from ..instruction import asm as asm
from ..data.movement import AUTO_SPRINT, B_DASH, ORIGINAL, SPRINT_SHOES_B_DASH, MovementSpeed

class Movement:
    def __init__(self):
        from .. import args as args
        self.movement = args.movement or AUTO_SPRINT

        if self.movement != ORIGINAL:
            self.mod()

    def mod(self):
        length = 0
        src = []

        src = self.get_auto_sprint_src()

        space = Write(Bank.F0, src, "Sprint subroutine")

        src = [
            asm.JSL(space.start_address_snes),
        ]
        space = Reserve(0x04e21, 0x04e37, "auto sprint", asm.NOP())
        space.write(src)

        self.sliding_dash_fix()


    def get_auto_sprint_src(self):
        from .. import args as args
        CURRENT_MAP_BYTE = 0x82 # 2 bytes
        OWZERS_MANSION_ID = 0x00CF # the door room can create visual artifacts on the map while dashing
        CONTROLLER1_BYTE2 = 0x4219
        SPRINT_SHOES_BYTE = 0x11df
        SPRINT_SHOES_MASK = 0x20
        B_BUTTON_MASK = 0x80
        FIELD_RAM_SPEED = 0x0875

        # moving at dash speed in Owzer's door room, or carrying it out via the door glitch will cause graphical artifacting randomly.
        # Simply disabling B button in Owzers to keep it consistent in WC. Will not worry about the door glitch
        owzers_src = [
            "CHECK_OWZERS",
            asm.A16(),                                  # set register A bit size to 16
            asm.LDA(CURRENT_MAP_BYTE, asm.ABS),         # if current map owzers mansion, disable the b-button
            asm.CMP(OWZERS_MANSION_ID, asm.IMM16),
            asm.BEQ("STORE_DEFAULT"),
            asm.LDA(0x0000, asm.IMM16),                 # clear A, otherwise will cause issues in albrook/imperial base
            asm.A8(),
        ]

        src = [
            "B_BUTTON_CHECK",
            asm.LDA(CONTROLLER1_BYTE2, asm.ABS),
            asm.AND(B_BUTTON_MASK, asm.IMM8),
            asm.BEQ("STORE_DEFAULT"),               # do nothing if b pressed
        ]

        if self.movement == AUTO_SPRINT:
            src += [
                "ON_B_BUTTON",
                asm.LDA(MovementSpeed.WALK, asm.IMM8),
                asm.BRA("STORE"),
            ]
        elif self.movement == B_DASH:
            src += owzers_src
            src += [
                "ON_B_BUTTON",
                asm.LDA(MovementSpeed.DASH, asm.IMM8),
                asm.BRA("STORE"),
            ]

        elif self.movement == SPRINT_SHOES_B_DASH:
            src += owzers_src
            src += [
                "ON_B_BUTTON",
                asm.LDA(SPRINT_SHOES_BYTE, asm.ABS),    # If sprint shoes equipped, store secondary movement speed
                asm.AND(SPRINT_SHOES_MASK, asm.IMM8),
                asm.BEQ("WALK")
            ]
            src += [
                "DASH",
                asm.LDA(MovementSpeed.DASH, asm.IMM8),
                asm.BRA("STORE"),
                "WALK",
                asm.LDA(MovementSpeed.WALK, asm.IMM8),
                asm.BRA("STORE"),
            ]

        src += [
            "STORE_DEFAULT",
            asm.A8(),
            asm.LDA(MovementSpeed.SPRINT, asm.IMM8),

            "STORE",
            asm.STA(FIELD_RAM_SPEED, asm.ABS_Y),        # store speed in ram
            asm.RTL(),                                  # return
        ]

        return src


    #  DIRECTION VALUE
    #   $087F ------dd
    #         d: facing direction
    #            00 = up
    #            01 = right
    #            10 = down
    #            11 = left

    # https://silentenigma.neocities.org/ff6/index.html
    # Will leave bits of documentation about in the event neocities does not stand the test of time

    # With dash enabled, this causes a bug that the player will appear to be standing still when
    # running down or right at move speed 5. This is because two sprite instances are thrown out of
    # the animation cycle when running at that speed; while Up/Left correctly omits the standing
    # sprite, Down/Right omits the stepping sprites, since the offsets lag by an iteration.
    def sliding_dash_fix(self):
        DIRECTION_VALUE = 0x087f

        # C0/0000: 4A         	LSR            ; Shift offset bits right
        # C0/0001: 4A         	LSR            ; Shift offset bits right
        # C0/0002: 48         	PHA            ; Push offset value to stack
        # C0/0003: B9 7F 08   	LDA $087F,y    ; Load direction value
        # C0/0006: C9 01      	CMP #$01       ; Check if direction is Right
        # C0/0008: F0 07      	BEQ $D69E      ; Branch if the direction is Right
        # C0/000A: C9 02      	CMP #$02       ; Check if the direction is Down
        # C0/000C: F0 03      	BEQ $D69E      ; Branch if the direction is Down
        # C0/000E: 68         	PLA            ; Pull offset back off of stack
        # C0/000F: 80 02      	BRA $D6A0      ; Branch to the third LSR
        # C0/0011: 68         	PLA            ; Pull offset back off of stack
        # C0/0012: 1A         	INC            ; Increase the offset value by 1
        # C0/0013: 4A         	LSR            ; Shift offset bits right
        # C0/0014: 60         	RTS            ; Return from subfunction
        subroutine_src = [
            asm.LSR(),
            asm.LSR(),
            asm.PHA(),
            asm.LDA(DIRECTION_VALUE, asm.ABS_Y),
            asm.DEC(),
            asm.BEQ("FACING_RIGHT"),
            asm.DEC(),
            asm.BNE("RETURN"),
            "FACING_RIGHT",
            asm.PLA(),
            asm.INC(),
            asm.PHA(),
            "RETURN",
            asm.PLA(),
            asm.LSR(),
            asm.RTS(),
        ]
        subroutine_space = Allocate(Bank.C0, 20, "walking speed calculation", asm.NOP())
        subroutine_space.write(subroutine_src)

        src = [
            asm.JSR(subroutine_space.start_address, asm.ABS)
        ]

        space = Reserve(0x5885, 0x5887, "Sprite offset calculation 1", asm.NOP())
        space.write(src)

        space = Reserve(0x5892, 0x5894, "Sprite offset calculation 2")
        space.write(src)
