import pkgutil
from . import LADXTestBase
from ..LADXR.utils import formatText

lines = pkgutil.get_data(__name__, "../LADXR/patches/marin.txt").splitlines(keepends=True)
while lines and lines[-1].strip() == b'':
    lines.pop(-1)

class TestMarinText(LADXTestBase):
    def test_not_too_long(self):
        for line in lines:
            formatted = formatText(line.strip().decode("unicode_escape"))
            # 359 isn't a hard limit but its our longest one that works and we really don't need to go longer
            self.assertTrue(len(formatted) <= 359, f"{len(formatted)}: {line}")
