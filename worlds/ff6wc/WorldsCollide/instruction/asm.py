# 16 = closing parenthesis, 24 = closing square bracket except for immediates
# e.g. ABS_X_16 = (abs, x)
#      DIR_16_Y = (dir), y
#      IMM16 = 16 bit immediate value
#
# 8 bit, 16 bit, and 24 bit arguments
IMM8, DIR, DIR_X, DIR_Y, DIR_16, DIR_X_16, DIR_16_Y, DIR_24, DIR_24_Y, S, S_16_Y,\
IMM16, ABS, ABS_X, ABS_Y, ABS_16, ABS_X_16, ABS_24,\
LNG, LNG_X = range(20)

class _Instruction:
    def __init__(self, arg, mode):
        self.arg = arg
        self.mode = mode

        # convert arg to bytes based on given mode
        if mode is None:
            self.args = []
        elif mode >= LNG:
            self.args = arg.to_bytes(3, "little")
        elif mode >= IMM16:
            self.args = (arg & 0xffff).to_bytes(2, "little")
        elif arg is not None:
            self.args = (arg & 0xff).to_bytes(1, "little")
        else:
            self.args = []

        self.opcode = self.mode_opcode[mode]

    def __opcode__(self, opcode, arg = None):
        self.opcode = opcode
        self.arg = arg
        self.mode = None
        if arg is not None:
            self.args = arg.to_bytes(1, "little")
        else:
            self.args = []

    def __len__(self):
        return 1 + len(self.args)

    def __call__(self, space):
        return self.opcode, self.args

    def __eq__(self, other):
        return type(self) is type(other) and self() == other()

    def __str__(self):
        result = type(self).__name__
        if self.arg is not None:
            arg_value = int.from_bytes(self.args, "little")
            if self.mode in [IMM8, IMM16]:
                result += f" #${arg_value:0{len(self.args) * 2}x}"
            elif self.mode in [DIR_X, ABS_X, LNG_X]:
                result += f" ${arg_value:0{len(self.args) * 2}x}, X"
            elif self.mode == DIR_Y:
                result += f" ${arg_value:0{len(self.args) * 2}x}, Y"
            elif self.mode in [DIR_16, ABS_16]:
                result += f" (${arg_value:0{len(self.args) * 2}x})"
            elif self.mode in [DIR_X_16, ABS_X_16]:
                result += f" (${arg_value:0{len(self.args) * 2}x}, X)"
            elif self.mode == DIR_16_Y:
                result += f" (${arg_value:0{len(self.args) * 2}x}), Y"
            elif self.mode in [DIR_24, ABS_24]:
                result += f" [${arg_value:0{len(self.args) * 2}x}]"
            elif self.mode == DIR_24_Y:
                result += f" [${arg_value:0{len(self.args) * 2}x}], Y"
            elif self.mode == S:
                result += f" ${arg_value:0{len(self.args) * 2}x}, S"
            elif self.mode == S_16_Y:
                result += f" (${arg_value:0{len(self.args) * 2}x}, S), Y"
            else:
                result += f" ${arg_value:0{len(self.args) * 2}x}"

        return result

class NOP(_Instruction):
    def __init__(self):
        super().__opcode__(0xea)

class REP(_Instruction):
    def __init__(self, arg):
        super().__opcode__(0xc2, arg)

class SEP(_Instruction):
    def __init__(self, arg):
        super().__opcode__(0xe2, arg)

A8 = lambda : SEP(0x20)
XY8 = lambda : SEP(0x10)
AXY8 = lambda : SEP(0x30)
A16 = lambda : REP(0x20)
XY16 = lambda : REP(0x10)
AXY16 = lambda : REP(0x30)

class PHA(_Instruction):
    def __init__(self):
        super().__opcode__(0x48)

class PLA(_Instruction):
    def __init__(self):
        super().__opcode__(0x68)

class PHX(_Instruction):
    def __init__(self):
        super().__opcode__(0xda)

class PLX(_Instruction):
    def __init__(self):
        super().__opcode__(0xfa)

class PHY(_Instruction):
    def __init__(self):
        super().__opcode__(0x5a)

class PLY(_Instruction):
    def __init__(self):
        super().__opcode__(0x7a)

class PHP(_Instruction):
    def __init__(self):
        super().__opcode__(0x08)

class PLP(_Instruction):
    def __init__(self):
        super().__opcode__(0x28)

class PHB(_Instruction):
    def __init__(self):
        super().__opcode__(0x8b)

