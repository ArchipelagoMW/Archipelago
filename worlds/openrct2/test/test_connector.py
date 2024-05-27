import unittest
import sys
import inspect
import asyncio
from pathlib import Path

if __name__ == '__main__':
    currentframe = Path(inspect.getfile(inspect.currentframe()))
    parentdir = currentframe.parent.parent
    sys.path.insert(0, str(parentdir))

from OpenRCT2Socket import OpenRCT2Socket

class FakeCtx():
    last_received = None
    received = asyncio.Event()

    async def send_msgs(self, data):
        print('FakeCtx.send_msgs:', data)
        self.last_received = data
        self.received.set()

test_network = False
class TestConn(unittest.TestCase):
    def test_init(self) -> None:
        global test_network
        self.assertTrue(True, "true is true")
        if not test_network:
            return
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.asynctests())
    
    async def asynctests(self):
        ctx = FakeCtx()
        gamesock = OpenRCT2Socket(ctx)

        print('waiting for game connection...')
        await gamesock.connected_to_game.wait()

        data = {'cmd': 'Ping', 'extra': 123}
        gamesock.sendobj(data)
        await ctx.received.wait()
        data['cmd'] = 'Pong'
        self.assertDictEqual(ctx.last_received[0], data)


def run_tests():
    global test_network
    test_network = True
    unittest.main(verbosity=9, warnings="error", failfast=True)

if __name__ == '__main__':
    run_tests()
