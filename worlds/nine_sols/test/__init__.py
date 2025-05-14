import os
import sys

path = os.path.dirname(__file__)
path = os.path.join(path, 'shared_static_logic')
if path not in sys.path:
    sys.path.append(path)
