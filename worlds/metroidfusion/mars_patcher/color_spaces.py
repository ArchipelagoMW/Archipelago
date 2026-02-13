import math
from enum import Enum
from typing import Any


class RgbBitSize(Enum):
    Rgb5 = 1
    Rgb8 = 2


class RgbColor:
    """Color represented as RGB using 5 or 8 bits per channel."""

    FACTOR = 255.0

    def __init__(self, R: int, G: int, B: int, bit_size: RgbBitSize):
        if bit_size == RgbBitSize.Rgb5:
            R <<= 3
            G <<= 3
            B <<= 3
        elif bit_size == RgbBitSize.Rgb8:
            self.red = R
            self.green = G
            self.blue = B
        else:
            raise ValueError(bit_size)
        self.red = R
        self.green = G
        self.blue = B

    @classmethod
    def from_rgb(cls, rgb: int, bit_size: RgbBitSize) -> "RgbColor":
        if bit_size == RgbBitSize.Rgb5:
            r = (rgb & 0x1F) << 3
            g = (rgb & 0x3E0) >> 2
            b = (rgb & 0x7C00) >> 7
        elif bit_size == RgbBitSize.Rgb8:
            r = (rgb >> 16) & 0xFF
            g = (rgb >> 8) & 0xFF
            b = rgb & 0xFF
        else:
            raise ValueError(bit_size)
        return RgbColor(r, g, b, RgbBitSize.Rgb8)

    def __str__(self) -> str:
        return self.hex_15()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, RgbColor):
            return self.rgb_24() == other.rgb_24()
        return False

    def __hash__(self) -> int:
        return self.rgb_24()

    def hsv(self) -> "HsvColor":
        r = self.r_fraction()
        g = self.g_fraction()
        b = self.b_fraction()
        channels = [r, g, b]
        channels.sort()

        # Get value
        c_min = channels[0]
        c_max = channels[2]
        v = c_max

        # Get hue
        c_range = c_max - c_min
        if c_range == 0:
            h = 0.0
        else:
            if c_max == r:
                h = 60 * ((g - b) / c_range)
            elif c_max == g:
                h = 60 * ((b - r) / c_range + 2)
            elif c_max == b:
                h = 60 * ((r - g) / c_range + 4)
            # Check if negative
            if h < 0:
                h += 360

        # Get saturation
        if v == 0:
            s = 0.0
        else:
            s = c_range / v

        return HsvColor(h, s, v)

    def oklab(self) -> "OklabColor":
        # Convert to linear RGB
        rl = self.srgb_to_linear(self.r_fraction())
        gl = self.srgb_to_linear(self.g_fraction())
        bl = self.srgb_to_linear(self.b_fraction())

        # Convert to LMS
        lg = 0.4122214708 * rl + 0.5363325363 * gl + 0.0514459929 * bl
        md = 0.2119034982 * rl + 0.6806995451 * gl + 0.1073969566 * bl
        st = 0.0883024619 * rl + 0.2817188376 * gl + 0.6299787005 * bl

        lg = lg ** (1 / 3)
        md = md ** (1 / 3)
        st = st ** (1 / 3)

        return OklabColor(
            0.2104542553 * lg + 0.7936177850 * md - 0.0040720468 * st,
            1.9779984951 * lg - 2.4285922050 * md + 0.4505937099 * st,
            0.0259040371 * lg + 0.7827717662 * md - 0.8086757660 * st,
        )

    def luma(self) -> float:
        return 0.299 * self.red + 0.587 * self.green + 0.114 * self.blue

    def r_5(self) -> int:
        return self.red >> 3

    def g_5(self) -> int:
        return self.green >> 3

    def b_5(self) -> int:
        return self.blue >> 3

    def rgb_15(self) -> int:
        return (self.b_5() << 10) | (self.g_5() << 5) | self.r_5()

    def rgb_24(self) -> int:
        return (self.blue << 16) | (self.green << 8) | self.red

    def hex_15(self) -> str:
        return f"{self.rgb_15():04X}"

    def r_fraction(self) -> float:
        return self.red / self.FACTOR

    def g_fraction(self) -> float:
        return self.green / self.FACTOR

    def b_fraction(self) -> float:
        return self.blue / self.FACTOR

    @classmethod
    def black(cls) -> "RgbColor":
        return RgbColor.from_rgb(0, RgbBitSize.Rgb8)

    @classmethod
    def white_5(cls) -> "RgbColor":
        return RgbColor.from_rgb(0x7FFF, RgbBitSize.Rgb5)

    @staticmethod
    def srgb_to_linear(value: float) -> float:
        if value > 0.04045:
            return math.pow((value + 0.055) / 1.055, 2.4)
        return value / 12.92


