import math
import random

from .color_spaces import HsvColor, OklabColor, RgbBitSize, RgbColor
from .rom import Rom

HUE_VARIATION_RANGE = 180.0
"""The maximum range that hue can be additionally rotated."""


class SineWave:
    STEP = (2 * math.pi) / 16

    def __init__(self, amplitude: float, frequency: float, phase: float):
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase

    @staticmethod
    def generate(max_range: float) -> "SineWave":
        """
        Generates a random sine wave of the form
            y = amplitude * sin(frequency * x + phase)
        where
            0 <= amplitude <= 1
            1/4 <= frequency <= 1
            x increases in steps of 1/16 of a cycle
            0 <= phase <= 2pi (one cycle)
        """
        assert 0 <= max_range <= 1
        # Prefer amplitudes closer to the max, otherwise the variation is often too subtle
        amplitude = random.uniform(max_range / 2, max_range)
        frequency = random.uniform(0.25, 1)
        phase = random.uniform(0, 2 * math.pi)
        return SineWave(amplitude, frequency, phase)

    def calculate_variation(self, x: int) -> float:
        assert 0 <= x < 16
        return self.amplitude * math.sin(self.frequency * x * self.STEP + self.phase)


class ColorChange:
    def __init__(self, hue_shift: float, hue_var: SineWave | None):
        self.hue_shift = hue_shift
        self.hue_var = hue_var

    def _get_hue_shift(self, index: int) -> float:
        shift = self.hue_shift
        if self.hue_var is not None:
            factor = HUE_VARIATION_RANGE / 2
            shift += self.hue_var.calculate_variation(index) * factor
        return shift

    def change_hsv(self, hsv: HsvColor, index: int) -> HsvColor:
        shift = self._get_hue_shift(index)
        hsv.hue = (hsv.hue + shift) % 360
        return hsv

    def change_oklab(self, lab: OklabColor, index: int) -> OklabColor:
        shift = self._get_hue_shift(index)
        # Convert hue shift to radians
        shift *= math.pi / 180
        lab.shift_hue(shift)
        return lab


class Palette:
    def __init__(self, rows: int, rom: Rom, addr: int):
        assert rows >= 1
        self.colors: list[RgbColor] = []
        for i in range(rows * 16):
            rgb = rom.read_16(addr + i * 2)
            color = RgbColor.from_rgb(rgb, RgbBitSize.Rgb5)
            self.colors.append(color)

    def __getitem__(self, key: int) -> RgbColor:
        return self.colors[key]

    def rows(self) -> int:
        return len(self.colors) // 16

    def byte_data(self) -> bytes:
        arr = bytearray()
        for color in self.colors:
            val = color.rgb_15()
            arr.append(val & 0xFF)
            arr.append(val >> 8)
        return bytes(arr)

    def write(self, rom: Rom, addr: int) -> None:
        data = self.byte_data()
        rom.write_bytes(addr, data)

    def change_colors_hsv(self, change: ColorChange, excluded_rows: set[int]) -> None:
        """Apply a color change using HSV color space."""
        black = RgbColor.black()
        white = RgbColor.white_5()
        for row in range(self.rows()):
            if row in excluded_rows:
                continue
            offset = row * 16
            for i in range(16):
                # Skip black and white
                rgb = self.colors[offset + i]
                if rgb == black or rgb == white:
                    continue
                orig_luma = rgb.luma()
                hsv = change.change_hsv(rgb.hsv(), i)
                rgb = hsv.rgb()
                # Rescale luma
                luma_ratio = orig_luma / rgb.luma()
                rgb.red = min(int(rgb.red * luma_ratio), 255)
                rgb.green = min(int(rgb.green * luma_ratio), 255)
                rgb.blue = min(int(rgb.blue * luma_ratio), 255)
                self.colors[offset + i] = rgb

    def change_colors_oklab(self, change: ColorChange, excluded_rows: set[int]) -> None:
        """Apply a color change using Oklab color space."""
        # Convert shift to radians
        for row in range(self.rows()):
            if row in excluded_rows:
                continue
            offset = row * 16
            for i in range(16):
                rgb = self.colors[offset + i]
                lab = change.change_oklab(rgb.oklab(), i)
                self.colors[offset + i] = lab.rgb()
