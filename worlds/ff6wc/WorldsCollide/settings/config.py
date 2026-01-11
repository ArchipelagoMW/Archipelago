from ..memory.space import Reserve, Bank, Write
from ..instruction import asm as asm
from .. import args as args

class Config:
    def __init__(self):
        self.mod()

    def mod(self):
        # Thanks to DoctorDT for most of this code

        # Set default configuration options to the most popular:
        # Config1: Msg Speed = 1 (Fastest), Bat Speed = 6 (Slowest), Bat Mode = 1 (Wait)

        # Config 1, set by this code:
        #   C3/70B8:	A92A    	LDA #$2A       ; Bat.Mode, etc.
        # RAM $1D4D, one byte sets: cmmm wbbb (command set c, message spd mmm + 1, battle mode w, battle speed bbb + 1)
        space = Reserve(0x370b9, 0x370b9, "config 1 default")
        space.write(0x0D) # default: 0x2A

        # Moving default location for Config 2 and 3 to support command line re-configuration
        # Set default memory location for Config #2:
        src = [
            asm.LDA(0x00, asm.IMM8),                    # LDA #$00;
            asm.STA(0x1D54, asm.ABS),                   # STA $1D54;  # Config #2
            asm.RTS(),
            ]
        space = Write(Bank.C3, src, "Config #2 default value")

        # Update the JSR for Config default #2
        config2_loc = space.start_address
        space = Reserve(0x370c2, 0x370c4, "Config_2_default")  # 0x0370C2: ['20', PP, NN, '20', PP + 06, NN]])  # JSR #$CONF2; JSR #$CONF3
        space.write(
            asm.JSR(config2_loc, asm.ABS),
        )
        # Config 3, set by this code:
        #   C3/70C5:	9C4E1D  	STZ $1D4E      ; Wallpaper, etc.
        # RAM $1D4E, one byte sets: gcsr wwww (gauge g, cursor c, sound s, reequip r, wallpaper wwww (0-7))
        src = [
            asm.LDA(0x00, asm.IMM8),  # default: 0
            asm.STA(0x1D4E, asm.ABS),  
            asm.RTS(),
        ]
        space = Write(Bank.C3, src, "Config_3_default")

        # Update the JSR for Config default #3
        config3_loc = space.start_address
        space = Reserve(0x370c5, 0x370c7, "Config_3_default")
        space.write(
            asm.JSR(config3_loc, asm.ABS),
        )
