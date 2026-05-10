from typing import Iterator, List, Optional, Union

from .rcon_mmap_file_access import PACKET_SIZE
from .rcon_packet import RCONPacket


class RCONMessage:
    """
    A RCONMessage represents a message which may consist of multiple packets.
    """

    def __init__(
            self,
            packet: Optional[Union[RCONPacket, List[RCONPacket]]] = None,
            id: Optional[int] = None,
            type: Optional[int] = None,
            body: Optional[str] = None) -> None:
        """
        creates a new RCONMessage object.

        A RCONMessage is a higher abstraction from RCONPackets.
        It has an id, type and a body as a RCONPacket has.
        But the body can be longer than the maximum size of a single
        RCONPacket.

        This can either be created from a packets or by giving an
        *id*, *type* and *body*.

        If build from packes then all packets need to have the same type
        and id.

        :param packet: a RCONPacket or a list of RCONPackets.
        :param id: int, the id of the packet
        :param type: int, the type of the packet
        :param body: str, the body of the message, a regular python string,
        not a bytearray.
        """
        if packet is not None:  # build the message from packets

            # other parameters should not be set
            assert id is None, "id parameter should not be set if packet is given"
            assert type is None, "type parameter should not be set if packet is given"
            assert body is None, "body parameter should not be set if packet is given"

            # make sure that packet is a list
            if isinstance(packet, RCONPacket):  # pyright: ignore[reportUnnecessaryIsInstance]
                packet = [packet]

            assert len(packet) != 0, "packet has to be a RCONPacket or"\
                                     "an non empty list of RCONPackets"

            # check if all packets have the same type and id
            type = packet[0].type
            id = packet[0].id

            for i, p in enumerate(packet[1:]):
                assert p.type == type, "type of packet 0 %s and packet %d %s dont match" % (packet[0], i, p)
                assert p.id == id, "id of packet 0 %s and packet %d %s dont match" % (packet[0], i, p)

            self.packets = packet

        else:  # build the message from id, type, body
            assert id is not None, "id parameter should be set if no packet is given"
            assert type is not None, "type parameter should be set if no packet is given"
            assert body is not None, "body parameter should be set if no packet is given"

            self.packets = [RCONPacket(id=id, type=type, body="")]
            self.body = body  # call the body via the property to make sure that
            # it is split over multiple packets

    def add_packet(self, packet: RCONPacket) -> None:
        """
        Add an RCONPacket to the message.

        :param packet: a RCONPacket.
        """
        assert isinstance(packet, RCONPacket)

        self.packets.append(packet)

    def __iter__(self) -> Iterator[RCONPacket]:
        """Returns an iterator over the packets.
        The iterator has always at least one packet (which may be empty)."""
        return iter(self.packets)

    def msg(self) -> bytes:
        """Return the whole message as a bytearray."""
        return b"".join(p.msg() for p in self.packets)

    @property
    def id(self) -> int:
        """The id of the RCONPackets"""
        return self.packets[0].id

    @id.setter
    def id(self, value: int) -> None:
        for packet in self.packets:
            packet.id = value

    @property
    def type(self) -> int:
        """The type of the RCONPackets"""
        return self.packets[0].type

    @type.setter
    def type(self, value: int) -> None:
        for packet in self.packets:
            packet.type = value

    @property
    def body(self) -> str:
        """
        Returns the body of the message. This is the body of all packets joined
        together.
        """
        return "".join(p.body for p in self.packets)

    @body.setter
    def body(self, value: str) -> None:
        """
        sets the body of the RCONMessage.
        This may lead to adding/removing packets to/from the message.
        """
        # maximum packet size is 4096 - 10 bytes (id, type, 2x terminator)
        max_size = PACKET_SIZE - 10

        id = self.packets[0].id
        type = self.packets[0].type

        # Typing fix for python 3.5
        packets = [RCONPacket(0, 0, "")]
        packets.clear()
        while True:
            next_size = min(max_size, len(value))
            packets.append(RCONPacket(id=id, type=type, body=value[0:next_size]))
            value = value[next_size:]
            if len(value) == 0:
                break
        self.packets = packets

    @property
    def size(self) -> int:
        """The sum of all packets in this message."""
        return sum(p.size for p in self.packets)

    def __repr__(self) -> str:
        return "<RCONMessage type={}, id={}, body={}, num_packets={}>".format(
            self.type, self.id, self.body, len(self.packets))
