from .mf.auto_generated_types import MarsschemamfTitletextItem
from .mf.constants.reserved_space import ReservedConstantsMF
from .rom import Rom

TITLE_TEXT_POINTER_ADDR = ReservedConstantsMF.TITLESCREEN_TEXT_POINTERS_POINTER_ADDR
MAX_LENGTH = 30
MAX_LINES = 14


class TitleScreenText:
    def __init__(self, text: str | None = None, line_num: int | None = None):
        self.line_num = line_num
        self.text = text

    @classmethod
    def from_json(cls, data: MarsschemamfTitletextItem) -> "TitleScreenText":
        text = data.get("Text", None)
        line_num = data.get("LineNum", None)
        return TitleScreenText(text, line_num)


def write_title_text(rom: Rom, lines: list[MarsschemamfTitletextItem]) -> None:
    if len(lines) > MAX_LINES:
        raise ValueError("Maximum number of title-screen lines exceeded.")

    for line in lines:
        write_title_text_line(rom, line)


def write_title_text_line(rom: Rom, line: MarsschemamfTitletextItem) -> None:
    if len(line["Text"]) > 30:
        raise ValueError(f'String for title-screen text exceeds 30 characters.\n"{line["Text"]}"')
    text_pointers = rom.read_ptr(ReservedConstantsMF.TITLESCREEN_TEXT_POINTERS_POINTER_ADDR)
    addr = rom.read_ptr(text_pointers + (line["LineNum"] * 4))
    rom.write_bytes(addr, line["Text"].encode("ascii"))
