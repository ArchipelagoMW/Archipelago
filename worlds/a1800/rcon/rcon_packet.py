from .util import to_int32, from_int, check_int32


class RCONPacket:

    # The number 2 is there in two cases.
    # this is intended by the protocol.
    # AUTH_RESPONSE is only send server -> client
    # and EXECCOMMAND is only send client -> server
    # Therefore there should be no case in which
    # a packet could be missunderstood due to the identical packet type
    SERVERDATA_AUTH = int(3)
    SERVERDATA_AUTH_RESPONSE = int(2)
    SERVERDATA_EXECCOMMAND = int(2)
    SERVERDATA_RESPONSE_VALUE = int(0)

    PACKET_TYPES = [SERVERDATA_AUTH, SERVERDATA_AUTH_RESPONSE,
                    SERVERDATA_EXECCOMMAND, SERVERDATA_RESPONSE_VALUE]

    def __init__(self, id: int = 0, type: int = 0, body: str = "") -> None:
        """Creates a RCON packet."""
        self.id = id
        self.type = type
        self.body = body
        self.terminator = b"\x00"

    @classmethod
    def from_buffer(cls, buffer: bytes) -> "RCONPacket":
        """Tries to build a RCONPacket from the given buffer.
        This method only builds one packet.
        :return: a tuple with an RCONPacket and the remaining buffer if a
        whole packet was received. A tuple with None and the remaining buffer
        otherwise.
        :param buffer: The buffer as a bytestring.
        """
        if len(buffer) > 12:
            size = from_int(buffer[0:4])  # TODO check for malformed packages
            # size can not be < 10
            # maybe raise Exception
            assert size >= 10, "Packet size can not be smaller than 10"
            id = from_int(buffer[4:8])
            type = from_int(buffer[8:12])

            # check if the buffer is long enough to fit the body
            # first 4 bytes are for the size
            if len(buffer) >= 4 + size:
                # +4 for the size, -2 for the 2 \x00 at the end
                body = buffer[12:size+4-2].decode("ascii")
                packet = cls(id, type, body)
                return packet

        raise ValueError("buffer is too small: {}".format(len(buffer)))

    @property
    def type(self) -> int:
        """returns the packet type"""
        return self._type

    @type.setter
    def type(self, value: int) -> None:
        """Sets the packet type. raises a ValueError if the packet type is invalid"""
        if value not in RCONPacket.PACKET_TYPES:
            raise ValueError("{} is not a valid value.".format(value))
        if check_int32(value):
            self._type = value
        else:
            raise ValueError("{} is to large for a 32 bit signed int".format(value))

    @property
    def id(self) -> int:
        """:return: the id field of the packet."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """:param value: the new value for id. Has to fit into a 32 bit
        signed integer. Raises a ValueError if it does not fit."""
        if check_int32(value):
            self._id = value
        else:
            raise ValueError("{} is to large for a 32 bit signed int".format(value))

    @property
    def body(self) -> str:
        """Returns the body of the packet."""
        return self._body

    @body.setter
    def body(self, value: str) -> None:
        """Sets the body to the given value.
        The body is a regular python string. It is not encoded as bytearray!
        It also does not contain the null termination."""
        if not isinstance(value, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise ValueError("body needs to be a string.")
        else:
            self._body = value

    @property
    def size(self) -> int:
        """Return the size of the packet."""
        # 4 ID
        # 4 Type
        # X body
        # 1 terminator for body
        # 1 terminator of the packet
        return 4 + 4 + len(self._body) + 2*len(self.terminator)

    def msg(self) -> bytes:
        """
        Returns a bytearray which may consist of multiple RCONPackets
        directly after each other if the body is to large for one packet.
        """
        size = to_int32(self.size)
        id = to_int32(self.id)
        type = to_int32(self._type)

        return size + id + type + self._body.encode("ascii") + self.terminator + self.terminator

    def __repr__(self) -> str:
        return "<RCONPacket type={}, id={}, body={}>".format(self.type, self.id, self.body)
