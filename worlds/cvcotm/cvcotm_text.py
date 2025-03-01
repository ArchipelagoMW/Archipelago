from typing import Literal

cvcotm_char_dict = {"\n": 0x09, " ": 0x26, "!": 0x4A, '"': 0x78, "#": 0x79, "$": 0x7B, "%": 0x68, "&": 0x73, "'": 0x51,
                    "(": 0x54, ")": 0x55, "*": 0x7A, "+": 0x50, ",": 0x4C, "-": 0x58, ".": 0x35, "/": 0x70, "0": 0x64,
                    "1": 0x6A, "2": 0x63, "3": 0x6C, "4": 0x71, "5": 0x69, "6": 0x7C, "7": 0x7D, "8": 0x72, "9": 0x85,
                    ":": 0x86, ";": 0x87, "<": 0x8F, "=": 0x90, ">": 0x91, "?": 0x48, "@": 0x98, "A": 0x3E, "B": 0x4D,
                    "C": 0x44, "D": 0x45, "E": 0x4E, "F": 0x56, "G": 0x4F, "H": 0x40, "I": 0x43, "J": 0x6B, "K": 0x66,
                    "L": 0x5F, "M": 0x42, "N": 0x52, "O": 0x67, "P": 0x4B, "Q": 0x99, "R": 0x46, "S": 0x41, "T": 0x47,
                    "U": 0x60, "V": 0x6E, "W": 0x49, "X": 0x6D, "Y": 0x53, "Z": 0x6F, "[": 0x59, "\\": 0x9A, "]": 0x5A,
                    "^": 0x9B, "_": 0xA1, "a": 0x29, "b": 0x3C, "c": 0x33, "d": 0x32, "e": 0x28, "f": 0x3A, "g": 0x39,
                    "h": 0x31, "i": 0x2D, "j": 0x62, "k": 0x3D, "l": 0x30, "m": 0x36, "n": 0x2E, "o": 0x2B, "p": 0x38,
                    "q": 0x61, "r": 0x2C, "s": 0x2F, "t": 0x2A, "u": 0x34, "v": 0x3F, "w": 0x37, "x": 0x57, "y": 0x3B,
                    "z": 0x65, "{": 0xA3, "|": 0xA4, "}": 0xA5, "`": 0xA2, "~": 0xAC,
                    # Special command characters
                    "▶": 0x02,  # Press A with prompt arrow.
                    "◊": 0x03,  # Press A without prompt arrow.
                    "\t": 0x01,  # Clear the text buffer; usually after pressing A to advance.
                    "\b": 0x0A,  # Reset text alignment; usually after pressing A.
                    "「": 0x06,  # Start orange text
                    "」": 0x07,  # End orange text
                    }

# Characters that do not contribute to the line length.
weightless_chars = {"\n", "▶", "◊", "\b", "\t", "「", "」"}


def cvcotm_string_to_bytearray(cvcotm_text: str, textbox_type: Literal["big top", "big middle", "little middle"],
                               speed: int, portrait: int = 0xFF, wrap: bool = True,
                               skip_textbox_controllers: bool = False) -> bytearray:
    """Converts a string into a textbox bytearray following CVCotM's string format."""
    text_bytes = bytearray(0)
    if portrait == 0xFF and textbox_type != "little middle":
        text_bytes.append(0x0C)  # Insert the character to convert a 3-line named textbox into a 4-line nameless one.

    # Figure out the start and end params for the textbox based on what type it is.
    if textbox_type == "little middle":
        main_control_start_param = 0x10
        main_control_end_param = 0x20
    elif textbox_type == "big top":
        main_control_start_param = 0x40
        main_control_end_param = 0xC0
    else:
        main_control_start_param = 0x80
        main_control_end_param = 0xC0

    # Figure out the number of lines and line length limit.
    if textbox_type == "little middle":
        total_lines = 1
        len_limit = 29
    elif textbox_type != "little middle" and portrait != 0xFF:
        total_lines = 3
        len_limit = 21
    else:
        total_lines = 4
        len_limit = 23

    # Wrap the text if we are opting to do so.
    if wrap:
        refined_text = cvcotm_text_wrap(cvcotm_text, len_limit, total_lines)
    else:
        refined_text = cvcotm_text

    # Add the textbox control characters if we are opting to add them.
    if not skip_textbox_controllers:
        text_bytes.extend([0x1D, main_control_start_param + (speed & 0xF)])  # Speed should be a value between 0 and 15.

    # Add the portrait (if we are adding one).
    if portrait != 0xFF and textbox_type != "little middle":
        text_bytes.extend([0x1E, portrait & 0xFF])

    for i, char in enumerate(refined_text):
        if char in cvcotm_char_dict:
            text_bytes.extend([cvcotm_char_dict[char]])
            # If we're pressing A to advance, add the text clear and reset alignment characters.
            if char in ["▶", "◊"] and not skip_textbox_controllers:
                text_bytes.extend([0x01, 0x0A])
        else:
            text_bytes.extend([0x48])

    # Add the characters indicating the end of the whole message.
    if not skip_textbox_controllers:
        text_bytes.extend([0x1D, main_control_end_param, 0x00])
    else:
        text_bytes.extend([0x00])
    return text_bytes