class PLB(_Instruction):
    def __init__(self):
        super().__opcode__(0xab)

class PHK(_Instruction):
    def __init__(self):
        super().__opcode__(0x4b)

class PEI(_Instruction):
    mode_opcode = {
                   DIR      : 0xd4,
                  }

    def __init__(self, arg):
        super().__init__(arg, DIR)

class PER(_Instruction):
    mode_opcode = {
                   IMM16    : 0x62,
                  }

    def __init__(self, arg):
        super().__init__(arg, IMM16)

class PEA(_Instruction):
    mode_opcode = {
                   IMM16    : 0xf4,
                  }

    def __init__(self, arg):
        super().__init__(arg, IMM16)

class TAX(_Instruction):
    def __init__(self):
        super().__opcode__(0xaa)

class TXA(_Instruction):
    def __init__(self):
        super().__opcode__(0x8a)

class TAY(_Instruction):
    def __init__(self):
        super().__opcode__(0xa8)

class TYA(_Instruction):
    def __init__(self):
        super().__opcode__(0x98)

class TXY(_Instruction):
    def __init__(self):
        super().__opcode__(0x9b)

class TYX(_Instruction):
    def __init__(self):
        super().__opcode__(0xbb)

class TXS(_Instruction):
    def __init__(self):
        super().__opcode__(0x9a)

class TSX(_Instruction):
    def __init__(self):
        super().__opcode__(0xba)

class LDA(_Instruction):
    mode_opcode = {
        DIR_X_16 : 0xa1,
        S        : 0xa3,
        DIR      : 0xa5,
        DIR_24   : 0xa7,
        IMM8     : 0xa9,
        IMM16    : 0xa9,
        ABS      : 0xad,
        LNG      : 0xaf,
        DIR_16_Y : 0xb1,
        DIR_16   : 0xb2,
        S_16_Y   : 0xb3,
        DIR_X    : 0xb5,
        DIR_24_Y : 0xb7,
        ABS_Y    : 0xb9,
        ABS_X    : 0xbd,
        LNG_X    : 0xbf,
    }

class LDX(_Instruction):
    mode_opcode = {
        IMM8     : 0xa2,
        IMM16    : 0xa2,
        DIR      : 0xa6,
        ABS      : 0xae,
        DIR_Y    : 0xb6,
        ABS_Y    : 0xbe,
    }

class LDY(_Instruction):
    mode_opcode = {
        IMM8     : 0xa0,
        IMM16    : 0xa0,
        DIR      : 0xa4,
        ABS      : 0xac,
        DIR_X    : 0xb4,
        ABS_X    : 0xbc,
    }

class STA(_Instruction):
    mode_opcode = {
        DIR_X_16 : 0x81,
        S        : 0x83,
        DIR      : 0x85,
        DIR_24   : 0x87,
        ABS      : 0x8d,
        LNG      : 0x8f,
        DIR_16_Y : 0x91,
        DIR_16   : 0x92,
        S_16_Y   : 0x93,
        DIR_X    : 0x95,
        DIR_24_Y : 0x97,
        ABS_Y    : 0x99,
        ABS_X    : 0x9d,
        LNG_X    : 0x9f,
    }

class STX(_Instruction):
    mode_opcode = {
        DIR      : 0x86,
        ABS      : 0x8e,
        DIR_Y    : 0x96,
    }

class STY(_Instruction):
    mode_opcode = {
        DIR      : 0x84,
        ABS      : 0x8c,
        DIR_X    : 0x94,
    }

class STZ(_Instruction):
    mode_opcode = {
        DIR      : 0x64,
        DIR_X    : 0x74,
        ABS      : 0x9c,
        ABS_X    : 0x9e,
    }

class INC(_Instruction):
    mode_opcode = {
        None     : 0x1a,
        DIR      : 0xe6,
        ABS      : 0xee,
        DIR_X    : 0xf6,
        ABS_X    : 0xfe,
    }

    def __init__(self, arg = None, mode = None):
            super().__init__(arg, mode)

class DEC(_Instruction):
    mode_opcode = {
        None     : 0x3a,
        DIR      : 0xc6,
        ABS      : 0xce,
        DIR_X    : 0xd6,
        ABS_X    : 0xde,
    }

    def __init__(self, arg = None, mode = None):
        super().__init__(arg, mode)

class INX(_Instruction):
    def __init__(self):
        super().__opcode__(0xe8)

class DEX(_Instruction):
    def __init__(self):
        super().__opcode__(0xca)