class HsvColor:
    """
    Color represented as HSV, where 0 <= hue <= 360,
    0 <= saturation <= 1, and 0 <= value <= 1.
    See https://en.wikipedia.org/wiki/HSL_and_HSV
    """

    def __init__(self, hue: float, saturation: float, value: float):
        self.hue = hue
        self.saturation = saturation
        self.value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, HsvColor):
            return (
                self.hue == other.hue
                and self.saturation == other.saturation
                and self.value == other.value
            )
        return False

    def __hash__(self) -> int:
        return hash(self.hue) ^ hash(self.saturation) ^ hash(self.value)

    def rgb(self) -> RgbColor:
        c = self.value * self.saturation
        hp = self.hue / 60
        x = c * (1 - abs(hp % 2 - 1))

        if hp < 1:
            rgb = (c, x, 0.0)
        elif hp < 2:
            rgb = (x, c, 0.0)
        elif hp < 3:
            rgb = (0.0, c, x)
        elif hp < 4:
            rgb = (0.0, x, c)
        elif hp < 5:
            rgb = (x, 0.0, c)
        else:
            rgb = (c, 0.0, x)

        m = self.value - c
        factor = RgbColor.FACTOR
        r = round((rgb[0] + m) * factor)
        g = round((rgb[1] + m) * factor)
        b = round((rgb[2] + m) * factor)
        return RgbColor(r, g, b, RgbBitSize.Rgb8)


class OklabColor:
    """
    Color represented as Oklab, where 0.0 <= L <= 1.0,
    and A and B are typically between -0.4 and 0.4.
    See https://bottosson.github.io/posts/oklab/
    """

    def __init__(self, L: float, A: float, B: float):
        self.l_star = L
        self.a_star = A
        self.b_star = B

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, OklabColor):
            return (
                self.l_star == other.l_star
                and self.a_star == other.a_star
                and self.b_star == other.b_star
            )
        return False

    def __hash__(self) -> int:
        return hash(self.l_star) ^ hash(self.a_star) ^ hash(self.b_star)

    def rgb(self) -> RgbColor:
        # Convert to LMS
        lg = self.l_star + 0.3963377774 * self.a_star + 0.2158037573 * self.b_star
        md = self.l_star - 0.1055613458 * self.a_star - 0.0638541728 * self.b_star
        st = self.l_star - 0.0894841775 * self.a_star - 1.2914855480 * self.b_star

        lg = lg**3
        md = md**3
        st = st**3

        # Convert to linear RGB
        rl = +4.0767416621 * lg - 3.3077115913 * md + 0.2309699292 * st
        gl = -1.2684380046 * lg + 2.6097574011 * md - 0.3413193965 * st
        bl = -0.0041960863 * lg - 0.7034186147 * md + 1.7076147010 * st

        # Convert to sRGB
        rf = self.linear_to_srgb(rl)
        gf = self.linear_to_srgb(gl)
        bf = self.linear_to_srgb(bl)

        r = int(round(rf * 255))
        g = int(round(gf * 255))
        b = int(round(bf * 255))

        return RgbColor(
            max(0, min(r, 255)), max(0, min(g, 255)), max(0, min(b, 255)), RgbBitSize.Rgb8
        )

    def hue(self) -> float:
        """Gets the hue measured in radians. Ranges from -pi to pi."""
        return math.atan2(self.b_star, self.a_star)

    def chroma(self) -> float:
        """
        The intensity or purity of a color, i.e. how far it is from a
        neutral gray of the same lightness."""
        return math.sqrt(self.a_star * self.a_star + self.b_star * self.b_star)

    def shift_hue(self, shift: float) -> None:
        """Shifts hue by the provided amount, measured in radians."""
        # Get hue in range 0 to 2pi
        hue = self.hue() + math.pi
        hue = (hue + shift) % (2 * math.pi)
        # Put hue back in range -pi to pi
        hue -= math.pi
        # Get new A and B values
        chroma = self.chroma()
        self.a_star = chroma * math.cos(hue)
        self.b_star = chroma * math.sin(hue)

    @staticmethod
    def linear_to_srgb(value: float) -> float:
        if value > 0.0031308:
            return 1.055 * math.pow(value, 1.0 / 2.4) - 0.055
        return value * 12.92
