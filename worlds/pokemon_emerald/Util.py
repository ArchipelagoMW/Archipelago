import os
import json

data_json = None

def get_data_json():
    global data_json
    if (data_json == None):
        json_string = ""
        with open(os.path.join(os.path.dirname(__file__), f"data/data.json"), "r") as infile:
            for line in infile.readlines():
                json_string += line
        data_json = json.loads(json_string)
    
    return data_json

def set_bytes_little_endian(byte_array, address, size, value):
    offset = 0
    while (size > 0):
        byte_array[address + offset] = value & 0xFF
        value = value >> 8
        offset += 1
        size -= 1