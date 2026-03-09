import os
import unittest

from WebHostLib.customserver import parse_game_ports, create_random_port_socket, get_used_ports

ci = bool(os.environ.get("CI"))


class TestPortAllocating(unittest.TestCase):
    def test_parse_game_ports(self) -> None:
        """Ensure that game ports with ranges are parsed correctly"""
        val = parse_game_ports(("1000-2000", "2000-5000", "1000-2000", 20, 40, "20", "0"))
        self.assertEqual(len(val.parsed_ports), 6, "Parsed port ranges is not the expected length")
        self.assertEqual(len(val.weights), 6, "Parsed weights are not the expected length")

        self.assertEqual(val.parsed_ports[0], range(1000, 2001), "The first range wasn't parsed correctly")
        self.assertEqual(val.parsed_ports[1], range(2000, 5001), "The second range wasn't parsed correctly")
        self.assertEqual(val.parsed_ports[0], val.parsed_ports[2],
                         "The first and third range are not the same when they should be")
        self.assertEqual(val.parsed_ports[3], range(20, 21), "The fourth range wasn't parsed correctly")
        self.assertEqual(val.parsed_ports[4], range(40, 41), "The fifth range was not parsed correctly")
        self.assertEqual(val.parsed_ports[3], val.parsed_ports[5],
                         "The fourth and last range are not the same when they should be")

        self.assertTrue(val.ephemeral_allowed, "The ephemeral allowed flag is not set even though it was passed")

        self.assertListEqual(val.weights, [1001, 4002, 5003, 5004, 5005, 5006],
                             "Cumulative weights are not the expected value")

        val = parse_game_ports(())
        self.assertListEqual(val.parsed_ports, [], "Empty list of game port returned something")
        self.assertFalse(val.ephemeral_allowed, "Empty list returned that ephemeral is allowed")

        val = parse_game_ports((0,))
        self.assertListEqual(val.parsed_ports, [], "Empty list of ranges returned something")
        self.assertTrue(val.ephemeral_allowed, "List with just 0 is not allowing ephemeral ports")

        val = parse_game_ports((1,))
        self.assertEqual(val.parsed_ports, [range(1,2)], "Parsed ports doesn't contain the expected values")
        self.assertFalse(val.ephemeral_allowed, "List with just single port returned that ephemeral is allowed")


    def test_parse_game_port_errors(self) -> None:
        """Ensure that game ports with incorrect values raise the expected error"""
        with self.assertRaises(ValueError, msg="Negative numbers didn't get interpreted as an invalid range"):
            parse_game_ports(tuple("-50215"))
        with self.assertRaises(ValueError, msg="Text got interpreted as a valid number"):
            parse_game_ports(tuple("dwafawg"))
        with self.assertRaises(
                ValueError,
                msg="A range with an extra dash at the end didn't get interpreted as an invalid number because of it's end dash"
        ):
            parse_game_ports(tuple("20-21215-"))
        with self.assertRaises(ValueError, msg="Text got interpreted as a valid number for the start of a range"):
            parse_game_ports(tuple("f-21215"))

    def test_random_port_socket_edge_cases(self) -> None:
        """Verify if edge cases on creation of random port socket is working fine"""
        # Try giving an empty tuple and fail over it
        with self.assertRaises(OSError) as err:
            create_random_port_socket(tuple(), "127.0.0.1")
        self.assertEqual(err.exception.errno, 98, "Raised an unexpected error code")
        self.assertEqual(err.exception.strerror, "No available ports", "Raised an unexpected error string")

        # Try only having ephemeral ports enabled
        try:
            create_random_port_socket(("0",), "127.0.0.1").close()
        except OSError as err:
            self.assertEqual(err.errno, 98, "Raised an unexpected error code")
            # If it returns our error string that means something is wrong with our code
            self.assertNotEqual(err.strerror, "No available ports",
                                "Raised an unexpected error string")

    @unittest.skipUnless(ci, "can't guarantee free ports outside of CI")
    def test_random_port_socket(self) -> None:
        """Verify if returned sockets use the correct port ranges"""
        sockets = []
        for _ in range(6):
            socket = create_random_port_socket(("8080-8085",), "127.0.0.1")
            sockets.append(socket)
            _, port = socket.getsockname()
            self.assertIn(port, range(8080, 8086), "Port of socket was not inside the expected range")
        for s in sockets:
            s.close()

        sockets.clear()
        for _ in range(30_000 - (len(get_used_ports()) + 100)):
            socket = create_random_port_socket(("30000-65535",), "127.0.0.1")
            sockets.append(socket)
            _, port = socket.getsockname()
            self.assertIn(port, range(30_000, 65536), "Port of socket was not inside the expected range")

        for s in sockets:
            s.close()
