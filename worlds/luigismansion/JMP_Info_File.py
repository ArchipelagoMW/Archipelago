import re
import struct
import io
import json
from pkgutil import get_data

from gclib.rarc import RARC
from .JMP_Field_Header import JMPFieldHeader
from .Helper_Functions import StringByteFunction as sbf

IMPORTANT_HEADER_BYTE_LENGTH = 16
FIELD_DATA_BYTE_LENGTH = 12
INTEGER_BYTE_LENGTH = 4
STRING_BYTE_LENGTH = 32

class JMPInfoFile:
    __header_byte_length = 0
    __data_line_byte_length = 0
    __info_file_headers = None
    __end_file_terminator = None

    info_file_field_entries = None
    info_file_entry = None

    def __init__(self, main_rarc_file: RARC, name_of_info_file: str):
        # A valid file must already be loaded prior to calling this module.
        if main_rarc_file is None:
            raise Exception("A pre-loaded RARC object was not provided, unable to retrieve JMP info files...")

        # RARC files can have multiple sub-file entries / fragments associated with it.
        # This project cares about the JMP File Info entries, which will only work if they exist
        self.info_file_entry = next((info_files for info_files in main_rarc_file.file_entries if
                                info_files.name == name_of_info_file), None)

        if self.info_file_entry is None:
            raise Exception("Unable to find an info file with name '" + name_of_info_file + "' in provided RARC file.")

        json_data = json.loads(get_data(__name__, "data/names.json"))

        if name_of_info_file not in json_data:
            raise Exception("Unable to load info file headers for '" + name_of_info_file + "'.")

        header_name_list = json_data[name_of_info_file]

        # After loading a JMP info file, then the file bytes must be observed.
        # In the beginning, info files have a series of bytes that provide metadata about the file itself.
        # First 4 bytes (signed integer) give the total lines available in the file.
        # Second 4 bytes (signed integer) give us the number of fields per data line.
        # The next 4 bytes (unsigned integer) give us the header size of the file, in bytes
        # The next 4 bytes (unsigned integer) tell us the size of the data lines themselves in bytes.
        # After, the rest of the header bytes describe data related to the file's fields.
        # After the header bytes, then the actual data lines would be stored.
        # Based on the data line size, the bytes would need to be split into their logical fields.
        self.info_file_entry.data.seek(0)

        data_line_count, field_count, self.__header_byte_length, self.__data_line_byte_length = (
            struct.unpack(">iiII", self.info_file_entry.data.read(IMPORTANT_HEADER_BYTE_LENGTH)))

        # As mentioned before, these extra header bytes describe each field, taking up 12 bytes each.
        # (see more details in JMP_Field_Header.py)
        self.__extra_header_bytes = io.BytesIO(self.info_file_entry.data.read(
            self.__header_byte_length-IMPORTANT_HEADER_BYTE_LENGTH))

        # This will get the header field data for each field defined.
        self.__info_file_headers = []
        header_index = 0
        for header_line in range(0, len(self.__extra_header_bytes.getvalue()), FIELD_DATA_BYTE_LENGTH):
            current_line = io.BytesIO(self.__extra_header_bytes.read(FIELD_DATA_BYTE_LENGTH))
            local_field_header = JMPFieldHeader(header_name_list[header_index], current_line)
            self.__info_file_headers.append(local_field_header)
            header_index += 1

        # This will grab the data lines defined in the file.
        # Note that for Integers, the bitmask and bit shift are absolutely required, but for floats and
        #    strings, they are not required to get the data. Strings will automatically strip padding and null chars.
        self.info_file_field_entries = []

        for data_line in range(self.__header_byte_length, len(self.info_file_entry.data.getvalue()),
                               self.__data_line_byte_length):
            current_line = io.BytesIO(self.info_file_entry.data.read(self.__data_line_byte_length))

            # Some info files have random @ signs as their file terminator.
            # This project captures this information and saves it for later when the file is converted back to bytes
            if len(current_line.getvalue()) < self.__data_line_byte_length and bool(re.search("@{4,}", str(current_line.getvalue()))):
                self.__end_file_terminator = current_line
                break

            data_line_info = {}

            for jmp_header in self.__info_file_headers:
                # Set the data stream in the starting bit right position.
                current_line.seek(jmp_header.get_field_start_bit)

                match jmp_header.get_field_type:
                    case "Int":
                        current_bytes = struct.unpack(">I", current_line.read(INTEGER_BYTE_LENGTH))[0]
                        int_val = (current_bytes & jmp_header.get_field_bitmask) >> jmp_header.get_field_shift_bit
                        data_line_info[jmp_header.get_field_name] = int_val
                    case "Str":
                        str_val = sbf.byte_string_strip(current_line.read(STRING_BYTE_LENGTH))
                        data_line_info[jmp_header.get_field_name] = str_val
                    case "Flt":
                        flt_val = struct.unpack(">f", current_line.read(INTEGER_BYTE_LENGTH))[0]
                        data_line_info[jmp_header.get_field_name] = flt_val

            self.info_file_field_entries.append(data_line_info)

    def add_blank_data_lines(self, line_amount: int):
        # Go back to an existing line
        if not self.__end_file_terminator is None:
            self.info_file_entry.data.seek(len(self.info_file_entry.data.getbuffer()) -
                    len(self.__end_file_terminator.getbuffer()) - self.__data_line_byte_length)
        else:
            self.info_file_entry.data.seek(len(self.info_file_entry.data.getbuffer()) - self.__data_line_byte_length)

        # Copy the data (which may include bitmask information, offset, and shift details)
        old_line = io.BytesIO(self.info_file_entry.data.read(self.__data_line_byte_length))

        # Get the end file offset where we need to begin writing
        end_file_buffer = len(self.info_file_entry.data.getbuffer())
        if not self.__end_file_terminator is None:
            end_file_buffer -= len(self.__end_file_terminator.getbuffer())
        self.info_file_entry.data.seek(end_file_buffer)

        for x in range(line_amount):
            self.info_file_entry.data.write(old_line.getvalue())

        # Add the file terminator back if it existed
        if not self.__end_file_terminator is None:
            self.info_file_entry.data.seek(len(self.info_file_entry.data.getbuffer()))
            self.info_file_entry.data.write(self.__end_file_terminator.getvalue())

    def print_header_info(self):
        print(self.info_file_entry.name + "; Data Line(s) Count: " + str(len(self.info_file_field_entries)) +
              "; # of Fields: " + str(len(self.__info_file_headers)) + "; Header Byte Length: " +
              str(self.__header_byte_length) + "; Single Data Line Byte Length: " + str(self.__data_line_byte_length))


    # Using the original BytesIO stream, we will write back to the original data as needed.
    # This allows us to ensure the important data bits are unchanged.
    def update_info_file_bytes(self):
        self.info_file_entry.data.seek(0)
        data_line_count = int(struct.unpack(">i", self.info_file_entry.data.read(INTEGER_BYTE_LENGTH))[0])
        if data_line_count != len(self.info_file_field_entries):
            self.info_file_entry.data.seek(0)
            self.info_file_entry.data.write(struct.pack(">i", len(self.info_file_field_entries)))
            self.add_blank_data_lines(len(self.info_file_field_entries) - data_line_count)

        for index, data_line in enumerate(self.info_file_field_entries):
            data_field_offset = self.__header_byte_length+(index*self.__data_line_byte_length)

            for jmp_header in self.__info_file_headers:
                # Set the data stream in the starting bit right position.
                # Stream starts at the current line starting point + Starting Bit offset
                self.info_file_entry.data.seek(data_field_offset+jmp_header.get_field_start_bit)

                match jmp_header.get_field_type:
                    case "Int":
                        old_val = struct.unpack(">I", self.info_file_entry.data.read(INTEGER_BYTE_LENGTH))[0]
                        new_val = ((old_val & ~jmp_header.get_field_bitmask) |
                                   ((data_line[jmp_header.get_field_name] << jmp_header.get_field_shift_bit) &
                                    jmp_header.get_field_bitmask))
                        self.info_file_entry.data.seek(data_field_offset + jmp_header.get_field_start_bit)
                        self.info_file_entry.data.write(struct.pack(">I", new_val))
                    case "Str":
                        current_val = data_line[jmp_header.get_field_name]
                        str_val = sbf.byte_string_strip(self.info_file_entry.data.read(STRING_BYTE_LENGTH))

                        if len(str_val) > len(current_val):
                            length_to_use = len(str_val)
                        else:
                            length_to_use = len(current_val)

                        if length_to_use < STRING_BYTE_LENGTH:
                            current_val = sbf.string_to_bytes(current_val, length_to_use+1)


                        self.info_file_entry.data.seek(data_field_offset + jmp_header.get_field_start_bit)
                        self.info_file_entry.data.write(current_val)
                    case "Flt":
                        flt_val = struct.pack(">f", data_line[jmp_header.get_field_name])
                        self.info_file_entry.data.write(flt_val)