"""sys.path bootstrap for pure-Python dependencies vendored in ``worlds/cvaos/vendor``.

Works both as a loose world folder and inside a zipped .apworld: zipimport accepts
sys.path entries that point inside a zip archive, as long as the path is normalized
(no ``..`` segments).
"""

import os
import sys

_VENDOR_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))


def ensure_vendor_on_sys_path() -> None:
    """Make the vendored packages importable (idempotent).

    The vendor dir is appended rather than prepended so that packages installed in the
    environment win; the vendored copies are a fallback for frozen Archipelago
    installs, which cannot pip-install anything.
    """
    if _VENDOR_DIR not in sys.path:
        sys.path.append(_VENDOR_DIR)
