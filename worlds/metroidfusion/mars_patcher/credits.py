from .constants.credits import (
    LINE_TYPE_HEIGHTS,
    LINE_TYPE_VALS,
    TEXT_LINE_TYPES,
    LineType,
)
from .mf.auto_generated_types import MarsschemamfCreditstextItem
from .rom import Rom

FULL_LINE_LEN = 36
LINE_WIDTH = 30


class CreditsLine:
    LINE_TYPE_ENUMS = {
        "Blank": LineType.BLANK,
        "Blue": LineType.BLUE,
        "Red": LineType.RED,
        "White1": LineType.WHITE1,
        "White2": LineType.WHITE2,
    }

    def __init__(
        self,
        line_type: LineType,
        blank_lines: int = 0,
        text: str | None = None,
        centered: bool = True,
    ):
        self.line_type = line_type
        self.blank_lines = blank_lines
        self.text = text
        self.centered = centered

    @classmethod
    def from_json(cls, data: MarsschemamfCreditstextItem) -> "CreditsLine":
        line_type = cls.LINE_TYPE_ENUMS[data["LineType"]]
        blank_lines = data.get("BlankLines", 0)
        text = data.get("Text")
        centered = data.get("Centered", True)
        return CreditsLine(line_type, blank_lines, text, centered)


class CreditsWriter:
    def __init__(self, rom: Rom, addr: int):
        self.rom = rom
        self.addr = addr
        self.num_lines = 0

    def write_lines(self, lines: list[CreditsLine]) -> None:
        for line in lines:
            lt_val = LINE_TYPE_VALS[line.line_type]
            line_bytes = bytearray([lt_val, line.blank_lines])
            if line.line_type in TEXT_LINE_TYPES and line.text:
                text = line.text
                if line.centered:
                    spacing = " " * ((LINE_WIDTH - len(text)) // 2)
                    text = spacing + text
                line_bytes.extend(text.encode("ascii"))
            self.write_line(line_bytes)
            line_height = LINE_TYPE_HEIGHTS.get(line.line_type, 0)
            self.num_lines += line_height + line.blank_lines

    def write_line(self, line: bytearray) -> None:
        if len(line) > FULL_LINE_LEN:
            raise ValueError(f"Line too long: {line}")
        self.rom.write_bytes(self.addr, line)
        for i in range(len(line), FULL_LINE_LEN):
            self.rom.write_8(self.addr + i, 0)
        self.addr += FULL_LINE_LEN
