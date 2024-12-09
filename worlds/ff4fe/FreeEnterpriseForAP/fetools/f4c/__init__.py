from .compile import compile, CompileOptions
from .bytes_patch import BytesPatch

def encode_text(text):
    from . import ff4struct
    byte_list = ff4struct.text.encode(text, allow_dual_char=False)
    if byte_list and byte_list[-1] == 0x00:
        byte_list.pop()
    return byte_list
