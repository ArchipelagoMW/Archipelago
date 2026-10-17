import socket
import struct
import threading
import unittest
from collections.abc import Callable
from unittest.mock import Mock, patch

from .. import Memory
from ..Memory import (
    APBridgeError,
    APBridgeRemoteError,
    APBridgeWriteUncertainError,
    DolphinMemory,
    WiiMemory,
)


class FakeWRTXCache:
    """Recent transactions shared across UDP peers, recorded before acknowledgments."""

    def __init__(self, apply_write: Callable[[int, bytes], None] | None = None) -> None:
        self.transactions: dict[int, tuple[int, int, bytes]] = {}
        self.memory: dict[int, int] = {}
        self.writes: list[tuple[int, bytes]] = []
        self.apply_write = apply_write

    def reply(self, request: bytes) -> bytes:
        address, length, _, txid = struct.unpack(">IHHQ", request[4:20])
        transaction = (address, length, request[20:])
        previous = self.transactions.get(txid)
        if txid == 0 or (previous is not None and previous != transaction):
            code = 5 if txid == 0 else 6
            return b"ERR!" + request[4:10] + bytes([code, 0]) + request[12:20]
        if previous is None:
            payload = request[20:]
            self.memory.update((address + offset, value) for offset, value in enumerate(payload))
            self.writes.append((address, payload))
            if self.apply_write is not None:
                self.apply_write(address, payload)
            self.transactions[txid] = transaction
            if len(self.transactions) > 16:
                del self.transactions[next(iter(self.transactions))]
        return b"WROK" + request[4:20]


class FakeAPBridge:
    """A local UDP peer; assertions stay in the test thread, never in the worker."""

    def __init__(self, responder: Callable[[bytes], bytes | None] | None = None) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("127.0.0.1", 0))
        self.socket.settimeout(0.05)
        self.port = self.socket.getsockname()[1]
        self.write_cache = FakeWRTXCache()
        self.responder = responder or self.process_request
        self.requests: list[bytes] = []
        self.request_peers: list[tuple[str, int]] = []
        self.peers: set[tuple[str, int]] = set()
        self.errors: list[Exception] = []
        self.stopping = threading.Event()
        self.thread = threading.Thread(target=self.run, daemon=True)

    @staticmethod
    def reply(request: bytes) -> bytes:
        if request == b"HELLO":
            return b"NIN-AP"
        address, length = struct.unpack(">IH", request[4:10])
        if request[:4] == b"READ":
            payload = b"GZLE99" if address == 0x80000000 and length == 6 else bytes(range(256))[:length]
            return b"DATA" + request[4:12] + payload
        if request[:4] == b"WRTX":
            return b"WROK" + request[4:20]
        raise ValueError(f"Unexpected request magic: {request[:4]!r}")

    def process_request(self, request: bytes) -> bytes:
        if request[:4] == b"WRTX":
            return self.write_cache.reply(request)
        return self.reply(request)

    def run(self) -> None:
        while not self.stopping.is_set():
            try:
                request, peer = self.socket.recvfrom(65535)
            except TimeoutError:
                continue
            self.requests.append(request)
            self.request_peers.append(peer)
            self.peers.add(peer)
            try:
                reply = self.responder(request)
                if reply is not None:
                    self.socket.sendto(reply, peer)
            except Exception as error:
                self.errors.append(error)
                return

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *_):
        self.stopping.set()
        self.thread.join(2)
        self.socket.close()
        if self.thread.is_alive():
            raise AssertionError("Fake UDP peer did not stop")
        if self.errors:
            raise AssertionError(self.errors)


