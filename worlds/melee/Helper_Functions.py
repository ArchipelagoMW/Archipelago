from typing import NamedTuple, Optional

class LMRamData(NamedTuple):
    ram_addr: Optional[int] = None
    bit_position: Optional[int] = None
    ram_byte_size: Optional[int] = None
    pointer_offset: Optional[int] = None
    in_game_room_id: Optional[int] = None
    item_count: Optional[int] = None

class StringByteFunction:
    @staticmethod
    def string_to_bytes(user_string: str, encoded_byte_length: int) -> bytes:
        """
        Encodes a provided string to UTF-8 format. Adds padding until the expected length is reached.
        If provided string is longer than expected length, raise an exception

        :param user_string: String that needs to be encoded to bytes.
        :param encoded_byte_length: Expected length of the provided string.
        """
        encoded_string = user_string.encode('utf-8')

        if len(encoded_string) < encoded_byte_length:
            encoded_string += b'\x00' * (encoded_byte_length - len(encoded_string))
        elif len(encoded_string) > encoded_byte_length:
            raise Exception("Provided string '" + user_string + "' was longer than the expected byte length of '" +
                            str(encoded_byte_length) + "', which will not be accepted by the info file.")

        return encoded_string

    @staticmethod
    def string_to_bytes_with_limit(user_string: str, max_bytes_length: int) -> bytes:
        """
        Encodes a provided string to UTF-8 format. Adds padding until the expected length is reached.
        If provided string is longer than expected length, chop it off at the max bytes length instead.

        :param user_string: String that needs to be encoded to bytes.
        :param max_bytes_length: Max length of the bytes.
        """
        encoded_string = user_string.encode('utf-8')
        if len(encoded_string) < max_bytes_length:
            encoded_string += b'\x00' * (max_bytes_length - len(encoded_string))
        return encoded_string[:max_bytes_length]

    @staticmethod
    def byte_string_strip(bytes_input: bytes):
        """
        Strips the un-necessary padding / bytes that are not a part of the core string.

        :param bytes_input: User provided byte array, which will convert to string.
        """
        result = []

        for single_byte in bytes_input:
            if single_byte < 32 or single_byte > 127:
                break
            result.append(chr(single_byte))

        return ''.join(result)

    @staticmethod
    def byte_string_strip_null_terminator(bytes_input: bytes):
        return bytes_input.decode().strip("\0")