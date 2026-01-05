__all__ = [
    "parse_int",
    "parse_dec",
    "parse_hex",
]

def parse_int(value: str | int | None, *, base: int = 10) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if text == "":
        return None
    if text.startswith(("0x", "0X")):
        text = text[2:]
    return int(text, base)


parse_dec = lambda v: parse_int(v, base=10)
parse_hex = lambda v: parse_int(v, base=16)
