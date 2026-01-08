import binascii
from typing import Optional, Dict, Iterator, List, Union, Tuple, Generator

from . import utils
import os
import re
import pkgutil
import unicodedata


REGS8 = {"A": 7, "B": 0, "C": 1, "D": 2, "E": 3, "H": 4, "L": 5, "[HL]": 6}
REGS16A = {"BC": 0, "DE": 1, "HL": 2, "SP": 3}
REGS16B = {"BC": 0, "DE": 1, "HL": 2, "AF": 3}
FLAGS = {"NZ": 0x00, "Z": 0x08, "NC": 0x10, "C": 0x18}

CONST_MAP: Dict[str, int] = {}


class ExprBase:
    def asReg8(self) -> Optional[int]:
        return None

    def isA(self, kind: str, value: Optional[str] = None) -> bool:
        return False


class Token(ExprBase):
    def __init__(self, kind: str, value: Union[str, int], line_nr: int) -> None:
        self.kind = kind
        self.value = value
        self.line_nr = line_nr

    def isA(self, kind: str, value: Optional[str] = None) -> bool:
        return self.kind == kind and (value is None or value == self.value)

    def __repr__(self) -> str:
        return "[%s:%s:%d]" % (self.kind, self.value, self.line_nr)

    def asReg8(self) -> Optional[int]:
        if self.kind == 'ID':
            return REGS8.get(str(self.value), None)
        return None

    def copy(self):
        return Token(self.kind, self.value, self.line_nr)


class REF(ExprBase):
    def __init__(self, expr: ExprBase) -> None:
        self.expr = expr

    def asReg8(self) -> Optional[int]:
        if self.expr.isA('ID', 'HL'):
            return REGS8['[HL]']
        return None

    def __repr__(self) -> str:
        return "[%s]" % (self.expr)


class OP(ExprBase):
    def __init__(self, op: str, left: ExprBase, right: Optional[ExprBase] = None):
        self.op = op
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return "(%s %s %s)" % (self.left, self.op, self.right)

    @staticmethod
    def make(op: str, left: ExprBase, right: Optional[ExprBase] = None) -> ExprBase:
        if left.isA('NUMBER') and right is not None and right.isA('NUMBER'):
            assert isinstance(right, Token) and isinstance(right.value, int)
            assert isinstance(left, Token) and isinstance(left.value, int)
            if op == '+':
                left.value += right.value
                return left
            if op == '-':
                left.value -= right.value
                return left
            if op == '*':
                left.value *= right.value
                return left
            if op == '/':
                left.value //= right.value
                return left
            if op == '<':
                left.value = 1 if left.value < right.value else 0
                return left
            if op == '>':
                left.value = 1 if left.value > right.value else 0
                return left
            if op == '<=':
                left.value = 1 if left.value <= right.value else 0
                return left
            if op == '>=':
                left.value = 1 if left.value >= right.value else 0
                return left
            if op == '==':
                left.value = 1 if left.value == right.value else 0
                return left
            if op == '<<':
                left.value <<= right.value
                return left
            if op == '>>':
                left.value >>= right.value
                return left
            if op == '&':
                left.value &= right.value
                return left
            if op == '|':
                left.value |= right.value
                return left
        if left.isA('NUMBER') and right is None:
            assert isinstance(left, Token) and isinstance(left.value, int)
            if op == '+':
                return left
            if op == '-':
                left.value = -left.value
                return left
        return OP(op, left, right)


class CALL(ExprBase):
    def __init__(self, function, params, *, line_nr):
        self.function = function
        self.params = params
        self.line_nr = line_nr

    def __repr__(self) -> str:
        return f"{self.function}({self.params})"


