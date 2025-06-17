from io import BufferedReader


def parse_string(input_stream: BufferedReader, encoding: str = "shift-jis"):
    output = input_stream.read(1)
    while not output.endswith(b"\0"):
        output += input_stream.read(1)
    return output.replace(b"\0", b"").decode(encoding)
