import unittest

from Utils import DaemonThreadPoolExecutor


class DaemonThreadPoolExecutorTest(unittest.TestCase):
    def test_is_daemon(self) -> None:
        def run() -> None:
            pass

        with DaemonThreadPoolExecutor(1) as executor:
            executor.submit(run)

            self.assertTrue(next(iter(executor._threads)).daemon)