class AssemblerException(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message


class Tokenizer:
    TOKEN_REGEX = re.compile('|'.join('(?P<%s>%s)' % pair for pair in [
        ('NUMBER', r'\d+(\.\d*)?'),
        ('HEX', r'\$[0-9A-Fa-f]+'),
        ('ASSIGN', r':='),
        ('COMMENT', r';[^\n]*'),
        ('LABEL', r':'),
        ('DIRECTIVE', r'#[A-Za-z_]+'),
        ('STRING', '[a-zA-Z]?"[^"]*"'),
        ('ID', r'\.?[A-Za-z_][A-Za-z0-9_\.]*'),
        ('OP', r'(?:<=)|(?:>=)|(?:==)|(?:<<)|(?:>>)|[+\-*/,\(\)<>&|]'),
        ('REFOPEN', r'\['),
        ('REFCLOSE', r'\]'),
        ('MACROARG', r'\\[0-9]+'),
        ('TOKENCONCAT', r'##'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]))

    def __init__(self, code: str) -> None:
        self.__tokens: List[Token] = []
        self.shiftCode(code)

    def shiftCode(self, code: str) -> None:
        new_tokens: List[Token] = []
        line_num = 1
        for mo in self.TOKEN_REGEX.finditer(code):
            kind = mo.lastgroup
            assert kind is not None
            value: Union[str, int] = mo.group()
            if kind == 'MISMATCH':
                print(code.split("\n")[line_num-1])
                raise AssemblerException(Token('?', '', line_num), "Syntax error on line: %d: %s" % (line_num, value))
            elif kind == 'SKIP':
                pass
            elif kind == 'COMMENT':
                pass
            else:
                if kind == 'NUMBER':
                    value = int(value)
                elif kind == 'HEX':
                    value = int(str(value)[1:], 16)
                    kind = 'NUMBER'
                elif kind == 'ID':
                    value = str(value).upper()
                new_tokens.append(Token(kind, value, line_num))
                if kind == 'NEWLINE':
                    line_num += 1
        new_tokens.append(Token('NEWLINE', '\n', line_num))
        self.shift(new_tokens)

    def peek(self) -> Token:
        return self.__tokens[0]

    def pop(self) -> Token:
        return self.__tokens.pop(0)

    def shift(self, tokens: List[Token]) -> None:
        self.__tokens = tokens + self.__tokens

    def expect(self, kind: str, value: Optional[str] = None) -> Token:
        pop = self.pop()
        if not pop.isA(kind, value):
            if value is not None:
                raise AssemblerException(pop, "%s != %s:%s" % (pop, kind, value))
            raise AssemblerException(pop, "%s != %s" % (pop, kind))
        return pop

    def popIf(self, kind: str, value: Optional[str] = None) -> bool:
        token = self.peek()
        if token.isA(kind, value):
            self.pop()
            return True
        return False

    def __bool__(self) -> bool:
        return bool(self.__tokens)


class Section:
    def __init__(self, base_address: Optional[int] = None, bank: Optional[int] = None) -> None:
        self.base_address = base_address if base_address is not None else -1
        self.bank = bank
        self.data = bytearray()
        self.link: Dict[int, Tuple[int, ExprBase]] = {}

    def __repr__(self) -> str:
        if self.bank is not None:
            return f"Section@{self.bank:02x}:{self.base_address:04x} {binascii.hexlify(self.data).decode('ascii')}"
        if self.base_address > -1:
            return f"Section@{self.base_address:04x} {binascii.hexlify(self.data).decode('ascii')}"
        return f"Section {binascii.hexlify(self.data).decode('ascii')}"


class Assembler:
    SIMPLE_INSTR = {
        'NOP':  0x00,
        'RLCA': 0x07,
        'RRCA': 0x0F,
        'STOP': 0x010,
        'RLA':  0x17,
        'RRA':  0x1F,
        'DAA':  0x27,
        'CPL':  0x2F,
        'SCF':  0x37,
        'CCF':  0x3F,
        'HALT': 0x76,
        'RETI': 0xD9,
        'DI':   0xF3,
        'EI':   0xFB,
    }

    LINK_REL8 = 0
    LINK_ABS8 = 1
    LINK_ABS16 = 2
    LINK_HIGH8 = 3

    def __init__(self) -> None:
        self.__sections: List[Section] = []
        self.__current_section = Section()
        self.__label: Dict[str, Tuple[Section, int]] = {}
        self.__constant: Dict[str, int] = {}
        self.__scope: Optional[str] = None
        self.__macros: Dict[str, List[Token]] = {}
        self.__asserts: List[Tuple[Token, ExprBase]] = []
        self.__base_path = None
        self.__tok = Tokenizer("")

    def processFile(self, base_path: str, filename: str, **kwargs):
        data = pkgutil.get_data(base_path, filename)
        if data is None:
            raise FileNotFoundError(f"{base_path}/{filename}")
        self.process(data.decode("utf-8"), **kwargs)

    def newSection(self, *, base_address: Optional[int] = None, bank: Optional[int] = None):
        self.__current_section = Section(base_address, bank)
        self.__sections.append(self.__current_section)
        self.__scope = None

    def process(self, code: str, *, base_address: Optional[int] = None, bank: Optional[int] = None) -> None:
        self.newSection(base_address=base_address, bank=bank)
        conditional_stack = [True]
        self.__tok = Tokenizer(code)
        while self.__tok:
            start = self.__tok.pop()
            if start.kind == 'NEWLINE':
                pass  # Empty newline
            elif start.kind == 'DIRECTIVE':
                if start.value == '#IF':
                    t = self.parseExpression()
                    assert isinstance(t, Token)
                    conditional_stack.append(conditional_stack[-1] and t.value != 0)
                    self.__tok.expect('NEWLINE')
                elif start.value == '#ELSE':
                    conditional_stack[-1] = not conditional_stack[-1] and conditional_stack[-2]
                    self.__tok.expect('NEWLINE')
                elif start.value == '#ENDIF':
                    conditional_stack.pop()
                    assert conditional_stack
                    self.__tok.expect('NEWLINE')
                elif start.value == '#MACRO':
                    name = self.__tok.expect('ID')
                    self.__tok.expect('NEWLINE')
                    macro = []
                    while not self.__tok.peek().isA('DIRECTIVE', '#END'):
                        macro.append(self.__tok.pop())
                        if not self.__tok:
                            raise AssemblerException(name, 'Unterminated macro')
                    self.__tok.pop()
                    self.__tok.expect('NEWLINE')
                    self.__macros[name.value] = macro
                elif start.value == '#INCLUDE':
                    filename = self.__tok.expect('STRING').value[1:-1]
                    self.__tok.expect('NEWLINE')
                    data = pkgutil.get_data(self.__base_path, filename)
                    if data is None:
                        raise FileNotFoundError(f"{self.__base_path}/{filename}")
                    self.__tok.shiftCode(data.decode("utf-8"))
                elif start.value == '#ALIGN':
                    value = self.__tok.expect('NUMBER').value
                    self.__tok.expect('NEWLINE')
                    while len(self.__current_section.data) % value:
                        self.__current_section.data.append(0)
                elif start.value == '#INCGFX':
                    filename = self.__tok.expect('STRING').value[1:-1]
                    self.__tok.expect('NEWLINE')
                    import patches.aesthetics
                    self.__current_section.data += patches.aesthetics.imageTo2bpp(os.path.join(self.__base_path, filename), tileheight=8)
                elif start.value == '#ASSERT':
                    self.__asserts.append((start, self.parseExpression()))
                    self.__tok.expect('NEWLINE')
                else:
                    raise AssemblerException(start, "Unexpected directive")
            elif not conditional_stack[-1]:
                while not self.__tok.pop().isA('NEWLINE'):
                    pass
            elif start.kind == 'ID':
                if start.value == 'DB':
                    self.instrDB()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'DS':
                    self.instrDS()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'DW':
                    self.instrDW()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'LD':
                    self.instrLD()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'LDH':
                    self.instrLDH()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'LDI':
                    self.instrLDI()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'LDD':
                    self.instrLDD()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'INC':
                    self.instrINC()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'DEC':
                    self.instrDEC()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'ADD':
                    self.instrADD()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'ADC':
                    self.instrALU(0x88)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'SUB':
                    self.instrALU(0x90)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'SBC':
                    self.instrALU(0x98)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'AND':
                    self.instrALU(0xA0)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'XOR':
                    self.instrALU(0xA8)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'OR':
                    self.instrALU(0xB0)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'CP':
                    self.instrALU(0xB8)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'BIT':
                    self.instrBIT(0x40)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'RES':
                    self.instrBIT(0x80)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'SET':
                    self.instrBIT(0xC0)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'RET':
                    self.instrRET()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'CALL':
                    self.instrCALL()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'RLC':
                    self.instrCB(0x00)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'RRC':
                    self.instrCB(0x08)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'RL':
                    self.instrCB(0x10)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'RR':
                    self.instrCB(0x18)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'SLA':
                    self.instrCB(0x20)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'SRA':
                    self.instrCB(0x28)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'SWAP':
                    self.instrCB(0x30)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'SRL':
                    self.instrCB(0x38)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'RST':
                    self.instrRST()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'JP':
                    self.instrJP()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'JR':
                    self.instrJR()
                    self.__tok.expect('NEWLINE')
                elif start.value == 'PUSH':
                    self.instrPUSHPOP(0xC5)
                    self.__tok.expect('NEWLINE')
                elif start.value == 'POP':
                    self.instrPUSHPOP(0xC1)
                    self.__tok.expect('NEWLINE')
                elif start.value in self.SIMPLE_INSTR:
                    self.__current_section.data.append(self.SIMPLE_INSTR[str(start.value)])
                    self.__tok.expect('NEWLINE')
                elif start.value in self.__macros:
                    params = [[]]
                    while not self.__tok.peek().isA('NEWLINE'):
                        if self.__tok.peek().isA('OP', ','):
                            params.append([])
                            self.__tok.pop()
                        else:
                            params[-1].append(self.__tok.pop())
                    self.__tok.pop()
                    to_add = []
                    concat = False
                    for token in self.__macros[start.value]:
                        if concat:
                            concat = False
                            if not to_add[-1].isA('ID'):
                                raise AssemblerException(token, "Can only concat ID tokens")
                            to_add[-1] = to_add[-1].copy()
                            if token.isA('MACROARG'):
                                argn = int(token.value[1:]) - 1
                                if argn >= len(params):
                                    raise AssemblerException(start, "Missing argument for macro")
                                for p in params[int(token.value[1:]) - 1]:
                                    to_add[-1].value += p.value
                            else:
                                to_add[-1].value = to_add[-1].value + token.value
                        elif token.isA('MACROARG'):
                            argn = int(token.value[1:]) - 1
                            if argn >= len(params):
                                raise AssemblerException(start, "Missing argument for macro")
                            for p in params[argn]:
                                to_add.append(p.copy())
                        elif token.isA('TOKENCONCAT'):
                            concat = True
                        else:
                            to_add.append(token.copy())
                    self.__tok.shift(to_add)
                elif self.__tok.peek().kind == 'LABEL':
                    self.__tok.pop()
                    self.addLabel(str(start.value))
                elif self.__tok.peek().kind == 'ASSIGN':
                    self.__tok.pop()
                    value = self.parseExpression()
                    if value.kind != 'NUMBER':
                        raise AssemblerException(start, "Can only assign numbers")
                    self.setConstant(str(start.value), int(value.value))
                else:
                    raise AssemblerException(start, "Syntax error")
            else:
                raise AssemblerException(start, "Syntax error")

    def insert8(self, expr: ExprBase) -> None:
        if expr.isA('NUMBER'):
            assert isinstance(expr, Token)
            value = int(expr.value)
        else:
            self.__current_section.link[len(self.__current_section.data)] = (Assembler.LINK_ABS8, expr)
            value = 0
        if 0 <= value < 0x100:
            self.__current_section.data.append(value)
        else:
            raise AssemblerException(expr, "8 bit value out of range")

    def insertHigh8(self, expr: ExprBase) -> None:
        if expr.isA('NUMBER'):
            assert isinstance(expr, Token)
            value = int(expr.value)
        else:
            self.__current_section.link[len(self.__current_section.data)] = (Assembler.LINK_HIGH8, expr)
            value = 0
        if 0xFF00 <= value < 0x10000:
            self.__current_section.data.append(value & 0xFF)
        else:
            raise AssemblerException(expr, "HRAM 8 bit value out of range")

    def insertRel8(self, expr: ExprBase) -> None:
        if expr.isA('NUMBER'):
            assert isinstance(expr, Token)
            self.__current_section.data.append(int(expr.value))
        else:
            self.__current_section.link[len(self.__current_section.data)] = (Assembler.LINK_REL8, expr)
            self.__current_section.data.append(0x00)

    def insert16(self, expr: ExprBase) -> None:
        if expr.isA('NUMBER'):
            assert isinstance(expr, Token)
            value = int(expr.value)
        else:
            self.__current_section.link[len(self.__current_section.data)] = (Assembler.LINK_ABS16, expr)
            value = 0
        assert 0 <= value <= 0xFFFF
        self.__current_section.data.append(value & 0xFF)
        self.__current_section.data.append(value >> 8)

    def insertString(self, token: Token) -> None:
        string = token.value
        if string.startswith('"') and string.endswith('"'):
            string = string[1:-1]
            string = unicodedata.normalize('NFKD', string)
            self.__current_section.data += string.encode("latin1", "ignore")
        elif string.startswith("m\"") and string.endswith("\""):
            self.__current_section.data += utils.formatText(string[2:-1].replace("|", "\n"))
        else:
            raise AssemblerException(token, f"Cannot handle string: {string}")

    def insertData(self, data: bytes) -> None:
        self.__current_section.data += data

    def currentSectionSize(self) -> int:
        return len(self.__current_section.data)

    def instrLD(self) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        lr8 = left_param.asReg8()
        rr8 = right_param.asReg8()
        if lr8 is not None and rr8 is not None:
            self.__current_section.data.append(0x40 | (lr8 << 3) | rr8)
        elif left_param.isA('ID', 'A') and isinstance(right_param, REF):
            if right_param.expr.isA('ID', 'BC'):
                self.__current_section.data.append(0x0A)
            elif right_param.expr.isA('ID', 'DE'):
                self.__current_section.data.append(0x1A)
            elif right_param.expr.isA('ID', 'HL+'):
                self.__current_section.data.append(0x2A)
            elif right_param.expr.isA('ID', 'HL-'):
                self.__current_section.data.append(0x3A)
            elif right_param.expr.isA('ID', 'C'):
                self.__current_section.data.append(0xF2)
            else:
                self.__current_section.data.append(0xFA)
                self.insert16(right_param.expr)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF):
            if left_param.expr.isA('ID', 'BC'):
                self.__current_section.data.append(0x02)
            elif left_param.expr.isA('ID', 'DE'):
                self.__current_section.data.append(0x12)
            elif left_param.expr.isA('ID', 'HL+'):
                self.__current_section.data.append(0x22)
            elif left_param.expr.isA('ID', 'HL-'):
                self.__current_section.data.append(0x32)
            elif left_param.expr.isA('ID', 'C'):
                self.__current_section.data.append(0xE2)
            else:
                self.__current_section.data.append(0xEA)
                self.insert16(left_param.expr)
        elif left_param.isA('ID', 'BC'):
            self.__current_section.data.append(0x01)
            self.insert16(right_param)
        elif left_param.isA('ID', 'DE'):
            self.__current_section.data.append(0x11)
            self.insert16(right_param)
        elif left_param.isA('ID', 'HL'):
            self.__current_section.data.append(0x21)
            self.insert16(right_param)
        elif left_param.isA('ID', 'SP'):
            if right_param.isA('ID', 'HL'):
                self.__current_section.data.append(0xF9)
            else:
                self.__current_section.data.append(0x31)
                self.insert16(right_param)
        elif right_param.isA('ID', 'SP') and isinstance(left_param, REF):
            self.__current_section.data.append(0x08)
            self.insert16(left_param.expr)
        elif lr8 is not None:
            self.__current_section.data.append(0x06 | (lr8 << 3))
            self.insert8(right_param)
        else:
            raise AssemblerException(left_param, "Syntax error")

    def instrLDH(self) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('ID', 'A') and isinstance(right_param, REF):
            if right_param.expr.isA('ID', 'C'):
                self.__current_section.data.append(0xF2)
            else:
                self.__current_section.data.append(0xF0)
                self.insertHigh8(right_param.expr)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF):
            if left_param.expr.isA('ID', 'C'):
                self.__current_section.data.append(0xE2)
            else:
                self.__current_section.data.append(0xE0)
                self.insertHigh8(left_param.expr)
        else:
            raise AssemblerException(left_param, "Syntax error")

    def instrLDI(self) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('ID', 'A') and isinstance(right_param, REF) and right_param.expr.isA('ID', 'HL'):
            self.__current_section.data.append(0x2A)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF) and left_param.expr.isA('ID', 'HL'):
            self.__current_section.data.append(0x22)
        else:
            raise AssemblerException(left_param, "Syntax error")

    def instrLDD(self) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('ID', 'A') and isinstance(right_param, REF) and right_param.expr.isA('ID', 'HL'):
            self.__current_section.data.append(0x3A)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF) and left_param.expr.isA('ID', 'HL'):
            self.__current_section.data.append(0x32)
        else:
            raise AssemblerException(left_param, "Syntax error")

    def instrINC(self) -> None:
        param = self.parseParam()
        r8 = param.asReg8()
        if r8 is not None:
            self.__current_section.data.append(0x04 | (r8 << 3))
        elif param.isA('ID', 'BC'):
            self.__current_section.data.append(0x03)
        elif param.isA('ID', 'DE'):
            self.__current_section.data.append(0x13)
        elif param.isA('ID', 'HL'):
            self.__current_section.data.append(0x23)
        elif param.isA('ID', 'SP'):
            self.__current_section.data.append(0x33)
        else:
            raise AssemblerException(param, "Syntax error")

    def instrDEC(self) -> None:
        param = self.parseParam()
        r8 = param.asReg8()
        if r8 is not None:
            self.__current_section.data.append(0x05 | (r8 << 3))
        elif param.isA('ID', 'BC'):
            self.__current_section.data.append(0x0B)
        elif param.isA('ID', 'DE'):
            self.__current_section.data.append(0x1B)
        elif param.isA('ID', 'HL'):
            self.__current_section.data.append(0x2B)
        elif param.isA('ID', 'SP'):
            self.__current_section.data.append(0x3B)
        else:
            raise AssemblerException(param, "Syntax error")

    def instrADD(self) -> None:
        left_param = self.parseParam()
        if self.__tok.popIf('OP', ','):
            right_param = self.parseParam()
            if left_param.isA('ID', 'A'):
                rr8 = right_param.asReg8()
                if rr8 is not None:
                    self.__current_section.data.append(0x80 | rr8)
                else:
                    self.__current_section.data.append(0xC6)
                    self.insert8(right_param)
            elif left_param.isA('ID', 'HL') and right_param.isA('ID') and isinstance(right_param, Token) and right_param.value in REGS16A:
                self.__current_section.data.append(0x09 | REGS16A[str(right_param.value)] << 4)
            elif left_param.isA('ID', 'SP'):
                self.__current_section.data.append(0xE8)
                self.insert8(right_param)
            else:
                raise AssemblerException(left_param, "Syntax error")
        else:
            lr8 = left_param.asReg8()
            if lr8 is not None:
                self.__current_section.data.append(0x80 | lr8)
            else:
                self.__current_section.data.append(0xC6)
                self.insert8(left_param)

    def instrALU(self, code_value: int) -> None:
        param = self.parseParam()
        if param.isA('ID', 'A') and self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            param = self.parseParam()
        r8 = param.asReg8()
        if r8 is not None:
            self.__current_section.data.append(code_value | r8)
        else:
            self.__current_section.data.append(code_value | 0x46)
            self.insert8(param)

    def instrRST(self) -> None:
        param = self.parseParam()
        if param.isA('NUMBER') and isinstance(param, Token) and (int(param.value) & ~0x38) == 0:
            self.__current_section.data.append(0xC7 | int(param.value))
        else:
            raise AssemblerException(param, "Syntax error")

    def instrPUSHPOP(self, code_value: int) -> None:
        param = self.parseParam()
        if param.isA('ID') and isinstance(param, Token) and str(param.value) in REGS16B:
            self.__current_section.data.append(code_value | (REGS16B[str(param.value)] << 4))
        else:
            raise AssemblerException(param, "Syntax error")

    def instrJR(self) -> None:
        param = self.parseParam()
        if self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            condition = param
            param = self.parseParam()
            if condition.isA('ID') and isinstance(condition, Token) and str(condition.value) in FLAGS:
                self.__current_section.data.append(0x20 | FLAGS[str(condition.value)])
            else:
                raise AssemblerException(condition, "Syntax error")
        else:
            self.__current_section.data.append(0x18)
        self.insertRel8(param)

    def instrCB(self, code_value: int) -> None:
        param = self.parseParam()
        r8 = param.asReg8()
        if r8 is not None:
            self.__current_section.data.append(0xCB)
            self.__current_section.data.append(code_value | r8)
        else:
            raise AssemblerException(param, "Syntax error")

    def instrBIT(self, code_value: int) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        rr8 = right_param.asReg8()
        if left_param.isA('NUMBER') and 0 <= left_param.value < 8 and isinstance(left_param, Token) and rr8 is not None:
            self.__current_section.data.append(0xCB)
            self.__current_section.data.append(code_value | (int(left_param.value) << 3) | rr8)
        else:
            raise AssemblerException(left_param, "Syntax error")

    def instrRET(self) -> None:
        if self.__tok.peek().isA('ID'):
            condition = self.__tok.pop()
            if condition.isA('ID') and condition.value in FLAGS:
                self.__current_section.data.append(0xC0 | FLAGS[str(condition.value)])
            else:
                raise AssemblerException(condition, "Syntax error")
        else:
            self.__current_section.data.append(0xC9)

    def instrCALL(self) -> None:
        param = self.parseParam()
        if self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            condition = param
            param = self.parseParam()
            if condition.isA('ID') and isinstance(condition, Token) and condition.value in FLAGS:
                self.__current_section.data.append(0xC4 | FLAGS[str(condition.value)])
            else:
                raise AssemblerException(condition, "Syntax error")
        else:
            self.__current_section.data.append(0xCD)
        self.insert16(param)

    def instrJP(self) -> None:
        param = self.parseParam()
        if self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            condition = param
            param = self.parseParam()
            if condition.isA('ID') and isinstance(condition, Token) and condition.value in FLAGS:
                self.__current_section.data.append(0xC2 | FLAGS[str(condition.value)])
            else:
                raise AssemblerException(condition, "Syntax error")
        elif param.isA('ID', 'HL'):
            self.__current_section.data.append(0xE9)
            return
        else:
            self.__current_section.data.append(0xC3)
        self.insert16(param)

    def instrDW(self) -> None:
        param = self.parseExpression()
        self.insert16(param)
        while self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            param = self.parseExpression()
            self.insert16(param)

    def instrDS(self) -> None:
        param = self.parseExpression()
        if not param.isA('NUMBER'):
            raise AssemblerException(param, "Syntax error")
        amount = param.value
        data = b'\x00'
        if self.__tok.popIf('OP', ','):
            param = self.parseExpression()
            if not param.isA('NUMBER'):
                raise AssemblerException(param, "Syntax error")
            data = bytes([param.value])
        self.insertData(data * amount)

    def instrDB(self) -> None:
        param = self.parseExpression()
        if param.isA('STRING'):
            assert isinstance(param, Token)
            self.insertString(param)
        else:
            self.insert8(param)
        while self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            param = self.parseExpression()
            if param.isA('STRING'):
                assert isinstance(param, Token)
                self.insertString(param)
            else:
                self.insert8(param)

    def addLabel(self, label: str) -> None:
        if label.startswith("."):
            assert self.__scope is not None
            label = self.__scope + label
        else:
            assert "." not in label, label
            self.__scope = label
        assert label not in self.__label, "Duplicate label: %s" % (label)
        assert label not in self.__constant, "Duplicate label: %s" % (label)
        self.__label[label] = self.__current_section, len(self.__current_section.data)

    def addConstant(self, name: str, value: int) -> None:
        assert name not in self.__constant, "Duplicate constant: %s" % (name)
        assert name not in self.__label, "Duplicate constant: %s" % (name)
        self.__constant[name] = value

    def setConstant(self, name: str, value: int) -> None:
        assert name not in self.__label, "Duplicate constant: %s" % (name)
        self.__constant[name] = value

    def parseParam(self) -> ExprBase:
        t = self.__tok.peek()
        if t.kind == 'REFOPEN':
            self.__tok.pop()
            expr = self.parseExpression()
            self.__tok.expect('REFCLOSE')
            return REF(expr)
        return self.parseExpression()

    def parseExpression(self) -> ExprBase:
        t = self.parseBitOr()
        return t

    def parseBitOr(self) -> ExprBase:
        t = self.parseBitAnd()
        p = self.__tok.peek()
        while p.isA('OP', '|'):
            self.__tok.pop()
            t = OP.make(str(p.value), t, self.parseBitAnd())
            p = self.__tok.peek()
        return t

    def parseBitAnd(self) -> ExprBase:
        t = self.parseCompare()
        p = self.__tok.peek()
        while p.isA('OP', '&'):
            self.__tok.pop()
            t = OP.make(str(p.value), t, self.parseCompare())
            p = self.__tok.peek()
        return t

    def parseCompare(self) -> ExprBase:
        t = self.parseShift()
        p = self.__tok.peek()
        while p.isA('OP', '<') or p.isA('OP', '>') or p.isA('OP', '<=') or p.isA('OP', '>=') or p.isA('OP', '=='):
            self.__tok.pop()
            t = OP.make(str(p.value), t, self.parseShift())
            p = self.__tok.peek()
        return t

    def parseShift(self) -> ExprBase:
        t = self.parseAddSub()
        p = self.__tok.peek()
        while p.isA('OP', '<<') or p.isA('OP', '>>'):
            self.__tok.pop()
            t = OP.make(str(p.value), t, self.parseAddSub())
            p = self.__tok.peek()
        return t

    def parseAddSub(self) -> ExprBase:
        t = self.parseFactor()
        p = self.__tok.peek()
        while p.isA('OP', '+') or p.isA('OP', '-'):
            self.__tok.pop()
            if self.__tok.peek().isA('REFCLOSE') and t.isA('ID', 'HL'): # Special exception for HL+/HL-
                assert isinstance(t, Token)
                return Token('ID', f'HL{p.value}', t.line_nr)
            t = OP.make(str(p.value), t, self.parseFactor())
            p = self.__tok.peek()
        return t

    def parseFactor(self) -> ExprBase:
        t = self.parseUnary()
        p = self.__tok.peek()
        while p.isA('OP', '*') or p.isA('OP', '/'):
            self.__tok.pop()
            t = OP.make(str(p.value), t, self.parseUnary())
            p = self.__tok.peek()
        return t

    def parseUnary(self) -> ExprBase:
        t = self.__tok.pop()
        if t.isA('OP', '-') or t.isA('OP', '+'):
            return OP.make(str(t.value), self.parseUnary())
        elif t.isA('OP', '('):
            result = self.parseExpression()
            self.__tok.expect('OP', ')')
            return result
        if t.kind not in ('ID', 'NUMBER', 'STRING'):
            raise AssemblerException(t, "Unexpected")
        if t.isA('ID') and t.value in CONST_MAP:
            t.kind = 'NUMBER'
            t.value = CONST_MAP[str(t.value)]
        elif t.isA('ID') and t.value in self.__constant:
            t = t.copy()
            t.kind = 'NUMBER'
            t.value = self.__constant[str(t.value)]
        elif t.isA('ID') and str(t.value).startswith("."):
            assert self.__scope is not None
            t.value = self.__scope + str(t.value)
        elif t.isA('ID') and self.__tok.peek().isA('OP', '('):
            self.__tok.pop()
            params = [self.parseExpression()]
            while self.__tok.popIf('OP', ','):
                params.append(self.parseExpression())
            self.__tok.expect('OP', ')')
            return CALL(t.value, params, line_nr=t.line_nr)
        return t

    def link(self) -> None:
        for token, expr in self.__asserts:
            result = self.resolveExpr(expr)
            if not result.isA('NUMBER'):
                raise AssemblerException(token, f"Failed to parse assert {expr}, symbol not found?")
            assert isinstance(result, Token)
            value = int(result.value)
            if value == 0:
                raise AssemblerException(token, f"Assertion failed")
        for section in self.__sections:
            inline_strings: Dict[bytes, int] = {}
            for offset, (link_type, link_expr) in section.link.items():
                expr = self.resolveExpr(link_expr)
                assert expr is not None
                if expr.isA('STRING') and (expr.value.startswith("i") or expr.value.startswith("M")):
                    if expr.value.startswith("i"):
                        strdata = expr.value[2:-1].encode("ascii") + b'\x00'
                    else:
                        strdata = utils.formatText(expr.value[2:-1].replace("|", "\n"))
                    if strdata not in inline_strings:
                        inline_strings[strdata] = len(section.data) + section.base_address
                        section.data += strdata
                    expr = Token('NUMBER', inline_strings[strdata], expr.line_nr)
                if isinstance(expr, CALL) and expr.function == 'INLINE':
                    data = bytearray()
                    for p in expr.params:
                        p = self.resolveExpr(p)
                        if not p.isA('NUMBER'):
                            raise AssemblerException(p, f"Failed to link {p}, symbol not found?")
                        if p.value < 0 or p.value > 255:
                            raise AssemblerException(p, f"Value out of range for INLINE")
                        data.append(p.value)
                    data = bytes(data)
                    if data not in inline_strings:
                        inline_strings[data] = len(section.data) + section.base_address
                        section.data += data
                    expr = Token('NUMBER', inline_strings[data], expr.line_nr)
                if not expr.isA('NUMBER'):
                    raise AssemblerException(expr, f"Failed to link {link_expr}, symbol not found?")
                assert isinstance(expr, Token)
                value = int(expr.value)
                if link_type == Assembler.LINK_REL8:
                    byte = (value - section.base_address) - offset - 1
                    if byte < -128 or byte > 127:
                        raise AssemblerException(expr, f"Failed to link {link_expr}, result out of range for jr")
                    section.data[offset] = byte & 0xFF
                elif link_type == Assembler.LINK_ABS8:
                    assert 0 <= value <= 0xFF
                    section.data[offset] = value & 0xFF
                elif link_type == Assembler.LINK_HIGH8:
                    assert 0xFF00 <= value <= 0xFFFF
                    section.data[offset] = value & 0xFF
                elif link_type == Assembler.LINK_ABS16:
                    assert section.base_address > -1, "Cannot place absolute values in a relocatable code piece"
                    assert 0 <= value <= 0xFFFF
                    section.data[offset] = value & 0xFF
                    section.data[offset + 1] = value >> 8
                else:
                    raise RuntimeError

    def resolveExpr(self, expr: Optional[ExprBase]) -> Optional[ExprBase]:
        if expr is None:
            return None
        elif isinstance(expr, OP):
            left = self.resolveExpr(expr.left)
            assert left is not None
            return OP.make(expr.op, left, self.resolveExpr(expr.right))
        elif isinstance(expr, CALL):
            if expr.function == 'BANK':
                if len(expr.params) != 1:
                    raise AssemblerException(expr, f"Wrong number of parameters to BANK() function")
                if expr.params[0].value not in self.__label:
                    raise AssemblerException(expr, f"Cannot find label: {expr.params[0].value}")
                section, offset = self.__label[expr.params[0].value]
                if section.bank is None:
                    raise AssemblerException(expr, f"Tried to get bank of label: {expr.params[0].value}, but label not in a bank.")
                return Token('NUMBER', section.bank, expr.params[0].line_nr)
            elif expr.function == 'LOW':
                if len(expr.params) != 1:
                    raise AssemblerException(expr, f"Wrong number of parameters to LOW() function")
                param = self.resolveExpr(expr.params[0])
                if param.isA('NUMBER'):
                    return Token('NUMBER', param.value & 0xFF, expr.line_nr)
            elif expr.function == 'HIGH':
                if len(expr.params) != 1:
                    raise AssemblerException(expr, f"Wrong number of parameters to HIGH() function")
                param = self.resolveExpr(expr.params[0])
                if param.isA('NUMBER'):
                    return Token('NUMBER', (param.value >> 8) & 0xFF, expr.line_nr)
        elif isinstance(expr, Token) and expr.isA('ID') and isinstance(expr, Token) and expr.value in self.__label:
            section, offset = self.__label[str(expr.value)]
            return Token('NUMBER', offset + section.base_address, expr.line_nr)
        return expr

    def getSections(self) -> Iterator[Section]:
        return iter(self.__sections)

    def getLabels(self) -> Generator[Tuple[str, int, int], None, None]:
        for label, (section, address) in self.__label.items():
            yield label, address + section.base_address, section.bank

    def getLabel(self, name: str) -> Tuple[int, int]:
        section, offset = self.__label[name.upper()]
        return section.base_address + offset, section.bank


