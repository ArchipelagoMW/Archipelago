import math
from typing import Any, Callable
from typing_extensions import override
from uuid import uuid4

from werkzeug.routing import BaseConverter

from . import TestBase


class TestSUUID(TestBase):
    converter: BaseConverter
    filter: Callable[[Any], str]

    @override
    def setUp(self) -> None:
        from werkzeug.routing import Map

        super().setUp()
        self.converter = self.app.url_map.converters["suuid"](Map())
        self.filter = self.app.jinja_env.filters["suuid"]  # type: ignore  # defines how we use it, not what it can be

    def test_is_reversible(self) -> None:
        u = uuid4()
        self.assertEqual(u, self.converter.to_python(self.converter.to_url(u)))
        s = "A" * 22  # uuid with all zeros
        self.assertEqual(s, self.converter.to_url(self.converter.to_python(s)))

    def test_uuid_length(self) -> None:
        with self.assertRaises(ValueError):
            self.converter.to_python("AAAA")

    def test_padding(self) -> None:
        self.converter.to_python("A" * 22)  # check that the correct value works
        with self.assertRaises(ValueError):
            self.converter.to_python("A" * 22 + "==")  # converter should not allow padding

    def test_empty(self) -> None:
        with self.assertRaises(ValueError):
            self.converter.to_python("")

    def test_stray_equal_signs(self) -> None:
        self.converter.to_python("A" * 22)  # check that the correct value works
        with self.assertRaises(ValueError):
            self.converter.to_python("A" * 22 + "==" + "AA")  # the "==AA" should not be ignored, but error out
        with self.assertRaises(ValueError):
            self.converter.to_python("A" * 20 + "==" + "AA")  # the final "A"s should not be appended to the first "A"s

    def test_stray_whitespace(self) -> None:
        s = "A" * 22
        self.converter.to_python(s)  # check that the correct value works
        for char in " \t\r\n\v":
            for pos in (0, 11, 22):
                with self.subTest(char=char, pos=pos):
                    s_with_whitespace = s[0:pos] + char * 4 + s[pos:]  # insert 4 to make padding correct
                    # check that the constructed s_with_whitespace is correct
                    self.assertEqual(len(s_with_whitespace), len(s) + 4)
                    self.assertEqual(s_with_whitespace[pos], char)
                    # s_with_whitespace should be invalid as SUUID
                    with self.assertRaises(ValueError):
                        self.converter.to_python(s_with_whitespace)

    def test_filter_returns_valid_string(self) -> None:
        u = uuid4()
        s = self.filter(u)
        self.assertIsInstance(s, str)
        self.assertNotIn("=", s)
        self.assertEqual(len(s), math.ceil(len(u.bytes) * 4 / 3))

    def test_filter_is_same_as_converter(self) -> None:
        u = uuid4()
        self.assertEqual(self.filter(u), self.converter.to_url(u))

    def test_filter_bad_type(self) -> None:
        with self.assertRaises(Exception):  # currently the type is not checked directly, so any exception is valid
            self.filter(None)
