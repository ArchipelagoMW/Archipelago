import os
import unittest
from socket import socket as Socket  # noqa: N812

from Utils import is_macos
from WebHostLib.customserver import RandomPortSocketCreator

ci = bool(os.environ.get("CI"))


class TestPortAllocating(unittest.TestCase):
    def test_parse_game_ports(self) -> None:
        """Ensure that game ports with ranges are parsed correctly"""
        val = RandomPortSocketCreator._parse_game_ports(("1000-2000", "2000-5000", "1000-2000", 20, 40, "20", "0"))

        self.assertCountEqual(val.valid_ports,
                              [*range(1000, 2001), *range(2000, 5001), *range(1000, 2001), 20, 40, 20],
                              "The parsed game ports are not the expected length")
        self.assertTrue(val.ephemeral_allowed, "The ephemeral allowed flag is not set even though it was passed")

        val = RandomPortSocketCreator._parse_game_ports(())
        self.assertListEqual(val.valid_ports, [], "Empty list of game port returned something")
        self.assertFalse(val.ephemeral_allowed, "Empty list returned that ephemeral is allowed")

        val = RandomPortSocketCreator._parse_game_ports((0,))
        self.assertListEqual(val.valid_ports, [], "Empty list of ranges returned something")
        self.assertTrue(val.ephemeral_allowed, "List with just 0 is not allowing ephemeral ports")

        val = RandomPortSocketCreator._parse_game_ports((1,))
        self.assertListEqual(val.valid_ports, [1], "Valid ports doesn't contain the expected values")
        self.assertFalse(val.ephemeral_allowed, "List with just single port returned that ephemeral is allowed")

    def test_parse_game_port_errors(self) -> None:
        """Ensure that game ports with incorrect values raise the expected error"""
        with self.assertRaises(ValueError, msg="Negative numbers didn't get interpreted as an invalid range"):
            RandomPortSocketCreator._parse_game_ports(tuple("-50215"))
        with self.assertRaises(ValueError, msg="Text got interpreted as a valid number"):
            RandomPortSocketCreator._parse_game_ports(tuple("dwafawg"))
        with self.assertRaises(
                ValueError,
                msg="A range with an extra dash at the end didn't get interpreted as an invalid number because of it's end dash"
        ):
            RandomPortSocketCreator._parse_game_ports(tuple("20-21215-"))
        with self.assertRaises(ValueError, msg="Text got interpreted as a valid number for the start of a range"):
            RandomPortSocketCreator._parse_game_ports(tuple("f-21215"))

    def test_random_port_socket_edge_cases(self) -> None:
        """Verify if edge cases on creation of random port socket is working fine"""
        # Try giving an empty tuple and fail over it
        creator = RandomPortSocketCreator(())
        with self.assertRaises(OSError) as err:
            creator.create("127.0.0.1")
        self.assertEqual(err.exception.errno, 98, "Raised an unexpected error code")
        self.assertEqual(err.exception.strerror, "No available ports", "Raised an unexpected error string")

        # Try only having ephemeral ports enabled
        creator = RandomPortSocketCreator(("0",))
        try:
            creator.create("127.0.0.1").close()
        except OSError as err:
            self.assertEqual(err.errno, 98, "Raised an unexpected error code")
            # If it returns our error string that means something is wrong with our code
            self.assertNotEqual(err.strerror, "No available ports",
                                "Raised an unexpected error string")

    @unittest.skipUnless(ci, "can't guarantee free ports outside of CI")
    def test_random_port_socket(self) -> None:
        """Verify if returned sockets use the correct port ranges"""
        creator = RandomPortSocketCreator(("8080-8085",))
        sockets: list[Socket] = []
        for _ in range(6):
            socket = creator.create("127.0.0.1")
            sockets.append(socket)
            _, port = socket.getsockname()
            self.assertIn(port, range(8080, 8086), "Port of socket was not inside the expected range")
        for s in sockets:
            s.close()

        sockets.clear()
        creator = RandomPortSocketCreator(("30000-65535",))
        length = 5_000 if is_macos else (30_000 - len(creator._get_used_ports()))
        for _ in range(length):
            socket = creator.create("127.0.0.1")
            sockets.append(socket)
            _, port = socket.getsockname()
            self.assertIn(port, range(30_000, 65536), "Port of socket was not inside the expected range")

        for s in sockets:
            s.close()