class INY(_Instruction):
    def __init__(self):
        super().__opcode__(0xc8)

class DEY(_Instruction):
    def __init__(self):
        super().__opcode__(0x88)

class AND(_Instruction):
    mode_opcode = {
        DIR_X_16 : 0x21,
        S        : 0x23,
        DIR      : 0x25,
        DIR_24   : 0x27,
        IMM8     : 0x29,
        IMM16    : 0x29,
        ABS      : 0x2d,
        LNG      : 0x2f,
        DIR_16_Y : 0x31,
        DIR_16   : 0x32,
        S_16_Y   : 0x33,
        DIR_X    : 0x35,
        DIR_24_Y : 0x37,
        ABS_Y    : 0x39,
        ABS_X    : 0x3d,
        LNG_X    : 0x3f,
    }

class XOR(_Instruction):
    mode_opcode = {
        DIR_X_16 : 0x41,
        S        : 0x43,
        DIR      : 0x45,
        DIR_24   : 0x47,
        IMM8     : 0x49,
        IMM16    : 0x49,
        ABS      : 0x4d,
        LNG      : 0x4f,
        DIR_16_Y : 0x51,
        DIR_16   : 0x52,
        S_16_Y   : 0x53,
        DIR_X    : 0x55,
        DIR_24_Y : 0x57,
        ABS_Y    : 0x59,
        ABS_X    : 0x5d,
        LNG_X    : 0x5f,
    }
EOR = XOR

class ORA(_Instruction):
    mode_opcode = {
        DIR_X_16 : 0x01,
        S        : 0x03,
        DIR      : 0x05,
        DIR_24   : 0x07,
        IMM8     : 0x09,
        IMM16    : 0x09,
        ABS      : 0x0d,
        LNG      : 0x0f,
        DIR_16_Y : 0x11,
        DIR_16   : 0x12,
        S_16_Y   : 0x13,
        DIR_X    : 0x15,
        DIR_24_Y : 0x17,
        ABS_Y    : 0x19,
        ABS_X    : 0x1d,
        LNG_X    : 0x1f,
    }

class ASL(_Instruction):
    mode_opcode = {
        DIR      : 0x06,
        None     : 0x0a,
        ABS      : 0x0e,
        DIR_X    : 0x16,
        ABS_X    : 0x1e,
    }

    def __init__(self, arg = None, mode = None):
        super().__init__(arg, mode)

class LSR(_Instruction):
    mode_opcode = {
        DIR      : 0x46,
        None     : 0x4a,
        ABS      : 0x4e,
        DIR_X    : 0x56,
        ABS_X    : 0x5e,
    }

    def __init__(self, arg = None, mode = None):
        super().__init__(arg, mode)

class ROL(_Instruction):
    mode_opcode = {
        DIR      : 0x26,
        None     : 0x2a,
        ABS      : 0x2e,
        DIR_X    : 0x36,
        ABS_X    : 0x3e,
    }

    def __init__(self, arg = None, mode = None):
        super().__init__(arg, mode)

class ROR(_Instruction):
    mode_opcode = {
        DIR      : 0x66,
        None     : 0x6a,
        ABS      : 0x6e,
        DIR_X    : 0x76,
        ABS_X    : 0x7e,
    }

    def __init__(self, arg = None, mode = None):
        super().__init__(arg, mode)

class ADC(_Instruction):
    mode_opcode = {
        DIR_X_16 : 0x61,
        S        : 0x63,
        DIR      : 0x65,
        DIR_24   : 0x67,
        IMM8     : 0x69,
        IMM16    : 0x69,
        ABS      : 0x6d,
        LNG      : 0x6f,
        DIR_16_Y : 0x71,
        DIR_16   : 0x72,
        S_16_Y   : 0x73,
        DIR_X    : 0x75,
        DIR_24_Y : 0x77,
        ABS_Y    : 0x79,
        ABS_X    : 0x7d,
        LNG_X    : 0x7f,
    }

class SBC(_Instruction):
    mode_opcode = {
        DIR_X_16 : 0xe1,
        S        : 0xe3,
        DIR      : 0xe5,
        DIR_24   : 0xe7,
        IMM8     : 0xe9,
        IMM16    : 0xe9,
        ABS      : 0xed,
        LNG      : 0xef,
        DIR_16_Y : 0xf1,
        DIR_16   : 0xf2,
        S_16_Y   : 0xf3,
        DIR_X    : 0xf5,
        DIR_24_Y : 0xf7,
        ABS_Y    : 0xf9,
        ABS_X    : 0xfd,
        LNG_X    : 0xff,
    }