def const(name: str, value: int) -> None:
    name = name.upper()
    assert name not in CONST_MAP
    CONST_MAP[name] = value


def resetConsts() -> None:
    CONST_MAP.clear()
    data = pkgutil.get_data(__name__, "assembler.const")
    if data is None:
        raise FileNotFoundError(f"{__name__}/assembler.const")
    for line in data.decode("utf-8").splitlines():
        if ":" in line:
            value, _, key = line.strip().partition(":")
            CONST_MAP[key.upper()] = int(value, 16)


def ASM(code: str, base_address: Optional[int] = None, labels_result: Optional[Dict[str, int]] = None) -> bytes:
    asm = Assembler()
    asm.process(code, base_address=base_address)
    asm.link()
    if labels_result is not None:
        assert base_address is not None
        for label, offset, bank in asm.getLabels():
            labels_result[label] = offset
    for section in asm.getSections():
        return binascii.hexlify(section.data)
    return b''


def allOpcodesTest() -> None:
    import json
    data = pkgutil.get_data(__name__, "Opcodes.json")
    if data is None:
        raise FileNotFoundError(f"{__name__}/Opcodes.json")
    opcodes = json.loads(data.decode("utf-8"))
    for label in (False, True):
        for prefix, codes in opcodes.items():
            for num, op in codes.items():
                if op['mnemonic'].startswith('ILLEGAL_') or op['mnemonic'] == 'PREFIX':
                    continue
                params = []
                postfix = ''
                for o in op['operands']:
                    name = o['name']
                    if name == 'd16' or name == 'a16':
                        if label:
                            name = 'LABEL'
                        else:
                            name = '$0000'
                    if name == 'd8' or name == 'a8':
                        name = '$00'
                    if name == 'r8':
                        if label and num != '0xE8':
                            name = 'LABEL'
                        else:
                            name = '$00'
                    if name[-1] == 'H' and name[0].isnumeric():
                        name = '$' + name[:-1]
                    if o['immediate']:
                        params.append(name)
                    else:
                        params.append("[%s]" % (name))
                    if 'increment' in o and o['increment']:
                        postfix = 'I'
                    if 'decrement' in o and o['decrement']:
                        postfix = 'D'
                code = op["mnemonic"] + postfix + " " + ", ".join(params)
                code = code.strip()
                try:
                    data = ASM("LABEL:\n%s" % (code), 0x0000)
                    if prefix == 'cbprefixed':
                        assert data[0:2] == b'cb'
                        data = data[2:]
                    assert data[0:2] == num[2:].encode('ascii').lower(), data[0:2] + b"!=" + num[2:].encode('ascii').lower()
                except Exception as e:
                    print("%s\t\t|%r|\t%s" % (code, e, num))
                    print(op)


