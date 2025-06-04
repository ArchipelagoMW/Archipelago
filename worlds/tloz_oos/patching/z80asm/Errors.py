
class UnknownMnemonicError(Exception):
    def __init__(self, argument, origin_line):
        super().__init__(f"Could not find a valid mnemonic for `{argument}` in `{origin_line}`")


class IncompleteMnemonicError(Exception):
    def __init__(self, origin_line):
        super().__init__(f"Could not find a complete mnemonic for `{origin_line}`. Did you forget arguments?")


class TooManyArgsError(Exception):
    def __init__(self, origin_line):
        super().__init__(f"Too many arguments in line `{origin_line}`")


class UnknownFloatingChunkError(Exception):
    def __init__(self, chunk_name):
        super().__init__(f"Unknown floating chunk {chunk_name}")


class ArgumentOverflowError(Exception):
    def __init__(self, value, expected_size):
        super().__init__(f"Argument overflow: {hex(value)} cannot fit in {expected_size} byte(s)")


class InvalidAddressError(Exception):
    def __init__(self, addr):
        super().__init__(f"Invalid address: {hex(addr)}")
