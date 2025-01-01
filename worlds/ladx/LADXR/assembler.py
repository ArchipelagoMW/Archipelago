import binascii
from typing import Optional, Dict, ItemsView, List, Union, Tuple
import unicodedata

from . import utils
import re


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
        return "%s %s %s" % (self.left, self.op, self.right)

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
        if left.isA('NUMBER') and right is None:
            assert isinstance(left, Token) and isinstance(left.value, int)
            if op == '+':
                return left
            if op == '-':
                left.value = -left.value
                return left
        return OP(op, left, right)


class Tokenizer:
    TOKEN_REGEX = re.compile('|'.join('(?P<%s>%s)' % pair for pair in [
        ('NUMBER', r'\d+(\.\d*)?'),
        ('HEX', r'\$[0-9A-Fa-f]+'),
        ('ASSIGN', r':='),
        ('COMMENT', r';[^\n]+'),
        ('LABEL', r':'),
        ('DIRECTIVE', r'#[A-Za-z_]+'),
        ('STRING', '[a-zA-Z]?"[^"]*"'),
        ('ID', r'\.?[A-Za-z_][A-Za-z0-9_\.]*'),
        ('OP', r'[+\-*/,\(\)]'),
        ('REFOPEN', r'\['),
        ('REFCLOSE', r'\]'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]))

    def __init__(self, code: str) -> None:
        self.__tokens: List[Token] = []
        line_num = 1
        for mo in self.TOKEN_REGEX.finditer(code):
            kind = mo.lastgroup
            assert kind is not None
            value: Union[str, int] = mo.group()
            if kind == 'MISMATCH':
                line = code.split("\n")[line_num - 1]
                raise RuntimeError(f"Syntax error on line: {line_num}: {kind}:`{line}`")
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
                self.__tokens.append(Token(kind, value, line_num))
                if kind == 'NEWLINE':
                    line_num += 1
        self.__tokens.append(Token('NEWLINE', '\n', line_num))

    def peek(self) -> Token:
        return self.__tokens[0]

    def pop(self) -> Token:
        return self.__tokens.pop(0)

    def expect(self, kind: str, value: Optional[str] = None) -> None:
        pop = self.pop()
        if not pop.isA(kind, value):
            if value is not None:
                raise SyntaxError("%s != %s:%s" % (pop, kind, value))
            raise SyntaxError("%s != %s" % (pop, kind))

    def __bool__(self) -> bool:
        return bool(self.__tokens)


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

    def __init__(self, base_address: Optional[int] = None) -> None:
        self.__base_address = base_address or -1
        self.__result = bytearray()
        self.__label: Dict[str, int] = {}
        self.__constant: Dict[str, int] = {}
        self.__link: Dict[int, Tuple[int, ExprBase]] = {}
        self.__scope: Optional[str] = None

        self.__tok = Tokenizer("")

    def process(self, code: str) -> None:
        conditional_stack = [True]
        self.__tok = Tokenizer(code)
        try:
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
                    else:
                        raise SyntaxError(start)
                elif not conditional_stack[-1]:
                    while not self.__tok.pop().isA('NEWLINE'):
                        pass
                elif start.kind == 'ID':
                    if start.value == 'DB':
                        self.instrDB()
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
                        self.__result.append(self.SIMPLE_INSTR[str(start.value)])
                        self.__tok.expect('NEWLINE')
                    elif self.__tok.peek().kind == 'LABEL':
                        self.__tok.pop()
                        self.addLabel(str(start.value))
                    elif self.__tok.peek().kind == 'ASSIGN':
                        self.__tok.pop()
                        value = self.__tok.pop()
                        if value.kind != 'NUMBER':
                            raise SyntaxError(start)
                        self.addConstant(str(start.value), int(value.value))
                    else:
                        raise SyntaxError(start)
                else:
                    raise SyntaxError(start)
        except SyntaxError:
            print("Syntax error on line: %s" % code.split("\n")[self.__tok.peek().line_nr-1])
            raise

    def insert8(self, expr: ExprBase) -> None:
        if expr.isA('NUMBER'):
            assert isinstance(expr, Token)
            value = int(expr.value)
        else:
            self.__link[len(self.__result)] = (Assembler.LINK_ABS8, expr)
            value = 0
        assert 0 <= value < 256
        self.__result.append(value)

    def insertRel8(self, expr: ExprBase) -> None:
        if expr.isA('NUMBER'):
            assert isinstance(expr, Token)
            self.__result.append(int(expr.value))
        else:
            self.__link[len(self.__result)] = (Assembler.LINK_REL8, expr)
            self.__result.append(0x00)

    def insert16(self, expr: ExprBase) -> None:
        if expr.isA('NUMBER'):
            assert isinstance(expr, Token)
            value = int(expr.value)
        else:
            self.__link[len(self.__result)] = (Assembler.LINK_ABS16, expr)
            value = 0
        assert 0 <= value <= 0xFFFF
        self.__result.append(value & 0xFF)
        self.__result.append(value >> 8)

    def insertString(self, string: str) -> None:
        if string.startswith('"') and string.endswith('"'):
            string = string[1:-1]
            string = unicodedata.normalize('NFKD', string)
            self.__result += string.encode("latin1", "ignore")
        elif string.startswith("m\"") and string.endswith("\""):
            self.__result += utils.formatText(string[2:-1].replace("|", "\n"))
        else:
            raise SyntaxError

    def instrLD(self) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        lr8 = left_param.asReg8()
        rr8 = right_param.asReg8()
        if lr8 is not None and rr8 is not None:
            self.__result.append(0x40 | (lr8 << 3) | rr8)
        elif left_param.isA('ID', 'A') and isinstance(right_param, REF):
            if right_param.expr.isA('ID', 'BC'):
                self.__result.append(0x0A)
            elif right_param.expr.isA('ID', 'DE'):
                self.__result.append(0x1A)
            elif right_param.expr.isA('ID', 'HL+'):  # TODO
                self.__result.append(0x2A)
            elif right_param.expr.isA('ID', 'HL-'):  # TODO
                self.__result.append(0x3A)
            elif right_param.expr.isA('ID', 'C'):
                self.__result.append(0xF2)
            else:
                self.__result.append(0xFA)
                self.insert16(right_param.expr)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF):
            if left_param.expr.isA('ID', 'BC'):
                self.__result.append(0x02)
            elif left_param.expr.isA('ID', 'DE'):
                self.__result.append(0x12)
            elif left_param.expr.isA('ID', 'HL+'):  # TODO
                self.__result.append(0x22)
            elif left_param.expr.isA('ID', 'HL-'):  # TODO
                self.__result.append(0x32)
            elif left_param.expr.isA('ID', 'C'):
                self.__result.append(0xE2)
            else:
                self.__result.append(0xEA)
                self.insert16(left_param.expr)
        elif left_param.isA('ID', 'BC'):
            self.__result.append(0x01)
            self.insert16(right_param)
        elif left_param.isA('ID', 'DE'):
            self.__result.append(0x11)
            self.insert16(right_param)
        elif left_param.isA('ID', 'HL'):
            self.__result.append(0x21)
            self.insert16(right_param)
        elif left_param.isA('ID', 'SP'):
            if right_param.isA('ID', 'HL'):
                self.__result.append(0xF9)
            else:
                self.__result.append(0x31)
                self.insert16(right_param)
        elif right_param.isA('ID', 'SP') and isinstance(left_param, REF):
            self.__result.append(0x08)
            self.insert16(left_param.expr)
        elif lr8 is not None:
            self.__result.append(0x06 | (lr8 << 3))
            self.insert8(right_param)
        else:
            raise SyntaxError

    def instrLDH(self) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('ID', 'A') and isinstance(right_param, REF):
            if right_param.expr.isA('ID', 'C'):
                self.__result.append(0xF2)
            else:
                self.__result.append(0xF0)
                self.insert8(right_param.expr)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF):
            if left_param.expr.isA('ID', 'C'):
                self.__result.append(0xE2)
            else:
                self.__result.append(0xE0)
                self.insert8(left_param.expr)
        else:
            raise SyntaxError

    def instrLDI(self) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('ID', 'A') and isinstance(right_param, REF) and right_param.expr.isA('ID', 'HL'):
            self.__result.append(0x2A)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF) and left_param.expr.isA('ID', 'HL'):
            self.__result.append(0x22)
        else:
            raise SyntaxError

    def instrLDD(self) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        if left_param.isA('ID', 'A') and isinstance(right_param, REF) and right_param.expr.isA('ID', 'HL'):
            self.__result.append(0x3A)
        elif right_param.isA('ID', 'A') and isinstance(left_param, REF) and left_param.expr.isA('ID', 'HL'):
            self.__result.append(0x32)
        else:
            raise SyntaxError

    def instrINC(self) -> None:
        param = self.parseParam()
        r8 = param.asReg8()
        if r8 is not None:
            self.__result.append(0x04 | (r8 << 3))
        elif param.isA('ID', 'BC'):
            self.__result.append(0x03)
        elif param.isA('ID', 'DE'):
            self.__result.append(0x13)
        elif param.isA('ID', 'HL'):
            self.__result.append(0x23)
        elif param.isA('ID', 'SP'):
            self.__result.append(0x33)
        else:
            raise SyntaxError

    def instrDEC(self) -> None:
        param = self.parseParam()
        r8 = param.asReg8()
        if r8 is not None:
            self.__result.append(0x05 | (r8 << 3))
        elif param.isA('ID', 'BC'):
            self.__result.append(0x0B)
        elif param.isA('ID', 'DE'):
            self.__result.append(0x1B)
        elif param.isA('ID', 'HL'):
            self.__result.append(0x2B)
        elif param.isA('ID', 'SP'):
            self.__result.append(0x3B)
        else:
            raise SyntaxError

    def instrADD(self) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()

        if left_param.isA('ID', 'A'):
            rr8 = right_param.asReg8()
            if rr8 is not None:
                self.__result.append(0x80 | rr8)
            else:
                self.__result.append(0xC6)
                self.insert8(right_param)
        elif left_param.isA('ID', 'HL') and right_param.isA('ID') and isinstance(right_param, Token) and right_param.value in REGS16A:
            self.__result.append(0x09 | REGS16A[str(right_param.value)] << 4)
        elif left_param.isA('ID', 'SP'):
            self.__result.append(0xE8)
            self.insert8(right_param)
        else:
            raise SyntaxError

    def instrALU(self, code_value: int) -> None:
        param = self.parseParam()
        if param.isA('ID', 'A') and self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            param = self.parseParam()
        r8 = param.asReg8()
        if r8 is not None:
            self.__result.append(code_value | r8)
        else:
            self.__result.append(code_value | 0x46)
            self.insert8(param)

    def instrRST(self) -> None:
        param = self.parseParam()
        if param.isA('NUMBER') and isinstance(param, Token) and (int(param.value) & ~0x38) == 0:
            self.__result.append(0xC7 | int(param.value))
        else:
            raise SyntaxError

    def instrPUSHPOP(self, code_value: int) -> None:
        param = self.parseParam()
        if param.isA('ID') and isinstance(param, Token) and str(param.value) in REGS16B:
            self.__result.append(code_value | (REGS16B[str(param.value)] << 4))
        else:
            raise SyntaxError

    def instrJR(self) -> None:
        param = self.parseParam()
        if self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            condition = param
            param = self.parseParam()
            if condition.isA('ID') and isinstance(condition, Token) and str(condition.value) in FLAGS:
                self.__result.append(0x20 | FLAGS[str(condition.value)])
            else:
                raise SyntaxError
        else:
            self.__result.append(0x18)
        self.insertRel8(param)

    def instrCB(self, code_value: int) -> None:
        param = self.parseParam()
        r8 = param.asReg8()
        if r8 is not None:
            self.__result.append(0xCB)
            self.__result.append(code_value | r8)
        else:
            raise SyntaxError

    def instrBIT(self, code_value: int) -> None:
        left_param = self.parseParam()
        self.__tok.expect('OP', ',')
        right_param = self.parseParam()
        rr8 = right_param.asReg8()
        if left_param.isA('NUMBER') and isinstance(left_param, Token) and rr8 is not None:
            self.__result.append(0xCB)
            self.__result.append(code_value | (int(left_param.value) << 3) | rr8)
        else:
            raise SyntaxError

    def instrRET(self) -> None:
        if self.__tok.peek().isA('ID'):
            condition = self.__tok.pop()
            if condition.isA('ID') and condition.value in FLAGS:
                self.__result.append(0xC0 | FLAGS[str(condition.value)])
            else:
                raise SyntaxError
        else:
            self.__result.append(0xC9)

    def instrCALL(self) -> None:
        param = self.parseParam()
        if self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            condition = param
            param = self.parseParam()
            if condition.isA('ID') and isinstance(condition, Token) and condition.value in FLAGS:
                self.__result.append(0xC4 | FLAGS[str(condition.value)])
            else:
                raise SyntaxError
        else:
            self.__result.append(0xCD)
        self.insert16(param)

    def instrJP(self) -> None:
        param = self.parseParam()
        if self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            condition = param
            param = self.parseParam()
            if condition.isA('ID') and isinstance(condition, Token) and condition.value in FLAGS:
                self.__result.append(0xC2 | FLAGS[str(condition.value)])
            else:
                raise SyntaxError
        elif param.isA('ID', 'HL'):
            self.__result.append(0xE9)
            return
        else:
            self.__result.append(0xC3)
        self.insert16(param)

    def instrDW(self) -> None:
        param = self.parseExpression()
        self.insert16(param)
        while self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            param = self.parseExpression()
            self.insert16(param)

    def instrDB(self) -> None:
        param = self.parseExpression()
        if param.isA('STRING'):
            assert isinstance(param, Token)
            self.insertString(str(param.value))
        else:
            self.insert8(param)
        while self.__tok.peek().isA('OP', ','):
            self.__tok.pop()
            param = self.parseExpression()
            if param.isA('STRING'):
                assert isinstance(param, Token)
                self.insertString(str(param.value))
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
        self.__label[label] = len(self.__result)

    def addConstant(self, name: str, value: int) -> None:
        assert name not in self.__constant, "Duplicate constant: %s" % (name)
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
        t = self.parseAddSub()
        return t

    def parseAddSub(self) -> ExprBase:
        t = self.parseFactor()
        p = self.__tok.peek()
        if p.isA('OP', '+') or p.isA('OP', '-'):
            self.__tok.pop()
            return OP.make(str(p.value), t, self.parseAddSub())
        return t

    def parseFactor(self) -> ExprBase:
        t = self.parseUnary()
        p = self.__tok.peek()
        if p.isA('OP', '*') or p.isA('OP', '/'):
            self.__tok.pop()
            return OP.make(str(p.value), t, self.parseFactor())
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
            raise SyntaxError
        if t.isA('ID') and t.value in CONST_MAP:
            t.kind = 'NUMBER'
            t.value = CONST_MAP[str(t.value)]
        elif t.isA('ID') and t.value in self.__constant:
            t.kind = 'NUMBER'
            t.value = self.__constant[str(t.value)]
        elif t.isA('ID') and str(t.value).startswith("."):
            assert self.__scope is not None
            t.value = self.__scope + str(t.value)
        return t

    def link(self) -> None:
        for offset, (link_type, link_expr) in self.__link.items():
            expr = self.resolveExpr(link_expr)
            assert expr is not None
            assert expr.isA('NUMBER'), expr
            assert isinstance(expr, Token)
            value = int(expr.value)
            if link_type == Assembler.LINK_REL8:
                byte = (value - self.__base_address) - offset - 1
                assert -128 <= byte <= 127, expr
                self.__result[offset] = byte & 0xFF
            elif link_type == Assembler.LINK_ABS8:
                assert 0 <= value <= 0xFF
                self.__result[offset] = value & 0xFF
            elif link_type == Assembler.LINK_ABS16:
                assert self.__base_address >= 0, "Cannot place absolute values in a relocatable code piece"
                assert 0 <= value <= 0xFFFF
                self.__result[offset] = value & 0xFF
                self.__result[offset + 1] = value >> 8
            else:
                raise RuntimeError

    def resolveExpr(self, expr: Optional[ExprBase]) -> Optional[ExprBase]:
        if expr is None:
            return None
        elif isinstance(expr, OP):
            left = self.resolveExpr(expr.left)
            assert left is not None
            return OP.make(expr.op, left, self.resolveExpr(expr.right))
        elif isinstance(expr, Token) and expr.isA('ID') and isinstance(expr, Token) and expr.value in self.__label:
            return Token('NUMBER', self.__label[str(expr.value)] + self.__base_address, expr.line_nr)
        return expr

    def getResult(self) -> bytearray:
        return self.__result

    def getLabels(self) -> ItemsView[str, int]:
        return self.__label.items()


def const(name: str, value: int) -> None:
    name = name.upper()
    assert name not in CONST_MAP or CONST_MAP[name] == value
    CONST_MAP[name] = value


def resetConsts() -> None:
    CONST_MAP.clear()


def ASM(code: str, base_address: Optional[int] = None, labels_result: Optional[Dict[str, int]] = None) -> bytes:
    asm = Assembler(base_address)
    asm.process(code)
    asm.link()
    if labels_result is not None:
        assert base_address is not None
        for label, offset in asm.getLabels():
            labels_result[label] = base_address + offset
    return binascii.hexlify(asm.getResult())


def allOpcodesTest() -> None:
    import json
    opcodes = json.load(open("Opcodes.json", "rt"))
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
    """, 0)
    ASM("""
    jr label
label:
    """)
    assert ASM("db 1 + 2 * 3") == b'07'