resetConsts()


if __name__ == "__main__":
    #allOpcodesTest()
    const("CONST1", 1)
    const("CONST2", 2)
    ASM("""
    ld a, (123)
    ld hl, $1234 + 456
    ld hl, $1234 + CONST1
    ld hl, label
    ld hl, label.end - label
    ld c, label.end - label
label:
    nop
.end:
    """, 0x100)
    ASM("""
    jr label
label:
    """)
    assert ASM("db 1 + 2 * 3") == b'07'
    assert ASM("""
    dw M"Inline string"
    dw M"Inline string"
""", 0x1000)[:8] == b'04100410'

    asm = Assembler()
    asm.process(" db 1, 2, 3\nlabel:\ndw label", base_address=0x4000, bank=1)
    asm.process(" db 2, BANK(label), 3\ndw label", base_address=0x4000, bank=2)
    asm.link()
    for s in asm.getSections():
        print(s)
    ASM("ld a, [hl+]")

    assert ASM("db 1 <= 1+1") == b'01'
    assert ASM("db 1+1 >= 1") == b'01'
    assert ASM("db 1+1 == 1") == b'00'
    assert ASM("add a, a") == ASM("add a")
    assert ASM("add a, $10") == ASM("add $10")

    assert ASM("db 1 << 1") == b'02'
    assert ASM("db 1 << 1 + 1") == b'04'
    assert ASM("db 1 & 2") == b'00'
    assert ASM("db 1 | 2") == b'03'
    assert ASM(r"""
#MACRO test
    dw test ## \1
#END
testhello := $100
testtest := $200
    test hello
    test test""") == b'00010002'