def cvcotm_text_truncate(cvcotm_text: str, textbox_len_limit: int) -> str:
    """Truncates a string at a given in-game text line length."""
    line_len = 0

    for i in range(len(cvcotm_text)):
        if cvcotm_text[i] not in weightless_chars:
            line_len += 1

        if line_len > textbox_len_limit:
            return cvcotm_text[0x00:i]

    return cvcotm_text


def cvcotm_text_wrap(cvcotm_text: str, textbox_len_limit: int, total_lines: int = 4) -> str:
    """Rebuilds a string with some of its spaces replaced with newlines to ensure the text wraps properly in an in-game
    textbox of a given length. If the number of lines allowed per textbox is exceeded, an A prompt will be placed
    instead of a newline."""
    words = cvcotm_text.split(" ")
    new_text = ""
    line_len = 0
    num_lines = 1

    for word_index, word in enumerate(words):
        # Reset the word length to 0 on every word iteration and make its default divider a space.
        word_len = 0
        word_divider = " "

        # Check if we're at the very beginning of a line and handle the situation accordingly by increasing the current
        # line length to account for the space if we are not. Otherwise, the word divider should be nothing.
        if line_len != 0:
            line_len += 1
        else:
            word_divider = ""

        new_word = ""

        for char_index, char in enumerate(word):
            # Check if the current character contributes to the line length.
            if char not in weightless_chars:
                line_len += 1
                word_len += 1

            # If we're looking at a manually-placed newline, add +1 to the lines counter and reset the length counters.
            if char == "\n":
                word_len = 0
                line_len = 0
                num_lines += 1
                # If this puts us over the line limit, insert the A advance prompt character.
                if num_lines > total_lines:
                    num_lines = 1
                    new_word += "▶"

            # If we're looking at a manually-placed A advance prompt, reset the lines and length counters.
            if char in ["▶", "◊"]:
                word_len = 0
                line_len = 0
                num_lines = 1

            # If the word alone is long enough to exceed the line length, wrap without moving the entire word.
            if word_len > textbox_len_limit:
                word_len = 1
                line_len = 1
                num_lines += 1
                word_splitter = "\n"

                # If this puts us over the line limit, replace the newline with the A advance prompt character.
                if num_lines > total_lines:
                    num_lines = 1
                    word_splitter = "▶"

                new_word += word_splitter

            # If the total length of the current line exceeds the line length, wrap the current word to the next line.
            if line_len > textbox_len_limit:
                word_divider = "\n"
                line_len = word_len
                num_lines += 1
                # If we're over the allowed number of lines to be displayed in the textbox, insert the A advance
                # character instead.
                if num_lines > total_lines:
                    num_lines = 1
                    word_divider = "▶"

            # Add the character to the new word if the character is not a newline immediately following up an A advance.
            if char != "\n" or new_word[len(new_word)-1] not in ["▶", "◊"]:
                new_word += char

        new_text += word_divider + new_word

    return new_text
