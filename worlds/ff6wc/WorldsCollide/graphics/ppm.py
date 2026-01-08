def write_ppm6(width, height, bits_per_value, values, output_file):
    max_value = (1 << bits_per_value) - 1

    header = f"P6 {width} {height} {max_value}\n"
    with open(output_file, "wb") as output:
        output.write(header.encode("ascii"))
        output.write(bytes(values))
        
def get_ppm(width, height, bits_per_value, values):
    max_value = (1 << bits_per_value) - 1
    header = f"P6 {width} {height} {max_value}\n"
    arr = bytearray(header.encode('ascii'))
    arr.extend(bytes(values))
    return arr