class BIT(_Instruction):
    mode_opcode = {
        DIR      : 0x24,
        ABS      : 0x2c,
        DIR_X    : 0x34,
        ABS_X    : 0x3c,
        IMM8     : 0x89,
        IMM16    : 0x89,
    }

class TSB(_Instruction):
    mode_opcode = {
        DIR      : 0x04,
        ABS      : 0x0c,
    }

class TRB(_Instruction):
    mode_opcode = {
        DIR      : 0x14,
        ABS      : 0x1c,
    }

class CMP(_Instruction):
    mode_opcode = {
        DIR_X_16 : 0xc1,
        S        : 0xc3,
        DIR      : 0xc5,
        DIR_24   : 0xc7,
        IMM8     : 0xc9,
        IMM16    : 0xc9,
        ABS      : 0xcd,
        LNG      : 0xcf,
        DIR_16_Y : 0xd1,
        DIR_16   : 0xd2,
        S_16_Y   : 0xd3,
        DIR_X    : 0xd5,
        DIR_24_Y : 0xd7,
        ABS_Y    : 0xd9,
        ABS_X    : 0xdd,
        LNG_X    : 0xdf,
    }

class CPX(_Instruction):
    mode_opcode = {
        IMM8     : 0xe0,
        IMM16    : 0xe0,
        DIR      : 0xe4,
        ABS      : 0xec,
    }

class CPY(_Instruction):
    mode_opcode = {
        IMM8     : 0xc0,
        IMM16    : 0xc0,
        DIR      : 0xc4,
        ABS      : 0xcc,
    }

class _Branch(_Instruction):
    def __init__(self, opcode, arg):
        if isinstance(arg, str):
            self.opcode = opcode
            self.args = arg
            self.arg = arg
        else:
            super().__opcode__(opcode, arg)

    def __len__(self):
        if isinstance(self.args, str):
            return 2
        return super().__len__()

    def __call__(self, space):
        if isinstance(self.args, str):
            self.branch_distance = space.branch_distance(self.args)
            return self.opcode, self.branch_distance
        return super().__call__(space)

    def __str__(self):
        result = type(self).__name__
        if isinstance(self.arg, str):
            return result + f" '{self.arg}'"
        return super().__str__()

class BRA(_Branch):
    def __init__(self, arg):
        super().__init__(0x80, arg)

class BEQ(_Branch):
    def __init__(self, arg):
        super().__init__(0xf0, arg)

class BNE(_Branch):
    def __init__(self, arg):
        super().__init__(0xd0, arg)

class BCS(_Branch):
    def __init__(self, arg):
        super().__init__(0xb0, arg)
BGE = BCS

class BCC(_Branch):
    def __init__(self, arg):
        super().__init__(0x90, arg)
BLT = BCC

class BMI(_Branch):
    def __init__(self, arg):
        super().__init__(0x30, arg)

class BPL(_Branch):
    def __init__(self, arg):
        super().__init__(0x10, arg)

class BVS(_Branch):
    def __init__(self, arg):
        super().__init__(0x70, arg)

class BVC(_Branch):
    def __init__(self, arg):
        super().__init__(0x50, arg)

class CLC(_Instruction):
    def __init__(self):
        super().__opcode__(0x18)

class SEC(_Instruction):
    def __init__(self):
        super().__opcode__(0x38)

class JMP(_Instruction):
    mode_opcode = {
        ABS      : 0x4c,
        LNG      : 0x5c,
        ABS_16   : 0x6c,
        ABS_X_16 : 0x7c,
        ABS_24   : 0xdc,
    }

class JSR(_Instruction):
    mode_opcode = {
        ABS      : 0x20,
        ABS_X_16 : 0xfc,
    }

class JSL(_Instruction):
    mode_opcode = {
        LNG      : 0x22,
    }

    def __init__(self, arg):
        super().__init__(arg, LNG)

class RTS(_Instruction):
    def __init__(self):
        super().__opcode__(0x60)

class RTL(_Instruction):
    def __init__(self):
        super().__opcode__(0x6b)

class XBA(_Instruction):
    def __init__(self):
        super().__opcode__(0xeb)

class TCD(_Instruction):
    def __init__(self):
        super().__opcode__(0x5b)

class TDC(_Instruction):
    def __init__(self):
        super().__opcode__(0x7b)