class TestWiiMemory(unittest.TestCase):
    def connect(self, peer: FakeAPBridge) -> WiiMemory:
        memory = WiiMemory("127.0.0.1", peer.port, timeout=0.5)
        self.addCleanup(memory.un_hook)
        memory.hook()
        return memory

    def test_probe_and_socket_reuse(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            self.assertTrue(memory.is_hooked())
            self.assertEqual(peer.requests, [b"HELLO", b"READ\x80\x00\x00\x00\x00\x06\x00\x00"])
            memory.read_bytes(0x803FE87C, 1)
            memory.write_byte(0x803FE87C, 42)
            self.assertEqual(len(peer.peers), 1)
            memory.un_hook()
            memory.un_hook()
            self.assertFalse(memory.is_hooked())
            with self.assertRaisesRegex(APBridgeError, "disconnected"):
                memory.read_byte(0x803FE87C)

    def test_hello_validation(self):
        for reply in (b"", b"NIN-A", b"NIN-AP\0", b"OTHER!"):
            with self.subTest(reply=reply), FakeAPBridge(lambda request, reply=reply: reply) as peer:
                memory = WiiMemory("127.0.0.1", peer.port)
                with self.assertRaisesRegex(APBridgeError, "NIN-AP"):
                    memory.hook()
                self.assertFalse(memory.is_hooked())
                self.assertIsNone(memory._socket)
                self.assertEqual(peer.requests, [b"HELLO"])

    def test_wrong_game_probe(self):
        def responder(request):
            if request == b"HELLO":
                return b"NIN-AP"
            return b"DATA" + request[4:12] + b"GLMP01"

        with FakeAPBridge(responder) as peer:
            memory = WiiMemory("127.0.0.1", peer.port)
            with self.assertRaisesRegex(APBridgeError, "GZLE99"):
                memory.hook()
            self.assertFalse(memory.is_hooked())
            self.assertIsNone(memory._socket)

    def test_read_encoding_and_big_endian_primitives(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            self.assertEqual(memory.read_bytes(0x81234567, 256), bytes(range(256)))
            self.assertEqual(peer.requests[-1], b"READ\x81\x23\x45\x67\x01\x00\x00\x00")
            self.assertEqual(memory.read_byte(0x803FE87C), 0)
            self.assertEqual(memory.read_word(0x803FE87C), 0x00010203)

    def test_read_retries_after_packet_loss_and_retains_replacement_socket(self):
        for dropped_replies in (1, 2):
            with self.subTest(dropped_replies=dropped_replies), FakeAPBridge() as peer:
                memory = self.connect(peer)
                sockets = [memory._socket]
                socket_factory = socket.socket
                attempts = 0

                def new_socket(*args, socket_factory=socket_factory, sockets=sockets, **kwargs):
                    replacement = socket_factory(*args, **kwargs)
                    sockets.append(replacement)
                    return replacement

                def responder(request, dropped_replies=dropped_replies):
                    nonlocal attempts
                    attempts += 1
                    return None if attempts <= dropped_replies else FakeAPBridge.reply(request)

                peer.responder = responder
                with patch.object(socket, "socket", side_effect=new_socket):
                    self.assertEqual(memory.read_bytes(0x803FE87C, 4), b"\x00\x01\x02\x03")
                request = b"READ\x80\x3F\xE8\x7C\x00\x04\x00\x00"
                self.assertEqual(peer.requests[2:], [request] * (dropped_replies + 1))
                self.assertEqual(len(sockets), dropped_replies + 1)
                self.assertEqual(len(set(peer.request_peers[2:])), dropped_replies + 1)
                for retired_socket in sockets[:-1]:
                    self.assertEqual(retired_socket.fileno(), -1)
                active_socket = sockets[-1]
                self.assertIs(memory._socket, active_socket)
                self.assertEqual(active_socket.gettimeout(), 0.5)
                self.assertTrue(memory.is_hooked())

                peer.responder = FakeAPBridge.reply
                memory.read_byte(0x803FE87C)
                memory.write_byte(0x803FE87C, 42)
                self.assertIs(memory._socket, active_socket)
                self.assertEqual(peer.request_peers[-3:], [active_socket.getsockname()] * 3)

    def test_probe_read_retries_without_repeating_hello(self):
        for dropped_replies in (1, 2):
            with self.subTest(dropped_replies=dropped_replies), FakeAPBridge() as peer:
                memory = WiiMemory("127.0.0.1", peer.port, timeout=0.15)
                self.addCleanup(memory.un_hook)
                attempts = 0
                probe_states = []

                def responder(request, memory=memory, probe_states=probe_states, dropped_replies=dropped_replies):
                    nonlocal attempts
                    if request[:4] == b"READ":
                        attempts += 1
                        probe_states.append(memory.is_hooked())
                        if attempts <= dropped_replies:
                            return None
                    return FakeAPBridge.reply(request)

                peer.responder = responder
                memory.hook()
                probe = b"READ\x80\x00\x00\x00\x00\x06\x00\x00"
                self.assertEqual(peer.requests, [b"HELLO"] + [probe] * (dropped_replies + 1))
                self.assertEqual(probe_states, [False] * (dropped_replies + 1))
                self.assertEqual(len(set(peer.request_peers[1:])), dropped_replies + 1)
                self.assertTrue(memory.is_hooked())
                self.assertEqual(memory._socket.getsockname(), peer.request_peers[-1])

    def test_probe_read_exhaustion_disconnects(self):
        with FakeAPBridge(lambda request: b"NIN-AP" if request == b"HELLO" else None) as peer:
            memory = WiiMemory("127.0.0.1", peer.port, timeout=0.15)
            with self.assertRaisesRegex(APBridgeError, "timed out after 3 attempts"):
                memory.hook()
            self.assertFalse(memory.is_hooked())
            self.assertIsNone(memory._socket)
            probe = b"READ\x80\x00\x00\x00\x00\x06\x00\x00"
            self.assertEqual(peer.requests, [b"HELLO", probe, probe, probe])
            self.assertEqual(len(peer.peers), 3)

    def test_protocol_error_after_timeout_stops_read_retries(self):
        for error_reply in (b"BAD", b"ERR!\x80\x3F\xE8\x7C\x00\x01\x02\x00"):
            with self.subTest(error_reply=error_reply), FakeAPBridge() as peer:
                memory = self.connect(peer)
                attempts = 0

                def responder(request, error_reply=error_reply):
                    nonlocal attempts
                    attempts += 1
                    return None if attempts == 1 else error_reply

                peer.responder = responder
                with self.assertRaises(APBridgeError):
                    memory.read_byte(0x803FE87C)
                self.assertEqual(len(peer.requests), 4)
                self.assertEqual(peer.requests[-2:], [b"READ\x80\x3F\xE8\x7C\x00\x01\x00\x00"] * 2)
                self.assertFalse(memory.is_hooked())
                self.assertIsNone(memory._socket)

    def test_non_timeout_transport_error_is_not_retried(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            transport = Mock(wraps=memory._socket)
            transport.recv.side_effect = ConnectionResetError("Connection reset")
            memory._socket = transport
            with patch.object(memory, "_open_socket") as open_socket:
                with self.assertRaisesRegex(APBridgeError, "UDP exchange failed"):
                    memory.read_byte(0x803FE87C)
                open_socket.assert_not_called()
            transport.send.assert_called_once_with(b"READ\x80\x3F\xE8\x7C\x00\x01\x00\x00")
            transport.close.assert_called_once_with()
            self.assertFalse(memory.is_hooked())
            self.assertIsNone(memory._socket)

    def test_read_retry_socket_creation_failure_disconnects(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            old_socket = memory._socket
            peer.responder = lambda request: None
            with patch.object(socket, "socket", side_effect=OSError("Cannot create socket")) as create_socket:
                with self.assertRaisesRegex(APBridgeError, "Cannot create socket"):
                    memory.read_byte(0x803FE87C)
                create_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
            self.assertEqual(old_socket.fileno(), -1)
            self.assertEqual(len(peer.requests), 3)
            self.assertFalse(memory.is_hooked())
            self.assertIsNone(memory._socket)

    def test_read_retry_rejects_reused_source_port(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            old_socket = memory._socket
            replacement = Mock()
            replacement.getsockname.return_value = old_socket.getsockname()
            peer.responder = lambda request: None
            with patch.object(socket, "socket", return_value=replacement):
                with self.assertRaisesRegex(APBridgeError, "fresh UDP source port"):
                    memory.read_byte(0x803FE87C)
            replacement.send.assert_not_called()
            replacement.close.assert_called_once_with()
            self.assertEqual(old_socket.fileno(), -1)
            self.assertFalse(memory.is_hooked())
            self.assertIsNone(memory._socket)

    def test_write_encoding_and_wrok(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            payload = bytes(range(256))
            txid = 0xFEDCBA9876543210
            with patch.object(Memory.secrets, "randbits", side_effect=[txid, txid + 1]) as randbits:
                self.assertIsNone(memory.write_bytes(0x803FE87C, payload))
                self.assertEqual(
                    peer.requests[-1],
                    b"WRTX\x80\x3F\xE8\x7C\x01\x00\x00\x00\xFE\xDC\xBA\x98\x76\x54\x32\x10" + payload,
                )
                self.assertEqual(len(peer.requests[-1]), 276)
                memory.write_byte(0x803FE87C, 0xA5)
                self.assertEqual(
                    peer.requests[-1],
                    b"WRTX\x80\x3F\xE8\x7C\x00\x01\x00\x00\xFE\xDC\xBA\x98\x76\x54\x32\x11\xA5",
                )
                self.assertEqual(randbits.call_count, 2)
                randbits.assert_called_with(64)
            self.assertFalse(any(request.startswith(b"WRIT") for request in peer.requests))

    def test_remote_error_codes(self):
        for operation in ("read", "write"):
            for code in range(1, 5 if operation == "read" else 7):
                with self.subTest(operation=operation, code=code), FakeAPBridge() as peer:
                    memory = self.connect(peer)
                    peer.responder = (
                        lambda request, code=code: b"ERR!" + request[4:10] + bytes([code, 0]) + request[12:20]
                    )
                    with self.assertRaises(APBridgeRemoteError) as caught:
                        if operation == "read":
                            memory.read_byte(0x803FE87C)
                        else:
                            memory.write_byte(0x803FE87C, 42)
                    self.assertEqual(caught.exception.code, code)
                    self.assertIn("0x803FE87C", str(caught.exception))
                    self.assertFalse(memory.is_hooked())
                    self.assertIsNone(memory._socket)
                    self.assertEqual(len(peer.requests), 3)

    def test_wrtx_retries_deduplicate_and_retain_fresh_socket(self):
        for dropped_replies in (1, 2):
            with self.subTest(dropped_replies=dropped_replies), FakeAPBridge() as peer:
                memory = WiiMemory("127.0.0.1", peer.port, timeout=0.15)
                self.addCleanup(memory.un_hook)
                memory.hook()
                sockets = [memory._socket]
                socket_factory = socket.socket
                attempts = 0

                def new_socket(*args, socket_factory=socket_factory, sockets=sockets, **kwargs):
                    self.assertEqual(sockets[-1].fileno(), -1)
                    replacement = socket_factory(*args, **kwargs)
                    sockets.append(replacement)
                    return replacement

                def responder(request, peer=peer, dropped_replies=dropped_replies):
                    nonlocal attempts
                    reply = peer.process_request(request)
                    attempts += 1
                    return None if attempts <= dropped_replies else reply

                peer.responder = responder
                with patch.object(Memory.secrets, "randbits", return_value=0x0102030405060708) as randbits:
                    with patch.object(socket, "socket", side_effect=new_socket):
                        memory.write_byte(0x803FE87C, 42)
                    randbits.assert_called_once_with(64)
                expected = b"WRTX\x80\x3F\xE8\x7C\x00\x01\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\x2A"
                self.assertEqual(peer.requests[2:], [expected] * (dropped_replies + 1))
                self.assertEqual(peer.write_cache.writes, [(0x803FE87C, b"\x2A")])
                self.assertEqual(peer.write_cache.memory[0x803FE87C], 42)
                self.assertEqual(len(set(peer.request_peers[2:])), dropped_replies + 1)
                self.assertEqual(len(sockets), dropped_replies + 1)
                active_socket = sockets[-1]
                self.assertIs(memory._socket, active_socket)
                self.assertTrue(memory.is_hooked())

                peer.responder = peer.process_request
                memory.read_byte(0x803FE87C)
                memory.write_byte(0x803FE87D, 43)
                self.assertIs(memory._socket, active_socket)
                self.assertEqual(peer.request_peers[-3:], [active_socket.getsockname()] * 3)
                self.assertFalse(any(request.startswith(b"WRIT") for request in peer.requests))

    def test_wrtx_exhausted_acknowledgments_apply_once(self):
        with FakeAPBridge() as peer:
            memory = WiiMemory("127.0.0.1", peer.port, timeout=0.15)
            memory.hook()

            def responder(request):
                reply = peer.process_request(request)
                return None if request[:4] == b"WRTX" else reply

            peer.responder = responder
            with patch.object(Memory.secrets, "randbits", return_value=0x123456789ABCDEF0) as randbits:
                with self.assertRaisesRegex(APBridgeWriteUncertainError, "timed out after 3 attempts"):
                    memory.write_byte(0x803FE87C, 42)
                randbits.assert_called_once_with(64)
            self.assertEqual(len(peer.requests), 5)
            self.assertEqual(peer.requests[2:], [peer.requests[2]] * 3)
            self.assertEqual(len(set(peer.request_peers[2:])), 3)
            self.assertEqual(peer.write_cache.writes, [(0x803FE87C, b"\x2A")])
            self.assertFalse(memory.is_hooked())
            self.assertIsNone(memory._socket)
            memory.hook()
            memory.un_hook()
            self.assertEqual(peer.requests[5:], [b"HELLO", b"READ\x80\x00\x00\x00\x00\x06\x00\x00"])
            self.assertEqual(len(peer.write_cache.writes), 1)

    def test_wrtx_independent_writes_get_new_transaction_ids(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            with patch.object(Memory.secrets, "randbits", side_effect=[17, 18]) as randbits:
                memory.write_byte(0x803FE87C, 42)
                memory.write_byte(0x803FE87C, 42)
                self.assertEqual(randbits.call_count, 2)
            self.assertEqual([int.from_bytes(request[12:20], "big") for request in peer.requests[2:]], [17, 18])
            self.assertEqual(peer.write_cache.writes, [(0x803FE87C, b"\x2A")] * 2)

    def test_wrtx_transaction_id_generation_skips_zero(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            with patch.object(Memory.secrets, "randbits", side_effect=[0, 0, 0xFFFFFFFFFFFFFFFF]) as randbits:
                memory.write_byte(0x803FE87C, 42)
                self.assertEqual(randbits.call_count, 3)
                self.assertTrue(all(call.args == (64,) for call in randbits.call_args_list))
            self.assertEqual(peer.requests[-1][12:20], b"\xFF" * 8)
            self.assertEqual(len(peer.requests), 3)

    def test_wrtx_transaction_conflict_does_not_write_or_retry(self):
        for address, payload in ((0x803FE87D, b"\x2A"), (0x803FE87C, b"\x2B"), (0x803FE87C, b"\x2A\x2B")):
            with self.subTest(address=address, payload=payload), FakeAPBridge() as peer:
                memory = self.connect(peer)
                with patch.object(Memory.secrets, "randbits", return_value=123):
                    memory.write_byte(0x803FE87C, 42)
                    with self.assertRaisesRegex(APBridgeRemoteError, "transaction ID conflict") as caught:
                        memory.write_bytes(address, payload)
                self.assertEqual(caught.exception.code, 6)
                self.assertEqual(len(peer.requests), 4)
                self.assertEqual(peer.write_cache.writes, [(0x803FE87C, b"\x2A")])
                self.assertEqual(peer.write_cache.memory, {0x803FE87C: 42})
                self.assertFalse(memory.is_hooked())

    def test_wrtx_wrong_echoed_transaction_id_is_uncertain(self):
        for magic, status in ((b"WROK", 0), (b"ERR!", 6)):
            with self.subTest(magic=magic), FakeAPBridge() as peer:
                memory = self.connect(peer)

                def responder(request, magic=magic, status=status, peer=peer):
                    peer.process_request(request)
                    return magic + request[4:10] + bytes([status, 0]) + (124).to_bytes(8, "big")

                peer.responder = responder
                with patch.object(Memory.secrets, "randbits", return_value=123):
                    with self.assertRaisesRegex(APBridgeWriteUncertainError, "echoed transaction ID"):
                        memory.write_byte(0x803FE87C, 42)
                self.assertEqual(len(peer.requests), 3)
                self.assertEqual(len(peer.write_cache.writes), 1)
                self.assertFalse(memory.is_hooked())
                self.assertIsNone(memory._socket)

    def test_wrtx_legacy_wrok_is_uncertain_and_does_not_fall_back(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            peer.responder = lambda request: peer.process_request(request)[:12]
            with self.assertRaisesRegex(APBridgeWriteUncertainError, "reply size 12, expected 20"):
                memory.write_byte(0x803FE87C, 42)
            self.assertEqual(len(peer.requests), 3)
            self.assertEqual(peer.requests[-1][:4], b"WRTX")
            self.assertEqual(peer.write_cache.writes, [(0x803FE87C, b"\x2A")])
            self.assertFalse(memory.is_hooked())

    def test_wrtx_transport_errors_do_not_retry(self):
        for stage, error in (("send", TimeoutError()), ("send", OSError("Send failed")),
                             ("recv", ConnectionResetError("Connection reset"))):
            with self.subTest(stage=stage, error=error), FakeAPBridge() as peer:
                memory = self.connect(peer)
                transport = Mock(wraps=memory._socket)
                getattr(transport, stage).side_effect = error
                memory._socket = transport
                with patch.object(memory, "_open_socket") as open_socket:
                    with self.assertRaises(APBridgeWriteUncertainError):
                        memory.write_byte(0x803FE87C, 42)
                    open_socket.assert_not_called()
                self.assertEqual(transport.send.call_count, 1)
                self.assertEqual(transport.send.call_args.args[0][:4], b"WRTX")
                if stage == "send":
                    transport.recv.assert_not_called()
                transport.close.assert_called_once_with()
                self.assertFalse(memory.is_hooked())
                self.assertIsNone(memory._socket)

    def test_wrtx_retry_socket_failure_is_uncertain(self):
        for failure in ("create", "reuse"):
            with self.subTest(failure=failure), FakeAPBridge() as peer:
                memory = WiiMemory("127.0.0.1", peer.port, timeout=0.15)
                memory.hook()
                old_socket = memory._socket
                replacement = Mock()
                replacement.getsockname.return_value = old_socket.getsockname()

                def responder(request, peer=peer):
                    peer.process_request(request)

                peer.responder = responder
                error = OSError("Cannot create socket") if failure == "create" else None
                with patch.object(socket, "socket", side_effect=error, return_value=replacement):
                    with self.assertRaises(APBridgeWriteUncertainError):
                        memory.write_byte(0x803FE87C, 42)
                replacement.send.assert_not_called()
                if failure == "reuse":
                    replacement.close.assert_called_once_with()
                self.assertEqual(old_socket.fileno(), -1)
                self.assertEqual(len(peer.requests), 3)
                self.assertEqual(len(peer.write_cache.writes), 1)
                self.assertFalse(memory.is_hooked())
                self.assertIsNone(memory._socket)

    def test_wrtx_protocol_error_after_timeout_is_not_retried(self):
        for valid_error in (False, True):
            with self.subTest(valid_error=valid_error), FakeAPBridge() as peer:
                memory = WiiMemory("127.0.0.1", peer.port, timeout=0.15)
                memory.hook()
                attempts = 0

                def responder(request, peer=peer, valid_error=valid_error):
                    nonlocal attempts
                    peer.process_request(request)
                    attempts += 1
                    if attempts == 1:
                        return None
                    if valid_error:
                        return b"ERR!" + request[4:10] + b"\x06\x00" + request[12:20]
                    return b"BAD"

                peer.responder = responder
                expected_error = APBridgeRemoteError if valid_error else APBridgeWriteUncertainError
                with self.assertRaises(expected_error):
                    memory.write_byte(0x803FE87C, 42)
                self.assertEqual(len(peer.requests), 4)
                self.assertEqual(peer.requests[2:], [peer.requests[2]] * 2)
                self.assertEqual(len(peer.write_cache.writes), 1)
                self.assertFalse(memory.is_hooked())

    def test_malformed_responses(self):
        changes = {
            "magic": lambda reply: b"NOPE" + reply[4:],
            "address": lambda reply: reply[:4] + b"\x80\x00\x00\x00" + reply[8:],
            "length": lambda reply: reply[:8] + b"\x00\x02" + reply[10:],
            "reserved high": lambda reply: reply[:10] + b"\x01\x00" + reply[12:],
            "reserved low": lambda reply: reply[:10] + b"\x00\x01" + reply[12:],
            "short header": lambda reply: reply[:11],
            "short response": lambda reply: reply[:-1],
            "long response": lambda reply: reply + b"\x00",
            "oversized datagram": lambda reply: reply + bytes(1024),
        }
        for operation in ("read", "write"):
            for label, change in changes.items():
                with self.subTest(operation=operation, change=label), FakeAPBridge() as peer:
                    memory = self.connect(peer)
                    peer.responder = lambda request, change=change: change(FakeAPBridge.reply(request))
                    error = APBridgeError if operation == "read" else APBridgeWriteUncertainError
                    with self.assertRaises(error):
                        if operation == "read":
                            memory.read_byte(0x803FE87C)
                        else:
                            memory.write_byte(0x803FE87C, 42)
                    self.assertFalse(memory.is_hooked())
                    self.assertIsNone(memory._socket)
                    self.assertEqual(len(peer.requests), 3)

    def test_malformed_error_responses(self):
        replies = (
            b"ERR!\x80\x3F\xE8\x7C\x00\x01\x00\x00",  # zero error code
            b"ERR!\x80\x3F\xE8\x7C\x00\x01\x07\x00",  # unknown error code
            b"ERR!\x80\x3F\xE8\x7C\x00\x01\x01\x01",  # reserved
            b"ERR!\x80\x3F\xE8\x7D\x00\x01\x01\x00",  # address
            b"ERR!\x80\x3F\xE8\x7C\x00\x02\x01\x00",  # length
            b"ERR!\x80\x3F\xE8\x7C\x00\x01\x01",  # short
            b"ERR!\x80\x3F\xE8\x7C\x00\x01\x01\x00\x00",  # long
        )
        for reply in replies:
            with self.subTest(reply=reply), FakeAPBridge() as peer:
                memory = self.connect(peer)
                peer.responder = lambda request, reply=reply: reply + request[12:20]
                with self.assertRaises(APBridgeWriteUncertainError):
                    memory.write_byte(0x803FE87C, 42)
                self.assertFalse(memory.is_hooked())
                self.assertEqual(len(peer.requests), 3)

    def test_timeouts_do_not_replay_writes_after_reconnect(self):
        for operation in ("hello", "read", "write"):
            with self.subTest(operation=operation), FakeAPBridge() as peer:
                memory = WiiMemory("127.0.0.1", peer.port, timeout=0.15)
                if operation != "hello":
                    memory.hook()
                peer.responder = lambda request: None
                with self.assertRaisesRegex(APBridgeError, "timed out") as caught:
                    if operation == "hello":
                        memory.hook()
                    elif operation == "read":
                        memory.read_byte(0x803FE87C)
                    else:
                        memory.write_byte(0x803FE87C, 42)
                self.assertFalse(memory.is_hooked())
                self.assertIsNone(memory._socket)
                self.assertEqual(len(peer.requests), {"hello": 1, "read": 5, "write": 5}[operation])
                if operation == "read":
                    self.assertIn("timed out after 3 attempts", str(caught.exception))
                    self.assertEqual(peer.requests[2:], [b"READ\x80\x3F\xE8\x7C\x00\x01\x00\x00"] * 3)
                    self.assertEqual(len(set(peer.request_peers[2:])), 3)
                if operation == "write":
                    self.assertIsInstance(caught.exception, APBridgeWriteUncertainError)
                    # A fresh connection probes only; it never replays the timed-out write.
                    peer.responder = FakeAPBridge.reply
                    memory.hook()
                    memory.un_hook()
                    self.assertEqual(sum(request.startswith(b"WRTX") for request in peer.requests), 3)
                    self.assertEqual(peer.requests[2:5], [peer.requests[2]] * 3)
                    self.assertFalse(any(request.startswith(b"WRIT") for request in peer.requests))

    def test_reject_invalid_ranges_before_sending(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            invalid = (
                (0x80000000, 0), (0x80000000, 257), (0x80000000, -1),
                (0x7FFFFFFF, 1), (0x81800000, 1), (0x817FFFFF, 2),
                (0x817FFF01, 256), (-1, 1), (0x100000000, 1),
            )
            for address, length in invalid:
                with self.subTest(address=address, length=length):
                    with self.assertRaises(APBridgeError):
                        memory.read_bytes(address, length)
                    if length >= 0:
                        with self.assertRaises(APBridgeError):
                            memory.write_bytes(address, bytes(length))
            self.assertEqual(len(peer.requests), 2)
            self.assertTrue(memory.is_hooked())

    def test_mem1_valid_boundaries(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            for address, length in ((0x80000000, 1), (0x817FFFFF, 1), (0x817FFF00, 256)):
                with self.subTest(address=address, length=length):
                    self.assertEqual(len(memory.read_bytes(address, length)), length)
                    memory.write_bytes(address, bytes(length))

    def test_connected_socket_ignores_other_peer(self):
        with FakeAPBridge() as peer, socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as stranger:
            memory = self.connect(peer)
            stranger.bind(("127.0.0.1", 0))
            stranger.sendto(b"BAD!", next(iter(peer.peers)))
            self.assertEqual(memory.read_byte(0x803FE87C), 0)

    def test_invalid_byte_values_are_not_truncated(self):
        with FakeAPBridge() as peer:
            memory = self.connect(peer)
            for value in (-1, 256):
                with self.assertRaises(ValueError):
                    memory.write_byte(0x803FE87C, value)
            self.assertEqual(len(peer.requests), 2)


class TestDolphinMemory(unittest.TestCase):
    def test_delegates_native_operations(self):
        engine = Mock()
        engine.is_hooked.return_value = True
        engine.read_bytes.return_value = b"GZLE99"
        engine.read_byte.return_value = 42
        engine.read_word.return_value = 0x12345678
        with patch.dict("sys.modules", {"dolphin_memory_engine": engine}):
            memory = DolphinMemory()
            self.assertFalse(memory.is_hooked())
            memory.un_hook()
            engine.un_hook.assert_not_called()
            memory.hook()
            self.assertTrue(memory.is_hooked())
            self.assertEqual(memory.read_bytes(0x80000000, 6), b"GZLE99")
            self.assertEqual(memory.read_byte(0x803FE87C), 42)
            self.assertEqual(memory.read_word(0x803FE87C), 0x12345678)
            memory.write_byte(0x803FE87C, 42)
            memory.write_bytes(0x803FE87C, b"\x12\x34")
            memory.un_hook()
            engine.hook.assert_called_once_with()
            engine.read_bytes.assert_called_once_with(0x80000000, 6)
            engine.read_byte.assert_called_once_with(0x803FE87C)
            engine.read_word.assert_called_once_with(0x803FE87C)
            engine.write_byte.assert_called_once_with(0x803FE87C, 42)
            engine.write_bytes.assert_called_once_with(0x803FE87C, b"\x12\x34")
            engine.un_hook.assert_called_once_with()
