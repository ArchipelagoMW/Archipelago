import ctypes

# ctypes.wintypes is available on linux? might not be in older versions
# so not touching for now
# various Mock that allows the doc to be build on darwin/linux
try:
    import ctypes.wintypes
except ValueError:
    from unittest.mock import Mock

    ctypes.wintypes = Mock()
    ctypes.wintypes.MAX_PATH = 1
    ctypes.WinDLL = Mock()

# Allows docs to be built with ci tools that run on linux
try:
    getattr(ctypes, "WinDLL")
except AttributeError:
    class MockObject:
        def __init__(self, *args, **kwargs):
            return

        def __call__(self, *args, **kwargs):
            return self

        def __getattr__(self, item):
            return self

    ctypes.Windll = MockObject()
