from enum import Enum
class TextType(Enum):
    TEXT1 = 1
    TEXT2 = 2
    TEXT3 = 3
TEXT1 = TextType.TEXT1
TEXT2 = TextType.TEXT2
TEXT3 = TextType.TEXT3

def convert(string, to_type):
    if to_type == TEXT1:
        from ...data.text.text1 import text_value
    elif to_type == TEXT2:
        from ...data.text.text2 import text_value
    elif to_type == TEXT3:
        from ...data.text.text3 import text_value
    else:
        raise NameError("text_type {} not found".format(text_type))

    result = ""
    string_index = 0
    slen = len(string)
    while string_index < slen:
        cur_value = 0xffffff
        if string[string_index] == '<':
            # text starting with '<' is variable length but ends with '>'
            substring_end = string.find('>', string_index) + 1
            substring = string[string_index:substring_end]
            if substring in text_value:
                result += substring
            string_index = substring_end - 1
        else:
            # value represents either 2 or 1 characters
            substring = string[string_index:string_index + 2]
            if substring in text_value:
                result += substring
                string_index += 1
            elif string[string_index] in text_value:
                result += string[string_index]
        string_index += 1
    return result

def get_string(values, text_type):
    if text_type == TEXT1:
        from ...data.text.text1 import value_text
    elif text_type == TEXT2:
        from ...data.text.text2 import value_text
    elif text_type == TEXT3:
        from ...data.text.text3 import value_text
    else:
        raise NameError("text_type {} not found".format(text_type))

    result = ''
    value_index = 0
    vlen = len(values)
    while value_index < vlen:
        cur_text = '\0'
        if values[value_index] in value_text:
            cur_text = value_text[values[value_index]]
        elif value_index < len(values) - 1:
            two_byte_value = values[value_index] << 8 | values[value_index + 1]
            if two_byte_value in value_text:
                cur_text = value_text[two_byte_value]
                value_index += 1

        result += cur_text
        value_index += 1

    return result

def get_bytes(string, text_type):
    if text_type == TEXT1:
        from ...data.text.text1 import text_value
    elif text_type == TEXT2:
        from ...data.text.text2 import text_value
    elif text_type == TEXT3:
        from ...data.text.text3 import text_value
    else:
        raise NameError("text_type {} not found".format(text_type))

    result = [None] * len(string)
    result_index = 0
    string_index = 0
    slen = len(string)
    while string_index < slen:
        cur_value = 0xff
        if string[string_index] == '<':
            # text starting with '<' is variable length but ends with '>'
            substring_end = string.find('>', string_index) + 1
            substring = string[string_index:substring_end]
            if substring in text_value:
                cur_value = text_value[substring]
            string_index = substring_end - 1
        else:
            # value represents either 2 or 1 characters
            substring = string[string_index:string_index + 2]
            if substring in text_value:
                cur_value = text_value[substring]
                string_index += 1
            elif string[string_index] in text_value:
                cur_value = text_value[string[string_index]]

        if cur_value > 0xff:
            # two bytes
            result[result_index] = cur_value >> 8
            result_index += 1
            result[result_index] = cur_value & 0xff
            result_index += 1
        else:
            result[result_index] = cur_value
            result_index += 1
        string_index += 1

    return result[:result_index]
