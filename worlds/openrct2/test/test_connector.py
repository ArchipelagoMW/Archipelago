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
else:
    from worlds.openrct2.OpenRCT2Socket import OpenRCT2Socket

class FakeCtx():
    last_received = None
    received = asyncio.Event()

    async def send_msgs(self, data):
        print('FakeCtx.send_msgs:', data)
        self.last_received = data
        self.received.set()

test_network = False
class TestConn(unittest.TestCase):
    def subTest(self, msg, **kargs):
        print('\n=============\nsubTest', msg)
        return super().subTest(msg, **kargs)

    def test_init(self) -> None:
        global test_network
        self.assertTrue(True, "true is true")
        if not test_network:
            return
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.asynctests())
    
    async def ping(self, data):
        self.gamesock.sendobj(data)
        await asyncio.wait_for(self.ctx.received.wait(), 60)
        self.ctx.received.clear()
        data['cmd'] = 'Pong'
        last_received = self.ctx.last_received[0]
        self.assertDictEqual(last_received, data)

    async def asynctests(self):
        self.ctx = FakeCtx()
        self.gamesock = OpenRCT2Socket(self.ctx)
        print('waiting for game connection...')
        await self.gamesock.connected_to_game.wait()

        with self.subTest("small packet"):
            data = {'cmd': 'Ping', 'extra': 123}
            await self.ping(data)

        with self.subTest("large packet"):
            data = {'cmd': 'Ping', 'extra': 123}
            for i in range(4): # We'll never forget you int()!
                data["key" + str(i)] = i
            await self.ping(data)
        
        with self.subTest("larger packet"):
            data = {'cmd': 'Ping', 'extra': 123}
            for i in range(2000):
                data["key" + str(i)] = i
            await self.ping(data)
        
        with self.subTest("largest packet"):
            data = {'cmd': 'Ping', 'extra': 123}
            for i in range(42069):
                data["key" + str(i)] = i
            await self.ping(data)


def run_tests():
    global test_network
    test_network = True
    unittest.main(verbosity=9, warnings="error", failfast=True)

if __name__ == '__main__':
    run_tests()
